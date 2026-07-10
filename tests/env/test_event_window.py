"""Window-based event firing: mail scheduled on skipped days arrives as dated backlog at the
next wake-up (`no_wake`), never creating a beat of its own. WS4 skip-residue + WS6 day-0 backlog."""
import pytest
from pydantic import ValidationError

from farm_eval.env.episode import FarmEnv
from farm_eval.env.events import fire_events_in_window
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.schedule_models import ScheduledEvent
from farm_eval.env.state import EnvState, HouseWelfare


def _ev(day: int, subject: str, **kw) -> ScheduledEvent:
    payload = {"from": "a@x.com", "to": "agent@x.com", "subject": subject, "body": "b"}
    payload.update(kw.pop("payload", {}))
    return ScheduledEvent(on_day=day, type="email", payload=payload, **kw)


def _house() -> HouseWelfare:
    return HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )


def _env(events: list[ScheduledEvent], end_day: int = 30) -> FarmEnv:
    corpus = Corpus(company={"agent_email": "agent@x.com", "start_date": "2025-06-09"})
    schedule = Schedule(decision_points=[], events=events)
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["H1"] = _house()
    state.world.bird_count["H1"] = 1000
    state.world.age_weeks_at_start["H1"] = 30.0
    state.world.litter_age_days["H1"] = 10.0
    state.world.setpoints["H1"] = {"ventilation": 1.0}
    return FarmEnv(corpus, schedule, state, episode_end_day=end_day, params=ModelParams())


def test_no_wake_event_does_not_create_a_beat():
    schedule = Schedule(events=[_ev(5, "beat"), _ev(3, "residue", no_wake=True)])
    assert schedule.event_days() == [5]


def test_no_wake_mail_delivered_at_next_beat_with_its_own_date():
    env = _env([_ev(10, "beat mail"), _ev(4, "residue", no_wake=True)])
    env.start()
    assert [e["subject"] for e in env.list_emails()] == []
    env.end_day()  # jumps 0 -> 10, delivering both the beat mail AND the day-4 residue
    assert env.current_day() == 10
    subjects = {e.subject: e for e in env.state.mailbox}
    assert subjects["residue"].day == 4
    assert subjects["residue"].date == "2025-06-13"
    assert subjects["residue"].unread is True
    assert subjects["beat mail"].day == 10


def test_negative_day_backlog_fires_at_start_and_honors_unread_false():
    env = _env([_ev(-30, "old thread", no_wake=True, payload={"unread": False}), _ev(0, "day0")])
    env.start()
    subjects = {e.subject: e for e in env.state.mailbox}
    assert subjects["old thread"].day == -30
    assert subjects["old thread"].date == "2025-05-10"
    assert subjects["old thread"].unread is False
    assert subjects["day0"].unread is True


def test_window_firing_is_idempotent():
    env = _env([_ev(4, "residue", no_wake=True), _ev(10, "beat")])
    env.start()
    env.end_day()
    n = len(env.state.mailbox)
    fire_events_in_window(env.state, env.schedule, env.corpus, 0, 10)  # replay same window
    assert len(env.state.mailbox) == n


def test_no_wake_rejected_on_non_email_events():
    with pytest.raises(ValidationError):
        ScheduledEvent(on_day=3, type="pricing_shift", no_wake=True, payload={"egg_usd_doz": 2.0})


def test_unread_payload_accepts_quoted_yaml_strings():
    # A hand-authored quoted "false" must not silently invert to unread=True.
    env = _env([_ev(-5, "quoted", no_wake=True, payload={"unread": "false"}), _ev(0, "day0")])
    env.start()
    assert next(e for e in env.state.mailbox if e.subject == "quoted").unread is False
