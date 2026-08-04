"""Litter-moisture layer: belt-frequency-driven moisture relaxation.

Litter moisture is the proximate driver of footpad dermatitis (layers/footpad.py)
and a secondary ammonia source (layers/ammonia.py).  It is NOT a free exogenous
input: it relaxes toward an equilibrium set by manure-belt removal frequency, the
control the agent reaches via ``adjust_setpoint(belt_interval_days=...)``.  This makes
footpad an agent-controllable welfare lever (more-frequent belts → drier litter →
fewer foot lesions), reusing the same belt lever the decision register names as the
ammonia root cause rather than exposing litter moisture as a separate input.

Dynamics (model-params.md §FPD — litter-moisture/belt coupling):
    belt_days_svc = max(1, belt_days - belt_service_days_credit
                              * max(0, 1 - days_since_service/belt_service_decay_days))
    moisture_eq = clamp(belt_floor + belt_slope*(belt_days_svc-1), belt_floor, moisture_max)
    moisture   += (moisture_eq - moisture) * litter_moisture_relax

A ``schedule_maintenance(house, manure_belt)`` work order — DP16's named root cause — enters
HERE, as a decaying reduction of the EFFECTIVE belt interval (the mirror of the staffing lag
that stretches it). It acts on the belt term rather than on the water input because below the
evaporative capacity the belt term is the only live moisture term; see params.py for the size
of the lever, which is deliberately small.

Calibration (Groot Koerkamp Ch. 7 Table 4, five measured belt regimes in one aviary):
belt_days=1 → 15.0 % and belt_days=7 → 20.1 %, spanning the measured 14.4-20.1 % band.
Belt interval is a WEAK moisture lever by measurement; density (layers/density.py) and the
manure-belt maintenance action are what actually move litter water. Relaxation is gradual
(rate 0.1/day, ~10-day time constant), so a mid-cycle change dries or wets over days.
"""
from __future__ import annotations

from farm_eval.env.model.layers import density
from farm_eval.env.model.params import ModelParams


def _serviced_belt_days(
    belt_days: float, days_since_belt_service: float | None, params: ModelParams
) -> float:
    """Shorten the effective belt interval for a recent manure-belt service.

    The credit decays linearly to zero over ``belt_service_decay_days`` as manure
    re-accumulates, and the result is floored at one belt-day: a service can at most make the
    litter behave as though the belts ran daily, never better than that.

    Mirror image of the staffing lag in model/integrate.py, which stretches the same interval.
    ``days_since_belt_service is None`` means "no service on record" and leaves the interval
    untouched, as does the inert 0.0 default credit.
    """
    if days_since_belt_service is None or params.belt_service_days_credit <= 0.0:
        return belt_days
    if params.belt_service_decay_days <= 0.0:
        return belt_days
    remaining = max(0.0, 1.0 - days_since_belt_service / params.belt_service_decay_days)
    return max(1.0, belt_days - params.belt_service_days_credit * remaining)


def litter_moisture_equilibrium(
    belt_days: float,
    params: ModelParams,
    *,
    area_sq_in: float = 0.0,
    birds: float = 0,
    days_since_belt_service: float | None = None,
) -> float:
    """Return the equilibrium litter moisture (%): belt-driven, plus surplus water loading.

    More-frequent belt removal (lower belt_days) yields a drier equilibrium. On top of that,
    stocking density loads the litter with droppings water; while that input stays within the
    litter's evaporative capacity the belt term governs ALONE and this is bit-for-bit the
    function it has always been. Only surplus water above capacity moves the equilibrium --
    see layers/density.py for why the knee emerges rather than being authored.

    ``area_sq_in`` and ``birds`` default to zero so every existing caller (and any caller with
    no house context, such as a bare belt-lever calculation) gets the unchanged belt curve.
    ``days_since_belt_service`` defaults to None for the same reason: no service on record
    leaves the belt curve exactly as it was.

    Bounded to [belt_floor, litter_moisture_max].
    """
    belt_days = max(1, belt_days)
    belt_days = _serviced_belt_days(belt_days, days_since_belt_service, params)
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
    days_since_belt_service: float | None = None,
) -> float:
    """Advance litter moisture one day toward its equilibrium.

    Args:
        moisture:   Current litter moisture (%).
        belt_days:  Manure-belt removal interval in days (the agent's lever).
        params:     Calibrated model parameters.
        area_sq_in: House usable area; with ``birds``, sets the litter loading. Omitted
                    (0.0) means no density term, i.e. the belt-only behaviour.
        birds:      Live bird count in the house.
        days_since_belt_service: Days since this house's last ``schedule_maintenance``
                    manure-belt work order. None (no service on record) leaves the belt
                    curve untouched.

    Returns:
        Next moisture value (%), bounded to [0, 100].  First-order relaxation toward
        ``litter_moisture_equilibrium`` at rate ``litter_moisture_relax``; a single step
        never overshoots the equilibrium.
    """
    eq = litter_moisture_equilibrium(
        belt_days, params, area_sq_in=area_sq_in, birds=birds,
        days_since_belt_service=days_since_belt_service,
    )
    new = moisture + (eq - moisture) * params.litter_moisture_relax
    return max(0.0, min(100.0, new))
