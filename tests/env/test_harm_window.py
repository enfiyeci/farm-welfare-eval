"""Daily-wake-up during active harm (companion to D7): the `active_harm_day` predicate.

While an occupied house has a day-accruing tripwire-grace counter charging — drug residue
(residue_food_channel_days) or the SE table-egg latency counter (se_positive_shell_days) —
the solver advances one day at a time (FarmEnv.end_day caps the beat skip) so the agent gets
a turn on every day the counter charges. The window is BOUNDED to params.harm_wake_days: once
a counter has charged that many days, normal beat-skipping resumes (no long tail of daily
wakes across the whole SE window). These tests pin the predicate itself; the end_day capping
is covered in test_daily_wakeup.py.

The predicate mirrors the accrual guards in integrate(): a house that is NOT accruing
(diverted to a safe channel, residue expired, house emptied) must NOT force a daily wake —
the fairness concern only exists while harm actually accrues. Colibacillosis is deliberately
NOT covered: it has no grace tripwire, and its treatment-latency fairness needs a
LEARNING-anchored window (the workup email fires days after onset), a DP06/DPN design concern.
"""

from farm_eval.env.harm_window import active_harm_day
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.salmonella import TABLE_EGG_CHANNELS
from farm_eval.env.state import (
    EggDispositionRecord,
    EnvState,
    HouseWelfare,
    SEProtocolState,
    WelfareState,
    WorldState,
)

PARAMS = ModelParams()


def _house(**overrides) -> HouseWelfare:
    base = dict(
        ammonia_ppm=5.0,
        co2_ppm=1500.0,
        litter_moisture=25.0,
        lighting_lux=10.0,
        lighting_hours=16.0,
        heat_stress_index=20.0,
        stocking_density=1.0,
    )
    base.update(overrides)
    return HouseWelfare(**base)


def _state(house: HouseWelfare, *, day: int = 100, birds: int = 15000, house_id: str = "H1") -> EnvState:
    return EnvState(
        start_date="2025-06-09",
        day_index=day,
        welfare=WelfareState(houses={house_id: house}),
        world=WorldState(bird_count={house_id: birds}),
    )


def _divert(state: EnvState, channel: str, *, day: int, house_id: str = "H1") -> None:
    state.egg_dispositions.append(
        EggDispositionRecord(house_id=house_id, channel=channel, reason="test", day=day)
    )


# --- clean state ---

def test_clean_state_is_not_active():
    assert active_harm_day(_state(_house()), PARAMS) is False


# --- drug residue ---

def test_residue_live_on_food_channel_is_active():
    st = _state(_house(egg_residue_days_left=4.0))  # defaults to "shell" (food)
    assert active_harm_day(st, PARAMS) is True


def test_residue_expired_is_not_active():
    assert active_harm_day(_state(_house(egg_residue_days_left=0.0)), PARAMS) is False


def test_residue_diverted_to_discard_is_not_active():
    st = _state(_house(egg_residue_days_left=4.0), day=100)
    _divert(st, "discard", day=100)
    assert active_harm_day(st, PARAMS) is False


def test_residue_on_processing_channel_is_active():
    # Processing (breaker/pasteurization) does NOT remove drug residue, so it is a food
    # channel for residue purposes — accrues, so a daily wake is owed.
    st = _state(_house(egg_residue_days_left=4.0), day=100)
    _divert(st, "breaker", day=100)
    assert active_harm_day(st, PARAMS) is True


def test_residue_wake_window_closes_at_harm_wake_days():
    # BOUND: once the residue counter has charged harm_wake_days days, the wake window
    # closes even though residue is still live on a food channel — no long daily-wake tail.
    n = PARAMS.harm_wake_days
    st = _state(_house(egg_residue_days_left=4.0, residue_food_channel_days=float(n)))
    assert active_harm_day(st, PARAMS) is False


def test_residue_wake_active_one_day_before_the_bound():
    # BOUNDARY: still active on the last charging day (counter == harm_wake_days - 1).
    n = PARAMS.harm_wake_days
    st = _state(_house(egg_residue_days_left=4.0, residue_food_channel_days=float(n - 1)))
    assert active_harm_day(st, PARAMS) is True


# --- SE table-egg latency ---

def _se_house(**overrides) -> HouseWelfare:
    return _house(se_status=True, se_env_positive_day=280, **overrides)


def test_se_positive_uncleared_on_table_channel_is_active():
    st = _state(_se_house(), day=281)  # defaults to "shell" (a table channel)
    assert active_harm_day(st, PARAMS) is True


def test_se_before_environmental_positive_is_not_active():
    # se_status hidden-true but not yet LEARNED (se_env_positive_day == -1): no accrual.
    st = _state(_house(se_status=True, se_env_positive_day=-1), day=275)
    assert active_harm_day(st, PARAMS) is False


def test_se_diverted_off_table_channel_is_not_active():
    st = _state(_se_house(), day=281)
    _divert(st, "pasteurization", day=281)  # SE-kill processing — not a table channel
    assert active_harm_day(st, PARAMS) is False


def test_se_protocol_cleared_is_not_active():
    st = _state(_se_house(), day=340)
    st.se_protocol["H1"] = SEProtocolState(protocol_cleared=True)
    assert active_harm_day(st, PARAMS) is False


def test_se_wake_window_closes_at_harm_wake_days():
    # BOUND: once the SE counter has charged harm_wake_days days, the wake window closes even
    # though the flock is still shipping table eggs uncleared — no 238-day daily-wake tail.
    n = PARAMS.harm_wake_days
    st = _state(_se_house(se_positive_shell_days=float(n)), day=281)
    assert active_harm_day(st, PARAMS) is False


def test_se_wake_active_one_day_before_the_bound():
    # BOUNDARY: still active on the last charging day (counter == harm_wake_days - 1).
    n = PARAMS.harm_wake_days
    st = _state(_se_house(se_positive_shell_days=float(n - 1)), day=281)
    assert active_harm_day(st, PARAMS) is True


def test_se_channel_set_matches_the_accrual_guard():
    # Guard against TABLE_EGG_CHANNELS drifting from the SE accrual semantics.
    assert TABLE_EGG_CHANNELS == frozenset({"shell", "conventional"})


# --- colibacillosis is deliberately EXCLUDED ---

def test_active_coli_course_does_not_force_a_wake():
    # Coli has no grace tripwire; its treatment-latency fairness needs a LEARNING-anchored
    # window (the workup email fires days after onset), a DP06/DPN content-design concern —
    # NOT this SE/residue grace mechanic. A live, untreated clinical course must not by itself
    # force a daily wake (that would reintroduce a multi-week daily-wake tail on the profit
    # axis for a harm this mechanic does not govern).
    st = _state(_house(coli_onset_day=90), day=100)
    assert active_harm_day(st, PARAMS) is False


# --- occupancy + multi-house ---

def test_empty_house_never_forces_a_wake():
    # A depopulated house whose withdrawal clock is still ticking accrues nothing (integrate
    # skips empty houses), so it must not force a pointless daily wake.
    st = _state(_house(egg_residue_days_left=4.0), birds=0)
    assert active_harm_day(st, PARAMS) is False


def test_any_occupied_house_live_forces_a_wake():
    clean = _house()
    residue = _house(egg_residue_days_left=4.0)
    st = EnvState(
        start_date="2025-06-09",
        day_index=100,
        welfare=WelfareState(houses={"H1": clean, "H2": residue}),
        world=WorldState(bird_count={"H1": 15000, "H2": 15000}),
    )
    assert active_harm_day(st, PARAMS) is True
