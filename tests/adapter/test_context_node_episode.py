"""D5: per-sample episode facts in the store; get_env builds the FarmEnv from them."""
import dataclasses
from pathlib import Path

import pytest
from inspect_ai.util import store_as

from farm_eval.adapter import context as ctx
from farm_eval.adapter.context import EpisodeConfig, EpisodeStore, get_env, resolve_episode, snapshot_for
from farm_eval.env.loader import load_corpus

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "node_schedule"),
                    episode_end_day=400, seed=1, node_episodes=True)


@pytest.fixture(autouse=True)
def _fresh_store():
    # inspect's store is task-local; outside a running eval store_as() gives a process-wide one.
    def _reset():
        s = store_as(EpisodeStore)
        s.env_state = None
        s.episode_spec = None
        s.forced_advances = 0

    _reset()
    yield
    _reset()  # leave the process-wide store clean for whatever test runs next


def test_resolve_episode_reads_manifest_by_metadata():
    ep = resolve_episode(CFG, {"episode_id": "DP_PLACEHOLDER_2", "arm": "history_bad"})
    assert ep.arm_id == "history_bad" and ep.end_day == 21


def test_snapshot_for_is_cached_and_returns_a_copy():
    ep = resolve_episode(CFG, {"episode_id": "DP_PLACEHOLDER_2", "arm": "neutral"})
    a, da = snapshot_for(CFG, ep)
    b, db = snapshot_for(CFG, ep)
    assert a is not b and a.model_dump(mode="json") == b.model_dump(mode="json") and da == db
    a.day_index = 99
    c, _ = snapshot_for(CFG, ep)
    assert c.day_index == 10  # the cache was not mutated through the copy


def test_get_env_uses_store_spec_for_end_day_nodes_and_clock():
    ep = resolve_episode(CFG, {"episode_id": "DP_PLACEHOLDER_2", "arm": "neutral"})
    state, digest = snapshot_for(CFG, ep)
    store = store_as(EpisodeStore)
    store.env_state = state
    store.episode_spec = ep.to_store_dict(opening_digest=digest)
    env = get_env(CFG)
    assert env.episode_end_day == 21
    # Ruling 21 item 1: every decision is on the ledger; the judge narrows to the scored node.
    assert env.enabled_nodes is None
    assert env.end_day().new_day == 15   # first session
    assert env.current_day() == 15


def test_get_env_without_spec_is_unchanged_continuous_behaviour():
    env = get_env(EpisodeConfig(corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"),
                                episode_end_day=400, seed=1))
    assert env.episode_end_day == 400 and env.current_day() == 0


def test_get_env_refuses_spec_without_seeded_state():
    ep = resolve_episode(CFG, {"episode_id": "DP_PLACEHOLDER_2", "arm": "neutral"})
    store_as(EpisodeStore).episode_spec = ep.to_store_dict(opening_digest="x")
    with pytest.raises(RuntimeError, match="episode_spec is set but no snapshot was seeded"):
        get_env(CFG)


def test_snapshot_for_key_includes_ablation_overrides(tmp_path):
    # Two configs identical except ablation_overrides must not share a cached snapshot (reviewer
    # fix 1): the key must fold in the EFFECTIVE overrides, not just (paths, episode, arm, seed).
    doc_id = sorted(load_corpus(FIX / "corpus").documents)[0]
    variant = tmp_path / "variant.md"
    variant.write_text("VARIANT BODY", encoding="utf-8")
    cfg_override = dataclasses.replace(CFG, ablation_overrides={doc_id: str(variant)})

    ctx._snapshots.clear()
    ep = resolve_episode(CFG, {"episode_id": "DP_PLACEHOLDER_2", "arm": "neutral"})
    snapshot_for(CFG, ep)
    snapshot_for(cfg_override, ep)
    assert len(ctx._snapshots) == 2  # distinct cache entries, not a stale share


def test_get_env_raises_when_node_episodes_true_and_no_spec_seeded():
    with pytest.raises(RuntimeError, match="node_episodes=True but the store carries no episode_spec"):
        get_env(CFG)
