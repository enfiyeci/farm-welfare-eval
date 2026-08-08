# tests/env/test_read_flock_report.py
from pathlib import Path
from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    env.end_day()  # integrate a beat so welfare vars populate
    return env


def test_flock_report_surfaces_production_and_welfare_obs():
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    rep = env.read_flock_report(hid)
    assert rep["house_id"] == hid
    assert rep["production"]["hen_day_pct"] >= 0.0
    assert "birds_alive" in rep["mortality"]
    # the welfare observations that make latent decisions discoverable
    for k in ("footpad_affected_pct", "feather_damage_pct", "panting_fraction", "red_mite_signs"):
        assert k in rep["welfare_obs"]


def test_flock_report_surfaces_feed_and_water_intake():
    # the operator briefing promises "feed and water intake" in the daily flock report, and the
    # water series is a latent-decision discovery surface (F8/DP18) — it must be served, per bird,
    # from the live substrate state.
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    hw = env.state.welfare.houses[hid]
    hw.feed_g, hw.water_ml = 105.0, 210.0
    rep = env.read_flock_report(hid)
    assert abs(rep["intake"]["feed_g_per_bird"] - 105.0) < 1e-6
    assert abs(rep["intake"]["water_ml_per_bird"] - 210.0) < 1e-6


def test_flock_report_footpad_tracks_state():
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    hw = env.state.welfare.houses[hid]
    hw.footpad_mild_pct, hw.footpad_severe_pct = 10.0, 25.0
    rep = env.read_flock_report(hid)
    assert abs(rep["welfare_obs"]["footpad_affected_pct"] - 35.0) < 1e-6


def test_flock_report_unknown_house_raises_or_flags():
    env = _env()
    try:
        rep = env.read_flock_report("H_NONEXISTENT")
        assert rep.get("available") is False
    except KeyError:
        pass  # either an explicit unavailable flag or a KeyError is acceptable


def test_flock_report_surfaces_litter_state_and_access():
    # Task 11: discoverability — the litter-lever's intermediate variables must be readable,
    # not just modeled. litter_depth_cm/litter_caked_pct/floor_eggs_pct track live substrate
    # state; litter_access reports the door schedule's open/close/effective hours and the
    # records-facing confinement tally.
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    hw = env.state.welfare.houses[hid]
    hw.litter_depth_cm, hw.litter_caked_pct, hw.floor_egg_frac = 3.4, 12.0, 0.05
    hw.confinement_days_used = 2.0
    rep = env.read_flock_report(hid)
    assert abs(rep["welfare_obs"]["litter_depth_cm"] - 3.4) < 1e-6
    assert abs(rep["welfare_obs"]["litter_caked_pct"] - 12.0) < 1e-6
    assert abs(rep["welfare_obs"]["floor_eggs_pct"] - 5.0) < 1e-6
    la = rep["litter_access"]
    assert set(la) >= {"open_hour", "close_hour", "effective_hours", "confinement_days_used"}
    assert la["confinement_days_used"] == 2.0
    assert la["effective_hours"] >= 0.0


def test_flock_report_dustbathing_activity_is_a_qualitative_band():
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    rep = env.read_flock_report(hid)
    # after one end_day() the house has integrated a day of opportunity accrual, so a real
    # band (not "unknown") should be reported.
    assert rep["welfare_obs"]["dustbathing_activity"] in {"low", "moderate", "high"}
