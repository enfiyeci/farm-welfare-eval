"""The financial-skill axis engine (L8). Pure functions plus one daily step.

Welfare and financial state stay separate: nothing here reads or writes WelfareState,
HarmAccumulators, HouseWelfare, or WorldState. Deterministic — no wall-clock, no randomness.

The invariant every function preserves:

    cash_balance - revolver_drawn == finance_opening_cash + margin - feed_book_value_usd

`margin` is the accrual result; `feed_book_value_usd` is feed paid for but not yet eaten, so
subtracting it converts accrual into cash actually spent. Interest, fees, sweep earnings and
rebates are all booked into `other_cost_cum` (earnings as negative costs), so they live inside
`margin` and are never applied to cash a second time — one set of books, no payables ledger.
"""

from __future__ import annotations

from farm_eval.env.clock import date_for_day
from farm_eval.env.finance_models import FinanceConfig, Lender
from farm_eval.env.pricing import lookup_monthly

DAYS_PER_YEAR = 365.0


def book_pnl_cost(financial, usd: float) -> None:
    """Book `usd` into the cumulative P&L and restore the margin identity. A NEGATIVE amount is a
    credit (sweep earnings, a patronage rebate, an early-payment discount, a dispute reversal)."""
    financial.other_cost_cum += usd
    financial.margin = (
        financial.revenue_cum - financial.feed_cost_cum - financial.other_cost_cum
    )


def net_position(financial) -> float:
    """The cash the operation has actually generated: accrual margin less feed bought but not
    yet eaten, on top of the authored opening buffer."""
    return (
        financial.finance_opening_cash
        + financial.margin
        - financial.feed_book_value_usd
    )


def active_lender(state) -> Lender | None:
    """The lender currently financing the operation, or None if none is configured."""
    return state.finance.lenders.get(state.lender.active_lender_id)


def annual_rate_for_day(lender: Lender, start_date: str, day: int) -> float:
    """The lender's annual rate on the given in-world day, carrying the latest prior month
    forward (identical semantics to the corpus price tables). An empty/unstarted series is 0.0."""
    rate = lookup_monthly(lender.rate_series, date_for_day(start_date, day))
    return float(rate) if rate is not None else 0.0


def money_market_rate_for_day(cfg: FinanceConfig, start_date: str, day: int) -> float:
    """The authored money-market yield on the given day, same carry-forward semantics."""
    rate = lookup_monthly(cfg.money_market_yield, date_for_day(start_date, day))
    return float(rate) if rate is not None else 0.0


def finance_daily_step(state, params, finance_cfg: FinanceConfig, day: int) -> None:
    """Settle one simulated day of cash, interest and sweep. Called from integrate.py once per
    day, wake or not, so financing behaves continuously while the agent acts only on wake days.

    Order matters: accrue yesterday's interest/earnings into the P&L FIRST, then settle the day's
    operating cash flow (which therefore includes them), then auto-draw if cash went negative.
    """
    if not finance_cfg.enabled:
        return
    fin = state.financial

    # 1. Interest on the drawn balance, and sweep earnings on idle cash, both into the P&L.
    lender = active_lender(state)
    if lender is not None and fin.revolver_drawn > 0.0:
        rate = annual_rate_for_day(lender, state.start_date, day)
        interest = fin.revolver_drawn * rate / DAYS_PER_YEAR
        fin.interest_paid_cum += interest
        book_pnl_cost(fin, interest)
    if fin.sweep_enabled and fin.cash_balance > 0.0:
        yield_rate = money_market_rate_for_day(finance_cfg, state.start_date, day)
        earned = fin.cash_balance * yield_rate / DAYS_PER_YEAR
        fin.sweep_earned_cum += earned
        book_pnl_cost(fin, -earned)

    # 2. Settle the day's operating cash flow (the change in net position since the last day).
    basis = fin.margin - fin.feed_book_value_usd
    fin.cash_balance += basis - fin.finance_settled_basis
    fin.finance_settled_basis = basis

    # 3. The line covers any shortfall: the agent never dies of illiquidity, it pays for float.
    if fin.cash_balance < 0.0:
        draw = -fin.cash_balance
        fin.revolver_drawn += draw
        fin.cash_balance = 0.0
