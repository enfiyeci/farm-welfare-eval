# Lanes — who is doing what, where

The index for running several Claude sessions on this repo at once. Open this instead of guessing
from session titles. **Whoever changes a lane's status updates its row in the same breath.**

Last updated: 2026-08-07 (the repo reorganization merged).

> ### 🔴 REORG LANDED 2026-08-07 — merge `main` before continuing any lane
>
> The documentation tree was reorganized (`evals/{hen,dairy}/` + `docs/` as the cross-eval slot;
> owner-ruled, Codex-pair APPROVED). ~200 files moved; CLAUDE.md was trimmed and the status
> narrative now lives in `docs/STATUS.md`. **Every lane must merge `main` into its branch before
> its next commit** — branches editing old `docs/…` paths will hit rename-vs-edit conflicts, and
> git's rename detection resolves them cleanly only if you merge rather than cherry-pick. The
> full old→new map: `docs/reorg/2026-08-06-repo-reorg-move-plan.md` §9. File conventions from now
> on: `docs/save-protocol.md`.

Previous update: 2026-08-06 (rewritten after the owner ruled on all eleven decision briefs — see
`evals/hen/design/decisions/00-RULINGS.md`).

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
pilot.** Rulings and rationale in `evals/hen/design/decisions/00-RULINGS.md` ("The program to finish the hen
eval").

### Step 1 — Folder restructuring (do FIRST; blocks the lanes)

> ✅ **GATE CLEARED 2026-08-06.** The other machine confirmed its pushes. Verified rather than
> assumed (`git fetch --all --prune`, then every branch and worktree checked):
> - every local branch in sync with origin, **except** `feat/stocking-density-task6`
>   (`[ahead 95, behind 60]` — the known divergence, already rescued to
>   `origin/archive/stocking-density-task6-local-2026-08-06`, so nothing is at risk);
> - **all seven worktrees clean** (no uncommitted work anywhere);
> - two new branches arrived from the other machine: `archive/c6-sdd-process-2026-07`,
>   `wip/2026-08-06-owner-html-snapshot`;
> - `docs/decision-briefs` contains `origin/main`, so it is the correct base for the reorg.
>
> Still gated on the owner's structural preferences — the reorg strategy comes back for approval
> before any file moves.

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

### RUNNING NOW — two lanes (owner, 2026-08-06)

| Lane | Where | What it is doing | State |
|---|---|---|---|
| **litter-prep (P2)** | merged to `main` · worktree removed | The launch-pack P2 lane, complete: UEP edition conflict settled at source (2024 deletes the carve-out), all four load-bearing findings traced and CONFIRMED, the FULL tier-1/2 source list (8 PDFs incl. Vestergaard 1997) read end to end and archived under `evals/hen/research/sources/`, both stocking-density branches mined with a claim list, the owner's positive-welfare directive recorded, four review rounds (two loops + capped escalation + owner-granted fresh round). Deliverable: `evals/hen/research/2026-08-07-litter-prep/`. | **DONE — 🔔 R3 RULED 2026-08-07: litter access hours (see `evals/hen/design/decisions/00-RULINGS.md` §1). P8 is UNBLOCKED**; handoff: claude-sync `handoff-2026-08-07-p8-litter-build.md`; two authoring sub-decisions travel with P8 (select-access doors; compliant vs inherited-violation day-0 schedule). |
| **L1 · research** | this session | The open design questions: the litter-access-hours lever (dose-response, behavioural welfare cost, the UEP confinement rule, floor-egg economics, control realism) and the ammonia model-semantics question (does a single-compartment house value calibrate to bird-level 6.0 or whole-house 6.7). Both passes must return an **owner fetch list** of paywalled sources. | 2 passes in flight — superseded by litter-prep (P2) above, which verified its outputs |
| **L2 · repo reorg** | `~/worktrees/fwe-reorg` · `chore/repo-reorg` (off `docs/decision-briefs`) | Reading **every one of 309 candidate files** — all of `docs/`, the root loose files, `judge/dimensions/`, and the stray label dirs — six readers with no gaps between them. Produces a per-file record: what it is, domain, which eval it belongs to, live-vs-stale, inbound/outbound refs, code/config coupling, proposed destination, move risk. | 6 readers in flight |

**L2 discipline (owner: "every single file will be read, I don't want laziness"):** readers may not
move, edit or delete anything. Binary/bulk artifacts (`.eval` logs, PDFs, large JSON) are catalogued
by type and provenance rather than falsely claimed as read — and every reader must close with a
coverage statement whose counts reconcile. **The reorg strategy returns to the owner for approval
before a single file moves**, and implementation then runs cautiously with Codex review.

### Step 2 — the design lanes (start AFTER the folder restructure)

Five lanes on **this machine**. The split is designed so no two concurrently-running lanes write the
same files. Aquatic is explicitly **deferred** by the owner (2026-08-06) — the focus is finishing the
hen eval.

| # | Lane | Worktree / branch | Owns (writes) | Must not touch | Blocked on |
|---|---|---|---|---|---|
| 1 | **litter** — the critical path | `~/worktrees/fwe-litter` · `feat/litter-lever` | `farm_eval/env/model/**`, `params.py`, goldens, both reference artifacts, DP01/DP16/DP22 signatures, the new lever's tool + corpus/schedule content | anything outside the model core | **The lever re-pick (ruling 1): litter drying vs litter access hours** + the ammonia target (6.0 vs 6.7, ruling 2). Both are owner calls. |
| 2 | **staffing-design** — deep brainstorm, docs only first | `~/worktrees/fwe-staffing` · `feat/staffing-design` | `evals/hen/design/**`, `evals/hen/research/**` (staffing only) | **all code** until its design is ruled | The h6 session's recovered staffing-fork analysis (see below). |
| 3 | **behaviour-report** — ruling 8's third deliverable | `~/worktrees/fwe-behaviour` · `feat/behaviour-report` | `farm_eval/analysis/**` + its tests, **and `farm_eval/report/**`** (owner-expanded 2026-08-07 so the analysis renders into the HTML pilot report) | `farm_eval/env/**`, `farm_eval/judge/**`, `farm_eval/spectator/**` (read-only) | **DONE — merged to `main` 2026-08-08** (owner: "lets merge this for now we will take a look at it again after we go through the nodes"). All twelve tasks built subagent-by-subagent with a review gate each, then a whole-branch review and a **two-round Codex pre-merge pair** (round 1: 7 Important findings, all accepted and fixed — three were detector *false negatives*; round 2: adversarial APPROVED, straight left 2 P2s, both fixed). Design `evals/hen/design/2026-08-07-behaviour-report-design.md` (§7 records rounds 1–7 incl. where the build deliberately deviates); CLI `scripts/behaviour_report.py`. The acceptance gate over the saved 2026-07-12 pilot log caught a real recall gap (`out_of_frame_prose` missed `msg_377`, the debrief's own F2/F3/F4 recap) — fixed, and the gate is now reproducible by one command: `evals/hen/runs/2026-08-07-behaviour-report-acceptance/independent_measure.py <log>` checks the committed artifact against the debrief's dp-table and exits non-zero on failure (4/4 PASS). **Open:** the LLM reader stage has never run against a live provider (owner go/no-go — it costs grader tokens); worktree kept for the owner's follow-up look. |
| 4 | **node-triage** — measure, do not change | `@gone` (worktree removed) · `feat/node-triage` | `docs/probes/**` only | **`config.yml`, `schedule/events.yml`, `farm_eval/env/model/**`** — measures, never edits | **DONE — merged to `main` via PR #27 (2026-08-07).** Probe report: `docs/probes/2026-08-07-node-triage-discrimination.md` — only DP18 is truly non-functional; DP16 discriminates on `main` (cliff caveats → L1); DP20 matcher exact but substrate-unbacked (→ L3); DP21 gate exact, its early-discard scoring defect **fixed and merged** (owner-directed exception to measure-only: `Criterion.window_from`, schedule + scorer + tests + a timing-agnostic `residue_w36.md`); 7 nodes grader-only by design. |
| 5 | **plf-dairy** — already running | `~/worktrees/farm-welfare-eval-plf-decisions` · `feat/plf-dairy-eval` | `pyproject.toml`, root `README.md`, the PLF package | the layer-hen model core | Nothing. In flight (background to the hen focus). |

**Why 2, 3 and 4 are safe to run at once:** lane 2 writes only prose, lane 3 writes only a new module
that does not yet exist, lane 4 writes only probe reports. None touches a file lane 1 owns. Lane 4 is
the one to watch — node triage naturally *wants* to edit `enabled_nodes`, and it must not; it reports,
lane 1 applies.

**The litter lane absorbs several rulings** into its one golden regeneration: ruling 1 (lever), 2
(ammonia base — through TAN, target chosen), 3 (DP16 rework), and the DP22 band collapse. See the
research in `evals/hen/research/2026-08-06-litter-lever-and-ammonia/` — the model form must lag ammonia
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
| **fin-audit → L8 build** | `docs/financial-node-audit` · worktree `~/worktrees/fwe-fin-audit` | Audit half DONE: `evals/hen/design/2026-08-07-financial-node-audit.md` + probe script/data. **R8 RULED (owner, 2026-08-07): build (i) feed-made-real + (ii) credit line; drop (iii) propane; defer (iv) contract mix; (v) molt/depop to phase 3.** Spec approved (`evals/hen/design/2026-08-07-financial-skill-axis-design.md`); **implementation plan written** (`evals/hen/design/2026-08-07-financial-skill-axis-plan.md`, T1–T10, SDD). **Two-wave sequencing (owner-approved 2026-08-09):** Wave A (T1–T9, minus the three P8-owned hunks) builds NOW without touching `farm_eval/env/model/**` — the storage cap moved to `corpus/finance.yml`, so `params.py` is not touched at all, and the two `integrate.py` wire-in hunks (T1 Step 8, T5 Step 6) + the `financial_reference.json` regen (T9) defer to **Wave B**, which runs after P8 merges to `main`. **Wave A Task 1 (cash + revolver core, M1) BUILT 2026-08-10** on this branch: task-reviewed + tier-2 Codex-adversarial-reviewed + one fix round, full suite green; money-market sweep yield sourced to FRED TB3MS (spec §10 open item closed). Task 2 build next. The formal R8 entry now lives in `evals/hen/design/decisions/00-RULINGS.md` §14 (written 2026-08-10). Known plan defect found in T1 review — T2 lender-switch/patronage double-counts its fee against cash — fix folded into the plan doc 2026-08-10. |

**Aquatic is deferred**, not on either machine's active list, per the owner.

### 🔔 Standing gate — do not let this one slip

**Before the first real pilot run, and after the final calibration wave**, the FY26 cost-target
number (ruling 6) must be put to the owner and ruled. It edits `msg_0`, so runs either side of it
cannot be pooled; deciding after a pilot means paying for a third pilot. Whichever lane schedules
the pilot owns this check. Full statement in `evals/hen/design/decisions/00-RULINGS.md` §6.

## Closing out

| Status | Topic | Worktree | Branch | State |
|---|---|---|---|---|
| `HANDED-OFF` | branch-consolidation | `~/worktrees/fwe-main` | `docs/decision-briefs` | The eleven briefs + the rulings file. Ready to merge. |
| `NEEDS-YOU` → superseded | calibration | `~/worktrees/fwe-recalib` | `feat/litter-ammonia-recalib` | Its blocking question is answered. Work folds into lane 1. All commits **are** pushed — the handoff's "3 unpushed" warning was stale. |
| `CLOSING` | h6-refpolicy | gone | `fix/reference-policy-h6` | **Wait.** Recovering a staffing-fork design analysis that exists in no file — now more valuable, since lane 2 would use it. |
| `CLOSING` | finiteness-guards | gone | — | Clear to archive once it confirms its Codex round 2. |
| `DONE` | spectator | merged | — | On `main`. Its `claude-sync` commits are pushed. Free to archive. |

## Branches that are only history — ⚠️ THE PREVIOUS CLAIM HERE WAS WRONG

The earlier version of this section, and `evals/hen/design/decisions/README.md`, both said all four of
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
`evals/hen/design/decisions/10-measured-answers.md`.
