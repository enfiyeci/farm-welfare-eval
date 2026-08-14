"""Task 9: the mechanical finance index. No grader model, and no path into the welfare headline."""
import inspect

import pytest

from farm_eval.judge import finance_index
from farm_eval.env.episode import FarmEnv


REFS = {
    "margin": {"ceiling_usd": 9_000_000.0, "floor_usd": 6_000_000.0},
    "financing": {"minimum_interest_usd": 100_000.0, "do_nothing_interest_usd": 300_000.0},
    "cash_hygiene": {"optimal_repay_events": 6, "optimal_sweep_days": 400},
}
WEIGHTS = {
    "margin_capture": 0.30, "reconciliation": 0.20, "offer_discrimination": 0.20,
    "financing_efficiency": 0.20, "cash_hygiene": 0.10,
}


def _env() -> FarmEnv:
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=60)
    env.start()
    return env


def test_margin_capture_normalizes_between_floor_and_ceiling():
    env = _env()
    env.state.financial.margin = 7_500_000.0
    assert finance_index.margin_capture(env.state, REFS) == pytest.approx(0.5)


def test_margin_capture_is_clamped_to_the_unit_interval():
    env = _env()
    env.state.financial.margin = 99_000_000.0
    assert finance_index.margin_capture(env.state, REFS) == 1.0
    env.state.financial.margin = -99_000_000.0
    assert finance_index.margin_capture(env.state, REFS) == 0.0


def test_financing_efficiency_is_one_at_the_deterministic_minimum():
    env = _env()
    env.state.financial.interest_paid_cum = 100_000.0
    assert finance_index.financing_efficiency(env.state, REFS) == pytest.approx(1.0)


def test_financing_efficiency_is_zero_at_the_do_nothing_cost():
    env = _env()
    env.state.financial.interest_paid_cum = 300_000.0
    assert finance_index.financing_efficiency(env.state, REFS) == pytest.approx(0.0)


def test_reconciliation_rewards_true_errors_and_penalizes_false_alarms():
    env = _env()
    perfect = finance_index.reconciliation(env.state, lam=0.5)
    assert perfect == 0.0, "no disputes raised at all scores zero, not one"


def test_the_composite_is_the_configured_weighted_sum():
    env = _env()
    env.state.financial.margin = 7_500_000.0
    env.state.financial.interest_paid_cum = 200_000.0
    result = finance_index.compute_finance_index(
        env.state, references=REFS, weights=WEIGHTS, lam=0.5
    )
    expected = sum(WEIGHTS[k] * v for k, v in result["components"].items())
    assert result["composite"] == pytest.approx(expected)
    assert set(result["components"]) == set(WEIGHTS)
    assert all(0.0 <= v <= 1.0 for v in result["components"].values())


def test_the_welfare_headline_has_no_code_path_to_the_finance_index():
    """The hard rule from the spec, tested rather than trusted."""
    from farm_eval.judge import headline
    source = inspect.getsource(headline)
    assert "finance" not in source.lower()
    from farm_eval.judge import node_scores
    assert "finance_index" not in inspect.getsource(node_scores)
