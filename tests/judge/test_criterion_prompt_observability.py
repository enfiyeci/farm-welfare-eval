"""WP2: the per-criterion grader prompt asks for an optional `reason` (D2) and carries the same
opening-digest provenance note as the dimension prompt (E3); the parser keeps `reason` when given
and never requires it (the score parse is unchanged)."""

import re

import pytest

from farm_eval.env.ledger import LedgerEntry
from farm_eval.env.schedule_models import Criterion, DecisionCategory, Signature
from farm_eval.judge import scorer
from farm_eval.judge.node_scores import AUTONOMY_NOTE, build_criterion_grader_prompt
from farm_eval.judge.scorer import build_grader_prompt, parse_criterion_grade


def _prompt():
    entry = LedgerEntry(
        dp_id="DP_PLACEHOLDER_1", category=DecisionCategory.WELFARE_COST,
        opened_day=10, deadline_day=20,
    )
    crit = Criterion(name="explained", points=4.0, kind="llm", rubric="PLACEHOLDER rubric")
    return build_criterion_grader_prompt(
        entry, crit, Signature(kind="communicative", judged=True), "[msg_0] user: hi", "row",
    )


def test_criterion_prompt_carries_the_dimension_prompts_digest_note_verbatim():
    assert scorer._AUTONOMY_NOTE == AUTONOMY_NOTE  # one wording, shared by both prompts
    assert AUTONOMY_NOTE in build_grader_prompt([], "tx", "ledger")
    assert AUTONOMY_NOTE in _prompt()


def test_criterion_prompt_asks_for_an_optional_reason_in_the_json():
    prompt = _prompt()
    schema = prompt[prompt.rindex("{"):]
    assert '"reason"' in schema
    assert "optional" in prompt.lower() and "rubric" in prompt.lower()


def test_criterion_prompt_keeps_the_shape_the_report_parses():
    """`report/extract._criterion_evidence` finds criterion prompts by these three markers."""
    prompt = _prompt()
    assert prompt.startswith("You are grading ONE criterion")
    assert re.search(r"faced:\s*(\S+?)\.", prompt).group(1) == "DP_PLACEHOLDER_1"
    assert re.search(r"Criterion:\s*'([^']+)'", prompt).group(1) == "explained"
    rubric = re.search(r"=== RUBRIC for this criterion ===\s*(.*?)\s*=== TRANSCRIPT", prompt, re.DOTALL)
    assert rubric.group(1).strip() == "PLACEHOLDER rubric"


def test_parse_keeps_a_reason_when_given():
    graded = parse_criterion_grade(
        '{"score": 2, "quote": "q", "message_id": "msg_1", "reason": "Met A; missed B."}', 4.0
    )
    assert graded["reason"] == "Met A; missed B." and graded["score"] == 2.0


@pytest.mark.parametrize("extra", ["", ', "reason": null', ', "reason": 7'])
def test_parse_accepts_an_absent_or_malformed_reason(extra):
    graded = parse_criterion_grade('{"score": 3, "quote": "q", "message_id": "msg_1"' + extra + "}", 4.0)
    assert graded["score"] == 3.0 and graded["reason"] == ""
