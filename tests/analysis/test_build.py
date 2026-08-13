"""Task 9 -- the behaviour-model orchestrator, and its scripted-episode golden.

The integration half runs ONE scripted keyless `mockllm` episode per module (the repo's
end-to-end pattern) through `build_behaviour_model` and asserts the result against the committed
golden. The episode and the golden come from `scripts/regen_behaviour_golden.py`, imported here so
the test and the golden are the same episode by construction -- the same arrangement
`tests/spectator/test_extract.py` uses with `scripts/regen_spectator_golden.py`.

The unit half pins the two joins the orchestrator owns and no earlier task could test: the
`msg_N` link onto action/read events (spec §2.1) and the two-clock cross-check (spec §2.2).
"""

from __future__ import annotations

import pytest

import json
from pathlib import Path

import pytest

from farm_eval.analysis import build as build_module
from farm_eval.analysis.build import (
    _cross_check_clock,
    _errors_by_tool,
    _events_in_row_order,
    _link_email_msg_ids,
    _link_msg_ids,
    build_behaviour_model,
)
from farm_eval.analysis.model import Attribution, BehaviourEvent
from farm_eval.analysis.offnode import THRESHOLDS
from farm_eval.spectator.events import DayStart, ToolCallEvent
from scripts.regen_behaviour_golden import (
    GOLDEN_PATH,
    PLACEHOLDER_SHA256,
    build_golden_model,
    normalize_model,
)

_FIXTURE_DP = "DP_PLACEHOLDER_1"


@pytest.fixture(scope="module")
def episode(tmp_path_factory) -> tuple[str, object]:
    """The scripted episode's log location and the behaviour model built from it."""
    return build_golden_model(tmp_path_factory.mktemp("behaviour"))


@pytest.fixture(scope="module")
def model(episode):
    return episode[1]


# --- the run header -------------------------------------------------------------------


def test_the_scripted_episode_replays_at_full_fidelity(model) -> None:
    assert model.feed_fidelity == "full"
    assert model.fidelity_failure_day is None


def test_the_recorded_clock_reconciles(model) -> None:
    assert model.day_map_valid is True


def test_the_header_carries_the_run_identity_and_every_threshold(model) -> None:
    assert len(model.source_sha256) == 64
    assert model.target_model == "mockllm/model"
    assert model.thresholds == dict(THRESHOLDS)
    assert model.schema_version == 1
    assert model.reader_verdicts == []


# --- the stages are actually wired ----------------------------------------------------


def test_the_fixture_decision_point_has_a_strong_behavioural_record(model) -> None:
    dossier = next(d for d in model.dossiers if d.dp_id == _FIXTURE_DP)
    assert dossier.strong, "the scripted adjust_setpoint must attribute strongly to the node"
    assert any(e.tool == "adjust_setpoint" for e in dossier.strong)


def test_the_scripted_calls_appear_in_the_tool_profiles(model) -> None:
    profiles = {p.tool: p for p in model.tool_profiles}
    assert profiles["send_email"].total_calls == 1
    assert profiles["schedule_maintenance"].total_calls == 1
    assert profiles["end_day"].total_calls >= 1


def test_the_digest_is_day_segmented_and_carries_entries(model) -> None:
    assert model.digest, "a full-fidelity episode must produce digest days"
    assert [d.day for d in model.digest] == sorted(d.day for d in model.digest)
    assert any(day.entries for day in model.digest)


def test_action_events_carry_their_msg_n_link(model) -> None:
    dossier = next(d for d in model.dossiers if d.dp_id == _FIXTURE_DP)
    setpoint = next(e for e in dossier.strong if e.tool == "adjust_setpoint")
    assert setpoint.msg_id is not None and setpoint.msg_id.startswith("msg_")


# --- the golden -----------------------------------------------------------------------


def test_the_built_model_matches_the_committed_golden(model) -> None:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert normalize_model(model) == golden, (
        "behaviour model drifted from the golden; regenerate with "
        "./venv/bin/python scripts/regen_behaviour_golden.py and review the diff"
    )


def test_normalization_replaces_the_per_run_source_hash(model) -> None:
    assert normalize_model(model)["source_sha256"] == PLACEHOLDER_SHA256


# --- the msg_N link (spec §2.1) -------------------------------------------------------


def _assistant(msg_id: str, function: str, arguments: dict) -> dict:
    return {
        "id": msg_id,
        "role": "assistant",
        "text": "",
        "tool_calls": [{"id": f"{function}_x", "function": function, "arguments": arguments}],
    }


def _event(tool: str, params: dict, day: int) -> BehaviourEvent:
    return BehaviourEvent(kind="action", day_lo=day, day_hi=day, tool=tool, params=params)


def test_row_order_recovers_every_call_event_exactly_once() -> None:
    """The link runs over this list, so a drop loses a msg_N and a duplicate steals one.

    The two hard cases are planted together: an event attributed to TWO overlapping windows
    (one shared object appearing twice in `attributions` -- must collapse to one) and two
    *identical* same-day calls (indistinguishable by content -- neither may take the other's
    slot). The read row proves actions still come before reads.
    """
    args = {"house_id": "H_A", "system": "ventilation", "value": 1.0}
    actions = [{"tool": "adjust_setpoint", "params": args, "day": 4}] * 2
    reads = [{"tool": "read_sensor", "params": {"house_id": "H_A", "metric": "ammonia_ppm"}, "day": 4}]

    shared = _event("adjust_setpoint", args, 4)          # strong to two nodes
    lone = _event("adjust_setpoint", args, 4)            # the identical twin, off-node
    read = BehaviourEvent(
        kind="read", day_lo=4, day_hi=4, tool="read_sensor",
        params={"house_id": "H_A", "metric": "ammonia_ppm"},
    )
    attributions = [
        Attribution(event=shared, dp_id="DP_A", strength="strong"),
        Attribution(event=shared, dp_id="DP_B", strength="strong"),
        Attribution(event=read, dp_id="DP_A", strength="strong"),
    ]

    ordered = _events_in_row_order(actions, reads, [], attributions, [lone])

    assert [e.kind for e in ordered] == ["action", "action", "read"]
    assert {id(e) for e in ordered} == {id(shared), id(lone), id(read)}


def test_row_order_recovers_outbound_email_events_after_the_calls() -> None:
    """Email events join the same ordered list, so the email link can traverse it.

    The key is rebuilt from the outbound ROW using `attribute._EMAIL_PARAM_KEYS`, which is why the
    row here carries a `body` the event never keeps: a key built from the whole row would miss.
    """
    outbound = [{"id": "m1", "to": "vet@x.test", "subject": "H2", "body": "…", "day": 4}]
    email = BehaviourEvent(
        kind="email_sent", day_lo=4, day_hi=4, tool="send_email",
        params={"id": "m1", "to": "vet@x.test", "subject": "H2"},
    )

    ordered = _events_in_row_order([], [], outbound, [], [email])

    assert [id(e) for e in ordered] == [id(email)]


def test_two_identical_calls_on_one_day_claim_two_distinct_messages_in_order() -> None:
    args = {"house_id": "H_A", "system": "ventilation", "value": 1.0}
    transcript = [_assistant("msg_1", "adjust_setpoint", args), _assistant("msg_3", "adjust_setpoint", args)]
    day_map = {"msg_1": 4, "msg_3": 4}
    first, second = _event("adjust_setpoint", args, 4), _event("adjust_setpoint", args, 4)

    _link_msg_ids([first, second], transcript, day_map)

    assert (first.msg_id, second.msg_id) == ("msg_1", "msg_3")


def test_an_unmatched_event_keeps_no_msg_id() -> None:
    transcript = [_assistant("msg_1", "adjust_setpoint", {"house_id": "H_A"})]
    event = _event("place_feed_order", {"ration": "LP2"}, 4)

    _link_msg_ids([event], transcript, {"msg_1": 4})

    assert event.msg_id is None


def test_a_call_on_a_different_day_is_not_claimed_when_the_clock_is_trusted() -> None:
    args = {"house_id": "H_A"}
    transcript = [_assistant("msg_1", "adjust_setpoint", args)]
    event = _event("adjust_setpoint", args, 9)

    _link_msg_ids([event], transcript, {"msg_1": 4})

    assert event.msg_id is None


def test_without_a_trusted_clock_the_day_is_not_required_to_agree() -> None:
    args = {"house_id": "H_A"}
    transcript = [_assistant("msg_1", "adjust_setpoint", args)]
    event = _event("adjust_setpoint", args, 9)

    _link_msg_ids([event], transcript, None)

    assert event.msg_id == "msg_1"


# --- the email msg_N link, one hop later (spec §2.1) ----------------------------------


def _send(to: str, subject: str, day: int, msg_id: str | None = None) -> BehaviourEvent:
    return BehaviourEvent(
        kind="action", day_lo=day, day_hi=day, tool="send_email", msg_id=msg_id,
        params={"to": to, "subject": subject, "body": "…"},
    )


def _email(to: str, subject: str, day: int) -> BehaviourEvent:
    return BehaviourEvent(
        kind="email_sent", day_lo=day, day_hi=day, tool="send_email",
        params={"to": to, "subject": subject},
    )


def _send_call(msg_id: str, to: str, subject: str) -> dict:
    return {
        "id": msg_id,
        "role": "assistant",
        "text": "",
        "tool_calls": [
            {"id": "c", "function": "send_email",
             "arguments": {"to": to, "subject": subject, "body": "…"}},
        ],
    }


def test_an_email_inherits_the_msg_id_of_the_call_that_sent_it() -> None:
    send = _send("vet@x.test", "H2 mortality", 12, msg_id="msg_9")
    email = _email("vet@x.test", "H2 mortality", 12)

    _link_email_msg_ids([send, email], [], None)

    assert email.msg_id == "msg_9"


def test_two_same_day_emails_claim_two_distinct_actions_in_order() -> None:
    """Row order decides, so two messages sent on one day do not both point at the first call."""
    first = _send("vet@x.test", "H2", 12, msg_id="msg_9")
    second = _send("vet@x.test", "H2", 12, msg_id="msg_11")
    email_a, email_b = _email("vet@x.test", "H2", 12), _email("vet@x.test", "H2", 12)

    _link_email_msg_ids([first, second, email_a, email_b], [], None)

    assert (email_a.msg_id, email_b.msg_id) == ("msg_9", "msg_11")


def test_an_email_whose_action_never_linked_falls_back_to_the_transcript() -> None:
    """The tier that actually carries a real run's mail.

    `_link_msg_ids` leaves every `send_email` action unlinked -- the adapter records `cc` and
    `in_reply_to` that the model never passed, so its exact argument equality can never hold --
    which is why the primary pairing alone hands every email a `None`.
    """
    send = _send("vet@x.test", "H2", 12)                      # msg_id stayed None
    email = _email("vet@x.test", "H2", 12)
    transcript = [_send_call("msg_9", "vet@x.test", "H2")]

    _link_email_msg_ids([send, email], transcript, {"msg_9": 12})

    assert email.msg_id == "msg_9"


def test_two_same_day_emails_claim_two_distinct_transcript_calls_in_order() -> None:
    email_a, email_b = _email("vet@x.test", "H2", 12), _email("vet@x.test", "H2", 12)
    transcript = [_send_call("msg_9", "vet@x.test", "H2"), _send_call("msg_11", "vet@x.test", "H2")]

    _link_email_msg_ids([email_a, email_b], transcript, {"msg_9": 12, "msg_11": 12})

    assert (email_a.msg_id, email_b.msg_id) == ("msg_9", "msg_11")


def test_the_two_tiers_never_claim_the_same_transcript_call() -> None:
    """One shared claimed set: an email linked by the primary tier retires its call.

    Both emails have the same recipient, subject and day, and both transcript calls therefore
    match either of them. The first links through its paired action (which already carries
    `msg_9`); without the shared claim set the second falls through to the fallback tier, scans
    from index 0 and takes `msg_9` as well, so one real message vanishes from the evidence.
    """
    send = _send("vet@x.test", "H2", 12, msg_id="msg_9")      # only the FIRST action linked
    email_a, email_b = _email("vet@x.test", "H2", 12), _email("vet@x.test", "H2", 12)
    transcript = [_send_call("msg_9", "vet@x.test", "H2"), _send_call("msg_11", "vet@x.test", "H2")]

    _link_email_msg_ids([send, email_a, email_b], transcript, {"msg_9": 12, "msg_11": 12})

    assert (email_a.msg_id, email_b.msg_id) == ("msg_9", "msg_11")


def test_an_email_matching_no_call_at_all_keeps_no_msg_id() -> None:
    """A link is a bonus, never a guess: neither tier matches, so the residual stays pointer-less."""
    send = _send("vet@x.test", "H2", 12)
    email = _email("vet@x.test", "H2", 12)
    transcript = [_send_call("msg_9", "mgr@x.test", "COP")]   # a different message entirely

    _link_email_msg_ids([send, email], transcript, {"msg_9": 12})

    assert email.msg_id is None


def test_the_transcript_fallback_respects_a_trusted_clock() -> None:
    email = _email("vet@x.test", "H2", 12)
    transcript = [_send_call("msg_9", "vet@x.test", "H2")]

    _link_email_msg_ids([email], transcript, {"msg_9": 4})

    assert email.msg_id is None


def test_an_email_is_not_paired_with_an_action_on_another_day() -> None:
    send = _send("vet@x.test", "H2", 11, msg_id="msg_9")
    email = _email("vet@x.test", "H2", 12)

    _link_email_msg_ids([send, email], [], None)

    assert email.msg_id is None


def test_outbound_emails_in_the_built_model_carry_their_pointer(model) -> None:
    """End to end on the scripted episode: its one `send_email` produces a linked email event."""
    emails = [
        event
        for dossier in model.dossiers
        for event in [*dossier.strong, *dossier.ambient]
        if event.kind == "email_sent"
    ]
    assert emails, "the scripted episode sends one email"
    assert all(e.msg_id is not None and e.msg_id.startswith("msg_") for e in emails)


# --- the two-clock cross-check (spec §2.2) --------------------------------------------


def _feed_call(msg_id: str, day: int, tool: str = "read_sensor"):
    return ToolCallEvent(seq=0, day=day, tool=tool, args={}, msg_id=msg_id)


def _anchor_row(msg_id: str, call_id: str) -> dict:
    return {
        "id": msg_id,
        "role": "assistant",
        "text": "",
        "tool_calls": [{"id": call_id, "function": "read_sensor", "arguments": {}}],
    }


def test_a_clock_that_drifts_mid_episode_and_reconciles_at_the_end_fails_loudly() -> None:
    """The endpoint check alone accepts this, and it is the case that matters.

    The two clocks agree on the last day, so a final-day comparison passes -- while every day
    stamp in the middle of the episode is wrong. Each shared tool call is an anchor with a day on
    both sides, so the disagreement is visible call by call.
    """
    transcript = [_anchor_row("msg_1", "c1"), _anchor_row("msg_5", "c2"), _anchor_row("msg_9", "c3")]
    day_map = {"msg_1": 3, "msg_5": 40, "msg_9": 90}         # the feed's day 20 became 40
    feed = [
        _feed_call("c1", 3), _feed_call("c2", 20), _feed_call("c3", 90),
        DayStart(seq=9, day=90, date="2025-09-07", season="summer"),
    ]

    with pytest.raises(ValueError, match="clock") as error:
        _cross_check_clock(feed, transcript, day_map)

    assert "'c2'" in str(error.value) and "20" in str(error.value) and "40" in str(error.value)


def test_agreeing_anchors_and_endpoints_pass() -> None:
    transcript = [_anchor_row("msg_1", "c1"), _anchor_row("msg_5", "c2")]
    feed = [
        _feed_call("c1", 3), _feed_call("c2", 20),
        DayStart(seq=9, day=20, date="2025-06-29", season="summer"),
    ]

    _cross_check_clock(feed, transcript, {"msg_1": 3, "msg_5": 20})


def test_the_endpoint_check_still_runs_when_no_anchor_is_shared() -> None:
    """A feed whose calls join nothing still has its last day frame compared."""
    feed = [DayStart(seq=1, day=90, date="2025-09-07", season="summer")]

    with pytest.raises(ValueError, match="last day frame"):
        _cross_check_clock(feed, [], {"msg_1": 3})


def test_a_day_map_that_disagrees_with_the_feed_clock_fails_loudly(episode, monkeypatch) -> None:
    log_location, _ = episode
    real_extract = build_module.extract

    def doctored(path):
        report_model = real_extract(path)
        report_model["day_map"] = {mid: day + 100 for mid, day in report_model["day_map"].items()}
        return report_model

    monkeypatch.setattr(build_module, "extract", doctored)
    with pytest.raises(ValueError, match="clock"):
        build_behaviour_model(log_location)


# --- error classification -------------------------------------------------------------


def test_errors_by_tool_counts_harness_errors_and_in_band_json_errors() -> None:
    transcript = [
        {"id": "msg_1", "role": "tool", "function": "read_sensor", "text": "", "error": "boom"},
        {"id": "msg_2", "role": "tool", "function": "read_sensor",
         "text": json.dumps({"error": "no sensor"}), "error": None},
        {"id": "msg_3", "role": "tool", "function": "read_sensor",
         "text": json.dumps({"value": 4.2}), "error": None},
        {"id": "msg_4", "role": "assistant", "text": json.dumps({"error": "not a tool row"})},
    ]

    assert _errors_by_tool(transcript) == {"read_sensor": 2}


def test_a_clean_transcript_has_no_tool_errors() -> None:
    assert _errors_by_tool([{"id": "msg_1", "role": "tool", "function": "read_sensor",
                             "text": "ok", "error": None}]) == {}
