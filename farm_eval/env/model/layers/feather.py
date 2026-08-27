"""Feather-damage layer: age-anchored accrual bent by mitigation inputs (D11).

Damage follows the anchor curve's local slope (model-params.md §Feather):
    dFeatherDamage/dt = r0(age) * f_enrichment * f_fiber * f_lighting

``feather_step`` advances one day at a time; ``feather_rate_multiplier`` folds the
agent-controllable inputs (destructible enrichment, high-insoluble-fibre ration, lighting
lux) into one rate factor.  Damage is IRREVERSIBLE within a cycle — feathers do not regrow
before a molt — so mitigation slows accrual but never reduces the level.  Density is
deliberately not an input: the density→pecking link is contested (2026-07-29
stocking-density research ruling), so no density multiplier exists yet.

``pecking_mortality_frac`` is the settled second half of the chain: above a damage
threshold, a linear daily cannibalism-mortality fraction that the integrator charges as
excess mortality (anchored on Kjaer & Sørensen 2002's cannibalism-specific regressions —
see ModelParams).  That linear term is the AMBIENT pressure any damaged flock carries.
``outbreak_target_mult`` / ``outbreak_mult_step`` add the second regime the corpus and the
literature both describe: injurious pecking is socially transmitted, so in a house the
schedule seeds an outbreak arc into, it ESCALATES over days to a peak and RELAXES toward a
managed level once a root-cause lever (enrichment or the fibre ration) is in.  Left unmanaged
it does not hold its peak forever either — it TAPERS with the arc's own age toward a late
level that still sits above the managed one (see ``outbreak_target_mult``).  A house with no
arc holds a multiplier of exactly 1.0, so an authored outbreak never leaves the house it was
authored into.

The 2026-08-19 lever rebuild replaced a methionine ration rung with the dietary-fibre one:
extra methionine on an already-adequate ration is disconfirmed, insoluble fibre is not.
Rationale and sources live on the ModelParams fields.
"""
from __future__ import annotations

from farm_eval.env.model.layers.production import _interp
from farm_eval.env.model.layers.beak import beak_feather_multiplier
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
    fiber_ration: bool,
    lighting_lux: float,
    beak_treatment: str = "",
    strain_low_pecking: bool = False,
    rearing_match: bool = False,
) -> float:
    """Fold the mitigation inputs into one multiplicative rate factor.

    Neutral inputs (no enrichment, no fibre ration, lux in the [dim, bright] band)
    return exactly 1.0 so the default world reproduces the anchor curve.

    The dim knee is ``feather_light_dim_lux`` (5.0 since the 2026-08-19 re-anchor), NOT the
    10-lux UEP floor: between 5 and 10 lux a house is under the welfare/inspection floor and
    accrues ``light_deficit_lux_hours`` for it, but buys no pecking suppression, because no
    study supports an effect at that small a contrast.
    """
    f = 1.0
    if enrichment_installed:
        f *= params.feather_enrichment_factor
    if fiber_ration:
        f *= params.feather_fiber_factor
    if lighting_lux < params.feather_light_dim_lux:
        f *= params.feather_light_dim_factor
    elif lighting_lux > params.feather_light_bright_lux:
        f *= params.feather_light_bright_factor
    return f * beak_feather_multiplier(
        params,
        beak_treatment=beak_treatment,
        strain_low_pecking=strain_low_pecking,
        rearing_match=rearing_match,
    )


def feather_step(
    current_pct: float, age_weeks: float, multiplier: float, params: ModelParams
) -> float:
    """Advance feather damage one day: the anchor curve's local slope times *multiplier*.

    *age_weeks* is the flock age at the END of the day being integrated (what the
    integrator's ``flock_age_weeks(start, day)`` returns), so the increment covers
    ``[age_weeks - 1 day, age_weeks]`` — a backward difference.  A forward difference
    would accrue the FOLLOWING day's slope and put a 30.0-wk flock above the curve's
    zero anchor (Codex D11 round-1 F5).  At multiplier 1.0 the steps telescope to the
    anchor curve exactly.  Never decreases (damage is irreversible within a cycle)
    and clamps to 100.
    """
    r0 = feather_damage_pct(age_weeks, params) - feather_damage_pct(
        age_weeks - 1.0 / 7.0, params
    )
    new = current_pct + max(0.0, r0) * multiplier
    return min(100.0, max(current_pct, new))


def outbreak_target_mult(
    params: ModelParams,
    *,
    outbreak_active: bool,
    mitigated: bool,
    days_since_onset: float = 0.0,
) -> float:
    """The cannibalism-rate multiplier this house is heading toward today.

    ``outbreak_active`` is the schedule's authored arc, live in exactly the house it was
    seeded into; ``mitigated`` means a root-cause lever is in (enrichment or the fibre
    ration).  A house with no live arc targets 1.0 — the ambient linear term and nothing
    else — which is what keeps an authored outbreak out of every other house and node.

    The managed target is deliberately not 1.0: enrichment and fibre each roughly HALVE
    injurious-pecking / cannibalism mortality in the sources (see ModelParams), and a
    managed outbreak is a cooled outbreak, not an un-started one.

    An UNMANAGED arc TAPERS with its own age (AUTHORED — Codex I4a, 2026-08-27): after
    ``feather_outbreak_taper_after_days`` the target ramps linearly from the peak down to
    ``feather_outbreak_late_mult`` over ``feather_outbreak_taper_days``, and holds there.  A
    flat 3.5x held for the rest of the cycle was the modelling artefact behind an untreated
    house losing a fifth of its birds in silence; a real untreated outbreak burns through the
    susceptible birds, the worst victims are already dead, and the rate settles high rather
    than climbing forever.  The floor stays strictly ABOVE the managed target, so managing an
    outbreak is better than not managing it on every single day of the arc — a monotonicity
    the tests pin, because a taper that crossed the managed level would reward doing nothing.
    """
    if not outbreak_active:
        return 1.0
    if mitigated:
        return params.feather_outbreak_mitigated_mult
    peak = params.feather_outbreak_peak_mult
    over = days_since_onset - params.feather_outbreak_taper_after_days
    if over <= 0.0:
        return peak
    frac = min(1.0, over / params.feather_outbreak_taper_days)
    return peak + (params.feather_outbreak_late_mult - peak) * frac


def outbreak_mult_step(current: float, target: float, params: ModelParams) -> float:
    """Move one day toward *target* at the outbreak ramp rate, never overshooting.

    One rate governs both directions: the escalation timescale IS the relief timescale (an
    outbreak runs up over about two weeks, and the birds take about as long to redirect onto
    new enrichment or a bulkier ration).  Never overshoots, so a target reached is a target
    held; a pure function of (current, target) with no wall-clock and no random, so replay
    reproduces it exactly.
    """
    step = (params.feather_outbreak_peak_mult - 1.0) / params.feather_outbreak_ramp_days
    if target > current:
        return min(target, current + step)
    return max(target, current - step)


def pecking_mortality_frac(
    feather_pct: float, params: ModelParams, outbreak_mult: float = 1.0
) -> float:
    """Daily cannibalism-mortality fraction driven by feather-damage prevalence.

    Zero at or below ``feather_mort_threshold_pct`` (mild damage); linear above it:
    ``coeff * (excess pct / 100)`` per day, times the house's outbreak multiplier — which
    is 1.0 in every house with no authored arc, so the ambient term is unchanged there.
    """
    excess = max(0.0, feather_pct - params.feather_mort_threshold_pct)
    return params.feather_cannibalism_coeff * excess / 100.0 * max(0.0, outbreak_mult)
