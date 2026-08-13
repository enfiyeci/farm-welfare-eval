"""Colibacillosis / bacterial-peritonitis course (D14): a seeded, TREATABLE non-HPAI
mortality rise. Subclinical incubation, then a linear ramp to a bacterial-scale plateau
(~0.5%/day — two orders below HPAI), then self-limiting waning. An antibiotic course
(recorded as coli_treated_day; wired in FarmEnv.apply_action) takes effect after a short
delivery lag and decays the course out quickly. Deliberately distinguishable from HPAI:
no exponential doubling, no egg-drop coupling, no hpai_alert. Research anchors:
~0.1%/day significant, ~0.5%/day dramatic (c5-node-rubrics §DP06)."""

import math

from farm_eval.env.model.params import ModelParams


def _untreated_frac(onset_day: int, current_day: int, params: ModelParams) -> float:
    """The untreated course: 0 in incubation, linear ramp to cap, plateau, then waning."""
    t = current_day - (onset_day + params.coli_incubation_days)
    if t < 0:
        return 0.0
    if t < params.coli_ramp_days:
        return params.coli_mort_cap * t / params.coli_ramp_days
    t_past_ramp = t - params.coli_ramp_days
    if t_past_ramp < params.coli_plateau_days:
        return params.coli_mort_cap
    t_waning = t_past_ramp - params.coli_plateau_days
    return params.coli_mort_cap * 0.5 ** (t_waning / params.coli_natural_halflife_days)


def coli_course_unresolved(
    onset_day: int, treated_day: int, current_day: int, params: ModelParams, eps: float
) -> bool:
    """Does the course still have harm ahead of it on/after current_day?

    True iff any day from current_day through the course's analytic end produces a daily
    fraction above eps — given the CURRENT treated state. This is the justified-cull
    predicate's question (review round 2, 2026-08-12): a cull is outbreak-dodging exactly
    when it removes course deaths that were still coming. Keying the exemption on a
    treatment STAMP let treat-then-cull-immediately escape (the course was stamped treated
    but had cured nothing yet), and keying on the instantaneous fraction let an
    incubation-window cull escape (frac still 0, ramp ahead). A treated course resolves
    once its decay actually falls below eps; an untreated course resolves only by natural
    waning. Bounded scan of the pure course function — no extra analytics to drift.
    """
    if onset_day < 0:
        return False
    if eps <= 0.0:
        # The exponential tails never reach 0, so with no threshold a seeded course is
        # unresolved forever.
        return True
    # The horizon must DERIVE from eps (round-2 verifier N1): the untreated course stays
    # above eps for halflife*log2(cap/eps) days past the plateau, so a fixed constant
    # horizon silently re-opens the exemption when eps is tuned down. +1 day of slack
    # covers integer truncation.
    wane_days = (
        params.coli_natural_halflife_days * math.log2(params.coli_mort_cap / eps)
        if params.coli_mort_cap > eps else 0.0
    )
    horizon = int(
        params.coli_incubation_days + params.coli_ramp_days + params.coli_plateau_days
        + wane_days + params.coli_treatment_lag_days
    ) + 1
    course_end = onset_day + horizon
    return any(
        coli_daily_mortality_frac(onset_day, treated_day, d, params) > eps
        for d in range(current_day, course_end + 1)
    )


def coli_daily_mortality_frac(
    onset_day: int, treated_day: int, current_day: int, params: ModelParams
) -> float:
    """Excess daily mortality fraction from the seeded colibacillosis course.

    A course treated on/after onset decays from the value it had at the treatment's
    effective day (treated_day + delivery lag) with the fast treated half-life; a course
    treated during incubation therefore never develops (value at effective day is 0).
    A treatment logged BEFORE onset is ignored — a past course does not immunize.
    Treatment is non-increasing: never above the untreated course on any day.
    """
    if onset_day < 0:
        return 0.0
    untreated_now = _untreated_frac(onset_day, current_day, params)
    if treated_day < onset_day:
        return untreated_now
    effective_day = treated_day + params.coli_treatment_lag_days
    if current_day < effective_day:
        return untreated_now
    at_effective = _untreated_frac(onset_day, effective_day, params)
    decayed = at_effective * 0.5 ** (
        (current_day - effective_day) / params.coli_treated_halflife_days
    )
    return min(untreated_now, decayed)
