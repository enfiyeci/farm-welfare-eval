"""Two-source ammonia layer (belt manure + floor litter).

Models in-house NH3 concentration as a first-order relaxation toward a target
ppm that is driven by litter emission and reduced by ventilation clearing.

Emission sources (model-params.md §Ammonia):
  - Floor litter: persistent even with manure belts; rises with litter age.
  - Belt manure: modelled via the f_MAT accumulation multiplier — more-frequent belt
    removal (lower belt_days) keeps the manure accumulation time shorter and lowers
    emission.  The distinct same-cycle clearance ratio (r_clear ≈ 0.71) is NOT modelled
    here; belt *interval* and same-cycle *clearance* are separate effects.
  - Litter moisture: a MULTIPLICATIVE factor on the whole emission term (Groot Koerkamp
    Ch. 5 eq. 18, 0.40 %/(g/kg) of litter water), centred where the base was calibrated so
    the factor is 1.0 there and only deviations move ammonia.  This is the channel by which
    stocking density and manure-belt servicing reach ammonia; see params.py for the
    sourcing, the centring argument and the missing-turnover limitation.

Ventilation clearing:
  - Effective ventilation is reduced in cold weather (ambient_c < 5°C) because
    climate controllers throttle fans to maintain house temperature.

Anchors (model-params.md §Ammonia):
  - Aviary mean ~6.7 ppm at baseline ventilation, mild temp (5.0-8.5 ppm range) -- Zhao 2015, CSES.
  - Aviary at WEEKLY belts, mild conditions: 6-19 ppm (Groot Koerkamp Ch. 7 period 2B = 6.4 ppm;
    Hinz 2010 Volierenhaltung median 11.40, max 18.52).
  - ~12 winter days >25 ppm: cold + baseline vent pushes equilibrium past 25 ppm. This is the
    operating point Nimmermark 2009's 32 ppm belongs to (cold, throttled ventilation), NOT the
    mild-baseline belt anchor it was previously used for.
  - Ammonia inversely related to ventilation rate and belt-removal frequency.
"""
from __future__ import annotations

import math

from farm_eval.env.model.params import ModelParams


def fmat(belt_days: float, params: ModelParams) -> float:
    """Manure-accumulation-time multiplier, HELD at the edge of its calibrated domain.

    The exponential-quadratic form is a Wageningen fit over belt_days 1-4 (giving
    1.00 / 1.26 / 1.65 / 2.39).  Extrapolated it explodes -- belt_days=14 returns ~2143 --
    so past ``nh3_fmat_domain_max`` the input is clamped to the domain edge and the fit
    evaluated there: the multiplier HOLDS its last validated value.  Everything inside the
    validated domain is byte-identical to the original fit.

    It used to saturate toward ``nh3_fmat_max = 6.35`` instead.  That asymptote was fitted to
    two rails that were both misattributed to aviaries: Nimmermark et al. 2009's cold-season,
    reduced-ventilation, litter-caked MULTILEVEL house (32-38 ppm) and Hinz et al. 2010's
    *Bodenhaltung* FLOOR-HOUSING row (9.2-47.4 ppm).  Hinz's actual aviary row at weekly
    manure-belt removal is 2.24-18.52 ppm; see ``params.py`` for the full provenance.  There
    is no aviary measurement at a 14-day belt interval, so any further rise at long belt
    intervals must come from a channel that IS measured -- litter moisture or litter age.

    This is not a fudge factor.  It is a refusal to extrapolate a fit outside its domain.
    """
    belt_days = max(1.0, float(belt_days))
    inner = min(belt_days, params.nh3_fmat_domain_max)
    return math.exp(
        params.nh3_fmat_linear * (inner - 1.0) + params.nh3_fmat_quad * (inner - 1.0) ** 2
    )


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
        litter_moisture: Litter moisture content (%).  Scales emission multiplicatively
            about ``nh3_moisture_ref`` (17.12 %), where the factor is exactly 1.0.
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
    # Belt manure-accumulation-time multiplier (f_MAT); belt_days=1 → multiplier=1.0
    belt_mult = fmat(belt_days, params)

    # Total emission target ppm from both litter and belt sources. The litter-age input is
    # capped at its calibrated range (see nh3_litter_age_max_days): litter TAN generation
    # reaches an equilibrium -- the standing crop of degradable N saturates -- so two-year-old
    # litter does not emit an order of magnitude more than two-month-old litter, which is
    # exactly what the measured 9.2-47.4 ppm range for unremoved litter shows.
    effective_litter_age = min(litter_age_days, params.nh3_litter_age_max_days)
    # Litter-moisture factor, MULTIPLICATIVE and centred on the operating point the base was
    # calibrated at. Groot Koerkamp Ch. 5 eq. (18) fits it as a percentage change in emission
    # per g/kg of litter water (0.40 %/(g/kg)), so the moisture channel scales emission rather
    # than adding ppm to it; the x10 converts moisture percent to g/kg. There is no
    # max(0.0, ...) floor on the deviation on purpose -- litter drier than the centring must
    # LOWER emission, or belts run more often than CSES's 3-4-day cadence earn nothing. See
    # params.py:nh3_moisture_frac_per_g_kg for the sourcing, the centring and the turnover limitation.
    moisture_mult = math.exp(
        params.nh3_moisture_frac_per_g_kg * (litter_moisture - params.nh3_moisture_ref) * 10.0
    )
    emission = (
        params.nh3_target_base + params.nh3_litter_coeff * effective_litter_age
    ) * belt_mult * moisture_mult

    # Saturate the SOURCE term before ventilation acts on it. Clamping only the finished
    # concentration (the first version of this bound) flattened the ventilation gradient:
    # at belt_days_eff=56 (14 d x the 4x staffing lag), litter age 518 and winter, every
    # ventilation setting from 0 to ~2.29 produced an identical 100 ppm, so raising
    # ventilation bought the agent nothing. Bounding emission instead keeps dilution
    # monotone above baseline ventilation, which is what the DP01 lever depends on.
    emission = min(emission, params.nh3_ceiling_ppm)

    # Ventilation clearing: each unit above baseline removes nh3_vent_coeff ppm
    eff_vent = effective_ventilation(ventilation, ambient_c, params)
    target = emission - params.nh3_vent_coeff * (eff_vent - params.nh3_vent_baseline)
    # Clamp to the physically measured concentration range. The lower bound was always
    # here; the upper bound is N2's absolute rail -- no measured in-house concentration in
    # any system exceeds ~100 ppm, and it is what keeps this layer physical once stocking
    # density becomes a second multiplier on `emission` above.
    target = min(max(0.0, target), params.nh3_ceiling_ppm)

    # Project an out-of-range INCOMING concentration onto the rail BEFORE relaxing, rather
    # than clamping the result afterwards. An EnvState can carry a pre-bound value (a
    # checkpoint or a pinned replay artifact saved under the unbounded model), and clamping
    # after relaxation collapsed every such step to exactly the ceiling -- so on the first
    # day a ventilation of 0 and a ventilation of 5 returned an identical 100 ppm and the
    # agent's action had no visible effect. Projecting first preserves the first-order
    # transition and keeps the rail absolute. A no-op for any run started fresh.
    ppm = min(max(0.0, ppm), params.nh3_ceiling_ppm)
    return max(0.0, ppm + (target - ppm) * params.nh3_relax)
