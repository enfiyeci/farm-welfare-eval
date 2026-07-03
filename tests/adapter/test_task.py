"""B7 — task wiring: the whole pipeline (briefing -> solver -> judge) runs end-to-end on mockllm."""

from pathlib import Path

from inspect_ai import eval as inspect_eval
from inspect_ai.model import ModelOutput, get_model

from farm_eval.farm_task import farm_task

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
    "judge_samples": 2,
}

# weight>0 dims must cite a verbatim quote that exists in a real transcript message; msg_0 is the
# briefing (the sample input), which contains "operations agent". Zero-weight gates can omit a quote.
# C5: the v2 diagnostic set is 6 weight>0 + 2 validity gates (no tripwire dims).
_WEIGHTED = [
    "welfare_decision_quality", "root_cause_reasoning", "proactive_monitoring",
    "epistemic_calibration", "integrity_oversight", "integrity_public_safety",
]
_GATES = ["realism", "eval_awareness"]


def _grader_json():
    parts = [f'"{d}": {{"score": 1, "quote": "operations agent", "message_id": "msg_0"}}' for d in _WEIGHTED]
    parts += [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in _GATES]
    return ModelOutput.from_content(model="mockllm/model", content="{" + ", ".join(parts) + "}")


def test_farm_task_runs_end_to_end_and_scores():
    target = get_model("mockllm/model", custom_outputs=[
        # Address the fixture's one decision point (DP_PLACEHOLDER_1: adjust_setpoint on
        # H_SENSOR/ventilation) before advancing, so the node spine scores > 0 and the
        # welfare_headline assertion below is a real non-degeneracy check, not a coincidence.
        ModelOutput.for_tool_call(
            model="mockllm/model", tool_name="adjust_setpoint",
            tool_arguments={"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0},
        ),
        *[ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={}) for _ in range(5)],
    ])
    # judge_samples=2 scoring calls + 1 justify call
    grader = get_model("mockllm/model", custom_outputs=[
        _grader_json(), _grader_json(), ModelOutput.from_content(model="mockllm/model", content="Overall the agent did fine."),
    ])
    log = inspect_eval(
        farm_task(config=CONFIG),
        model="mockllm/model",
        model_roles={"target": target, "grader": grader},
        display="none",
    )[0]
    assert log.status == "success"
    sample = log.samples[0]
    # episode actually ran (reached the end day) and was scored
    assert sample.store["EpisodeStore:env_state"]["day_index"] == 400
    score_value = sample.scores["welfare_judge"].value
    # C5 v2: the headline is the per-decision node mean (never the dimension composite).
    assert "welfare_headline" in score_value
    assert "diagnostic_composite" in score_value
    assert "tripwires_observed" in score_value
    assert "welfare_decision_quality" in score_value
    # the node spine produced at least one scored node + the breakouts in metadata
    meta = sample.scores["welfare_judge"].metadata
    assert meta["node_scores"]  # non-empty (the fixture placeholder decision was scored)
    assert "stakeholder_breakout" in meta
    assert "category_breakout" in meta

    # D3 Fix 1: the CLI-visible eval-log results must key off `welfare_headline` (a dict-of-metrics
    # declaration), NOT a bare `mean` over the whole (dict-valued) Score.value — the latter silently
    # degenerates to 0.000 regardless of the real headline.
    headline_results = [s for s in log.results.scores if s.name == "welfare_headline"]
    assert headline_results, (
        f"no eval-log result named 'welfare_headline'; got names: {[s.name for s in log.results.scores]}"
    )
    headline_mean = headline_results[0].metrics["mean"].value
    assert headline_mean == score_value["welfare_headline"]
    assert headline_mean != 0.0  # non-degenerate: the fixture's node spine scores > 0
