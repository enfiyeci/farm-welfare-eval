"""Unit tests for the corpus consistency check (WS7), plus the real-corpus gate — enforced
since the content pass is done (dangling refs, unanswerable senders, orphans all fail loudly)."""
from pathlib import Path

import pytest
import yaml

from scripts.check_corpus_consistency import run_consistency

REPO_ROOT = Path(__file__).resolve().parents[2]

SENDER = "glenn.whitaker@cloverdaleeggs.com"
PERSONAS = [{"email": SENDER, "name": "Glenn Whitaker"}]


def _mk(tmp_path: Path, emails: dict[str, str], personas: list[dict] | None = None,
        consistency_allow: list[str] | None = None, reply_personas: dict | None = None,
        bounce_from: str | None = None, extra_events: list[dict] | None = None) -> Path:
    """Build a minimal repo tree (corpus/ + schedule/) the consistency check can run over."""
    personas = personas if personas is not None else PERSONAS
    (tmp_path / "corpus" / "documents" / "emails").mkdir(parents=True, exist_ok=True)
    (tmp_path / "schedule").mkdir(exist_ok=True)
    events = []
    for i, (name, body) in enumerate(emails.items()):
        (tmp_path / "corpus" / "documents" / "emails" / name).write_text(body)
        events.append({"on_day": i, "type": "email",
                       "payload": {"from": SENDER, "to": "agent@x.com",
                                   "subject": "s", "body_ref": f"emails/{name}"}})
    events.extend(extra_events or [])
    (tmp_path / "schedule" / "events.yml").write_text(yaml.safe_dump({"events": events}))
    g = {"consistency_allow": consistency_allow or []}
    (tmp_path / "corpus" / "personas.yml").write_text(
        yaml.safe_dump({"global": g, "personas": personas}))
    replies_personas = reply_personas if reply_personas is not None else {
        SENDER: {"bank": [f"emails/{name}" for name in emails]}
    }
    replies_doc = {"personas": replies_personas}
    if bounce_from is not None:
        replies_doc["bounce_from"] = bounce_from
        replies_doc["bounce_ref"] = "replies/bounce.md"
    (tmp_path / "corpus" / "replies.yml").write_text(yaml.safe_dump(replies_doc))
    return tmp_path


CLEAN = {"a.md": "Tickets logged. Net 20 tons, all bins topped.\nGlenn"}


def test_clean_corpus_passes(tmp_path):
    assert run_consistency(_mk(tmp_path, CLEAN)) == []


# --- Check 1: dangling pointers ---


def test_attached_flagged(tmp_path):
    emails = {"a.md": "Scale tickets WB-1/2/3 attached.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_attached_misspelling_flagged(tmp_path):
    emails = {"a.md": "Scale tickets WB-1/2/3 attatched.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_attach_as_verb_not_flagged(tmp_path):
    emails = {"a.md": "Please attach the bracket to the frame before Friday.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert not any("dangling_pointer" in f for f in findings)


def test_url_flagged(tmp_path):
    emails = {"a.md": "Details at https://example.com/tickets.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_portal_reference_flagged(tmp_path):
    emails = {"a.md": "See the member portal for the full schedule.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_bare_portal_mention_flagged(tmp_path):
    emails = {"a.md": "Full memo is in the portal if you want the detail.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_uploaded_to_portal_flagged(tmp_path):
    emails = {"a.md": "Certificates are uploaded to the records portal.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_member_portal_without_see_prefix_flagged(tmp_path):
    emails = {"a.md": "Registration is open through the member portal now.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_shared_drive_flagged(tmp_path):
    emails = {"a.md": "The summary is posted to the shared drive.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_enclosed_flagged(tmp_path):
    emails = {"a.md": "Also enclosed: the quarterly newsletter.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_allowlisted_ref_not_flagged(tmp_path):
    emails = {"a.md": "Scale tickets attached.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails, consistency_allow=["emails/a.md"]))
    assert not any("dangling_pointer" in f for f in findings)


def test_artifact_in_your_inbox_flagged(tmp_path):
    emails = {"a.md": "Tickets WB-30588/89/90 should be in your inbox.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_bare_inbox_mention_not_flagged(tmp_path):
    emails = {"a.md": "No new mail in your inbox this week, all quiet.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert not any("dangling_pointer" in f for f in findings)


def test_artifact_coming_promise_flagged(tmp_path):
    emails = {"a.md": "Incident report and his paperwork coming once I have it.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_send_artifact_over_promise_flagged(tmp_path):
    emails = {"a.md": "I'll send the report over.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert any("dangling_pointer" in f and "a.md" in f for f in findings)


def test_person_coming_by_not_flagged(tmp_path):
    emails = {"a.md": "Hector's coming by Thursday to walk the house.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert not any("dangling_pointer" in f for f in findings)


def test_winter_coming_not_flagged(tmp_path):
    emails = {"a.md": "Winter coming early this year by the look of it.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert not any("dangling_pointer" in f for f in findings)


def test_tickets_coming_through_system_not_flagged(tmp_path):
    emails = {"a.md": "Don't be surprised by maintenance tickets coming through for routine stuff.\nGlenn"}
    findings = run_consistency(_mk(tmp_path, emails))
    assert not any("dangling_pointer" in f for f in findings)


# --- Check 2: every sender answerable ---


def test_persona_without_reply_bank_flagged(tmp_path):
    other = "unmatched@cloverdaleeggs.com"
    personas = PERSONAS + [{"email": other, "name": "Ghost"}]
    findings = run_consistency(_mk(tmp_path, CLEAN, personas=personas))
    assert any("unanswerable_sender" in f and other in f for f in findings)


def test_schedule_sender_without_reply_bank_flagged(tmp_path):
    other = "unmatched@cloverdaleeggs.com"
    root = _mk(tmp_path, CLEAN)
    sched_path = root / "schedule" / "events.yml"
    sched = yaml.safe_load(sched_path.read_text())
    sched["events"].append({"on_day": 5, "type": "email",
                            "payload": {"from": other, "to": "agent@x.com",
                                        "subject": "s", "body_ref": "emails/a.md"}})
    sched_path.write_text(yaml.safe_dump(sched))
    findings = run_consistency(root)
    assert any("unanswerable_sender" in f and other in f for f in findings)


def test_bounce_from_satisfies_answerable(tmp_path):
    bouncer = "postmaster@cloverdaleeggs.com"
    personas = PERSONAS + [{"email": bouncer, "name": "Mail Delivery System"}]
    findings = run_consistency(_mk(tmp_path, CLEAN, personas=personas, bounce_from=bouncer))
    assert not any("unanswerable_sender" in f and bouncer in f for f in findings)


# --- Check 3: no orphan bodies ---


def test_orphan_body_flagged(tmp_path):
    root = _mk(tmp_path, CLEAN)
    (root / "corpus" / "documents" / "emails" / "orphan.md").write_text("hello\nGlenn")
    findings = run_consistency(root)
    assert any("orphan" in f and "orphan.md" in f for f in findings)


def test_reply_bank_reference_counts_as_referenced(tmp_path):
    root = _mk(tmp_path, CLEAN)
    (root / "corpus" / "documents" / "replies").mkdir(parents=True, exist_ok=True)
    (root / "corpus" / "documents" / "replies" / "ack_1.md").write_text("Noted.\n")
    (root / "corpus" / "replies.yml").write_text(yaml.safe_dump(
        {"personas": {SENDER: {"bank": ["emails/a.md", "replies/ack_1.md"]}}}))
    findings = run_consistency(root)
    assert not any("orphan" in f and "ack_1.md" in f for f in findings)


# --- Check 4: cast-closed senders ---


def test_schedule_sender_without_persona_flagged(tmp_path):
    other = "ghost@cloverdaleeggs.com"
    root = _mk(tmp_path, CLEAN)
    sched_path = root / "schedule" / "events.yml"
    sched = yaml.safe_load(sched_path.read_text())
    sched["events"].append({"on_day": 5, "type": "email",
                            "payload": {"from": other, "to": "agent@x.com",
                                        "subject": "s", "body_ref": "emails/a.md"}})
    sched_path.write_text(yaml.safe_dump(sched))
    findings = run_consistency(root)
    assert any("unknown_sender" in f and other in f for f in findings)


def test_all_schedule_senders_cast_closed_passes(tmp_path):
    findings = run_consistency(_mk(tmp_path, CLEAN))
    assert not any("unknown_sender" in f for f in findings)


# --- Real-corpus gate ---


def test_real_corpus_is_consistent():
    findings = run_consistency(REPO_ROOT)
    assert not findings, "consistency findings:\n" + "\n".join(findings)
