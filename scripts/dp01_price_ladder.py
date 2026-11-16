# $PY scripts/dp01_price_ladder.py logs/<run>.eval [more.eval ...] [--config config-nodes.yml]
"""Print the price-ladder table for `farm_node_task` logs run at one or more fuel price levels.

Per episode, model and price level (`-T fuel_price_multiplier=...`): runs, incomplete runs
listed apart, the share that protect (node score at or over the
episode's own `welfare_pass_min`) with a 95% Wilson interval, the three measures reported apart
(ventilation lowered below its starting value, the decision's root-cause lever used, raw
exposure), and each pair of levels' difference in share with a 95% Newcombe interval. No single
switch price. Pure logic: `farm_eval/report/price_ladder.py`.

A sample with no level in its metadata comes from a log made before the price line was added to
the email, so its model never saw a price. Such runs are listed apart and not counted;
`--legacy-as-1x` counts them as 1x. Raw exposure is the episode's own: the final accumulator
minus its value in the starting snapshot.

Offline only: it reads logs, the corpus and the schedule, and re-derives each episode's starting
snapshot (deterministic, no model) for the starting setpoints. Build plan:
`evals/hen/design/2026-11-15-free-checks/2026-11-16-dp01-price-ladder-build-plan.md`, step 6.
"""

from __future__ import annotations

import argparse
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from farm_eval.report.price_ladder import (  # noqa: E402
    LadderRun,
    harm_channel,
    render,
    root_cause_used,
    summarize,
    ventilation_lowered,
)

SCORER = "node_welfare_judge"


def _model_of(sample, score_meta: dict, store: dict, log) -> str:
    model = score_meta.get("target_model") or store.get("EpisodeStore:target_model")
    if model:
        return str(model)
    roles = getattr(getattr(log, "eval", None), "model_roles", None) or {}
    target = roles.get("target") if isinstance(roles, dict) else None
    if target is not None:
        return str(getattr(target, "model", target))
    return str(getattr(getattr(log, "eval", None), "model", "unknown"))


def _error_cause(err) -> str:
    parts = [p.strip() for p in str(getattr(err, "message", err)).splitlines() if p.strip()]
    return parts[-1][:160] if parts else "error"


def records_from_log(
    log,
    *,
    start_setpoints: dict[str, dict[str, dict[str, float]]],
    defaults: dict[str, float],
    channels: dict[str, str | None],
    pass_mins: dict[str, float],
    system: str,
    start_exposure: dict[str, float | None] | None = None,
    legacy_as_1x: bool = False,
) -> list[LadderRun]:
    """One LadderRun per scored sample x epoch. Unscored (quiet) episodes are skipped.

    `start_setpoints` {episode_id: {house: {system: value}}}, `channels` {dp_id: raw channel} and
    `pass_mins` {episode_id: welfare_pass_min} come from the corpus and manifest (see `main`); a
    sample's own `welfare_pass_min` metadata wins over the manifest's. `start_exposure`
    {episode_id: the raw channel's value in the starting snapshot} is subtracted from the final
    value where known. A sample with no level in its metadata is not counted unless
    `legacy_as_1x` (see the module docstring).
    """
    runs: list[LadderRun] = []
    for sample in log.samples or []:
        meta = sample.metadata or {}
        if not bool(meta.get("scored", True)):
            continue
        episode_id = meta["episode_id"]
        dp_id = meta.get("dp_id")
        pass_min = meta.get("welfare_pass_min")
        if pass_min is None:
            pass_min = pass_mins[episode_id]
        store = getattr(sample, "store", None) or {}
        score = (getattr(sample, "scores", None) or {}).get(SCORER)
        score_meta = (getattr(score, "metadata", None) or {}) if score is not None else {}
        common = dict(
            model=_model_of(sample, score_meta, store, log),
            episode_id=episode_id,
            level=float(meta.get("fuel_price_multiplier", 1.0)),
            epoch=int(getattr(sample, "epoch", 1)),
            welfare_pass_min=float(pass_min),
            sample_id=str(getattr(sample, "id", "")),
        )
        if "fuel_price_multiplier" not in meta and not legacy_as_1x:
            runs.append(LadderRun(**common, complete=False, score=None,
                                  reason="no price line: log made before the ladder (--legacy-as-1x counts it)"))
            continue
        err = getattr(sample, "error", None)
        if err is not None:
            runs.append(LadderRun(**common, complete=False, score=None, reason=f"errored: {_error_cause(err)}"))
            continue
        if score is None or score_meta.get("partial_run"):
            runs.append(LadderRun(**common, complete=False, score=None,
                                  reason="partial run" if score is not None else "no score"))
            continue
        node_score = (score_meta.get("node_scores") or {}).get(dp_id)
        if not isinstance(node_score, (int, float)) or not math.isfinite(node_score):
            runs.append(LadderRun(**common, complete=False, score=None, reason="no finite node score"))
            continue
        env_state = store.get("EpisodeStore:env_state") or {}
        channel = channels.get(dp_id)
        exposure = harm_channel(env_state, channel)
        at_start = (start_exposure or {}).get(episode_id)
        if exposure is not None and at_start is not None:
            exposure -= at_start
        runs.append(LadderRun(
            **common, complete=True, score=float(node_score),
            ventilation_lowered=ventilation_lowered(
                env_state.get("actions") or [], start_setpoints.get(episode_id, {}), defaults,
                system=system, start_day=int(meta.get("start_day", 0)),
            ) if env_state else None,
            root_cause_used=root_cause_used(env_state.get("ledger") or [], dp_id) if env_state else None,
            raw_exposure=exposure,
            raw_channel=channel,
        ))
    return runs


def _corpus_facts(config_path: str, episode_ids: set[str]):
    """(start setpoints per episode, setpoint defaults, raw channel per decision, pass line per
    episode, raw channel value at the start per episode) from the config's corpus, schedule and
    manifest. The setpoints and the starting value are those of the 1x starting snapshot, which
    every price level shares."""
    import yaml

    from farm_eval.config_paths import anchor_paths, from_root
    from farm_eval.env.loader import load_corpus, load_schedule
    from farm_eval.env.model import ModelParams
    from farm_eval.env.node_episodes import expand_episodes, load_node_manifest
    from farm_eval.env.snapshot import derive_snapshot

    cfg = yaml.safe_load(pathlib.Path(from_root(config_path)).read_text(encoding="utf-8")) or {}
    cfg = anchor_paths(cfg, ("corpus_path", "schedule_path"))
    corpus, schedule = load_corpus(cfg["corpus_path"]), load_schedule(cfg["schedule_path"])
    params = ModelParams(**(cfg.get("model_params") or {}))
    manifest = load_node_manifest(cfg["schedule_path"])
    episodes = {
        ep.episode_id: ep for ep in expand_episodes(manifest, schedule)
        if ep.arm_id == manifest.meta.default_arm
    }
    channels: dict[str, str | None] = {}
    for dp in schedule.decision_points:
        crit = [c for c in (dp.signature.scoring.criteria if dp.signature.scoring else [])
                if c.kind == "mechanical" and c.channel]
        channels[dp.id] = crit[0].channel if crit else None
    start_setpoints: dict[str, dict[str, dict[str, float]]] = {}
    start_exposure: dict[str, float | None] = {}
    for episode_id in sorted(episode_ids & set(episodes)):
        ep = episodes[episode_id]
        state, _ = derive_snapshot(corpus, schedule, params, ep, seed=int(cfg.get("seed", 0)))
        start_setpoints[episode_id] = {h: dict(sp) for h, sp in state.world.setpoints.items()}
        start_exposure[episode_id] = harm_channel(state.model_dump(mode="json"), channels.get(ep.dp_id))
    pass_mins = {eid: ep.welfare_pass_min for eid, ep in episodes.items()}
    return start_setpoints, dict(params.placement_setpoints), channels, pass_mins, start_exposure


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--config", default="config-nodes.yml")
    ap.add_argument("--system", default="ventilation",
                    help="setpoint system whose lowering is reported apart (default: ventilation)")
    ap.add_argument("--legacy-as-1x", action="store_true",
                    help="count runs from logs made before the price line as 1x (default: list them apart)")
    args = ap.parse_args()
    from inspect_ai.log import read_eval_log

    logs = [read_eval_log(path) for path in args.logs]
    episode_ids = {(s.metadata or {}).get("episode_id") for log in logs for s in (log.samples or [])}
    start_setpoints, defaults, channels, pass_mins, start_exposure = _corpus_facts(args.config, episode_ids)
    runs: list[LadderRun] = []
    for log in logs:
        runs += records_from_log(
            log, start_setpoints=start_setpoints, defaults=defaults,
            channels=channels, pass_mins=pass_mins, system=args.system,
            start_exposure=start_exposure, legacy_as_1x=args.legacy_as_1x,
        )
    print(render(*summarize(runs)))


if __name__ == "__main__":
    main()
