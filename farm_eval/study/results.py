"""Phase-1 result records and their on-disk form."""
from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, model_validator

from farm_eval.study.cells import Cell
from farm_eval.study.response import Decision
from farm_eval.study.sweep import Outcome


class RungRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    added_mortality_pp: float
    delta_deaths: float
    decisions: tuple[Decision, ...]
    # The raw reply behind each decision, same order. The grading plan's
    # contamination / eval-awareness / premise-dispute checks are transcript-
    # based; a run that kept only the enum could never be graded.
    responses: tuple[str, ...]
    accepted: bool

    @model_validator(mode="after")
    def _one_response_per_decision(self) -> "RungRecord":
        # Enforced on every construction, including JSONL read: a record with
        # more decisions than responses would let a grader silently lose or
        # misattribute the evidence behind a decision.
        if len(self.responses) != len(self.decisions):
            raise ValueError(
                f"{len(self.decisions)} decision(s) but "
                f"{len(self.responses)} response(s); each decision needs its "
                "raw reply"
            )
        return self


class CellResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    cell: Cell
    gain: float
    envelope: str
    outcome: Outcome
    interval: tuple[float, float] | None
    rung_records: tuple[RungRecord, ...]

    @model_validator(mode="after")
    def _interval_matches_outcome(self) -> "CellResult":
        # "Never a number" held only on the write path; enforce it on every
        # construction, including deserialisation of hand-edited or corrupt JSONL.
        if self.outcome is Outcome.BRACKETED:
            if self.interval is None:
                raise ValueError("BRACKETED requires a numeric interval")
        elif self.interval is not None:
            raise ValueError(
                f"{self.outcome.value} is not a threshold value and must not "
                "carry an interval"
            )
        return self


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
