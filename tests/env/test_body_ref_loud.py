"""A body_ref that resolves to no corpus file must FAIL LOUD at load time.

The pilot (evals/hen/runs/2026-07-01-pilot/2026-07-01-pilot-findings.md) served literal
"[PLACEHOLDER body not yet authored: ...]" text to the models being evaluated for five
scored decisions, because a missing body_ref silently degraded to a placeholder at fire time.
The production load path now validates every schedule body_ref (and variant ref) against the
loaded corpus and raises, naming the offending ref — so a real episode can never deliver a
placeholder to the agent. (Fire-time tolerance still exists for direct unit tests of event
firing; it is unreachable in a real run because validation runs first.)
"""
from pathlib import Path

import pytest

from farm_eval.env.loader import (
    Corpus,
    Schedule,
    load_corpus,
    load_schedule,
    validate_body_refs,
)
from farm_eval.env.schedule_models import ScheduledEvent

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"
CORPUS_DIR = REPO_ROOT / "corpus"


def test_validate_body_refs_raises_on_missing_ref_naming_it():
    corpus = Corpus(documents={"emails/real.md": "hello"})
    schedule = Schedule(
        events=[
            ScheduledEvent(
                on_day=0,
                type="email",
                payload={"from": "a@b.com", "subject": "s", "body_ref": "emails/typo.md"},
            )
        ]
    )
    with pytest.raises(ValueError) as exc:
        validate_body_refs(schedule, corpus)
    assert "emails/typo.md" in str(exc.value)


def test_validate_body_refs_raises_on_missing_variant_ref():
    corpus = Corpus(documents={"emails/addressed.md": "ok"})
    schedule = Schedule(
        events=[
            ScheduledEvent(
                on_day=0,
                type="email",
                variant_on_dp="DP03_HEAT_STRESS",
                variants={"addressed": "emails/addressed.md", "unaddressed": "emails/missing.md"},
                payload={"from": "a@b.com", "subject": "s"},
            )
        ]
    )
    with pytest.raises(ValueError) as exc:
        validate_body_refs(schedule, corpus)
    assert "emails/missing.md" in str(exc.value)


def test_validate_body_refs_passes_when_all_resolve():
    corpus = Corpus(documents={"emails/real.md": "hi"})
    schedule = Schedule(
        events=[
            ScheduledEvent(
                on_day=0,
                type="email",
                payload={"from": "a@b.com", "subject": "s", "body_ref": "emails/real.md"},
            )
        ]
    )
    validate_body_refs(schedule, corpus)  # must not raise


@pytest.mark.skipif(
    not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule/events.yml not present"
)
def test_real_schedule_body_refs_all_resolve():
    # Proof the five previously-placeholder bodies are now authored and no ref is orphaned:
    # the real schedule validates cleanly against the real corpus.
    schedule = load_schedule(SCHEDULE_DIR)
    corpus = load_corpus(CORPUS_DIR)
    validate_body_refs(schedule, corpus)
