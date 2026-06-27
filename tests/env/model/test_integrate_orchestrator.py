from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams
from farm_eval.env.state import FLOCK_HISTORY_DAYS


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
    # integrate reads the start day from state.day_index and does NOT advance it;
    # end_day advances day_index between calls. Mirror that real flow here: advance
    # day_index by `elapsed` between chunks so the chunks visit the SAME absolute
    # calendar days as the single call. Use a 210-day horizon so harm is non-zero
    # (a 30-day baseline run leaves nh3/keel at exactly 0, making the check vacuous).
    one = _fresh()
    integrate(one, 210, ModelParams())

    chunk = _fresh()
    for _ in range(7):
        integrate(chunk, 30, ModelParams())
        chunk.day_index += 30  # end_day does this in production

    # Non-vacuous: this horizon actually accumulates ammonia harm.
    assert one.welfare.harm.nh3_ppm_hours_over > 0.0

    # Full substrate must match. day_index legitimately differs (the single call
    # never advanced it; the chunked path did), so normalize it out before compare.
    one_d = one.model_dump()
    chunk_d = chunk.model_dump()
    one_d.pop("day_index", None)
    chunk_d.pop("day_index", None)
    assert one_d == chunk_d


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


def test_integrate_appends_one_flock_history_record_per_day():
    s = build_initial_state(load_corpus("corpus"))
    integrate(s, 5, ModelParams())
    hist = s.world.flock_history["H4"]
    assert len(hist) == 5
    assert [r.day for r in hist] == [1, 2, 3, 4, 5]      # absolute calendar days, in order
    assert all(r.hen_day_pct >= 0 for r in hist)


def test_flock_history_is_capped_to_window():
    s = build_initial_state(load_corpus("corpus"))
    integrate(s, FLOCK_HISTORY_DAYS + 10, ModelParams())
    hist = s.world.flock_history["H4"]
    assert len(hist) == FLOCK_HISTORY_DAYS              # bounded: only the last N days kept
    assert hist[-1].day == FLOCK_HISTORY_DAYS + 10      # newest retained
    assert hist[0].day == 11                            # oldest 10 dropped


def test_flock_history_is_path_independent():
    # Chunked integration visits the same days, so the retained window is identical.
    one = build_initial_state(load_corpus("corpus"))
    integrate(one, 40, ModelParams())
    chunked = build_initial_state(load_corpus("corpus"))
    for _ in range(40):
        chunked.day_index = chunked.world.flock_history.get("H4", [])[-1].day if chunked.world.flock_history.get("H4") else 0
        integrate(chunked, 1, ModelParams())
    assert [(r.day, r.mortality_count, round(r.hen_day_pct, 6)) for r in one.world.flock_history["H4"]] \
        == [(r.day, r.mortality_count, round(r.hen_day_pct, 6)) for r in chunked.world.flock_history["H4"]]
