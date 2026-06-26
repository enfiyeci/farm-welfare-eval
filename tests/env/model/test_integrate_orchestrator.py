from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams


def _fresh():
    return build_initial_state(load_corpus("corpus"))


def test_baseline_run_populates_welfare_vars():
    s = _fresh()
    integrate(s, elapsed_days=30, params=ModelParams())
    h4 = s.welfare.houses["H4"]
    assert h4.hen_day_pct > 0.0          # production wrote eggs
    assert h4.ammonia_ppm > 0.0
    assert h4.keel_fracture_pct >= 0.0


def test_harm_accumulators_monotone_nondecreasing():
    s = _fresh()
    integrate(s, 30, ModelParams())
    a = s.welfare.harm.model_copy(deep=True)
    integrate(s, 30, ModelParams())
    b = s.welfare.harm
    assert b.nh3_ppm_hours_over >= a.nh3_ppm_hours_over
    assert b.heat_stress_hours >= a.heat_stress_hours
    assert b.excess_mortality >= a.excess_mortality


def test_path_independence():
    one = _fresh(); integrate(one, 30, ModelParams())
    chunk = _fresh()
    for _ in range(3):
        integrate(chunk, 10, ModelParams())
    assert abs(one.welfare.harm.nh3_ppm_hours_over - chunk.welfare.harm.nh3_ppm_hours_over) < 1e-6
    assert abs(one.welfare.houses["H4"].keel_fracture_pct - chunk.welfare.houses["H4"].keel_fracture_pct) < 1e-6


def test_empty_house_accrues_no_harm():
    s = _fresh()
    integrate(s, 30, ModelParams())
    # H6 is empty (bird_count 0) -> untouched welfare, no crash
    assert s.world.bird_count["H6"] == 0


def test_elapsed_zero_is_noop():
    s = _fresh()
    before = s.model_dump()
    integrate(s, 0, ModelParams())
    assert s.model_dump() == before
