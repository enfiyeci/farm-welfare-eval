"""The late-lay mobility / nest-access layer (DPE option D, owner ruling 16, 2026-08-19).

Unit-level: the hazard function's window, its factors, and the accumulator. The end-to-end
"a retrofit really lowers the channel" behaviour lives in tests/env/test_dpe_retrofit.py.
"""

import pytest

from farm_eval.env.model.accumulators import accrue_mobility
from farm_eval.env.model.layers.keel import keel_prevalence_pct
from farm_eval.env.model.layers.mobility import mobility_harm_fraction
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import HarmAccumulators

P = ModelParams()
IN_WINDOW = 53.0  # the DPE beat's own flock age


def test_harm_drops_when_retrofits_are_installed():
    base = mobility_harm_fraction(IN_WINDOW, False, False, P)
    both = mobility_harm_fraction(IN_WINDOW, True, True, P)
    assert base > 0.0
    assert both < base
    assert both == pytest.approx(base * P.mobility_ramp_factor * P.mobility_perch_factor)


def test_each_fitting_helps_on_its_own_and_ramps_help_more():
    base = mobility_harm_fraction(IN_WINDOW, False, False, P)
    ramps = mobility_harm_fraction(IN_WINDOW, True, False, P)
    perch = mobility_harm_fraction(IN_WINDOW, False, True, P)
    assert ramps == pytest.approx(base * P.mobility_ramp_factor)
    assert perch == pytest.approx(base * P.mobility_perch_factor)
    # Ramps are the stronger, better-replicated lever — the rubric's 4-vs-3 split has to be
    # backed by the physics, not just by the points.
    assert ramps < perch < base


def test_channel_accrues_only_inside_the_late_lay_window():
    lo, hi = P.mobility_window_wk
    assert mobility_harm_fraction(lo - 0.1, False, False, P) == 0.0
    assert mobility_harm_fraction(hi + 0.1, False, False, P) == 0.0
    assert mobility_harm_fraction(lo, False, False, P) > 0.0
    assert mobility_harm_fraction(hi, False, False, P) > 0.0


def test_a_retrofit_outside_the_window_changes_nothing():
    lo, _ = P.mobility_window_wk
    assert mobility_harm_fraction(lo - 5.0, True, True, P) == 0.0


def test_harm_tracks_the_age_only_impaired_share():
    # The layer READS keel prevalence as the impaired-bird share; it never writes it. This is
    # the honesty ruling in unit form: a house with both fittings has the SAME keel prevalence
    # as a house with none, and only the mobility number moves.
    expected = keel_prevalence_pct(IN_WINDOW, P) / 100.0 * P.mobility_base_rate
    assert mobility_harm_fraction(IN_WINDOW, False, False, P) == pytest.approx(expected)


def test_accrue_mobility_is_hours():
    h = HarmAccumulators()
    accrue_mobility(h, 0.5, 1.0)
    assert h.mobility_access_hours == pytest.approx(12.0)
    accrue_mobility(h, 0.5, 2.0)
    assert h.mobility_access_hours == pytest.approx(36.0)


def test_accrue_mobility_is_monotone():
    h = HarmAccumulators()
    accrue_mobility(h, -1.0, 1.0)  # a nonsense negative fraction must never pay harm back
    assert h.mobility_access_hours == 0.0
