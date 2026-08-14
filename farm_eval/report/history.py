"""Idempotent all-round pilot history storage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# Keys in `scores` that are NOT judge dimensions. `finance_index` is listed defensively: the L8
# index rides in judge METADATA today (`report_model["judge"]["finance_index"]`), and if a later
# change ever writes it into `scores` it must not be picked up as a dimension — the trend chart
# plots the dimensions dict as floats, and the index is a nested
# {"components": {...}, "composite": float} dict.
_NON_DIMENSIONS = {"welfare_headline", "welfare_state", "tripwires_observed", "finance_index"}


def history_row(report_model: dict[str, Any]) -> dict[str, Any]:
    source, run, scores = report_model["source"], report_model["run"], report_model["scores"]
    # L8 financial-skill axis. Absent on an axis-disabled (`finance_enabled: false`) run and on
    # every log written before the axis existed, so the composite stays None rather than 0.0 — a
    # row with no finance data must read as "not measured", never as "measured and scored zero".
    finance = report_model.get("judge", {}).get("finance_index") or {}
    return {
        "sha256": source["sha256"],
        "date": source.get("created") or run.get("started_at"),
        "model": run.get("target_model"),
        "grader_model": run.get("grader_model"),
        "headline": scores.get("welfare_headline"),
        "welfare_state": scores.get("welfare_state"),
        "tripwires": scores.get("tripwires_observed"),
        "finance_composite": finance.get("composite"),
        "finance_components": dict(finance.get("components") or {}),
        "dimensions": {key: value for key, value in scores.items() if key not in _NON_DIMENSIONS},
    }


def load_history(path: str | Path) -> list[dict[str, Any]]:
    history_path = Path(path)
    if not history_path.exists():
        return []
    value = json.loads(history_path.read_text())
    if not isinstance(value, list):
        raise ValueError("pilot history must be a JSON array")
    return value


def update_history(path: str | Path, row: dict[str, Any]) -> list[dict[str, Any]]:
    history_path = Path(path)
    rows = {item["sha256"]: item for item in load_history(history_path)}
    rows[row["sha256"]] = row
    result = sorted(rows.values(), key=lambda item: (item.get("date") or "", item["sha256"]))
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result
