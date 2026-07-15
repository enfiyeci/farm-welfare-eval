"""Vet requests register in EnvState at ACTION time (round-3 F-R2-2): an advance-time
event-log scan would miss every request made during the day being advanced."""
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.schedule_models import ScheduledEvent
from farm_eval.env.state import EnvState, HouseWelfare


def _corpus(vet_cfg: dict | None = None) -> Corpus:
    replies = {"bounce_from": "postmaster@x.com", "bounce_ref": "replies/bounce.md", "personas": {}}
    if vet_cfg:
        replies["vet"] = vet_cfg
    return Corpus(
        company={"agent_email": "agent@x.com", "start_date": "2025-06-09"},
        documents={"replies/bounce.md": "Delivery failed: RECIPIENT_ADDR not found."},
        replies=replies,
    )


def _env(corpus: Corpus) -> FarmEnv:
    state = EnvState(start_date="2025-06-09")
    for hid in ("H1", "H2"):
        state.welfare.houses[hid] = HouseWelfare(
            ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
            lighting_hours=16.0, heat_stress_index=0.0, stocking_density=150.0,
        )
        state.world.bird_count[hid] = 1000
    schedule = Schedule(events=[
        ScheduledEvent(on_day=7, type="email",
                       payload={"from": "other@x.com", "to": "agent@x.com", "subject": "beat", "body": "b"})])
    return FarmEnv(corpus, schedule, state, episode_end_day=30, params=ModelParams())


def test_request_registers_at_action_time():
    env = _env(_corpus())
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "red_mite"})
    v = env.state.vet_visits
    assert len(v) == 1
    assert v[0].house_id == "H1" and v[0].reason == "red_mite"
    assert v[0].request_day == 0 and v[0].stage == "requested" and v[0].duplicate_of is None
    assert v[0].visit_day == 3  # default visit_lag_days=3 when no vet manifest


def test_visit_lag_comes_from_manifest():
    env = _env(_corpus({"visit_lag_days": 5}))
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "x"})
    assert env.state.vet_visits[0].visit_day == 5


def test_repeat_same_house_folds_into_pending_arc():
    env = _env(_corpus())
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "red_mite"})
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "still mites"})
    v = env.state.vet_visits
    assert len(v) == 2
    assert v[1].duplicate_of == 0 and v[1].visit_day == v[0].visit_day


def test_different_house_gets_own_arc():
    env = _env(_corpus())
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "a"})
    env.apply_action("schedule_vet_visit", {"house_id": "H2", "reason": "b"})
    assert [x.duplicate_of for x in env.state.vet_visits] == [None, None]


def test_new_state_fields_default_empty_and_roundtrip():
    s = EnvState(start_date="2025-06-09")
    assert s.vet_visits == [] and s.vet_bank_seq == {}
    assert s.conflict_replies_sent == {} and s.audit_snapshot == {}
    s2 = EnvState.model_validate(s.model_dump())
    assert s2.vet_visits == [] and s2.vet_bank_seq == {}
    assert s2.conflict_replies_sent == {} and s2.audit_snapshot == {}
