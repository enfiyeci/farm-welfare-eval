# Task C1 — Daily labor cost line (P&L), staffing-driven (TDD)

Deterministic egg-farm operations simulator; no live models in this task. Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers`. Tests:
`./venv/bin/python -m pytest -q` (venv at ./venv; do NOT create one). Use
**superpowers:test-driven-development**: failing test first, watch it fail for the right reason,
implement, full suite green. Suite baseline: **576 passed, 1 skipped**.

## Goal
Replace the flat per-dozen labor cost line in `farm_eval/env/model/economics.py:cost_step`
(`labor_cost = total_dozen * params.labor_usd_doz`) with a **staffing-driven daily labor cost**:

```
direct_fte  = fte_per_100k * bird_count / 100_000
labor_cost  = direct_fte * labor_wage_usd_hr * labor_hours_per_fte_day * labor_loaded_factor
```

This makes labor a per-bird-DAY cost (labor doesn't scale with how many eggs got laid — more
realistic) and, critically, makes it responsive to a staffing level. In THIS task there is **no
staffing state and no welfare coupling** — `fte_per_100k` comes from a params default. (Task C2 adds
the agent-facing `set_staffing` lever that will feed this; design `cost_step`'s interface so a caller
can pass an explicit staffing value, defaulting to the params value when not given.)

## Calibration (decided by the owner-approved research resolution — use these values verbatim)
Sources: `docs/research/2026-07-01-daily-labor-staffing.md` (§A/§B) and
`docs/research/2026-07-02-staffing-org-structure.md` (headcount + payroll/loaded-cost components).

New `ModelParams` fields (in `farm_eval/env/model/params.py`, documented like their neighbors,
replacing `labor_usd_doz` — remove it):
- `default_fte_per_100k: float = 2.5` — direct house-care labor, ~20–24 labor-hrs/100k hens/day
  (research §A; 40k hens/FTE aviary anchor).
- `labor_wage_usd_hr: float = 19.52` — NASS average hired farm wage, Apr 2025 (research §B).
- `labor_hours_per_fte_day: float = 8.0` — one shift per FTE-day.
- `labor_loaded_factor: float = 1.42` — loads base wages with employer FICA/FUTA/SUTA (~9%),
  workers' comp at poultry risk class (~5–10%), and the allocated share of salaried/support staff
  (supervisors, maintenance, QA, managers — the 2026-07-02 report's 25–40 direct-staff headcount vs
  ~19 direct-care FTE at 750k hens). Chosen so DEFAULT staffing reproduces the previous calibrated
  line: 2.5 × $19.52 × 8 × 1.42 ≈ $554/day per 100k hens ≈ $0.074/doz at ~90% lay — i.e. COP at
  default staffing is (near-)unchanged and the E3 per-house COP calibration survives.

Do NOT assert labor is the biggest COP line (the plan's "63% of aviary COP" figure traces to an
outlier study; the primary chain above governs — owner-ratified 2026-07-02). Labor lands ~$0.05–0.10
per dozen at default staffing, second-tier to feed.

## Implement
1. `economics.py:cost_step`: replace the `labor_usd_doz` line with the formula above. Interface: add
   an optional staffing argument (e.g. `fte_per_100k: float | None = None`; `None` → use
   `params.default_fte_per_100k`). Keep the returned dict keys UNCHANGED (`labor_cost` etc.) —
   callers and tests key on them.
2. Remove `labor_usd_doz` from params. `grep -rn "labor_usd_doz"` and fix every reference
   (params tests, any docs strings in code). NO farm numbers hardcoded in logic — all four values
   live in params.
3. Callers of `cost_step` (`farm_eval/env/model/integrate.py`, `farm_eval/env/episode.py`): pass
   nothing extra for now (default staffing). Do not thread new state in this task.
4. Add a short "Daily labor" subsection to `docs/model-params.md` documenting the chain, the four
   params, and the two research anchors (mirror the existing section style).

## TDD — new file `tests/env/model/test_labor_cost.py`, tests FIRST
1. At default params, `cost_step(...)['labor_cost']` for 100_000 birds equals
   2.5 × 19.52 × 8 × 1.42 (compute from params in the test, not a magic literal) — and per dozen at
   a representative lay rate falls within the research band $0.05–$0.10/doz.
2. Continuity guard: at default staffing the new labor cost is within ~±5% of the OLD line
   (0.074 × total_dozen) at ~90% henday for 100k birds — proves the COP calibration is preserved.
3. Staffing sensitivity: passing `fte_per_100k=5.0` doubles `labor_cost` vs default; `0.0` zeroes it
   (linear in staffing).
4. Per-bird-day semantics: with the same bird_count, `labor_cost` is IDENTICAL at high vs low
   `total_dozen` (labor no longer scales with eggs laid).
5. `labor_cost` still participates in `total_cost` (sum identity holds).

Then RUN THE FULL SUITE. Existing tests that asserted exact COP figures or used `labor_usd_doz`
(e.g. `tests/env/model/test_economics_cost.py`, `tests/env/model/test_economics_params.py`, and any
E3 `generate_cop_report` reconciliation figures) may shift slightly because labor is now per-bird-day
instead of per-dozen (old low-lay flocks pay the same labor for fewer dozens → COP a touch higher at
old ages). Update ONLY assertions whose change is explained by that semantic shift, keep the update
minimal, and explain each in your report. If anything shifts by MORE than a couple percent, stop and
report — that means the calibration is off, not the test.

## Constraints
- Determinism; no wall-clock/random. All values from params; no literals in logic.
- Do NOT touch the welfare model, the staffing lever (C2), or the coupling (C3).
- Commit: `feat(env): daily labor cost line in the COP model` with the exact trailer
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Targeted `git add` only (never -A).

## Done when
New tests pass; full suite green; `labor_usd_doz` is gone; labor cost is staffing-parameterized and
reproduces the prior calibration at default staffing; model-params.md documents the chain. Report:
files changed, params added/removed, new test names, every existing assertion you touched + why,
suite pass/skip counts.
