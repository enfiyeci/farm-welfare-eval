import pytest

from farm_eval.env.model.pain import heat_pain, is_awake_hour
from farm_eval.env.model.pain_params import PainParams


PP = PainParams()


def test_below_the_danger_threshold_accrues_nothing():
    d = heat_pain(27.0, 0.0, 1000, 1.0, PP)
    assert (d.annoying, d.hurtful, d.disabling) == (0.0, 0.0, 0.0)


def test_the_mild_band_is_annoying_for_the_whole_house():
    assert heat_pain(28.0, 0.5, 1000, 1.0, PP).annoying == pytest.approx(1000.0)


def test_the_mild_band_ignores_panting_entirely():
    # Below 30 the split does not apply — panting must not leak Disabling into the mild band.
    d = heat_pain(28.0, 1.0, 1000, 1.0, PP)
    assert d.disabling == 0.0 and d.hurtful == 0.0


def test_above_thirty_the_house_splits_by_panting_and_sums_to_one_hundred_percent():
    d = heat_pain(31.0, 0.25, 1000, 1.0, PP)
    assert d.disabling == pytest.approx(250.0)
    assert d.hurtful == pytest.approx(750.0)
    assert d.annoying == 0.0
    assert d.disabling + d.hurtful == pytest.approx(1000.0)


def test_no_panting_above_thirty_is_all_hurtful():
    assert heat_pain(31.0, 0.0, 1000, 1.0, PP).hurtful == pytest.approx(1000.0)


def test_full_panting_above_thirty_is_all_disabling():
    assert heat_pain(31.0, 1.0, 1000, 1.0, PP).disabling == pytest.approx(1000.0)


def test_a_panting_fraction_outside_zero_one_fails_loudly():
    with pytest.raises(ValueError, match="panting_fraction"):
        heat_pain(31.0, 1.5, 1000, 1.0, PP)


def test_total_bird_hours_never_exceed_the_house_hour_product():
    for thi in (26.0, 27.5, 29.9, 30.0, 40.0):
        for p in (0.0, 0.5, 1.0):
            d = heat_pain(thi, p, 1000, 1.0, PP)
            assert d.annoying + d.hurtful + d.disabling <= 1000.0 + 1e-9


def test_the_awake_window_is_sixteen_contiguous_hours():
    awake = [h for h in range(24) if is_awake_hour(h, PP)]
    assert len(awake) == 16
    assert awake == list(range(min(awake), min(awake) + 16))


def test_heat_pain_edges_match_the_substrate_thresholds():
    # Drift guard (Global Constraints, write-for-adjustment rule 2): the severe edge is
    # pinned to heat.py's OWN acute-mortality onset, not a duplicated literal, so a substrate
    # recalibration that moves the onset fails here loudly. Deriving the default instead is
    # blocked by the import cycle pain_params -> layers.heat -> params -> pain_params.
    from farm_eval.env.model.layers import heat
    from farm_eval.env.model.params import ModelParams

    p = ModelParams()
    assert p.pain.heat_thi_mild == p.heat_danger_thi
    assert p.pain.heat_thi_severe == heat._MORT_ONSET
