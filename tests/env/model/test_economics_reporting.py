from farm_eval.env.state import FinancialState
from farm_eval.env.model.economics import cop_cents_doz, margin_cents_doz


def test_cop_and_margin_per_dozen():
    # margin must be set explicitly: FinancialState.margin is computed by integrate() (not a
    # pydantic validator), so it defaults to 0.0 unless passed directly.
    f = FinancialState(revenue_cum=150.0, feed_cost_cum=40.0, other_cost_cum=50.0,
                       margin=60.0, sellable_dozen_cum=100.0)
    # total cost 90 over 100 doz = $0.90/doz = 90 cents
    assert abs(cop_cents_doz(f) - 90.0) < 1e-6
    # margin 60 over 100 doz = 60 cents
    assert abs(margin_cents_doz(f) - 60.0) < 1e-6


def test_per_dozen_zero_safe():
    f = FinancialState()  # no eggs yet
    assert cop_cents_doz(f) == 0.0
    assert margin_cents_doz(f) == 0.0
