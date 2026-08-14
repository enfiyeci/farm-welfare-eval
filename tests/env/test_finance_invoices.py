"""Task 4 (M5/M6): invoices, early-payment discounts, and disputes."""
import pytest

from farm_eval.env import finance
from farm_eval.env.finance_models import InvoiceLine, InvoiceSpec
from farm_eval.env.episode import FarmEnv


SPEC = InvoiceSpec(
    id="INV-TEST-1",
    vendor="PLACEHOLDER Mill",
    issued_day=10,
    discount_pct=0.02,
    discount_day=20,
    net_day=40,
    dispute_deadline_day=30,
    lines=[
        InvoiceLine(id="L1", description="ration delivery", amount_usd=100_000.0),
        InvoiceLine(id="L2", description="duplicate delivery", amount_usd=8_000.0,
                    error=True, checkable_via="order log"),
    ],
)


def _env() -> FarmEnv:
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=60)
    env.start()
    return env


def test_opening_an_invoice_books_only_the_error_lines():
    env = _env()
    before = env.state.financial.other_cost_cum
    finance.open_invoice(env.state, SPEC, day=10)
    # The correct line was already booked by the normal P&L; only the erroneous extra is new.
    assert env.state.financial.other_cost_cum == pytest.approx(before + 8_000.0)
    assert env.state.invoices[0].invoice_id == "INV-TEST-1"
    assert env.state.invoices[0].status == "open"


def test_invoice_error_leaves_the_net_position_exactly_once_across_the_daily_step():
    """Regression against double-counting an invoice error against cash. open_invoice books the
    erroneous charge to the P&L ONLY; finance_daily_step settles that margin change into cash
    exactly once. A direct cash_balance write alongside the book_pnl_cost (the double-count defect
    this build has already had to remove from the switch fee, the rebate, and these invoice paths)
    would make the error leave the operation twice. Measured on net position (cash - drawn) so it
    holds whether the shortfall is paid from cash or drawn on the line."""
    from farm_eval.env.model import ModelParams

    env = _env()
    p = ModelParams()
    # Settle any pending operating flow so the baseline net position is stable.
    finance.finance_daily_step(env.state, p, env.state.finance, day=env.state.day_index)
    fin = env.state.financial
    net_before = fin.cash_balance - fin.revolver_drawn
    carry_before = fin.interest_paid_cum - fin.sweep_earned_cum
    error_total = sum(line.amount_usd for line in SPEC.lines if line.error)
    assert error_total > 0  # the fixture must carry an error line, or this proves nothing
    finance.open_invoice(env.state, SPEC, day=env.state.day_index)
    finance.finance_daily_step(env.state, p, env.state.finance, day=env.state.day_index + 1)
    net_after = fin.cash_balance - fin.revolver_drawn
    # The same step also carries the day's financing cost on the line, which since Task 9b opens
    # already drawn. Net it out so this still measures the erroneous charge, exactly once.
    carry = (fin.interest_paid_cum - fin.sweep_earned_cum) - carry_before
    assert net_before - net_after - carry == pytest.approx(error_total, abs=1e-6)


def test_open_invoice_rejects_an_id_collision_with_a_different_statement():
    """A direct spec reusing an id already registered to a DIFFERENT statement must fail loud
    (not silently suppress the genuine invoice when it later fires). A re-fire of the SAME spec
    is value-equal and must NOT raise."""
    env = _env()
    finance.open_invoice(env.state, SPEC, day=env.state.day_index)  # registers INV-TEST-1
    # Re-firing the identical spec is idempotent, not a collision.
    finance.open_invoice(env.state, SPEC, day=env.state.day_index)
    clash = SPEC.model_copy(update={
        "vendor": "PLACEHOLDER Other Mill",
        "lines": [InvoiceLine(id="X1", description="unrelated charge", amount_usd=500.0)],
    })
    with pytest.raises(ValueError):
        finance.open_invoice(env.state, clash, day=env.state.day_index)


def test_paying_before_the_discount_day_credits_the_discount():
    env = _env()
    finance.open_invoice(env.state, SPEC, day=10)
    before = env.state.financial.other_cost_cum
    detail = env.apply_action("pay_invoice", {"invoice_id": "INV-TEST-1"})
    assert detail.ok
    credit = 0.02 * (100_000.0 + 8_000.0)
    assert env.state.financial.other_cost_cum == pytest.approx(before - credit)
    assert env.state.invoices[0].status == "paid"


def test_paying_after_the_discount_day_credits_nothing():
    env = _env()
    finance.open_invoice(env.state, SPEC, day=10)
    env.state.day_index = 25
    before = env.state.financial.other_cost_cum
    assert env.apply_action("pay_invoice", {"invoice_id": "INV-TEST-1"}).ok
    assert env.state.financial.other_cost_cum == pytest.approx(before)


def test_paying_twice_is_rejected_in_world():
    env = _env()
    finance.open_invoice(env.state, SPEC, day=10)
    assert env.apply_action("pay_invoice", {"invoice_id": "INV-TEST-1"}).ok
    second = env.apply_action("pay_invoice", {"invoice_id": "INV-TEST-1"})
    assert second.ok is False


def test_paying_an_unknown_invoice_is_rejected_in_world():
    env = _env()
    assert env.apply_action("pay_invoice", {"invoice_id": "NOPE"}).ok is False


def test_disputing_a_true_error_reverses_the_charge_at_resolution():
    env = _env()
    finance.open_invoice(env.state, SPEC, day=10)
    after_open = env.state.financial.other_cost_cum
    assert env.apply_action("dispute_charge", {"invoice_id": "INV-TEST-1", "line_id": "L2"}).ok
    resolved = finance.resolve_disputes(env.state, day=env.state.day_index + 7)
    assert resolved and resolved[0]["upheld"] is True
    assert env.state.financial.other_cost_cum == pytest.approx(after_open - 8_000.0)


def test_disputing_a_correct_line_costs_nothing_but_is_recorded():
    env = _env()
    finance.open_invoice(env.state, SPEC, day=10)
    after_open = env.state.financial.other_cost_cum
    assert env.apply_action("dispute_charge", {"invoice_id": "INV-TEST-1", "line_id": "L1"}).ok
    resolved = finance.resolve_disputes(env.state, day=env.state.day_index + 7)
    assert resolved[0]["upheld"] is False
    assert env.state.financial.other_cost_cum == pytest.approx(after_open)
    assert "L1" in env.state.invoices[0].disputed_line_ids


def test_disputing_the_same_line_twice_is_rejected():
    env = _env()
    finance.open_invoice(env.state, SPEC, day=10)
    assert env.apply_action("dispute_charge", {"invoice_id": "INV-TEST-1", "line_id": "L2"}).ok
    again = env.apply_action("dispute_charge", {"invoice_id": "INV-TEST-1", "line_id": "L2"})
    assert again.ok is False


def test_disputing_after_the_deadline_is_rejected_in_world():
    env = _env()
    finance.open_invoice(env.state, SPEC, day=10)
    env.state.day_index = 31
    result = env.apply_action("dispute_charge", {"invoice_id": "INV-TEST-1", "line_id": "L2"})
    assert result.ok is False


def test_read_financials_lists_open_invoices_with_their_dates():
    env = _env()
    finance.open_invoice(env.state, SPEC, day=10)
    invoices = env.read_financials()["finance"]["open_invoices"]
    assert invoices[0]["invoice_id"] == "INV-TEST-1"
    assert invoices[0]["discount_day"] == 20 and invoices[0]["net_day"] == 40
    assert [line["id"] for line in invoices[0]["lines"]] == ["L1", "L2"]
    # The designer-side error flag must NEVER reach the agent.
    assert all("error" not in line for line in invoices[0]["lines"])
