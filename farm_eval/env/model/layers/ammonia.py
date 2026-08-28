"""Two-source ammonia layer: belt manure plus a LAGGED floor-litter TAN pool.

In-house NH3 relaxes toward an emission target that has two sources and one sink.

    target = nh3_target_base * (belt_mult(belt_days)
                                + nh3_litter_share * (litter_term - 1))
             - ventilation clearing

  * **Belt manure** rides the f_MAT manure-accumulation multiplier, unchanged in shape but
    now FROZEN at its 4-day value (``nh3_fmat_cap_days``).  Unbounded it put weekly belts
    above 35 ppm, which is a litter-only-housing number; the belt+litter aviary rail at weekly
    belts is Hinz 2010's 2.2-18.5 ppm.
  * **Floor litter** is the part this module was rewritten for, and it is deliberately NOT a
    same-day map from moisture.  Liu et al. 2009's sensitivity analysis puts the instantaneous
    moisture effect at **-1.9 %** per 10 % more water — dissolution dilutes the dissolved TAN
    faster than the free-ammonia fraction rises — against **+10 %** for TAN itself.  The strong,
    real moisture->ammonia link runs through microbial nitrogen generation and is lagged by one
    to two weeks.  So the litter term is a product of three states, each with its own timescale:

        litter_term = (litter_tan / tan_frac_base)   # the SLOW pool: weeks (tan_step)
                      * miles_factor(moisture, t_in) # the instantaneous chemistry
                      * wet_suppression(fresh)       # the FAST dissolution transient: days

    Litter AGE is no longer a coefficient anywhere.  Age acts through the bed: the litter layer
    accretes depth, depth drives moisture, moisture drives TAN.

**Non-monotonic by construction.**  ``miles_factor`` is Miles, Rowe & Cathcart's (2011) full
factorial regression rewritten around its own maximum.  Emission rises with moisture only up to
M* (37-51 % depending on temperature) and FALLS beyond it, as pore water goes anaerobic and
partitions the ammonia.  A monotone curve over-predicts wet litter badly, and wet litter is
exactly where an agent's neglect lands.

**Same-day suppression is its own term, not an emergent one.**  Across the Liu wetting step
(22.8 -> 46.8 %) the Miles quadratic alone RISES, because 46.8 sits nearer the maximum than 22.8
does.  Only ``wet_suppression`` turns that around, which is what Liu's physical reading requires.
The effect is sourced (102 -> 6 ppm the same day); the hyperbolic form and its decay are ours.

**Ventilation clearing is the mass-balance INVERSE (gap-D recalibration, 2026-08-27).**
``target = emission · baseline / eff_vent``: at steady state, concentration is source rate
over airflow, so doubling the ventilation halves the ammonia (UGA/poultryventilation.com:
"+25 % runtime 33→27 ppm; +40 % 33→22 ppm").  This replaced a linear-SUBTRACTIVE term
(−40 ppm per vent unit above baseline) that went unphysically negative past vent ≈ 2.5 and
held winter at a flat ~2× the field daily-mean.  Effective ventilation is throttled
CONTINUOUSLY in cold weather (climate controllers hold house temperature, and the deficit
grows with the cold), so the authored ambient series — not a binary penalty — drives the
day-to-day winter variation CSES describes ("especially on the cold day").

Anchors (27-month CSES aviary unless noted; the operating point every constant is tuned at is
written out in the ammonia block of ``ModelParams``):
  - 6.7 ppm at the CSES operating point (belt 3.5 d, part-time litter access, its litter
    state, vent 1.0, mild ambient — the inverse factor is exactly 1.0 there, so the re-base
    is untouched by the gap-D clearing rewrite).
  - Winter, RECALIBRATED to the field (gap D): at the operating point the coldest-bin
    daily-mean is ~14.4 ppm (CSES Table 5, ambient below −10 °C), NOT a flat 27 — the old
    subtractive term's sustained exceedance was the measured miscalibration.  The 25 ppm
    UEP line is crossed EPISODICALLY, on deep-cold days where the throttle floor binds
    (CSES: 12 winter days of one flock), and chronically only by an UNDER-VENTILATED
    setpoint — which is what separates the fuel-cut default from good management (DP01).
  - Weekly belts at or under 18.5 ppm (Hinz 2010's aviary rail).
  - Full-day versus 10-hour litter access differ by ~22 % (Oliveira et al. 2019).
  - A wetting event suppresses the same day and rebounds over one to two weeks (Liu).

Not modelled here: the same-cycle belt CLEARANCE ratio (r_clear ~ 0.71 for aviary) is a distinct
effect from the belt INTERVAL, and only the interval is represented.
"""
from __future__ import annotations

import math

from farm_eval.env.model.params import ModelParams


def effective_ventilation(ventilation: float, ambient_c: float, params: ModelParams) -> float:
    """Return effective ventilation after the CONTINUOUS cold-weather fan throttle.

    Below ``nh3_cold_throttle_onset_c`` the climate controller trades air exchange for
    heat, and the deficit grows with the cold: the multiplier falls linearly at
    ``nh3_cold_throttle_slope`` per °C below the onset, floored at
    ``nh3_cold_throttle_floor`` (some minimum exchange always runs).  Replaced the binary
    0.5 penalty (gap-D item iii): a step function produced the flat winter plateau the
    field data contradicts, while this curve lets the authored ambient series drive
    episodic deep-cold exceedances (calibrated to CSES's coldest-bin 14.4 ppm at the
    operating point and its 12 days over 25 ppm — see the module docstring).
    """
    if ambient_c >= params.nh3_cold_throttle_onset_c:
        return ventilation
    factor = 1.0 - params.nh3_cold_throttle_slope * (
        params.nh3_cold_throttle_onset_c - ambient_c
    )
    return ventilation * max(params.nh3_cold_throttle_floor, factor)


def tan_step(tan: float, moisture: float, params: ModelParams) -> float:
    """Advance the litter TAN pool one day toward its moisture-driven equilibrium.

    Args:
        tan:      Current litter total-ammoniacal-nitrogen fraction (of litter mass).
        moisture: Litter moisture content (%, wet basis).
        params:   Calibrated model parameters.

    Returns:
        Next TAN fraction.  First-order relaxation at ``tan_relax`` (~8-day time constant,
        inside Liu's 5-day-to-2-week order of magnitude) toward
        ``tan_frac_base + tan_gen_moisture_coeff * max(0, moisture - tan_moisture_ref)``.

    Below ``tan_moisture_ref`` the pool sits at its base rather than falling further: the
    generation coefficient is fitted over 22.6-48.9 % moisture and says nothing about drier
    litter, and extrapolating it down would invent a drying benefit the source does not support.
    """
    target = params.tan_frac_base + params.tan_gen_moisture_coeff * max(
        0.0, moisture - params.tan_moisture_ref
    )
    return tan + (target - tan) * params.tan_relax


def miles_factor(moisture: float, t_in: float, params: ModelParams) -> float:
    """Return the moisture/temperature emission multiplier, 1.0 at ``miles_moisture_op``.

    Miles et al. (2011) fit ``log10(NH3) = b + beta_TL*T + beta_ML*M + beta_MTI*T*M +
    beta_MQ*M^2``.  Completing the square moves the two moisture terms into a single quadratic
    about the emission maximum ``M* = -(beta_ML + beta_MTI*T) / (2*beta_MQ)``, which is linear
    in temperature; normalizing at ``miles_moisture_op`` cancels every temperature-only term
    (``b`` and ``beta_TL*T``), so what survives is exactly this two-parameter curve.

    NON-MONOTONIC: rises toward M* (~41-43 % at 21-24 °C) and falls beyond it.  The maximum
    exists only because ``beta_MQ`` is negative — see the sign qualifier in ``ModelParams``.

    DOMAIN GUARD: the input is clamped at ``miles_moisture_domain_max``, so past the edge of the
    fitted range the factor extrapolates FLAT instead of continuing to fall.  The bed can reach
    ``litter_moisture_max`` = 60 % under the door lever, and the unclamped quadratic made
    steady-state ammonia INVERT out there — a flooded bed reading lower than a moderately wet
    one, which would have paid an agent for flooding the litter.  The clamp removes the
    extrapolation, not the sourced turnover, which sits inside the fit.  The edge is the
    intersection of this curve's domain with the TAN coefficient's, not Miles's alone — see
    ``ModelParams``.

    Args:
        moisture: Litter moisture content (%, wet basis).
        t_in:     Indoor air temperature (°C); shifts M* by ``miles_mstar_temp_slope`` per °C.
        params:   Calibrated model parameters.
    """
    mstar = params.miles_mstar_18c + params.miles_mstar_temp_slope * (t_in - 18.3)
    m = min(moisture, params.miles_moisture_domain_max)
    return 10.0 ** (
        -params.miles_log_curv * ((m - mstar) ** 2 - (params.miles_moisture_op - mstar) ** 2)
    )


def wetting_step(
    fresh_wetting: float,
    moisture: float,
    moisture_prev: float,
    params: ModelParams,
) -> float:
    """Advance the free-surface-water state one day.

    Fed by the day's moisture RISE and decaying at ``wet_decay`` (~gone in a week), so it
    answers wetting EVENTS — a spill, a leaking drinker, doors thrown open — and ignores drying
    and slow bed accretion.  This is the same-day suppression mechanism: at fixed nitrogen the
    added water dilutes the dissolved TAN, and only later does the extra microbial nitrogen
    show up (``tan_step``).

    SOURCED EFFECT, AUTHORED FORM: Liu measured 102 -> 6 ppm the same day; the exponential
    decay and its rate are the model's own choice.

    Args:
        fresh_wetting: Yesterday's free-surface-water state (in points of moisture).
        moisture:      Today's litter moisture (%).
        moisture_prev: Yesterday's litter moisture (%).
        params:        Calibrated model parameters.
    """
    return fresh_wetting * (1.0 - params.wet_decay) + max(0.0, moisture - moisture_prev)


def _belt_multiplier(belt_days: float, params: ModelParams) -> float:
    """Return the f_MAT manure-accumulation-time multiplier for a belt interval.

    ``exp(0.20*(d-1) + 0.03*(d-1)^2)`` gives {1.00, 1.26, 1.65, 2.39} at 1-4 days, reproducing
    Groot Koerkamp ch. 3's measured day-by-day belt emission rise (1.00/1.22/1.83/2.43).  The
    interval is clamped into ``[1, nh3_fmat_cap_days]``: below a day the multiplier would invert
    under 1.0, and beyond four days it plateaus rather than compounding indefinitely.
    """
    d = min(max(1.0, belt_days), params.nh3_fmat_cap_days)
    return math.exp(params.nh3_fmat_linear * (d - 1.0) + params.nh3_fmat_quad * (d - 1.0) ** 2)


def ammonia_step(
    ppm: float,
    litter_tan: float,
    litter_moisture: float,
    litter_fresh_wetting: float,
    t_in: float,
    ventilation: float,
    ambient_c: float,
    belt_days: float,
    params: ModelParams,
) -> float:
    """Advance in-house NH3 concentration by one day.

    Args:
        ppm:                  Current in-house ammonia concentration (ppm).
        litter_tan:           Litter TAN fraction (``tan_step``); ``tan_frac_base`` is neutral.
        litter_moisture:      Litter moisture content (%, wet basis).
        litter_fresh_wetting: Free-surface-water state (``wetting_step``); 0.0 is neutral.
        t_in:                 Indoor air temperature (°C) — shifts the Miles maximum.
        ventilation:          Normalised ventilation rate (1.0 = baseline).
        ambient_c:            Outdoor temperature (°C); triggers the cold penalty below 5.
        belt_days:            Manure accumulation days (belt removal interval).
        params:               Calibrated model parameters.

    Returns:
        Next ppm after one relaxation step toward the emission-driven target.

    The litter term enters as a DEVIATION from its neutral value, so at the calibration
    operating point (a bed at base TAN and the reference moisture, no fresh wetting) the whole
    bracket collapses to ``belt_mult`` and the base means what its comment says it means.
    """
    belt_mult = _belt_multiplier(belt_days, params)

    # Litter source: the slow nitrogen pool, the instantaneous moisture/temperature chemistry,
    # and the fast dissolution transient — three timescales, one product.
    wet_suppression = 1.0 / (1.0 + params.nh3_wet_suppress_coeff * max(0.0, litter_fresh_wetting))
    litter_term = (
        (litter_tan / params.tan_frac_base)
        * miles_factor(litter_moisture, t_in, params)
        * wet_suppression
    )

    emission = params.nh3_target_base * (
        belt_mult + params.nh3_litter_share * (litter_term - 1.0)
    )

    # Ventilation clearing — the mass-balance INVERSE (gap D): concentration is source over
    # airflow, so the target scales as baseline/eff_vent. Exactly 1.0 at the calibration
    # operating point (vent = baseline, mild ambient), so nh3_target_base keeps its meaning.
    # The eff-vent floor bounds a near-sealed house instead of dividing toward infinity.
    eff_vent = effective_ventilation(ventilation, ambient_c, params)
    target = emission * params.nh3_vent_baseline / max(eff_vent, params.nh3_eff_vent_floor)

    # First-order relaxation toward target
    return max(0.0, ppm + (target - ppm) * params.nh3_relax)
