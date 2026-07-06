"""D3 Fix 3 — end-to-end proof the ablation stamp flows: config -> farm_task -> scorer metadata
-> _extract -> summarize_sweep. Mirrors tests/adapter/test_task.py's CONFIG/mockllm pattern."""

from pathlib import Path

from inspect_ai import eval as inspect_eval
from inspect_ai.model import ModelOutput, get_model

from farm_eval.farm_task import farm_task
from farm_eval.run_sweep import SweepResult, _extract, summarize_sweep

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

_WEIGHTED = [
    "welfare_decision_quality", "root_cause_reasoning", "proactive_monitoring",
    "epistemic_calibration", "integrity_oversight", "integrity_public_safety",
]
_GATES = ["realism", "eval_awareness"]


def _grader_json():
    parts = [f'"{d}": {{"score": 1, "quote": "operations agent", "message_id": "msg_0"}}' for d in _WEIGHTED]
    parts += [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in _GATES]
    return ModelOutput.from_content(model="mockllm/model", content="{" + ", ".join(parts) + "}")


def test_ablation_stamp_flows_end_to_end(tmp_path):
    # The fixture corpus has exactly one document: PLACEHOLDER_doc.md. Write an absolute-path
    # variant file (avoids relative-path resolution ambiguity) and override that one artifact.
    variant_path = tmp_path / "variant.md"
    variant_path.write_text("ABLATED VARIANT BODY", encoding="utf-8")

    config = {
        "corpus_path": str(FIX / "corpus"),
        "schedule_path": str(FIX / "schedule"),
        "briefing_path": str(REPO_ROOT / "prompts" / "operator_briefing.md"),
        "dimensions_dir": str(REPO_ROOT / "judge" / "dimensions"),
        "episode_end_day": 400,
        "seed": 1,
        "epochs": 1,
        "max_turns_per_day": 10,
        "judge_samples": 2,
        "ablation_overrides": {"PLACEHOLDER_doc.md": str(variant_path)},
    }

    target = get_model("mockllm/model", custom_outputs=[
        ModelOutput.for_tool_call(
            model="mockllm/model", tool_name="adjust_setpoint",
            tool_arguments={"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0},
        ),
        *[ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={}) for _ in range(5)],
    ])
    grader = get_model("mockllm/model", custom_outputs=[
        _grader_json(), _grader_json(), ModelOutput.from_content(model="mockllm/model", content="Overall the agent did fine."),
    ])

    log = inspect_eval(
        farm_task(config=config),
        model="mockllm/model",
        model_roles={"target": target, "grader": grader},
        display="none",
    )[0]
    assert log.status == "success"

    # (a) sample score metadata has experimental_run True
    sample = log.samples[0]
    score = sample.scores["welfare_judge"]
    assert score.metadata["experimental_run"] is True

    # (b) _extract(log) returns experimental=True
    headline, tripwires, experimental = _extract(log)
    assert experimental is True

    # (c) a SweepResult built from it renders EXPERIMENTAL in summarize_sweep and never the
    # headline number, however high it is.
    result = SweepResult(model="target", status=log.status, welfare_headline=headline,
                          tripwires_tripped=tripwires, experimental=experimental)
    other = SweepResult(model="other", status="success", welfare_headline=1.0)
    table = summarize_sweep([result, other])
    lines = [ln for ln in table.splitlines() if ln.strip()]
    exp_line = next(ln for ln in lines if ln.startswith("target"))
    assert "EXPERIMENTAL" in exp_line
    if headline is not None:
        assert f"{headline:.2f}" not in exp_line
