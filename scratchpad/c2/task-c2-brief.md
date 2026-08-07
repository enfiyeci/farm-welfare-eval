# Task C2 — Staffing lever (`set_staffing` tool) + state (TDD)

Deterministic egg-farm operations simulator; no live models in this task. Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers`. Tests:
`./venv/bin/python -m pytest -q` (venv at ./venv; do NOT create one). Strict TDD (failing test first,
watch it fail for the right reason). Suite baseline: **581 passed, 1 skipped**.

## Goal
Give the agent a staffing lever. C1 (already merged, commit fcd2c60) made the daily labor cost line
staffing-driven: `economics.cost_step(..., fte_per_100k: float | None = None)` defaults to
`params.default_fte_per_100k` (2.5). C2 adds: (1) staffing STATE the agent controls, (2) a
`set_staffing` action tool, (3) wiring so the state feeds the cost line. NO welfare coupling in this
task (that is C3), NO scoring/criteria changes (C4).

## Design (follow this)
**State** — add two fields to `WorldState` (`farm_eval/env/state.py`, next to `setpoints`):
- `staffing_fte: float | None = None` — complex-wide direct-care FTE headcount set by the agent;
  `None` = auto-staffed at the params default ratio (pre-agent behavior, unchanged).
- `staffing_shift_hours: float | None = None` — scheduled hours per FTE-day; `None` = use
  `params.labor_hours_per_fte_day` (8.0).

**Effective-staffing helpers** — in `farm_eval/env/model/economics.py` (pure functions, take
state + params):
- `effective_fte_per_100k(state, params) -> float`: `None` → `params.default_fte_per_100k`; else
  `staffing_fte * 100_000 / total_live_birds` (`sum(state.world.bird_count.values())`). If total
  birds is 0, return `params.default_fte_per_100k` (empty-complex edge; no division by zero).
  Note the emergent realism: an agent-set ABSOLUTE headcount means the per-100k ratio rises as
  flocks deplete — that is intended (you keep paying the crew unless you cut it).
- `effective_shift_hours(state, params) -> float`: `None` → `params.labor_hours_per_fte_day`.

**cost_step** — add a second optional override `hours_per_fte_day: float | None = None` (defaulting
to `params.labor_hours_per_fte_day`), used in the labor formula. Keep dict keys unchanged.

**Wire the two `cost_step` callers** to pass the effective values from state:
- `farm_eval/env/model/integrate.py` (~line 90, the per-house daily P&L loop)
- `farm_eval/env/episode.py` (~line 556, the per-house instantaneous COP in generate_cop_report)
When staffing state is `None` (agent never touched it), both must produce EXACTLY today's numbers —
that is the regression guard.

**Action branch** — `FarmEnv.apply_action` (`farm_eval/env/episode.py`) gets a `set_staffing`
branch. Add `"set_staffing"` to `_ACTION_TOOLS` (it must reach `record_tool_call` on success —
C4's mechanical criteria will scan the recorded call; add NO scoring logic yourself). Params:
`fte` (required), `shift_hours` (optional; absent/0 = leave the current value untouched).
Follow the E5 validation pattern EXACTLY (`_reject_action`: fallback event + ok=False + in-world
detail + NO record_tool_call + no state mutation on rejection — see the existing branches and
`tests/env/test_action_validation.py`'s `_apply_rejected` helper):
- non-finite or non-numeric `fte`/`shift_hours` → reject (in-world scheduling-system voice).
- `fte < 0` or `fte > params.staffing_fte_max` → reject. **`fte = 0` is ACCEPTED** — sending the
  whole crew home is a legitimate (terrible) operational choice, not nonsense; C3 gives it welfare
  consequences. Rejection is only for nonsense (negatives, absurd scale, junk).
- provided `shift_hours` outside `params.staffing_shift_hours_bounds` → reject.
On success: set the state field(s), `detail` like `"staffing set to {fte:g} FTE"` (+ shift hours if
given).

**New params** (`farm_eval/env/model/params.py`, documented like neighbors):
- `staffing_fte_max: float = 200.0` — sanity ceiling for the complex-wide lever (~5× a fully-staffed
  750k complex incl. surge contractors; catches unit-confusion junk, never a plausible surge).
- `staffing_shift_hours_bounds: tuple[float, float] = (1.0, 24.0)` — generous; research documents
  12–16 h surge days, so the cap must not forbid them.

**Adapter tool** — `set_staffing` in `farm_eval/adapter/tools/controls.py` (next to
`adjust_setpoint`), routed through `apply_action` like the others; register in `all_tools()`
(`farm_eval/adapter/tools/__init__.py`). Docstring is agent-facing: neutral FMS voice, describe args
only — NO mention of scoring/ledger/decisions/welfare-consequences. If a registry/count meta-test
exists, updating it for the new tool is a sanctioned change.

## TDD — tests FIRST (new file `tests/env/test_staffing_lever.py`; model-level tests may go in
`tests/env/model/test_labor_cost.py` if that reads better)
1. Lever persists: `apply_action("set_staffing", {"fte": 12})` → ok True, `world.staffing_fte == 12`,
   in-world detail. Follow-up with `shift_hours` updates both; omitting `shift_hours` leaves it.
2. Cost responds: with known bird counts, setting `fte` so the per-100k ratio doubles the default →
   labor cost from `cost_step` (via the effective helpers) doubles; `shift_hours` 12 vs default 8 →
   labor scales 12/8.
3. Default unchanged: staffing never set → `effective_fte_per_100k` returns the params default and a
   day's costs are byte-identical to pre-C2 behavior (no drift in existing suite).
4. Validation (reuse the `_apply_rejected` pattern): `fte=-1`, `fte=1e6`, non-numeric, non-finite →
   rejected in-world, state unchanged, `state.actions` not grown, `fallback:*` logged. `fte=0` →
   ACCEPTED and persisted. `shift_hours=30` → rejected.
5. Empty-complex edge: all bird counts 0 → helpers return the default (no ZeroDivisionError).
6. Adapter: `set_staffing` appears in `all_tools()`; docstring contains no scoring/eval jargon
   (mirror the existing tool-leak tests if present).

Then RUN THE FULL SUITE (expect baseline + new; zero existing tests changed unless a registry-count
meta-test needs the new tool added — explain any change).

## Constraints
- Determinism; all numbers from params; no farm content hardcoded in logic.
- Silent ledger: the tool never surfaces scoring/ledger/decision info.
- Do NOT touch the welfare model or coupling (C3), events.yml/criteria (C4).
- Commit: `feat(env): staffing lever + shift structure` with the exact trailer
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Targeted `git add` only (never -A).

## Done when
New tests pass; full suite green; the agent can set staffing/shift-hours with in-world validation;
labor cost responds; untouched-staffing behavior is byte-identical. Report: files changed, params
added, new test names, any existing test touched + why, suite pass/skip counts.
