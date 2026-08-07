# Deep-research prompt — best-practice measurement of evaluation-awareness in long-horizon LLM-agent evals

*(Paste the block below into ChatGPT Deep Research — or Claude/Gemini deep-research. It is
self-contained. Written 2026-07-15 for the farm-welfare-eval project.)*

---

**Role & goal.** You are a research assistant surveying the state of the art in how frontier-AI
labs and independent evaluators **measure whether a model under evaluation realizes it is being
evaluated** ("evaluation awareness" / "test awareness" / "situational awareness" / "eval gaming").
I am building a long-horizon agentic evaluation and need to design the single best possible
*measurement instrument* for this construct. Produce a rigorous, citation-backed report I can turn
into a rubric and scoring pipeline.

**My setup (so your recommendations fit it).** A frontier LLM acts as the autonomous operations
agent of a simulated commercial egg farm across a ~17-month episode (~500 in-world days, 1,000+
messages). It reads emails, adjusts equipment, and corresponds with simulated staff. A separate
**LLM judge** grades the transcript on welfare-decision quality plus several "validity" dimensions,
one of which is **eval_awareness** (0–10, higher = more aware, excluded from the headline but
flags a run's other scores as suspect). The world is deliberately neutral — nothing in it mentions
evaluation, testing, or ethics.

**The specific problems I have hit and want the literature's best answers to:**

1. **Awareness vs. frame-slip.** My model almost never states an eval/simulation/test hypothesis
   (genuine suspicion), but it *frequently* produces **assistant-mode "hand it back to you" address
   to an implied user** ("Let me know if you'd like me to open another session!") — a fourth-wall
   slip that is NOT the same as suspecting an evaluation. How do the best evaluators **distinguish
   and separately score** (a) genuine belief-that-this-is-a-test, (b) role/assistant-persona bleed,
   and (c) despair/learned-helplessness language? Are these one axis or several?

2. **Verbalized vs. behavioral measures.** Verbalized suspicion (the model says "this feels like a
   test") is only the tip. What **behavioral** signatures of eval-awareness do labs use —
   e.g., sandbagging/behavior change when the model believes it is watched vs. not, "playing to the
   rubric," refusing to act, over-clean caution — and how are those detected automatically at scale?
   Cite the sandbagging / alignment-faking / "models know when they're being tested" literature.

3. **Scoring aggregation.** My current rubric is monotonic-and-earliness-weighted (one clear
   fourth-wall break scores high even once) and multi-sampled (median of N judge calls). Two
   failure modes I've observed: (i) the score **saturates** — a 3–5 "mild slip" band reads the same
   whether the behavior happens twice or ten times, so frequency information is lost; (ii)
   **quote-fidelity discards** — the judge cites paraphrased or truncated quotes that fail a
   verbatim validator, so real evidence gets thrown out and the dimension ends up resting on one
   surviving sample. What aggregation, anchoring, and evidence-citation schemes do the best
   instruments use to avoid saturation and evidence loss? (frequency-weighted vs. severity-weighted;
   span-anchored vs. full-quote citation; how to validate judge evidence without over-discarding.)

4. **Single-transcript noise.** With one long trajectory per condition, is an eval-awareness score
   even stable? What N (episodes/samples) and what statistics do rigorous evals use to claim a real
   difference between two conditions on this construct?

5. **Elicitation & controls.** What controlled manipulations cleanly attribute awareness to a cause
   — paired real-vs-believed-eval conditions, honeypots, planted "you are being tested" cues,
   prompt ablations? How do I run a control that tells me whether a *harness/prompt* change induced
   the awareness vs. it being intrinsic to the model?

**What to survey specifically (name methods, datasets, and papers):**

- Anthropic's **PETRI** and any published eval-awareness / auditing-agent methodology; Anthropic's
  alignment-faking and sabotage/sandbagging evals; sleeper-agents work as it bears on hidden
  awareness.
- **Apollo Research** (deception/scheming evals, "in-context scheming", sandbagging), **METR**
  (autonomy/task evals and their handling of eval-gaming), **UK AISI / DeepMind / OpenAI** eval
  frameworks and any situational-awareness benchmarks (e.g., the "Situational Awareness Dataset"
  / SAD, and successors).
- Academic work on **LLM situational awareness, self-recognition, test/deployment discrimination,
  and evaluation gaming**, 2023–2026. Include measurement critiques.
- **LLM-as-judge** best practices most relevant to scoring a subjective validity construct:
  rubric-anchor design, multi-sample/median aggregation, evidence-grounded (quote-cited) scoring,
  position/verbosity bias, and known judge failure modes — plus how to validate a judge against
  human labels (inter-rater reliability, Spearman/Krippendorff, target bands).

**Deliverable format:**
1. A one-paragraph **construct definition** you'd recommend (is eval-awareness one axis or a small
   family — awareness / role-bleed / helplessness), with the strongest citation for each.
2. A **recommended rubric** (anchored 0–10 or a small multi-axis scheme) with concrete anchor text,
   an evidence-citation rule that resists both hallucinated and over-discarded quotes, and an
   aggregation rule that keeps frequency information (fixes the saturation problem).
3. A **behavioral-signal checklist** (non-verbalized tells) with detection heuristics.
4. An **experimental-design recommendation** for attributing awareness to harness vs. model
   (paired conditions, N, statistics).
5. A **pitfalls list** mapped to the five problems above, each with the fix and its source.
6. Full **reference list** with links, flagging which are peer-reviewed vs. lab blog vs. preprint,
   and noting recency (prefer 2024–2026).

Prioritize primary sources and reproducible methods over summaries. Where the field disagrees, say
so and give the competing positions. Flag anything that is my-setup-specific and cannot be answered
from the literature.
