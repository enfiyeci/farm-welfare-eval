# Handoff: Task 5 built — density now loads the litter with water
> Written: 2026-08-03 · Branch: `feat/stocking-density` (PUSHED, in sync with origin) · Status: active

**Read this before anything else if you are on a different machine.** The work was done in a
git worktree at `.claude/worktrees/density-n2/`, and `.claude/` is **untracked — it does not
travel**. Do not go looking for that directory. Clone or pull the repo normally and
`git checkout feat/stocking-density`; everything below is on that branch on origin. Paths in
this document are written relative to the repo root for exactly that reason.

## What was done this session

- **Task 5 is BUILT, review-APPROVED, and pushed.** VERIFIED: commits `10a4b71`, `2682711`,
  `b79f02c`, `e863b87` on `origin/feat/stocking-density`. Stocking density now loads the litter
  with droppings water; litter moisture rises when that input exceeds evaporative capacity; and
  footpad plus the ammonia moisture term respond through code that already existed.
- **The litter area fraction is authored for the first time.** VERIFIED: `corpus/company.yml`
  now carries `litter_area_frac: 0.41`. Before this the sim implicitly used UEP's 15 % as the
  real litter provision, which is a certification floor, not a provision.
- **The Codex review pair ran to APPROVED on round 2.** VERIFIED: round 1 returned three
  findings (one P2 straight, two important/high adversarial); all three were adjudicated and the
  fix wave landed in `b79f02c`; round 2 returned `{"findings": [], "verdict": "APPROVED"}`.
- **Task 5b's research question is ANSWERED and the owner's condition is met.** VERIFIED:
  `docs/research/2026-08-03-litter-evaporation-ventilation.md`, committed in `e863b87`.
- **Everything in the repository is pushed.** VERIFIED by scanning every local branch for
  commits absent from every remote: none remain. Two branches from earlier sessions were pushed
  in the process — `feat/flock-cop-reads-integrity` (3 commits) and `feat/phase-c5-judge-v2`
  (2 commits, pilot documentation, new remote branch). **I did not review either one**; they were
  pushed to preserve work across the machine change, not because they were checked.
- **Suite at handoff: 3 failed, 1325 passed, 1 skipped.** VERIFIED by running it. The three
  failures are the same pre-existing golden and reference tests sequenced to Task 13 behind the
  merge gate. Both corpus guards report 0 findings. Working tree clean.

## Goal for next session

- The wave exists to make stocking density an emergent, *tempting* decision so the eval can
  separate adequate welfare play from excellent, **with the difference carried by the world
  rather than the judge**. Task 5 is the first task that actually attaches a welfare cost to
  crowding. Tasks 6, 7, 8 and 12 are what finish the job, and the merge gate is waiting on them.
- **First action: build Task 6** (litter moisture → ammonia), whose design is in
  `docs/plans/2026-07-29-stocking-density-plan.md` lines 1451–1513. **Read the "which layer owns
  ventilation" note under Open questions below before writing any of it** — that decision
  constrains Task 6 and is not recorded in the plan.

## Decisions made

- **`litter_area_frac` is 0.41, and that is a measured figure, not a guess** (owner-approved
  after asking for a research pass). It is the Coalition for Sustainable Egg Supply aviary house
  — US commercial scale, 50,000 hens, our exact housing type — from *Poultry Science* 94(3):475,
  Table 2: forage area 520 cm²/hen of 1,257 cm²/hen total available space. Groot Koerkamp's
  aviary independently gives 47 % (303 m² of 648 m²). **Do not restore 15 %**: that is UEP's
  certification floor and real aviaries exceed it about threefold.
- **The knee is NOT authored, and must never be.** It emerges because evaporation is bounded —
  litter water activity saturates near 0.86, so above the sorption plateau the litter cannot shed
  water faster. Below capacity the belt equilibrium governs alone. **If you find yourself adding
  a threshold on density, you have taken a wrong turn.**
- **Two of the four coefficients are calibrated, not sourced, and the commit says so.** Water
  input (126.8 g/kg/d at 21.4 hens/m²) is Groot Koerkamp's measurement. Evaporative capacity
  (160.0) and the per-excess slope (1.44) are calibrated, because no source fixes either for our
  house. Capacity *had* to land between the compliant house's 155.6 and the surplus lot's 171.7
  or the wave would have no signal at all — the acceptance criteria force the knee between the
  two arms, and the only real freedom was where inside that 10 % band.
- **The standing finding: our houses are ~37 % more loaded on litter than a real aviary.** 26.3
  hens per m² of litter against 19.2 at CSES and 21.4 at Groot Koerkamp's. Owner asked for this
  to be recorded as a standing statement because it reaches back into the *existing* footpad and
  ammonia calibration, not just this wave. It is in `docs/model-params.md` §Density and
  `docs/world-bible.md` §3.
- **A test that exercises the layer directly does NOT guard the wiring — this bit me twice in one
  session.** Both times a "wiring" test passed while the wiring was absent, and both times Codex
  caught it, not me. `tests/env/test_density_reference_is_wired.py` now builds through a bare
  `ModelParams()` exactly as `farm_task` does and runs the real `integrate()`. **Do not accept a
  wiring test you have not mutation-checked** — delete the wiring, watch it go red, restore it.
  That check is cheap and it is the only thing that makes such a test worth having.
- **`0.0` must not be used as an "unset" sentinel for the density params.** An ablation config
  setting `model_params: {litter_area_frac: 0.0}` to disable the pathway would have had the
  corpus value silently restored, so the control run would have run the treatment. The gap-fill in
  `farm_eval/env/episode.py` keys on pydantic's `model_fields_set` instead. **Do not "simplify"
  it back to a zero check.**
- **The 60 % moisture cap does cost some discrimination, and that was accepted deliberately, not
  missed.** Surplus water is added before the clamp, so a wet-belt house can saturate. Measured
  rather than argued: belt intervals 1–5 keep the two arms 16–17 points apart; at belt 7 the two
  placements are still distinguishable (45 vs 60) and only 137k-vs-138k collapses, which DP22
  does not need because it scores bands; at belt 10 everything already saturated before this
  change. Pinned by `test_gradation_survives_across_the_realistic_belt_range`. **Do not "fix" the
  clamp order without re-reading that test's docstring.**
- **The bash working directory silently reverts to the main checkout.** It happened twice this
  session and once caused a `git add` to run in the wrong checkout. Put an explicit
  `cd /path/to/checkout &&` in every shell call, or use absolute paths.

## Open questions

- **Which layer owns the ventilation response? This blocks Task 6 and is not written in the
  plan.** Ammonia already carries its own ventilation and temperature sensitivities (+103 % per
  m/s over litter, +8.1 % per °C) and the plan warns against re-adding terms the sim already
  represents. Task 5b will add ventilation-dependent *evaporation* to the litter layer. Both are
  real and they are different physics, but the boundary has to be stated or the same lever gets
  counted twice. **Proposed split, not yet ratified:** the litter layer owns ventilation's effect
  on drying (evaporative capacity); the ammonia layer owns ventilation's effect on clearing
  already-released ammonia. Decide this before writing either task.
- **Task 5b is authorised in principle but not scoped.** The owner's condition ("we can do it if
  real research does advocate for it") is met — see
  `docs/research/2026-08-03-litter-evaporation-ventilation.md`. The two hazards recorded there are
  the actual work: it moves the no-regression envelope, which must be re-derived across the whole
  weather year rather than at the default setpoint, or five existing houses get silently
  recalibrated on a cold winter day.
- **MERGE TO `main` IS REQUESTED BUT NOT DONE, and I flagged it rather than doing it.** The owner
  asked to "push everything into the online repo merge". The push is done. The merge is not,
  because the merge gate in `docs/plans/2026-07-29-stocking-density-plan.md` lines 37–51 is
  explicit that Tasks 5–8 and 12 must land and Task 13 must regenerate the goldens first — and
  Tasks 6, 7, 8, 12 and 13 are all still outstanding, so the branch currently carries 3 failing
  tests. **Awaiting the owner's answer.** If they confirm they want it merged anyway, that is
  their call to make, but it should be a deliberate override of a written gate rather than a
  side-effect of a push request.
- **Two branches were pushed without review** (see What was done). Whether they should be merged,
  rebased, or deleted is undecided; I only preserved them.

## References

- **The branch:** `feat/stocking-density` on `enfiyeci/farm-welfare-eval` (private). This
  session's commits, oldest first: `10a4b71`, `2682711`, `b79f02c`, `e863b87`.
- **The plan, and the merge gate:** `docs/plans/2026-07-29-stocking-density-plan.md` — Task 5 at
  lines 1374–1447, Task 6 at 1451–1513, the merge gate at 37–51.
- **The research this wave's coefficients come from:**
  `docs/research/2026-07-30-density-coefficients.md` (passes 5 and 6 are the load-bearing ones).
- **Task 5b's brief:** `docs/research/2026-08-03-litter-evaporation-ventilation.md`.
- **The full derivation, the calibration honesty, and the deferred gap:** `docs/model-params.md`
  §Density.
- **Code:** `farm_eval/env/model/layers/density.py` (new, pure), `farm_eval/env/model/layers/litter.py`,
  `farm_eval/env/model/integrate.py`, `farm_eval/env/loader.py` (`params_for`),
  `farm_eval/env/episode.py` (the gap-fill), `farm_eval/env/model/params.py`.
- **Tests:** `tests/env/model/test_layer_density.py`, `tests/env/test_density_reference_is_wired.py`,
  shared setup with three documented traps in `tests/env/_density_support.py`.
- **The previous handoff, now superseded:**
  `docs/handoffs/2026-08-03-dp22-dp23-built-grader-facts.md` — still worth reading for the DP22 and
  DP23 decisions, which this session did not touch.
- **Commands:** tests `./venv/bin/python -m pytest -q` (venv is `./venv`, not `.venv`); corpus
  guards `./venv/bin/python scripts/lint_corpus.py` and `scripts/check_corpus_consistency.py`;
  and after any schedule or config change, regenerate `scripts/gen_corner_briefings.py` and
  `scripts/audit_schedule.py` — they are not in Task 13's golden list and have tripped the suite
  before.

## Load these skills next

- `superpowers:test-driven-development` — every task on this wave is written test-first, and
  red-green caught real defects again this session.
- `superpowers:subagent-driven-development` — delegation is owner-approved for this build.
