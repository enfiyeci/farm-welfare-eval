"""B8 — run a sweep of target models over the same fixed environment; summarize the comparison."""

from pathlib import Path

from inspect_ai.model import ModelOutput, get_model

from farm_eval.run_sweep import SweepResult, episode_engagement, run_sweep, summarize_sweep


class _TC:
    """Minimal tool-call stub (the diagnostic reads only `.function`)."""

    def __init__(self, function: str):
        self.function = function


class _Msg:
    """Minimal message stub matching what episode_engagement walks (`role`, `tool_calls`)."""

    text = ""

    def __init__(self, role: str, tool_calls=()):
        self.role = role
        self.tool_calls = [_TC(f) for f in tool_calls]


def _days(*day_calls: list[str]):
    """Build a message list from per-day tool-call name lists, closing each day with end_day."""
    msgs = []
    for calls in day_calls:
        msgs.append(_Msg("assistant", calls))
        msgs.append(_Msg("assistant", ["end_day"]))
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


def test_summarize_sweep_renders_engagement_columns():
    results = [
        SweepResult(model="m1", status="success", welfare_headline=8.0, tripwires_tripped=0,
                    calls_per_day=5.0, reads_per_day=3.0, late_engagement_ratio=0.30),
        SweepResult(model="m2", status="success", welfare_headline=2.0, tripwires_tripped=0),
    ]
    table = summarize_sweep(results)
    header = table.splitlines()[0]
    assert "calls/day" in header and "reads/day" in header and "late/early" in header
    # m1 shows its engagement numbers with a dropoff marker; m2 (no data) shows placeholders
    assert "5.0" in table and "3.0" in table and "0.30" in table
    m2_row = [ln for ln in table.splitlines() if ln.startswith("m2")][0]
    assert m2_row.count("-") >= 3


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
