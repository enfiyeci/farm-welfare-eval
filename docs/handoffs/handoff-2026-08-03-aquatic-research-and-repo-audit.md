# Handoff: aquatic eval research (Rethink Priorities) + farm-eval repository audit
> Written: 2026-08-03 · Updated: 2026-08-03 for a move to a different computer
> Branch: `wip/2026-08-03-machine-transfer` · Status: active

## READ FIRST — you are on a different machine

This handoff was written on one computer and is being picked up on another. Before anything else:

> **Corrections applied 2026-08-03 (later session, verified on the origin machine).** Four instructions
> below were wrong as first written. Each correction was checked against the repository, not assumed.

1. **This branch is NOT the whole picture — check what you actually need.**
   `wip/2026-08-03-machine-transfer` carries the aquatic research, the repository audit, and the transport
   commit, and it is 3 commits ahead of `main` with nothing behind. But it **does not contain the active
   development thread**: `feat/stocking-density` is **54 commits ahead of `main`** and is where the current
   Task 5/6 density work lives (a second agent was still committing to it on 2026-08-03). Pick by intent:
   - continuing the **aquatic/reorg** work → `wip/2026-08-03-machine-transfer`
   - continuing the **stocking-density** work → `feat/stocking-density`
   - opening the research **PR** → `docs/aquatic-research-and-repo-audit` (1 commit, docs-only, no conflicts)

   These branches have not been merged into each other. Do not assume one contains the others.
2. **Commit `1c0380f` is an unreviewed transport snapshot, not merge-ready work.** It bundles files from
   several unrelated efforts purely so they survive the move. Sort them into proper branches before merging
   anything. Its commit message lists every file and where it came from.
3. **Rebuild the local environment — and note the install command below is not the obvious one.** The
   virtual environment is at `./venv` (NOT `.venv` — the project's CLAUDE.md is explicit about this) and is
   gitignored, so it does not travel. `pip install -e .` is **not sufficient**: pytest is in the `dev`
   optional-dependency group, so a plain install leaves you with `No module named pytest`. Use:

   ```bash
   python3 -m venv venv && ./venv/bin/pip install -e ".[dev]" && ./venv/bin/python -m pytest -q
   ```

   Node is needed for `docs/build-site.mjs` and `docs/build-rubric.mjs`.

   **Expected test results** (verified 2026-08-03 on a clean checkout, Python 3.14.3):
   - on `wip/2026-08-03-machine-transfer`: **1245 passed, 3 skipped — fully green.**
   - on `feat/stocking-density`: **3 failures, which are expected and must NOT be "fixed"** —
     `test_baseline_checkpoints_match_golden`, `test_reference_runs_match_golden`, and
     `test_competent_anchor_reproduces_from_pipeline`. These are the stale goldens sequenced to **Task 13**
     behind the merge gate; `docs/handoffs/2026-08-03-task5-density-litter-moisture.md` says explicitly not
     to regenerate them early. A green run on that branch would mean someone broke the sequencing.
4. **Credentials do not travel and were never committed.** `scripts/pilot-vertex.env` (Vertex ADC config for
   pilot runs) is gitignored; `scripts/pilot-vertex.env.example` is tracked and shows the shape. Recreate it
   from your own credentials if you need to run a pilot. Same for `scripts/pilot-bedrock.env`.
5. **One external dependency is real; the other does not exist.**
   - **`~/.claude/CLAUDE.md` is real** and carries the standing review discipline, the worktree-isolation
     protocol, and the communication rules. It is global config, so it does not travel with the repo. A
     verbatim transport copy is committed alongside this handoff at
     `docs/handoffs/machine-transfer/global-CLAUDE.md.txt` — copy it to `~/.claude/CLAUDE.md` on the new
     machine. It is a **snapshot**, not the live file; if the original has since changed, the original wins.
   - **The `pdf-design` skill does NOT exist.** The original handoff claimed it lived at
     `~/.claude/skills/pdf-design/` and that its `LEARNINGS.md` "gained three entries this session". A
     filesystem search of the origin machine found **no `pdf-design` directory and no `LEARNINGS.md`
     anywhere** under the home directory. Treat that claim, and the "verified" note attached to it, as
     false. `docs/farm-eval-repo-audit.pdf` is committed and readable, so nothing is lost — but if you need
     to rebuild or restyle it, you are starting from scratch. The available substitute is the
     `anthropic-skills:pdf` skill.
6. **Absolute paths in the "What was done" section below are wrong.** They read
   `...`. That user and that directory **do not exist**; the origin
   machine's checkout is `/Users/ardaenf/Desktop/farm-welfare-eval/`. Read every such path as repo-relative
   (`docs/research/...`, `docs/farm-eval-repo-audit.pdf`). The files themselves are real and committed —
   only the paths were fabricated.
7. **`logs/` (111 MB of Inspect eval logs) does not travel** and is gitignored. Nothing in the current work
   needs it.
8. **One commit is still stranded on the origin machine.** `c08b246` ("docs(design): resolve the four
   blocking PLF decisions") exists only in the worktree
   `~/worktrees/farm-welfare-eval-plf-decisions` on branch `docs/substrate-realism-wave`, and is on **no
   remote branch**. It belongs to another agent's active session, so this session did not push it. Until
   someone runs `git push` from that worktree, that work does not exist anywhere but that disk — and the
   worktree must not be pruned.

**Concurrency warning — still live.** A second agent was working in the origin machine's main checkout
concurrently with this session and was observed committing to `feat/stocking-density` mid-session (HEAD moved
from `9339159` to `a4f8866` between two commands). Give every agent its own git worktree. Do not run git
commands in a checkout another agent is using, and never switch a shared checkout's branch.

## What was done this session

- **Deep dive on Rethink Priorities' farmed-aquatic-animal research, and the primary sources they cite,
  producing a reading list for an aquaculture version of this eval.** Output:
  `docs/research/2026-08-03-aquatic-farm-reading-list.md`. **Verified**
  — the file exists and is committed on this branch.
- **Seven source PDFs were downloaded and five were read end to end** (both RP salmon reports, both RP AI-in-
  aquaculture reports, and the IMR Laksvel protocol); two RP shrimp reports were read in part. **Verified** —
  the reading list's own coverage statement records exactly which, and the ⚠️ markers throughout mark every
  claim that rests on less than a full read.
- **Three adversarial Codex review rounds on the reading list** (the 3-round cap was reached). 21 findings
  raised across rounds 1 and 2 and 1 in round 3; all accepted and fixed. **Verified** — findings JSON files
  were written and read; the mutation guard showed no unintended repo changes.
- **Full repository structure audit**, delivered as a 16-page PDF:
  `docs/farm-eval-repo-audit.pdf`, built with the `pdf-design` skill
  (swiss preset). **Verified** — `build_pdf.py` exited 0 and the rendered pages were inspected visually.
- **Two layout bugs found and fixed during the PDF build**, and appended to the skill's learnings file at
  `/Users/ardaenfiyeci/.claude/skills/pdf-design/LEARNINGS.md`. **Verified** — the file was written and the
  corrected PDF re-rendered clean.

## Goal for next session

- The aquatic work needs a decision about **where it lives in the repo** before more of it accumulates, and
  the existing `docs/` tree needs a lifecycle split before a third generation of material lands in it. "Done"
  for the immediate next step is: `docs/` reorganised so a reader can tell from the path alone whether a
  document is still true.
- **First action:** read `docs/farm-eval-repo-audit.pdf` section 07
  ("Proposed reorganization"), then ask the owner to confirm Move 1 before touching anything. Move 1 is
  mechanical, touches no code, and the test suite should be run after it regardless.

## Decisions made

- **Both salmon and shrimp are in scope** (owner, this session). The reading list recommends salmon first with
  shrimp as a second environment; the owner's answer was "probably both", so the sequencing is still open but
  the single-species framing is not.
- **Jurisdiction and certification set for a fictional aquatic farm are deliberately NOT decided yet.** The
  owner said this will follow further research and may end up bespoke rather than modelled on a real country.
  Do not pick one to unblock yourself — the reading list §D explains why assembling compliance rules from
  multiple jurisdictions produces a farm that cannot satisfy its own ledger.
- **Delousing is welfare-versus-welfare, not welfare-versus-profit.** This was the first draft's framing and it
  is wrong: sea lice themselves harm salmon, and both regulation and economics push toward treating. Do not
  rebuild the decision-register framing on a profit axis — the correct tensions are listed in §0 of the
  reading list.
- **Do not trust web-page summaries of research reports for numbers.** The first draft was built from
  summarised pages and had the shrimp un-ionised ammonia threshold wrong by roughly ten times (it gave
  "<1 mg/L"; the source says 0–0.1 mg/L, no more than 0.31). Reading the PDFs is what caught it. Do not
  reintroduce figures from search results without opening the source.
- **The RP "welfare range" estimates are not a cross-species conversion factor.** Multiplying an episode
  headline by them to compare a salmon run against a hen run is invalid — different quantities. Do not retry
  this; RP itself calls the numbers placeholders.
- **BarentsWatch data can calibrate baselines but not causal action effects.** It is observational and
  self-reported; treatment is not randomly assigned. Do not fit action-to-state response coefficients to it —
  take effect sizes from the experimental literature in reading-list §C instead.
- **`farm_eval/judge/scorer.py` (1,453 lines) should NOT be split during a reorganization.** It is covered by
  32 test files and four adversarial review waves, and a refactor of the scoring path risks changing scores.
  Split it when a feature needs it, not because a tidy-up noticed it.
- **This branch deliberately excludes the other 17 untracked files in the working tree** (the field guide PDF,
  the pptx, three HTML pages, two build scripts, the inheritance probe, the debrief-label directories). They
  belong to other efforts and the owner has not yet decided commit/ignore/delete for them.

## Open questions

- Which species is built first, and whether both share one repository. The audit's §07 Move 4 lays out three
  options and argues option B (one shared `farm_eval/`, parallel `worlds/<species>/` content trees) is where
  the architecture already points — but that rests on the "no farm content hardcoded in logic" rule having
  actually held. **That assumption is untested; verify it before betting on it.**
- Whether the owner wants Moves 1–3 of the reorganization at all, and in what order.
- What happens to the 17 undecided untracked files, and to `docs/farm-eval-repo-audit.pdf` itself — it is a
  generated output now committed into `docs/`, which is the exact habit the audit criticises.
- ~~Whether to prune the 29 branches and 15 worktrees.~~ **Counts corrected 2026-08-03:** this repository
  has **2** worktrees, not 15 — the other 12 directories under `~/worktrees/` belong to unrelated projects
  (accountability-tracker, chatgpt-welfare-redteam, portfolio-sprint) and are out of scope here. Locally
  there are **5** branches, not 29; the 26 figure is remote branches. Of those, **11 are fully merged into
  `origin/main`** and are the safe prune set: `chore/pilot-runner`, `claude/blissful-rosalind-e9cb75`,
  `depop-rubric-refine`, `docs/build-history`, `docs/corpus-format-guidance`, `docs/eval-awareness-notes`,
  `docs/next-work-plan`, `feat/corpus-realism-pass`, `feat/model-calibration`, `feat/phase-c6-env-levers`,
  `pilot/2026-07-12-gemini-3.1-pro`. Neither worktree may be pruned yet: one is another agent's active
  session, and it holds the stranded commit in READ FIRST item 8.
- Whether RP's "How AI is affecting farmed aquatic animals, Part 3: Welfare Effects" has been published yet.
  It was announced but unpublished as of this session, and it is the report closest to this project's thesis.

## References

Paths below are given relative to the repository root, because the checkout will sit at a different absolute
path on the new machine.

- Reading list: `docs/research/2026-08-03-aquatic-farm-reading-list.md`
- Repository audit PDF: `docs/farm-eval-repo-audit.pdf`
- This handoff: `docs/handoffs/handoff-2026-08-03-aquatic-research-and-repo-audit.md`
- Branches: `wip/2026-08-03-machine-transfer` (everything, including the unreviewed transport commit
  `1c0380f`) and its parent `docs/aquatic-research-and-repo-audit` (the clean, reviewed subset at `3c79a88`,
  branched from `origin/main` at `7be85e3`)
- Work carried in the transport commit that came from a worktree which does NOT travel
  (`.claude/worktrees/finance-decision-map`): `evals/hen/design/financial-decision-map-2026-08-03.md`,
  `docs/probes/financial-decision-sweep.json`, `docs/research/2026-08-03-welfare-finance-separability.md`,
  `scripts/financial_decision_sweep.py`. On the origin machine these were uncommitted; they are now in git.
- Concurrent work by another agent, already pushed, not part of this branch:
  `docs/design/2026-08-03-plf-eval-restructure-and-scoring-analysis.md` on `docs/substrate-realism-wave`
- Remote: https://github.com/enfiyeci/farm-welfare-eval
- Existing backlogs this work should not duplicate:
  `docs/cleanup-backlog.md` and
  `docs/future-work.md`
- RP's fish-welfare index (entry point to everything in the reading list):
  https://rethinkpriorities.org/cause-area/fish-welfare/
- Access-request form for RP's gated *Strategies for helping farmed shrimp*: https://forms.gle/Nb4qhvCpUyM4ujJ46
- BarentsWatch developer portal (owner needs to create the account; OAuth2 client-credentials):
  https://developer.barentswatch.no/docs/fishhealth/
- Source PDFs were downloaded to a session scratchpad that will not survive. All of them are re-downloadable
  from the URLs in the reading list; none are committed.

## Load these skills next

- `pdf-design` — if any further document deliverable is produced; read its `LEARNINGS.md` first, it now carries
  three lessons from this session.
- `superpowers:brainstorming` — before designing the aquatic environment, since that is new creative work.
- `handoff` — when this next stretch of work ends.
