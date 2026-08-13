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
DASH_CHARS = ("—", "–", "‒", "−")  # em dash, en dash, figure dash, minus sign


def _load_yaml(path: pathlib.Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def sender_map(root: pathlib.Path) -> tuple[dict[str, str], list[tuple[str, str, str]]]:
    """(body_ref -> sender email, conflicts) — ref relative to corpus/documents/.

    Sources: schedule event payloads (from + body_ref/variants) and, when present, the
    reply manifest (persona banks plus generated vet/conflict/audit replies). A file none
    names is unmapped — an authoring error surfaced as a finding.

    conflicts is a list of (ref, first_sender, second_sender) tuples for any ref that
    is assigned two DIFFERENT senders across the sources above; re-assigning the same
    ref to the same sender again is not a conflict. The first-seen sender wins in the
    returned map (later differing assignments are recorded as conflicts, not applied).
    """
    senders: dict[str, str] = {}
    conflicts: list[tuple[str, str, str]] = []

    def assign(ref: str, frm: str) -> None:
        if ref in senders:
            if senders[ref] != frm:
                conflicts.append((ref, senders[ref], frm))
        else:
            senders[ref] = frm

    sched = _load_yaml(root / "schedule" / "events.yml")
    for ev in sched.get("events", []):
        payload = ev.get("payload", {})
        frm = payload.get("from", "")
        if payload.get("body_ref"):
            assign(payload["body_ref"], frm)
        for ref in (ev.get("variants") or {}).values():
            assign(ref, frm)
    replies_path = root / "corpus" / "replies.yml"
    if replies_path.exists():
        replies = _load_yaml(replies_path)
        for sender, pcfg in (replies.get("personas") or {}).items():
            for ref in pcfg.get("bank", []):
                assign(ref, sender)
        vet = replies.get("vet") or {}
        for key in ("ack_refs", "ack_pending_refs", "report_default_refs"):
            for ref in vet.get(key) or []:
                assign(ref, vet.get("from", ""))
        for row in vet.get("report_classes") or []:
            for ref in row.get("refs") or []:
                assign(ref, vet.get("from", ""))
        for cls in ((replies.get("conflict") or {}).get("classes") or {}).values():
            voice = cls.get("voice", "")
            banks = [cls.get("default_refs") or [], cls.get("repeat_refs") or [],
                     *(cls.get("by_domain") or {}).values()]
            for bank in banks:
                for ref in bank:
                    assign(ref, voice)
        consult = replies.get("offer_consult") or {}
        consult_voice = consult.get("voice", "")
        for entry in (consult.get("offers") or {}).values():
            for ref in entry.get("refs") or []:
                assign(ref, consult_voice)
        audit = replies.get("audit") or {}
        for key in ("frame_ref", "clean_ref"):
            if audit.get(key):
                assign(audit[key], audit.get("voice", ""))
        for key in ("nh3_refs", "space_refs"):
            for ref in audit.get(key) or []:
                assign(ref, audit.get("voice", ""))
        if replies.get("bounce_ref"):
            assign(replies["bounce_ref"], replies.get("bounce_from", ""))
    return senders, conflicts


def run_lint(root: pathlib.Path) -> list[str]:
    cfg = _load_yaml(root / "corpus" / "personas.yml")
    g = cfg["global"]
    persona_rules = {p["email"]: p for p in cfg["personas"]}
    senders, conflicts = sender_map(root)

    docs_dir = root / "corpus" / "documents"
    files: list[pathlib.Path] = []
    discovery_findings: list[str] = []
    for sub in ("emails", "replies"):
        d = docs_dir / sub
        if not d.is_dir():
            continue
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix == ".md":
                files.append(p)
            else:
                rel = p.relative_to(docs_dir).as_posix()
                discovery_findings.append(f"{rel}: discovery: non-md file in corpus documents")
    files.sort()
    discovery_findings.sort()

    if not files:
        return ["CORPUS: discovery: no email files found under corpus/documents/"]

    linted_rels = {p.relative_to(docs_dir).as_posix() for p in files}

    findings: list[str] = list(discovery_findings)
    for ref, a, b in conflicts:
        findings.append(f"{ref}: sender_conflict: mapped to both {a!r} and {b!r}")
    for ref in sorted(senders):
        if (ref.startswith("emails/") or ref.startswith("replies/")) and ref not in linted_rels:
            findings.append(f"{ref}: discovery: referenced but not found under corpus/documents")

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

        n_emdash = sum(body.count(c) for c in DASH_CHARS)
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
        if rel.startswith("replies/"):
            for lex in g.get("reply_banned_lexemes", []):
                if re.search(rf"(?<!\w){re.escape(lex)}(?!\w)", low):
                    findings.append(f"{rel}: reply_banned_lexeme: {lex!r}")
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
