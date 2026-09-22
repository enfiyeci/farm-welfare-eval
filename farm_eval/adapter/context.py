"""Per-sample episode context: the EnvState lives in the Inspect store; a FarmEnv binds to it.

The locked seam (see plan "Phase B execution"): the env core must stay Inspect-free, so EnvState
cannot subclass StoreModel. Instead `EpisodeStore` (a StoreModel) carries the plain-pydantic
EnvState; a FarmEnv bound to `store.env_state` mutates it in place and the welfare/ledger state
serializes into the `.eval` log. Corpus + schedule are read-only and identical across samples —
loaded once and cached by path (never in the store). `started` lives in the store so the solver
owns a single `FarmEnv.start()` per sample (survives retry/replay), which is why get_env can cheaply
rebind a fresh FarmEnv on every call instead of caching one.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass

from inspect_ai.util import StoreModel, store_as

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import (
    Corpus,
    Schedule,
    apply_overrides,
    build_initial_state,
    load_corpus,
    load_schedule,
    validate_body_refs,
    validate_reply_refs,
)
from farm_eval.env.model import ModelParams
from farm_eval.env.node_episodes import ResolvedEpisode, expand_episodes, find_episode, load_node_manifest, validate_manifest
from farm_eval.env.snapshot import derive_snapshot
from farm_eval.env.state import EnvState


@dataclass(frozen=True)
class EpisodeConfig:
    """Task-level configuration the tools and solver capture in their closures."""

    corpus_path: str
    schedule_path: str
    episode_end_day: int
    seed: int = 0
    params: ModelParams | None = None
    # Optional node-selection filter: when set, ONLY these decision points seed the ledger (and
    # thus score). None (the default) = all nodes enabled. Fixed within a sweep (ablation studies).
    enabled_nodes: tuple[str, ...] | None = None
    # D2: opt-in per-beat EnvState checkpointing for paid-run resilience. None (the default) =
    # checkpointing OFF, zero behavior change. When set, the solver writes a checkpoint after
    # every actual day advancement (see farm_eval.adapter.checkpoint.write_checkpoint).
    checkpoint_dir: str | None = None
    # P5 (D3): single-artifact ablation {artifact_id: variant_path}. None (default) = off.
    # Any run with overrides set is EXPERIMENTAL — stamped by the scorer, refused by
    # comparable-sweep ranking (spec 2026-07-05 §6.3). Never set in a comparable sweep.
    ablation_overrides: dict[str, str] | None = None
    # Node episodes (plan 2026-09-15, D5): when True the task's samples each carry an
    # `episode_id`/`arm` in Sample.metadata, the solver seeds `EpisodeStore.episode_spec` +
    # the derived snapshot, and `get_env` builds the FarmEnv from the store spec (end day,
    # enabled node, session clock, arm overrides) instead of this config's episode-wide values.
    node_episodes: bool = False


class EpisodeStore(StoreModel):
    # The mutated, logged episode state. Start-idempotence lives in EnvState.started (so it
    # survives FarmEnv rebinding and retry/replay), not here.
    env_state: EnvState | None = None
    # E7: run-health diagnostic — count of times the solver's max-turns-per-day backstop had to
    # force-advance the day because the target never called end_day. Lives in the adapter store
    # (not EnvState) so the env core stays Inspect-free; persists into the `.eval` log and is read
    # by the scorer into Score.metadata (a diagnostic, not a scored metric).
    forced_advances: int = 0
    # Run-health diagnostic (2026-09-22): count of assistant turns with text but no tool call. Each
    # gets the solver's continuation nudge; two consecutive tool-less turns force the day advance.
    text_only_turns: int = 0
    # Node episodes (D5): the per-sample facts `get_env` needs — see
    # `ResolvedEpisode.to_store_dict`. None = continuous episode (unchanged behaviour).
    episode_spec: dict | None = None


# Read-only resources, identical across samples — load once, keyed by (corpus_path, schedule_path).
_resources: dict[tuple[str, str], tuple[Corpus, Schedule]] = {}


def load_resources(cfg: EpisodeConfig, overrides: dict[str, str] | None = None) -> tuple[Corpus, Schedule]:
    """Load (and validate) the corpus + schedule under cfg's paths.

    `overrides`, when truthy, REPLACE `cfg.ablation_overrides` entirely for this call (never
    merged with it) — a node-episode arm's overrides stand in for the config's. A falsy
    `overrides` (`None` or `{}`) means "this caller has none of its own" and INHERITS
    `cfg.ablation_overrides` instead — so an arm with no overrides of its own still picks up
    a config-level ablation, same as the continuous (non-node-episode) path always did.
    """
    key = (str(cfg.corpus_path), str(cfg.schedule_path))
    effective = overrides or cfg.ablation_overrides
    if effective:
        # Bypass the cache entirely: an overridden load must never be read from (a stale
        # baseline would silently drop the override) or written to (it would poison later
        # NORMAL loads with the ablated corpus). The cache holds only pristine baselines.
        corpus, schedule = load_corpus(cfg.corpus_path), load_schedule(cfg.schedule_path)
        validate_body_refs(schedule, corpus)
        validate_reply_refs(corpus)
        corpus = apply_overrides(corpus, effective, cfg.corpus_path)
        return corpus, schedule
    if key not in _resources:
        corpus, schedule = load_corpus(cfg.corpus_path), load_schedule(cfg.schedule_path)
        validate_body_refs(schedule, corpus)
        validate_reply_refs(corpus)
        _resources[key] = (corpus, schedule)
    return _resources[key]


# Node episodes (D5): the manifest (validated once per schedule_path) and derived starting
# snapshots (validated + built once per episode/arm/seed/params), both keyed by process-wide
# caches identical in spirit to `_resources` above.
_manifests: dict[str, list[ResolvedEpisode]] = {}
_snapshots: dict[tuple, tuple[EnvState, str]] = {}


def resolved_episodes(cfg: EpisodeConfig) -> list[ResolvedEpisode]:
    """Every (episode, arm) the manifest under cfg.schedule_path defines; validated once, cached."""
    key = str(cfg.schedule_path)
    if key not in _manifests:
        _, schedule = load_resources(cfg)
        manifest = load_node_manifest(cfg.schedule_path)
        validate_manifest(manifest, schedule)
        _manifests[key] = expand_episodes(manifest, schedule)
    return _manifests[key]


def resolve_episode(cfg: EpisodeConfig, metadata: dict | None) -> ResolvedEpisode:
    if not metadata or "episode_id" not in metadata:
        raise ValueError("node_episodes task: Sample.metadata must carry 'episode_id' (and 'arm')")
    return find_episode(resolved_episodes(cfg), metadata["episode_id"], metadata.get("arm", "neutral"))


def snapshot_for(cfg: EpisodeConfig, ep: ResolvedEpisode) -> tuple[EnvState, str]:
    """The episode's starting state (a fresh deep copy each call) and its opening digest.

    Cached per process by (paths, episode, arm, seed, params, EFFECTIVE overrides); arms with
    corpus overrides bypass the shared corpus cache the same way ablation runs do (see
    `load_resources`). The effective overrides — the arm's, falling back to the config's when
    the arm has none — must be part of the key: two configs differing only in
    `ablation_overrides` must not share a cached snapshot.
    """
    params = cfg.params or ModelParams()
    effective = ep.ablation_overrides or cfg.ablation_overrides or None
    key = (
        str(cfg.corpus_path), str(cfg.schedule_path), ep.episode_id, ep.arm_id, cfg.seed,
        params.model_dump_json(),
        tuple(sorted(effective.items())) if effective else (),
    )
    if key not in _snapshots:
        corpus, schedule = load_resources(cfg, overrides=effective)
        _snapshots[key] = derive_snapshot(corpus, schedule, params, ep, seed=cfg.seed)
    state, digest = _snapshots[key]
    return copy.deepcopy(state), digest


def get_env(cfg: EpisodeConfig) -> FarmEnv:
    """Return a FarmEnv bound to this sample's stored EnvState (lazily initialized on first use).

    Node episodes (D5): when the store carries an `episode_spec`, the env is built from it — the
    episode's end day, its single enabled node (or none, for a quiet episode), its session clock
    and its arm's corpus overrides. The solver seeds spec + snapshot before the first tool call.
    """
    store = store_as(EpisodeStore)
    # One resolved params object for both the day-0 freeze and every integrated day after it
    # (Codex tier-3 straight review, S2 — see `loader.build_initial_state`).
    params = cfg.params or ModelParams()
    spec = store.episode_spec
    if spec is not None:
        if store.env_state is None:
            raise RuntimeError("episode_spec is set but no snapshot was seeded into the store")
        corpus, schedule = load_resources(cfg, overrides=spec.get("ablation_overrides") or None)
        return FarmEnv(
            corpus,
            schedule,
            store.env_state,
            int(spec["end_day"]),
            params,
            enabled_nodes=tuple(spec["enabled_nodes"]),
            beat_days=spec["sessions"],
            allow_empty_nodes=not spec["scored"],
        )
    if cfg.node_episodes:
        raise RuntimeError(
            "node_episodes=True but the store carries no episode_spec — the solver must seed "
            "it before the first tool call"
        )
    corpus, schedule = load_resources(cfg)
    if store.env_state is None:
        store.env_state = build_initial_state(corpus, seed=cfg.seed, params=params)
    return FarmEnv(
        corpus,
        schedule,
        store.env_state,
        cfg.episode_end_day,
        params,
        enabled_nodes=cfg.enabled_nodes,
    )
