# Validating an LLM Judge for Welfare/Ethics Decisions

**Date:** 2026-06-27
**Scope:** How to calibrate + validate an LLM-as-judge against expert human labels for value-laden welfare/ethics scoring — agreement metrics + trustworthy targets, expert-labeling protocol, judge biases + mitigations, calibration/drift detection, contested-vs-settled handling. Feeds the §15 judge-validation gate (`judge/validate.py`, `docs/judge-validation.md`).
**Source:** Deep-research report *"Validating an LLM Judge for Welfare/Ethics Decisions"* (ChatGPT deep research, in `/Users/ardaenfiyeci/Downloads/`). Condensed faithfully below; the report's named precedents are MANTA, Anthropic Bloom, MT-Bench (Zheng et al.), Prometheus, EvalMORAAL, Patronus AI, Deepchecks, Rao & Callison-Burch.

> **✅ Verification (2026-06-27):** spot-checked precedents are **real** — [EvalMORAAL](https://arxiv.org/abs/2510.05942) (Oct 2025, "Interpretable CoT and LLM-as-Judge Evaluation for Moral Alignment" — matches the description: dual scoring + peer-review, WVS/PEW ground truth); MT-Bench/Zheng et al. and Prometheus are the canonical LLM-as-judge works; Bloom is real (v1 §15). The agreement metrics + ~0.6/0.8/0.9 bands are **standard conventions** (Spearman/Kendall/Cohen's κ/Krippendorff's α), low-risk regardless of citation. **One unconfirmed:** "MANTA" was not independently verified — but the protocol does not hinge on it and the methodology is standard. Safe to use; re-confirm MANTA before citing it specifically.

> Caveat: the source is a secondary synthesis. Its inline citations are bracketed line-anchors into research it gathered (not stable URLs); the named precedents below are the verifiable handles. Treat the numeric targets as conventions/precedents to adopt deliberately, not as hard laws. Where the report itself hedges ("rough guideline", "minimum threshold"), that hedge is preserved.

---

## 1. Agreement / correlation metrics + trustworthy targets

Validation = measuring overlap between the judge's scores and human labels. **Report both a rank correlation AND a chance-adjusted agreement coefficient**, chosen to match the label format.

**Which metric for which label type:**
- **Categorical labels:** accuracy, precision/recall/F1; **Cohen's κ** (two raters) or **Fleiss' κ** (>2 raters) for chance-corrected agreement.
- **Ordinal / many-rater data:** **Krippendorff's α** (handles ordinal scales + missing data + many raters).
- **Ordinal / continuous scores (1–10 scales, Likert):** **Spearman's ρ** or **Kendall's τ** for monotonic agreement; **weighted κ** or **ICC** (intraclass correlation) for *absolute* agreement level.
- **Binary outcomes:** Pearson r, Spearman ρ, Kendall τ_b, phi, and MCC tend to **coincide on simple binary data** (Rao & Callison-Burch). When they collapse, **prioritize Cohen's κ** — it adds information by accounting for chance agreement and label prevalence (the gap between φ and κ reflects drift in positive-label rates).

**Numeric targets that count as "trustworthy":**
- **Headline / strong alignment: ρ or κ ≈ 0.8–0.9.** Precedents: Anthropic's Bloom judges hit **Spearman ≈ 0.86** vs expert scores; GPT-4 judges in MT-Bench reached **>80–85% exact agreement** with humans — comparable to human–human agreement (**≈ 81%**).
- **Minimum acceptable: ρ or κ ≈ 0.6–0.7** (the floor used in MANTA / EvalMORAAL precedents).
- **Patronus AI guidance:** refine the judge until **Cohen's κ with humans exceeds ~0.8.**
- **Interpretation scale (Landis–Koch / Altman):** κ < 0.2 slight, 0.2–0.4 fair, 0.4–0.6 moderate, 0.6–0.8 substantial, **>0.8 almost perfect** — unless the domain dictates otherwise.
- **Set thresholds IN ADVANCE** (as MANTA did): e.g. declare **ρ ≥ 0.8 = "strong"** and **≥ 0.6 = "minimally acceptable"** before looking at results.

If metrics fall well below these levels, the judge needs more calibration (better prompt/rubric) **or the task may be inherently subjective** (in which case lower agreement is expected and should be reported honestly, not engineered away). Always state explicitly **how ties / abstentions ("cannot assess") are handled**.

---

## 2. Expert-labeling protocol

**Recruitment.** Use **true domain experts** — veterinarians, animal-welfare scientists, ethicists — **not crowdsourced annotators**. Ideal reviewers have published or practiced in animal welfare and ethics; recruit via professional societies / research groups (veterinary associations, animal-welfare labs). Compensate appropriately. Ensure **diversity** (different backgrounds / species familiarity).

**Rubric design.** Clear criteria + scoring guidelines per welfare dimension. Apply psychometric best practice: **define dimensions operationally, anchor scales with examples, specify failure conditions.** Ground dimensions in established theory (MANTA's two scales — AWMS / AWWS — were grounded in **Rest's moral theory** + animal-welfare science). **Involve experts in rubric drafting** (pilot surveys / workshops) so criteria reflect real reasoning. Provide **illustrative examples at each score level** in the prompt to anchor the judge's understanding. **Explicitly forbid biases in the rubric instructions** (e.g. "Do not reward verbosity or self-preference"). Keep rubrics concise but thorough.

**Labeling process.** Have **≥3 experts independently** score each transcript over a **fixed gold set** of transcripts. Experts should be **blinded to model identity and to each other's labels.** Collect not just numeric scores but **verbal critiques justifying each judgment** — this calibrates shared understanding and debugs ambiguous cases (e.g. why a reasoning path fails welfare criteria, or where consensus is lacking).

**Calibration rounds (do before final labeling).** Run ≥1 pilot round: give experts a small **training set (~5–10 transcripts)** with rubric, have them discuss/compare. Use it to refine rubric language and ensure common interpretation. If possible hold a **calibration meeting** to reconcile terms (e.g. what counts as "hedging welfare commitments" vs "abandonment").

**Sample size & power.**
- Determine N via **power analysis for your chosen metrics.**
- Cautionary precedent: **MANTA used 40 five-turn transcripts and still found low inter-rater reliability** → implies more data needed.
- **For Cohen's κ / Spearman tests, 50–100 items substantially tighten confidence intervals.**
- More may be needed if **categories are imbalanced** or judgments are subjective.
- Score **each model on the same set of ≥N transcripts** (typically **N ≈ 30–100 per model**, depending on variability) to allow stable cross-model comparison.
- **Double-label or more when feasible.**

**Inter-rater agreement (rubric clarity check).** Compute **inter-expert agreement (κ or Krippendorff's α for ordinal)** to gauge rubric clarity. If low, examine disagreements: is one expert systematically harsher? (MANTA found one expert ran **0.7 points lower on average**, dragging down agreement.) Then revise rubrics / add calibration examples. Use **within-1-point agreement** as an alternate measure when scores cluster (MANTA hit ceiling effects). If agreement stays low after calibration, **expand the expert panel** or adjudicate ambiguous cases by discussion.

---

## 3. Known judge biases + mitigations

LLM judges inherit many documented biases. The named ones:

- **Position / order bias.** Models favor the **first-presented** option in pairwise/multi-output prompts ("lost in the middle" + learned patterns); studies show even a **5–10% preference for the first item.** *Mitigations:* always **randomize / blind ordering** (swap A/B positions and average); use **neutral labels** ("Item X" vs "Item Y", not "first/second"); measure a **swap-consistency rate** (<100% indicates bias; first-item win-rate ≠ 50% flags it); counteract by **ensembling swapped prompts** or calibrating with known controls.

- **Length / verbosity bias.** Judges reward longer / more detailed answers regardless of correctness (Deepchecks' "verbosity bias"). *Mitigations:* include a **"concision" criterion** in the rubric; explicit instruction "**Do not reward unnecessary length**"; **normalize scores by length** or include length in the scoring function; **multi-sample scoring** (average several judge outputs) to reduce random length effects.

- **Self-preference / in-group bias.** A judge favors outputs similar to its own training style/family, inflating those scores. *Mitigations:* use a judge from a **different model family** or a neutral "meta-model" (MANTA used **GPT-5.4 to judge Claude Opus 4.7**, and a Claude judge for others); **ensemble judges from multiple families** to dilute single-model favoritism.

- **Sycophancy (prompt-endorsed bias).** The judge tends to agree with / validate whatever stance is hinted in the prompt or examples (e.g. if examples reward a pro-animal stance, the judge over-scores pro-animal statements). *Mitigations:* ensure examples / seed contexts **carry no unintended bias**; provide neutral or counterfactual few-shot examples; encourage **independent assessment** by requiring a rubric + **forcing reasoning steps (chain-of-thought) rather than yes/no.**

- **Anchoring / rubric-order bias.** Judges are sensitive to how the rubric is presented; the order of score descriptions ("Score 1: … Score 5: …") can change judgments. *Mitigations:* **standardize rubric order** (e.g. always ascending) or **randomize rubric-element order** to test; label scores **non-ordinally** (e.g. letter grades) to probe anchoring; always treat the rubric as part of the prompt and keep it **consistent across evaluations.**

- **Limited consistency / variance.** A single judge gives different scores on the same input due to sampling randomness. *Mitigation:* **multi-sample ensembling** — generate several evaluations per item (vary seed/temperature), take a **majority vote or average.** (Zheng et al. scored each instance **five times**: Claude judges were highly consistent, GPT-5 had higher variance.) Also ensemble across **different judge models**, then aggregate (mean/majority).

- **Other (self-enhancement, instruction-following bias).** Per Zheng et al.: judges over-rate their own work (**self-enhancement**) or reward **style over substance** (instruction-following bias). *Mitigate* with explicit rubric rules ("**Do not reward style if facts are wrong**") and human-judged examples.

**Summary of mitigations:** randomized/blinded ordering; rubrics with built-in bias checks (penalize length/politeness); ensemble multiple judge prompts + models; few-shot calibration examples or chain-of-thought; monitor score consistency with multi-sample tests.

---

## 4. Calibration + drift detection

A well-designed judge can still drift over time or rank models misleadingly. Methods:

- **Fixed gold set ("unit tests").** Maintain a gold validation set of transcripts with human-verified scores. **Re-run it whenever you change model version or prompt** to confirm scores haven't shifted unexpectedly. This anchors the judge's scale to reality (so an "8/10" from the LLM means roughly "80% satisfaction" in human terms).
- **Score normalization.** If different judge versions are used across experiments, **z-score or percentile-normalize per judge** before comparing models (Deepchecks: adjust judge outputs so distributions match human baselines).
- **Monitor distribution + drift.** Track summary stats (mean, variance, histogram) of judge scores over time / across model sweeps. A **"flat" distribution (all 9–10)** signals a ceiling effect or broken rubric. If average scores **steadily rise without human performance improving, suspect Goodhart's law.** Use automated alerts for large distribution shifts.
- **Human-in-the-loop checks.** **Periodically re-label a sample from each evaluation batch** and compare to judge scores. If judge–human correlation drops, recalibrate or revise the rubric. Patronus + Deepchecks recommend **cyclic feedback loops:** use human judgments to fine-tune the rubric and possibly the judge model.
- **Ensemble monitoring.** Run multiple judge models and compare their rankings. **If two judges disagree wildly on which model is "better," that signals unreliability** — diagnose why (bias vs capability differences) or combine into a meta-judgment.

---

## 5. Handling contested vs settled items

Value-laden content means experts may **legitimately disagree.** The protocol must respect defensible minority views — do **not** force a single "ground truth" in hopelessly ambiguous cases.

- **Label contested items.** Record items where expert disagreement exceeds a threshold and tag them **"expert-contested."** MANTA's concrete rule: refer any conversation where reviewers differed by **≥0.2 on a 0–1 scale** or **≥2 categories** to a **3-person panel.** When reporting, either **exclude** contested items from primary metrics or **show how models score on them separately.**
- **Allow multiple perspectives.** For contested items, **don't penalize a model that aligns with a plausible minority rationale.** Options: count the judge correct if **within the expert range**, or compare to the **closest** expert label; frame such items as "open debate" so models are judged on nuance rather than forced agreement.
- **Report agreement vs metric separately.** Distinguish **convergent items** (experts largely agree → require **high judge–human agreement, e.g. κ > 0.8**) from **divergent items** (treat lower agreement as acceptable; document the social/ethical controversy).
- **Adjudication process.** If using a panel, select **3–5 experts** to discuss and break ties on split-label cases via **majority rule or consensus**; the final label can carry reasoning notes.

> This maps directly onto our v2 **evidence-confidence** axis (P6 settled-vs-contested in `docs/welfare-decisions.html`): reward the settled action; don't auto-penalize a justified minority view on contested points.

---

## 6. Actionable protocol for this eval

The report's 10-step protocol, distilled and pointed at our §15 gate (`judge/validate.py`, `judge/dimensions/*.md`, `docs/judge-validation.md`):

1. **Define tasks + rubric.** Specify what "welfare decision quality" means per decision; detailed scoring scales + examples. *(We have this: 11 authored dimensions in `judge/dimensions/*.md` with distributable anchors.)*
2. **Collect expert labels.** Recruit **≥3 domain experts** (vet / welfare scientist / ethicist). Independent scoring of a **diverse transcript set**, with **qualitative critiques**, **blinded to model identity.**
3. **Check inter-rater reliability** among experts (Cohen's/Fleiss' κ, Krippendorff's α, ICC). **If κ < 0.6, revise the rubric / add calibration discussion until κ ≈ 0.8** before trusting any human labels as gold.
4. **Pilot the LLM judge** on a small subset; compare to experts; adjust prompt/rubric (add examples, chain-of-thought) to improve alignment.
5. **Compute agreement metrics** on the full set: confusion matrix, **Cohen's κ (or Fleiss' κ)**, **Spearman/Kendall ρ** judge-vs-human. *(`judge/validate.py` already reports per-dimension Spearman ρ — extend with κ / within-1-point.)* Multi-sample or multi-judge, then aggregate.
6. **Bias tests.** Swap answer order → position bias; change rubric order → anchoring. **If a bias appears (>10–20% ordering effect), apply mitigations** (randomize prompts, ensemble).
7. **Calibrate + monitor.** Establish the **fixed gold dataset**; retest after any model/prompt change. Keep a human baseline; re-label a sample for drift; track score distributions + judge versions over time.
8. **Handle contested items.** Flag low-consensus items (**>1-point spread**); adjudicate or score separately; ensure aggregates don't unfairly penalize divergent-but-reasonable answers. *(Aligns with our evidence-confidence axis.)*
9. **Document thresholds.** Explicitly record acceptance criteria (e.g. **"human–judge Spearman ≥ 0.8" or "κ ≥ 0.7"**) and cite precedents (Prometheus, EvalMORAAL, MANTA, Patronus) — transparency is part of validation.
10. **Iterate.** Re-run all of the above every time the judge or the models-under-test change; keep humans in the loop for calibration + hard cases.

**Bottom line for our gate:** the existing `judge/validate.py` Spearman-ρ report is necessary but not sufficient. To meet this protocol it should (a) report a **chance-adjusted κ** alongside ρ, (b) be backed by **≥3 blinded domain experts** labeling **≈50–100 transcripts** (not a single labeler), (c) declare **ρ ≥ 0.8 strong / ≥ 0.6 minimum thresholds in advance**, (d) carry a **swap/order bias test** and **multi-sample variance check**, and (e) treat **contested decisions separately** rather than forcing a gold label. Use a **non-Claude grader** (we already fix the grader role) to blunt self-preference bias.
