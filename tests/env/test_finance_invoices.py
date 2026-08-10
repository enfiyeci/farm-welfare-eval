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
