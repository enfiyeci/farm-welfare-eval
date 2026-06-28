from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.economics import revenue_step


def test_revenue_full_quality_no_downgrade():
    p = ModelParams()
    # 1000 birds at 90% lay = 900 eggs = 75 dozen; price $2/doz; no downgrades
    r = revenue_step(90.0, 1000, 2.0, 0.0, p)
    assert abs(r["total_dozen"] - 75.0) < 1e-6
    assert abs(r["sellable_dozen"] - 75.0) < 1e-6
    assert abs(r["downgrade_dozen"] - 0.0) < 1e-6
    assert abs(r["revenue_usd"] - 150.0) < 1e-6


def test_revenue_with_downgrade_to_breaker():
    p = ModelParams(breaker_price_frac=0.30)
    # 75 dozen, 20% downgraded: 60 doz @ $2 + 15 doz @ $0.60 = 120 + 9 = 129
    r = revenue_step(90.0, 1000, 2.0, 0.20, p)
    assert abs(r["sellable_dozen"] - 60.0) < 1e-6
    assert abs(r["downgrade_dozen"] - 15.0) < 1e-6
    assert abs(r["revenue_usd"] - 129.0) < 1e-6
