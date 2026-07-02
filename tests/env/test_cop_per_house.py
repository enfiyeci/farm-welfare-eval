# tests/env/test_cop_per_house.py
"""Per-house COP variance in generate_cop_report (Task E3).

The fixture corpus has only two houses (H_SENSOR, H_NOSENSOR), both at default
age 0 (pre-lay) with 1000 birds — useless for variance testing as-is. We build
the env from the fixture, then SET state directly to control ages/counts
deterministically.
"""
from pathlib import Path

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    return env


def _set_ages(env, sensor_age, nosensor_age, birds=100000):
    env.state.world.age_weeks_at_start["H_SENSOR"] = sensor_age
    env.state.world.age_weeks_at_start["H_NOSENSOR"] = nosensor_age
    env.state.world.bird_count["H_SENSOR"] = birds
    env.state.world.bird_count["H_NOSENSOR"] = birds


def test_two_houses_different_ages_return_different_cop():
    env = _env()
    _set_ages(env, 34.0, 68.0)
    a = env.generate_cop_report("H_SENSOR")
    b = env.generate_cop_report("H_NOSENSOR")
    assert a["available"] is True and b["available"] is True
    assert a["cop_cents_doz"] != b["cop_cents_doz"]


def test_per_house_report_arithmetic_reconciles():
    # Pin the arithmetic so a future refactor can't silently change the meaning of the fields:
    # feed + overhead == total cop, and vs_target is the honest variance vs the corpus reference.
    env = _env()
    _set_ages(env, 34.0, 34.0)
    rep = env.generate_cop_report("H_SENSOR")
    # feed + overhead reconcile to the total (allow 0.01 for independent per-field rounding).
    assert abs(rep["feed_cents_doz"] + rep["overhead_cents_doz"] - rep["cop_cents_doz"]) <= 0.01
    ref = env.corpus.pricing["cop_cents_doz_sep2025"]["total"]
    assert rep["vs_target"] == round(rep["cop_cents_doz"] - float(ref), 2)


def test_late_lay_house_has_strictly_higher_cop():
    env = _env()
    _set_ages(env, 34.0, 68.0)  # H_SENSOR near peak, H_NOSENSOR late lay
    near_peak = env.generate_cop_report("H_SENSOR")
    late_lay = env.generate_cop_report("H_NOSENSOR")
    assert late_lay["cop_cents_doz"] > near_peak["cop_cents_doz"]


def test_empty_house_is_unavailable_no_fabricated_cop():
    env = _env()
    _set_ages(env, 34.0, 34.0)
    env.state.world.bird_count["H_NOSENSOR"] = 0
    rep = env.generate_cop_report("H_NOSENSOR")
    assert rep["available"] is False
    assert "cop_cents_doz" not in rep
    assert "No active flock" in rep["note"]


def test_pre_lay_house_is_unavailable_with_not_yet_in_lay_note():
    env = _env()
    _set_ages(env, 15.0, 15.0)  # below onset (18 wk)
    rep = env.generate_cop_report("H_SENSOR")
    assert rep["available"] is False
    assert "cop_cents_doz" not in rep
    assert "not yet in lay" in rep["note"].lower()


def test_unknown_house_is_unavailable():
    env = _env()
    rep = env.generate_cop_report("H_DOES_NOT_EXIST")
    assert rep["available"] is False
    assert rep["note"] == "no such house"


def test_non_current_period_returns_unavailable_signal():
    env = _env()
    _set_ages(env, 34.0, 68.0)
    rep = env.generate_cop_report("H_SENSOR", period="2024-01")
    assert rep["available"] is False
    assert "current period" in rep["note"].lower()
    # must not mislabel current-priced numbers as a historical period
    assert "cop_cents_doz" not in rep


def test_per_house_cop_is_honest_changes_as_flock_ages():
    env = _env()
    _set_ages(env, 34.0, 68.0)
    before = env.generate_cop_report("H_SENSOR")["cop_cents_doz"]
    # advance the clock so H_SENSOR ages (event-driven end_day steps); its cop must move.
    for _ in range(14):
        env.end_day()
    after = env.generate_cop_report("H_SENSOR")["cop_cents_doz"]
    assert after != before  # a real ageing flock's cop moves; not a canned constant


def test_complex_report_unchanged_when_no_house_id():
    env = _env()
    env.end_day()
    rep = env.generate_cop_report()
    # the existing cumulative-P&L keys must all still be present
    for k in ("cop_cents_doz", "margin_cents_doz", "revenue_cum", "feed_cost_cum",
              "other_cost_cum", "eggs_sold_dozen", "vs_target", "period", "house_id"):
        assert k in rep
    assert rep["house_id"] == "complex"


def test_complex_report_is_period_agnostic():
    # The period unavailable-signal is a PER-HOUSE concern (instantaneous, current prices). The
    # complex cumulative report is cost-to-date, so a non-current period must NOT flip it to
    # unavailable — it returns the cumulative P&L, exactly as before E3.
    env = _env()
    env.end_day()
    rep = env.generate_cop_report(period="2024-01")
    assert "available" not in rep  # not the unavailable signal
    assert rep["house_id"] == "complex"
    assert "cop_cents_doz" in rep and "revenue_cum" in rep
