"""`scripts/gen_pilot_report.py`'s pairing guard.

`--behaviour` takes a behaviour model built from some log; the positional argument is the log
being reported. Nothing forced those to be the SAME log, and a mismatched pair renders a report
whose judge layer and whose behaviour layer describe different runs with nothing on the page to
say so. The guard is a hash comparison, so it is tested against files rather than real `.eval`
logs: `_load_behaviour` hashes whatever bytes it is given, exactly as `report.extract` does.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from farm_eval.analysis.model import BehaviourModel
from scripts.gen_pilot_report import _load_behaviour


def _model(sha: str) -> BehaviourModel:
    return BehaviourModel(
        source_sha256=sha,
        target_model="target/placeholder",
        feed_fidelity="full",
        day_map_valid=True,
        thresholds={},
        dossiers=[],
        tool_profiles=[],
        offnode_findings=[],
        digest=[],
    )


def _write(tmp_path: Path, name: str, content: bytes) -> Path:
    path = tmp_path / name
    path.write_bytes(content)
    return path


def test_a_behaviour_model_built_from_another_log_is_refused(tmp_path: Path) -> None:
    log = _write(tmp_path, "current.eval", b"the log being reported")
    other = _write(tmp_path, "other.eval", b"a different run entirely")
    model_path = tmp_path / "behaviour_model.json"
    model_path.write_text(
        _model(hashlib.sha256(other.read_bytes()).hexdigest()).model_dump_json()
    )

    with pytest.raises(SystemExit) as exit_info:
        _load_behaviour(model_path, log)

    message = str(exit_info.value)
    assert hashlib.sha256(other.read_bytes()).hexdigest() in message   # what the model records
    assert hashlib.sha256(log.read_bytes()).hexdigest() in message     # what the log actually is
    assert "current.eval" in message


def test_a_matching_pair_loads(tmp_path: Path) -> None:
    log = _write(tmp_path, "current.eval", b"the log being reported")
    model_path = tmp_path / "behaviour_model.json"
    sha = hashlib.sha256(log.read_bytes()).hexdigest()
    model_path.write_text(_model(sha).model_dump_json())

    assert _load_behaviour(model_path, log).source_sha256 == sha
