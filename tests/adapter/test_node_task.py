"""End to end: manifest -> samples -> solver -> node scorer, on mockllm, over the node fixture."""
from pathlib import Path

import pytest
from inspect_ai import eval as inspect_eval
from inspect_ai.model import ModelOutput, get_model

from farm_eval.node_task import farm_node_task

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

CONFIG = {
    "corpus_path": str(FIX / "corpus"),
    "schedule_path": str(FIX / "node_schedule"),
    "briefing_path": str(REPO_ROOT / "prompts" / "operator_briefing.md"),
    "dimensions_dir": str(REPO_ROOT / "judge" / "dimensions"),
    "seed": 1,
    "epochs": 1,
    "max_turns_per_day": 10,
    "judge_samples": 1,
    "dimension_mode": "validity_only",
}
_GATES = ["realism", "eval_awareness", "assistant_persona_bleed", "helplessness_resignation"]


def _validity_json():
    parts = [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in _GATES]
    return ModelOutput.from_content(model="mockllm/model", content="{" + ", ".join(parts) + "}")


def _act():
    return ModelOutput.for_tool_call(model="mockllm/model", tool_name="adjust_setpoint",
                                     tool_arguments={"house_id": "H_NOSENSOR", "system": "ventilation", "value": 1.2})


def _end():
    return ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={})


def test_node_task_expands_manifest_and_scores_each_episode():
    # three samples (neutral, history_bad, QUIET_D15). mockllm's custom_outputs is ONE iterator
    # per model instance shared across concurrently-running samples, so max_samples=1 is required
    # to force strict dataset order — otherwise whichever sample reaches generate() first consumes
    # _act() and the others only ever see end_day, making the neutral-scores-10.0 assertion below
    # a race. With order forced, only the first sample (neutral) acts; the rest only end days.
    target = get_model("mockllm/model", custom_outputs=[_act(), *[_end() for _ in range(8)]] * 3)
    grader = get_model("mockllm/model", custom_outputs=[_validity_json() for _ in range(3)])
    log = inspect_eval(farm_node_task(config=CONFIG), model="mockllm/model",
                       model_roles={"target": target, "grader": grader}, display="none",
                       max_samples=1)[0]
    assert log.status == "success"
    by_id = {s.id: s for s in log.samples}
    assert set(by_id) == {"DP_PLACEHOLDER_2::neutral", "DP_PLACEHOLDER_2::history_bad", "QUIET_D15::neutral"}
    neutral = by_id["DP_PLACEHOLDER_2::neutral"]
    assert neutral.metadata["dp_id"] == "DP_PLACEHOLDER_2" and neutral.metadata["arm"] == "neutral"
    score = neutral.scores["node_welfare_judge"]
    assert score.value["welfare_headline"] == 10.0
    assert score.metadata["node_scores"] == {"DP_PLACEHOLDER_2": 10.0}
    assert score.metadata["episode_id"] == "DP_PLACEHOLDER_2" and score.metadata["arm"] == "neutral"
    assert "welfare_decision_quality" not in score.value      # validity_only: weighted dims not graded
    assert "eval_awareness" in score.value
    quiet = by_id["QUIET_D15::neutral"].scores["node_welfare_judge"]
    # grade_episode assigns float("nan") in-process (see scorer.py's own note at the
    # welfare_judge @scorer decorator: "NaN is still a float, so metrics compute [...] and the
    # persisted log value round-trips as null" — pydantic's model_dump_json has no NaN literal).
    # inspect_eval's returned EvalLog has already gone through that JSON round-trip, so the
    # value surfaces here as None, not NaN — verified directly (Score(value={"a": float("nan")})
    # .model_dump_json() == '{"value":{"a":null,...}}' on this pinned inspect-ai 0.3.241).
    assert quiet.value["welfare_headline"] is None and quiet.metadata["quiet_episode"] is True


def test_episode_filter_selects_a_subset():
    target = get_model("mockllm/model", custom_outputs=[_end() for _ in range(8)])
    grader = get_model("mockllm/model", custom_outputs=[_validity_json()])
    log = inspect_eval(farm_node_task(config=CONFIG, episode_ids="QUIET_D15"), model="mockllm/model",
                       model_roles={"target": target, "grader": grader}, display="none")[0]
    assert [s.id for s in log.samples] == ["QUIET_D15::neutral"]


def test_invalid_dimension_mode_rejected_before_any_run():
    with pytest.raises(ValueError, match="dimension_mode"):
        farm_node_task(config=CONFIG, dimension_mode="validty_only")
