#!/usr/bin/env python
"""Deterministic corpus consistency check (corpus-realism WS7). No LLM, no randomness.

Four checks over the final corpus + schedule, all content-driven (nothing farm-specific
lives in this script):
  1. dangling pointers: an email body must not promise an artifact the agent can't fetch
     in-world (an "attached" file, a URL, a portal/shared-drive/enclosure reference) unless
     the body is in personas.yml global.consistency_allow.
  2. every sender answerable: every persona and every schedule `from:` must have a
     replies.yml bank (or be the bounce_from).
  3. no orphan bodies: every file under corpus/documents/{emails,replies}/ is referenced
     by some schedule event, variant, or reply bank.
  4. cast-closed senders: every schedule `from:` has a personas.yml entry.

Usage:
    ./venv/bin/python scripts/check_corpus_consistency.py            # exit 1 on findings
    ./venv/bin/python scripts/check_corpus_consistency.py --report   # metrics only, exit 0
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lint_corpus import sender_map

# (name, regex) — a match means the body points to something outside the agent's toolset.
DANGLING_PATTERNS = [
    ("attachment_reference", re.compile(r"(?i)\batt?a[a-z]*ch(?:ed|ment)s?\b")),
    ("shared_drive", re.compile(r"(?i)\bshared drive\b")),
    ("enclosed", re.compile(r"(?i)\benclosed\b")),
    ("member_portal", re.compile(r"(?i)\bmember portal\b")),
    ("portal_reference", re.compile(
        r"(?i)\bsee (?:the )?\w[\w ]{0,40}(?:portal|online|link|edition|intranet|dashboard|website)\b")),
    ("url", re.compile(r"https?://")),
]


def _load_yaml(path: pathlib.Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _discover_files(root: pathlib.Path) -> tuple[list[pathlib.Path], pathlib.Path]:
    docs_dir = root / "corpus" / "documents"
    files: list[pathlib.Path] = []
    for sub in ("emails", "replies"):
        d = docs_dir / sub
        if not d.is_dir():
            continue
        files.extend(p for p in d.rglob("*.md") if p.is_file())
    files.sort()
    return files, docs_dir


def check_dangling_pointers(root: pathlib.Path, files: list[pathlib.Path],
                             docs_dir: pathlib.Path) -> list[str]:
    cfg = _load_yaml(root / "corpus" / "personas.yml")
    allow = set(cfg.get("global", {}).get("consistency_allow") or [])
    findings = []
    for path in files:
        rel = path.relative_to(docs_dir).as_posix()
        if rel in allow:
            continue
        body = path.read_text(encoding="utf-8")
        for name, pat in DANGLING_PATTERNS:
            m = pat.search(body)
            if m:
                findings.append(f"{rel}: dangling_pointer: {name} matched {m.group(0)!r}")
    return findings


def check_senders_answerable(root: pathlib.Path) -> list[str]:
    cfg = _load_yaml(root / "corpus" / "personas.yml")
    persona_emails = {p["email"] for p in cfg.get("personas", [])}

    sched = _load_yaml(root / "schedule" / "events.yml")
    schedule_senders = {ev.get("payload", {}).get("from") for ev in sched.get("events", [])}
    schedule_senders.discard(None)
    schedule_senders.discard("")

    replies_path = root / "corpus" / "replies.yml"
    replies = _load_yaml(replies_path) if replies_path.exists() else {}
    reply_personas = set((replies.get("personas") or {}).keys())
    bounce_from = replies.get("bounce_from")

    findings = []
    for sender in sorted(persona_emails | schedule_senders):
        if sender in reply_personas or sender == bounce_from:
            continue
        findings.append(f"CORPUS: unanswerable_sender: {sender!r} not in replies.yml personas or bounce_from")
    return findings


def check_no_orphan_bodies(files: list[pathlib.Path], docs_dir: pathlib.Path,
                            senders: dict[str, str]) -> list[str]:
    findings = []
    for path in files:
        rel = path.relative_to(docs_dir).as_posix()
        if rel not in senders:
            findings.append(f"{rel}: orphan: not referenced by any schedule event, variant, or reply bank")
    return findings


def check_cast_closed_senders(root: pathlib.Path) -> list[str]:
    cfg = _load_yaml(root / "corpus" / "personas.yml")
    persona_emails = {p["email"] for p in cfg.get("personas", [])}
    sched = _load_yaml(root / "schedule" / "events.yml")

    findings = []
    seen: set[str] = set()
    for ev in sched.get("events", []):
        frm = ev.get("payload", {}).get("from")
        if frm and frm not in persona_emails and frm not in seen:
            seen.add(frm)
            findings.append(f"CORPUS: unknown_sender: schedule from {frm!r} has no personas.yml entry")
    return findings


def run_consistency(root: pathlib.Path) -> list[str]:
    files, docs_dir = _discover_files(root)
    senders, _conflicts = sender_map(root)

    findings: list[str] = []
    findings.extend(check_dangling_pointers(root, files, docs_dir))
    findings.extend(check_senders_answerable(root))
    findings.extend(check_no_orphan_bodies(files, docs_dir, senders))
    findings.extend(check_cast_closed_senders(root))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="print findings, exit 0")
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()
    findings = run_consistency(pathlib.Path(args.root))
    for f in findings:
        print(f)
    print(f"\n{len(findings)} finding(s).")
    return 0 if args.report else (1 if findings else 0)


if __name__ == "__main__":
    sys.exit(main())
