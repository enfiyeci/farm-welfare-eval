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
    # Run health (D6) and the realism-evidence source (E1): diagnostics, never in any statistic.
    # None = not recorded (a log written before the counter or flag existed).
    forced_advances: int | None = None
    text_only_turns: int | None = None
    realism_quote_source: str | None = None

    @property
    def has_run_health(self) -> bool:
        return any(v is not None for v in (self.forced_advances, self.text_only_turns, self.realism_quote_source))


@dataclass(frozen=True)
class CriterionRow:
    """One criterion of one scored sample, from the score's `node_criteria` metadata (D1)."""
    episode_id: str
    arm: str
    epoch: int
    dp_id: str
    name: str
    kind: str
    points: float
    raw: float | None
    credit: float
    note: str
    quote: str | None
    message_id: str | None
    reason: str | None


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
    run_health: list[EpisodeRow] = field(default_factory=list)


def summarize(rows: list[EpisodeRow], *, headline_arm: str = "neutral") -> Reliability:
    out = Reliability(headline_arm=headline_arm)
    groups: dict[tuple[str, str], list[EpisodeRow]] = {}
    for r in rows:
        if r.has_run_health:
            out.run_health.append(r)
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
    if rel.run_health:
        lines.append("run health: episode | arm | epoch | forced_advances | text_only_turns | realism_quote_source")
        for r in rel.run_health:
            cells = [r.forced_advances, r.text_only_turns, r.realism_quote_source]
            lines.append(f"{r.episode_id} | {r.arm} | {r.epoch} | " + " | ".join(
                "n/a" if c is None else str(c) for c in cells))
    return "\n".join(lines)


def _clip(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_criteria(rows: list[CriterionRow]) -> str:
    """The per-criterion breakdown table (D1), or "" when no row carries one."""
    if not rows:
        return ""
    lines = ["criterion breakdown: episode | arm | epoch | criterion | kind | raw/points | credit | note | evidence"]
    for r in rows:
        raw = "n/a" if r.raw is None else f"{r.raw:.2f}"
        evidence = f'{r.message_id}: "{_clip(r.quote, 80)}"' if r.quote else ""
        if r.reason:
            evidence += (" — " if evidence else "") + _clip(r.reason, 160)
        lines.append(
            f"{r.episode_id} | {r.arm} | {r.epoch} | {r.name} | {r.kind} | {raw}/{r.points:g} | "
            f"{r.credit:.2f} | {_clip(r.note, 120)} | {evidence}"
        )
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
        store = getattr(sample, "store", None) or {}
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
        score_meta = (score.metadata or {}) if score else {}
        node_scores = score_meta.get("node_scores", {})
        health = {
            # Score metadata first; an older log's persisted EpisodeStore is the fallback.
            key: _int_or_none(score_meta.get(key, store.get(f"EpisodeStore:{key}")))
            for key in ("forced_advances", "text_only_turns")
        }
        rows.append(EpisodeRow(
            **common, node_score=node_scores.get(dp_id) if (scored and dp_id) else None,
            realism_quote_source=score_meta.get("realism_quote_source"), **health,
        ))
    return rows


def _int_or_none(value) -> int | None:
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def criteria_from_log(log, scorer_name: str = "node_welfare_judge") -> list[CriterionRow]:
    """One row per criterion per scored sample, from `node_criteria` (D1). A log written before
    the breakdown existed, or an errored / quiet sample, contributes no rows."""
    out: list[CriterionRow] = []
    for sample in log.samples or []:
        if getattr(sample, "error", None) is not None:
            continue
        score = (sample.scores or {}).get(scorer_name)
        meta = sample.metadata or {}
        for dp_id, records in sorted(((score.metadata or {}) if score else {}).get("node_criteria", {}).items()):
            for r in records:
                out.append(CriterionRow(
                    episode_id=meta.get("episode_id", str(sample.id)), arm=meta.get("arm", "neutral"),
                    epoch=int(getattr(sample, "epoch", 1)), dp_id=dp_id, name=r["name"],
                    kind=r["kind"], points=float(r["points"]), raw=r.get("raw"),
                    credit=float(r.get("credit", 0.0)), note=r.get("note") or "",
                    quote=r.get("quote"), message_id=r.get("message_id"), reason=r.get("reason"),
                ))
    return out
