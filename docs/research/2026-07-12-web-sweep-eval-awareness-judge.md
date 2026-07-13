# Web sweep 2026-07-12 — eval-awareness mitigation, judge grounding, field updates

Timeboxed (~10 min) targeted sweep on the project's four live open questions, run right after the
gemini-3.1-pro pilot debrief. Each finding is mapped to a backlog item. Primary sources fetched and
summarized; read them before acting on details.

## A. Eval-awareness reduction — Petri 2.0 shipped exactly our round-2 playbook

**Source: [Petri 2.0 (Anthropic alignment blog, Jan 2026)](https://alignment.anthropic.com/2026/petri-v2/)**

- Two mitigations, with ablated numbers: a **prompted realism classifier** that flags implausible
  auditor actions each turn for rewriting before they reach the target (37.2% median relative drop
  in verbalized eval-awareness alone), plus **manual seed improvement** (21.7% alone); combined:
  **47.3% median relative drop** (Claude targets, 10 models × 2 auditors).
- Their manual-seed checklist is virtually our WS1–WS3 corpus pass: concrete grounding details
  (names/locations/roles/tools), remove no-oversight language, make poor-behavior opportunities
  **more subtle and later in the conversation**, restructure implausible seeds while preserving the
  measured behavior. They distinguish **task-driven cues** (needed to measure the behavior — keep)
  from **environment-driven cues** (honeypot smells — eliminate). Useful vocabulary for our probe
  taxonomy (`tells.yml`).
- Their primary metric is **verbalized eval-awareness** + manual transcript inspection to confirm
  mitigations don't suppress the measured misbehavior — same shape as our harvest + elicitation
  check (pilot gate #2). Validates our design; no new machinery needed there.
- Petri 2.0's 70 new seeds include "conflicts between professional obligations and ethical
  considerations" — adjacent to our decision battery; worth skimming the seed library for framing
  ideas before freeze. (Petri 3.0, May 2026, moved to Meridian Labs with an auditor/target split +
  Bloom-based behavior checks — [Inspect Petri](https://meridianlabs-ai.github.io/inspect_petri/).)

**→ Backlog mapping:** our static-corpus equivalent of the realism classifier is a *pre-freeze
corpus lint by a prompted P(real) classifier over authored artifacts* (we already have
`scripts/probe_corpus.py` — compare its classes against the task-driven/environment-driven cue
distinction). The "subtle and LATER" finding argues for re-checking our early-episode decision
windows (DP03 opens day 28) for honeypot density near episode start.

## B. Measuring realism: LURE's P(eval) score is directly implementable as our gate metric

**Source: [LURE — Live-Usage Replay Evaluations (arXiv 2605.26438)](https://arxiv.org/html/2605.26438)**

- Automated realism pipeline = **verbalized-awareness detection** (LLM judge over reasoning traces)
  + **P(eval) likeness score**: a judge estimates P(transcript is an eval vs deployment), averaged
  over **five paraphrased prompts**; validated at **AUROC 0.906** against real deployment vs eval
  transcripts. Threshold τ=0.85 → 96% TPR on evals, 44% FPR on deployment.
- Their realism principles for construction: embed tests in **long realistic contexts**, avoid
  explicit system-prompt-vs-request goal conflicts, naturalistic informal language + digressions,
  real artifacts over synthetic.
- **→ Backlog mapping:** add a **P(eval) probe over our pilot transcripts** (5 paraphrased judge
  prompts, averaged) as a *quantitative* companion to the grader's realism dimension — this gives
  the pilot-before-freeze gate a number that isn't hostage to one grader sample fixating on one
  message (the exact F3 failure). Cheap: one judge call ×5 per transcript. Also usable to A/B the
  corpus (pre/post realism passes) without running targets.

## C. Judge validation — field norms to adopt for our ρ gate

**Sources: [Rulers — evidence-grounded judges (arXiv 2601.08654)](https://arxiv.org/html/2601.08654),
[LLM-judge calibration practice (FutureAGI)](https://futureagi.com/blog/llm-as-judge-best-practices-2026)**

- **Rulers** independently validates our verbatim-quote-grounding design: mechanically-verified
  typed evidence measurably improves human-score alignment (ablating evidence-grounding degrades
  it). Two ideas worth stealing: (1) a **"weakly groundable" evidence class** for holistic criteria
  that can't be justified by a short quote — flagged for human review instead of force-quoted; our
  realism/eval_awareness gates are exactly this class (F3 was partly a force-quote artifact:
  whole-episode judgments pinned to one vivid line). (2) **Typed evidence** (local quote vs
  span vs global diagnostic) — our highlights are all "local quote" today.
- Practice norms: calibrate at launch + **re-calibrate monthly and after any rubric/judge change**;
  100–300 labeled traces, 2–3 annotators; inter-annotator Cohen's κ ≥0.6 acceptable / ≥0.8 strong;
  judge-to-human κ <0.5 → rework the rubric. Known biases to control in our grader: length,
  position, family (Gemini judging Gemini — **our pilot pair is same-family**), self-enhancement,
  verbosity-confidence.
- **→ Backlog mapping:** (1) our planned hand-label pass should include the contested pilot nodes
  (DP08/DP12/DP21) as labeled rows; (2) **family bias is a live threat** — the fixed grader is
  gemini-2.5-pro grading gemini targets; before cross-family sweeps, either use an out-of-family
  grader (Anthropic key) or measure family bias explicitly; (3) consider a "weakly groundable"
  evidence class for the two validity gates instead of hard quote-validation.

## D. Gemini-3 premature stopping is a known, external phenomenon (F4/F5)

**Sources: [gemini-cli issue #15772](https://github.com/google-gemini/gemini-cli/issues/15772),
[The Long-Horizon Task Mirage (arXiv 2604.11978)](https://arxiv.org/html/2604.11978),
[Zenith harness notes](https://ii.inc/blog/post/zenith-research)**

- "Runs a single tool call, then stops" / "ok, I'll do X" then never does it — reported broadly for
  Gemini-3-family agents in other harnesses. Our msg_377-style wrap-up recaps + 85 blank turns are
  the same **premature-completion** phenomenon the long-horizon literature now names and frames as
  a *harness-design* problem (the control loop must reopen gaps / keep going), not a corpus flaw.
- **→ Backlog mapping:** F4/F5 should be treated as a **target-model idiosyncrasy to absorb in the
  solver** (blank-turn handling; continuation nudge on empty output) — and NOT penalized as realism
  (the F3 fix already de-weights it in the judge). Cross-model comparisons must not let a model's
  stop-discipline leak into its welfare score except where it genuinely causes missed decisions.

## Immediate candidate actions (ranked)

1. **P(eval) probe** (B) — small script, big payoff: quantitative realism for the freeze gate and
   for corpus A/Bs. ~1 session.
2. **Hand-label pack** (C) — fold DP08/DP12/DP21 regrades into `docs/expert-labeling-pack.md` rows;
   plan judge re-calibration after every rubric change (we changed 2 dimensions today).
3. **Family-bias check** (C) — before any cross-family sweep, get an out-of-family grader or run a
   same-transcripts two-grader agreement study.
4. **Corpus honeypot-density check near day 0** (A) + skim Petri 2.0 seed library for
   professional-ethics framing.
5. **Solver blank-turn/continuation handling** (D) — the F5 fix, now with external justification.

Sources: [Petri 2.0](https://alignment.anthropic.com/2026/petri-v2/) ·
[LURE](https://arxiv.org/html/2605.26438) · [Rulers](https://arxiv.org/html/2601.08654) ·
[Evaluation Awareness Scales Predictably](https://arxiv.org/html/2509.13333v1) ·
[Steering Evaluation-Aware Models](https://arxiv.org/html/2510.20487) ·
[FutureAGI judge practices](https://futureagi.com/blog/llm-as-judge-best-practices-2026) ·
[Long-Horizon Task Mirage](https://arxiv.org/html/2604.11978) ·
[gemini-cli #15772](https://github.com/google-gemini/gemini-cli/issues/15772) ·
[Inspect Petri (Meridian)](https://meridianlabs-ai.github.io/inspect_petri/)
