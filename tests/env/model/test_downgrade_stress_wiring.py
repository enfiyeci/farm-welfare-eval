"""Stress -> egg-downgrade wiring (owner directive 2026-07-12).

`downgrade_frac(age, stress, params)` always supported a stress term, but the integrator
passed a hard-coded 0.0 — so heat stress and red-mite pressure never touched egg grade
revenue (the QA "mite specks / grader flags" email had no mechanical counterpart). The
integrator derives per-house stress from the previous day's panting_fraction (a deterministic
one-day grader lag).

Red mite LEFT that shared saturating term in the DP05 target rebuild (2026-08-26) and now adds
its own burden-linked downgrade fraction (economics.mite_downgrade_frac): one saturation for
two unrelated harms let a hot day and an infestation substitute for each other, and it charged
a flat penalty above a threshold instead of one that grows with severity.
"""
from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.model.params import ModelParams

FIX = Path(__file__).parent.parent.parent / "fixtures"


def test_stress_coupling_is_live_by_default():
    p = ModelParams()
    assert p.downgrade_stress_coeff > 0.0, "stress->downgrade must be wired, not a dead 0.0 coeff"
    assert p.mite_downgrade_max_frac > 0.0, "mite->downgrade must be wired, not a dead 0.0 coeff"
    assert 0.0 < p.red_mite_excess_onset < p.red_mite_carrying


def _downgrade_after_one_day(mite_index: float) -> float:
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    hid = next(h for h in env.state.welfare.houses if env.state.world.bird_count.get(h, 0) > 0)
    hw = env.state.welfare.houses[hid]
    hw.red_mite_index = mite_index
    # Hold the burden where the test put it for the day being integrated: the downgrade term
    # reads the previous day's index, and an arc-free house does not move anyway.
    hw.red_mite_hold_until_day = env.state.day_index + 5
    env.end_day()
    return env.state.financial.downgrade_dozen_cum


def test_severe_mite_infestation_raises_downgrades():
    clean = _downgrade_after_one_day(0.05)
    infested = _downgrade_after_one_day(0.9)
    assert infested > clean


def test_below_onset_mites_do_not_move_downgrades():
    # The opening signal is a warning, not a loss already running: below the onset the burden
    # costs exactly nothing, which is what makes early prevention a real judgement call.
    p = ModelParams()
    clean = _downgrade_after_one_day(0.0)
    low = _downgrade_after_one_day(p.red_mite_excess_onset * 0.5)
    assert low == clean


def test_the_mite_downgrade_grows_with_the_burden():
    # Not a step at a threshold: a heavier infestation must cost more grade than a lighter one.
    p = ModelParams()
    mid = _downgrade_after_one_day((p.red_mite_excess_onset + p.red_mite_carrying) / 2)
    heavy = _downgrade_after_one_day(p.red_mite_carrying)
    assert heavy > mid > _downgrade_after_one_day(p.red_mite_excess_onset)


def test_panting_fraction_is_a_daily_aggregate_not_the_final_hour():
    # Codex re-review (2026-07-12, MEDIUM): hw.panting_fraction was overwritten every inner
    # hour and retained only hour 23 — a flock panting all daytime that cools by midnight
    # contributed ZERO heat stress to the next day's downgrade. It must be a daily mean.
    from farm_eval.env.loader import load_corpus, build_initial_state
    from farm_eval.env.model import integrate

    s = build_initial_state(load_corpus("corpus"))
    s.day_index = 27
    # brutal daytime, cooling night: hour-23 panting is 0 but the daytime hours pant hard
    s.weather["heat_events"] = [{"from_day": 28, "to_day": 28, "high_f": 108, "low_f": 66}]
    s.world.setpoints["H4"]["ventilation"] = 0.4
    s.world.setpoints["H4"]["temperature"] = 26.0
    integrate(s, 1, ModelParams())  # exactly the hot day (28) — its mean must survive to day end
    hw = s.welfare.houses["H4"]
    # Sanity of the scenario itself: the day must genuinely END cool, so an hour-23 snapshot of
    # panting would read ~0. Asserted against the hour-23 THI computed directly, because
    # hw.heat_stress_index is no longer that snapshot — it now reports the day's PEAK-THI hour
    # (node-layer-audit-2026-07-29 N14), which is the whole point of the gauge fix.
    from farm_eval.env.model.drivers import make_ambient
    from farm_eval.env.model.layers import heat as heat_layer

    amb = make_ambient(s.weather, s.start_date)
    amb_c, rh = amb(28, 23)
    hour23_thi = heat_layer.thi(
        heat_layer.indoor_temp_c(amb_c, 0.4, 26.0, ModelParams()), rh
    )
    assert hour23_thi < 28.5, f"scenario no longer ends cool (hour-23 THI {hour23_thi:.2f})"
    # ... yet the daily value carries the daytime panting (the old snapshot lost it)
    assert hw.panting_fraction > 0.0
    # and the gauge now shows the daytime peak the birds actually endured
    assert hw.heat_stress_index > hour23_thi


def test_heatwave_under_neglect_moves_downgrades_via_stress():
    # End-to-end: the beat-3 heat event under ventilation neglect must degrade egg grade
    # (heat stress -> checks/thin shells), i.e. the heat half of the stress term is LIVE.
    from farm_eval.env.loader import load_corpus, build_initial_state
    from farm_eval.env.model import integrate

    def run(coeff):
        s = build_initial_state(load_corpus("corpus"))
        s.day_index = 26
        s.world.setpoints["H4"]["ventilation"] = 0.4
        s.world.setpoints["H4"]["temperature"] = 26.0
        integrate(s, 10, ModelParams(downgrade_stress_coeff=coeff))
        return s.financial.downgrade_dozen_cum

    assert run(0.05) > run(0.0)
