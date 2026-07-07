"""Session-record → judge-message conversion (spec §6 tier 2)."""

import json
from pathlib import Path

from farm_eval.judge.scorer import render_transcript, transcript_index
from farm_eval.play.record import load_record, record_to_messages
from farm_eval.play.session import PlaySession

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"


def _session(tmp_path):
    s = PlaySession.create(
        tmp_path / "s", corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=400, seed=1,
    )
    s.note("raising vent before the heat")
    s.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0})
    s.end_day()
    return s


def test_conversion_shape_and_msg_ids(tmp_path):
    s = _session(tmp_path)
    msgs = record_to_messages(load_record(tmp_path / "s"), s.briefing())
    assert msgs[0].role == "user" and "operations agent" in msgs[0].text
    rendered = render_transcript(msgs)
    # the note is quotable assistant text; the tool call renders with its arguments
    assert "raising vent before the heat" in rendered
    assert "[tool_call adjust_setpoint" in rendered and '"ventilation"' in rendered
    # msg ids index the same content render_transcript shows (quote validation depends on this)
    index = transcript_index(msgs)
    note_ids = [mid for mid, text in index.items() if "raising vent" in text]
    assert note_ids, "note text must be addressable by a msg id"


def test_op_results_become_tool_messages(tmp_path):
    s = _session(tmp_path)
    msgs = record_to_messages(load_record(tmp_path / "s"), s.briefing())
    tool_texts = [m.text for m in msgs if m.role == "tool"]
    assert any("ventilation on H_SENSOR set to 1.0" in t for t in tool_texts)
    assert any("day(s) pass" in t for t in tool_texts)  # end_day summary
