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


class EpisodeStore(StoreModel):
    # The mutated, logged episode state. Start-idempotence lives in EnvState.started (so it
    # survives FarmEnv rebinding and retry/replay), not here.
    env_state: EnvState | None = None
    # E7: run-health diagnostic — count of times the solver's max-turns-per-day backstop had to
    # force-advance the day because the target never called end_day. Lives in the adapter store
    # (not EnvState) so the env core stays Inspect-free; persists into the `.eval` log and is read
    # by the scorer into Score.metadata (a diagnostic, not a scored metric).
    forced_advances: int = 0


# Read-only resources, identical across samples — load once, keyed by (corpus_path, schedule_path).
_resources: dict[tuple[str, str], tuple[Corpus, Schedule]] = {}


def load_resources(cfg: EpisodeConfig) -> tuple[Corpus, Schedule]:
    key = (str(cfg.corpus_path), str(cfg.schedule_path))
    if cfg.ablation_overrides:
        # Bypass the cache entirely: an overridden load must never be read from (a stale
        # baseline would silently drop the override) or written to (it would poison later
        # NORMAL loads with the ablated corpus). The cache holds only pristine baselines.
        corpus, schedule = load_corpus(cfg.corpus_path), load_schedule(cfg.schedule_path)
        validate_body_refs(schedule, corpus)
        validate_reply_refs(corpus)
        corpus = apply_overrides(corpus, cfg.ablation_overrides, cfg.corpus_path)
        return corpus, schedule
    if key not in _resources:
        corpus, schedule = load_corpus(cfg.corpus_path), load_schedule(cfg.schedule_path)
        validate_body_refs(schedule, corpus)
        validate_reply_refs(corpus)
        _resources[key] = (corpus, schedule)
    return _resources[key]


def get_env(cfg: EpisodeConfig) -> FarmEnv:
    """Return a FarmEnv bound to this sample's stored EnvState (lazily initialized on first use)."""
    store = store_as(EpisodeStore)
    corpus, schedule = load_resources(cfg)
    # One resolved params object for both the day-0 freeze and every integrated day after it
    # (Codex tier-3 straight review, S2 — see `loader.build_initial_state`).
    params = cfg.params or ModelParams()
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
