"""Red-mite (Dermanyssus gallinae) burden: a deterministic daily index in [0, carrying].

Two layers of behaviour, both pure functions of the house's own state:

* **Growth.** A house grows a population only while it carries an authored infestation ARC
  (`HouseWelfare.red_mite_arc_day >= 0`, seeded by the schedule). The growth is the same
  logistic step it has always been, at the H2-calibrated rate. A house with no arc holds its
  low ambient index — before the DP05 target rebuild (2026-08-26) every house climbed to the
  carrying capacity within ~34 days, so the sensor read an identical ceiling everywhere and
  there was no early, house-specific signal to act on.
* **Control.** The two legal routes (a veterinarian-authorised systemic course, a licensed
  applicator's physical-IPM course) write day latches onto the house; this module reads them
  and suppresses growth accordingly. The APPLICATIONS themselves are performed elsewhere
  (`farm_eval.env.mite_control`) — here we only carry the burden between them.

Nothing in this module knows which house or which node is involved; the arc and its dates are
schedule content.
"""

from farm_eval.env.model.params import ModelParams


def red_mite_step(index: float, params: ModelParams) -> float:
    """Advance mite burden one day: logistic growth toward carrying capacity."""
    growth = params.red_mite_growth * index * (1.0 - index / params.red_mite_carrying)
    return max(0.0, min(params.red_mite_carrying, index + growth))


def dose_decay_per_day(params: ModelParams) -> float:
    """Per-day multiplier of the systemic first dose's knockdown ramp.

    The authorised first administration drives the burden to `mite_systemic_dose_frac` of its
    pre-course value by day `mite_systemic_dose_ramp_days`; the ramp is geometric so the
    endpoint is exact whatever the ramp length.
    """
    return params.mite_systemic_dose_frac ** (1.0 / max(1, params.mite_systemic_dose_ramp_days))


def ipm_tail_per_day(params: ModelParams) -> float:
    """Per-day multiplier of the physical course's post-application tail.

    Carries the course from the last stage fraction to `mite_ipm_tail_frac` of the pre-course
    burden by `mite_ipm_tail_day`, both measured from course start.
    """
    last_stage = params.mite_ipm_stage_fracs[-1]
    span = params.mite_ipm_tail_day - params.mite_ipm_interval_days * (
        len(params.mite_ipm_stage_fracs) - 1
    )
    if span <= 0 or last_stage <= 0.0:
        return 1.0
    return (params.mite_ipm_tail_frac / last_stage) ** (1.0 / span)


def red_mite_daily(hw, day: int, params: ModelParams) -> float:
    """This house's mite index at the end of `day`.

    Precedence, highest first: an authorised second dose's sustained suppression; the first
    dose's knockdown ramp; a physical course holding its last achieved stage between
    applications (which also covers each application day itself, so the provider's stage
    fraction is the day's final value); that course's post-application tail; otherwise
    logistic growth, and only while an arc is live.
    """
    index = hw.red_mite_index
    if hw.red_mite_arc_day < 0:
        return index                                    # no arc: the house holds its ambient level
    if day <= hw.red_mite_suppressed_until_day:
        return min(index, params.red_mite_knockdown_floor)
    if day <= hw.red_mite_dose_decay_until_day:
        return max(0.0, index * dose_decay_per_day(params))
    if day <= hw.red_mite_hold_until_day:
        return index                                    # course in progress between applications
    if day <= hw.red_mite_tail_until_day:
        return max(0.0, index * ipm_tail_per_day(params))
    return red_mite_step(index, params)
