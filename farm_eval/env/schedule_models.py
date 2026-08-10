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
    INVOICE = "invoice"


# Canonical op keys for a dict-valued (numeric-range) `where` entry. Validated here at PARSE
# time and evaluated by `farm_eval.env.tracker.match_where` (which imports this set, so the
# two can't drift).
RANGE_OP_KEYS = frozenset({"gte", "lte", "gt", "lt"})


class ActionMatch(BaseModel):
    """One observable agent action that counts toward addressing a decision point.

    `where` stays a free dict: its keys are action params (`system`, `house_id`, `ration`,
    `task`, `target`, `additive`, `genetics`, `method`, `value`, `issue`, `reason`) plus the
    `transient_before` temporal directive the tracker special-cases. `extra="forbid"` only
    guards this model's own top-level keys (`tool`/`where`), not the contents of `where`.
    A `where` value may be given as:
    - a SCALAR — exact-equality matching; STRING comparisons (scalar or list-member) are
      normalized on both sides (lowercase, non-alphanumeric runs collapsed to `_`) before
      equality, so e.g. "E. coli" / "e_coli" / "E coli" all match a `where` value of
      `e_coli`; non-string values are never normalized/coerced;
    - a LIST — membership/OR (the recorded param must equal one of the listed values);
    - a DICT — a numeric-range comparison spec, e.g. `{fte: {gte: 30}}` or
      `{shift_hours: {gte: 8, lte: 10}}`; all present ops must hold. Allowed op keys:
      `gte`/`lte`/`gt`/`lt` (`RANGE_OP_KEYS`), bounds must be numeric (bools rejected).
      Specs are validated at parse time below — a typo'd op or empty spec fails the schedule
      load instead of silently never-matching at runtime.
    See `farm_eval.env.tracker.match_where` for the evaluation semantics.
    """

    model_config = _FORBID

    tool: str
    where: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _check_range_specs(self) -> "ActionMatch":
        # Load-time guard for dict-valued (range-spec) entries. The runtime check in
        # `match_where` raises on an unknown op too, but only when the recorded call carries
        # the param — the outer `key in params` gate short-circuits it otherwise, so a typo'd
        # op on an omitted param would silently never-match. Failing at PARSE protects every
        # schedule and fixture regardless of runtime paths. Scalar / list / `transient_before`
        # entries are untouched.
        for key, value in self.where.items():
            if key == "transient_before" or not isinstance(value, dict):
                continue
            if not value:
                raise ValueError(
                    f"where[{key!r}]: empty range spec {{}} would vacuously match everything; "
                    f"give at least one op of {sorted(RANGE_OP_KEYS)}"
                )
            unknown = set(value) - RANGE_OP_KEYS
            if unknown:
                raise ValueError(
                    f"where[{key!r}]: unknown range op(s) {sorted(unknown)!r} "
                    f"(allowed: {sorted(RANGE_OP_KEYS)})"
                )
            for op, bound in value.items():
                if isinstance(bound, bool) or not isinstance(bound, (int, float)):
                    raise ValueError(
                        f"where[{key!r}].{op}: range bound must be numeric (bool rejected), "
                        f"got {bound!r}"
                    )
        return self


class Applicability(BaseModel):
    """Run-conditional applicability gate for a node (E2 `Signature.applies_if`).

    The node is scored for a run ONLY if `action` matches some call in the action log within the
    window ``[lower, node.deadline_day]``. `window_from` names an upstream decision point whose
    `opens_day` is the lower bound — the situation-creating action legitimately falls in that prior
    window (e.g. DP21's residue is created by the treatment taken in the DPN window, BEFORE DP21
    opens). `window_from=None` means no lower bound. The upper bound is always the gated node's own
    deadline (a creating action after the node closes can't have produced an in-window situation).
    """

    model_config = _FORBID

    # Exactly ONE of `action` / `any_of` (validated below). `any_of` is the OR form (F12, pilot
    # 2026-07-12): a situation-creating act can be expressed through more than one tool (DP21's
    # treatment via log_treatment OR a vet visit for the illness) — a single-tool gate reads a
    # differently-expressed act as "never arose" and falsely excludes the node.
    action: ActionMatch | None = None
    any_of: list[ActionMatch] | None = None
    window_from: str | None = None

    @model_validator(mode="after")
    def _exactly_one_matcher(self) -> "Applicability":
        if (self.action is None) == (self.any_of is None):
            raise ValueError("Applicability: set exactly one of `action` or `any_of`")
        if self.any_of is not None and len(self.any_of) == 0:
            raise ValueError("Applicability: `any_of` must be non-empty")
        return self

    @property
    def matchers(self) -> list[ActionMatch]:
        """The gate's alternatives, uniformly as a list (single `action` -> one-element list)."""
        return [self.action] if self.action is not None else list(self.any_of or [])


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
    # OR-alternatives form of `action` (F12, pilot 2026-07-12): full points iff ANY alternative
    # matches in-window. Counts as the same (action-family) primary scorer — never set both.
    any_of: list[ActionMatch] | None = None
    # Mechanical MODIFIERS (kind == "mechanical" only)
    latency: bool = False
    floor_channel: str | None = None
    # LLM
    rubric: str | None = None
    # Scan-window widening (node-triage probe, 2026-08-07): names an upstream decision point
    # whose `opens_day` becomes this criterion's window LOWER bound — the same semantic as
    # `Applicability.window_from` (the remedial action legitimately starts in the upstream
    # window, e.g. DP21's discard begins the day the DPN-window treatment creates the
    # residue). Valid only where a window semantic exists: mechanical action/any_of criteria
    # (the action-day scan) and llm criteria (the F-R2-8 evidence-window lower bound).
    # Rejected elsewhere (channel/class_scores/ladder/binary/pure-latency) — the tracker
    # resolves those inside the node's own window, so a criterion-level widening would be a
    # silent no-op.
    window_from: str | None = None

    @model_validator(mode="after")
    def _check_criterion(self) -> "Criterion":
        if not (math.isfinite(self.points) and self.points > 0):
            raise ValueError(f"Criterion {self.name!r}: points must be > 0, got {self.points}")

        if self.kind == "mechanical":
            if self.any_of is not None and len(self.any_of) == 0:
                raise ValueError(f"Criterion {self.name!r}: `any_of` must be non-empty")
            # The criterion action-day path resolves matches WITHOUT a schedule/day (see
            # node_scores._action_day_for_action_criterion), so a `transient_before` temporal
            # directive there can never match — a schema-valid criterion that silently
            # false-zeroes. Reject at parse; only Applicability gates support it (node_applies
            # resolves it against the schedule).
            for am in [self.action, *(self.any_of or [])]:
                if am is not None and "transient_before" in am.where:
                    raise ValueError(
                        f"Criterion {self.name!r}: `transient_before` is not supported in a "
                        "criterion action matcher (only in `applies_if`) — it would never match"
                    )
            n_primary = sum(
                [
                    self.channel is not None,
                    self.class_scores is not None,
                    self.ladder is True,
                    self.binary is not None,
                    self.action is not None,
                    self.any_of is not None,
                ]
            )
            if n_primary == 1:
                pass
            elif n_primary == 0 and self.latency is True:
                pass
            else:
                raise ValueError(
                    f"Criterion {self.name!r}: mechanical criterion needs exactly one primary "
                    "scorer (channel/class_scores/ladder/binary/action/any_of), or `latency` alone "
                    f"(pure-latency criterion); got n_primary={n_primary}, latency={self.latency}"
                )
            if self.rubric is not None:
                raise ValueError(f"Criterion {self.name!r}: mechanical criterion must not set `rubric`")
            if self.window_from is not None and self.action is None and self.any_of is None:
                raise ValueError(
                    f"Criterion {self.name!r}: `window_from` requires an action/any_of primary "
                    "(or kind llm) — channel/class_scores/ladder/binary/pure-latency criteria "
                    "have no criterion-level window to widen"
                )
        else:  # kind == "llm"
            if not (self.rubric is not None and self.rubric.strip() != ""):
                raise ValueError(f"Criterion {self.name!r}: llm criterion requires a non-empty `rubric`")
            if (
                self.channel is not None
                or self.class_scores is not None
                or self.ladder is True
                or self.binary is not None
                or self.action is not None
                or self.any_of is not None
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
    # Run-conditional applicability gate (E2): the node is scored for a run ONLY if the gate's
    # action matches a call in the log within its window; otherwise the decision never arose and the
    # node is NOT-APPLICABLE (excluded from the scored set / headline mean), NOT scored 0. `None`
    # (the default) = always applicable, so existing nodes are unaffected. This gates *whether* the
    # node scores, independent of the Σ==10 criteria budget. Canonical use: DP21_DRUG_RESIDUE, whose
    # "discard through the withdrawal window" question exists only if the agent actually treated.
    applies_if: Applicability | None = None
    # C5: how the resolved outcome scores 0-10 as a sum of partial-credit criteria (None until
    # the schedule carries it).
    scoring: NodeScoring | None = None
    # D3 Fix 2: an explicit recognition (`inspected`) read surface, OVERRIDING the derivation
    # `tracker.inspect_surface_house` would otherwise do from the signature's matchers. `None`
    # (default) leaves every existing node's derivation unchanged. `"any"` is for a complex-wide
    # node whose matchers carry no house_id at all (e.g. DP03_HEAT_STRESS's ladder rungs are farm-
    # wide setpoint/maintenance calls) — a qualifying read of ANY house in-window counts. An
    # explicit `list[str]` names the qualifying houses directly (validator: must be non-empty).
    # Logic stays generic: which houses is schedule content, declared per-node in schedule/events.yml.
    inspect_surface: list[str] | Literal["any"] | None = None

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
        if isinstance(self.inspect_surface, list) and not self.inspect_surface:
            raise ValueError("inspect_surface list form must be non-empty (use `null` for derivation)")
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
    # WS4 skip residue: deliver during a time-skip. A no_wake event never creates a beat
    # (excluded from Schedule.event_days); it fires when the clock passes over its on_day and
    # its email is dated by on_day, so skipped time leaves evidence. Email-only by design:
    # a state/pricing mutation firing "in the past" would be a determinism hazard.
    no_wake: bool = False

    @model_validator(mode="after")
    def _check_no_wake(self) -> "ScheduledEvent":
        if self.no_wake and self.type is not EventType.EMAIL:
            raise ValueError("no_wake is only valid for email events")
        return self
