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
