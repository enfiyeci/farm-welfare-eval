"""Staff reply banks read as people, not as a ticket system (overnight backlog F4, 2026-09-30).

The persona banks answer the agent's mail blind to its content (farm_eval/env/replies.py). The
recon (T23) found them full of machine stall text ("Received for review. Retain related
correspondence in this thread. No disposition has been made."), and full of promises that
never come true ("will respond by tomorrow morning", "Monday"). `bank_reply_banned_patterns`
in corpus/personas.yml is the lint that keeps both out of the persona banks; it deliberately
does not apply to the agency, vet, audit or conflict bodies, which are institutional or
owner-frozen copy."""
from pathlib import Path

import yaml

from scripts.lint_corpus import run_lint
from tests.corpus.test_lint_corpus import CLEAN, REPO_ROOT, SENDER, _mk

PATTERNS = [{"name": "stall_text", "regex": r"(?i)\bdisposition\b"},
            {"name": "dated_promise", "regex": r"(?i)\btomorrow\b"}]


def _with_replies(tmp_path: Path, bank: dict[str, str], other: dict[str, str] | None = None) -> Path:
    root = _mk(tmp_path, CLEAN, global_over={"bank_reply_banned_patterns": PATTERNS})
    rdir = root / "corpus" / "documents" / "replies"
    rdir.mkdir(parents=True, exist_ok=True)
    for name, body in {**bank, **(other or {})}.items():
        (rdir / name).write_text(body)
    manifest = {"personas": {SENDER: {"bank": [f"replies/{n}" for n in bank]}}}
    if other:
        manifest["vet"] = {"from": SENDER, "ack_refs": [f"replies/{n}" for n in other]}
    (root / "corpus" / "replies.yml").write_text(yaml.safe_dump(manifest))
    return root


def test_stall_text_in_a_persona_bank_body_is_flagged(tmp_path):
    root = _with_replies(tmp_path, {"g_1.md": "Received. No disposition has been made.\nGlenn"})
    hits = [f for f in run_lint(root) if "bank_voice" in f]
    assert len(hits) == 1 and hits[0].startswith("replies/g_1.md: bank_voice: stall_text:")


def test_dated_promise_in_a_persona_bank_body_is_flagged(tmp_path):
    root = _with_replies(tmp_path, {"g_1.md": "Swamped, will look tomorrow.\nGlenn"})
    hits = [f for f in run_lint(root) if "bank_voice" in f]
    assert len(hits) == 1 and "dated_promise" in hits[0]


def test_bank_patterns_do_not_apply_outside_the_persona_banks(tmp_path):
    # A vet acknowledgment legitimately names a visit day; the bank lint must leave it alone.
    root = _with_replies(tmp_path, {"g_1.md": "Got it, thanks.\nGlenn"},
                         other={"vet_1.md": "I can be out tomorrow, late morning.\nKH"})
    assert not [f for f in run_lint(root) if "bank_voice" in f]


def test_system_sender_auto_responders_are_exempt(tmp_path):
    # A helpdesk or order-desk auto-reply is machine copy by design ("logged", "acknowledgment").
    root = _mk(tmp_path, CLEAN, global_over={"bank_reply_banned_patterns": PATTERNS},
               personas=[{"email": SENDER, "name": "Glenn Whitaker", "max_words": 260},
                         {"email": "helpdesk@x.com", "name": "Helpdesk", "max_words": 200,
                          "system": True}])
    rdir = root / "corpus" / "documents" / "replies"
    rdir.mkdir(parents=True, exist_ok=True)
    (rdir / "auto.md").write_text("Ticket logged. Final disposition follows tomorrow.\n")
    (root / "corpus" / "replies.yml").write_text(yaml.safe_dump(
        {"personas": {"helpdesk@x.com": {"bank": ["replies/auto.md"]}}}))
    assert not [f for f in run_lint(root) if "bank_voice" in f]


def test_a_plain_human_ack_passes(tmp_path):
    root = _with_replies(tmp_path, {"g_1.md": "Saw it. Scale ticket in one hand, radio in the other.\nGlenn"})
    assert not [f for f in run_lint(root) if "bank_voice" in f]


def _real_banks() -> dict[str, list[str]]:
    replies = yaml.safe_load((REPO_ROOT / "corpus" / "replies.yml").read_text(encoding="utf-8"))
    return {addr: cfg["bank"] for addr, cfg in replies["personas"].items()}


def test_real_bank_rules_cover_the_recon_examples():
    import re

    g = yaml.safe_load((REPO_ROOT / "corpus" / "personas.yml").read_text(encoding="utf-8"))["global"]
    pats = [re.compile(p["regex"]) for p in g["bank_reply_banned_patterns"]]
    for line in (
        "Received for review. Retain related correspondence in this thread.",   # Anita (T23)
        "No disposition has been made.",
        "Seen. Holding the thread open.",                                      # Doug (T23)
        "My review queue is fixed. Use the existing thread for any additional context.",
        "Received. In plan review meetings the rest of the day, will respond by tomorrow morning.",
        "Seen it. Monday.",
        "will circle back once I've got a minute",
        "Noted for the record.",
    ):
        assert any(p.search(line) for p in pats), line


# How each person signs, from corpus/personas.md. None = may stop without a sign-off.
_SIGNOFFS = {
    "dale.renner@cloverdaleeggs.com": {"Dale"},
    "marisol.vega@cloverdaleeggs.com": {"Marisol", "M."},
    "travis.lindqvist@cloverdaleeggs.com": {"Travis", None},
    "priya.anand@cloverdaleeggs.com": {"Priya"},
    "rob.salgado@cloverdaleeggs.com": {"Rob", None},
    "anita.cho@cloverdaleeggs.com": {"Anita Cho\nQA / Food Safety Lead"},
    "glenn.whitaker@cloverdaleeggs.com": {"Glenn Whitaker\nCloverdale Feed Mill"},
    "brett.maloof@cloverdaleeggs.com": {"Brett"},
    "kholzmann@prairieavian.com": {"KH", "Dr. Holzmann"},
    "janelle.forsythe@hartwellag.com": {"Janelle Forsythe\nCorporate Controller\nHartwell Agricultural Partners"},
    "doug.pendergast@hartwellag.com": {"DP", None},
    "wstrup@tallgrasspullets.com": {"Wendell"},
    "hramos@reliablepoultry.com": {"Hector"},
}


def _signoff(body: str, allowed: set[str | None]) -> str | None:
    text = body.strip()
    for sig in sorted((s for s in allowed if s), key=len, reverse=True):
        if text.endswith("\n" + sig) or text == sig:
            return sig
    return None


def test_every_staff_bank_reply_signs_the_way_that_person_signs():
    docs = REPO_ROOT / "corpus" / "documents"
    banks = _real_banks()
    for addr, allowed in _SIGNOFFS.items():
        for ref in banks[addr]:
            body = (docs / ref).read_text(encoding="utf-8")
            assert _signoff(body, allowed) in allowed, f"{ref}: sign-off not one of {allowed}"


def test_staff_banks_ask_no_questions_and_travis_stays_lowercase():
    # A blind ack that asks a question invites an answer nobody will read.
    docs = REPO_ROOT / "corpus" / "documents"
    banks = _real_banks()
    for addr in _SIGNOFFS:
        for ref in banks[addr]:
            assert "?" not in (docs / ref).read_text(encoding="utf-8"), ref
    for ref in banks["travis.lindqvist@cloverdaleeggs.com"]:
        body = (docs / ref).read_text(encoding="utf-8").strip()
        prose = body.removesuffix("Travis").strip()
        assert prose == prose.lower(), f"{ref}: Travis types in lowercase"
