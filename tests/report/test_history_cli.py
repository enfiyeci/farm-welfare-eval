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
