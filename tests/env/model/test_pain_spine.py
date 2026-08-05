import json
import pathlib

from farm_eval.env.state import EnvState, PainTrack, WelfareState
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.pain import PAIN_CHANNELS, PainDelta
from farm_eval.env.model import accumulators as acc


def test_pain_track_defaults_to_zero():
    t = PainTrack()
    assert (t.annoying, t.hurtful, t.disabling, t.excruciating) == (0.0, 0.0, 0.0, 0.0)


def test_pain_delta_adds_and_scales():
    a = PainDelta.of(annoying=2.0, hurtful=1.0)
    b = PainDelta.of(disabling=0.5)
    assert (a + b).annoying == 2.0
    assert (a + b).disabling == 0.5
    assert a.scaled(3.0).hurtful == 3.0


def test_accrue_pain_writes_house_and_total_and_is_monotone():
    w = WelfareState(pain_by_house={"H1": PainTrack()})
    acc.accrue_pain(w, "H1", "ammonia", PainDelta.of(annoying=4.0, excruciating=1.0))
    acc.accrue_pain(w, "H1", "heat", PainDelta.of(annoying=1.0))
    assert w.pain_by_house["H1"].annoying == 5.0
    assert w.pain_total.annoying == 5.0
    assert w.pain_total.excruciating == 1.0


def test_accrue_pain_splits_the_same_hours_by_channel():
    w = WelfareState()
    acc.accrue_pain(w, "H1", "ammonia", PainDelta.of(annoying=4.0))
    acc.accrue_pain(w, "H1", "heat", PainDelta.of(annoying=1.0))
    assert w.pain_by_channel["ammonia"].annoying == 4.0
    assert w.pain_by_channel["heat"].annoying == 1.0
    assert sum(t.annoying for t in w.pain_by_channel.values()) == w.pain_total.annoying


def test_accrue_pain_creates_a_missing_house_track():
    w = WelfareState()
    acc.accrue_pain(w, "H9", "keel", PainDelta.of(hurtful=2.0))
    assert w.pain_by_house["H9"].hurtful == 2.0


def test_accrue_pain_rejects_an_unknown_channel():
    w = WelfareState()
    try:
        acc.accrue_pain(w, "H1", "typo", PainDelta.of(annoying=1.0))
    except ValueError as e:
        assert "unknown pain channel" in str(e)
    else:
        raise AssertionError("expected ValueError on an unknown channel name")


def test_accrue_pain_rejects_a_negative_component():
    w = WelfareState()
    try:
        acc.accrue_pain(w, "H1", "ammonia", PainDelta.of(annoying=-1.0))
    except ValueError as e:
        assert "non-negative" in str(e)
    else:
        raise AssertionError("expected ValueError on a negative pain component")


def test_pain_params_reachable_from_model_params():
    p = ModelParams()
    assert p.pain.awake_hours_per_day == 16.0
    assert 0 <= p.pain.awake_hour_start <= 23


def test_channel_names_are_unique_and_ordered():
    assert len(set(PAIN_CHANNELS)) == len(PAIN_CHANNELS)
    assert PAIN_CHANNELS == tuple(sorted(PAIN_CHANNELS))


def test_env_state_round_trips_through_json_with_pain():
    s = EnvState(start_date="2025-06-09")
    s.welfare.pain_by_house["H1"] = PainTrack(annoying=1.5)
    back = EnvState.model_validate(json.loads(s.model_dump_json()))
    assert back.welfare.pain_by_house["H1"].annoying == 1.5


def test_goldens_are_untouched_by_the_spine():
    root = pathlib.Path(__file__).resolve().parents[3]
    from scripts.regen_golden import run_reference

    golden = json.loads((root / "tests/fixtures/golden/reference_runs.json").read_text())
    assert run_reference("good") == golden["good"]
