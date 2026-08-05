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
action that resolved it, and the parity test would fail. Restricted to the kinds the translator
handles, the recorded order IS timestamp order (verified against a real log), so `_OrderedStream`
restores it -- see its docstring for the assumption this rests on and the display latency it costs.

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
    """Restores transcript order on the live hook event stream, with a one-event lookahead.

    Inspect delivers an event once it stops being `pending`, so a `ToolEvent` arrives AFTER the
    `StoreEvent`s produced inside it, carrying an earlier timestamp. Buffered events are therefore
    released only when an event with a strictly later timestamp arrives, in timestamp order.

    **The assumption:** a late arrival's timestamp is always earlier than everything still
    buffered -- true for a sequential agent loop, where a pending tool or generate always completes
    before the next one starts. (A tool that itself called a model and outlived a later completed
    call would break it. Nothing in this harness does that.)

    **The cost:** an event is written one handled-event later than it arrived. In the solver's
    Model -> Tool -> Store -> Model loop that means the day frame, mail and decision lines of a beat
    land when the next turn's generate returns, so the page can trail the run by one turn.

    Only the kinds the translator handles pass through here (`HANDLED_EVENT_TYPES`): an unhandled
    event of the tool's own span arrives BEFORE the tool event, so letting one trigger a release
    would emit the effects ahead of their cause -- the exact inversion this class exists to undo.
    """

    def __init__(self) -> None:
        self._buffer: list[Any] = []

    def push(self, event: Any) -> list[Any]:
        """Buffer *event*; return the events now known to be in order (possibly none)."""
        if not isinstance(event, HANDLED_EVENT_TYPES):
            return []
        timestamp = event.timestamp
        ready = [held for held in self._buffer if held.timestamp < timestamp]
        self._buffer = [held for held in self._buffer if held.timestamp >= timestamp]
        self._buffer.append(event)
        # Stable, so simultaneous events keep their arrival order.
        return sorted(ready, key=lambda held: held.timestamp)

    def drain(self) -> list[Any]:
        """Everything still buffered, in order: the stream ended, so nothing earlier can arrive."""
        held, self._buffer = sorted(self._buffer, key=lambda event: event.timestamp), []
        return held


class _FeedFile:
    """One sample's append-only feed file. Whole lines, flushed now, fsynced at day boundaries."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self._file = path.open("a", encoding="utf-8")
        # No day has been written yet, so the first batch always fsyncs -- which is what makes the
        # head of a feed durable even if the run dies during day 0.
        self._day: int | None = None

    def write(self, feed_events: Iterable[FeedEvent], *, day: int) -> None:
        """Append and flush each line, then fsync if *day* is not the day last written.

        *day* is the translator's current day, not any event's own `day` field: mail carries the
        day it was SENT (backlog mail arrives later stamped earlier), so an event-derived boundary
        would both fsync spuriously and walk backwards.
        """
        for event in feed_events:
            self._file.write(dump_feed_line(event) + "\n")
            self._file.flush()
        if day != self._day:
            self._day = day
            os.fsync(self._file.fileno())

    def close(self) -> None:
        try:
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

    def finish(self, status: str) -> None:
        """Translate whatever is still buffered, then close the feed with its `episode_end`."""
        for ordered in self._stream.drain():
            self._write(self._translator.handle(ordered))
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
            # A sample cancelled hard enough to skip `on_sample_end` leaves an open file. Its feed
            # simply ends without an `episode_end` line, which the page reads as "still running";
            # inventing a status for a sample nobody reported on would be worse.
            for sample_id, feed in list(self._feeds.items()):
                if feed.eval_id == data.eval_id:
                    self._feeds.pop(sample_id, None)
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
