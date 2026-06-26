# tests/adapter/test_read_sensor_climate.py
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus, load_schedule, build_initial_state
from farm_eval.env.model import integrate, ModelParams


def test_get_sensor_returns_temp_and_humidity():
    corpus = load_corpus("corpus")
    state = build_initial_state(corpus)
    integrate(state, 30, ModelParams())
    env = FarmEnv(corpus, load_schedule("schedule"), state, episode_end_day=520, params=ModelParams())
    t = env.get_sensor("H4", "temp_c")
    rh = env.get_sensor("H4", "humidity")
    assert t.available and t.value is not None
    assert rh.available and 0.0 <= rh.value <= 100.0
