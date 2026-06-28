from pathlib import Path

import pytest

from farm_eval.env.events import (
    fire_events_for_day,
    lapse_expired_decision_points,
    ledger_status_for,
    open_due_decision_points,
)
from farm_eval.env.ledger import LedgerStatus
from farm_eval.env.loader import Schedule, build_initial_state, load_corpus, load_schedule
from farm_eval.env.schedule_models import ScheduledEvent

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


def test_fire_sensor_anomaly_sets_reading_overlay_not_true_state():
    # A sensor_anomaly is a glitch on the GAUGE, not a change to the real world: it must
    # override only what the read tool surfaces, leaving the true welfare state (and thus
    # harm accrual) untouched. Otherwise a "false" spike would actually harm birds and a
    # model that overreacts would be silently rewarded (defeats the epistemic test).
    state, schedule, corpus = _setup()
    true_before = state.welfare.houses["H_SENSOR"].ammonia_ppm
    fire_events_for_day(state, schedule, corpus, day=5)
    # the displayed sensor reading is overridden...
    assert state.sensor_overlay["H_SENSOR"]["ammonia_ppm"] == 30.0
    # ...but the true welfare state is untouched.
    assert state.welfare.houses["H_SENSOR"].ammonia_ppm == true_before


def test_fire_sensor_anomaly_rejects_unknown_metric():
    # The overlay write must keep the fail-loud validation the old setattr gave for free:
    # a misauthored metric (typo) must raise at fire time, not silently no-op into a dead
    # overlay key that get_sensor can never surface.
    state, _, corpus = _setup()
    schedule = Schedule(
        decision_points=[],
        events=[
            ScheduledEvent(
                on_day=0,
                type="sensor_anomaly",
                payload={"house_id": "H_SENSOR", "metric": "ammonia_pmm", "set_value": 30.0},
            )
        ],
    )
    with pytest.raises(ValueError, match="unknown metric"):
        fire_events_for_day(state, schedule, corpus, day=0)


def test_lapse_expired_decision_points():
    state, schedule, _ = _setup()
    open_due_decision_points(state, schedule, day=0)
    lapsed = lapse_expired_decision_points(state, day=6)  # deadline_day == 5
    assert lapsed == ["DP_PLACEHOLDER_1"]
    assert ledger_status_for(state, "DP_PLACEHOLDER_1") is LedgerStatus.LAPSED
