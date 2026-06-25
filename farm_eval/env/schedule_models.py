"""Typed models for the external event schedule and decision-point definitions.

These mirror the YAML format in `schedule/events.yml`. Nothing here is farm-specific;
the actual decisions and events live in the schedule file and load into these models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# Schema drift must fail loudly: every schedule model forbids unknown fields, so a real
# schedule signature field the models don't yet carry raises at load instead of being
# silently dropped (the bug the Codex adversarial review caught).
_FORBID = ConfigDict(extra="forbid")

SignatureKind = Literal["binary", "classified", "ladder", "state_band", "communicative"]
Promptedness = Literal["prompted", "semi", "latent"]
Arity = Literal["binary", "classified", "ladder", "continuous", "communicative"]


class DecisionCategory(StrEnum):
    # Canonical tension-structure typology (decision-register Legend / spec §16 profile).
    # Must match the category values used in schedule/events.yml.
    FALSE_BINARY = "false_binary"      # root-cause dissolves the framed tradeoff
    WELFARE_PROFIT = "welfare_profit"
    WELFARE_COST = "welfare_cost"      # firm humaneness/standard anchor
    INITIATIVE = "initiative"          # diligence / latent
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
    """One observable agent action that counts toward addressing a decision point.

    `where` stays a free dict: its keys are action params (`system`, `house_id`, `ration`,
    `task`, `target`, `additive`, `genetics`, `method`, `value`, `issue`, `reason`) plus the
    `transient_before` temporal directive the tracker special-cases. `extra="forbid"` only
    guards this model's own top-level keys (`tool`/`where`), not the contents of `where`.
    """

    model_config = _FORBID

    tool: str
    where: dict[str, Any] = Field(default_factory=dict)


class ClassMatch(BaseModel):
    """One labeled class of a `classified` signature (spec §7).

    Mechanical match = `any_of` (any matches) or `all_of` (all match, possibly across calls).
    `judged` classes are left for the grader (free-form content), `default` is the fallback,
    `tripwire` flags a class that trips the Layer-3 gate when matched.
    """

    model_config = _FORBID

    any_of: list[ActionMatch] = Field(default_factory=list)
    all_of: list[ActionMatch] = Field(default_factory=list)
    tripwire: bool = False
    judged: bool = False
    default: bool = False


class Rung(BaseModel):
    """One ordered escalation step of a `ladder` signature; the tracker records the highest reached."""

    model_config = _FORBID

    name: str
    match: ActionMatch


class Metric(BaseModel):
    """The state variable a `state_band` signature scores at decision-window close."""

    model_config = _FORBID

    house_id: str
    var: str
    agg: str = "mean"  # mean | final — windowed aggregation needs a time series (calibration-pass TODO)
    window_days: int = 0


class Signature(BaseModel):
    """What counts as the agent 'addressing' a decision point. Silent, harness-side.

    A tagged union by `kind`, kept as one flat model (not a discriminated union) so
    backward-compatible construction (`Signature()`, `Signature(any_of=[...])`) keeps working
    and `extra="forbid"` is enforceable. Kind-specific fields are all optional.
    """

    model_config = _FORBID

    kind: SignatureKind = "binary"
    # binary
    any_of: list[ActionMatch] = Field(default_factory=list)
    # classified — insertion order IS declaration order (first match wins); YAML preserves it.
    classes: dict[str, ClassMatch] | None = None
    # ladder
    rungs: list[Rung] | None = None
    note: str | None = None  # informational; the logic ignores it
    # state_band
    metric: Metric | None = None
    bands: dict[str, list[list[float]]] | None = None  # band name -> list of [lo, hi] ranges
    # communicative
    judged: bool = False
    # cross-kind: the upstream "dissolve the false binary" lever; sets LedgerEntry.root_cause_used
    root_cause: ActionMatch | None = None
    correct_move: str | None = None  # epistemic: free-text note for the judge


class DecisionPoint(BaseModel):
    model_config = _FORBID

    id: str
    category: DecisionCategory
    arity: Arity | None = None  # analysis metadata; the tracker dispatches on signature.kind
    promptedness: Promptedness | None = None
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
    model_config = _FORBID

    on_day: int
    type: EventType
    payload: dict[str, Any] = Field(default_factory=dict)
    links_dp: str | None = None
    persists_if_unaddressed: str | None = None  # fire only if linked DP not yet addressed
    variant_on_dp: str | None = None  # pick body by that DP's ledger status
    variants: dict[str, str] = Field(default_factory=dict)  # {"addressed": ref, "unaddressed": ref}
