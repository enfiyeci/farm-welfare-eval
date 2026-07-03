"""Tests for `farm_eval.env.replay.replay_env` — deterministic state reconstruction from the
recorded action log (D1). See `farm_eval/env/replay.py` for the module docstring and the
rejected-attempts caveat this file asserts against.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import build_initial_state, load_corpus, load_schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.replay import replay_env
from farm_eval.env.schedule_models import ScheduledEvent
from farm_eval.env.state import EnvState

FIX = Path(__file__).parent.parent / "fixtures"


def _corpus_and_schedule():
    corpus = load_corpus(FIX / "corpus")
    # A richer schedule than the shared fixture's single-DP one, so the action mix below (setpoint,
    # feed order, staffing, disposition, email, treatment) has beats to land on across several days.
    schedule = load_schedule(FIX / "schedule")
    schedule = schedule.model_copy(
        update={
            "events": schedule.events
            + [
                ScheduledEvent(on_day=10, type="audit", payload={}),
                ScheduledEvent(on_day=20, type="audit", payload={}),
                ScheduledEvent(on_day=30, type="audit", payload={}),
            ]
        }
    )
    return corpus, schedule


def _dump(state: EnvState) -> str:
    return json.dumps(state.model_dump(mode="json"), sort_keys=True)


def _drive_realistic_episode(
    corpus, schedule, *, params, episode_end_day, enabled_nodes=None, with_rejections=False, seed=1
):
    """Drive a fixture episode imperatively through several beats with a realistic mix of
    successful actions (and, optionally, a couple of rejected attempts interleaved). Returns the
    live `FarmEnv` at its final state (episode over). Constructed the same way `FarmEnv.from_paths`
    (and `replay_env`) build the initial state, so a replay with the same `seed` is comparable."""
    state = build_initial_state(corpus, seed=seed)
    env = FarmEnv(corpus, schedule, state, episode_end_day, params, enabled_nodes)
    env.start()  # day 0

    env.apply_action("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 2.5})
    env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 5.0})
    if with_rejections:
        # Absurd feed order (unit-confusion class of mistake) — rejected, never enters `actions`.
        env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 999_000_000.0})
    env.end_day()  # -> day 5 (sensor_anomaly)

    env.apply_action("set_staffing", {"fte": 6.0, "shift_hours": 9.0})
    env.apply_action(
        "send_email",
        {"to": "dale.renner@cloverdaleeggs.com", "subject": "ammonia", "body": "raising ventilation in H_SENSOR"},
    )
    if with_rejections:
        # Nonsense staffing level — rejected, never enters `actions`.
        env.apply_action("set_staffing", {"fte": -5.0})
    env.end_day()  # -> day 10 (audit)

    env.apply_action(
        "set_egg_disposition", {"house_id": "H_SENSOR", "channel": "breaker", "reason": "downgrade routing"}
    )
    env.apply_action("log_treatment", {"house_id": "H_SENSOR", "issue": "red_mite", "drug": "spinosad"})
    env.end_day()  # -> day 20 (audit)

    env.apply_action("adjust_setpoint", {"house_id": "H_NOSENSOR", "system": "ventilation", "value": 1.8})
    env.end_day()  # -> day 30 (audit)

    while not env.is_over():
        env.end_day()

    return env


def test_full_replay_is_bit_identical_when_no_rejections():
    corpus, schedule = _corpus_and_schedule()
    params = ModelParams()
    original = _drive_realistic_episode(corpus, schedule, params=params, episode_end_day=400)

    replayed = replay_env(
        corpus, schedule, original.state.actions, to_day=original.state.day_index, params=params,
        episode_end_day=400, seed=1,
    )

    assert _dump(replayed) == _dump(original.state)


def test_replay_with_rejected_attempts_matches_on_scoring_relevant_fields():
    corpus, schedule = _corpus_and_schedule()
    params = ModelParams()
    original = _drive_realistic_episode(
        corpus, schedule, params=params, episode_end_day=400, with_rejections=True
    )

    replayed = replay_env(
        corpus, schedule, original.state.actions, to_day=original.state.day_index, params=params,
        episode_end_day=400, seed=1,
    )

    # Scoring-relevant fields are bit-identical (the rejected attempts never touched EnvState).
    for field in (
        "ledger", "actions", "welfare", "financial", "market", "world", "mailbox", "outbound",
        "egg_dispositions", "fired_event_ids", "day_index",
    ):
        assert getattr(replayed, field) == getattr(original.state, field), f"field {field!r} diverged"

    # event_log differs ONLY by the absent fallback:* entries: filtering them out of the original
    # yields exactly the replayed event_log.
    original_filtered = [e for e in original.state.event_log if not str(e.get("type", "")).startswith("fallback:")]
    assert original_filtered == replayed.event_log
    # Sanity: the original really did record fallback entries (the rejections actually happened).
    assert len(original_filtered) < len(original.state.event_log)


def test_truncated_replay_stops_at_last_beat_leq_to_day_and_resolves_only_due_windows():
    corpus, schedule = _corpus_and_schedule()
    params = ModelParams()
    original = _drive_realistic_episode(corpus, schedule, params=params, episode_end_day=400)

    # to_day=15 is mid-episode, between the day-10 and day-20 beats: the replay must stop AT day 10
    # (the last beat <= 15), not overshoot to day 20.
    truncated = replay_env(
        corpus, schedule, original.state.actions, to_day=15, params=params, episode_end_day=400, seed=1,
    )
    assert truncated.day_index == 10

    # DP_PLACEHOLDER_1 (deadline_day=5) is long past its deadline by day 10 -> resolved (lapsed or
    # addressed, but not left open).
    dp1 = next(e for e in truncated.ledger if e.dp_id == "DP_PLACEHOLDER_1")
    assert dp1.status.value != "open"

    # No overshoot integration: the truncated run's harm accumulators are strictly <= the full run's
    # (accumulators are monotonic non-decreasing, so stopping earlier can only integrate less or the
    # same, never more).
    full = replay_env(
        corpus, schedule, original.state.actions, to_day=original.state.day_index, params=params,
        episode_end_day=400, seed=1,
    )
    assert truncated.welfare.harm.nh3_ppm_hours_over <= full.welfare.harm.nh3_ppm_hours_over
    assert truncated.day_index < full.day_index


def test_replay_raises_loudly_on_a_doctored_action_day():
    corpus, schedule = _corpus_and_schedule()
    params = ModelParams()
    original = _drive_realistic_episode(corpus, schedule, params=params, episode_end_day=400)

    doctored = list(original.state.actions)
    bad = doctored[0].model_copy(update={"day": doctored[0].day + 3})  # 3 is not a beat day
    doctored[0] = bad

    with pytest.raises(Exception, match=r"day.*3|3.*day"):
        replay_env(corpus, schedule, doctored, to_day=original.state.day_index, params=params, episode_end_day=400, seed=1)


def test_replay_raises_loudly_when_a_recorded_success_now_rejects():
    corpus, schedule = _corpus_and_schedule()
    params = ModelParams()
    original = _drive_realistic_episode(corpus, schedule, params=params, episode_end_day=400)

    doctored = list(original.state.actions)
    # Mutate the recorded setpoint action's system to one the controller now rejects — a
    # was-successful action that would diverge on replay (schedule/params/corpus mismatch).
    for i, rec in enumerate(doctored):
        if rec.tool == "adjust_setpoint":
            doctored[i] = rec.model_copy(update={"params": {**rec.params, "system": "not_a_real_system"}})
            break
    else:
        pytest.fail("expected an adjust_setpoint record in the driven episode")

    with pytest.raises(Exception):
        replay_env(corpus, schedule, doctored, to_day=original.state.day_index, params=params, episode_end_day=400, seed=1)


def test_enabled_nodes_pass_through_seeds_only_selected_nodes():
    corpus, schedule = _corpus_and_schedule()
    params = ModelParams()
    restricted = frozenset({"DP_PLACEHOLDER_1"})
    original = _drive_realistic_episode(
        corpus, schedule, params=params, episode_end_day=400, enabled_nodes=restricted
    )
    assert {e.dp_id for e in original.state.ledger} == restricted

    replayed = replay_env(
        corpus, schedule, original.state.actions, to_day=original.state.day_index, params=params,
        episode_end_day=400, enabled_nodes=restricted, seed=1,
    )
    assert {e.dp_id for e in replayed.ledger} == restricted
    assert _dump(replayed) == _dump(original.state)
