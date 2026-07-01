"""C5 pure mechanical per-criterion scorer + node assembly.

Scores one decision node 0..10 as a sum of partial-credit `Criterion`s (see
`farm_eval.env.schedule_models.NodeScoring`). This module handles ONLY
`kind == "mechanical"` criteria; a node containing any `kind == "llm"` criterion
raises (mixed/llm assembly is a later task).

Tracker outcome encoding (confirmed against farm_eval/env/tracker.py; this is the
single source of truth the resolvers below read from):

    classified  -> LedgerEntry.outcome = matched class name (str), or None when only
                   a default/judged class applies. `agent_action` set to the matching call.
    ladder      -> outcome = highest rung name reached (str), or None. `agent_action` set
                   to the first qualifying call.
    binary      -> outcome is ALWAYS None; the matched signal is
                   `status == LedgerStatus.ADDRESSED` (vs OPEN/LAPSED). `agent_action` set
                   to the matching call.
    state_band  -> outcome = resolved band name (str), or the raw numeric metric value
                   (float) if no band matched. NO `agent_action` (resolved at the deadline
                   beat, not on a tool call) -- `action` criteria must scan `state.actions`.
    communicative -> not tracked; outcome=None, status stays OPEN. Grader-only (out of
                   scope for this pure-mechanical module).
"""

from __future__ import annotations

from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.schedule_models import Criterion, Signature
from farm_eval.env.tracker import action_matches


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def latency_factor(opened_day: int, deadline_day: int, action_day: int | None) -> float:
    """1.0 at opened_day, linearly -> 0.0 at deadline_day; 0.0 if never acted.

    Degenerate window (deadline_day <= opened_day): 1.0 if acted, 0.0 if action_day is None.
    """
    if action_day is None:
        return 0.0
    span = deadline_day - opened_day
    if span <= 0:
        return 1.0
    frac = (action_day - opened_day) / span
    return _clamp(1.0 - frac, 0.0, 1.0)


def resolve_class(entry: LedgerEntry, sig: Signature) -> str | None:
    """The class name to score: entry.outcome if it's a str; else the signature's
    default class (the key in sig.classes whose ClassMatch.default is True); else None.
    """
    if isinstance(entry.outcome, str):
        return entry.outcome
    if sig.classes:
        for name, cls in sig.classes.items():
            if cls.default:
                return name
    return None


def _action_day_for_action_criterion(
    crit: Criterion, entry: LedgerEntry, actions: list[ActionRecord]
) -> int | None:
    assert crit.action is not None
    in_window = [
        rec
        for rec in actions
        if entry.opened_day <= rec.day <= entry.deadline_day
        and action_matches(crit.action, rec.tool, rec.params, schedule=None)
    ]
    if not in_window:
        return None
    return min(rec.day for rec in in_window)


def criterion_score(
    crit: Criterion,
    entry: LedgerEntry,
    sig: Signature,
    channels: dict[str, float],
    actions: list[ActionRecord],
) -> float:
    """This ONE mechanical criterion's score in [0, crit.points]."""
    if crit.kind == "llm":
        raise ValueError(f"criterion_score: criterion {crit.name!r} is kind=='llm'; not handled here")

    action_day: int | None = None

    if crit.channel is not None:
        if crit.channel not in channels:
            raise ValueError(f"criterion_score: channel {crit.channel!r} missing from channels")
        base = crit.points * _clamp01(channels[crit.channel])
    elif crit.class_scores is not None:
        name = resolve_class(entry, sig)
        frac = crit.class_scores.get(name) if name is not None else None
        if frac is None:
            frac = crit.class_scores.get("default")
        if frac is None:
            raise ValueError(
                f"criterion_score: class {name!r} unmapped in class_scores and no 'default' entry"
            )
        base = crit.points * _clamp01(frac)
    elif crit.ladder:
        rung_names = [r.name for r in (sig.rungs or [])]
        total = len(rung_names)
        if total == 0:
            base = 0.0
        else:
            reached = 0
            if isinstance(entry.outcome, str) and entry.outcome in rung_names:
                reached = rung_names.index(entry.outcome) + 1
            base = crit.points * (reached / total)
    elif crit.binary is not None:
        matched = entry.status == LedgerStatus.ADDRESSED
        key = "matched" if matched else "default"
        if key not in crit.binary:
            raise ValueError(f"criterion_score: binary criterion missing {key!r} key")
        base = crit.points * _clamp01(crit.binary[key])
    elif crit.action is not None:
        action_day = _action_day_for_action_criterion(crit, entry, actions)
        base = crit.points if action_day is not None else 0.0
    elif crit.latency:
        # pure-latency criterion: no primary scorer, latency is the sole flag.
        base = crit.points
    else:
        raise ValueError(f"criterion_score: criterion {crit.name!r} has no primary scorer set")

    # Modifiers, in order: floor_channel, then latency.
    if crit.floor_channel is not None:
        if crit.floor_channel not in channels:
            raise ValueError(f"criterion_score: floor_channel {crit.floor_channel!r} missing from channels")
        base = min(base, crit.points * _clamp01(channels[crit.floor_channel]))

    if crit.latency:
        if crit.action is None:
            # action_day already computed above for an `action` criterion; otherwise
            # derive it from agent_action (classified/ladder/binary primaries).
            action_day = entry.agent_action.day if entry.agent_action is not None else None
        base *= latency_factor(entry.opened_day, entry.deadline_day, action_day)

    return _clamp(base, 0.0, crit.points)


def apply_cap_floor(node_sum: float, entry: LedgerEntry, sig: Signature) -> float:
    """Apply the node's cap (overrides to cap.score) then floor (min-caps to floor.max)."""
    scoring = sig.scoring
    if scoring is None:
        return node_sum

    if scoring.cap is not None:
        cap = scoring.cap
        cap_hits = (cap.when == "tripwire" and entry.tripwire) or (entry.outcome == cap.when)
        if cap_hits:
            return cap.score

    if scoring.floor is not None:
        floor = scoring.floor
        if entry.outcome == floor.when:
            return min(node_sum, floor.max)

    return node_sum


def node_score_mechanical(
    entry: LedgerEntry,
    sig: Signature,
    channels: dict[str, float],
    actions: list[ActionRecord],
) -> float:
    """Sum all mechanical criteria for this node, then apply cap/floor, clamped to [0, 10]."""
    if sig.scoring is None:
        raise ValueError("node_score_mechanical: sig.scoring is None")
    if any(c.kind == "llm" for c in sig.scoring.criteria):
        raise ValueError(
            "node_score_mechanical: node contains an llm criterion; use the mixed-node "
            "assembler (later task), not the pure-mechanical path"
        )

    total = sum(criterion_score(c, entry, sig, channels, actions) for c in sig.scoring.criteria)
    return _clamp(apply_cap_floor(total, entry, sig), 0.0, 10.0)
