# Reorg catalogue R4 — `docs/plans/` + `docs/specs/` (40 files)

Reader R4, 2026-08-06. Read-only; `git status --porcelain` empty at start and end.

## Coverage (counts reconcile)

**40 assigned · 23 markdown read in full by R4 · 15 markdown read in full by delegates · 1 HTML read
in full · 2 HTML catalogued with a ⚠️ · 0 unopenable.**
(`docs/specs` md = 12: R4 read 10, delegates 2. `docs/plans` md = 25: R4 read 12, delegates 13.
Assets = 3: 1 read in full, 2 partial.)

⚠️ For `assets/composite-v2.html` and `extras.html` R4 read all markup, text and inline SVG but
**excluded the `<style>` block in each and the `<script>` block in `composite-v2.html`.**
R4 independently verified every delegate *status* claim against artifacts on disk, and confirmed four
non-existent paths (`scripts/audit_levers.py`, `farm_eval/env/model/pain.py` — both absent, confirming
two "unbuilt" verdicts). It did **not** re-derive delegates' outbound reference lists.

---

## 🔴 HEADLINE 1 — the engine-vs-hen split across the 12 specs

They sort into **three** groups, not two.

| Spec | Verdict | Destination |
|---|---|---|
| `2026-07-03-partial-scoring-and-judge-validation-design.md` | **ENGINE ~100%** — partial-run detection, NaN-not-zero headline, blind label sheets, Spearman runner. A dairy eval reuses it verbatim. | `engine/design/` |
| `2026-07-05-eval-awareness-reduction-design.md` | **ENGINE ~90%** — tells taxonomy is unit-tested to contain no farm vocabulary | `engine/design/` |
| `2026-07-06-playable-dashboard-design.md` | **ENGINE ~95%** — its own test bans farm strings from the page | `engine/design/` |
| `2026-08-04-spectator-dashboard-design.md` | **ENGINE ~90%** — routes the breed label through `ModelParams.breed_label` so the page hardcodes nothing | `engine/design/` + its `assets/` |
| `2026-06-24-farm-welfare-eval-design.md` | **MIXED ~55% engine — the hard one** | `evals/hen/design/` **whole** |
| `2026-06-26-model-calibration-design.md` | **MIXED ~45% engine** — the package layout + reference-run anchoring method are engine; the six layers and all anchors are hen | `evals/hen/design/` |
| `2026-08-04-welfare-currency-design.md` | **MIXED ~40% engine** [delegated] | `evals/hen/design/` now |
| `2026-06-26-farm-eval-v2-design-decisions.md` | **A HEN-DERIVED VARIANT, not engine** | `studies/v2-broadened-scope/` + a pointer |
| `2026-06-26-flock-cop-reads-integrity-design.md` · `2026-07-08-corpus-realism-pass-design.md` · `2026-07-28-substrate-realism-wave-design.md` · `2026-07-29-stocking-density-design.md` | **HEN** | `evals/hen/design/` |

**Do not split the v1 founding spec**, even though it is the most engine-heavy hen document. Its
sections cross-reference constantly, `CLAUDE.md`'s "Read these first" table cites it by **nine** section
numbers, and four other docs cite it by section. Splitting breaks all of those at once; moving it whole
breaks one path in six places. Write the engine architecture doc as a **follow-on authoring task**.

## 🔴 HEADLINE 2 — `play/` means two different things in the scheme

The scheme's `evals/<eval>/play/` = "what the agent/human can SEE". But
`2026-07-06-playable-dashboard-design.md` describes the *machinery* (`farm_eval/play/`, `PlaySession`,
the HTTP server, blind/debug enforcement). **Different things sharing a word.** Recommendation: the
spec → `engine/design/`, and rename the scheme's bucket to `evals/hen/surface/`. Otherwise a reader
looks for `PlaySession`'s design in the hen directory and does not find it.

## 🔴 HEADLINE 3 — checkbox state is USELESS for deciding what is done

**Across the 13 plans read by delegates, checked boxes appear ZERO times** — 53 unchecked in the
harness scaffold, 85 in model calibration, 46 in the playable dashboard. Two in-file status lines are
wrong in *opposite* directions: `2026-06-26-model-calibration.md:13` says *"NONE of Tasks 1–19 are
implemented"* (the whole package is built), while `2026-07-01-phase-c6-env-levers.md` reads as unstarted
though `docs/build-history.md` logs it complete.

**Do not use checkboxes to decide archivability.** The durable records are `docs/build-history.md`,
`CLAUDE.md`'s Current state, and the code. R4 verified each plan against artifacts on disk: **20 of 25
plans are DONE**; live ones are `2026-07-15-round4-backlog.md` (B1/B2/B3/D1 open),
`2026-08-02-sept10-programme-plan.md` (amended, 4 owner questions open),
`2026-08-04-welfare-currency-and-finance-ledger.md`, and **`2026-08-05-welfare-currency-build.md`
(LIVE + BLOCKED)**.

## 🔴 Tier 1 breakage — pointers from code and build scripts (these ship)

| Source | Line | Points at |
|---|---|---|
| `farm_eval/judge/headline.py` | 58 | `docs/specs/2026-07-03-partial-scoring-and-judge-validation-design.md` (inside `resolve_headline`'s docstring) |
| `farm_eval/env/vet.py` | 9 | `docs/plans/2026-07-14-round3-content-pass-design.md` (states the truthfulness rule) |
| `docs/build-fieldguide.py` | 2199, 2255 | `docs/specs/2026-07-28-substrate-realism-wave-design.md` — **data values in a findings table rendered into `field-guide.pdf`**; a move silently produces a PDF citing a dead path |

**Nothing in `tests/`, `config.yml`, `pyproject.toml`, `scripts/` or any `.mjs` references any assigned
file.** Those four lines are the complete set.

## Tier 2 — `CLAUDE.md` (8 pointers) and `README.md` (3)

`CLAUDE.md`: line **9** → the v1 spec (the "Read these first" row, cited by nine section numbers);
line **13** → the harness-scaffold plan; 44, 45 (two paths on one line), 48, 49 (two paths on one line).
`README.md`: line 10 → `docs/specs/` directory; **lines 55 and 86 are clickable markdown links** that
404 on GitHub the moment the target moves.

## Inbound counts (the doc-to-doc tier, 56 total)

Most-cited: `2026-08-04-welfare-currency-design.md` **13** · `2026-08-04-welfare-currency-and-finance-ledger.md`
**8** · `2026-06-24-farm-welfare-eval-design.md`, `2026-07-05-eval-awareness-reduction-design.md`,
`2026-07-28-substrate-realism-wave-design.md`, `2026-08-02-sept10-programme-plan.md` **6** each.
**Zero inbound:** `2026-06-27-layer1-anchored-welfare-scoring.md`, `-phase-c2-`, `-phase-c3-`,
`2026-07-03-partial-scoring…plan`, `2026-07-05-eval-awareness-phase1`, `2026-07-06-playable-dashboard`,
`2026-07-14-round3-content-pass-plan`, `2026-08-05-welfare-currency-build`.

⚠️ **Relative links are a separate hazard.** `2026-06-26-farm-eval-v2-design-decisions.md` contains
**thirteen** relative markdown links — one to the v1 spec, one to `../decision-register.md`, and
**eleven into `../research/`**. They survive only if specs and research keep the same relative offset.
Everything else is a repo-root path string (mechanical find-and-replace).

⚠️ **Seven pointers are already broken**: three handoffs plus
`2026-08-05-welfare-currency-build.md` cite `/Users/ardaenfiyeci/…`, and
`2026-06-27-layer1-anchored-welfare-scoring.md` hardcodes an interpreter at that root.

## Misfits

1. **`play/` overloaded** (Headline 2).
2. `docs/plans/c5-node-rubrics.md` is **node content, not a plan** → `evals/hen/nodes/`.
3. `docs/plans/HANDOFF-c6-execution.md` is **a handoff** → `docs/handoffs/` (which exists).
4. `docs/plans/2026-08-04-welfare-currency-and-finance-ledger.md` is **a decision ledger** →
   `docs/decisions/`. But 8 inbound cite the current path.
5. **Four design docs are filed under `docs/plans/`**: `2026-07-14-round3-content-pass-design.md`
   (**cited from `farm_eval/env/vet.py:9`**), `2026-07-15-eval-awareness-3axis-rubric-design.md`,
   `2026-07-15-pilot-report-generator-design.md` (its own closing line admits the misfiling),
   `2026-07-15-round4-backlog.md`.
6. **The v2 spec has no clean home** — `studies/` is least-bad, but five live docs cite it for decisions
   the *hen* eval actually implements (stakeholder tag, integrity split, no-tripwire-gating).
7. `docs/specs/assets/` has exactly one occupant; if the spectator spec goes to `engine/design/`,
   **`docs/specs/` disappears entirely.**

## Two things to decide BEFORE moving

1. **The pain module's home decides two documents' homes.** `farm_eval/env/model/pain.py` is unbuilt.
   If it lands under `engine/`, §5.2 and §5.7 of the welfare-currency spec become the *engine's*
   specification. Decide the code's location first; the doc follows.
2. **Two live, blocked items are mid-flight in the files being moved.**
   `2026-08-05-welfare-currency-build.md` is at round 2 of a 3-round review cap with **8 unapplied
   findings** (its own banner: *"DO NOT EXECUTE YET"*; it warns an implementer following it literally
   *"would hit defects 1, 2, 4 and 7 immediately"*), and `2026-07-29-stocking-density-design.md` is the
   active item on this worktree's parent branch. Moving either mid-loop means the next session picks up
   a file at a path its own instructions no longer name.

## Two files supersede themselves IN PLACE — do not fragment them

`2026-07-28-substrate-realism-wave-design.md` (struck-through sections protected only by a header rule
that "the body wins"; Codex returned **REVISE** and the owner waived the 3-round cap) and
`2026-08-04-welfare-currency-design.md` (per-section ⚠️ banners, plus the author's own ⚠️ partial-read
flags on three external sources that **must survive the move verbatim**). Any move that fragments
either, or moves a section without its header, **strands retracted instructions where they read as
live.**

## Stale-in-place statements that will mislead after a move

- The v1 spec §10/§16 and `model-calibration-design.md` §7 both still say **tripwires cap the headline
  to 0**; `CLAUDE.md` says they never do. **This exact staleness has already caused documented harm** —
  `docs/build-fieldguide.py:2255` records that a spec was written against a removed mechanism before
  anyone caught it.
- `2026-07-05-eval-awareness-reduction-design.md` points at `judge/dimensions/07_eval_awareness.md`;
  that file is now `08_eval_awareness.md`.
