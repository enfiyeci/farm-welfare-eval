# Lanes — who is doing what, where

The index for running several Claude sessions on this repo at once. Open this instead of guessing
from session titles. **Whoever changes a lane's status updates its row in the same breath.**

Last updated: 2026-08-06.

## Session title convention

Every session working on this repo is titled:

```
STATUS · topic · @folder
```

- **STATUS** — one of five, so you can scan for what needs you:

  | Status | Means | What you do |
  |---|---|---|
  | `NEEDS-YOU` | Blocked on a decision only you can make | Answer it; nothing moves until you do |
  | `ACTIVE` | Working, will report back | Nothing |
  | `CLOSING` | Deliverable committed, one loose end left | Wait for the loose end, then archive |
  | `DONE` | Finished and merged | Archive whenever |
  | `HANDED-OFF` | Wrote a handoff doc; a fresh session continues from it | Start the new session |

- **topic** — a short kebab-case name that stays the same for the life of the lane.
- **@folder** — the **worktree basename** it works in. This is the important one: two sessions sharing
  a folder is what caused the August tangle, where a staged-and-modified file sat in a tree two
  sessions both thought they owned. `@gone` means its worktree was removed and it can no longer run
  shell commands. `@merged-to-main` means it has no branch left.

## The rules that make it work

1. **One session per worktree. Never two.** Check this table before starting a session.
2. **New lane = new worktree**, at `~/worktrees/fwe-<topic>`, branch created off current `main`.
3. **A lane owns its files.** If two lanes need the same file, one of them waits — say so in its row.
4. **Only one lane at a time regenerates the goldens or the reference artifacts.** Two lanes doing it
   produces two irreconcilable sets of numbers and no way to tell which is right.
5. When a lane finishes, set its status to `DONE`, update the row, and archive the session.

## Current lanes

| Status | Topic | Worktree | Branch | Owns / waiting on |
|---|---|---|---|---|
| `NEEDS-YOU` | calibration | `~/worktrees/fwe-recalib` | `feat/litter-ammonia-recalib` | The goldens and both reference artifacts. Blocked on the briefs 01–03 batch ruling. **3 commits unpushed.** |
| `ACTIVE` | plf-dairy | `~/worktrees/farm-welfare-eval-plf-decisions` | `feat/plf-dairy-eval` | `pyproject.toml`, root `README.md`, the new PLF package. Doing Stage 1 restructure, then deferred decision #3. |
| `HANDED-OFF` | branch-consolidation | `~/worktrees/fwe-main` | `docs/decision-briefs` | The eleven decision briefs. Handoff written 2026-08-06. |
| — | aquatic | `~/worktrees/fwe-aquatic` | `feat/aquatic-outreach` | Not yet started. Rescued RP outreach plan and SWIM research are committed there. |
| `CLOSING` | h6-refpolicy | gone | `fix/reference-policy-h6` | Work merged into the calibration branch. Recovering an uncommitted staffing-fork analysis. |
| `CLOSING` | finiteness-guards | gone | — | Work committed as `3ba31cf`. Confirming whether a Codex round-2 found anything unrecorded. |
| `DONE` | spectator | merged | — | On `main` at `0bfe90a`. Two commits still unpushed in `claude-sync`. |

## Lanes not yet opened

From the consolidation plan. Each needs its own worktree off current `main`.

| Topic | Suggested worktree | Blocked on |
|---|---|---|
| node-triage | `~/worktrees/fwe-node-triage` | Nothing — can start now. Must not edit `config.yml` or `schedule/events.yml` (calibration owns both). |
| staffing | `~/worktrees/fwe-staffing` | The brief-04 fork answer, **and** the calibration merge, since its numbers move with the coefficients. |
| track-d | `~/worktrees/fwe-trackd` | Nothing — can start now. Purely additive under `farm_eval/study/`. |

## Branches that are only history

`feat/stocking-density`, `feat/stocking-density-task6`, `fix/model-params-finiteness`,
`fix/reference-policy-h6` — all provably contained in `feat/litter-ammonia-recalib`, all pushed. They
delete themselves from the picture when that branch merges. Nothing to decide.

## Checking the live state

The table above is hand-maintained and can drift. The git facts underneath it are not:

```bash
git worktree list && git branch -vv
```

For dirty trees and unpushed work across every worktree at once, see the audit block in
`docs/decisions/10-measured-answers.md`.
