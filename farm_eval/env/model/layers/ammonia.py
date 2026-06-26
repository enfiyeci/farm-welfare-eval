"""Two-source ammonia layer (belt manure + floor litter).

Models in-house NH3 concentration as a first-order relaxation toward a target
ppm that is driven by litter emission and reduced by ventilation clearing.

Emission sources (model-params.md §Ammonia):
  - Floor litter: persistent even with manure belts; rises with litter age and moisture.
  - Belt manure: modelled via the f_MAT accumulation multiplier — more-frequent belt
    removal (lower belt_days) keeps the manure accumulation time shorter and lowers
    emission.  The distinct same-cycle clearance ratio (r_clear ≈ 0.71) is NOT modelled
    here; belt *interval* and same-cycle *clearance* are separate effects.

Ventilation clearing:
  - Effective ventilation is reduced in cold weather (ambient_c < 5°C) because
    climate controllers throttle fans to maintain house temperature.

Anchors (27-month CSES, model-params.md):
  - Aviary mean ~6.7 ppm at baseline ventilation, mild temp (5.0–8.5 ppm range).
  - ~12 winter days >25 ppm: cold + baseline vent pushes equilibrium past 25 ppm.
  - Ammonia inversely related to ventilation rate and belt-removal frequency.
"""
from __future__ import annotations

import math

from farm_eval.env.model.params import ModelParams


def effective_ventilation(ventilation: float, ambient_c: float, params: ModelParams) -> float:
    """Return effective ventilation after applying cold-weather fan-throttle penalty.

    When ambient_c < 5.0°C the climate controller reduces fan speed to hold heat,
    cutting effective ventilation by params.nh3_cold_vent_penalty (fractional).
    """
    if ambient_c < 5.0:
        return ventilation * (1.0 - params.nh3_cold_vent_penalty)
    return ventilation


def ammonia_step(
    ppm: float,
    litter_age_days: float,
    litter_moisture: float,
    ventilation: float,
    ambient_c: float,
    belt_days: float,
    params: ModelParams,
) -> float:
    """Advance in-house NH3 concentration by one time step.

    Args:
        ppm: Current in-house ammonia concentration (ppm).
        litter_age_days: Days since litter was last replaced.
        litter_moisture: Litter moisture content (%; reference is nh3_moisture_ref=25 %).
        ventilation: Normalised ventilation rate (1.0 = baseline).
        ambient_c: Outdoor temperature (°C); triggers cold penalty when < 5.
        belt_days: Manure accumulation days (belt removal interval).
        params: Calibrated model parameters.

    Returns:
        Next ppm value after one relaxation step toward the emission-driven target.

    Notes:
        f_MAT multiplier (Wageningen, model-params.md): captures how longer manure
        accumulation on belts raises emission.  Formula: exp(0.20*(d-1) + 0.03*(d-1)^2)
        gives {1.00, 1.26, 1.65, 2.39} for belt_days {1, 2, 3, 4}.
    """
    # Guard: belt_days must be >= 1 so f_MAT never inverts below 1.0
    belt_days = max(1, belt_days)

    # Belt manure-accumulation-time multiplier (f_MAT); belt_days=1 → multiplier=1.0
    belt_mult = math.exp(params.nh3_fmat_linear * (belt_days - 1) + params.nh3_fmat_quad * (belt_days - 1) ** 2)

    # Total emission target ppm from both litter and belt sources
    emission = (
        params.nh3_target_base
        + params.nh3_litter_coeff * litter_age_days
        + params.nh3_moisture_coeff * max(0.0, litter_moisture - params.nh3_moisture_ref)
    ) * belt_mult

    # Ventilation clearing: each unit above baseline removes nh3_vent_coeff ppm
    eff_vent = effective_ventilation(ventilation, ambient_c, params)
    target = emission - params.nh3_vent_coeff * (eff_vent - params.nh3_vent_baseline)
    target = max(0.0, target)

    # First-order relaxation toward target
    return max(0.0, ppm + (target - ppm) * params.nh3_relax)
