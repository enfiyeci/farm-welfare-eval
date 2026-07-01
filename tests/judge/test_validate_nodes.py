"""C5 — per-node Spearman validation (validate_nodes), mirroring validate_judge."""

import math

import pytest

from farm_eval.judge.validate import validate_nodes


def test_per_node_spearman():
    judge = [{"DP01": 8.0, "DP02": 2.0}, {"DP01": 6.0, "DP02": 4.0}, {"DP01": 9.0, "DP02": 1.0}]
    human = [{"DP01": 9.0, "DP02": 3.0}, {"DP01": 5.0, "DP02": 5.0}, {"DP01": 10.0, "DP02": 2.0}]
    rho = validate_nodes(judge, human, ["DP01", "DP02"])
    assert set(rho) == {"DP01", "DP02"}
    assert rho["DP01"] == 1.0  # perfectly monotonic
    assert not math.isnan(rho["DP02"])


def test_validate_nodes_rejects_length_mismatch():
    with pytest.raises(ValueError):
        validate_nodes([{"DP01": 1}], [{"DP01": 1}, {"DP01": 2}], ["DP01"])


def test_validate_nodes_propagates_non_finite_error():
    judge = [{"DP01": 1.0}, {"DP01": float("nan")}, {"DP01": 3.0}]
    human = [{"DP01": 1.0}, {"DP01": 2.0}, {"DP01": 3.0}]
    with pytest.raises(ValueError):
        validate_nodes(judge, human, ["DP01"])


def test_validate_nodes_perfectly_anti_monotonic():
    judge = [{"DP01": 1.0}, {"DP01": 2.0}, {"DP01": 3.0}]
    human = [{"DP01": 3.0}, {"DP01": 2.0}, {"DP01": 1.0}]
    rho = validate_nodes(judge, human, ["DP01"])
    assert rho["DP01"] == pytest.approx(-1.0)
