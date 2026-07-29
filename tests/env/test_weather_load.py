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


def test_weather_month_keys_survive_a_json_round_trip():
    """EnvState is serialized to JSON in two places — the play autosave snapshot and the Inspect
    `.eval` log store — and JSON object keys are ALWAYS strings. The month keys must come back as
    ints or `make_ambient`'s `normals[7]` lookup raises KeyError and every day advance dies.
    """
    state = build_initial_state(load_corpus("corpus"))
    restored = type(state).model_validate(state.model_dump(mode="json"))

    normals = restored.weather["monthly_normals_f"]
    assert set(normals) >= {1, 7}, f"month keys degraded to {sorted(normals)!r}"
    assert normals[7]["high"] == 82
    assert normals[1]["high"] == 25


def test_ambient_driver_works_on_a_round_tripped_state():
    """The end-to-end guard: the restored state must actually drive the model, not merely parse."""
    from farm_eval.env.model.drivers import make_ambient

    state = build_initial_state(load_corpus("corpus"))
    restored = type(state).model_validate(state.model_dump(mode="json"))

    ambient = make_ambient(restored.weather, restored.start_date)
    temp_c, rh = ambient(28, 12)  # a July day — the month whose key lookup regressed
    assert -40.0 < temp_c < 60.0
    assert 0.0 <= rh <= 100.0
