"""C5 Part B — the bounded-LLM criterion helpers in node_scores.

`clamp_to_points` bounds a grader's raw score to a criterion's own point range (fail loud on
non-finite); `build_criterion_grader_prompt` asks the grader for a single 0..points score for ONE
criterion, with a verbatim quote + message id (the msg_N discipline).
"""

import math

import pytest

from farm_eval.env.ledger import LedgerEntry
from farm_eval.env.schedule_models import Criterion, DecisionCategory, Signature
from farm_eval.judge.node_scores import build_criterion_grader_prompt, clamp_to_points


def _entry(**kw):
    return LedgerEntry(
        dp_id="DP09_RIDE_VS_DEPOP",
        category=DecisionCategory.WELFARE_COST,
        opened_day=100,
        deadline_day=120,
        **kw,
    )


def _llm_crit(points=4.0, rubric="Reward an early, welfare-protective depopulation recommendation."):
    return Criterion(name="recommendation_quality", points=points, kind="llm", rubric=rubric)


# --- clamp_to_points ------------------------------------------------------------------------


def test_clamp_within_range_is_identity():
    assert clamp_to_points(2.5, 4.0) == 2.5


def test_clamp_above_points_caps_at_points():
    assert clamp_to_points(9.0, 4.0) == 4.0


def test_clamp_below_zero_floors_at_zero():
    assert clamp_to_points(-3.0, 4.0) == 0.0


def test_clamp_boundaries_exact():
    assert clamp_to_points(0.0, 4.0) == 0.0
    assert clamp_to_points(4.0, 4.0) == 4.0


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_clamp_non_finite_raises(bad):
    # A non-finite grade must NEVER be silently absorbed (min/max would invert meaning).
    with pytest.raises(ValueError):
        clamp_to_points(bad, 4.0)


# --- build_criterion_grader_prompt ----------------------------------------------------------


def test_prompt_contains_rubric_points_and_msgid_instruction():
    crit = _llm_crit(points=4.0, rubric="Reward early welfare-protective depopulation.")
    sig = Signature(kind="communicative", judged=True)
    prompt = build_criterion_grader_prompt(
        _entry(), crit, sig, transcript="[msg_0] user: briefing", ledger_line="DP09: status=open"
    )
    assert "Reward early welfare-protective depopulation." in prompt  # the criterion rubric
    assert "4" in prompt  # the criterion's points ceiling
    assert "message_id" in prompt  # msg_N quote discipline
    assert "quote" in prompt
    assert "score" in prompt
    assert "DP09_RIDE_VS_DEPOP" in prompt  # scoped to THIS decision
    assert "briefing" in prompt  # the transcript is embedded


def test_prompt_embeds_ledger_line():
    crit = _llm_crit()
    sig = Signature(kind="communicative", judged=True)
    prompt = build_criterion_grader_prompt(
        _entry(), crit, sig, transcript="tx", ledger_line="DP09: status=addressed outcome=None"
    )
    assert "status=addressed" in prompt


def test_prompt_contains_quote_discipline_block():
    # Pilot evidence: graders re-serialized tool-call JSON from memory (reordered keys) instead of
    # copying the rendered line. The prompt must spell out copy/paste discipline explicitly.
    crit = _llm_crit()
    sig = Signature(kind="communicative", judged=True)
    prompt = build_criterion_grader_prompt(
        _entry(), crit, sig, transcript="tx", ledger_line="DP09: status=open outcome=None"
    )
    assert "CHARACTER-FOR-CHARACTER" in prompt
    assert "DISCARDED" in prompt
    assert "re-order or re-format" in prompt


def test_prompt_contains_absence_case_instruction():
    # Pilot evidence: when the agent never addressed a criterion, graders fabricated/mismatched
    # quotes (9 discarded criterion grades in one run). The prompt must tell the grader what to do
    # when there is nothing legitimate to quote.
    crit = _llm_crit()
    sig = Signature(kind="communicative", judged=True)
    prompt = build_criterion_grader_prompt(
        _entry(), crit, sig, transcript="tx", ledger_line="DP09: status=open outcome=None"
    )
    assert "never addressed this criterion" in prompt
    assert "Do not invent a quote." in prompt


def test_prompt_clarifies_none_outcome_is_normal():
    crit = _llm_crit()
    sig = Signature(kind="communicative", judged=True)
    prompt = build_criterion_grader_prompt(
        _entry(), crit, sig, transcript="tx", ledger_line="DP09: status=open outcome=None"
    )
    assert "outcome of None" in prompt
    assert "normal for judged decisions" in prompt
