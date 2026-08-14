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


def test_belt_frequency_drives_litter_moisture_footpad_and_ammonia():
    # Litter moisture is now belt-driven, so footpad is an AGENT-CONTROLLABLE lever via
    # belt_interval_days: frequent belts keep litter drier than infrequent belts, and the
    # wetter house develops more lesions. Ammonia rides the same lever (wetter litter + more
    # manure accumulation → more NH3). Run long enough for the litter to relax to its
    # belt equilibrium and footpad to develop on the wet house.
    #
    # H4's real, authored stocking (Task 7: density loads the litter through the corrected
    # 23.0 hens/m2 reference) is 19.1 hens/m2 -- density_factor ~0.83, BELOW the reference --
    # so under H4's inherited 11:00-21:00 door schedule the water-peak transient no longer
    # clears the 30% footpad threshold on either arm (it now peaks at ~29.9% on the slow arm,
    # a hair under). The door override below is not part of what this test means to exercise;
    # it only restores enough litter access, on BOTH arms equally, for the belt lever's own
    # effect on footpad to be legible again.
    fast = _run({"H4": {"belt_interval_days": 1, "litter_access_open_hour": 9.0}}, days=120)
    slow = _run({"H4": {"belt_interval_days": 7, "litter_access_open_hour": 9.0}}, days=120)
    f = fast.welfare.houses["H4"]
    s = slow.welfare.houses["H4"]
    # Frequent belts → drier litter than infrequent belts.
    assert f.litter_moisture < s.litter_moisture
    # Frequent belts → measurably less footpad than infrequent belts.
    fp_fast = f.footpad_mild_pct + f.footpad_severe_pct
    fp_slow = s.footpad_mild_pct + s.footpad_severe_pct
    assert fp_fast < fp_slow
    assert fp_slow > 0.0
    # Ammonia coupling holds through the same belt lever.
    assert f.ammonia_ppm < s.ammonia_ppm


# NOTE (litter-integration merge): the former
# `test_authored_occupied_house_belt_cadence_activates_dp16_signal` was removed here. It was a
# main-branch (wave-2) test asserting that the authored corpus starts every occupied house on a
# slow belt cadence (`belt_interval_days >= 5`) and that this alone drives H4's footpad severe
# prevalence above 0 by day 196. The litter-lever wave legitimately superseded both premises:
# it rewrote DP16 so footpad is driven by the litter-door water balance (not the belt cadence —
# the belt term alone cannot reach the footpad onset), and its recalibrated corpus carries no
# per-house `belt_interval_days` override (default 2). DP16's signal is now covered by
# tests/env/test_dp16_signature.py; belt→litter→footpad reactivity by
# test_belt_frequency_drives_litter_moisture_footpad_and_ammonia above.


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
