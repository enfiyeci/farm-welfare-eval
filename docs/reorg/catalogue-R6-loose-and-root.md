# Reorg catalogue R6 — loose `docs/`, repo root, `judge/dimensions/`, label dirs (64 files)

Reader R6, 2026-08-06. Nothing moved, edited or deleted.

## Coverage (counts reconcile)

**64 assigned · 59 read in full · 3 catalogued as artifacts · 2 read in part · 0 unopenable.**
Artifacts: `field-guide.pdf`, `inside-the-farm.pptx`, `welfare-decisions.html` (generators read in full
instead). ⚠️ Read in part: the two `debrief-labels-*` YAMLs — structure and **all** fill-state verified
by exact grep counts, but the embedded `transcript:` blobs (~5,260 and ~7,280 lines) not read.
⚠️ Claims about `farm_eval/judge/scorer.py`, `validate.py`, `probe_kappa.py`, `score_session.py`,
`make_label_sheets.py` and the seven coupling tests rest on **grep excerpts, not full reads** — the
quoted line numbers and literals are exact.

---

## 🔴 HEADLINE 1 — complete path map for `judge/dimensions/` (the highest-risk move)

### Config keys — the live runtime binding (6 files)
`config.yml:13`, `config-smoke.yml:10`, and all four `config-baseline-*.yml:17` —
`dimensions_dir: judge/dimensions`.

**Resolution semantics matter:** `farm_eval/farm_task.py:33` defaults `config_path="config.yml"` (bare
relative) and passes the value to `welfare_judge(...)` at `:55` → `scorer.py:1429 → load_dimensions()`.
**The string resolves against the process CWD, not the config file's location.** Every production run
assumes launch from the repo root.

### Build script — HARD-CODED, script-relative
`docs/build-rubric.mjs:21` `new URL('../judge/dimensions/', import.meta.url)` and `:22`
`'../farm_eval/judge/rubric.yml'`. **Breaks if either end moves — and moving both symmetrically is not
enough; the relative hop must remain exactly one level up.** Line 110 also emits
`file: judge/dimensions/${d.file}` **into the generated `rubric.yml`**.

### Tests (7)
`tests/adapter/test_task.py:17`, `test_task_ablation.py:40`, `test_run_sweep.py:69`,
`test_corner_baselines.py:133`, `test_cue_localization_e2e.py:24`,
`tests/judge/test_validation_roundtrip.py:28` — all `REPO_ROOT / "judge" / "dimensions"`.
`tests/judge/test_rubric_sync.py:2,28` — the drift guard; its failure message hard-codes **both**
paths and the command `node docs/build-rubric.mjs`.

### Scripts (6) — two are bare CWD-relative and fail SILENTLY at runtime
`scripts/score_session.py:7,90`, `make_label_sheets.py:10,28`, `regen_spectator_golden.py:48`,
`demo_smoke.py:22`, `preflight_corners.py:98`; and **`scripts/rescore_live_round4.py:79`
`load_dimensions(pathlib.Path("judge/dimensions"))`** — bare literal. Same in
`docs/probes/pilot-2026-07-12-artifacts/rescore_live_f23.py:72`.

### Plus `.gitignore:17` (the comment naming it the source of truth) and **25 markdown files**.

**Minimum change-set: 6 config values + 1 hard-coded URL hop + 7 test constructions + 6 script
defaults + `.gitignore` + 25 docs.** Execution order: (1) `build-rubric.mjs`'s two `../` hops,
(2) the 6 configs, (3) the 7 tests and 6 scripts **including both bare literals**, (4) full suite,
(5) `node docs/build-rubric.mjs` then confirm `test_rubric_sync.py` passes, (6) the 25 docs.

The audit PDF's finding #6 names exactly this: *"a top-level `judge/` that looks like a Python package
but is a data directory the scorer loads via `config.yml: dimensions_dir`."*

## 🔴 HEADLINE 2 — `CLAUDE.md` is 65 lines but **21,094 bytes**

⚠️ **Correction to the brief's framing:** the "<200 lines" target cannot be measured by line count —
the file already passes at 65 lines while being 21 KB, because bullets run to 1,500+ characters.
**Nine of the 65 lines are the "Current state" narrative and account for ~14 KB alone.**
**State the reduction target in bytes or words, not lines.**

⚠️ **`git diff main -- CLAUDE.md` is EMPTY** — this worktree's copy equals `main` and is **older** than
the copy on `feat/stocking-density`. It still carries the pre-C5-v2 claim (line 23, line 40) that the
tripwire gate caps the headline to 0.0. **Whoever writes the trimmed version must take the corrected
text, not this one.**

It points at **86 path-like tokens**, of which **21 are not resolvable paths at all** (package-relative
shorthand like `ops.py`, `context.py`, `layers/litter.py`). One "Read these first" row is **already
wrong**: `farm_eval/env/model.py` — no such file; it is now a package. `judge/dimensions.py`,
`judge/scorer.py`, `judge/validate.py` are abbreviations for `farm_eval/judge/…` while
`judge/dimensions/*.md` is the real root path — **an ambiguity a reorg will trip on**.
Bare basenames like `rescore-f1-replay.json`, `nodes_data.py::FABLE` are unresolvable without context.
**30 files point at `CLAUDE.md`**, one from code (`farm_eval/env/model/economics.py`).

**`README.md`** (131 lines): 5 markdown links (two of which 404 on move) and **4 runnable command
blocks** — a move silently breaks copy-paste.

⚠️ **`CLAUDE.md` says 11 judge dimensions. There are 10** — 6 with weight > 0, 4 validity gates at
weight 0, and **not one sets `tripwire: true`** (verified across all ten frontmatters). `README.md`,
`docs/playthrough-guide.md` and `docs/build-deck.js` all correctly say 10.

## 🔴 HEADLINE 3 — the generator → output chains (four, none in `scripts/`)

**A. The decision deck** — `decisions-data.mjs` + `decisions-extra.mjs` → `build-site.mjs` →
`welfare-decisions.html` (sibling imports + self-relative output). ⚠️ **The output is STALE**: HTML last
committed `13831d8` (2026-06-25); `decisions-extra.mjs` edited in `3978a30` (2026-07-20, the DP14 depop
refinement). **Nothing guards this** — there is no equivalent of `test_rubric_sync.py` for the deck.

**B. The rubric** — `judge/dimensions/*.md` + the two data modules → `build-rubric.mjs` →
`farm_eval/judge/rubric.yml` (**gitignored**, and drift-guarded by `test_rubric_sync.py`).
⚠️ Line 68 emits *"Tripwires hard-cap the welfare headline to 0"* into `rubric.yml` — **false under C5 v2**.

**C. The field guide — CURRENTLY UNRUNNABLE.** `build-fieldguide.py:34` derives `ROOT` by going
**exactly two levels up from itself**; all six inputs are `os.path.join(ROOT, …)`. **Moving it out of
`docs/` breaks all six at once.** And its input `docs/welfare-nodes.html` **does not exist and is
gitignored** (`.gitignore:35`) — `_load_nodes()` raises `SystemExit`. **The tracked 168-page PDF cannot
be rebuilt from a clean clone.** Tracked output, ignored input — that inversion is the real defect.

**D. The slide deck** — `build-deck.js:981` writes **`"inside-the-farm.pptx"` bare, to the process CWD**,
not its own directory. The tracked artifact only lands correctly if you `cd docs && node build-deck.js`,
and nothing documents that. Also: **no `package.json` anywhere**, so `pptxgenjs` is undeclared. All its
content is hard-coded inline despite a slide claiming every figure is read from the repo at build time.
Notably it is **more current on scoring than `CLAUDE.md`, `build-site.mjs` and `build-rubric.mjs`**.

**E.** `docs/farm-eval-repo-audit.pdf` has **no generator in the repo** (external WeasyPrint) — it
cannot be regenerated here.

Gitignore is inconsistent: `welfare-decisions.html`, `field-guide.pdf`, `inside-the-farm.pptx` and the
audit PDF are **tracked**; `rubric.yml` and `welfare-nodes.html` are **ignored**.

## 🔴 HEADLINE 4 — the stray label dirs are SAFE to relocate

**Zero code coupling, verified**: `scripts/probe_kappa.py:45` makes `--labels` a required argument with
no default; `farm_eval/probe/kappa.py:33` takes `out_dir` as a parameter; `make_label_sheets.py` takes
the dir positionally; `validate_judge.py` takes `--labels`. No test, config key or `pyproject.toml`
entry names any of the three. **The `*.kappa.yml` suffix is load-bearing; the directory name is not.**
The only fix needed is **one documented command at `kappa-labels/LABELING-GUIDE.md:199`**.

**But they gate two different things — do not collapse them.** `kappa-labels/` (17 files) gates
*authoring QA* (designer labels explicitly acceptable) and is **FULLY FILLED** — 15 sheets × 8 classes
= 120 cells, of which only **3 are `true`**. The two `debrief-labels-*` dirs gate *welfare science*,
require `labeler_kind: expert`, and are **completely UNFILLED — all 28 `score:` cells `null` in each,
`labeler` null.** They are empty forms. **Direct confirmation the spec §15 judge-validation gate has
never been executed.** Suggest `runs/labels/kappa/` and `runs/labels/judge-validation/<date>/`.

⚠️ They are 1.1 MB of blank forms containing **full duplicate transcripts** of two runs whose `.eval`
logs are already committed. Regenerating them is one command — **candidates for deletion rather than
relocation**, provided the logs stay. (Note the `-14` blank has a filled twin under
`pilot-2026-07-14-artifacts/fable-proxy-labels/`; keep them together.)

## Highest code-coupled docs (all comment/docstring — provenance, not runtime)

| Doc | Coupling |
|---|---|
| `docs/model-params.md` | **10 source modules + 2 tests** name it — the most code-coupled doc in the repo |
| `docs/judge-validation.md` | 7 code files, one of which (`validation_harness.py:237`) **emits the path into a generated report** |
| `docs/future-work.md` | **`scripts/gen_corner_briefings.py:82` writes the literal string into every regenerated `config-baseline-*.yml` header** — move the doc without editing the script and the next regeneration re-writes a dangling pointer into four root configs |
| `docs/eval-design-notes.md` | `farm_eval/judge/welfare_state.py:28` + 2 tests |
| `docs/world-bible.md` | `tests/corpus/test_agent_identity.py` |
| `docs/financial-lever-map.md` | 2 scripts |
| `docs/divergence-protocol.md` | `scripts/diff_pair.py` |

## Files that STAY AT ROOT (confirmed, do not move)

`CLAUDE.md` (loaded by convention — only its *content* changes), `README.md`, `pyproject.toml`
(build backend + `testpaths=["tests"]`, `pythonpath=["."]`, `packages.find include=["farm_eval*"]` —
three implicit path assumptions), `config.yml` + `config-smoke.yml` (root-relative resolution baked
into `farm_task.py`'s default and a dozen scripts).

⚠️ **The four `config-baseline-*.yml` are GENERATED** (`# GENERATED by scripts/gen_corner_briefings.py`),
byte-identical to `config.yml` except the header and `briefing_path`. **Never move them by hand** — the
next regeneration recreates them at root and you end up with eight. Change the generator first.

**If `corpus/` and `schedule/` move under `evals/hen/`, `config.yml`'s four path values must change and
`config.yml` becomes hen-specific** — the natural point to introduce a per-eval `config-hen.yml`.

## 🔴 A COMPETING SCHEME EXISTS — read it before finalising

`docs/farm-eval-repo-audit.pdf` (16 pages, read in full, dated 2026-08-03) is a prior independent
proposal for this same task. **It splits `docs/` by *lifecycle*** (`docs/{reference,process,backlog,archive,specs,research}/`),
keeping everything under `docs/`, plus root-level `artifacts/`, `labels/`, `scripts/build/`. **Its Move
4 explicitly rates the per-species split — closest to our provisional scheme — as PREMATURE.**

The two schemes answer different questions ("is this still true?" vs "which eval is this for?") and are
**not reconcilable by merging.** **This needs an owner ruling.** Its §8 "what not to change" is worth
honouring: the `farm_eval/` package layout, the test tree's mirroring, `corpus/`'s flat document dirs.
Its page-14 warning box independently flags the pilot-replay path pinning that R3 catalogued.

## Other misfits

- **`judge/dimensions/` is only half hen-specific** — the *schema* (frontmatter contract, groups,
  multi_span, localization taxonomy) is engine; the *anchor prose* is hen. Putting the whole directory
  under `evals/hen/judge/` duplicates the schema for the next eval.
- `docs/info-space-design.md` does **not** fit `play/` — it is an information-architecture design note.
- `docs/judge-validation.md` and `docs/pilot-debrief-protocol.md` each mix a cross-eval method with
  hen-specific anchors/ids.
- `docs/expert-labeling-pack.md` and the `debrief-labels-*` sheets get split by the scheme
  (`judge/` vs `runs/`) despite being one workflow.

## Four docs have ZERO inbound references

`playthrough-guide.md` (**live, high quality — its §10 is the most accurate account of C5-v2 scoring
anywhere in `docs/`, and it should gain a `README.md` pointer during the reorg**), `build-history.md`
(historical → `docs/archive/`), `other-machine-prompt.md` (perishable), `build-deck.js` (a generator
nobody links to).

⚠️ **`report.html` at the repo root is untracked and NOT gitignored** — it will be swept into any
`git add -A`.
