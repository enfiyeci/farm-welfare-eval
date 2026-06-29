from pathlib import Path

import pytest

from farm_eval.env.loader import load_corpus, build_initial_state, Schedule
from farm_eval.env.schedule_models import ScheduledEvent, EventType
from farm_eval.env.events import fire_events_for_day

FIX = Path(__file__).parent.parent / "fixtures"


def _seed(field, value, house="H4"):
    corpus = load_corpus(FIX / "corpus")
    state = build_initial_state(corpus)
    house_id = next(iter(state.welfare.houses))  # a real house in the fixture
    sched = Schedule(events=[ScheduledEvent(on_day=0, type=EventType.STATE_SEED,
                     payload={"house_id": house_id, "field": field, "value": value})])
    fire_events_for_day(state, sched, corpus, day=0)
    return state.welfare.houses[house_id]


def test_state_seed_sets_bool_se_status():
    hw = _seed("se_status", True)
    assert hw.se_status is True


def test_state_seed_sets_int_hpai_onset_day():
    hw = _seed("hpai_onset_day", 246)
    assert hw.hpai_onset_day == 246


def _fire(payload):
    corpus = load_corpus(FIX / "corpus")
    state = build_initial_state(corpus)
    sched = Schedule(events=[ScheduledEvent(on_day=0, type=EventType.STATE_SEED, payload=payload)])
    fire_events_for_day(state, sched, corpus, day=0)


def test_state_seed_rejects_unknown_house():
    with pytest.raises(ValueError):
        _fire({"house_id": "NO_SUCH_HOUSE", "field": "se_status", "value": True})


def test_state_seed_rejects_non_field_attribute():
    # Only declared HouseWelfare data fields may be seeded — not methods/dunders/model internals.
    corpus = load_corpus(FIX / "corpus")
    state = build_initial_state(corpus)
    house_id = next(iter(state.welfare.houses))
    with pytest.raises(ValueError):
        _fire({"house_id": house_id, "field": "model_config", "value": {}})
