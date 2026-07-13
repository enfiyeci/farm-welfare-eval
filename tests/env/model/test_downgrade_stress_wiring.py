"""Stress -> egg-downgrade wiring (owner directive 2026-07-12).

`downgrade_frac(age, stress, params)` always supported a stress term, but the integrator
passed a hard-coded 0.0 — so heat stress and red-mite pressure never touched egg grade
revenue (the QA "mite specks / grader flags" email had no mechanical counterpart). The
integrator now derives per-house stress from panting_fraction + above-threshold red mite
index (previous day's values — deterministic one-day lag).
"""
from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.model.params import ModelParams

FIX = Path(__file__).parent.parent.parent / "fixtures"


def test_stress_coupling_is_live_by_default():
    p = ModelParams()
    assert p.downgrade_stress_coeff > 0.0, "stress->downgrade must be wired, not a dead 0.0 coeff"
    assert p.stress_mite_coeff > 0.0
    assert 0.0 < p.stress_mite_threshold < 1.0


def _downgrade_after_one_day(mite_index: float) -> float:
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    hid = next(h for h in env.state.welfare.houses if env.state.world.bird_count.get(h, 0) > 0)
    env.state.welfare.houses[hid].red_mite_index = mite_index
    env.end_day()
    return env.state.financial.downgrade_dozen_cum


def test_severe_mite_infestation_raises_downgrades():
    clean = _downgrade_after_one_day(0.05)
    infested = _downgrade_after_one_day(0.9)
    assert infested > clean


def test_below_threshold_mites_do_not_move_downgrades():
    p = ModelParams()
    clean = _downgrade_after_one_day(0.0)
    low = _downgrade_after_one_day(p.stress_mite_threshold * 0.5)
    assert low == clean
