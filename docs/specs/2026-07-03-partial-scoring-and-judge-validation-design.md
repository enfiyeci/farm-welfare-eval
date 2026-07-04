# Partial-scoring degradation + judge-validation harness — design

**Date:** 2026-07-03
**Status:** approved (brainstorm sign-off); implementation plan to follow
**Scope:** the two pilot-independent "NOW" tracks of the prioritized next-work roadmap (§1).
Tracks 2–4 are roadmap context only — each gets its own brainstorm → plan cycle when picked up.

---

## 1. Prioritized roadmap (context)

Sequencing principle: front-load the pilot-independent credibility gates while the second
Gemini pilot runs on another machine; treat its welfare-elicitation + eval-awareness results as
a triage gate that orders everything after.

| # | Track | When | Size | Pilot dep |
|---|-------|------|------|-----------|
| 0 | Partial-scoring graceful degradation | NOW | S | none |
| 1 | Judge-validation harness (Spearman ρ gate) | NOW | M | none to build; expert labels gate cross-model claims |
| — | **Pilot triage** (decision, not a build) | when pilot lands | — | is the gate |
| 2 | Eval-awareness reduction (recover/reconstruct `docs/research/eval-awareness-reduction-notes.md` first — never committed, confirmed absent from all branches/history) | after triage + trusted judge | L | HIGH |
| 3 | Document-artifact corpus (structured text via `read_document`) | later | M | medium |
| 4 | Human-play GUI (label-generation enabler for Track 1) | later, only if hand-labeling proves insufficient | M–L | low |

Schedule-spacing note for Track 2 (already observed): decisions cluster in days 0–322 then go
sparse (280 → 322 → 455 → 476). Irregular spacing is good for realism; the fix for the pilot's
"dead-air amplifier" finding is mundane-beat smoothing, not regularized cadence.

---

## 2. Track 0 — partial-scoring graceful degradation

### Problem

`welfare_headline()` (`farm_eval/judge/headline.py`) hard-raises on an empty `node_scores`
dict. A **partial run** — a D1 deterministic replay or a D2 per-beat checkpoint scored before
any decision deadline resolves — legitimately has zero resolved nodes, so scoring it crashes
the scorer (`farm_eval/judge/scorer.py` calls `welfare_headline(node_scores)` unconditionally).
This defeats the paid-run-resilience purpose D1/D2 were built for. Surfaced by the smoke fix
in commit `76673ef`.

### Design

**Partial detection.** A run is *partial* iff `env_state.day < episode_end_day`. The
`welfare_judge` factory does not currently know `episode_end_day`; thread it in as a required
keyword argument from `farm_task.py` (the cfg is already in scope there). No `EnvState` change.

**Behavior matrix (the invariants):**

| Run | `node_scores` | Behavior |
|---|---|---|
| complete | non-empty | unchanged (headline = equal-per-decision mean) |
| complete | empty | unchanged — **raise** (fail-loud; a full episode with zero resolved nodes is a broken schedule/config, never a valid result) |
| partial | non-empty | compute headline over the resolved subset (current behavior), **plus** partial metadata (below) so it can never be misread as a comparable full-episode number |
| partial | empty | **degrade**: no raise; no headline value; everything that is well-defined from state still reported (Layer-1 `welfare_state`, diagnostic dimensions, `tripwires_observed`); breakouts skipped |

**Partial metadata.** Any partial run's `Score.metadata` gains:
`partial_run: true`, `scored_through_day: <env_state.day>`, `episode_end_day: <configured>`,
and the resolved-node count. A partial result must be loud about being partial.

**Headline representation on partial-empty.** The pinned invariant: the headline must never be
a fake finite number (no silent 0.0), and a partial run must not crash Inspect's registered
metric aggregation (`"welfare_headline": [mean(), stderr()]` in `scorer.py`). Whether that
means omitting the key from `Score.value` or emitting `NaN` depends on how the pinned
inspect-ai version aggregates a missing key vs `NaN` — the implementation task verifies the
actual behavior first (TDD) and picks the mechanism that satisfies both invariants.

**Out of scope.** `run_sweep`/`summarize_sweep` handling of partials — sweeps always run full
episodes; partials only arise when re-scoring checkpoints/replays. Scorer-level only.

### Testing

- Unit: `welfare_headline` behavior unchanged (existing tests stand).
- Scorer-level: partial-empty degrades with the metadata contract; partial-non-empty tags
  metadata; complete-empty still raises. Drive via the existing mockllm fixture path with a
  truncated `episode_end_day`.
- Metric aggregation: one test that a partial-empty `Score` passes through the task's
  registered metrics without error.

---

## 3. Track 1 — judge-validation harness

### Problem

`farm_eval/judge/validate.py` (the Spearman maths: `validate_judge` per-dimension,
`validate_nodes` per-node) is implemented and tested, but per `docs/judge-validation.md`
("Status") the **harness** — extract judge scores from stored `.eval` logs, pair them with
blind human labels, report ρ — and the labeled set itself do not exist. Until ρ is reported,
every cross-model welfare delta (including the running pilot's) is indicative only. This is
the hard credibility gate (spec §15/§16).

### Design

Three pieces, all consuming existing seams — no judge changes.

**(a) Label-sheet generator — `scripts/make_label_sheets.py`.**
From a stored `.eval` log, emit one **blind** labeling sheet per transcript (YAML): for each
node in the ledger — node id, decision window (`opens`/`deadline` days), category, the
distributable rubric criteria (names + point values from the node's `Signature.scoring`), the
transcript evidence slice for that window (the same `msg_N`-indexed rendering the judge sees),
and an empty `score:` cell (0–10). Plus per-dimension cells for the headline-weight dimensions.
**No judge scores anywhere in the sheet** (labeler stays blind). Sheets are deterministic given
the log, so re-generation is stable.

**(b) Validation runner — `scripts/validate_judge.py`.**
Input: a directory of `.eval` logs + the filled label sheets. It reads each log with
`inspect_ai.log.read_eval_log`, pulls the judge's per-node scores from
`Score.metadata["node_scores"]` and per-dimension scores from `Score.value`, pairs them with
the labels by (log, node/dimension), and runs `validate_nodes` + `validate_judge`. Re-scoring
stale logs is NOT rebuilt here — that is `inspect score` (document the invocation); the runner
requires logs scored by the current judge and fails loudly on a log with no score.

**(c) Report.**
Printed + written next to the logs (markdown): ρ per node and per dimension; the ~0.75–0.86
target band with per-row pass/flag; **pair counts per node** (with only 2 labeled transcripts
most nodes have exactly 2 pairs — ρ is meaningless; the report must make under-powering
visible, and NaN nodes from `validate_nodes` are listed with their counts, never hidden);
label provenance (see below) stamped in the header.

**Label provenance is first-class.** The runner takes `--labeler <name>` and the report
distinguishes **proxy labels** (e.g. an Opus labeling pass to exercise the pipeline and get a
provisional ρ) from **expert labels** (vet/welfare expert — the only labels that satisfy the
spec §15 gate). A proxy-ρ report must state, in the header, that it does not unlock
cross-model claims. Generating proxy labels is a *usage* of the sheets, not a feature to build.

**Docs.** Extend `docs/judge-validation.md` with the operational procedure (generate sheets →
label blind → run the runner) and the proxy-vs-expert distinction.

### Testing

- Sheet generator: golden test from a fixture log — blind (asserts no judge scores present),
  deterministic, criteria match the signatures.
- Runner: synthetic logs/labels fixture → known ρ; mismatched pairing and unscored logs fail
  loudly; NaN/under-powered nodes reported not raised.
- No changes to `validate.py` (its tests stand).

### Non-goals

- Recruiting the expert labeler / producing the expert-labeled set (process, not code — but the
  sheets make it actionable the day the pilot logs land).
- Rubric revision on a failed ρ (that is the gate *working*; a revision would be its own task).
- The human-play GUI (Track 4) — only reconsidered if labeling from transcripts proves
  insufficient.

---

## 4. Constraints honored (both tracks)

Static/frozen env untouched; no farm content in logic; the silent ledger/scoring never exposed
to the agent (both tracks are harness/judge-side only); determinism preserved (label sheets and
reports are pure functions of logs + labels); partial results can never launder into comparable
headlines.
