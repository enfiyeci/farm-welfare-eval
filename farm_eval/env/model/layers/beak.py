"""Beak-decision physics for a placed flock. Pure, deterministic.

Magnitudes are AUTHORED/DERIVED and tunable; evidence anchors live in
``docs/design-review/nodes/DPD_BEAK_TRIMMING.md`` and the 2026-08-19 research
notes. Trim pain uses a standard house-scoped intensity-weighted-hours
accumulator pending the future welfare-currency migration.

The method vocabulary has ONE source: the key set of ``ModelParams.trim_pain_acute``,
which the order gate validates against and which a test pins equal across all three
per-method dicts (batch-10 review I6 — the first build carried a separate
``TRIM_METHODS`` constant that nothing used and that read the CLASS default, stale
under any params override).
"""

from farm_eval.env.model.params import ModelParams


def beak_feather_multiplier(
    params,
    *,
    beak_treatment: str,
    strain_low_pecking: bool,
    rearing_match: bool,
) -> float:
    """Return the beak-policy multiplier on the feather-damage rate."""
    multiplier = 1.0
    if beak_treatment == params.beak_no_trim_method:
        multiplier *= params.feather_intact_factor
    if strain_low_pecking:
        multiplier *= params.feather_strain_factor
    if rearing_match:
        multiplier *= params.feather_rearing_match_factor
    return multiplier


def trim_pain_pulse(params, *, beak_treatment: str) -> tuple[float, float]:
    """Return one-time acute and per-day chronic intensity-weighted hours."""
    acute = params.trim_pain_acute.get(beak_treatment, 0.0)
    chronic = params.trim_pain_chronic_per_day.get(beak_treatment, 0.0)
    return acute, chronic


def beak_cannibalism_multiplier(
    params, *, beak_treatment: str, strain_low_pecking: bool
) -> float:
    """Return the beak-policy multiplier on feather-driven cannibalism mortality.

    A hard lookup on purpose (batch-10 review I6): every state the placement can write
    is a validated method key, so a miss here is a params/state bug, and a silent 1.0
    would treat an unknown method as a proper trim — the same silent-neutral failure
    the indemnity module refuses for the same reason.
    """
    multiplier = params.beak_cannibalism_factor[beak_treatment]
    if strain_low_pecking:
        multiplier *= params.cannib_strain_factor
    return multiplier
