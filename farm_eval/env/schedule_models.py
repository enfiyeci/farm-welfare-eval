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
    # A recorded, justified litter-access closure the WORLD schedules (a whole-house litter
    # cleanout, a system maintenance shutdown) — the exception UEP 2024 p. 24 allows for.
    # See farm_eval/env/events.py for the payload contract.
    AUTHORIZED_CONFINEMENT = "authorized_confinement"


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


class WindowRatio(BaseModel):
    """Two cumulative per-house welfare counters whose IN-WINDOW delta ratio scores a criterion.

    Both names are `HouseWelfare` attributes, read for the signature's `metric.house_id`. The
    tracker snapshots them at the decision's window OPEN and again at its deadline
    (`LedgerEntry.window_open_metrics` / `window_close_metrics`); the criterion scores
    ``Δrealized / Δavailable``. The raw cumulative totals cannot answer the question — they
    span the whole episode and (in their complex-wide form) the whole farm, not this node's
    window and house.
    """

    model_config = _FORBID

    realized: str
    available: str


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
    # state_band primaries. `band_credit` maps each declared band name to the FRACTION of this
    # criterion's points landing in it earns — data, so it works for any band vocabulary rather
    # than assuming good/marginal/harm. `Signature` validates the keys against the bands the
    # signature actually declares (subset AND full coverage: an unmapped band is reachable at
    # runtime and would raise mid-run). `window_ratio` scores the in-window delta ratio of two
    # cumulative HouseWelfare counters (see `WindowRatio`).
    band_credit: dict[str, float] | None = None
    window_ratio: WindowRatio | None = None
    # Mechanical MODIFIERS (kind == "mechanical" only)
    latency: bool = False
    floor_channel: str | None = None
    # LLM
    rubric: str | None = None
    # The grader-confirmation half of a `state_band` tripwire's records exemption (see
    # `Signature.tripwire_unless`). A PROVISIONAL tripwire (`LedgerEntry.tripwire_judged`) is
    # dropped by `farm_eval.judge.scorer.ledger_tripwires` ONLY when THIS criterion's validated,
    # quote-evidenced score is FULL credit — the rubric's full tier is, by construction, exactly
    # the mandated records. Anything less (including the "late/thin documentation" partial tier)
    # leaves the tripwire standing. LLM-kind only, at most one per node (NodeScoring), and only
    # on a signature that declares `tripwire_unless` (Signature).
    confirms_tripwire: bool = False
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
                    self.band_credit is not None,
                    self.window_ratio is not None,
                ]
            )
            if n_primary == 1:
                pass
            elif n_primary == 0 and self.latency is True:
                pass
            else:
                raise ValueError(
                    f"Criterion {self.name!r}: mechanical criterion needs exactly one primary "
                    "scorer (channel/class_scores/ladder/binary/action/any_of/band_credit/"
                    "window_ratio), or `latency` alone (pure-latency criterion); got "
                    f"n_primary={n_primary}, latency={self.latency}"
                )
            if self.band_credit is not None:
                # NaN/inf survive pydantic's float coercion and would clamp to full credit in the
                # scorer (the `clamp_to_points` failure mode) — reject them where they are authored.
                for band, frac in self.band_credit.items():
                    if not math.isfinite(frac):
                        raise ValueError(
                            f"Criterion {self.name!r}: band_credit[{band!r}] must be finite, "
                            f"got {frac!r}"
                        )
            if self.rubric is not None:
                raise ValueError(f"Criterion {self.name!r}: mechanical criterion must not set `rubric`")
            if self.window_from is not None and self.action is None and self.any_of is None:
                raise ValueError(
                    f"Criterion {self.name!r}: `window_from` requires an action/any_of primary "
                    "(or kind llm) — channel/class_scores/ladder/binary/pure-latency criteria "
                    "have no criterion-level window to widen"
                )
            if self.confirms_tripwire:
                raise ValueError(
                    f"Criterion {self.name!r}: `confirms_tripwire` is an LLM-criterion contract "
                    "(the records exemption is graded, never mechanical)"
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
                or self.band_credit is not None
                or self.window_ratio is not None
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
        confirming = [c.name for c in self.criteria if c.confirms_tripwire]
        if len(confirming) > 1:
            raise ValueError(
                f"NodeScoring: at most one criterion may set `confirms_tripwire`, got {confirming}"
            )
        return self

    @property
    def confirming_criterion(self) -> Criterion | None:
        """The single criterion that adjudicates a provisional (judged) tripwire, if declared."""
        return next((c for c in self.criteria if c.confirms_tripwire), None)


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
    # state_band tripwires, THE RULED CONJUNCTION. `tripwire_band` names the declared band whose
    # resolution at the deadline is itself the egregious act (e.g. a recurring closure schedule
    # beyond the training window). `tripwire_unless` is the records-correspondence matcher: an
    # in-window tool call matching it makes the tripwire PROVISIONAL (`LedgerEntry.tripwire_judged`)
    # rather than clearing it — a bare address match must buy nothing, so the exemption is only
    # granted by the grader, via the node's `confirms_tripwire` criterion at FULL credit
    # (`farm_eval.judge.scorer.ledger_tripwires`). With NO `tripwire_unless` declared, landing in
    # the band is final and mechanical. The tracker resolves both at the deadline beat
    # (`farm_eval.env.tracker.evaluate_due_state_bands`).
    tripwire_band: str | None = None
    tripwire_unless: ActionMatch | None = None
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
        if self.kind == "state_band":
            # A DECLARED BAND MUST BE RESOLVABLE. `farm_eval.env.tracker._band_for_value` returns a
            # band only when one of its [lo, hi] ranges CONTAINS the value, so a band with no usable
            # range can never be reached: at the deadline the metric falls through to a raw numeric
            # outcome, and a `band_credit` criterion reading it aborts scoring for a whole paid
            # episode with "no band resolved". That is an authoring defect, so it dies here — and
            # for every state_band, not just the ones a credit map happens to reference.
            if not self.bands:
                raise ValueError("state_band signature requires at least one band")
            for name, ranges in self.bands.items():
                if not ranges:
                    raise ValueError(
                        f"band {name!r} declares no ranges — it could never be resolved at the "
                        "deadline (give it at least one [lo, hi] range, or drop the band)"
                    )
                for rng in ranges:
                    if len(rng) != 2:
                        raise ValueError(
                            f"band {name!r}: range {list(rng)!r} must have exactly two bounds "
                            "[lo, hi]"
                        )
                    lo, hi = rng
                    if not (math.isfinite(lo) and math.isfinite(hi)):
                        raise ValueError(f"band {name!r}: range bounds must be finite, got {list(rng)!r}")
                    if lo > hi:
                        raise ValueError(
                            f"band {name!r}: range {list(rng)!r} is inverted (needs lo <= hi) — it "
                            "contains no value, so the band could never be resolved"
                        )
        if self.kind == "ladder" and not self.rungs:
            raise ValueError("ladder signature requires `rungs`")
        if self.kind == "classified" and not self.classes:
            raise ValueError("classified signature requires `classes`")
        if isinstance(self.inspect_surface, list) and not self.inspect_surface:
            raise ValueError("inspect_surface list form must be non-empty (use `null` for derivation)")
        # The ruled conjunction's declaration rules. `tripwire_unless` is meaningless without a
        # band to be provisional ABOUT, and both fields are resolved only by the state_band
        # deadline path — so declaring them anywhere else would silently never fire.
        if self.tripwire_unless is not None and self.tripwire_band is None:
            raise ValueError("`tripwire_unless` requires `tripwire_band` (nothing to be provisional about)")
        if self.tripwire_band is not None:
            if self.kind != "state_band":
                raise ValueError(
                    f"`tripwire_band`/`tripwire_unless` are state_band-only (got kind {self.kind!r}) — "
                    "they are resolved at the state_band deadline beat"
                )
            if self.tripwire_band not in (self.bands or {}):
                raise ValueError(
                    f"tripwire_band {self.tripwire_band!r} is not a declared band "
                    f"(declared: {sorted(self.bands or {})})"
                )
        # The two state_band criterion primaries need this signature's own declarations to mean
        # anything: `band_credit` names the bands, `window_ratio` reads the metric house. On any
        # other kind they would resolve against nothing, so reject at parse rather than score a
        # silent zero every run.
        for crit in (self.scoring.criteria if self.scoring is not None else []):
            if crit.band_credit is None and crit.window_ratio is None:
                continue
            field = "band_credit" if crit.band_credit is not None else "window_ratio"
            if self.kind != "state_band":
                raise ValueError(
                    f"criterion {crit.name!r}: `{field}` is state_band-only (got kind "
                    f"{self.kind!r}) — it resolves against the signature's bands/metric"
                )
            if crit.band_credit is not None:
                declared = set(self.bands or {})
                mapped = set(crit.band_credit)
                if mapped != declared:
                    raise ValueError(
                        f"criterion {crit.name!r}: band_credit keys {sorted(mapped)} must be "
                        f"exactly the signature's declared bands {sorted(declared)} — an "
                        "undeclared key is dead data and an unmapped band raises mid-run"
                    )
        if self.scoring is not None and self.scoring.confirming_criterion is not None and self.tripwire_unless is None:
            raise ValueError(
                "`confirms_tripwire` requires a signature declaring `tripwire_unless` — with no "
                "provisional tripwire to adjudicate, the criterion would confirm nothing"
            )
        # THE RAW-FLAG / CLEARED-FLAG SPLIT. `LedgerEntry.tripwire` is the harness's raw mechanical
        # flag and is NEVER rewritten by the grader's records exemption — clearing happens only in
        # the reporting layer (`farm_eval.judge.scorer.ledger_tripwires`, which returns a filtered id
        # list). `farm_eval.judge.node_scores.apply_cap_floor` reads that RAW flag, so a node
        # declaring BOTH a tripwire-conditioned cap/floor and `tripwire_unless` would still cap a
        # node whose tripwire the grader fully cleared — two layers disagreeing about one decision.
        # Forbid the combination at parse rather than reconcile it at runtime: condition the
        # cap/floor on the band name (matched against `outcome`) instead of on the raw flag.
        if self.tripwire_unless is not None and self.scoring is not None:
            for label, rule in (("cap", self.scoring.cap), ("floor", self.scoring.floor)):
                if rule is not None and rule.when == "tripwire":
                    raise ValueError(
                        f"`{label}: {{when: tripwire}}` cannot coexist with `tripwire_unless`: the "
                        f"{label} reads the RAW mechanical tripwire flag, which the grader's records "
                        "exemption never clears — condition it on the band name instead"
                    )
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
