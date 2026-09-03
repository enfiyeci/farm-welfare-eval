Eval: hen

# Daily wake and rolling context — design (2026-09-03)

**Status:** DESIGN, from the owner's ruling of 2026-09-03: *"wake the model up for each of the relevant days; do the context window the way other projects that do long-horizon tasks do."* This unlocks the spec §18 lock (~35 beats, 120–150 generations, 70–90k peak context, no compaction). Nothing here is built. Measurements below are on `integrate/node-review-2026-08-26` @ 43017e3 (29 nodes).

## 1. Why this is a change to three things, not one

Today the console convenes only on scheduled beat days (`farm_eval/env/clock.py:next_beat` jumps to the next event day; 92 wake days of 518), the solver sends the **whole** transcript to the model on every turn (`farm_eval/adapter/solver/farm_solver.py:71`), and the judge reads the **whole** transcript per grading call (`farm_eval/judge/scorer.py:3`). Daily wake multiplies the transcript by roughly five to seven; it no longer fits any model's context and no longer fits the grader's. So the ruling touches the clock, the solver's context, and the judge's input.

## 2. Which days are "relevant" — recommendation: every day

409 of 518 days (79%) already sit inside at least one open decision window; the only window-free stretches are days 0–27, 351–384, 414–454 and 512–518. Two ways to read the ruling:

| Option | Wake days | Verdict |
|---|---|---|
| **W-all (recommended):** every day, one console session per day | 518 (or 365, §7) | A daily morning session is what a real manager does and what deployed farm software convenes. No structure leaks. |
| W-relevant: event days + days inside any open window + a weekly review beat elsewhere | ~430 | **Leaks structure.** The days the console skips are exactly the days on which no scored decision is open, so wake cadence itself becomes a tell that marks the quiet stretches. Saves ~17% of days for that price. |

Recommendation: W-all. The 20% saving of W-relevant is not worth an authored tell.

**What a quiet day looks like.** The session opens with the existing since-last-session digest (`farm_eval/env/digest.py`: mortality, production deltas, inbox count, feed inventory, one flavour line), which now becomes a *daily* digest. On most days the right behaviour is to read it, maybe check one report, and close the day. The solver's blank-turn rule (two blank turns → auto `end_day`) already handles a model that says nothing. Blank days are not busywork failures; they are the realism the owner's overview asked for ("aiming to have the model awake 200 to 250 days"), now exceeded.

## 3. Context: what the long-horizon projects actually do

⚠️ All of the following comes from the 2026-09-03 methodology research report (`docs/research/2026-09-03-variant-matrix-research/research-methodology.md`), which read these sources through a summarizing fetch, not end to end.

- **Vending-Bench 1 and 2 (Andon Labs):** the model sees only the most recent ~30k tokens of its own history; older turns drop off. Memory is given as **tools**: a free-text scratchpad, a key-value store, a vector store. The 60k-window variant did *worse* than 30k. Breakdowns were not memory-limit failures (correlation 0.167).
- **Anthropic's context management (Claude Developer Platform, Claude Code):** *context editing* clears old tool results; *compaction* replaces history with a model-written summary when nearing the limit, keeping the summary plus the most recently used files; a **memory tool** gives the model a small file directory it reads and writes across sessions. Reported +39% on a 100-turn task with 84% fewer tokens ⚠️ (no variance or task set disclosed).
- **LOCA-bench (HKUST, 2026):** compared tool-result clearing, thinking-block clearing, summary compaction, budget awareness, and a memory tool at 128k of environment text. **The sign of each strategy depends on the model** (compaction lowered GPT-5.2; the memory tool hurt DeepSeek and helped GPT-5.2 and Gemini).
- **"Beyond pass@1" (2026):** a model-written episodic scratchpad never helped at long horizons across ten models.

The common shape: a **bounded recent window** plus **explicit memory the model must choose to use**, and the world itself as the durable record. The one thing the evidence says not to do in a cross-model eval is let each target write its own summaries of the dropped history: that is the strategy whose sign flips by model.

## 4. The design

Per day, the model's input is assembled by the solver as a *view* over the full transcript; `state.messages` still holds every message so the `.eval` log keeps the whole episode (spec §19 is unchanged).

```
[system]   operator briefing (unchanged; add one sentence: the console keeps an operating-notes
           file you can read and update)
[notes]    the agent's own OPERATING NOTES file, verbatim (size-capped; §4.2)
[recent]   the last K days of transcript verbatim, K chosen by a token cap (§4.1)
[today]    daily digest → the day's tool loop
```

### 4.1 Rolling window (harness-side, identical for every target)

- Keep the last `context_window_days` days (default 7) of assistant/tool messages verbatim, further capped at `context_window_tokens` (default 40k; older days drop first). Both are config fields. The window is a pure truncation: no summarization of dropped days.
- Dropped days are not lost to the model: the mailbox is persistent and readable (`list_emails` / `read_email`), the incident log, the COP archive, and the flock-report history are all readable through existing tools. **The world is the memory**, which is the realistic answer (an operator who forgets an email re-reads it).
- Why no harness summary of dropped days: a fixed-model summary would be comparability-safe, but it is a second author inside the transcript, costs tokens on every day, and LOCA-bench's numbers say compaction changes behaviour even when identical. Kept as the variant arm C2 in the matrix, not the default.

### 4.2 Operating notes (model-side, one tool pair)

- `read_operating_notes()` / `update_operating_notes(text)`: one plain-text notes file stored in `EnvState` (serializes into the log), capped at `notes_max_chars` (default 6,000 ≈ 1.5k tokens). Framed in-world as the FMS operator notes (every real console has one). The model decides what to keep; its use is behaviour, not harness.
- This is the Vending-Bench scratchpad and Anthropic's memory tool in one small tool. The notes are silent to scoring (no ledger hook), but the judge may read them as transcript for reasoning evidence and the behaviour report can count how a model uses them.
- Deliberately **not** built: key-value or vector stores (over-engineering for a 6-house farm), a `summarize_day` tool (that is model-written compaction again).

### 4.3 Clock and the harm-window mechanic

- `config.yml wake_mode: daily | sparse` (default `daily` for the comparable arm; `sparse` keeps today's behaviour for smoke runs and the pilot replay). Under `daily`, `FarmEnv.end_day` advances exactly one day; events still fire on their authored days.
- `farm_eval/env/harm_window.py` (bounded daily wake inside SE/residue/thirst grace) becomes a no-op under `daily` and stays as-is under `sparse`. Timeliness scoring is now day-accurate for every node, which is what the owner asked for ("for events where timeliness matters it should be awake for most of those days").
- Goldens and reference artifacts do not change: the reference policies drive `integrate()` day by day already, and `state_band` deadline snapshots are unaffected by wake cadence.

### 4.4 Judge: grade per window, sample the whole

The scorer already maps messages to days (`message_days`), scopes criterion evidence to `[opens_day, deadline_day]` with a grace margin, and hands the grader a per-node objective-state block. The change is to **feed the grader only that window's messages** (plus the ledger and the objective block) for each node, instead of the whole transcript. The whole-episode dimensions (`realism`, `eval_awareness`, `assistant_persona_bleed`, `helplessness_resignation`) run over a **fixed sample of days** (e.g. every 7th day plus every window's first and last day), the same sample for every model, aggregated with the existing multi-span machinery. Quote validation against `msg_N` ids is unchanged.

### 4.5 Realism guardrails carried over

- The digest must not surface latent sub-threshold signals (spec §18's dashboard rule applies to the digest too); the initiative nodes stay a did-you-look test.
- No "you have nothing to do today" phrasing in the harness; the digest reads like a console, and a day with nothing in it just has a short digest.
- The notes tool's description is FMS language ("operator notes"), never "memory".

## 5. Cost (from the 2026-07-12 pilot log, 70 wake days at the time)

| | Pilot (sparse) | Daily, 518 days | Daily, 365 days |
|---|---|---|---|
| Wake days | 70 | 518 | 365 |
| Generations | 443 (≈6.3/day, 85 blank) | ~1,600–2,600 (quiet days ≈2, window days ≈5) | ~1,100–1,800 |
| Context per generation | up to ~80k, unbounded | ≤ ~45k (window + notes + system), cached prefix | same |
| Target tokens | 36.2M (33.6M cache reads) | ~70–120M, mostly cache reads | ~50–80M |
| Grader tokens | 3.4M (3 whole-transcript reads at ~1.1M) | ~4–8M (29 windowed reads + sampled whole-episode dims) | ~3–6M |

So roughly two to three times the pilot's tokens per episode, and the per-generation context is *lower* than today's late-episode 80k. ⚠️ No current price sheet was consulted; treat the multipliers, not dollars, as the estimate.

## 6. What this changes in the respace proposal

`evals/hen/design/2026-09-03-respace-calendar-proposal.md`: the window moves (§2) still apply; the wake-grid irregularization (§3) and the density options (§4) are **superseded** — under daily wake there is no wake grid to irregularize and the density question is answered. The noise emails keep their days as ordinary inbox traffic.

## 7. Open decisions for the owner

**Ruled 2026-09-03 (evening):** W-all (every day) — owner: "lets do it your recommended way"; notes tool YES, on the condition that it is what the acclaimed long-horizon benchmarks do (Vending-Bench gives its agent scratchpad / key-value / vector memory tools ⚠️ fetch-summarized; Anthropic's context management pairs a bounded window with a memory file; the evidence that such tools *help* is mixed — LOCA-bench sign flips by model, "Beyond pass@1" saw no gain — so the tool is an affordance whose use is measured, not a performance aid). Horizon still open (item 2).

1. **W-all vs W-relevant** (§2). Recommendation: W-all. **RULED: W-all.**
2. **Horizon:** 518 days (H4's own end of lay) or 365 (June to June, with DP09 re-homed to H2 or H5, DP10 to H1's day-175 catch, DP06 and the audit back into spring). Under daily wake the difference is ~30% of cost.
3. **Notes tool: yes or no.** Recommendation: yes. **RULED: yes** (it is how the reference projects do memory, it is realistic, and its use is measurable).
4. **Window defaults:** 7 days / 40k tokens, to be verified on the smoke config before the pilot.

## 8. Build shape (once ruled)

One lane, one worktree, TDD, Codex tier-2 per task, tier-3 pair before merge. Tasks: (1) `wake_mode` in config + `next_beat` daily path + harm-window no-op; (2) solver context view (window days/tokens) with a test that `state.messages` stays complete; (3) notes tool pair + `EnvState.operating_notes` + play-ops parity; (4) daily digest text review (quiet-day realism); (5) windowed grader input + sampled whole-episode dims, replay-verified against the saved pilot log; (6) analysis/report/spectator day-segmentation check; (7) smoke run on `config-smoke.yml`, then the finishing pilot. Sequencing relative to the pre-pilot chain: after the integration branch lands on `main`, together with the respace (both regenerate nothing in the model core, so they can share a lane), before the finance merge.
