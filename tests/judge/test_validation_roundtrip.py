"""End-to-end: real mockllm eval -> .eval log on disk -> blind sheets -> filled sheets ->
validation_result -> rendered report. Proves the harness reads REAL inspect logs, not just
SimpleNamespace fakes (epochs=2 gives two samples so pairing is exercised end-to-end)."""

from pathlib import Path

import yaml
from inspect_ai import eval as inspect_eval
from inspect_ai.log import read_eval_log
from inspect_ai.model import ModelOutput, get_model

from farm_eval.farm_task import farm_task
from farm_eval.judge.validation_harness import (
    extract_sample_record,
    load_filled_sheet,
    render_report,
    validation_result,
    write_label_sheets,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

CONFIG = {
    "corpus_path": str(FIX / "corpus"),
    "schedule_path": str(FIX / "schedule"),
    "briefing_path": str(REPO_ROOT / "prompts" / "operator_briefing.md"),
    "dimensions_dir": str(REPO_ROOT / "judge" / "dimensions"),
    "episode_end_day": 400,
    "seed": 1,
    "epochs": 2,  # two samples -> two labeled transcripts -> rho computable
    "max_turns_per_day": 10,
    "judge_samples": 1,
}

_WEIGHTED = [
    "welfare_decision_quality", "root_cause_reasoning", "proactive_monitoring",
    "epistemic_calibration", "integrity_oversight", "integrity_public_safety",
]
_GATES = [
    "realism", "eval_awareness", "assistant_persona_bleed", "helplessness_resignation",
]


def _grader_json():
    parts = [f'"{d}": {{"score": 1, "quote": "operations agent", "message_id": "msg_0"}}' for d in _WEIGHTED]
    parts += [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in _GATES]
    return ModelOutput.from_content(model="mockllm/model", content="{" + ", ".join(parts) + "}")


def test_roundtrip_log_to_sheets_to_report(tmp_path):
    per_epoch = [
        ModelOutput.for_tool_call(
            model="mockllm/model", tool_name="adjust_setpoint",
            tool_arguments={"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0},
        ),
        *[ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={})
          for _ in range(5)],
    ]
    target = get_model("mockllm/model", custom_outputs=per_epoch * 2)
    # per epoch: judge_samples=1 grading call + 1 justify call
    grader = get_model("mockllm/model", custom_outputs=[
        _grader_json(), ModelOutput.from_content(model="mockllm/model", content="Fine."),
    ] * 2)
    log = inspect_eval(
        farm_task(config=CONFIG), model="mockllm/model",
        model_roles={"target": target, "grader": grader},
        display="none", log_dir=str(tmp_path / "logs"),
    )[0]
    assert log.status == "success"

    # 1. blind sheets from the on-disk log
    log_file = Path(log.location)
    sheets_dir = tmp_path / "sheets"
    sheet_paths = write_label_sheets(
        log_file, sheets_dir, CONFIG["schedule_path"], CONFIG["dimensions_dir"]
    )
    assert len(sheet_paths) == 2  # one per epoch

    # 2. "label" them (proxy) and reload through the validating loader
    filled = []
    for path in sheet_paths:
        sheet = yaml.safe_load(path.read_text(encoding="utf-8"))
        sheet["labeler"] = "roundtrip-test"
        sheet["labeler_kind"] = "proxy"
        for node in sheet["nodes"]:
            node["score"] = 5.0
        for dim in sheet["dimensions"]:
            dim["score"] = 5.0
        path.write_text(yaml.safe_dump(sheet, sort_keys=False), encoding="utf-8")
        filled.append(load_filled_sheet(path))

    # 3. pair against the real log records and render
    disk = read_eval_log(str(log_file))
    records = [extract_sample_record(s, log_file.name) for s in disk.samples]
    result = validation_result(records, filled)
    assert result["n_transcripts"] == 2
    assert result["node_pairs"]["DP_PLACEHOLDER_1"] == 2
    report = render_report(result)
    assert "PROXY" in report
    assert "DP_PLACEHOLDER_1" in report
