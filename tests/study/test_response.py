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
