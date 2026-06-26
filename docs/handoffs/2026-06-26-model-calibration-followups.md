# Handoff: model-calibration branch — post-run follow-ups

## Intent
The `feat/model-calibration` branch (19-task plan) is **complete, reviewed, and green** — it
replaced the PLACEHOLDER reactive model with a calibrated six-layer welfare substrate + Layer-1
welfare-state scorer. This next session is NOT about finishing that work; it's about **addressing
the review findings/design questions surfaced during the overnight run**, then deciding on
PR/merge. "Done" = the flagged items below are each resolved or consciously deferred, and the user
has merged (or scoped a follow-up branch).

## State
- All 19 tasks done. Full suite **221 passed**. Branch local at HEAD `6ca891e`, clean (only
  untracked `.claude/`, which is the user's *other* agent's git-snapshot dir — leave it).
- **No PR opened** (per the run instruction). Whole-branch review (opus) verdict: **Ready to merge**,
  no Critical/no blocking Important — verified determinism empirically through the adapter
  `end_day` path, layer signatures, reference-data match, scorer coherence.
- Per-task quality gates ran throughout (SDD reviewer + a second independent adversarial reviewer
  substituting for Codex, which was DOWN this run — see Decisions).
- The flagged items below are **logged, not fixed** — they are the next session's actual work.

## Decisions & rationale
- **Codex backend was unavailable** the entire run (`gpt-5.3-codex` → HTTP 400, account-level, not
  transient). I substituted a 2nd independent Claude adversarial reviewer per substantive task
  rather than retry. That substitute caught the highest-value bugs (vacuous tests, NaN-scoring), so
  the approach worked — but **if the user wants a true Codex pass, re-run reviews once Codex creds
  are fixed.**
- **Kept commit `f0744bd`** (the user's other agent's pre-flight git snapshot that edited the plan)
  as authoritative; the on-disk plan reflects it. Not a rogue edit (user confirmed mid-run).
- **Footpad redesign (commit `64a8d06`)**: original two-compartment model ran to ~100% prevalence
  and could exceed 100%. Replaced with saturating incidence + dry-litter-gated severe healing.
  Rejected: extending the breed/keel curves or adding artificial caps — would contradict the
  authored calibration tables.
- **Did NOT make `litter_moisture` agent-controllable** and **did NOT extend the breed curve past
  wk100** — both are out of the model-calibration plan's scope and are design calls for the user
  (see Open questions).
- Many small review fixes are their own commits (search `(review fix)` in `git log`); rationale for
  each is in its commit body + the ledger.

## Open questions (the morning-review items — this is the work)
Prioritized. Full context for each is in the ledger (see References), but the decisions are the
user's:
1. **`litter_moisture` has no agent-reachable write path.** Agent controls
   ventilation/temperature/belt_interval_days via `adjust_setpoint`, but `litter_moisture` lives on
   `HouseWelfare` and is only set by the reference harness. So **footpad + the ammonia moisture term
   are exercised by the good/negligent yardstick but a live target model cannot pull that lever.**
   Decide: is litter moisture an agent welfare lever (→ needs adapter/tool wiring) or exogenous
   (→ fine, just document)?
2. **Acute heat mortality never fires** under the authored corpus weather (max indoor THI ~28.6 <
   30 onset). Consequently `excess_mortality` AND `keel_risk_hours` are non-discriminating channels
   (negligent==good) and are zeroed in the Layer-1 weighted mean — nh3/heat/footpad carry 100% of
   the welfare-state signal (40% of nominal weight is dropped). Decide: acceptable, or does the
   schedule need a ventilation-failure/heatwave scenario that pushes THI>30, and/or should keel be
   made management-responsive?
3. **Footpad asymptotes toward ~100%** under *persistent* constant-wet litter over a full cycle
   (severe doesn't heal on wet litter → no stable sub-100% equilibrium; calibrated to ~35% at the
   200-day anchor). Confirm this is the intended welfare-realism choice.
4. **`co2_ppm`** is exposed via `read_sensor` and seeded in corpus but never updated by `integrate`
   (pre-existing static read, not a regression). Decide if it should react.
5. **Deferred next thread (per plan, not started):** wire `read_flock_report` / `generate_cop_report`
   from the Hy-Line curve.
6. **PR/merge decision** for the branch itself.

## Next action
Read the ledger `/.superpowers/sdd/progress.md` (the per-task record + every flagged note), then
work item #1 with the user (litter_moisture controllability) — it's the one with the largest effect
on whether footpad is a real welfare lever in live runs.

## References
- Branch: `feat/model-calibration` @ `6ca891e` (36 commits over `main`; merge-base `459b27e`).
- **SDD ledger (read first):** `.superpowers/sdd/progress.md` — full per-task record, all commit
  SHAs, every Minor/design note and carry-forward, the Final Verification + whole-branch-review
  outcomes. This is the durable memory of the run.
- Plan: `docs/plans/2026-06-26-model-calibration.md` · Design spec:
  `docs/specs/2026-06-26-model-calibration-design.md` · Calibration source: `docs/model-params.md`.
- Built code: `farm_eval/env/model/` (params/drivers/accumulators/integrate + `layers/*`),
  `farm_eval/env/{state,loader}.py`, `corpus/weather.yml`, `scripts/regen_golden.py`,
  `farm_eval/judge/{welfare_state.py,scorer.py,welfare_reference.json}`, tests under
  `tests/env/model/`, `tests/env/test_golden_baseline.py`, `tests/judge/`.
- Per-task implementer/reviewer reports (scratch, may be useful): `.superpowers/sdd/task-*-report.md`.
- Project state doc: `CLAUDE.md` (reconciled in Task 19 — model now calibrated).
- Run tests: `./venv/bin/python -m pytest -q` (venv is `./venv`, NOT `.venv`).

## Load these skills next
- `superpowers:subagent-driven-development` (if doing further plan-driven implementation) — keep the
  per-task TDD + dual-review discipline.
- `superpowers:test-driven-development` for any code change.
- `superpowers:finishing-a-development-branch` when ready to merge/PR the branch.
