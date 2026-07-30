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


def test_resume_then_advance_survives_the_real_corpus(tmp_path):
    """Resume must be able to ADVANCE, not merely rebuild.

    The rest of this module runs against `tests/fixtures/corpus`, which ships no `weather.yml`.
    That blinded the suite to a real defect: `resume()` overwrites every state field from the
    JSON snapshot, and JSON keys are strings, so `weather["monthly_normals_f"]` came back keyed
    "1".."12" and the next `end_day()` died in `make_ambient` on `normals[7]`. A human player hit
    it on the first resume after any completed day. Pinned against the REAL corpus because the
    fixture corpus cannot express the regression.
    """
    kw = dict(
        corpus_path=REPO_ROOT / "corpus", schedule_path=REPO_ROOT / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=40, seed=0,
    )
    s = PlaySession.create(tmp_path / "real", **kw)
    s.end_day()  # writes the autosave snapshot
    del s

    resumed = PlaySession.resume(tmp_path / "real")
    assert set(resumed._env.state.weather["monthly_normals_f"]) >= {1, 7}
    result = resumed.end_day()  # the advance that used to raise KeyError: 7
    assert result["new_day"] > 0


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


def test_failed_debug_resume_does_not_stamp_debug_ever(tmp_path):
    """A debug resume that dies on a corrupt snapshot must not taint the session:
    no debug data was ever exposed, so `debug_ever` must stay False and the
    session remains usable as blind evidence."""
    s = PlaySession.create(tmp_path / "s", **KW)
    s.end_day()
    (tmp_path / "s" / "state.snapshot.json").write_text("{truncated", encoding="utf-8")
    with pytest.raises(ValueError, match="snapshot"):
        PlaySession.resume(tmp_path / "s", mode="debug")
    meta = yaml.safe_load((tmp_path / "s" / "meta.yml").read_text(encoding="utf-8"))
    assert meta["debug_ever"] is False


def test_failed_replay_on_debug_resume_does_not_stamp_debug_ever(tmp_path):
    """Same guarantee when the failure comes later, from a malformed session.jsonl
    tail record: the stamp lands only after replay completes."""
    s = PlaySession.create(tmp_path / "s", **KW)
    s.end_day()
    with (tmp_path / "s" / "session.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"seq": 99, "kind": "op", "op": "no_such_op", "params": {}}) + "\n")
    with pytest.raises(KeyError):
        PlaySession.resume(tmp_path / "s", mode="debug")
    meta = yaml.safe_load((tmp_path / "s" / "meta.yml").read_text(encoding="utf-8"))
    assert meta["debug_ever"] is False


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
