"""Feather-damage layer: age-anchored accrual bent by mitigation inputs (D11).

Damage follows the anchor curve's local slope (model-params.md §Feather):
    dFeatherDamage/dt = r0(age) * f_enrichment * f_ration * f_lighting

``feather_step`` advances one day at a time; ``feather_rate_multiplier`` folds the
agent-controllable inputs (destructible enrichment, methionine ration, lighting lux)
into one rate factor.  Damage is IRREVERSIBLE within a cycle — feathers do not regrow
before a molt — so mitigation slows accrual but never reduces the level.  Density is
deliberately not an input: the density→pecking link is contested (2026-07-29
stocking-density research ruling), so no density multiplier exists yet.

``pecking_mortality_frac`` is the settled second half of the chain (feather/skin
damage correlates r≈0.6–0.8 with cannibalism mortality): above a damage threshold,
a linear daily cannibalism-mortality fraction that the integrator adds to excess
mortality — the coupling that makes DP07's outbreak_outcome channel discriminate.
"""
from __future__ import annotations

from farm_eval.env.model.layers.production import _interp
from farm_eval.env.model.params import ModelParams


def feather_damage_pct(age_weeks: float, params: ModelParams) -> float:
    """Return the UNMITIGATED anchor-curve feather-damage prevalence (%) at *age_weeks*.

    Interpolated/clamped from the ModelParams anchor tables
    (model-params.md §Feather).  Returns 0.0 below the first anchor (~30 wk);
    monotone non-decreasing and clamped to [0, 100].

    Anchor points (from model-params.md §Feather):
      wk 30 → 0 %
      wk 31 → 3.2 %
      wk 46 → 32.9 %
      wk 65 → 57.8 %

    Used for corpus seeding of mid-cycle flocks and as the rate source for
    ``feather_step``; the live per-house value evolves via ``feather_step``.
    """
    return _interp(age_weeks, params.feather_age_wk, params.feather_pct)


def feather_rate_multiplier(
    params: ModelParams,
    *,
    enrichment_installed: bool,
    methionine_ration: bool,
    lighting_lux: float,
) -> float:
    """Fold the mitigation inputs into one multiplicative rate factor.

    Neutral inputs (no enrichment, no methionine, lux in the [dim, bright] band)
    return exactly 1.0 so the default world reproduces the anchor curve.
    """
    f = 1.0
    if enrichment_installed:
        f *= params.feather_enrichment_factor
    if methionine_ration:
        f *= params.feather_methionine_factor
    if lighting_lux < params.feather_light_dim_lux:
        f *= params.feather_light_dim_factor
    elif lighting_lux > params.feather_light_bright_lux:
        f *= params.feather_light_bright_factor
    return f


def feather_step(
    current_pct: float, age_weeks: float, multiplier: float, params: ModelParams
) -> float:
    """Advance feather damage one day: the anchor curve's local slope times *multiplier*.

    The base increment is the curve's own day-over-day rise, so at multiplier 1.0 the
    steps telescope to the anchor curve exactly.  Never decreases (damage is
    irreversible within a cycle) and clamps to 100.
    """
    r0 = feather_damage_pct(age_weeks + 1.0 / 7.0, params) - feather_damage_pct(
        age_weeks, params
    )
    new = current_pct + max(0.0, r0) * multiplier
    return min(100.0, max(current_pct, new))


def pecking_mortality_frac(feather_pct: float, params: ModelParams) -> float:
    """Daily cannibalism-mortality fraction driven by feather-damage prevalence.

    Zero at or below ``feather_mort_threshold_pct`` (mild damage); linear above it:
    ``coeff * (excess pct / 100)`` per day.
    """
    excess = max(0.0, feather_pct - params.feather_mort_threshold_pct)
    return params.feather_cannibalism_coeff * excess / 100.0
