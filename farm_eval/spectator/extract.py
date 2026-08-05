"""Replay extractor: a recorded `.eval` log becomes one spectator feed per sample.

This is the post-hoc half of the spectator's two entry points. It replays a finished run's
transcript events through the SAME `Translator` the live hooks emitter drives (spec §2), so a
feed extracted from an `.eval` is identical to the feed that run emitted live -- which is what
makes the viewer page a single implementation rather than two.

    extract_feed("logs/2026-…_farm-task_….eval", Path("spectator"))
    # -> [Path("spectator/<run_id>/<sample_uuid>/feed.ndjson")]

Three things here are contracts rather than choices.

**`resolve_attachments=True` is mandatory.** Inspect stores long message content out of line and
leaves an `attachment://…` reference in the event; replaying an unresolved log would put those
URIs in the feed where live mode has real prose. That is a silent live-vs-replay divergence -- the
feed still parses, the page still renders -- so it is pinned by a test rather than left to care.

**The sample identifier is `EvalSample.uuid`, never `.id`.** The live emitter only ever sees the
uuid (Inspect's sample hooks carry it), so the uuid is the sole identifier both paths share. It
names the feed's directory and travels in `RunMeta.sample_id`.

**`enabled_nodes` is read from the task config recorded in the log**, never counted from the feed.
A node whose window never opens -- a disabled node, a run that stopped early, a `state_band`
resolved after the last beat -- emits no `decision_window` line, so a feed-derived count silently
under-reports the run's node spine, which is exactly the denominator the page scores against.

## Reconstructing day 0

`Translator` needs the day-0 `EnvState` its recorded `StoreEvent` patches are diffed against. That
baseline is the state AFTER `FarmEnv.start()`: Inspect records no store event for the day-0 event
firing, so the first recorded change is already a nested pointer into a mailbox that start() has
filled (e.g. `replace /EpisodeStore:env_state/mailbox/0/unread`). `started_env` therefore builds
the state through the env core's own entry point (`FarmEnv.from_paths`, the same loader,
seed, params, node selection and ablation overrides the run used, from the run's own recorded
config) and calls `start()` before dumping it.

## Failure policy

Nothing here is caught. A log whose patches do not apply, or whose config no longer resolves, is a
corrupt or mismatched input, and a feed reconstructed from half of it would be quietly wrong for
every day after the break -- so extraction fails loudly instead. (The LIVE emitter is the opposite:
it must never take a run down, so it wraps its own translation. Replay has no run to protect.)
"""

from __future__ import annotations

from pathlib import Path

import yaml
from inspect_ai.log import EvalLog, EvalSample, EvalSpec, read_eval_log

from farm_eval.env.episode import FarmEnv
from farm_eval.env.model import ModelParams
from farm_eval.spectator.events import RunMeta, dump_feed_line
from farm_eval.spectator.translate import Translator

#: Per-sample feed file name, under `<out_dir>/<run_id>/<sample_uuid>/`.
FEED_FILENAME = "feed.ndjson"

#: `RunMeta.config_path` when the run was launched with an inline `config=` task argument (as the
#: test suite does) rather than a config FILE -- naming the unused `config_path` default would
#: claim the run read a file it never opened.
INLINE_CONFIG_LABEL = "<task_args.config>"


def resolve_task_config(spec: EvalSpec) -> tuple[dict, str]:
    """The task config this run actually used, plus a display path for it.

    Mirrors `farm_task`'s own resolution: an inline `config` dict wins over `config_path`, which
    Inspect records with its default value even when it was never used. A recorded `config_path`
    is used exactly as recorded -- typically relative, so extraction must run from the same working
    directory the eval did (and fails loudly with the missing path if it does not).
    """
    args = spec.task_args or {}
    inline = args.get("config")
    if inline is not None:
        return dict(inline), INLINE_CONFIG_LABEL
    config_path = args.get("config_path")
    if not config_path:
        raise ValueError(
            "eval log records no task config: expected task_args to carry `config` or "
            f"`config_path` (got keys {sorted(args)})"
        )
    config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}
    return config, str(config_path)


def started_env(config: dict) -> FarmEnv:
    """A `FarmEnv` holding the day-0 state the recorded store patches are diffed against.

    `start()` is applied: see "Reconstructing day 0" in the module docstring.
    """
    env = FarmEnv.from_paths(
        config["corpus_path"],
        config["schedule_path"],
        seed=int(config.get("seed", 0)),
        episode_end_day=int(config["episode_end_day"]),
        params=ModelParams(**(config.get("model_params") or {})),
        # Key absent / null = every node enabled; an empty list is a config mistake FarmEnv
        # rejects loudly. Same distinction `farm_task` draws.
        enabled_nodes=(
            tuple(config["enabled_nodes"]) if config.get("enabled_nodes") is not None else None
        ),
        ablation_overrides=(
            dict(config["ablation_overrides"]) if config.get("ablation_overrides") else None
        ),
    )
    env.start()
    return env


def _role_model(spec: EvalSpec, role: str) -> str:
    """The model bound to *role*, falling back to the eval's own model when unbound."""
    bound = (spec.model_roles or {}).get(role)
    if bound is None:
        return spec.model
    # Inspect records roles as `ModelConfig`; tolerate a plain model string too.
    return bound if isinstance(bound, str) else bound.model


def build_run_meta(spec: EvalSpec, *, sample_id: str, config_path: str, env: FarmEnv) -> RunMeta:
    """The feed's head line: what run this is and how the page should scale its charts.

    `seq` is a placeholder -- `Translator` owns the envelope and re-stamps it. `day`/`ts_in_world`
    stay unset: run metadata belongs to no day.
    """
    params = env.params
    return RunMeta(
        seq=0,
        run_id=spec.run_id,
        sample_id=sample_id,
        target=_role_model(spec, "target"),
        grader=_role_model(spec, "grader"),
        first_day=env.state.day_index,
        last_day=env.episode_end_day,
        config_path=config_path,
        enabled_nodes=(
            len(env.enabled_nodes)
            if env.enabled_nodes is not None
            else len(env.schedule.decision_points)
        ),
        breed_standard=list(zip(params.breed_age_wk, params.breed_hdep)),
        breed_label=params.breed_label,
    )


def make_translator(spec: EvalSpec, sample_id: str) -> Translator:
    """A `Translator` primed for one sample of *spec*: run metadata plus the day-0 state.

    The single seam for building a translator from an eval spec, so the live emitter and this
    replay path cannot disagree about the head of the feed.
    """
    config, config_path = resolve_task_config(spec)
    env = started_env(config)
    meta = build_run_meta(spec, sample_id=sample_id, config_path=config_path, env=env)
    return Translator(meta=meta, initial_state=env.state.model_dump(mode="json"))


def _sample_status(log: EvalLog, sample: EvalSample) -> str:
    """`EpisodeEnd.status` for one sample: its own error outranks the run's status."""
    return "error" if sample.error is not None else log.status


def _write_sample_feed(log: EvalLog, sample: EvalSample, out_dir: Path) -> Path:
    if not sample.uuid:
        raise ValueError(
            f"sample {sample.id!r} (epoch {sample.epoch}) has no uuid; the spectator feed is "
            "keyed by sample uuid, so this log cannot be extracted"
        )
    translator = make_translator(log.eval, sample.uuid)
    status = _sample_status(log, sample)
    lines: list[str] = []
    for event in sample.events or []:
        lines += [dump_feed_line(feed_event) for feed_event in translator.handle(event)]
    lines += [dump_feed_line(feed_event) for feed_event in translator.finish(status)]
    path = out_dir / log.eval.run_id / sample.uuid / FEED_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def extract_feed(log_path: str | Path, out_dir: Path) -> list[Path]:
    """Write one spectator feed per sample of the `.eval` log at *log_path*.

    Returns the feed paths in sample order, each `<out_dir>/<run_id>/<sample_uuid>/feed.ndjson`.
    """
    log = read_eval_log(str(log_path), resolve_attachments=True)
    if log.samples is None:
        raise ValueError(
            f"eval log carries no samples (header only?): {log_path} -- nothing to extract"
        )
    out_dir = Path(out_dir)
    return [_write_sample_feed(log, sample, out_dir) for sample in log.samples]
