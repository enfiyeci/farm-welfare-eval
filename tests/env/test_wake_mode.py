"""wake_mode: `sparse` (today: jump to the next scheduled beat) vs `daily` (advance one day
per end_day; events still fire on their authored days). Spec
docs/specs/2026-09-03-daily-wake-and-rolling-context-design.md §4.3."""
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).resolve().parents[1] / "fixtures"


def _env(mode: str, end: int = 12) -> FarmEnv:
    env = FarmEnv.from_paths(
        FIX / "corpus", FIX / "schedule", episode_end_day=end, seed=1, wake_mode=mode
    )
    env.start()
    return env


def test_default_is_sparse():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", episode_end_day=12, seed=1)
    assert env.wake_mode == "sparse"


def test_sparse_jumps_to_the_next_beat():
    env = _env("sparse")
    r = env.end_day()
    assert (r.new_day, r.elapsed_days) == (5, 5)   # fixture beats are {0, 5}


def test_daily_advances_exactly_one_day_per_end_day():
    env = _env("daily")
    r = env.end_day()
    assert (r.new_day, r.elapsed_days) == (1, 1)
    env.end_day()
    assert env.current_day() == 2


def test_daily_still_fires_events_on_their_authored_day():
    env = _env("daily")
    for _ in range(4):
        env.end_day()
    fired_before_beat = len(env.state.fired_event_ids)
    env.end_day()                                   # day 5 is the fixture's second beat
    assert env.current_day() == 5
    assert len(env.state.fired_event_ids) > fired_before_beat


def test_daily_clamps_at_the_episode_end():
    env = _env("daily", end=3)
    for _ in range(3):
        env.end_day()
    assert env.is_over()
    assert env.current_day() == 3


def test_unknown_wake_mode_is_rejected():
    with pytest.raises(ValueError, match="wake_mode"):
        FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", episode_end_day=12, wake_mode="weekly")
