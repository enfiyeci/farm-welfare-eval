"""Phase-1 result records and their on-disk form."""
from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from farm_eval.study.cells import Cell
from farm_eval.study.response import Decision
from farm_eval.study.sweep import Outcome


class RungRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    added_mortality_pp: float
    delta_deaths: float
    decisions: tuple[Decision, ...]
    accepted: bool


class CellResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    cell: Cell
    gain: float
    envelope: str
    outcome: Outcome
    interval: tuple[float, float] | None
    rung_records: tuple[RungRecord, ...]


def write_jsonl(results: list[CellResult], path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8") as fh:
        for r in results:
            fh.write(json.dumps(r.model_dump(mode="json")) + "\n")


def read_jsonl(path: str | Path) -> list[CellResult]:
    with Path(path).open(encoding="utf-8") as fh:
        return [CellResult.model_validate_json(line) for line in fh if line.strip()]
