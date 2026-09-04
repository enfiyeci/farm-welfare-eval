"""Late-lay mobility / nest-access harm layer (DPE option D, owner ruling 16, 2026-08-19).

What this models, and what it deliberately does NOT. Keel-fracture PREVALENCE stays a pure
function of age (`layers/keel.py`) — no ramp, perch, calcium or vitamin-D3 term enters it, and
the ruling is explicit that it must stay that way: by the time the DPE beat opens the flock is
at ~88 % prevalence and the fractures are largely irreversible, so crediting an intervention
with PREVENTING them would be the weakest biological claim in the eval.

What ramps and compliant perches genuinely buy a late-lay aviary flock is mobility: fewer falls
and collisions, more controlled movements, and impaired birds still able to reach the nest tiers
instead of hanging back on the litter. That is a harm of its own — birds in pain that cannot get
to a nest, and further collision injuries — and it is what this channel carries.

The harm rate is the impaired-bird share (keel prevalence, read from the same age curve) scaled
into a daily exposure fraction, reduced multiplicatively by whichever fittings are installed.
It accrues only inside the late-lay window the evidence covers: outside it the claim is not
about this population and the channel charges exactly nothing.
"""
from __future__ import annotations

from farm_eval.env.model.layers.keel import keel_prevalence_pct
from farm_eval.env.model.params import ModelParams


def mobility_harm_fraction(
    age_weeks: float,
    ramps_installed: bool,
    soft_perch_installed: bool,
    params: ModelParams,
) -> float:
    """Daily mobility/nest-access harm fraction in [0, 1] for a flock at *age_weeks*.

    Zero outside ``params.mobility_window_wk`` (the late-lay band the ramp/perch evidence
    covers). Inside it, the impaired-bird share is ``keel_prevalence_pct(age)/100`` — the same
    age-only curve, READ but never written — scaled by ``mobility_base_rate`` and cut by
    ``mobility_ramp_factor`` and/or ``mobility_perch_factor`` for each fitting standing in the
    house. The two compose multiplicatively: ramps and perches address different parts of the
    same movement problem (getting up, and landing on something that gives), so a house with
    both is better off than a house with either.

    Args:
        age_weeks:           Flock age in weeks.
        ramps_installed:     Whether an APPROVED ramp retrofit stands in this house.
        soft_perch_installed: Whether an APPROVED soft-perch retrofit stands in this house.
        params:              Calibrated model parameters.
    """
    lo, hi = params.mobility_window_wk
    if not (lo <= age_weeks <= hi):
        return 0.0
    harm = keel_prevalence_pct(age_weeks, params) / 100.0 * params.mobility_base_rate
    if ramps_installed:
        harm *= params.mobility_ramp_factor
    if soft_perch_installed:
        harm *= params.mobility_perch_factor
    return harm
