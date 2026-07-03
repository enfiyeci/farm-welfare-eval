"""B1 — `enabled_nodes` filters which decision points seed the ledger (and thus score).

Uses the REAL schedule (`schedule/`) + corpus (`corpus/`) via `FarmEnv.from_paths`: the test
fixture schedule has only a placeholder DP, so it can't exercise a multi-node subset filter.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.events import open_due_decision_points

ROOT = Path(__file__).resolve().parents[2]


def _env(enabled=None):
    env = FarmEnv.from_paths(
        ROOT / "corpus", ROOT / "schedule", seed=1, episode_end_day=511, enabled_nodes=enabled
    )
    env.start()
    return env


def test_enabled_nodes_seeds_only_the_named_subset():
    env = _env(enabled=["DP01_AMMONIA_VENT", "DP16_FOOTPAD"])
    # Seed the ledger past both nodes' opens_days by opening everything due by day 511.
    open_due_decision_points(env.state, env.schedule, 511, env.enabled_nodes)
    assert {e.dp_id for e in env.state.ledger} == {"DP01_AMMONIA_VENT", "DP16_FOOTPAD"}


def test_enabled_nodes_none_seeds_the_full_set():
    env = _env(enabled=None)
    open_due_decision_points(env.state, env.schedule, 511, env.enabled_nodes)
    assert len({e.dp_id for e in env.state.ledger}) == len(env.schedule.decision_points)


def test_unknown_enabled_node_id_fails_loud():
    with pytest.raises(ValueError):
        FarmEnv.from_paths(
            ROOT / "corpus",
            ROOT / "schedule",
            seed=1,
            episode_end_day=511,
            enabled_nodes=["DP01_AMMONIA_VENT", "NOPE_NODE"],
        )


def test_empty_enabled_nodes_fails_loud():
    # An empty selection would seed an empty ledger and crash later in welfare_headline; reject it
    # at construction with a clear message (distinct from unknown-id).
    with pytest.raises(ValueError, match="empty"):
        FarmEnv.from_paths(
            ROOT / "corpus", ROOT / "schedule", seed=1, episode_end_day=511, enabled_nodes=[]
        )


def test_only_enabled_nodes_reach_the_scorer():
    from farm_eval.judge.scorer import compute_welfare_state, score_nodes

    enabled = ["DP01_AMMONIA_VENT", "DP16_FOOTPAD"]
    env = _env(enabled=enabled)
    open_due_decision_points(env.state, env.schedule, 511, env.enabled_nodes)
    signatures = {dp.id: dp.signature for dp in env.schedule.decision_points}
    channels = compute_welfare_state(env.state)["channels"]
    scores = score_nodes(
        env.state.ledger,
        signatures,
        channels,
        actions=[],
        grade_fn=lambda e, c, s: 0.0,
        schedule=env.schedule,
    )
    # Both enabled nodes carry a scoring config, so both score — and ONLY they do (a disabled node
    # never seeds the ledger, so it can never score).
    assert set(scores) == set(enabled)
