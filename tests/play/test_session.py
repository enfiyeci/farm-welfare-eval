"""PlaySession: recording, end_day, blind/debug enforcement (spec §3/§5/§7)."""

import json
from pathlib import Path

import pytest

from farm_eval.play.session import EpisodeOver, PlaySession

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"


def _session(tmp_path, mode="blind") -> PlaySession:
    return PlaySession.create(
        tmp_path / "s1",
        corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=400, seed=1, mode=mode,
    )


def _records(session_dir: Path) -> list[dict]:
    lines = (session_dir / "session.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(l) for l in lines]


def test_call_records_op_and_returns_result(tmp_path):
    s = _session(tmp_path)
    out = s.call("get_datetime", {})
    assert out.startswith("day ")
    recs = _records(tmp_path / "s1")
    assert recs[-1]["kind"] == "op" and recs[-1]["op"] == "get_datetime"
    assert recs[-1]["result"] == out and recs[-1]["seq"] == len(recs) - 1


def test_call_validates_against_registry(tmp_path):
    s = _session(tmp_path)
    with pytest.raises(KeyError):
        s.call("read_ledger", {})
    with pytest.raises(ValueError, match="required"):
        s.call("read_sensor", {"house_id": "H_SENSOR"})  # missing required `metric`
    with pytest.raises(ValueError, match="unknown parameter"):
        s.call("get_datetime", {"verbose": True})


def test_end_day_records_and_advances(tmp_path):
    s = _session(tmp_path)
    before = s.meta()["day_index"]
    out = s.end_day()
    assert out["new_day"] > before
    day_recs = [r for r in _records(tmp_path / "s1") if r["kind"] == "day"]
    assert day_recs and day_recs[-1]["new_day"] == out["new_day"]


def test_action_after_horizon_raises_episode_over(tmp_path):
    s = _session(tmp_path)
    while not s.meta()["is_over"]:
        s.end_day()
    with pytest.raises(EpisodeOver):
        s.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0})
    # reads stay allowed after the horizon (reviewing the final state is not acting in it)
    assert s.call("get_datetime", {})


def test_note_records(tmp_path):
    s = _session(tmp_path)
    s.note("H_SENSOR vent low, raising a stage")
    recs = _records(tmp_path / "s1")
    assert recs[-1] == {
        "seq": recs[-1]["seq"], "kind": "note",
        "day_index": s.meta()["day_index"], "text": "H_SENSOR vent low, raising a stage",
    }


def test_blind_session_denies_debug_accessors(tmp_path):
    s = _session(tmp_path)
    for accessor in (s.ledger, s.env_snapshot, s.schedule_preview):
        with pytest.raises(PermissionError):
            accessor()


def test_debug_session_serves_accessors(tmp_path):
    s = _session(tmp_path, mode="debug")
    assert isinstance(s.ledger(), list)
    assert s.env_snapshot()["day_index"] == s.meta()["day_index"]
    assert isinstance(s.schedule_preview(), list)


def test_briefing_returns_operator_briefing(tmp_path):
    assert "operations agent" in _session(tmp_path).briefing()


def test_blind_session_has_no_public_env_handle(tmp_path):
    s = _session(tmp_path)
    assert not hasattr(s, "env")   # no public raw-env handle
    with pytest.raises(PermissionError):
        s.state_for_report()       # mid-play terminal-state access is refused
