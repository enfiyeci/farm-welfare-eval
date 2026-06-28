# tests/env/model/test_integrate_economics.py
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams


def _fresh():
    return build_initial_state(load_corpus("corpus"))


def test_integrate_populates_pnl():
    s = _fresh()
    integrate(s, elapsed_days=30, params=ModelParams())
    f = s.financial
    assert f.revenue_cum > 0.0
    assert f.feed_cost_cum > 0.0
    assert f.other_cost_cum > 0.0
    assert f.eggs_sold > 0.0
    # margin identity
    assert abs(f.margin - (f.revenue_cum - f.feed_cost_cum - f.other_cost_cum)) < 1e-6


def test_pnl_path_independence():
    one = _fresh()
    integrate(one, 210, ModelParams())
    chunk = _fresh()
    for _ in range(7):
        integrate(chunk, 30, ModelParams())
        chunk.day_index += 30
    # Non-vacuity: the one-shot run must have accrued real P&L, else 0 == 0 passes trivially.
    # Cover the dozen accumulators too, so their path-equality below is not a 0 == 0 tautology.
    assert one.financial.revenue_cum > 0.0
    assert one.financial.feed_cost_cum > 0.0
    assert one.financial.sellable_dozen_cum > 0.0
    assert one.financial.downgrade_dozen_cum > 0.0
    # Every financial accumulator must be path-independent, not just revenue/margin.
    for field in ("revenue_cum", "feed_cost_cum", "other_cost_cum", "margin",
                  "sellable_dozen_cum", "downgrade_dozen_cum", "eggs_sold",
                  "mortality_loss_cum"):
        assert abs(getattr(one.financial, field) - getattr(chunk.financial, field)) < 1e-6, field


def test_mortality_charges_sunk_pullet_cost():
    s = _fresh()
    integrate(s, 60, ModelParams())
    assert s.financial.mortality_loss_cum > 0.0
