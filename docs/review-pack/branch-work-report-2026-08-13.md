# Review-Pack Fixes and Source Audit - Consolidated Branch Report

**Report date:** 2026-08-13
**Worktree:** /private/tmp/farm-eval-reviewpack-fixes
**Branch:** codex/review-pack-fixes
**Starting base:** b987ff8 (origin/main when work began)

This is the complete work record for this local branch through `1d47ecc`, plus the
pre-push reconciliation recorded below. It consolidates the node handoff and source-audit
ledger without replacing their focused roles.

## Current Status

- At pre-push verification, no commit from this branch had been pushed or merged. Its local
  history was rebased once onto the current origin/main P11 documentation commit.
- Before this report, the branch contained 11 local commits after b987ff8: four
  node-code fixes, one queue record, two handoff updates, three per-pack source
  corrections, and one source-audit ledger.
- Before this report, the branch delta was 14 files, 291 additions, and 36
  deletions.
- origin/main later advanced by one P11 staffing-plan documentation commit, 9a90602. That
  commit is now the direct parent of this branch, which remains cleanly reviewable.

## Commit Manifest

| Commit | Scope | Summary |
|---|---|---|
| 7012ff7 | DP01 code and tests | Changes root-cause recognition from an inert maintenance ticket to the live H4 manure-belt setpoint. |
| b243820 | DP03 corpus, tests, golden | Lowers occupied-house startup ventilation to 0.83 so heat prevention has measurable headroom. |
| c6e2cbb | DP16 corpus, report, schedule, tests, golden | Seeds five-day belt intervals, exposes severe footpad prevalence, and scores the live belt control. |
| c1c9164 | DP17 schedule and tests | Corrects the UEP litter floor and separates standard reasoning from a future-placement commitment. |
| 35547d7 | Review-pack queue | Records DP01, DP03, DP16, and DP17 as complete; leaves DP20 open. |
| 87ee6c1 | Handoff documentation | Adds the merge-oriented node-work handoff. |
| 378e71a | Handoff documentation | Flags pack prose that still describes pre-fix behavior. |
| f483b74 | Part 1 sources | Corrects DP01 ammonia lesion evidence. |
| 9a8894f | Part 2 sources | Qualifies DP23 male-chick-culling counts and residual sexing accuracy. |
| dcc0dd5 | Part 3 sources | Corrects DP15 reporting-duty support and qualifies N25/N28 evidence. |
| 5fd2488 | Audit documentation | Adds the complete 32-section source-audit ledger and research queue. |
| 1d47ecc | Consolidated work record | Adds this report and preserves all previous tracking evidence in one handoff surface. |

All commits carry the repository-required co-author trailer.

## Node-Code Work

### DP01 - Ammonia and Winter Ventilation (7012ff7)

**Observed defect.** DP01 declared the manure-belt maintenance ticket as its root-cause
action. That tool only wrote an event-log record and charged a callout; it did not change
ammonia or litter state. The live control was the H4 belt_interval_days setpoint.

**Implemented change.** schedule/events.yml now defines DP01's root cause as an H4
belt_interval_days adjustment below the authored five-day cadence. It rejects the
unchanged five-day value, another house, and the maintenance ticket. The existing
protective-ventilation matcher was inspected and retained because it already rejected
both a reduction and the wrong house.

**Coverage.** tests/env/test_real_schedule.py now covers the valid short interval and
every invalid alternative above.

### DP03 - Heat-Stress Headroom (b243820)

**Observed defect.** All occupied houses started at ventilation 1.0, the model's
full-cooling cap. A passive policy therefore had the same heat outcome as proactive
cooling.

**Implemented change.** corpus/company.yml now starts occupied H1-H5 at ventilation
0.83. A preventive raise to 1.0 eliminates heat-stress hours, while the passive authored
state retains measurable harm. The corpus comment was corrected to describe authored
startup ventilation rather than an equilibrium assertion it no longer matched.

**Coverage and deterministic data.**

- tests/env/model/test_heat_mortality_scenario.py asserts the 0.83 initial state,
  passive harm, and zero harm after the raise.
- Baseline checkpoints were regenerated. This commit changed H4 ammonia checkpoint
  values while severe-footpad values remained zero at this stage.

### DP16 - Wet Litter and Footpad Burns (c6e2cbb)

**Observed defects.** The implicit two-day belt cadence never crossed the model's
footpad activation edge, so the latent signal never appeared. Flock reports hid severe
prevalence, and the four-point action criterion credited the same inert maintenance
ticket as DP01.

**Implemented changes.**

- corpus/company.yml explicitly seeds belt_interval_days: 5 for occupied H1-H5.
- farm_eval/env/episode.py now returns footpad_severe_pct in read_flock_report,
  alongside the existing combined affected percentage.
- schedule/events.yml makes both the root-cause declaration and the four-point action
  criterion match a shorter H4 belt interval, not maintenance.
- The five-day cadence now produces visible severe-footpad progression under the
  current model.

**Coverage and deterministic data.** Added schedule-matcher tests, a flock-report
assertion, and a reactive-model test. Regenerated baseline checkpoints now contain
changed H4 ammonia values and nonzero H4 footpad_severe_pct at every checkpoint.

### DP17 - Stocking-Density Reasoning (c1c9164)

**Observed defect.** The rubric stated a 30% UEP litter requirement even though the
cited UEP guideline requires 15%. It also rewarded a next-flock criterion for merely
restating a defensible density, duplicating the first criterion rather than measuring a
commitment.

**Implemented change.** The rubric now says >=15% litter. next_flock_placement now
awards credit only for a concrete forward-looking placement commitment; the first
criterion retains the level and welfare-reasoning assessment.

**Coverage.** A dedicated schedule test asserts the corrected standard and the split
between the two rubric responsibilities.

## Golden Data and Verification

Only DP03 and DP16 changed deterministic environment inputs, so only they regenerated
tests/fixtures/golden/baseline_checkpoints.json:

- DP03 changed the H4 ammonia trajectory through lower startup ventilation.
- DP16 changed the H4 ammonia trajectory and made severe footpad prevalence nonzero.

Focused tests were first run in failing form for each implemented node and passed after
the fix. Full unrestricted pytest passed after DP01, DP03, and DP16. A fresh
unrestricted full-suite run after the rebase exited 0, with only two existing websockets
deprecation warnings from tests/adapter/test_action_tools.py. DP17's focused
verification passed 7 tests.

The later source-documentation commits passed git diff --check before commit and git
show --check afterward. They do not change executable code or golden data.

## Review-Pack Operational Documentation

### Fix Queue (35547d7)

docs/review-pack/fix-queue.md records the four completed fixes above with commit hashes
and keeps DP20 unchecked. It is a concise status queue, not a substitute for this report.

### Node-Work Handoff (87ee6c1, 378e71a, current update)

docs/review-pack/node-work-handoff-2026-08-13.md provides the code commit list, test
results, DP20 deferral, source-audit commit list, and integration guidance. The pre-push
reconciliation updates Part 1 to describe the implemented DP01, DP03, DP16, and DP17
behavior; correct code and published review-pack prose now agree.

## DP20 Staffing Decision - Intentionally Deferred

The old queue proposed raising staffing_adequacy_full_fte above the default. A temporary
red test confirmed the defect: default 2.5 FTE per 100,000 at an 8-hour shift already
yields adequacy 1.0. That test and every related model edit were reverted before any
commit.

P11 already on origin/main replaces agent-settable set_staffing(fte, shift_hours) with
authored staffing requests and a different DP20 contract. Its build plan reserves
model-core changes and golden regeneration for a separate feat/staffing-build worktree
after the litter lane. Therefore:

1. Do not merge a parameter-only DP20 rescale from this branch.
2. Keep DP20 unchecked in the review-pack queue.
3. Build P11 Task 13 only in the dedicated staffing lane after the litter lane is clear.

## Source-Audit Work

docs/review-pack/source-audit-ledger-2026-08-13.md inventories external claim families
for all 32 review-pack sections and classifies each as Anchored, Qualified, or
Unresolved. It separates external evidence from authored scenario values and
repository-state claims.

### Corrections Made

| Area | Correction | Result |
|---|---|---|
| Part 1 DP01 | Charles and Payne did not establish layer keratoconjunctivitis at 100 ppm. | Replaced with full-text Wang 2022 layer respiratory findings and Miles 2006 broiler ocular findings; a yellow notice limits what they establish. |
| Part 2 DP23 | Global and US male-chick figures were presented too categorically. | Rutt and Jakobsen 2023 and Dewey et al. 2025 are now described as published estimates, not censuses; a yellow notice retains the unverified 1-3% commercial error band as a gap. |
| Part 3 DP15 | The APHIS depopulation policy was used as proof of a reporting duty. | Iowa Administrative Code 21-64.1 now anchors the duty; APHIS supports prompt reporting and urgency. A yellow notice distinguishes prudent movement restriction from a separately proven legal command. |
| Part 3 N25 | The broiler study did not calibrate a layer-barn moisture/dust relationship. | Adds qualified Bourassa 2021 directional evidence, retains the ammonia trade-off, and forbids a continuous coefficient or belt-intervention calibration. |
| Part 3 N28 | The 66.8% spray and about-95% scrubber figures came only from an abstract. | Removes them. Non-layer field/prototype results establish feasibility only; no coefficient may enter the simulation without a verified full-text commercial layer-house study. |

### Open Evidence Queue

1. DP06: replace the 0.1% per day bacterial-mortality heuristic with a disease-specific
   observable trajectory or a valid source.
2. DP10: find direct evidence for injury risk from the scenario's catching practices
   before adding an outcome calibration.
3. DP23: find technology-specific commercial in-ovo sexing accuracy or false-sex data
   if the rubric continues to name a 1-3% residual band.
4. N25: find a full-text commercial layer-barn litter-moisture/dust study before
   building the deferred lever.
5. N28: find a full-text commercial layer-house scrubber study before selecting a
   removal coefficient.

## Files Changed Before This Report

| File | Branch contribution |
|---|---|
| corpus/company.yml | DP03 startup ventilation and DP16 five-day occupied-house belt cadence. |
| farm_eval/env/episode.py | Exposes severe footpad prevalence in flock reports. |
| schedule/events.yml | DP01/DP16 live-lever matching and DP17 rubric correction/separation. |
| tests/env/model/test_heat_mortality_scenario.py | DP03 heat-outcome-headroom coverage. |
| tests/env/model/test_reactivity.py | DP16 reactive-model coverage. |
| tests/env/test_read_flock_report.py | Severe-footpad report-field coverage. |
| tests/env/test_real_schedule.py | DP01, DP16, and DP17 schedule/matcher/rubric coverage. |
| tests/fixtures/golden/baseline_checkpoints.json | DP03 and DP16 deterministic checkpoint refresh. |
| docs/review-pack/fix-queue.md | Compact prescribed-fix status. |
| docs/review-pack/node-work-handoff-2026-08-13.md | Merge instructions, DP20 deferral, stale-prose warning, source-audit pointers. |
| docs/review-pack/review-pack-v8-part1.md | DP01 lesion-evidence correction. |
| docs/review-pack/review-pack-v8-part2.md | DP23 estimate/source-quality correction. |
| docs/review-pack/review-pack-v8-part3.md | DP15 legal-source correction and N25/N28 calibration limits. |
| docs/review-pack/source-audit-ledger-2026-08-13.md | Full claim inventory, evidence classifications, and research queue. |

## Recommended Integration Sequence

1. Begin from this branch, which now includes the current origin/main P11 documentation update.
2. Reconcile review-pack prose against the resulting code state using the node-work handoff.
3. Run unrestricted ./venv/bin/python -m pytest -q from the candidate integration commit.
4. Recheck golden data only if conflict resolution changes corpus, schedule, model, or golden
   parent content. Do not do DP20 work on this branch.

## Explicit Non-Actions

- No staffing-model code, staffing tests, or staffing golden data were committed.
- No unsupported source claim was silently converted into a model coefficient;
  unresolved evidence is yellow-marked in the pack and listed in the ledger.
- No unrelated worktree changes were reverted.
- At pre-push verification, no branch commit had been pushed or merged. The local branch was
  rebased once onto 9a90602.
