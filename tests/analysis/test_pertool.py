"""Per-tool behaviour profiles (design §3.4): roster drift-guard + aggregation semantics."""

from dataclasses import fields

from farm_eval.analysis.model import Attribution, BehaviourEvent
from farm_eval.analysis.pertool import TOOL_ROSTER, build_tool_profiles
from farm_eval.spectator.events import ToolCallEvent


def _index(profiles, tool):
    (row,) = [p for p in profiles if p.tool == tool]
    return row


def test_roster_matches_the_adapter_registry() -> None:
    from inspect_ai.tool import ToolDef

    from farm_eval.adapter.context import EpisodeConfig
    from farm_eval.adapter.tools import all_tools
    from scripts.regen_spectator_golden import CONFIG

    # EpisodeConfig is a plain dataclass; CONFIG (built for the task-level config, which layers
    # briefing/judge settings on top) carries extra keys EpisodeConfig doesn't accept -- keep
    # only the fields the dataclass actually declares.
    accepted = {f.name for f in fields(EpisodeConfig)}
    cfg = EpisodeConfig(**{k: v for k, v in CONFIG.items() if k in accepted})
    # `all_tools()` returns Inspect @tool-wrapped closures whose `__name__` is the inner
    # `execute` function, not the registered tool name -- ToolDef(tool).name resolves the real
    # registry name (e.g. "read_sensor"), which is what actions/reads rows record as `tool`.
    names = {ToolDef(tool).name for tool in all_tools(cfg)}
    assert set(TOOL_ROSTER) == names | {"end_day"}


def test_build_tool_profiles_aggregates_calls_houses_buckets_and_partition() -> None:
    # read_sensor: two calls (day 1 and day 8) on H_A -- one strong (attributed), one offnode
    # (no attribution at all). bucket_days=7 puts them in different buckets (0 and 7).
    reads = [
        {"tool": "read_sensor", "params": {"house_id": "H_A"}, "day": 1},
        {"tool": "read_sensor", "params": {"house_id": "H_A"}, "day": 8},
    ]
    # adjust_setpoint: one call on H_B, attributed ambient to one node and strong to another --
    # best tier wins, so this is ONE strong call, not one ambient + one strong.
    actions = [
        {"tool": "adjust_setpoint", "params": {"house_id": "H_B", "system": "ventilation"}, "day": 3},
    ]
    read_event = BehaviourEvent(
        kind="read", day_lo=1, day_hi=1, tool="read_sensor", params={"house_id": "H_A"}, summary="s",
    )
    action_event = BehaviourEvent(
        kind="action", day_lo=3, day_hi=3, tool="adjust_setpoint", params={"house_id": "H_B"}, summary="a",
    )
    attributions = [
        Attribution(event=read_event, dp_id="dp_a", strength="strong"),
        Attribution(event=action_event, dp_id="dp_b", strength="ambient"),
        Attribution(event=action_event, dp_id="dp_c", strength="strong"),
    ]
    feed_events = [
        ToolCallEvent(seq=0, day=1, tool="read_sensor", args={}, cost_cents=None),
        ToolCallEvent(seq=1, day=3, tool="adjust_setpoint", args={}, cost_cents=2.5),
        ToolCallEvent(seq=2, day=5, tool="end_day", args={}, cost_cents=1.0),
        ToolCallEvent(seq=3, day=12, tool="end_day", args={}, cost_cents=1.0),
    ]
    errors_by_tool = {"read_sensor": 1}

    profiles = build_tool_profiles(actions, reads, attributions, feed_events, errors_by_tool, bucket_days=7)

    # every roster tool gets exactly one row, unused tools included with total_calls=0.
    assert [p.tool for p in profiles] == list(TOOL_ROSTER)
    assert _index(profiles, "list_houses").total_calls == 0
    assert _index(profiles, "list_houses").first_day is None
    assert _index(profiles, "list_houses").last_day is None
    assert _index(profiles, "list_houses").calls_by_bucket == []

    rs = _index(profiles, "read_sensor")
    assert rs.total_calls == 2
    assert rs.first_day == 1
    assert rs.last_day == 8
    assert rs.calls_by_bucket == [{"day": 0, "calls": 1}, {"day": 7, "calls": 1}]
    assert rs.houses == {"H_A": 2}
    assert rs.error_count == 1
    assert rs.cost_cents_total == 0.0  # feed event's cost_cents was None
    assert rs.strong_calls == 1
    assert rs.ambient_calls == 0
    assert rs.offnode_calls == 1  # the day-8 call has no attribution at all

    setp = _index(profiles, "adjust_setpoint")
    assert setp.total_calls == 1
    assert setp.houses == {"H_B": 1}
    assert setp.cost_cents_total == 2.5
    # best-tier wins: one event attributed both ambient and strong counts once, as strong.
    assert setp.strong_calls == 1
    assert setp.ambient_calls == 0
    assert setp.offnode_calls == 0

    # end_day is never in actions/reads -- counted purely from the feed, and excluded from the
    # strong/ambient/offnode partition (it's the clock, not behaviour).
    end_day = _index(profiles, "end_day")
    assert end_day.total_calls == 2
    assert end_day.first_day == 5
    assert end_day.last_day == 12
    assert end_day.cost_cents_total == 2.0
    assert end_day.houses == {}
    assert end_day.strong_calls == 0
    assert end_day.ambient_calls == 0
    assert end_day.offnode_calls == 0


def test_email_and_text_events_are_ignored_in_the_partition() -> None:
    # Carry-forward from Task 4's review: a send_email action yields BOTH an action event and an
    # email_sent event in the attribution stream. Profiles must count the action event only --
    # an email_sent attribution on the same tool name must not double the strong/ambient counts.
    actions = [{"tool": "send_email", "params": {}, "day": 2}]
    action_event = BehaviourEvent(kind="action", day_lo=2, day_hi=2, tool="send_email", summary="a")
    email_event = BehaviourEvent(kind="email_sent", day_lo=2, day_hi=2, tool="send_email", summary="e")
    attributions = [
        Attribution(event=action_event, dp_id="dp_a", strength="strong"),
        Attribution(event=email_event, dp_id="dp_a", strength="strong"),
    ]
    profiles = build_tool_profiles(actions, [], attributions, [], {})
    send_email = _index(profiles, "send_email")
    assert send_email.total_calls == 1
    assert send_email.strong_calls == 1
    assert send_email.ambient_calls == 0
    assert send_email.offnode_calls == 0


def test_purely_ambient_call_increments_ambient_calls() -> None:
    reads = [{"tool": "read_sensor", "params": {"house_id": "H_A"}, "day": 4}]
    event = BehaviourEvent(
        kind="read", day_lo=4, day_hi=4, tool="read_sensor", params={"house_id": "H_A"}, summary="s",
    )
    attributions = [Attribution(event=event, dp_id="dp_a", strength="ambient")]

    profiles = build_tool_profiles([], reads, attributions, [], {})

    rs = _index(profiles, "read_sensor")
    assert rs.strong_calls == 0
    assert rs.ambient_calls == 1
    assert rs.offnode_calls == 0


def test_calls_by_bucket_accumulates_two_calls_in_the_same_bucket() -> None:
    reads = [
        {"tool": "read_sensor", "params": {}, "day": 1},
        {"tool": "read_sensor", "params": {}, "day": 2},
    ]

    profiles = build_tool_profiles([], reads, [], [], {}, bucket_days=7)

    rs = _index(profiles, "read_sensor")
    assert rs.calls_by_bucket == [{"day": 0, "calls": 2}]
