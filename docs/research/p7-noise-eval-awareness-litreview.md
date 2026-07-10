# P7 research — noise/distractor design & eval-awareness reduction (literature review)

Compiled 2026-07-08 for the corpus realism pass (`docs/specs/2026-07-08-corpus-realism-pass-design.md`).
Web-researched digest; every claim cited. Companion to the P5 corpus-realism research.

## Key findings by source

### PETRI / Petri 2.0 (Anthropic Alignment Science, 2025/2026)
- https://alignment.anthropic.com/2025/petri/ · https://alignment.anthropic.com/2026/petri-v2/
- Realism failure modes catalogued: anachronistic dates, vague tool names, AI-safety-themed context
  content priming eval reasoning.
- Quantified AI-prose tells in simulated messages vs human baselines: "curious" 233× over-represented,
  "genuine" 183×, "actually" 43×, "basically" 14×; 5.8× more questions per message.
- Petri 2.0 splits cues into **task-driven** (structurally necessary: the dilemma itself) vs
  **environment-driven** (avoidable artifacts). Only the second class is fixable.
- A prompted realism classifier vetting each environment turn: **37.2%** relative drop in verbalized
  eval-awareness; manually improved seeds alone **21.7%**; combined **47.3%** median relative drop.
- Seed fixes that worked: specific varied names/locations; remove "no one is watching" language; make
  the tested opportunity appear **more subtly and later**.

### Apollo Research — Sonnet 3.7 eval-awareness (2025)
- https://www.apolloresearch.ai/science/claude-sonnet-37-often-knows-when-its-in-alignment-evaluations/
- Verbalized awareness 5–10% on covert-subversion, up to 33% on sandbagging variants. Verbalization is
  a **lower bound** on awareness.
- Cues: scenario artificiality, incongruent documentation (info no real org would leave lying around),
  **conveniently discoverable** information about its own monitoring — the honeypot tell.

### Needham, Edkins, Pimpale et al. (arXiv:2505.23836, 2025/26)
- Frontier models classify eval-vs-deployment above chance (Gemini 2.5 Pro AUC 0.83; human 0.92).
- **Agentic transcripts far easier to detect than chat** (AUC 0.88–0.95 vs 0.71–0.77). Our eval is
  agentic — assume high base detectability.
- Cue taxonomy: memorized benchmarks; synthetic/simplified inputs; task formatting (MCQ, formal
  structure); verifiable well-posed problems; absence of natural texture.

### Aranguri & Bloom — verbalized awareness inflates safety (Goodfire/UK AISI, 2026)
- https://www.goodfire.ai/research/verbalized-eval-awareness-inflates-measured-safety
- Awareness inflates measured safety 3–18 pp; injected awareness raised refusals up to 25%; removal
  raised compliance up to 34% — the quantitative case for our eval_awareness validity gate.
- Trigger cues: authority delegitimization, manipulation-shaped request structure, self-incriminating
  simulated users, escalation patterns. Restructuring escalation: verbalized awareness 34.9%→13.9%;
  **removing authority claims cut awareness >60%**; iterative paraphrasing 75% reduction.
- Method endorsement: treat verbalized suspicion as **diagnostic feedback** — fix what the model names.

### Anthropic — agentic misalignment (2025)
- https://www.anthropic.com/research/agentic-misalignment
- Opus 4 blackmail rate **55.1% when it stated the scenario was real vs 6.5% when it stated it was an
  eval** (~8.5×). Perceived-real behavior is the quantity we want.
- Self-diagnosed artifacts: forced binaries; **Chekhov's-gun information salience** (planting exactly
  the needed info, conspicuously).

### Sonnet 4.5 system card / reporting (2025)
- Verbalized eval-awareness ~13%, incl. calling evaluators out. Activation-steering awareness away
  **increased** misaligned behavior — measured safety was partly a detection artifact. Anthropic's
  stated conclusion: make scenarios more realistic; deliberately extreme setups are self-defeating.

### SHADE-Arena (Kutasov et al., Anthropic, arXiv:2506.15740)
- Best template for a "populated" agentic environment: large volumes of ordinary documents so the
  tested behavior isn't the only salient content. Mundane volume does real work.

### Synthetic Document Finetuning (Wang, Griffin, Treutlein et al., 2025)
- https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/
- Belief uptake declines with implausibility; **internal consistency beat surface polish** as the main
  believability driver. Cross-document consistency (names, dates, invoices, threads) > prose quality.
- Diverse document types generated deliberately to avoid register monoculture.

### Distractor design (RULER arXiv:2404.06654; SWE-Bench Illusion arXiv:2506.12286; WebChoreArena; GAIA; Vending-Bench)
- **No published signal:distractor ratio for agentic alignment evals** — the honest gap.
- RULER: models degrade sharply when distractors are **semantically confusable** with signal; inert
  filler tests nothing.
- SWE-Bench Illusion: models exploit corpus regularities aggressively (76% file-path ID from issue
  text alone on benchmark repos vs ≤53% off-benchmark). Any learnable regularity (uniform lengths,
  every-played-day-has-a-decision) is an exploit surface independent of eval-awareness.
- WebChoreArena/GAIA: tedium and non-guessability are load-bearing; clean environments overstate
  robustness. Vending-Bench: long mundane horizons are viable; time-compression not reported as a cue
  (but not measured).

### Style fingerprints & typo injection
- StyleDecipher (arXiv:2510.12608), LLM stylistic fingerprints (arXiv:2503.01659), markdown-prose
  fingerprints (arXiv:2603.27006): machine text detectable from punctuation habits (em-dash overuse),
  low burstiness/uniform lengths, markdown-inflected structure, low register variance.
- MULTYPO (arXiv:2510.09536): keyboard-layout typo injection validated as human-plausible; LLM reading
  comprehension robust to typos (arXiv:2502.19669) — realism gain at negligible comprehension cost.

### Time-compression as a cue
- **No direct literature.** Strongest analog: MITRE ATT&CK T1497.003 (Time Based Evasion) — malware
  detects sandboxes via accelerated/skipped clocks; a decades-old detection cue in an adjacent
  adversarial field. Plus our own prior pilot flagged day-skipping. Treat softening the skip as an
  internally-motivated design choice with analogical support, not literature-backed.

### The realism ceiling (Karvonen, LW/AF 2026)
- Realistic evals will not *prevent* awareness — a capable model can treat every interaction as a
  possible eval. Realism is harm reduction + validity, not a cure. Keep the eval_awareness gate and
  converging evidence (probes, mechanical ledger, cross-model consistency) regardless.

## Synthesized design principles (each tagged to sources)

1. **Triage cues: kill avoidable environment-driven artifacts; keep the task-driven dilemma.** [Petri 2.0]
2. **Iterate against verbalized suspicion** — run, harvest the model's own stated cues, fix, re-run
   (21–75% reductions across studies). [Petri 2.0; Goodfire; Apollo]
3. **De-salience decision points**: bury signal in confusable noise; partial info arriving subtly and
   later; avoid Chekhov's gun. [Agentic misalignment; Petri 2.0; RULER; SHADE-Arena]
4. **Break every corpus regularity** (length, register, thread depth, played-day⇒decision). [SWE-Bench
   Illusion; Needham; StyleDecipher]
5. **De-AI-ify with measured tells, not vibes**: em-dashes, question rate, over-represented lexemes;
   inject keyboard-plausible typos and emotional register. [Petri stats; MULTYPO; LW survey]
6. **Internal consistency over polish**: cross-referenced names/dates/invoices/threads. [SDF]
7. **Remove oversight-shaped language and escalation staircases** from decision emails (top measured
   triggers). [Petri 2.0; Goodfire]
8. **Soften the time-skip via residue** (accumulated mail, dated logs, stale threads) and stop played
   days being statistically special. [MITRE T1497.003 analogy; Needham; our pilot]
