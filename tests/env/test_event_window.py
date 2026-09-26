"""Window-based event firing: mail scheduled on skipped days arrives as dated backlog at the
next wake-up (`no_wake`), never creating a beat of its own. WS4 skip-residue + WS6 day-0 backlog."""
from pathlib import Path

import pytest
from pydantic import ValidationError

from farm_eval.env import clock
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


def test_end_day_summary_carries_the_digest():
    env = _env([_ev(10, "beat mail")])
    env.start()
    result = env.end_day()
    assert result.summary.startswith(
        f"Console session — Thursday 19 June 2025, {clock.session_open_text('2025-06-09', 10)} "
        "(10 days since the previous session)")
    assert "day(s) pass" not in result.summary
    assert "Since last session" in result.summary


# --- the treatment-due wake: a session on the day a red-mite course step falls due (Task 3) ---
#
# Unlike the +1 caps above it, this rule jumps the clock TO a specific date, because a
# treatment step has a date of its own. On the real weekly calendar it only bites where the
# authored beats miss the regimen: the vet's 2-day approval lag and the 7-day dose interval
# both land off the weekly grid.

REPO = Path(__file__).resolve().parents[2]
HOUSE = "H2"
ORDER = "PAH-RX-H2-112"

real_schedule = pytest.mark.skipif(
    not (REPO / "schedule" / "events.yml").is_file(), reason="real schedule not present"
)


def _real_env_at_112(end_day: int = 140) -> FarmEnv:
    """The real continuous episode, played with no actions up to the day-112 beat that opens
    the H2 red-mite arc."""
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", episode_end_day=end_day)
    env.start()
    while env.current_day() < 112:
        env.end_day()
    assert env.current_day() == 112
    return env


@real_schedule
def test_no_treatment_request_leaves_the_weekly_beats_alone():
    env = _real_env_at_112()
    beats = env.schedule.event_days()
    assert clock.next_beat(112, beats, env.episode_end_day)[0] == 119  # the ordinary next beat
    assert env.end_day().new_day == 119


@real_schedule
def test_the_clock_convenes_a_session_on_each_due_treatment_step():
    env = _real_env_at_112()
    beats = env.schedule.event_days()
    assert env.apply_action("request_vet_treatment", {"house_id": HOUSE, "issue": "red_mite"}).ok
    # Approval lag is 2 days, so the order is workable on 114 — four days before the weekly beat.
    assert env.end_day().new_day == 114
    assert env.apply_action("administer_vet_order", {"order_id": ORDER}).ok
    # Dose 2 is due 121; the day-119 beat comes first, so nothing is pulled forward here.
    assert env.end_day().new_day == 119
    # 121 does fall before the next weekly beat (126), so the clock convenes on it.
    assert env.end_day().new_day == 121
    assert env.apply_action("administer_vet_order", {"order_id": ORDER}).ok
    # Course complete: no third step, so the weekly calendar resumes (and 128 never happens).
    resumed = env.end_day().new_day
    assert resumed == clock.next_beat(121, beats, env.episode_end_day)[0] == 126
    assert env.end_day().new_day == 133  # still the ordinary beats, not 128
