import pytest

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.heat import (
    thi, stull_wet_bulb_c, panting_fraction, heat_mortality_frac, water_multiplier,
    indoor_temp_c,
)


def test_stull_wet_bulb_reproduces_the_papers_own_example():
    # Stull 2011 (J. Appl. Meteorol. Climatol. 50:2267-2269) works 20.0 degC / RH 50 %
    # to Twb = 13.7 degC in the text.
    assert stull_wet_bulb_c(20.0, 50.0) == pytest.approx(13.7, abs=0.1)


def test_thi_is_zulovich_deshazer_on_the_kang_scale():
    # The 2026-08-09 source-verification doc's worked example: 36 degC / 45 % RH reads
    # ~32.1 on the Zulovich degC scale (the value Kang 2020 actually reports), where the
    # retired Thom formula read ~29.5. This is the scale every threshold now cites.
    assert thi(36.0, 45.0) == pytest.approx(32.1, abs=0.2)
    # 0.6*Tdb + 0.4*Twb identity at saturation: wet-bulb approaches dry-bulb, so THI -> T.
    assert thi(30.0, 99.0) == pytest.approx(30.0, abs=0.35)


def test_thi_rises_with_humidity_at_fixed_temperature():
    assert thi(30.0, 80.0) > thi(30.0, 30.0)


def test_panting_onset_at_thi_28_5():
    assert panting_fraction(28.0) == 0.0
    assert 0.0 < panting_fraction(29.25) < 1.0
    assert panting_fraction(30.0) == 1.0


def test_no_acute_mortality_below_kang_gradual_arm_peak():
    # Kang 2020's progressive arm reached index 31.2 over 6 h with zero mortality; the
    # model is threshold+duration (no rate-of-rise), so the onset sits AT 31.2 and the
    # gradual arm stays clean by construction.
    p = ModelParams()
    assert heat_mortality_frac(31.0, hours_over_onset=6, params=p) == 0.0
    assert heat_mortality_frac(31.19, hours_over_onset=6, params=p) == 0.0
    assert heat_mortality_frac(31.3, hours_over_onset=1, params=p) > 0.0


def test_kang_shape_duration_escalates_and_magnitude_stays_field_scale():
    # Kang 2020's SHAPE at an AUTHORED field magnitude (the register: "authored calibration
    # on Kang 2020's shape, Riquena 2019 field bounds"). Duration matters as much as peak:
    # the fifth sustained hour at index 32 runs an order of magnitude above the first. The
    # lab's >95%-in-5h endpoint is deliberately NOT reproduced (no coefficient pair holds
    # it without wiping any commercial profile in the same THI neighborhood — heat.py
    # docstring); five sustained hours stay under the daily cap's scale.
    p = ModelParams()
    first = heat_mortality_frac(32.0, hours_over_onset=1, params=p)
    fifth = heat_mortality_frac(32.0, hours_over_onset=5, params=p)
    assert fifth > 10 * first
    total = sum(
        min(1.0, heat_mortality_frac(32.0, hours_over_onset=h, params=p))
        for h in range(1, 6)
    )
    assert 0.001 < total < 0.10


def test_sustained_extreme_heat_is_severe():
    # Sustained extreme heat accumulates real mortality; a 1h just-over-onset blip does not
    blip = heat_mortality_frac(31.5, hours_over_onset=1, params=ModelParams())
    sustained = heat_mortality_frac(33.0, hours_over_onset=5, params=ModelParams())
    assert sustained > 10 * blip


def test_water_rises_with_heat_to_the_sourced_5_to_1():
    # Hendrix-Genetics: ~2:1 thermoneutral rising to ~5:1 under heat. The old 8.0
    # endpoint exceeded every source (2026-08-09 verification doc).
    assert water_multiplier(15.0) == 2.0
    assert water_multiplier(38.0) == 5.0
    assert 2.0 < water_multiplier(30.0) < 5.0


def test_indoor_rises_when_ventilation_cannot_cope():
    p = ModelParams()
    cool = indoor_temp_c(ambient_c=35.0, ventilation=3.0, setpoint_c=21.0, params=p)
    hot = indoor_temp_c(ambient_c=35.0, ventilation=0.3, setpoint_c=21.0, params=p)
    assert hot > cool                      # low ventilation -> hotter barn
    assert indoor_temp_c(20.0, 1.0, 21.0, p) <= 21.5   # mild day stays near setpoint
