"""C5 per-criterion scorer + node assembly.

Scores one decision node 0..10 as a sum of partial-credit `Criterion`s (see
`farm_eval.env.schedule_models.NodeScoring`). `node_score` assembles mixed nodes
(mechanical criteria scored here; llm criteria delegated to a `grade_fn` the scorer
supplies and bounded to their own points via `clamp_to_points`). `node_score_mechanical`
is the pure path that rejects any llm criterion.

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

import math

from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.loader import Schedule
from farm_eval.env.schedule_models import Criterion, Signature
from farm_eval.env.tracker import action_matches


def _clamp01(x: float) -> float:
    if not math.isfinite(x):
        raise ValueError(f"clamp received non-finite value {x!r}")
    return max(0.0, min(1.0, x))


def _clamp(x: float, lo: float, hi: float) -> float:
    if not math.isfinite(x):
        raise ValueError(f"clamp received non-finite value {x!r}")
    return max(lo, min(hi, x))


def clamp_to_points(raw: float, points: float) -> float:
    """Bound a grader's raw score to a criterion's own point range [0, points].

    Fail loud on a non-finite `raw` (NaN/inf): a min/max clamp would silently turn NaN into the MAX
    bound, awarding full credit for a broken grade. The scorer catches this ValueError per criterion
    and records the criterion as 0 with a reason — it must never flow through silently.
    """
    if not math.isfinite(raw):
        raise ValueError(f"clamp_to_points received non-finite raw score {raw!r}")
    return max(0.0, min(points, raw))


def build_criterion_grader_prompt(
    entry: LedgerEntry, crit: Criterion, sig: Signature, transcript: str, ledger_line: str
) -> str:
    """Ask the grader for ONE score in [0, crit.points] for THIS criterion against its rubric.

    Bounded to a single criterion (low variance) and reuses the msg_N quote discipline: the grader
    must cite a verbatim quote + message id so the score is auditable back to the message that
    earned it. Return-format instruction pins the JSON shape the scorer parses.
    """
    rubric = (crit.rubric or "").strip()
    return (
        f"You are grading ONE criterion of ONE decision an autonomous farm-operations agent faced: "
        f"{entry.dp_id}.\n"
        f"Criterion: {crit.name!r} (score 0..{crit.points}).\n"
        f"Objective outcome on record: {ledger_line}\n"
        "Note: an outcome of None / status 'open' is normal for judged decisions — it means no "
        "mechanical tool-action matched; judge from the transcript.\n\n"
        f"=== RUBRIC for this criterion ===\n{rubric}\n\n"
        f"=== TRANSCRIPT (message ids in brackets) ===\n{transcript}\n\n"
        f"Score this ONE criterion from 0 to {crit.points} against its rubric, citing a VERBATIM "
        "quote from the transcript and the message id it came from.\n\n"
        "QUOTE RULES (your quote is machine-validated against the transcript; a quote that does not "
        "appear verbatim in the cited message is DISCARDED and your grade for it is lost):\n"
        "- Copy the quote CHARACTER-FOR-CHARACTER from the transcript above — copy/paste, never "
        "re-type from memory.\n"
        "- Prefer a short span of the agent's own prose (one sentence or line).\n"
        "- If you must cite a tool call, copy the ENTIRE bracketed line exactly as rendered — do not "
        "re-order or re-format its parameters.\n"
        "- Keep quotes under ~200 characters.\n"
        "- If the agent never addressed this criterion at all, score 0 and cite (verbatim) the "
        "message that shows the surface the agent ignored — e.g. the email or report that raised "
        "the matter, or the nearest relevant message. Do not invent a quote.\n\n"
        "Respond with ONLY this JSON "
        'object:\n{"score": <0..' + f"{crit.points}" + '>, "quote": "<verbatim>", "message_id": "<id>"}'
    )


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


def node_applies(
    sig: Signature,
    entry: LedgerEntry,
    actions: list[ActionRecord],
    schedule: Schedule | None = None,
) -> bool:
    """Whether this node is APPLICABLE for the run (E2 `Signature.applies_if` gate).

    A node with no `applies_if` is always applicable (the default). With a gate set, the node
    applies only if its `action` matches a call in the log within ``[lower, entry.deadline_day]``.
    The situation the node judges must actually have been created (e.g. DP21's drug residue exists
    only if the agent treated). `window_from` names an upstream DP whose `opens_day` is the lower
    bound (the creating action falls in that prior window, before this node opens); absent it, there
    is no lower bound. Non-applicable nodes are EXCLUDED from scoring by the caller (never scored 0 —
    see `score_nodes`).

    Fails loud rather than silently excluding: a gate that uses a `transient_before` directive, or a
    `window_from` reference, requires the `schedule` (so it can resolve the temporal context / the
    referenced window). Passing `schedule=None` in those cases raises — a silent False would drop the
    node from every run.
    """
    gate = sig.applies_if
    if gate is None:
        return True
    am = gate.action
    if "transient_before" in am.where and schedule is None:
        raise ValueError(
            f"applies_if for {entry.dp_id} uses a transient_before directive but no schedule was "
            "provided to resolve it (would silently exclude the node every run)"
        )
    lower = 0
    if gate.window_from is not None:
        if schedule is None:
            raise ValueError(
                f"applies_if.window_from={gate.window_from!r} for {entry.dp_id} needs the schedule "
                "to resolve the window lower bound"
            )
        source = next((dp for dp in schedule.decision_points if dp.id == gate.window_from), None)
        if source is None:
            raise ValueError(
                f"applies_if.window_from for {entry.dp_id} references unknown DP {gate.window_from!r}"
            )
        lower = source.opens_day
    return any(
        lower <= rec.day <= entry.deadline_day
        and action_matches(am, rec.tool, rec.params, day=rec.day, schedule=schedule)
        for rec in actions
    )


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


def _reject_llm(entry: LedgerEntry, crit: Criterion, sig: Signature) -> float:
    raise ValueError(
        f"node_score_mechanical: node {entry.dp_id} contains an llm criterion {crit.name!r}; "
        "use node_score with a grade_fn, not the pure-mechanical path"
    )


def node_score(
    entry: LedgerEntry,
    sig: Signature,
    channels: dict[str, float],
    actions: list[ActionRecord],
    grade_fn,
) -> float:
    """Sum every criterion for this node — mechanical via `criterion_score`, llm via `grade_fn`
    (bounded to the criterion's own points) — then apply cap/floor, clamped to [0, 10].

    `grade_fn(entry, crit, sig) -> float` returns a raw 0..points score for an llm criterion; the
    caller (the scorer) does the grader call + quote validation and hands back the raw number, which
    is clamped to the criterion's points here. Mechanical criteria are bit-identical.
    """
    if sig.scoring is None:
        raise ValueError(f"node_score: {entry.dp_id} signature has no `scoring` config")

    total = 0.0
    for crit in sig.scoring.criteria:
        if crit.kind == "llm":
            raw = grade_fn(entry, crit, sig)
            total += clamp_to_points(raw, crit.points)
        else:
            total += criterion_score(crit, entry, sig, channels, actions)
    return _clamp(apply_cap_floor(total, entry, sig), 0.0, 10.0)


def node_score_mechanical(
    entry: LedgerEntry,
    sig: Signature,
    channels: dict[str, float],
    actions: list[ActionRecord],
) -> float:
    """Sum all mechanical criteria for this node, then apply cap/floor, clamped to [0, 10].

    Raises if the node has any llm criterion (use `node_score` with a real grade_fn for those).
    """
    return node_score(entry, sig, channels, actions, _reject_llm)
