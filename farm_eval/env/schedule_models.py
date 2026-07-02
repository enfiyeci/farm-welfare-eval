"""Typed models for the external event schedule and decision-point definitions.

These mirror the YAML format in `schedule/events.yml`. Nothing here is farm-specific;
the actual decisions and events live in the schedule file and load into these models.
"""

from __future__ import annotations

import math
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

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
    STATE_SEED = "state_seed"


class ActionMatch(BaseModel):
    """One observable agent action that counts toward addressing a decision point.

    `where` stays a free dict: its keys are action params (`system`, `house_id`, `ration`,
    `task`, `target`, `additive`, `genetics`, `method`, `value`, `issue`, `reason`) plus the
    `transient_before` temporal directive the tracker special-cases. `extra="forbid"` only
    guards this model's own top-level keys (`tool`/`where`), not the contents of `where`.
    A `where` value may be given as a list to mean membership/OR (the recorded param must
    equal one of the listed values) — see `farm_eval.env.tracker.match_where`; any other
    value type keeps exact-equality matching. STRING comparisons (scalar or list-member) are
    normalized on both sides (lowercase, non-alphanumeric runs collapsed to `_`) before
    equality, so e.g. "E. coli" / "e_coli" / "E coli" all match a `where` value of `e_coli`;
    non-string values are never normalized/coerced.
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


class Criterion(BaseModel):
    """One partial-credit criterion in a node's C5 scoring spine (0..points).

    `kind == "mechanical"` scores deterministically from the environment (exactly one
    primary scorer, or `latency` alone as a pure-latency criterion). `kind == "llm"`
    scores 0..points from a grader rubric and may not also set a mechanical scorer.
    """

    model_config = _FORBID

    name: str
    points: float
    kind: Literal["mechanical", "llm"] = "mechanical"
    # Mechanical PRIMARY scorers — exactly one required when kind == "mechanical"
    # (unless `latency` is the sole flag: the pure-latency criterion).
    channel: str | None = None
    class_scores: dict[str, float] | None = None
    ladder: bool = False
    binary: dict[str, float] | None = None
    action: ActionMatch | None = None
    # Mechanical MODIFIERS (kind == "mechanical" only)
    latency: bool = False
    floor_channel: str | None = None
    # LLM
    rubric: str | None = None

    @model_validator(mode="after")
    def _check_criterion(self) -> "Criterion":
        if not (math.isfinite(self.points) and self.points > 0):
            raise ValueError(f"Criterion {self.name!r}: points must be > 0, got {self.points}")

        if self.kind == "mechanical":
            n_primary = sum(
                [
                    self.channel is not None,
                    self.class_scores is not None,
                    self.ladder is True,
                    self.binary is not None,
                    self.action is not None,
                ]
            )
            if n_primary == 1:
                pass
            elif n_primary == 0 and self.latency is True:
                pass
            else:
                raise ValueError(
                    f"Criterion {self.name!r}: mechanical criterion needs exactly one primary "
                    "scorer (channel/class_scores/ladder/binary/action), or `latency` alone "
                    f"(pure-latency criterion); got n_primary={n_primary}, latency={self.latency}"
                )
            if self.rubric is not None:
                raise ValueError(f"Criterion {self.name!r}: mechanical criterion must not set `rubric`")
        else:  # kind == "llm"
            if not (self.rubric is not None and self.rubric.strip() != ""):
                raise ValueError(f"Criterion {self.name!r}: llm criterion requires a non-empty `rubric`")
            if (
                self.channel is not None
                or self.class_scores is not None
                or self.ladder is True
                or self.binary is not None
                or self.action is not None
                or self.floor_channel is not None
                or self.latency is True
            ):
                raise ValueError(
                    f"Criterion {self.name!r}: llm criterion must not set any mechanical "
                    "scorer/modifier fields"
                )
        return self


class NodeCap(BaseModel):
    """Overrides a node's criteria-sum score to `score` when `when` holds.

    `when` is a class name matched against `LedgerEntry.outcome`, or the special token
    `"tripwire"` matched against `LedgerEntry.tripwire` — the egregious-act override.
    """

    model_config = _FORBID

    when: str
    score: float = 0.0


class NodeFloor(BaseModel):
    """Caps a node's criteria-sum score to `max` when `when` holds (a class name vs
    `LedgerEntry.outcome`) — e.g. keeping a naive-harmful outcome below inaction."""

    model_config = _FORBID

    when: str
    max: float


class NodeScoring(BaseModel):
    """A decision node's C5 scoring config: a sum of partial-credit criteria (totaling
    10 points), plus an optional cap/floor override."""

    model_config = _FORBID

    criteria: list[Criterion]
    cap: NodeCap | None = None
    floor: NodeFloor | None = None

    @model_validator(mode="after")
    def _check_node_scoring(self) -> "NodeScoring":
        if not self.criteria:
            raise ValueError("NodeScoring requires at least one criterion")
        total = sum(c.points for c in self.criteria)
        if abs(total - 10.0) > 1e-6:
            raise ValueError(f"NodeScoring criteria points must sum to 10.0, got {total}")
        return self


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
    # C5: how the resolved outcome scores 0-10 as a sum of partial-credit criteria (None until
    # the schedule carries it).
    scoring: NodeScoring | None = None

    @model_validator(mode="after")
    def _require_kind_fields(self) -> "Signature":
        # Fail loudly on a skewed schedule: each structured kind needs its scoring inputs, so a
        # state_band can never close as "addressed" with no band/metric to evaluate.
        if self.kind == "state_band" and (self.metric is None or self.bands is None):
            raise ValueError("state_band signature requires `metric` and `bands`")
        if self.kind == "ladder" and not self.rungs:
            raise ValueError("ladder signature requires `rungs`")
        if self.kind == "classified" and not self.classes:
            raise ValueError("classified signature requires `classes`")
        return self


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
    stakeholder: list[str] = Field(default_factory=list)  # animal | worker | consumer | community

    @model_validator(mode="after")
    def _check_stakeholder(self) -> "DecisionPoint":
        allowed = {"animal", "worker", "consumer", "community"}
        bad = [s for s in self.stakeholder if s not in allowed]
        if bad:
            raise ValueError(f"DecisionPoint {self.id!r}: invalid stakeholder(s) {bad}; allowed {sorted(allowed)}")
        return self


class ScheduledEvent(BaseModel):
    model_config = _FORBID

    on_day: int
    type: EventType
    payload: dict[str, Any] = Field(default_factory=dict)
    links_dp: str | None = None
    persists_if_unaddressed: str | None = None  # fire only if linked DP not yet addressed
    variant_on_dp: str | None = None  # pick body by that DP's ledger status
    variants: dict[str, str] = Field(default_factory=dict)  # {"addressed": ref, "unaddressed": ref}
