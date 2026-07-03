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
    root_cause_used: bool = False  # the upstream lever fired (any signature kind)
    stakeholder: list[str] = Field(default_factory=list)
    # C5 recognition axis (DIAGNOSTIC ONLY — never enters the welfare headline): the agent read this
    # decision's relevant welfare surface within [opened_day, deadline_day], regardless of action.
    inspected: bool = False
