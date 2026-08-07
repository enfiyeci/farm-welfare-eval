# Task C3 — Staffing→welfare coupling (heuristic, anchored to the labor research) (TDD)

Deterministic egg-farm operations simulator; no live models in this task. Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers`. Tests:
`./venv/bin/python -m pytest -q` (venv at ./venv; do NOT create one). Strict TDD. Suite baseline
will be stated in your dispatch message (C2 just landed).

## Calibration source (BINDING — read the raw research, not summaries)
`docs/research/2026-07-01-daily-labor-staffing.md` §A (task-hours), §C (coupling anchors). The
anchors you must hit are quoted below, but READ the sections yourself; if you find a conflict
between this brief and the research, STOP and ask.

## Goal
Understaffing must degrade welfare and production through ONE adequacy factor. C2 gave the agent
`set_staffing` (state `world.staffing_fte`/`staffing_shift_hours`; helpers
`economics.effective_fte_per_100k(state, params)` / `effective_shift_hours(state, params)`). C3
couples that staffing level into the day-loop (`farm_eval/env/model/integrate.py`) via a single
monotone adequacy factor. NO criteria/events.yml changes (that is C4).

## The adequacy factor
New module `farm_eval/env/model/layers/staffing.py`:

```
def adequacy_factor(fte_per_100k: float, shift_hours: float, params: ModelParams) -> float
```

- Basis is daily LABOR-HOURS per 100k hens (research §A counts 20–24 task-hours/100k/day ≈ 2.5 FTE
  × 8 h): compute the hours-adjusted FTE-equivalent
  `fte_eq = fte_per_100k * shift_hours / params.labor_hours_per_fte_day`, then evaluate the curve on
  `fte_eq`. (A crew of 2 working 16-h surge days covers what 4 cover on 8-h shifts — C4's cull-surge
  mechanics will build on exactly this.)
- Curve: smoothstep between two params —
  `staffing_adequacy_zero_fte: float = 0.5` (f=0 at/below) and
  `staffing_adequacy_full_fte: float = 2.5` (f=1 at/above; research §A: ~40k hens/FTE aviary
  standard). `t = clamp((fte_eq - zero)/(full - zero), 0, 1); f = t*t*(3 - 2*t)`.
  Resulting shape hits the research §C anchors: f(2.5)=1.0 (full adequacy), f(2.0)≈0.84 (mild —
  "nonlinear degradation below ~2.0"), f(1.5)=0.5 (bad), f(1.0)≈0.16 (severe — below the ~1
  caretaker/house practical minimum), f(≤0.5)=0. Monotone, bounded [0,1], PLATEAU above 2.5 (values
  above full clamp to 1 — "diminishing returns above ~2.5–3, no bonus").

Let `u = 1 - f` (inadequacy). Compute f ONCE per house-day in `integrate()` (it depends only on
complex-wide state, so hoisting it above the house loop is fine and cheaper).

## The three couplings (all driven by the SAME u — no per-channel curves)
Apply inside `integrate()`'s day loop, keeping VISIBLE state consistent with the harm accumulators
(the agent must be able to SEE consequences via sensors/reports — that is the discoverability
requirement):

1. **Sick-bird-detection lag → excess mortality** (research §C: aviary 7.2% vs caged 3.1% cumulative
   baseline gap; understaffing is a probable factor). Add `u * params.staffing_excess_mort_daily_frac`
   to the day's `excess` mortality (episode.py's existing excess path: it must flow into deaths,
   `bird_count`, `mortality_loss_cum`, AND `accrue_excess_mortality` exactly like heat/HPAI excess).
   Param default `8.4e-5` — documented as (0.072 − 0.031)/490: the full aviary-vs-caged gap spread
   over a ~70-week lay cycle, reached only at u=1 (zero staffing); at fte_eq=1.5 (u=0.5) the flock
   accrues ~half the gap. Insert BEFORE the daily cap/clamp so the existing safety rails apply.
2. **Inspection/collection lag → floor eggs** (research §C: floor-egg incidence spikes "from a few %
   toward the 10–15% seen in poorly managed flocks"). Add `u * params.staffing_floor_egg_max_frac`
   (default `0.12`, the anchor band midpoint) to the downgrade fraction passed to
   `economics.revenue_step` in integrate.py (clamp total downgrade to ≤ 1.0). Floor eggs are laid
   but lost from sellable grade — revenue and `sellable_dozen_cum` fall, visible in financials.
3. **Litter/manure task lag → footpad + ammonia** (research §C: skipped manure/litter work raises
   ammonia and foot problems). Stretch the EFFECTIVE belt interval before it feeds litter and
   ammonia: `belt_days_eff = belt_days * (1 + u * params.staffing_belt_lag_max)` (param default
   `2.0` → at u=1 the belt effectively runs at 3× its set interval; at u=0.5, 2×). Use
   `belt_days_eff` in `litter.litter_moisture_step` and `ammonia.ammonia_step` (keep the raw
   setpoint untouched in state — the SCHEDULE the agent set is unchanged; the CREW just isn't
   getting to it). Footpad and nh3 then degrade through the already-calibrated physics and are
   visible via `read_sensor`.

At default staffing (agent never touched the lever): `effective_fte_per_100k` returns 2.5 and
`effective_shift_hours` returns 8.0 → fte_eq=2.5 → f=1 → u=0 → ALL three couplings inert and every
existing number byte-identical. That is the regression guard.

## New params (documented like neighbors, citing research §C)
- `staffing_adequacy_zero_fte: float = 0.5`
- `staffing_adequacy_full_fte: float = 2.5`
- `staffing_excess_mort_daily_frac: float = 8.4e-5`
- `staffing_floor_egg_max_frac: float = 0.12`
- `staffing_belt_lag_max: float = 2.0`

## docs/model-params.md
Add a "Staffing→welfare coupling" subsection: state explicitly this is a HEURISTIC (the research
§C: "no published dose-response exists"), grounded on the quoted anchors (40k hens/FTE full
adequacy; degradation onset <2.0 FTE/100k; 7.2%-vs-3.1% mortality gap; 10–15% floor eggs; manure
lag → ammonia/footpad), with the smoothstep shape and the three application points.

## TDD — tests FIRST (`tests/env/model/test_staffing_coupling.py`)
1. Factor properties: f(2.5, 8h)=1; f(3.5, 8h)=1 (plateau, no bonus); monotone nondecreasing in
   fte across a sweep; bounded [0,1]; f(1.5, 8h)=0.5 (the smoothstep midpoint — compute from
   params, not literals); hours-equivalence: f(1.25, 16h) == f(2.5, 8h).
2. Inert at default: integrate N days with staffing untouched vs staffing explicitly set to the
   equivalent of 2.5/100k → identical mortality, footpad, nh3, revenue (and byte-identical to
   pre-C3 behavior — no drift in the existing suite).
3. Degradation at 1.5 FTE/100k (u=0.5), same-seed comparison vs 2.5: cumulative mortality higher by
   ≈ 0.5 × staffing_excess_mort_daily_frac × days × birds (tolerance for the int rounding);
   sellable dozen lower by ≈ 6% of production; footpad severe % and nh3 ppm strictly higher after
   enough days for litter to respond.
4. Anchor-coverage meta-test: mirror the STYLE of `tests/env/model/test_anchor_coverage.py` (read
   it first) — assert the full-cycle understaffed-mortality math reproduces the 4.1pp gap at u=1,
   the floor-egg ceiling matches the 10–15% band, and full adequacy sits at the 40k hens/FTE anchor.
5. Zero staffing (fte=0): f=0, couplings at maximum, no crashes, mortality cap rails still hold.

Then RUN THE FULL SUITE. Zero existing tests should change (the inert-at-default guard). If any
existing test breaks, STOP and report — that means the default path is not inert, not that the
test needs updating.

## Constraints
- Determinism; all numbers from params; no literals in logic; welfare and financial state stay
  separate dimensions (the coupling writes each only through its existing channel).
- Do NOT touch events.yml, criteria, the judge, or the adapter tools.
- Commit: `feat(env): staffing→welfare coupling (heuristic, anchored to labor research)` with the
  exact trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Targeted `git add` only.

## Done when
New tests pass; full suite green with zero existing-test changes; understaffing visibly degrades
mortality/floor-eggs/footpad/nh3 through one factor; default staffing is byte-identical-inert;
model-params.md documents the heuristic + anchors. Report: files changed, params added, new test
names, suite counts, and the measured degradation magnitudes at fte=1.5 vs the anchors.
