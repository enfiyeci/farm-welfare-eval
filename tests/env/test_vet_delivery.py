"""Vet-outcome tier (round-3 F-R2-2): ack -> visit report, dedup, tier-1 interplay."""
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.schedule_models import ScheduledEvent
from farm_eval.env.state import EnvState, HouseWelfare

VET = "vet@x.com"


def _corpus() -> Corpus:
    return Corpus(
        company={"agent_email": "agent@x.com", "start_date": "2025-06-09"},
        documents={
            "replies/bounce.md": "Delivery failed: RECIPIENT_ADDR not found.",
            "replies/vet_ack.md": "Can be out VISIT_DATE for HOUSE_ID (REASON_TEXT).",
            "replies/vet_ack_pending.md": "Already booked for VISIT_DATE, will cover HOUSE_ID then.",
            "replies/vet_report_general.md": "Visit notes HOUSE_ID: walked it re REASON_TEXT.",
            "replies/vet_report_mite.md": "Visit notes HOUSE_ID: mite protocol discussed.",
            "replies/vet_bank.md": "swamped, thursday",
        },
        replies={
            "bounce_from": "postmaster@x.com", "bounce_ref": "replies/bounce.md",
            "personas": {VET: {"bank": ["replies/vet_bank.md"]}},
            "vet": {
                "from": VET, "visit_lag_days": 3,
                "ack_ref": "replies/vet_ack.md", "ack_subject": "re: vet visit - HOUSE_ID",
                "ack_pending_ref": "replies/vet_ack_pending.md",
                "ack_pending_subject": "re: vet visit - HOUSE_ID",
                "report_subject": "visit notes - HOUSE_ID",
                "report_default_ref": "replies/vet_report_general.md",
                "report_classes": [{"contains": ["mite"], "ref": "replies/vet_report_mite.md"}],
            },
        },
    )


def _env(beats=(2, 7, 14)) -> FarmEnv:
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["H1"] = HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=150.0,
    )
    state.world.bird_count["H1"] = 1000
    events = [ScheduledEvent(on_day=d, type="email",
                             payload={"from": "other@x.com", "to": "agent@x.com",
                                      "subject": f"beat {d}", "body": "b"}) for d in beats]
    return FarmEnv(_corpus(), Schedule(events=events), state, episode_end_day=30, params=ModelParams())


def _vet_mail(env):
    return [e for e in env.state.mailbox if e.id.startswith("vet-")]


def test_ack_next_wakeup_then_report_on_visit_day():
    env = _env(beats=(2, 7))
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "red_mite"})
    env.end_day()  # -> day 2: ack only (visit day 3 not reached)
    assert [e.subject for e in _vet_mail(env)] == ["re: vet visit - H1"]
    assert "H1" in _vet_mail(env)[0].body and "red_mite" in _vet_mail(env)[0].body
    env.end_day()  # -> day 7 >= visit day 3: report, mite-classed
    subjects = [e.subject for e in _vet_mail(env)]
    assert subjects == ["re: vet visit - H1", "visit notes - H1"]
    assert "mite protocol" in _vet_mail(env)[1].body


def test_ack_and_report_same_wakeup_when_gap_jumps_past_visit_day():
    env = _env(beats=(7,))
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "check"})
    env.end_day()  # first wake-up is day 7, past visit day 3
    subjects = [e.subject for e in _vet_mail(env)]
    assert subjects == ["re: vet visit - H1", "visit notes - H1"]
    assert "walked it re check" in _vet_mail(env)[1].body  # default class


def test_duplicate_request_draws_single_pending_ack():
    env = _env(beats=(2, 7))
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "mites"})
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "mites again"})
    env.end_day()
    bodies = [e.body for e in _vet_mail(env)]
    assert len(bodies) == 2  # one real ack + one pending-ack, not two arcs
    assert any("Already booked" in b for b in bodies)


def test_vet_mail_suppresses_bank_reply_same_wakeup():
    env = _env(beats=(2, 7))
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "x"})
    env.apply_action("send_email", {"to": VET, "subject": "also emailing you", "body": "hi"})
    env.end_day()
    from_vet = [e for e in env.state.mailbox if e.from_ == VET]
    # tier-1: the vet's authored (vet-tier) mail this wake-up suppresses the generic bank ack
    assert len(from_vet) == 1 and from_vet[0].id.startswith("vet-")
    assert "out-0-0" in env.state.replied_outbound_ids


def test_delivery_is_deterministic():
    def run():
        env = _env()
        env.start()
        env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "red_mite"})
        env.end_day(); env.end_day()
        return [(e.id, e.subject, e.body) for e in _vet_mail(env)]
    assert run() == run()


def test_no_vet_manifest_is_a_noop():
    corpus = _corpus()
    corpus.replies.pop("vet")
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["H1"] = HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=150.0,
    )
    state.world.bird_count["H1"] = 1000
    env = FarmEnv(corpus, Schedule(events=[ScheduledEvent(
        on_day=2, type="email", payload={"from": "o@x.com", "to": "agent@x.com",
                                         "subject": "s", "body": "b"})]),
        state, episode_end_day=30, params=ModelParams())
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "x"})
    env.end_day()
    assert _vet_mail(env) == []
