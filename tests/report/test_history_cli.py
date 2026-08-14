from __future__ import annotations

import json
from pathlib import Path

from farm_eval.report.history import history_row, load_history, update_history


def test_history_update_is_idempotent_and_sorted(tmp_path: Path, report_model: dict) -> None:
    path = tmp_path / "pilot-history.json"
    first = history_row(report_model)
    update_history(path, first)
    changed = {**first, "headline": 9.0}
    update_history(path, changed)
    rows = load_history(path)
    assert len(rows) == 1
    assert rows[0]["sha256"] == "a" * 64
    assert rows[0]["headline"] == 9.0
    assert json.loads(path.read_text()) == rows


def test_history_row_contains_trend_contract(report_model: dict) -> None:
    row = history_row(report_model)
    assert row["sha256"] == "a" * 64
    assert row["headline"] == 8.0
    assert row["dimensions"]["proactive_monitoring"] == 7.0
    assert row["tripwires"] == 0.0
    assert row["model"] == "target/current"


def test_history_row_carries_the_finance_index(report_model: dict) -> None:
    report_model["judge"]["finance_index"] = {
        "components": {"margin_capture": 0.62, "cash_hygiene": 0.9},
        "composite": 0.71,
    }
    row = history_row(report_model)
    assert row["finance_composite"] == 0.71
    assert row["finance_components"]["margin_capture"] == 0.62
    # A separate axis: it must never leak into the judge-dimension trend series.
    assert "finance_index" not in row["dimensions"]


def test_history_row_reads_not_measured_when_the_axis_is_disabled(report_model: dict) -> None:
    """An axis-disabled run and a pre-axis log both carry no index. `None`, never 0.0 — a row
    reading 0.0 would plot as a real (bad) finance score in the trend."""
    report_model["judge"].pop("finance_index", None)
    row = history_row(report_model)
    assert row["finance_composite"] is None
    assert row["finance_components"] == {}


def test_history_row_ignores_a_finance_index_that_lands_in_scores(report_model: dict) -> None:
    """Defensive: `_NON_DIMENSIONS` keeps a nested index dict out of the float-only trend series
    even if a later change writes it into `scores`."""
    report_model["scores"]["finance_index"] = {"composite": 0.5}
    assert "finance_index" not in history_row(report_model)["dimensions"]
