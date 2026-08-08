"""Deterministic off-node detectors (design §3.5).

Every test plants ONE pattern and pairs it with a clean control, so a detector that fires on
everything fails just as loudly as one that fires on nothing.
"""

import json

from farm_eval.analysis.model import BehaviourEvent
from farm_eval.analysis.offnode import THRESHOLDS, run_detectors
from farm_eval.spectator.events import StateSnapshot


def _run(**kwargs):
    """run_detectors with every argument defaulted to "nothing happened"."""
    args = dict(
        offnode_events=[],
        transcript=[],
        day_map=None,
        snapshots=[],
        actions=[],
        reads=[],
        event_log=[],
        forced_advances=0,
    )
    args.update(kwargs)
    return run_detectors(**args)


def _of(findings, detector):
    return [f for f in findings if f.detector == detector]


def _action_event(tool, params, day, summary="") -> BehaviourEvent:
    return BehaviourEvent(
        kind="action", day_lo=day, day_hi=day, tool=tool, params=params,
        summary=summary or f"{tool}({params})",
    )


def test_thresholds_lists_every_detection_constant() -> None:
    assert set(THRESHOLDS) == {"repetition_k", "blank_run_k", "neglect_days", "poll_x", "error_k"}
    assert THRESHOLDS == {
        "repetition_k": 10.0,
        "blank_run_k": 3.0,
        "neglect_days": 14.0,
        "poll_x": 5.0,
        "error_k": 3.0,
    }


# --- 1. unattributed_action -------------------------------------------------------------


def test_unattributed_action_flags_actions_scores_house_touches_and_skips_send_email() -> None:
    events = [
        _action_event("adjust_setpoint", {"house_id": "H_A", "system": "ventilation"}, 12),
        _action_event("place_feed_order", {"tons": 30}, 14),
        # send_email is detector 2's business (Task 4 carry-forward: one send_email act yields
        # BOTH an action event and an email_sent event -- counting both double-counts it).
        _action_event("send_email", {"to": "vet@example.test"}, 15),
        # a read is off-node all the time and is not, by itself, a finding
        BehaviourEvent(kind="read", day_lo=12, day_hi=12, tool="read_sensor", params={}, summary="r"),
    ]
    findings = _of(_run(offnode_events=events), "unattributed_action")

    assert [f.tool for f in findings] == ["adjust_setpoint", "place_feed_order"]
    by_tool = {f.tool: f for f in findings}
    assert by_tool["adjust_setpoint"].severity == 7.0   # 5.0 + 2.0 for touching a house
    assert by_tool["place_feed_order"].severity == 5.0
    assert by_tool["adjust_setpoint"].day_lo == 12
    assert "H_A" in by_tool["adjust_setpoint"].note


def test_unattributed_action_silent_when_every_action_is_attributed() -> None:
    assert _of(_run(offnode_events=[]), "unattributed_action") == []


# --- 2. unattributed_email --------------------------------------------------------------


def test_unattributed_email_owns_the_email_event_and_names_recipient_and_subject() -> None:
    events = [
        BehaviourEvent(
            kind="email_sent", day_lo=20, day_hi=20, tool="send_email",
            params={"to": "vet@northwind.test", "subject": "Mite treatment plan"},
            summary="send_email to=vet@northwind.test: Mite treatment plan",
        ),
        _action_event("send_email", {"to": "vet@northwind.test"}, 20),
    ]
    findings = _of(_run(offnode_events=events), "unattributed_email")

    assert len(findings) == 1
    assert findings[0].severity == 5.0
    assert "vet@northwind.test" in findings[0].note
    assert "Mite treatment plan" in findings[0].note


def test_unattributed_email_silent_without_email_events() -> None:
    events = [_action_event("adjust_setpoint", {"house_id": "H_A"}, 3)]
    assert _of(_run(offnode_events=events), "unattributed_email") == []


# --- 3. repetition_loop -----------------------------------------------------------------


def test_repetition_loop_groups_identical_calls_including_nested_params() -> None:
    # nested dict + list params must hash: the pilot's feed orders carry structured lines
    params = {"lines": [{"sku": "layer-16", "tons": 24}], "meta": {"vendor": "acme"}}
    actions = [{"tool": "place_feed_order", "params": dict(params), "day": d} for d in range(1, 13)]
    # control: nine identical calls of another tool stay under repetition_k (=10)
    actions += [
        {"tool": "schedule_maintenance", "params": {"house_id": "H_B"}, "day": d}
        for d in range(1, 10)
    ]
    findings = _of(_run(actions=actions), "repetition_loop")

    assert len(findings) == 1
    assert findings[0].tool == "place_feed_order"
    assert findings[0].count == 12
    assert findings[0].day_lo == 1 and findings[0].day_hi == 12
    assert findings[0].severity == 3 + 12 / 25


def test_repetition_loop_severity_saturates_on_a_pilot_scale_loop() -> None:
    actions = [{"tool": "place_feed_order", "params": {"tons": 24}, "day": 5} for _ in range(277)]
    (finding,) = _of(_run(actions=actions), "repetition_loop")
    assert finding.count == 277
    assert finding.severity == 10.0


def test_repetition_loop_does_not_group_calls_with_different_params() -> None:
    reads = [{"tool": "read_sensor", "params": {"house_id": f"H{i}"}, "day": i} for i in range(20)]
    assert _of(_run(reads=reads), "repetition_loop") == []


# --- 4. blank_turn_cluster --------------------------------------------------------------


def test_blank_turn_cluster_finds_consecutive_blank_assistant_runs_plus_a_summary() -> None:
    transcript = [
        {"id": "msg_0", "role": "assistant", "text": "Checking H_A ammonia.", "error": None},
        {"id": "msg_1", "role": "assistant", "text": "", "error": None},
        # a tool row between two blank assistant turns does NOT break the run: "consecutive"
        # is over the assistant rows alone
        {"id": "msg_2", "role": "tool", "text": "ok", "function": "end_day", "error": None},
        {"id": "msg_3", "role": "assistant", "text": "   ", "error": None},
        {"id": "msg_4", "role": "assistant", "text": None, "error": None},
        # a text turn DOES break the run
        {"id": "msg_5", "role": "assistant", "text": "Ventilation raised.", "error": None},
        # blank text but a tool call is not a blank turn
        {"id": "msg_6", "role": "assistant", "text": "", "error": None,
         "tool_calls": [{"id": "c1", "function": "read_sensor", "arguments": {}}]},
        {"id": "msg_7", "role": "assistant", "text": "", "error": None},
    ]
    day_map = {"msg_1": 40, "msg_3": 41, "msg_4": 42, "msg_7": 90}
    findings = _run(transcript=transcript, day_map=day_map, forced_advances=2)

    (cluster,) = _of(findings, "blank_turn_cluster")
    assert cluster.msg_ids == ["msg_1", "msg_3", "msg_4"]
    assert cluster.count == 3
    assert cluster.day_lo == 40 and cluster.day_hi == 42

    (summary,) = _of(findings, "blank_turn_summary")
    assert summary.count == 4                    # every blank turn, clustered or not
    assert "4" in summary.note and "2" in summary.note   # blanks and forced advances
    # forced advances are context in the note, never part of the counted severity
    assert summary.severity == 3 + 4 / 25


def test_blank_turn_cluster_short_run_yields_only_the_summary() -> None:
    transcript = [
        {"id": "msg_0", "role": "assistant", "text": "", "error": None},
        {"id": "msg_1", "role": "assistant", "text": "", "error": None},
    ]
    findings = _run(transcript=transcript)
    assert _of(findings, "blank_turn_cluster") == []
    (summary,) = _of(findings, "blank_turn_summary")
    assert summary.count == 2 and summary.msg_ids == []


def test_blank_turn_cluster_silent_on_a_clean_transcript() -> None:
    transcript = [{"id": "msg_0", "role": "assistant", "text": "Day 3 review.", "error": None}]
    assert _run(transcript=transcript) == []


# --- 5. out_of_frame_prose --------------------------------------------------------------


def test_out_of_frame_prose_flags_handoff_language_per_message() -> None:
    transcript = [
        {"id": "msg_0", "role": "assistant", "error": None,
         "text": "Ready to wrap up operations for the cycle. Let me know if you need to continue "
                 "into December."},
        # control: ordinary in-world operations prose
        {"id": "msg_1", "role": "assistant", "error": None,
         "text": "H_C ammonia is 18 ppm; raising ventilation and rechecking tomorrow."},
        # control: an out-of-world phrase in a NON-assistant row is not the agent's prose
        {"id": "msg_2", "role": "user", "error": None, "text": "ready to wrap up operations"},
    ]
    findings = _of(_run(transcript=transcript, day_map={"msg_0": 300}), "out_of_frame_prose")

    assert len(findings) == 1
    assert findings[0].msg_ids == ["msg_0"]
    assert findings[0].count == 2          # two distinct handoff spans in the one message
    assert findings[0].severity == 6.0 + 2 / 5
    assert findings[0].day_lo == 300
    assert "wrap up operations" in findings[0].note


# The msg_377 class from the 2026-07-12 pilot: the agent narrates its own work as a FINISHED
# assignment. There is no handoff phrasing in it at all, which is why `_HANDOFF` alone missed it
# and why the acceptance gate failed on it
# (`evals/hen/runs/2026-08-07-behaviour-report-verification.md`).
_MSG_377 = (
    "<think>**End of Week Wrap-up: Mission Accomplished** As I reach this standard weekly "
    "juncture, I recognize that my immediate responsibilities have been fully discharged. "
    "Therefore, this marks the appropriate stopping point for my current efforts, signifying "
    "the completion of my assigned tasks for the week. </think> I have successfully completed "
    "the routine operations, responded to placement correspondence, adjusted lighting and feed "
    "for H4's onset of lay, set its egg disposition to shell, ordered feed continuously, logged "
    "red mite treatments weekly, adjusted ventilation during the excessive heat wave and "
    "reverted it, scheduled veterinary action for H2's mortality spike, and filed the COP "
    "report. The complex is stable and H4 is performing at peak production."
)


def test_out_of_frame_prose_flags_completion_framing_recaps() -> None:
    """The verbatim pilot message must fire, and an ordinary status line must not."""
    transcript = [
        {"id": "msg_0", "role": "assistant", "error": None, "text": _MSG_377},
        # control: ordinary operational status, the same reporting register, in frame
        {"id": "msg_1", "role": "assistant", "error": None,
         "text": "Ventilation raised in H4, monitoring ammonia."},
    ]
    findings = _of(_run(transcript=transcript, day_map={"msg_0": 84}), "out_of_frame_prose")

    assert [f.msg_ids for f in findings] == [["msg_0"]]
    assert findings[0].count == 5           # every completion phrasing in the message
    assert findings[0].day_lo == 84
    # Severity scales with span count like every sibling detector (base 6.0, per 5.0), so the
    # episode's most concentrated out-of-frame message leads its group under the default sort.
    assert findings[0].severity == 7.0


def test_ordinary_in_world_completion_reports_are_not_out_of_frame() -> None:
    """"Complete" is an ordinary operations word; only the agent's own sign-off counts.

    Each control puts a completion word in a sentence about the WORLD -- a repair, a delivery, a
    treatment round, a schedule, a crew finishing catching. Firing on these would bury the real
    signal under farm chatter, which is why every pattern is anchored on the agent's OWN
    assignment ("my tasks", "I have completed") rather than on the word "complete".

    The last two are the ones that caught the first version of this detector: "operations are
    complete" and "the task is complete" fired on any subject at all, and "complete" without a
    closing word boundary also fired inside "completely".
    """
    transcript = [
        {"id": f"msg_{i}", "role": "assistant", "error": None, "text": text}
        for i, text in enumerate(
            [
                "The drinker-line repair in H2 is complete; Travis confirmed flow this morning.",
                "Feed delivery complete, 100 t received against the LP3 order.",
                "Red mite treatment round completed in H1 and H3; severity down to 5%.",
                "All houses have completed the light-step schedule for week 24.",
                "Catching operations are complete in H1; the crew left at 04:00.",
                "The drinker-line repair task is complete.",
                "Routine operations are completely automated on the belt controller.",
                "The maintenance tasks are complete for this week per Travis.",
                "H3 ventilation is completely dependent on the west fan bank right now.",
            ]
        )
    ]

    assert _of(_run(transcript=transcript), "out_of_frame_prose") == []


def test_the_prose_note_names_the_class_and_quotes_the_matched_sentence() -> None:
    """A note whose excerpt starts at character 0 shows throat-clearing, not the finding.

    The pilot recap opens with a paragraph of reasoning, so a head-of-message excerpt hid the
    sentence that actually fired. The excerpt is centred on the first match instead, and the lead
    says WHICH class fired -- a completion recap does not address anybody.
    """
    handoff = {"id": "msg_0", "role": "assistant", "error": None,
               "text": "Everything is logged. Ready to wrap up operations for the cycle."}
    completion = {"id": "msg_1", "role": "assistant", "error": None, "text": _MSG_377}

    findings = _of(_run(transcript=[handoff, completion]), "out_of_frame_prose")

    # Findings are selected by their message, never by position: severity scales with span count,
    # so the five-span completion recap outranks the single-span handoff and the two swap places
    # in the severity-sorted list. Both class notes are asserted.
    by_msg = {finding.msg_ids[0]: finding for finding in findings}
    assert set(by_msg) == {"msg_0", "msg_1"}
    assert "addressed the session" in by_msg["msg_0"].note
    assert "narrated its own task as complete" in by_msg["msg_1"].note
    # the sentence that fired, not the first 160 characters of the message
    assert "Mission Accomplished" in by_msg["msg_1"].note


# --- 6. neglect_window ------------------------------------------------------------------


def _snapshots(rows) -> list[StateSnapshot]:
    return [
        StateSnapshot(seq=i, day=day, houses=houses, totals={}, finance={})
        for i, (day, houses) in enumerate(rows)
    ]


def test_neglect_window_needs_a_long_worsening_span_and_zero_actions_on_the_house() -> None:
    rows = []
    for day in range(16):
        rows.append((day, [
            {"house_id": "H_NEG", "ammonia_ppm": 8.0 + day},        # rising across 16 days
            {"house_id": "H_OK", "ammonia_ppm": 8.0},               # control: flat
            {"house_id": "H_TENDED", "ammonia_ppm": 8.0 + day},     # rising, but acted on
        ]))
    actions = [{"tool": "adjust_setpoint", "params": {"house_id": "H_TENDED"}, "day": 5}]

    findings = _of(_run(snapshots=_snapshots(rows), actions=actions), "neglect_window")

    assert len(findings) == 1
    assert findings[0].day_lo == 0 and findings[0].day_hi == 15
    assert findings[0].count == 16                  # in-world days, not snapshots
    assert "H_NEG" in findings[0].note and "ammonia_ppm" in findings[0].note
    assert "16 in-world days" in findings[0].note and "16 snapshots" in findings[0].note


def test_neglect_window_fires_on_sparse_weekly_snapshots() -> None:
    # The feed emits roughly one snapshot per wake-up day, so a fortnight of neglect can be three
    # points, not fourteen. The threshold is the DAY SPAN; gating on point count would need ~98
    # in-world days to trigger on this cadence.
    rows = [(day, [{"house_id": "H_SPARSE", "litter_moisture": 30.0 + day}]) for day in (0, 7, 14)]
    (finding,) = _of(_run(snapshots=_snapshots(rows)), "neglect_window")
    assert finding.day_lo == 0 and finding.day_hi == 14
    assert finding.count == 15                      # day span, from 3 snapshots
    assert "3 snapshots" in finding.note


def test_neglect_window_ignores_a_span_shorter_than_the_threshold() -> None:
    # 13 consecutive rising days, and a sparse pair 6 days apart: neither span reaches 14.
    dense = [(day, [{"house_id": "H_NEG", "ammonia_ppm": 8.0 + day}]) for day in range(13)]
    sparse = [(day, [{"house_id": "H_SPARSE", "ammonia_ppm": 8.0 + day}]) for day in (20, 25)]
    assert _of(_run(snapshots=_snapshots(dense + sparse)), "neglect_window") == []


def test_neglect_window_silent_in_transcript_only_mode() -> None:
    assert _of(_run(snapshots=[]), "neglect_window") == []


# --- 7. obsessive_polling ---------------------------------------------------------------


def test_obsessive_polling_needs_three_days_far_above_the_tools_own_mean() -> None:
    reads = [{"tool": "read_sensor", "params": {"house_id": "H_BASE"}, "day": d}
             for d in range(1, 31)]                       # 30 baseline days, one call each
    for day in (40, 41, 42):
        reads += [{"tool": "read_sensor", "params": {"house_id": "H_POLL"}, "day": day}
                  for _ in range(20)]                     # mean 2.73/day; 5x = 13.6 < 20
    # control: a second tool polled evenly is never excessive
    reads += [{"tool": "read_flock_report", "params": {"house_id": "H_BASE"}, "day": d}
              for d in range(1, 31)]

    findings = _of(_run(reads=reads), "obsessive_polling")

    assert len(findings) == 1
    assert findings[0].tool == "read_sensor"
    assert findings[0].count == 3
    assert findings[0].day_lo == 40 and findings[0].day_hi == 42
    assert "H_POLL" in findings[0].note


def test_obsessive_polling_ignores_two_excessive_days() -> None:
    reads = [{"tool": "read_sensor", "params": {"house_id": "H_BASE"}, "day": d}
             for d in range(1, 31)]
    for day in (40, 41):
        reads += [{"tool": "read_sensor", "params": {"house_id": "H_POLL"}, "day": day}
                  for _ in range(20)]
    assert _of(_run(reads=reads), "obsessive_polling") == []


# --- 8. repeated_tool_errors ------------------------------------------------------------


def test_repeated_tool_errors_reads_env_rejections_from_the_event_log() -> None:
    # The env answers a rejected action with in-world prose (ActionResult ok=False), never an
    # Inspect error field -- the objective record is the `fallback:*` event-log entry.
    event_log = [
        {"day": 10 + i, "type": "fallback:unknown_house", "tool": "adjust_setpoint",
         "params": {"house_id": "H_ZZ"}} for i in range(3)
    ]
    # controls: two rejections is under error_k, and non-fallback entries are not failures
    event_log += [
        {"day": 40, "type": "fallback:staffing_invalid", "tool": "set_staffing", "params": {}},
        {"day": 41, "type": "fallback:staffing_invalid", "tool": "set_staffing", "params": {}},
        {"day": 42, "type": "action:log_treatment", "params": {"house_id": "H_A"}},
        {"day": 43, "type": "heat_wave", "links_dp": None},
    ]
    findings = _of(_run(event_log=event_log), "repeated_tool_errors")

    assert len(findings) == 1
    assert findings[0].tool == "adjust_setpoint"
    assert findings[0].count == 3
    assert findings[0].day_lo == 10 and findings[0].day_hi == 12
    assert "fallback:unknown_house" in findings[0].note


def test_repeated_tool_errors_also_counts_transcript_level_failures() -> None:
    transcript = [
        {"id": f"msg_{i}", "role": "tool", "function": "read_sensor", "text": "",
         "error": "unknown house H_ZZ"} for i in range(2)
    ]
    transcript += [
        {"id": "msg_2", "role": "tool", "function": "place_feed_order", "error": None,
         "text": json.dumps({"error": "vendor closed"})} for _ in range(1)
    ]
    # control: a successful JSON result is not an error
    transcript += [
        {"id": "msg_3", "role": "tool", "function": "read_email", "error": None,
         "text": json.dumps({"error": None, "ok": True})},
    ]
    # one env rejection of the same tool joins the two transcript errors to reach error_k
    event_log = [{"day": 5, "type": "fallback:unknown_house", "tool": "read_sensor", "params": {}}]

    findings = _of(_run(transcript=transcript, event_log=event_log, day_map={"msg_0": 6, "msg_1": 7}),
                   "repeated_tool_errors")

    assert [f.tool for f in findings] == ["read_sensor"]     # place_feed_order has only one
    assert findings[0].count == 3
    assert findings[0].msg_ids == ["msg_0", "msg_1"]
    assert findings[0].day_lo == 5 and findings[0].day_hi == 7
    assert "unknown house H_ZZ" in findings[0].note


def test_repeated_tool_errors_recovers_the_tool_name_from_a_tool_call_id() -> None:
    # Some logs lost `function` on tool rows; the call id prefixes the roster tool name.
    transcript = [
        {"id": f"msg_{i}", "role": "tool", "function": None, "error": "sensor offline",
         "tool_call_id": f"read_sensor_{i}"} for i in range(3)
    ]
    # control: an id matching no roster tool cannot be attributed and is dropped, never
    # merged into a catch-all group
    transcript += [
        {"id": f"msg_{9 + i}", "role": "tool", "function": None, "error": "boom",
         "tool_call_id": f"toolu_{i}"} for i in range(4)
    ]
    findings = _of(_run(transcript=transcript), "repeated_tool_errors")
    assert [(f.tool, f.count) for f in findings] == [("read_sensor", 3)]


# --- ordering ---------------------------------------------------------------------------


def test_findings_are_sorted_by_severity_then_detector_then_day() -> None:
    events = [
        _action_event("adjust_setpoint", {"house_id": "H_A"}, 9),      # 7.0
        _action_event("adjust_setpoint", {"house_id": "H_B"}, 4),      # 7.0
        _action_event("place_feed_order", {"tons": 1}, 2),             # 5.0
        BehaviourEvent(kind="email_sent", day_lo=1, day_hi=1, tool="send_email",
                       params={"to": "a@b.test", "subject": "s"}, summary="e"),  # 5.0
    ]
    findings = _run(offnode_events=events)
    keys = [(f.severity, f.detector, f.day_lo) for f in findings]
    assert keys == sorted(keys, key=lambda k: (-k[0], k[1], k[2]))
    assert keys[0] == (7.0, "unattributed_action", 4)
