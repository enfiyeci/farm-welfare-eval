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


def dump_jsonl_line(result: CellResult) -> str:
    """The single on-disk line form — shared by batch and incremental writers so
    the two can never drift apart."""
    return json.dumps(result.model_dump(mode="json")) + "\n"


def write_jsonl(results: list[CellResult], path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8") as fh:
        for r in results:
            fh.write(dump_jsonl_line(r))


def read_jsonl(path: str | Path) -> list[CellResult]:
    with Path(path).open(encoding="utf-8") as fh:
        return [CellResult.model_validate_json(line) for line in fh if line.strip()]
