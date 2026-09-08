#!/usr/bin/env python
"""build-nodes-pack.py — assemble the send-ready "nodes pack" from the coworker pages.

Reads config.yml (enabled_nodes), docs/design-review/coworker/00-OVERVIEW.md (the themed
order) and 00-IDEA.md (the one-paragraph intro), and writes:

    docs/nodes-pack.md    one Markdown document: intro + every enabled node's page
    docs/nodes-pack.docx  the same, rendered by pandoc for pasting into a Google Doc

Fails loudly if an enabled node has no coworker page or no entry in 00-OVERVIEW.md, so the
pack can never silently miss a scored decision. Pages that exist but are not enabled are
skipped and listed.

Run:  ./venv/bin/python docs/build-nodes-pack.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COWORKER = os.path.join(ROOT, "docs", "design-review", "coworker")
OUT_MD = os.path.join(ROOT, "docs", "nodes-pack.md")
OUT_DOCX = os.path.join(ROOT, "docs", "nodes-pack.docx")

LINK_RE = re.compile(r"\[([^\]]+)\]\((?:\.\./nodes/)?[A-Z0-9_]+\.md\)")
PAGE_LINK_RE = re.compile(r"\*\*\[[^\]]+\]\(([A-Z0-9_]+)\.md\)\*\*")


def enabled_nodes() -> list[str]:
    with open(os.path.join(ROOT, "config.yml")) as f:
        cfg = yaml.safe_load(f)
    nodes = cfg.get("enabled_nodes") or []
    if not nodes:
        sys.exit("config.yml has no enabled_nodes")
    return list(nodes)


def overview_order() -> list[tuple[str, str]]:
    """(group heading, node id) pairs in the order 00-OVERVIEW.md lists them."""
    order: list[tuple[str, str]] = []
    group = ""
    with open(os.path.join(COWORKER, "00-OVERVIEW.md")) as f:
        for line in f:
            if line.startswith("## "):
                group = line[3:].strip()
            m = PAGE_LINK_RE.search(line)
            if m:
                order.append((group, m.group(1)))
    return order


def transform_page(text: str) -> str:
    """Make a standalone page fit inside the pack."""
    out: list[str] = []
    for line in text.splitlines():
        if line.startswith("#"):
            line = "#" + line  # demote one level: groups are H1, nodes H2, sections H3
        out.append(line)
    text = "\n".join(out)
    text = LINK_RE.sub(r"\1", text)  # cross-page links become plain text
    text = re.sub(r"<u>(.*?)</u>", r"[\1]{.underline}", text, flags=re.S)
    return text.strip() + "\n"


def git_stamp() -> str:
    try:
        sha = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], text=True).strip()
        date = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%cs"], text=True).strip()
        return f"{date}, revision {sha}"
    except Exception:  # noqa: BLE001 — a stamp is a nicety, never a build failure
        return "unversioned working copy"


def main() -> None:
    nodes = enabled_nodes()
    order = overview_order()
    listed = [n for _, n in order]
    missing_pages = [n for n in nodes if not os.path.exists(os.path.join(COWORKER, n + ".md"))]
    missing_overview = [n for n in nodes if n not in listed]
    if missing_pages or missing_overview:
        msg = []
        if missing_pages:
            msg.append("enabled nodes with no coworker page: " + ", ".join(missing_pages))
        if missing_overview:
            msg.append("enabled nodes with no 00-OVERVIEW.md entry: " + ", ".join(missing_overview))
        sys.exit("nodes pack NOT built.\n  " + "\n  ".join(msg))
    skipped = [n for n in listed if n not in nodes]

    with open(os.path.join(COWORKER, "00-IDEA.md")) as f:
        idea = f.read().strip().replace("{n_nodes}", str(len(nodes)))

    parts = ["# FarmBench: the welfare decisions", "", idea, ""]
    current_group = None
    for group, node in order:
        if node not in nodes:
            continue
        if group != current_group:
            parts += [f"# {group}", ""]
            current_group = group
        with open(os.path.join(COWORKER, node + ".md")) as f:
            parts += [transform_page(f.read()), ""]
    parts += ["---", "", f"*Assembled from the project repository on {git_stamp()}. "
              f"{len(nodes)} scored decisions.*", ""]
    with open(OUT_MD, "w") as f:
        f.write("\n".join(parts))

    subprocess.run(["pandoc", OUT_MD, "-f", "markdown", "-t", "docx", "-o", OUT_DOCX], check=True)
    print(f"wrote {OUT_MD} and {OUT_DOCX}: {len(nodes)} nodes")
    if skipped:
        print("pages present but not enabled (skipped): " + ", ".join(skipped))


if __name__ == "__main__":
    main()
