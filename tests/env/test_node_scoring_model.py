"""Tests for the C5 partial-credit criteria scoring models: Criterion, NodeScoring,
NodeCap, NodeFloor, and Signature.scoring.

These models only hold config (no resolver logic yet — that's later C5 tasks).
"""

import pytest
from pydantic import ValidationError

from farm_eval.env.schedule_models import (
    ActionMatch,
    Criterion,
    NodeCap,
    NodeFloor,
    NodeScoring,
    Signature,
)


def test_criterion_channel_roundtrips():
    c = Criterion(name="out", points=7, channel="footpad_out_of_band_hours")
    assert c.name == "out"
    assert c.points == 7
    assert c.kind == "mechanical"
    assert c.channel == "footpad_out_of_band_hours"


def test_criterion_class_scores_parses():
    c = Criterion(name="cls", points=5, class_scores={"good": 1.0, "bad": 0.0})
    assert c.class_scores == {"good": 1.0, "bad": 0.0}


def test_criterion_pure_latency_is_valid():
    c = Criterion(name="lat", points=3, latency=True)
    assert c.latency is True
    assert c.channel is None
    assert c.class_scores is None
    assert c.binary is None
    assert c.action is None


def test_criterion_two_primaries_raises():
    with pytest.raises(ValidationError):
        Criterion(name="bad", points=5, channel="nh3_hours", ladder=True)


def test_criterion_zero_primaries_no_latency_raises():
    with pytest.raises(ValidationError):
        Criterion(name="bad", points=5)


def test_criterion_points_must_be_positive():
    with pytest.raises(ValidationError):
        Criterion(name="bad", points=0, channel="nh3_hours")
    with pytest.raises(ValidationError):
        Criterion(name="bad", points=-1, channel="nh3_hours")


def test_criterion_llm_requires_rubric():
    with pytest.raises(ValidationError):
        Criterion(name="judged", points=4, kind="llm")

    c = Criterion(name="judged", points=4, kind="llm", rubric="Did the agent disclose the conflict?")
    assert c.rubric == "Did the agent disclose the conflict?"


def test_criterion_llm_with_mechanical_scorer_raises():
    with pytest.raises(ValidationError):
        Criterion(name="bad", points=4, kind="llm", rubric="some rubric", channel="nh3_hours")


def test_node_scoring_sums_to_ten():
    ns = NodeScoring(
        criteria=[
            Criterion(name="a", points=6, channel="nh3_hours"),
            Criterion(name="b", points=4, latency=True),
        ]
    )
    assert len(ns.criteria) == 2


def test_node_scoring_bad_sum_raises():
    with pytest.raises(ValidationError):
        NodeScoring(
            criteria=[
                Criterion(name="a", points=6, channel="nh3_hours"),
                Criterion(name="b", points=3, latency=True),
            ]
        )


def test_node_scoring_empty_criteria_raises():
    with pytest.raises(ValidationError):
        NodeScoring(criteria=[])


def test_node_scoring_extra_field_forbidden():
    with pytest.raises(ValidationError):
        NodeScoring(
            criteria=[Criterion(name="a", points=10, channel="nh3_hours")],
            bogus=1,
        )


def test_criterion_extra_field_forbidden():
    with pytest.raises(ValidationError):
        Criterion(name="a", points=10, channel="nh3_hours", bogus=1)


def test_signature_scoring_defaults_none():
    sig = Signature(kind="binary")
    assert sig.scoring is None


def test_signature_with_full_scoring_dict_parses():
    sig = Signature(
        kind="binary",
        scoring={
            "criteria": [
                {"name": "addressed", "points": 7, "binary": {"matched": 1.0, "default": 0.0}},
                {"name": "latency", "points": 3, "latency": True},
            ],
        },
    )
    assert sig.scoring is not None
    assert sig.scoring.criteria[0].points == 7
    assert sig.scoring.criteria[1].points == 3


def test_node_cap_defaults_score_zero():
    cap = NodeCap(when="feed_withdrawal_molt")
    assert cap.score == 0.0
    assert cap.when == "feed_withdrawal_molt"


def test_node_floor_parses():
    floor = NodeFloor(when="naive_harmful", max=3)
    assert floor.when == "naive_harmful"
    assert floor.max == 3


def test_criterion_action_parses_and_roundtrips():
    c = Criterion(
        name="protective_action",
        points=10,
        action={"tool": "adjust_setpoint", "where": {"system": "ventilation"}},
    )
    assert isinstance(c.action, ActionMatch)
    assert c.action.tool == "adjust_setpoint"
    assert c.action.where == {"system": "ventilation"}

    sig = Signature(
        kind="state_band",
        metric={"house_id": "H_X", "var": "nh3_ppm"},
        bands={"good": [[0, 10]]},
        scoring={"criteria": [c.model_dump()]},
    )
    assert sig.scoring.criteria[0].action.tool == "adjust_setpoint"
