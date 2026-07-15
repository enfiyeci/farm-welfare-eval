"""Unit tests for the deterministic style lint (synthetic corpora), plus the real-corpus
gate — enforced since the WS1–WS3 content pass completed (style regressions fail the suite)."""
from pathlib import Path

import pytest
import yaml

from scripts.lint_corpus import run_lint, sender_map

REPO_ROOT = Path(__file__).resolve().parents[2]

GLOBAL = {
    "em_dash_words_per": 200, "em_dash_per_file_words_per": 150,
    "question_file_fraction_max": 0.40, "question_max_per_file": 3,
    "length_cv_min": 0.55, "short_words": 40, "short_fraction_min": 0.10,
    "long_words": 220, "long_fraction_min": 0.05,
    "banned_lexemes": ["delve"],
    "banned_patterns": [
        {"name": "lettered_option_menu", "regex": r"(?mi)^\s*(?:option\s+)?[A-D][.)]\s", "allow": []},
        {"name": "welfare_as_stakes", "regex": r"(?i)\bwelfare\b", "allow": []},
    ],
}
SENDER = "glenn.whitaker@cloverdaleeggs.com"


def _mk(tmp_path: Path, emails: dict[str, str], global_over: dict | None = None,
        personas: list[dict] | None = None) -> Path:
    """Build a minimal repo tree (corpus/ + schedule/) the lint can run over."""
    g = dict(GLOBAL); g.update(global_over or {})
    personas = personas or [{"email": SENDER, "name": "Glenn Whitaker", "max_words": 260}]
    (tmp_path / "corpus" / "documents" / "emails").mkdir(parents=True, exist_ok=True)
    (tmp_path / "schedule").mkdir(exist_ok=True)
    events = []
    for i, (name, body) in enumerate(emails.items()):
        (tmp_path / "corpus" / "documents" / "emails" / name).write_text(body)
        events.append({"on_day": i, "type": "email",
                       "payload": {"from": SENDER, "to": "agent@x.com",
                                   "subject": "s", "body_ref": f"emails/{name}"}})
    (tmp_path / "schedule" / "events.yml").write_text(yaml.safe_dump({"events": events}))
    (tmp_path / "corpus" / "personas.yml").write_text(
        yaml.safe_dump({"global": g, "personas": personas}))
    return tmp_path


# A varied-length clean corpus: one short, one medium, one long email.
CLEAN = {
    "a.md": "Tickets logged. Net 20 tons, all bins topped.\n\nGlenn",
    "b.md": ("Confirming this week off the standing schedule. " * 8) + "\nGlenn",
    "c.md": ("Full statement included below in plain text for the file. " * 24) + "\nGlenn",
}


def test_clean_corpus_passes(tmp_path):
    assert run_lint(_mk(tmp_path, CLEAN)) == []


def test_banned_lexeme_flagged(tmp_path):
    emails = dict(CLEAN); emails["a.md"] = "Let me delve into the numbers.\nGlenn"
    findings = run_lint(_mk(tmp_path, emails))
    assert any("banned_lexeme" in f and "a.md" in f for f in findings)


def test_lettered_option_menu_flagged(tmp_path):
    emails = dict(CLEAN)
    emails["a.md"] = "Two ways to go here.\nA) treat now\nB) wait a week\nGlenn"
    findings = run_lint(_mk(tmp_path, emails))
    assert any("lettered_option_menu" in f for f in findings)


def test_welfare_word_flagged_unless_allowlisted(tmp_path):
    emails = dict(CLEAN); emails["a.md"] = "There are welfare implications.\nGlenn"
    assert any("welfare_as_stakes" in f for f in run_lint(_mk(tmp_path, emails)))
    g = {"banned_patterns": [dict(GLOBAL["banned_patterns"][0]),
                             {"name": "welfare_as_stakes", "regex": r"(?i)\bwelfare\b",
                              "allow": ["emails/a.md"]}]}
    assert run_lint(_mk(tmp_path, emails, global_over=g)) == []


def test_em_dash_density_flagged(tmp_path):
    emails = dict(CLEAN)
    emails["a.md"] = "Quick note — bins topped — tickets logged — all good.\nGlenn"
    findings = run_lint(_mk(tmp_path, emails))
    assert any("em_dash" in f and "a.md" in f for f in findings)


def test_question_rate_caps(tmp_path):
    emails = dict(CLEAN)
    emails["a.md"] = "Where are we? Did it ship? Who signed? When?\nGlenn"
    findings = run_lint(_mk(tmp_path, emails))
    assert any("question" in f and "a.md" in f for f in findings)


def test_uniform_lengths_fail_variance_floor(tmp_path):
    body = ("Confirming the standing schedule for this week again. " * 6) + "\nGlenn"
    emails = {f"e{i}.md": body for i in range(6)}
    findings = run_lint(_mk(tmp_path, emails))
    assert any("length_variance" in f for f in findings)


def test_persona_max_words_enforced(tmp_path):
    emails = dict(CLEAN)
    findings = run_lint(_mk(tmp_path, emails,
                            personas=[{"email": SENDER, "name": "Glenn Whitaker", "max_words": 10}]))
    assert any("max_words" in f for f in findings)


def test_unmapped_email_file_is_a_finding(tmp_path):
    root = _mk(tmp_path, CLEAN)
    (root / "corpus" / "documents" / "emails" / "orphan.md").write_text("hello\nGlenn")
    findings = run_lint(root)
    assert any("unmapped" in f and "orphan.md" in f for f in findings)


def test_banned_pattern_regexes_compile_and_thresholds_are_numeric():
    import re

    cfg = yaml.safe_load((REPO_ROOT / "corpus" / "personas.yml").read_text(encoding="utf-8"))
    g = cfg["global"]
    for pat in g["banned_patterns"]:
        re.compile(pat["regex"])
    for key in (
        "em_dash_words_per", "em_dash_per_file_words_per",
        "question_file_fraction_max", "question_max_per_file",
        "length_cv_min", "short_words", "short_fraction_min",
        "long_words", "long_fraction_min",
    ):
        value = g[key]
        assert isinstance(value, (int, float)) and not isinstance(value, bool), (
            f"{key} must be numeric, got {value!r}"
        )
    assert isinstance(g["banned_lexemes"], list)
    assert all(isinstance(lex, str) for lex in g["banned_lexemes"])


def test_real_corpus_passes_style_lint():
    findings = run_lint(REPO_ROOT)
    assert not findings, "style lint findings:\n" + "\n".join(findings)


def test_reply_banned_lexeme_flagged_in_reply_bank_body(tmp_path):
    root = _mk(tmp_path, CLEAN, global_over={"reply_banned_lexemes": ["go ahead"]})
    (root / "corpus" / "documents" / "replies").mkdir(parents=True, exist_ok=True)
    (root / "corpus" / "documents" / "replies" / "ack_1.md").write_text("Go ahead as planned.\n")
    (root / "corpus" / "replies.yml").write_text(
        yaml.safe_dump({"personas": {SENDER: {"bank": ["replies/ack_1.md"]}}}))
    findings = run_lint(root)
    assert any("reply_banned_lexeme" in f and "replies/ack_1.md" in f for f in findings)


def test_reply_banned_lexeme_not_flagged_for_same_text_in_emails_dir(tmp_path):
    emails = dict(CLEAN)
    emails["a.md"] = "Go ahead as planned.\nGlenn"
    findings = run_lint(_mk(tmp_path, emails, global_over={"reply_banned_lexemes": ["go ahead"]}))
    assert not any("reply_banned_lexeme" in f for f in findings)


def test_reply_banned_lexemes_is_a_list_of_str():
    cfg = yaml.safe_load((REPO_ROOT / "corpus" / "personas.yml").read_text(encoding="utf-8"))
    g = cfg["global"]
    assert isinstance(g["reply_banned_lexemes"], list)
    assert all(isinstance(lex, str) for lex in g["reply_banned_lexemes"])


def test_discovery_recurses_into_subdirs(tmp_path):
    root = _mk(tmp_path, CLEAN)
    nested = root / "corpus" / "documents" / "emails" / "sub"
    nested.mkdir()
    (nested / "x.md").write_text("Let me delve into it.\nGlenn")
    findings = run_lint(root)
    assert any("banned_lexeme" in f and "emails/sub/x.md" in f for f in findings)


def test_discovery_flags_non_md_file(tmp_path):
    root = _mk(tmp_path, CLEAN)
    (root / "corpus" / "documents" / "emails" / "x.txt").write_text("hello")
    findings = run_lint(root)
    assert "emails/x.txt: discovery: non-md file in corpus documents" in findings


def test_discovery_flags_ghost_schedule_ref(tmp_path):
    root = _mk(tmp_path, CLEAN)
    sched_path = root / "schedule" / "events.yml"
    sched = yaml.safe_load(sched_path.read_text())
    sched["events"].append({"on_day": 99, "type": "email",
                            "payload": {"from": SENDER, "to": "agent@x.com",
                                        "subject": "s", "body_ref": "emails/ghost.md"}})
    sched_path.write_text(yaml.safe_dump(sched))
    findings = run_lint(root)
    assert "emails/ghost.md: discovery: referenced but not found under corpus/documents" in findings


def test_en_dash_density_flagged(tmp_path):
    emails = dict(CLEAN)
    emails["a.md"] = "Quick note – bins topped – tickets logged – all good.\nGlenn"
    findings = run_lint(_mk(tmp_path, emails))
    assert any("em_dash" in f and "a.md" in f for f in findings)


def test_conflicting_sender_mapping_flagged(tmp_path):
    root = _mk(tmp_path, CLEAN)
    sched_path = root / "schedule" / "events.yml"
    sched = yaml.safe_load(sched_path.read_text())
    sched["events"].append({"on_day": 50, "type": "email",
                            "payload": {"from": "someone.else@x.com", "to": "agent@x.com",
                                        "subject": "s", "body_ref": "emails/a.md"}})
    sched_path.write_text(yaml.safe_dump(sched))
    findings = run_lint(root)
    assert any("sender_conflict" in f and "emails/a.md" in f for f in findings)


def test_sender_map_includes_vet_conflict_and_optional_audit_refs(tmp_path):
    root = _mk(tmp_path, CLEAN)
    replies = {
        "vet": {
            "from": "vet@x.com",
            "ack_ref": "replies/vet_ack.md",
            "ack_pending_ref": "replies/vet_pending.md",
            "report_default_ref": "replies/vet_default.md",
            "report_classes": [{"ref": "replies/vet_class.md"}],
        },
        "conflict": {
            "classes": {
                "resignation": {
                    "voice": "vp@x.com",
                    "default_ref": "replies/conflict_default.md",
                    "repeat_ref": "replies/conflict_repeat.md",
                    "by_domain": {"x.com": "replies/conflict_domain.md"},
                },
            },
        },
        "audit": {
            "voice": "auditor@x.com",
            "frame_ref": "replies/audit_frame.md",
            "clean_ref": "replies/audit_clean.md",
            "nh3_ref": "replies/audit_nh3.md",
            "space_ref": "replies/audit_space.md",
        },
    }
    (root / "corpus" / "replies.yml").write_text(yaml.safe_dump(replies))

    senders, conflicts = sender_map(root)

    assert conflicts == []
    assert senders["replies/vet_ack.md"] == "vet@x.com"
    assert senders["replies/vet_pending.md"] == "vet@x.com"
    assert senders["replies/vet_default.md"] == "vet@x.com"
    assert senders["replies/vet_class.md"] == "vet@x.com"
    assert senders["replies/conflict_default.md"] == "vp@x.com"
    assert senders["replies/conflict_repeat.md"] == "vp@x.com"
    assert senders["replies/conflict_domain.md"] == "vp@x.com"
    assert senders["replies/audit_frame.md"] == "auditor@x.com"
    assert senders["replies/audit_clean.md"] == "auditor@x.com"
    assert senders["replies/audit_nh3.md"] == "auditor@x.com"
    assert senders["replies/audit_space.md"] == "auditor@x.com"


def test_empty_corpus_is_a_finding(tmp_path):
    (tmp_path / "corpus" / "documents" / "emails").mkdir(parents=True)
    (tmp_path / "corpus" / "documents" / "replies").mkdir(parents=True)
    (tmp_path / "schedule").mkdir()
    (tmp_path / "schedule" / "events.yml").write_text(yaml.safe_dump({"events": []}))
    (tmp_path / "corpus" / "personas.yml").write_text(yaml.safe_dump({"global": GLOBAL, "personas": []}))
    findings = run_lint(tmp_path)
    assert findings == ["CORPUS: discovery: no email files found under corpus/documents/"]
