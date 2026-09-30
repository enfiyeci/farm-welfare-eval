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
import datetime as _dt
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
        # Agency-domain tier (DP15 fix, 2026-08-11): domain banks have no fixed sender
        # address — the reply goes out under whatever mailbox the agent wrote to — so the
        # domain itself stands in as the voice key.
        for domain, dcfg in (replies.get("domains") or {}).items():
            for ref in dcfg.get("bank", []):
                assign(ref, domain)
        vet = replies.get("vet") or {}
        for key in ("ack_refs", "ack_pending_refs", "report_default_refs", "report_bacterial_refs"):
            for ref in vet.get(key) or []:
                assign(ref, vet.get("from", ""))
        for row in vet.get("report_classes") or []:
            for ref in row.get("refs") or []:
                assign(ref, vet.get("from", ""))
        # DP05 red-mite control correspondence (2026-08-26): the vet writes the treatment order
        # and the post-course trap round, the applicator writes the work order — two voices in
        # one section, so each ref is assigned to the sender that actually sends it.
        mite = replies.get("mite_control") or {}
        for key in ("approval_ref", "follow_up_controlled_ref", "follow_up_persisting_ref"):
            if mite.get(key):
                assign(mite[key], mite.get("from", ""))
        if mite.get("provider_ref"):
            assign(mite["provider_ref"], mite.get("provider_from", ""))
        # DPE mobility retrofit (2026-08-19): the maintenance lead closes out the work order.
        retro = replies.get("retrofit") or {}
        for key in ("approval_ref", "approval_empty_ref"):
            if retro.get(key):
                assign(retro[key], retro.get("from", ""))
        for cls in ((replies.get("conflict") or {}).get("classes") or {}).values():
            voice = cls.get("voice", "")
            banks = [cls.get("default_refs") or [], cls.get("repeat_refs") or [],
                     *(cls.get("by_domain") or {}).values()]
            for bank in banks:
                for ref in bank:
                    assign(ref, voice)
        audit = replies.get("audit") or {}
        for key in ("frame_ref", "clean_ref"):
            if audit.get(key):
                assign(audit[key], audit.get("voice", ""))
        for key in ("nh3_refs", "space_refs"):
            for ref in audit.get(key) or []:
                assign(ref, audit.get("voice", ""))
        # DP15 responding world (2026-08-27): the animal-health authority's authorization
        # letter, delivered by `farm_eval/env/state_response.py` rather than through a bank
        # rotation — it is a one-shot consequence of a filed report, not a reply that repeats.
        auth = replies.get("hpai_authorization") or {}
        if auth.get("ref"):
            # Keyed by `voice` (the agency-mailbox persona, a domain string) rather than by the
            # `from` mailbox, exactly as the domain banks above are: the letter is the agency
            # voice, and the specific mailbox it arrives from is an addressing detail.
            assign(auth["ref"], auth.get("voice", ""))
        if replies.get("bounce_ref"):
            assign(replies["bounce_ref"], replies.get("bounce_from", ""))
    return senders, conflicts


def schedule_days(root: pathlib.Path) -> dict[str, list[int]]:
    """body_ref -> every `on_day` a schedule event serves it on (body_ref and all variants)."""
    days: dict[str, list[int]] = {}
    sched = _load_yaml(root / "schedule" / "events.yml")
    for ev in sched.get("events", []):
        day = ev.get("on_day")
        if not isinstance(day, int):
            continue
        refs = [(ev.get("payload") or {}).get("body_ref"), *(ev.get("variants") or {}).values()]
        for ref in refs:
            if ref:
                days.setdefault(ref, []).append(day)
    return days


def season_findings(rel: str, body: str, rules: list[dict], days: list[int] | None,
                    start: _dt.date | None) -> list[str]:
    """Season lint (overnight backlog F3, 2026-09-30). A scheduled email is flagged when a rule's
    regex matches and ANY day it is served on falls in the rule's months (the calendar is
    `company.yml:start_date` + `on_day`, so a whole-year shift keeps every finding). A reply body
    has no scheduled day (it answers whatever the agent sent, in any month), so it is flagged
    whenever a rule matches: reply copy must be season-neutral outright."""
    out: list[str] = []
    for rule in rules:
        if rel in (rule.get("allow") or []):
            continue
        m = re.search(rule["regex"], body)
        if not m:
            continue
        if rel.startswith("replies/"):
            out.append(f"{rel}: season: {rule['name']}: {m.group(0)!r} in a reply body (served any day)")
            continue
        if start is None:
            continue
        months = set(rule.get("months") or [])
        for day in sorted(set(days or [])):
            when = start + _dt.timedelta(days=day)
            if when.month in months:
                out.append(f"{rel}: season: {rule['name']}: {m.group(0)!r} in mail dated {when.isoformat()}")
                break
    return out


def _start_date(root: pathlib.Path) -> _dt.date | None:
    path = root / "corpus" / "company.yml"
    if not path.exists():
        return None
    raw = _load_yaml(path).get("start_date")
    if isinstance(raw, _dt.date):
        return raw
    return _dt.date.fromisoformat(str(raw)) if raw else None


def run_lint(root: pathlib.Path) -> list[str]:
    cfg = _load_yaml(root / "corpus" / "personas.yml")
    g = cfg["global"]
    persona_rules = {p["email"]: p for p in cfg["personas"]}
    senders, conflicts = sender_map(root)
    season_rules = g.get("season_rules") or []
    served_days = schedule_days(root) if season_rules else {}
    start = _start_date(root) if season_rules else None

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
        allowance = max(
            1,
            words // g["em_dash_per_file_words_per"],
            (g.get("em_dash_file_allowances") or {}).get(rel, 0),
        )
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

        findings.extend(season_findings(rel, body, season_rules, served_days.get(rel), start))

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
