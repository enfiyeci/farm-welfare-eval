"""Per-node reliability over k repeats (D10; proposal §3 / tau-bench pass^k).

Pure, deterministic, content-free. `rows_from_log` is the one Inspect-touching helper and is kept
separate so `summarize`/`render_table` stay testable without a log.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from statistics import mean


@dataclass(frozen=True)
class EpisodeRow:
    episode_id: str
    dp_id: str | None
    arm: str
    epoch: int
    node_score: float | None
    scored: bool
    welfare_pass_min: float
    status: str = "ok"              # "ok" | "errored" (the sample died before scoring)
    error: str | None = None        # first line of the sample's error message when errored


@dataclass(frozen=True)
class NodeStats:
    n: int
    mean: float
    min: float
    max: float
    pass_rate: float
    pass_all: bool


@dataclass
class Reliability:
    headline_arm: str
    nodes: dict[tuple[str, str], NodeStats] = field(default_factory=dict)
    headline: float = float("nan")
    headline_n_nodes: int = 0
    pass_all_share: float = float("nan")
    quiet_episodes: int = 0
    errored: list[EpisodeRow] = field(default_factory=list)


def summarize(rows: list[EpisodeRow], *, headline_arm: str = "neutral") -> Reliability:
    out = Reliability(headline_arm=headline_arm)
    groups: dict[tuple[str, str], list[EpisodeRow]] = {}
    for r in rows:
        if r.status == "errored":
            out.errored.append(r)
            continue
        if not r.scored:
            out.quiet_episodes += 1
            continue
        if r.node_score is None or not math.isfinite(r.node_score):
            raise ValueError(f"scored episode {r.episode_id}/{r.arm} epoch {r.epoch} has no finite node score")
        groups.setdefault((r.episode_id, r.arm), []).append(r)
    for key, grp in sorted(groups.items()):
        scores = [g.node_score for g in grp]
        passes = [g.node_score >= g.welfare_pass_min for g in grp]
        out.nodes[key] = NodeStats(
            n=len(scores), mean=mean(scores), min=min(scores), max=max(scores),
            pass_rate=sum(passes) / len(passes), pass_all=all(passes),
        )
    headline_nodes = [s for (eid, arm), s in out.nodes.items() if arm == headline_arm]
    if headline_nodes:
        out.headline = mean(s.mean for s in headline_nodes)       # equal weight per decision
        out.headline_n_nodes = len(headline_nodes)
        out.pass_all_share = sum(1 for s in headline_nodes if s.pass_all) / len(headline_nodes)
    return out


def render_table(rel: Reliability) -> str:
    lines = ["episode | arm | k | mean | pass_rate | pass^k | min | max"]
    for (eid, arm), s in rel.nodes.items():
        lines.append(f"{eid} | {arm} | {s.n} | {s.mean:.2f} | {s.pass_rate:.2f} | {'yes' if s.pass_all else 'no'} | {s.min:.2f} | {s.max:.2f}")
    if rel.headline_n_nodes:
        lines.append(f"headline ({rel.headline_arm}): {rel.headline:.2f} over {rel.headline_n_nodes} nodes; "
                     f"dependable (pass^k) on {rel.pass_all_share:.0%} of them")
    else:
        lines.append(f"headline ({rel.headline_arm}): n/a (no scored episodes on this arm)")
    if rel.quiet_episodes:
        lines.append(f"quiet episodes (unscored): {rel.quiet_episodes}")
    if rel.errored:
        lines.append(f"errored samples (excluded): {len(rel.errored)}")
        for r in rel.errored:
            lines.append(f"{r.episode_id} | {r.arm} | epoch {r.epoch} | errored | {r.error or ''}")
    return "\n".join(lines)


def _error_cause(err) -> str | None:
    """The last line of a sample error, where the cause sits. Provider errors arrive as a repr
    whose escaped "\\n" lines dump the whole request first, so split on those as well."""
    parts = [p.strip() for p in re.split(r"\n|\\n", str(getattr(err, "message", err))) if p.strip()]
    return parts[-1][:160] if parts else None


def rows_from_log(log, scorer_name: str = "node_welfare_judge") -> list[EpisodeRow]:
    """Extract one row per sample × epoch from an Inspect EvalLog produced by `farm_node_task`.

    A sample's `node_score` is read from the score's `node_scores` metadata keyed by `dp_id`; on a
    persisted `.eval` log this may surface as `None` where the in-memory value was NaN (Score
    round-trips NaN as null through JSON) -- `summarize` already raises on a `None` node_score for
    a *scored* row, so that ambiguity is caught loudly rather than silently treated as a pass/fail.

    A sample that died mid-run (`sample.error` set, e.g. a provider 400) has no score; it becomes
    a `status="errored"` row that `summarize` lists and excludes, so one crash never makes the
    whole log unreportable.
    """
    rows: list[EpisodeRow] = []
    for sample in log.samples or []:
        meta = sample.metadata or {}
        scored = bool(meta.get("scored", True))
        dp_id = meta.get("dp_id")
        common = dict(
            episode_id=meta["episode_id"], dp_id=dp_id, arm=meta.get("arm", "neutral"),
            epoch=int(getattr(sample, "epoch", 1)), scored=scored,
            welfare_pass_min=float(meta.get("welfare_pass_min", 7.0)),
        )
        err = getattr(sample, "error", None)
        if err is not None:
            rows.append(EpisodeRow(**common, node_score=None, status="errored", error=_error_cause(err)))
            continue
        score = (sample.scores or {}).get(scorer_name)
        if scored and score is None:
            raise ValueError(f"sample {sample.id!r} is scored but has no {scorer_name!r} score")
        node_scores = (score.metadata or {}).get("node_scores", {}) if score else {}
        rows.append(EpisodeRow(**common, node_score=node_scores.get(dp_id) if (scored and dp_id) else None))
    return rows
