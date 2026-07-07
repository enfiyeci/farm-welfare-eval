"""Autosave/resume determinism + the permanent debug stamp (spec §5/§7)."""

import json
from pathlib import Path

import pytest
import yaml

from farm_eval.play.session import PlaySession

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"
KW = dict(
    corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
    briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
    episode_end_day=400, seed=1,
)


def _play_script(s: PlaySession) -> None:
    s.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.2})
    s.end_day()
    s.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.4})
    s.end_day()


def test_autosave_writes_snapshot_on_end_day(tmp_path):
    s = PlaySession.create(tmp_path / "s", **KW)
    s.end_day()
    snap = json.loads((tmp_path / "s" / "state.snapshot.json").read_text(encoding="utf-8"))
    assert snap["env_state"]["day_index"] == s.meta()["day_index"]


def test_resume_reproduces_straight_through_state(tmp_path):
    a = PlaySession.create(tmp_path / "a", **KW)
    _play_script(a)
    straight = a._env.state.model_dump(mode="json")

    b = PlaySession.create(tmp_path / "b", **KW)
    b.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.2})
    b.end_day()
    # simulate a mid-day tail after the last snapshot, then a process death
    b.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.4})
    del b
    r = PlaySession.resume(tmp_path / "b")
    r.end_day()
    assert r._env.state.model_dump(mode="json") == straight


def test_resume_does_not_duplicate_records(tmp_path):
    s = PlaySession.create(tmp_path / "s", **KW)
    _play_script(s)
    n = len((tmp_path / "s" / "session.jsonl").read_text(encoding="utf-8").splitlines())
    PlaySession.resume(tmp_path / "s")
    n2 = len((tmp_path / "s" / "session.jsonl").read_text(encoding="utf-8").splitlines())
    assert n2 == n  # replay re-executes, never re-records


def test_debug_stamp_is_permanent(tmp_path):
    s = PlaySession.create(tmp_path / "s", **KW)
    s.end_day()
    PlaySession.resume(tmp_path / "s", mode="debug")
    meta = yaml.safe_load((tmp_path / "s" / "meta.yml").read_text(encoding="utf-8"))
    assert meta["debug_ever"] is True
    # reopening blind does NOT unstamp
    PlaySession.resume(tmp_path / "s")
    meta2 = yaml.safe_load((tmp_path / "s" / "meta.yml").read_text(encoding="utf-8"))
    assert meta2["debug_ever"] is True


def test_resume_blind_on_debug_session_stays_blind_but_stamped(tmp_path):
    s = PlaySession.create(tmp_path / "s", mode="debug", **KW)
    s.end_day()
    r = PlaySession.resume(tmp_path / "s", mode="blind")
    assert r.meta()["mode"] == "blind"
    meta = yaml.safe_load((tmp_path / "s" / "meta.yml").read_text(encoding="utf-8"))
    assert meta["debug_ever"] is True


@pytest.mark.parametrize("snapshot_content", [
    "{truncated",
    "null",
    "[]",
    "{}",
    '{"seq": 1, "env_state": {"day_index": "not-a-state"}}',
])
def test_corrupt_snapshot_fails_loud(tmp_path, snapshot_content):
    s = PlaySession.create(tmp_path / "s", **KW)
    s.end_day()
    (tmp_path / "s" / "state.snapshot.json").write_text(snapshot_content, encoding="utf-8")
    with pytest.raises(ValueError, match="snapshot"):
        PlaySession.resume(tmp_path / "s")
