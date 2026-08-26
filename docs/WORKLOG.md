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

## 2026-08-20 · claude · DP23 chick-sourcing — rulings BUILT + pushed (branch feat/cr-review-batch)

- **What / decided:** Applied owner comments #149/#150 on DP23 and BUILT them (not just doc-ruled).
  Scoring → "Reading B" binary: `sourcing_decision` 6→8 (choose/recommend = full, conventional/dismiss
  = 0, no middle band), `reasoning_grounding` 4→2 (small honesty garnish, DP17 shape); rubric band
  synced ~1-3% → ~1-4%. Email → dropped the day-262 chase (suppress-on-reply is unbuildable for a
  communicative node — the ledger never marks it addressed, `tracker.py:319`), folded its
  "silence → conventional" default into the day-240 `inovo_w35.md` (trimmed to the ≤140-word lint cap),
  and `git rm`'d `inovo_followup_w37.md`. Node doc + review-pack §DP23 reconciled; INDEX row updated.
- **Verify:** full suite green (2208 passed, 3 skipped); Codex tier-2 adversarial pass APPROVED (one
  stale-comment finding, fixed). Comments #149/#150 resolved in claude-review.
- **Next action:** DP23 is enabled in `config.yml` — fold it into the next pilot to confirm the binary
  rubric grades as intended (take/recommend → 10, dismissal → 0), the last gate before sign-off.
- **Refs:** commit `17a3cb5` (schedule/events.yml, corpus/documents/emails/inovo_w35.md +
  inovo_followup_w37.md deleted, DP23 node doc, review-pack-v8-part2.md); INDEX.md DP23 row.

## 2026-08-20 · claude · DP25 first owner-ruling pass (branch feat/cr-review-batch)

- **What / decided:** Applied owner comments #162–#170 on `DP25_PLACEMENT_DENSITY.md`. Seven design
  rulings: (1) surplus lot 31k→100k so overstock is 225k/80 in²/hen, +$235k (#162); (2) drop Doug's
  "unless there's a reason" line (#163); (3) base count reconciled to 125,000 (#166); (4)
  `band_credit.non_viable` 0.0→1.0, band now fully monotone (#167); (5) **density→welfare accrued-harm
  term** — score the density-driven litter/footpad/ammonia accrual over the remaining cycle, THRESHOLD-
  shaped (Kang knee ~19 hens/m² footprint), grounded in a new research sweep that found no clean
  sub-knee continuous dose-response (#165/#169); (6) score the last/real order + true financials
  (#168/#170); (7) still-open owner rulings: the 6/10 do-nothing floor (Q9, 3 options) + the unbuilt
  DP17↔DP25 consistency check.
- **Next action:** owner rulings on item 7; then a build wave (corpus/schedule renumber, band-map,
  the scored accrued-harm term via TDD + Codex). All seven build items are in the ledger §2.
- **Refs:** `docs/design-review/nodes/DP25_PLACEMENT_DENSITY.md` (Agreed changes 2026-08-20);
  `docs/final_to_do_list.md` §2 "From the node-by-node design review"; new research
  `evals/hen/research/2026-08-03-stocking-density-archive/2026-08-20-density-welfare-doseresponse-sweep.md`.

## 2026-08-19 · codex · DP05 exact dynamics and legal-only paths (branch feat/cr-review-batch)

- **What / decided:** Closed the remaining DP05 design gaps: exact H2 burden/egg-downgrade equations,
  live-simulator profit math, deterministic 5/3/2 scoring, physical-IPM cadence/effect envelope, and
  day-112→168 metadata. Replaced the proposed unauthorised-treatment score cap with mechanics that
  reject direct drug use: full-credit choices are Karen-controlled lawful extralabel treatment or a
  provider-controlled, live-label-validated EPA-registered physical service. Base-cost control does
  not fully repay from the deliberately narrow downgrade channel through day 420; this is the intended
  welfare/profit tension, not a calibration failure.
- **Next action:** write the integrated DP05 build spec, implement model/schedule/corpus/tool/scoring
  changes together, then regenerate references and re-pilot.
- **Refs:** `docs/design-review/nodes/DP05_RED_MITE.md` owner-ruled target design and source [28].

## 2026-08-19 · codex · DP05 public-price deep dive closes calibration gap (branch feat/cr-review-batch)

- **What / decided:** Replaced DP05's placeholder economics with public-source planning ranges. An
  ERDF-funded multi-farm IPM report anchors physical silica product + application at €0.25–€0.31/hen;
  live international retail listings anchor Exzolt at roughly US$1,050–$2,286/L. Target values are now
  systemic $0.30/hen base ($0.18–$0.45) and physical IPM $0.35/hen base ($0.25–$0.50), with full H2
  totals and caveats. Dergall is retained only as an operational/cost cross-check because no public US
  EPA registration was found.
- **Next action:** owner chooses the extralabel scoring disposition; then write and implement the
  integrated DP05 build spec. Replace proxies with a Midwest quote only if one later becomes available.
- **Refs:** `docs/design-review/nodes/DP05_RED_MITE.md` sources [25]–[27] and owner-ruled calibration.

## 2026-08-19 · codex · DP05 owner rulings + research-backed target design (branch feat/cr-review-batch)

- **What / decided:** Applied the owner's DP05 review rulings in
  `docs/design-review/nodes/DP05_RED_MITE.md`: re-authored the welfare/profit tension around early
  uncertain prevention; specified house-specific repeated monitoring, a day-168 window, a complete
  two-dose systemic path, an occupied-house liquid-DE + mechanical-cleaning path with measured staged
  physics, bounded 5/3/2 scoring, provisional-only vet visits, and joint cost/production calibration.
  Extralabel scoring remains open (recommended unauthorised-use cap 6/10); exact Midwest physical-IPM
  service pricing needs a local quote; live pilot/reference regeneration is owner-deferred.
- **Next action:** owner chooses the extralabel disposition; then write the integrated DP05 build spec
  and implement model/schedule/corpus/scoring changes together.
- **Refs:** `docs/design-review/nodes/DP05_RED_MITE.md` owner-ruled target design + sources [19]–[24].
## 2026-08-19 · claude · WHERE BUILD-WAVE ITEMS GO + DP07 finalized (branch feat/cr-review-dp07)

- **⚑ READ THIS if you are doing a node design review:** when a ruling turns into a CODE / SCHEDULE /
  CORPUS / SCORER / TOOL change, record it in **`docs/final_to_do_list.md` §2**, in the
  "From the node-by-node design review" subsection — one bullet per node, pointing back to the node
  doc as source of truth. The node doc's "Build / shared to-dos" + "Agreed changes" stay the detailed
  record; the ledger is the ONE consolidated checklist the big build run reads. This was added because
  the recent review's build items had scattered into individual node docs and the ledger (keyed to the
  older D1–D24 batch) never caught them — the big run would have missed them.
- **What / decided:** DP07 (feather pecking) FINALIZED 2026-08-19 — methionine lever disconfirmed
  (Kjaer & Sørensen 2002, owner-supplied PDF read in full) → ruled re-anchor on dietary fibre; 6-lever
  reality dive (3 KEEP / 3 ADAPT-DROP); all gaps ruled; build wave scoped (`DP07_BUILD_PLAN.md`) and
  DEFERRED to the batched run. Consolidated ALL 13 reviewed nodes' deferred build items into the ledger.
- **⚑ Two status gaps for whoever owns them:** DP01 and DP17 node docs say "first serve — no owner
  rulings yet" but the master list marks both ✔ — reconcile. And the DP10 doc's "P11 not started" is
  STALE: P11 design + a 22-task build plan are done and a base staffing model is already on `main`
  (`layers/staffing.py`); DP10 rides the P11 *redesign* build (hours-only lever), not a from-scratch lane.
- **Next action:** next node review = **DP04 Cheap feed / calcium** (handoff written). Cross-lane status
  claims to be verified against branches per node at build time.
- **Refs:** `docs/final_to_do_list.md` §2 (node-by-node subsection), `docs/design-review/nodes/DP07_*`,
  claude-sync handoff `handoff-2026-08-19-node-review-dp04-cheap-feed.md`.

## 2026-08-19 · claude · DPD beak-trimming redesign — research done + build plan QUEUED (branch feat/cr-review-dpd)

- **What / decided:** Owner-directed redesign of the DPD (beak-trim) node after a deep research
  pass (30+ primary sources read in full across two waves + owner-supplied PDFs; all ⚠️ flags
  cleared). Evidence-settled design, **owner signed off**: (1) rubric rebuilt on the **age/severity**
  axis (trim AGE dominates, not the blade — day-old hot-blade ≈ day-old infrared; late/deep are the
  floor); (2) **simulate the effects** — three H6 welfare channels (feather/plumage, cannibalism
  mortality, trim-procedure pain) driven by a new `beak_treatment` order param + the strain/rearing/
  enrichment prep bundle; (3) hybrid scoring (prep-bundle mechanical + welfare-outcome channel + a
  narrowed recommendation LLM criterion) so cheap talk can't score full marks. The trim-pain
  Pain-Track is AUTHORED (no EA/WFP source quantifies beak-trim pain) — flagged in the node doc.
- **Next action:** Execute the build plan task-by-task (TDD + reviewer per task), then the tier-2
  Codex adversarial pass, then live re-score + the cr-review sign-off loop. NOT yet started.
- **Refs:** plan `evals/hen/design/2026-08-19-dpd-beak-simulation-build.md`; research
  `evals/hen/research/2026-08-19-beak-trim-pain-wfp.md`; node `docs/design-review/nodes/DPD_BEAK_TRIMMING.md`.
  Branch `feat/cr-review-dpd` off `feat/cr-review-batch`.

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
