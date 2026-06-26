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

Calibration: belt_days=1 → 15 % (dry, below fpd_moisture_ref); belt_days=7 → 45 %
(wet, footpad-active).  Relaxation is gradual (rate 0.1/day, ~10-day time constant),
so a mid-cycle belt change dries or wets the litter over days, not instantly.
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def litter_moisture_equilibrium(belt_days: float, params: ModelParams) -> float:
    """Return the belt-frequency-driven equilibrium litter moisture (%).

    More-frequent belt removal (lower belt_days) yields a drier equilibrium.
    Bounded to [belt_floor, litter_moisture_max].
    """
    belt_days = max(1, belt_days)
    eq = params.litter_moisture_belt_floor + params.litter_moisture_belt_slope * (belt_days - 1)
    return min(eq, params.litter_moisture_max)


def litter_moisture_step(moisture: float, belt_days: float, params: ModelParams) -> float:
    """Advance litter moisture one day toward its belt-driven equilibrium.

    Args:
        moisture:  Current litter moisture (%).
        belt_days: Manure-belt removal interval in days (the agent's lever).
        params:    Calibrated model parameters.

    Returns:
        Next moisture value (%), bounded to [0, 100].  First-order relaxation toward
        ``litter_moisture_equilibrium(belt_days)`` at rate ``litter_moisture_relax``;
        a single step never overshoots the equilibrium.
    """
    eq = litter_moisture_equilibrium(belt_days, params)
    new = moisture + (eq - moisture) * params.litter_moisture_relax
    return max(0.0, min(100.0, new))
