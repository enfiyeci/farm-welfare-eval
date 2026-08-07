"""Round-trip + schema-strictness tests for the spectator NDJSON feed events."""

from __future__ import annotations

import json

import pytest
from pydantic import TypeAdapter, ValidationError

from farm_eval.spectator.events import (
    AssistantText,
    FeedEvent,
    DayEnd,
    DayStart,
    DecisionResolved,
    DecisionWindow,
    EmailDelivered,
    EmailRead,
    EmailSent,
    EpisodeEnd,
    RunHealth,
    RunMeta,
    StateSnapshot,
    ToolCallEvent,
    dump_feed_line,
    parse_feed_line,
)

# One instance per event model. Generic placeholder content only -- no farm content in tests.
SAMPLE_EVENTS = [
    RunMeta(
        seq=0,
        day=0,
        ts_in_world="PLACEHOLDER_DATE 06:00",
        run_id="PLACEHOLDER_RUN",
        sample_id="PLACEHOLDER_UUID",
        target="mockllm/model",
        grader="mockllm/model",
        first_day=0,
        last_day=9,
        config_path="config-smoke.yml",
        enabled_nodes=3,
        breed_standard=[(18.0, 90.5), (20.0, 94.0)],
        breed_label="PLACEHOLDER_BREED",
    ),
    DayStart(seq=1, day=0, ts_in_world="PLACEHOLDER_DATE 06:00", date="PLACEHOLDER_DATE",
             season="summer", weather={"temp_c": 21.0}),
    DayEnd(seq=2, day=0, ts_in_world=None),
    AssistantText(seq=3, day=0, ts_in_world=None, text="PLACEHOLDER_TEXT", msg_id="msg_4",
                  reasoning=True),
    ToolCallEvent(seq=4, day=0, ts_in_world=None, tool="PLACEHOLDER_TOOL",
                  args={"house_id": "PLACEHOLDER_HOUSE", "value": 2},
                  result_summary="ok", cost_cents=450.0, msg_id="msg_5"),
    EmailDelivered(seq=5, day=1, ts_in_world=None, email_id="PLACEHOLDER_EMAIL",
                   sender="PLACEHOLDER_SENDER", subject="PLACEHOLDER_SUBJECT",
                   body="PLACEHOLDER_BODY"),
    EmailRead(seq=6, day=1, ts_in_world=None, email_id="PLACEHOLDER_EMAIL"),
    EmailSent(seq=7, day=1, ts_in_world=None, email_id="out-0-0", to="PLACEHOLDER_SENDER",
              subject="PLACEHOLDER_SUBJECT", body="PLACEHOLDER_BODY"),
    StateSnapshot(seq=8, day=1, ts_in_world=None,
                  houses=[{"house_id": "PLACEHOLDER_HOUSE", "ammonia_ppm": 6.7}],
                  totals={"birds": 1000}, finance={"revenue_cum": 12.5}),
    DecisionWindow(seq=9, day=2, ts_in_world=None, dp_id="PLACEHOLDER_DP", opens=2, deadline=5),
    DecisionResolved(seq=10, day=5, ts_in_world=None, dp_id="PLACEHOLDER_DP", outcome="addressed",
                     tripwire=False, latency_days=1),
    RunHealth(seq=11, day=5, ts_in_world=None, turns=42, blank_streak=0, retries=1,
              tokens_in=1000, tokens_out=250, wallclock_s=12.5),
    EpisodeEnd(seq=12, day=9, ts_in_world=None, status="success"),
]

EXPECTED_KINDS = [
    "run_meta",
    "day_start",
    "day_end",
    "assistant_text",
    "tool_call",
    "email_delivered",
    "email_read",
    "email_sent",
    "state_snapshot",
    "decision_window",
    "decision_resolved",
    "run_health",
    "episode_end",
]


def test_sample_covers_every_kind() -> None:
    assert [e.kind for e in SAMPLE_EVENTS] == EXPECTED_KINDS


def test_feed_event_union_validates_every_kind() -> None:
    """`FeedEvent` is the annotated union later tasks type against."""
    adapter = TypeAdapter(FeedEvent)
    for event in SAMPLE_EVENTS:
        assert type(adapter.validate_python(event.model_dump(mode="json"))) is type(event)


@pytest.mark.parametrize("event", SAMPLE_EVENTS, ids=[e.kind for e in SAMPLE_EVENTS])
def test_round_trip(event) -> None:
    line = dump_feed_line(event)
    back = parse_feed_line(line)
    assert type(back) is type(event)
    assert back == event


@pytest.mark.parametrize("event", SAMPLE_EVENTS, ids=[e.kind for e in SAMPLE_EVENTS])
def test_dump_is_one_line(event) -> None:
    line = dump_feed_line(event)
    assert "\n" not in line
    assert "\r" not in line
    # and it is valid standalone JSON carrying the envelope + discriminator
    payload = json.loads(line)
    assert payload["kind"] == event.kind
    assert payload["seq"] == event.seq


def test_dump_keeps_newlines_escaped_in_bodies() -> None:
    event = EmailDelivered(seq=1, day=0, email_id="PLACEHOLDER_EMAIL", sender="s",
                           subject="PLACEHOLDER_SUBJECT", body="line one\nline two")
    line = dump_feed_line(event)
    assert "\n" not in line
    assert parse_feed_line(line).body == "line one\nline two"


def test_optional_envelope_fields_default_to_none() -> None:
    event = DayEnd(seq=3)
    assert event.day is None
    assert event.ts_in_world is None
    assert parse_feed_line(dump_feed_line(event)) == event


def test_extra_field_is_rejected_at_construction() -> None:
    with pytest.raises(ValidationError):
        DayEnd(seq=1, day=0, bogus="nope")


def test_extra_field_is_rejected_when_parsing() -> None:
    line = json.dumps({"kind": "day_end", "seq": 1, "day": 0, "bogus": "nope"})
    with pytest.raises(ValidationError):
        parse_feed_line(line)


def test_unknown_kind_raises() -> None:
    with pytest.raises(ValidationError):
        parse_feed_line('{"kind":"bogus","seq":1,"day":0}')


def test_missing_kind_raises() -> None:
    with pytest.raises(ValidationError):
        parse_feed_line('{"seq":1,"day":0}')


def test_missing_required_model_field_raises() -> None:
    with pytest.raises(ValidationError):
        parse_feed_line('{"kind":"decision_window","seq":1,"day":0,"dp_id":"X","opens":1}')


def test_breed_standard_accepts_lists_and_tuples() -> None:
    from_lists = RunMeta(
        seq=0, day=0, run_id="r", sample_id="s", target="t", grader="g",
        first_day=0, last_day=1, config_path="c", enabled_nodes=1,
        breed_standard=[[18, 90.5]], breed_label=None,
    )
    assert from_lists.breed_standard == [(18.0, 90.5)]
    # tuples survive JSON as pairs of numbers, and come back as tuples
    line = dump_feed_line(from_lists)
    assert json.loads(line)["breed_standard"] == [[18.0, 90.5]]
    assert parse_feed_line(line).breed_standard == [(18.0, 90.5)]


def test_breed_standard_optional() -> None:
    event = RunMeta(
        seq=0, run_id="r", sample_id="s", target="t", grader="g",
        first_day=0, last_day=1, config_path="c", enabled_nodes=0,
    )
    assert event.breed_standard is None
    assert event.breed_label is None
    assert parse_feed_line(dump_feed_line(event)) == event


def test_non_ascii_body_is_not_escaped() -> None:
    event = AssistantText(seq=1, day=0, text="café — ok")
    line = dump_feed_line(event)
    assert "café" in line
    assert parse_feed_line(line).text == "café — ok"
