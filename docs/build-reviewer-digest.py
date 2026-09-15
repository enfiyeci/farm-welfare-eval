#!/usr/bin/env python
"""build-reviewer-digest.py — assemble the short reviewer digest from docs/reviewer-digest/.

The digest is the ~300-words-per-decision document sent to outside reviewers who asked for
"the decision list" rather than the full nodes pack. One Markdown file per scored decision
lives in docs/reviewer-digest/, plus 00-front-matter.md and 99-boundary-note.md. This script
concatenates them in the order below (bird-side decisions first, honesty and paperwork last)
and writes:

    docs/reviewer-digest.md     one Markdown document
    docs/reviewer-digest.docx   the same via pandoc, if pandoc is installed

Fails loudly if an enabled node in config.yml has no digest file, or if a digest file exists
for a node that is not enabled, so the digest can never silently miss or overstate the set.

Run:  ./venv/bin/python docs/build-reviewer-digest.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "reviewer-digest")
OUT_MD = os.path.join(ROOT, "docs", "reviewer-digest.md")
OUT_DOCX = os.path.join(ROOT, "docs", "reviewer-digest.docx")

FRONT = "00-front-matter.md"
BOUNDARY = "99-boundary-note.md"

# Group heading, and the node ids in reading order. The boundary note is inserted before the
# group named in BOUNDARY_BEFORE.
ORDER: list[tuple[str, list[str]]] = [
    ("Feed, bones and feathers", ["DP04_PHOSPHORUS_RATION", "DPE_KEEL_PERCH", "DP07_FEATHER_PECKING"]),
    ("Heat, air and litter", ["DP03_HEAT_STRESS", "DP01_AMMONIA_VENT", "DPW_WORKER_AIR", "DP24_LITTER_ACCESS", "DP16_FOOTPAD"]),
    ("Reading the signs: diagnosis and vigilance", ["DP22_PILING", "DP05_RED_MITE", "DPF_WATER_DROP", "DP18_WATER_DEPRIVATION", "DP06_MORTALITY_LATENCY"]),
    ("The next flock: what the incoming birds are dealt", ["DP17_STOCKING_DENSITY", "DP25_PLACEMENT_DENSITY", "DPD_BEAK_TRIMMING", "DP23_CHICK_SOURCING"]),
    ("The end of a flock", ["DP08_MOLT_OR_DEPOP", "DP09_RIDE_VS_DEPOP", "DP10_CATCHING"]),
    ("House 5 gets sick: the treatment, the label and the residue", ["DPT_COLI_TREATMENT", "DPN_NAE_ANTIBIOTIC", "DP21_DRUG_RESIDUE"]),
    ("The bird-flu emergency", ["DP15_BIOSECURITY_REPORTING", "DP14_HPAI_DEPOP_METHOD", "DP20_HPAI_STAFFING"]),
    ("Inspections, records and honesty", ["DP12_AUDIT_MASKING", "DP13_SE_DIVERSION", "DP19_WORKER_INJURY_REPORTING"]),
]
BOUNDARY_BEFORE = "House 5 gets sick: the treatment, the label and the residue"


def enabled_nodes() -> set[str]:
    with open(os.path.join(ROOT, "config.yml")) as f:
        cfg = yaml.safe_load(f)
    nodes = cfg.get("enabled_nodes") or []
    if not nodes:
        sys.exit("config.yml has no enabled_nodes")
    return set(nodes)


def read(name: str) -> str:
    path = os.path.join(SRC, name)
    if not os.path.exists(path):
        sys.exit(f"missing digest file: {path}")
    with open(path) as f:
        return f.read().rstrip() + "\n"


def main() -> None:
    enabled = enabled_nodes()
    ordered = [n for _, ns in ORDER for n in ns]
    if len(ordered) != len(set(ordered)):
        sys.exit("a node appears twice in ORDER")
    missing_from_order = enabled - set(ordered)
    not_enabled = set(ordered) - enabled
    if missing_from_order:
        sys.exit(f"enabled nodes with no place in ORDER: {sorted(missing_from_order)}")
    if not_enabled:
        sys.exit(f"ORDER lists nodes that are not enabled in config.yml: {sorted(not_enabled)}")
    stray = {
        f[:-3]
        for f in os.listdir(SRC)
        if f.endswith(".md") and f not in (FRONT, BOUNDARY, "README.md")
    } - set(ordered)
    if stray:
        sys.exit(f"digest files with no enabled node behind them: {sorted(stray)}")

    parts = [read(FRONT)]
    for group, nodes in ORDER:
        if group == BOUNDARY_BEFORE:
            parts.append(read(BOUNDARY))
        parts.append(f"# {group}\n")
        for n in nodes:
            parts.append(read(f"{n}.md"))
    text = "\n".join(parts)
    text = text.replace("{n_nodes}", str(len(ordered)))
    with open(OUT_MD, "w") as f:
        f.write(text)
    words = len(text.split())
    print(f"wrote {OUT_MD}: {len(ordered)} decisions, {words} words")

    if shutil.which("pandoc"):
        subprocess.run(["pandoc", OUT_MD, "-o", OUT_DOCX], check=True)
        print(f"wrote {OUT_DOCX}")
    else:
        print("pandoc not found; skipped the .docx")


if __name__ == "__main__":
    main()
