from farm_eval.env.loader import load_corpus, build_initial_state


def test_weather_loaded(tmp_path):
    corpus = load_corpus("corpus")
    w = corpus.weather
    assert set(w["monthly_normals_f"].keys()) >= {1, 7}
    assert w["monthly_normals_f"][7]["high"] == 82
    assert w["monthly_normals_f"][1]["high"] == 25
    assert any(28 >= ev["from_day"] and ev["to_day"] >= 28 for ev in w["heat_events"])


def test_state_carries_weather():
    s = build_initial_state(load_corpus("corpus"))
    assert s.weather["monthly_normals_f"][7]["high"] == 82
