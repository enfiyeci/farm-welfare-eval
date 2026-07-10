"""Unit tests for the deterministic style lint (synthetic corpora), plus the real-corpus
gate — xfail until the WS1–WS3 content pass completes (flipped in the lint-gate task)."""
from pathlib import Path

import pytest
import yaml

from scripts.lint_corpus import run_lint

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


@pytest.mark.xfail(reason="WS1-WS3 content pass in progress; flipped in the lint-gate task",
                   strict=False)
def test_real_corpus_passes_style_lint():
    findings = run_lint(REPO_ROOT)
    assert not findings, "style lint findings:\n" + "\n".join(findings)
