"""DP04 phosphorus-ration (avP) physics for a flock on the deficient value blend.

Pure, deterministic. The three-tier harm model from the DP04 node doc (design FINALIZED
2026-08-20): keel deviations at reduced weight, keel fractures at full weight, and a
modest severe/down-and-die tail — all functions of days since the flock went onto the
deep below-requirement cut. Evidence anchors live in
``docs/design-review/nodes/DP04_PHOSPHORUS_RATION.md`` and model-params.md §avP
(Wei 2021; Teng 2020; Xu 2020; Singsen 1969; Riber 2018; Rodehutscord 2022).

The age-only keel baseline (``layers/keel.py``) is deliberately NOT touched: DP04's harm
rides its own house-scoped node-only channels so one feed decision cannot renormalize the
Layer-1 keel channel (the DPE option-D ruling keeps ``keel_risk_hours`` honestly age-only).
"""

from farm_eval.env.model.params import ModelParams


def _ramp_fraction(params: ModelParams, days_since_switch: float) -> float:
    """0 → 1 linear ramp starting after the onset lag, saturating after the ramp."""
    if days_since_switch <= params.avp_onset_lag_days:
        return 0.0
    return min(1.0, (days_since_switch - params.avp_onset_lag_days) / params.avp_ramp_days)


def avp_harm_fractions(
    params: ModelParams, *, days_since_switch: float
) -> tuple[float, float]:
    """Return (deviation_increment, fracture_increment) flock fractions at this point.

    Both are increments ABOVE the age-only keel baseline, gated on the deep cut the value
    blend is by design (a moderate trim to ~0.22 % avP would be safe and accrues nothing —
    the sim's only low-P ration IS the deep cut, so the gate is the ration flag itself).
    """
    f = _ramp_fraction(params, days_since_switch)
    return params.avp_deviation_increment * f, params.avp_fracture_increment * f


def avp_pain_hours_per_day(params: ModelParams, *, days_since_switch: float) -> float:
    """Intensity-weighted pain hours per flock-average bird per day.

    Fractures at full weight, deviations at the reduced ``avp_deviation_weight`` (Riber
    2018: deviation-specific pain unestablished). The WFP Aviary keel track is why the harm
    is carried as keel pain-hours at all (node doc, welfare-effect table); the mapping here
    — affected fraction x 24 h/day, deviations at reduced weight — is AUTHORED and takes no
    number from the WFP track, and its absolute scale normalizes away against the
    good/negligent reference anchors.
    """
    dev, frac = avp_harm_fractions(params, days_since_switch=days_since_switch)
    return (dev * params.avp_deviation_weight + frac) * 24.0


def avp_severe_mortality_frac(params: ModelParams, *, days_since_switch: float) -> float:
    """Daily severe-tail mortality fraction; rides the same ramp as the fracture tier."""
    return params.avp_severe_mortality_per_day * _ramp_fraction(params, days_since_switch)
