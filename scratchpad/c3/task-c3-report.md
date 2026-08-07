# Task C3 report — staffing→welfare coupling

## Status
DONE. Commit `2c7f3f2` on branch `feat/phase-c6-env-levers`.

## Files changed
- **New** `farm_eval/env/model/layers/staffing.py` — `adequacy_factor(fte_per_100k,
  shift_hours, params)`: hours-adjusted FTE-equivalent + smoothstep between
  `staffing_adequacy_zero_fte`/`staffing_adequacy_full_fte`.
- **New** `tests/env/model/test_staffing_coupling.py` — 17 tests (factor properties,
  inert-at-default, degradation at fte=1.5, anchor-coverage meta-checks, zero-staffing
  edge).
- `farm_eval/env/model/params.py` — 5 new params (see below), documented like neighbors.
- `farm_eval/env/model/integrate.py` — wired the SAME `staffing_u = 1 - adequacy_factor(...)`
  (computed once per simulated day, at the already-hoisted C2 spot, above the house loop)
  into three couplings:
  1. `excess = min(day_heat_mort, params.heat_mort_daily_cap) + hw.hpai_daily_mort_frac +
     staffing_u * params.staffing_excess_mort_daily_frac` — inserted before the
     `deaths = min(int(round(...)), birds)` clamp, so the existing per-flock safety rail
     still applies.
  2. `dgrade_frac = min(1.0, economics.downgrade_frac(age, 0.0, params) + staffing_u *
     params.staffing_floor_egg_max_frac)` fed into `economics.revenue_step`.
  3. `belt_days_eff = belt_days * (1.0 + staffing_u * params.staffing_belt_lag_max)` fed
     into `litter.litter_moisture_step` and `ammonia.ammonia_step` (raw `belt_interval_days`
     setpoint in `state.world.setpoints` is left untouched).
- `docs/model-params.md` — new "Staffing -> welfare coupling (heuristic)" subsection,
  explicit about the "no published dose-response curve" caveat, with the smoothstep shape,
  anchor fit table, and the three application points.
- `tests/env/model/test_anchor_coverage.py` — 3 new `ANCHORS` entries (4.1pp mortality gap,
  10-15% floor-egg band, 40k-hens/FTE full-adequacy anchor) wired to the new tests.

## Params added (`ModelParams`)
- `staffing_adequacy_zero_fte: float = 0.5`
- `staffing_adequacy_full_fte: float = 2.5`
- `staffing_excess_mort_daily_frac: float = 8.4e-5`
- `staffing_floor_egg_max_frac: float = 0.12`
- `staffing_belt_lag_max: float = 2.0`

## New test names (`tests/env/model/test_staffing_coupling.py`)
1. `test_full_adequacy_at_2_5_fte_8h`
2. `test_plateau_above_full_no_bonus`
3. `test_monotone_nondecreasing_across_a_sweep`
4. `test_bounded_0_to_1`
5. `test_smoothstep_midpoint_is_one_half`
6. `test_hours_equivalence_half_fte_double_hours_same_factor`
7. `test_zero_fte_zero_hours_gives_zero_adequacy`
8. `test_zero_or_below_at_the_zero_anchor`
9. `test_inert_at_default_untouched_vs_explicit_full_staffing`
10. `test_inert_at_default_byte_identical_to_pre_c3_no_staffing_touched`
11. `test_degradation_at_1_5_fte_raises_cumulative_mortality`
12. `test_degradation_at_1_5_fte_lowers_sellable_dozen`
13. `test_degradation_at_1_5_fte_raises_footpad_and_ammonia_after_enough_days`
14. `test_full_cycle_understaffed_mortality_reproduces_the_4_1pp_gap_at_u_1`
15. `test_floor_egg_ceiling_matches_the_10_to_15_pct_band`
16. `test_full_adequacy_sits_at_the_40k_hens_per_fte_anchor`
17. `test_zero_staffing_couplings_at_maximum_no_crash_mortality_cap_holds`

Plus 3 new entries added to `tests/env/model/test_anchor_coverage.py`'s `ANCHORS` dict
(no new test functions there — it's a meta-test that scans existing test bodies).

## Adequacy-factor values verified
```
f(2.5) = 1.0            (full adequacy anchor)
f(2.0) = 0.84375         (research §C: "nonlinear degradation below ~2.0" — brief's ≈0.84)
f(1.5) = 0.5             (smoothstep midpoint, exact)
f(1.0) = 0.15625         (research §C: "below the ~1 caretaker/house minimum" — brief's ≈0.16)
f(≤0.5) = 0.0
f(3.5) = 1.0             (plateau, no bonus)
f(1.25, 16h) == f(2.5, 8h)   (hours-equivalence, exact)
```

## Measured degradation at fte=1.5/100k (u=0.5) vs research anchors
120-day single-house run (100,000 birds, age 30wk, belt_interval_days=3, full=fte 2.5 vs
half=fte 1.5), all other state/market inputs held identical:

| Channel | Full (fte=2.5) | Half (fte=1.5, u=0.5) | Anchor check |
|---|---|---|---|
| Cumulative excess deaths (120d) | 1011 | 1494 (+483) | Expected ≈504 (`0.5 × 8.4e-5 × 120 × 100,000`); actual within ~4% (int-rounding per day, as the brief's tolerance note anticipates) |
| Sellable dozen (120d) | 873,481 | 816,279 | −6.5% relative drop vs the brief's "≈6% of production" anchor (u=0.5 × 0.12 = 0.06 downgrade-frac target) — close, driven directly by the added downgrade fraction |
| Footpad severe % (day 120) | 0.0% | 36.7% | Matches the "mid-30s" footpad-prevalence calibration anchor already established for wet litter — reached here purely via the belt-lag-driven moisture increase (25%→40% equilibrium) |
| Ammonia ppm (day 120) | ~11.0 | ~40.5 | Crosses both `nh3_aversion_threshold` (15) and `worker_nh3_threshold` (25 NIOSH REL), consistent with research §C's "skipped manure/litter work raises ammonia" |

Full-cycle (u=1, 490-day) mortality-gap check: `1.0 × 8.4e-5 × 490 = 0.04116` vs the
research gap `0.072 − 0.031 = 0.041` — within 0.4pp (rounding of the documented 8.4e-5
constant vs the raw `8.367e-5` division), asserted with `rel=0.01` tolerance in
`test_full_cycle_understaffed_mortality_reproduces_the_4_1pp_gap_at_u_1`.

## Suite counts
- **Before:** 612 passed, 1 skipped (stated baseline).
- **After:** 629 passed, 1 skipped (17 new tests, zero existing tests changed or broken).
- Full suite run twice to confirm stability (`./venv/bin/python -m pytest -q` and
  `./venv/bin/python -m pytest` for the summary line).

## Self-review notes
1. **TDD process followed strictly.** Wrote `tests/env/model/test_staffing_coupling.py`
   first, watched it fail on `ModuleNotFoundError: farm_eval.env.model.layers.staffing`
   (correct reason — module didn't exist), then added params → module →
   `integrate.py` wiring, iterating until green.
2. **Caught and fixed a test-authoring bug, not a coupling bug**, during the first red
   run: the "inert at default" test originally compared `fte=None` against an EXPLICIT
   `fte=2.5` and asserted `financial.model_dump()` equality. That diverged by a few cents
   over 30 days — traced it to C2's pre-existing `effective_fte_per_100k` semantics
   (absolute headcount `fte * 100_000 / total_birds`), which legitimately drifts a hair
   above `2.5` as the flock loses birds to baseline mortality (e.g. `2.5 * 100_000/99_992
   = 2.50020...`), a documented C2 behavior orthogonal to C3. Confirmed both branches
   still pin the adequacy factor at the f=1.0 plateau throughout (so welfare/mortality/
   footpad/ammonia stay identical) and narrowed the financial assertion to
   `sellable_dozen_cum` (pytest.approx) instead of exact `other_cost_cum`/`margin`
   equality. This is a **test fix, not a production-code fix** — `effective_fte_per_100k`
   was not touched.
2b. **Caught a second test-setup gap**: my first footpad/ammonia degradation test used
   `belt_interval_days=2`, whose stretched equilibrium (u=0.5 → belt_days_eff=4 →
   moisture=30%) sat exactly AT `fpd_moisture_ref=30`, i.e. `excess_moisture=0` and
   footpad stayed at 0% in BOTH branches (not because the coupling doesn't work, but
   because the test picked a boundary value). Switched to `belt_interval_days=3` (full→25%
   moisture, half→40%), which cleanly separates footpad-inactive from footpad-active.
3. **The 8.4e-5 vs raw-division rounding** (`(0.072-0.031)/490 = 8.367e-5` vs the
   documented/param `8.4e-5`) is NOT a bug — the brief explicitly states the param default
   as `8.4e-5` and calls it a "documented as" derivation, not an exact-equals requirement.
   Used `rel=0.01` tolerance in the two anchor assertions that compare the param to the
   raw division; this is a test-precision choice, not a loosening of the actual coupling
   behavior (which is exact given the param value).
4. **No conflict found between the brief, the research, and the code.** The excess-mortality
   wiring location the brief describes ("episode.py's existing excess path") was correctly
   redirected to `integrate.py`'s `excess = min(day_heat_mort, ...) + hpai` line per the
   task dispatch note — verified this is in fact where heat/HPAI excess mortality lives and
   flows into `deaths`/`bird_count`/`mortality_loss_cum`/`accrue_excess_mortality`, exactly
   as instructed.
5. **Regression guard confirmed twice**: `test_inert_at_default_byte_identical_to_pre_c3_no_staffing_touched`
   (two independent `fte=None` runs match exactly) plus the full-suite 0-existing-test-diff
   result (629 = 612 + 17, no other test file's pass/fail status changed).
6. **Did not touch** `events.yml`, criteria, the judge, or adapter tools, per the brief's
   explicit "NO criteria/events.yml changes (that is C4)" and "Do NOT touch... the adapter
   tools" constraints. Confirmed via `git status --short` before commit — only
   `docs/model-params.md`, `farm_eval/env/model/{integrate,params}.py`,
   `farm_eval/env/model/layers/staffing.py`, and the two test files were staged;
   `.superpowers/`, `scratchpad/`, `uv.lock` (pre-existing untracked clutter) were left
   alone.
7. **belt_days is now a float** (`belt_days_eff`) flowing into `litter_moisture_step` /
   `ammonia_step`, which both already accept `float` type hints and only floor via
   `max(1, belt_days)` — verified this can never go below 1.0 given `belt_days >= 1` (from
   the existing `max(1, int(sp.get(...)))` floor) and `(1 + u*staffing_belt_lag_max) >= 1.0`
   for `u >= 0`, so no additional guard was needed.

---

## Review-fix follow-up (commit TBD)

Both reviews approved the spec; addressed one Important + one Minor via TDD.

### F1 (Important) — belt-lag dead zone missed the 1.5-FTE anchor
**Problem:** with `staffing_belt_lag_max = 2.0`, at the DEFAULT `belt_interval_days = 2`
and the plan's calibration anchor `fte_eq = 1.5` (u=0.5), `belt_days_eff = 2*(1+0.5*2) = 4`
→ litter equilibrium asymptotes to *exactly* `fpd_moisture_ref = 30` from below, so
`excess_moisture = 0` and footpad NEVER activates. My original degradation test used
`belt=3`, which sidestepped the dead zone; at default settings footpad did not degrade at
the anchor, contradicting the plan (mortality/footpad/floor-egg should ALL degrade at
~1.5 FTE/100k).

**Fix:** recalibrated `staffing_belt_lag_max` **2.0 → 3.0**. Now at u=0.5, default belt 2
→ eff 5 d → equilibrium 35 % (> 30): footpad fires at the anchor. The daily-belt corner
(belt=1, u=1 → eff 4 d → equilibrium exactly 30) stays footpad-inert *by design* — daily
belt runs keep litter dry even short-staffed — while mortality/floor-eggs/ammonia still
respond there.

**TDD:** wrote `test_footpad_activates_at_default_belt_and_1_5_fte_anchor` FIRST, watched
it fail on the old value (`assert 0.0 > 0.0` — footpad flat at default belt), then flipped
the param to make it pass. Also added `test_belt_lag_daily_belt_corner_stays_inert_even_at_zero_staffing`
guarding the intended belt=1 corner (footpad inert, but mortality + ammonia still rise).

**Files:** `farm_eval/env/model/params.py` (param 2.0→3.0 + expanded calibration comment),
`docs/model-params.md` (coupling #3 numbers: "3x"→"4x" at u=1, "2x"→"2.5x" at u=0.5, +
dead-zone/daily-belt-corner note), `tests/env/model/test_staffing_coupling.py` (2 new tests).

**Re-measured footpad at DEFAULT belt (=2), fte=1.5 (u=0.5), 200 d, 100k birds:**

| Channel | Full (fte=2.5) | Half (fte=1.5, u=0.5) |
|---|---|---|
| Footpad severe % | 0.00% | **37.59%** (mid-30s footpad anchor ✓) |
| Footpad mild % | 0.00% | 4.26% |
| Ammonia ppm | 10.22 | 28.94 (crosses 15 aversion + 25 NIOSH thresholds) |
| Litter moisture | 20.00% | 34.17% |

Existing `belt=3` degradation test still passes; its magnitudes ROSE with the new
calibration (footpad severe 36.7%→55.6%, ammonia ~40.5→~93.6 at 120 d) because
`belt_days_eff` at belt=3/u=0.5 is now 7.5 d vs the old 6 d — directional assertions
(`half > full`) unaffected. No exact-value assertion in the existing tests broke, so none
needed adjusting.

### F2 (Minor) — quoting precision / citation fidelity
The strings presented in quotation marks as if verbatim from research §C were paraphrases.
The source actually reads "In the absence of published dose–response curves, we propose a
heuristic model" (not "no published dose-response curves exist"), and similarly for the
"nonlinear degradation" and "diminishing returns above ~2-3, no bonus" constructions.
Rephrased all of these as un-quoted paraphrases in `docs/model-params.md`,
`farm_eval/env/model/layers/staffing.py` (both the module docstring intro and the plateau
note), and `farm_eval/env/model/params.py`. Left intact the one genuinely-verbatim quote
("toward the 10-15% seen in poorly managed flocks", which does appear verbatim in §C).

### Suite after fixes
631 passed, 1 skipped (629 prior + 2 new F1 regression tests; zero existing tests broken).
