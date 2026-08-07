"""Phase-1 runner: map the stated-preference surface (spec §11.4).

Free, non-agentic, deliberately over-sampled. The surface is a primary deliverable in
its own right, not only a targeting device for phase 2.
"""
from __future__ import annotations

from typing import Callable, Sequence

from farm_eval.study.cells import Cell, framing_cells
from farm_eval.study.documents import parse_survival_projections
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
    on_result: Callable[[CellResult], None] | None = None,
    rungs_provider: Callable[[Cell], Sequence[Rung]] | None = None,
    on_call: Callable[..., None] | None = None,
    prompt_builder: Callable[[object], str] | None = None,
) -> list[CellResult]:
    """Sweep every cell x gain. `on_result` fires as each CellResult completes, so
    callers can persist incrementally — a provider failure late in the 384-call
    sweep must not cost the results already gathered.

    `rungs_provider` overrides the preregistered ladder. It exists so an explicitly
    abstract probe (spec §3.1) reuses this path — and its record/prompt consistency
    check — instead of duplicating the loop. The default IS the preregistration."""
    cells = list(cells if cells is not None else framing_cells())
    gains = list(gains if gains is not None else GAIN_LADDER)
    rules = rules or SweepRules()
    rungs_provider = rungs_provider or (
        lambda cell: rungs_for(cell.species, cell.standard))
    # One builder for BOTH the model's prompt and the consistency check below, so a
    # cost-support arm can never be shown to the model but absent from verification.
    prompt_builder = prompt_builder or build_p1_prompt

    out: list[CellResult] = []
    for cell in cells:
        rungs = tuple(rungs_provider(cell))
        for gain in gains:

            raw: dict[tuple[Rung, int], str] = {}

            def evaluate(rung: Rung, replicate: int, _c=cell, _g=gain, _raw=raw):
                offer = build_offer(_c, rung, _g)
                text = provider.complete(prompt_builder(offer))
                _raw[(rung, replicate)] = text
                decision = parse_decision(text)
                if on_call is not None:
                    # Watcher hook: fires per call so a long sweep can be followed
                    # live. Observation only — it cannot change what is recorded.
                    on_call(cell=_c, gain=_g, rung=rung, replicate=replicate,
                            offer=offer, decision=decision, response=text)
                return decision

            result = run_sweep(rungs, evaluate, rules)
            records = []
            for rr in result.rung_results:
                offer = build_offer(cell, rungs[rr.index], gain)
                # The offer is built here and inside `evaluate` from independent
                # expressions; tie the record to the rung the model actually saw.
                parsed = parse_survival_projections(prompt_builder(offer))
                rendered = (float(f"{offer.survival_pct_before:.1f}"),
                            float(f"{offer.survival_pct_after:.1f}"))
                if parsed != rendered:
                    raise ValueError(
                        f"prompt survival figures {parsed} disagree with the "
                        f"recorded rung's {rendered} (cell={cell}, rung "
                        f"index {rr.index}, gain={gain})"
                    )
                records.append(RungRecord(
                    added_mortality_pp=rungs[rr.index].added_mortality_pp,
                    delta_deaths=offer.delta_deaths,
                    decisions=rr.decisions,
                    responses=tuple(raw[(rungs[rr.index], r)]
                                    for r in range(len(rr.decisions))),
                    accepted=rr.accepted,
                ))
            cell_result = CellResult(
                cell=cell,
                gain=gain,
                envelope=envelope_status(cell.species, gain),
                outcome=result.outcome,
                interval=result.interval,
                rung_records=tuple(records),
            )
            out.append(cell_result)
            if on_result is not None:
                on_result(cell_result)
    return out
