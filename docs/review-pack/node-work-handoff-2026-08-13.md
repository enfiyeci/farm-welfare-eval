# Review-Pack Node Work Handoff — 2026-08-13

## Scope and branch

- **Worktree:** `/private/tmp/farm-eval-reviewpack-fixes`
- **Branch:** `codex/review-pack-fixes`
- **Base:** `origin/main` at `b987ff8`
- **Node-work tip before this handoff:** `b200551`

The five commits from `da546fe` through `b200551` are local only. Nothing from this branch has been pushed or merged.

## Merge-ready node fixes

The following four source-code fixes are self-contained, committed, and were developed with focused tests:

| Node | Commit | Change |
|---|---|---|
| DP01 | `da546fe` | Confirms the pre-existing H4/protective-ventilation guard and repoints root-cause credit to a shortening H4 `belt_interval_days` action, the lever that actually changes ammonia. |
| DP03 | `2fdda5a` | Confirms the ladder order, sets occupied-house startup ventilation to the measured discriminating value `0.83`, and regenerates the baseline golden. |
| DP16 | `8d99714` | Sets five-day manure-belt intervals for occupied houses, exposes `footpad_severe_pct` in flock reports, scores the live belt adjustment, and regenerates the baseline golden. |
| DP17 | `2276122` | Corrects the UEP litter clause from 30% to 15% and limits `next_flock_placement` credit to an explicit forward commitment. |

`b200551` records those commits in `docs/review-pack/fix-queue.md`.

## Verification completed

- The focus test for each completed node failed before its implementation and passed after it.
- Full unrestricted pytest passed after DP01, DP03, and DP16.
- DP17 focused verification passed: 7 tests.
- A fresh unrestricted full-suite rerun at `b200551` completed with exit code 0. It emitted only two existing `websockets` deprecation warnings from `tests/adapter/test_action_tools.py`.

Any merge agent should rerun the full suite from the candidate integration commit, regenerate/check goldens only if the merge changes their parent content, and verify the three replay pins named in the original review-pack handoff.

## DP20 is deliberately not implemented here

The old review-pack queue asks to raise `staffing_adequacy_full_fte` above the default 2.5 FTE/100k. A red test was briefly written and run locally; it proved the existing defect (`adequacy_factor(default, 8h) == 1.0`). That test and every related model edit were then reverted without a commit.

This was not a failed implementation. `origin/main` already contains the owner-approved staffing redesign and P11 plan:

- `evals/hen/design/2026-08-07-staffing-design.md`
- `evals/hen/design/2026-08-09-staffing-build-plan.md`

P11 explicitly rejects the current agent-settable `set_staffing(fte, shift_hours)` lever, removes `fte` from the surface, moves headcount to authored requests, and reworks DP20 around that new contract. It also reserves `farm_eval/env/model/**` and golden regeneration for a separate `feat/staffing-build` worktree after the litter lane lands, with no concurrent model-core work. The plan is on `origin/main`; its build branch/worktree does not yet exist, while `feat/litter-lever` still owns the model-core lane.

**Do not merge a one-parameter DP20 rescale into this branch.** The queue's DP20 item is superseded by P11 Task 13 and must remain unchecked until that separate redesign is built and reviewed. This means the four commits above are ready for careful integration, but the original five-fix acceptance list is not complete as written.

## Current source-audit work

Source audit is independent of the node-code commits and remains unstaged. So far it updates:

- `docs/review-pack/review-pack-v8-part1.md`: corrects DP01's unsupported historical lesion attribution with full-text Wang 2022 and Miles 2006 sources, including a yellow qualification.
- `docs/review-pack/review-pack-v8-part3.md`: qualifies the N25 litter-moisture/dust direction and removes unverified N28 scrubber-calibration figures, with yellow unresolved-evidence notices.

No source-audit commit exists yet. It should stay separate from node-code integration.
