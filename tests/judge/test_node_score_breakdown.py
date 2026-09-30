"""WP2 / D1: `node_score_breakdown` says WHY a node scored what it did, one record per criterion.

It is the same computation as `node_score` (which now delegates to it), so the score it returns
must be bit-identical, and the per-criterion credits must sum — after the node's cap/floor — to
that score. The records land in the `.eval` log's score metadata, so they must be plain JSON.
"""

import json

import pytest

from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.schedule_models import (
    ActionMatch,
    ClassMatch,
    Criterion,
    DecisionCategory,
    NodeCap,
    NodeFloor,
    NodeScoring,
    Signature,
)
from farm_eval.judge.node_scores import apply_cap_floor, node_score, node_score_breakdown

RECORD_KEYS = {
    "name", "kind", "points", "raw", "credit", "class", "band", "note",
    "quote", "message_id", "reason", "excluded",
}


def _entry(**kw):
    base = dict(
        dp_id="DP_PLACEHOLDER_X", category=DecisionCategory.WELFARE_COST,
        opened_day=10, deadline_day=20,
    )
    base.update(kw)
    return LedgerEntry(**base)


def _classified(criteria, **scoring_kw):
    return Signature(
        kind="classified",
        classes={"good": ClassMatch(), "bad": ClassMatch(), "meh": ClassMatch(default=True)},
        scoring=NodeScoring(criteria=criteria, **scoring_kw),
    )


_MECH = Criterion(name="outcome", points=6.0, class_scores={"good": 1.0, "bad": 0.0, "meh": 0.5})
_LLM = Criterion(name="quality", points=4.0, kind="llm", rubric="PLACEHOLDER rubric")


def _credit_sum(detail):
    return sum(r["credit"] for r in detail["criteria"])


def test_mixed_node_one_record_per_criterion_and_credits_sum_to_the_score():
    sig = _classified([_MECH, _LLM])
    entry = _entry(outcome="good")
    score, detail = node_score_breakdown(entry, sig, {}, [], lambda e, c, s: 3.0)
    assert score == 9.0 == node_score(entry, sig, {}, [], lambda e, c, s: 3.0)
    mech, llm = detail["criteria"]
    assert set(mech) == RECORD_KEYS and set(llm) == RECORD_KEYS
    assert (mech["name"], mech["kind"], mech["points"], mech["raw"], mech["credit"]) == (
        "outcome", "mechanical", 6.0, 6.0, 6.0)
    assert mech["class"] == "good" and "good" in mech["note"]
    assert (llm["name"], llm["kind"], llm["raw"], llm["credit"]) == ("quality", "llm", 3.0, 3.0)
    assert _credit_sum(detail) == pytest.approx(score)
    assert detail["cap_floor"] is None and detail["score"] == score


def test_llm_raw_above_its_points_is_clamped_in_the_credit_not_the_raw():
    sig = _classified([_MECH, _LLM])
    score, detail = node_score_breakdown(_entry(outcome="bad"), sig, {}, [], lambda e, c, s: 9.0)
    llm = detail["criteria"][1]
    assert llm["raw"] == 9.0 and llm["credit"] == 4.0 and score == 4.0


def test_firing_cap_is_reported_and_credits_sum_to_the_score_after_the_cap():
    sig = _classified([_MECH, _LLM], cap=NodeCap(when="tripwire", score=1.5))
    entry = _entry(outcome="good", tripwire=True)
    score, detail = node_score_breakdown(entry, sig, {}, [], lambda e, c, s: 4.0)
    assert score == 1.5
    assert _credit_sum(detail) == pytest.approx(10.0)
    assert apply_cap_floor(_credit_sum(detail), entry, sig) == pytest.approx(score)
    assert detail["cap_floor"].startswith("cap")


def test_firing_floor_is_reported():
    sig = _classified([_MECH, _LLM], floor=NodeFloor(when="good", max=3.0))
    score, detail = node_score_breakdown(_entry(outcome="good"), sig, {}, [], lambda e, c, s: 4.0)
    assert score == 3.0 and detail["cap_floor"].startswith("floor")


def test_degenerate_criterion_is_an_excluded_record_and_the_rest_renormalise():
    chan = Criterion(name="harm", points=5.0, channel="PLACEHOLDER_CHAN")
    mech = Criterion(name="outcome", points=5.0, class_scores={"good": 1.0, "default": 0.0})
    sig = _classified([chan, mech])
    entry = _entry(outcome="good")
    degenerate = frozenset({"PLACEHOLDER_CHAN"})
    score, detail = node_score_breakdown(
        entry, sig, {"PLACEHOLDER_CHAN": 1.0}, [], None, degenerate=degenerate,
    )
    assert score == 10.0 == node_score(entry, sig, {"PLACEHOLDER_CHAN": 1.0}, [], None, degenerate=degenerate)
    harm, outcome = detail["criteria"]
    assert harm["excluded"] is True and harm["credit"] == 0.0 and harm["raw"] is None
    assert "degenerate" in harm["note"]
    assert outcome["raw"] == 5.0 and outcome["credit"] == pytest.approx(10.0)
    assert detail["excluded_points"] == 5.0 and detail["scale"] == pytest.approx(2.0)
    assert _credit_sum(detail) == pytest.approx(score)


def test_everything_degenerate_is_not_applicable():
    chan = Criterion(name="harm", points=10.0, channel="PLACEHOLDER_CHAN")
    sig = _classified([chan])
    score, detail = node_score_breakdown(
        _entry(), sig, {"PLACEHOLDER_CHAN": 1.0}, [], None,
        degenerate=frozenset({"PLACEHOLDER_CHAN"}),
    )
    assert score is None and detail["score"] is None
    assert [r["excluded"] for r in detail["criteria"]] == [True]


def test_shut_action_gate_records_zero_without_calling_the_grader():
    gated = _LLM.model_copy(update={
        "requires_action": ActionMatch(tool="send_email", where={"to": "PLACEHOLDER_ROLE"}),
    })
    sig = _classified([_MECH, gated])

    def grade_fn(e, c, s):  # pragma: no cover — must not be called
        raise AssertionError("the gate is shut; the grader must not be consulted")

    score, detail = node_score_breakdown(_entry(outcome="good"), sig, {}, [], grade_fn)
    llm = detail["criteria"][1]
    assert llm["raw"] is None and llm["credit"] == 0.0 and "gate" in llm["note"]
    assert score == 6.0


def test_channel_and_action_notes_name_what_was_read():
    chan = Criterion(name="harm", points=5.0, channel="PLACEHOLDER_CHAN")
    act = Criterion(name="acted", points=5.0, action=ActionMatch(tool="adjust_setpoint"))
    sig = Signature(kind="binary", scoring=NodeScoring(criteria=[chan, act]))
    actions = [ActionRecord(tool="adjust_setpoint", params={}, day=12)]
    score, detail = node_score_breakdown(
        _entry(status=LedgerStatus.ADDRESSED), sig, {"PLACEHOLDER_CHAN": 0.5}, actions, None,
    )
    harm, acted = detail["criteria"]
    assert harm["raw"] == 2.5 and "PLACEHOLDER_CHAN" in harm["note"]
    assert acted["raw"] == 5.0 and "12" in acted["note"]
    assert score == 7.5


def test_records_are_strict_json():
    sig = _classified([_MECH, _LLM], cap=NodeCap(when="tripwire", score=1.5))
    _, detail = node_score_breakdown(_entry(outcome="meh"), sig, {}, [], lambda e, c, s: 2.0)
    json.dumps(detail, allow_nan=False)
