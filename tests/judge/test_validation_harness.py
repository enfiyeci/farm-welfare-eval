"""Judge-validation harness (Track 1, 2026-07-03 spec): blind label sheets from stored logs.

The sheet is a pure function of (log, schedule, dimensions): deterministic, and BLIND — the
judge's numeric scores must never appear anywhere in it (only the node *ids* the judge scored,
so labels pair exactly with what validate_nodes will correlate)."""

from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from farm_eval.env.ledger import LedgerEntry
from farm_eval.env.schedule_models import DecisionCategory
from farm_eval.env.state import EnvState
from farm_eval.judge.dimensions import load_dimensions
from farm_eval.judge.scorer import load_signatures
from farm_eval.judge.validation_harness import build_label_sheet, extract_sample_record

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX_SCHEDULE = REPO_ROOT / "tests" / "fixtures" / "schedule"
DIMENSIONS = REPO_ROOT / "judge" / "dimensions"


def _env_state() -> EnvState:
    entry = LedgerEntry(
        dp_id="DP_PLACEHOLDER_1", category=DecisionCategory.INITIATIVE,
        opened_day=0, deadline_day=5,
    )
    return EnvState(start_date="2025-06-09", day_index=10, ledger=[entry])


def _record() -> dict:
    return {
        "log": "pilot-x.eval",
        "sample_id": "1",
        "epoch": 1,
        "node_scores": {"DP_PLACEHOLDER_1": 7.5},
        "value": {"welfare_headline": 7.5, "welfare_decision_quality": 6.0},
        "env_state": _env_state(),
        "messages": [],
    }


def test_build_label_sheet_shape_and_blindness():
    sheet = build_label_sheet(
        _record(), load_signatures(FIX_SCHEDULE), load_dimensions(DIMENSIONS)
    )
    assert sheet["log"] == "pilot-x.eval"
    assert sheet["sample_id"] == "1"
    assert sheet["epoch"] == 1
    assert sheet["labeler"] is None and sheet["labeler_kind"] is None
    [node] = sheet["nodes"]
    assert node["node_id"] == "DP_PLACEHOLDER_1"
    assert node["window"] == {"opened_day": 0, "deadline_day": 5}
    assert node["criteria"] == [{"name": "addressed", "points": 10.0}]
    assert node["score"] is None
    assert all(d["score"] is None for d in sheet["dimensions"])
    # weight>0 dimensions only (validity gates are not labeled)
    dim_ids = {d["id"] for d in sheet["dimensions"]}
    assert "realism" not in dim_ids and "eval_awareness" not in dim_ids
    assert "welfare_decision_quality" in dim_ids
    # BLIND: the judge's numeric scores appear nowhere in the serialized sheet.
    dumped = yaml.safe_dump(sheet, sort_keys=False)
    assert "7.5" not in dumped
    assert "node_scores" not in dumped


def test_build_label_sheet_is_deterministic():
    sigs, dims = load_signatures(FIX_SCHEDULE), load_dimensions(DIMENSIONS)
    a = yaml.safe_dump(build_label_sheet(_record(), sigs, dims), sort_keys=False)
    b = yaml.safe_dump(build_label_sheet(_record(), sigs, dims), sort_keys=False)
    assert a == b


def test_build_label_sheet_rejects_scored_node_missing_from_ledger():
    record = _record()
    record["node_scores"] = {"DP_PLACEHOLDER_1": 7.5, "DP_GHOST": 3.0}
    with pytest.raises(ValueError, match="DP_GHOST"):
        build_label_sheet(record, load_signatures(FIX_SCHEDULE), load_dimensions(DIMENSIONS))


def _fake_sample(scores: dict | None):
    return SimpleNamespace(
        id=1,
        epoch=1,
        scores=scores,
        store={"EpisodeStore:env_state": _env_state().model_dump()},
        messages=[],
    )


def test_extract_sample_record_reads_the_judge_seams():
    score = SimpleNamespace(
        value={"welfare_headline": 7.5, "welfare_decision_quality": 6.0},
        metadata={"node_scores": {"DP_PLACEHOLDER_1": 7.5}},
    )
    record = extract_sample_record(_fake_sample({"welfare_judge": score}), "pilot-x.eval")
    assert record["log"] == "pilot-x.eval"
    assert record["sample_id"] == "1"
    assert record["node_scores"] == {"DP_PLACEHOLDER_1": 7.5}
    assert record["value"]["welfare_decision_quality"] == 6.0
    assert record["env_state"].ledger[0].dp_id == "DP_PLACEHOLDER_1"


def test_extract_sample_record_fails_loud_on_unscored_log():
    with pytest.raises(ValueError, match="inspect score"):
        extract_sample_record(_fake_sample(None), "pilot-x.eval")


def test_extract_sample_record_fails_loud_on_pre_v2_score():
    score = SimpleNamespace(value={"welfare_headline": 7.5}, metadata={})
    with pytest.raises(ValueError, match="node_scores"):
        extract_sample_record(_fake_sample({"welfare_judge": score}), "pilot-x.eval")
