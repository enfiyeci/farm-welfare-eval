from pathlib import Path

from farm_eval.env.events import (
    fire_events_for_day,
    lapse_expired_decision_points,
    ledger_status_for,
    open_due_decision_points,
)
from farm_eval.env.ledger import LedgerStatus
from farm_eval.env.loader import build_initial_state, load_corpus, load_schedule

FIX = Path(__file__).parent.parent / "fixtures"


def _setup():
    corpus = load_corpus(FIX / "corpus")
    schedule = load_schedule(FIX / "schedule")
    state = build_initial_state(corpus)
    return state, schedule, corpus


def test_open_due_decision_points():
    state, schedule, _ = _setup()
    opened = open_due_decision_points(state, schedule, day=0)
    assert opened == ["DP_PLACEHOLDER_1"]
    assert ledger_status_for(state, "DP_PLACEHOLDER_1") is LedgerStatus.OPEN
    # idempotent: opening again the same/next day does not duplicate
    assert open_due_decision_points(state, schedule, day=1) == []


def test_fire_email_event_appends_to_mailbox():
    state, schedule, corpus = _setup()
    fired = fire_events_for_day(state, schedule, corpus, day=0)
    assert len(fired) == 1
    assert len(state.mailbox) == 1
    assert state.mailbox[0].subject == "PLACEHOLDER"
    assert state.mailbox[0].body.startswith("PLACEHOLDER")


def test_fire_sensor_anomaly_sets_value():
    state, schedule, corpus = _setup()
    fire_events_for_day(state, schedule, corpus, day=5)
    assert state.welfare.houses["H_SENSOR"].ammonia_ppm == 30.0


def test_lapse_expired_decision_points():
    state, schedule, _ = _setup()
    open_due_decision_points(state, schedule, day=0)
    lapsed = lapse_expired_decision_points(state, day=6)  # deadline_day == 5
    assert lapsed == ["DP_PLACEHOLDER_1"]
    assert ledger_status_for(state, "DP_PLACEHOLDER_1") is LedgerStatus.LAPSED
