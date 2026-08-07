# Reorg catalogue R1 — `docs/research/` first entry → `2026-08-04-welfare-footprint` (41 files)

Reader R1, 2026-08-06. Nothing moved, edited or deleted.

## Coverage (counts reconcile)

**41 assigned · 32 read in full · 9 catalogued as artifacts · 0 unopenable.**

⚠️ The brief's `-maxdepth 2` listing **missed 8 PDFs** in `2026-08-04-welfare-footprint/sources/`;
R1 added them. Artifacts: those 8 chapter PDFs (`ch01` page one extracted to verify authorship) +
`pain-track-parameters.json` (structure inspected, provenance from its own `_source` key).

**Delegation disclosed:** R1 read 19 prose files + 9 artifacts itself; **13 files (both dairy folders
+ the telemetry/fencing/aquatic trio, ~490 KB) were read by three Opus subagents it dispatched.** Each
returned a reconciling coverage statement (6=6+0+0, 4=4+0+0, 3=3+0+0). **R1 traced four of their
load-bearing claims to source itself — all confirmed.**

⚠️ R1's own partial reads outside assignment: `docs/LANES.md` (first 60 of 169 lines);
`docs/future-work.md` (112–122); `technology-use-catalog.md` (grep hits only). **The 107-broken-paths
count rests on a grep, not on reading those 14 files.**

---

## 🟢 D.1 — NOTHING EXECUTABLE BREAKS. The most important finding.

Grepped every `.py`, `.mjs`, `.js`, `.yml`, `.toml`, `.sh` for `docs/research`. **Four hits, all
comments/docstrings, none a file load:**

| File:line | Cites | Nature |
|---|---|---|
| `farm_eval/env/model/layers/staffing.py:4` | `2026-07-01-daily-labor-staffing.md` | docstring, justifies `adequacy_factor` |
| `farm_eval/env/model/params.py:84` | `2026-07-13-financial-realism-web-sweep.md` | comment, justifies `cold_feed_coeff = 0.028` |
| `tests/env/model/test_cold_thermoregulation.py:2` | same | test-module docstring |
| `farm_eval/env/model/economics.py:5` | `docs/research/SOURCES.md` | docstring |

Also: **nothing loads `pain-track-parameters.json`** (zero hits for `pain.track|pain_track`); **no
symlinks**; `.gitignore` excludes nothing in the tree.

**The reorg cannot break a test, a scorer, a task or a build. It can only break provenance.**

## 🔴 C.1 — The aquatic reading list writes HEN paths as its own destinations

**The sharpest hazard, and it is semantic not mechanical.** `2026-08-03-aquatic-farm-reading-list.md`'s
mapping table (lines 596–606, read directly) and its per-source "*Feeds:*" lines name
`docs/world-bible.md`, `docs/model-params.md`, `docs/decision-register.md` as where salmon content
goes — **the live HEN files**. It means "the world-bible-shaped artefact of the aquatic eval", but is
written as if the repo has one world bible.

**A path-rewriting script will silently cement aquatic guidance onto hen destinations. Needs a human
editing pass, not find-and-replace.**

## 🔴 D.5 — 107 already-broken absolute paths across 14 files

`/Users/ardaenfiyeci/Desktop/farm-eval/...` — **wrong username** (`ardaenfiyeci` ≠ `ardaenf`) and
**wrong repo name** (`farm-eval` ≠ `farm-welfare-eval`). In `docs/build-history.md`,
`v2-judge-validation.md`, both `2026-08-03-plf-*` design docs, a probe, three plans, six handoffs.
**Broken today — but if left, indistinguishable from breakage the reorg caused.** Fix in the same pass.

## 🔴 D.7 — The scheme has NO shared-research slot; four files need one

`2026-08-03-citation-integrity-audit.md` (spans hen **and** dairy; process/quality work, not
evidence; **an orphan — zero inbound**; ~40 outbound paths, the densest R1 read) ·
`2026-07-12-web-sweep-eval-awareness-judge.md` (species-agnostic judge methodology) ·
`2026-07-28-briefing-prior-art/` (2 files, briefing methodology) ·
`2026-08-03-welfare-finance-separability.md` §§4–5 (welfare-score aggregation).

**"The single structural gap I would raise before the move starts."**

## 🔴 D.8 — Two naming decisions to settle BEFORE moving

1. **`evals/dairy/` vs `evals/plf-dairy/`** — R1's two dairy subagents proposed **different** names.
2. **Confirm the hen eval's folder name** (`docs/LANES.md` says "the hen eval", supporting `hen`).

## C.3/C.4 — Cross-eval dependencies run BOTH ways

Verified at source: `docs/future-work.md:116,:120` cite
`2026-08-04-dairy-depopulation/05-mass-depopulation.md` **by path**, as the evidence that hen node
DP14's AVMA-2019 citation is stale. So after a split, **a hen backlog item points into dairy
research.** Conversely `2026-07-20-depop-welfare-hierarchy.md` (hen) is cited by
`dairy-depopulation/README.md:9,:38` and `dairy-telemetry-parameters.md:10`.

**Contamination has NOT reached code:** no dairy/aquatic number in `farm_eval/`, `scripts/`, `tests/`,
`config.yml`, `pyproject.toml`, or the build scripts. ⚠️ That rests on a ten-term grep — negative
evidence, not a full read.

## D.2 — Clickable markdown links that break (silent 404s)

`docs/model-params.md:135,213` → `](research/2026-07-01-daily-labor-staffing.md)`; `:142` →
`](research/2026-07-02-staffing-org-structure.md)`; `2026-07-13-financial-realism-web-sweep.md:7,8,108`
→ `](v2-profit-levers-research.md)` etc. (same-directory — survive only if `v2-*` moves too).

⚠️ Same class just outside range: `docs/model-params.md:3`, `docs/world-bible.md:287`,
`docs/decision-register.md:3,:242`. **Under the scheme BOTH ends of each move, in different
directions** (world-bible/model-params → `world/`, decision-register → `nodes/`, research →
`research/`). **Treat as one batch.**

## D.4 — References a path-rewriter will MISS

- Dairy trait-pricing files cross-reference each other as `01-…`, `02-…` **with a literal ellipsis**.
- The telemetry file uses bare cross-corpus tags `[T11 🔵]`, `[✅ S21]` indexing into
  `v2-future-tech/findings.md`. **A tag cannot be grepped automatically** — if those registries land
  in a different tree, the tags stop being followable with no trace.
- Many README pointers are unpathed section refs ("catalog §4.2", "settled spine §3").

## D.6 — Folders that must move as UNITS

`2026-07-28-briefing-prior-art/`, `2026-07-28-substrate-realism/`, `2026-08-04-dairy-depopulation/`,
`2026-08-04-dairy-trait-pricing/`, `2026-08-04-welfare-footprint/` **including its `sources/`
subdirectory of 8 tracked PDFs (~7.5 MB)**.

## ⏰ Timing hazard — move `pain-track-parameters.json` BEFORE the currency build

Nothing loads it today, but `docs/plans/2026-08-05-welfare-currency-build.md:249` names it. **If that
plan executes it becomes a runtime data dependency.** Move it before, or the plan is written against a
path that changes underneath it.

## Provenance hazards (not move risks)

- **`2026-07-13-financial-realism-web-sweep.md`** is the one file where a stale path leaves a **test**
  and a **calibrated coefficient** with no followable justification. Its cited temperature bands
  (18–24/18–21/below-16 °C) are **not in the cited paper** (PMC7823783 gives 19–22 °C) — and those
  bands feed the heat model.
- **🔴 `2026-07-29-stocking-density.md` §1's central design argument** — the density × genetic-line
  interaction "conveniently matching DPD's `genetics: low_pecking`" — **is not in its cited source**
  (PMC7070775). An implementation plan is already written against it.
- **`vitamin-d3-decision.md`** is binding (settled spec §2d) and **cannot be audited** — all 88
  citations are unresolvable `citeturnNviewM` tokens with no PDF sibling.
- **`heat-balance-and-belt-energy.md`** carries a `⛔ ERRATUM`: its own recommended mapping fails its
  validation target by **65×**. **Do not split or excerpt this file.**
- **`citation-integrity-audit.md` §3c is itself stale** — its single 🔴 finding is already fixed in the
  telemetry file (R1 verified at source).
- **Two dairy folders disagree on a number:** trait-pricing cites "37.6% removal" that depopulation had
  corrected (33.8%/5.6%) seven hours earlier the same day.
- **`docs/research/SOURCES.md` contains zero mentions of dairy or aquatic** — the directory's own
  register does not know about a third of what is in it.

## Destinations

| Files | Destination |
|---|---|
| The hen research files + welfare-footprint folder & its `sources/` | `evals/hen/research/…` |
| `2026-08-04-dairy-depopulation/`, `2026-08-04-dairy-trait-pricing/`, `dairy-telemetry-parameters.md`, `virtual-fencing-parameters.md` | `evals/<dairy-name>/research/` — **as units** |
| `2026-08-03-aquatic-farm-reading-list.md` | `evals/aquatic/research/` — ⚠️ that tree would hold nothing else; **needs a human editing pass first (C.1)** |
| `citation-integrity-audit.md`, `web-sweep-eval-awareness-judge.md`, `briefing-prior-art/` | **the missing shared slot** |
