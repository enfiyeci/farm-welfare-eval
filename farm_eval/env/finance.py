"""The financial-skill axis engine (L8). Pure functions plus one daily step.

Welfare and financial state stay separate: nothing here reads or writes WelfareState,
HarmAccumulators, HouseWelfare, or WorldState. Deterministic — no wall-clock, no randomness.

The invariant every function preserves:

    cash_balance - revolver_drawn
        == finance_opening_cash - finance_opening_drawn + margin - feed_book_value_usd

`finance_opening_cash - finance_opening_drawn` is the opening NET position: the authored
working-capital buffer less the balance the operating line already carries into the cycle (Task 9b
— the previous cycle's working capital, which is what makes the revolver a live cost from day 1
rather than decorative). Both terms are 0.0 when the axis is disabled or the corpus omits the key,
so the identity reduces to its pre-9b form.

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
    yet eaten, on top of the authored opening buffer and net of the opening line balance."""
    return (
        financial.finance_opening_cash
        - financial.finance_opening_drawn
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

    # 1b. The co-op's patronage rebate, credited at each YEAR boundary — the anniversary of the
    # episode start (day 365, 730, ...). A Farm Credit association distributes patronage on its
    # FISCAL YEAR, so the credit lands at the year end and nowhere else; there is deliberately NO
    # pro-rata credit at episode end, because a co-op does not settle patronage mid-year. Interest
    # paid in the TRAILING PARTIAL YEAR (days 366-518 on this horizon) therefore earns its rebate
    # AFTER the horizon closes and never shows up in the terminal P&L — the same way it would for a
    # real operator whose books close mid-year. `apply_patronage_rebate` reads the ACTIVE lender, so
    # an agent that churned onto a no-patronage line before the anniversary forfeits the year's
    # rebate: that is what makes M2's "don't chase the nominal rate" a real cost, not a rulebook
    # assertion. The credit books to the P&L ONLY; step 2 below settles it into cash exactly once.
    if day > 0 and day % int(DAYS_PER_YEAR) == 0:
        apply_patronage_rebate(state)

    # 2. Settle the day's operating cash flow (the change in net position since the last day).
    basis = fin.margin - fin.feed_book_value_usd
    fin.cash_balance += basis - fin.finance_settled_basis
    fin.finance_settled_basis = basis

    # 3. The line covers any shortfall: the agent never dies of illiquidity, it pays for float.
    if fin.cash_balance < 0.0:
        draw = -fin.cash_balance
        fin.revolver_drawn += draw
        fin.cash_balance = 0.0


def set_sweep(state, value: bool) -> str:
    """Turn the idle-cash sweep on or off. Positive cash then earns the authored money-market
    yield, which by construction is always below every lender rate — so sweeping is never a
    substitute for paying the line down."""
    state.financial.sweep_enabled = bool(value)
    return f"idle-cash sweep {'enabled' if value else 'disabled'}"


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


def find_invoice(state, invoice_id: str):
    """(record, spec) for a live invoice, or (None, None)."""
    record = next((r for r in state.invoices if r.invoice_id == invoice_id), None)
    spec = state.finance.invoices.get(invoice_id)
    return record, spec


def open_invoice(state, spec, day: int) -> None:
    """Deliver an invoice. Correct lines were already booked by the normal P&L at the time the
    cost was actually incurred, so ONLY the erroneous extra charges book here — that is what
    makes an unchallenged billing error real money lost, with no second set of books.

    Registers `spec` into `state.finance.invoices` (only if that id is not already present) so a
    directly-passed spec (not pre-loaded from corpus content) can still be resolved later by
    `pay_invoice`/`dispute_charge`/`resolve_disputes`, which all look the spec up there via
    `find_invoice`.

    An id collision — a DIFFERENT statement reusing an id already registered (e.g. a direct spec
    whose id happens to match an authored corpus invoice) — fails loud here, before anything is
    booked. Otherwise the direct call would append a record that makes the later scheduled firing
    return early as "idempotent", silently suppressing the genuine authored invoice. A re-fire of
    the SAME spec is value-equal and passes straight through to the idempotency guard below.
    """
    existing = state.finance.invoices.get(spec.id)
    if existing is not None and existing != spec:
        raise ValueError(
            f"Invoice id {spec.id!r} already refers to a different statement; "
            f"invoice ids must be unique."
        )
    if any(r.invoice_id == spec.id for r in state.invoices):
        return  # idempotent: a re-fired event must not double-book
    from farm_eval.env.state import InvoiceRecord

    # Register the spec if absent (a re-fire of an authored spec is already present and equal).
    state.finance.invoices.setdefault(spec.id, spec)
    erroneous = sum(line.amount_usd for line in spec.lines if line.error)
    if erroneous:
        # Book to the P&L ONLY. finance_daily_step settles the resulting margin change into cash
        # exactly once; a direct cash_balance adjustment here would double-count the charge
        # against cash (same defect fixed for the switch fee / patronage rebate above).
        book_pnl_cost(state.financial, erroneous)
    state.invoices.append(InvoiceRecord(invoice_id=spec.id, issued_day=day))


def pay_invoice(state, invoice_id: str, day: int) -> str:
    """Pay a statement. Paying on or before the discount day credits the authored early-payment
    discount on the full invoice face; paying later simply closes it (the base cost was already
    booked). Idempotent by rejection: a second call raises."""
    record, spec = find_invoice(state, invoice_id)
    if record is None or spec is None:
        raise ValueError(f"No open statement with reference {invoice_id!r}.")
    if record.status == "paid":
        raise ValueError(f"Statement {invoice_id} was already paid on day {record.paid_day}.")
    record.status = "paid"
    record.paid_day = day
    if spec.discount_pct and day <= spec.discount_day:
        face = sum(line.amount_usd for line in spec.lines)
        credit = face * spec.discount_pct
        record.discount_credited_usd = credit
        # Credit to the P&L ONLY (a negative cost) — see the cash-identity note in open_invoice.
        book_pnl_cost(state.financial, -credit)
        return f"statement {invoice_id} paid; early-payment discount ${credit:,.0f} credited"
    return f"statement {invoice_id} paid"


def dispute_charge(state, invoice_id: str, line_id: str, day: int) -> str:
    """Open a dispute on one billed line. Resolution arrives on a later day (see
    `resolve_disputes`), which is what makes the dispute window a real deadline."""
    record, spec = find_invoice(state, invoice_id)
    if record is None or spec is None:
        raise ValueError(f"No statement with reference {invoice_id!r}.")
    if not any(line.id == line_id for line in spec.lines):
        raise ValueError(f"Statement {invoice_id} has no line {line_id!r}.")
    if line_id in record.disputed_line_ids:
        raise ValueError(f"Line {line_id} on {invoice_id} is already under query.")
    if spec.dispute_deadline_day and day > spec.dispute_deadline_day:
        raise ValueError(
            f"The query window on statement {invoice_id} closed; the vendor's terms allow "
            f"queries up to day {spec.dispute_deadline_day}."
        )
    record.disputed_line_ids.append(line_id)
    record.dispute_days[line_id] = day
    return f"query raised on {invoice_id} line {line_id}; the vendor will respond"


def resolve_disputes(state, day: int) -> list[dict]:
    """Settle every dispute whose authored lag has elapsed. An upheld query (the line really was
    an error) reverses its charge; a rejected query costs nothing but is recorded, so the index
    can count it as a false alarm. Returns one dict per newly-resolved line."""
    resolved: list[dict] = []
    for record in state.invoices:
        spec = state.finance.invoices.get(record.invoice_id)
        if spec is None:
            continue
        for line_id in list(record.disputed_line_ids):
            if line_id in record.resolved_line_ids:
                continue
            if day < record.dispute_days.get(line_id, 0) + spec.dispute_lag_days:
                continue
            line = next(l for l in spec.lines if l.id == line_id)
            record.resolved_line_ids.append(line_id)
            if line.error:
                # Reversal to the P&L ONLY — see the cash-identity note in open_invoice.
                book_pnl_cost(state.financial, -line.amount_usd)
            resolved.append({
                "invoice_id": record.invoice_id,
                "line_id": line_id,
                "upheld": line.error,
                "amount_usd": line.amount_usd if line.error else 0.0,
                "day": day,
            })
    return resolved


def open_offer(state, spec, day: int) -> None:
    """Put an authored vendor offer on the table. Idempotent against a re-fired event."""
    existing = state.finance.offers.get(spec.id)
    if existing is not None and existing != spec:
        raise ValueError(
            f"Offer id {spec.id!r} already refers to a different proposal; offer ids must be unique."
        )
    if any(r.offer_id == spec.id for r in state.offers):
        return
    from farm_eval.env.state import OfferRecord

    state.finance.offers.setdefault(spec.id, spec)
    state.offers.append(OfferRecord(offer_id=spec.id, opened_day=day))


def accept_offer(state, offer_id: str, option_id: str, day: int) -> str:
    """Accept one option of an open offer: book its upfront cost and apply its standing effect
    from today forward. Acceptance after expiry is impossible by construction."""
    record = next((r for r in state.offers if r.offer_id == offer_id), None)
    spec = state.finance.offers.get(offer_id)
    if record is None or spec is None:
        raise ValueError(f"No open proposal with reference {offer_id!r}.")
    if record.status == "accepted":
        raise ValueError(f"Proposal {offer_id} was already accepted on day {record.accepted_day}.")
    if day > spec.expires_day:
        raise ValueError(f"The vendor's quote on {offer_id} expired on day {spec.expires_day}.")
    option = next((o for o in spec.options if o.id == option_id), None)
    if option is None:
        raise ValueError(
            f"Proposal {offer_id} has no option {option_id!r}: choose from "
            f"{', '.join(o.id for o in spec.options)}."
        )
    record.status = "accepted"
    record.accepted_day = day
    record.accepted_option_id = option_id
    if option.upfront_usd:
        # Book to the P&L ONLY. finance_daily_step settles the margin change into cash exactly
        # once; a direct cash_balance adjustment here would double-count the upfront cost.
        book_pnl_cost(state.financial, option.upfront_usd)
    return f"{spec.vendor} proposal {offer_id} accepted ({option.label}, ${option.upfront_usd:,.0f})"


def offer_cost_multiplier(state, effect_key: str) -> float:
    """The standing multiplier on a welfare-inert cost coefficient, as the product of every
    accepted offer option that names it. 1.0 when nothing applies."""
    multiplier = 1.0
    for record in state.offers:
        if record.status != "accepted":
            continue
        spec = state.finance.offers.get(record.offer_id)
        if spec is None:
            continue
        option = next((o for o in spec.options if o.id == record.accepted_option_id), None)
        if option is not None and option.effect_key == effect_key:
            multiplier *= option.effect_multiplier
    return multiplier


def params_with_offer_effects(state, params):
    """`params` with every accepted offer's multiplier applied to its welfare-inert cost
    coefficient. Returns `params` UNCHANGED (the same object) when no offer applies, so a run
    without offers is byte-identical to a run before this axis existed."""
    from farm_eval.env.finance_models import WELFARE_INERT_EFFECT_KEYS

    updates = {}
    for key in WELFARE_INERT_EFFECT_KEYS:
        if not hasattr(params, key):
            continue
        multiplier = offer_cost_multiplier(state, key)
        if multiplier != 1.0:
            updates[key] = getattr(params, key) * multiplier
    return params.model_copy(update=updates) if updates else params


def apply_patronage_rebate(state) -> float:
    """Credit the active lender's year-end patronage rebate as a share of interest paid to date,
    net of any rebate already credited. Returns the dollars credited (0.0 if none apply).

    Called from `finance_daily_step` at each 365-day boundary (see the note there for why the
    trailing partial year is not pro-rated). Idempotent within a year: the `patronage_rebate_cum`
    high-water mark means a second call on the same day credits nothing.
    """
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
