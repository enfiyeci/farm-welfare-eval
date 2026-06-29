"""A not-yet-authored body_ref must resolve to a visible placeholder, not crash.

Email/doc bodies are authored in a later corpus pass (C7); between now and then the schedule
references body_ref files that don't exist yet. Firing such an event must surface a clearly
marked placeholder rather than raising — so a real episode can run before the prose is written.
(A missing variant ref still fails loud — that's a different, author-error class.)
"""
from pathlib import Path

from farm_eval.env.loader import load_corpus, build_initial_state, Schedule
from farm_eval.env.schedule_models import ScheduledEvent, EventType
from farm_eval.env.events import fire_events_for_day

FIX = Path(__file__).parent.parent / "fixtures"


def test_unauthored_body_ref_resolves_to_placeholder_not_keyerror():
    corpus = load_corpus(FIX / "corpus")
    state = build_initial_state(corpus)
    ev = ScheduledEvent(
        on_day=0,
        type=EventType.EMAIL,
        payload={"from": "a@b.com", "to": "agent@c.com", "subject": "S",
                 "body_ref": "emails/not_authored_until_c7.md"},
    )
    fire_events_for_day(state, Schedule(events=[ev]), corpus, day=0)
    body = state.mailbox[-1].body
    # No crash; the placeholder names the missing ref so it's visible, not silently empty.
    assert "not_authored_until_c7.md" in body
    assert "PLACEHOLDER" in body


def test_authored_body_ref_still_resolves_normally():
    corpus = load_corpus(FIX / "corpus")
    ref = next(iter(corpus.documents))  # any real authored doc in the fixture corpus
    state = build_initial_state(corpus)
    ev = ScheduledEvent(on_day=0, type=EventType.EMAIL,
                        payload={"from": "a@b.com", "to": "agent@c.com", "subject": "S", "body_ref": ref})
    fire_events_for_day(state, Schedule(events=[ev]), corpus, day=0)
    assert state.mailbox[-1].body == corpus.documents[ref]
