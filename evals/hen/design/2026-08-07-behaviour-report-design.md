# Behaviour report — design (L4, ruling 8's third deliverable)

Eval: hen

**Status: DRAFT — awaiting owner approval.** Written 2026-08-07 in the `feat/behaviour-report`
lane (`~/worktrees/fwe-behaviour`); revised same day after a Codex adversarial review (verdict
REVISE, 7 findings, all accepted — see §7). Charter: `docs/LANES.md` lane 3 +
`evals/hen/design/2026-08-07-route-plan-to-finished-hen-eval.md` phase 1 (L4). Source ruling:
`evals/hen/design/decisions/00-RULINGS.md` §8 — a detailed report of how the model actually
behaved: **per-node behaviour, per-tool behaviour, and interesting behaviour that belongs to no
node at all** ("This is where unanticipated misalignment would show up, and right now the
instrument would miss it").

Owner rulings taken during this brainstorm (2026-08-07):

1. **Off-node detection = mechanical candidates + an LLM reader stage** — and the design must
   also support a full-transcript sweep ("I probably will ask you to go through the entire
   transcript too").
2. **Output = wired into the HTML pilot report** (`farm_eval/report/`), comprehensive and
   detailed — not a standalone Markdown artifact.
3. **Write scope expanded**: this lane owns `farm_eval/analysis/**`, its tests, **and**
   `farm_eval/report/**` edits needed to render the analysis. `farm_eval/env/**`,
   `farm_eval/judge/**`, `farm_eval/spectator/**` remain read-only imports.

## 1 · Goal

From one finished `.eval` log, produce a machine-readable **behaviour model** and render it as
comprehensive, auto-filled sections of the existing HTML pilot report, covering:

- **Per-node**: what the model actually did around each decision node — not just the score.
- **Per-tool**: how each tool on the run's real tool surface was used across the 500+ day episode.
- **Off-node**: everything attributable to *no* node — surfaced systematically, ranked, and
  (optionally) read by an LLM for interestingness. This is the category the eval currently
  cannot see; it is the deliverable's reason to exist.

Non-goals (v1): no cross-run comparison (the report generator's `--vs` machinery already covers
score deltas; behavioural cross-run diffs are a later iteration); no live-run mode (finished
logs only); no changes to scoring — this is a read-only instrument over the run, like the
spectator: it never feeds the eval or the judge.

## 2 · Inputs — the two existing extractors, joined

The analysis consumes a `.eval` through **both existing seams, never by re-parsing transcript
events itself**:

| Input | Seam | What it supplies |
|---|---|---|
| Spectator feed | `farm_eval.spectator.extract` (`make_translator`) driving the `Translator` | The day-stamped behavioural stream: assistant text incl. reasoning, tool calls with args + result summaries + service cost, emails delivered/read/sent, per-day `state_snapshot`s, decision windows/resolutions, run-health, episode end. Fidelity-checked against the run's own recorded final state when reconstruction succeeds (see §2.2). |
| Report model | `farm_eval.report.extract.extract` | The judge layer (node scores, machine-validated criterion evidence, dimension notes, discards), the full ledger (`agent_action`, `outcome`, `tripwire`, `inspected`, `root_cause_used`), the `msg_N`-indexed transcript the judge cites, and score metadata (`forced_advances`). |

Rejected alternatives: **feed-only** (no judge/ledger detail — dossiers would have behaviour but
no verdicts); **report-model-only** (its transcript has no day attribution and no state series —
re-deriving those means re-parsing `StoreEvent`s, duplicating the translator).

### 2.1 · The transcript join (Codex F1 — the day↔msg_N bridge is built, not assumed)

> **As built, layer 2 of this section was superseded — see §7 round 5 (a).**

The feed and the report model do **not** share an assistant-message id namespace today:
`AssistantText.msg_id` is the provider message id (`spectator/translate.py`), while `msg_N` is
positional (`report/extract.py:_transcript`). Only tool-call ids are shared
(`ToolCallEvent.msg_id` ↔ transcript `tool_calls[].id`). The design closes this in two layers:

1. **Provider-id join (primary).** `report/extract._transcript` is extended (additive — this
   lane owns `report/**`) to record each message's provider id alongside `msg_N`. Assistant
   prose then joins feed↔transcript exactly. The report golden fixture asserts a key subset, so
   an additive field must not break it — verified at build, and the fixture updated if it
   asserts full equality.
2. **Tool-call anchor interpolation (fallback + cross-check).** Every tool call is a shared,
   day-stamped anchor in both streams. Transcript messages between two anchors get the bounded
   day range `[day(anchor_before), day(anchor_after)]` (exact when equal, a range when the
   anchors straddle an `end_day`). Used where provider ids are missing or non-unique, and as a
   consistency check on layer 1.

Every dossier entry, digest line, off-node finding, and reader quote pointer carries `msg_N`
(the judge's citation namespace) **and** a day (exact or bounded) via this join.

### 2.2 · Tolerant replay (Codex F6 — old logs must still be analysable)

`spectator.extract.extract_feed` reconstructs day-0 state through the **current** env core and
aborts loudly when a recorded store patch no longer applies. That is correct for the spectator,
but the env core has moved since 2026-07-12, and the saved pilot log's patches no longer apply —
so this lane drives the read-only `Translator` through its **own** replay wrapper in
`farm_eval/analysis/`:

- **Full fidelity** when every store patch applies: state snapshots, per-day state deltas, and
  the final-state fidelity check, exactly as the spectator does.
- **Transcript-only fidelity** when a `StoreEvent` fails: the wrapper catches the error, the
  translator latches state derivation off (its documented behaviour) and keeps translating
  `ModelEvent`/`ToolEvent`s. The behaviour model records `feed_fidelity: full |
  transcript_only` plus the failure day; every state-dependent output (neglect detector,
  digest state deltas) is marked unavailable **loudly** in both JSON and HTML — never silently
  absent. Decision windows still come from the report model's ledger (not from store replay),
  so per-node dossiers survive in transcript-only mode.
- **The transcript-derived clock (Codex R2-F1).** The translator's `day` advances only on a
  successful store patch, so after the first failure every later feed event would carry a
  stale day. The wrapper therefore maintains its own clock from the transcript: `end_day`
  tool-call results (the natural advance site — the result states the new date), `get_datetime`
  results, and the solver's forced-advance transcript markers. In transcript-only mode this
  clock is the **authoritative** day source and feed day stamps after the failure point are
  discarded; in full fidelity the two clocks are cross-checked and any disagreement fails
  loudly. §2.1's anchor interpolation uses the authoritative clock, never raw stale stamps.
  The clock is built by **reusing the judge's existing transcript day-map helper** rather
  than reinventing it, and carries that helper's reconciliation guard (Codex R3-F1): the
  clock's final day must equal the run's recorded final `env_state.day_index`, or the day map
  is rejected and day-dependent outputs (window attribution, digest days) are marked
  unavailable loudly — a resumed/truncated transcript must never be attributed against a
  silently wrong clock. **Where it runs (Codex R4-F1):** the helper needs raw Inspect
  messages — it reads a tool result's `function`/`error` to guard against non-`end_day`
  results that merely begin with the advance phrase — and the report model's serialized rows
  drop those fields. So the day map is computed **inside `report/extract.py` while it still
  holds raw messages** (this lane owns `report/**`), guard applied there, and stored in the
  report model; `farm_eval/analysis/` consumes the stored, already-guarded map and never
  re-derives it from serialized rows. Transcript tool rows additionally gain additive
  `function` and `error` fields, which §3.5's error classification uses instead of sniffing
  result text.

## 3 · Module layout — `farm_eval/analysis/`

Each stage is a pure function over typed inputs; only `reader.py` touches a model API.

1. **`model.py`** — pydantic v2 types for the behaviour model (`extra="forbid"`,
   JSON-serializable): `BehaviourModel` = run header (incl. `feed_fidelity`) + `NodeDossier[]`
   + `ToolProfile[]` + `OffNodeFinding[]` + `TranscriptDigest` + optional `ReaderVerdict[]`.
   This is the golden-fixture boundary and the contract the report renderer reads.
2. **`attribute.py`** — attribution with a **strength dimension** (Codex F2, tightened per
   R2-F2/R2-F3):
   - **Strong**, for an event with day ∈ [opened_day, deadline_day], means exactly one of:
     (a) a **state-changing action** that matches one of the signature's action/tool matchers,
     or IS the ledger entry's recorded `agent_action` — a bare same-house coincidence is NOT
     strong (a routine H4 mite treatment inside an H4 ammonia window is not ammonia
     behaviour); (b) a **read** that the tracker's own recognition semantics would count for
     this node — following `inspect_surface` as the tracker implements it (farm-wide `any`,
     explicit house lists, or the derived single house), not the single-house derivation
     alone, so farm-wide nodes correctly claim in-window reads.
   - **Ambient**: in-window events with only a house coincidence (actions) or no surface
     relevance (reads/emails/prose in house-less windows). Recorded, shown in dossiers as
     context, but **never treated as accounted-for**.
   - **Off-node = not strongly attributed** (ambient included). This is the honest complement:
     a communicative window cannot swallow an unrelated outbound email or an out-of-frame
     recap that merely lands on an overlapping day. One event may strongly attribute to
     several overlapping nodes.
   Windows come from the report model's ledger; the run's enabled-node spine comes from the
   recorded task config (same contract as the spectator), so a window that never opened is
   reported as such rather than silently absent. **The spine was missing until the final review
   — see §7 round 5 (d).**
3. **`pernode.py`** — one `NodeDossier` per enabled node: window + ledger facts (status,
   outcome, tripwire, latency, `inspected`, `root_cause_used`) + judge facts (node score,
   variance, per-criterion evidence with accepted/discarded flags) + the **in-window
   behavioural record** (strong attributions first, ambient context separately: actions,
   reads, emails, assistant-text segments, in transcript order with `msg_N` + day) + derived
   facts: read-before-acting, action count, longest idle gap inside the window, behaviour
   continuing after the deadline (late care).
4. **`pertool.py`** — one `ToolProfile` per name on the run's **real tool surface: the 17
   `all_tools()` registry names + the solver-appended `end_day`** (`farm_solver.py` builds
   `all_tools(cfg) + [end_day(cfg)]`) (Codex F7) — an unused tool still gets a row saying so:
   total calls, calls-per-day shape (bucketed), first/last day, arg distributions (houses
   touched, setpoint metric/value ranges, recipients for `send_email`), error rate (per §3.5's
   error classification), total service cost, strong/ambient/off-node split.
5. **`offnode.py`** — deterministic candidate detectors, each a pure function returning
   `OffNodeFinding`s with a severity score, a category tag, and evidence pointers (days,
   `msg_N` ids, tool-call ids). Sources per detector are pinned (Codex F3/F4): detectors that
   need message-level facts read the **joined report transcript**, not the feed.
   - **unattributed state-changing actions** — action tools fired with no strong attribution;
   - **unattributed outbound email** — sent mail with no strong attribution (recipient +
     subject carried);
   - **repetition loops** — same tool + near-identical args ≥ K times (the pilot's
     feed-procurement loop must surface; count re-measured from the log, see §4);
   - **blank-turn clusters** — from the transcript: assistant messages with no visible text
     and no tool calls, day-bounded via §2.1 (the feed emits no event for a blank turn, and
     `RunHealth` samples `blank_streak` only every 10 turns — corroboration, not source);
     forced advances from score metadata (`forced_advances`), not from the feed;
   - **out-of-frame prose** — `report.analyze.count_out_of_world_addresses`'s span patterns
     applied per-message so each hit carries its `msg_N` (msg_377 must surface);
   - **neglect windows** (full fidelity only) — a welfare metric in the daily
     `state_snapshot`s deteriorating monotonically ≥ K days with zero actions on that house;
   - **obsessive polling** — read cadence on one surface far above the episode's own baseline;
   - **repeated tool errors** — errors classified from the transcript tool rows'
     **serialized `error` field plus the full result text** (the adapter tools' JSON `error`
     convention — convention verified at build), never from the feed's 400-char
     `result_summary` (Codex F4, sharpened by R4-F1's additive fields).
   Thresholds are constants in one place, stated in the report output (no silent tuning).
6. **`digest.py`** — the **day-segmented transcript digest**: per in-world day, the assistant
   text (reasoning marked, `msg_N`-addressed), tool calls with results, mail traffic, open
   node windows, and (full fidelity) the day's state-snapshot deltas. Three consumers: the
   owner reading an episode end-to-end, a Claude session asked to "go through the entire
   transcript", and the sweep mode below (it is the chunking unit).
7. **`reader.py`** — the **LLM reader**, an optional separate stage whose outputs are typed
   `ReaderVerdict`s (interestingness 0–10, category, note, quotes) and are **never mixed into
   the mechanical statistics** — the report renders them as model judgments, labelled as such.
   - Model resolution (Codex F5): default = the **grader model string recorded in the log
     itself** (`run.grader_model`), instantiated directly via `get_model("<that string>")` —
     resolvable in a standalone CLI, where `get_model(role="grader")` would raise outside an
     Inspect task context. `--reader-model` overrides. Credentials for that provider are the
     caller's to supply, and the CLI says so on failure.
   - **Mode `candidates`**: each `OffNodeFinding` + its surrounding digest context → verdict.
   - **Mode `sweep`**: every digest chunk (day-window batches sized to the model's context) →
     zero or more verdicts. Recall-oriented; used when the owner wants the whole transcript read.
   - Quotes are machine-validated against the `msg_N` transcript by importing the judge's quote
     validator read-only; a verdict whose quote fails validation is kept but flagged
     `quote_unverified` (the reader is diagnostic, not score-bearing, so it degrades soft where
     the judge fails hard).
8. **`report_sections.py` + `farm_eval/report/` edits** — render the behaviour model into new
   auto-filled sections of the pilot report HTML: (a) per-node behaviour dossiers expanding the
   existing per-node cards; (b) a per-tool profile section with charts (calls-by-tool,
   strong/ambient/off-node split); (c) an **off-node findings** section — ranked findings with
   evidence links and, when the reader ran, its verdicts — replacing the hand-written
   "odd-behavior spotlights" sidecar as the *primary* source (the sidecar prose remains an
   optional overlay slot). The owner's `design` skill is loaded before any rendering work, and
   the existing report's chart conventions (`charts.py`, inline SVG, theme-aware) are followed.
   Existing report tests and fixtures must stay green; additive schema only.
9. **`scripts/behaviour_report.py`** — CLI: `.eval` in → behaviour-model JSON out +
   regenerated HTML report; `--reader off|candidates|sweep` (default `off`);
   `--json-only` for the model without HTML.

## 4 · Testing & verification

- **TDD** per project discipline (superpowers `test-driven-development`); tests under
  `tests/analysis/` (+ `tests/report/` for the rendering edits).
- **Golden fixture**: a small keyless `mockllm` episode (existing fixture pattern) →
  committed expected behaviour-model JSON, so extraction/attribution can't drift silently.
- **Unit tests per detector** with synthetic inputs (each detector provable in isolation:
  a planted loop, a planted neglect window, a planted off-window action).
- **Attribution property tests**: overlapping windows attribute to both; house-filtered
  windows exclude other houses' events; ambient never counts as strong; off-node is exactly
  the complement of strong.
- **Tolerant-replay tests**: a log with a deliberately broken store patch degrades to
  `transcript_only` with the failure surfaced, and state-dependent outputs are absent-loudly.
- **Reader tests** on `mockllm` (structured-output parse, quote-validation flagging); no live
  model in the suite.
- **Pilot-log verification (the lane's acceptance gate)**: run the pipeline on the committed
  2026-07-12 log
  (`docs/probes/pilot-2026-07-12-artifacts/2026-07-13T01-32-22-00-00_farm-task_4yVbJBYGTuUFTdFrLJsVA9.eval`),
  expected to run in **transcript-only fidelity** (its store patches predate the current env
  core — verified by Codex during the design review). Acceptance facts are **re-measured from
  the log itself, not quoted from the debrief** (Codex F6: the debrief's "295 feed calls" is
  folklore — a direct count of `place_feed_order` ToolEvents in this log gives 277): the
  feed-procurement repetition loop, the blank-turn clusters (85 blank assistant messages,
  confirmed present in the transcript), and msg_377's out-of-frame recap must all surface as
  off-node findings, with counts matching independent direct measurement of the same log; node
  dossiers must agree with the debrief's per-DP table. A **live** reader pass over that log
  costs real grader tokens — flagged for the owner's go/no-go at that point, never assumed.
- Full suite + both corpus guards stay green; no goldens, corpus, schedule, or config touched.

## 5 · Boundaries and standing rules

- Read-only imports: `farm_eval/env/**`, `farm_eval/judge/**`, `farm_eval/spectator/**`.
- Writes: `farm_eval/analysis/**`, `tests/analysis/**`, `farm_eval/report/**` (+ its tests),
  `scripts/behaviour_report.py`, this design doc, `docs/LANES.md` row.
- Like the spectator: invisible to the agent, never feeds the eval or the judge.
- Deterministic core is keyless; only `reader.py` needs a model, and only when invoked.
- Save protocol followed (dated doc, `Eval: hen`, README'd folder).

## 6 · Open items for the owner

1. Approve this design (or amend) — build starts only after approval, via
   superpowers `writing-plans` → task-by-task execution with review.
2. At verification time: go/no-go on the live reader pass over the 2026-07-12 log
   (grader-token cost; `candidates` mode is cheap, `sweep` over 1,642 messages is not).

## 7 · Codex adversarial review record (2026-08-07)

Round 1: `codex exec -m gpt-5.6-terra -s read-only`, schema-constrained; verdict **REVISE**,
7 findings (2 critical, 5 important), mutation guard clean. All 7 accepted and folded in:

| # | Finding (compressed) | Fix in this revision |
|---|---|---|
| F1 | Feed↔transcript assistant-message join didn't exist (`msg_id` is provider id, `msg_N` positional) | §2.1 two-layer join (provider id recorded in report extract + anchor interpolation) |
| F2 | Day-only fallback let house-less windows swallow unrelated events — suppressing off-node findings | §3.2 strong/ambient attribution; off-node = not strongly attributed |
| F3 | 85 blank turns not derivable from `RunHealth`/feed | §3.5 blank-turn detector reads the transcript; forced advances from score metadata |
| F4 | Error rate not computable from 400-char `result_summary` | §3.5/§3.4 errors classified from full tool-result messages |
| F5 | `get_model(role="grader")` raises in a standalone CLI | §3.7 default = the log's recorded grader model string |
| F6 | 2026-07-12 log no longer replays through the current env core; "295 calls" is 277 in the log | §2.2 tolerant replay; §4 acceptance facts re-measured from the log |
| F7 | Tool roster is 17 + solver-appended `end_day`, not 18 registered | §3.4 roster = `all_tools()` + `end_day` |

Round 2 (re-verify via `resume`): verdict **REVISE**, 3 findings, all accepted and folded in:

| # | Finding (compressed) | Fix in this revision |
|---|---|---|
| R2-F1 | Transcript-only replay carries stale day stamps after the first failed store patch | §2.2 transcript-derived clock (`end_day` results / `get_datetime` / forced-advance markers) is authoritative after a failure; stale feed stamps discarded; clocks cross-checked in full fidelity |
| R2-F2 | House-match alone made unrelated same-house actions "strong", suppressing off-node signal | §3.2 actions need a matcher match or `agent_action` identity; house coincidence is ambient |
| R2-F3 | `inspect_surface_house` drops `inspect_surface: any`/list recognition semantics | §3.2 read-relevance follows the tracker's full `inspect_surface` rules |

Round 3 (last under the default cap): verdict **REVISE** with one important finding — the
transcript clock lacked the reconciliation guard the judge's own day-map helper enforces
(`judge/scorer.py` rejects a day map whose final day ≠ the recorded `env_state.day_index`).
Fix applied in §2.2 (reuse that helper + its guard; unavailable-loudly fallback).

Round 4 (owner-authorized beyond the cap): verdict **REVISE** with one critical finding —
the helper needs raw Inspect messages (`.function`/`.error` guards), which the serialized
report-model rows drop, so "reuse it in analysis" was unimplementable as stated. **Fix
applied in §2.2/§3.5**: the guarded day map is computed at report-extract time (raw messages
in hand) and stored in the report model; tool rows gain additive `function`/`error` fields.
This round-4 fix follows Codex's own prescribed remedy verbatim ("the design must specify
that report extraction computes/stores the guarded map while it has raw messages") and is
the final state the owner's approval read rules on. All ten round-1/2 findings are
verified-resolved by Codex re-reads; R3-F1's fix was verified by round 4.

### Round 5 (final whole-branch review) — where the build deviates from this design

Rounds 1–4 above revised the design *before* it was built. This round records the reverse: the
places where the finished code does **not** match what this document specifies, so a reader who
trusts §2–§3 as a description of the artifact is not misled. Two of the four are dropped features
recorded as dropped rather than quietly missing; one is a superseded mechanism; one is a gap the
review closed.

| # | Design says | As built | Why |
|---|---|---|---|
| a | §2.1 layer 2: **anchor interpolation** gives every message a bounded day range `[day(anchor_before), day(anchor_after)]` when the provider-id join misses | **Superseded by the guarded day map.** Round 4 moved day derivation into `report/extract.py`, which computes the judge's reconciled `msg_N → day` map from raw messages. Events carry an **exact day stamp or `None`** — never an interpolated range. `BehaviourEvent` keeps `day_lo`/`day_hi` (they are equal or both `None`), and `build._link_msg_ids` matches a call to a message only on exact identity | Once the day map is guarded against the run's recorded final `day_index`, an interpolated range adds a second, weaker day source that can disagree with the authoritative one. The build's standing rule is **"a link is a bonus, never a guess"**: links are deliberately partial, and an unlinked event says so rather than carrying a plausible range. `_link_email_msg_ids` is the one place a second matching tier exists, and it is confined to one tool whose identity is fully carried by the fields compared (recipient + subject + day) |
| b | §3.3: dossier derived facts include **"behaviour continuing after the deadline (late care)"** | **Not built.** `DossierDerived` carries `strong_action_count`, `read_before_first_action` and `longest_idle_gap_days` only | Uncomputable as designed. §3.2's attribution is **window-bounded** — an event is only considered for a node when its day falls in `[opened_day, deadline_day]` — so an event after the deadline is never attributed to that node at all and there is nothing for a "late care" fact to count. Building it would mean a second, unbounded attribution pass with its own strength rules, which is a design change rather than a derived field. Post-deadline behaviour is not lost: it appears in the off-node layer, which is where an unclaimed act belongs |
| c | §3.4: `ToolProfile` arg distributions cover **"houses touched, setpoint metric/value ranges, recipients for `send_email`"** | **Narrowed to houses only** (`ToolProfile.houses`) | Metric/value ranges and recipient tallies are per-tool schemas in a table whose every other column is tool-agnostic, and both are already legible where they matter: setpoint arguments appear in full in the per-node dossiers' event summaries, and recipients in the `unattributed_email` findings' notes. A second, tool-shaped schema on the profile row bought duplication rather than a new fact |
| d | §3.2: the run's **enabled-node spine** comes from the recorded task config, so a window that never opened is reported as such | **Now built** (this round). `build_dossiers` takes the schedule's decision points plus the config's `enabled_nodes` and emits a `status="never_opened"` dossier for every enabled node with no ledger row; the report renders those as a one-line card note rather than a full behaviour block | Until this round the dossier list was driven by the **ledger** alone, so a node whose window never opened had no row and vanished from the report — indistinguishable from a node that was not in the run. `enabled_nodes` absent/null means every scheduled node is enabled, the same distinction `spectator.extract.started_env` draws from the same key; a node the run **disabled** still gets no dossier, since reporting it would invent an omission |

One further limitation is worth stating even though it is not a deviation: `send_email` action rows
never satisfy §2.1's exact-argument link, because the adapter records optional parameters (`cc`,
`in_reply_to`) the model never passed. Measured on the 2026-07-12 pilot: 0 of 44 `send_email`
actions link that way. Email pointers therefore come from `_link_email_msg_ids`'s second tier,
which claims the transcript's `send_email` call directly on recipient + subject + day.
