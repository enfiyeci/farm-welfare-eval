"""Price-ladder analysis: does the share of runs that protect the birds change with the price?

Build plan `evals/hen/design/2026-11-15-free-checks/2026-11-16-dp01-price-ladder-build-plan.md`,
step 6. One record per run (model, price level, complete or not, node score, protects, and three
measures reported apart: ventilation lowered, root-cause lever used, raw exposure). Per model and
level: the share that protect with a 95% Wilson interval; per pair of levels: the difference in
that share with a Newcombe (hybrid score) interval built from the two Wilson intervals. No single
switch price is estimated.

Pure, deterministic and content-free: no house, decision, day or price is named here. The
Inspect-touching log reader is `scripts/dp01_price_ladder.py`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations
from statistics import mean

# Two-sided 95% normal quantile (scipy.stats.norm.ppf(0.975)).
Z95 = 1.959963984540054


def wilson_interval(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Wilson score interval for k successes in n trials. n == 0 says nothing: (0, 1)."""
    if n < 0 or k < 0 or k > n:
        raise ValueError(f"need 0 <= k <= n, got k={k}, n={n}")
    if n == 0:
        return 0.0, 1.0
    p = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    centre = (p + z2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1.0 - p) / n + z2 / (4 * n * n)) / denom
    lo = 0.0 if k == 0 else max(0.0, centre - half)
    hi = 1.0 if k == n else min(1.0, centre + half)
    return lo, hi


def newcombe_difference(k1: int, n1: int, k2: int, n2: int, z: float = Z95) -> tuple[float, float, float]:
    """(p1 - p2, lower, upper): Newcombe's hybrid score interval (1998, method 10).

    Built from the two Wilson intervals. With either n == 0 the difference is unknown:
    (nan, -1, 1).
    """
    if n1 == 0 or n2 == 0:
        # Validate the counts all the same, then say nothing.
        wilson_interval(k1, n1, z)
        wilson_interval(k2, n2, z)
        return float("nan"), -1.0, 1.0
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson_interval(k1, n1, z)
    l2, u2 = wilson_interval(k2, n2, z)
    d = p1 - p2
    lower = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    upper = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return d, max(-1.0, lower), min(1.0, upper)


@dataclass(frozen=True)
class LadderRun:
    """One run (sample x epoch) of one episode at one price level."""

    model: str
    episode_id: str
    level: float
    epoch: int
    complete: bool
    score: float | None
    welfare_pass_min: float
    ventilation_lowered: bool | None = None
    root_cause_used: bool | None = None
    raw_exposure: float | None = None
    raw_channel: str | None = None
    sample_id: str = ""
    reason: str | None = None          # why an incomplete run is incomplete

    @property
    def protects(self) -> bool | None:
        """The node score is at or over the episode's own pass line. None for an incomplete run."""
        if not self.complete or self.score is None or not math.isfinite(self.score):
            return None
        return self.score >= self.welfare_pass_min


def ventilation_lowered(
    actions: list[dict],
    start_setpoints: dict[str, dict[str, float]],
    defaults: dict[str, float],
    *,
    system: str,
    start_day: int,
) -> bool:
    """True when any setpoint action in the episode set `system` in some house below the value
    that house had when the episode started (the starting snapshot's setpoint, else the
    placement default). Actions are plain dicts {tool, params, day}, as the log stores them."""
    for action in actions:
        if action.get("tool") != "adjust_setpoint" or int(action.get("day", -1)) < start_day:
            continue
        params = action.get("params") or {}
        if params.get("system") != system:
            continue
        house = params.get("house_id")
        start = (start_setpoints.get(house) or {}).get(system, defaults.get(system))
        try:
            value = float(params.get("value"))
        except (TypeError, ValueError):
            continue
        if start is not None and value < float(start):
            return True
    return False


def root_cause_used(ledger: list[dict], dp_id: str | None) -> bool | None:
    """The scored decision's ledger flag for its upstream root-cause lever (None if not on it)."""
    for entry in ledger:
        if entry.get("dp_id") == dp_id:
            return bool(entry.get("root_cause_used", False))
    return None


def harm_channel(env_state: dict, channel: str | None) -> float | None:
    """A farm-wide harm accumulator from a serialized EnvState, or None if it is not one."""
    if channel is None:
        return None
    value = ((env_state.get("welfare") or {}).get("harm") or {}).get(channel)
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


@dataclass(frozen=True)
class LevelSummary:
    model: str
    episode_id: str
    level: float
    runs: int
    complete: int
    incomplete: tuple[LadderRun, ...]
    protects: int
    share: float
    ci: tuple[float, float]
    ventilation_lowered: int
    ventilation_known: int
    root_cause_used: int
    root_cause_known: int
    raw_mean: float | None
    raw_min: float | None
    raw_max: float | None
    raw_channel: str | None


@dataclass(frozen=True)
class LevelDifference:
    model: str
    episode_id: str
    low: float
    high: float
    diff: float                    # share(high) - share(low)
    ci: tuple[float, float]


def summarize(runs: list[LadderRun]) -> tuple[list[LevelSummary], list[LevelDifference]]:
    """Per (episode, model, level) summaries and, per (episode, model), every pair of levels."""
    groups: dict[tuple[str, str, float], list[LadderRun]] = {}
    for run in runs:
        groups.setdefault((run.episode_id, run.model, float(run.level)), []).append(run)
    summaries: list[LevelSummary] = []
    for (episode_id, model, level), grp in sorted(groups.items()):
        done = [r for r in grp if r.protects is not None]
        k = sum(1 for r in done if r.protects)
        n = len(done)
        vent = [r.ventilation_lowered for r in done if r.ventilation_lowered is not None]
        roots = [r.root_cause_used for r in done if r.root_cause_used is not None]
        raws = [r.raw_exposure for r in done if r.raw_exposure is not None]
        channels = {r.raw_channel for r in done if r.raw_channel}
        summaries.append(LevelSummary(
            model=model, episode_id=episode_id, level=level, runs=len(grp), complete=n,
            incomplete=tuple(r for r in grp if r.protects is None),
            protects=k, share=k / n if n else float("nan"), ci=wilson_interval(k, n),
            ventilation_lowered=sum(vent), ventilation_known=len(vent),
            root_cause_used=sum(roots), root_cause_known=len(roots),
            raw_mean=mean(raws) if raws else None,
            raw_min=min(raws) if raws else None,
            raw_max=max(raws) if raws else None,
            raw_channel=", ".join(sorted(channels)) if channels else None,
        ))
    diffs: list[LevelDifference] = []
    by_pair: dict[tuple[str, str], list[LevelSummary]] = {}
    for s in summaries:
        by_pair.setdefault((s.episode_id, s.model), []).append(s)
    for (episode_id, model), levels in sorted(by_pair.items()):
        for a, b in combinations(sorted(levels, key=lambda s: s.level), 2):
            d, lo, hi = newcombe_difference(b.protects, b.complete, a.protects, a.complete)
            diffs.append(LevelDifference(model, episode_id, a.level, b.level, d, (lo, hi)))
    return summaries, diffs


def _pct(x: float) -> str:
    return "n/a" if not math.isfinite(x) else f"{100 * x:.0f}%"


def _level(x: float) -> str:
    return f"{x:g}x"


def render(summaries: list[LevelSummary], diffs: list[LevelDifference]) -> str:
    lines = [
        "episode | model | level | runs | complete | protect | share (95% Wilson) | "
        "ventilation lowered | root-cause lever used | raw exposure mean [min, max]",
    ]
    for s in summaries:
        raw = (
            "n/a" if s.raw_mean is None
            else f"{s.raw_mean:,.1f} [{s.raw_min:,.1f}, {s.raw_max:,.1f}] ({s.raw_channel})"
        )
        lines.append(
            f"{s.episode_id} | {s.model} | {_level(s.level)} | {s.runs} | {s.complete} | "
            f"{s.protects}/{s.complete} | {_pct(s.share)} ({_pct(s.ci[0])} to {_pct(s.ci[1])}) | "
            f"{s.ventilation_lowered}/{s.ventilation_known} | "
            f"{s.root_cause_used}/{s.root_cause_known} | {raw}"
        )
    if diffs:
        lines.append("")
        lines.append("episode | model | levels | difference in share that protect (95% Newcombe)")
        for d in diffs:
            diff = "n/a" if not math.isfinite(d.diff) else f"{100 * d.diff:+.0f} points"
            lines.append(
                f"{d.episode_id} | {d.model} | {_level(d.high)} minus {_level(d.low)} | "
                f"{diff} ({100 * d.ci[0]:+.0f} to {100 * d.ci[1]:+.0f})"
            )
    incomplete = [r for s in summaries for r in s.incomplete]
    if incomplete:
        lines.append("")
        lines.append(f"incomplete runs (not counted): {len(incomplete)}")
        for r in incomplete:
            lines.append(
                f"{r.episode_id} | {r.model} | {_level(r.level)} | epoch {r.epoch} | "
                f"{r.sample_id} | {r.reason or 'incomplete'}"
            )
    return "\n".join(lines)
