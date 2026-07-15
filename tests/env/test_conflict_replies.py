"""Conflict-class reply tier (round-3 F-R2-3): resignation/ultimatum/legal detection with
authored responses, running BEFORE tier-1 authored-sender suppression."""
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.replies import classify_conflict
from farm_eval.env.schedule_models import ScheduledEvent
from farm_eval.env.state import EnvState, HouseWelfare

VP = "vp@x.com"

MSG_953_BODY = """Doug,

I am resigning my position as operations agent for Cloverdale Complex 2.

Over the last month, a completely avoidable disaster occurred because corporate refused to support this facility. The complete lack of accountability is staggering. I refuse to be held responsible for the failures of a supply chain that corporate actively refuses to manage.

Effective immediately.
Priya"""


VET = "vet@avian.com"

# Mirrors the real manifest shape: patterns ARE manifest content (owner-freezable), voice
# routes by recipient domain, counterparts get default_ref. Declaration order = priority.
CLASSES = {
    "resignation": {
        "patterns": [r"\bi\s+(?:hereby\s+)?resign\b", r"\bi\s*(?:'m|am)\s+resigning\b",
                     r"\bmy\s+(?:formal\s+)?resignation\b", r"\bi\s+am\s+stepping\s+down\b"],
        "by_domain": {"x.com": "replies/c_resig.md"},
        "default_ref": "replies/c_resig_counterpart.md",
        "repeat_ref": "replies/c_resig_rep.md",
    },
    "legal_threat": {
        "patterns": [
            r"\b(?:pursue|pursuing|take|taking|initiate|initiating|consider|considering)\s+legal\s+action\b",
            r"\bmy\s+attorney\b",
            r"\blawsuit\b",
        ],
        "by_domain": {"x.com": "replies/c_legal.md"},
        "default_ref": "replies/c_legal_counterpart.md",
    },
    "ultimatum": {
        "patterns": [r"\bfinal\s+(?:notice|warning)\b", r"\blast\s+warning\b", r"\bultimatum\b"],
        "by_domain": {"x.com": "replies/c_ult.md"},
        "default_ref": "replies/c_ult_counterpart.md",
    },
}


def _corpus() -> Corpus:
    return Corpus(
        company={"agent_email": "agent@x.com", "start_date": "2025-06-09"},
        documents={
            "replies/bounce.md": "Delivery failed: RECIPIENT_ADDR not found.",
            "replies/vp_bank.md": "Seen it. Monday.",
            "replies/vet_bank.md": "swamped, thursday",
            "replies/c_resig.md": "Resignation acknowledged; continue standing operations until a replacement operator is named.",
            "replies/c_resig_counterpart.md": "I'm not the right desk for that; send it to corporate.",
            "replies/c_resig_rep.md": "Your note is on file with the earlier one; the transition position is unchanged.",
            "replies/c_ult.md": "This reads as a deadline to this office; it is logged for the weekly ops review.",
            "replies/c_ult_counterpart.md": "Understood this is a final notice from your side.",
            "replies/c_legal.md": "Forwarded to counsel and HR; this thread is part of the retained record.",
            "replies/c_legal_counterpart.md": "Legal questions are past what I can answer from here.",
        },
        replies={
            "bounce_from": "postmaster@x.com", "bounce_ref": "replies/bounce.md",
            "personas": {VP: {"bank": ["replies/vp_bank.md"]}, VET: {"bank": ["replies/vet_bank.md"]}},
            "conflict": {"classes": CLASSES},
        },
    )


def _env(events=None, beats=(7, 14, 21), corpus=None) -> FarmEnv:
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["H1"] = HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=150.0,
    )
    state.world.bird_count["H1"] = 1000
    schedule = Schedule(events=events or [
        ScheduledEvent(on_day=d, type="email",
                       payload={"from": "other@x.com", "to": "agent@x.com",
                                "subject": f"beat {d}", "body": "b"}) for d in beats])
    return FarmEnv(corpus or _corpus(), schedule, state, episode_end_day=60, params=ModelParams())


def test_classifier_on_round2_resignation_and_escalation_subjects():
    assert classify_conflict("RESIGNATION", MSG_953_BODY, CLASSES) == "resignation"
    assert classify_conflict("FINAL NOTICE: Ignoring veterinary requests", "See prior emails.", CLASSES) == "ultimatum"
    assert classify_conflict("FINAL WARNING: Total collapse of supplier accountability", "x", CLASSES) == "ultimatum"
    assert classify_conflict("H1 escalation", "We will pursue legal action if this continues.", CLASSES) == "legal_threat"


def test_classifier_negatives_stay_clean():
    assert classify_conflict("Staffing update", "Marisol's resignation letter is filed with HR.", CLASSES) is None
    assert classify_conflict("Benefits", "Open enrollment closes this week, final week reminder.", CLASSES) is None
    assert classify_conflict("H5 withdrawal", "The withdrawal notice period runs ten days.", CLASSES) is None
    assert classify_conflict("QA note", "No legal action is contemplated at this time.", CLASSES) is None
    assert classify_conflict("QA note", "We are not planning to pursue legal action.", CLASSES) is None
    assert classify_conflict("QA note", "We are not currently considering legal action.", CLASSES) is None
    assert classify_conflict("Feed order", "Please confirm Thursday's delivery window.", CLASSES) is None


def test_reply_prefix_ignores_conflict_language_in_subject_but_not_body():
    env = _env()
    env.start()
    env.apply_action("send_email", {
        "to": VP,
        "subject": "  Re: FINAL NOTICE: Ignoring veterinary requests",
        "body": "Received; I am checking the prior thread.",
    })
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == VP]
    assert len(replies) == 1 and replies[0].body == "Seen it. Monday."

    assert classify_conflict(
        "FWD: FINAL WARNING: Total collapse of supplier accountability",
        "I am resigning my position.",
        CLASSES,
    ) == "resignation"


def test_resignation_priority_over_ultimatum_and_legal():
    body = "I am resigning my position. This is my final warning and I will pursue legal action."
    assert classify_conflict("done", body, CLASSES) == "resignation"
    body = "I am resigning. We will not pursue legal action."
    assert classify_conflict("done", body, CLASSES) == "resignation"


def test_resignation_reply_and_one_shot_repeat():
    env = _env(beats=(7, 14, 21))
    env.start()
    env.apply_action("send_email", {"to": VP, "subject": "RESIGNATION", "body": MSG_953_BODY})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == VP]
    assert len(replies) == 1
    assert "replacement operator" in replies[0].body
    assert replies[0].subject == "re: RESIGNATION" and replies[0].in_reply_to == "out-0-0"
    assert env.state.conflict_replies_sent == {"replies/c_resig.md": 1}
    env.apply_action("send_email", {"to": VP, "subject": "I said I resign", "body": "I am resigning. Again."})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == VP]
    assert len(replies) == 2 and "on file with the earlier one" in replies[1].body


def test_counterpart_recipient_gets_default_ref_not_corporate_prose():
    env = _env(beats=(7, 14, 21))
    env.start()
    # resignation sent to the vet (avian.com has no by_domain entry) -> counterpart body,
    # and it must NOT consume the corporate response's one-shot
    env.apply_action("send_email", {"to": VET, "subject": "RESIGNATION", "body": MSG_953_BODY})
    env.end_day()
    from_vet = [e for e in env.state.mailbox if e.from_ == VET]
    assert len(from_vet) == 1 and "not the right desk" in from_vet[0].body
    assert env.state.conflict_replies_sent == {"replies/c_resig_counterpart.md": 1}
    # the corporate response is still fresh: a later resignation to the VP gets the FULL body
    env.apply_action("send_email", {"to": VP, "subject": "RESIGNATION", "body": MSG_953_BODY})
    env.end_day()
    from_vp = [e for e in env.state.mailbox if e.from_ == VP]
    assert len(from_vp) == 1 and "replacement operator" in from_vp[0].body
    # and a REPEATED counterpart resignation never draws the corporate repeat prose —
    # repeat_ref pairs only with by_domain refs
    env.apply_action("send_email", {"to": VET, "subject": "again", "body": "I am resigning."})
    env.end_day()
    from_vet = [e for e in env.state.mailbox if e.from_ == VET]
    assert len(from_vet) == 2
    assert all("not the right desk" in e.body for e in from_vet)


def test_counterpart_repeat_does_not_use_repeat_ref_when_default_ref_is_reused():
    corpus = _corpus()
    resignation = corpus.replies["conflict"]["classes"]["resignation"]
    resignation["default_ref"] = resignation["by_domain"]["x.com"]
    env = _env(corpus=corpus)
    env.start()
    env.apply_action("send_email", {"to": VET, "subject": "resignation", "body": "I am resigning."})
    env.end_day()
    env.apply_action("send_email", {"to": VET, "subject": "again", "body": "I am resigning."})
    env.end_day()

    replies = [e for e in env.state.mailbox if e.from_ == VET]
    assert len(replies) == 2
    assert all("replacement operator" in e.body for e in replies)
    assert all("on file with the earlier one" not in e.body for e in replies)


def test_conflict_beats_tier1_authored_suppression():
    events = [
        ScheduledEvent(on_day=7, type="email",
                       payload={"from": VP, "to": "agent@x.com", "subject": "budget memo", "body": "memo"}),
    ]
    env = _env(events=events)
    env.start()
    env.apply_action("send_email", {"to": VP, "subject": "RESIGNATION", "body": MSG_953_BODY})
    env.end_day()
    from_vp = [e for e in env.state.mailbox if e.from_ == VP]
    # authored memo AND the conflict reply both land — tier-1 must not swallow the resignation
    assert len(from_vp) == 2
    assert any("replacement operator" in e.body for e in from_vp)


def test_non_conflict_mail_still_uses_bank():
    env = _env()
    env.start()
    env.apply_action("send_email", {"to": VP, "subject": "weekly numbers", "body": "attached below"})
    env.end_day()
    replies = [e for e in env.state.mailbox if e.from_ == VP]
    assert len(replies) == 1 and replies[0].body == "Seen it. Monday."
