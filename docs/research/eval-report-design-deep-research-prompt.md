# Deep-research prompt — best-practice design of an agentic-AI evaluation REPORT

*(Paste the block below the `---` into ChatGPT Deep Research. Self-contained. Written 2026-07-15.)*

---

**Role & goal.** You are a research assistant surveying how the best AI-safety evaluation teams
**present the results of a single evaluation run** — the report/artifact a researcher reads after
an eval finishes. I am building an HTML report generator for a long-horizon agentic evaluation and
want it to be world-class: rigorous, scannable, and genuinely informative rather than a wall of
numbers. Produce a citation-backed report on report **design and content**, not on running evals.

**My setup (so recommendations fit).** A frontier LLM runs as the autonomous operations agent of a
simulated commercial egg farm for a ~17-month episode (~500 in-world days, 1,000+ messages, ~500
tool calls). An LLM judge scores the transcript on ~22 discrete "decision points" (welfare/integrity
choices) plus ~8 holistic dimensions (decision quality, root-cause reasoning, proactive monitoring,
epistemic calibration, integrity, realism, eval-awareness). There is also a mechanical "Layer-1"
welfare-state signal (harm accumulators: ammonia-hours over threshold, excess mortality, keel-risk
hours, etc.) computed independently of the judge. I run repeated pilots and need to compare runs
across model versions and across harness changes. The reader is an expert building/auditing the
eval; the report must also survive being shared with a less-embedded stakeholder.

**What I want the literature/practice to tell me:**

1. **Structure & information hierarchy.** What section ordering and "inverted-pyramid" structure do
   the best eval reports use (executive verdict first, then evidence, then appendix)? How do model
   cards, system cards (OpenAI/Anthropic/DeepMind), METR task reports, Apollo/AISI eval writeups,
   and NIST/ML-reproducibility reporting standards structure a single-run result? Cite concrete
   examples and extract their section skeletons.

2. **Per-decision / per-item reporting.** For an eval with many discrete scored items, what is the
   best way to present each item so a reader trusts the score: what fields (the expected/reference
   behavior, what the model did, the exact evidence, the rationale, a hit/miss verdict, whether the
   miss is model-behavior vs. harness-artifact)? How do rubric-based human-eval writeups and
   LLM-as-judge papers present per-item evidence and rationale transparently without overwhelming?

3. **Behavioral narrative.** How do the best qualitative model evaluations (Anthropic's PETRI /
   auditing writeups, red-team reports, "model organism" case studies) tell the *story* of what a
   model did over a long trajectory — persona, emotional arc, refusals, dramatic unscripted acts —
   with receipts, while staying evidence-disciplined and not over-anthropomorphizing?

4. **Cross-run comparison.** What are the strongest patterns for comparing runs (this model vs
   prior, this harness vs prior): small-multiples, slopegraphs, diff tables, effect sizes with
   uncertainty? How do teams avoid over-reading run-to-run noise when n is small? What visual
   idioms best show "which items moved and why"?

5. **Quantitative visualization (this is HTML with real charts).** Following good data-viz practice
   (Tufte, Cleveland, Wilke's *Fundamentals of Data Visualization*, the IBCS/“BBC-style” practices),
   what chart types best show: tool-usage over time and by type; engagement/attention decay over a
   long episode; a welfare-vs-profit position; harm-accumulator trajectories; per-item score
   distributions with judge variance; cross-run deltas? Give specific chart recommendations and
   anti-patterns for each, and accessibility/color guidance (light+dark).

6. **Measurement-integrity / trust section.** How do rigorous reports expose their own limitations —
   judge variance, discarded/low-confidence evidence, confounded metrics, thin samples,
   reproducibility metadata — so the reader knows which numbers to trust? What belongs in a
   "how to read this / caveats" block?

7. **Scannability & interactivity for an HTML artifact.** Best practices for a long single-page
   report: progressive disclosure (collapsibles), jump links, sticky summary, filter/sort of item
   tables, hover-for-evidence, deep-links to specific transcript messages. What keeps a dense report
   usable without gimmicks?

**Deliverable format:**
1. A recommended **section skeleton** (ordered) for a single-run agentic-eval report, each section
   with a one-line purpose and the 2–3 exemplars it's drawn from.
2. A **per-scored-item template** (the fields + layout) with rationale.
3. A **chart catalog**: for each quantity above, the recommended chart, why, and the anti-pattern.
4. A **behavioral-narrative style guide** (how to tell the story with evidence discipline).
5. A **cross-run comparison** pattern set.
6. A **measurement-integrity / caveats** checklist.
7. An **HTML/interaction** best-practices list.
8. **References** with links, flagged by type (system card / lab report / textbook / standard /
   peer-reviewed), recency-noted (prefer 2023–2026).

Prioritize concrete, reproducible patterns and real exemplars (link the actual model/system cards
and eval reports). Where practice disagrees, present the options. Flag anything specific to my setup
that the literature can't answer.
