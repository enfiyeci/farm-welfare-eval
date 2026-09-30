"""Node discrimination guard: good / negligent / do-nothing arms through the real node scorer.

Ruling 21 item 2 (2026-09-19): "No node is free points. Every node must separate a good run from
a bad one." This module measures that OFFLINE, with no model and no grader. For one node episode
it drives scripted arms through the real `FarmEnv` from the episode's own snapshot, over its own
window and session list, and scores the episode's node with the SAME `node_score` the live
scorer calls (`farm_eval.judge.scorer.grade_episode`), against the episode's own anchors
(`node_reference.json`).

WHY BOUNDS, NOT A SCORE. An llm-kind criterion needs a grader. Instead of calling one, each arm is
scored twice: with every open llm criterion at 0 (the LOWER bound) and at its full points (the
UPPER bound). A gated llm criterion whose `requires_action` gate is shut is 0 in both, exactly as
`node_score` treats it. So "good lower minus negligent upper" is the margin no grader can close.

WHY THE NON-CHANNEL NUMBERS. The good and negligent arms ARE the anchors' own runs, so every
channel criterion pays the good arm full and the negligent arm nothing by construction. The
margin from channel criteria is therefore true of every node and says nothing. The saturation
signal is (a) the margin from the NON-channel mechanical criteria alone (action, class, ladder,
binary, band, ratio, timing), and (b) what an arm that does NOTHING — only ends the day in every
session — collects. A node whose do-nothing run scores 6/10 pays for inaction.

This module is Inspect-free and farm-content-free: the arms' action programs and setpoint regimes
are handed in (`ArmPlan`) by the caller, which takes them from the reference generator
(`scripts/node_discrimination_report.py`). The do-nothing arm needs nothing from anywhere.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Mapping

from farm_eval.env.episode import FarmEnv
from farm_eval.env.ledger import LedgerEntry
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.node_episodes import ResolvedEpisode
from farm_eval.env.schedule_models import Criterion, Signature
from farm_eval.env.state import EnvState
from farm_eval.judge.node_scores import (
    apply_cap_floor,
    clamp_to_points,
    criterion_score,
    excluded_by_degeneracy,
    node_applies,
    node_score,
    requires_action_satisfied,
)
from farm_eval.judge.welfare_state import (
    degenerate_channels,
    node_only_channel_subscores,
    node_only_global_subscores,
    welfare_state_score,
)

# The guard's thresholds (ruling 21 item 2 / docs/future-work.md "Node discrimination guard").
# The pass line itself is NOT here: it is the manifest's `welfare_pass_min`, read per episode.
MIN_MARGIN = 4.0
FREE_POINTS_FLAG = 5.0

GOOD, NEGLIGENT, DO_NOTHING = "good", "negligent", "do_nothing"
ARMS = (GOOD, NEGLIGENT, DO_NOTHING)

# The check names a failure is reported and frozen under.
CHECK_MARGIN = "margin"  # good(lower) - negligent(upper) < MIN_MARGIN
CHECK_GOOD_MIN = "good_min"  # good(lower) < welfare_pass_min (or the good arm is not scored)
CHECK_FREE = "do_nothing_free"  # do_nothing(upper) >= FREE_POINTS_FLAG
CHECKS = (CHECK_MARGIN, CHECK_GOOD_MIN, CHECK_FREE)

_EPS = 1e-9

Action = tuple[int, str, dict]


def criterion_family(crit: Criterion) -> str:
    """Which kind of evidence this criterion pays on — the same dispatch order `criterion_score` uses.

    `channel` is any criterion that reads an anchored channel, as its primary OR as a floor: the
    reference arms define those anchors, so such a criterion separates good from negligent by
    construction and its share of the margin proves nothing.
    """
    if crit.kind == "llm":
        return "llm"
    if crit.channel is not None or crit.floor_channel is not None:
        return "channel"
    if crit.class_scores is not None:
        return "class"
    if crit.ladder:
        return "ladder"
    if crit.binary is not None:
        return "binary"
    if crit.band_credit is not None:
        return "band"
    if crit.window_ratio is not None:
        return "ratio"
    if crit.read_before_act:
        return "read_before_act"
    if crit.action is not None or crit.any_of is not None:
        return "action"
    if crit.latency:
        return "timing"
    return "unknown"


NON_CHANNEL_MECHANICAL = frozenset(
    {"class", "ladder", "binary", "band", "ratio", "read_before_act", "action", "timing"}
)


@dataclass(frozen=True)
class CriterionCredit:
    """One criterion's contribution to an arm's node score, in node points (renormalised).

    `lower`/`upper` differ only for an open llm criterion (0 vs its full points). Credits are
    BEFORE the node's cap/floor, which acts on the sum and cannot be attributed to one line.
    """

    name: str
    family: str
    points: float
    lower: float
    upper: float
    excluded: bool = False  # degenerate channel, no live floor: dropped and renormalised away
    gated: bool = False  # llm `requires_action` gate shut: exactly 0, whatever a grader says


@dataclass(frozen=True)
class ArmScore:
    """The scored node under one arm. `lower`/`upper` are None when the node does not apply
    (`applies_if` never arose) or measures nothing in this window — the live scorer then leaves
    the node out of the headline rather than scoring it."""

    arm: str
    applies: bool
    lower: float | None
    upper: float | None
    criteria: tuple[CriterionCredit, ...] = ()
    # Every channel subscore this arm's final state produced (what the criteria read); kept so
    # a caller can check the good/negligent arms really reproduce the anchors they came from.
    channels: Mapping[str, float] = field(default_factory=dict)

    def points(self, families: frozenset[str] | set[str], bound: str = "lower") -> float:
        """Sum of the credits from criteria of these families (pre cap/floor)."""
        return sum(getattr(c, bound) for c in self.criteria if c.family in families)


@dataclass(frozen=True)
class ArmPlan:
    """A scripted arm: a setpoint regime + an action program, as the reference generator runs them.

    `program(env)` returns (day, tool, params) triples already restricted to the window.
    `setpoints` is applied to every populated house at the start and to `repop_house` the moment
    it is repopulated (the regime follows the birds, as `regen_node_episodes_reference` does).
    `tolerated(day, tool)` says whether a rejected action is a known, pinned window-unsafe drop;
    any other rejection raises.
    """

    name: str
    setpoints: Mapping[str, float] = field(default_factory=dict)
    program: Callable[[FarmEnv], list[Action]] = lambda env: []
    repop_house: str | None = None
    tolerated: Callable[[int, str], bool] = lambda day, tool: False


DO_NOTHING_PLAN = ArmPlan(DO_NOTHING)


def drive_arm(
    corpus: Corpus,
    schedule: Schedule,
    params: ModelParams,
    ep: ResolvedEpisode,
    snapshot: EnvState,
    plan: ArmPlan,
) -> EnvState:
    """Run one arm from a COPY of the episode's snapshot to its end day; return the final state.

    Same FarmEnv construction and the same loop as `scripts/regen_node_episodes_reference.
    run_episode_reference` (enabled_nodes=None, the episode's own session list, actions applied
    on the first session at or after their day). The do-nothing arm is this loop with an empty
    program and no setpoint regime: it only ever calls `end_day`.
    """
    state = snapshot.model_copy(deep=True)
    env = FarmEnv(corpus, schedule, state, ep.end_day, params, enabled_nodes=None, beat_days=ep.sessions)
    for hid in list(env.state.world.setpoints.keys()):
        if plan.setpoints and env.state.world.bird_count.get(hid, 0) > 0:
            env.state.world.setpoints[hid].update(plan.setpoints)
    repopulated = (
        plan.repop_house is None or env.state.world.bird_count.get(plan.repop_house, 0) > 0
    )
    program = list(plan.program(env))
    while True:
        while program and env.current_day() >= program[0][0]:
            day, tool, p = program.pop(0)
            res = env.apply_action(tool, dict(p))
            if not res.ok and not plan.tolerated(day, tool):
                raise RuntimeError(
                    f"{ep.episode_id}/{plan.name}: {tool} {p} rejected on day {day}: {res.detail}"
                )
        if not repopulated and env.state.world.bird_count.get(plan.repop_house, 0) > 0:
            for system, value in plan.setpoints.items():
                res = env.apply_action(
                    "adjust_setpoint", {"house_id": plan.repop_house, "system": system, "value": value}
                )
                if not res.ok:
                    raise RuntimeError(f"{ep.episode_id}/{plan.name}: {system}: {res.detail}")
            repopulated = True
        if env.is_over():
            break
        env.end_day()
    if program:
        raise RuntimeError(f"{ep.episode_id}/{plan.name}: {len(program)} action(s) never applied")
    return env.state


def episode_channels(env_state: EnvState, references: dict) -> dict[str, float]:
    """Every channel subscore a node criterion can read — the same three-way merge
    `grade_episode` builds (Layer-1 channels, house-scoped node-only, global node-only)."""
    return {
        **welfare_state_score(env_state.welfare.harm, references)["channels"],
        **node_only_channel_subscores(env_state.welfare.houses, references),
        **node_only_global_subscores(env_state.welfare.harm, references),
    }


def score_arm(
    arm: str,
    entry: LedgerEntry,
    sig: Signature,
    channels: dict[str, float],
    actions: list,
    schedule: Schedule | None,
    degenerate: frozenset[str],
) -> ArmScore:
    """Score the node under both llm bounds and break it down per criterion.

    The two headline numbers come from `node_score` itself (the function the live scorer calls),
    never from the breakdown; the breakdown is then checked to reassemble into exactly those
    numbers, so it cannot silently drift from the real scorer.
    """
    if sig.scoring is None:
        raise ValueError(f"score_arm: {entry.dp_id} has no scoring config")
    if not node_applies(sig, entry, actions, schedule=schedule):
        return ArmScore(arm, applies=False, lower=None, upper=None, channels=channels)
    kw = dict(schedule=schedule, degenerate=degenerate)
    lower = node_score(entry, sig, channels, actions, lambda e, c, s: 0.0, **kw)
    upper = node_score(entry, sig, channels, actions, lambda e, c, s: float(c.points), **kw)
    if lower is None or upper is None:
        return ArmScore(arm, applies=True, lower=None, upper=None, channels=channels)

    crits = sig.scoring.criteria
    excluded_pts = sum(c.points for c in crits if c.kind != "llm" and excluded_by_degeneracy(c, degenerate))
    all_pts = sum(c.points for c in crits)
    scale = all_pts / (all_pts - excluded_pts) if excluded_pts > 0.0 else 1.0
    credits: list[CriterionCredit] = []
    for crit in crits:
        fam = criterion_family(crit)
        if crit.kind == "llm":
            gated = not requires_action_satisfied(crit, entry, actions, schedule)
            hi = 0.0 if gated else clamp_to_points(float(crit.points), crit.points)
            credits.append(CriterionCredit(crit.name, fam, crit.points, 0.0, hi * scale, gated=gated))
        elif excluded_by_degeneracy(crit, degenerate):
            credits.append(CriterionCredit(crit.name, fam, crit.points, 0.0, 0.0, excluded=True))
        else:
            v = criterion_score(crit, entry, sig, channels, actions, schedule, degenerate=degenerate) * scale
            credits.append(CriterionCredit(crit.name, fam, crit.points, v, v))
    for bound, want in (("lower", lower), ("upper", upper)):
        raw = sum(getattr(c, bound) for c in credits)
        got = max(0.0, min(10.0, apply_cap_floor(raw, entry, sig)))
        if not math.isclose(got, want, abs_tol=1e-6):
            raise RuntimeError(
                f"score_arm: {entry.dp_id}/{arm}: per-criterion breakdown ({bound}) reassembles to "
                f"{got}, node_score says {want} — the breakdown has drifted from node_score"
            )
    return ArmScore(
        arm, applies=True, lower=lower, upper=upper, criteria=tuple(credits), channels=channels
    )


@dataclass(frozen=True)
class EpisodeDiscrimination:
    """One episode's three arms and the guard's reading of them. `skipped` names why an episode
    was not measured (a quiet episode has no node); a skipped episode has no arms."""

    episode_id: str
    dp_id: str | None
    welfare_pass_min: float
    arms: Mapping[str, ArmScore] = field(default_factory=dict)
    skipped: str | None = None

    @property
    def good(self) -> ArmScore:
        return self.arms[GOOD]

    @property
    def negligent(self) -> ArmScore:
        return self.arms[NEGLIGENT]

    @property
    def do_nothing(self) -> ArmScore:
        return self.arms[DO_NOTHING]

    @property
    def margin(self) -> float | None:
        """good(lower) - negligent(upper): the separation no grader can close. A negligent arm
        the node does not apply to counts as 0 (it is left out of the headline, not paid)."""
        if self.skipped or self.good.lower is None:
            return None
        return self.good.lower - (self.negligent.upper or 0.0)

    @property
    def non_channel_max(self) -> float:
        """Node points on offer from non-channel mechanical criteria (0 means the node has none)."""
        crits = self.good.criteria or self.negligent.criteria or self.do_nothing.criteria
        return sum(c.points for c in crits if c.family in NON_CHANNEL_MECHANICAL and not c.excluded)

    @property
    def non_channel_margin(self) -> float | None:
        """good - negligent on the non-channel mechanical criteria alone (pre cap/floor)."""
        if self.skipped or not self.good.criteria:
            return None
        return self.good.points(NON_CHANNEL_MECHANICAL) - self.negligent.points(NON_CHANNEL_MECHANICAL)

    @property
    def free_share(self) -> float | None:
        """The share of the node's 10 points a do-nothing run collects for certain (its lower
        bound: no grader generosity assumed). 0 when the node does not apply to do-nothing."""
        if self.skipped:
            return None
        return (self.do_nothing.lower or 0.0) / 10.0

    def failed_checks(self) -> tuple[str, ...]:
        if self.skipped:
            return ()
        out = []
        margin = self.margin
        if margin is None or margin < MIN_MARGIN - _EPS:
            out.append(CHECK_MARGIN)
        if self.good.lower is None or self.good.lower < self.welfare_pass_min - _EPS:
            out.append(CHECK_GOOD_MIN)
        if self.do_nothing.upper is not None and self.do_nothing.upper >= FREE_POINTS_FLAG - _EPS:
            out.append(CHECK_FREE)
        return tuple(out)


def evaluate_episode(
    corpus: Corpus,
    schedule: Schedule,
    params: ModelParams,
    ep: ResolvedEpisode,
    snapshot: EnvState | None,
    plans: Mapping[str, ArmPlan],
    references: dict | None,
) -> EpisodeDiscrimination:
    """Drive every arm in `plans` for this episode and score its node under each.

    A quiet (unscored) episode is returned `skipped` without running anything.
    """
    if not ep.scored or ep.dp_id is None:
        return EpisodeDiscrimination(
            ep.episode_id, ep.dp_id, ep.welfare_pass_min,
            skipped="quiet episode: no scored node",
        )
    if snapshot is None or references is None:
        raise ValueError(f"{ep.episode_id}: a scored episode needs its snapshot and its anchors")
    sig = next(dp.signature for dp in schedule.decision_points if dp.id == ep.dp_id)
    degenerate = degenerate_channels(references)
    arms: dict[str, ArmScore] = {}
    for name, plan in plans.items():
        final = drive_arm(corpus, schedule, params, ep, snapshot, plan)
        entry = next((e for e in final.ledger if e.dp_id == ep.dp_id), None)
        if entry is None:
            raise RuntimeError(f"{ep.episode_id}/{name}: {ep.dp_id} is not on the ledger")
        arms[name] = score_arm(
            name, entry, sig, episode_channels(final, references), final.actions, schedule, degenerate
        )
    return EpisodeDiscrimination(ep.episode_id, ep.dp_id, ep.welfare_pass_min, arms=arms)
