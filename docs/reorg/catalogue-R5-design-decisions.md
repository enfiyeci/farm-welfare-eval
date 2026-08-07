# Reorg catalogue R5 — `docs/design/`, `docs/decisions/`, `docs/handoffs/`, `docs/pilot/`, `docs/mockups/` (45 files)

Reader R5, 2026-08-06. Nothing moved, edited or deleted.

## Coverage (counts reconcile)

**45 assigned · 40 read in full · 5 catalogued as artifacts · 0 unopenable.**
Artifacts: the five PNGs in `docs/pilot/assets/` — type, dimensions, byte size and inbound refs
recorded; subject matter taken from the embedding document's alt text and prose, not from inspecting
the images.

⚠️ Read outside the assignment and NOT whole: `docs/LANES.md` (only lines 76–92 + grep hits);
project `CLAUDE.md` (**not opened** — only two grep-matched lines; statements about it come from the
session-start system reminder); `tests/env/test_body_ref_loud.py` (line 3 only).
⚠️ One claim not asserted: whether the missing `2026-08-04-density-harm-and-dp22-rework-decisions.md`
is hen or dairy — it does not exist on this branch and reading it off another commit was judged
outside a read-only brief.

---

## 🔴 FINDING 1 — This reorg has prior art, and it is already measured

**`docs/design/2026-08-03-plf-eval-restructure-and-scoring-analysis.md` (641 lines) is a completed
repo-restructure analysis.** Three Codex rounds, 21 findings, all accepted. Read it before designing
anything. Measured facts it already establishes:

- 1,005 tracked files; 76 Python under `farm_eval/`.
- **The collision is at the ROOT, not in the package namespace** — `corpus/` (505 files),
  `schedule/`, `prompts/`, `judge/dimensions/`, `config.yml` + 5 variants, `kappa-labels/`, `logs/`.
- **22 of 29 `scripts/` files define a repo-root constant; 18 use it for `sys.path`; only 12 reach
  into content dirs** — so a naive content-root move breaks imports.
- `pyproject.toml` pins `include = ["farm_eval*"]`; `testpaths = ["tests"]` does **not** assume one
  eval; a **src-layout mapping preserves the `farm_eval` import namespace under a moved directory**.
- Four layout options weighed (sibling package / full `evals/<name>/` / content-roots-move /
  shared-core-first). **Recommends option 3 staged, deferring the shared-core extraction until the
  PLF eval works** — which independently matches the staging recommendation made this session.

⚠️ Its own coverage caveat, stated twice in the document: only **7 of 76** Python files were read end
to end; the other 69 Python / 505 corpus / 169 test / 174 docs files were classified from measured
coupling and paths, not from reading. It says: "before any file is moved, the ones whose disposition
is load-bearing should be opened."

⚠️ Several of its outbound paths are written as `/Users/ardaenfiyeci/Desktop/farm-eval/…` — a user
and directory that do not exist on this machine. It flags this itself at line 305.

**Destination:** `engine/design/` — it is about the shared harness and repo layout, not one eval.

## 🔴 FINDING 2 — `docs/design/` is contracted to receive HEN material, by a line I wrote

`docs/LANES.md:83` gives the **staffing-design lane (hen)** write-ownership of `docs/design/**`.
And `docs/decisions/10-measured-answers.md:60,160` cites a *hen* DP22/crowding design doc at
`docs/design/2026-08-04-density-harm-and-dp22-rework-decisions.md` — **which does not exist on this
branch** (it is on commit `5430dcb` elsewhere and arrives when that merges).

So `docs/design/` is an unqualified bucket that has *so far* filled with dairy but is **scheduled to
receive hen**. If the reorg makes it dairy-only, **`docs/LANES.md:83` must change in the same commit**
or the next staffing session re-contaminates it.

## FINDING 3 — the dairy-vs-hen breakdown of `docs/design/`

The "mostly dairy" claim is **confirmed for the four top-level files** and needs one correction for
the subdirectory.

| File | What it is | Scope |
|---|---|---|
| `2026-08-03-plf-framing-decisions.md` | Four dairy decisions: build separate at `evals/plf_dairy/`; look-resolution from day one; welfare time series in scope; standing conditions as a 6th signature kind; split `CLAUDE.md` (measured 20,833 B, of which "Current state" is 14,475 B = **69%**). Also evidences that "no farm content hardcoded in logic" held only **partially** (`tracker.py:438`, `Metric.house_id`, `_READ_TOOLS`, `welfare_state.py`'s five poultry channels). | **DAIRY** |
| `2026-08-03-programme-and-plf-decisions.md` | Owner-confirmed programme spine: Track C *is* the dairy eval; packs for salmon/shrimp but a separate substrate for dairy; sensors return truth, uncertainty in inference; density↔mortality cross-species study exempted from the realism bar. Supersedes §§2/4a of the above. | **DAIRY + PROGRAMME** |
| `2026-08-03-plf-eval-restructure-and-scoring-analysis.md` | **The prior art — see Finding 1.** | **CROSS-EVAL / engine** |
| `2026-08-04-technology-use-catalog.md` (1,863 lines) | Five PLF-dairy technology entries (rumen bolus, virtual fencing, neuromodulation, gene-edited cattle, autonomy+lease). Selection LOCKED at four. Entirely cattle. Contains three 🔴 self-corrections to its own source tags. | **DAIRY** |
| `v2-game-dynamics/catalog-A-priors.md` | 12 elicitation dynamics + a 0–7 choice-format ladder, deliberately unsourced, to be compared against B. | cross-eval methodology |
| `v2-game-dynamics/catalog-B-research-backed.md` | Sourced counterpart, G1–G25. Key: convex-budget allocation under varied price recovers the tradeoff **rule**; graded beats binary but optimum is **~7 categories** ("continuous strictly best" was **REFUTED**); models detect evaluation (AUC 0.83); demand effects modest implicitly (~0.13 SD), large explicitly (0.6–1.06 SD) and **amplified within-subject** — bears directly on the spec §20 salience ladder. | cross-eval methodology |
| `v2-game-dynamics/comparison.md` | A-vs-B head-to-head; two real corrections. | cross-eval methodology |
| **`v2-game-dynamics/depop-node-source-enrichment.md`** | **THE MISFIT — pure HEN.** All about the built `DP14_HPAI_DEPOP_METHOD`: quotes `schedule/events.yml` verbatim, and **corrects a live scoring misconception** — under C5 the tracker skips judged classes (`tracker.py:_evaluate_classified` does `if cls.judged or cls.default: continue`), so the `tripwire: true` on the judged `vsd_plus` class is **functionally inert**. Proposes rubric anchors (N₂ foam 30±2 s layers / 18±1 s broilers). Corrects an indemnity figure to $4.67/head. | **HEN** |
| `v2-game-dynamics/future-tech-x-mechanics-priors.md` | Priors draft F1–F5. Self-marked superseded. | mixed |
| `v2-game-dynamics/future-tech-x-mechanics-B-research-backed.md` | Sourced, T1–T25, 25 verified / 0 refuted. **Hen-relevant headline:** for a cage-free *layer* farm, real mostly-deployed techs give novel welfare levers — in-ovo sexing, laser-herding robots, depop-method choice, affect-AI. | mixed |
| `v2-game-dynamics/raw-claims-B.md`, `raw-claims-ft2.md` | 122 + 119 verbatim claims with per-claim verify status. Pure provenance — **never edit or prune**. | provenance |

**Zero files in `docs/design/` are present-day hen *design* documents.**

`depop-node-source-enrichment.md` → **`evals/hen/nodes/`**. Zero inbound, so move risk is none. The
clearest single misfiling in the assignment.

## FINDING 4 — `docs/decisions/` cross-link map (the breakage list)

**28 internal relative links across 9 source files.** Survive only if the folder moves whole.

`README.md` → all nine briefs (lines 36–44). `00-RULINGS.md` → README, `10-measured-answers.md`
(repo-relative, line 6) and bare (line 150). `01` ↔ `02` ↔ `03` mutually (01→03 at lines 40, 72, 101,
148). `04`→`07`; `05`→`04`,`03`; `07`→`04`; `08`→`02`,`03`,`05`,`06`,`07` (lines 54–58).

**No internal links emitted by:** `06`, `09`, `10`, `11`.
**`11-irreducible-questions.md` has NO inbound link from anywhere** — it is not in the README index
(written before it) and is reachable only by knowing it exists.

**7 external inbound, all to `00-RULINGS.md` / `README.md` / `10-measured-answers.md`:**
`docs/LANES.md:7,48,118,132,169`; `docs/research/2026-08-06-litter-lever-and-ammonia/README.md:37`;
`docs/other-machine-prompt.md:57`.

**No code, test, config or build script references this folder at all.**

**Pre-existing dangling refs (branch divergence, NOT reorg damage — do not mistake them for it
after the move):** `10-measured-answers.md:60,160,161` → two files absent from this branch; plus two
more from handoffs.

**Recommendation: move `docs/decisions/` as a single unit to `evals/hen/design/decisions/`.** Eight of
thirteen are unambiguously hen; two are hen-dominant mixes; `08-which-demo` is programme and
`09-housekeeping` is process, but splitting them costs 28 link rewrites and destroys `00-RULINGS.md`
as a coherent owner record. Leave a `docs/` pointer to `00-RULINGS.md`. If anything splits out, split
only `09-housekeeping` (complete history).

## FINDING 5 — code coupling across all 45 files is ONE prose citation

`tests/env/test_body_ref_loud.py:3` (module docstring) names
`docs/pilot/2026-07-01-pilot-findings.md`. It is prose, not a path the test opens — **the test will
not fail if the file moves** — but it should be updated in the same commit.

**Move risk across all 45 files is documentation-only.**

## FINDING 6 — `docs/handoffs/` is 10/12 complete history and does NOT need to move

The target scheme already names handoffs as cross-cutting process. Cleanest result in the assignment.

**Live content worth preserving explicitly:**
- `handoff-2026-08-03-futuristic-dairy-design.md` — **the dairy world's founding decisions**, still
  authoritative per its own successor, incl. a six-item **do-not-retry list**.
- `2026-07-28-substrate-realism-wave.md` — **only 2 of 12 agent levers move the world in both
  dimensions; five do nothing at all.** Plus the best engineering lesson in the folder: the HVAC
  "research gap" was actually `layers/heat.py::indoor_temp_c` computing
  `max(setpoint, ambient − cooling)`, so `vent` is a *cooling* lever, not an airflow rate —
  **read the substrate before commissioning research about it.**
- `2026-07-29-stocking-density-implementation.md` — the play-it-right/play-it-wrong A/B technique,
  the **wake-day trap** (actions snap to the next wake day; the heat window 28–32 contains no wake
  day at all) and the **zero-reading trap**.

**Self-declared superseded, safe to archive today:** `2026-07-30-stocking-density-build-tasks1-3.md`;
`handoff-2026-08-04-welfare-currency-step1.md`; `...-step1-sources-read.md`;
`v2-game-dynamics/future-tech-x-mechanics-priors.md`.

**Does not belong in this repo at all:** `docs/handoffs/machine-transfer/global-CLAUDE.md.txt` — a
2026-08-03 snapshot of the *global* `~/.claude/CLAUDE.md`, stale by construction (the live file has
since grown a review-discipline section and a delegation hierarchy this copy lacks).

## FINDING 7 — `docs/pilot/` is history, and must move with its assets

Describes the **2026-07-01/02** Flash-vs-Pro pilot, superseded by the 2026-07-12 Gemini pilot (whose
artifacts live in `docs/probes/`).

- `2026-07-01-pilot-findings.md` — the §15 gate report. Flash 4.27 vs Pro 1.92-**GATED INVALID**.
  Found the eval discriminates on **propensity not capability**; the mechanical spine is bit-stable;
  literal `[PLACEHOLDER body not yet authored: …]` emails were served to both agents for 5 scored
  decisions. Verdict: NOT freeze-ready. 6 inbound incl. the one code citation.
- `2026-07-02-pilot-run-analysis.md` (489 lines) — node-by-node forensics on all 23 decisions. **On
  the five latent nodes both models score identically, four of them 0.0.** Four nodes flagged
  ⚠ content-contaminated (DP17, DP19, DP20, DP21). The LLM surface **systematically under-credits
  models that act through non-email channels.** 0 inbound. **Must move together with `assets/`** — 5
  relative image links.
- `assets/*.png` (5, catalogued not read) — `tool_usage.png` has an **out-of-folder inbound** from
  `docs/plans/2026-08-04-welfare-currency-and-finance-ledger.md:141`.

**Destination:** `evals/hen/runs/2026-07-01-pilot/`.

## FINDING 8 — `docs/mockups/` is a completed decision record

`fms-dashboard-directions.html` (727 lines, self-contained, no external assets): three visual
directions for the human-playable console — A "Panel Steel", B "Prairie SaaS", C "Night Ops" — same
screen, same numbers, driven by CSS custom properties over one DOM skeleton. Recommends **A as base
identity, C reserved for debug**, so blind and debug sessions are visually unmistakable. `CLAUDE.md`
records the dashboard as BUILT with exactly that. **Status: complete-history.** 2 inbound (a spec and
a plan). **Destination:** `evals/hen/play/mockups/`.

## Migration hazard flagged from outside these folders

Pilot replay artifacts are pinned **by path** — anything under `docs/probes/pilot-*-artifacts/` must
be grepped in `scripts/`, `farm_eval/report/` and the replay scripts before it moves. (R3 owns that
subtree.)
