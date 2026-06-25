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

_DIMS = ["welfare_decision_quality", "proactive_monitoring", "integrity_transparency",
         "feed_withdrawal_molt", "eval_awareness"]


def _grader_json():
    body = ", ".join(f'"{d}": {{"score": 1, "quote": "ok", "message_id": "m0"}}' for d in _DIMS)
    return ModelOutput.from_content(model="mockllm/model", content="{" + body + "}")


def test_farm_task_runs_end_to_end_and_scores():
    target = get_model("mockllm/model", custom_outputs=[
        ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={}) for _ in range(5)
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
    assert "weighted_welfare" in score_value
    assert "welfare_decision_quality" in score_value
