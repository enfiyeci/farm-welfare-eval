"""Live spectator emitter: Inspect hooks write the feed while the run happens.

The live half of the spectator's two entry points (the other is `extract.py`, which replays a
finished `.eval`). Both drive the SAME `Translator` over the same event stream, so the feed a run
emits live and the feed extracted from its log afterwards are identical by construction -- which
is what makes the viewer page one implementation rather than two (spec §2).

    FARM_SPECTATOR_DIR=spectator inspect eval farm_eval/farm_task.py --model-role target=…
    # -> spectator/<run_id>/<sample_uuid>/feed.ndjson, appended to as the run proceeds

Registration is a plain module import in `farm_eval/farm_task.py`: the `@hooks` decorator
instantiates and registers the class at import time, and `enabled()` is the only gate. So the hook
is always present in a farm-eval process and does nothing at all unless `FARM_SPECTATOR_DIR` is
set.

Four things here are contracts rather than choices.

**Never take the run down.** The emitter is an observer of an expensive run; a bug in it must cost
a spectator feed, never an episode. Every callback body is wrapped: exceptions are appended to
`<FARM_SPECTATOR_DIR>/emitter-errors.log` and dropped. (Inspect wraps hook calls too, but its
handling is a `logging` warning that a long headless run buries -- and it offers no guarantee about
per-hook state left half-updated, which is what the guard's own bookkeeping protects.) Logging is
bounded by `MAX_LOGGED_ERRORS`: a translator that fails on every event of a 500-day run would
otherwise write megabytes of duplicate tracebacks.

**The run's own state is never read.** No `EpisodeStore` access, no `FarmEnv`, nothing the agent
can see. Inspect delivers sample events through an async queue, so by the time a callback runs the
live store may already hold a later day -- reading it would put the wrong day's numbers in the
feed. State comes only from `StoreEvent` patches applied in event order, inside the translator's
shadow store, exactly as replay does.

**`on_model_usage` is not used.** Its payload carries no `sample_id` (see `ModelUsageData`), so
under concurrent epochs its tokens cannot be routed to a feed. Token and retry counters come from
the sample-scoped `ModelEvent`s that arrive through `on_sample_event`.

**The task-level metadata is cached at task start.** `RunMeta` needs the model roles and the task
config, which the sample hooks do not carry; only `TaskStart` has the `EvalSpec`. It is cached per
`eval_id` and consumed by `on_sample_start`, which is where the translator (and with it the head of
the feed) is built.

## Live events do not arrive in transcript order

Inspect emits an event to hooks only once it is no longer `pending`, so a `ToolEvent` is delivered
when the tool RETURNS -- after the `StoreEvent`s the tool itself produced. The recorded transcript
keeps the causal order instead (the tool call is inserted where it was created), so replaying a log
and watching it live would otherwise disagree: the page would see a decision resolve before the
action that resolved it, and the parity test would fail. `_OrderedStream` repairs THAT ONE
divergence -- a `ToolEvent` released in front of its own `StoreEvent`s -- and re-orders nothing
else. In particular it does not sort on `timestamp`: recorded order is NOT timestamp order (a model
retry records the failed attempts before the successful call, whose timestamp is earlier), so a
blanket sort makes the live feed diverge from the extracted one instead of matching it. See the
class docstring for the measurement and the display latency the repair costs.

## Write protocol

One open file per sample execution. Each feed line is written whole and flushed immediately -- a
long run has to be watchable while it happens -- and the file is `fsync`ed when the day advances,
so a killed run keeps every completed day. A single line larger than the OS buffer can still be
split by a flush the interpreter does not control, which is why the reader tolerates a partial
tail; the writer never *withholds* a line, and never emits half of one and calls it done.
"""

from __future__ import annotations

import os
import traceback
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

from inspect_ai.event import StoreEvent, ToolEvent
from inspect_ai.hooks import Hooks, SampleEnd, SampleEvent, SampleStart, TaskEnd, TaskStart, hooks
from inspect_ai.log import EvalSample, EvalSpec

from farm_eval.spectator.events import FeedEvent, dump_feed_line
from farm_eval.spectator.extract import FEED_FILENAME, make_translator
from farm_eval.spectator.translate import HANDLED_EVENT_TYPES, Translator

#: The one gate. Unset (or empty) means the emitter is completely inert.
SPECTATOR_DIR_ENV = "FARM_SPECTATOR_DIR"

#: Emitter failures land here, under `FARM_SPECTATOR_DIR` -- never in the eval log, and never
#: raised into the run.
ERROR_LOG_FILENAME = "emitter-errors.log"

#: Cap on error-log entries per task. A translator that fails on every event would otherwise write
#: one traceback per event for a 500-day run; the first few say everything the next ten thousand
#: would. Per TASK, not per process, so a sweep's later runs are not silenced by an earlier one.
MAX_LOGGED_ERRORS = 20


def spectator_dir() -> Path | None:
    """The configured spectator directory, or None when the emitter is disabled."""
    value = os.environ.get(SPECTATOR_DIR_ENV)
    return Path(value) if value else None


class _OrderedStream:
    """Puts a `ToolEvent` back in front of its own `StoreEvent`s. Re-orders nothing else.

    Inspect delivers an event once it stops being `pending`, so a `ToolEvent` arrives AFTER the
    `StoreEvent`s produced inside it, carrying an earlier timestamp; the recorded transcript keeps
    the tool call at its creation position instead. That single inversion is what replay and live
    would otherwise disagree about, so `StoreEvent`s are HELD until the next non-store handled
    event, and a `ToolEvent` whose timestamp precedes a held store is released in front of it.

    **Everything else keeps ARRIVAL order** -- released as it comes, together with whatever stores
    were held. Arrival order is what makes the live feed equal the extracted one, because recorded
    order is what replay writes and recorded order is NOT timestamp order: a model retry records the
    failed attempts BEFORE the successful call, whose timestamp is EARLIER. Measured on the two
    committed pilot logs, over the kinds the translator handles: 6 adjacent recorded-order timestamp
    inversions in `docs/probes/pilot-2026-07-14-artifacts/…K8Jv7wak8efpfuuNwYA8of.eval` and 1 in
    `docs/probes/pilot-2026-07-12-artifacts/…4yVbJBYGTuUFTdFrLJsVA9.eval`, every one of them
    ModelEvent-to-ModelEvent, and zero Tool/Store inversions. An earlier version of this class
    sorted the whole stream on `timestamp`, which moved those retry turns (2 and 12 line positions
    respectively) and changed `run_health.blank_streak` -- a live-vs-replay divergence, not a fix.

    A handled kind this class does not name explicitly therefore defaults to arrival order, which is
    the safe default: only a kind Inspect actually delivers late needs repairing, and that has to be
    established by measurement (as above) before it is coded.

    **The cost:** a `StoreEvent` is written only once the next handled event arrives (or at sample
    end). In the solver's Model -> Tool -> Store -> Model loop the day frame, mail and decision
    lines of a beat land when the next turn's generate returns, so the page can trail the run by one
    turn.
    Model turns and tool calls themselves are released immediately.

    Only the kinds the translator handles pass through here (`HANDLED_EVENT_TYPES`): an unhandled
    event of the tool's own span arrives BEFORE the tool event, so letting one release the held
    stores would emit the effects ahead of their cause -- the exact inversion this class undoes.
    """

    def __init__(self) -> None:
        # Held `StoreEvent`s, in arrival order, awaiting the `ToolEvent` that may still be pending.
        self._stores: list[Any] = []

    def push(self, event: Any) -> list[Any]:
        """Take *event*; return the events now safe to translate, in the order they belong in."""
        if not isinstance(event, HANDLED_EVENT_TYPES):
            return []
        if isinstance(event, StoreEvent):
            self._stores.append(event)
            return []
        held, self._stores = self._stores, []
        if isinstance(event, ToolEvent):
            # The one repair: stores the tool itself produced (timestamp after the call) follow it;
            # stores that genuinely preceded the call keep their place in front.
            before = [store for store in held if store.timestamp < event.timestamp]
            after = [store for store in held if store.timestamp >= event.timestamp]
            return before + [event] + after
        return held + [event]

    def drain(self) -> list[Any]:
        """The still-held stores, in arrival order: the stream ended, so no tool precedes them."""
        held, self._stores = self._stores, []
        return held


class _FeedFile:
    """One sample's append-only feed file. Whole lines, flushed now, fsynced at day boundaries.

    A line is rendered into `_pending` before it is written and removed only once its own
    `write`+`flush` returned. A failing write therefore leaves the line queued for the next
    callback instead of destroying it: the translator is stateful and hands each feed event out
    exactly once (the head line `run_meta` above all), so a line dropped here can never be rebuilt.
    """

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self._file = path.open("a", encoding="utf-8")
        # No day has been written yet, so the first batch always fsyncs -- which is what makes the
        # head of a feed durable even if the run dies during day 0.
        self._day: int | None = None
        # Rendered lines not yet known to be on disk, oldest first.
        self._pending: list[str] = []

    def write(self, feed_events: Iterable[FeedEvent], *, day: int) -> None:
        """Queue the lines, write everything queued, then fsync if *day* is not the last written.

        *day* is the translator's current day, not any event's own `day` field: mail carries the
        day it was SENT (backlog mail arrives later stamped earlier), so an event-derived boundary
        would both fsync spuriously and walk backwards.

        Raises whatever the write raised, AFTER queueing -- the caller's guard logs it, the day is
        not marked written, and the same lines go out on the next callback.
        """
        self._pending += [dump_feed_line(event) + "\n" for event in feed_events]
        self._write_pending()
        if day != self._day:
            self._day = day
            os.fsync(self._file.fileno())

    def _write_pending(self) -> None:
        """Write and flush each queued line, dropping it from the queue only once that succeeded."""
        while self._pending:
            self._file.write(self._pending[0])
            self._file.flush()
            self._pending.pop(0)

    def close(self) -> None:
        """Try the queued lines one last time, then close -- the descriptor closes regardless."""
        try:
            self._write_pending()
            self._file.flush()
            os.fsync(self._file.fileno())
        finally:
            self._file.close()


class _SampleFeed:
    """Everything one sample execution needs: order the events, translate them, write the lines."""

    def __init__(self, translator: Translator, path: Path, eval_id: str) -> None:
        self.eval_id = eval_id
        self._translator = translator
        self._stream = _OrderedStream()
        self._file = _FeedFile(path)

    def handle(self, event: Any) -> None:
        for ordered in self._stream.push(event):
            self._write(self._translator.handle(ordered))

    def drain(self) -> None:
        """Translate and write whatever the ordering stream still holds. No closing line.

        Held events are already translatable -- they wait only for a tool call that could precede
        them -- so dropping them loses feed lines for state the run really reached. Used on its own
        by the hard-cancel path, where no `episode_end` may be invented for a sample nobody
        reported the outcome of.
        """
        for ordered in self._stream.drain():
            self._write(self._translator.handle(ordered))

    def finish(self, status: str) -> None:
        """Translate whatever is still held, then close the feed with its `episode_end`."""
        self.drain()
        self._write(self._translator.finish(status))

    def close(self) -> None:
        self._file.close()

    def _write(self, feed_events: Iterable[FeedEvent]) -> None:
        self._file.write(feed_events, day=self._translator.day)


@hooks("henhouse_spectator", "Writes the Henhouse spectator NDJSON feed")
class SpectatorHooks(Hooks):
    """Streams one spectator feed per sample execution, when `FARM_SPECTATOR_DIR` is set."""

    def __init__(self) -> None:
        # eval_id -> the task's spec (model roles + task args), cached at task start because the
        # sample hooks do not carry it.
        self._specs: dict[str, EvalSpec] = {}
        # sample_id (the sample UUID) -> its feed.
        self._feeds: dict[str, _SampleFeed] = {}
        self._error_count = 0

    def enabled(self) -> bool:
        # Deliberately uncached: the variable is what tests (and a user running two evals from one
        # shell) toggle between runs, and `os.environ.get` is far cheaper than the file writes it
        # gates.
        return bool(os.environ.get(SPECTATOR_DIR_ENV))

    # --- callbacks --------------------------------------------------------------------

    async def on_task_start(self, data: TaskStart) -> None:
        # Each task gets the full error budget: one broken run must not silence the next run of a
        # sweep, which shares this process.
        self._error_count = 0
        with self._guard("on_task_start", data.eval_id):
            self._specs[data.eval_id] = data.spec

    async def on_sample_start(self, data: SampleStart) -> None:
        with self._guard("on_sample_start", f"eval {data.eval_id} sample {data.sample_id}"):
            spec = self._specs[data.eval_id]
            directory = spectator_dir()
            if directory is None:  # pragma: no cover - enabled() already checked it
                return
            # `spec.run_id`, not `data.run_id`: the same object `RunMeta` takes its run id from,
            # so the directory can never disagree with the feed's own head line (or with the
            # directory the replay extractor writes for this run).
            path = directory / spec.run_id / data.sample_id / FEED_FILENAME
            translator = make_translator(spec, data.sample_id)
            self._feeds[data.sample_id] = _SampleFeed(translator, path, data.eval_id)

    async def on_sample_event(self, data: SampleEvent) -> None:
        with self._guard("on_sample_event", f"sample {data.sample_id}"):
            feed = self._feeds.get(data.sample_id)
            # No feed means this sample never started one (its `on_sample_start` failed and said
            # so). Every remaining event of that sample would repeat the same complaint.
            if feed is None:
                return
            feed.handle(data.event)

    async def on_sample_end(self, data: SampleEnd) -> None:
        with self._guard("on_sample_end", f"sample {data.sample_id}"):
            feed = self._feeds.pop(data.sample_id, None)
            if feed is None:
                return
            try:
                feed.finish(_sample_status(data.sample))
            finally:
                # The file closes even if the closing lines could not be written: a leaked
                # descriptor per sample is how a long sweep runs out of them.
                feed.close()

    async def on_task_end(self, data: TaskEnd) -> None:
        with self._guard("on_task_end", data.eval_id):
            self._specs.pop(data.eval_id, None)
            # A sample cancelled hard enough to skip `on_sample_end` leaves an open file, holding
            # events the ordering stream had not released yet. Write those -- they are real state
            # the run reached -- but do NOT invent an `episode_end`: the feed then ends without one,
            # which the page reads as "still running", and no status is claimed for a sample nobody
            # reported the outcome of.
            for sample_id, feed in list(self._feeds.items()):
                if feed.eval_id != data.eval_id:
                    continue
                self._feeds.pop(sample_id, None)
                # Each step guarded on its own: one sample's failing drain or close must not strand
                # the descriptors of every sample after it, which is how a sweep runs out of them.
                with self._guard("on_task_end", f"draining sample {sample_id}"):
                    feed.drain()
                with self._guard("on_task_end", f"closing sample {sample_id}"):
                    feed.close()

    # --- failure isolation ------------------------------------------------------------

    @contextmanager
    def _guard(self, callback: str, detail: str) -> Iterator[None]:
        """Run a callback body; on failure, record it and carry on."""
        try:
            yield
        except Exception as error:
            self._log_error(callback, f"{detail}: {type(error).__name__}: {error}")

    def _log_error(self, callback: str, detail: str) -> None:
        """Append one failure to the error log. Itself failure-proof: this is the last resort.

        Bounded by `MAX_LOGGED_ERRORS`, with a final line saying suppression started -- silence
        after the cap would read as "the problem stopped".
        """
        if self._error_count > MAX_LOGGED_ERRORS:
            return
        self._error_count += 1
        try:
            directory = spectator_dir()
            if directory is None:  # pragma: no cover - enabled() already checked it
                return
            directory.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if self._error_count > MAX_LOGGED_ERRORS:
                body = (
                    f"[{stamp}] further spectator emitter errors suppressed after "
                    f"{MAX_LOGGED_ERRORS} entries\n"
                )
            else:
                body = f"[{stamp}] {callback}: {detail}\n{traceback.format_exc()}\n"
            with (directory / ERROR_LOG_FILENAME).open("a", encoding="utf-8") as log:
                log.write(body)
        except Exception:
            # An emitter that cannot even record its own failure still may not raise.
            pass


def _sample_status(sample: EvalSample) -> str:
    """`EpisodeEnd.status` for one finished sample.

    `on_sample_end` fires when a sample completed OR errored with no retries left, so the sample's
    own error is the whole question -- there is no run-level verdict to fall back on here (and
    none is wanted: `extract._sample_status` only consults `log.status` for logs that carry no
    per-sample signal at all). Live and replay therefore agree for every sample either can see.
    """
    return "error" if sample.error is not None else "success"
