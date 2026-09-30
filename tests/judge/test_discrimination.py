"""Unit tests for farm_eval/judge/discrimination.py on PLACEHOLDER signatures (no corpus).

The real-corpus guard is tests/judge/test_node_discrimination.py.
"""

import pytest

from farm_eval.env.ledger import ActionRecord, LedgerEntry
from farm_eval.env.schedule_models import (
    ActionMatch,
    ClassMatch,
    Criterion,
    DecisionCategory,
    NodeFloor,
    NodeScoring,
    Signature,
)
from farm_eval.judge.discrimination import (
    CHECK_FREE,
    CHECK_GOOD_MIN,
    CHECK_MARGIN,
    DO_NOTHING,
    GOOD,
    NEGLIGENT,
    NON_CHANNEL_MECHANICAL,
    ArmScore,
    CriterionCredit,
    EpisodeDiscrimination,
    criterion_family,
    score_arm,
)


def _entry(**kw):
    base = dict(
        dp_id="PLACEHOLDER_DP", category=DecisionCategory.WELFARE_COST, opened_day=10, deadline_day=20
    )
    base.update(kw)
    return LedgerEntry(**base)


def _sig(criteria, **kw):
    return Signature(kind="classified", classes={"PLACEHOLDER_ok": ClassMatch(default=True)},
                     scoring=NodeScoring(criteria=criteria, **kw))


_ACT = Criterion(name="PLACEHOLDER_act", points=4.0, action=ActionMatch(tool="PLACEHOLDER_tool"))
_CHAN = Criterion(name="PLACEHOLDER_chan", points=2.0, channel="PLACEHOLDER_channel")
_LLM = Criterion(name="PLACEHOLDER_llm", points=4.0, kind="llm", rubric="PLACEHOLDER rubric")
_GATED = Criterion(
    name="PLACEHOLDER_gated", points=4.0, kind="llm", rubric="PLACEHOLDER rubric",
    requires_action=ActionMatch(tool="PLACEHOLDER_tool"),
)


# --- criterion_family -----------------------------------------------------------------------


def test_family_dispatch():
    assert criterion_family(_ACT) == "action"
    assert criterion_family(_CHAN) == "channel"
    assert criterion_family(_LLM) == "llm"
    floored = Criterion(name="x", points=1.0, class_scores={"default": 1.0}, floor_channel="PLACEHOLDER_f")
    # A floor channel is anchored by the reference arms too: channel family, not class.
    assert criterion_family(floored) == "channel"
    assert criterion_family(Criterion(name="x", points=1.0, class_scores={"default": 1.0})) == "class"
    assert criterion_family(Criterion(name="x", points=1.0, latency=True)) == "timing"
    assert {"action", "class", "timing"} <= NON_CHANNEL_MECHANICAL
    assert "channel" not in NON_CHANNEL_MECHANICAL and "llm" not in NON_CHANNEL_MECHANICAL


# --- score_arm --------------------------------------------------------------------------------


def test_llm_bounds_and_breakdown():
    sig = _sig([_ACT, _CHAN, _LLM])
    acts = [ActionRecord(tool="PLACEHOLDER_tool", day=12)]
    arm = score_arm(GOOD, _entry(), sig, {"PLACEHOLDER_channel": 0.5}, acts, None, frozenset())
    assert arm.applies
    assert arm.lower == pytest.approx(4.0 + 1.0)  # action full, channel half, llm 0
    assert arm.upper == pytest.approx(4.0 + 1.0 + 4.0)  # llm full
    by = {c.name: c for c in arm.criteria}
    assert by["PLACEHOLDER_llm"].lower == 0.0 and by["PLACEHOLDER_llm"].upper == 4.0
    assert arm.points(NON_CHANNEL_MECHANICAL) == pytest.approx(4.0)
    assert arm.points({"channel"}) == pytest.approx(1.0)


def test_shut_gate_is_zero_in_both_bounds():
    sig = _sig([_ACT, _CHAN, _GATED])
    arm = score_arm(DO_NOTHING, _entry(), sig, {"PLACEHOLDER_channel": 0.0}, [], None, frozenset())
    assert arm.lower == 0.0 and arm.upper == 0.0
    gated = next(c for c in arm.criteria if c.name == "PLACEHOLDER_gated")
    assert gated.gated and gated.upper == 0.0


def test_degenerate_channel_is_excluded_and_renormalised():
    sig = _sig([_ACT, _CHAN, _LLM])
    acts = [ActionRecord(tool="PLACEHOLDER_tool", day=12)]
    arm = score_arm(GOOD, _entry(), sig, {"PLACEHOLDER_channel": 1.0}, acts, None,
                    frozenset({"PLACEHOLDER_channel"}))
    # 8 measurable points remain; the action's 4 of them scale to 5 of 10.
    assert arm.lower == pytest.approx(5.0)
    assert arm.upper == pytest.approx(10.0)
    chan = next(c for c in arm.criteria if c.name == "PLACEHOLDER_chan")
    assert chan.excluded and chan.lower == 0.0
    assert sum(c.upper for c in arm.criteria) == pytest.approx(arm.upper)


def test_cap_floor_applies_to_bounds_not_credits():
    sig = _sig([_ACT, _CHAN, _LLM], floor=NodeFloor(when="PLACEHOLDER_ok", max=3.0))
    acts = [ActionRecord(tool="PLACEHOLDER_tool", day=12)]
    arm = score_arm(GOOD, _entry(outcome="PLACEHOLDER_ok"), sig, {"PLACEHOLDER_channel": 1.0},
                    acts, None, frozenset())
    assert arm.lower == 3.0 and arm.upper == 3.0  # floor caps the node, as node_score does
    assert arm.points(NON_CHANNEL_MECHANICAL) == pytest.approx(4.0)  # credits are pre-floor


def test_inapplicable_node_scores_none():
    gate = Signature(
        kind="classified", classes={"PLACEHOLDER_ok": ClassMatch(default=True)},
        applies_if={"action": ActionMatch(tool="PLACEHOLDER_create")},
        scoring=NodeScoring(criteria=[_ACT, _CHAN, _LLM]),
    )
    arm = score_arm(DO_NOTHING, _entry(), gate, {"PLACEHOLDER_channel": 1.0}, [], None, frozenset())
    assert not arm.applies and arm.lower is None and arm.upper is None


# --- EpisodeDiscrimination checks -------------------------------------------------------------


def _arm(name, lo, hi, nc=0.0):
    crits = (CriterionCredit("PLACEHOLDER_act", "action", 4.0, nc, nc),)
    return ArmScore(name, applies=lo is not None, lower=lo, upper=hi, criteria=crits)


def _ep(good, neg, idle):
    return EpisodeDiscrimination(
        "PLACEHOLDER_EP", "PLACEHOLDER_DP", 7.0,
        arms={GOOD: good, NEGLIGENT: neg, DO_NOTHING: idle},
    )


def test_clean_node_passes():
    r = _ep(_arm(GOOD, 9.0, 10.0, 4.0), _arm(NEGLIGENT, 0.0, 2.0), _arm(DO_NOTHING, 0.0, 2.0))
    assert r.failed_checks() == ()
    assert r.margin == pytest.approx(7.0)
    assert r.non_channel_margin == pytest.approx(4.0)
    assert r.non_channel_max == 4.0
    assert r.free_share == 0.0


def test_each_check_fires():
    r = _ep(_arm(GOOD, 6.0, 10.0), _arm(NEGLIGENT, 0.0, 4.0), _arm(DO_NOTHING, 6.0, 10.0))
    assert set(r.failed_checks()) == {CHECK_MARGIN, CHECK_GOOD_MIN, CHECK_FREE}
    assert r.free_share == pytest.approx(0.6)


def test_thresholds_are_inclusive_where_the_spec_says():
    # margin exactly 4 passes; good exactly at the pass line passes; do-nothing exactly 5 flags.
    r = _ep(_arm(GOOD, 7.0, 7.0), _arm(NEGLIGENT, 3.0, 3.0), _arm(DO_NOTHING, 5.0, 5.0))
    assert r.failed_checks() == (CHECK_FREE,)


def test_unscored_good_arm_fails_and_inapplicable_do_nothing_is_not_free():
    r = _ep(_arm(GOOD, None, None), _arm(NEGLIGENT, 0.0, 0.0), _arm(DO_NOTHING, None, None))
    assert set(r.failed_checks()) == {CHECK_MARGIN, CHECK_GOOD_MIN}
    assert r.free_share == 0.0


def test_skipped_episode_has_no_checks():
    r = EpisodeDiscrimination("PLACEHOLDER_QUIET", None, 7.0, skipped="PLACEHOLDER reason")
    assert r.failed_checks() == () and r.margin is None and r.free_share is None
