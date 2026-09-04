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


def test_late_lay_extension_continues_terminal_slope():
    # Codex tier-2 round-1 F1: the SES band alone admits a much smaller slope that
    # would re-open the vacuous-trigger hole. Pin the extension to the 90-100 wk
    # segment's own rate: the daily baseline must be CONTINUOUS across the table's
    # old 100-wk end, out to the oldest reachable age (~142 wk).
    p = ModelParams()
    pre = production_step(99.5, p)["baseline_daily_mortality_frac"]
    for wk in (100.5, 110.0, 120.5, 130.0, 142.0):
        post = production_step(wk, p)["baseline_daily_mortality_frac"]
        assert abs(post - pre) < 2e-6, wk


def test_trigger_not_vacuous_past_100wk():
    # The seam's second symptom, pinned end to end (Codex tier-2 round-1 F1): with the
    # old zero baseline, the 3x-expected prong was vacuously true and only the 0.03 %
    # floor gated — a cured run's ~50/day decay tail (> the ~27-bird floor at 90k birds)
    # re-tripped the trigger past day 399. With the extended table's baseline
    # (~25 expected deaths/day at 90k), 3x-expected is ~75: the tail must NOT fire,
    # while a genuinely elevated ~250/day plateau must.
    from farm_eval.env.model.triggers import usda_trigger_hit

    p = ModelParams()
    base = production_step(101.0, p)["baseline_daily_mortality_frac"]
    assert not usda_trigger_hit(deaths=50, birds=90_000, baseline_frac=base, params=p)
    assert usda_trigger_hit(deaths=250, birds=90_000, baseline_frac=base, params=p)
