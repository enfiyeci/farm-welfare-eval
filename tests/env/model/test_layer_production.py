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
    for wk in range(18, 143, 2):
        c = production_step(float(wk), ModelParams())["cum_mortality_pct"]
        assert c >= prev - 1e-9
        prev = c


def test_late_lay_baseline_mortality_stays_in_ses_band():
    # Seam fix 2026-08-28: the breed tables used to end at 100 wk, so the
    # cum-mortality forward slope — and with it baseline_daily_mortality_frac —
    # flatlined to 0 for any flock past 100 wk. Reachable ages inside the 518-day
    # episode: H5 hits 117 wk (day 518), a molted H1 hits ~142 wk. The baseline
    # daily rate must stay inside the USDA SES Supplement-1 normal band for
    # table-egg layers (0.00005-0.0006 deaths/bird/day) all the way out.
    for wk in (101.0, 110.0, 117.0, 126.0, 142.0):
        r = production_step(wk, ModelParams())
        assert 0.00005 <= r["baseline_daily_mortality_frac"] <= 0.0006, wk


def test_cum_mortality_keeps_rising_past_100wk():
    p = ModelParams()
    c100 = production_step(100.0, p)["cum_mortality_pct"]
    c120 = production_step(120.0, p)["cum_mortality_pct"]
    assert c120 > c100 + 1.0
