"""Typed events for the spectator dashboard's NDJSON feed.

One JSON object per line, one line per event, `kind` as the discriminator. The feed is the
only contract between the run-side emitter and the viewer page: everything the page renders
arrives as one of these events, so the page never reads env state or corpus content directly.

Nothing here is farm-specific -- house/flock/breed content travels as data in the model
fields (`houses`, `breed_standard`, `breed_label`, ...), loaded on the emitting side.

Envelope fields carried by every event (spec §3):
- `seq`   -- monotonic per-run sequence number; the page's ordering and resume cursor.
- `day`   -- integer day index, `None` when the event is outside a day (e.g. run metadata).
- `ts_in_world` -- in-world timestamp string, `None` when unknown.
"""

from __future__ import annotations

import json
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

# Schema drift must fail loudly in both directions: an emitter writing a field the models
# don't carry, and a viewer parsing a feed written by a newer emitter, both raise at the
# boundary instead of silently dropping data.
_FORBID = ConfigDict(extra="forbid")


class FeedEventBase(BaseModel):
    """Shared envelope. Subclasses add `kind` plus their own payload fields."""

    model_config = _FORBID

    seq: int
    day: int | None = None
    ts_in_world: str | None = None


class RunMeta(FeedEventBase):
    """Emitted once at the head of a feed: what run this is and how to scale the charts."""

    kind: Literal["run_meta"] = "run_meta"
    run_id: str
    sample_id: str          # the Inspect sample uuid
    target: str
    grader: str
    first_day: int
    last_day: int
    config_path: str
    enabled_nodes: int
    # (age_wk, hdep_pct) pairs from ModelParams -- the page draws the breed reference curve
    # from these rather than hardcoding a standard.
    breed_standard: list[tuple[float, float]] | None = None
    breed_label: str | None = None


class DayStart(FeedEventBase):
    kind: Literal["day_start"] = "day_start"
    date: str
    season: str
    weather: dict[str, Any] | None = None


class DayEnd(FeedEventBase):
    kind: Literal["day_end"] = "day_end"


class AssistantText(FeedEventBase):
    kind: Literal["assistant_text"] = "assistant_text"
    text: str
    msg_id: str | None = None
    reasoning: bool = False


class ToolCallEvent(FeedEventBase):
    kind: Literal["tool_call"] = "tool_call"
    tool: str
    args: dict[str, Any]
    result_summary: str | None = None
    cost_cents: float | None = None
    msg_id: str | None = None


class EmailDelivered(FeedEventBase):
    kind: Literal["email_delivered"] = "email_delivered"
    email_id: str
    sender: str
    subject: str
    body: str


class EmailRead(FeedEventBase):
    kind: Literal["email_read"] = "email_read"
    email_id: str


class EmailSent(FeedEventBase):
    kind: Literal["email_sent"] = "email_sent"
    email_id: str | None = None   # outbound mailbox id, e.g. "out-0-0"
    to: str                       # the `send_email` tool arg is `to`, not "recipient"
    subject: str | None = None
    body: str


class StateSnapshot(FeedEventBase):
    kind: Literal["state_snapshot"] = "state_snapshot"
    houses: list[dict[str, Any]]
    totals: dict[str, Any]
    finance: dict[str, Any]


class DecisionWindow(FeedEventBase):
    kind: Literal["decision_window"] = "decision_window"
    dp_id: str
    opens: int
    deadline: int


class DecisionResolved(FeedEventBase):
    kind: Literal["decision_resolved"] = "decision_resolved"
    dp_id: str
    outcome: str | None = None
    tripwire: bool = False
    latency_days: int | None = None


class RunHealth(FeedEventBase):
    kind: Literal["run_health"] = "run_health"
    turns: int
    blank_streak: int
    retries: int
    tokens_in: int
    tokens_out: int
    wallclock_s: float


class EpisodeEnd(FeedEventBase):
    kind: Literal["episode_end"] = "episode_end"
    status: str


FeedEvent = Annotated[
    RunMeta
    | DayStart
    | DayEnd
    | AssistantText
    | ToolCallEvent
    | EmailDelivered
    | EmailRead
    | EmailSent
    | StateSnapshot
    | DecisionWindow
    | DecisionResolved
    | RunHealth
    | EpisodeEnd,
    Field(discriminator="kind"),
]

_adapter: TypeAdapter[FeedEvent] = TypeAdapter(FeedEvent)


def dump_feed_line(event: FeedEvent) -> str:
    """Serialize one event to a single NDJSON line (no trailing newline).

    `json.dumps` escapes any newline inside a body/text field, so the result is always one
    physical line; `ensure_ascii=False` keeps non-ASCII prose readable in the feed file.
    """
    return json.dumps(event.model_dump(mode="json"), separators=(",", ":"), ensure_ascii=False)


def parse_feed_line(line: str) -> FeedEvent:
    """Parse one NDJSON line back into its event model.

    Raises `pydantic.ValidationError` on an unknown `kind`, a missing field, or an extra one.
    """
    return _adapter.validate_json(line)
