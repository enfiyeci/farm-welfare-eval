from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model.drivers import flock_age_weeks


def test_focal_house_age_progresses():
    state = build_initial_state(load_corpus("corpus"))
    a0 = state.world.age_weeks_at_start["H4"]
    assert a0 == 17.0
    assert flock_age_weeks(a0, 0) == 17.0
    assert flock_age_weeks(a0, 70) == 27.0   # +10 weeks


def test_old_house_age():
    state = build_initial_state(load_corpus("corpus"))
    assert state.world.age_weeks_at_start["H1"] == 68.0
