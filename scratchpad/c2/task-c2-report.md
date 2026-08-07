# Task C2 report — staffing lever (`set_staffing`)

## Files changed

- `farm_eval/env/state.py` — `WorldState` gains `staffing_fte: float | None = None` and
  `staffing_shift_hours: float | None = None`, next to `setpoints`.
- `farm_eval/env/model/economics.py` — new pure helpers `effective_fte_per_100k(state, params)`
  and `effective_shift_hours(state, params)`; `cost_step` gets a second optional override
  `hours_per_fte_day: float | None = None` (defaults to `params.labor_hours_per_fte_day`),
  used in the labor formula in place of the previously-hardcoded `params.labor_hours_per_fte_day`
  reference. Dict keys returned by `cost_step` are unchanged.
- `farm_eval/env/model/integrate.py` — the per-house daily P&L loop's `cost_step` call now
  passes `fte_per_100k=effective_fte_per_100k(state, params)` and
  `hours_per_fte_day=effective_shift_hours(state, params)`.
- `farm_eval/env/episode.py`:
  - `_ACTION_TOOLS` gains `"set_staffing"` (NOT added to `_HOUSE_KEYED_TOOLS` — it's
    complex-wide, no house_id).
  - New `set_staffing` branch in `apply_action`, following the E5 `_reject_action` pattern
    exactly: non-numeric/non-finite `fte` or `shift_hours` → reject; `fte < 0` or
    `fte > params.staffing_fte_max` → reject; `fte == 0` → **accepted**; provided
    `shift_hours` outside `params.staffing_shift_hours_bounds` → reject (absent/0 leaves the
    current value untouched — no bounds check in that case). On success sets
    `state.world.staffing_fte` (and `staffing_shift_hours` if a nonzero value was given),
    detail `"staffing set to {fte:g} FTE"` (+ `, {shift_hours:g} h/shift` if given), then falls
    through to the shared `record_tool_call` at the end of `apply_action`.
  - `generate_cop_report`'s per-house instantaneous `cost_step` call now passes the same two
    effective-value overrides from `self.state`/`self.params`.
- `farm_eval/env/model/params.py` — two new params, documented like neighbors:
  `staffing_fte_max: float = 200.0` and `staffing_shift_hours_bounds: tuple[float, float] =
  (1.0, 24.0)`.
- `farm_eval/adapter/tools/controls.py` — new `set_staffing` Inspect tool (agent-facing
  docstring: args only, no scoring/ledger/welfare jargon), routed through
  `env.apply_action("set_staffing", {"fte": fte, "shift_hours": shift_hours})`.
- `farm_eval/adapter/tools/__init__.py` — imports and registers `set_staffing` in
  `all_tools()`, right after `adjust_setpoint`.
- `tests/env/test_staffing_lever.py` (new) — 25 tests, see below.
- `tests/env/model/test_labor_cost.py` — 3 new tests for the `hours_per_fte_day` `cost_step`
  seam (kept alongside the existing C1 labor-cost tests per the brief's suggestion).
- `tests/adapter/test_action_tools.py` / `tests/adapter/test_read_tools.py` — the registry-count
  meta-test (`len(all_tools(CFG))`) updated from 16 to 17 (9 reads + 8 actions), a sanctioned
  change per the brief since `set_staffing` is a new registered tool.

## Params added

- `staffing_fte_max: float = 200.0` — sanity ceiling for the complex-wide `set_staffing` lever.
- `staffing_shift_hours_bounds: tuple[float, float] = (1.0, 24.0)` — generous shift-length bounds.

## New tests

`tests/env/test_staffing_lever.py` (25 tests):

- Lever persists: `test_set_staffing_persists_fte_and_returns_in_world_detail`,
  `test_set_staffing_records_tool_call_on_success`,
  `test_set_staffing_with_shift_hours_updates_both`,
  `test_set_staffing_omitted_shift_hours_leaves_current_value_untouched`,
  `test_set_staffing_zero_shift_hours_also_leaves_current_value_untouched`.
- Cost responds: `test_effective_fte_per_100k_doubling_doubles_labor_cost_via_cost_step`,
  `test_effective_fte_per_100k_from_state_doubles_the_ratio`,
  `test_effective_shift_hours_scales_labor_12_over_8`,
  `test_effective_shift_hours_from_state`,
  `test_end_to_end_set_staffing_changes_generate_cop_report_overhead` (drives a real `FarmEnv`
  through `end_day()` until the fixture flock is in lay, then compares `generate_cop_report`
  overhead before/after doubling the complex-wide effective FTE ratio).
- Default unchanged: `test_effective_fte_per_100k_defaults_to_params_when_unset`,
  `test_effective_shift_hours_defaults_to_params_when_unset`,
  `test_untouched_staffing_produces_byte_identical_day_costs` (two fresh envs, neither ever
  calls `set_staffing`, `end_day()` once each, asserts `state.financial.model_dump()` equal —
  the regression guard).
- Validation (via the `_apply_rejected` helper, copied/adapted from
  `tests/env/test_action_validation.py`): `test_set_staffing_negative_fte_is_rejected`,
  `test_set_staffing_absurdly_large_fte_is_rejected`,
  `test_set_staffing_non_numeric_fte_is_rejected`,
  `test_set_staffing_non_finite_fte_is_rejected` (both `inf` and `nan`),
  `test_set_staffing_zero_fte_is_accepted`,
  `test_set_staffing_shift_hours_out_of_bounds_is_rejected`,
  `test_set_staffing_non_numeric_shift_hours_is_rejected`,
  `test_set_staffing_at_max_boundary_is_accepted`.
- Empty-complex edge: `test_effective_fte_per_100k_empty_complex_returns_default_no_zero_division`
  (all bird counts present but 0), `test_effective_fte_per_100k_no_houses_at_all_returns_default`
  (no houses in `bird_count` at all).
- Adapter: `test_set_staffing_registered_in_all_tools` (via `ToolDef(t).name`, matching the
  pattern in `tests/adapter/test_egg_disposition_tool.py`),
  `test_set_staffing_docstring_has_no_scoring_or_ledger_jargon` (checks
  `inspect.getdoc(execute)` for banned substrings: ledger/decision/welfare/scor/judge/tripwire).

`tests/env/model/test_labor_cost.py` (3 new tests, appended after the existing C1 tests):
`test_labor_cost_hours_per_fte_day_override_scales_labor_proportionally`,
`test_labor_cost_hours_per_fte_day_none_defaults_to_params`,
`test_labor_cost_dict_keys_unchanged_with_hours_override`.

## Existing tests touched (and why)

- `tests/adapter/test_action_tools.py::test_all_tools_registry` and
  `tests/adapter/test_read_tools.py::test_pricing_tools_registered_and_computed`: both assert
  `len(all_tools(CFG))`. Updated `16 → 17` (comment updated `7 actions → 8 actions (C2: +
  set_staffing)`). This is the registry-count meta-test the brief explicitly sanctioned
  updating for a new tool. No other existing test was modified.

## Full-suite results

- Baseline (confirmed before any change): **581 passed, 1 skipped**.
- After C2: **609 passed, 1 skipped** (`./venv/bin/python -m pytest --tb=short -p no:warnings`).
  609 − 581 = 28 = 25 (new `test_staffing_lever.py`) + 3 (new `test_labor_cost.py` tests).
  Skip count unchanged (1), and it is the same pre-existing skip, not a new one — the
  end-to-end COP test in `test_staffing_lever.py` was written to advance the fixture flock via
  `end_day()` until `generate_cop_report` reports `available: True` (with a `pytest.skip` guard
  only as a last resort if the fixture window were ever too short; in practice it wasn't
  triggered — see self-review below).

## Self-review notes

- **TDD discipline**: wrote `tests/env/test_staffing_lever.py` and the 3 new
  `test_labor_cost.py` tests first, watched them fail for the right reason (`ImportError:
  cannot import name 'effective_fte_per_100k'` and `TypeError: cost_step() got an unexpected
  keyword argument 'hours_per_fte_day'`), then implemented.
- **E5 pattern fidelity**: the `set_staffing` branch mirrors `adjust_setpoint`'s validation
  exactly — non-numeric coercion via `try/except (TypeError, ValueError): float(...)`, then a
  combined `not math.isfinite(...) or out-of-bounds` check, each returning through
  `self._reject_action(fallback_type, tool, params, detail)` with realistic in-world wording
  ("Scheduling system rejects ..."), never mutating state or calling `record_tool_call` on any
  rejection path. Verified via the full `_apply_rejected` contract (ok=False, addressed_dps=[],
  `state.actions` didn't grow, a `fallback:*` event-log entry was appended) — same helper
  semantics as `tests/env/test_action_validation.py`.
- **Order-of-checks bug caught before commit**: the initial end-to-end COP test computed a
  "doubled" FTE using only `H_SENSOR`'s bird count, but `effective_fte_per_100k` divides by
  the TOTAL bird count across all houses (`sum(state.world.bird_count.values())`) per the
  brief's design — with two 1000-bird fixture houses, that made the "doubled" FTE evaluate
  to exactly the params default (no observable change), and the assertion failed with `67.6 >
  67.6`. Fixed by computing the doubled FTE from `sum(bird_count.values())`, which is also a
  good confirmation that `effective_fte_per_100k`'s complex-wide (not per-house) semantics are
  exactly as designed — an important nuance since `generate_cop_report`'s per-house branch
  still uses the COMPLEX-wide effective ratio (matching `cost_step`'s existing per-house call
  signature, which takes a single `fte_per_100k` scalar either way).
- **`fte=0` and `shift_hours=0` semantics double-checked**: `fte=0` mutates
  `state.world.staffing_fte = 0.0` (accepted, not treated as "leave untouched" — only
  `shift_hours` has the absent/0-means-untouched semantics per the brief). Verified with
  `test_set_staffing_zero_fte_is_accepted` and the "leave shift_hours untouched" tests.
- **NaN handling**: `math.isfinite(float("nan"))` is `False`, so `not math.isfinite(fte)` alone
  correctly rejects NaN without relying on `fte < 0` (which is `False` for NaN under IEEE 754
  comparison semantics) — verified explicitly with `test_set_staffing_non_finite_fte_is_rejected`
  covering both `inf` and `nan`.
- **Regression guard verified two ways**: (1) `effective_fte_per_100k`/`effective_shift_hours`
  unit tests confirm `None` → params defaults; (2) an end-to-end `test_untouched_staffing_
  produces_byte_identical_day_costs` runs two independent fresh `FarmEnv`s that never call
  `set_staffing`, advances each one `end_day()`, and asserts `state.financial.model_dump()`
  is exactly equal — proving the wiring changes in `integrate.py` and `episode.py` don't alter
  today's numbers when the lever is untouched.
- **No welfare coupling, no scoring changes**: confirmed no edits to any welfare model file
  under `farm_eval/env/model/layers/`, `judge/`, or `schedule/events.yml` — `set_staffing`
  reaches `record_tool_call` on success (so C4's mechanical criteria can scan for it later) but
  no scoring logic was added in this task, per the brief.
- **No farm content hardcoded**: all new numeric bounds live in `ModelParams`
  (`staffing_fte_max`, `staffing_shift_hours_bounds`); `apply_action`/`cost_step` reference only
  those params, never literals.
- **Determinism**: no wall-clock/randomness introduced; all new logic is pure functions of
  state + params.

---

# Codex review fixes (commit edecae4)

Coordinator relayed a Codex adversarial review of 364bf84 with two Important findings and one
Minor. All three fixed via TDD (F1 and F2 tests written first and watched fail for the right
reason; F3 is a strengthened guard on already-correct code, so it passes immediately by design).

## F1 (Important) — per-day staffing hoist in `integrate.py`

**Bug confirmed:** `effective_fte_per_100k(state, params)` was evaluated inside the per-house
loop, but `state.world.bird_count[hid] = birds - deaths` (mortality, line ~184) mutates the
complex total inside that same loop. With `staffing_fte` set, houses later in iteration order
were costed against a post-mortality total → inflated ratio → total daily labor exceeded the
absolute FTE setting and depended on house iteration order.

**Fix:** both effective-staffing lookups hoisted out of the house loop — computed once per
simulated day, inside `for offset in range(elapsed_days)`, before `for hid, hw in ...`, and the
precomputed values passed to `cost_step`. Multi-day semantics preserved: the ratio is
re-resolved at each day's start, so it still rises as flocks deplete ACROSS days (the intended
emergent realism), while being consistent WITHIN a day. `generate_cop_report`'s inline lookup
in `episode.py` is untouched — it is an instantaneous read outside any mutation loop.

**New test:** `test_staffing_total_labor_is_absolute_headcount_despite_within_day_mortality`
(+ helper `_two_house_state`). Drives `integrate(state, 1, params)` directly on a bare
two-house state (120k + 80k birds at 30 wk, so baseline mortality kills birds within the day —
asserted explicitly, or the test proves nothing). Isolates labor as the `other_cost_cum` delta
between a staffed (`fte=10`) and a default (`fte=None`) run — every other cost line is
identical across the two, and mortality is staffing-independent (also asserted). Asserts the
staffed complex's total daily labor equals exactly `fte × wage × hours × loaded` within 1e-6.
Watched it fail against the old code with error $0.0399 (the mortality-order inflation), pass
after the hoist.

## F2 (Important) — shift-hours reset discoverability

Once a non-default `shift_hours` is set, 0/absent means "leave unchanged" and `None` is
rejected, so the agent could never discover how to restore the standard schedule. Per the
coordinator's chosen resolution (no new sentinels, no behavior change): the standard value is
now stated in the `set_staffing` adapter docstring in neutral FMS voice —
"Scheduled hours per worker per day (standard schedule: 8). Omit or pass 0 to leave the
current schedule unchanged." Since params are fixed per run, setting 8 explicitly is a
complete reset.

**New test:** `test_set_staffing_docstring_states_standard_shift_for_reset_discoverability` —
asserts the docstring contains `f"standard schedule: {ModelParams().labor_hours_per_fte_day:g}"`,
cross-checking the stated number against the params value so the docstring cannot silently
drift from `labor_hours_per_fte_day`. (The literal "8" in the docstring is agent-facing corpus
voice, and the test pins it to params.)

## F3 (Minor) — conversion test at a non-100k total

The original `test_effective_fte_per_100k_from_state_doubles_the_ratio` used exactly 100,000
birds, where the conversion is its own inverse — an INVERTED formula
(`fte * total / 100_000`) would also have passed. Added
`test_effective_fte_per_100k_non_100k_total_rejects_inverted_formula`: 250,000-bird complex
(150k + 100k), `staffing_fte = 2 × default × 2.5`, asserts the effective ratio equals
`2 × default` (the inverted formula would return 31.25 vs the correct 5.0).

## Files changed in the fix commit

- `farm_eval/env/model/integrate.py` — per-day hoist (F1).
- `farm_eval/adapter/tools/controls.py` — docstring standard-schedule note (F2).
- `tests/env/test_staffing_lever.py` — 3 new tests + `_two_house_state` helper (F1/F2/F3).

## Suite after fixes

**612 passed, 1 skipped** = post-C2 baseline (609 + 1 skip) + 3 new tests. No existing test
touched in this commit.
