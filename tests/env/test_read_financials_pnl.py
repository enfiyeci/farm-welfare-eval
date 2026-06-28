from pathlib import Path

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env() -> FarmEnv:
    # Mirrors tests/env/test_episode.py::_env — from_paths(corpus_dir, schedule_dir, ...)
    return FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)


def test_read_financials_exposes_pnl_block():
    env = _env()
    env.start()
    env.end_day()  # advance at least one beat so P&L accrues
    rep = env.read_financials()
    assert "pnl" in rep
    pnl = rep["pnl"]
    for k in ("revenue_cum", "feed_cost_cum", "other_cost_cum", "margin",
              "cop_cents_doz", "margin_cents_doz", "eggs_sold_dozen", "downgrade_dozen"):
        assert k in pnl
    # Non-vacuity: after a beat advances, real P&L must have accrued — a zeros block must fail.
    assert pnl["revenue_cum"] > 0.0
    assert pnl["feed_cost_cum"] > 0.0
    assert pnl["other_cost_cum"] > 0.0
    assert pnl["eggs_sold_dozen"] > 0.0
    assert pnl["downgrade_dozen"] > 0.0
    # Reported margin must satisfy the Tier-0 identity (rounding tolerance on the 2-dp fields).
    assert abs(pnl["margin"] - (pnl["revenue_cum"] - pnl["feed_cost_cum"] - pnl["other_cost_cum"])) < 0.01
