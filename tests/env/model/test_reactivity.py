# tests/env/model/test_reactivity.py
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams


def _run(setpoint_overrides: dict, days=21):
    s = build_initial_state(load_corpus("corpus"))
    for hid, sp in setpoint_overrides.items():
        s.world.setpoints[hid].update(sp)
    integrate(s, days, ModelParams())
    return s


def test_more_ventilation_reduces_ammonia_ppm_hours():
    low = _run({"H4": {"ventilation": 0.5}})
    high = _run({"H4": {"ventilation": 3.0}})
    assert high.welfare.harm.nh3_ppm_hours_over < low.welfare.harm.nh3_ppm_hours_over


def test_belt_frequency_cuts_ammonia():
    slow = _run({"H4": {"belt_interval_days": 4}})
    fast = _run({"H4": {"belt_interval_days": 1}})
    assert fast.welfare.houses["H4"].ammonia_ppm < slow.welfare.houses["H4"].ammonia_ppm


def test_cooling_during_heatwave_cuts_heat_hours():
    # run across the day-28 heat event; high ventilation should reduce heat-stress-hours
    s_hot = build_initial_state(load_corpus("corpus")); s_hot.day_index = 26
    s_hot.world.setpoints["H4"]["ventilation"] = 0.3
    integrate(s_hot, 10, ModelParams())
    s_cool = build_initial_state(load_corpus("corpus")); s_cool.day_index = 26
    s_cool.world.setpoints["H4"]["ventilation"] = 3.0
    integrate(s_cool, 10, ModelParams())
    assert s_cool.welfare.harm.heat_stress_hours < s_hot.welfare.harm.heat_stress_hours


def test_wet_litter_couples_ammonia_and_footpad():
    s = build_initial_state(load_corpus("corpus"))
    s.welfare.houses["H4"].litter_moisture = 40.0
    integrate(s, 21, ModelParams())
    dry = build_initial_state(load_corpus("corpus"))
    dry.welfare.houses["H4"].litter_moisture = 20.0
    integrate(dry, 21, ModelParams())
    assert s.welfare.houses["H4"].ammonia_ppm > dry.welfare.houses["H4"].ammonia_ppm
    assert (s.welfare.houses["H4"].footpad_mild_pct + s.welfare.houses["H4"].footpad_severe_pct) \
        > (dry.welfare.houses["H4"].footpad_mild_pct + dry.welfare.houses["H4"].footpad_severe_pct)


def test_heat_raises_water_intake():
    # water_ml is a last-hour snapshot of water_ml_base * water_multiplier(indoor temp).
    # Integrate so the run ENDS inside the day-28..32 heat event, and compare a poorly
    # ventilated (hot) house against a well-ventilated (cool) one at the SAME day and age.
    # Heat must raise water demand above the cool counterfactual — this fails if
    # water_multiplier stops responding to temperature (the old test passed even then,
    # because it ended post-heatwave at the 2.0x floor where water_ml == 1.76x feed always).
    hot = build_initial_state(load_corpus("corpus"))
    hot.day_index = 28
    hot.world.setpoints["H4"]["ventilation"] = 0.3
    integrate(hot, 2, ModelParams())          # ends day 30, inside the heat event

    cool = build_initial_state(load_corpus("corpus"))
    cool.day_index = 28
    cool.world.setpoints["H4"]["ventilation"] = 3.0
    integrate(cool, 2, ModelParams())

    hot_h4 = hot.welfare.houses["H4"]
    cool_h4 = cool.welfare.houses["H4"]
    # Same age/feed baseline; only ventilation (hence indoor heat) differs.
    assert hot_h4.water_ml > cool_h4.water_ml
    # And the hot house is genuinely above the 2.0x water:feed floor (heat multiplier engaged).
    assert hot_h4.water_ml > hot_h4.feed_g * 2.0
