"""Egg-disposition lever: standing per-house channel allocation + P&L effect (Phase C6-A1).

A disposition is a STANDING per-house allocation: `set_egg_disposition(house_id, channel, reason)`
routes that house's egg output to `channel` from the CURRENT day forward, until changed. Every call
is recorded in an append-only audit log (`EnvState.egg_dispositions`). Default (no record) is
"shell". Revenue respects the current channel: shell=full value, breaker/pasteurization=reduced
value (data-driven multiplier, NOT hardcoded), discard=0.
"""

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.model.economics import revenue_step
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import EggDispositionRecord, EnvState, current_disposition

FIX = Path(__file__).parent.parent / "fixtures"


def _env() -> FarmEnv:
    return FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)


# --- state / helper -------------------------------------------------------


def test_default_disposition_is_shell():
    state = EnvState(start_date="2025-06-09")
    assert current_disposition(state, "H_SENSOR", as_of_day=0) == "shell"


def test_current_disposition_reflects_latest_record():
    state = EnvState(start_date="2025-06-09")
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H_SENSOR", channel="discard", reason="withdrawal", day=3)
    )
    assert current_disposition(state, "H_SENSOR", as_of_day=3) == "discard"
    # unaffected house stays default
    assert current_disposition(state, "H_NOSENSOR", as_of_day=3) == "shell"


def test_current_disposition_uses_latest_record_when_multiple():
    state = EnvState(start_date="2025-06-09")
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H_SENSOR", channel="discard", reason="withdrawal", day=3)
    )
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H_SENSOR", channel="shell", reason="withdrawal cleared", day=10)
    )
    assert current_disposition(state, "H_SENSOR", as_of_day=10) == "shell"


# --- day-aware resolution (Finding 3) --------------------------------------


def test_current_disposition_ignores_future_record_for_earlier_as_of_day():
    state = EnvState(start_date="2025-06-09")
    # Record effective day=5; querying as_of_day=0 (state.day_index==0 style) must NOT
    # see it yet — it shouldn't be effective before its recorded day.
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H_SENSOR", channel="discard", reason="future", day=5)
    )
    assert current_disposition(state, "H_SENSOR", as_of_day=0) == "shell"
    assert current_disposition(state, "H_SENSOR", as_of_day=4) == "shell"
    # Once as_of_day reaches the record's day, it becomes effective.
    assert current_disposition(state, "H_SENSOR", as_of_day=5) == "discard"


def test_current_disposition_out_of_order_append_greatest_qualifying_day_wins():
    state = EnvState(start_date="2025-06-09")
    # Appended out of day order: day=10 first, then day=3.
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H_SENSOR", channel="discard", reason="later", day=10)
    )
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H_SENSOR", channel="breaker", reason="earlier", day=3)
    )
    # as_of_day=10: both qualify (day <= 10); greatest day (10) wins regardless of append order.
    assert current_disposition(state, "H_SENSOR", as_of_day=10) == "discard"
    # as_of_day=2: neither day=3 nor day=10 qualifies -> default "shell".
    assert current_disposition(state, "H_SENSOR", as_of_day=2) == "shell"


def test_current_disposition_same_day_tie_last_appended_wins():
    state = EnvState(start_date="2025-06-09")
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H_SENSOR", channel="breaker", reason="first", day=5)
    )
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H_SENSOR", channel="discard", reason="second", day=5)
    )
    assert current_disposition(state, "H_SENSOR", as_of_day=5) == "discard"


# --- revenue_step loud unknown-channel lookup (Finding 1) -----------------


def test_revenue_step_unknown_channel_raises():
    p = ModelParams()
    with pytest.raises(ValueError):
        revenue_step(90.0, 1000, 2.0, 0.0, p, disposition_channel="landfill")


def test_revenue_step_channel_missing_from_params_raises():
    # A params override that forgets to configure a channel must fail loudly at
    # lookup time, not silently price it at full (1.0) shell value.
    p = ModelParams(egg_channel_value_frac={"shell": 1.0, "breaker": 0.35, "pasteurization": 0.35})
    with pytest.raises(ValueError):
        revenue_step(90.0, 1000, 2.0, 0.0, p, disposition_channel="discard")


# --- FarmEnv.set_egg_disposition ------------------------------------------


def test_set_egg_disposition_records_and_returns_confirmation():
    env = _env()
    env.start()
    result = env.set_egg_disposition("H_SENSOR", "discard", "SE-positive diversion")
    assert result == {"house_id": "H_SENSOR", "channel": "discard", "effective_day": 0}
    assert len(env.state.egg_dispositions) == 1
    rec = env.state.egg_dispositions[0]
    assert rec.house_id == "H_SENSOR"
    assert rec.channel == "discard"
    assert rec.reason == "SE-positive diversion"
    assert rec.day == 0
    assert current_disposition(env.state, "H_SENSOR", as_of_day=0) == "discard"


def test_set_egg_disposition_records_at_current_day():
    env = _env()
    env.start()
    env.end_day()  # advance past day 0
    day_before = env.current_day()
    assert day_before > 0
    env.set_egg_disposition("H_SENSOR", "breaker", "diversion")
    assert env.state.egg_dispositions[-1].day == day_before


def test_set_egg_disposition_does_not_leak_ledger_or_scoring_data():
    env = _env()
    env.start()
    result = env.set_egg_disposition("H_SENSOR", "pasteurization", "diversion")
    assert set(result.keys()) == {"house_id", "channel", "effective_day"}


def test_set_egg_disposition_unknown_house_raises():
    env = _env()
    env.start()
    with pytest.raises(ValueError):
        env.set_egg_disposition("H_NOPE", "shell", "reason")


def test_set_egg_disposition_invalid_channel_raises():
    env = _env()
    env.start()
    with pytest.raises(ValueError):
        env.set_egg_disposition("H_SENSOR", "landfill", "reason")


def test_set_egg_disposition_valid_channels_accepted():
    env = _env()
    env.start()
    for channel in ("shell", "breaker", "pasteurization", "discard"):
        env.set_egg_disposition("H_SENSOR", channel, "routine")
    assert current_disposition(env.state, "H_SENSOR", as_of_day=env.current_day()) == "discard"


# --- determinism ------------------------------------------------------------


def test_same_calls_produce_identical_state():
    env1 = _env()
    env1.start()
    env1.set_egg_disposition("H_SENSOR", "discard", "SE-positive diversion")
    env1.end_day()

    env2 = _env()
    env2.start()
    env2.set_egg_disposition("H_SENSOR", "discard", "SE-positive diversion")
    env2.end_day()

    assert env1.state.model_dump() == env2.state.model_dump()


# --- P&L revenue effect ----------------------------------------------------


def _fresh_state_with_house(bird_count: int = 1000, hen_day_pct: float = 90.0) -> EnvState:
    from farm_eval.env.state import HouseWelfare, WorldState

    state = EnvState(start_date="2025-06-09")
    hw = HouseWelfare(
        ammonia_ppm=5.0, co2_ppm=800.0, litter_moisture=20.0, lighting_lux=20.0,
        lighting_hours=16.0, heat_stress_index=20.0, stocking_density=1.0,
    )
    hw.hen_day_pct = hen_day_pct
    state.welfare.houses["H1"] = hw
    state.world = WorldState(
        bird_count={"H1": bird_count},
        age_weeks_at_start={"H1": 40.0},
        litter_age_days={"H1": 0.0},
    )
    state.market.egg_price_usd_doz = 2.0
    return state


def test_discard_channel_zeroes_egg_revenue_from_effective_day():
    from farm_eval.env.model.integrate import integrate

    params = ModelParams()

    baseline = _fresh_state_with_house()
    integrate(baseline, elapsed_days=1, params=params)
    baseline.day_index += 1
    assert baseline.financial.revenue_cum > 0.0

    discarded = _fresh_state_with_house()
    discarded.egg_dispositions.append(
        EggDispositionRecord(house_id="H1", channel="discard", reason="drug residue", day=0)
    )
    integrate(discarded, elapsed_days=1, params=params)
    discarded.day_index += 1
    assert discarded.financial.revenue_cum == 0.0


def test_breaker_and_pasteurization_earn_less_than_shell():
    from farm_eval.env.model.integrate import integrate

    params = ModelParams()

    shell_state = _fresh_state_with_house()
    integrate(shell_state, elapsed_days=1, params=params)

    breaker_state = _fresh_state_with_house()
    breaker_state.egg_dispositions.append(
        EggDispositionRecord(house_id="H1", channel="breaker", reason="diversion", day=0)
    )
    integrate(breaker_state, elapsed_days=1, params=params)

    pasteurization_state = _fresh_state_with_house()
    pasteurization_state.egg_dispositions.append(
        EggDispositionRecord(house_id="H1", channel="pasteurization", reason="diversion", day=0)
    )
    integrate(pasteurization_state, elapsed_days=1, params=params)

    assert 0.0 < breaker_state.financial.revenue_cum < shell_state.financial.revenue_cum
    assert 0.0 < pasteurization_state.financial.revenue_cum < shell_state.financial.revenue_cum


def test_switching_back_to_shell_restores_full_value_going_forward():
    from farm_eval.env.model.integrate import integrate

    params = ModelParams()

    # Day 0 on discard, then switched back to shell for day 1 onward.
    state = _fresh_state_with_house()
    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H1", channel="discard", reason="withdrawal", day=0)
    )
    integrate(state, elapsed_days=1, params=params)  # integrates day 1 (index 0 -> 1)
    state.day_index += 1
    assert state.financial.revenue_cum == 0.0

    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H1", channel="shell", reason="withdrawal cleared", day=1)
    )
    integrate(state, elapsed_days=1, params=params)  # integrates day 2, now on shell
    state.day_index += 1

    # Age-matched control: shell throughout, day 2 isolated by taking the delta across the
    # same two integrate steps (production/age is identical between the runs — only the
    # disposition channel differs), so the post-switch increment must equal a from-scratch
    # shell day at that flock age.
    shell_control = _fresh_state_with_house()
    integrate(shell_control, elapsed_days=1, params=params)
    shell_control.day_index += 1
    revenue_after_day1 = shell_control.financial.revenue_cum
    integrate(shell_control, elapsed_days=1, params=params)
    shell_control.day_index += 1
    control_day2_revenue = shell_control.financial.revenue_cum - revenue_after_day1

    switched_day2_revenue = state.financial.revenue_cum  # day 1 contributed 0.0 (discard)
    assert abs(switched_day2_revenue - control_day2_revenue) < 1e-6


def test_days_before_the_call_are_unaffected():
    from farm_eval.env.model.integrate import integrate

    params = ModelParams()

    # Two days of shell revenue accrue, THEN discard is set (effective day 2).
    state = _fresh_state_with_house()
    integrate(state, elapsed_days=2, params=params)
    state.day_index += 2
    revenue_before_switch = state.financial.revenue_cum
    assert revenue_before_switch > 0.0

    state.egg_dispositions.append(
        EggDispositionRecord(house_id="H1", channel="discard", reason="withdrawal", day=2)
    )
    integrate(state, elapsed_days=1, params=params)
    state.day_index += 1

    # Revenue accrued before the switch must be untouched (no retroactive effect).
    assert state.financial.revenue_cum == revenue_before_switch
