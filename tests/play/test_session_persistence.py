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


def _interrupt_meta_writes(monkeypatch):
    """Make every write targeting a meta file write half its data, then die.

    Simulates a crash/short write mid-write. An atomic (tmp + os.replace) writer
    only ever exposes the partial data in the tmp file; an in-place writer
    truncates meta.yml itself.
    """
    real = Path.write_text
    def interrupted(self, data, *args, **kwargs):
        if "meta" in self.name:
            real(self, data[: len(data) // 2], *args, **kwargs)
            raise OSError("simulated interrupted write")
        return real(self, data, *args, **kwargs)
    monkeypatch.setattr(Path, "write_text", interrupted)


def test_interrupted_initial_meta_write_leaves_no_truncated_meta(tmp_path, monkeypatch):
    _interrupt_meta_writes(monkeypatch)
    with pytest.raises(OSError, match="interrupted"):
        PlaySession.create(tmp_path / "s", **KW)
    # no half-written meta.yml may exist — it would poison every later resume
    assert not (tmp_path / "s" / "meta.yml").exists()


def test_interrupted_debug_stamp_leaves_meta_intact(tmp_path, monkeypatch):
    s = PlaySession.create(tmp_path / "s", **KW)
    s.end_day()
    before = (tmp_path / "s" / "meta.yml").read_text(encoding="utf-8")
    _interrupt_meta_writes(monkeypatch)
    with pytest.raises(OSError, match="interrupted"):
        PlaySession.resume(tmp_path / "s", mode="debug")
    assert (tmp_path / "s" / "meta.yml").read_text(encoding="utf-8") == before


def test_meta_writes_leave_no_tmp_residue(tmp_path):
    s = PlaySession.create(tmp_path / "s", **KW)
    s.end_day()
    PlaySession.resume(tmp_path / "s", mode="debug")
    residue = [p.name for p in (tmp_path / "s").iterdir() if p.name.endswith(".tmp")]
    assert residue == []


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


def test_resume_tolerates_torn_final_line(tmp_path):
    """A crash mid-append leaves a truncated final JSONL line. That record never became
    durable, so resume drops it (with a loud warning) and replays from the last complete
    record — the session must not require manual log surgery."""
    a = PlaySession.create(tmp_path / "a", **KW)
    _play_script(a)
    straight = a._env.state.model_dump(mode="json")

    b = PlaySession.create(tmp_path / "b", **KW)
    b.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.2})
    b.end_day()
    b.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.4})
    del b
    with (tmp_path / "b" / "session.jsonl").open("a", encoding="utf-8") as fh:
        fh.write('{"seq": 99, "kind": "op", "op": "adjust_setp')  # torn: no closing, no newline
    with pytest.warns(RuntimeWarning, match="torn"):
        r = PlaySession.resume(tmp_path / "b")
    r.end_day()
    assert r._env.state.model_dump(mode="json") == straight


def test_torn_final_line_is_truncated_from_the_log(tmp_path):
    """Repair must remove the torn line from disk: a later plain append would otherwise
    concatenate onto the partial line and corrupt the NEXT record too."""
    s = PlaySession.create(tmp_path / "s", **KW)
    _play_script(s)
    log = tmp_path / "s" / "session.jsonl"
    n_good = len(log.read_text(encoding="utf-8").splitlines())
    with log.open("a", encoding="utf-8") as fh:
        fh.write('{"seq": 99, "kind"')
    with pytest.warns(RuntimeWarning, match="torn"):
        r = PlaySession.resume(tmp_path / "s")
    r.note("post-repair")
    records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    assert [rec["seq"] for rec in records] == list(range(n_good + 1))


def test_resume_tolerates_torn_final_line_inside_a_utf8_codepoint(tmp_path):
    """Records are written with ensure_ascii=False, so the log carries raw UTF-8 and a
    crash can tear the final line midway through a multibyte character. That must repair
    like any torn line, not die in UnicodeDecodeError before the repair logic runs."""
    s = PlaySession.create(tmp_path / "s", **KW)
    _play_script(s)
    log = tmp_path / "s" / "session.jsonl"
    n_good = len(log.read_text(encoding="utf-8").splitlines())
    with log.open("ab") as fh:
        fh.write('{"seq": 99, "kind": "note", "text": "café'.encode("utf-8")[:-1])  # cut mid-é
    with pytest.warns(RuntimeWarning, match="torn"):
        PlaySession.resume(tmp_path / "s")
    records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    assert len(records) == n_good


def test_mid_file_corruption_still_fails_loud(tmp_path):
    """Only the FINAL line can be a torn append; corruption anywhere else is real
    damage and must not be silently dropped."""
    s = PlaySession.create(tmp_path / "s", **KW)
    _play_script(s)
    log = tmp_path / "s" / "session.jsonl"
    lines = log.read_text(encoding="utf-8").splitlines()
    lines[1] = '{"seq": 1, "kind"'
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="corrupt session record"):
        PlaySession.resume(tmp_path / "s")


def test_blank_interior_line_fails_loud(tmp_path):
    """The writer never emits blank lines, so a blank INTERIOR line is real corruption:
    silently skipping it would make _count_records undercount and a later append could
    reuse an existing seq, breaking the snapshot-tail replay filter."""
    s = PlaySession.create(tmp_path / "s", **KW)
    _play_script(s)
    log = tmp_path / "s" / "session.jsonl"
    raw = log.read_bytes()
    first_nl = raw.index(b"\n")
    log.write_bytes(raw[: first_nl + 1] + b"\n" + raw[first_nl + 1 :])
    with pytest.raises(ValueError, match="blank line"):
        PlaySession.resume(tmp_path / "s")


def test_missing_final_newline_is_repaired(tmp_path):
    """A crash can also land exactly between the JSON bytes and the newline: the final
    record is complete and must be KEPT, but the newline must be restored so the next
    append starts on a fresh line instead of merging into it."""
    s = PlaySession.create(tmp_path / "s", **KW)
    _play_script(s)
    log = tmp_path / "s" / "session.jsonl"
    log.write_text(log.read_text(encoding="utf-8").rstrip("\n"), encoding="utf-8")
    r = PlaySession.resume(tmp_path / "s")
    r.note("after")
    records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    assert records[-1] == {"seq": len(records) - 1, "kind": "note",
                           "day_index": r.meta()["day_index"], "text": "after"}


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
