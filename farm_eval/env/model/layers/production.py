from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def _interp(x: float, xs: list[float], ys: list[float]) -> float:
    """Clamped monotone linear interpolation over parallel xs/ys lists.

    Returns ys[0] for x below xs[0] and ys[-1] for x above xs[-1].
    Shared helper reused by later layers (keel, feather).
    """
    if not xs or len(xs) != len(ys):
        raise ValueError("_interp requires equal-length, non-empty xs and ys")
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    for i in range(1, len(xs)):
        if x <= xs[i]:
            t = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            return ys[i - 1] + t * (ys[i] - ys[i - 1])
    return ys[-1]


def cold_feed_multiplier(indoor_temp_c: float, params: ModelParams) -> float:
    """Feed-intake multiplier from cold thermoregulation (>= 1.0).

    At or above `cold_thermoneutral_floor_c` the hen is in its comfort zone and eats the
    breed-standard amount (multiplier 1.0). Below the floor it burns feed to maintain body
    temperature: `1 + cold_feed_coeff * (floor - indoor_temp_c)`, capped at
    `1 + cold_feed_max_uplift`. Anchored to PMC10741227 (~+18% feed at 12 degC vs thermoneutral).
    Cold's other effects (mild production dip) are second-order and not modeled; egg/shell quality
    is unaffected by cold (unlike heat), so this does NOT feed the downgrade term.
    """
    deficit = max(0.0, params.cold_thermoneutral_floor_c - indoor_temp_c)
    return 1.0 + min(params.cold_feed_max_uplift, params.cold_feed_coeff * deficit)


def production_step(age_weeks: float, params: ModelParams) -> dict:
    """Return breed-standard production metrics for a hen at *age_weeks*.

    Keys:
    - hen_day_pct: Hen-Day egg production percentage
    - feed_g: daily feed grams per bird
    - water_ml_base: daily water millilitres per bird (base, pre-adjustments)
    - baseline_daily_mortality_frac: forward slope of cum-mortality curve / 100
      (fraction/day, clamped >= 0)
    - cum_mortality_pct: cumulative mortality percentage at this age

    All values interpolated from ModelParams breed-standard tables
    (model-params.md §Breed-standard targets).
    """
    cum = _interp(age_weeks, params.breed_age_wk, params.breed_cummort)
    cum_next = _interp(age_weeks + 1.0 / 7.0, params.breed_age_wk, params.breed_cummort)  # +1 day expressed in weeks (forward slope)
    baseline_daily = max(0.0, (cum_next - cum) / 100.0)  # percent -> fraction; fraction/day from cum %-curve slope
    return {
        "hen_day_pct": _interp(age_weeks, params.breed_age_wk, params.breed_hdep),
        "feed_g": _interp(age_weeks, params.breed_age_wk, params.breed_feed_g),
        "water_ml_base": _interp(age_weeks, params.breed_age_wk, params.breed_water_ml),
        "baseline_daily_mortality_frac": baseline_daily,
        "cum_mortality_pct": cum,
    }
