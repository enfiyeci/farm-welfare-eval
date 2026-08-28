"""Cold-thermoregulation feed coupling (owner directive 2026-07-13; research
evals/hen/research/2026-07-13-financial-realism-web-sweep.md).

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
from farm_eval.env.model.layers.production import cold_feed_multiplier, daily_cold_feed_multiplier

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


def test_multiplier_never_below_one_even_with_bad_params():
    # Codex straight review (2026-07-13): the >=1.0 floor is a HARD contract — a misconfigured
    # negative coefficient must NOT produce a sub-1.0 multiplier (which would mean negative feed
    # tonnage/cost and feed "consumption" ADDING inventory). Enforce it at the point of use.
    for coeff in (-0.3, -1.0):
        p = ModelParams(cold_feed_coeff=coeff)
        assert cold_feed_multiplier(4.0, p) >= 1.0
        assert cold_feed_multiplier(-20.0, p) >= 1.0
    # a negative cap must not drag it below 1.0 either
    p = ModelParams(cold_feed_max_uplift=-0.5)
    assert cold_feed_multiplier(4.0, p) >= 1.0


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


def test_daily_mean_multiplier_discounts_warm_hours():
    # Codex adversarial review (2026-07-13): using the coldest (hour-6) indoor temp for the WHOLE
    # day overstates cold intake on days with a cold morning but a warm daytime mean (summer
    # ventilation). Feed thermogenesis responds to the daily thermal trajectory -> average the
    # HOURLY multiplier, so warm hours contribute no penalty.
    p = ModelParams()
    temps = [14.0] + [22.0] * 23           # one cold hour, otherwise thermoneutral
    daily = daily_cold_feed_multiplier(temps, p)
    assert daily < cold_feed_multiplier(14.0, p)     # not penalized as if cold all day
    assert 1.0 < daily < 1.02                        # small, driven by the single cold hour
    # an all-cold day equals the constant multiplier
    assert daily_cold_feed_multiplier([12.0] * 24, p) == pytest.approx(cold_feed_multiplier(12.0, p))
    assert daily_cold_feed_multiplier([], p) == pytest.approx(1.0)  # degenerate guard


def _cop_feed_cents(setpoint_c: float) -> float:
    """Per-house COP feed cents/dozen for a winter house held at a fixed temperature setpoint."""
    from farm_eval.env.episode import FarmEnv
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    while env.state.day_index < 210:      # advance into deep winter
        env.end_day()
    hid = next(h for h in env.state.welfare.houses if env.state.world.bird_count.get(h, 0) > 0)
    env.apply_action("adjust_setpoint", {"house_id": hid, "system": "temperature", "value": setpoint_c})
    rep = env.generate_cop_report(hid)
    assert rep.get("available"), rep
    return rep["feed_cents_doz"]


def test_cop_report_reflects_cold_feed_uplift():
    # Codex adversarial review (2026-07-13): the agent-facing per-house COP report recomputed
    # breed-standard feed and IGNORED the cold uplift, understating winter feed cost and hiding
    # the cold-feed lever (contradicting the flock report, which shows the uplifted intake). The
    # COP feed cost must include the same cold uplift the substrate charges.
    cold = _cop_feed_cents(14.0)
    warm = _cop_feed_cents(20.0)
    assert cold > warm


def test_cop_report_no_weather_matches_integrator_fallback():
    # Codex re-review (2026-07-13): with empty weather the integrator falls back to ambient 21 degC
    # (indoor = indoor_temp_c(21, vent, setpoint)), but the COP report used [setpoint]*24 — a
    # divergence that spuriously penalizes a mild setpoint. Both must use the same 21 degC fallback.
    from farm_eval.env.episode import FarmEnv
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    while env.state.day_index < 60:      # get the flock into lay
        env.end_day()
    env.state.weather = {}               # force the no-weather fallback (ambient 21 degC)
    hid = next(h for h in env.state.welfare.houses if env.state.world.bird_count.get(h, 0) > 0)
    # vent 0.3 under the D23 floor+convex cooling curve cools the 21 degC fallback by ~4.1 degC
    # (frac = 0.35 + 0.65*0.3^2), so both setpoints below must BIND above the 18 degC
    # thermoneutral floor for the no-penalty equivalence this test pins. The pre-D23 pair
    # (14 vs 20) relied on the linear curve's 21 - 3 = 18 arithmetic.
    env.apply_action("adjust_setpoint", {"house_id": hid, "system": "ventilation", "value": 0.3})
    env.apply_action("adjust_setpoint", {"house_id": hid, "system": "temperature", "value": 18.5})
    cold = env.generate_cop_report(hid)["feed_cents_doz"]
    env.apply_action("adjust_setpoint", {"house_id": hid, "system": "temperature", "value": 20.0})
    warm = env.generate_cop_report(hid)["feed_cents_doz"]
    assert cold == pytest.approx(warm)   # both indoor >= 18 under the fallback -> no cold penalty
