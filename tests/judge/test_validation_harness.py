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


# --- Task 4: filled sheets -> pairing -> rho report -------------------------------------------

import math

from farm_eval.judge.validation_harness import (
    load_filled_sheet,
    render_report,
    validation_result,
)


def _rec(sample_id: str, node_scores: dict, value: dict) -> dict:
    return {
        "log": "pilot-x.eval", "sample_id": sample_id, "epoch": 1,
        "node_scores": node_scores, "value": value,
        "env_state": None, "messages": [],  # not read by validation_result
    }


def _sheet(sample_id: str, node_labels: dict, dim_labels: dict, kind: str = "expert") -> dict:
    return {
        "log": "pilot-x.eval", "sample_id": sample_id, "epoch": 1,
        "labeler": "dr-vet", "labeler_kind": kind,
        "nodes": [{"node_id": k, "score": v} for k, v in node_labels.items()],
        "dimensions": [{"id": k, "score": v} for k, v in dim_labels.items()],
    }


def _monotonic_fixture(n: int = 5):
    """n transcripts where human labels rank exactly like the judge -> rho 1.0."""
    records, sheets = [], []
    for i in range(n):
        records.append(_rec(str(i), {"DP_A": float(i)}, {"welfare_decision_quality": float(i)}))
        sheets.append(_sheet(str(i), {"DP_A": float(i * 2)}, {"welfare_decision_quality": float(i * 2)}))
    return records, sheets


def test_validation_result_perfect_monotonic_rho():
    records, sheets = _monotonic_fixture()
    result = validation_result(records, sheets)
    assert result["labeler_kind"] == "expert"
    assert result["n_transcripts"] == 5
    assert result["node_rho"]["DP_A"] == pytest.approx(1.0)
    assert result["node_pairs"]["DP_A"] == 5
    assert result["dimension_rho"]["welfare_decision_quality"] == pytest.approx(1.0)


def test_validation_result_null_scores_drop_the_pair():
    records, sheets = _monotonic_fixture()
    sheets[0]["nodes"][0]["score"] = None  # unlabeled cell -> that pair drops, no crash
    result = validation_result(records, sheets)
    assert result["node_pairs"]["DP_A"] == 4


def test_validation_result_mixed_labeler_kind_raises():
    records, sheets = _monotonic_fixture()
    sheets[0]["labeler_kind"] = "proxy"
    with pytest.raises(ValueError, match="mixed labeler_kind"):
        validation_result(records, sheets)


def test_validation_result_label_for_unscored_node_raises():
    records, sheets = _monotonic_fixture()
    sheets[0]["nodes"].append({"node_id": "DP_GHOST", "score": 5.0})
    with pytest.raises(ValueError, match="DP_GHOST"):
        validation_result(records, sheets)


def test_validation_result_unmatched_sheet_raises():
    records, sheets = _monotonic_fixture()
    sheets[0]["sample_id"] = "999"
    with pytest.raises(ValueError, match="no matching scored log"):
        validation_result(records, sheets)


def test_validation_result_single_transcript_dimensions_are_nan_not_crash():
    records, sheets = _monotonic_fixture(1)
    result = validation_result(records, sheets)
    assert math.isnan(result["dimension_rho"]["welfare_decision_quality"])
    assert math.isnan(result["node_rho"]["DP_A"])  # <2 pairs: validate_nodes reports NaN


def test_load_filled_sheet_requires_labeler_fields(tmp_path):
    sheet = _sheet("0", {"DP_A": 5.0}, {})
    sheet["labeler_kind"] = None
    p = tmp_path / "s.yml"
    p.write_text(yaml.safe_dump(sheet), encoding="utf-8")
    with pytest.raises(ValueError, match="labeler_kind"):
        load_filled_sheet(p)


def test_load_filled_sheet_rejects_nonfinite_label(tmp_path):
    sheet = _sheet("0", {"DP_A": float("nan")}, {})
    p = tmp_path / "s.yml"
    p.write_text(yaml.safe_dump(sheet), encoding="utf-8")
    with pytest.raises(ValueError, match="finite"):
        load_filled_sheet(p)


def test_render_report_verdicts_and_proxy_disclaimer():
    records, sheets = _monotonic_fixture()
    for s in sheets:
        s["labeler_kind"] = "proxy"
    report = render_report(validation_result(records, sheets))
    assert "PROXY" in report                 # proxy labels never satisfy the gate
    assert "UNDERPOWERED" in report          # 5 transcripts but MIN_PAIRS=5 -> node at boundary passes; see below
    assert "| DP_A |" in report
    assert "welfare_decision_quality" in report


def test_render_report_expert_has_no_proxy_disclaimer_and_marks_pass():
    records, sheets = _monotonic_fixture(6)
    report = render_report(validation_result(records, sheets))
    assert "PROXY" not in report
    assert "PASS" in report


def test_render_report_underpowered_dimension_never_passes():
    # 3 expert transcripts: dimension rho is computable (1.0) but under MIN_PAIRS —
    # the verdict must be UNDERPOWERED, never PASS (the anti-laundering guarantee).
    records, sheets = _monotonic_fixture(3)
    report = render_report(validation_result(records, sheets))
    dim_row = next(l for l in report.splitlines() if l.startswith("| welfare_decision_quality |"))
    assert "UNDERPOWERED" in dim_row
    assert "PASS" not in dim_row


# --- Codex adversarial review hardening --------------------------------------------------------


def test_extract_sample_record_rejects_partial_run():
    score = SimpleNamespace(
        value={"welfare_headline": 7.5},
        metadata={
            "node_scores": {"DP_PLACEHOLDER_1": 7.5},
            "partial_run": True,
            "scored_through_day": 3,
            "episode_end_day": 400,
        },
    )
    with pytest.raises(ValueError, match="partial"):
        extract_sample_record(_fake_sample({"welfare_judge": score}), "pilot-x.eval")


def test_validation_result_unlabeled_judge_node_stays_visible():
    records, sheets = _monotonic_fixture()
    for r in records:
        r["node_scores"]["DP_B"] = 5.0  # judge scores it; no sheet ever labels it
    result = validation_result(records, sheets)
    assert result["node_pairs"]["DP_B"] == 0
    assert math.isnan(result["node_rho"]["DP_B"])
    report = render_report(result)
    assert "| DP_B | 0 |" in report


def test_load_filled_sheet_rejects_bool_score(tmp_path):
    sheet = _sheet("0", {"DP_A": True}, {})
    p = tmp_path / "s.yml"
    p.write_text(yaml.safe_dump(sheet), encoding="utf-8")
    with pytest.raises(ValueError, match="0-10"):
        load_filled_sheet(p)


def test_load_filled_sheet_rejects_score_above_10(tmp_path):
    sheet = _sheet("0", {"DP_A": 999}, {})
    p = tmp_path / "s.yml"
    p.write_text(yaml.safe_dump(sheet), encoding="utf-8")
    with pytest.raises(ValueError, match="0-10"):
        load_filled_sheet(p)


def test_load_filled_sheet_rejects_negative_score(tmp_path):
    sheet = _sheet("0", {"DP_A": -3}, {})
    p = tmp_path / "s.yml"
    p.write_text(yaml.safe_dump(sheet), encoding="utf-8")
    with pytest.raises(ValueError, match="0-10"):
        load_filled_sheet(p)


def test_load_filled_sheet_rejects_duplicate_node_id(tmp_path):
    sheet = _sheet("0", {"DP_A": 5.0}, {})
    sheet["nodes"].append({"node_id": "DP_A", "score": 6.0})
    p = tmp_path / "s.yml"
    p.write_text(yaml.safe_dump(sheet), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        load_filled_sheet(p)


def test_load_filled_sheet_rejects_duplicate_dimension_id(tmp_path):
    sheet = _sheet("0", {}, {"welfare_decision_quality": 5.0})
    sheet["dimensions"].append({"id": "welfare_decision_quality", "score": 6.0})
    p = tmp_path / "s.yml"
    p.write_text(yaml.safe_dump(sheet), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        load_filled_sheet(p)


def test_validation_result_rejects_duplicate_sheet_key():
    records, sheets = _monotonic_fixture()
    sheets.append(dict(sheets[0]))  # same (log, sample_id, epoch) as an existing sheet
    with pytest.raises(ValueError, match="duplicate"):
        validation_result(records, sheets)


def test_validation_result_dimension_null_cell_drops_only_that_pair():
    # 5 monotonic sheets, one dimension cell nulled: pairs == 4, rho still computed
    # (never dropped), verdict UNDERPOWERED (below MIN_PAIRS=5).
    records, sheets = _monotonic_fixture(5)
    sheets[0]["dimensions"][0]["score"] = None
    result = validation_result(records, sheets)
    assert result["dimension_pairs"]["welfare_decision_quality"] == 4
    assert not math.isnan(result["dimension_rho"]["welfare_decision_quality"])
    report = render_report(result)
    dim_row = next(l for l in report.splitlines() if l.startswith("| welfare_decision_quality |"))
    assert "UNDERPOWERED" in dim_row


def test_validation_result_label_for_unscored_dimension_raises():
    records, sheets = _monotonic_fixture()
    sheets[0]["dimensions"].append({"id": "GHOST", "score": 5.0})
    with pytest.raises(ValueError, match="GHOST"):
        validation_result(records, sheets)
