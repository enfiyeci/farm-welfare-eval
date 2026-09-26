"""FarmEnv's per-episode clock override + the explicit empty-node allowance (node episodes, D6/D8)."""
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import build_initial_state, load_corpus, load_schedule
from farm_eval.env.model import ModelParams

FIX = Path(__file__).resolve().parents[1] / "fixtures"


def _env(**kw) -> FarmEnv:
    corpus, schedule = load_corpus(FIX / "corpus"), load_schedule(FIX / "node_schedule")
    state = build_initial_state(corpus, seed=1)
    return FarmEnv(corpus, schedule, state, 21, ModelParams(), **kw)


def test_beat_days_override_replaces_the_schedule_beats():
    env = _env(beat_days=[10, 21])   # skip the day-5 and day-15 beats
    env.start()
    assert env.end_day().new_day == 10
    assert env.end_day().new_day == 21
    assert env.is_over()


def test_events_between_overridden_beats_still_fire_and_are_dated():
    env = _env(beat_days=[21])
    env.start()
    env.end_day()
    days = sorted(e.day for e in env.state.mailbox)
    # day 20 is the two-version follow-up fixture (DP_PLACEHOLDER_1 addressed/unaddressed).
    assert days == [0, 10, 15, 20]  # the skipped days' mail still arrived, dated by its own day


def test_default_clock_unchanged_when_beat_days_is_none():
    env = _env()
    env.start()
    assert [env.end_day().new_day for _ in range(4)] == [5, 10, 15, 20]


def test_empty_enabled_nodes_still_rejected_by_default():
    with pytest.raises(ValueError, match="enabled_nodes is empty"):
        _env(enabled_nodes=())


def test_empty_enabled_nodes_allowed_when_explicit():
    env = _env(enabled_nodes=(), allow_empty_nodes=True)
    env.start()
    env.end_day()
    assert env.state.ledger == []  # nothing seeded, nothing scored


def test_replay_env_threads_allow_empty_nodes():
    from farm_eval.env.replay import replay_env
    corpus, schedule = load_corpus(FIX / "corpus"), load_schedule(FIX / "node_schedule")
    state = replay_env(corpus, schedule, [], 9, ModelParams(), episode_end_day=21,
                       enabled_nodes=frozenset(), allow_empty_nodes=True, seed=1)
    assert state.day_index == 5 and state.ledger == []
