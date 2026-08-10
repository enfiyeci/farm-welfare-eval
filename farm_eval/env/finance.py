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


def select_lender(state, lender_id: str, day: int) -> str:
    """Switch the operating line to `lender_id`, booking the OUTGOING lender's switch fee at the
    moment of the switch. Raises ValueError on an unknown id or a no-op re-selection — the caller
    turns that into an in-world rejection."""
    if lender_id not in state.finance.lenders:
        raise ValueError(f"No operating line is available from {lender_id!r}.")
    if lender_id == state.lender.active_lender_id:
        raise ValueError(f"The operating line is already with {lender_id!r}.")
    outgoing = active_lender(state)
    fee = outgoing.switch_fee_usd if outgoing is not None else 0.0
    state.lender.active_lender_id = lender_id
    state.lender.switch_days.append(day)
    if fee:
        state.lender.switch_fees_cum += fee
        # Book the fee to the P&L ONLY. finance_daily_step settles the resulting margin change
        # into cash exactly once (drawing on the line if cash is short). Do NOT also subtract the
        # fee from cash_balance here: the next daily step re-settles the margin drop, so a direct
        # adjustment double-counts the fee against cash and breaks the load-bearing cash identity.
        book_pnl_cost(state.financial, fee)
    incoming = state.finance.lenders[lender_id]
    rate = annual_rate_for_day(incoming, state.start_date, day)
    return f"operating line moved to {incoming.name} at {rate * 100:.2f}% (switch fee ${fee:,.0f})"


def repay(state, amount: float) -> str:
    """Pay down the drawn balance from cash on hand. Clamped to both cash and the balance — an
    over-large request pays what it can rather than failing, the way a real payment does. Raises
    ValueError on a non-positive / non-finite amount."""
    import math

    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("Repayment amount must be a positive number of dollars.")
    fin = state.financial
    paid = min(amount, fin.cash_balance, fin.revolver_drawn)
    fin.cash_balance -= paid
    fin.revolver_drawn -= paid
    return f"paid down ${paid:,.0f}; line balance now ${fin.revolver_drawn:,.0f}"


def apply_patronage_rebate(state) -> float:
    """Credit the active lender's year-end patronage rebate as a share of interest paid to date,
    net of any rebate already credited. Returns the dollars credited (0.0 if none apply)."""
    lender = active_lender(state)
    if lender is None or not lender.patronage_rebate_frac:
        return 0.0
    earned = state.financial.interest_paid_cum * lender.patronage_rebate_frac
    credited = earned - state.lender.patronage_rebate_cum
    if credited <= 0:
        return 0.0
    state.lender.patronage_rebate_cum += credited
    # Credit the rebate to the P&L ONLY (a negative cost). finance_daily_step settles it into cash
    # exactly once; adding it to cash_balance here as well would credit the rebate twice and break
    # the cash identity (same double-count as the switch fee above).
    book_pnl_cost(state.financial, -credited)
    return credited
