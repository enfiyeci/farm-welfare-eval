from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.production import production_step, body_weight_g


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


def test_body_weight_matches_hyline_brown_anchors():
    p = ModelParams()
    # Anchor points from the Hy-Line Brown Dec-2025 standards table (range midpoints).
    assert body_weight_g(18, p) == 1452
    assert body_weight_g(30, p) == 1918
    assert body_weight_g(100, p) == 2022


def test_body_weight_is_monotone_nondecreasing_and_plateaus():
    p = ModelParams()
    weights = [body_weight_g(a, p) for a in p.breed_age_wk]
    assert weights == sorted(weights)              # body weight only rises with age
    assert 1900 <= body_weight_g(60, p) <= 2100    # mature plateau ~1.9–2.1 kg (world-bible §16)


def test_body_weight_clamps_outside_age_range():
    p = ModelParams()
    assert body_weight_g(10, p) == body_weight_g(18, p)    # below first anchor -> first value
    assert body_weight_g(120, p) == body_weight_g(100, p)  # above last anchor -> last value
