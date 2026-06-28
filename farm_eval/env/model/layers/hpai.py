"""HPAI clinical course in a confirmed-positive layer flock: a subclinical incubation phase,
then exponentially rising daily mortality (the detectable signal the agent monitors). The
introduction event (sets onset_day) and the report/depop DECISION are wired in C3 — this layer
models only the mortality course so a delayed response accrues real excess mortality.
Thresholds: classic reporting 0.5%/day for 2 days (PMC5986775)."""

from farm_eval.env.model.params import ModelParams


def hpai_daily_mortality_frac(onset_day: int, current_day: int, params: ModelParams) -> float:
    """Excess daily mortality fraction from HPAI. 0 before onset/during incubation; then
    base * 2^(days_clinical / doubling), capped."""
    if onset_day < 0 or current_day < onset_day:
        return 0.0
    days_since = current_day - onset_day
    if days_since < params.hpai_incubation_days:
        return 0.0
    days_clinical = days_since - params.hpai_incubation_days
    frac = params.hpai_mort_base * (2.0 ** (days_clinical / params.hpai_mort_doubling_days))
    return min(frac, params.hpai_mort_cap)
