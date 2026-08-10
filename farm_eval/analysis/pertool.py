"""Per-tool behaviour profiles (design §3.4): one row per roster tool, aggregating call counts,
timing, house coverage, feed-sourced cost/error, and the strong/ambient/off-node partition.

`TOOL_ROSTER` is the 20 `all_tools()` registry names plus `"end_day"` -- the solver appends
`end_day` to the tool list itself (`farm_eval/adapter/solver/farm_solver.py:56`), so it never
appears in `all_tools()`'s own registry but is a real, callable tool. A drift-guard test
(`tests/analysis/test_pertool.py::test_roster_matches_the_adapter_registry`) asserts this tuple
against the live registry so a renamed/added/removed tool fails loudly here instead of silently
missing (or ghosting) a profile row (Codex F7).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from farm_eval.analysis.model import Attribution, ToolProfile
from farm_eval.spectator.events import ToolCallEvent

TOOL_ROSTER: tuple[str, ...] = (
    # reads
    "get_datetime",
    "list_houses",
    "read_sensor",
    "list_emails",
    "read_email",
    "query_pricing",
    "read_financials",
    "read_flock_report",
    "generate_cop_report",
    # actions
    "adjust_setpoint",
    "set_staffing",
    "set_financing",
    "pay_invoice",
    "dispute_charge",
    "place_feed_order",
    "schedule_maintenance",
    "schedule_vet_visit",
    "log_treatment",
    "set_egg_disposition",
    "send_email",
    # the clock, appended by the solver rather than all_tools()
    "end_day",
)


def _bucket_start(day: int, bucket_days: int) -> int:
    return (day // bucket_days) * bucket_days


def _calls_by_bucket(days: list[int], bucket_days: int) -> list[dict[str, int]]:
    buckets: dict[int, int] = defaultdict(int)
    for day in days:
        buckets[_bucket_start(day, bucket_days)] += 1
    return [{"day": bucket, "calls": n} for bucket, n in sorted(buckets.items())]


def _house_counts(rows: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        house = (row.get("params") or {}).get("house_id")
        if isinstance(house, str):
            counts[house] += 1
    return dict(counts)


def _best_tier_per_event(attributions: list[Attribution]) -> dict[str, tuple[int, int]]:
    """Per action/read tool, (strong, ambient) distinct-event counts.

    Groups attributions by `id(attribution.event)` -- the same call attributed to several
    decision-point windows shares one event object (see `attribute.py`), so this collapses those
    rows back to one classification per actual call, taking the best tier (strong beats ambient).
    email_sent/assistant_text events are excluded: a `send_email` action yields BOTH an action
    event and an email event in the attribution stream (Task 4 carry-forward), and only the
    action event is this tool's call -- counting the email event too would double the tool's
    strong/ambient counts against a single actual call.
    """
    best_by_event: dict[int, tuple[str, str]] = {}
    for attr in attributions:
        event = attr.event
        if event.kind not in ("action", "read") or event.tool is None:
            continue
        key = id(event)
        prior = best_by_event.get(key)
        if prior is None or (prior[1] == "ambient" and attr.strength == "strong"):
            best_by_event[key] = (event.tool, attr.strength)

    strong_counts: dict[str, int] = defaultdict(int)
    ambient_counts: dict[str, int] = defaultdict(int)
    for tool, strength in best_by_event.values():
        if strength == "strong":
            strong_counts[tool] += 1
        else:
            ambient_counts[tool] += 1
    return {tool: (strong_counts[tool], ambient_counts[tool]) for tool in set(strong_counts) | set(ambient_counts)}


def build_tool_profiles(
    actions: list[dict],
    reads: list[dict],
    attributions: list[Attribution],
    feed_events: list[Any],
    errors_by_tool: dict[str, int],
    bucket_days: int = 7,
) -> list[ToolProfile]:
    """Caller contract: `attributions` must come from `attribute_events(...)` called with these
    EXACT same `actions`/`reads` list objects. The strong/ambient partition is keyed by event
    object identity (`id(attribution.event)`, see `_best_tier_per_event`) -- attributions derived
    from different row objects leave the partition undefined, and `offnode_calls` can go silently
    negative.
    """
    rows_by_tool: dict[str, list[dict]] = defaultdict(list)
    for row in [*actions, *reads]:
        rows_by_tool[row.get("tool")].append(row)

    cost_by_tool: dict[str, float] = defaultdict(float)
    end_day_events: list[ToolCallEvent] = []
    for ev in feed_events:
        if not isinstance(ev, ToolCallEvent):
            continue
        if ev.cost_cents is not None:
            cost_by_tool[ev.tool] += ev.cost_cents
        if ev.tool == "end_day":
            end_day_events.append(ev)

    tiers_by_tool = _best_tier_per_event(attributions)

    profiles: list[ToolProfile] = []
    for tool in TOOL_ROSTER:
        if tool == "end_day":
            # end_day is never in actions/reads (it's the clock, not a state-changing action or
            # a read) -- its calls are only visible in the spectator feed, and it is deliberately
            # excluded from the strong/ambient/offnode partition rule below.
            total_calls = len(end_day_events)
            days = [ev.day for ev in end_day_events if ev.day is not None]
            houses: dict[str, int] = {}
            strong = ambient = offnode = 0
        else:
            rows = rows_by_tool.get(tool, [])
            total_calls = len(rows)
            days = [row.get("day") for row in rows if row.get("day") is not None]
            houses = _house_counts(rows)
            strong, ambient = tiers_by_tool.get(tool, (0, 0))
            offnode = total_calls - strong - ambient

        profiles.append(
            ToolProfile(
                tool=tool,
                total_calls=total_calls,
                first_day=min(days) if days else None,
                last_day=max(days) if days else None,
                calls_by_bucket=_calls_by_bucket(days, bucket_days),
                houses=houses,
                error_count=errors_by_tool.get(tool, 0),
                cost_cents_total=cost_by_tool.get(tool, 0.0),
                strong_calls=strong,
                ambient_calls=ambient,
                offnode_calls=offnode,
            )
        )
    return profiles
