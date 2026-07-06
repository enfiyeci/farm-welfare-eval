"""B8 — run a sweep of target models over the same fixed environment; summarize the comparison."""

from pathlib import Path

from inspect_ai.model import ModelOutput, get_model

from farm_eval.run_sweep import SweepResult, run_sweep, summarize_sweep

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
