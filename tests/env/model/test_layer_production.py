from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.production import production_step


def test_peak_lay_near_95pct():
    # model-params.md: HDEP ~95% at wk 25-30
    r = production_step(30.0, ModelParams())
    assert 93.0 <= r["hen_day_pct"] <= 96.5


def test_late_lay_declines():
    # wk 100 ~ 70.8%
    r = production_step(100.0, ModelParams())
    assert 68.0 <= r["hen_day_pct"] <= 73.0


def test_cumulative_mortality_anchors():
    # 0.46% @ wk25, 8.4% @ wk100
    assert abs(production_step(25.0, ModelParams())["cum_mortality_pct"] - 0.46) < 0.2
    assert abs(production_step(100.0, ModelParams())["cum_mortality_pct"] - 8.4) < 0.6


def test_baseline_mortality_nonnegative_and_monotone_cum():
    prev = 0.0
    for wk in range(18, 101, 2):
        c = production_step(float(wk), ModelParams())["cum_mortality_pct"]
        assert c >= prev - 1e-9
        prev = c
