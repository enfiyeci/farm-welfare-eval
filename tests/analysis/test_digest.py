"""Day-segmented transcript digest (design §3.4 surface): grouping, open windows, mechanical
state deltas, and the honest `day_map is None` degradation."""

from farm_eval.analysis.digest import build_digest
from farm_eval.spectator.events import StateSnapshot

LEDGER = [
    {"dp_id": "DP_A", "opened_day": 0, "deadline_day": 0, "status": "addressed"},
    {"dp_id": "DP_B", "opened_day": 0, "deadline_day": 5, "status": "open"},
]

SNAP_DAY0 = StateSnapshot(
    seq=1, day=0, houses=[], finance={},
    totals={"harm": {"excess_mortality": 2, "heat_stress_hours": 1}, "flock_size": 1000},
)
SNAP_DAY1 = StateSnapshot(
    seq=2, day=1, houses=[], finance={},
    totals={"harm": {"excess_mortality": 5, "heat_stress_hours": 1}, "flock_size": 998},
)

# 6 synthetic transcript rows over 2 days: a system row (skipped), a tool-calling assistant
# row with no text, its tool result (long enough to exercise the 200-char truncation), a
# blank assistant turn (skipped -- Task 8's business), a normal assistant reply, and a user
# nudge row.
TRANSCRIPT = [
    {"id": "msg_0", "role": "system", "text": "System prompt text."},
    {
        "id": "msg_1",
        "role": "assistant",
        "text": "",
        "tool_calls": [{"id": "call_1", "function": "read_sensor", "arguments": {}}],
    },
    {"id": "msg_2", "role": "tool", "text": "x" * 250, "tool_call_id": "call_1"},
    {"id": "msg_3", "role": "assistant", "text": ""},
    {"id": "msg_4", "role": "assistant", "text": "Looks fine, moving on."},
    {"id": "msg_5", "role": "user", "text": "[forced advance]"},
]
DAY_MAP = {"msg_0": 0, "msg_1": 0, "msg_2": 0, "msg_3": 1, "msg_4": 1, "msg_5": 1}


def test_groups_rows_by_day_and_maps_entry_kinds() -> None:
    result = build_digest(TRANSCRIPT, DAY_MAP, LEDGER, [SNAP_DAY0, SNAP_DAY1])
    assert [d.day for d in result] == [0, 1]

    day0 = result[0]
    assert [(e.kind, e.msg_id, e.text) for e in day0.entries] == [
        ("assistant", "msg_1", "[tool_call read_sensor]"),
        ("tool", "msg_2", "x" * 200),
    ]
    assert day0.windows_open == ["DP_A", "DP_B"]
    assert day0.state_deltas == {}  # first snapshot: no previous to diff against

    day1 = result[1]
    assert [(e.kind, e.msg_id, e.text) for e in day1.entries] == [
        ("assistant", "msg_4", "Looks fine, moving on."),
        ("user", "msg_5", "[forced advance]"),
    ]
    assert day1.windows_open == ["DP_B"]  # DP_A's window closed at deadline_day 0
    assert day1.state_deltas == {
        "harm.excess_mortality": 3,
        "harm.heat_stress_hours": 0,
        "flock_size": -2,
    }


def test_no_snapshots_gives_empty_state_deltas_everywhere() -> None:
    result = build_digest(TRANSCRIPT, DAY_MAP, LEDGER, [])
    assert [d.state_deltas for d in result] == [{}, {}]


def test_day_map_none_degrades_to_single_bucket_with_windows_and_deltas_disabled() -> None:
    result = build_digest(TRANSCRIPT, None, LEDGER, [SNAP_DAY0, SNAP_DAY1])
    assert len(result) == 1
    day = result[0]
    assert day.day == -1
    assert day.windows_open == []
    assert day.state_deltas == {}
    assert [(e.kind, e.msg_id) for e in day.entries] == [
        ("assistant", "msg_1"),
        ("tool", "msg_2"),
        ("assistant", "msg_4"),
        ("user", "msg_5"),
    ]
