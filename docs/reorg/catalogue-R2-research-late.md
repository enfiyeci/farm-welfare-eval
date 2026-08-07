# Reorg catalogue R2 — `docs/research/` from `2026-08-05-avma…` to end (44 files)

Reader R2, 2026-08-06. Nothing was moved, edited or deleted. Coverage statement at the end; ⚠️ flags
are the reader's own.

## Coverage (counts reconcile)

**44 assigned · 37 read in full · 7 catalogued as artifacts (not read) · 0 unopenable.**
Artifacts not read: `sources/P1-compliance-context.pdf`, `P2-model-calibration.pdf`,
`P4-welfare-decision-brief.pdf`, `P5-corpus-realism.pdf`, `P6-rubric-anchors.pdf`,
`P8-eval-awareness-construct-2026-07-15.docx`, `P9-eval-report-design-2026-07-15.docx` — type, size,
page count and embedded title recorded; contents inferred from consumers, not from the artifact.

⚠️ `docs/research/2026-08-03-citation-integrity-audit.md` is NOT in R2's assignment and was NOT read;
four of its lines are cited as grep output only. Verify before relying.
⚠️ `P1-compliance-context.pdf` page count contested between tools (`file` says 8, Spotlight says 6).
⚠️ Inbound greps covered md/py/yml/yaml/mjs/js/html/toml/json only — shell scripts, `.txt`, notebooks
and binaries were not searched.

## Headline findings

### 1. Cross-eval contamination confirmed
`v2-future-tech/` (5 files) and `plf-foresight/` (1 file) are **not hen research** — virtual fencing
(cattle/sheep), robotic milking, pig PLF, salmon/shrimp. `v2-future-tech/findings.md:65-69` says so
itself: virtual fencing is cattle/sheep while "the current eval is a **cage-free layer** farm." Their
consumers are the **dairy** lane (`docs/design/2026-08-04-technology-use-catalog.md` ×4,
`docs/design/v2-game-dynamics/catalog-A-priors.md`, the futuristic-dairy handoff,
`2026-08-03-dairy-telemetry-parameters.md`).

**But they are not cleanly dairy either.** `v2-future-tech/sources.md` rows S8 (NH₃/PM sensing in a
commercial cage-free aviary) and S9 (cage-free floor-egg computer vision) are hen-specific and cited
from the hen side. `node-source-registry.md`'s `air-quality-zone-response` row "bridges v1 mechanics
to v2 sensing" — a hen node. **A clean per-eval split orphans hen-relevant rows.** Needs an owner
decision: shared foresight location, or split the rows.

### 2. ⚠️ The `v2-` prefix is a TRAP — do not split on it
Eight `v2-*` files are **hen** ("v2" = the second design iteration of the layer eval). Only
`v2-future-tech/` is the cross-species sweep. Sorting by prefix would either misfile the sweep into
hen, or drag eight hen files into dairy. **Sort by content.**

### 3. Roughly a third of the assignment is not research under the scheme's own definitions
`docs/research/` has operated as a catch-all for anything a research pass produced.

### 4. What would BREAK if these files move

| # | Break | Where | Why |
|---|---|---|---|
| **B1** | Research → **code**, depth 3 | `2026-08-06-litter-lever-and-ammonia/ammonia-calibration-verification.md:184` links `../../../farm_eval/env/model/layers/ammonia.py` and `../params.py` | Only research→code relative link. Breaks on **any** depth change, including a same-eval move. Highest certainty. |
| **B2** | `plf-foresight` → `v2-future-tech` sibling | `plf-foresight/…:13` and `:291`, both `../v2-future-tech/findings.md` | Siblings today; the reorg may send them to different destinations. Also names the path as prose at :13 and :126. |
| **B3** | Dairy design → v2-future-tech, depth 2 | `docs/design/v2-game-dynamics/catalog-A-priors.md:10` → `../../research/v2-future-tech/node-source-registry.md` | **Two-ended** move; must be re-derived, not re-rooted. |
| **B4** | Spec → nine research files | `docs/specs/2026-06-26-farm-eval-v2-design-decisions.md` lines 5, 87, 278, 345 (six links on one line), 351–354 | Densest inbound cluster: ~20 `../research/…` hrefs. |
| **B5** | `docs/`-root → research, depth 0 | `docs/world-bible.md:287` → `research/sources/P1-…pdf`; `docs/model-params.md:3` → `research/sources/P2-…pdf`; `docs/decision-register.md:3` and `:242` | Bare `research/…` form works only from `docs/`. **Both ends move.** |
| **B6** | Stale path strings in Python | `farm_eval/env/model/economics.py:5`, `farm_eval/env/model/params.py:49` — both cite `docs/research/SOURCES.md` | **Not functional** — no code opens them. Misleading comments after the move. |
| **B7** | Intra-folder links (safe only if folders move whole) | claudemd-governance README:52; litter-lever README:21-24 + realism:98,110 + cost:6; all five `v2-future-tech/*.md` (~14 links) | **Do not flatten these three folders.** |
| **B8** | Bare-basename prose refs | avma:84→staffing-anchors; `v2-model-parameters.md:7`→disease-compliance; profit-levers↔profit-modeling↔redesign; industry-realism:137 | Survive only if each cluster moves as a unit. |

**Nothing in `config.yml`, `pyproject.toml`, `tests/`, `scripts/`, `corpus/`, `schedule/` or any build
script reads any assigned file. Functional break risk = ZERO; documentation-link risk is real and
concentrated in B1–B5.**

### 5. Supersession (all within two days, no marker on the older file)
- `2026-08-05-footpad-thresholds-for-dp16.md` → partly superseded by `2026-08-06-footpad-pdfs-read-in-full.md` (Volkmann now read: contains **no** moisture dose-response; attribution corrected to Wang, Ekstrand & Svedberg).
- `2026-08-05-staffing-and-worker-anchors.md` → partly superseded by `2026-08-06-labour-and-bls-read-in-full.md` (the per-year-vs-per-cycle ambiguity resolved).
- `2026-08-05-avma-2026-and-cost-target.md` Part 1 → partly superseded by `2026-08-06-aphis-hpai-read-in-full.md` (median 51.3 h depopulation).
- `litter-lever-realism.md` §Q3 → explicitly superseded by `litter-drying-cost-numbers.md` (stated in both; **do not separate them**).
- `2026-08-05-belt-vs-litter-moisture-resolved.md` — self-corrected in place, live.
- **`SOURCES.md` is the stalest live file.** Its index lists only the nine `v2-*` files — **no row for any 2026-07 or 2026-08 research**. Several anchors contradicted by later work (line 63 litter→FPD optimum; line 51 AVMA tiers; line 69 footpad mid-30s). It advertises itself as the master register and is cited as such. **Keep, but flag: its authority claim outruns its coverage.**

Stale pointers: `eval-awareness-reduction-notes.md:3,217` names a design doc path that does not exist
(actual: `docs/specs/2026-07-05-eval-awareness-reduction-design.md`) and calls it "NOT yet written".
`v2-corpus-realism-eval-awareness.md:127` and `eval-awareness-reduction-notes.md:115` still say "26
email bodies"; the corpus is now ~211.

### 6. Duplicates and gaps
- `sources/P4-welfare-decision-brief.md` vs `.pdf` — same document; the `.md` has extraction damage (dead `sandbox:/mnt/data/P4.md` link, unresolvable `citeturn…` markers), the **PDF retains resolvable URLs**. Keep both; they are one artifact.
- `p7-noise-eval-awareness-litreview.md` vs `eval-awareness-reduction-notes.md` — heavy overlap, different purposes. Not safe to merge; should land together.
- **Gap:** `research-prompts.md` §P3 (economic realism) has **no filed output** in `sources/`.

## Destinations

| File(s) | Domain | Scope | Destination | Risk |
|---|---|---|---|---|
| `2026-08-05-avma…`, `-belt-vs-litter…`, `-footpad-thresholds…`, `-staffing-and-worker…`, `2026-08-06-aphis…`, `-footpad-pdfs…`, `-labour-and-bls…` | research | hen | `evals/hen/research/` | low–none |
| `2026-08-06-claudemd-governance/` (2) | **process** | **cross-eval — not eval content at all** | **`docs/`** | low (move whole) |
| `2026-08-06-litter-lever-and-ammonia/` (5) | research | hen | `evals/hen/research/` | **HIGH** (B1 in `ammonia-calibration-verification.md`) |
| `plf-foresight/` (1) | research | **dairy-dominant** | `evals/dairy/research/` or shared | **HIGH** (B2 + 4 inbound from a moving doc) |
| `v2-future-tech/README, findings, raw-claims, sources` | research | **cross-eval, dairy-dominant** | `evals/dairy/research/` (+ hen pointer for S8/S9) | **HIGH** (B2/B3) |
| `v2-future-tech/node-source-registry.md` | **nodes, not research** | dairy-dominant, 1 hen row | `evals/dairy/nodes/` | **HIGH** (B3 two-ended) |
| `v2-redesign`, `v2-profit-levers`, `v2-profit-modeling`, `v2-disease-compliance`, `v2-corpus-realism` | research | **hen** | `evals/hen/research/` | medium (B4/B8) |
| `v2-industry-realism-timeline.md` | **world**, filed as research | hen | `evals/hen/world/` | medium |
| `v2-document-templates.md` | **play** (corpus authoring), filed as research | hen | `evals/hen/play/` | medium |
| `v2-judge-validation.md` | **judge**, filed as research | hen | `evals/hen/judge/` | medium |
| `SOURCES.md` | research index | hen (legend inherited cross-eval) | `evals/hen/research/` | **HIGH** — most-referenced file; only two Python mentions (B6) |
| `research-prompts.md` | process | hen | `evals/hen/research/` | none (orphan) |
| `eval-awareness-measurement-…-prompt.md` | **judge** methodology | cross-eval | `evals/hen/judge/` or shared | low |
| `eval-report-design-…-prompt.md` | process/reporting | cross-eval | `docs/` | low |
| `eval-awareness-reduction-notes.md` | research/process | hen | `evals/hen/research/` or `studies/` | medium (7 inbound) |
| `p7-noise-eval-awareness-litreview.md` | research | hen | `evals/hen/research/` | low |
| `sources/P1, P2, P4.md, P4.pdf, P5` | research artifacts | hen | `evals/hen/research/sources/` | **HIGH for P1/P2** (B5 live links from world-bible/model-params) |
| `sources/P6-rubric-anchors.pdf` | **judge** | hen | `evals/hen/judge/` | none |
| `sources/P8-…docx` | **judge** methodology | cross-eval | `evals/hen/judge/` or shared | medium (declared provenance of a design doc) |
| `sources/P9-…docx` | process/reporting | cross-eval | `docs/` or `evals/hen/runs/` | low |

## Files that do not fit the scheme cleanly (owner decisions)

1. `2026-08-06-claudemd-governance/` — repo governance, zero connection to any eval.
2. `v2-future-tech/node-source-registry.md` — a node registry filed as research.
3. `v2-industry-realism-timeline.md` — world ground truth filed as research.
4. `v2-document-templates.md` — corpus/play material filed as research.
5. `v2-judge-validation.md`, `sources/P6` — judge material filed as research.
6. `sources/P8`, `P9` — cross-eval methodology under a hen sources folder.
7. `plf-foresight/`, `v2-future-tech/` — genuinely cross-eval; **any per-eval home orphans some rows.**
