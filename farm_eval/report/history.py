"""Idempotent all-round pilot history storage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


_NON_DIMENSIONS = {"welfare_headline", "welfare_state", "tripwires_observed"}


def history_row(report_model: dict[str, Any]) -> dict[str, Any]:
    source, run, scores = report_model["source"], report_model["run"], report_model["scores"]
    return {
        "sha256": source["sha256"],
        "date": source.get("created") or run.get("started_at"),
        "model": run.get("target_model"),
        "grader_model": run.get("grader_model"),
        "headline": scores.get("welfare_headline"),
        "welfare_state": scores.get("welfare_state"),
        "tripwires": scores.get("tripwires_observed"),
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
