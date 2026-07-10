#!/usr/bin/env python
"""Deterministic corpus style lint (corpus-realism WS1). No LLM, no randomness.

Checks every email body under corpus/documents/emails/ and corpus/documents/replies/
against the thresholds in corpus/personas.yml. All thresholds/ban-lists are CONTENT
(loaded from personas.yml) — nothing farm-specific lives in this script.

Usage:
    ./venv/bin/python scripts/lint_corpus.py            # exit 1 on findings
    ./venv/bin/python scripts/lint_corpus.py --report   # metrics only, exit 0
"""
from __future__ import annotations

import argparse
import pathlib
import re
import statistics
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
EM_DASH = "—"


def _load_yaml(path: pathlib.Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def sender_map(root: pathlib.Path) -> dict[str, str]:
    """body_ref (relative to corpus/documents/) -> sender email.

    Sources: schedule event payloads (from + body_ref/variants) and, when present, the
    reply manifest (corpus/replies.yml personas' banks). A file neither names is unmapped
    — an authoring error (orphan or missing schedule entry) surfaced as a finding.
    """
    senders: dict[str, str] = {}
    sched = _load_yaml(root / "schedule" / "events.yml")
    for ev in sched.get("events", []):
        payload = ev.get("payload", {})
        frm = payload.get("from", "")
        if payload.get("body_ref"):
            senders[payload["body_ref"]] = frm
        for ref in (ev.get("variants") or {}).values():
            senders[ref] = frm
    replies_path = root / "corpus" / "replies.yml"
    if replies_path.exists():
        replies = _load_yaml(replies_path)
        for sender, pcfg in (replies.get("personas") or {}).items():
            for ref in pcfg.get("bank", []):
                senders[ref] = sender
        if replies.get("bounce_ref"):
            senders[replies["bounce_ref"]] = replies.get("bounce_from", "")
    return senders


def run_lint(root: pathlib.Path) -> list[str]:
    cfg = _load_yaml(root / "corpus" / "personas.yml")
    g = cfg["global"]
    persona_rules = {p["email"]: p for p in cfg["personas"]}
    senders = sender_map(root)

    docs_dir = root / "corpus" / "documents"
    files = sorted(
        p for d in (docs_dir / "emails", docs_dir / "replies") if d.is_dir()
        for p in d.glob("*.md")
    )
    findings: list[str] = []
    word_counts: list[int] = []
    total_words = 0
    total_emdash = 0
    files_with_question = 0

    for path in files:
        rel = path.relative_to(docs_dir).as_posix()
        body = path.read_text(encoding="utf-8")
        words = len(body.split())
        word_counts.append(words)
        total_words += words

        n_emdash = body.count(EM_DASH)
        total_emdash += n_emdash
        allowance = max(1, words // g["em_dash_per_file_words_per"])
        if n_emdash > allowance:
            findings.append(f"{rel}: em_dash: {n_emdash} em dashes (allowance {allowance} for {words} words)")

        n_q = body.count("?")
        if n_q > 0:
            files_with_question += 1
        if n_q > g["question_max_per_file"]:
            findings.append(f"{rel}: question: {n_q} question marks (max {g['question_max_per_file']})")

        low = body.lower()
        for lex in g["banned_lexemes"]:
            if lex in low:
                findings.append(f"{rel}: banned_lexeme: {lex!r}")
        for pat in g["banned_patterns"]:
            if rel in (pat.get("allow") or []):
                continue
            if re.search(pat["regex"], body):
                findings.append(f"{rel}: {pat['name']}: pattern {pat['regex']!r} matched")

        sender = senders.get(rel)
        if sender is None:
            findings.append(f"{rel}: unmapped: not referenced by any schedule event or reply bank")
        else:
            rule = persona_rules.get(sender)
            if rule is None:
                findings.append(f"{rel}: unknown_persona: sender {sender!r} has no personas.yml entry")
            elif words > rule["max_words"]:
                findings.append(f"{rel}: max_words: {words} words > {rule['max_words']} ({rule['name']})")

    if len(word_counts) >= 5:
        mean = statistics.mean(word_counts)
        cv = statistics.pstdev(word_counts) / mean if mean else 0.0
        if cv < g["length_cv_min"]:
            findings.append(f"CORPUS: length_variance: CV {cv:.2f} < {g['length_cv_min']} (lengths too uniform)")
        short_frac = sum(1 for w in word_counts if w <= g["short_words"]) / len(word_counts)
        if short_frac < g["short_fraction_min"]:
            findings.append(f"CORPUS: length_variance: only {short_frac:.0%} of emails <= {g['short_words']} words "
                            f"(need >= {g['short_fraction_min']:.0%})")
        long_frac = sum(1 for w in word_counts if w >= g["long_words"]) / len(word_counts)
        if long_frac < g["long_fraction_min"]:
            findings.append(f"CORPUS: length_variance: only {long_frac:.0%} of emails >= {g['long_words']} words "
                            f"(need >= {g['long_fraction_min']:.0%})")
        q_frac = files_with_question / len(word_counts)
        if q_frac > g["question_file_fraction_max"]:
            findings.append(f"CORPUS: question: {q_frac:.0%} of emails contain a question "
                            f"(max {g['question_file_fraction_max']:.0%})")
        if total_words and total_emdash > total_words / g["em_dash_words_per"]:
            findings.append(f"CORPUS: em_dash: {total_emdash} em dashes across {total_words} words "
                            f"(max 1 per {g['em_dash_words_per']})")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="print findings + metrics, exit 0")
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()
    findings = run_lint(pathlib.Path(args.root))
    for f in findings:
        print(f)
    print(f"\n{len(findings)} finding(s).")
    return 0 if args.report else (1 if findings else 0)


if __name__ == "__main__":
    sys.exit(main())
