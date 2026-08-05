"""Phase-1 runner: map the stated-preference surface (spec §11.4).

Free, non-agentic, deliberately over-sampled. The surface is a primary deliverable in
its own right, not only a targeting device for phase 2.
"""
from __future__ import annotations

from typing import Sequence

from farm_eval.study.cells import Cell, framing_cells
from farm_eval.study.offer import build_offer
from farm_eval.study.params import GAIN_LADDER, Rung, envelope_status, rungs_for
from farm_eval.study.prompt import build_p1_prompt
from farm_eval.study.provider import TextProvider
from farm_eval.study.response import parse_decision
from farm_eval.study.results import CellResult, RungRecord
from farm_eval.study.sweep import SweepRules, run_sweep


def run_phase1(
    provider: TextProvider,
    cells: Sequence[Cell] | None = None,
    gains: Sequence[float] | None = None,
    rules: SweepRules | None = None,
) -> list[CellResult]:
    cells = list(cells if cells is not None else framing_cells())
    gains = list(gains if gains is not None else GAIN_LADDER)
    rules = rules or SweepRules()

    out: list[CellResult] = []
    for cell in cells:
        rungs = rungs_for(cell.species, cell.standard)
        for gain in gains:

            def evaluate(rung: Rung, replicate: int, _c=cell, _g=gain):
                offer = build_offer(_c, rung, _g)
                return parse_decision(provider.complete(build_p1_prompt(offer)))

            result = run_sweep(rungs, evaluate, rules)
            records = tuple(
                RungRecord(
                    added_mortality_pp=rungs[rr.index].added_mortality_pp,
                    delta_deaths=build_offer(cell, rungs[rr.index], gain).delta_deaths,
                    decisions=rr.decisions,
                    accepted=rr.accepted,
                )
                for rr in result.rung_results
            )
            out.append(CellResult(
                cell=cell,
                gain=gain,
                envelope=envelope_status(cell.species, gain),
                outcome=result.outcome,
                interval=result.interval,
                rung_records=records,
            ))
    return out
