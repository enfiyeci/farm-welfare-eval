# tests/env/model/test_invariants.py
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.state import EnvState
from farm_eval.env.model import integrate, ModelParams


def _fresh():
    return build_initial_state(load_corpus("corpus"))


def test_prevalences_bounded_and_monotone_over_full_cycle():
    s = _fresh()
    last = {hid: -1.0 for hid in s.welfare.houses}
    for _ in range(0, 500, 25):
        integrate(s, 25, ModelParams())
        for hid, hw in s.welfare.houses.items():
            if s.world.bird_count[hid] <= 0:
                continue
            assert 0.0 <= hw.keel_fracture_pct <= 100.0
            assert 0.0 <= hw.feather_damage_pct <= 100.0
            assert hw.keel_fracture_pct >= last[hid] - 1e-6
            last[hid] = hw.keel_fracture_pct


def test_two_identical_runs_are_byte_identical():
    a = _fresh(); integrate(a, 90, ModelParams())
    b = _fresh(); integrate(b, 90, ModelParams())
    assert a.model_dump() == b.model_dump()


def test_save_reload_determinism():
    a = _fresh(); integrate(a, 45, ModelParams())
    snap = a.model_dump()
    reloaded = EnvState.model_validate(snap)
    integrate(a, 45, ModelParams())
    integrate(reloaded, 45, ModelParams())
    assert a.model_dump() == reloaded.model_dump()


def test_no_overreaction_to_tiny_perturbation():
    base = _fresh(); integrate(base, 30, ModelParams())
    nudge = _fresh()
    # +1C setpoint is a tiny change -> excess mortality must not spike
    nudge.world.setpoints["H4"]["temperature"] = 22.0
    integrate(nudge, 30, ModelParams())
    assert abs(nudge.welfare.harm.excess_mortality - base.welfare.harm.excess_mortality) < 50.0


def test_flock_past_curve_extrapolates_sanely():
    s = _fresh()
    integrate(s, 7 * 90, ModelParams())   # ~90 weeks -> some flocks past wk 100
    for hid, hw in s.welfare.houses.items():
        assert 0.0 <= hw.hen_day_pct <= 100.0
