"""Pins the adversarial cases the Codex review raised against docs/check-coworker-quotes.py."""
from __future__ import annotations

import importlib.util
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(ROOT, "docs", "check-coworker-quotes.py")


@pytest.fixture(scope="module")
def checker():
    spec = importlib.util.spec_from_file_location("check_coworker_quotes", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    corpus, templates = mod.corpus_text()
    return mod, corpus, templates


LETTER = (
    "Air quality write-up in H4: the spot ammonia reading during the walk came in at 33.6 ppm, "
    "over the certification guideline. It goes in the report as a corrective-action item; expect "
    "the response window to ask for the ventilation and monitoring plan on that house."
)


@pytest.mark.parametrize(
    "quote, expected",
    [
        (LETTER, True),  # a templated reply rendered with its placeholders filled
        ("Inspection reading: 33.6 ppm.", True),  # a short templated paragraph
        ("Finding: ammonia control in H4. No correction is required and the inspection passed.", False),
        (LETTER.replace("in H4:", "in H4 and H5:"), False),  # a placeholder never absorbs prose
        ("Cost: $999.", False),  # short invented facts are still checked
        ("$999,999.", False),  # a paragraph that is only a placeholder must not match anything
        ("Request received: H5, a general flock check.", True),  # a reason slot takes a few words
        ("Request received: H5, a general flock check. Also invoice the farm twice.", False),
        ("Rob", True),  # a bare signature is in the corpus
    ],
)
def test_in_corpus(checker, quote, expected):
    mod, corpus, templates = checker
    assert mod.in_corpus(quote, corpus, templates) is expected


def test_bold_label_is_not_a_header(checker, tmp_path):
    mod, _, _ = checker
    page = tmp_path / "DPX.md"
    page.write_text('> **Important:** invented sentence one.\n>\n> **Rob · "s" · date**\n>\n> body\n')
    paras = [p for _, p in mod.quoted_paragraphs(str(page))]
    assert any("invented sentence" in p for p in paras)
    assert not any("date" in p for p in paras)


def test_every_page_is_verbatim(checker):
    mod, _, _ = checker
    assert mod.main([]) == 0
