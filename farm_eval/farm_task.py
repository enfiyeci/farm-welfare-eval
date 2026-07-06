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
        ),
        epochs=int(cfg.get("epochs", 1)),
    )
