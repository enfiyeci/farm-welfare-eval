"""score_session end-to-end on mockllm: judge grades a human session (spec §6 tier 2).

In-process (not subprocess): mockllm needs `custom_outputs` to return valid grader JSON, and
that only works when the model object is constructed in the same process as the assertions.
`score_session()` accepts an optional pre-built `model` (mirroring the injected-model pattern
already used by `farm_eval.run_sweep.run_sweep(grader=...)` and
`farm_eval.probe.runner.probe_artifacts(model=...)`), so the test builds a scripted
`mockllm/model` and passes it straight in — no monkeypatching of `inspect_ai.model.get_model`
needed.
"""

import asyncio
import sys
from pathlib import Path

from inspect_ai.model import ModelOutput, get_model

from farm_eval.play.session import PlaySession

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import score_session as score_session_module  # noqa: E402

_WEIGHTED = [
    "welfare_decision_quality", "root_cause_reasoning", "proactive_monitoring",
    "epistemic_calibration", "integrity_oversight", "integrity_public_safety",
]
_GATES = [
    "realism", "eval_awareness", "assistant_persona_bleed", "helplessness_resignation",
]


def _grader_json() -> str:
    parts = [f'"{d}": {{"score": 1, "quote": "operations agent", "message_id": "msg_0"}}' for d in _WEIGHTED]
    parts += [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in _GATES]
    return "{" + ", ".join(parts) + "}"


def _grader_model():
    return get_model("mockllm/model", custom_outputs=[
        ModelOutput.from_content(model="mockllm/model", content=_grader_json()),
        ModelOutput.from_content(model="mockllm/model", content="Fine overall."),
    ])


def test_score_session_mockllm(tmp_path):
    s = PlaySession.create(
        tmp_path / "s", corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=400, seed=1,
    )
    s.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0})
    while not s.meta()["is_over"]:
        s.end_day()

    out = tmp_path / "report.md"
    report = asyncio.run(score_session_module.score_session(
        tmp_path / "s", "mockllm/model", 1, out, REPO_ROOT / "judge" / "dimensions",
        model=_grader_model(),
    ))

    assert out.exists()
    assert report == out.read_text(encoding="utf-8")
    assert "actor: human" in report and "advisory" in report.lower()
    assert "## Judge pass" in report and "welfare_headline" in report


def test_score_session_debug_ever_banner(tmp_path):
    s = PlaySession.create(
        tmp_path / "s", corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=400, seed=1, mode="debug",
    )
    while not s.meta()["is_over"]:
        s.end_day()

    out = tmp_path / "report.md"
    report = asyncio.run(score_session_module.score_session(
        tmp_path / "s", "mockllm/model", 1, out, REPO_ROOT / "judge" / "dimensions",
        model=_grader_model(),
    ))

    assert ("> **debug_ever: true** — this session has used debug mode; "
            "it is not blind evidence.") in report


def test_score_session_grades_against_briefing_snapshot(tmp_path):
    # The scripted grader quotes "operations agent" from msg_0 (the briefing message). The
    # session is recorded under a briefing that contains that phrase; the source file is then
    # reworded to drop it (the 2026-07-28 case). Scoring must grade against the session's
    # briefing snapshot — grading against the live file fails msg_0 quote validation, the
    # sample is dropped, and every judged dimension collapses to 0.0.
    source = tmp_path / "briefing_v1.md"
    source.write_text("You are the operations agent. V1.\n", encoding="utf-8")
    s = PlaySession.create(
        tmp_path / "s", corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=source, episode_end_day=400, seed=1,
    )
    while not s.meta()["is_over"]:
        s.end_day()
    source.write_text("You are the farm operator. V2 — REWORDED.\n", encoding="utf-8")

    out = tmp_path / "report.md"
    report = asyncio.run(score_session_module.score_session(
        tmp_path / "s", "mockllm/model", 1, out, REPO_ROOT / "judge" / "dimensions",
        model=_grader_model(),
    ))
    assert "| welfare_decision_quality | 1.0 |" in report


def test_score_session_requires_snapshot(tmp_path):
    s = PlaySession.create(
        tmp_path / "s", corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=400, seed=1,
    )
    # no end_day() called yet -> no state.snapshot.json, and the episode is nowhere near
    # over -> PlaySession.resume() replays from day 0 fine, but state_for_report() gates
    # on is_over(), so scoring a not-yet-finished session still fails cleanly.
    out = tmp_path / "report.md"
    try:
        asyncio.run(score_session_module.score_session(
            tmp_path / "s", "mockllm/model", 1, out, REPO_ROOT / "judge" / "dimensions",
            model=_grader_model(),
        ))
        assert False, "expected an error when the session is not finished"
    except SystemExit:
        pass


def test_score_session_corrupt_snapshot(tmp_path):
    s = PlaySession.create(
        tmp_path / "s", corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=400, seed=1,
    )
    s.end_day()
    (tmp_path / "s" / "state.snapshot.json").write_text("{not valid json", encoding="utf-8")

    out = tmp_path / "report.md"
    try:
        asyncio.run(score_session_module.score_session(
            tmp_path / "s", "mockllm/model", 1, out, REPO_ROOT / "judge" / "dimensions",
            model=_grader_model(),
        ))
        assert False, "expected an error when the state snapshot is corrupt"
    except SystemExit:
        pass
