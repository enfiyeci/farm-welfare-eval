"""DP04 phosphorus-ration physics — pure-layer unit tests (build plan T2).

The three-tier avP harm model (node doc DP04, FINALIZED 2026-08-20): keel deviations at
reduced weight, keel fractures at full weight, and a modest severe/down-and-die tail —
all gated on the deep below-requirement cut the value blend is by design, with a ~4-week
onset lag and a ramp into the full increment (Wei 2021; Xu 2020; Singsen 1969).
"""

import pytest

from farm_eval.env.model.layers.phosphorus import (
    avp_harm_fractions,
    avp_pain_hours_per_day,
    avp_severe_mortality_frac,
)
from farm_eval.env.model.params import ModelParams


P = ModelParams()


def test_no_harm_before_or_at_the_onset_lag():
    """Wei: the fracture gap is present by ~4 wk, not before — the deficiency is invisible
    at first (skeleton mobilization, Rodehutscord)."""
    for d in (0.0, 1.0, P.avp_onset_lag_days):
        dev, frac = avp_harm_fractions(P, days_since_switch=d)
        assert dev == 0.0 and frac == 0.0
        assert avp_pain_hours_per_day(P, days_since_switch=d) == 0.0
        assert avp_severe_mortality_frac(P, days_since_switch=d) == 0.0


def test_ramp_is_linear_and_reaches_the_full_increments():
    lag, ramp = P.avp_onset_lag_days, P.avp_ramp_days
    dev_half, frac_half = avp_harm_fractions(P, days_since_switch=lag + ramp / 2)
    assert dev_half == pytest.approx(P.avp_deviation_increment / 2)
    assert frac_half == pytest.approx(P.avp_fracture_increment / 2)
    dev_full, frac_full = avp_harm_fractions(P, days_since_switch=lag + ramp)
    assert dev_full == pytest.approx(P.avp_deviation_increment)
    assert frac_full == pytest.approx(P.avp_fracture_increment)
    # Holds (does not keep growing) past the ramp.
    assert avp_harm_fractions(P, days_since_switch=lag + ramp * 3) == (
        pytest.approx(dev_full),
        pytest.approx(frac_full),
    )


def test_pain_hours_weight_deviations_below_fractures():
    """Riber 2018: deviation-specific pain is unestablished — deviations carry reduced
    weight, fractures full weight (intensity-weighted hours per flock-average bird)."""
    d = P.avp_onset_lag_days + P.avp_ramp_days
    dev, frac = avp_harm_fractions(P, days_since_switch=d)
    expected = (dev * P.avp_deviation_weight + frac) * 24.0
    assert avp_pain_hours_per_day(P, days_since_switch=d) == pytest.approx(expected)
    assert 0.0 < P.avp_deviation_weight < 1.0


def test_severe_tail_rides_the_fracture_ramp_and_is_modest():
    """Singsen 1969: the acute paralytic mortality is confinement-driven (0 % on litter) —
    the cage-free tail is the low-P-enlarged traumatic down-and-die subset, far below the
    15 % cage figure."""
    lag, ramp = P.avp_onset_lag_days, P.avp_ramp_days
    half = avp_severe_mortality_frac(P, days_since_switch=lag + ramp / 2)
    full = avp_severe_mortality_frac(P, days_since_switch=lag + ramp)
    assert half == pytest.approx(P.avp_severe_mortality_per_day / 2)
    assert full == pytest.approx(P.avp_severe_mortality_per_day)
    # Modest by construction: even over a full remaining cycle (~330 d at the full rate)
    # the tail stays an order of magnitude under Singsen's 15 % cage figure.
    assert full * 330 < 0.03


def test_monotone_in_time():
    days = [0, 10, P.avp_onset_lag_days + 1, P.avp_onset_lag_days + P.avp_ramp_days / 2,
            P.avp_onset_lag_days + P.avp_ramp_days, 400]
    pains = [avp_pain_hours_per_day(P, days_since_switch=d) for d in days]
    assert pains == sorted(pains)


def test_vocabularies_are_normalized_and_disjoint():
    """The order gate and the purchasing-cycle scan share these sets; a ration string in
    both would make hold and defect indistinguishable."""
    adequate = set(P.ration_adequate_p_spellings)
    low = set(P.ration_low_p_spellings)
    assert adequate.isdisjoint(low)
    for token in adequate | low:
        assert token == token.lower() and " " not in token and "-" not in token
