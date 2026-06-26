# tests/env/test_state_schema.py
from farm_eval.env.state import EnvState, HouseWelfare, HarmAccumulators, WelfareState


def test_house_welfare_new_fields_default():
    hw = HouseWelfare(
        ammonia_ppm=5.0, co2_ppm=2100.0, litter_moisture=20.0,
        lighting_lux=10.0, lighting_hours=12.0, heat_stress_index=0.0, stocking_density=1.0,
    )
    assert hw.temp_c == 21.0 and hw.humidity == 55.0
    assert hw.panting_fraction == 0.0 and hw.keel_fracture_pct == 0.0
    assert hw.feather_damage_pct == 0.0 and hw.hen_day_pct == 0.0


def test_harm_accumulators_default_zero():
    h = HarmAccumulators()
    assert h.nh3_ppm_hours_over == 0.0 and h.heat_stress_hours == 0.0
    assert h.excess_mortality == 0.0 and h.keel_risk_hours == 0.0
    assert h.footpad_out_of_band_hours == 0.0


def test_welfare_state_has_harm_block():
    assert WelfareState().harm.heat_stress_hours == 0.0


def test_state_roundtrips_with_new_fields():
    s = EnvState(start_date="2025-06-09")
    s.welfare.harm.nh3_ppm_hours_over = 12.5
    s2 = EnvState.model_validate(s.model_dump())
    assert s2.welfare.harm.nh3_ppm_hours_over == 12.5
