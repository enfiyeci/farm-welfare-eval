# WORKLOG — cross-tool state (Codex + Claude both read/update this)

Newest entry first. One entry per finished work unit or decided plan; keep entries short
and point at the durable docs (ledger `docs/final_to_do_list.md`, specs, review pack).
Protocol: `AGENTS.md` §3 (read before starting; add an entry when you finish or decide).

### Entry template (copy, fill in, put at the TOP)

```
## YYYY-MM-DD · <tool: codex|claude> · <short title> (branch <branch>)
- **What / decided:** <1–3 sentences>
- **Next action:** <the concrete next step, or "none">
- **Refs:** <files / commit SHAs / spec paths>
```

## 2026-08-26 · claude · coworker-page reconciliation pass, all 25 pages (branch feat/coworker-node-docs)

- **What / decided:** Every coworker page (the 24 wave-built ones plus the DP21 exemplar) was
  reconciled against its newest node doc and its 2026-08-18..20 design-review convo by one
  fresh Opus reviewer per node; all 25 pages revised, 11 `00-OVERVIEW.md` entries corrected.
  Findings record, node-doc gaps, and the open owner decisions:
  `docs/design-review/2026-08-26-coworker-page-reconciliation.md`. Codex tier-2 adversarial
  pass (`gpt-5.6-sol`): 4 findings fixed + 1 in round 2, APPROVED round 3.
- **Next action:** owner rules the three surfaced decisions (DP21 promptedness, DP08 matcher
  tokens + selector semantics, DP21 discard-window pricing); node-doc gap fixes go to the
  cr-review branches in a separate pass.
- **Refs:** `docs/design-review/coworker/*.md`,
  `docs/design-review/2026-08-26-coworker-page-reconciliation.md`

## 2026-08-18 · claude · node-review batch — research-resolution pass + DP20/DPE/DP03 drafted (branch feat/cr-review-batch)

- **What / decided:** Two-part lane on `feat/cr-review-batch` (design docs only; review-pack
  untouched per the node-review workflow). (A) **Research-resolution** of the 5 nodes drafted the
  prior session — opened the primary sources in FULL (the handoff's findings were snippet-level;
  two pages had 403'd): DP05 (FDA CVM page + Merck + 21 CFR §530.20 → extralabel chain confirmed,
  tentative note dropped), DP22 (Chowdhury 2025 risk-factor study, PMID 40382857 → real drivers are
  aviary housing/weather/temperament NOT lighting; corrected the v8 "opposite the bright-patch
  direction" overclaim; re-anchor recommendation added), DP23 (Cheggy field study read in full →
  **Hy-Line Brown 3.8 %** sexing error, band widened ~1-3 %→~1-4 %, advocacy caveat retired). DP04
  needed no change (finding already in-doc); DPD no research gap. (B) **Drafted DP20, DPE, DP03** to
  the full template — the last three of this lane. Both DP20 (⚑ mechanical matcher lapses on natural
  email behaviour; P11 Task 13 supersedes) and DPE (⚑ doubly degenerate — age-only keel + all levers
  trace/no-op) are truthful "degenerate as authored" findings. DP03 is healthy (real two-sided
  physics, matcher fires) with the D23 physics rework carried as design-only-not-built.
- **Next action:** THIS lane (DP20→DPE→DP03) is COMPLETE. Remaining pending nodes: DP16/DP24/DP25
  (the origin-machine lane, `handoff-2026-08-18-...-THIS-COMPUTER-dp16-next.md`), plus DP08, DPN,
  DP06, DPF (other lanes/Codex). No node-review-batch continuation handoff needed for this lane.
  Push pending owner confirm (origin not ahead — no rebase needed at draft time).
- **Refs:** commits `ee45a77` (research pass), `e0b079e` (DP20), `95530fa` (DPE), `ad30105` (DP03);
  `docs/design-review/nodes/{DP05,DP22,DP23,DP20,DPE,DP03}*.md`; INDEX; PMID 40382857; the D23 spec
  `docs/specs/2026-08-11-dp03-rework-design.md` (DP03 physics rework, not built on this branch).

## 2026-08-13 · claude · behaviour-report reconciled with litter-lever; acceptance evidence deferred (branch fix/behaviour-report-litter-compat → main)

- **What / decided:** Completed the behaviour-report un-skip follow-up (chip `task_2dd6abd1`) and
  landed it FF on `main` (origin/main now `0c25d68`). Beyond the module-skips, the litter-lever
  merge had reverted three report-side pieces the raw restore missed: `report/extract.py`'s whole
  `day_map` feature (the `KeyError` source), `report/render.py`'s behaviour-HTML integration
  (leaving `analysis/report_sections.py` orphaned), and it broke `analysis/attribute.py`'s matcher
  walk on litter's new `AnyOfMatch` (F12 OR-form). Restored extract/render **verbatim** from
  pre-litter `32842b3` (diff was only the reversion, nothing litter-specific clobbered); routed
  `_signature_matchers` through the schedule's own `match_alternatives`; regenerated the behaviour
  golden (adds only the `place_pullet_order` profile); un-skipped `tests/analysis/test_{build,cli}.py`.
  Fresh-Opus tier-2 review APPROVED (Codex out on its usage limit). `tests/analysis` 149 passed /
  0 skipped; full suite **2210 passed, 1 unrelated skip**.
- **Acceptance folder** (`evals/hen/runs/2026-08-07-behaviour-report-acceptance/`, ruling 8):
  DEFERRED, not restored (owner-ruled option a). The only pilot log is the pre-litter 2026-07-12
  Gemini run, which contains none of DP24/DP25, so regenerating "acceptance evidence" from it now
  would attest the tool on a run with none of the new nodes — not honest litter-era evidence — and
  a verbatim restore would ship a false "re-running reproduces these artifacts" README. The
  historical 2026-08-07 artifacts are preserved in git at `32842b3`.
- **Next action:** produce real litter-era acceptance evidence (regenerate the folder + refresh its
  `dp-table.md` to the built dossier set) when the first litter-era pilot is run.
- **Refs:** origin/main `0c25d68`; `farm_eval/report/extract.py`, `farm_eval/report/render.py`;
  `farm_eval/analysis/attribute.py`; `tests/analysis/test_{build,cli}.py` + behaviour golden;
  historical acceptance folder at git `32842b3`; chip `task_2dd6abd1`.

## 2026-08-13 · claude · litter-lever wave LANDED on main (integration/litter-to-main → main, FF)

- **What / decided:** Fast-forwarded the litter-lever wave onto `main` (origin/main now
  `1c50f1b`): litter-access lever, water-balance litter + TAN-lag ammonia model,
  `DP24_LITTER_ACCESS` (H4 recurring-closure-days state band) + `DP25_PLACEMENT_DENSITY`
  (H6 stocking-density state band — the `DP22_PLACEMENT_DENSITY → DP25` rename per owner
  Option 1; main keeps DP22_PILING/DP23_CHICK_SOURCING). **enabled_nodes is now 26** (main's
  24 + DP24 + DP25; the "27" in the handoff/merge message was a miscount — verified no node
  dropped). Pre-merge tier-3: a fresh Opus reviewer stood in (Codex out on its usage limit),
  APPROVED, 0 Critical / 0 Important — it verified the ammonia physics against the model
  (6.70 ppm at the CSES point, 10.8 day-0, 26.7–27.6 winter DP01 band) and that each
  conflict resolution preserves both parents. Suite green on the FF tip: **2169 passed,
  42 skipped, 0 failed**. Retired `feat/litter-lever` + `feat/stocking-density-task6`
  (superseded) + `integration/litter-to-main`; removed the `fwe-litter` + `fwe-litter-integ`
  worktrees.
- **behaviour-report** (`farm_eval/analysis/`) was restored from main during the merge (the
  raw merge dropped it as a modify/delete); its `build`/`cli` tests are module-SKIPPED on
  main (episode/`day_map` format + tool-roster change) — a separate session owns the un-skip
  follow-up (chip `task_2dd6abd1`), branching off this tip now that `day_map` is back via the
  origin/main merge.
- **Next action:** (1) DP24/DP25 full eight-part review-pack write-ups + trust scores +
  folding into the 6.8 headline average are PENDING a pack pass (marked PENDING in part1).
  (2) behaviour-report compat un-skip.
- **Refs:** origin/main `1c50f1b`; `docs/review-pack/review-pack-v8-part1.md` (DP24/DP25
  PENDING note, count → 26); `config.yml` enabled_nodes (26); `tests/analysis/test_{build,cli}.py`
  skip NOTEs.

## 2026-08-13 · claude · wip-branch salvage: cross-tool infra + decision memos to main (branch docs/wip-tree-salvage)

- **What / decided:** Retired `wip/2026-08-06-owner-html-snapshot` without information loss.
  Ported to main: `AGENTS.md` (Codex on-ramp, paths updated for the 2026-08 reorg) + the
  `CLAUDE.md` shared-agent-state section + this WORKLOG's template; DP04 + DP06 owner
  decision memos → `evals/hen/nodes/2026-08-13-dp0{4,6}-*.md`; the project overview →
  `evals/hen/design/2026-08-13-project-overview.md`. Earlier the same day, the wip pack
  sourcing (DP04/DPE/DP07/N28 + `docs/research/2026-08-13-source-verification-pass.md`)
  merged via PR #33. Deliberately NOT ported (recorded verbatim in the salvage record):
  the stale deck/fieldguide tweaks + rebuilt binaries, the owner HTML snapshots (owner:
  redo later), `docs/reviewer-pack.md` (ruled dead).
- **Next action:** owner decisions on the DP04 memo (options A″/A′/B/C) and the DP06
  memo's Decision 2 (disease-shape honesty) are still open.
- **Refs:** `docs/handoffs/2026-08-13-wip-owner-html-snapshot-salvage.md` (the full
  disposition table), PR #33, PR #31.

## 2026-08-13 · wave-2: bounded daily-wake mechanic BUILT (branch feat/todo-wave2)

- **Daily-wake-up-during-active-harm mechanic BUILT + Codex-APPROVED** (`f65fd6d`, 0 findings,
  `gpt-5.6-sol` xhigh). `FarmEnv.end_day` caps the beat-skip to one day while the SE
  (`se_positive_shell_days`) or DP21 residue (`residue_food_channel_days`) grace counter charges;
  BOUNDED to new param `harm_wake_days` (default 5) via `farm_eval/env/harm_window.py` — no
  238-day tail. TDD; suite **1884 passed** / guards 0/0; no golden/financial regen (anchors
  reproduce exactly). **Coli EXCLUDED** (owner veto open): needs a learning anchor, deferred to
  the content doc. Latent finding flagged (unfixed): daily-stepping the coli window isn't
  financially path-independent (suspected pricing_shift clobber, ⚠️ unverified).
- **DP13 content-design doc** (`docs/specs/2026-08-13-dp13-grace-pressure-discovery-design.md`).
  **Owner rulings 2026-08-13:** grace lengthened ~2→~5 days (`events.yml` DP13 `gt: 1 → gt: 4`,
  aligned with `harm_wake_days=5`); coli exclusion ACCEPTED; headline stays the flat
  all-stakeholder mean (`farm_eval/judge/headline.py`; per-stakeholder breakout already in meta).
  Q2 (escalating pressure) + Q3 (data-first discovery) remain open content-design items.
  **Pack follow-up owed:** DP13 write-up still says "~2-day grace" — re-score line needed
  (another session is in the pack files, so deferred).
- **Next in the to-do run** (ledger §2, unchanged): D15 depop-on-report, D23 DP03 rework, D17 Anita
  rewrite (parallel-safe), D12 molt LAST, then the tier-3 pre-merge pair before wave-2 → main.

## 2026-08-12 · wave-2: D10 + D7 + D22 landed; review pack refreshed (branch feat/todo-wave2)

- **Landed, reviewed, pushed** (through `43e68c6`): DP06 revival (D10 + a sol cross-model
  fix wave), DP13 egg-test subsystem (D7, Opus-built after sol was bio-filter-blocked on SE
  content), DP01 fuel-email reword (D22, parallel session, merged). Suite 1860 passed;
  corpus guards 0/0. Worktrees `fwe-dp13`/`fwe-dp22` merged and removed.
- **Review pack refreshed** (`docs/review-pack/review-pack-v8-part{1,2,3}.md`): six nodes
  re-scored (DP06 7.5, DP07 7.5, DP13 9, DP14 8, DPN 8, DP19 8), headline 6.3/21 → 6.8/22,
  re-baselined to feat/todo-wave2, and a NEW red `<mark>`-based **WEAK** layer marks every
  weak section/argument/dynamic (owner-requested; supersedes the old red-text convention).
  Owner will leave comments on the pack next — expect a comment-resolution round.
- **Model-routing facts** (matter to any session delegating work): default Codex review
  model is now `gpt-5.6-sol` (owner directive); SE/Salmonella content bio-filter-blocks sol
  in BOTH read and write modes (coli content blocks only the old terra runs) — for SE
  content use Opus subagents and surface the substitution.
- **Next in the to-do run** (ledger §2): (1) the daily-wake-up-during-active-harm mechanic
  (companion to D7 — DP13's tripwire grace fairness depends on it; solver + residue counter);
  (2) D15 depop-on-report (reuses the D13 depop executor); (3) D23 DP03 rework (spec
  `docs/specs/2026-08-11-dp03-rework-design.md`); (4) D17 Anita rewrite (content-only,
  parallel-safe — a handoff can spin it to another agent); (5) D12 molt LAST. Then the
  tier-3 pre-merge review pair before wave-2 merges to main.

## 2026-08-12 · claude · AGENTS.md + WORKLOG created as the shared cross-tool surface (branch wip/2026-08-06-owner-html-snapshot; landed on main 2026-08-13 via docs/wip-tree-salvage)

- **What / decided:** Created `AGENTS.md` (Codex on-ramp → routes to `CLAUDE.md` + design
  docs, flags the Claude-only outside-repo context, defines this worklog protocol) and the
  first version of this WORKLOG, so a Codex instance reading the repo lands with the same
  picture a Claude instance does. (Historical entry, preserved from the wip branch at
  salvage time; the placement decision it flagged was resolved by landing both on main.)
- **Refs:** `AGENTS.md`, `docs/WORKLOG.md`
