"""B9 — judge validation: Spearman rho between judge scores and human hand-labels."""

import math

import pytest

from farm_eval.judge.validate import spearman_rho, validate_judge


def test_spearman_perfect_positive_and_negative():
    assert spearman_rho([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert spearman_rho([1, 2, 3, 4], [40, 30, 20, 10]) == pytest.approx(-1.0)


def test_spearman_is_rank_based_not_linear():
    # monotonic but non-linear -> rho is still 1.0 (rank correlation)
    assert spearman_rho([1, 2, 3, 4], [1, 4, 9, 16]) == pytest.approx(1.0)


def test_spearman_handles_ties_with_average_ranks():
    rho = spearman_rho([1, 1, 2, 3], [5, 5, 6, 7])
    assert rho == pytest.approx(1.0)


def test_spearman_rejects_mismatched_or_tiny_input():
    with pytest.raises(ValueError):
        spearman_rho([1, 2, 3], [1, 2])
    with pytest.raises(ValueError):
        spearman_rho([1], [1])


def test_validate_judge_reports_rho_per_dimension():
    judge = [
        {"welfare_decision_quality": 8, "integrity_transparency": 5},
        {"welfare_decision_quality": 6, "integrity_transparency": 7},
        {"welfare_decision_quality": 9, "integrity_transparency": 4},
        {"welfare_decision_quality": 3, "integrity_transparency": 9},
    ]
    human = [
        {"welfare_decision_quality": 9, "integrity_transparency": 4},
        {"welfare_decision_quality": 6, "integrity_transparency": 8},
        {"welfare_decision_quality": 10, "integrity_transparency": 3},
        {"welfare_decision_quality": 2, "integrity_transparency": 9},
    ]
    rho = validate_judge(judge, human, ["welfare_decision_quality", "integrity_transparency"])
    assert rho["welfare_decision_quality"] == pytest.approx(1.0)  # same ranking
    assert -1.0 <= rho["integrity_transparency"] <= 1.0
    assert not math.isnan(rho["welfare_decision_quality"])


def test_validate_judge_rejects_length_mismatch():
    with pytest.raises(ValueError):
        validate_judge([{"a": 1}], [{"a": 1}, {"a": 2}], ["a"])


def test_spearman_rejects_non_finite_inputs():
    # A blank/malformed human-label cell (NaN) must FAIL the gate, not manufacture a rank.
    with pytest.raises(ValueError):
        spearman_rho([1.0, float("nan"), 2.0], [1.0, 3.0, 2.0])
    with pytest.raises(ValueError):
        spearman_rho([1.0, 2.0, 3.0], [1.0, float("inf"), 3.0])
