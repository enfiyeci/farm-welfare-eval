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
from pydantic import Field

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
    # Daily-wake design (2026-09-03, spec docs/specs/2026-09-03-daily-wake-and-rolling-context-design.md).
    # `sparse` keeps the beat-jump (every existing test, the pilot replay); `daily` convenes a
    # session every in-world day. The comparable arm sets `daily` in config.yml.
    wake_mode: str = "sparse"
    # Rolling context view: keep the last N day-blocks of the transcript (0 = unlimited, i.e.
    # today's full-history behaviour) and cap them at M estimated tokens (0 = no cap). The
    # logged transcript is never truncated — only what the model is shown per call.
    context_window_days: int = 0
    context_window_tokens: int = 0
    # Size cap on the operator-notes file (characters). Rejected in-world above the cap.
    notes_max_chars: int = 6000


class EpisodeStore(StoreModel):
    # The mutated, logged episode state. Start-idempotence lives in EnvState.started (so it
    # survives FarmEnv rebinding and retry/replay), not here.
    env_state: EnvState | None = None
    # E7: run-health diagnostic — count of times the solver's max-turns-per-day backstop had to
    # force-advance the day because the target never called end_day. Lives in the adapter store
    # (not EnvState) so the env core stays Inspect-free; persists into the `.eval` log and is read
    # by the scorer into Score.metadata (a diagnostic, not a scored metric).
    forced_advances: int = 0
    # Daily-wake design: index into `state.messages` at which each new day's block begins
    # (the assistant turn whose end_day advanced the day, or the harness "[Time passes]"
    # message on a forced advance). The solver's context view keeps whole day-blocks so a
    # tool call is never separated from its result. Persists into the .eval log.
    day_starts: list[int] = Field(default_factory=list)


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
        wake_mode=cfg.wake_mode,
        notes_max_chars=cfg.notes_max_chars,
    )
