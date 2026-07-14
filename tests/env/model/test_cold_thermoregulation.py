"""Cold-thermoregulation feed coupling (owner directive 2026-07-13; research
docs/research/2026-07-13-financial-realism-web-sweep.md).

Below the thermoneutral floor (~18 °C) laying hens burn feed to stay warm: a controlled study
(indoor 12 °C vs 24 °C) measured feed intake +18.6% / FCR +33% with egg production ~unchanged
(PMC10741227). This makes the temperature setpoint a real, two-sided lever: dropping it saves
winter make-up-air heating but raises feed cost — and because feed dominates COP, the feed penalty
should exceed the heating saved, moving the profit-optimal setpoint UP into the thermoneutral band
(the welfare optimum). Feed is the dominant cold channel; cold does NOT degrade shell/egg quality
(unlike heat), so it is NOT wired into downgrades.
"""
from pathlib import Path

import pytest

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.production import cold_feed_multiplier

FIX = Path(__file__).parent.parent.parent / "fixtures"


def test_no_penalty_at_or_above_thermoneutral_floor():
    p = ModelParams()
    assert cold_feed_multiplier(p.cold_thermoneutral_floor_c, p) == pytest.approx(1.0)
    assert cold_feed_multiplier(p.cold_thermoneutral_floor_c + 5.0, p) == pytest.approx(1.0)
    assert cold_feed_multiplier(28.0, p) == pytest.approx(1.0)  # hot: no cold penalty (heat handled elsewhere)


def test_feed_rises_below_floor_and_matches_study_anchor():
    p = ModelParams()
    # 6 °C below the floor -> a clear increase
    m6 = cold_feed_multiplier(p.cold_thermoneutral_floor_c - 6.0, p)
    assert m6 > 1.0
    # study anchor: at 12 °C indoor, feed ~ +15-20% vs thermoneutral
    m12 = cold_feed_multiplier(12.0, p)
    assert 1.12 <= m12 <= 1.22


def test_multiplier_monotone_and_capped():
    p = ModelParams()
    vals = [cold_feed_multiplier(t, p) for t in (18.0, 14.0, 10.0, 4.0, -10.0)]
    assert all(a <= b for a, b in zip(vals, vals[1:]))       # colder -> more feed
    assert vals[-1] <= 1.0 + p.cold_feed_max_uplift + 1e-9   # never runs away


def _winter_feed_cost(setpoint_c: float) -> tuple[float, float]:
    """Terminal feed_cost_cum and a representative hen feed_g after a stretch of deep-winter days
    at a fixed temperature setpoint."""
    from farm_eval.env.loader import load_corpus, build_initial_state
    from farm_eval.env.model import integrate
    s = build_initial_state(load_corpus("corpus"))
    s.day_index = 205  # early-January winter window (day 0 = 2025-06-09)
    for hid in list(s.world.setpoints.keys()):
        if s.world.bird_count.get(hid, 0) > 0:
            s.world.setpoints[hid].update({"ventilation": 0.8, "temperature": setpoint_c})
    integrate(s, 20, ModelParams())
    hid = next(h for h in s.welfare.houses if s.world.bird_count.get(h, 0) > 0)
    return s.financial.feed_cost_cum, s.welfare.houses[hid].feed_g


def test_low_winter_setpoint_raises_feed_cost_and_intake():
    cold_cost, cold_feed = _winter_feed_cost(14.0)
    warm_cost, warm_feed = _winter_feed_cost(20.0)
    assert cold_cost > warm_cost      # a colder house eats more feed -> higher feed cost
    assert cold_feed > warm_feed      # and the per-bird intake shown in the flock report rises
