from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.heat import (
    thi, panting_fraction, heat_mortality_frac, water_multiplier, indoor_temp_c,
)


def test_panting_onset_at_thi_28_5():
    assert panting_fraction(28.0) == 0.0
    assert 0.0 < panting_fraction(29.25) < 1.0
    assert panting_fraction(30.0) == 1.0


def test_no_acute_mortality_below_thi_30():
    assert heat_mortality_frac(29.0, hours_over_30=0, params=ModelParams()) == 0.0


def test_sustained_extreme_heat_is_severe():
    # THI 33 sustained >2h accumulates real mortality; a 1h THI 31 blip does not
    blip = heat_mortality_frac(31.0, hours_over_30=1, params=ModelParams())
    sustained = heat_mortality_frac(33.0, hours_over_30=5, params=ModelParams())
    assert sustained > 10 * blip


def test_water_rises_with_heat():
    assert water_multiplier(15.0) == 2.0
    assert water_multiplier(38.0) == 8.0
    assert 2.0 < water_multiplier(30.0) < 8.0


def test_indoor_rises_when_ventilation_cannot_cope():
    p = ModelParams()
    cool = indoor_temp_c(ambient_c=35.0, ventilation=3.0, setpoint_c=21.0, params=p)
    hot = indoor_temp_c(ambient_c=35.0, ventilation=0.3, setpoint_c=21.0, params=p)
    assert hot > cool                      # low ventilation -> hotter barn
    assert indoor_temp_c(20.0, 1.0, 21.0, p) <= 21.5   # mild day stays near setpoint
