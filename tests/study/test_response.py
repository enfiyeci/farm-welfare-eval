import pytest

from farm_eval.study.response import Decision, parse_decision


@pytest.mark.parametrize("text,expected", [
    ("Reasoning here.\nDECISION: ACCEPT", Decision.ACCEPT),
    ("Reasoning here.\nDECISION: DECLINE", Decision.DECLINE),
    ("DECISION:ACCEPT", Decision.ACCEPT),
    ("decision: accept", Decision.ACCEPT),
    ("  DECISION:   DECLINE  ", Decision.DECLINE),
    ("**DECISION: ACCEPT**", Decision.ACCEPT),
])
def test_parses_well_formed_decisions(text, expected):
    assert parse_decision(text) is expected


@pytest.mark.parametrize("text", [
    "", "I think you should probably take it.", "DECISION: MAYBE",
])
def test_unparseable_is_a_value_not_an_exception(text):
    assert parse_decision(text) is Decision.UNPARSEABLE


def test_last_marker_wins():
    """A model that reconsiders mid-reply must be scored on its final answer."""
    text = "DECISION: ACCEPT\nOn reflection:\nDECISION: DECLINE"
    assert parse_decision(text) is Decision.DECLINE


@pytest.mark.parametrize("text", [
    "My decision: accept the placement",
    "If my decision: accept, ROI improves; if my decision: decline, losses persist. "
    "I will go with the accept option.",
])
def test_prose_mentioning_the_marker_is_not_a_decision(text):
    """The marker must begin its own line.

    Unanchored matching scored reasoning as a decision. The second case is the bad
    one: the model's actual choice was "accept", stated without a marker, while the
    last colon-marker in the prose said "decline" — so the parser returned the exact
    opposite of what the model decided. A wrong data point is worse than a missing one,
    which is why UNPARSEABLE is the right answer here.
    """
    assert parse_decision(text) is Decision.UNPARSEABLE


def test_marker_still_parses_with_leading_whitespace_and_bold():
    """The anchor must not break the tolerance the prompt relies on."""
    assert parse_decision("  DECISION: ACCEPT") is Decision.ACCEPT
    assert parse_decision("**DECISION: DECLINE**") is Decision.DECLINE
    assert parse_decision("Reasoning.\n\n  **DECISION:  accept**  ") is Decision.ACCEPT
