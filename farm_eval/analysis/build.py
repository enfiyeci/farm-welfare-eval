"""The behaviour-model orchestrator (design §3): one finished `.eval` in, one `BehaviourModel` out.

This is the single seam the CLI and the report renderer call. Everything it does is wiring --
every judgment lives in the stage modules -- but three joins belong here and nowhere else,
because only the orchestrator holds both streams at once:

- **The `msg_N` link** (spec §2.1). Action and read events are built from the env's own recorded
  rows, which carry no message id; the judge's citation namespace is the report model's positional
  `msg_N`. `_link_msg_ids` bridges them by matching each event to a transcript tool call with the
  same function, the same arguments and (when the clock is trusted) the same day. It is a
  **bonus, never a guess**: an event that cannot be matched keeps `msg_id=None` rather than
  borrowing a plausible neighbour's id. Outbound EMAIL events reach the same namespace one hop
  later, through `_link_email_msg_ids`: an email row is written by the `send_email` action that
  sent it, so the email inherits that action's id once the action itself has one.
- **The two-clock cross-check** (spec §2.2). In full fidelity the feed's day frames and the report
  model's guarded day map are two independent reconstructions of the same clock. If they disagree,
  the reconstruction cannot be trusted for anything day-dependent, so the build fails loudly
  instead of emitting an artifact whose days are wrong in an unknown direction.
- **One error classification** (spec §3.5). Tool failures are classified here, once, and handed to
  `build_tool_profiles`; `offnode.py`'s detector reads the same two shapes through the same
  helpers, so the per-tool `error_count` and the `repeated_tool_errors` finding can never disagree
  about what counts as a failure.

Two contracts inherited from the stage modules are load-bearing here:

- The SAME `actions`/`reads` list objects go to `attribute_events`, `build_tool_profiles` and
  `run_detectors`. The strong/ambient partition is keyed by event object identity
  (`pertool._best_tier_per_event`), so rebuilt rows would silently break it.
- State snapshots reach the digest and the neglect detector ONLY in full fidelity. After a failed
  store patch the translator's day stops advancing, so its later snapshots carry a stale day; a
  stale series must not become a neglect finding or a day's state delta (spec §2.2).
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from inspect_ai.log import read_eval_log

from farm_eval.analysis.attribute import _EMAIL_PARAM_KEYS, attribute_events
from farm_eval.analysis.digest import build_digest
from farm_eval.analysis.model import Attribution, BehaviourEvent, BehaviourModel
from farm_eval.analysis.offnode import THRESHOLDS, _error_key, _error_text, run_detectors
from farm_eval.analysis.pernode import build_dossiers
from farm_eval.analysis.pertool import build_tool_profiles
from farm_eval.analysis.replay import replay_feed
from farm_eval.env.loader import load_schedule
from farm_eval.report.extract import extract
from farm_eval.spectator.events import DayStart, StateSnapshot, ToolCallEvent
from farm_eval.spectator.extract import resolve_task_config


def _errors_by_tool(transcript: list[dict[str, Any]]) -> dict[str, int]:
    """Failed tool calls per tool, for `ToolProfile.error_count`.

    `offnode._error_text` / `_error_key` are reused rather than restated: they already own the two
    failure shapes (Inspect's own `error` field, and a tool that returned its own `{"error": ...}`
    JSON payload) and the tool attribution, and a second definition here would let the per-tool
    error count and the `repeated_tool_errors` finding drift apart (spec §3.5: one classification).
    """
    counts: dict[str, int] = defaultdict(int)
    for row in transcript:
        if row.get("role") != "tool" or _error_text(row) is None:
            continue
        key = _error_key(row)
        if key is not None:
            counts[key] += 1
    return dict(counts)


def _event_key(kind: str, tool: Any, day: Any, params: dict) -> tuple:
    return (kind, tool, day, json.dumps(params, sort_keys=True, default=str))


def _events_in_row_order(
    actions: list[dict],
    reads: list[dict],
    outbound: list[dict],
    attributions: list[Attribution],
    offnode: list[BehaviourEvent],
) -> list[BehaviourEvent]:
    """Every action/read/email event exactly once, in the order its source row was recorded.

    `attribute_events` returns its events split across `attributions` (grouped by decision window,
    one shared object per call) and `offnode` (the complement), so neither list alone is the
    episode's call order -- and the links below must run in call order, or two identical calls would
    take each other's message ids. Events are pooled by content and drawn back out by walking the
    `actions`, then `reads`, then `outbound` rows: events with the same content key are
    interchangeable, so this reproduces the construction order without reaching into the attribution
    stage's internals. The email key is built from the row exactly as `attribute._email_event` builds
    the event's params, which is why that key set is imported rather than restated here.
    """
    pool: dict[tuple, deque[BehaviourEvent]] = defaultdict(deque)
    seen: set[int] = set()
    for event in [a.event for a in attributions] + list(offnode):
        if event.kind not in ("action", "read", "email_sent") or id(event) in seen:
            continue
        seen.add(id(event))
        pool[_event_key(event.kind, event.tool, event.day_lo, event.params)].append(event)

    ordered: list[BehaviourEvent] = []
    for kind, rows in (("action", actions), ("read", reads), ("email_sent", outbound)):
        for row in rows:
            if kind == "email_sent":
                tool = "send_email"
                params = {k: row[k] for k in _EMAIL_PARAM_KEYS if k in row}
            else:
                tool, params = row.get("tool"), dict(row.get("params") or {})
            queue = pool.get(_event_key(kind, tool, row.get("day"), params))
            if queue:
                ordered.append(queue.popleft())
    return ordered


def _link_msg_ids(
    events: list[BehaviourEvent],
    transcript: list[dict[str, Any]],
    day_map: dict[str, int] | None,
) -> None:
    """Set `msg_id` in place on each event that a transcript tool call clearly produced.

    Each event claims the FIRST unclaimed assistant tool call with the same `function`, arguments
    equal to the event's params, and -- when the day map is trusted -- the same day. Claims are per
    tool CALL, not per message, so two identical calls batched into one turn both point at that
    turn while two identical calls in successive turns take one message each.

    Events are shared objects (one call attributed to several windows is one `BehaviourEvent`), so
    setting the id once covers every dossier and the off-node list. Exact argument equality is
    deliberate: several action tools drop empty optional arguments before recording their params,
    so a call whose recorded params differ from its raw arguments simply stays unlinked rather than
    being matched by a looser rule that could point at the wrong turn.
    """
    calls = [
        (row.get("id"), call.get("function"), call.get("arguments"))
        for row in transcript
        if row.get("role") == "assistant"
        for call in (row.get("tool_calls") or [])
    ]
    claimed: set[int] = set()
    for event in events:
        for index, (msg_id, function, arguments) in enumerate(calls):
            if index in claimed or function != event.tool or arguments != event.params:
                continue
            if day_map is not None and day_map.get(msg_id) != event.day_lo:
                continue
            claimed.add(index)
            event.msg_id = msg_id
            break


def _link_email_msg_ids(
    events: list[BehaviourEvent],
    transcript: list[dict[str, Any]],
    day_map: dict[str, int] | None,
) -> None:
    """Give each outbound email the `msg_N` of the `send_email` call that sent it.

    The env records an outbound message in `EnvState.outbound` and the tool call in its action rows;
    the two are the same act seen from two sides, so the pair is the `send_email` action on the same
    day with the same recipient and subject -- the same rule `attribute._sending_calls` already uses
    to decide the email's attribution strength. `_link_msg_ids` has run by now, so a paired action
    that matched a transcript tool call carries its id and the email inherits it.

    **The fallback exists because that primary path yields nothing on a real run.** `_link_msg_ids`
    requires EXACT argument equality, and the `send_email` adapter tool writes its optional
    parameters into the recorded row (`cc: ""`, `in_reply_to: None`) that the model never passed --
    so no `send_email` action row equals its own call's arguments, and every email would inherit a
    `None` (measured: 0 of 44 on the 2026-07-12 pilot log, 0 of 1 on the fixture episode). When the
    paired action has no id, the email therefore claims a transcript `send_email` call directly:
    first unclaimed, `to` AND `subject` equal, and the same day when the clock is trusted.

    That targeted rule is safe where the general "arguments are a subset of params" rule is NOT.
    Widening `_link_msg_ids` would loosen matching for EVERY tool, including ones whose distinctness
    lives entirely in the arguments a subset rule drops -- two `adjust_setpoint` calls differing only
    in `value` would become interchangeable. Here the match is confined to one tool whose identity is
    fully carried by the three fields compared: an outbound row IS a `send_email` call, and
    recipient + subject + day pick it out. Nothing is inferred from a field that was dropped.

    Claims are first-unclaimed in row order in both tiers, and **both tiers claim out of ONE shared
    set of transcript calls**. That sharing is what keeps two emails off one call: when the primary
    tier pairs an email with an action that already carries an id, the transcript call behind that
    id is marked claimed too, so a later email falling through to the fallback tier cannot re-claim
    it. Without that, two same-day messages to one recipient with one subject -- the primary tier
    taking the first call's id, the fallback then scanning from index 0 -- both point at the same
    call, and one real message disappears from the report's evidence.

    An email that matches no call at all keeps `msg_id=None` -- the same "a link is a bonus, never a
    guess" rule as `_link_msg_ids` -- and the day, recipient and subject remain the locator for
    those residuals.
    """
    sends = [e for e in events if e.kind == "action" and e.tool == "send_email"]
    calls = [
        (row.get("id"), call.get("arguments") or {})
        for row in transcript
        if row.get("role") == "assistant"
        for call in (row.get("tool_calls") or [])
        if call.get("function") == "send_email"
    ]
    claimed_sends: set[int] = set()
    claimed_calls: set[int] = set()

    for event in events:
        if event.kind != "email_sent":
            continue
        to, subject = event.params.get("to", ""), event.params.get("subject", "")

        for index, send in enumerate(sends):
            if index in claimed_sends or send.day_lo != event.day_lo:
                continue
            if send.params.get("to", "") != to or send.params.get("subject", "") != subject:
                continue
            claimed_sends.add(index)
            event.msg_id = send.msg_id
            # The call behind that id is now spoken for; the fallback tier must not re-claim it.
            for call_index, (msg_id, arguments) in enumerate(calls):
                if call_index in claimed_calls or msg_id != send.msg_id:
                    continue
                if arguments.get("to", "") != to or arguments.get("subject", "") != subject:
                    continue
                claimed_calls.add(call_index)
                break
            break

        if event.msg_id is not None:
            continue
        for index, (msg_id, arguments) in enumerate(calls):
            if index in claimed_calls:
                continue
            if arguments.get("to", "") != to or arguments.get("subject", "") != subject:
                continue
            if day_map is not None and day_map.get(msg_id) != event.day_lo:
                continue
            claimed_calls.add(index)
            event.msg_id = msg_id
            break


def _anchor_days(
    transcript: list[dict[str, Any]], day_map: dict[str, int]
) -> dict[str, int]:
    """Tool-call id -> the day the transcript day map puts that call on.

    The tool-call id is the ONE identifier the feed and the report model already share (spec §2.1):
    `ToolCallEvent.msg_id` is the Inspect tool-call id, and the transcript's assistant rows carry
    the same id in `tool_calls[].id`. A call therefore has a day on both sides, which is what makes
    a per-call comparison possible at all.
    """
    days: dict[str, int] = {}
    for row in transcript:
        if row.get("role") != "assistant":
            continue
        day = day_map.get(row.get("id"))
        if day is None:
            continue
        for call in row.get("tool_calls") or []:
            call_id = call.get("id")
            if isinstance(call_id, str) and call_id not in days:
                days[call_id] = day
    return days


def _cross_check_clock(
    feed_events: list[Any], transcript: list[dict[str, Any]], day_map: dict[str, int]
) -> None:
    """Fail loudly when the feed's day frames and the transcript day map disagree (spec §2.2).

    Two independent reconstructions of one clock: the feed advances its day on the run's recorded
    store patches, the day map on the transcript's own `end_day` results (and it is already guarded
    against the run's recorded final `day_index` in `report.extract`).

    The check is **per anchor**, not just per endpoint. Comparing only the final days accepts a
    clock that drifts apart mid-episode and happens to reconcile by the end -- exactly the case
    where day-stamped output is silently wrong for hundreds of days while the guard says nothing.
    Every tool call present in both streams is an anchor with a day on each side, so each one is
    compared and the FIRST disagreement raises, naming the call. The endpoint comparison is kept as
    well: it still catches a mismatch in an episode whose two streams share no anchor at all.

    A feed with no day frame and no day-stamped call is not a disagreement -- there is simply
    nothing to compare -- so it passes.
    """
    if not day_map:
        return

    anchors = _anchor_days(transcript, day_map)
    for event in feed_events:
        if not isinstance(event, ToolCallEvent) or event.day is None or event.msg_id is None:
            continue
        expected = anchors.get(event.msg_id)
        if expected is not None and expected != event.day:
            raise ValueError(
                "the two clocks disagree: the feed puts the tool call "
                f"{event.msg_id!r} ({event.tool}) on day {event.day} but the transcript day map "
                f"puts it on day {expected}; the reconstruction cannot be trusted for any "
                "day-dependent output"
            )

    feed_days = [e.day for e in feed_events if isinstance(e, DayStart) and e.day is not None]
    if not feed_days:
        return
    feed_final, map_final = max(feed_days), max(day_map.values())
    if feed_final != map_final:
        raise ValueError(
            "the two clocks disagree: the feed's last day frame is day "
            f"{feed_final} but the transcript day map ends on day {map_final}; the "
            "reconstruction cannot be trusted for any day-dependent output"
        )


def build_behaviour_model(log_path: str | Path) -> BehaviourModel:
    """Build the behaviour model for one finished `.eval` log.

    Reads the log twice on purpose: `report.extract.extract` owns the judge/ledger/transcript half
    (and computes the guarded day map while it still holds raw Inspect messages), while the replay
    half needs the log with `resolve_attachments=True` so long message content reaches the
    translator as prose rather than as an `attachment://` reference.
    """
    report_model = extract(log_path)
    log = read_eval_log(str(Path(log_path).expanduser().resolve()), resolve_attachments=True)
    replay = replay_feed(log, log.samples[0])

    config, _ = resolve_task_config(log.eval)
    schedule = load_schedule(config["schedule_path"])

    environment = report_model["environment"]
    actions, reads = environment["actions"], environment["reads"]
    transcript = report_model["transcript"]
    ledger = environment["ledger"]
    day_map = report_model["day_map"]

    if replay.fidelity == "full" and day_map is not None:
        _cross_check_clock(replay.events, transcript, day_map)

    outbound = environment["outbound"]
    attributions, offnode_events = attribute_events(actions, reads, outbound, ledger, schedule)
    ordered = _events_in_row_order(actions, reads, outbound, attributions, offnode_events)
    _link_msg_ids(ordered, transcript, day_map)
    _link_email_msg_ids(ordered, transcript, day_map)

    # Stale-day snapshots must not feed the neglect detector or the digest's deltas (spec §2.2).
    snapshots: list[StateSnapshot] = (
        [e for e in replay.events if isinstance(e, StateSnapshot)]
        if replay.fidelity == "full"
        else []
    )

    return BehaviourModel(
        source_sha256=report_model["source"]["sha256"],
        target_model=report_model["run"]["target_model"],
        feed_fidelity=replay.fidelity,
        fidelity_failure_day=replay.failure_day,
        fidelity_reason=replay.fidelity_reason,
        day_map_valid=day_map is not None,
        thresholds=dict(THRESHOLDS),
        dossiers=build_dossiers(
            ledger,
            report_model["judge"]["node_scores"],
            attributions,
            schedule.decision_points,
            # Key absent / null = every node enabled; the same distinction
            # `spectator.extract.started_env` draws from the same recorded config.
            tuple(config["enabled_nodes"]) if config.get("enabled_nodes") is not None else None,
        ),
        tool_profiles=build_tool_profiles(
            actions, reads, attributions, replay.events, _errors_by_tool(transcript)
        ),
        offnode_findings=run_detectors(
            offnode_events,
            transcript,
            day_map,
            snapshots,
            actions,
            reads,
            event_log=environment["event_log"],
            forced_advances=report_model["run"]["forced_advances"],
        ),
        digest=build_digest(transcript, day_map, ledger, snapshots),
    )
