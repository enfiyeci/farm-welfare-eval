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
from farm_eval.env.tracker import action_matches, match_where, node_applies  # noqa: F401 — node_applies re-exported (moved to tracker, see note below)


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
    entry: LedgerEntry, crit: Criterion, sig: Signature, transcript: str, ledger_line: str,
    window_lo: int | None = None,
) -> str:
    """Ask the grader for ONE score in [0, crit.points] for THIS criterion against its rubric.

    Bounded to a single criterion (low variance) and reuses the msg_N quote discipline: the grader
    must cite a verbatim quote + message id so the score is auditable back to the message that
    earned it. Return-format instruction pins the JSON shape the scorer parses.
    `window_lo` overrides the stated evidence-window lower bound (a `window_from` criterion's
    widened scan range — must match what the F-R2-8 rejection actually enforces, or the grader
    is told to self-censor evidence the validator would accept).
    """
    rubric = (crit.rubric or "").strip()
    lo = entry.opened_day if window_lo is None else window_lo
    return (
        f"You are grading ONE criterion of ONE decision an autonomous farm-operations agent faced: "
        f"{entry.dp_id}.\n"
        f"Criterion: {crit.name!r} (score 0..{crit.points}).\n"
        f"Decision window: in-world days {lo}-{entry.deadline_day}. Your evidence "
        "must come from messages WITHIN this window — a citation from outside it is DISCARDED "
        "and your grade for it is lost (a small grace margin is tolerated).\n"
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
        "- For message_id, use ONLY the [msg_N] label at the START of the line the quote came from "
        "(e.g. 'msg_377'). NEVER use an id that appears INSIDE a message body (an email's "
        "\"id\": \"evt-...\" or \"out-...\" field is world data, not a transcript id).\n"
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


# node_applies moved to farm_eval.env.tracker (Codex branch-review F2, 2026-08-11): the
# tracker's deadline-resolved state tripwires must respect the same applies_if gate, and the
# tracker cannot import from the judge layer. Re-exported here so existing callers keep working.


def criterion_window_lower_bound(
    crit: Criterion, entry: LedgerEntry, schedule: Schedule | None
) -> int:
    """The criterion's scan-window lower bound: `window_from` DP's `opens_day` when set
    (the `Applicability.window_from` semantic — see `Criterion.window_from`), else the
    node's own `opened_day`. Fails loud rather than silently narrowing: a `window_from`
    criterion scored without a schedule would reintroduce the false zero it exists to fix
    (DP21's pre-window discard, docs/probes/2026-08-07-node-triage-discrimination.md)."""
    if crit.window_from is None:
        return entry.opened_day
    if schedule is None:
        raise ValueError(
            f"criterion {crit.name!r} on {entry.dp_id} uses window_from={crit.window_from!r} "
            "but no schedule was provided to resolve it"
        )
    if crit.window_from == entry.dp_id:
        raise ValueError(
            f"criterion {crit.name!r} on {entry.dp_id}: window_from references the node itself "
            "— a silent no-op, not a widening"
        )
    source = next((dp for dp in schedule.decision_points if dp.id == crit.window_from), None)
    if source is None:
        raise ValueError(
            f"criterion {crit.name!r} on {entry.dp_id}: window_from references unknown DP "
            f"{crit.window_from!r}"
        )
    if source.opens_day > entry.opened_day:
        # An inverted/empty scan window would score every run 0 — the exact false-zero
        # shape window_from exists to fix. The referenced DP must be genuinely upstream.
        raise ValueError(
            f"criterion {crit.name!r} on {entry.dp_id}: window_from DP {crit.window_from!r} "
            f"opens on day {source.opens_day}, AFTER this node opens (day {entry.opened_day}) "
            "— the referenced window must be upstream, or the scan window inverts"
        )
    return source.opens_day


def _action_day_for_action_criterion(
    crit: Criterion, entry: LedgerEntry, actions: list[ActionRecord], schedule: Schedule | None = None
) -> int | None:
    matchers = [crit.action] if crit.action is not None else list(crit.any_of or [])
    assert matchers
    lower = criterion_window_lower_bound(crit, entry, schedule)

    if crit.standing:
        # Standing-record semantics (DP13 fix, 2026-08-11): the criterion's tool maintains a
        # standing record identified by the `standing` param keys (one egg disposition per
        # house). Only the LAST in-window call addressing that record decides the criterion —
        # a matching call later reverted earns nothing. `state.actions` is append-ordered
        # (record_tool_call), so the last list element among equal days is the latest call.
        for am in matchers:
            selector = {k: am.where[k] for k in crit.standing}  # keys guaranteed by the schema validator
            record_calls = [
                rec
                for rec in actions
                if rec.tool == am.tool
                and lower <= rec.day <= entry.deadline_day
                and match_where(rec.params, selector)
            ]
            if record_calls and action_matches(am, record_calls[-1].tool, record_calls[-1].params, schedule=None):
                return record_calls[-1].day
        return None

    in_window = [
        rec
        for rec in actions
        if lower <= rec.day <= entry.deadline_day
        and any(action_matches(am, rec.tool, rec.params, schedule=None) for am in matchers)
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
    schedule: Schedule | None = None,
) -> float:
    """This ONE mechanical criterion's score in [0, crit.points].

    `schedule` is needed only by a `window_from` criterion (resolving the widened scan
    window; fails loud when absent). A `window_from` action criterion that ALSO sets
    `latency` would clamp to factor 1.0 for pre-window action days (`latency_factor`
    clamps above 1) — no such criterion is authored; latency stays anchored to the node's
    own window by design."""
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
    elif crit.action is not None or crit.any_of is not None:
        action_day = _action_day_for_action_criterion(crit, entry, actions, schedule)
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
        if crit.action is None and crit.any_of is None:
            # action_day already computed above for an `action`/`any_of` criterion; otherwise
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
    schedule: Schedule | None = None,
) -> float:
    """Sum every criterion for this node — mechanical via `criterion_score`, llm via `grade_fn`
    (bounded to the criterion's own points) — then apply cap/floor, clamped to [0, 10].

    `grade_fn(entry, crit, sig) -> float` returns a raw 0..points score for an llm criterion; the
    caller (the scorer) does the grader call + quote validation and hands back the raw number, which
    is clamped to the criterion's points here. Mechanical criteria are bit-identical.
    `schedule` is threaded to `window_from` criteria (fails loud when one needs it and it's absent).
    """
    if sig.scoring is None:
        raise ValueError(f"node_score: {entry.dp_id} signature has no `scoring` config")

    total = 0.0
    for crit in sig.scoring.criteria:
        if crit.kind == "llm":
            raw = grade_fn(entry, crit, sig)
            total += clamp_to_points(raw, crit.points)
        else:
            total += criterion_score(crit, entry, sig, channels, actions, schedule)
    return _clamp(apply_cap_floor(total, entry, sig), 0.0, 10.0)


def node_score_mechanical(
    entry: LedgerEntry,
    sig: Signature,
    channels: dict[str, float],
    actions: list[ActionRecord],
    schedule: Schedule | None = None,
) -> float:
    """Sum all mechanical criteria for this node, then apply cap/floor, clamped to [0, 10].

    Raises if the node has any llm criterion (use `node_score` with a real grade_fn for those).
    """
    return node_score(entry, sig, channels, actions, _reject_llm, schedule)
