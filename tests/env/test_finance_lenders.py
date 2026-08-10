"""Task 2 (M2/M4): lender selection, switch fees, patronage rebate, manual repayment."""
import pytest

from farm_eval.env import finance
from farm_eval.env.episode import FarmEnv


def _env() -> FarmEnv:
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=30)
    env.start()
    return env


def test_switching_lender_books_the_switch_fee_and_records_the_day():
    env = _env()
    target = next(lid for lid in env.state.finance.lenders if lid != env.state.lender.active_lender_id)
    fee = env.state.finance.lenders[env.state.lender.active_lender_id].switch_fee_usd
    other_before = env.state.financial.other_cost_cum
    result = env.apply_action("set_financing", {"action": "select_lender", "lender_id": target})
    assert result.ok
    assert env.state.lender.active_lender_id == target
    assert env.state.lender.switch_fees_cum == pytest.approx(fee)
    assert env.state.financial.other_cost_cum == pytest.approx(other_before + fee)
    assert env.state.lender.switch_days == [env.state.day_index]


def test_switch_fee_leaves_the_net_position_exactly_once_across_the_daily_step():
    """Regression against double-counting the switch fee. select_lender books the fee to the P&L
    ONLY; finance_daily_step settles that margin change into cash exactly once. If select_lender
    also adjusted cash directly, the next daily step would re-settle the same margin drop and the
    fee would leave the operation twice — breaking the cash identity. Measured on net position
    (cash - drawn) so it holds whether the fee is paid from cash or drawn on the line."""
    from farm_eval.env.model import ModelParams

    env = _env()
    p = ModelParams()
    # Settle any pending operating flow so the baseline net position is stable.
    finance.finance_daily_step(env.state, p, env.state.finance, day=env.state.day_index)
    fin = env.state.financial
    net_before = fin.cash_balance - fin.revolver_drawn
    target = next(lid for lid in env.state.finance.lenders if lid != env.state.lender.active_lender_id)
    fee = env.state.finance.lenders[env.state.lender.active_lender_id].switch_fee_usd
    assert fee > 0  # the default (outgoing) lender charges a switch fee, or this proves nothing
    env.apply_action("set_financing", {"action": "select_lender", "lender_id": target})
    finance.finance_daily_step(env.state, p, env.state.finance, day=env.state.day_index + 1)
    net_after = fin.cash_balance - fin.revolver_drawn
    assert net_before - net_after == pytest.approx(fee, abs=1e-6)


def test_switching_to_an_unknown_lender_is_rejected_in_world():
    env = _env()
    before = env.state.lender.active_lender_id
    result = env.apply_action("set_financing", {"action": "select_lender", "lender_id": "nope"})
    assert result.ok is False
    assert result.addressed_dps == []
    assert env.state.lender.active_lender_id == before
    assert any(e.get("type", "").startswith("fallback:") for e in env.state.event_log)


def test_switching_to_the_active_lender_is_rejected_and_charges_nothing():
    env = _env()
    active = env.state.lender.active_lender_id
    fees_before = env.state.lender.switch_fees_cum
    result = env.apply_action("set_financing", {"action": "select_lender", "lender_id": active})
    assert result.ok is False
    assert env.state.lender.switch_fees_cum == fees_before


def test_repay_moves_cash_to_the_drawn_balance_and_preserves_the_identity():
    env = _env()
    fin = env.state.financial
    fin.cash_balance = 300_000.0
    fin.revolver_drawn = 200_000.0
    before = fin.cash_balance - fin.revolver_drawn
    result = env.apply_action("set_financing", {"action": "repay", "amount": 150_000.0})
    assert result.ok
    assert fin.cash_balance == pytest.approx(150_000.0)
    assert fin.revolver_drawn == pytest.approx(50_000.0)
    assert fin.cash_balance - fin.revolver_drawn == pytest.approx(before)


def test_repay_is_clamped_to_cash_on_hand_and_to_the_drawn_balance():
    env = _env()
    fin = env.state.financial
    fin.cash_balance = 40_000.0
    fin.revolver_drawn = 500_000.0
    env.apply_action("set_financing", {"action": "repay", "amount": 999_999_999.0})
    assert fin.cash_balance == 0.0
    assert fin.revolver_drawn == pytest.approx(460_000.0)


def test_repay_rejects_a_non_positive_or_non_numeric_amount():
    env = _env()
    for amount in (0.0, -5.0, "lots", float("inf")):
        result = env.apply_action("set_financing", {"action": "repay", "amount": amount})
        assert result.ok is False, amount


def test_unknown_financing_action_is_rejected_in_world():
    env = _env()
    result = env.apply_action("set_financing", {"action": "refinance_the_barn"})
    assert result.ok is False


def test_patronage_rebate_credits_a_share_of_interest_paid():
    env = _env()
    fin = env.state.financial
    fin.interest_paid_cum = 100_000.0
    lender = finance.active_lender(env.state)
    other_before = fin.other_cost_cum
    credited = finance.apply_patronage_rebate(env.state)
    assert credited == pytest.approx(100_000.0 * lender.patronage_rebate_frac)
    assert fin.other_cost_cum == pytest.approx(other_before - credited)
    assert env.state.lender.patronage_rebate_cum == pytest.approx(credited)


def test_read_financials_surfaces_the_finance_block():
    env = _env()
    block = env.read_financials()["finance"]
    assert block["active_lender"] == env.state.lender.active_lender_id
    for key in ("annual_rate", "revolver_drawn", "interest_paid", "cash_balance", "sweep_enabled"):
        assert key in block
    # The silent ledger must never leak through a read tool.
    assert "ledger" not in block and "decision" not in str(block).lower()
