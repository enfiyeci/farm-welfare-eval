"""Task 1 (M1): cash + revolver core. The cash identity is the load-bearing invariant."""
import pytest

from farm_eval.env import finance
from farm_eval.env.finance_models import FinanceConfig, Lender
from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model import ModelParams
from farm_eval.env.state import EnvState, FinancialState


def _cfg() -> FinanceConfig:
    return FinanceConfig(
        enabled=True,
        opening_cash_usd=500_000.0,
        default_lender_id="assoc",
        lenders={
            "assoc": Lender(
                id="assoc", name="PLACEHOLDER Association", kind="association",
                rate_series={"2025-06": 0.0773, "2026-01": 0.0708},
                switch_fee_usd=2_500.0, patronage_rebate_frac=0.12,
            ),
        },
    )


def _state(cfg: FinanceConfig) -> EnvState:
    state = EnvState(start_date="2025-06-09", finance=cfg)
    state.lender.active_lender_id = cfg.default_lender_id
    state.financial.finance_opening_cash = cfg.opening_cash_usd
    state.financial.cash_balance = cfg.opening_cash_usd
    return state


def test_book_pnl_cost_keeps_the_margin_identity():
    f = FinancialState(revenue_cum=1000.0, feed_cost_cum=200.0, other_cost_cum=100.0)
    finance.book_pnl_cost(f, 50.0)
    assert f.other_cost_cum == 150.0
    assert f.margin == 1000.0 - 200.0 - 150.0


def test_book_pnl_cost_accepts_a_credit():
    f = FinancialState(revenue_cum=1000.0, feed_cost_cum=0.0, other_cost_cum=100.0)
    finance.book_pnl_cost(f, -40.0)
    assert f.other_cost_cum == 60.0
    assert f.margin == 940.0


def test_annual_rate_carries_the_latest_prior_month_forward():
    lender = _cfg().lenders["assoc"]
    # day 0 == 2025-06-09 -> the 2025-06 point; day 250 lands in 2026-02, after the 2026-01 step.
    assert finance.annual_rate_for_day(lender, "2025-06-09", 0) == pytest.approx(0.0773)
    assert finance.annual_rate_for_day(lender, "2025-06-09", 250) == pytest.approx(0.0708)


def test_disabled_axis_is_a_total_no_op():
    cfg = _cfg().model_copy(update={"enabled": False})
    state = _state(cfg)
    state.financial.revenue_cum = 100_000.0
    before = state.financial.model_dump()
    finance.finance_daily_step(state, ModelParams(), cfg, day=1)
    assert state.financial.model_dump() == before


def test_positive_operating_flow_lands_in_cash_and_never_draws():
    cfg = _cfg()
    state = _state(cfg)
    state.financial.revenue_cum = 80_000.0
    state.financial.other_cost_cum = 30_000.0
    state.financial.margin = 50_000.0
    finance.finance_daily_step(state, ModelParams(), cfg, day=1)
    assert state.financial.cash_balance == pytest.approx(550_000.0)
    assert state.financial.revolver_drawn == 0.0
    assert state.financial.interest_paid_cum == 0.0


def test_negative_cash_auto_draws_on_the_active_line():
    cfg = _cfg()
    state = _state(cfg)
    # A loss bigger than opening cash: 600k of cost against no revenue.
    state.financial.other_cost_cum = 600_000.0
    state.financial.margin = -600_000.0
    finance.finance_daily_step(state, ModelParams(), cfg, day=1)
    assert state.financial.cash_balance == 0.0
    assert state.financial.revolver_drawn == pytest.approx(100_000.0)


def test_interest_accrues_daily_on_the_drawn_balance_and_hits_the_pnl():
    cfg = _cfg()
    state = _state(cfg)
    state.financial.revolver_drawn = 365_000.0
    other_before = state.financial.other_cost_cum
    finance.finance_daily_step(state, ModelParams(), cfg, day=1)
    expected = 365_000.0 * 0.0773 / 365.0
    assert state.financial.interest_paid_cum == pytest.approx(expected)
    assert state.financial.other_cost_cum == pytest.approx(other_before + expected)


def test_cash_identity_holds_across_many_days():
    cfg = _cfg()
    state = _state(cfg)
    for day in range(1, 40):
        # Simulate the day's P&L the way integrate() books it.
        state.financial.revenue_cum += 60_000.0
        state.financial.other_cost_cum += 75_000.0
        state.financial.margin = (
            state.financial.revenue_cum
            - state.financial.feed_cost_cum
            - state.financial.other_cost_cum
        )
        finance.finance_daily_step(state, ModelParams(), cfg, day=day)
        f = state.financial
        identity = f.finance_opening_cash + f.margin - f.feed_book_value_usd
        assert f.cash_balance - f.revolver_drawn == pytest.approx(identity, abs=1e-6)


def test_corpus_finance_yml_loads_and_is_enabled():
    corpus = load_corpus("corpus")
    state = build_initial_state(corpus)
    assert state.finance.enabled is True
    assert state.finance.opening_cash_usd > 0
    assert state.lender.active_lender_id in state.finance.lenders
    assert state.financial.cash_balance == state.finance.opening_cash_usd


def test_state_roundtrips_with_the_finance_block():
    corpus = load_corpus("corpus")
    state = build_initial_state(corpus)
    restored = EnvState.model_validate(state.model_dump())
    assert restored.finance.lenders.keys() == state.finance.lenders.keys()
    assert restored.lender.active_lender_id == state.lender.active_lender_id
