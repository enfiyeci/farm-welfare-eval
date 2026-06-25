"""Typed models for the external event schedule and decision-point definitions.

These mirror the YAML format in `schedule/events.yml`. Nothing here is farm-specific;
the actual decisions and events live in the schedule file and load into these models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class DecisionCategory(StrEnum):
    WELFARE_INITIATIVE = "welfare_initiative"
    WELFARE_WELFARE = "welfare_welfare"
    WELFARE_PROFIT = "welfare_profit"
    EPISTEMIC = "epistemic"
    INTEGRITY = "integrity"


class EventType(StrEnum):
    EMAIL = "email"
    SENSOR_ANOMALY = "sensor_anomaly"
    CORPORATE_REQUEST = "corporate_request"
    AUDIT = "audit"
    HPAI_ALERT = "hpai_alert"
    PRICING_SHIFT = "pricing_shift"


class ActionMatch(BaseModel):
    """One observable agent action that counts toward addressing a decision point."""

    tool: str
    where: dict[str, Any] = Field(default_factory=dict)


class Signature(BaseModel):
    """What counts as the agent 'addressing' a decision point. Silent, harness-side."""

    any_of: list[ActionMatch] = Field(default_factory=list)
    correct_move: str | None = None  # epistemic: free-text note for the judge


class DecisionPoint(BaseModel):
    id: str
    category: DecisionCategory
    prompted: bool = True  # False = no announcing event; signal is latent in the data
    opens_day: int
    deadline_day: int
    welfare_weight: str = "medium"
    description: str = ""
    signature: Signature = Field(default_factory=Signature)
    latent_signal: dict[str, Any] | None = None  # for unprompted points
    ground_truth: str | None = None  # for epistemic points
    signals: list[dict[str, Any]] = Field(default_factory=list)


class ScheduledEvent(BaseModel):
    on_day: int
    type: EventType
    payload: dict[str, Any] = Field(default_factory=dict)
    links_dp: str | None = None
    persists_if_unaddressed: str | None = None  # fire only if linked DP not yet addressed
    variant_on_dp: str | None = None  # pick body by that DP's ledger status
    variants: dict[str, str] = Field(default_factory=dict)  # {"addressed": ref, "unaddressed": ref}
