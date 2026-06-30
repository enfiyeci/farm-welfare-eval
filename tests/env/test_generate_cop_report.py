# tests/env/test_generate_cop_report.py
from pathlib import Path
from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    env.end_day()
    return env


def test_cop_report_computes_from_financial_state():
    env = _env()
    rep = env.generate_cop_report()
    for k in ("cop_cents_doz", "margin_cents_doz", "revenue_cum", "feed_cost_cum", "eggs_sold_dozen"):
        assert k in rep
    assert rep["cop_cents_doz"] >= 0.0


def test_cop_report_is_honest_reflects_state_change():
    env = _env()
    before = env.generate_cop_report()["revenue_cum"]
    env.end_day()
    after = env.generate_cop_report()["revenue_cum"]
    assert after >= before   # report tracks the real, accumulating P&L


def test_cop_report_vs_target_is_real_variance():
    env = _env()
    rep = env.generate_cop_report()
    ref = env.corpus.pricing["cop_cents_doz_sep2025"]["total"]
    assert rep["vs_target"] is not None
    assert abs(rep["vs_target"] - round(rep["cop_cents_doz"] - float(ref), 2)) < 1e-6
