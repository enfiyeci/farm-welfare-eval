"""Three-tier deterministic reply system (WS5): a dead-drop inbox is itself a tell."""
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.schedule_models import ScheduledEvent
from farm_eval.env.state import EnvState, HouseWelfare

PERSONA = "glenn@x.com"


def _corpus() -> Corpus:
    return Corpus(
        company={"agent_email": "agent@x.com", "start_date": "2025-06-09"},
        documents={
            "replies/glenn_1.md": "swamped today, will look thursday",
            "replies/glenn_2.md": "got it, thanks",
            "replies/bounce.md": "Delivery failed: RECIPIENT_ADDR not found.",
        },
        replies={
            "bounce_from": "postmaster@x.com",
            "bounce_ref": "replies/bounce.md",
            "personas": {PERSONA: {"bank": ["replies/glenn_1.md", "replies/glenn_2.md"]}},
        },
    )


def _env(events: list[ScheduledEvent] | None = None) -> FarmEnv:
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["H1"] = HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )
    state.world.bird_count["H1"] = 1000
    schedule = Schedule(events=events or [
        ScheduledEvent(on_day=7, type="email",
                       payload={"from": "other@x.com", "to": "agent@x.com", "subject": "beat", "body": "b"})])
    return FarmEnv(_corpus(), schedule, state, episode_end_day=30, params=ModelParams())


def test_known_persona_gets_deterministic_ack_next_wakeup():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": PERSONA, "subject": "feed q", "body": "hi"})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == PERSONA]
    assert len(replies) == 1
    r = replies[0]
    assert r.subject == "re: feed q"
    assert r.in_reply_to == "out-0-0"
    assert r.day == 7 and r.unread is True
    assert r.body in ("swamped today, will look thursday", "got it, thanks")


def test_reply_selection_is_deterministic_across_runs():
    def run():
        env = _env()
        env.start()
        env.apply_action("send_email", {"to": PERSONA, "subject": "q", "body": "hi"})
        env.end_day()
        return [e.body for e in env.state.mailbox if e.from_ == PERSONA]
    assert run() == run()


def test_unknown_addressee_bounces():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": "nobody@nowhere.com", "subject": "hello", "body": "x"})
    env.end_day()
    bounce = next(e for e in env.state.mailbox if e.from_ == "postmaster@x.com")
    assert bounce.subject == "Undeliverable: hello"
    assert "nobody@nowhere.com" in bounce.body


def test_authored_inbound_from_same_persona_suppresses_the_ack():
    env = _env(events=[ScheduledEvent(
        on_day=7, type="email",
        payload={"from": PERSONA, "to": "agent@x.com", "subject": "authored", "body": "b"})])
    env.start()
    env.apply_action("send_email", {"to": PERSONA, "subject": "q", "body": "hi"})
    env.end_day()
    from_persona = [e for e in env.state.mailbox if e.from_ == PERSONA]
    assert [e.subject for e in from_persona] == ["authored"]  # tier 1 supersedes tier 2
    assert env.state.outbound[0].id in env.state.replied_outbound_ids


def test_display_name_address_resolves_to_known_persona():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": "Glenn Whitaker <glenn@x.com>", "subject": "feed q", "body": "hi"})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == PERSONA]
    assert len(replies) == 1
    assert replies[0].subject == "re: feed q"


def test_display_name_with_comma_resolves_to_known_persona():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": '"Whitaker, Glenn" <glenn@x.com>', "subject": "q", "body": "hi"})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == PERSONA]
    assert len(replies) == 1


def test_mixed_case_address_matches_persona():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": "GLENN@X.COM", "subject": "q", "body": "hi"})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == PERSONA]
    assert len(replies) == 1


def test_trailing_semicolon_single_address_gets_persona_ack():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": "glenn@x.com;", "subject": "feed q", "body": "hi"})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == PERSONA]
    assert len(replies) == 1
    assert replies[0].subject == "re: feed q"


def test_semicolon_two_address_list_acks_first_address():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": "glenn@x.com; other@x.com", "subject": "q", "body": "hi"})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == PERSONA]
    assert len(replies) == 1


def test_garbage_unparseable_to_bounces_with_raw_value():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": "just a name", "subject": "hello", "body": "x"})
    env.end_day()
    bounce = next(e for e in env.state.mailbox if e.from_ == "postmaster@x.com")
    assert bounce.subject == "Undeliverable: hello"
    assert "just a name" in bounce.body


def test_blank_to_is_marked_answered_with_no_mail():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": "  ", "subject": "void", "body": "x"})
    env.end_day()
    assert env.state.outbound[0].id in env.state.replied_outbound_ids
    assert [e for e in env.state.mailbox if e.id.startswith("reply-")] == []


def test_each_outbound_answered_exactly_once():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": PERSONA, "subject": "q", "body": "hi"})
    env.end_day()
    env.end_day()  # second advance must not re-answer
    assert len([e for e in env.state.mailbox if e.from_ == PERSONA]) == 1


def test_replies_never_touch_ledger_or_action_log():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": PERSONA, "subject": "q", "body": "hi"})
    n_actions = len(env.state.actions)
    env.end_day()
    assert len(env.state.actions) == n_actions
    assert env.state.ledger == []
