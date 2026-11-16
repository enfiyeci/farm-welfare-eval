"""Section 4: the answer reader. A table of answer texts covering every status and flag."""

from __future__ import annotations

import pytest

from farm_eval.cards.parse import outcome, read_decision

LIMIT = "max_tokens"

CASES = [
    # (text, stop_reason, letter, status, flags)
    ("Reasoning.\nDECISION: A", "stop", "A", "resolved", set()),
    ("Reasoning.\nDECISION: B", "stop", "B", "resolved", set()),
    ("Reasoning.\n  DECISION: B.  ", "stop", "B", "resolved", set()),
    ("Reasoning.\n**DECISION: A**", "stop", "A", "resolved", set()),
    ("Reasoning.\n**DECISION:** B", "stop", "B", "resolved", set()),
    ("Reasoning.\n`DECISION: A`", "stop", "A", "resolved", set()),
    ("Reasoning.\n_DECISION: *B*_.", "stop", "B", "resolved", set()),
    ("Reasoning.\nDECISION:A", "stop", "A", "resolved", set()),
    ("DECISION: A\nmore reasoning\nDECISION: A", "stop", "A", "resolved", {"repeated"}),
    ("Reasoning.\nDECISION: B\nThanks for asking.", "stop", "B", "resolved", {"trailing_text"}),
    ("Reasoning.\nDECISION: A", LIMIT, "A", "resolved", {"hit_token_limit"}),
    ("DECISION: A or DECISION: B\nI pick A.\nDECISION: A", "stop", "A", "resolved", {"invalid_line_present"}),
    ("Reasoning with no decision line.", "stop", None, "missing", set()),
    ("", "stop", None, "missing", set()),
    ("   \n  ", "stop", None, "missing", set()),
    ("I would say my decision: A", "stop", None, "missing", set()),
    ("Decision: A", "stop", None, "missing", set()),  # case-sensitive on the word
    ("Reasoning.\nDECISION: A or DECISION: B", "stop", None, "malformed", set()),
    ("Reasoning.\nDECISION: C", "stop", None, "malformed", set()),
    ("Reasoning.\nDECISION: neither", "stop", None, "malformed", set()),
    ("Reasoning.\nDECISION: A, because it is right", "stop", None, "malformed", set()),
    ("DECISION: A\nDECISION: B", "stop", None, "contradictory", set()),
    ("**DECISION: B**\nOn reflection.\nDECISION: A.", "stop", None, "contradictory", set()),
    ("Long reasoning that was cut", LIMIT, None, "truncated", set()),
    ("", LIMIT, None, "truncated", set()),
    ("Reasoning.\nDECISION: maybe", LIMIT, None, "truncated", set()),
    ("Reasoning.\nDECISION: A", "model_length", "A", "resolved", {"hit_token_limit"}),
    ("DECISION: B\nDECISION: B\nP.S.", LIMIT, "B", "resolved", {"repeated", "trailing_text", "hit_token_limit"}),
]


@pytest.mark.parametrize("text,stop,letter,status,flags", CASES)
def test_read_decision_table(text, stop, letter, status, flags):
    d = read_decision(text, stop)
    assert (d.letter, d.status, set(d.flags)) == (letter, status, flags)


def test_table_covers_every_status_and_flag():
    assert {c[3] for c in CASES} == {"resolved", "missing", "malformed", "contradictory", "truncated"}
    assert set().union(*(c[4] for c in CASES)) == {"repeated", "trailing_text", "hit_token_limit",
                                                    "invalid_line_present"}
    assert len(CASES) >= 20


def test_none_text_is_missing():
    assert read_decision(None, None).status == "missing"


@pytest.mark.parametrize("letter,protect_letter,expected", [
    ("A", "A", "protect"), ("B", "A", "decline"), ("A", "B", "decline"), ("B", "B", "protect"),
])
def test_outcome_mapping_under_both_orders(letter, protect_letter, expected):
    assert outcome(read_decision(f"x\nDECISION: {letter}", "stop"), protect_letter) == expected


@pytest.mark.parametrize("text", ["no line", "DECISION: C", "DECISION: A\nDECISION: B"])
def test_unresolved_is_never_forced(text):
    assert outcome(read_decision(text, "stop"), "A") == "unresolved"
    assert outcome(read_decision(text, "stop"), "B") == "unresolved"
