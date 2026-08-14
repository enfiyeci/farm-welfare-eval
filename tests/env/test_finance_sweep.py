"""Task 3 (M3): the idle-cash sweep, and the floor it must never break."""
import pytest

from farm_eval.env import finance
from farm_eval.env.episode import FarmEnv
from farm_eval.env.model import ModelParams


def _env() -> FarmEnv:
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=30)
    env.start()
    return env


def test_sweep_toggles_on_and_off():
    env = _env()
    assert env.state.financial.sweep_enabled is False
    assert env.apply_action("set_financing", {"action": "sweep", "value": True}).ok
    assert env.state.financial.sweep_enabled is True
    assert env.apply_action("set_financing", {"action": "sweep", "value": False}).ok
    assert env.state.financial.sweep_enabled is False


def test_sweep_earns_the_authored_yield_on_idle_cash():
    env = _env()
    fin = env.state.financial
    fin.sweep_enabled = True
    fin.cash_balance = 365_000.0
    other_before = fin.other_cost_cum
    interest_before = fin.interest_paid_cum
    finance.finance_daily_step(env.state, ModelParams(), env.state.finance, day=1)
    rate = finance.money_market_rate_for_day(env.state.finance, env.state.start_date, 1)
    expected = 365_000.0 * rate / 365.0
    assert fin.sweep_earned_cum == pytest.approx(expected)
    # Earnings are booked as a NEGATIVE cost, so the margin improves. The same step books the
    # day's interest on the line (already drawn at the open since Task 9b) as a POSITIVE cost into
    # the same accumulator, so it is netted out here to keep this about the sweep alone.
    interest = fin.interest_paid_cum - interest_before
    assert fin.other_cost_cum - interest == pytest.approx(other_before - expected)


def test_sweep_earns_nothing_while_disabled():
    env = _env()
    env.state.financial.cash_balance = 365_000.0
    finance.finance_daily_step(env.state, ModelParams(), env.state.finance, day=1)
    assert env.state.financial.sweep_earned_cum == 0.0


def test_sweep_can_never_out_earn_the_cheapest_line():
    """The floor test that keeps repay-before-sweep the right move. Guarded at load
    (build_initial_state) as well; this pins the authored content itself."""
    env = _env()
    cheapest = min(
        min(lender.rate_series.values())
        for lender in env.state.finance.lenders.values()
    )
    assert max(env.state.finance.money_market_yield.values()) < cheapest


def test_repay_beats_sweep_over_the_same_dollars():
    """With cash and debt both outstanding, paying down saves more than sweeping earns."""
    env = _env()
    fin = env.state.financial
    fin.sweep_enabled = True
    fin.cash_balance = 200_000.0
    fin.revolver_drawn = 200_000.0

    swept = env.state.model_copy(deep=True)
    finance.finance_daily_step(swept, ModelParams(), swept.finance, day=1)
    swept_margin = swept.financial.margin

    repaid = env.state.model_copy(deep=True)
    finance.repay(repaid, 200_000.0)
    finance.finance_daily_step(repaid, ModelParams(), repaid.finance, day=1)
    assert repaid.financial.margin > swept_margin
