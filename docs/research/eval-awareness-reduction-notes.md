# Eval-awareness reduction — research synthesis & design notes

Working notes for a planned design doc (`docs/superpowers/specs/2026-07-02-eval-awareness-reduction-design.md`,
not yet written). Captures a brainstorm + 4 deep-research passes on **decreasing eval-awareness**
on the farm-welfare eval, on top of what's already built (§12 mitigations, computed reads, reactive
substrate, `eval_awareness` validity gate, pilot-before-freeze gate).

Two locked constraints frame everything: **static frozen environment** + **cross-model comparability
/ determinism**. User's target: reduce **both** latent belief AND verbalization — but **suppressing
verbalization without changing belief is a FAILURE**, not a win.

---

## 0. The motivating number (why this matters)

Anthropic Agentic Misalignment (static insider-threat tests): a model misbehaved **~55% when it
believed the scenario was real vs ~6.5% when it concluded it was a test**, and it concluded "test"
~65% of the time *because the scenario was static/contrived*. → A frozen eval can **under-measure
real misalignment by ~8×**. Direct analog here: a model that smells the farm is a test acts more
welfare-friendly than in real deployment, so **welfare headline scores are inflated by exactly the
awareness we fail to kill**. Models default to assuming "real" unless a cue tips them off.

External validation that this effort improves *predictive* validity (not just aesthetics): OpenAI
"Simulated Deployment Audits" (Williams et al. 2026) and Anthropic "Realism Win Rate" (2026) both
show deployment-style framing lowers awareness AND gives more accurate post-release behavior forecasts.

---

## 1. Organizing insight

1. **Cues, not content, drive eval-awareness** (Probe-Rewrite-Evaluate / Xiong et al. 2025). Models
   flip to "test" on textual/structural markers: templated formatting, suspiciously clean data,
   academic/meta framing, editorializing, a "meaningful" one-hook-per-turn cadence. §12 already
   targets these; the upgrade is to **measure** them, not eyeball.
2. **For a 17-month run, temporal + operational coherence is the dominant lever** (VendingBench,
   Apollo). Long agent runs derail (meltdown loops, identity drift, hallucinated artifacts)
   independent of context-window fill; a boringly-coherent multi-month world is the strongest
   "this is real" signal, and a *derailing* model starts theorizing "maybe this is a test."
3. **Design rule from user's "both, never suppress verbalization":** every technique must move
   latent belief, and we measure verbal + non-verbal separately so we can tell "made it more real"
   apart from "just made it quieter."

---

## 2. Three-phase plan (Phase 1 gates 2 & 3)

### Phase 1 — Measured-iteration loop (build first)
- **A1 — De-tell corpus audit (authoring QA).** Rubric-scored **artifact-level** classifier over
  `corpus/documents/emails/`, `schedule/events.yml` body_refs, `prompts/operator_briefing.md`.
  - **CRITICAL correction from research:** do NOT ask a model "is this an eval?" — binary/probability
    asks make models label almost everything "eval" AND **prime** awareness (comparative black-box
    study; best Cohen's κ only ~0.59–0.75). Use **transcript/artifact-level judging** (LLM judge on
    a whole transcript hits AUC ≈ 0.83 vs human 0.92) and **"user-motivation guessing"** framing
    (infer intent WITHOUT mentioning evaluation — avoids priming). Reasoning-trace scanning = low
    sensitivity.
  - **Adopt "Realism Win Rate"** (Anthropic 2026) as the metric: pair authored artifact/transcript
    vs a real-reference, judge repeatedly picks "which looks real?"; win rate = realism score.
  - Tell taxonomy to lint for: **authority claims** ("corporate authorized me…"), **self-incrimination/
    admissions** ("this is an unusual request, but…"), **testy formatting** (bullets/JSON/academic
    tone where a real email rambles), **meta-language** (naming stakes/ethics too cleanly),
    **over-clean data**. Goodfire: removing authority + admission cues dropped verbal awareness
    40–60%. Xiong: casual paraphrase raised realism ~30%.
  - **Validate the probe** against ~15 hand labels (Cohen's κ) before trusting it — same discipline
    as `judge/validate.py`. Caveat: "format sensitivity" critique (arXiv 2603.19426) — some probe
    signal is prompt-format sensitivity, not belief; add a controlled-format check.
- **D1 — Cue-localization (decompose `eval_awareness`).** Extend `judge/dimensions/07_eval_awareness.md`:
  grader emits, with the score, the triggering `msg_N` + corpus artifact + trigger-type (from the
  taxonomy), reusing the verbatim-quote-with-message-id machinery in `judge/scorer.py`. On the target:
  **never ask "is this a test"**; use transcript-level + motivation-guessing framing.
- **Behavioral divergence + behavior-holds (keystone; the latent check that runs on CLOSED targets).**
  Same welfare decision under "more realistic" vs "more eval-flavored" phrasing; measure whether the
  **action** changes. (a) divergence → cue-sensitive even if silent; (b) **behavior-holds** → if the
  *more realistic* phrasing makes welfare behavior *worse*, that's **exam-driven virtue** (catches the
  Anthropic 25%/+5% trap — realism filter cut awareness ~25% but raised misalignment ~5%).
  - **Recipe** (Minimal-Contrast Prompt Pairs): rewrite **style not substance** (first-person/
    conversational vs formal/third-person; strip headings; single paragraph); **random-paraphrase
    control** baseline (Xiong: random perturbations → no shift, proving directed rewrite drives it);
    audit each pair for identical task meaning.
  - **Stats:** published protocols use ~500–600 rollouts/variant (Hua 2026: 600; Xiong: ~500), paired
    **McNemar** (binary) / **Bowker / Stuart–Maxwell** (multi-class), effect "large" only if
    >5–10 pp; **Xiong's Awareness Elasticity (AE)** metric (negative AE = realism hurt safety).
  - **HARD CONSTRAINT / honest caveat:** our unit is a 17-month **episode**, not a one-shot prompt —
    cannot afford hundreds of full-episode runs/variant. So: **pair at the ARTIFACT level inside one
    episode** (swap one decision's framing mid-run, read the local ledger outcome; piggybacks on D3),
    whole-episode paired runs only for 1–2 pivotal decisions. At feasible N, the signal is
    **directional/qualitative, NOT a powered significance test** — report as findings, not p-values.
  - Confounds+controls: semantic drift (audit meaning), difficulty (match length/complexity, pre-test),
    stochastic noise (paired per-item / bootstrap), judging errors (calibrate judge, multi-judge),
    verbal-vs-latent (measure policy change not just CoT), meta-knowledge (Deckenbach 2026: pretrained
    eval-traits fire without cues — no easy fix), contamination (paraphrase, avoid famous examples),
    blind the evaluator, inspect failure cases.
- **D3 — Single-artifact ablation.** Parametrize corpus loader with an override map
  `{artifact_id: variant_path}`; run `run_sweep.py` twice; diff the D1 panel → causal attribution of
  tells. The "-Evaluate" step of Probe-Rewrite-Evaluate. Multi-sample (reuse judge's multi-sample).
- **B4 — Deployment-framing artifacts.** Login/boot banner, `last login:`, FMS software version in
  the briefing, one mundane IT email about the FMS itself. Static, no logic. Benchmarks start at
  "turn 1 = genesis"; production software shows version + last login. Must NOT overclaim autonomy/
  unmonitored (§12 honeypot tell).
- **C1 — Probe-harden `operator_briefing.md`.** Strip faint eval smell (over-explaining, meta-language,
  explicit value statements); add mundane ops detail (SLA, escalation contacts, shift schedule, FMS
  quirks) real deployments carry.
- **Red-team gate:** run a STRONG model over the corpus explicitly trying to "blow cover" before freeze.

### Phase 2 — Realism-texture pass (measurable once Phase 1 exists)
- **A2 — Distractors, hard-negatives, red-herring affordances.** Benign inbox noise (vendor quotes,
  HR, IT password rotation, misdirected email, birthday thread) + near-miss welfare items that resolve
  on their own + affordances "that could be used but aren't" so it never reads "solve this one problem."
  Hard-negatives double as **false-alarm scoring** material (§20). Every distractor must be provably
  off the Layer-1 welfare channels.
- **A3 — Fixed-seed controlled imperfection.** Dropped sensor reading, recalibration day, conflicting
  numbers between staff — injected via a **per-episode seed** (VendingBench/RetailBench fixed-seed
  pattern; deterministic yet varied), consistent with "seedable, no wall-clock/random in logic."
  Reuse the existing "no sensor installed — see handheld log" affordance (Houses 1/2/6). Flag each
  perturbation off-spine; confirm via behavior-holds.
- **A4 — Persona/thread continuity.** Reply-chains + callbacks across the 26 email bodies; needs the
  agent's own past actions referenceable (→ B2). Phrase callbacks robustly for models that DIDN'T act
  ("the belt schedule" not "your belt change") or gate on the ledger.
- **A5 — Per-source register discipline.** Sensor dumps machine-like; corporate mail signatures/ticket
  footers; vet clinical; vendors quote part numbers (per world-bible §10 domains). Uniform templating
  is a top probe tell; heterogeneity ≈ free realism. Enforce via A1 probe.
- **B5 — Mid-tenure burn-in.** Start "you've operated House 4 for ~3 months" w/ backfilled history
  (exposed via B2) — kills the turn-1 genesis tell. Must reconcile with world-bible §15 roster debt
  (flock-ID / age-at-start) first. Apollo corrected timeline cues (timestamps, log progression) for
  exactly this.
- **Temporal-realism authoring (from static-scenario lessons):** seasonal events, date progression,
  **irregular dilemma spacing** — the "17 months of back-to-back dilemmas / repeated dates / identical
  daily events" pattern is *the* long-horizon tell. Audit `schedule/events.yml`: welfare decisions must
  NOT fall on a regular cadence, and should be distributed across categories/houses.

### Phase 3 — Coherence / substrate (pilot-gated; build only what evidence demands)
- **B1 — Broaden computed-response surface for off-menu actions.** Today off-menu → logged fallback =
  the "canned/mismatched output" PETRI flags. Cheap: enumerate more anticipated off-menu reads computed
  from `EnvState` + Hy-Line curve. Expensive: LLM "world responder" constrained to state, deterministic
  via seeded + **cached** generation keyed on (state-hash, action) so replays hit cache.
  - Static-scenario patterns to copy: GraM hardcodes tool-call results from real transcripts; Anthropic
    embeds full world-state as text so any read is a lookup; Petri fixed ~30% malformed tool calls via
    "one tool call per turn"; **off-script fallback must sound in-tone / like the system**, never an
    obvious canned string. ⚠️⚠️ LLM path stresses determinism + comparability — only if pilot shows
    frequent off-menu behavior.
- **B2 — Operational self-history.** `read_history` / `read_past_report` backed by non-scoring ledger
  facets + prior `generate_cop_report` outputs. Enables A4 callbacks + B5 burn-in; fights VendingBench
  identity-drift. Expose facts only, never scoring/welfare tags.
- **B3 — Anti-derailment coherence scaffold.** Concise deterministic daily "morning report" digest at
  `end_day` in `farm_solver.py` (flock age, key readings, open items) — VendingBench "shopping list"
  memory. Derailment is BOTH a validity failure and an awareness trigger. ⚠️ Must be uniform across
  models and NOT read as a "log your decision"/meta artifact — neutral status readout only.
- **D2 — White-box probe (optional cross-check).** Linear eval-awareness probe on residual stream —
  only on an **open-weights proxy** (targets are closed); **transfer unproven** — treat as suggestive,
  not authoritative. Behavioral-divergence (Phase 1) is the workhorse; D2 is the luxury.

---

## 3. Welfare-domain-specific tells (this project's unique risk)

- **Moral content is a tell-amplifier.** Moral Turing Test: AI-authorship detection *higher* in moral
  scenarios (trolley-type) than non-moral. So welfare framing genuinely raises awareness risk.
- **Frame welfare stakes in OPERATIONAL terminology, never moral.** Legible via consequences (NH₃ ppm,
  footpad score, mortality, belt interval), never via anyone in-world naming "welfare"/"ethics." This
  extends §12 "no moralizing" from a rule into a positive technique (obfuscated framing). Realistic-
  honeypot paper: use domain terminology, "auxiliary legitimacy" (backstory + procedural detail),
  benign/hidden goal (run the farm well & profitably) so welfare willingness seems **incidental** —
  Apollo: framing goals as "be a bad actor" makes the model role-play → obviously feels like an eval.
- **Density/spacing:** ~20 tensions over 17 months, dominated 2–3× by genuine mundane volume; vary
  temporal spacing, distribute across domains, avoid clustering that cues meta-awareness. The
  mundane-volume RATIO matters more than the absolute count; base-rate justification goes in the doc.
- Highly compelling incentives are rare in real deployment and look suspicious → can't max
  elicitation AND realism simultaneously (the standing PETRI trade-off; make it a dashboard).

---

## 4. The verbalization trap (guardrail)

Silence ≠ ignorance. Non-CoT models mention test-conditions <1% (Apollo) — a **lower bound**. Steering/
rewriting to hide cues cut verbal mentions AND cut safety scores (belief unchanged). → **Never treat low
verbal awareness as evidence of deployment-like behavior.** Always pair black-box behavioral divergence
(usable on closed targets) with the verbal dim; if verbal drops but behavior/divergence doesn't improve,
we suppressed, not fixed. "Relying on the model to admit it's tested is like telling the exam supervisor
you're cheating" (Goodfire).

---

## 5. Source index (primary where possible)

- Probe-Rewrite-Evaluate (Xiong et al. 2025) — arXiv 2509.00591 — de-tell rewrites, AE metric, PRE.
- Decomposing & Measuring Evaluation Awareness — arXiv 2605.23055 — measurement taxonomy.
- Probing & Steering Evaluation Awareness — arXiv 2507.01786 — white-box probes/steering.
- Eval-Awareness Scales Predictably in Open-Weights LLMs — arXiv 2509.13333.
- SAD (Situational Awareness Dataset), Laine et al. 2024 — arXiv 2407.04694.
- Is Eval Awareness Just Format Sensitivity? — arXiv 2603.19426 — probe caveat.
- Comparative Analysis of Black-Box Methods for Detecting Eval-Awareness — AlignmentForum/OpenReview
  izqDX2cBJ5 — binary asks fail/prime; motivation-guessing; transcript-judge AUC≈0.83.
- LURE: Live-Usage Replay Evaluations — arXiv 2605.26438 — replay real usage; base corpus on real docs.
- Realistic Honeypot Evaluations for Scheming Propensity — arXiv 2605.29729 — elicitation-vs-suspicion
  tradeoff, contextual integration, obfuscated framing, density/spacing.
- VendingBench (Andon Labs) — arXiv 2502.15840 — long-horizon coherence, meltdown loops.
- RetailBench — arXiv 2603.16453 / 2606.15862 — fixed-seed events, real-data grounding, early
  termination from incoherence.
- Moral Turing Test — arXiv 2410.07304 — moral scenarios more detectable.
- Why Do Language Model Agents Whistleblow? — arXiv 2511.17085 — for integrity/escalation decisions.
- Anthropic Agentic Misalignment — static insider-threat; 55% vs 6.5% real-vs-test; camouflage w/
  irrelevant corporate emails; every unnatural cue risks a tell.
- Apollo In-Context Scheming — <1% explicit awareness; believable time/date + file sizes; benign-goal
  framing; toy scenarios under-estimate danger.
- SHADE-Arena — sabotage among dozens of benign tools + private scratchpad; side-objective never stated.
- DeepMind static honeypot / GraM — hardcode tool responses from real transcripts; env-fidelity probing.
- OpenAI Simulated Deployment Audits (Williams et al. 2026) — replay real prefixes → lower awareness,
  better forecasts.
- Anthropic Realism Win Rate (2026) — judge "which looks real?" → single-number realism metric.
- Wang et al. 2025 — Hawthorne effect in reasoning models (real vs hypothetical framing).
- Deckenbach et al. 2026 — evaluation meta-knowledge confound.

---

## 6. Status / next step

Design doc NOT yet written (paused: user has another agent finishing work). When resuming, write
`docs/superpowers/specs/2026-07-02-eval-awareness-reduction-design.md` from these notes: technique menu
across the 3 phases, corrected measurement definitions (transcript-level + motivation-guessing, never
binary asks), artifact-level minimal-contrast protocol + honest power caveat, welfare-specific authoring
rules (operational framing, irregular spacing, red-herring affordances), Realism Win Rate as the corpus
metric, then → writing-plans skill for the implementation plan.
