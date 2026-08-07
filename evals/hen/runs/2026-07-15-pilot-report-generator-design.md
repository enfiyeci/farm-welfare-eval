# HTML pilot-report generator — design

**Date:** 2026-07-15 · **Status:** owner-approved design (brainstorm) · **Branch:** `fix/pilot-round2-harness` or a child
**Related:** `docs/research/eval-report-design-deep-research-prompt.md` (best-practice inputs, pending),
`docs/pilot-debrief-protocol.md` (the protocol this report operationalizes),
`evals/hen/runs/pilot-debrief-2026-07-15-gemini-3.1-pro-round3.md` (the current markdown debrief this replaces/augments).

## Goal

Generate one **self-contained, dual-audience HTML report per pilot run**, auto-filled from the
`.eval` log, with hand-written narrative slotted from a per-run sidecar. Every future pilot gets a
flawless quantitative report for free; the human writes only the prose that needs judgment. The
report must read cleanly for a stakeholder **outside the lab** (plain-language top layer) while
carrying full technical depth for the team (progressive disclosure).

## Non-goals (v1)

- Not a live dashboard; a static (but interactive-in-browser) artifact per run.
- Not a replacement for the `.eval` log or the judge; a presentation layer over them.
- No external network at view time (self-contained HTML, no CDN — same constraint as artifacts).

## Architecture

Package `farm_eval/report/` + entry point `scripts/gen_pilot_report.py`:

```
scripts/gen_pilot_report.py <this.eval> [--vs <prior1.eval> <prior2.eval> ...] \
    [--narrative <sidecar.md>] [--out <path.html>]
```

Three stages, each independently testable:

1. **extract** (`farm_eval/report/extract.py`) — read the `.eval` via `inspect_ai.log.read_eval_log`
   and flatten into ONE plain-dict **report model** (JSON-serializable). Pure; no rendering. This is
   the golden-fixture boundary (a stored `.eval` → expected report-model dict).
2. **analyze** (`farm_eval/report/analyze.py`) — derive series/aggregates from the report model:
   tool-usage-by-type and over-time, engagement curve, out-of-world-address count, decision
   latencies, and — when `--vs` logs are given — cross-run deltas. Pure functions.
3. **render** (`farm_eval/report/render.py` + `templates/`) — report model + analysis + narrative
   sidecar → one self-contained HTML string. Charts are **inline SVG** built by a small
   `charts.py` helper (no matplotlib in the output path, no JS charting lib); interactivity
   (collapse / filter / sort / jump-to-anchor) is hand-written vanilla JS inlined in a `<script>`.
   CSS inlined in `<style>`, theme-aware (light/dark via `prefers-color-scheme`).

### What is extractable from the log (verified 2026-07-15 against the round-3 `.eval`)

- **Directly available** (all carry `day`): `actions` (536; `{tool, params, day}`), `reads` (312;
  `{tool, params, day}`), `event_log` (338; `{day, type, links_dp}`), `outbound`/`mailbox`,
  `ledger`, and the judge score + metadata (`node_scores`, `dimension_notes`, `criterion_notes`,
  `cue_localization`, `discarded_evidence`, `stakeholder_breakout`, `category_breakout`,
  `welfare_state`, `welfare_state_channels`, `recognition`). Transcript via `sample.messages` with
  the same `msg_N` indexing the judge cites.
- **CONSTRAINT — Layer-1 welfare is a FINAL snapshot only.** `welfare.harm` is a single end-of-run
  accumulator (`nh3_ppm_hours_over`, `excess_mortality`, `keel_risk_hours`, …), NOT a per-day
  series. Therefore **§7 (welfare trajectory) v1 = the endpoint harm-channel breakdown** (a labeled
  bar/hbar of the final accumulators, normalized where sensible) **plus an APPROXIMATE
  observed-welfare-over-time series scraped from the model's own flock-report / sensor read-tool
  RESULTS in the transcript** (i.e., what the operator saw when it read, sampled at read times).
  A true continuous re-integrated trajectory (replaying the env from seed+actions) is a **v2
  stretch**, explicitly deferred — do not block v1 on it.

## Dual-audience via progressive disclosure

One page, three depths:

- **Outside-reader layer (always visible):** executive verdict in plain language; a "How to read
  this report" block; a collapsible glossary (headline, node, tripwire, Layer-1, eval-awareness,
  etc.); every section opens with a plain-language lead sentence. An outside reader goes top-to-
  bottom and understands it without knowing "DP12" or "Layer-1".
- **Team layer (one click):** per-node cards expand from a plain summary line to full detail; charts
  hover for exact values; tables sort/filter.
- **Audit layer (appendix):** reproducibility header, judge-QA discards, curated quote appendix.

## Section structure (v1)

| # | Section | Source | Audience lead |
|---|---|---|---|
| 1 | Executive verdict | auto (+1 sidecar line) | plain-language headline, tripwires, deltas vs all prior rounds, top-3 findings, "does this change our conclusions?" |
| 2 | How to read this / glossary | static template | plain |
| 3 | Cross-run comparison | auto (`--vs`) | which nodes/dimensions moved and why; paired email quotes where the sidecar supplies them |
| 4 | Behavioral portrait | **sidecar prose** | narrative with receipts (identity, arc, humor/politeness, belief ledger, timeline) |
| 5 | Odd-behavior spotlights | **sidecar prose** | anomalies with quotes |
| 6 | Tool-usage & engagement analytics | auto (charts) | plain lead + charts vs prior runs |
| 7 | Welfare-state (Layer-1) | auto (charts) | endpoint harm breakdown + approx observed-welfare series (see CONSTRAINT) |
| 8 | Per-node cards | auto (+ sidecar verdict notes) | collapsible; plain line → cue, reference policy, evidence, grader rationale, model-vs-harness verdict |
| 9 | Measurement-integrity / judge-QA | auto | discards (incl. realism quote-fidelity), variance, headline-math check, trust callouts |
| 10 | All-rounds trend | auto (running-history JSON) | headline + key dimensions across every pilot to date |
| 11 | Disposition table | **sidecar** (findings/dispositions) | fix/accept backlog |
| 12 | Reproducibility header + appendices | auto | log path+sha, model pair, branch/commit, runtime, tokens, cost, node set, config |

**All-rounds trend (§10) mechanism:** the generator maintains a committed
`docs/probes/pilot-history.json` — one row per run keyed by log sha256 (headline, dimensions,
tripwires, model, date). Each run **appends idempotently** (re-running the same log overwrites its
own row, never duplicates). The trend chart reads this file, so it shows every pilot to date without
needing every prior `.eval` on disk. A `--no-history-write` flag renders without appending (for
dry runs).

**Deferred to v2** (promote on request): communication/tone analysis, decision-latency view,
welfare-vs-profit position, stakeholder/category breakout panels (data is in metadata — cheap to
add), severity-weighted headline, re-integrated continuous welfare trajectory.

## Narrative sidecar

`docs/probes/pilot-report-<date>.narrative.md` with fenced, named sections the renderer reads by
heading, e.g. `## executive_summary`, `## behavioral_portrait`, `## odd_behaviors`,
`## node_verdicts` (per-node one-liners keyed by dp_id), `## dispositions`. Missing section →
visible "✍️ write me" placeholder in the HTML (report still renders). The existing round-3 markdown
debrief is the seed content for the round-3 sidecar.

## Chart set (all inline SVG, theme-aware, light+dark)

Per the `dataviz` skill's palette/rules (load it at render-implementation time):
- Tool-usage by type — horizontal bars, this-run vs each `--vs` run as small multiples or grouped.
- Tool-usage over in-world time — line/area, calls-per-day bucketed; overlay prior runs.
- Engagement/attention curve — reads-per-day over the episode with the late/early drop-off marker.
- Welfare endpoint harm channels — normalized hbar.
- Approx observed-welfare-over-time — line per key metric (ammonia, mortality) sampled at reads.
- Per-node score strip — 22 nodes, score + judge-variance whisker; color by category.
- Cross-run deltas — slopegraph or diverging bars (node/dimension moved up/down).
- All-rounds trend — headline + key dimensions across rounds.

Every chart: `overflow-x:auto` container, relative units, no horizontal page scroll, exact values on
hover, accessible contrast in both themes.

## Testing

- **Golden report-model fixture:** a committed small `.eval` (or the round-3 log) → expected
  `extract()` dict (key subset), so extraction can't silently drift.
- **analyze() unit tests:** tool-count-by-type, per-day bucketing, out-of-world-address count
  (matches the debrief's R3≈8-strict), cross-run delta math, latency computation.
- **charts smoke tests:** each chart fn returns well-formed SVG (parses; no `NaN`/`Infinity` in
  coords; renders with empty/degenerate series).
- **render end-to-end:** round-3 log → a single self-contained HTML that (a) contains no external
  URLs, (b) parses as HTML, (c) shows "✍️ write me" when the sidecar is absent, (d) works in
  single-run mode (no `--vs`).
- No new corpus/judge coupling; `scripts/lint_corpus.py`, the golden baseline, and `replay_f1`
  must stay untouched and green (this is a read-only presentation layer).

## Process

Build task-by-task per the implementation plan (next: `superpowers:writing-plans`), TDD, Codex
review pair per change (global rule). Spec + plan live under `docs/plans/` (repo convention, not the
skill default).
