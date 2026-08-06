# Lanes — who is doing what, where

The index for running several Claude sessions on this repo at once. Open this instead of guessing
from session titles. **Whoever changes a lane's status updates its row in the same breath.**

Last updated: 2026-08-06 (rewritten after the owner ruled on all eleven decision briefs — see
`docs/decisions/00-RULINGS.md`).

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

## The program to finish the hen eval (2026-08-06)

**Goal (owner):** finish the hen eval — a complete, runnable, defensible version, then a real full
pilot run of it. "Demo" = finished project, not a screenshot and not a replay.

**Order (owner):** **(1) folder restructuring first → (2) the design lanes → (3) the finishing
pilot.** Rulings and rationale in `docs/decisions/00-RULINGS.md` ("The program to finish the hen
eval").

### Step 1 — Folder restructuring (do FIRST; blocks the lanes)

> 🚧 **GATE (owner, 2026-08-06): do NOT start the reorg until the OTHER machine has pushed
> everything and both machines are synced.** A restructure while the other machine holds unpushed
> commits would create irreconcilable conflicts (the exact failure this project keeps hitting). The
> other machine has been told to push all it has; wait for confirmation, `git fetch --all`, verify
> no branch is ahead of origin anywhere, THEN reorder. Also gated on the owner's structural
> preferences — it is not a mechanical reorg.

Not a mechanical reorg — it needs the owner's taste on the target layout. It also applies ruling 12
(instruction-file protocol): trim `CLAUDE.md` to stable conventions + pointers (Anthropic targets
<200 lines), move the drifting "Current state" narrative into this file (`docs/LANES.md`) as the
single-owner status doc, decide the `AGENTS.md`/`CLAUDE.md` relationship, and fix the stale breed
label on `feat/stocking-density` + `feat/litter-ammonia-recalib` before either merges. Research
backing: `docs/research/2026-08-06-claudemd-governance/`. **Blocked on the owner's structural
preferences.**

### The one rule that shapes everything (Step 2)

**Exactly one lane owns `farm_eval/env/model/` and the golden regeneration: the `litter` lane.**
Everything else is either docs-only, or additive in its own new module. Two lanes regenerating
goldens produces two irreconcilable sets of numbers with no way to tell which is right.

### Step 2 — the design lanes (start AFTER the folder restructure)

Five lanes on **this machine**. The split is designed so no two concurrently-running lanes write the
same files. Aquatic is explicitly **deferred** by the owner (2026-08-06) — the focus is finishing the
hen eval.

| # | Lane | Worktree / branch | Owns (writes) | Must not touch | Blocked on |
|---|---|---|---|---|---|
| 1 | **litter** — the critical path | `~/worktrees/fwe-litter` · `feat/litter-lever` | `farm_eval/env/model/**`, `params.py`, goldens, both reference artifacts, DP01/DP16/DP22 signatures, the new lever's tool + corpus/schedule content | anything outside the model core | **The lever re-pick (ruling 1): litter drying vs litter access hours** + the ammonia target (6.0 vs 6.7, ruling 2). Both are owner calls. |
| 2 | **staffing-design** — deep brainstorm, docs only first | `~/worktrees/fwe-staffing` · `feat/staffing-design` | `docs/design/**`, `docs/research/**` (staffing only) | **all code** until its design is ruled | The h6 session's recovered staffing-fork analysis (see below). |
| 3 | **behaviour-report** — ruling 8's third deliverable | `~/worktrees/fwe-behaviour` · `feat/behaviour-report` | a new module (suggest `farm_eval/analysis/`), its own tests | `farm_eval/env/**`, `farm_eval/judge/**` (read-only) | Nothing once Step 1 lands. |
| 4 | **node-triage** — measure, do not change | `~/worktrees/fwe-node-triage` · `feat/node-triage` | `docs/probes/**` only | **`config.yml`, `schedule/events.yml`, `farm_eval/env/model/**`** — measures, never edits | Nothing once Step 1 lands. |
| 5 | **plf-dairy** — already running | `~/worktrees/farm-welfare-eval-plf-decisions` · `feat/plf-dairy-eval` | `pyproject.toml`, root `README.md`, the PLF package | the layer-hen model core | Nothing. In flight (background to the hen focus). |

**Why 2, 3 and 4 are safe to run at once:** lane 2 writes only prose, lane 3 writes only a new module
that does not yet exist, lane 4 writes only probe reports. None touches a file lane 1 owns. Lane 4 is
the one to watch — node triage naturally *wants* to edit `enabled_nodes`, and it must not; it reports,
lane 1 applies.

**The litter lane absorbs several rulings** into its one golden regeneration: ruling 1 (lever), 2
(ammonia base — through TAN, target chosen), 3 (DP16 rework), and the DP22 band collapse. See the
research in `docs/research/2026-08-06-litter-lever-and-ammonia/` — the model form must lag ammonia
through litter TAN, not map moisture→NH₃ same-day.

### Step 3 — the finishing pilot

FY26 cost target ruled first (ruling 6, `msg_0`, irreversible). Out-of-family grader. Full 518-day
episode = the finished hen eval demonstrated. Vertex ADC works; `scripts/pilot-vertex.env` (gitignored)
is created. **Do NOT run before Step 2 lands** (owner: no fresh pilots until the design is done).

### Other machine (docs-only support, safe to run anytime — no model-core collision)

| Lane | Branch | Why safe here |
|---|---|---|
| **validation-gate prep** | `docs/validation-gate` | The expert labelling pack, eval-awareness blind sheets, and outreach for a real vet/welfare labeller. The long pole for the "result" half of the eval, independent of engineering. |
| **research-backlog** | `docs/research-backlog` | The still-blocked sources — EFSA 2023, Sirovnik 2018, Campe 2018, Bell & Weaver. Writes only under `docs/research/`. |

**Aquatic is deferred**, not on either machine's active list, per the owner.

### 🔔 Standing gate — do not let this one slip

**Before the first real pilot run, and after the final calibration wave**, the FY26 cost-target
number (ruling 6) must be put to the owner and ruled. It edits `msg_0`, so runs either side of it
cannot be pooled; deciding after a pilot means paying for a third pilot. Whichever lane schedules
the pilot owns this check. Full statement in `docs/decisions/00-RULINGS.md` §6.

## Closing out

| Status | Topic | Worktree | Branch | State |
|---|---|---|---|---|
| `HANDED-OFF` | branch-consolidation | `~/worktrees/fwe-main` | `docs/decision-briefs` | The eleven briefs + the rulings file. Ready to merge. |
| `NEEDS-YOU` → superseded | calibration | `~/worktrees/fwe-recalib` | `feat/litter-ammonia-recalib` | Its blocking question is answered. Work folds into lane 1. All commits **are** pushed — the handoff's "3 unpushed" warning was stale. |
| `CLOSING` | h6-refpolicy | gone | `fix/reference-policy-h6` | **Wait.** Recovering a staffing-fork design analysis that exists in no file — now more valuable, since lane 2 would use it. |
| `CLOSING` | finiteness-guards | gone | — | Clear to archive once it confirms its Codex round 2. |
| `DONE` | spectator | merged | — | On `main`. Its `claude-sync` commits are pushed. Free to archive. |

## Branches that are only history — ⚠️ THE PREVIOUS CLAIM HERE WAS WRONG

The earlier version of this section, and `docs/decisions/README.md`, both said all four of
`feat/stocking-density`, `feat/stocking-density-task6`, `fix/model-params-finiteness` and
`fix/reference-policy-h6` were "provably contained in `feat/litter-ammonia-recalib`, all pushed",
with "nothing at risk and nothing to weigh". **Two of the four were neither.** Verified with
`git merge-base --is-ancestor` against the calibration tip on 2026-08-06:

| Branch | Contained in calibration? | On a remote? |
|---|---|---|
| `fix/model-params-finiteness` | **Yes** | yes |
| `fix/reference-policy-h6` | **Yes** | yes |
| `feat/stocking-density` | **NO** | yes (`origin/feat/stocking-density`) |
| `feat/stocking-density-task6` | **NO** | **was on NO remote at all** |

`feat/stocking-density-task6` had **95 commits that existed only on this machine**, diverged from
its own remote branch (which holds 60 commits the local one does not — a rebase that was never
pushed). Its local tip `bf87cc4` is a day newer than the remote tip and differs by **126 files**,
including `config.yml`, the four baseline configs, corpus emails, design docs and handoffs. Several
of its commits are directly load-bearing for the litter-drying lane — "Kang 2016 halves the moisture
coefficient" and "our NH3 ceiling is the wrong housing system".

**Rescued 2026-08-06** to `origin/archive/stocking-density-task6-local-2026-08-06`. A new ref was
used deliberately rather than force-pushing over the diverged branch, which would have destroyed the
60 remote-only commits. Force-push is also blocked by a global safety hook, and correctly so.

**Do not delete either `feat/stocking-density` or `feat/stocking-density-task6` on the assumption
that merging the calibration branch absorbs them. It does not.** Someone has to decide what in them
is still wanted — that is a real open question, not the non-decision the briefs described.

## Checking the live state

The table above is hand-maintained and can drift. The git facts underneath it are not:

```bash
git worktree list && git branch -vv
```

For dirty trees and unpushed work across every worktree at once, see the audit block in
`docs/decisions/10-measured-answers.md`.
