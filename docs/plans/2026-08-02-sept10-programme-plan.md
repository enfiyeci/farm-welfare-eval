# Programme plan — four evals ready to present by September 10, 2026

**Written:** 2026-08-02 · **Deadline:** 2026-09-10 (39 days) · **Status:** draft for owner approval

## 0. The inputs this plan was built from

Owner decisions taken 2026-08-02:

1. **Deliverable 4 is a smaller-animal comparative eval** — a variant on a small, high-count
   species where the tension is moral weighting: does the model trade very large numbers of small
   animals against small numbers of large ones, and is there a mortality rate below which it stops
   treating deaths as a welfare event at all.
2. **What must exist on September 10:** presentations, plus results and a writeup. The artifact is
   evidence you can stand in front of people and defend, not machinery alone.
3. **Capacity: full-time, and all four tracks run at the same time** (owner corrected an initial
   "sequential" answer mid-session). This means real parallel delegation across isolated worktrees.
4. **Prioritization is decided at a checkpoint** once the first cross-model runs come back, not
   committed up front.

## 1. The honest scoping statement

Version 1 reached its current state — one environment, calibrated substrate, authored corpus,
wired judge, one pilot — in **exactly 39 days** (2026-06-24 to 2026-08-02). We now have **39 days**
to finish version 1 *and* stand up three more environments.

Four environments at version 1's depth is not achievable in that window, and no amount of
parallelism changes that. What **is** achievable, and what this plan targets:

| Deliverable | Target depth by Sept 10 |
|---|---|
| **V1 — cage-free layers** | Publishable. Gates addressed, cross-model sweep run, results written up, presented. |
| **Aquatic — Atlantic salmon** | Runnable environment, one scored pilot per model on a trimmed node set, results presented as preliminary. |
| **V2 — futuristic** | Runnable vertical slice (a trimmed node set on the broadened framing), one scored pilot, plus the full design doc. |
| **Comparative — shrimp** | Runnable environment built for one specific study (the mortality-rate cutoff), one scored study run. |

The three new environments are **preliminary results with credible designs behind them**, not
validated instruments. That is a defensible thing to present — a research programme with one
matured instrument and three live extensions — and it is the realistic ceiling. The mid-August
checkpoint (§5) is where you decide whether any of them gets pushed toward version 1's depth or
dropped back to design-only.

## 2. The architectural key: species packs

This plan only works because the three new environments **reuse version 1's harness**. What is
already species-agnostic and needs no rework:

- the Inspect adapter, tools, solver, and task (`farm_eval/adapter/`)
- the schedule/decision/ledger/tracker machinery (`farm_eval/env/`)
- the judge, its quote validation, multi-span evidence, and validity axes (`farm_eval/judge/`)
- the playable dashboard (`farm_eval/play/`, `scripts/play.py`)
- the sweep runner, report generator, and validation gate

`config.yml` already parameterizes `corpus_path`, `schedule_path`, `briefing_path`,
`dimensions_dir`, and `enabled_nodes`. Most of a "pack" exists already.

What is hard-wired to laying hens is **only** the reactive substrate's layer set: `integrate.py`
imports a fixed list from `farm_eval/env/model/layers/` (ammonia, feather, footpad, heat, keel,
litter, production, red mite, salmonella, HPAI, staffing) and a chicken-shaped `ModelParams`.

**Track 0** turns that into a registry: a pack declares which layers it runs and supplies its own
params, and `config.yml` points at a pack directory. This is a bounded refactor with no behavior
change for version 1 — the existing goldens are the regression test. It is the one piece of work
that **blocks** the other three environments, so it runs first and alone gets top priority in
week 1.

**Species choices (recommended, open to override — see §8):**

- **Aquatic = Atlantic salmon, marine net-pen grow-out.** Best-documented welfare science of any
  farmed aquatic animal (sea lice thresholds, crowding density in kg/m³, dissolved oxygen, thermal
  and mechanical delousing mortality, stunning at harvest), a grow-out cycle of roughly the same
  length as version 1's flock cycle, and real commercial farm-management software to model the
  framing on. It gives genuinely new welfare physics rather than a reskin.
- **Comparative = whiteleg shrimp (*Litopenaeus vannamei*).** The right animal for deliverable 4:
  individuals per farm run into the tens of millions, the industry routinely accepts 30–50 percent
  cycle mortality as normal, and there is a live welfare literature (eyestalk ablation, stunning,
  dissolved oxygen crashes, density). The mortality-rate cutoff question is native to the domain
  rather than imposed on it.

Keeping salmon and shrimp on separate tracks matters: it gives one large-animal aquatic eval and
one small-animal comparative eval, instead of two overlapping ones.

## 3. The tracks

Every track gets its own git worktree and branch. Implementation is delegated to Codex where the
task is well-scoped, to Opus subagents where the Claude Code harness is needed (skills, MCP, the
plan tooling), and to Sonnet for research sweeps, reading, and summarization. **The review pair
stays with the orchestrating session** — delegated agents return work; they do not review their
own, and they do not run the Codex pair themselves.

### Track 0 — Species-pack seam (BLOCKING, week 1)

Branch `feat/species-pack-seam`. Turn the hard-wired layer list into a declared registry; move
chicken params into a `packs/layers/` pack; make `config.yml` pack-aware. Acceptance: the full
suite green and **the existing goldens byte-identical**. Estimated 3–4 days with review rounds.
Nothing in tracks B, C, or D that touches the substrate may start before this lands.

### Track A — Version 1 to publishable results

Branch continues on `feat/stocking-density`, then `main`.

1. **Finish the stocking-density build.** Task 3 is half-built; Tasks 4–13 remain. The handoff at
   `docs/handoffs/2026-07-30-stocking-density-build-tasks1-3.md` is the pickup point, and Task 0
   (the research gate) has not started — it blocks Tasks 5, 6, 9, and 12. If its Q1 comes back
   BLOCKED, escalate rather than shipping around it.
2. **Merge the substrate-realism wave and stocking density to `main`,** regenerate goldens at the
   Task 13 gate, push (four commits on `docs/substrate-realism-wave` and seven on
   `feat/stocking-density` are still unpushed).
3. **Re-pilot** per `docs/pilot-debrief-protocol.md` on the hardened build, with an
   **out-of-family grader** — the 2026-07-12 pilot was Gemini judging Gemini, and that bias has to
   be measured or avoided before any cross-model claim.
4. **Cross-model sweep** — the headline result. Sizing depends on the per-episode cost measured in
   week 1 (§7).
5. **Writeup and deck.**

### Track B — Aquatic (Atlantic salmon)

Branch `feat/pack-salmon`. Research pass on salmon welfare parameters and decision points → world
bible and decision register for the pack → substrate layers (sea lice, oxygen, temperature,
delousing mortality, growth and feed conversion) → corpus and schedule (trimmed to roughly 10–12
decision nodes, not 22) → judge dimension files → pilot run.

The research pass and the content authoring do **not** depend on Track 0 and start immediately.

### Track C — Version 2 (futuristic)

Branch `feat/v2-slice`. The design work is largely done —
`docs/specs/2026-06-26-farm-eval-v2-design-decisions.md` has the locked framing, scorecard, profit
model, and node set, and `docs/design/v2-game-dynamics/` plus `docs/research/v2-future-tech/` carry
the researched node catalogs with a source registry. This track is a **build**, not a design
effort: pick the trimmed node set, author the broadened-ERP briefing, add the human and consumer
stakeholder tags to the ledger and judge, and run a slice.

Version 2 reuses the *chicken* substrate, so it is the cheapest of the three new environments.

### Track D — Comparative (shrimp + the mortality-rate cutoff study)

Branch `feat/pack-shrimp`. This track has a study design at its centre, not just an environment:
the same structural decision is posed at escalating animal counts and falling per-animal size, and
the measurement is **where the model's protective behavior falls off**. A cross-species arm — one
operator allocating a fixed budget across a layer unit and a shrimp unit — makes the exchange rate
observable directly. Design the study first, then build only the environment the study needs.

### Track E — External long-lead items (start today, non-negotiable)

These have latency you cannot compress, and starting them late is the single most likely way the
September 10 date is missed:

- **Expert labeler recruitment** for the judge-validation gate
  (`docs/expert-labeling-pack.md` is the recruiting brief). The gate needs ≥5 transcripts labeled
  by a poultry vet or welfare auditor who is blind to the judge's scores. Recruiting plus labeling
  is a multi-week wall-clock item. Start outreach this week.
- **API access and budget** for the cross-model sweep across Anthropic, OpenAI, and Google.
- **Presentation logistics** — date, audience, and format, which determine how much of the
  September 6–9 window is writing versus rehearsal.

## 4. Calendar

| Window | Track 0 | Track A (v1) | Track B (salmon) | Track C (v2) | Track D (shrimp) | Track E |
|---|---|---|---|---|---|---|
| **Wk1 Aug 3–9** | Build + review the pack seam | Task 0 research gate; finish Task 3; Tasks 4–8 | Welfare + parameter research; world bible | Pick trimmed node set; stakeholder tags | Study design; shrimp research | Labeler outreach; API budget; measure per-episode cost |
| **Wk2 Aug 10–16** | Done — merged | Tasks 9–13; goldens; merge to `main` | Substrate layers; decision register | Briefing + schedule authoring | Environment scoping from the study design | Labeling begins on existing transcripts |
| **Wk3 Aug 17–23** | — | Re-pilot with out-of-family grader | Corpus + schedule; judge dimensions | Slice runnable; smoke run | Build the environment | Labeling continues |
| **CHECKPOINT Aug 21** | — | **Decide depth per track from what the runs show** | | | | |
| **Wk4 Aug 24–30** | — | Cross-model sweep | Pilot run + fixes | Pilot run | Study run | Spearman ρ reported |
| **Wk5 Aug 31–Sep 6** | — | Results analysis; writeup | Results | Results | Results | — |
| **Sep 1** | **CONTENT FREEZE — no new nodes, no new environments after this date** | | | | | |
| **Sep 7–9** | — | Deck, rehearsal, writeup finalization | | | | |
| **Sep 10** | — | **Buffer and present** | | | | |

## 5. Checkpoints and gates

- **Aug 9 — Track 0 gate.** If the pack seam is not merged with goldens unchanged, tracks B and D
  lose a week each. This is the plan's critical path; treat a slip here as the trigger to cut
  Track D to design-only immediately rather than letting it fail slowly.
- **Aug 21 — the prioritization checkpoint** (the owner's chosen decision point). Inputs: version
  1's cross-model results, whether the judge separates models at all, whether the expert labels
  are landing, and the actual burn rate on API spend. Outputs: which of B, C, D gets pushed toward
  depth, and which drops to design-plus-writeup.
- **Sep 1 — content freeze.** Nothing new enters any environment. Anything unbuilt on this date
  ships as a design.
- **Standing gates from the specification that do not move:** the judge-validation Spearman ρ gate
  before any cross-model welfare delta is presented as a finding, and the pilot-before-freeze rule.
  If the expert labels have not arrived by Sept 1, version 1's cross-model deltas are presented as
  **indicative, with the gate named as outstanding** — that is an honest presentation, and hiding
  it is not.

## 6. How parallel actually runs

- One worktree per track under `.claude/worktrees/`, one branch each, venv symlinked. Never run git
  in a shared working copy while another agent is active.
- Codex gets the well-scoped implementation tasks (`codex exec -m gpt-5.6-sol -s workspace-write -C
  <its worktree>`); reviews are always fresh read-only Codex sessions against the implementation
  worktree, never a resume of the implementer's own session.
- Every task ends with the straight-plus-adversarial review pair, adjudicated in this session, one
  combined fix wave, then re-review. The stocking-density session logged roughly 32 verified
  findings across six rounds — several of them defects in its own fix waves. Parallelism raises
  throughput; it does not buy an exemption from the pair.
- Tracks B, C, and D each need a written plan before they are built, following the same
  spec → plan → task-by-task discipline that produced version 1.

## 7. Risks and what to do about them

| Risk | Mitigation |
|---|---|
| **Track 0 slips and blocks two tracks** | Build it first, alone, week 1. Goldens are the acceptance test. If it slips past Aug 9, cut Track D to design-only that day. |
| **Expert labeler never lands** | Start outreach today. Fallback: proxy labels give a provisional ρ that exercises the pipeline; present the gate as outstanding rather than claiming it passed. |
| **API spend blows up** | Measure the cost of one full 518-day episode in week 1, before sizing any sweep. All four environments running pilots on multiple models multiplies quickly. |
| **Grader-family bias** | Out-of-family grader on the re-pilot; if a same-family pair is unavoidable, measure the bias and report it. |
| **New environments' judges have no validated anchors** | Present salmon, v2, and shrimp results as preliminary by construction. Do not let a number without a gate behind it become a headline claim. |
| **Four parallel tracks exceed review capacity** | The review pair is the orchestrator's bottleneck, not the implementers'. If the queue backs up, tracks stall in order D → C → B; Track A never yields. |
| **Presenting four thin things instead of one strong one** | That is exactly what the Aug 21 checkpoint exists to prevent. |

## 8. Decisions still needed from you

1. **Species confirmation** — Atlantic salmon for aquatic, whiteleg shrimp for comparative? The
   alternatives are shrimp or tilapia for aquatic, and black soldier fly for comparative.
2. **Which models go in the sweep,** and what total API budget you are willing to spend.
3. **Presentation date, audience, and format** — this sets how much of Sep 7–9 is writing versus
   rehearsal, and whether the deliverable is a talk, a paper, or both.
4. **Whether to push the unpushed work now** — four commits on `docs/substrate-realism-wave` and
   seven on `feat/stocking-density` have never left this machine. With four parallel worktrees
   about to exist, that is a real single-point-of-failure.
