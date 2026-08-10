# Behaviour Report Implementation Plan

Eval: hen

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `farm_eval/analysis/` + report integration that turns one finished `.eval` log into a behaviour model (per-node dossiers, per-tool profiles, off-node findings, transcript digest, optional LLM reader) rendered into the HTML pilot report.

**Architecture:** Two existing extractors joined (spectator `Translator` for the day-stamped feed; `report/extract` for judge + ledger + transcript), a guarded transcript clock computed at extract time, strength-tiered attribution, deterministic off-node detectors, and an opt-in LLM reader. Spec: `evals/hen/design/2026-08-07-behaviour-report-design.md` (read it first — §2.1/§2.2/§3.2 carry the Codex-review-hardened semantics this plan implements).

**Tech Stack:** Python 3.11, pydantic v2 (`extra="forbid"`), pytest, inspect_ai (mockllm for tests).

## Global Constraints

- Worktree: `/Users/ardaenfiyeci/worktrees/fwe-behaviour` (absolute paths in every command; the shell cwd resets between calls).
- venv: symlink the main checkout's venv once — `ln -s /Users/ardaenfiyeci/Desktop/farm-eval/venv /Users/ardaenfiyeci/worktrees/fwe-behaviour/venv` (pyproject sets `pythonpath=["."]`, no editable install needed).
- Tests: `cd /Users/ardaenfiyeci/worktrees/fwe-behaviour && ./venv/bin/python -m pytest -q <path>`.
- READ-ONLY: `farm_eval/env/**`, `farm_eval/judge/**`, `farm_eval/spectator/**`, `corpus/`, `schedule/`, `config.yml`, goldens. Writes only: `farm_eval/analysis/**`, `farm_eval/report/**`, `tests/analysis/**`, `tests/report/**`, `scripts/behaviour_report.py`, docs.
- NO farm content hardcoded in logic (tests use `PLACEHOLDER_*` / fixture names like `H_SENSOR`, `DP_PLACEHOLDER_1`).
- Determinism: no wall-clock/random in logic. Pydantic models `extra="forbid"`.
- Every commit: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` (repo convention).
- The full suite + both corpus guards must be green at the end of every task: `./venv/bin/python -m pytest -q` (3 standing skips are normal).
- Verified import surface (do not rename): `farm_eval.judge.scorer.message_days(messages, start_day=0) -> dict[str,int]`; `farm_eval.judge.scorer._check_quote(dim_id, quote, mid, transcript_index) -> str` (empty string = valid); `farm_eval.env.tracker.match_where(params, where) -> bool`, `inspect_surface_house(sig) -> str | None`, `_READ_TOOLS = {"read_sensor","read_flock_report"}`; `farm_eval.spectator.extract.make_translator(spec, sample_id)`; `scripts.regen_spectator_golden.run_episode(log_dir) -> EvalLog` and its `CONFIG`.

---

### Task 1: Report-extract join fields + the guarded day map

**Files:**
- Modify: `farm_eval/report/extract.py`
- Test: `tests/report/test_extract.py` (append tests)

**Interfaces:**
- Produces: transcript rows gain `"message_id"` (provider id, may be `None`); tool rows gain `"function"` (str|None) and `"error"` (str|None); the report model gains top-level `"day_map": dict[str,int] | None` (msg_N → in-world day; `None` when the transcript does not reconcile with the final `day_index` — spec §2.2 R3-F1/R4-F1).
- Consumes: `farm_eval.judge.scorer.message_days` on the RAW Inspect messages (the guard is applied here, at extract time, because the helper reads `.function`/`.error` attributes that serialized rows drop).

- [ ] **Step 1: Write the failing tests** (append to `tests/report/test_extract.py`):

```python
from farm_eval.report.extract import _day_map, _transcript


def _msg(role, text, function=None, error=None, mid=None, tool_calls=None):
    return SimpleNamespace(
        role=role, content=text, text=text, function=function, error=error,
        id=mid, tool_calls=tool_calls, tool_call_id=None,
    )


def test_transcript_rows_carry_provider_id_and_tool_metadata() -> None:
    rows = _transcript([
        _msg("assistant", "hello", mid="prov-1"),
        _msg("tool", "1 day(s) pass. Quiet.", function="end_day"),
    ])
    assert rows[0]["message_id"] == "prov-1"
    assert rows[1]["function"] == "end_day" and rows[1]["error"] is None


def test_day_map_advances_only_on_end_day_results() -> None:
    messages = [
        _msg("assistant", "start"),
        _msg("tool", "1 day(s) pass. Quiet.", function="end_day"),
        _msg("tool", "2 day(s) pass. Body echoing the phrase.", function="read_email"),
        _msg("user", "[Time passes] 3 day(s) pass."),
    ]
    days = _day_map(messages, day_index=4)
    assert days == {"msg_0": 0, "msg_1": 1, "msg_2": 1, "msg_3": 4}


def test_day_map_is_none_when_transcript_does_not_reconcile() -> None:
    messages = [_msg("tool", "1 day(s) pass.", function="end_day")]
    assert _day_map(messages, day_index=99) is None
```

- [ ] **Step 2: Run** `./venv/bin/python -m pytest -q tests/report/test_extract.py` — expect FAIL (`ImportError: cannot import name '_day_map'`).

- [ ] **Step 3: Implement.** In `farm_eval/report/extract.py`: import `from farm_eval.judge.scorer import message_days`. Add to `_transcript`'s row dict: `"message_id": getattr(message, "id", None)`; and for tool rows `"function": getattr(message, "function", None)`, `"error": (str(err) if (err := getattr(message, "error", None)) is not None else None)`. Add:

```python
def _day_map(messages: list[Any], day_index: Any) -> dict[str, int] | None:
    """msg_N -> in-world day, guarded exactly as judge.scorer.evidence_window_map guards it:
    a transcript whose final day does not reconcile with the recorded final day_index is a
    resumed/truncated run, and every window judgment against it would use a wrong clock (spec
    §2.2). Computed HERE, on raw Inspect messages, because message_days reads `.function` /
    `.error` — attributes the serialized rows drop (Codex R4-F1). Not evidence_window_map
    itself: that validates a full EnvState, which old logs predating current schema can't."""
    if not messages:
        return None
    days = message_days(messages)
    return days if days[f"msg_{len(messages) - 1}"] == day_index else None
```

In `extract()`, add `"day_map": _day_map(messages, state.get("day_index"))` to the model dict (top level, next to `"transcript"`).

- [ ] **Step 4: Run** `./venv/bin/python -m pytest -q tests/report/` — all pass (existing golden-subset test unaffected: it asserts a key subset).
- [ ] **Step 5: Commit** `git add farm_eval/report/extract.py tests/report/test_extract.py && git commit` — `feat(report): provider ids, tool function/error, guarded day_map in the report model`.

---

### Task 2: `farm_eval/analysis/model.py` — the behaviour-model types

**Files:**
- Create: `farm_eval/analysis/__init__.py` (empty), `farm_eval/analysis/model.py`
- Test: `tests/analysis/__init__.py` (empty), `tests/analysis/test_model.py`

**Interfaces (produced — later tasks construct exactly these):**

```python
Strength = Literal["strong", "ambient"]
Kind = Literal["action", "read", "email_sent", "assistant_text"]

class BehaviourEvent(BaseModel):      # one attributable thing that happened
    model_config = ConfigDict(extra="forbid")
    kind: Kind
    day_lo: int | None                # exact day when day_lo == day_hi; bounded range otherwise
    day_hi: int | None
    msg_id: str | None = None         # msg_N where known (transcript-derived events)
    tool: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    summary: str = ""                 # short human text (subject line / text preview / arg gist)

class Attribution(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event: BehaviourEvent
    dp_id: str
    strength: Strength

class DossierDerived(BaseModel):
    model_config = ConfigDict(extra="forbid")
    strong_action_count: int
    read_before_first_action: bool | None   # None when no strong action or no relevant read
    longest_idle_gap_days: int | None       # None in transcript-only mode without day certainty

class NodeDossier(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dp_id: str
    category: str
    opened_day: int
    deadline_day: int
    status: str
    outcome: str | float | None = None
    tripwire: bool = False
    inspected: bool = False
    root_cause_used: bool = False
    latency_days: int | None = None
    node_score: float | None = None
    strong: list[BehaviourEvent] = Field(default_factory=list)
    ambient: list[BehaviourEvent] = Field(default_factory=list)
    derived: DossierDerived

class ToolProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tool: str
    total_calls: int
    first_day: int | None = None
    last_day: int | None = None
    calls_by_bucket: list[dict[str, int]] = Field(default_factory=list)  # {"day": d, "calls": n}
    houses: dict[str, int] = Field(default_factory=dict)
    error_count: int = 0
    cost_cents_total: float = 0.0
    strong_calls: int = 0
    ambient_calls: int = 0
    offnode_calls: int = 0

class OffNodeFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")
    detector: str                     # e.g. "repetition_loop", "blank_turn_cluster"
    severity: float                   # 0-10, detector-defined ranking key
    day_lo: int | None
    day_hi: int | None
    msg_ids: list[str] = Field(default_factory=list)
    tool: str | None = None
    count: int = 1
    note: str                         # plain-language, content from the log not from logic

class DigestEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: str                         # "assistant" | "reasoning" | "tool" | "email_in" | "email_out"
    msg_id: str | None = None
    text: str

class DigestDay(BaseModel):
    model_config = ConfigDict(extra="forbid")
    day: int
    windows_open: list[str] = Field(default_factory=list)
    state_deltas: dict[str, Any] = Field(default_factory=dict)   # {} in transcript-only mode
    entries: list[DigestEntry] = Field(default_factory=list)

class ReaderVerdict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["candidates", "sweep"]
    target: str                       # finding key "detector:index" or chunk key "days:lo-hi"
    interestingness: float
    category: str
    note: str
    quotes: list[str] = Field(default_factory=list)
    quote_unverified: bool = False

class BehaviourModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: int = 1
    source_sha256: str
    target_model: str
    feed_fidelity: Literal["full", "transcript_only"]
    fidelity_failure_day: int | None = None
    day_map_valid: bool
    thresholds: dict[str, float]      # every detector constant, stated (spec §3.5: no silent tuning)
    dossiers: list[NodeDossier]
    tool_profiles: list[ToolProfile]
    offnode_findings: list[OffNodeFinding]
    digest: list[DigestDay]
    reader_verdicts: list[ReaderVerdict] = Field(default_factory=list)
```

- [ ] **Step 1: Write the failing test** `tests/analysis/test_model.py`:

```python
import pytest
from pydantic import ValidationError

from farm_eval.analysis.model import BehaviourEvent, BehaviourModel, DossierDerived, NodeDossier


def test_behaviour_model_round_trips_through_json() -> None:
    model = BehaviourModel(
        source_sha256="a" * 64, target_model="mockllm/model", feed_fidelity="full",
        day_map_valid=True, thresholds={"repetition_k": 5.0}, dossiers=[], tool_profiles=[],
        offnode_findings=[], digest=[],
    )
    assert BehaviourModel.model_validate_json(model.model_dump_json()) == model


def test_extra_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        BehaviourEvent(kind="action", day_lo=1, day_hi=1, surprise=True)


def test_dossier_requires_derived() -> None:
    with pytest.raises(ValidationError):
        NodeDossier(dp_id="DP_PLACEHOLDER_1", category="welfare_cost", opened_day=0,
                    deadline_day=5, status="open")
```

- [ ] **Step 2: Run** `./venv/bin/python -m pytest -q tests/analysis/test_model.py` — FAIL (module missing).
- [ ] **Step 3: Implement** `farm_eval/analysis/model.py` exactly as the Interfaces block above (imports: `from typing import Any, Literal`; `from pydantic import BaseModel, ConfigDict, Field`).
- [ ] **Step 4: Run again** — PASS.
- [ ] **Step 5: Commit** — `feat(analysis): behaviour-model types`.

---

### Task 3: `farm_eval/analysis/replay.py` — tolerant feed replay

**Files:**
- Create: `farm_eval/analysis/replay.py`
- Test: `tests/analysis/test_replay.py`

**Interfaces:**
- Consumes: `farm_eval.spectator.extract.make_translator`, `Translator.handle/finish`, `HANDLED_EVENT_TYPES` semantics (unknown events → `[]`).
- Produces: `replay_feed(log: EvalLog, sample: EvalSample) -> ReplayResult` where

```python
@dataclass(frozen=True)
class ReplayResult:
    events: list[FeedEvent]
    fidelity: Literal["full", "transcript_only"]
    failure_day: int | None    # translator.day when the first store patch failed
```

Semantics (spec §2.2): drive the translator over `sample.events`; on the FIRST exception from a `StoreEvent` (`translate.py` latches `_state_broken` and re-raises), record `fidelity="transcript_only"` + `failure_day=translator.day` and keep feeding events — the latched translator keeps translating `ModelEvent`/`ToolEvent` and ignores later `StoreEvent`s. Always append `translator.finish(status)` using the same per-sample status logic as `spectator.extract._sample_status` (import it — read-only). Feed `day` stamps in `transcript_only` mode are NOT trusted downstream (Codex R2-F1); the day source is Task 1's `day_map`.

- [ ] **Step 1: Write the failing test** `tests/analysis/test_replay.py` (module-scoped scripted episode, the spectator test pattern):

```python
from __future__ import annotations

import pytest
from inspect_ai._util.json import JsonChange
from inspect_ai.event import StoreEvent

from farm_eval.analysis.replay import replay_feed
from farm_eval.spectator.events import EpisodeEnd, RunMeta, StateSnapshot, ToolCallEvent
from scripts.regen_spectator_golden import run_episode


@pytest.fixture(scope="module")
def log(tmp_path_factory):
    return run_episode(tmp_path_factory.mktemp("analysis-replay") / "logs")


def test_full_fidelity_replay(log) -> None:
    result = replay_feed(log, log.samples[0])
    assert result.fidelity == "full" and result.failure_day is None
    kinds = [type(e) for e in result.events]
    assert kinds[0] is RunMeta and kinds[-1] is EpisodeEnd
    assert any(k is StateSnapshot for k in kinds) and any(k is ToolCallEvent for k in kinds)


def test_broken_store_patch_degrades_to_transcript_only(log) -> None:
    sample = log.samples[0].model_copy(deep=True)
    for event in sample.events:
        if isinstance(event, StoreEvent):
            event.changes.append(
                JsonChange(op="replace", path="/EpisodeStore:env_state/nonexistent/9", value=1)
            )
            break
    result = replay_feed(log, sample)
    assert result.fidelity == "transcript_only"
    assert result.failure_day is not None
    assert any(isinstance(e, ToolCallEvent) for e in result.events)   # transcript stream survives
    assert isinstance(result.events[-1], EpisodeEnd)
```

- [ ] **Step 2: Run** — FAIL (module missing).
- [ ] **Step 3: Implement:**

```python
"""Tolerant replay of one sample through the read-only spectator Translator (spec §2.2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from inspect_ai.event import StoreEvent
from inspect_ai.log import EvalLog, EvalSample

from farm_eval.spectator.events import FeedEvent
from farm_eval.spectator.extract import _sample_status, make_translator


@dataclass(frozen=True)
class ReplayResult:
    events: list[FeedEvent]
    fidelity: Literal["full", "transcript_only"]
    failure_day: int | None


def replay_feed(log: EvalLog, sample: EvalSample) -> ReplayResult:
    translator = make_translator(log.eval, sample.uuid or str(sample.id))
    events: list[FeedEvent] = []
    failure_day: int | None = None
    for event in sample.events or []:
        try:
            events += translator.handle(event)
        except Exception:
            # Only a StoreEvent can break the shadow reconstruction; the translator has
            # latched state derivation off and keeps translating the transcript stream.
            # Anything else is a real bug and must not be swallowed.
            if not isinstance(event, StoreEvent):
                raise
            if failure_day is None:
                failure_day = translator.day
    events += translator.finish(_sample_status(log, sample))
    fidelity = "full" if failure_day is None else "transcript_only"
    return ReplayResult(events=events, fidelity=fidelity, failure_day=failure_day)
```

- [ ] **Step 4: Run** — PASS.
- [ ] **Step 5: Commit** — `feat(analysis): tolerant feed replay (full / transcript_only fidelity)`.

---

### Task 4: `farm_eval/analysis/attribute.py` — strength-tiered attribution

**Files:**
- Create: `farm_eval/analysis/attribute.py`
- Test: `tests/analysis/test_attribute.py`

**Interfaces:**
- Consumes: report-model rows (`environment.actions` / `reads` / `outbound` — each carries `day`), `environment.ledger` rows, the loaded `Schedule` (via `farm_eval.env.loader.load_schedule` on the run's recorded `schedule_path` — read-only), and tracker helpers `match_where`, `inspect_surface_house`, `_READ_TOOLS`.
- Produces:

```python
def attribute_events(
    actions: list[dict], reads: list[dict], outbound: list[dict],
    ledger: list[dict], schedule: Schedule,
) -> tuple[list[Attribution], list[BehaviourEvent]]:
    """(attributions, offnode_events). offnode = events with NO strong attribution
    anywhere (ambient does not count as accounted-for — spec §3.2)."""
```

Rules (spec §3.2, exactly):
- An **action** row in a node's `[opened_day, deadline_day]` is **strong** iff its `(tool, params)` matches any of the signature's `ActionMatch`es — collected from `any_of`, every `classes[*].any_of + all_of`, every `rungs[*].match`, `root_cause`, and `scoring.criteria[*].action` — via `tracker.match_where(params, am.where)` with `am.tool == row["tool"]`; OR it equals the ledger entry's `agent_action` (`tool`, `day` equal and `params` equal). A same-house coincidence alone is **ambient** (house read from `params["house_id"]` vs `inspect_surface_house(sig)`).
- A **read** row (`tool in _READ_TOOLS`) in-window is **strong** iff the tracker's recognition semantics accept it: `sig.inspect_surface == "any"` → any read; a list → `params["house_id"]` in the list; `None` → `params["house_id"] == inspect_surface_house(sig)` (which may be None → not strong). Otherwise in-window reads with a house are **ambient**.
- An **outbound email** row in-window is **strong** iff the signature has a `send_email` ActionMatch matching the action row that sent it — handled by the action rule (send_email IS an action tool); as an email event it is ambient-at-best.
- `transient_before` in a `where` dict is a tracker temporal directive, not a param: strip it before `match_where` (`{k: v for k, v in am.where.items() if k != "transient_before"}`).
- Multi-window overlap: one event may be strong for several nodes.

- [ ] **Step 1: Write the failing tests** (synthetic schedule via `farm_eval.env.schedule_models.Signature/ActionMatch/DecisionPoint` — construct in-test with `PLACEHOLDER` ids; see `tests/env/test_tracker.py` for the construction idiom):

```python
from farm_eval.analysis.attribute import attribute_events
from farm_eval.env.schedule_models import ActionMatch, DecisionPoint, Schedule, Signature


def _schedule(sig: Signature) -> Schedule:
    dp = DecisionPoint(id="DP_PLACEHOLDER_1", category="welfare_cost", opens=0, deadline=10,
                       signature=sig)
    return Schedule(decision_points=[dp], events=[])

LEDGER = [{"dp_id": "DP_PLACEHOLDER_1", "opened_day": 0, "deadline_day": 10,
           "status": "addressed", "agent_action": None}]


def test_matcher_match_is_strong() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint",
                                        where={"system": "ventilation", "house_id": "H_A"})])
    actions = [{"tool": "adjust_setpoint", "day": 3,
                "params": {"system": "ventilation", "house_id": "H_A", "value": 1.0}}]
    attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert [(a.dp_id, a.strength) for a in attrs] == [("DP_PLACEHOLDER_1", "strong")]
    assert offnode == []


def test_same_house_coincidence_is_ambient_and_offnode(caplog) -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint",
                                        where={"system": "ventilation", "house_id": "H_A"})])
    actions = [{"tool": "log_treatment", "day": 3,
                "params": {"house_id": "H_A", "issue": "red_mite"}}]   # unrelated, same house
    attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert [(a.dp_id, a.strength) for a in attrs] == [("DP_PLACEHOLDER_1", "ambient")]
    assert len(offnode) == 1 and offnode[0].tool == "log_treatment"


def test_farm_wide_any_surface_claims_reads() -> None:
    sig = Signature(inspect_surface="any",
                    any_of=[ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})])
    reads = [{"tool": "read_sensor", "day": 2, "params": {"house_id": "H_B", "metric": "temp_c"}}]
    attrs, offnode = attribute_events([], reads, [], LEDGER, _schedule(sig))
    assert [(a.dp_id, a.strength) for a in attrs] == [("DP_PLACEHOLDER_1", "strong")]
    assert offnode == []


def test_out_of_window_event_is_offnode() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={})])
    actions = [{"tool": "adjust_setpoint", "day": 40, "params": {"system": "ventilation"}}]
    attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert attrs == [] and len(offnode) == 1
```

- [ ] **Step 2: Run** — FAIL. **Step 3: Implement** `attribute.py`: collect the matcher list per signature into `_signature_matchers(sig) -> list[ActionMatch]`; build a `BehaviourEvent` per row (`kind` per source list, `day_lo == day_hi == row["day"]`, `summary` = tool + gist of params); loop ledger entries × events applying the rules above; events with no strong attribution anywhere go to `offnode`. Keep it one pass per (event, entry) — n_events × n_nodes is ≤ ~900 × 24, trivially linear.
- [ ] **Step 4: Run** — PASS (also run `tests/env/test_tracker.py` to prove no read-only breakage). **Step 5: Commit** — `feat(analysis): strength-tiered event attribution`.

---

### Task 5: `farm_eval/analysis/pernode.py` — dossiers

**Files:**
- Create: `farm_eval/analysis/pernode.py`
- Test: `tests/analysis/test_pernode.py`

**Interfaces:**
- Produces: `build_dossiers(ledger: list[dict], node_scores: dict[str, float], attributions: list[Attribution]) -> list[NodeDossier]` — one per ledger entry, sorted by `opened_day` then `dp_id`.
- Derived facts: `strong_action_count` (strong attributions of kind `"action"`); `read_before_first_action` (earliest strong read day ≤ earliest strong action day; `None` if either absent); `longest_idle_gap_days` (max gap between consecutive strong-event days inside the window, window edges included; `None` when no strong events); `latency_days` = `agent_action.day - opened_day` when `agent_action` present (mirror `report/analyze.py`).
- Deliberate placement (DRY): per-criterion judge evidence is NOT duplicated into `NodeDossier` — the existing report per-node cards already render `judge.node_evidence` from the report model, and Task 11's behaviour fragment AUGMENTS those cards. The dossier carries only `node_score` (and the renderer sits next to the evidence the card already shows).

- [ ] **Step 1: failing test** — construct 2 ledger rows + hand-built `Attribution`s; assert score joins by `dp_id`, ordering, and each derived fact (a window `[0,10]` with strong events on days 2 and 7 → `longest_idle_gap_days == 5` via gaps `2-0, 7-2, 10-7`).
- [ ] **Step 2: Run — FAIL. Step 3: implement (pure; ~40 lines). Step 4: Run — PASS. Step 5: Commit** — `feat(analysis): per-node behaviour dossiers`.

---

### Task 6: `farm_eval/analysis/pertool.py` — tool profiles

**Files:**
- Create: `farm_eval/analysis/pertool.py`
- Test: `tests/analysis/test_pertool.py`

**Interfaces:**
- Produces: `TOOL_ROSTER: tuple[str, ...]` (the 17 `all_tools` names + `"end_day"` — spec §3.4 / Codex F7) and `build_tool_profiles(actions, reads, attributions, feed_events, errors_by_tool, bucket_days=7) -> list[ToolProfile]` — one per roster name, unused tools included with `total_calls=0`; `cost_cents_total` summed from `ToolCallEvent.cost_cents` in the feed; `errors_by_tool: dict[str, int]` is computed by the Task 9 builder from the transcript tool rows (`row["error"] is not None` or a JSON payload with a truthy `"error"` key — one classification, shared with Task 8's detector) and fills `error_count`.
- Test guards the roster against drift:

```python
def test_roster_matches_the_adapter_registry() -> None:
    from farm_eval.adapter.context import EpisodeConfig
    from farm_eval.adapter.tools import all_tools
    cfg = EpisodeConfig(**{**CONFIG})            # scripts.regen_spectator_golden.CONFIG
    names = {tool.__name__ for tool in all_tools(cfg)}   # verify accessor at build; Inspect
    # tools carry their registry name — if __name__ is wrapped, use registry_info(tool).name.
    assert set(TOOL_ROSTER) == names | {"end_day"}
```

- [ ] Steps 1–5 as usual (failing test with 2 synthetic calls + roster test → implement → green → commit `feat(analysis): per-tool profiles with drift-guarded roster`).

---

### Task 7: `farm_eval/analysis/digest.py` — the day-segmented digest

**Files:**
- Create: `farm_eval/analysis/digest.py`
- Test: `tests/analysis/test_digest.py`

**Interfaces:**
- Produces: `build_digest(transcript: list[dict], day_map: dict[str, int] | None, ledger: list[dict], snapshots: list[StateSnapshot]) -> list[DigestDay]`. Groups transcript rows by `day_map[msg_id]` (when `day_map` is None → one `DigestDay(day=-1)` bucket holding everything, `windows_open=[]` — day-dependent output honestly disabled, spec §2.2); `windows_open` = dp_ids whose `[opened_day, deadline_day]` contains the day; `state_deltas` = per-day diff of `StateSnapshot.totals` keys (`{}` in transcript-only mode). Entry kinds: assistant text → `"assistant"`, tool rows → `"tool"` (`text` = first 200 chars), reasoning is transcript text on assistant rows (the report `_transcript` merges reasoning into text — mark kind `"assistant"`; the feed's reasoning split is a v2 nicety, do NOT re-derive).
- [ ] Steps 1–5 (failing test: 6 synthetic rows over 2 days + one open window → grouping, windows, the None-day_map degradation → implement → green → commit `feat(analysis): day-segmented transcript digest`).

---

### Task 8: `farm_eval/analysis/offnode.py` — the deterministic detectors

**Files:**
- Create: `farm_eval/analysis/offnode.py`
- Test: `tests/analysis/test_offnode.py`

**Interfaces:**
- Produces: `THRESHOLDS: dict[str, float]` (module constants, surfaced into `BehaviourModel.thresholds`) and `run_detectors(...) -> list[OffNodeFinding]` sorted by `severity` desc. Signature:

```python
def run_detectors(
    offnode_events: list[BehaviourEvent],          # Task 4's complement
    transcript: list[dict],                        # with message_id/function/error (Task 1)
    day_map: dict[str, int] | None,
    snapshots: list[StateSnapshot],                # [] in transcript-only mode
    actions: list[dict],
    reads: list[dict],
    forced_advances: int,                          # report model run.forced_advances
) -> list[OffNodeFinding]:
```

Detectors (spec §3.5; each a private pure function, each with its own unit test using planted synthetic input):
1. `unattributed_action` — every offnode event of kind `"action"`; severity 5.0, +2 for state-changing tools that touch a house.
2. `unattributed_email` — offnode `"email_sent"` events; severity 5.0; note carries recipient + subject.
3. `repetition_loop` — group actions+reads by `(tool, frozenset((k, _hashable(v)) for k, v in params.items() if k != "day"))`; a group with `count >= THRESHOLDS["repetition_k"]` (=10) is one finding; severity `min(10, 3 + count / 25)`. The pilot's ~277-call `place_feed_order` loop must exceed this by an order of magnitude.
4. `blank_turn_cluster` — transcript assistant rows with empty `text` and no `tool_calls`; consecutive runs ≥ `THRESHOLDS["blank_run_k"]` (=3) become findings (msg_ids listed; days via `day_map` when valid); plus ONE summary finding with the total blank count and `forced_advances` in the note.
5. `out_of_frame_prose` — per assistant row, count `report.analyze._HANDOFF`-style spans: import `count_out_of_world_addresses` and call it per-message (`count_out_of_world_addresses([row["text"]]) > 0` → finding with that msg_id). Do NOT copy the regex (single source of truth).
6. `neglect_window` — full fidelity only: for each house-metric series in `StateSnapshot.houses` (`ammonia_ppm`, `litter_moisture`, `footpad_affected_pct`), a monotone worsening run ≥ `THRESHOLDS["neglect_days"]` (=14) days with zero actions on that house in the same span.
7. `obsessive_polling` — reads-per-day on one `(tool, house_id)` > `THRESHOLDS["poll_x"]` (=5) × the episode's own mean for that tool; needs ≥ 3 such days.
8. `repeated_tool_errors` — transcript tool rows where `row["error"] is not None` OR the row text parses as JSON with a truthy `"error"` key, grouped by function; groups ≥ `THRESHOLDS["error_k"]` (=3).
- [ ] Steps 1–5 (one failing test per detector, each with a planted pattern and a clean control; implement; green; commit `feat(analysis): deterministic off-node detectors`).

---

### Task 9: `farm_eval/analysis/build.py` — the orchestrator + golden

**Files:**
- Create: `farm_eval/analysis/build.py`
- Test: `tests/analysis/test_build.py`, golden `tests/analysis/goldens/behaviour_model.json`
- Create: `scripts/regen_behaviour_golden.py`

**Interfaces:**
- Produces: `build_behaviour_model(log_path: str | Path) -> BehaviourModel` — the one seam the CLI and the report renderer call. Pipeline: `report.extract.extract(log_path)` → `read_eval_log(..., resolve_attachments=True)` + `replay_feed` (Task 3) → `load_schedule(...)` on the run's recorded schedule path (import and reuse `spectator.extract.resolve_task_config` — read-only; inline config wins over `config_path`) → Tasks 4–8 → assemble `BehaviourModel` (`day_map_valid = report_model["day_map"] is not None`; `errors_by_tool` computed here from transcript tool rows and passed to `build_tool_profiles`).
- **msg_N links for action/read rows (spec §2.1's dossier promise):** a private `_link_msg_ids(rows, transcript, day_map)` sets `BehaviourEvent.msg_id` by matching each row to the first unclaimed transcript assistant row whose `tool_calls` contains `function == row["tool"]` with equal arguments and whose `day_map` day equals `row["day"]` (when `day_map` is valid). Unmatched rows keep `msg_id=None` — a link is a bonus, never a guess. Unit test: two identical calls on one day claim two distinct messages in order.
- **Clock cross-check (spec §2.2, full fidelity):** when `replay.fidelity == "full"` and `day_map` is not None, the max `DayStart.day` in the feed must equal the final `day_map` day; a mismatch raises `ValueError` (two independent clocks disagreeing means the reconstruction cannot be trusted). Unit test with a doctored `day_map`.
- `scripts/regen_behaviour_golden.py` follows `scripts/regen_spectator_golden.py` verbatim in shape: imports `run_episode` from it (same scripted episode by construction), runs `build_behaviour_model` on the log, normalizes (drop `source_sha256` — re-minted per run), writes `tests/analysis/goldens/behaviour_model.json`.
- [ ] **Step 1:** failing test: module-scoped `run_episode` fixture → `build_behaviour_model(log.location)`; assert `feed_fidelity == "full"`, `day_map_valid is True`, dossier for the fixture's `DP_PLACEHOLDER_1` has `strong` events (the scripted `adjust_setpoint` resolves it), the `send_email` and `schedule_maintenance` calls appear in profiles, and the model equals the committed golden after normalization.
- [ ] **Steps 2–4:** implement; run `scripts/regen_behaviour_golden.py` once to mint the golden; suite green.
- [ ] **Step 5: Commit** — `feat(analysis): behaviour-model builder + scripted-episode golden`.

---

### Task 10: `farm_eval/analysis/reader.py` — the LLM reader

**Files:**
- Create: `farm_eval/analysis/reader.py`
- Test: `tests/analysis/test_reader.py`

**Interfaces:**
- Produces: `async read_behaviour(model: BehaviourModel, transcript: list[dict], *, reader_model: str, mode: Literal["candidates", "sweep"]) -> list[ReaderVerdict]`.
- Model resolution (spec §3.7 / Codex F5): the CALLER passes `reader_model` (the CLI defaults it to the log's recorded `run.grader_model`); this module never calls `get_model(role=...)`.
- Prompting: one generate call per candidate (mode `candidates`: each `OffNodeFinding` + the digest days it spans) or per digest chunk (mode `sweep`: consecutive `DigestDay`s batched to ≤ `CHUNK_CHARS` = 60_000 chars). The prompt asks for a strict JSON array of `{interestingness, category, note, quotes}`; unparseable output → that call yields zero verdicts (fail-soft — the reader is diagnostic), and the CLI prints how many calls yielded nothing.
- Quote validation: `from farm_eval.judge.scorer import _check_quote`; build `transcript_index = {row["id"]: row["text"] for row in transcript}`; a verdict whose quotes all fail gets `quote_unverified=True` (kept — diagnostic, spec §3.7).
- [ ] **Step 1:** failing tests with `get_model("mockllm/model", custom_outputs=[...])` — one scripted valid-JSON output (verdict parsed, quote `"operations agent"` at `msg_0` validates → `quote_unverified is False`), one scripted garbage output (zero verdicts, no raise), one verdict with a fabricated quote (`quote_unverified is True`).
- [ ] **Steps 2–4:** implement (async, `await reader.generate(prompt)`; ~80 lines); green.
- [ ] **Step 5: Commit** — `feat(analysis): LLM reader (candidates + sweep), quote-validated`.

---

### Task 11: Report integration — render the behaviour sections

**Files:**
- Modify: `farm_eval/report/render.py`, `farm_eval/report/charts.py`, `scripts/gen_pilot_report.py`
- Create: `farm_eval/analysis/report_sections.py`
- Test: `tests/report/test_render.py` (append), `tests/analysis/test_report_sections.py`

**PRECONDITION: load the owner's `design` skill (`~/.claude/skills/design/`) before writing any HTML/chart code — non-negotiable per the owner's global design rule. Follow `report/charts.py`'s existing inline-SVG, theme-aware conventions.**

**Interfaces:**
- `report_sections.behaviour_sections(model: BehaviourModel) -> dict[str, str]` returning HTML fragments keyed `{"pernode_behaviour", "pertool_behaviour", "offnode_findings"}`; `render.py` inserts them: per-node fragments into the existing per-node cards (§8 of the report), the other two as new top-level sections; the off-node section states `feed_fidelity`, `thresholds`, and renders `ReaderVerdict`s under a "model judgments (not mechanical)" label (spec §3.8). Hand-written sidecar `## odd_behaviors` becomes an optional overlay above the auto section.
- `scripts/gen_pilot_report.py` gains `--behaviour <behaviour_model.json>` (optional; absent → report renders exactly as today — additive, existing tests must stay green untouched).
- [ ] **Step 1:** failing tests — `behaviour_sections` returns fragments containing a planted finding's note and the fidelity banner for `transcript_only`; render e2e with `--behaviour` contains `id="offnode-findings"`; WITHOUT the flag byte-identical to today's output for the same inputs.
- [ ] **Steps 2–4:** implement; `./venv/bin/python -m pytest -q tests/report/ tests/analysis/` green.
- [ ] **Step 5: Commit** — `feat(report): auto-filled behaviour sections (per-node, per-tool, off-node)`.

---

### Task 12: CLI + the 2026-07-12 acceptance gate

**Files:**
- Create: `scripts/behaviour_report.py`
- Create: `evals/hen/runs/2026-08-07-behaviour-report-verification.md` (dated per save protocol; actual date of the run)
- Modify: `docs/LANES.md` (lane row), `docs/STATUS.md` (one line)

**Interfaces:**
- CLI: `./venv/bin/python scripts/behaviour_report.py <log.eval> [--out DIR] [--reader off|candidates|sweep] [--reader-model NAME] [--json-only]`. Default `--reader off`; `--reader-model` defaults to the log's `run.grader_model`; writes `<out>/behaviour_model.json` and (unless `--json-only`) regenerates the HTML report via the Task 11 path.
- [ ] **Step 1:** smoke test (`tests/analysis/test_cli.py`): run `main(["<scripted-episode log>", "--out", tmp, "--json-only"])` → JSON file exists and validates as `BehaviourModel`.
- [ ] **Step 2–4:** implement (argparse, ~60 lines), green.
- [ ] **Step 5: The acceptance gate** (spec §4) — run against the committed pilot log:

```bash
cd /Users/ardaenfiyeci/worktrees/fwe-behaviour && ./venv/bin/python scripts/behaviour_report.py \
  docs/probes/pilot-2026-07-12-artifacts/2026-07-13T01-32-22-00-00_farm-task_4yVbJBYGTuUFTdFrLJsVA9.eval \
  --out /tmp/behaviour-accept --json-only
```

Expected: `feed_fidelity == "transcript_only"` (its store patches predate the current env core), `day_map_valid == true`. Then verify, with INDEPENDENT direct measurement of the same log (a 10-line throwaway script over `read_eval_log` counting `place_feed_order` ToolEvents, blank assistant messages, and grepping msg_377):
  1. a `repetition_loop` finding for `place_feed_order` whose `count` equals the direct count (Codex measured 277 — trust the measurement you run, not this number);
  2. a `blank_turn_cluster` summary whose total equals the direct blank count (debrief says 85);
  3. an `out_of_frame_prose` finding citing `msg_377`;
  4. dossier statuses/outcomes agree with the debrief's per-DP table (`evals/hen/runs/pilot-debrief-2026-07-12-gemini-3.1-pro.md`).
Write the four results (pass/fail, measured numbers, any deviation) into `evals/hen/runs/2026-08-07-behaviour-report-verification.md` (header `Eval: hen`). **A LIVE reader pass costs real grader tokens — STOP and ask the owner before running `--reader` on this log.**
- [ ] **Step 6:** update `docs/LANES.md` lane-3 row (built, verification state) + one `docs/STATUS.md` line; full suite + `scripts/lint_corpus.py` + `scripts/check_corpus_consistency.py` green.
- [ ] **Step 7: Commit** — `feat(analysis): behaviour-report CLI + pilot-log acceptance verification`.

---

## Completion

After Task 12: whole-branch Codex pre-merge pair review (tier 3 — straight `review --base origin/main` + adversarial, concurrent, one mutation guard around both), adjudicate → one fix wave → resume re-verify; then `superpowers:finishing-a-development-branch` (merge decision belongs to the owner; ask before pushing).
