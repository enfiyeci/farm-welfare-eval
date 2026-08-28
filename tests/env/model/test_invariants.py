# tests/env/model/test_invariants.py
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.state import EnvState
from farm_eval.env.model import integrate, ModelParams


def _fresh():
    return build_initial_state(load_corpus("corpus"))


def test_prevalences_bounded_and_monotone_over_full_cycle():
    s = _fresh()
    last = {hid: -1.0 for hid in s.welfare.houses}
    saw_keel_rise = False
    for _ in range(0, 500, 25):
        integrate(s, 25, ModelParams())
        s.day_index += 25  # mirror end_day; without this the loop re-processes the same days
        for hid, hw in s.welfare.houses.items():
            if s.world.bird_count[hid] <= 0:
                continue
            assert 0.0 <= hw.keel_fracture_pct <= 100.0
            assert 0.0 <= hw.feather_damage_pct <= 100.0
            assert hw.keel_fracture_pct >= last[hid] - 1e-6
            if hw.keel_fracture_pct > last[hid] + 1e-6 and last[hid] >= 0.0:
                saw_keel_rise = True
            last[hid] = hw.keel_fracture_pct
    # non-vacuity: at least one house's keel must actually INCREASE across the cycle
    assert saw_keel_rise, "keel curve never rose — test would be vacuous"


def test_two_identical_runs_are_byte_identical():
    a = _fresh(); integrate(a, 90, ModelParams())
    b = _fresh(); integrate(b, 90, ModelParams())
    assert a.model_dump() == b.model_dump()


def test_save_reload_determinism():
    a = _fresh(); integrate(a, 45, ModelParams()); a.day_index += 45
    snap = a.model_dump()
    reloaded = EnvState.model_validate(snap)
    integrate(a, 45, ModelParams())
    integrate(reloaded, 45, ModelParams())
    assert a.model_dump() == reloaded.model_dump()
    # non-vacuity: state actually advanced (keel risk accrued by day 90)
    assert a.welfare.harm.keel_risk_hours > 0.0


def test_no_overreaction_to_tiny_perturbation():
    # "No overreaction": a tiny continuous input change must produce a small, bounded
    # output change. Setpoint perturbation is inert here (indoor=max(setpoint, ambient-cooling),
    # and ambient-cooling binds), and excess_mortality is structurally 0 under corpus weather.
    # So perturb VENTILATION slightly in a low-vent regime where ammonia harm is non-zero and
    # responds continuously, and bound the relative swing in nh3_ppm_hours_over.
    def run(vent):
        s = _fresh()
        s.world.setpoints["H4"]["ventilation"] = vent
        integrate(s, 30, ModelParams())
        return s.welfare.harm.nh3_ppm_hours_over
    # 0.15, not 0.50: the gap-D field recalibration puts a 0.5-vent summer house under
    # the 15 ppm threshold (0 accrual), so the low-vent regime must be deep for the bound
    # to stay non-vacuous — and comfortably PAST the threshold crossing: the accrual is
    # (ppm − 15)·hours, a rectifier, so a regime sitting right at 15 amplifies any input
    # nudge in RELATIVE terms without the underlying ppm response being discontinuous.
    base = run(0.15)
    nudge = run(0.153)  # +2% ventilation — a tiny perturbation
    assert base > 0.0, "low-vent regime must accrue ammonia harm (else the bound is vacuous)"
    # A 2% input nudge must not cause a disproportionate output swing. The inverse
    # clearing form makes the response ~1/vent, so a 2% nudge moves the target ~2%.
    assert abs(nudge - base) <= 0.10 * base


def test_flock_past_curve_extrapolates_sanely():
    s = _fresh()
    integrate(s, 7 * 90, ModelParams())   # ~90 weeks -> some flocks past wk 100
    saw_decline = False
    for hid, hw in s.welfare.houses.items():
        if s.world.bird_count[hid] <= 0:
            continue
        assert 0.0 <= hw.hen_day_pct <= 100.0
        if hw.hen_day_pct < 90.0:  # declining tail, not stuck at peak ~95%
            saw_decline = True
    assert saw_decline, "no house reached the declining tail — extrapolation not exercised"
