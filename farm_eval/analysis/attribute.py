"""Strength-tiered attribution of agent events to decision-point windows (design §3.2).

Three tiers, and the distinction between them is the whole point of the module:

- **strong** — the event IS this node's behaviour. For a state-changing ACTION that means the
  call matches one of the signature's own `ActionMatch`es, or IS the ledger entry's recorded
  `agent_action`; a bare same-house coincidence is deliberately NOT strong (a routine mite
  treatment inside an ammonia window is not ammonia behaviour). For a READ it means the
  tracker's own recognition semantics would count it for this node (`inspect_surface`:
  farm-wide `"any"`, an explicit house list, or the derived single house).
- **ambient** — in-window context only: an action on the node's house that matches nothing, a
  read the tracker would not count, an outbound email that no `send_email` matcher claims.
  Recorded so a dossier can show what else was happening; NEVER treated as accounted-for.
- **off-node** — every event with NO strong attribution to ANY node (ambient does not count).
  This is the honest complement the eval exists to expose: a window must not be able to swallow
  an unrelated email or an out-of-frame recap that merely lands on an overlapping day.

One event may attribute strongly to several overlapping nodes. Nothing here is farm-specific:
houses, tools and matchers all come from the loaded schedule and the recorded run.
"""

from __future__ import annotations

from typing import Any

from farm_eval.analysis.model import Attribution, BehaviourEvent, Strength
from farm_eval.env.loader import Schedule
from farm_eval.env.schedule_models import ActionMatch, Signature
from farm_eval.env.tracker import _READ_TOOLS, inspect_surface_house, match_where

# Email row keys carried onto the event's `params`. The body is deliberately excluded: the
# behaviour model is a committed JSON artifact and a full mail body per event would bloat it
# (the digest stage carries prose).
_EMAIL_PARAM_KEYS = ("id", "to", "cc", "subject", "in_reply_to")

_SUMMARY_VALUE_CHARS = 60


def _signature_matchers(sig: Signature) -> list[ActionMatch]:
    """Every `ActionMatch` the signature declares as this node's own behaviour.

    Collected from `any_of`, every class's `any_of`/`all_of`, every ladder rung, `root_cause`,
    and the C5 scoring criteria's action matchers (`action` and its OR-form `any_of` — the same
    action-family primary scorer, so both are node behaviour). `applies_if` is excluded on
    purpose: its matcher describes the situation-creating act, which legitimately falls in an
    UPSTREAM node's window and is that node's behaviour, not this one's.
    """
    matchers: list[ActionMatch] = list(sig.any_of)
    for cls in (sig.classes or {}).values():
        matchers += list(cls.any_of) + list(cls.all_of)
    for rung in sig.rungs or []:
        matchers.append(rung.match)
    if sig.root_cause is not None:
        matchers.append(sig.root_cause)
    if sig.scoring is not None:
        for criterion in sig.scoring.criteria:
            if criterion.action is not None:
                matchers.append(criterion.action)
            matchers += list(criterion.any_of or [])
    return matchers


def _matcher_hits(am: ActionMatch, tool: str, params: dict) -> bool:
    """Tool identity + a `match_where` subset match on the matcher's params.

    `transient_before` is stripped: it is a tracker temporal directive (was this raise shortly
    before an audit?), not an action param. Attribution asks "is this call this node's
    behaviour", which the temporal condition does not change — a pre-audit ventilation raise is
    ventilation behaviour whether or not the audit-window condition holds. (`match_where`
    already skips the key; stripping it here states the intent at the call site.)
    """
    if am.tool != tool:
        return False
    return match_where(params, {k: v for k, v in am.where.items() if k != "transient_before"})


def _is_recorded_agent_action(tool: str, params: dict, day: int | None, agent_action: Any) -> bool:
    """The row IS the ledger's recorded `agent_action` (same tool, day and params)."""
    if not isinstance(agent_action, dict):
        return False
    return (
        agent_action.get("tool") == tool
        and agent_action.get("day") == day
        and (agent_action.get("params") or {}) == params
    )


def _read_surface(sig: Signature) -> tuple[Any, str | None]:
    """This node's read surface, resolved once per node: `(inspect_surface, derived house)`.

    The derivation is only consulted when the signature declares no explicit surface, so it is
    computed only then (it walks every matcher).
    """
    surface = sig.inspect_surface
    return surface, inspect_surface_house(sig) if surface is None else None


def _surface_accepts(house: Any, surface: Any, derived: str | None) -> bool:
    """Would the tracker count a read of `house` as inspecting this node's welfare surface?

    Mirrors `tracker.resolve_inspected`: an explicit `inspect_surface` overrides the derivation
    (`"any"` = any house read at all; a list = membership), otherwise the single house derived
    by `inspect_surface_house` must match (None -> nothing qualifies). A read without a string
    `house_id` never qualifies, exactly as `tracker._qualifying_read_houses` requires.
    """
    if not isinstance(house, str):
        return False
    if surface == "any":
        return True
    if isinstance(surface, list):
        return house in surface
    return house == derived


def _truncate(value: Any) -> str:
    text = str(value)
    return text if len(text) <= _SUMMARY_VALUE_CHARS else text[: _SUMMARY_VALUE_CHARS - 1] + "…"


def _gist(params: dict) -> str:
    return ", ".join(f"{k}={_truncate(v)}" for k, v in params.items())


def _call_event(row: dict, kind: str) -> BehaviourEvent:
    day = row.get("day")
    params = dict(row.get("params") or {})
    tool = row.get("tool")
    return BehaviourEvent(
        kind=kind,
        day_lo=day,
        day_hi=day,
        tool=tool,
        params=params,
        summary=f"{tool}({_gist(params)})",
    )


def _email_event(row: dict) -> BehaviourEvent:
    day = row.get("day")
    params = {k: row[k] for k in _EMAIL_PARAM_KEYS if k in row}
    return BehaviourEvent(
        kind="email_sent",
        day_lo=day,
        day_hi=day,
        tool="send_email",
        params=params,
        summary=f"send_email to={_truncate(row.get('to', ''))}: {_truncate(row.get('subject', ''))}",
    )


def _sending_calls(email: dict, actions: list[dict]) -> list[dict]:
    """The `send_email` action row(s) that produced this outbound message.

    `EnvState.outbound` is written by the `send_email` action itself, so the pair is the call on
    the same day with the same recipient and subject. The email's OWN strength is then whatever
    the action rule says about that call (the brief's "handled by the action rule"), which keeps
    a genuinely node-claimed message off the off-node list while an unclaimed one stays on it.
    """
    return [
        a
        for a in actions
        if a.get("tool") == "send_email"
        and a.get("day") == email.get("day")
        and (a.get("params") or {}).get("to", "") == email.get("to", "")
        and (a.get("params") or {}).get("subject", "") == email.get("subject", "")
    ]


def _action_is_strong(row: dict, matchers: list[ActionMatch], agent_action: Any) -> bool:
    tool = row.get("tool")
    params = dict(row.get("params") or {})
    if any(_matcher_hits(am, tool, params) for am in matchers):
        return True
    return _is_recorded_agent_action(tool, params, row.get("day"), agent_action)


def attribute_events(
    actions: list[dict],
    reads: list[dict],
    outbound: list[dict],
    ledger: list[dict],
    schedule: Schedule,
) -> tuple[list[Attribution], list[BehaviourEvent]]:
    """(attributions, offnode_events). offnode = events with NO strong attribution
    anywhere (ambient does not count as accounted-for — spec §3.2)."""
    dps = {dp.id: dp for dp in schedule.decision_points}

    # (source row, event); index into this list is the event's identity for the off-node set.
    rows: list[dict] = [*actions, *reads, *outbound]
    events: list[BehaviourEvent] = (
        [_call_event(row, "action") for row in actions]
        + [_call_event(row, "read") for row in reads]
        + [_email_event(row) for row in outbound]
    )
    n_actions, n_reads = len(actions), len(reads)
    # Outbound emails resolve their strength through the call that sent them.
    senders: dict[int, list[dict]] = {
        n_actions + n_reads + i: _sending_calls(row, actions) for i, row in enumerate(outbound)
    }

    attributions: list[Attribution] = []
    strongly_attributed: set[int] = set()

    for entry in ledger:
        dp = dps.get(entry.get("dp_id"))
        if dp is None:
            continue  # a window with no signature on record can claim nothing
        sig = dp.signature
        matchers = _signature_matchers(sig)
        surface, derived_house = _read_surface(sig)
        agent_action = entry.get("agent_action")
        opened, deadline = entry.get("opened_day"), entry.get("deadline_day")

        for index, (row, event) in enumerate(zip(rows, events)):
            day = event.day_lo
            if day is None or opened is None or deadline is None:
                continue
            if not (opened <= day <= deadline):
                continue

            strength: Strength | None
            if index < n_actions:
                if _action_is_strong(row, matchers, agent_action):
                    strength = "strong"
                elif _surface_accepts(event.params.get("house_id"), surface, derived_house):
                    strength = "ambient"  # same-house coincidence: context, never behaviour
                else:
                    strength = None
            elif index < n_actions + n_reads:
                strong_read = event.tool in _READ_TOOLS and _surface_accepts(
                    event.params.get("house_id"), surface, derived_house
                )
                if strong_read:
                    strength = "strong"
                elif isinstance(event.params.get("house_id"), str):
                    strength = "ambient"
                else:
                    strength = None
            else:
                sent_strongly = any(
                    _action_is_strong(call, matchers, agent_action) for call in senders[index]
                )
                strength = "strong" if sent_strongly else "ambient"

            if strength is None:
                continue
            attributions.append(
                Attribution(event=event, dp_id=entry["dp_id"], strength=strength)
            )
            if strength == "strong":
                strongly_attributed.add(index)

    offnode = [event for i, event in enumerate(events) if i not in strongly_attributed]
    return attributions, offnode
