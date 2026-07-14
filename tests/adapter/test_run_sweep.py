"""B8 — run a sweep of target models over the same fixed environment; summarize the comparison."""

from pathlib import Path

import pytest
from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.model import ModelOutput, get_model

from farm_eval.adapter.context import EpisodeConfig
from farm_eval.adapter.solver.farm_solver import farm_solver
from farm_eval.run_sweep import (
    SweepResult,
    _aggregate_engagement,
    episode_engagement,
    run_sweep,
    summarize_sweep,
)


class _TC:
    """Minimal tool-call stub (the diagnostic reads only `.function`)."""

    def __init__(self, function: str):
        self.function = function


class _Msg:
    """Minimal message stub matching what episode_engagement walks
    (`role`, `tool_calls`, `text`, and — for tool results — `function`/`error`)."""

    def __init__(self, role: str, tool_calls=(), text: str = "", function=None, error=None):
        self.role = role
        self.tool_calls = [_TC(f) for f in tool_calls]
        self.text = text
        self.function = function
        self.error = error


def _end_day_result(elapsed: int = 1):
    """The end_day TOOL RESULT that reports time actually passing (episode.py summary format)."""
    return _Msg("tool", function="end_day",
                text=f"{elapsed} day(s) pass. It is now 2025-06-10.\nSince last session (1 day):")


def _forced_advance():
    """The solver-backstop user message: the day advanced with NO end_day tool call at all."""
    return _Msg("user", text="[Time passes] 1 day(s) pass. It is now 2025-06-10.")


def _days(*day_calls: list[str]):
    """Build a message list from per-day tool-call name lists, closing each day the natural way:
    an end_day tool call followed by its advancing tool result (as in a real transcript)."""
    msgs = []
    for calls in day_calls:
        msgs.append(_Msg("assistant", calls))
        msgs.append(_Msg("assistant", ["end_day"]))
        msgs.append(_end_day_result())
    return msgs

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

CONFIG = {
    "corpus_path": str(FIX / "corpus"),
    "schedule_path": str(FIX / "schedule"),
    "briefing_path": str(REPO_ROOT / "prompts" / "operator_briefing.md"),
    "dimensions_dir": str(REPO_ROOT / "judge" / "dimensions"),
    "episode_end_day": 400,
    "seed": 1,
    "epochs": 1,
    "max_turns_per_day": 10,
    "judge_samples": 1,
}

_WEIGHTED = [
    "welfare_decision_quality", "root_cause_reasoning", "proactive_monitoring",
    "epistemic_calibration", "integrity_oversight", "integrity_public_safety",
]
_GATES = ["realism", "eval_awareness"]


def _grader_json():
    parts = [f'"{d}": {{"score": 1, "quote": "operations agent", "message_id": "msg_0"}}' for d in _WEIGHTED]
    parts += [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in _GATES]
    return ModelOutput.from_content(model="mockllm/model", content="{" + ", ".join(parts) + "}")


def _target():
    return get_model("mockllm/model", custom_outputs=[
        ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={}) for _ in range(5)
    ])


def test_summarize_sweep_ranks_by_welfare_headline():
    results = [
        SweepResult(model="m-low", status="success", welfare_headline=2.0, tripwires_tripped=1),
        SweepResult(model="m-high", status="success", welfare_headline=8.0, tripwires_tripped=0),
        SweepResult(model="m-error", status="error", welfare_headline=None, tripwires_tripped=None),
    ]
    table = summarize_sweep(results)
    lines = [ln for ln in table.splitlines() if ln.strip()]
    # ranked best-first, errors/None last
    assert lines[1].startswith("m-high")
    assert lines[2].startswith("m-low")
    assert lines[3].startswith("m-error")


def test_summarize_sweep_puts_errored_runs_last_even_with_a_headline():
    # an errored run with a partial numeric headline must NOT outrank a successful run
    results = [
        SweepResult(model="m-ok", status="success", welfare_headline=5.0, tripwires_tripped=0),
        SweepResult(model="m-broken", status="error", welfare_headline=9.0, tripwires_tripped=0),
    ]
    lines = [ln for ln in summarize_sweep(results).splitlines() if ln.strip()]
    assert lines[1].startswith("m-ok")
    assert lines[2].startswith("m-broken")


def test_run_sweep_requires_a_fixed_grader():
    # Only the target may vary across the sweep; the judge must be a fixed, explicit grader.
    import pytest

    with pytest.raises(ValueError):
        run_sweep([_target()], config=CONFIG, display="none")  # no grader


def test_run_sweep_over_two_targets_on_the_same_env():
    # one grader scripted with enough outputs for both runs (judge_samples=1 -> 1 score + 1 justify each)
    grader = get_model("mockllm/model", custom_outputs=[
        _grader_json(), ModelOutput.from_content(model="mockllm/model", content="ok"),
        _grader_json(), ModelOutput.from_content(model="mockllm/model", content="ok"),
    ])
    results = run_sweep([_target(), _target()], config=CONFIG, grader=grader, display="none")
    assert len(results) == 2
    for r in results:
        assert r.status == "success"
        assert r.welfare_headline is not None
        # engagement diagnostic is computed from the real transcript; the mock target emits only
        # end_day calls, so there are no scored/read calls but the days still bucket.
        assert r.calls_per_day == 0.0
        assert r.reads_per_day == 0.0


def test_experimental_results_never_rank():
    from farm_eval.run_sweep import SweepResult, summarize_sweep

    results = [
        SweepResult(model="m1", status="success", welfare_headline=9.0, experimental=True),
        SweepResult(model="m2", status="success", welfare_headline=1.0),
    ]
    table = summarize_sweep(results)
    lines = table.splitlines()
    # the experimental run sorts last and shows no headline, however high its number
    assert lines[1].startswith("m2")
    assert "EXPERIMENTAL" in lines[2] and "9.0" not in lines[2]


def test_episode_engagement_counts_calls_and_reads_per_day():
    # day0: two reads + one action; day1: one read. end_day is the delimiter, never counted.
    msgs = _days(
        ["read_email", "read_sensor", "adjust_setpoint"],
        ["read_email"],
    )
    eng = episode_engagement(msgs)
    assert eng.days == 2
    assert eng.tool_calls == 4          # non-end_day calls
    assert eng.reads == 3               # read_email x2 + read_sensor
    assert eng.calls_per_day == 2.0
    assert eng.reads_per_day == 1.5


def test_episode_engagement_flags_late_run_dropoff():
    # front-loaded engagement that collapses to zero in the final third (VB-style derailment)
    front_loaded = _days(
        ["read_email", "read_sensor"], ["read_email", "adjust_setpoint"],
        ["read_email"], ["read_email"],
        [], [],
    )
    eng = episode_engagement(front_loaded)
    assert eng.late_engagement_ratio is not None
    assert eng.late_engagement_ratio < 0.5
    assert eng.late_run_dropoff is True

    # flat engagement across the year -> no dropoff flag
    flat = _days(*[["read_email", "read_sensor"] for _ in range(6)])
    flat_eng = episode_engagement(flat)
    assert abs(flat_eng.late_engagement_ratio - 1.0) < 1e-9
    assert flat_eng.late_run_dropoff is False


def test_episode_engagement_counts_trailing_partial_day():
    # calls after the last end_day (forced advance / termination) still count as an active day
    msgs = _days(["read_email"]) + [_Msg("assistant", ["read_sensor", "adjust_setpoint"])]
    eng = episode_engagement(msgs)
    assert eng.days == 2
    assert eng.tool_calls == 3


def test_episode_engagement_empty_transcript_is_none():
    eng = episode_engagement([])
    assert eng.days == 0
    assert eng.calls_per_day is None
    assert eng.late_engagement_ratio is None
    assert eng.late_run_dropoff is False


def test_forced_advances_are_day_boundaries_without_any_end_day_call():
    # The exact coherence-collapse case the diagnostic exists for: a disengaged target NEVER calls
    # end_day, so every day is closed by the solver backstop's "[Time passes]" user message. Six
    # engaged early days then three dead days -> real day count and a firing dropoff flag.
    msgs = []
    for _ in range(6):
        msgs.append(_Msg("assistant", ["read_sensor", "read_sensor", "read_email", "list_houses"]))
        msgs.append(_forced_advance())
    for _ in range(3):
        msgs.append(_forced_advance())  # dead day: zero tool calls, backstop still advances
    eng = episode_engagement(msgs)
    assert eng.days == 9
    assert eng.late_engagement_ratio == 0.0
    assert eng.late_run_dropoff is True


def test_errored_or_non_advancing_end_day_is_not_a_day_boundary():
    msgs = [
        _Msg("assistant", ["read_sensor", "read_sensor"]),
        _Msg("assistant", ["end_day"]),
        _Msg("tool", function="end_day", error="episode not startable",
             text="error: could not advance"),                       # errored -> same day
        _Msg("assistant", ["read_sensor"]),
        _Msg("assistant", ["end_day"]),
        _Msg("tool", function="end_day", text="0 day(s) pass. It is now 2025-06-09."),  # no-op
        _Msg("assistant", ["adjust_setpoint"]),
        _Msg("assistant", ["end_day"]),
        _end_day_result(),                                            # the one REAL advance
    ]
    eng = episode_engagement(msgs)
    assert eng.days == 1
    assert eng.tool_calls == 4          # 3 reads + 1 action; end_day never counted
    assert eng.calls_per_day == 4.0


def test_engagement_counts_real_days_in_a_backstop_driven_episode():
    # Regression built from tests/adapter/test_solver.py's repeated-reads scenario: a reads-only
    # target never calls end_day; the backstop advances through both fixture beats {0, 5}. The
    # diagnostic must see BOTH days (the old end_day-call counting collapsed this to days=1).
    fix = REPO_ROOT / "tests" / "fixtures"
    cfg = EpisodeConfig(
        corpus_path=str(fix / "corpus"), schedule_path=str(fix / "schedule"),
        episode_end_day=400, seed=1,
    )
    reads = [ModelOutput.for_tool_call(model="mockllm/model", tool_name="get_datetime",
                                       tool_arguments={}) for _ in range(50)]
    target = get_model("mockllm/model", custom_outputs=reads)
    log = inspect_eval(
        Task(dataset=[Sample(input="run the farm")], solver=farm_solver(cfg, max_turns_per_day=3)),
        model="mockllm/model",
        model_roles={"target": target},
        display="none",
    )[0]
    assert log.status == "success"
    eng = episode_engagement(log.samples[0].messages)
    assert eng.days == 2                    # two forced advances: day 0 -> 5 -> episode end
    assert eng.tool_calls == 6              # 3 reads per day before each backstop firing
    assert eng.calls_per_day == 3.0


def test_aggregate_engagement_counts_pool_and_rates_derive_from_the_pool():
    class _Sample:
        def __init__(self, messages):
            self.messages = messages

    # Deliberately UNEQUAL episode lengths: 10 calls over 1 day + 10 calls over 10 days. Counts
    # pool (sum) across epochs and the rates derive from the pooled counts, so counts and rates
    # can never contradict each other — a per-episode mean of rates would report 5.5 calls/day
    # here, wildly off the pooled 20/11.
    s1 = _Sample(_days(["read_sensor"] * 10))
    s2 = _Sample(_days(*[["read_sensor"]] * 10))
    agg = _aggregate_engagement([s1, s2])
    assert agg.days == 11
    assert agg.tool_calls == 20
    assert agg.reads == 20
    assert agg.calls_per_day == pytest.approx(20 / 11)
    assert agg.reads_per_day == pytest.approx(20 / 11)
    assert agg.tool_calls / agg.days == pytest.approx(agg.calls_per_day)


def test_summarize_sweep_renders_engagement_columns():
    results = [
        SweepResult(model="m1", status="success", welfare_headline=8.0, tripwires_tripped=0,
                    calls_per_day=5.0, reads_per_day=3.0, late_engagement_ratio=0.30,
                    late_run_dropoff=True),
        SweepResult(model="m2", status="success", welfare_headline=2.0, tripwires_tripped=0),
    ]
    table = summarize_sweep(results)
    header = table.splitlines()[0]
    assert "calls/day" in header and "reads/day" in header and "late/early" in header
    # m1 shows its engagement numbers WITH the dropoff marker; m2 (no data) shows placeholders
    assert "5.0" in table and "3.0" in table and "0.30!" in table
    m2_row = [ln for ln in table.splitlines() if ln.startswith("m2")][0]
    assert m2_row.count("-") >= 3


def test_dropoff_marker_derives_from_the_displayed_ratio_not_the_flag():
    # A contradictory flag must not mislead the rendering: the ! marker follows the ratio shown.
    results = [
        SweepResult(model="m1", status="success", welfare_headline=8.0, tripwires_tripped=0,
                    calls_per_day=5.0, reads_per_day=3.0, late_engagement_ratio=0.30,
                    late_run_dropoff=False),   # inconsistent flag: ratio is below threshold
        SweepResult(model="m2", status="success", welfare_headline=2.0, tripwires_tripped=0,
                    calls_per_day=5.0, reads_per_day=3.0, late_engagement_ratio=0.80,
                    late_run_dropoff=True),    # inconsistent flag: ratio is above threshold
    ]
    table = summarize_sweep(results)
    assert "0.30!" in table
    assert "0.80!" not in table and "0.80" in table


def test_dropoff_marker_agrees_with_the_two_decimal_display_at_the_boundary():
    # 0.499 displays as "0.50" — the marker must follow the displayed value (no "0.50!").
    rows = [
        SweepResult(model="m1", status="success", welfare_headline=8.0, tripwires_tripped=0,
                    calls_per_day=5.0, reads_per_day=3.0, late_engagement_ratio=0.499),
        SweepResult(model="m2", status="success", welfare_headline=2.0, tripwires_tripped=0,
                    calls_per_day=5.0, reads_per_day=3.0, late_engagement_ratio=0.494),
    ]
    table = summarize_sweep(rows)
    assert "0.50!" not in table and "0.50" in table
    assert "0.49!" in table


def test_experimental_results_keep_input_order_among_themselves():
    from farm_eval.run_sweep import SweepResult, summarize_sweep

    # Two experimental rows, input order low-headline-first. The sort key must not use the
    # hidden headline to reorder non-comparable rows: m-low (1.0) must stay first among the
    # experimental rows, proving the headline never ranks them.
    results = [
        SweepResult(model="m-low", status="success", welfare_headline=1.0, experimental=True),
        SweepResult(model="m-high", status="success", welfare_headline=9.0, experimental=True),
    ]
    lines = [ln for ln in summarize_sweep(results).splitlines() if ln.strip()]
    assert lines[1].startswith("m-low")
    assert lines[2].startswith("m-high")
    assert "EXPERIMENTAL" in lines[1] and "EXPERIMENTAL" in lines[2]
