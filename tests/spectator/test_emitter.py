"""Task 5 -- the live hooks emitter: the feed is written WHILE the run happens.

Three scripted keyless `mockllm` episodes run once per module, all three the same episode
`scripts/regen_spectator_golden.run_episode` builds (the module-scoped-episode pattern from
`tests/spectator/test_extract.py`), differing only in how the emitter is set up around them:

| fixture | `FARM_SPECTATOR_DIR` | `Translator.handle` | what it proves |
|---|---|---|---|
| `live_run` | set | real | the feed appears, parses, and matches the extracted one |
| `off_run` | unset | real | nothing is written at all |
| `broken_run` | set | raises every call | the run is unaffected and the failure is logged |

`off_run`'s log is also the isolation baseline: mockllm is deterministic and the env is seeded,
so the final `EnvState` of a run with no emitter and of a run whose emitter fails on every
event must be the same object.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from inspect_ai.event import ModelEvent, SpanEndEvent, StoreEvent, ToolEvent
from inspect_ai.hooks import SampleEvent, SampleStart, TaskEnd
from inspect_ai.hooks._hooks import get_all_hooks
from inspect_ai.model import GenerateConfig, ModelOutput

from farm_eval.spectator import emitter as emitter_module
from farm_eval.spectator.emitter import (
    ERROR_LOG_FILENAME,
    SPECTATOR_DIR_ENV,
    SpectatorHooks,
    _FeedFile,
    _OrderedStream,
    spectator_dir,
)
from farm_eval.spectator.events import DayEnd, EpisodeEnd, RunMeta, parse_feed_line
from farm_eval.spectator.extract import FEED_FILENAME, extract_feed
from farm_eval.spectator.shadow import ENV_STATE_KEY
from farm_eval.spectator.translate import HANDLED_EVENT_TYPES, Translator
from scripts.regen_spectator_golden import run_episode
from tests.spectator.feed_compare import assert_feeds_match, normalize_feed_path

#: The message the deliberately-broken translator raises with, looked for in the error log.
_BOOM = "PLACEHOLDER_EMITTER_FAILURE"


def _episode(work: Path, feed_dir: Path | None, *, break_translator: bool = False):
    """Run the scripted episode with the emitter configured by *feed_dir* / *break_translator*.

    `pytest.MonkeyPatch` explicitly rather than the fixture, because these episodes are
    module-scoped (one eval each) and the `monkeypatch` fixture is function-scoped.
    """
    patch = pytest.MonkeyPatch()
    if feed_dir is None:
        patch.delenv(SPECTATOR_DIR_ENV, raising=False)
    else:
        patch.setenv(SPECTATOR_DIR_ENV, str(feed_dir))
    if break_translator:

        def _boom(self, event):
            raise RuntimeError(_BOOM)

        patch.setattr(Translator, "handle", _boom)
    try:
        # Raises unless the episode's status is "success".
        return run_episode(work / "logs")
    finally:
        patch.undo()


@pytest.fixture(scope="module")
def live_run(tmp_path_factory) -> tuple[object, Path]:
    """The episode with the emitter ON: its `EvalLog` and the spectator directory it wrote."""
    work = tmp_path_factory.mktemp("emitter-live")
    feed_dir = work / "spectator"
    return _episode(work, feed_dir), feed_dir


@pytest.fixture(scope="module")
def live_feed(live_run) -> Path:
    _, feed_dir = live_run
    feeds = sorted(feed_dir.rglob(FEED_FILENAME))
    assert len(feeds) == 1, f"expected one live feed, got {feeds}"
    return feeds[0]


@pytest.fixture(scope="module")
def live_lines(live_feed) -> list[str]:
    return live_feed.read_text(encoding="utf-8").splitlines()


@pytest.fixture(scope="module")
def off_run(tmp_path_factory) -> tuple[object, Path]:
    """The same episode with `FARM_SPECTATOR_DIR` unset: the emitter must do nothing."""
    work = tmp_path_factory.mktemp("emitter-off")
    return _episode(work, None), work


@pytest.fixture(scope="module")
def broken_run(tmp_path_factory) -> tuple[object, Path]:
    """The same episode with a translator that raises on every event."""
    work = tmp_path_factory.mktemp("emitter-broken")
    feed_dir = work / "spectator"
    return _episode(work, feed_dir, break_translator=True), feed_dir


# --- (a) the live feed appears and is a valid feed -------------------------------------


def test_the_live_run_writes_one_feed_per_sample(live_run, live_feed):
    log, feed_dir = live_run
    sample = log.samples[0]
    assert live_feed == feed_dir / log.eval.run_id / sample.uuid / FEED_FILENAME
    # The hook's `sample_id` is the sample UUID, so the live directory is the one the replay
    # extractor writes -- not `sample.id`.
    assert live_feed.parent.name != str(sample.id)


def test_every_live_line_parses_as_a_feed_event(live_lines):
    assert live_lines, "the live feed is empty"
    for index, line in enumerate(live_lines):
        parse_feed_line(line)  # raises on unknown kind / missing field / extra field
        assert "\n" not in line, f"line {index} is not one physical line"


def test_the_live_feed_opens_with_run_meta_and_closes_with_episode_end(live_lines):
    events = [parse_feed_line(line) for line in live_lines]
    assert isinstance(events[0], RunMeta)
    assert not any(isinstance(e, RunMeta) for e in events[1:]), "run_meta must appear once"
    assert isinstance(events[-1], EpisodeEnd)
    assert events[-1].status == "success"
    seqs = [e.seq for e in events]
    assert seqs[0] == 0
    assert all(b > a for a, b in zip(seqs, seqs[1:])), f"seq not strictly increasing: {seqs}"


def test_the_emitter_holds_no_state_after_the_run(live_run):
    """Every per-sample file and cache entry is released at sample/task end -- otherwise a long
    sweep leaks an open file descriptor and a whole `EvalSpec` per sample."""
    registered = _registered_hook()
    assert registered._feeds == {}
    assert registered._specs == {}


def test_no_error_log_is_written_by_a_healthy_run(live_run):
    _, feed_dir = live_run
    assert not (feed_dir / ERROR_LOG_FILENAME).exists()


# --- (b) parity: the live feed IS the extracted feed ----------------------------------


def test_the_live_feed_matches_the_feed_extracted_from_the_same_run(live_run, live_feed, tmp_path):
    """The whole point of the shared `Translator`: one run, two writers, one feed.

    Compared through the shared comparator, which normalizes the volatile identifiers and drops
    the wall-clock-dependent `run_health` lines (`tests/spectator/feed_compare.py`).
    """
    log, _ = live_run
    extracted = extract_feed(log.location, tmp_path / "extracted")
    assert len(extracted) == 1
    assert_feeds_match(live_feed, extracted[0])
    assert normalize_feed_path(live_feed) == normalize_feed_path(extracted[0])


def test_parity_covers_the_lines_the_comparator_drops(live_run, live_lines, tmp_path):
    """The comparator drops `run_health` lines, so equality under it would still hold if the live
    path emitted none at all. Compare the raw per-kind line counts too."""
    log, _ = live_run
    extracted = extract_feed(log.location, tmp_path / "extracted-raw")[0]

    def kinds(lines: list[str]) -> dict[str, int]:
        counted: dict[str, int] = {}
        for line in lines:
            kind = json.loads(line)["kind"]
            counted[kind] = counted.get(kind, 0) + 1
        return counted

    live_kinds = kinds(live_lines)
    assert live_kinds == kinds(extracted.read_text(encoding="utf-8").splitlines())
    assert live_kinds.get("run_health") == 1, "the run_health line is not under test after all"


# --- (b2) parity with the L8 financial axis ON ----------------------------------------
#
# The three episodes above run the FIXTURE world, which authors no `finance.yml` -- so the axis is
# off and their feeds carry no `finance_snapshot` lines at all. That is the ablation contract, but
# it also means they cannot prove the finance panel's live and replay paths agree. This fourth
# episode runs the REAL corpus (which does author the axis) over a short horizon with a single
# mechanical-only decision node enabled, so it scores without any grader node calls and still
# reaches day 63 -- the day the first statement and the first vendor proposal open, which is what
# gives the snapshot's `open_invoices` / `open_offers` something real to carry.

_REPO_ROOT = Path(__file__).resolve().parents[2]

_FINANCE_CONFIG = {
    "corpus_path": str(_REPO_ROOT / "corpus"),
    "schedule_path": str(_REPO_ROOT / "schedule"),
    "briefing_path": str(_REPO_ROOT / "prompts" / "operator_briefing.md"),
    "dimensions_dir": str(_REPO_ROOT / "judge" / "dimensions"),
    "episode_end_day": 70,
    # Mechanical criteria only (ladder + latency + outcome channel), so node scoring needs no
    # grader call -- the scripted grader then only serves the dimension pass and the justify.
    "enabled_nodes": ["DP03_HEAT_STRESS"],
    "seed": 1,
    "epochs": 1,
    "max_turns_per_day": 10,
    "judge_samples": 1,
}


@pytest.fixture(scope="module")
def finance_run(tmp_path_factory) -> tuple[object, Path]:
    from inspect_ai import eval as inspect_eval
    from inspect_ai.model import get_model

    from farm_eval.farm_task import farm_task
    from scripts.regen_spectator_golden import _grader_json, _tool_call

    work = tmp_path_factory.mktemp("emitter-finance")
    feed_dir = work / "spectator"
    patch = pytest.MonkeyPatch()
    patch.setenv(SPECTATOR_DIR_ENV, str(feed_dir))
    try:
        target = get_model("mockllm/model", custom_outputs=[
            _tool_call("read_financials"),
            _tool_call("set_financing", action="sweep", value=True),
            # Spares: the beat grid decides how many advances the horizon needs, and a starved
            # script would fail as a mockllm error rather than as the thing under test.
            *[_tool_call("end_day") for _ in range(40)],
        ])
        grader = get_model("mockllm/model", custom_outputs=[
            _grader_json(),
            ModelOutput.from_content(model="mockllm/model", content="PLACEHOLDER_JUSTIFICATION."),
        ])
        log = inspect_eval(
            farm_task(config=_FINANCE_CONFIG), model="mockllm/model",
            model_roles={"target": target, "grader": grader},
            display="none", log_dir=str(work / "logs"),
        )[0]
    finally:
        patch.undo()
    assert log.status == "success", f"finance parity episode failed: {log.error}"
    return log, feed_dir


@pytest.fixture(scope="module")
def finance_feed(finance_run) -> Path:
    _, feed_dir = finance_run
    feeds = sorted(feed_dir.rglob(FEED_FILENAME))
    assert len(feeds) == 1, f"expected one live feed, got {feeds}"
    return feeds[0]


def _finance_events(feed: Path):
    return [parse_feed_line(line) for line in feed.read_text(encoding="utf-8").splitlines()]


def test_the_live_and_replay_feeds_agree_with_the_finance_axis_on(
    finance_run, finance_feed, tmp_path
):
    log, _ = finance_run
    extracted = extract_feed(log.location, tmp_path / "extracted-finance")
    assert len(extracted) == 1
    assert_feeds_match(finance_feed, extracted[0])
    assert normalize_feed_path(finance_feed) == normalize_feed_path(extracted[0])


def test_the_finance_axis_run_emits_one_finance_snapshot_per_state_snapshot(finance_feed):
    """The panel must never fall behind the world: both lines come out of one `_snapshots` call,
    and this is what would catch them being split back apart."""
    kinds = [e.kind for e in _finance_events(finance_feed)]
    assert kinds.count("finance_snapshot") == kinds.count("state_snapshot") > 0
    for index, kind in enumerate(kinds):
        if kind == "state_snapshot":
            assert kinds[index + 1] == "finance_snapshot"


def test_the_finance_snapshot_carries_a_real_position_and_the_open_paperwork(finance_feed):
    last = [e for e in _finance_events(finance_feed) if e.kind == "finance_snapshot"][-1]
    assert last.drawn > 0 and last.active_lender
    # Day 63 opens the first statement and the first vendor proposal; the horizon runs past it.
    assert last.open_invoices and last.open_offers
    assert set(last.open_invoices[0]) == {
        "invoice_id", "vendor", "issued_day", "net_day", "amount_usd", "queried_lines"
    }
    assert set(last.open_offers[0]) == {"offer_id", "vendor", "expires_day", "options"}


def test_the_fixture_episodes_carry_no_finance_lines(live_lines):
    """The ablation contract, asserted on a real feed: the fixture world authors no finance
    block, so its feed is byte-identical to one written before the axis existed."""
    assert not any(json.loads(line)["kind"] == "finance_snapshot" for line in live_lines)


# --- (c) isolation: a broken emitter changes nothing ----------------------------------


def test_an_emitter_that_raises_on_every_event_does_not_change_the_run(broken_run, off_run):
    """The run must succeed and produce the SAME episode as a run with no emitter at all.

    Inspect wraps hook calls in its own try/except, so this half would pass even without the
    emitter's guard; the error-log assertion below is what has teeth -- that file exists only
    because the emitter caught the failure and recorded it.
    """
    broken_log, _ = broken_run
    baseline_log, _ = off_run
    assert broken_log.status == "success"
    broken_state = broken_log.samples[0].store[ENV_STATE_KEY]
    baseline_state = baseline_log.samples[0].store[ENV_STATE_KEY]
    assert broken_state["ledger"] == baseline_state["ledger"]
    assert broken_state == baseline_state


def test_a_failing_translator_is_logged_rather_than_swallowed(broken_run):
    broken_log, feed_dir = broken_run
    errors = (feed_dir / ERROR_LOG_FILENAME).read_text(encoding="utf-8")
    assert _BOOM in errors
    assert "on_sample_event" in errors, "the error log must name the callback that failed"
    assert broken_log.samples[0].uuid in errors, "the error log must name the sample"
    assert "Traceback" in errors, "the error log must carry the traceback"


def test_the_error_log_is_bounded(broken_run):
    """Every event of a long run failing must not write an unbounded log -- and the log must say
    that it stopped writing, because silence would read as "the problem went away"."""
    _, feed_dir = broken_run
    text = (feed_dir / ERROR_LOG_FILENAME).read_text(encoding="utf-8")
    entries = text.count("] on_sample_event:")
    assert 0 < entries <= emitter_module.MAX_LOGGED_ERRORS
    assert "suppressed after" in text


# --- (d) off by default ---------------------------------------------------------------


def test_nothing_is_written_when_the_env_var_is_unset(off_run):
    log, work = off_run
    assert log.status == "success"
    assert not list(work.rglob(FEED_FILENAME)), "wrote a feed with the emitter disabled"
    assert not list(work.rglob(ERROR_LOG_FILENAME))
    # Nor anywhere else: a default output path (relative to the cwd, say) would satisfy the two
    # assertions above while still writing a feed nobody asked for. The run id is unique per eval,
    # so its absence in the working directory is a safe, non-flaky check.
    assert not (Path.cwd() / log.eval.run_id).exists()


def test_the_gate_is_the_env_var(monkeypatch, tmp_path):
    monkeypatch.delenv(SPECTATOR_DIR_ENV, raising=False)
    assert SpectatorHooks().enabled() is False
    assert spectator_dir() is None
    monkeypatch.setenv(SPECTATOR_DIR_ENV, "")
    assert SpectatorHooks().enabled() is False, "an empty value must not enable the emitter"
    monkeypatch.setenv(SPECTATOR_DIR_ENV, str(tmp_path))
    assert SpectatorHooks().enabled() is True
    assert spectator_dir() == tmp_path


def _registered_hook() -> SpectatorHooks:
    import farm_eval.farm_task  # noqa: F401  -- the import that performs the registration

    registered = [hook for hook in get_all_hooks() if isinstance(hook, SpectatorHooks)]
    assert len(registered) == 1, f"expected exactly one registered SpectatorHooks, got {registered}"
    return registered[0]


def test_importing_the_task_registers_the_hook(monkeypatch):
    """Registration is by import (`farm_eval/farm_task.py`), and `enabled()` is the only gate --
    so a run with the env var unset carries a registered hook that never acts."""
    hook = _registered_hook()
    monkeypatch.delenv(SPECTATOR_DIR_ENV, raising=False)
    assert hook.enabled() is False


# --- the write protocol ---------------------------------------------------------------


def test_each_line_is_readable_before_the_next_one_is_written(tmp_path):
    """A long run must be watchable while it happens: no line may sit in a buffer."""
    path = tmp_path / "run" / "sample" / FEED_FILENAME
    feed = _FeedFile(path)
    try:
        feed.write([DayEnd(seq=0, day=0)], day=0)
        assert parse_feed_line(path.read_text(encoding="utf-8").splitlines()[0]).seq == 0
        feed.write([DayEnd(seq=1, day=1)], day=1)
        assert len(path.read_text(encoding="utf-8").splitlines()) == 2
    finally:
        feed.close()


def test_the_feed_is_fsynced_at_day_boundaries(tmp_path, monkeypatch):
    synced: list[int] = []
    monkeypatch.setattr("os.fsync", lambda fd: synced.append(fd))
    feed = _FeedFile(tmp_path / "run" / "sample" / FEED_FILENAME)
    try:
        feed.write([DayEnd(seq=0, day=0)], day=0)
        assert len(synced) == 1, "the first batch establishes the day"
        feed.write([DayEnd(seq=1, day=0)], day=0)
        assert len(synced) == 1, "no fsync within a day -- it is a per-line cost otherwise"
        feed.write([DayEnd(seq=2, day=1)], day=1)
        assert len(synced) == 2, "the day advanced, so the day's lines are durable"
    finally:
        feed.close()
    assert len(synced) == 3, "close() must fsync the tail"


# --- restoring transcript order on the live stream ------------------------------------


def _stamped(kind, seconds: float, **fields):
    """A minimal handled event stamped at *seconds* past a fixed instant."""
    return kind(
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=seconds), **fields
    )


def _store(seconds: float):
    return _stamped(StoreEvent, seconds, changes=[])


def _tool(seconds: float, function: str = "end_day"):
    return _stamped(ToolEvent, seconds, id="PLACEHOLDER_CALL", function=function, arguments={})


def _model(seconds: float):
    return _stamped(
        ModelEvent,
        seconds,
        model="PLACEHOLDER_MODEL",
        input=[],
        tools=[],
        tool_choice="auto",
        config=GenerateConfig(),
        output=ModelOutput(),
    )


def test_a_tool_event_delivered_after_its_own_store_events_is_put_back_in_front():
    """The ONE divergence the stream exists to fix: Inspect delivers a `ToolEvent` when the tool
    RETURNS, so it arrives after the `StoreEvent`s it caused while carrying an earlier timestamp.
    Replay writes the recorded (causal) order, so the live stream must be restored to it."""
    stream = _OrderedStream()
    store, later_store, tool = _store(2.0), _store(2.5), _tool(1.0)
    assert stream.push(store) == [], "a store waits: the tool that caused it may still be pending"
    assert stream.push(later_store) == []
    assert stream.push(tool) == [tool, store, later_store], "the call precedes the state it changed"
    assert stream.drain() == []


def test_model_events_keep_arrival_order_when_their_timestamps_invert():
    """A model RETRY is recorded as the failed attempts followed by the successful call, whose
    timestamp is EARLIER (measured: 6 such adjacent inversions among the handled kinds in the
    2026-07-14 pilot log, 1 in the 2026-07-12 one, every one ModelEvent-to-ModelEvent).

    Replay writes recorded order, so re-ordering these -- as a blanket timestamp sort did -- makes
    the live feed diverge from the extracted feed, moving lines and changing `run_health`."""
    stream = _OrderedStream()
    first_error, second_error, success = _model(9.0), _model(11.0), _model(3.0)
    released = stream.push(first_error) + stream.push(second_error) + stream.push(success)
    assert released == [first_error, second_error, success], "arrival order, not timestamp order"
    assert stream.drain() == [], "and nothing is held back: model turns are released immediately"


def test_a_store_event_that_genuinely_precedes_a_tool_call_keeps_its_place():
    """Only the tool's OWN stores move behind it. A store already written before the call was made
    carries an earlier timestamp and stays in front of it."""
    stream = _OrderedStream()
    earlier, tool, caused = _store(1.0), _tool(2.0), _store(3.0)
    assert stream.push(earlier) == []
    assert stream.push(caused) == []
    assert stream.push(tool) == [earlier, tool, caused]


def test_held_stores_are_released_in_front_of_the_next_model_turn():
    """Nothing else is re-ordered, so a `ModelEvent` releases the held stores ahead of itself in
    arrival order -- whatever the timestamps say."""
    stream = _OrderedStream()
    store, model = _store(9.0), _model(3.0)
    assert stream.push(store) == []
    assert stream.push(model) == [store, model]


def test_an_unhandled_event_kind_neither_releases_the_held_stores_nor_enters_them():
    """A tool's span events arrive BEFORE the tool event, so letting one release the held stores
    would emit the effects ahead of their cause -- the exact inversion the stream undoes. The filter
    is the translator's OWN tuple, so a newly translated kind cannot stay un-ordered by accident."""
    assert HANDLED_EVENT_TYPES == (ModelEvent, ToolEvent, StoreEvent)
    stream = _OrderedStream()
    store = _store(2.0)
    stream.push(store)
    span_end = _stamped(SpanEndEvent, 2.5, id="PLACEHOLDER_SPAN")
    assert stream.push(span_end) == [], "an unhandled event must not release the held store"
    assert stream.drain() == [store], "and must not be handed to the translator either"


# --- failure isolation of the callbacks themselves -------------------------------------


def test_a_sample_start_with_no_task_start_logs_instead_of_raising(tmp_path, monkeypatch):
    """`RunMeta` needs the task's `EvalSpec`, cached by `on_task_start`. If a sample somehow
    starts without it there is no feed to write, which must be reported, not raised."""
    monkeypatch.setenv(SPECTATOR_DIR_ENV, str(tmp_path))
    hook = SpectatorHooks()
    # The hook reads only `eval_id` / `sample_id`; `summary` is unused (a frozen dataclass does
    # no runtime type checking, so None is enough to build the payload).
    start = SampleStart(
        eval_set_id=None,
        run_id="PLACEHOLDER_RUN",
        eval_id="PLACEHOLDER_EVAL",
        sample_id="PLACEHOLDER_SAMPLE",
        summary=None,
    )
    asyncio.run(hook.on_sample_start(start))
    errors = (tmp_path / ERROR_LOG_FILENAME).read_text(encoding="utf-8")
    assert "on_sample_start" in errors
    assert "PLACEHOLDER_EVAL" in errors
    assert hook._feeds == {}


def _task_end(eval_id: str) -> TaskEnd:
    """A `TaskEnd` payload. The hook reads only `eval_id`; `log` is unused (the dataclass is frozen
    but does no runtime type checking, so None is enough)."""
    return TaskEnd(eval_set_id=None, run_id="PLACEHOLDER_RUN", eval_id=eval_id, log=None)


class _StubTranslator:
    """A `Translator` stand-in: one `day_end` line per handled event, no state reconstruction."""

    day = 0

    def __init__(self) -> None:
        self.handled: list[object] = []

    def handle(self, event) -> list:
        self.handled.append(event)
        return [DayEnd(seq=len(self.handled) - 1, day=0)]

    def finish(self, status: str) -> list:
        return [EpisodeEnd(seq=len(self.handled), day=0, status=status)]


def test_a_hard_cancelled_sample_keeps_the_events_the_stream_was_still_holding(
    tmp_path, monkeypatch
):
    """`on_task_end` closes what a sample cancelled before `on_sample_end` left open. The ordering
    stream holds already-translatable events (they wait only for a tool call that could precede
    them), so closing without draining silently loses feed lines for state the run really reached --
    while still inventing no `episode_end`, since nobody reported this sample's outcome."""
    monkeypatch.setenv(SPECTATOR_DIR_ENV, str(tmp_path))
    hook = SpectatorHooks()
    path = tmp_path / "run" / "sample" / FEED_FILENAME
    feed = emitter_module._SampleFeed(_StubTranslator(), path, "PLACEHOLDER_EVAL")
    hook._feeds["PLACEHOLDER_SAMPLE"] = feed
    feed.handle(_store(1.0))
    assert path.read_text(encoding="utf-8") == "", "the store is held, so nothing is written yet"

    asyncio.run(hook.on_task_end(_task_end("PLACEHOLDER_EVAL")))

    kinds = [json.loads(line)["kind"] for line in path.read_text(encoding="utf-8").splitlines()]
    assert kinds == ["day_end"], "the held event's line must be written before the file closes"
    assert "episode_end" not in kinds, "no status may be invented for an unreported sample"
    assert hook._feeds == {}


def test_one_feed_that_fails_to_close_does_not_strand_the_rest(tmp_path, monkeypatch):
    """A single failing `close()` used to abort the loop, leaking every remaining open feed into the
    next task of a sweep -- which is how a long sweep runs out of file descriptors."""
    monkeypatch.setenv(SPECTATOR_DIR_ENV, str(tmp_path))
    hook = SpectatorHooks()

    class _Feed:
        def __init__(self, *, explodes: bool) -> None:
            self.eval_id = "PLACEHOLDER_EVAL"
            self._explodes = explodes
            self.closed = False

        def drain(self) -> None:
            pass

        def close(self) -> None:
            self.closed = True
            if self._explodes:
                raise RuntimeError(_BOOM)

    broken, healthy = _Feed(explodes=True), _Feed(explodes=False)
    hook._feeds = {"PLACEHOLDER_BROKEN": broken, "PLACEHOLDER_HEALTHY": healthy}

    asyncio.run(hook.on_task_end(_task_end("PLACEHOLDER_EVAL")))

    assert healthy.closed, "the feed after the failing one must still be closed"
    assert hook._feeds == {}
    errors = (tmp_path / ERROR_LOG_FILENAME).read_text(encoding="utf-8")
    assert _BOOM in errors and "PLACEHOLDER_BROKEN" in errors


class _FlakyFile:
    """A file object that accepts *allow* writes and then raises, to model a full disk."""

    def __init__(self, allow: int) -> None:
        self.written: list[str] = []
        self.allow = allow

    def write(self, text: str) -> None:
        if len(self.written) >= self.allow:
            raise OSError("PLACEHOLDER_DISK_FULL")
        self.written.append(text)

    def flush(self) -> None:
        pass

    def fileno(self) -> int:
        return -1

    def close(self) -> None:
        pass


def test_a_write_that_fails_mid_batch_retries_the_same_lines_next_callback(tmp_path, monkeypatch):
    """The translator hands each feed event out exactly ONCE -- the head `run_meta` line above
    all -- so a line dropped by a failed write can never be rebuilt. Lines therefore stay queued
    until their own write returned: a transient failure costs a retry, not the head of the feed."""
    monkeypatch.setattr("os.fsync", lambda fd: None)
    feed = _FeedFile(tmp_path / "run" / "sample" / FEED_FILENAME)
    flaky = _FlakyFile(allow=1)
    monkeypatch.setattr(feed, "_file", flaky)

    with pytest.raises(OSError):
        feed.write([DayEnd(seq=0, day=0), DayEnd(seq=1, day=0)], day=0)
    assert [json.loads(text)["seq"] for text in flaky.written] == [0], "one line got through"

    flaky.allow = 99
    feed.write([DayEnd(seq=2, day=0)], day=0)
    assert [json.loads(text)["seq"] for text in flaky.written] == [0, 1, 2], (
        "the failed line is retried, the rest of its batch is not dropped, and nothing is doubled"
    )


def test_an_event_for_an_unknown_sample_is_ignored_silently(tmp_path, monkeypatch):
    """A sample whose start already failed emits events for the rest of the run. Logging each of
    them would bury the one failure that matters."""
    monkeypatch.setenv(SPECTATOR_DIR_ENV, str(tmp_path))
    hook = SpectatorHooks()
    event = SampleEvent(
        eval_set_id=None,
        run_id="PLACEHOLDER_RUN",
        eval_id="PLACEHOLDER_EVAL",
        sample_id="PLACEHOLDER_SAMPLE",
        event=None,
    )
    asyncio.run(hook.on_sample_event(event))
    assert not (tmp_path / ERROR_LOG_FILENAME).exists()
