from farm_eval.env.state import FinancialState


def test_financial_state_has_pnl_accumulators():
    f = FinancialState()
    assert f.other_cost_cum == 0.0
    assert f.sellable_dozen_cum == 0.0
    assert f.downgrade_dozen_cum == 0.0
    assert f.feed_book_value_usd == 0.0
    # existing fields still present
    assert f.revenue_cum == 0.0 and f.feed_cost_cum == 0.0 and f.margin == 0.0
