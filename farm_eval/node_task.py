"""The node-episode Inspect @task: one sample per (scored decision × arm), k epochs each.

Companion to `farm_task.py` (the continuous 518-day run, unchanged). Every sample starts from the
manifest episode's routine-only snapshot (farm_eval/env/snapshot.py), plays its sessions, and is
scored on its ONE node by `node_welfare_judge`. Roles: `target` drives the agent, `grader` judges.

    inspect eval farm_eval/node_task.py -T config_path=config-nodes.yml \
        --model-role target=<id> --model-role grader=<id> --epochs 5
    inspect eval farm_eval/node_task.py -T config_path=config-nodes.yml -T episode_ids=DP05_RED_MITE,DP04_PHOSPHORUS_RATION ...
"""

from __future__ import annotations

from pathlib import Path

import yaml
from inspect_ai import Task, task
from inspect_ai.dataset import Sample

from farm_eval.adapter.briefing import load_briefing
from farm_eval.adapter.context import EpisodeConfig, resolved_episodes
from farm_eval.adapter.solver.farm_solver import farm_solver
from farm_eval.env.model import ModelParams
from farm_eval.judge.scorer import DIMENSION_MODES, node_welfare_judge

# Registers the spectator dashboard's live feed emitter (the `@hooks` decorator installs the
# class at import time). Inert unless FARM_SPECTATOR_DIR is set -- `SpectatorHooks.enabled()`
# is the gate, and every callback is failure-isolated, so this import cannot affect a run.
import farm_eval.spectator.emitter  # noqa: E402,F401  (registration side effect, inert unless FARM_SPECTATOR_DIR)


# Inspect chdirs into the task file's directory (farm_eval/) while loading AND running a file-based
# task, so a relative `config_path` -- and the relative corpus/schedule/prompt paths inside the
# config -- must be anchored to the repo root, not the cwd. Absolute paths pass through untouched.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_PATH_KEYS = ("corpus_path", "schedule_path", "briefing_path", "dimensions_dir", "node_reference_path")


def _from_root(path: str | Path) -> str:
    p = Path(path)
    return str(p if p.is_absolute() else _REPO_ROOT / p)


def _anchor_paths(cfg: dict) -> dict:
    out = dict(cfg)
    for key in _PATH_KEYS:
        if out.get(key):
            out[key] = _from_root(out[key])
    return out


def _load_config(config_path: str | Path) -> dict:
    return yaml.safe_load(Path(_from_root(config_path)).read_text(encoding="utf-8")) or {}


def _split(csv: str | list[str] | tuple[str, ...] | None) -> set[str] | None:
    """Normalise an episode/arm filter. Inspect parses ``-T episode_ids=a,b`` into a list and
    ``-T episode_ids=a`` into a string; both forms (and an explicit list) must work."""
    if csv is None:
        return None
    items = list(csv) if isinstance(csv, (list, tuple, set)) else str(csv).split(",")
    return {str(s).strip() for s in items if str(s).strip()} or None


@task
def farm_node_task(
    *,
    config_path: str | Path = "config-nodes.yml",
    config: dict | None = None,
    episode_ids: str | None = None,
    arms: str | None = None,
    dimension_mode: str | None = None,
) -> Task:
    cfg = _anchor_paths(config if config is not None else _load_config(config_path))
    effective_dimension_mode = dimension_mode if dimension_mode is not None else cfg.get("dimension_mode", "validity_only")
    if effective_dimension_mode not in DIMENSION_MODES:
        raise ValueError(
            f"dimension_mode must be one of {DIMENSION_MODES}, got {effective_dimension_mode!r}"
        )
    episode = EpisodeConfig(
        corpus_path=cfg["corpus_path"],
        schedule_path=cfg["schedule_path"],
        # Unused under node episodes (each sample's end day comes from the manifest); kept so
        # the dataclass stays one type across both tasks. Must be > every episode end_day.
        episode_end_day=int(cfg.get("episode_end_day", 10_000)),
        seed=int(cfg.get("seed", 0)),
        params=ModelParams(**(cfg.get("model_params") or {})),
        node_episodes=True,
    )
    wanted_eps, wanted_arms = _split(episode_ids), _split(arms)
    briefing = load_briefing(cfg["briefing_path"])
    samples: list[Sample] = []
    for ep in resolved_episodes(episode):
        if wanted_eps is not None and ep.episode_id not in wanted_eps:
            continue
        if wanted_arms is not None and ep.arm_id not in wanted_arms:
            continue
        samples.append(Sample(
            input=briefing,
            id=ep.sample_id,
            metadata={
                "episode_id": ep.episode_id, "arm": ep.arm_id, "dp_id": ep.dp_id,
                "start_day": ep.start_day, "end_day": ep.end_day, "scored": ep.scored,
                "welfare_pass_min": ep.welfare_pass_min,
            },
        ))
    if not samples:
        raise ValueError(f"no node episodes selected (episode_ids={episode_ids!r}, arms={arms!r})")
    return Task(
        dataset=samples,
        solver=farm_solver(episode, max_turns_per_day=int(cfg.get("max_turns_per_day", 30))),
        scorer=node_welfare_judge(
            cfg["dimensions_dir"],
            cfg["schedule_path"],
            samples=int(cfg.get("judge_samples", 1)),
            dimension_mode=effective_dimension_mode,
            node_reference_path=cfg.get("node_reference_path"),
        ),
        epochs=int(cfg.get("epochs", 1)),
        # B4 (k=1 run, 2026-09-22): Inspect's default fail_on_error=True let ONE sample's
        # provider 400 cancel every other in-flight episode. A node sample is a self-contained
        # episode, so an error is isolated to it (logged on the sample, listed by the
        # reliability report) and the rest still run and score. Key absent = False; a float in
        # (0, 1) or a count > 1 restores a threshold. The CLI `--fail-on-error` still overrides.
        fail_on_error=cfg.get("fail_on_error", False),
    )
