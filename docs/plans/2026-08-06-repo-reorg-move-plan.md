# Repo reorganization — the move plan

Eval: cross
Written 2026-08-06 on `chore/repo-reorg` (worktree `~/worktrees/fwe-reorg`). Nothing has moved.

This is the document ruling 13c asks for: *"write the full move plan — per-file destination table
compiled from the six reorg catalogues, batch order, verification gates — as a reviewable document,
and rule on it as a whole before any `git mv` runs."*

**Sources.** Ruling: `docs/decisions/00-RULINGS.md` §§12, 13a–13d (read in full). Evidence: the six
catalogues in `docs/reorg/` (all read in full). Every per-file claim below cites a catalogue section
like `(R5 Finding 4)`, or is marked **[verified in tree]** where I checked the working copy directly
today instead of relying on a catalogue.

---

## 1 · Goal and non-goals

**Goal.** Make "which eval is this document for?" answerable from the path, before dairy, salmon and
shrimp arrive. Documentation for one eval moves under `evals/<species>/`; everything else stays in
`docs/`. Apply ruling 12 in the same pass: shrink `CLAUDE.md` to conventions plus pointers and move
its "Current state" narrative into one committed status doc.

**Non-goals — nothing here touches these.**

- No code moves: `farm_eval/`, `scripts/`, `tests/`, the `docs/` generators (`build-*.py/.mjs/.js`,
  `decisions-*.mjs`).
- No content-root moves: `corpus/`, `schedule/`, `prompts/`, `judge/dimensions/`, `kappa-labels/`,
  `debrief-labels-*`.
- No root-config moves: `config.yml`, `config-smoke.yml`, the four `config-baseline-*.yml`,
  `pyproject.toml`, `CLAUDE.md`, `README.md`, `.gitignore`.
- No scorer, rubric, golden or judge-dimension changes. No deletions. No content rewrites beyond the
  link and pointer edits listed in §6 and the three hand-edits in §5 B5.

---

## 2 · The final tree

```
docs/                                  ← the cross-eval slot (ruling 13b)
  README.md                            ← NEW. The one-sentence rule + what each folder holds
  save-protocol.md                     ← NEW. Ruling 13d verbatim (§3)
  STATUS.md                            ← NEW. What is built, in what state (ruling 12)
  LANES.md                             ← who is working where, right now
  cleanup-backlog.md  lane-prompts.md  other-machine-prompt.md
  judge-validation.md  pilot-debrief-protocol.md  expert-labeling-pack.md
  divergence-protocol.md  future-work.md
  build-deck.js  build-fieldguide.py  build-rubric.mjs  build-site.mjs
  decisions-data.mjs  decisions-extra.mjs
  welfare-decisions.html  field-guide.pdf  inside-the-farm.pptx
  specs/                               ← cross-eval (engine) specs + assets/
  design/v2-game-dynamics/             ← cross-eval elicitation methodology + provenance
  research/                            ← cross-eval research only (4 orphans + governance + aquatic)
  handoffs/                            ← session process records, unchanged
  plans/                               ← empties except live cross-eval items
  reorg/                               ← this plan, the six catalogues, the two prior-art documents
  probes/                              ← code-coupled run artifacts that stay this pass (§5, deferred)

evals/hen/
  design/        what the eval should be: specs, design notes, and decisions/ (the ruling record)
  research/      evidence gathered for the hen eval, incl. sources/ (PDFs and DOCXs)
  nodes/         the decision points themselves: register, rubrics, node audits, schedule audit
  world/         ground truth about the simulated farm: world bible, model params, industry timeline
  judge/         hen-specific scoring methodology and its validation material
  surface/       what the agent or a human sees: playthrough guide, corpus templates, mockups/
  runs/          pilots and their debriefs and analyses
  archive/       dated records that are complete history: finished plans, build history

evals/dairy/
  design/        the dairy framing and programme decisions
  research/      dairy and cross-species-technology research, moved as whole folders
```

**Inner-folder set: `design`, `research`, `nodes`, `world`, `judge`, `surface`, `runs`, `archive`.**
Eight, defined one line each above. `surface/` replaces the catalogues' `play/`: R4 Headline 2 shows
`play/` collides with `farm_eval/play/` (the `PlaySession` machinery), so a reader would look for the
dashboard's design in `evals/hen/play/` and not find it. Applied consistently — `docs/mockups/` lands
in `evals/hen/surface/mockups/`, not `play/mockups/`.

**No `evals/salmon/` or `evals/shrimp/` tree is created in this pass.** Per ruling 13a they exist
only if at least one file lands there, and exactly one file is aquatic —
`2026-08-03-aquatic-farm-reading-list.md` — which covers salmon *and* shrimp and so belongs to
neither eval alone. Under 13b's own rule ("everything else stays in `docs/`") it stays in
`docs/research/`, and gets the C.1 hand-edit there.

**Two folders that do not exist yet and must be created empty of moves in B0:** `docs/README.md`
(ruling 13b requires the rule be written into it — **it does not exist today [verified in tree]**)
and `evals/`.

---

## 3 · The file-save protocol

**Home: a dedicated `docs/save-protocol.md`.** Chosen over `docs/README.md` because the protocol
governs files written anywhere in the repo — including under `evals/` — and burying a repo-wide rule
inside one directory's README makes it invisible to anyone working outside `docs/`. `docs/README.md`,
the root `README.md` and `CLAUDE.md` each carry a one-line pointer to it.

The file's content is ruling 13d verbatim:

> 1. **Every new document gets a `YYYY-MM-DD-` prefix** unless it is a living reference document. The
>    date prefix IS the lifecycle declaration: dated means "true when written; archive when superseded."
> 2. **Living reference documents are a closed, named list** (world bible, model params, decision
>    register, LANES, READMEs). Adding to the list is a deliberate act, never a default.
> 3. **Every document declares its eval in one line at the top**: `Eval: hen | dairy | salmon | shrimp
>    | cross` — greppable, changeable without moving anything, honest about mixed files.
> 4. **Research outputs go to a dated topic folder with a README as the first file** (the existing
>    de facto habit, now written down).
> 5. **No document is written into a folder that has no README** explaining what the folder holds.
> 6. **Session status goes in one committed status doc, never in `CLAUDE.md`** (= ruling 12).

Two operational notes attach to it, not part of the ruled text:

- Rule 2's closed list, as of this pass: `docs/README.md`, `docs/save-protocol.md`, `docs/STATUS.md`,
  `docs/LANES.md`, `evals/hen/world/world-bible.md`, `evals/hen/world/model-params.md`,
  `evals/hen/nodes/decision-register.md`, and the per-folder `README.md` files created in B0.
- Rule 6's status doc is **`docs/STATUS.md`** (new). Boundary against `docs/LANES.md`, stated in both
  files so they cannot drift into each other: **STATUS answers "what is built and in what state";
  LANES answers "who is working where right now."**

---

## 4 · The coupling rule (what decides MOVE vs STAY)

Stated once; the table applies it. A document **MOVES** if every reference to its path is a comment,
docstring or string literal that can be edited in the same commit. A document **STAYS** (deferred to
a later pass) if any one of these is true:

- **(a) A generated *config* would re-emit the old path.** `scripts/gen_corner_briefings.py:82` writes
  a literal `docs/…` string into every regenerated `config-baseline-*.yml`, and those four files must
  never be hand-edited (R6 "Files that STAY AT ROOT"). Catches `docs/future-work.md` and
  `f8-dp18-discoverability-2026-07-12.md`.
- **(b) A script *writes* to the path and cannot be re-run inside the verification gate.** An unverified
  write path fails silently and resurrects the old location on the next run (R3 §C Tier 1 #2–#6).
  Catches the five generated probe JSONs.
- **(c) The path is pinned by a depth-derived root.** `docs/probes/pilot-2026-07-12-artifacts/replay_f1.py:8`
  is `parents[3]` with a comment saying the depth is deliberate, then `os.chdir(ROOT)` and relative
  literals **[verified in tree]**; that script reproduces the canonical 6.804 anchor (R3 Tier 2).
  Catches all three `pilot-*-artifacts/` bundles.

Everything else moves. Read tests as a feature, not an exception: `tests/probe/test_schedule_audit.py:136`
reads `REPO_ROOT / "docs" / "probes" / "schedule-spacing-report.md"` **[verified in tree]** and fails
loudly on a bad move — that is the gate proving itself, so that file moves in a batch of its own.

---

## 5 · Batch plan

Each batch is one reviewable diff and one commit, ending with the **verification gate** of §8. `git mv`
only. Order is lowest-risk-first.

### B0 — create the tree, the READMEs and the protocol. No moves.

Create `evals/hen/{design,research,nodes,world,judge,surface,runs,archive}/`, `evals/dairy/{design,research}/`,
each with a `README.md` (rule 5 requires it before anything lands). Create `docs/README.md` carrying
the 13b rule verbatim, `docs/save-protocol.md` (§3), and `evals/README.md`. Create `docs/STATUS.md` as
an empty-but-headed file; it is filled in B6. Write `evals/hen/runs/README.md` from
`docs/pilot-debrief-protocol.md`'s per-run artifact set, **not** by promoting `docs/probes/README.md`,
which is the eval-awareness instrument index and describes a different thing entirely (R3 §"README does
NOT describe docs/probes/").

Gate: §8 (should be a no-op; it proves the baseline).

### B1 — pure-hen, zero-inbound, zero-coupling files

The lowest-risk set in the pass: files no catalogue found any inbound reference to and no code names.
`docs/design/v2-game-dynamics/depop-node-source-enrichment.md` (R5 Finding 3: "zero inbound, so move
risk is none — the clearest single misfiling"), `docs/plans/c5-node-rubrics.md`,
`docs/research/research-prompts.md`, `docs/build-history.md`, `docs/info-space-design.md`,
`docs/playthrough-guide.md`, plus the zero-inbound plans R4 lists. Full set in the table.

Gate: §8.

### B2 — hen folders that move as units

- `docs/decisions/` → `evals/hen/design/decisions/` **whole** (R5 Finding 4: 28 internal relative links
  survive only if the folder moves as one piece). Rewrite the 7 external inbound in the same commit.
- `docs/pilot/` + `docs/pilot/assets/` → `evals/hen/runs/2026-07-01-pilot/` **together** (R5 Finding 7:
  5 relative image links, plus one out-of-folder inbound to `assets/tool_usage.png`).
- `docs/mockups/` → `evals/hen/surface/mockups/` (R5 Finding 8).
- The dated hen plans and specs, split live-vs-done per the table.
- `docs/handoffs/` **does not move** (R5 Finding 6: 10 of 12 are complete history and the scheme already
  names handoffs as cross-cutting process). Recorded as STAY, not deferred.

Gate: §8, plus a `git log --follow` spot-check on `docs/decisions/00-RULINGS.md` to confirm rename
detection held.

### B3 — the research tree split

`docs/research/` splits three ways. Move whole folders only — R1 D.6 and R2 B7 both say flattening
`2026-07-28-briefing-prior-art/`, `2026-07-28-substrate-realism/`, `2026-08-04-welfare-footprint/`
(including its `sources/` of 8 tracked PDFs), `2026-08-04-dairy-depopulation/`,
`2026-08-04-dairy-trait-pricing/`, `v2-future-tech/` and `2026-08-06-litter-lever-and-ammonia/` breaks
their internal links.

Two sub-steps, because the risk is not uniform:

- **B3a — the stay-put files.** Nothing moves; this step only records and re-verifies that the four
  cross-eval orphans and `2026-08-06-claudemd-governance/` are untouched (ruling 13b's core saving:
  "zero link rewrites"). Fold into B3b's commit if the reviewer prefers one diff.
- **B3b — the hen and dairy moves.** `2026-08-06-litter-lever-and-ammonia/` is the high-risk item:
  `ammonia-calibration-verification.md:184` links `../../../farm_eval/env/model/layers/ammonia.py`,
  the only research→code relative link, and it breaks on **any** depth change including a same-eval
  move (R2 B1). Recompute that hop by hand; do not re-root it mechanically. `plf-foresight/` and
  `v2-future-tech/` move to the same parent so their sibling links survive (R2 B2).

Gate: §8, plus the dangling-link check of §8 restricted to `evals/` and `docs/research/`.

### B4 — dairy files

`docs/design/`'s three dairy documents → `evals/dairy/design/`. This is the batch that empties
`docs/design/` of eval-specific material, so **`docs/LANES.md`'s staffing-lane row must change in the
same commit** (ruling 13b: "required in the same commit as any move") — see B6 for the exact line.

Gate: §8.

### B5 — the hand-edit pass (no `git mv` in this batch)

1. **`2026-08-03-aquatic-farm-reading-list.md` — human editing pass, not find-and-replace.** Its
   mapping table (lines 596–606) and its per-source *"Feeds:"* lines name `docs/world-bible.md`,
   `docs/model-params.md`, `docs/decision-register.md` — the **live hen files** — as its own
   destinations (R1 C.1, ruling 13b rule 2). It means "the world-bible-shaped artefact of the aquatic
   eval." Rewrite those to describe the artefact kind, not a hen path. A path rewriter run before this
   edit silently cements salmon guidance onto hen documents.
2. **Pointer lines for mixed files** (13b rule 1, "never a copy, never a split"): one line in
   `evals/hen/research/README.md` pointing at `evals/dairy/research/v2-future-tech/` for its
   hen-specific rows S8, S9 and the `air-quality-zone-response` registry row (R2 Headline 1); one line
   in `docs/README.md` pointing at `evals/hen/design/decisions/00-RULINGS.md`; one in
   `evals/dairy/design/README.md` pointing back at `docs/design/v2-game-dynamics/`.
   **`heat-balance-and-belt-energy.md` is never split or excerpted** — it carries its own ⛔ erratum
   saying its recommended mapping fails its validation target by 65× (R1 "Provenance hazards", ruling
   13b rule 1).
3. **Fix the 107 broken absolute paths** across 14 files (R1 D.5): `/Users/ardaenfiyeci/Desktop/farm-eval/…`
   — wrong username (`ardaenfiyeci` ≠ `ardaenf`) and wrong repo (`farm-eval` ≠ `farm-welfare-eval`).
   Broken today, but if left they become indistinguishable from breakage this reorg caused. Same pass
   for R4's seven (three handoffs, `2026-08-05-welfare-currency-build.md`, and the hardcoded interpreter
   in `2026-06-27-layer1-anchored-welfare-scoring.md`) and R3 Tier 3's two
   (`rescore_live_f23.py:16`, `scripts/rescore_live_round4.py:34`). Rewrite to repo-relative paths, not
   to this machine's absolute path.

Gate: §8.

### B6 — `CLAUDE.md`, `LANES.md`, and the indexes

1. **Trim `CLAUDE.md` per ruling 12.** Target stated **in bytes, not lines** — R6 Headline 2 shows the
   file already passes a `<200 lines` test at 65 lines while being 21,094 bytes **[verified in tree:
   65 lines, 21,094 bytes]**, because single bullets run past 1,500 characters. Nine lines are the
   "Current state" narrative and account for ~14 KB. Move that narrative to `docs/STATUS.md`; leave a
   one-line pointer. **Take the corrected text, not this worktree's copy** — `git diff main -- CLAUDE.md`
   is empty here and the copy still carries the pre-C5-v2 claim that the tripwire gate caps the headline
   to 0.0 (R6 Headline 2). Also fix, while in the file: `farm_eval/env/model.py` (now a package, R6) and
   "11 judge dimensions" (there are 10 — R6 Headline 2, confirmed by `ls judge/dimensions/` **[verified
   in tree: 10 files]**).
2. **Fix the `docs/LANES.md` staffing-lane row** — required by ruling 13b. ⚠️ **The ruling names
   `docs/LANES.md:83`; that line number is stale.** LANES was rewritten after the rulings landed and is
   now 188 lines; the row giving the hen staffing-design lane write-ownership of `docs/design/**` is now
   **line 102** **[verified in tree]**. Target the content, not the number: change its owned paths from
   `docs/design/**, docs/research/**` to `evals/hen/design/**, evals/hen/research/**`. R5 Finding 2 shows
   the re-contamination this prevents is *scheduled*, not merely possible.
3. **Update the READMEs and indexes**: root `README.md`'s two clickable links that 404 on move (lines
   55 and 86, R4 Tier 2) and its four runnable command blocks (R6 Headline 2); `docs/README.md` gains
   the folder map; `docs/LANES.md`'s five references into `docs/decisions/` **[verified in tree: now
   lines 7, 48, 137, 151, 188 — also shifted from R5's recorded 7, 48, 118, 132, 169]**; a README pointer
   to `playthrough-guide.md`, whose §10 is the most accurate account of C5-v2 scoring anywhere in `docs/`
   and which has zero inbound today (R6 "Four docs have ZERO inbound").
4. **Move this plan and the catalogues** to `docs/reorg/` as the permanent process record, and update
   this file's own citations to the post-move paths.

Gate: §8, plus the full dangling-link check of §8 across the whole repo.

---

## 6 · Link-rewrite inventory

**The rule: a moved file's inbound links are rewritten in the same commit as the move.** No batch ends
with a known-dangling pointer. Line numbers below come from the catalogues and **must be re-derived by
grep at execution time** — R5's LANES line numbers had already drifted by 19 lines when I checked today.

| Batch | Link set | Where | Note |
|---|---|---|---|
| B2 | **28 internal `docs/decisions/` links across 9 files** | `README.md`→all nine briefs (36–44); `00-RULINGS`→README + `10-measured-answers`; `01`↔`02`↔`03`; `04`→`07`; `05`→`04`,`03`; `07`→`04`; `08`→`02`,`03`,`05`,`06`,`07` (R5 Finding 4) | **Zero rewrites needed** — they survive untouched because the folder moves whole. This is why it moves whole. |
| B2 | **7 external inbound** to `00-RULINGS.md` / `README.md` / `10-measured-answers.md` | `docs/LANES.md` ×5, `docs/research/2026-08-06-litter-lever-and-ammonia/README.md:37`, `docs/other-machine-prompt.md:57` (R5 Finding 4) | All rewritten in B2's commit. |
| B2 | 5 relative image links + 1 out-of-folder inbound | `docs/pilot/2026-07-02-pilot-run-analysis.md`→`assets/*.png`; `docs/plans/2026-08-04-welfare-currency-and-finance-ledger.md:141`→`assets/tool_usage.png` (R5 Finding 7) | Internal 5 survive (folder moves whole); the 1 external is rewritten. |
| B2 | 1 prose citation in a test | `tests/env/test_body_ref_loud.py:3` names `docs/pilot/2026-07-01-pilot-findings.md` **[verified in tree]** | Prose, not an opened path — the test will not fail — but updated in the same commit (R5 Finding 5). |
| B3 | **R1 D.2 batch — both ends move, in different directions** | `docs/model-params.md:135,213,142` → `](research/…)`; `docs/world-bible.md:287`; `docs/decision-register.md:3,:242` (R1 D.2, R2 B5) | `world-bible`/`model-params`→`world/`, `decision-register`→`nodes/`, targets→`research/`. Re-derive each hop; do not re-root mechanically. **Treat as one batch** (R1 D.2). |
| B3 | The densest inbound cluster: ~20 `../research/…` hrefs | `docs/specs/2026-06-26-farm-eval-v2-design-decisions.md` lines 5, 87, 278, 345 (six on one line), 351–354 (R2 B4; R4 counts 13 relative links, 11 into `../research/`) | The `design/`→`../research/` hop **is preserved by construction** if both ends land under `evals/hen/`. Verify each of the 11 targets is in fact a hen research file that moved; any that stayed needs a rewritten path. |
| B3 | The only research→code relative link | `…/ammonia-calibration-verification.md:184` → `../../../farm_eval/env/model/layers/ammonia.py` and `../params.py` (R2 B1) | Depth changes; recompute by hand. Highest certainty of breakage in the pass. |
| B3 | Sibling link pair | `plf-foresight/…:13,:291` → `../v2-future-tech/findings.md`, plus the path written as prose at `:13` and `:126` (R2 B2) | Both folders move to the same parent, so the link survives; the prose mention still needs editing. |
| B3 | Two-ended dairy link | `docs/design/v2-game-dynamics/catalog-A-priors.md:10` → `../../research/v2-future-tech/node-source-registry.md` (R2 B3) | Source stays in `docs/`, target moves to `evals/dairy/research/`. Must be re-derived. |
| B3 | Comment-only code citations to moved research | `farm_eval/env/model/layers/staffing.py:4`, `farm_eval/env/model/params.py:84`, `tests/env/model/test_cold_thermoregulation.py:2`, `farm_eval/env/model/economics.py:5` (R1 D.1 — **"nothing executable breaks"**) **[all four verified in tree]** | Edit the comments; no behavior change. |
| B3 | Un-greppable references — hand-check | Dairy trait-pricing files cross-reference each other as `01-…` **with a literal ellipsis**; the telemetry file uses bare tags `[T11 🔵]`, `[✅ S21]` indexing into `v2-future-tech/findings.md`; many README pointers are unpathed section refs (R1 D.4) | A tag cannot be grepped. Mitigated by moving both registries to the same tree so the tags stay followable. |
| B4/B6 | The `docs/design/**` ownership line | `docs/LANES.md` line **102** **[verified in tree; ruling says 83]** | Required by ruling 13b in the same commit as the `docs/design/` moves. |
| B6 | `CLAUDE.md` 8 pointers, `README.md` 3 | `CLAUDE.md` lines 9, 13, 44, 45, 48, 49; `README.md` lines 10, 55, 86 (R4 Tier 2) | Lines 55 and 86 are clickable and 404 on GitHub the moment the target moves. |
| B6 | Bare-basename prose refs | `avma:84`→staffing-anchors; `v2-model-parameters.md:7`→disease-compliance; profit-levers↔profit-modeling↔redesign; `industry-realism:137` (R2 B8) | Survive only if each cluster moves as a unit; all four clusters land in `evals/hen/research/` together. |
| B1/B2 | Editable source literals for moved files | `farm_eval/env/vet.py:9`→round3-content-pass-design; `farm_eval/judge/welfare_state.py:28`→eval-design-notes; `farm_eval/env/model/integrate.py:190` + `tests/env/model/test_climate_gauge_reports_daily_peak.py:3`→node-layer-audit; `docs/build-fieldguide.py:2199,2255`→substrate-realism-wave-design; `scripts/financial_lever_map.py:10`; `scripts/analyze_briefing_experiment.py:23`; `tests/env/model/test_layer_litter.py:6`; `tests/corpus/test_agent_identity.py` **[all verified in tree]** | Comments and docstrings only. Edited in the move's commit. |

---

## 7 · Hazard register

Every 🔴 from the six catalogues that touches this pass.

| # | Hazard | Source | Mitigation |
|---|---|---|---|
| H1 | **Aquatic reading list names hen files as its own destinations** — "the sharpest hazard, and it is semantic not mechanical" | R1 C.1; ruling 13b rule 2 | Human editing pass in **B5**, before any path rewriting touches it. It also stays in `docs/research/` (§2), so no mechanical rewriter runs over it at all. |
| H2 | **`heat-balance-and-belt-energy.md` must never be split** — carries a ⛔ erratum that its own recommended mapping fails validation by 65× | R1 "Provenance hazards"; ruling 13b rule 1 | Moves inside `2026-07-28-substrate-realism/` as a whole folder. No excerpting, no section extraction, ever. |
| H3 | **107 already-broken absolute paths** across 14 files (wrong username *and* wrong repo name) | R1 D.5 | Fixed in **B5**, in the same pass, so post-move breakage is attributable. Plus R4's 7 and R3 Tier 3's 2. |
| H4 | **`report.html` untracked and not gitignored at the repo root** — swept into any `git add -A` | R6 | **Out of scope but load-bearing for method:** stage by explicit path, never `git add -A`, in every batch. ⚠️ Not present in this worktree **[verified in tree]**; it exists in the main checkout. Owner item §10.3. |
| H5 | **Stale generated `docs/welfare-decisions.html`** — HTML last committed 2026-06-25; its input `decisions-extra.mjs` edited 2026-07-20. Nothing guards this; there is no `test_rubric_sync.py` equivalent for the deck | R6 Headline 3A | **Out of scope — the generator does not move**, so the reorg neither fixes nor worsens it. Output and generator both STAY. Recorded as a known defect; owner item §10.4. |
| H6 | **`tests/env/test_body_ref_loud.py:3` prose citation** of `docs/pilot/2026-07-01-pilot-findings.md` | R5 Finding 5 | The only code coupling across all 45 of R5's files, and it is prose — the test will not fail. Edited in B2's commit anyway. |
| H7 | **`pilot-*-artifacts/` bundles are path-pinned and reproduce the 6.804 anchor** — `replay_f1.py:8` is `parents[3]` with a comment saying the depth is deliberate, then `os.chdir(ROOT)` and relative literals | R3 Tier 2 **[verified in tree]** | **Deferred — coupling rule (c).** All three bundles STAY in `docs/probes/`. A silent depth break here would corrupt the project's only replayable anchor. |
| H8 | **The pinned rubric snapshot is only half redundant** — `dimensions-2026-07-12/` files 01–06 are byte-identical to live, but `07_realism.md` and `08_eval_awareness.md` differ (round-2 F2/F3 wording the recorded grader outputs were produced under). `load_dimensions()` reads the *directory* | R3 | **Do not prune the six duplicates.** Moot this pass (the bundle stays), but recorded so a later pass does not "clean up" the six. |
| H9 | **`docs/probes/README.md` does not describe `docs/probes/`** — it is the eval-awareness instrument index; only 1 of its 7 instruments lives there | R3 | Do not promote it to any `runs/README.md`. B0 writes a fresh `evals/hen/runs/README.md` from `docs/pilot-debrief-protocol.md`'s artifact set instead. |
| H10 | **Four docs have zero inbound references** | R6 | `playthrough-guide.md` → moves to `evals/hen/surface/` **and gains a README pointer** in B6 (live, high quality, §10 is the best C5-v2 scoring account in the repo). `build-history.md` → `evals/hen/archive/` (historical). `other-machine-prompt.md` → STAY (perishable, cross-machine process). `build-deck.js` → STAY (a generator; code does not move). |
| H11 | **Never hand-move or hand-edit the four `config-baseline-*.yml`** — they are generated, and the next regeneration recreates them at root, giving eight | R6 "Files that STAY AT ROOT" | Coupling rule (a). Configs are excluded from the pass entirely, and the two docs whose paths they embed (`future-work.md`, `f8-dp18-…md`) are deferred rather than moved. |
| H12 | **A competing scheme exists** — `docs/farm-eval-repo-audit.pdf` splits `docs/` by *lifecycle* and rates the per-species split as PREMATURE (its Move 4) | R6 "A COMPETING SCHEME EXISTS" | **Superseded by ruling 13c**, which chose species-with-lifecycle-inside after the owner's "next month will include dairy, salmon, shrimp" input. Its §8 "what not to change" list is honoured in full: `farm_eval/` layout, the test tree's mirroring, `corpus/`'s flat document dirs all stay. The PDF moves to `docs/reorg/` as prior art. |
| H13 | **Two live documents are mid-flight in the files being moved** — `2026-08-05-welfare-currency-build.md` sits at round 2 of a 3-round review cap with 8 unapplied findings and its own "DO NOT EXECUTE YET" banner; `2026-07-29-stocking-density-design.md` is the active item on this worktree's parent branch | R4 "Two things to decide BEFORE moving" #2 | Both move, but the new paths are written into `docs/LANES.md` in the same commit so the next session finds them. The real exposure is a **rename-vs-edit merge conflict** when `feat/stocking-density` lands — owner item §10.1. |
| H14 | **`2026-06-24-farm-welfare-eval-design.md` must not be split**, though it is the most engine-heavy hen document — `CLAUDE.md` cites it by nine section numbers and four other docs cite it by section | R4 Headline 1 | Moves whole to `evals/hen/design/`. Writing the separate engine-architecture doc is a follow-on authoring task, not part of this pass. |
| H15 | **Two files supersede themselves in place** — `2026-07-28-substrate-realism-wave-design.md` (struck-through sections protected only by a header rule) and `2026-08-04-welfare-currency-design.md` (per-section ⚠️ banners plus the author's own partial-read flags on three sources) | R4 "Two files supersede themselves IN PLACE" | Never fragment either; never move a section without its header. `git mv` of the whole file satisfies this by construction — which is another reason the pass is `git mv`-only. |
| H16 | **Checkbox state is useless for deciding what is done** — across 13 plans, checked boxes appear zero times; two in-file status lines are wrong in opposite directions | R4 Headline 3 | The live-vs-archive column in §9 uses R4's verification against artifacts on disk, never checkboxes. |
| H17 | **Stale claims that will mislead once moved** — the v1 spec §10/§16 and `model-calibration-design.md` §7 still say tripwires cap the headline to 0; `CLAUDE.md` says they never do. This staleness has already caused documented harm | R4 "Stale-in-place statements" | **Out of scope — content, not location.** Moving does not make it worse. Logged for the design lanes; `CLAUDE.md`'s own corrected text is used in B6 (see H18). |
| H18 | **This worktree's `CLAUDE.md` is stale** — `git diff main -- CLAUDE.md` is empty and it is older than the copy on `feat/stocking-density`; it still carries the pre-C5-v2 tripwire claim | R6 Headline 2 | B6 takes the corrected text from the newer branch, not from this worktree. |
| H19 | **`judge/dimensions/` is the highest-risk move in the repo** — 6 config keys, a hard-coded `../` hop in `build-rubric.mjs`, 7 test constructions, 6 script defaults (two bare CWD-relative, failing silently), `.gitignore`, 25 docs | R6 Headline 1 | **Out of scope — ruling 13c excludes it.** Recorded in the deferred table §9. Its exclusion removes the single largest breakage surface from this pass. |
| H20 | **The stray label dirs are safe to relocate but gate two different things** — `kappa-labels/` is fully filled authoring QA; the two `debrief-labels-*` are completely unfilled expert forms, direct confirmation the §15 gate has never run | R6 Headline 4 | **Out of scope — ruling 13c excludes them.** Deferred, §9. Note for a later pass: do not collapse the two kinds, and keep the `-14` blank with its filled twin under `pilot-2026-07-14-artifacts/fable-proxy-labels/`. |
| H21 | **R5's own prior-art document carries a coverage caveat** — only 7 of 76 Python files were read end to end in the restructure analysis, and it says "before any file is moved, the ones whose disposition is load-bearing should be opened" | R5 Finding 1 | Satisfied for this pass by the coupling rule: every load-bearing coupling in §4 and §6 was re-verified in the tree today, not taken from the analysis. |

---

## 8 · Verification gates

Stated once. **Every batch ends with all four passing before the commit is made.** Baseline recorded
pre-move per ruling 13c: full suite, exit 0, 3 standing skips.

```sh
cd /Users/ardaenf/worktrees/fwe-reorg
./venv/bin/python -m pytest -q                       # exit 0, 3 standing skips
./venv/bin/python scripts/lint_corpus.py             # 0 findings
./venv/bin/python scripts/check_corpus_consistency.py # 0 findings
```

Plus the dangling-relative-link check — one command, no tooling built:

```sh
cd /Users/ardaenf/worktrees/fwe-reorg && \
grep -rhoE '\]\(([^)#:]+\.(md|json|html|pdf|png|py|yml|mjs|js))\)' docs evals --include='*.md' \
  | sed -E 's/^\]\(//; s/\)$//' | sort -u | while read -r p; do
      [ -e "$p" ] || echo "CHECK: $p"
    done
```

It prints every markdown link target that is not a path relative to the repo root; a link written
relative to its own file shows up here too, so the output is a **review list, not a failure list** —
compare it against the same command's output taken before the batch, and only newly-appearing lines
are the batch's doing. Capture the pre-move baseline once, in B0.

**The pre-move baseline is 63 lines** (run over `docs/` today, before `evals/` exists) **[verified in
tree]** — all of them own-file-relative links that resolve correctly, including R2 B1's
`../../../farm_eval/env/model/layers/ammonia.py` and R2 B3's
`../../research/v2-future-tech/node-source-registry.md`. Those two are the exact links the batches must
re-derive, and their presence in the baseline is how you tell a rewritten hop from a broken one.

Additional discipline, from the owner's standing constraint and §7 H4:

- `git mv` only — never `mv` + `git add`, so rename detection survives.
- **Stage by explicit path. Never `git add -A`** (an untracked `report.html` sits at the root of the
  main checkout and would be swept in).
- Small batches: if a batch's diff does not fit in one review sitting, split it.

---

## 9 · The per-file destination table

Grouped by current directory. **Disposition** is MOVE → destination · STAY · HAND-EDIT · DEFERRED.
"DEFERRED" means the ruling or the coupling rule (§4) keeps it out of *this* pass, not that it is
wrong to move it later. Where a catalogue's proposed destination conflicts with the ruled scheme, the
ruling wins and the row says so.

### 9.1 `docs/research/` — R1 range (41 files)

| Current path | Disposition | Batch | Risk / notes |
|---|---|---|---|
| `2026-07-01-daily-labor-staffing.md` | MOVE → `evals/hen/research/` | B3b | `farm_eval/env/model/layers/staffing.py:4` docstring **[verified]**; inbound `docs/model-params.md:135,213` (R1 D.2) |
| `2026-07-02-staffing-org-structure.md` | MOVE → `evals/hen/research/` | B3b | inbound `docs/model-params.md:142` (R1 D.2) |
| `2026-07-12-web-sweep-eval-awareness-judge.md` | **STAY** `docs/research/` | — | Species-agnostic judge methodology; one of 13b's four genuine orphans — **zero link rewrites** (R1 D.7, ruling 13b) |
| `2026-07-13-financial-realism-web-sweep.md` | MOVE → `evals/hen/research/` | B3b | `farm_eval/env/model/params.py:84` + `tests/env/model/test_cold_thermoregulation.py:2` **[verified]**. ⚠️ Provenance: its cited temperature bands are **not in the cited paper**, and they feed the heat model (R1) — content defect, not a move risk |
| `2026-07-20-depop-welfare-hierarchy.md` | MOVE → `evals/hen/research/` | B3b | Cited **from dairy**: `dairy-depopulation/README.md:9,:38`, `dairy-telemetry-parameters.md:10` (R1 C.3) — cross-tree link, rewrite both ends |
| `2026-07-28-briefing-prior-art/` (2 files) | **STAY** `docs/research/` | — | Briefing methodology, cross-eval orphan (R1 D.7). Moves as a unit *if* ever moved (R1 D.6) |
| `2026-07-28-substrate-realism/` (5 files: README, egg-channel-value, **heat-balance-and-belt-energy**, keel-interventions, vitamin-d3-decision) | MOVE → `evals/hen/research/2026-07-28-substrate-realism/` **whole** | B3b | **H2: never split `heat-balance-and-belt-energy.md`.** ⚠️ `vitamin-d3-decision.md` is binding (spec §2d) and unauditable — all 88 citations are unresolvable tokens (R1) |
| `2026-07-29-stocking-density.md` | MOVE → `evals/hen/research/` | B3b | 🔴 Provenance: §1's central design argument is **not in its cited source** (PMC7070775), and an implementation plan is written against it (R1) |
| `2026-07-29-stocking-density-sources.md` | MOVE → `evals/hen/research/` | B3b | Moves with its sibling (R2 B8 basename-cluster logic) |
| `2026-08-03-aquatic-farm-reading-list.md` | **STAY** `docs/research/` + **HAND-EDIT** | B5 | **H1.** Ruling 13a: salmon/shrimp trees are created only if a file lands; this file spans both, so neither tree is created. R1 proposed `evals/aquatic/research/` — **the ruling's 13b sentence wins** |
| `2026-08-03-citation-integrity-audit.md` | **STAY** `docs/research/` | — | Cross-eval process/quality work; zero inbound; ~40 outbound paths, the densest R1 read (R1 D.7). ⚠️ Its §3c is itself stale (R1) |
| `2026-08-03-dairy-telemetry-parameters.md` | MOVE → `evals/dairy/research/` | B3b | Bare cross-corpus tags `[T11 🔵]`, `[✅ S21]` index into `v2-future-tech/findings.md` — **ungreppable** (R1 D.4); mitigated because both land under `evals/dairy/research/` |
| `2026-08-03-virtual-fencing-parameters.md` | MOVE → `evals/dairy/research/` | B3b | R1 destination table |
| `2026-08-03-welfare-finance-separability.md` | **STAY** `docs/research/` | — | §§4–5 are welfare-score aggregation = cross-eval; one of 13b's four named orphans (R1 D.7, ruling 13b) |
| `2026-08-04-dairy-depopulation/` (6) | MOVE → `evals/dairy/research/…/` **whole** | B3b | Unit move (R1 D.6). Cites hen `2026-07-20-depop-welfare-hierarchy.md` — cross-tree, rewrite. ⚠️ Disagrees with trait-pricing on a number (R1) |
| `2026-08-04-dairy-trait-pricing/` (4) | MOVE → `evals/dairy/research/…/` **whole** | B3b | Unit move. Cross-references siblings as `01-…` **with a literal ellipsis** — a rewriter misses these (R1 D.4) |
| `2026-08-04-welfare-footprint/` (3 md/json + `sources/` 8 PDFs) | MOVE → `evals/hen/research/…/` **whole incl. `sources/`** | B3b | Unit move, ~7.5 MB of tracked PDFs (R1 D.6). ⏰ **Timing:** `pain-track-parameters.json` is loaded by nothing today, but `docs/plans/2026-08-05-welfare-currency-build.md:249` names it — move it **before** that plan executes or the plan is written against a path that changes underneath it (R1 ⏰) |

Also relevant to this range, from R1 D.1: **no `.py`, `.mjs`, `.js`, `.yml`, `.toml` or `.sh` file
loads any of these — the four hits are all comments. "The reorg cannot break a test, a scorer, a task
or a build. It can only break provenance."** Confirmed independently **[verified in tree]**.

### 9.2 `docs/research/` — R2 range (48 present; R2 catalogued 44 — see §11)

| Current path | Disposition | Batch | Risk / notes |
|---|---|---|---|
| `2026-08-05-avma-2026-and-cost-target.md` | MOVE → `evals/hen/research/` | B3b | Part 1 partly superseded by `2026-08-06-aphis-…` (R2 §5); `:84` bare-basename ref to staffing-anchors (R2 B8) — same-cluster move preserves it |
| `2026-08-05-belt-vs-litter-moisture-resolved.md` | MOVE → `evals/hen/research/` | B3b | Self-corrected in place, live (R2 §5) |
| `2026-08-05-footpad-thresholds-for-dp16.md` | MOVE → `evals/hen/research/` | B3b | Partly superseded by `2026-08-06-footpad-pdfs-read-in-full.md`; **no supersession marker on the older file** (R2 §5) |
| `2026-08-05-staffing-and-worker-anchors.md` | MOVE → `evals/hen/research/` | B3b | Partly superseded by `2026-08-06-labour-and-bls-…` (R2 §5) |
| `2026-08-06-aphis-hpai-read-in-full.md` | MOVE → `evals/hen/research/` | B3b | low |
| `2026-08-06-footpad-pdfs-read-in-full.md` | MOVE → `evals/hen/research/` | B3b | low |
| `2026-08-06-labour-and-bls-read-in-full.md` | MOVE → `evals/hen/research/` | B3b | low |
| `2026-08-06-claudemd-governance/` (2) | **STAY** `docs/research/` | — | Repo governance, zero connection to any eval (R2 §"do not fit"; R2 destination said `docs/` — same answer). Intra-folder link at README:52 (R2 B7) — untouched |
| `2026-08-06-litter-lever-and-ammonia/` (**9 files** — README, ammonia-calibration-verification, ammonia-model-semantics, litter-access-dose-response, litter-access-hours-partial, litter-access-welfare-cost, litter-drying-cost-numbers, litter-lever-realism, moisture-to-ammonia-curve) | MOVE → `evals/hen/research/…/` **whole** | B3b | 🔴 **Highest-certainty breakage: R2 B1** — `ammonia-calibration-verification.md:184` links `../../../farm_eval/…`, breaks on **any** depth change. Intra-folder links at README:21–24, realism:98,110, cost:6 (R2 B7) — **do not flatten**. `litter-lever-realism.md` §Q3 is explicitly superseded by `litter-drying-cost-numbers.md`; **do not separate them** (R2 §5). ⚠️ R2 catalogued 5 files here; 4 more landed after (§11). Also inbound from `docs/decisions/00-RULINGS.md` and `…/README.md:37` |
| `plf-foresight/2026-07-20-plf-adoption-baseline.md` | MOVE → `evals/dairy/research/plf-foresight/` | B3b | 🔴 R2 B2 sibling links `../v2-future-tech/findings.md` at `:13`, `:291` + prose at `:13`, `:126`. **Moves to the same parent as `v2-future-tech/` so the sibling hop survives** |
| `v2-future-tech/` (5: README, findings, node-source-registry, raw-claims, sources) | MOVE → `evals/dairy/research/v2-future-tech/` **whole** | B3b | 🔴 R2 B3 two-ended. **Conflict resolved:** R2's destination table splits `node-source-registry.md` out to `evals/dairy/nodes/`; R2's own B7 says all five files carry ~14 intra-folder links and "do not flatten". **B7 wins** — keeping the folder intact costs one taxonomy impurity and saves 14 rewrites. Hen rows S8/S9 + `air-quality-zone-response` get a **pointer line**, never a copy (13b rule 1) |
| `v2-redesign-research.md`, `v2-profit-levers-research.md`, `v2-profit-modeling-research.md`, `v2-disease-compliance-dynamics.md`, `v2-corpus-realism-eval-awareness.md` | MOVE → `evals/hen/research/` | B3b | ⚠️ **The `v2-` prefix is a trap** — these are hen ("v2" = second design iteration); only `v2-future-tech/` is the cross-species sweep. **Sort by content, never by prefix** (R2 §2). B8 basename cluster: profit-levers↔profit-modeling↔redesign move together. `v2-corpus-realism…:127` still says "26 email bodies"; corpus is ~211 (R2 §5) |
| `v2-industry-realism-timeline.md` | MOVE → `evals/hen/world/` | B3b | World ground truth filed as research (R2 §"do not fit" #3); `:137` bare-basename ref (R2 B8) |
| `v2-document-templates.md` | MOVE → `evals/hen/surface/` | B3b | R2 said `evals/hen/play/`; renamed per R4 Headline 2 |
| `v2-judge-validation.md` | MOVE → `evals/hen/judge/` | B3b | Judge material filed as research (R2 §"do not fit" #5). Contains broken absolute paths (R1 D.5) → B5 |
| `v2-model-parameters.md` | MOVE → `evals/hen/world/` | B3b | ⚠️ Not in R2's destination table; assigned here by content match to `v2-industry-realism-timeline.md`. `:7` bare-basename ref to disease-compliance (R2 B8) — both land in `evals/hen/` |
| `welfare-decisions-research.md` | MOVE → `evals/hen/nodes/` | B3b | ⚠️ Not in R2's destination table; assigned by content (the decision-node evidence). Flagged in §11 |
| `SOURCES.md` | MOVE → `evals/hen/research/` | B3b | 🔴 R2: "most-referenced file". Its index covers only the nine `v2-*` files — **no row for any 2026-07 or 2026-08 research**, and several anchors are contradicted by later work. **Keep, but flag: its authority claim outruns its coverage** (R2 §5). Code: `farm_eval/env/model/economics.py:5` **[verified]**; R2 B6 also names `params.py:49` — **not confirmed by my grep** (line 84 cites a different file) |
| `research-prompts.md` | MOVE → `evals/hen/research/` | B1 | Orphan, zero inbound (R2). Gap: its §P3 has **no filed output** in `sources/` |
| `eval-awareness-reduction-notes.md` | MOVE → `evals/hen/research/` | B3b | 7 inbound (R2). ⚠️ `:3,217` name a design-doc path that does not exist and call it "NOT yet written" — actual file is `docs/specs/2026-07-05-eval-awareness-reduction-design.md`; `:115` still says "26 email bodies" (R2 §5) |
| `p7-noise-eval-awareness-litreview.md` | MOVE → `evals/hen/research/` | B3b | Heavy overlap with the previous row, different purpose — **not safe to merge; land them together** (R2 §6) |
| `eval-awareness-measurement-deep-research-prompt.md` | MOVE → `evals/hen/judge/` | B3b | Cross-eval judge methodology with hen anchors; majority hen (13b rule 1) |
| `eval-report-design-deep-research-prompt.md` | **STAY** `docs/research/` | — | Process/reporting, cross-eval (R2 destination: `docs/`) |
| `sources/P1-compliance-context.pdf`, `P2-model-calibration.pdf`, `P4-welfare-decision-brief.md`, `P4-…pdf`, `P5-corpus-realism.pdf` | MOVE → `evals/hen/research/sources/` | B3b | 🔴 **R2 B5 two-ended**: `docs/world-bible.md:287` → `research/sources/P1-…pdf` and `docs/model-params.md:3` → `research/sources/P2-…pdf` use the bare `research/…` form that works only from `docs/`. Both ends move, in different directions. Keep `P4.md` and `P4.pdf` together — one artifact; the `.md` has extraction damage, the PDF retains resolvable URLs (R2 §6) |
| `sources/P6-rubric-anchors.pdf` | MOVE → `evals/hen/judge/` | B3b | Judge material (R2) |
| `sources/P8-eval-awareness-construct-2026-07-15.docx` | MOVE → `evals/hen/judge/` | B3b | Cross-eval methodology but the declared provenance of a hen design doc — majority hen (R2 §"do not fit" #6, 13b rule 1) |
| `sources/P9-eval-report-design-2026-07-15.docx` | **STAY** → `docs/research/sources/` | — | Process/reporting, cross-eval (R2). Requires `docs/research/sources/` to survive with one occupant — acceptable; zero rewrites |

### 9.3 `docs/probes/` — R3 (75 files)

R3 is the most code-coupled directory in the pass. **54 of 75 files are DEFERRED under coupling rule
§4(b)/(c); 21 move.** This is a deliberate reading of ruling 13c's "code and code-coupled content do
not move" as covering content coupled *to* code by path — owner item §10.2.

| Current path | Disposition | Batch | Risk / notes |
|---|---|---|---|
| `pilot-2026-07-12-artifacts/` (**27 files** incl. the `.eval`, `dimensions-2026-07-12/` ×8, `replay_f1.py`, `nodes_data.py`, `build_report_v2.py`, `report_theme.py`, `rescore_live_f23.py`, 6 JSONs, `dp-table.md`, `harvest.txt`, `reply-recon.md`, `ws4-ws6.txt`, `score.json`, the PDF) | **DEFERRED** — STAY | — | 🔴 **H7, coupling rule (c).** `replay_f1.py:8` `parents[3]` + `os.chdir(ROOT)` + relative literals **[verified]**; it reproduces **6.803790995188118**, and `rescore-f1-replay.json` **is** the 6.804 anchor the round-4 plan says must never be rewritten. Also `emitter.py:113-114`, `scripts/spectate.py:15`, `tests/spectator/test_server.py:490` **[verified]**. **Moves as ONE unit or not at all** (R3). H8: do not prune the six duplicate dimension files |
| `pilot-2026-07-14-artifacts/` (**12 files** incl. the `.eval`, `all-emails.md`, `fable-proxy-labels/…yml`, 3 JSONs, `proxy-validation-report.md`) | **DEFERRED** — STAY | — | `emitter.py:113` measures its ordering contract on this log (6 recorded-order inversions) **[verified]**. Its regrade is one of two banked Spearman transcripts. R3 rates `proxy-validation-report.md` archivable (every cell `nan`/`NA`) — deferred with the bundle |
| `pilot-2026-07-15-artifacts/` (**7 files**) | **DEFERRED** — STAY | — | `tests/report/test_extract.py:21` builds this path **[verified]**; the `.eval` is gitignored and absent so the test **skips** — a wrong path there would fail *silently forever* (R3 Tier 4). `tests/judge/test_quote_validation_round3.py:2` names `sample00_epoch1_id1_score.json` **[verified]** |
| `inheritance-probe-2026-07-31/` (5) | MOVE → `docs/research/2026-07-31-inheritance-probe/` | B3b | **Not a run of this eval** — layer hens *and Pekin ducks*, a candidate v3 design; self-critical, 18/18 refused, states it did not instantiate its own hypothesis (R3 Misfits). R3 proposed `studies/`; under 13b cross-eval material stays in `docs/`. Its two `.py` are **self-locating** (`Path(__file__).parent`) — R3 calls this "the move-safe pattern to copy" |
| `schedule-spacing-report.md` | MOVE → `evals/hen/nodes/` | B2 | 🔴 **The only file whose move causes a hard, visible pytest failure** — `tests/probe/test_schedule_audit.py:136` and `scripts/audit_schedule.py:21` **[both verified]**. Two editable literals. Moved in a batch of its own so the gate demonstrably catches it |
| `pilot-history.json` | **DEFERRED** — STAY | — | Coupling rule (b): `scripts/gen_pilot_report.py:17` **reads and writes** it **[verified]**; re-running needs a log |
| `financial-decision-sweep.json` | **DEFERRED** — STAY | — | Coupling rule (b): write target, `scripts/financial_decision_sweep.py` (R3 §C #4) |
| `financial-lever-map-data.json` | **DEFERRED** — STAY | — | Coupling rule (b): `scripts/financial_lever_map.py:121` write **[verified]** |
| `round4-judge-wave-rescore-2026-07-15.json` | **DEFERRED** — STAY | — | Coupling rule (b): `scripts/rescore_live_round4.py:95` write, relative after `os.chdir` **[verified]** |
| `f8-dp18-discoverability-2026-07-12.md` | **DEFERRED** — STAY | — | Coupling rule (a): named in `config.yml:26`, all four `config-baseline-*.yml:30` and `schedule/events.yml:643` **[verified]**; the baselines are generated, so the comment cannot be hand-fixed |
| `round4-judge-wave-rescore-2026-07-15.md` | MOVE → `evals/hen/judge/` | B2 | Prose companion to the deferred JSON; add a pointer line to the JSON's unchanged path |
| `node-layer-audit-2026-07-29.md` | MOVE → `evals/hen/nodes/` | B2 | `farm_eval/env/model/integrate.py:190` + `tests/env/model/test_climate_gauge_reports_daily_peak.py:3` **[both verified]** — comments, editable. **N17 is the sharpest conclusion in the directory: welfare optimum and profit optimum are the same point** (R3) |
| `eval-awareness-briefing-experiment-2026-07-15.md` | MOVE → `docs/research/` | B3b | A designed but **unrun** controlled experiment (R3 Misfits → `studies/`; 13b routes cross-eval to `docs/`). `scripts/analyze_briefing_experiment.py:23` docstring **[verified]**, editable |
| `financial-decision-map-2026-08-03.md` | MOVE → `evals/hen/design/` | B2 | Analysis of the **substrate's economics**, not evidence from a run — "filing under `runs/` would be a category error" (R3). Its two JSONs stay (rule b), so it gains a pointer line. Headline: welfare and money are **not** in conflict in the current substrate |
| `substrate-realism-audit-2026-07-28.md` | MOVE → `evals/hen/runs/` | B2 | **F8: only 2 of 12 agent levers are live in both dimensions; 5 fully inert** (R3) |
| `dp06-mortality-latency-false-zero-2026-07-28.md` | MOVE → `evals/hen/nodes/` | B2 | Stale in content, live in role: its disposition says treat DP06 as N/A but **DP06 is still enabled** (R3) |
| `detelling-audit-2026-07.md` | MOVE → `evals/hen/surface/` | B2 | Corpus-authoring audit |
| `confirmation-signal-audit-2026-07-13.md` | MOVE → `evals/hen/nodes/` | B2 | low |
| `human-review-2026-07-08.md` | MOVE → `evals/hen/surface/` | B2 | **Doubly-roled** — corpus-authoring input *and* the canonical disposition-table template three docs cite (R3). Rewrite those three inbound. All 7 findings still say `open`; 4/5/7 were addressed by the corpus pass |
| `fable-node-regrade-2026-07-14.md`, `fable-node-regrade-2026-07-15.md` | MOVE → `evals/hen/judge/` | B2 | Candidate Spearman label rows |
| `pilot-debrief-2026-07-12-…md`, `-2026-07-14-…round2.md`, `-2026-07-15-…round3.md` | MOVE → `evals/hen/runs/` | B2 | Debriefs move; their artifact bundles stay. **Each gains a pointer line to its bundle's unchanged path** (13b rule 1: pointer, never a copy) |
| `pilot-report-2026-07-15.narrative.md` | MOVE → `evals/hen/runs/` | B2 | low |
| `pilot-report-2026-07-15-round3.html` | **DEFERRED** — STAY | — | 264 KB tracked build output; R3 rates it archivable, but `scripts/gen_pilot_report.py` regenerates into this directory (rule b) |
| `codex-review-2026-07-12-f1-validator.md`, `codex-rereview-2026-07-12-round2-fixwave.md` | MOVE → `evals/hen/archive/reviews/` | B2 | Reviews of code, not of a run — R3 proposed a `reviews/` tier; realized as a subfolder of `archive/` rather than a ninth top-level folder |
| `README.md` | **STAY** `docs/probes/` | — | **H9** — it is the eval-awareness instrument index, not a description of this folder. Do **not** promote it. Its gating convention ("probe findings before a κ PASS are not actionable") is cited by three docs |

### 9.4 `docs/plans/` + `docs/specs/` — R4 (40 files)

R4's `engine/design/` destinations are **superseded by ruling 13b**: there is no `engine/`; cross-eval
material stays in `docs/`. Recorded per row.

| Current path | Disposition | Batch | Risk / notes |
|---|---|---|---|
| `specs/2026-06-24-farm-welfare-eval-design.md` | MOVE → `evals/hen/design/` **whole** | B2 | **H14 — do not split.** Mixed ~55% engine, but `CLAUDE.md` cites it by **nine** section numbers and four docs cite it by section; splitting breaks all at once, moving whole breaks one path in six places (R4 Headline 1). H17: §10/§16 still say tripwires cap the headline — content defect, not a move risk |
| `specs/2026-06-26-model-calibration-design.md` | MOVE → `evals/hen/design/` | B2 | Mixed ~45% engine; the six layers and all anchors are hen (R4). §7 carries the same stale tripwire claim (H17) |
| `specs/2026-06-26-flock-cop-reads-integrity-design.md` | MOVE → `evals/hen/design/` | B2 | HEN (R4) |
| `specs/2026-07-08-corpus-realism-pass-design.md` | MOVE → `evals/hen/design/` | B2 | HEN (R4) |
| `specs/2026-07-28-substrate-realism-wave-design.md` | MOVE → `evals/hen/design/` | B2 | **H15 — supersedes itself in place**; struck-through sections protected only by a header rule. `docs/build-fieldguide.py:2199,2255` embed it as data values rendered into `field-guide.pdf` **[verified]** — editable, edited in the same commit. 6 inbound |
| `specs/2026-07-29-stocking-density-design.md` | MOVE → `evals/hen/design/` | B2 | **H13** — the active item on this worktree's parent branch; merge-conflict exposure, owner item §10.1 |
| `specs/2026-08-04-welfare-currency-design.md` | MOVE → `evals/hen/design/` | B2 | **H15** — per-section ⚠️ banners plus the author's partial-read flags **must survive verbatim**. **Most-cited plan/spec: 13 inbound** (R4) |
| `specs/2026-06-26-farm-eval-v2-design-decisions.md` | MOVE → `evals/hen/design/` | B3b | **Conflict resolved:** R4 proposed `studies/v2-broadened-scope/`; 13b has no `studies/` and five live docs cite it for decisions the **hen** eval implements — majority hen wins. Its **11 `../research/` links survive by construction** if the targets land in `evals/hen/research/` (design→`../research/` = the same hop as specs→`../research/` today) — **verify each of the 11 targets moved**; moves in B3b so the targets are already in place |
| `specs/2026-07-03-partial-scoring-and-judge-validation-design.md` | **STAY** `docs/specs/` | — | ENGINE ~100% — "a dairy eval reuses it verbatim" (R4). `farm_eval/judge/headline.py:58` cites it **[verified]** — **zero edit needed because it does not move** |
| `specs/2026-07-05-eval-awareness-reduction-design.md` | **STAY** `docs/specs/` | — | ENGINE ~90% (R4). 6 inbound, all satisfied unchanged. ⚠️ It points at `judge/dimensions/07_eval_awareness.md`; that file is now `08_…` **[verified: 10 files, `08_eval_awareness.md`]** — a content fix, not this pass |
| `specs/2026-07-06-playable-dashboard-design.md` | **STAY** `docs/specs/` | — | ENGINE ~95% — **this is the file that forced the `play/`→`surface/` rename** (R4 Headline 2) |
| `specs/2026-08-04-spectator-dashboard-design.md` | **STAY** `docs/specs/` | — | ENGINE ~90% — routes the breed label through `ModelParams.breed_label` so the page hardcodes nothing (R4) |
| `specs/assets/2026-08-04-spectator-dashboard/` (3 HTML) | **STAY** `docs/specs/assets/` | — | Stays with its spec. R4 misfit #7 (`docs/specs/` disappearing) does not arise: four engine specs keep it alive |
| `plans/2026-06-24-harness-scaffold-phase-a.md` | MOVE → `evals/hen/archive/plans/` | B2 | DONE (R4). `CLAUDE.md:13` inbound |
| `plans/2026-06-26-flock-cop-reads.md`, `-model-calibration.md`, `2026-06-27-phase-c1-financial-pnl.md`, `2026-07-02-phase-e-content-validity.md`, `2026-07-10-corpus-realism-pass.md`, `2026-07-15-round4-judge-wave-plan.md`, `2026-08-04-spectator-dashboard.md` | MOVE → `evals/hen/archive/plans/` | B2 | DONE (R4 verified against artifacts). ⚠️ `2026-06-26-model-calibration.md:13` says *"NONE of Tasks 1–19 are implemented"* — **false; the whole package is built** (R4 Headline 3) |
| `plans/2026-06-27-layer1-anchored-welfare-scoring.md`, `-phase-c2-reactive-channels.md`, `-phase-c3-schedule-nodes.md`, `2026-07-03-partial-scoring-and-judge-validation.md`, `2026-07-05-eval-awareness-phase1.md`, `2026-07-06-playable-dashboard.md`, `2026-07-14-round3-content-pass-plan.md` | MOVE → `evals/hen/archive/plans/` | B1 | **Zero inbound** (R4) — the lowest-risk plans. `2026-06-27-layer1-…md` hardcodes an interpreter at the non-existent root → B5 |
| `plans/2026-07-01-phase-c6-env-levers.md` | MOVE → `evals/hen/archive/plans/` | B2 | Reads as unstarted though `docs/build-history.md` logs it complete — **do not use checkboxes** (H16) |
| `plans/2026-07-14-round3-content-pass-design.md` | MOVE → `evals/hen/design/` | B2 | A **design doc filed under plans** (R4 misfit #5). `farm_eval/env/vet.py:9` cites it for the truthfulness rule **[verified]** — editable docstring |
| `plans/2026-07-15-eval-awareness-3axis-rubric-design.md` | MOVE → `evals/hen/judge/` | B2 | Design filed under plans (R4 misfit #5) |
| `plans/2026-07-15-pilot-report-generator-design.md` | MOVE → `evals/hen/runs/` | B2 | Design filed under plans; **its own closing line admits the misfiling** (R4) |
| `plans/2026-07-15-round4-backlog.md` | MOVE → `evals/hen/design/` | B2 | **LIVE** (B1/B2/B3/D1 open). New path written into `docs/LANES.md` in the same commit |
| `plans/2026-08-02-sept10-programme-plan.md` | **STAY** `docs/plans/` | — | **Programme-level and cross-eval** (Track C is the dairy eval); amended, 4 owner questions open. 6 inbound. 13b keeps it in `docs/` |
| `plans/2026-08-04-welfare-currency-and-finance-ledger.md` | MOVE → `evals/hen/design/decisions/` | B2 | **A decision ledger, not a plan** (R4 misfit #4) — lands with `docs/decisions/`. LIVE; **8 inbound cite the current path** — all rewritten in B2. Also holds the one out-of-folder link to `docs/pilot/assets/tool_usage.png` |
| `plans/2026-08-05-welfare-currency-build.md` | MOVE → `evals/hen/design/` | B2 | **H13 — LIVE + BLOCKED**, round 2 of a 3-round cap, 8 unapplied findings, its own banner says *"DO NOT EXECUTE YET"* and warns an implementer would hit defects 1, 2, 4 and 7 immediately. Zero inbound. Cites `/Users/ardaenfiyeci/…` → B5. **Names `pain-track-parameters.json`** at `:249` — R1's ⏰ timing hazard |
| `plans/HANDOFF-c6-execution.md` | MOVE → `docs/handoffs/` | B1 | A handoff filed under plans (R4 misfit #3); `docs/handoffs/` already exists and does not move |
| `plans/c5-node-rubrics.md` | MOVE → `evals/hen/nodes/` | B1 | **Node content, not a plan** (R4 misfit #2) |

R4's "decide before moving" #1 — *the pain module's home decides two documents' homes* — is **moot for
this pass**: `farm_eval/env/model/pain.py` is unbuilt and no code moves, so the welfare-currency spec's
§5.2/§5.7 stay with their document. Revisit when the currency build lands.

### 9.5 `docs/design/`, `decisions/`, `handoffs/`, `pilot/`, `mockups/` — R5 (45 files)

| Current path | Disposition | Batch | Risk / notes |
|---|---|---|---|
| `design/2026-08-03-plf-eval-restructure-and-scoring-analysis.md` | MOVE → `docs/reorg/` | B4 | **H21 / R5 Finding 1 — the prior art for this very pass** (641 lines, 3 Codex rounds, 21 findings). R5 proposed `engine/design/`; **13b has no `engine/`** — it is cross-eval, and `docs/reorg/` is where this pass's record lives. Contains `/Users/ardaenfiyeci/…` paths (it flags this itself at line 305) → B5 |
| `design/2026-08-03-plf-framing-decisions.md` | MOVE → `evals/dairy/design/` | B4 | DAIRY (R5 Finding 3). ⚠️ Its naming line (`evals/plf_dairy/`) **is history — superseded by ruling 13a**; add a one-line note rather than editing the record |
| `design/2026-08-03-programme-and-plf-decisions.md` | MOVE → `evals/dairy/design/` | B4 | DAIRY + programme; supersedes §§2/4a of the row above (R5 Finding 3) |
| `design/2026-08-04-technology-use-catalog.md` | MOVE → `evals/dairy/design/` | B4 | DAIRY, 1,863 lines, entirely cattle. Cited ×4 from `v2-future-tech/` (R2 §1) — **cross-tree link, rewrite both ends**; contains three self-corrections to its own source tags |
| `design/v2-game-dynamics/depop-node-source-enrichment.md` | MOVE → `evals/hen/nodes/` | B1 | **Pure HEN, zero inbound — "the clearest single misfiling in the assignment"** (R5 Finding 3). Corrects a live scoring misconception: the tracker skips judged classes, so `tripwire: true` on the judged `vsd_plus` class is **functionally inert** |
| `design/v2-game-dynamics/` remaining 7 (`catalog-A-priors`, `catalog-B-research-backed`, `comparison`, `future-tech-x-mechanics-priors`, `future-tech-x-mechanics-B-research-backed`, `raw-claims-B`, `raw-claims-ft2`) | **STAY** `docs/design/v2-game-dynamics/` | — | Cross-eval elicitation methodology + provenance; majority cross-eval so the folder stays (13b). `raw-claims-*` are pure provenance — **never edit or prune** (R5 Finding 3). `catalog-A-priors.md:10` is R2 B3's two-ended link → rewritten in B3b |
| `decisions/` — all **13** files (`00-RULINGS`, `01`–`11`, `README`) | MOVE → `evals/hen/design/decisions/` **whole** | B2 | **R5 Finding 4.** 28 internal relative links survive only if it moves as one piece; 7 external inbound rewritten. **No code, test, config or build script references this folder at all.** Leave a `docs/README.md` pointer to `00-RULINGS.md`. ⚠️ Pre-existing dangling refs at `10-measured-answers.md:60,160,161` are **branch divergence, not reorg damage — do not mistake them for it after the move**. `11-irreducible-questions.md` has **no inbound from anywhere** and is not in the README index — add it while there |
| `handoffs/` — 11 files | **STAY** `docs/handoffs/` | — | **R5 Finding 6: "does NOT need to move — the cleanest result in the assignment."** Interpretation stated: a handoff is a *session process record*, so it is cross-eval by function even when its subject is hen. Six of them carry the D.5 broken absolute paths → fixed in place in B5. Live content worth preserving named by R5: the futuristic-dairy founding decisions (with a six-item do-not-retry list), the substrate-realism lever finding, and the stocking-density wake-day and zero-reading traps |
| `handoffs/machine-transfer/global-CLAUDE.md.txt` | **HAND-EDIT / owner** | — | R5: *"does not belong in this repo at all"* — a stale 2026-08-03 snapshot of the global `~/.claude/CLAUDE.md`. **No deletions in this pass**; owner item §10.5 |
| `pilot/2026-07-01-pilot-findings.md` | MOVE → `evals/hen/runs/2026-07-01-pilot/` | B2 | The §15 gate report: Flash 4.27 vs Pro 1.92-**GATED INVALID**; found the eval discriminates on **propensity not capability**; literal `[PLACEHOLDER …]` emails served for 5 scored decisions; verdict NOT freeze-ready. 6 inbound incl. `tests/env/test_body_ref_loud.py:3` (H6) |
| `pilot/2026-07-02-pilot-run-analysis.md` | MOVE → `evals/hen/runs/2026-07-01-pilot/` | B2 | 489 lines, node-by-node on all 23 decisions; 0 inbound. **Must move together with `assets/`** — 5 relative image links (R5 Finding 7) |
| `pilot/assets/` (5 PNGs) | MOVE → `evals/hen/runs/2026-07-01-pilot/assets/` | B2 | `tool_usage.png` has an out-of-folder inbound from the welfare-currency ledger `:141` — rewritten in the same commit |
| `mockups/fms-dashboard-directions.html` | MOVE → `evals/hen/surface/mockups/` | B2 | Self-contained, no external assets; complete history; 2 inbound (a spec and a plan). R5 said `play/mockups/` → renamed per R4 Headline 2 |

### 9.6 Loose `docs/`, repo root, `judge/dimensions/`, label dirs — R6 (66 present; R6 catalogued 64)

| Current path | Disposition | Batch | Risk / notes |
|---|---|---|---|
| `docs/world-bible.md` | MOVE → `evals/hen/world/` | B3b | Living reference. `:287` is R2 B5's two-ended `research/sources/P1…` link. `tests/corpus/test_agent_identity.py` names it **[verified]** — prose, editable |
| `docs/model-params.md` | MOVE → `evals/hen/world/` | B3b | **The most code-coupled doc in the repo — 10 source modules + 2 tests** (R6), all comments **[verified: `test_layer_litter.py:6` among them]**. `:3` and `:135,142,213` are R1 D.2 / R2 B5 two-ended links. High edit churn, zero break risk |
| `docs/decision-register.md` | MOVE → `evals/hen/nodes/` | B3b | Living reference. `:3`, `:242` are two-ended links (R1 D.2). Inbound from `schedule/events.yml:2` (comment) and **`schedule/beat-calendar.md:3` as a relative markdown link `../docs/decision-register.md`** **[verified]** — `schedule/` does not move, so that link is rewritten in place |
| `docs/eval-design-notes.md` | MOVE → `evals/hen/design/` | B2 | `farm_eval/judge/welfare_state.py:28` + 2 tests **[verified]** — comments |
| `docs/financial-lever-map.md` | MOVE → `evals/hen/design/` | B2 | 2 scripts cite it; `scripts/financial_lever_map.py:10` is a docstring **[verified]**, editable. Its data JSON stays (rule b) → pointer line |
| `docs/info-space-design.md` | MOVE → `evals/hen/design/` | B1 | R6: does **not** fit `play/` — it is an information-architecture design note. Zero coupling |
| `docs/playthrough-guide.md` | MOVE → `evals/hen/surface/` | B1 | **Zero inbound today; §10 is the most accurate account of C5-v2 scoring anywhere in `docs/`** — R6 says it should gain a README pointer during the reorg (H10). Correctly says 10 dimensions |
| `docs/build-history.md` | MOVE → `evals/hen/archive/build-history.md` | B1 | Zero inbound; historical. **A durable record R4 relies on for done-vs-live** — keep it findable. Carries D.5 broken paths → B5 |
| `docs/LANES.md` | **STAY** + **HAND-EDIT** | B6 | Living cross-eval index. **Line 102 (not 83) is the `docs/design/**` ownership row [verified]**; ruling 13b requires the fix in the same commit as the `docs/design/` moves. Its 5 references into `docs/decisions/` are now lines 7, 48, 137, 151, 188 **[verified]** |
| `docs/judge-validation.md` | **STAY** `docs/` | — | Cross-eval method with hen anchors — majority method (R6 misfit; 13b rule 1). Also `farm_eval/judge/validation_harness.py:237` **emits the path into a generated report** **[verified]** — staying costs nothing and avoids a generated-output change |
| `docs/pilot-debrief-protocol.md` | **STAY** `docs/` | — | Same class (R6 misfit). **It is the source for the new `evals/hen/runs/README.md`** (R3): it defines the filename pattern and per-run artifact set |
| `docs/expert-labeling-pack.md` | **STAY** `docs/` | — | One workflow with the `debrief-labels-*` dirs, which do not move (R6 misfit) |
| `docs/future-work.md` | **DEFERRED** — STAY | — | **Coupling rule (a): `scripts/gen_corner_briefings.py:82` writes the literal into every regenerated `config-baseline-*.yml` header** **[verified]**. Move it without editing the generator and the next regeneration re-writes a dangling pointer into four root configs (R6). Also cites dairy research by path (R1 C.3) |
| `docs/divergence-protocol.md` | **STAY** `docs/` | — | Cross-eval method; `scripts/diff_pair.py:44` writes the path into output **[verified]** |
| `docs/cleanup-backlog.md` | **STAY** `docs/` | — | Repo cleanup backlog = cross-eval process. ⚠️ Inside R6's scope but **not named individually in its summary** — §11 |
| `docs/lane-prompts.md` | **STAY** `docs/` | — | Session-launch prompts = process. ⚠️ Same caveat as above — §11 |
| `docs/other-machine-prompt.md` | **STAY** `docs/` | — | Perishable, zero inbound (R6 H10); `:57` links into `docs/decisions/` → rewritten in B2 |
| `docs/build-deck.js`, `build-fieldguide.py`, `build-rubric.mjs`, `build-site.mjs`, `decisions-data.mjs`, `decisions-extra.mjs` | **STAY** — code | — | Ruling 13c excludes code. Each is additionally path-brittle: `build-fieldguide.py:34` derives ROOT **two levels up** and all six inputs hang off it; `build-rubric.mjs:21,22` hard-code `../judge/dimensions/` and `../farm_eval/judge/rubric.yml` — **the relative hop must remain exactly one level up**; `build-deck.js:981` writes `inside-the-farm.pptx` **bare to the process CWD** (R6 Headline 3) |
| `docs/welfare-decisions.html` | **STAY** — generated output | — | **H5: stale** — output last committed 2026-06-25, input `decisions-extra.mjs` edited 2026-07-20, and nothing guards it. Its generator writes self-relative, so output and generator stay together |
| `docs/field-guide.pdf` | **STAY** — generated output | — | **Currently unrebuildable**: `build-fieldguide.py`'s input `docs/welfare-nodes.html` does not exist and is gitignored, so `_load_nodes()` raises `SystemExit`. Tracked output, ignored input (R6 Headline 3C) |
| `docs/inside-the-farm.pptx` | **STAY** — generated output | — | No `package.json` anywhere, so `pptxgenjs` is undeclared; content hard-coded inline. Notably **more current on scoring than `CLAUDE.md`** (R6 Headline 3D) |
| `docs/farm-eval-repo-audit.pdf` | MOVE → `docs/reorg/` | B4 | **H12 — the competing lifecycle scheme**, superseded by ruling 13c but kept as prior art beside this plan. No generator in the repo; cannot be regenerated here |
| `CLAUDE.md` | **STAY** + **HAND-EDIT** | B6 | Ruling 12. **65 lines / 21,094 bytes [verified]** — state the target in bytes. 30 files point at it, one from code (`economics.py`) **[verified]**. Fix: `farm_eval/env/model.py` (now a package), "11 judge dimensions" (**10 [verified]**), and take the corrected C5-v2 text from the newer branch (H18) |
| `README.md` | **STAY** + **HAND-EDIT** | B6 | 5 markdown links, two of which 404 on move (lines 55, 86); 4 runnable command blocks a move silently breaks (R4 Tier 2, R6 Headline 2) |
| `pyproject.toml` | **STAY** | — | Three implicit path assumptions: `testpaths=["tests"]`, `pythonpath=["."]`, `packages.find include=["farm_eval*"]` (R6) |
| `config.yml`, `config-smoke.yml` | **STAY** | — | Root-relative resolution baked into `farm_task.py`'s default and a dozen scripts (R6) |
| `config-baseline-*.yml` (4) | **STAY** | — | **H11 — generated. Never move or hand-edit** (R6) |
| `.gitignore` | **STAY** | — | Line 17's comment names `judge/dimensions/*.md`; untouched because that folder does not move |
| `judge/dimensions/` (10 files) | **DEFERRED** | — | **H19 / R6 Headline 1 — the highest-risk move in the repo**, explicitly excluded by ruling 13c. Deferred set below |
| `kappa-labels/` (17) | **DEFERRED** | — | Excluded by ruling 13c. R6 Headline 4: zero code coupling, safe to relocate later; the `*.kappa.yml` **suffix** is load-bearing, the directory name is not; one documented command at `LABELING-GUIDE.md:199` would need updating |
| `debrief-labels-2026-07-14/`, `-2026-07-15/` (1 file each) | **DEFERRED** | — | Excluded by ruling 13c. **Completely unfilled — all 28 `score:` cells `null` in each: direct confirmation the spec §15 judge-validation gate has never been executed** (R6 Headline 4). 1.1 MB of blank forms with duplicate transcripts; R6 rates them deletion candidates. Keep the `-14` blank with its filled twin |

### 9.7 Deferred to a later pass — catalogue recommendations the ruling overrides

| What a catalogue recommended | Where it said so | Why it is deferred |
|---|---|---|
| Move `judge/dimensions/` under `evals/hen/judge/` (or split schema from anchors) | R6 Headline 1, R6 "Other misfits" | Ruling 13c: code-coupled content does not move. Minimum change-set is 6 config values + a hard-coded `../` hop + 7 test constructions + 6 script defaults (two bare CWD-relative, failing **silently**) + `.gitignore` + 25 docs. R6 even supplies the 6-step execution order for whenever it happens |
| Move `kappa-labels/` → `runs/labels/kappa/` and `debrief-labels-*` → `runs/labels/judge-validation/<date>/` | R6 Headline 4 | Ruling 13c excludes them. Note for later: **do not collapse the two kinds** — one gates authoring QA, the other gates welfare science |
| Move `corpus/`, `schedule/`, `prompts/` under `evals/hen/` and introduce `config-hen.yml` | R6 "Files that STAY AT ROOT" | Ruling 13c: "that seam gets its own decision when dairy's substrate is real." R6 notes `config.yml`'s four path values would have to change and `config.yml` becomes hen-specific |
| Create `engine/` (or `engine/design/`) for the four engine specs and the restructure analysis | R4 Headline 1, R5 Finding 1, R3 Misfits | **Ruled out by 13b**: `engine/` "would repeat a defect the audit named" — a top-level directory that looks like a package but holds prose. Those files stay in `docs/` |
| Create `studies/` for the inheritance probe, the unrun briefing experiment, and the v2 spec | R3 Misfits, R4 Headline 1 | 13b routes all cross-eval material to `docs/`; adding `studies/` invents a fifth vague top-level slot for three files. The two cross-eval items land in `docs/research/`; the v2 spec goes to hen by majority |
| Move the three `pilot-*-artifacts/` bundles and the generated probe JSONs into `evals/hen/runs/` | R3 Destinations | Coupling rule §4(b)/(c). `replay_f1.py`'s `parents[3]` would break the 6.804 anchor **silently** |
| Archive `pilot-analysis-gemini-3.1-pro.pdf`, `pilot-report-2026-07-15-round3.html`, `proxy-validation-report.md` | R3 "Safe to archive" | No deletions or archival-by-removal in this pass; two of the three sit inside deferred bundles |
| Delete the blank `debrief-labels-*` sheets; delete `machine-transfer/global-CLAUDE.md.txt` | R6 Headline 4, R5 Finding 6 | No deletions in this pass. Owner items §10.5 |
| Split `v2-future-tech/node-source-registry.md` out to `evals/dairy/nodes/` | R2 Destinations | Overridden by R2's own B7: ~14 intra-folder links; the folder stays intact |
| Fix `docs/probes/README.md` / promote it to `runs/README.md` | R3 | Explicitly rejected (H9). A fresh README is written instead |

---

## 10 · Open items for the owner

1. **Merge order against the in-flight branches.** `2026-07-29-stocking-density-design.md` is the active
   item on `feat/stocking-density`, and `2026-08-05-welfare-currency-build.md` is mid-review-loop (R4).
   `git mv` on this branch plus edits on those produces rename-vs-edit conflicts. I can sequence the
   reorg either way; only you know the branch schedule. **Recommendation: land or park those branches
   first, then merge the reorg.**
2. **Confirm my reading of "code-coupled content does not move."** I read it as covering
   `docs/probes/` artifacts that scripts read, write, or pin by path — which defers 54 of 75 probe
   files (§9.3). The alternative is to move them and edit ~8 scripts and 2 tests. I recommend
   deferring; the 6.804 anchor is not worth the risk of a silent depth break.
3. **`report.html` at the repo root** (main checkout, untracked, not gitignored). Delete it or gitignore
   it? I did neither — it is outside this pass and outside this worktree.
4. **The stale `welfare-decisions.html`** (H5) is 6 weeks behind its inputs with nothing guarding it.
   Regenerating it is a content change, not a move. Want it in this branch, or its own?
5. **Two deletion candidates I did not act on:** `docs/handoffs/machine-transfer/global-CLAUDE.md.txt`
   (R5: "does not belong in this repo at all") and the two blank `debrief-labels-*` sheets (R6: 1.1 MB
   of empty forms, one command to regenerate). Both need a yes from you.

---

## 11 · Coverage and count reconciliation

- **Read end to end this session:** `docs/decisions/00-RULINGS.md` (552 lines) and all six catalogues
  in `docs/reorg/` (144 + 112 + 152 + 144 + 175 + 190 lines). No partial reads among the inputs.
- **Verified directly in the tree** (marked **[verified]** above), not taken from a catalogue: the
  absence of `docs/README.md` and `evals/`; `CLAUDE.md` at 65 lines / 21,094 bytes; 10 files in
  `judge/dimensions/`; `docs/LANES.md` at 188 lines with the `docs/design/**` row at line **102**, not
  83; the five `docs/decisions/` references in LANES now at 7/48/137/151/188; the full grep of
  `farm_eval/`, `scripts/`, `tests/`, `schedule/`, the configs and `.gitignore` for `docs/` paths;
  `replay_f1.py:8`'s `parents[3]` + `os.chdir`; `test_schedule_audit.py:136`; `audit_schedule.py:21`;
  `financial_lever_map.py:121`; the per-directory file counts below.
- **Not verified:** the inbound-reference *counts* and line numbers inside documents (taken from the
  catalogues); the contents of the individual documents being moved — I read the catalogues' records of
  them, not the 309 files themselves.

**Counts.** The catalogues claim **309** candidates; the tree today holds **315** files in the same
scope. Reconciliation:

| Range | Catalogue claim | Present now | Difference |
|---|---|---|---|
| R1 `docs/research/` early | 41 | 41 | — |
| R2 `docs/research/` late | 44 | 48 | **+4**: `2026-08-06-litter-lever-and-ammonia/` holds 9 files; R2's table records 5. All four landed after R2 catalogued, in two waves: `moisture-to-ammonia-curve` (committed 16:42) and `litter-access-hours-partial` (before the handoff) the same afternoon, then the two re-runs `litter-access-dose-response` and `litter-access-welfare-cost` at 21:57 — the rulings' own §1 update describes the re-runs |
| R3 `docs/probes/` | 75 | 75 | — |
| R4 `docs/plans/` + `docs/specs/` | 40 | 40 | — |
| R5 design/decisions/handoffs/pilot/mockups | 45 | 45 | — |
| R6 loose docs + root + judge/dimensions + labels | 64 | 66 | **+2**, unexplained by R6's summary. My enumeration: 27 loose `docs/` + 10 root (incl. `.gitignore`) + 10 `judge/dimensions/` + 17 `kappa-labels/` + 2 `debrief-labels-*`. Most likely R6 excluded `.gitignore` and one other root file from its count |
| **Total** | **309** | **315** | **+6** |

**Rows in the §9 table: 315 files**, covered either individually or as an explicitly-named folder unit
(e.g. `docs/decisions/` = 13 files in one row, `pilot-2026-07-12-artifacts/` = 27 files in one row).
Every file present in the six catalogues' scope has a disposition.

**Not catalogued — needs a decision.** Seven files exist in `docs/` that no catalogue covered, because
they were created by this reorg effort after the readers finished:

| Path | Note |
|---|---|
| `docs/reorg/catalogue-R1…R6.md` (6) | The catalogues themselves. Proposed: **STAY** in `docs/reorg/` as the permanent evidence record |
| `docs/plans/2026-08-06-repo-reorg-move-plan.md` | This file. Proposed: **MOVE → `docs/reorg/`** in B6, with its own citations updated to post-move paths |

Two further files sit inside R6's stated scope but are **not named individually in its summary**:
`docs/cleanup-backlog.md` and `docs/lane-prompts.md`. I assigned both **STAY** on content (cross-eval
process), but they carry no catalogue evidence behind that call.

---

## 12 · Merge ritual

1. **Codex adversarial review of the finished branch before merge** — ruling 13c's standing constraint
   and the owner's standing review rule. Whole-branch grain, not per-batch; run from the repo root with
   `-s read-only`, findings file written outside the repo.
2. Adjudicate findings, one combined fix wave, re-verify by `resume`. Hard cap 3 rounds, then escalate.
3. Merge to `main`, then **push every branch the merge advanced** in the same breath.
4. `git worktree remove ~/worktrees/fwe-reorg` once `git status -s` is empty and
   `git rev-list --count main..chore/repo-reorg` is 0. Never `--force`.
