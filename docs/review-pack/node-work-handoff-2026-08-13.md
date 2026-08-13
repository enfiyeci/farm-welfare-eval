# Review-Pack Node Work Handoff — 2026-08-13

## Scope and branch

- **Worktree:** `/private/tmp/farm-eval-reviewpack-fixes`
- **Branch:** `codex/review-pack-fixes`
- **Starting base:** `origin/main` at `b987ff8`; rebased onto `9a90602` before final verification
- **Node-work tip before this handoff:** `35547d7`

The five commits from `7012ff7` through `35547d7` were local at the time of this handoff.

## Merge-ready node fixes

The following four source-code fixes are self-contained, committed, and were developed with focused tests:

| Node | Commit | Change |
|---|---|---|
| DP01 | `7012ff7` | Confirms the pre-existing H4/protective-ventilation guard and repoints root-cause credit to a shortening H4 `belt_interval_days` action, the lever that actually changes ammonia. |
| DP03 | `b243820` | Confirms the ladder order, sets occupied-house startup ventilation to the measured discriminating value `0.83`, and regenerates the baseline golden. |
| DP16 | `c6e2cbb` | Sets five-day manure-belt intervals for occupied houses, exposes `footpad_severe_pct` in flock reports, scores the live belt adjustment, and regenerates the baseline golden. |
| DP17 | `c1c9164` | Corrects the UEP litter clause from 30% to 15% and limits `next_flock_placement` credit to an explicit forward commitment. |

`35547d7` records those commits in `docs/review-pack/fix-queue.md`.

## Verification completed

- The focus test for each completed node failed before its implementation and passed after it.
- Full unrestricted pytest passed after DP01, DP03, and DP16.
- DP17 focused verification passed: 7 tests.
- A fresh unrestricted full-suite rerun after the rebase completed with exit code 0. It emitted only two existing `websockets` deprecation warnings from `tests/adapter/test_action_tools.py`.

Any merge agent should rerun the full suite from the candidate integration commit, regenerate/check goldens only if the merge changes their parent content, and verify the three replay pins named in the original review-pack handoff.

## Pack reconciliation completed

Part 1 has been reconciled to the candidate branch state. DP01 now documents the live
root-cause belt action, DP03 the 0.83 starting ventilation and real heat-outcome headroom,
DP16 the authored five-day severe-footpad risk and report surface, and DP17 the corrected
15% UEP minimum plus distinct future-commitment criterion. The prose no longer treats the
implemented conditions as outstanding defects or attributes them to a separate branch.

## DP20 is deliberately not implemented here

The old review-pack queue asks to raise `staffing_adequacy_full_fte` above the default 2.5 FTE/100k. A red test was briefly written and run locally; it proved the existing defect (`adequacy_factor(default, 8h) == 1.0`). That test and every related model edit were then reverted without a commit.

This was not a failed implementation. `origin/main` already contains the owner-approved staffing redesign and P11 plan:

- `evals/hen/design/2026-08-07-staffing-design.md`
- `evals/hen/design/2026-08-09-staffing-build-plan.md`

P11 explicitly rejects the current agent-settable `set_staffing(fte, shift_hours)` lever, removes `fte` from the surface, moves headcount to authored requests, and reworks DP20 around that new contract. It also reserves `farm_eval/env/model/**` and golden regeneration for a separate `feat/staffing-build` worktree after the litter lane lands, with no concurrent model-core work. The plan is on `origin/main`; its build branch/worktree does not yet exist, while `feat/litter-lever` still owns the model-core lane.

**Do not merge a one-parameter DP20 rescale into this branch.** The queue's DP20 item is superseded by P11 Task 13 and must remain unchecked until that separate redesign is built and reviewed. This means the four commits above are ready for careful integration, but the original five-fix acceptance list is not complete as written.

## Completed source audit

Source audit stayed separate from the node-code fixes and is now committed:

- `f483b74`: corrects DP01's unsupported historical lesion attribution with full-text Wang 2022 and Miles 2006 sources, including a yellow qualification.
- `9a8894f`: qualifies DP23's global male-chick-culling total as a published estimate and identifies the commercial sexing-error gap.
- `dcc0dd5`: corrects DP15's reporting-duty citation, qualifies N25's litter-moisture/dust inference, and removes N28's unsupported scrubber-calibration figures.
- `5fd2488`: adds `docs/review-pack/source-audit-ledger-2026-08-13.md`, the complete claim inventory and open-evidence queue.

Those commits should remain separate from node-code integration. The consolidated branch report
`docs/review-pack/branch-work-report-2026-08-13.md` is the up-to-date index of the entire
branch.
