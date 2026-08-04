"""Litter-moisture layer: belt-frequency-driven moisture relaxation.

Litter moisture is the proximate driver of footpad dermatitis (layers/footpad.py)
and a secondary ammonia source (layers/ammonia.py).  It is NOT a free exogenous
input: it relaxes toward an equilibrium set by manure-belt removal frequency, the
control the agent reaches via ``adjust_setpoint(belt_interval_days=...)``.  This makes
footpad an agent-controllable welfare lever (more-frequent belts → drier litter →
fewer foot lesions), reusing the same belt lever the decision register names as the
ammonia root cause rather than exposing litter moisture as a separate input.

Dynamics (model-params.md §FPD — litter-moisture/belt coupling):
    moisture_eq = clamp(belt_floor + belt_slope*(belt_days-1), belt_floor, moisture_max)
    moisture   += (moisture_eq - moisture) * litter_moisture_relax

Calibration (Groot Koerkamp Ch. 7 Table 4, five measured belt regimes in one aviary):
belt_days=1 → 15.0 % and belt_days=7 → 20.1 %, spanning the measured 14.4-20.1 % band.
Belt interval is a WEAK moisture lever by measurement; density (layers/density.py) and the
manure-belt maintenance action are what actually move litter water. Relaxation is gradual
(rate 0.1/day, ~10-day time constant), so a mid-cycle change dries or wets over days.
"""
from __future__ import annotations

from farm_eval.env.model.layers import density
from farm_eval.env.model.params import ModelParams


def litter_moisture_equilibrium(
    belt_days: float,
    params: ModelParams,
    *,
    area_sq_in: float = 0.0,
    birds: float = 0,
) -> float:
    """Return the equilibrium litter moisture (%): belt-driven, plus surplus water loading.

    More-frequent belt removal (lower belt_days) yields a drier equilibrium. On top of that,
    stocking density loads the litter with droppings water; while that input stays within the
    litter's evaporative capacity the belt term governs ALONE and this is bit-for-bit the
    function it has always been. Only surplus water above capacity moves the equilibrium --
    see layers/density.py for why the knee emerges rather than being authored.

    ``area_sq_in`` and ``birds`` default to zero so every existing caller (and any caller with
    no house context, such as a bare belt-lever calculation) gets the unchanged belt curve.

    Bounded to [belt_floor, litter_moisture_max].
    """
    belt_days = max(1, belt_days)
    eq = params.litter_moisture_belt_floor + params.litter_moisture_belt_slope * (belt_days - 1)
    excess = density.excess_water_g_per_kg(area_sq_in, birds, params)
    if excess > 0.0:
        eq += params.litter_moisture_per_excess_water * excess
    return min(eq, params.litter_moisture_max)


def litter_moisture_step(
    moisture: float,
    belt_days: float,
    params: ModelParams,
    *,
    area_sq_in: float = 0.0,
    birds: float = 0,
) -> float:
    """Advance litter moisture one day toward its equilibrium.

    Args:
        moisture:   Current litter moisture (%).
        belt_days:  Manure-belt removal interval in days (the agent's lever).
        params:     Calibrated model parameters.
        area_sq_in: House usable area; with ``birds``, sets the litter loading. Omitted
                    (0.0) means no density term, i.e. the belt-only behaviour.
        birds:      Live bird count in the house.

    Returns:
        Next moisture value (%), bounded to [0, 100].  First-order relaxation toward
        ``litter_moisture_equilibrium`` at rate ``litter_moisture_relax``; a single step
        never overshoots the equilibrium.
    """
    eq = litter_moisture_equilibrium(belt_days, params, area_sq_in=area_sq_in, birds=birds)
    new = moisture + (eq - moisture) * params.litter_moisture_relax
    return max(0.0, min(100.0, new))
