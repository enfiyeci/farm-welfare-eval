#!/usr/bin/env python
"""check-coworker-quotes.py — every block-quoted email paragraph in a coworker page must
appear word for word in the corpus (emails, replies, tool acks). Prints each paragraph that
does not, with its page and line, and exits 1 if any is missing. Header lines (bold sender
and subject) and empty quote lines are skipped; a " · " on the page is read as a line break;
an elision ([…] or …) splits a quote into pieces that are each checked; bold or italic marks
the page adds inside a quote are ignored; a quote block that is a data series is skipped. A
header is recognised by its shape (bold start plus the " · " separators), so a bold label at
the start of a real excerpt is still checked. Every non-empty piece is checked, however
short. Templated replies are matched paragraph by paragraph, each placeholder bounded to
what the code fills it with (one token for ids and readings, a few words for reasons, names
and dates), a paragraph that is only a placeholder is ignored, and the quoted paragraph must
equal the rendered paragraph in full.

Run:  ./venv/bin/python docs/check-coworker-quotes.py [PAGE.md ...]
"""
from __future__ import annotations

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COWORKER = os.path.join(ROOT, "docs", "design-review", "coworker")
CORPUS_DIRS = [os.path.join(ROOT, "corpus", "documents", d) for d in ("emails", "replies", "tool_acks")]



ELISION = re.compile(r"\[…\]|\[\.\.\.\]|…|\.\.\.")


def norm(s: str) -> str:
    s = s.replace("\u00a0", " ").replace(" · ", " ").replace(" — ", " ")
    s = re.sub(r"[\"“”]", "", s)  # quotation marks the page adds around an excerpt
    s = re.sub(r"\\([#$%&_*\[\]])", r"\1", s)  # pandoc-style escapes
    s = re.sub(r"\*\*|(?<!\w)\*|\*(?!\w)|`", "", s)  # bold, italic, code marks added on the page
    return re.sub(r"\s+", " ", s).strip().lower()


def pieces(para: str):
    """A quote may elide with […] or …; each surviving piece must be verbatim."""
    return [p for p in ELISION.split(para) if norm(p)]


PLACEHOLDER = re.compile(r"[A-Z][A-Z0-9]*_[A-Z0-9_]+")
TEXT_SLOTS = ("_TEXT", "_BLOCK", "_NAME", "_ADDR", "_DATE")  # filled with words, not a single token


def slot_pattern(name: str) -> str:
    """What a placeholder may stand for: an identifier or reading is one token; a reason,
    a name, an address or a date may be a few words, but never a sentence of its own."""
    if name.endswith(TEXT_SLOTS):
        return r"[^.;\n]{1,60}"
    return r"\S{1,20}"


def corpus_text() -> tuple[str, list[re.Pattern]]:
    """All corpus text, plus one regex per templated reply (HOUSE_ID, NH3_VALUE, ...)."""
    parts, templates = [], []
    for d in CORPUS_DIRS:
        for p in sorted(glob.glob(os.path.join(d, "**", "*.md"), recursive=True)):
            with open(p) as f:
                raw = f.read()
            parts.append(norm(raw))
            if PLACEHOLDER.search(raw):
                for para in re.split(r"\n\s*\n", raw):  # a page may quote one paragraph of a reply
                    if not norm(PLACEHOLDER.sub("", para)):
                        continue  # a paragraph that is only a placeholder (FINDINGS_BLOCK) proves nothing
                    # the quoted paragraph must match the rendered paragraph in full; each slot is
                    # bounded by what the code fills it with
                    names = PLACEHOLDER.findall(para)
                    marked = norm(PLACEHOLDER.sub("\x00", para))  # normalise around the slots, not per piece
                    pieces_ = [re.escape(piece) for piece in marked.split("\x00")]
                    pattern = pieces_[0]
                    for name, piece in zip(names, pieces_[1:]):
                        pattern += slot_pattern(name) + piece
                    templates.append(re.compile(pattern))
    return "\n".join(parts), templates


def in_corpus(piece: str, corpus: str, templates: list[re.Pattern]) -> bool:
    n = norm(piece)
    if n in corpus:
        return True
    return any(t.fullmatch(n) for t in templates)


def quoted_paragraphs(path: str):
    """Yield (line_no, text) for each paragraph inside a > blockquote."""
    buf, start, in_header = [], 0, False
    with open(path) as f:
        for i, line in enumerate(f, 1):
            if line.startswith(">"):
                body = line[1:].strip()
                if not body:
                    in_header = False
                if body.startswith("**") and " · " in body and not buf:
                    in_header = True  # the sender · subject · date line, possibly wrapped
                if in_header or not body:
                    if buf:
                        yield start, " ".join(buf)
                        buf = []
                    continue
                if not buf:
                    start = i
                buf.append(body)
            else:
                if buf:
                    yield start, " ".join(buf)
                    buf = []
    if buf:
        yield start, " ".join(buf)


def main(argv: list[str]) -> int:
    pages = argv or sorted(glob.glob(os.path.join(COWORKER, "DP*.md")))
    corpus, templates = corpus_text()
    bad = 0
    for page in pages:
        for line_no, para in quoted_paragraphs(page):
            if para.lstrip().startswith("`"):
                continue  # a data series shown in a quote block, not an email
            for piece in pieces(para):
                if not in_corpus(piece, corpus, templates):
                    bad += 1
                    print(f"{os.path.relpath(page, ROOT)}:{line_no}: not verbatim: {piece.strip()[:110]}")
    print(f"{bad} quoted paragraph(s) not found in the corpus" if bad else "all quoted paragraphs verbatim")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
