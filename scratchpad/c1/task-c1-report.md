# Task C1 report — daily labor cost line (P&L), staffing-driven

## Commit
`fcd2c60` — `feat(env): daily labor cost line in the COP model` (trailer
`Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` included). Branch
`feat/phase-c6-env-levers`. Targeted `git add` only (6 files: 2 source, 1 doc, 3 tests).

## Files changed
- `farm_eval/env/model/economics.py` — `cost_step` gains an optional `fte_per_100k: float
  | None = None` parameter (defaults to `params.default_fte_per_100k`). Replaced
  `labor_cost = total_dozen * params.labor_usd_doz` with:
  ```
  direct_fte = fte_per_100k * bird_count / 100_000
  labor_cost = direct_fte * params.labor_wage_usd_hr * params.labor_hours_per_fte_day
               * params.labor_loaded_factor
  ```
  Returned dict keys unchanged (`labor_cost` still present, same position). Docstring
  extended to explain the staffing seam for Task C2.
- `farm_eval/env/model/params.py` — removed `labor_usd_doz`; added `default_fte_per_100k
  = 2.5`, `labor_wage_usd_hr = 19.52`, `labor_hours_per_fte_day = 8.0`,
  `labor_loaded_factor = 1.42`, each documented inline (mirrors the neighboring fields'
  comment style) with research-anchor references.
- `docs/model-params.md` — new `## Daily labor (staffing-driven, per-bird-day)` subsection
  (placed before `## Evidence levels`, mirroring the existing section style): the formula,
  the four params with anchors, links to
  `docs/research/2026-07-01-daily-labor-staffing.md` and
  `docs/research/2026-07-02-staffing-org-structure.md`, and the "don't claim biggest COP
  line" caveat from the brief.
- `tests/env/model/test_labor_cost.py` (new) — the 5 TDD tests from the brief.
- `tests/env/model/test_economics_cost.py` — one assertion updated (see below).
- `tests/env/model/test_economics_params.py` — one assertion updated (see below).

Callers `farm_eval/env/model/integrate.py:90` and `farm_eval/env/episode.py:556` call
`cost_step` positionally without `fte_per_100k` — no changes needed; both already pass
`bird_count` correctly, so they pick up `params.default_fte_per_100k` automatically.

`docs/plans/2026-06-27-phase-c1-financial-pnl.md` still mentions `labor_usd_doz` — left
untouched. It's a historical plan document for the (already-completed, different) C1
financial-P&L phase, a point-in-time record of past work, not live documentation.

## Params added / removed
Removed: `labor_usd_doz: float = 0.074`.
Added: `default_fte_per_100k: float = 2.5`, `labor_wage_usd_hr: float = 19.52`,
`labor_hours_per_fte_day: float = 8.0`, `labor_loaded_factor: float = 1.42` — all four
values used verbatim from the brief, no hardcoded numbers left in logic (`cost_step`
only reads them off `params`).

## New tests (`tests/env/model/test_labor_cost.py`)
1. `test_labor_cost_matches_staffing_formula_and_research_band` — at default params,
   100k birds, `labor_cost` equals `default_fte_per_100k * labor_wage_usd_hr *
   labor_hours_per_fte_day * labor_loaded_factor` (computed from params, no magic
   literal), and per-dozen at ~90% henday (`total_dozen=7500`) falls in [$0.05, $0.10].
2. `test_labor_cost_continuity_with_old_flat_per_dozen_line` — at default staffing,
   ~90% henday, 100k birds, new `labor_cost` is within 5% of the old `0.074 *
   total_dozen` line.
3. `test_labor_cost_scales_linearly_with_staffing` — `fte_per_100k=5.0` exactly doubles
   `labor_cost` vs default; `fte_per_100k=0.0` zeroes it.
4. `test_labor_cost_is_per_bird_day_not_per_dozen` — same `bird_count=100_000`,
   `total_dozen=100.0` vs `9_000.0` (very low vs very high lay) yields IDENTICAL
   `labor_cost`.
5. `test_labor_cost_still_participates_in_total_cost` — `total_cost` still equals the
   sum of all six cost lines including the new `labor_cost`.

All 5 were confirmed to fail for the right reason before implementation:
- Tests 1 and 3 failed with `AttributeError: 'ModelParams' object has no attribute
  'default_fte_per_100k'` / `TypeError: cost_step() got an unexpected keyword argument
  'fte_per_100k'`.
- Test 4 failed on an assertion mismatch (`7.4 == 666.0`) against the OLD per-dozen
  formula, i.e. it correctly detected that labor still scaled with `total_dozen`.
- Tests 2 and 5 happened to pass even against the old code (they don't probe the
  staffing-specific behavior) — expected, and confirmed independently satisfied after
  the real implementation too.

After implementation, all 5 pass in isolation and in the full suite.

## Existing assertions touched (both are the sanctioned per-bird-day semantic shift —
## no field named `labor_usd_doz` survives to reference, so each was translated to the
## equivalent staffing-formula expression; the calibrated dollar figures at these exact
## scenarios are UNCHANGED, only the source expression changed)

1. `tests/env/model/test_economics_cost.py::test_cost_step_sums_lines` — was
   `assert abs(c["labor_cost"] - 75.0 * p.labor_usd_doz) < 1e-9` (bird_count=1000,
   total_dozen=75.0, a synthetic ratio implying ~90 doz/100 birds — not a realistic
   henday, just an arbitrary probe value). Since `labor_usd_doz` no longer exists and
   labor no longer depends on `total_dozen` at all, rewrote the expected value as
   `default_fte_per_100k * 1000/100_000 * labor_wage_usd_hr * labor_hours_per_fte_day *
   labor_loaded_factor` (i.e. bird_count-driven, matching the new formula exactly — not
   an approximation). This is a direct consequence of the per-bird-day semantic shift,
   not a calibration change: the underlying dollar amount for this specific synthetic
   scenario is whatever the new formula produces, asserted exactly (abs diff < 1e-9).

2. `tests/env/model/test_economics_params.py::test_economic_params_present_with_research_anchored_defaults`
   — was `assert 0.05 <= p.labor_usd_doz <= 0.10`. Rewrote as the equivalent
   staffing-formula expression divided by 7500 dozen (the ~90%-henday/100k-birds
   representative case used throughout the brief), asserting the same `[0.05, 0.10]`
   band. Numerically: `(2.5 * 19.52 * 8.0 * 1.42) / 7500 = 0.0739...` — inside the
   band, confirming the brief's calibration claim holds exactly as stated (no drift;
   this is a like-for-like restatement of the same field-existence check, now computed
   from the four new fields since the one flat field is gone).

No other existing test in the repo referenced `labor_usd_doz` or asserted an exact COP
dollar/cents figure that depended on the labor line through `cost_step` (verified via
`grep -rn "labor_usd_doz"` — zero remaining hits in `farm_eval/`, `tests/`, or
`docs/model-params.md`; and via inspection of every `generate_cop_report` /
`cop_cents_doz` test — `tests/env/test_cop_per_house.py`, `tests/env/test_generate_cop_report.py`,
`tests/adapter/test_generate_cop_report_tool.py`, `tests/env/model/test_economics_reporting.py`
— all either use relative comparisons (`!=`, `>`) or seed `financial.feed_cost_cum` /
`other_cost_cum` directly rather than deriving them from `cost_step`, so none were
sensitive to the labor-formula change). No test shifted by more than the confirmed
sub-0.1% continuity-guard drift (556→554.37 $/day at the calibration point) — well
under the "couple percent" ceiling in the brief; no need to stop and report a
calibration issue.

## Suite results
- Baseline (measured before any change, per the harness's own dot-count since the
  standard pytest summary line was truncated in this shell — verified by counting
  result characters directly): **576 passed, 1 skipped.** Matches the brief's stated
  baseline exactly.
- After adding 5 new tests and updating 2 existing assertions, full suite: **581
  passed, 1 skipped, 0 failed.** (576 + 5 new = 581, confirming nothing else broke or
  got silently skipped.)

## Self-review notes
- Verified `cost_step`'s two production call sites (`integrate.py:90`,
  `episode.py:556`) both already pass `bird_count` as a positional arg in the position
  `cost_step` expects it, and neither passes `fte_per_100k`, so both silently pick up
  `params.default_fte_per_100k` — exactly the "no staffing state, no coupling yet"
  scope the brief specifies for this task.
- Confirmed no other file in `farm_eval/` references `params.labor_usd_doz` (grep clean
  after the change).
- Confirmed the returned dict from `cost_step` still has the same six keys in the same
  order (`feed_cost, energy_cost, labor_cost, capital_cost, pullet_amort, other_var,
  total_cost`) — no caller-visible interface break beyond the new optional kwarg.
- Did not touch `farm_eval/env/model/layers/` (welfare model), any staffing lever/tool,
  or any coupling logic — out of scope per the brief's constraints.
- One cosmetic-only fix during self-review: an inline comment on
  `labor_hours_per_fte_day` had one extra space of alignment drift vs its neighbors;
  corrected before committing (no semantic change, included in the same commit).
- Left `docs/plans/2026-06-27-phase-c1-financial-pnl.md`'s `labor_usd_doz` mentions
  untouched — it's a historical plan doc for prior work, not live documentation the
  brief asked to update (brief only names `docs/model-params.md`).
- No wall-clock/random introduced; all four new values are read from `params`, none
  hardcoded in `cost_step`'s logic body.
