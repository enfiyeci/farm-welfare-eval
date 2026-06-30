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
    assert after > before   # strict: a real end_day() must increase revenue_cum (rejects canned constants)


def test_cop_report_vs_target_is_real_variance():
    env = _env()
    ref = env.corpus.pricing["cop_cents_doz_sep2025"]["total"]
    # Seed financial accumulators to a known state for independent arithmetic
    f = env.state.financial
    f.feed_cost_cum, f.other_cost_cum, f.sellable_dozen_cum = 500.0, 460.0, 1000.0
    rep = env.generate_cop_report()
    # independent: cop = (500 + 460) / 1000 * 100 = 96.0 cents/doz
    assert rep["cop_cents_doz"] == 96.0
    assert rep["vs_target"] == round(96.0 - float(ref), 2)  # 96.0 - 96.2 = -0.2
