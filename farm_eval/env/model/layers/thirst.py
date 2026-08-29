"""Partial water-restriction fault (DP18 staged revival — ruling 16c; spec
docs/specs/2026-08-28-dp18-staged-water-node-design.md).

A far-end drinker-line fault leaves ``HouseWelfare.water_restriction_frac`` of a house's
birds on restricted water. AUTHORED mapping throughout: the project's WFP source set has no
thirst track, and the open-access review of water deprivation in poultry states current
tools "are not sufficient to detect the degradation of welfare derived from thirst itself"
(Nielsen/Rault 2024, PMC10950878). Rault 2016 supplies direction only — drinker-seeking
motivation from 12 h, behaviour changes from 18 h, and a 48 h TOTAL deprivation dropping
lay to ~4 % within 6 days. The fault modeled here is partial RESTRICTION (birds crowd the
working nipples and drink less), so the consequences are deliberately scaled down and
slowed: a bounded lay dip ramping over days and a small late mortality tick — survivable
for weeks, which is what lets the authored four-week story stand.
"""

from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def fault_age_days(onset_day: int, day: int) -> int:
    """Days since the fault appeared; -1 when no fault has been seeded."""
    if onset_day < 0:
        return -1
    return day - onset_day


def lay_dip_pp(age_days: int, params: ModelParams) -> float:
    """Percentage-point hen-day dip at this fault age (0 before the ramp starts)."""
    if age_days < params.thirst_lay_ramp_start_day:
        return 0.0
    span = params.thirst_lay_ramp_full_day - params.thirst_lay_ramp_start_day
    if span <= 0 or age_days >= params.thirst_lay_ramp_full_day:
        return params.thirst_lay_dip_pp_max
    frac = (age_days - params.thirst_lay_ramp_start_day) / span
    return params.thirst_lay_dip_pp_max * frac


def mortality_frac(age_days: int, params: ModelParams) -> float:
    """The daily flock-fraction mortality tick (0 before `thirst_mort_start_day`)."""
    if age_days < params.thirst_mort_start_day:
        return 0.0
    return params.thirst_mort_daily_frac
