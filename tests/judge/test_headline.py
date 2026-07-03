"""Tests for farm_eval.judge.headline: pure aggregation helpers.

Phase C5 headline = equal-per-decision mean of node scores. This module also
provides stakeholder and category breakouts, and a stakeholder-balanced
aggregate. All functions are pure (no I/O, no farm content hardcoded).
"""
import math

import pytest

from farm_eval.judge.headline import (
    category_breakout,
    stakeholder_balanced,
    stakeholder_breakout,
    welfare_headline,
)

NODES = {"A": 10.0, "B": 0.0, "C": 6.0}
STK = {"A": ["animal", "worker"], "B": ["animal"], "C": ["consumer"]}
CAT = {"A": "welfare_cost", "B": "welfare_cost", "C": "integrity"}


class TestWelfareHeadline:
    def test_headline_is_plain_mean(self):
        assert welfare_headline(NODES) == pytest.approx((10.0 + 0.0 + 6.0) / 3)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            welfare_headline({})

    def test_nan_node_score_raises(self):
        with pytest.raises(ValueError):
            welfare_headline({"A": 10.0, "B": float("nan")})

    def test_inf_node_score_raises(self):
        with pytest.raises(ValueError):
            welfare_headline({"A": 10.0, "B": float("inf")})


class TestStakeholderBreakout:
    def test_dual_tag_node_counts_in_both(self):
        result = stakeholder_breakout(NODES, STK)
        assert result["animal"] == pytest.approx((10.0 + 0.0) / 2)
        assert result["worker"] == pytest.approx(10.0)
        assert result["consumer"] == pytest.approx(6.0)

    def test_node_missing_from_stakeholders_contributes_to_nothing(self):
        nodes = {"A": 10.0, "B": 0.0, "D": 5.0}
        stk = {"A": ["animal"], "B": ["animal"]}
        result = stakeholder_breakout(nodes, stk)
        assert set(result.keys()) == {"animal"}
        assert result["animal"] == pytest.approx(5.0)

    def test_node_with_empty_tag_list_contributes_to_nothing(self):
        nodes = {"A": 10.0, "B": 0.0}
        stk = {"A": ["animal"], "B": []}
        result = stakeholder_breakout(nodes, stk)
        assert result == {"animal": pytest.approx(10.0)}

    def test_nan_node_score_raises(self):
        nodes = {"A": float("nan"), "B": 0.0}
        stk = {"A": ["animal"], "B": ["animal"]}
        with pytest.raises(ValueError):
            stakeholder_breakout(nodes, stk)

    def test_inf_node_score_raises(self):
        nodes = {"A": float("inf"), "B": 0.0}
        stk = {"A": ["animal"], "B": ["animal"]}
        with pytest.raises(ValueError):
            stakeholder_breakout(nodes, stk)

    def test_duplicate_tag_in_a_node_does_not_double_count(self):
        result = stakeholder_breakout({"A": 10.0, "B": 0.0}, {"A": ["animal", "animal"], "B": ["animal"]})
        assert result == {"animal": pytest.approx(5.0)}


class TestCategoryBreakout:
    def test_groups_correctly(self):
        result = category_breakout(NODES, CAT)
        assert result["welfare_cost"] == pytest.approx((10.0 + 0.0) / 2)
        assert result["integrity"] == pytest.approx(6.0)

    def test_nan_node_score_raises(self):
        nodes = {"A": float("nan"), "B": 0.0}
        cat = {"A": "welfare_cost", "B": "welfare_cost"}
        with pytest.raises(ValueError):
            category_breakout(nodes, cat)


class TestStakeholderBalanced:
    def test_equals_mean_of_per_tag_means(self):
        breakout = stakeholder_breakout(NODES, STK)
        result = stakeholder_balanced(breakout)
        expected = (breakout["animal"] + breakout["worker"] + breakout["consumer"]) / 3
        assert result == pytest.approx(expected)

    def test_empty_breakout_raises(self):
        with pytest.raises(ValueError):
            stakeholder_balanced({})

    def test_nan_breakout_value_raises(self):
        with pytest.raises(ValueError):
            stakeholder_balanced({"animal": 5.0, "worker": float("nan")})

    def test_inf_breakout_value_raises(self):
        with pytest.raises(ValueError):
            stakeholder_balanced({"animal": 5.0, "worker": float("inf")})
