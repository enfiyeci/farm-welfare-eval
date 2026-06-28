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
    assert abs(one.financial.revenue_cum - chunk.financial.revenue_cum) < 1e-6
    assert abs(one.financial.margin - chunk.financial.margin) < 1e-6


def test_mortality_charges_sunk_pullet_cost():
    s = _fresh()
    integrate(s, 60, ModelParams())
    assert s.financial.mortality_loss_cum > 0.0
