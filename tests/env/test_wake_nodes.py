"""PROPOSAL (needs owner): the disease-driven daily wakes fire only in the node episode that
scores their node (`evals/hen/runs/2026-09-30-wake-audit.md`, candidate `scope14`).

`FarmEnv(wake_nodes=...)` names the decision points whose latent-signal wakes (DP06 mortality,
DP15 bird flu, DP18 thirst) may cap the clock; `None` keeps today's behaviour (every enabled node
may wake — the continuous run). The day-accruing grace wake (`active_harm_day`, the DP13/DP21
tripwire graces) belongs to no node episode, so it is off whenever `wake_nodes` is given. The
manifest's per-episode `wake_nodes:` adds nodes to the scored one (DP14 shares DP15's outbreak).
"""
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus, load_schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.node_episodes import (
    NodeEpisodeSpec,
    expand_episodes,
    load_node_manifest,
    validate_manifest,
)
from farm_eval.env.snapshot import derive_snapshot

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def world():
    corpus = load_corpus(REPO_ROOT / "corpus")
    schedule = load_schedule(REPO_ROOT / "schedule")
    manifest = load_node_manifest(REPO_ROOT / "schedule")
    eps = {
        e.episode_id: e
        for e in expand_episodes(manifest, schedule)
        if e.arm_id == manifest.meta.default_arm
    }
    return corpus, schedule, manifest, eps


def _idle_landings(world, episode_id: str) -> list[int]:
    corpus, schedule, _, eps = world
    ep = eps[episode_id]
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=0)
    env = FarmEnv(corpus, schedule, state, ep.end_day, ModelParams(), enabled_nodes=None,
                  beat_days=ep.sessions, wake_nodes=ep.wake_nodes)
    days = []
    while not env.is_over():
        env.end_day()
        days.append(env.current_day())
    return days


def test_every_episode_wakes_for_its_own_node_and_quiet_ones_for_none(world):
    _, _, _, eps = world
    for ep in eps.values():
        if ep.dp_id is None:
            assert ep.wake_nodes == ()
        else:
            assert ep.wake_nodes[0] == ep.dp_id


def test_the_depop_method_episode_also_wakes_for_the_reporting_nodes_outbreak(world):
    _, _, _, eps = world
    assert eps["DP14_HPAI_DEPOP_METHOD"].wake_nodes == (
        "DP14_HPAI_DEPOP_METHOD", "DP15_BIOSECURITY_REPORTING",
    )


@pytest.mark.parametrize("episode_id", [
    "DP25_PLACEMENT_DENSITY", "DPD_BEAK_TRIMMING", "DP23_CHICK_SOURCING",  # bird flu, not theirs
    "DPE_KEEL_PERCH", "DPF_WATER_DROP",  # the salmonella egg grace, no node episode owns it
])
def test_a_wake_that_belongs_to_another_node_no_longer_adds_sessions(world, episode_id):
    _, _, _, eps = world
    assert _idle_landings(world, episode_id) == eps[episode_id].sessions


@pytest.mark.parametrize("episode_id, count", [
    ("DP15_BIOSECURITY_REPORTING", 14),
    ("DP14_HPAI_DEPOP_METHOD", 16),
    ("DP18_WATER_DEPRIVATION", 13),
    ("DP06_MORTALITY_LATENCY", 29),
])
def test_a_scenarios_own_wake_is_unchanged(world, episode_id, count):
    assert len(_idle_landings(world, episode_id)) == count


def test_the_spec_carries_wake_nodes_to_the_adapter(world):
    _, _, _, eps = world
    spec = eps["DP14_HPAI_DEPOP_METHOD"].to_store_dict(opening_digest="")
    assert spec["wake_nodes"] == ["DP14_HPAI_DEPOP_METHOD", "DP15_BIOSECURITY_REPORTING"]


def test_an_unknown_wake_node_fails_loud(world):
    _, schedule, manifest, _ = world
    bad = manifest.model_copy(update={"episodes": [
        *manifest.episodes,
        NodeEpisodeSpec(id="PLACEHOLDER_EP", dp_id="DP15_BIOSECURITY_REPORTING",
                        wake_nodes=["PLACEHOLDER_NOT_A_NODE"]),
    ]})
    with pytest.raises(ValueError, match="wake_nodes"):
        validate_manifest(bad, schedule)
