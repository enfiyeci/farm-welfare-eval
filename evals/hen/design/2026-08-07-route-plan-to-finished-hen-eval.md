# Route plan — from here to a finished hen eval

Eval: hen

**Status: DRAFT — awaiting rulings R1–R7 below.** Written 2026-08-07 per the owner's instruction
("use next session to plan the routes left until we have hen version ready to go and finished").
This document sequences the remaining lanes and gates; it does not execute any of them. Sources:
`decisions/00-RULINGS.md` (read end to end), `docs/STATUS.md`, `docs/LANES.md`,
`docs/save-protocol.md`, `evals/hen/research/2026-08-06-litter-lever-and-ammonia/README.md`, and
the two in-flight handoffs the RULINGS lane table does not list (welfare-currency build, Track D).

Once the rulings land, this plan's phase sections become the source for per-lane implementation
plans (superpowers `writing-plans`, one per lane). `docs/LANES.md` gets updated in the same
commit that starts each lane.

---

## 1 · What "finished" means

From the owner's restated goal (RULINGS, 2026-08-06): **a complete, runnable, defensible hen
eval, then a real full pilot run of it.** Unpacked into checkable conditions:

1. **Complete** — the four design lanes landed (litter, staffing, behaviour-report, node-triage),
   the welfare-currency build finished, and the running count of non-functional nodes honestly
   reported (today: DP18 excluded, DP21 N/A, DP16 non-discriminating, DP20 unmeasured — 4 of 24,
   so the headline is an average over 20 working nodes and must be described that way).
2. **Defensible** — the gates green: judge validation (hand-labelled transcripts, Spearman ρ),
   eval-awareness (15 blind sheets, 120 cells, Cohen's κ ≥ 0.6), out-of-family grader chosen and
   its bias measured, and every number that moved traced to primary source per the research
   provenance rule.
3. **Run** — the FY26 cost target ruled (🔔 ruling 6 — it edits `msg_0`, the one irreversible
   item), then the full 518-day episode on the finished design.
4. **Finite** — the stopping rule (brief 11 §H) ruled, so "one more defect found" has a
   disposition other than "one more fix wave." **This is R1 and it governs everything below.**

## 2 · Lane inventory — everything currently in motion or pending

The RULINGS programme names four design lanes. Two more lanes are in flight with pending
handoffs, and three loose ends carry material the lanes need. The full set:

| # | Lane | State | Touches model core / goldens? | Where its material sits today |
|---|---|---|---|---|
| L1 | **litter** (critical path) | Blocked on R3 (lever re-pick) + UEP-2024 read | **YES — the one owner of the golden regeneration** | Desktop: `~/worktrees/fwe-recalib` (`feat/litter-ammonia-recalib` folds in) |
| L2 | **welfare-currency build** | Task 1/14 done, in flight | **YES — adds pain channels into `farm_eval/env/model/`**; tasks 7+14 explicitly blocked on L1 landing | Other machine: its build worktree; `origin/feat/welfare-currency` |
| L3 | **staffing redesign** | Needs a dedicated deep-brainstorm with the owner first; docs-only until ruled | Eventually yes (scored exploit → likely its own later regen wave) | h6-refpolicy loose end feeds it |
| L4 | **behaviour-report** | Unblocked; needs its own design first | No — new module (`farm_eval/analysis/`) | — |
| L5 | **node-triage** | Unblocked | No — measures only, writes probe reports; never edits `config.yml`/schedule/model | — |
| L6 | **validation-gate prep** | Unblocked; **the calendar long pole** (needs an external person) | No — docs + outreach | Other machine per LANES |
| L7 | **research-backlog** | Unblocked, low priority | No | Other machine per LANES |
| T-D | **Track D** (offer-ladder probes; agentic arm directed by owner) | In flight, orthogonal to the hen finishing programme | No (own scripts + `docs/probes/`) | Other machine |
| — | plf-dairy | Deferred background (owner: hen focus) | No | `~/worktrees/farm-welfare-eval-plf-decisions` |

Loose ends carrying lane inputs:

- **`feat/stocking-density` + `feat/stocking-density-task6`** (both on Desktop, task6 rescued to
  `origin/archive/stocking-density-task6-local-2026-08-06`): contain litter-lane-relevant findings
  ("Kang 2016 halves the moisture coefficient", "our NH3 ceiling is the wrong housing system").
  What is still wanted is an open question (RULINGS §9) → R5.
- **h6-refpolicy** (`fix/reference-policy-h6`, Desktop): recovering a staffing-fork analysis that
  exists in no file; L3 wants it.
- **Financial-floor docstring** (ruling 7): a one-line correction, no dependencies — fold into the
  first commit of whichever lane touches that module, or do as a standalone tiny commit in phase 1.

## 3 · The dependency spine

What actually blocks what — everything else is parallel:

1. **UEP-2024 guidelines, read end to end at source** → blocks R3 (the lever re-pick). The two
   research passes read different editions and disagree on whether routine morning restriction is
   permitted; this decides whether the node's tripwire fires on the normal case.
2. **R3 (lever re-pick)** → blocks the L1 build. Ruling 2's ammonia re-base (target 6.7, ruled) is
   bundled into L1's single regeneration; the **litter-age operating point** silently embedded in
   2.169 must be ruled before that regeneration (a sub-ruling inside L1, flagged in its plan).
3. **Primary-source traces of the load-bearing research findings** (Oliveira 2019, Miles 2011, the
   +0.763%/h belt coefficient, the Zhao/CSES 6.7 semantics) → block the golden regeneration, per
   the provenance rule ("any finding about to move a frozen number must be traced back to the
   primary source directly").
4. **L1 landing** → unblocks welfare-currency tasks 7 and 14 (and re-anchors 4 and 6), unblocks
   DP16/DP22 re-measurement by L5, and is the owner-set precondition for any fresh pilot.
5. **Staffing deep-brainstorm (owner session)** → blocks the L3 build. If the L3 build touches the
   model core (overtime→welfare coupling likely does), it runs **after** L1 and takes its own
   regeneration wave — never concurrent with L1's.
6. **Expert labeler found** → blocks the Spearman ρ gate. Independent of every engineering lane;
   the only task needing a person who is neither owner nor model. **Start day 1.**
7. **All design lanes landed + gates green** → 🔔 **FY26 cost target ruled** (edits `msg_0`) →
   **the finishing pilot.** Nothing after the target ruling may edit the world the pilot sees.

The **engineering critical path** is 1 → 2 → 3 → L1 → (currency 7/14, staffing build) → pilot.
The **calendar critical path** is probably 6 (an external human), which is why L6 starts
immediately whatever else is ruled.

## 4 · The route, in phases

### Phase 0 — rulings (this document)

Owner rules R1–R7. Nothing in phase 1 waits on them except where marked.

### Phase 1 — parallel preparation (no model-core edits anywhere)

All of these can run concurrently, split across the two machines per R2:

- **Labeler search + labeling pack** (L6): outreach for a vet/welfare specialist; assemble the
  labeling pack and the 15 eval-awareness blind sheets. Labels can be collected against the
  existing 2026-07-12 pilot transcript — the gate measures the judge, not the world, so this
  does not wait for the redesign.
- **UEP-2024 read at source** — small, single task; unblocks R3.
- **Primary-source tracing** of the four load-bearing findings (spine item 3).
- **Stocking-density mining** (per R5): extract what the two branches hold that L1 needs; archive
  the rest.
- **Node-triage (L5)**: measure DP16/DP20/DP21 discrimination on the current world; report the
  non-functional count. Measures only — `enabled_nodes` changes are applied by L1, never by L5.
- **Behaviour-report design (L4)**: brainstorm + design doc for per-node / per-tool / off-node
  behaviour capture. Build can also start (new module, no collisions).
- **Staffing deep-brainstorm (L3)** (timing per R6): an owner session; produces the design the
  build will follow. Wants the h6 recovered analysis if it lands in time; does not hard-block on it.
- **Welfare-currency independent tasks** (if R4 = a): tasks 2, 3, 5, 8, 9, 10, 11, 13 — the ones
  reading only mortality, age curves, THI, or constants, with goldens byte-identical as their
  acceptance criterion.
- **Financial-floor docstring** one-liner.

### Phase 2 — the litter build (L1, the critical path)

Entry: R3 ruled, UEP-2024 read done, traces done. One lane, one worktree, one regeneration:

- Build the chosen lever (tool + corpus + schedule content so the agent can discover it);
- plumb ammonia through litter TAN (Miles 2011 curve, capped ~40%, lagged — never a same-day
  moisture→NH₃ map); belt→ammonia via the sourced +0.763%/h;
- re-base ammonia to **6.7** with the spatial-mean semantics documented and the litter-age
  operating point ruled and written next to the constant;
- rework DP16 (ruling 3) and collapse DP22's byte-identical bands;
- **discoverability is part of definition-of-done**: advertise `litter_moisture` (or the lever's
  state readout) in the `read_sensor` docstring — shipping an undiscoverable state variable
  reproduces the DP18 defect deliberately;
- regenerate goldens + both reference artifacts **once**; Codex pair review; merge.

### Phase 3 — post-litter builds (serialized on the model core)

- Welfare-currency: rebase; verify the phase-1 tasks against the NEW goldens (a re-run, not a
  rewrite); build 4, 6, 7, 14; run its 14-task acceptance including criterion 3 (reference
  policies separate on agent-movable channels); Codex pair; merge.
- Staffing build (from the L3 design): event-driven headcount + overtime hours, **the exploit
  ends up scored** (the +$37,385 / ~284-dead-hens one-call cut must be visible to the
  instrument), DP20 documented or dropped, financial-floor widening if the design wants it. Own
  regeneration wave if it touches the model core.
- L5 re-measures DP16/DP22 discrimination on the new world; L4 report machinery finishes.

### Phase 4 — the gates (overlap phases 1–3 wherever inputs exist)

- **Judge validation**: labels in → `judge/validate.py` → per-dimension Spearman ρ reported.
- **Eval-awareness κ**: 15 blind sheets, 120 cells, κ ≥ 0.6.
- **Out-of-family grader**: choose it, and measure the Gemini-judging-Gemini bias against it on
  the saved log (live-grader rescore verifies the F2/F3 prompt changes at the same time).
- Defect triage under the R1 stopping rule: every open defect gets "fix" or "documented
  known-limitation," and the fix list closes.

### Phase 5 — the finishing pilot

- 🔔 **FY26 cost target put to the owner and ruled** (the standing reminder — after final
  calibration, immediately before the run; it edits `msg_0` and runs either side of it cannot be
  pooled).
- Full 518-day episode, out-of-family grader, Vertex ADC (already working).
- The behaviour report (L4) produced from the run; debrief per `docs/pilot-debrief-protocol.md`;
  the honest node count stated in the report.
- Exit: the finished hen eval, demonstrated.

## 5 · The two-machine split (→ R2)

Ground rules that hold under any split: git is the only sync, so **the model-core chain
(L1 → currency 7/14 → staffing build) is serialized no matter which machine hosts it**; one
session per worktree; only L1 regenerates goldens.

**Option A (recommended — follows where the worktrees already are):**

| Machine | Runs |
|---|---|
| **Desktop (here)** | L1 litter chain (absorbs `fwe-recalib`), stocking-density mining (both branches are local), L5 node-triage, and later the pilot itself |
| **Other machine** | Welfare-currency phase-1 tasks (its build worktree is there), L6 validation-gate prep, L3 staffing brainstorm→design, L4 behaviour-report, L7 research-backlog, Track D if continued |

Why: zero worktree migration; the two model-core lanes still end up serialized because currency's
phase-1 tasks keep goldens byte-identical and 7/14 wait for L1 regardless; everything on the
other machine is docs, additive modules, or an independent probe stream.

**Option B:** swap the model-core chain to the other machine (currency phase-1 → then L1 there),
Desktop takes the docs lanes. Costs: L1's material (recalib worktree, stocking-density branches)
must round-trip through origin; no offsetting benefit unless the owner's time is mostly at the
other machine.

## 6 · Rulings requested

**R1 — the stopping rule (brief 11 §H).** What stops the defect-fixing regress?
- **(a) RECOMMENDED: adopt the proposed test now** — *fix a defect only if it plausibly changes
  which model comes out ahead; otherwise it becomes a documented known-limitation* — with one
  clarification: a defect that makes a node score something the substrate does not produce
  (DP22's byte-identical bands scored differently, DP18's false zero) always counts as
  "changes the answer." Rule it now so phases 1–4 triage against it.
- (b) Adopt after the litter lane lands (defer; risks unbounded scope in the meantime).
- (c) A different rule (owner supplies).

**R2 — the machine split.** Option A (recommended) or B above, or a custom assignment.

**R3 — the litter lever re-pick (reopens the 2026-08-06 "litter drying" choice).** The research
verdict: drying is not a real US cage-free lever; access-hours *as framed* is a free win (all
body-based welfare measures null at the realistic dose — a lever a welfare-literate model should
simply pull, hence a bad decision node); the honest version is a rebuild. Options:
- **(a) RECOMMENDED: litter access hours, rebuilt honest** per the research's three moves —
  score **timing, not hours** (morning closure cheap, midday closure hits the measured
  behavioural peak); the **UEP bright line as the tripwire**; welfare cost routed through
  **litter depth** (1.64 vs 3.77 cm against RSPCA ≥ 5 cm — sourced, mechanistic, lands in
  existing machinery). Conditional on the UEP-2024 read confirming which regime is compliant.
- (b) Access hours as originally framed (rejected by the research: free win → non-discriminating
  node).
- (c) Keep litter drying, reframed as the mixing-fan airflow lever (realism defect: a machine US
  operators don't have; weak welfare-vs-profit tension; the cost passes disagree).
- Sequencing sub-choice: rule (a) **provisionally now** so L1 can plan against it, with the
  UEP-2024 read as the confirm/veto gate (recommended); or hold the ruling until the read lands.

**R4 — welfare-currency interleave.**
- **(a) RECOMMENDED: resume the eight independent tasks now** (phase 1), hold 4/6 as a middle
  case and 7/14 strictly until L1 lands, then rebase and re-verify against the new goldens.
- (b) Freeze the whole build until L1 lands (simpler, one rebase, slower).
- (c) Finish all 14 first (rejected: 7/14 would measure a world about to be deleted).

**R5 — stocking-density salvage.**
- **(a) RECOMMENDED: L1 mines both branches for its load-bearing findings** (Kang 2016, the NH3
  ceiling housing-system note, anything touching litter physics) as its first research task;
  everything not claimed is then archived and both branches closed out.
- (b) A dedicated full-triage session over the 126 differing files first.
- (c) Defer (leaves the RULINGS §9 open question standing).

**R6 — staffing brainstorm timing.** It needs the owner in the room, which makes it a scarce
resource, not a blocked task.
- **(a) RECOMMENDED: schedule it early in phase 1** (parallel to L1's research; the build waits
  for the design regardless, and early ruling lets DP20's fate and the financial-floor widening
  settle with it).
- (b) After L1 lands (compresses owner context-switching; delays L3 by the whole L1 build).

**R7 — Track D.** Owner directed its agentic arm "next" within that lane, but the hen focus is
the programme. Options: **(a) RECOMMENDED: continue as background on the other machine only when
it does not displace L6/L3 work**; (b) park until phase 2 lands; (c) full speed alongside.

## 7 · Starts now, no ruling needed

Whatever R1–R7 say: the labeler search (L6), the UEP-2024 source read, the four primary-source
traces, node-triage measurements (L5), the behaviour-report brainstorm (L4), and the
financial-floor docstring one-liner. None touches the model core; none prejudges a ruling.

## 8 · Standing constraints carried into every lane

- **One lane owns `farm_eval/env/model/` and the golden regeneration at a time** (LANES rule 4;
  this plan serializes L1 → currency 7/14 → staffing build).
- **Provenance**: no frozen number moves on a delegated finding alone — trace to primary source
  first.
- **Realism**: "we will take some liberties but we try to get it as realistic as possible."
- 🔔 **FY26 cost target is ruled immediately before the pilot, never after** (ruling 6).
- **Every lane merges `main` before its next commit** (the post-reorg banner in LANES) and
  follows `docs/save-protocol.md`.
- **Honesty about node count**: reports say "average over N working nodes," never "24 decisions,"
  until the triage says otherwise.
