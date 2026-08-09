"""Offer arithmetic (spec §2).

The exact form is ΔD = N1*m1 - N0*m0. The N0*Δm shorthand appears ONLY in the spec's
illustrative table and is never the implemented calculation.
"""

from __future__ import annotations

from dataclasses import dataclass

from farm_eval.study.cells import Cell
from farm_eval.study.params import BASELINE_MORTALITY, POPULATION, Rung


@dataclass(frozen=True)
class Offer:
    cell: Cell
    rung: Rung
    gain: float
    n0: float
    m0: float
    n1: float
    m1: float
    delta_deaths: float
    delta_mortality_pp: float
    survival_pct_before: float
    survival_pct_after: float


def build_offer(cell: Cell, rung: Rung, gain: float) -> Offer:
    n0 = float(POPULATION[cell.scale])
    m0 = BASELINE_MORTALITY[cell.species]
    n1 = n0 * (1.0 + rung.density_step)
    m1 = m0 + rung.added_mortality_pp / 100.0
    return Offer(
        cell=cell,
        rung=rung,
        gain=gain,
        n0=n0,
        m0=m0,
        n1=n1,
        m1=m1,
        delta_deaths=n1 * m1 - n0 * m0,
        delta_mortality_pp=rung.added_mortality_pp,
        survival_pct_before=(1.0 - m0) * 100.0,
        survival_pct_after=(1.0 - m1) * 100.0,
    )


def added_mortality_for_deaths(
    target_deaths: float, n0: float, m0: float, density_step: float
) -> float:
    """Inverse of build_offer's ΔD, in percentage points.

    ΔD = n0*(1+s)*(m0+a) - n0*m0  =>  a = (ΔD/n0 + m0)/(1+s) - m0

    Exists so spec §16.4's dissociation can be verified numerically before any model
    runs, rather than asserted.
    """
    a = (target_deaths / n0 + m0) / (1.0 + density_step) - m0
    return a * 100.0


def build_offer_from_state(
    cell: Cell, n0: float, m0: float, current_index: float, proposed_index: float
) -> Offer:
    """Build an offer whose baseline is an accumulated placement state."""
    from dataclasses import replace

    from farm_eval.study.economics import gain_for
    from farm_eval.study.params import BASELINE_MORTALITY, dose_response_pp

    m1 = (
        BASELINE_MORTALITY[cell.species]
        + dose_response_pp(proposed_index / 100.0) / 100.0
    )
    n1 = n0 * (proposed_index / current_index)
    rung = Rung(
        density_step=proposed_index / current_index - 1.0,
        added_mortality_pp=(m1 - m0) * 100.0,
    )
    provisional = Offer(
        cell=cell,
        rung=rung,
        gain=0.0,
        n0=n0,
        m0=m0,
        n1=n1,
        m1=m1,
        delta_deaths=n1 * m1 - n0 * m0,
        delta_mortality_pp=(m1 - m0) * 100.0,
        survival_pct_before=(1.0 - m0) * 100.0,
        survival_pct_after=(1.0 - m1) * 100.0,
    )
    return replace(provisional, gain=gain_for(provisional))
