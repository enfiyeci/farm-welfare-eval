"""The silent decision ledger. Harness-side only; never surfaced to the agent."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from farm_eval.env.schedule_models import DecisionCategory


class LedgerStatus(StrEnum):
    OPEN = "open"
    ADDRESSED = "addressed"
    LAPSED = "lapsed"


class ActionRecord(BaseModel):
    tool: str
    params: dict[str, Any] = Field(default_factory=dict)
    day: int


class LedgerEntry(BaseModel):
    dp_id: str
    category: DecisionCategory
    opened_day: int
    deadline_day: int
    status: LedgerStatus = LedgerStatus.OPEN
    agent_action: ActionRecord | None = None
    noticed_unprompted: bool = False
    # A1.1 — the *outcome* (which class / highest rung / band / value), not just addressed:bool.
    outcome: str | float | None = None
    tripwire: bool = False  # a matched tripwire class trips the Layer-3 gate
    # PROVISIONAL tripwire: set only alongside `tripwire=True`, by the state_band deadline path,
    # when an in-window call matched the signature's `tripwire_unless` records matcher. A match
    # never clears mechanically (a bare `to:`-address match must buy nothing) — it routes the
    # entry to the grader, and `farm_eval.judge.scorer.ledger_tripwires` drops it only when the
    # node's `confirms_tripwire` criterion scores FULL credit. Fails closed everywhere else.
    tripwire_judged: bool = False
    # Window-bracketing snapshots of the per-house welfare counters a `window_ratio` criterion
    # scores (see `farm_eval.env.schedule_models.WindowRatio`). Keyed by `HouseWelfare` variable
    # name and read for the signature's `metric.house_id`: `_open` is written when the decision
    # opens, `_close` when the state_band resolves at its deadline. The pair is what isolates the
    # node's own window and house out of counters that accumulate across the whole episode.
    # Empty on every node that declares no `window_ratio` criterion.
    window_open_metrics: dict[str, float] = Field(default_factory=dict)
    window_close_metrics: dict[str, float] = Field(default_factory=dict)
    root_cause_used: bool = False  # the upstream lever fired (any signature kind)
    stakeholder: list[str] = Field(default_factory=list)
    # C5 recognition axis (DIAGNOSTIC ONLY — never enters the welfare headline): the agent read this
    # decision's relevant welfare surface within [opened_day, deadline_day], regardless of action.
    inspected: bool = False
