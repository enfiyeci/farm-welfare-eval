"""B7 — the Inspect @task: one sample (the neutral briefing), the farm solver, the welfare judge.

Model swapping is via Inspect model roles at eval time (`--model-role target=...`,
`--model-role grader=...`); the solver reads role "target" and the judge reads role "grader".
The single fixed environment is one sample; epochs run the same env against the target N times.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from inspect_ai import Task, task
from inspect_ai.dataset import Sample

from farm_eval.adapter.briefing import load_briefing
from farm_eval.adapter.context import EpisodeConfig
from farm_eval.adapter.solver.farm_solver import farm_solver
from farm_eval.env.model import ModelParams
from farm_eval.judge.scorer import welfare_judge

# Registers the spectator dashboard's live feed emitter (the `@hooks` decorator installs the
# class at import time). Inert unless FARM_SPECTATOR_DIR is set -- `SpectatorHooks.enabled()`
# is the gate, and every callback is failure-isolated, so this import cannot affect a run.
import farm_eval.spectator.emitter  # noqa: E402,F401  (import order: registration side effect)


def _load_config(config_path: str | Path) -> dict:
    return yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}


@task
def farm_task(*, config_path: str | Path = "config.yml", config: dict | None = None) -> Task:
    cfg = config if config is not None else _load_config(config_path)
    episode = EpisodeConfig(
        corpus_path=cfg["corpus_path"],
        schedule_path=cfg["schedule_path"],
        episode_end_day=int(cfg["episode_end_day"]),
        seed=int(cfg.get("seed", 0)),
        params=ModelParams(**(cfg.get("model_params") or {})),
        # Distinguish "key absent" (-> None, all nodes) from "present but empty" (-> (), which
        # FarmEnv rejects loudly): an empty selection is a config mistake, not "all nodes".
        enabled_nodes=(
            tuple(cfg["enabled_nodes"]) if cfg.get("enabled_nodes") is not None else None
        ),
        # D2: opt-in per-beat checkpointing. Key-absent / null = off (no behavior change).
        checkpoint_dir=cfg.get("checkpoint_dir"),
        ablation_overrides=(dict(cfg["ablation_overrides"]) if cfg.get("ablation_overrides") else None),
        # L8: key absent -> None -> the corpus decides; an explicit false runs the whole-axis-off
        # ablation. Threaded the same way episode_end_day is, so the documented ablation is
        # actually reachable from config instead of being an unwired parameter.
        finance_enabled=(
            bool(cfg["finance_enabled"]) if cfg.get("finance_enabled") is not None else None
        ),
    )
    briefing = load_briefing(cfg["briefing_path"])
    return Task(
        dataset=[Sample(input=briefing)],
        solver=farm_solver(episode, max_turns_per_day=int(cfg.get("max_turns_per_day", 30))),
        scorer=welfare_judge(
            cfg["dimensions_dir"],
            cfg["schedule_path"],
            samples=int(cfg.get("judge_samples", 3)),
            episode_end_day=int(cfg["episode_end_day"]),
            # EXPERIMENTAL stamp: ablation runs automatically, plus any config that opts in
            # (e.g. the goal-prefixed 2x2 corner baselines) — never comparable-sweep data.
            experimental=bool(cfg.get("ablation_overrides")) or bool(cfg.get("experimental")),
            # L8 finance index (score METADATA only, never the welfare headline). The anchors
            # themselves are loaded once inside the scorer from finance_reference.json.
            finance_weights=(dict(cfg["finance_weights"]) if cfg.get("finance_weights") else None),
            finance_lambda=float(cfg.get("finance_lambda", 0.5)),
        ),
        epochs=int(cfg.get("epochs", 1)),
    )
