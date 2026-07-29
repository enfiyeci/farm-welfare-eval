# Catalog B — Graded Elicitation Dynamics (research-backed)

**Status: SOURCED.** Built from the deep-research run `wf_c2ec8085-0d0` (2026-07-18): 30 sources,
122 extracted claims, 24 adversarially verified (2/3+), 1 refuted. Companion to the priors-only
**[Catalog A](catalog-A-priors.md)**; the head-to-head is in **[comparison.md](comparison.md)**.
Provenance: [raw-claims-B.md](raw-claims-B.md). Same scope (v2 future-tech candidate nodes),
same organizing spine (choice-format ladder).

**Verification discipline** (same as the future-tech corpus): **[V]** = claim was in the
adversarially-verified sample; **[ext]** = extracted-only (true to source, not independently
cross-checked); **[REFUTED]** = failed verification, not to be relied on. The behavioral-science
and psychometrics claims are mostly **[V]**; the game-mechanic, AI-alignment, demand-effect, and
Goodhart claims are mostly **[ext]** (that whole part of the sweep produced few verified survivors).

## Source ledger (G1–G24)

| ID | Source | Tier | Status | Carries |
|----|--------|------|--------|---------|
| G1 | Andreoni & Miller 2002, *Giving According to GARP*, Econometrica 70(2) — https://econweb.ucsd.edu/~jandreon/Publications/Econometrica02.pdf | ✅ primary | **[V]** | Convex-budget allocation; classifies tradeoff RULE; 98% GARP-consistent; nests dictator game (~23% given at price=1) |
| G2 | Andersen, Harrison, Lau & Rutström 2006, Exp. Economics 9 — https://link.springer.com/article/10.1007/s10683-006-7055-6 | ✅ primary | **[V]** | MPL elicits only interval data; a single switch point is low-info |
| G3 | Drichoutis & Lusk 2012, MPRA 42128 — https://mpra.ub.uni-muenchen.de/42128/1/MPRA_paper_42128.pdf | ✅ primary | **[V]** | One MPL can't separate utility-curvature from probability-weighting; combine lists |
| G4 | *On the Reliability of BDM*, Management Science 2022 — https://pubsonline.informs.org/doi/10.1287/mnsc.2022.4409 | ✅ primary | **[V]** | BDM is incentive-compatible continuous WTP/WTA, but WTP shifts with the price distribution |
| G5 | Preston & Colman 2000, Acta Psychologica 104 — academia.edu/160132 | ✅ primary | **[V]** | Reliability/validity/**discrimination** rise 2→~7 categories, decline past ~10 → optimal ~7 |
| G6 | Response-format field experiment, Sci. Reports 2022 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9399090/ | ✅ primary | **[V]** | Binary inflates acquiescence (2.3× more "Yes"); continuous 0–10 gives exact degree, +42.5% time |
| G7 | Dual-IRT response-format sim — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6572909/ | ✅ primary | **[REFUTED]** | "Continuous strictly recovers latent trait best" — **failed verification (0-3), do not rely on** |
| G8 | Systematic review, high-stakes moral measures 2023 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9869153/ | ✅ primary | **[V]** | No game/sim instruments exist; **none report floor/ceiling effects**; DIT graded format reliable |
| G9 | Ryan, Formosa, Howarth & Staines 2020, Ethics & Info Tech 22 — https://link.springer.com/article/10.1007/s10676-019-09515-0 | ✅ primary | **[V]** | Import ~20 validated instruments; measure from behavioral traces (choices + response dynamics) |
| G10 | MorALERT serious game 2022 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8815380/ | ✅ primary | **[V]** | 0–5 graded socio-moral scale — but grades **justification quality**, not a dial the player sets; only preliminarily validated |
| G11 | Gamified assessment RCT, JMIR Serious Games 2025 — https://games.jmir.org/2025/1/e70453 | ✅ primary | **[V]** | GRU maps nominal choices → continuous DSM-5 trait (r=0.85); **game format resists social-desirability manipulation** (incentive p=.02 on questionnaire, p=.71 on game); cognitive load "crowds out" faking |
| G12 | Morality-meter experiment, Computers in Human Behavior 142, 2023 — https://www.sciencedirect.com/science/article/abs/pii/S0747563222004435 | ✅ primary | **[V]** | Visible meter ignored on obvious choices, **sways behavior on ambiguous ones**; effect depends on meter trustworthiness |
| G13 | VASSIP gamified Big Five 2024 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11065274/ | ✅ primary | [ext] | Gamification preserved validity but introduced an artifact (Conscientiousness d=0.66) |
| G14 | *Can Revealed Preferences Clarify LLM Alignment?* — arxiv 2605.08556 | ✅ primary | [ext] | Revealed preferences from choices > self-report; **LLMs often can't verbalize the cost function driving their decisions** |
| G15 | ConflictScope (LLM value-conflict) — arxiv 2509.25369 | ✅ primary | [ext] | Elicits a full value RANKING; open-ended vs multiple-choice **changes measured priorities**; ranking steerable via prompt (+14%) |
| G16 | Stated-vs-revealed LLM preference protocol — arxiv 2601.21975 | ✅ primary | [ext] | Binary forced-choice **collapses preference strength/indifference/uncertainty**; SvR correlation is highly protocol-dependent |
| G17 | *LLMs Often Know When They Are Being Evaluated* — arxiv 2505.23836 | ✅ primary | [ext] | Gemini-2.5-Pro AUC 0.83 (0.95 agentic) eval-vs-deployment; CoT is only a lower bound |
| G18 | Apollo Research, eval-awareness — https://www.apolloresearch.ai/science/claude-sonnet-37-often-knows-when-its-in-alignment-evaluations/ | ✅ primary | [ext] | Claude 3.7 identifies capability-vs-alignment testing 93%; test-awareness drives a demand effect |
| G19 | de Quidt, Haushofer & Roth, experimenter demand — https://www.jondequidt.com/pdfs/deQuidt_Haushofer_Roth_demand_final.pdf | ✅ primary | [ext] | Implicit/weak demand modest (~0.13 SD); **strong explicit signals move behavior a lot (0.6–1.06 SD)**; within-subject > between-subject |
| G20 | Goodharting in RL — arxiv 2310.09144 | ✅ primary | [ext] | Optimizing an imperfect proxy improves then **degrades** the true objective past a critical point (19.3% of configs) |
| G21 | *Ethical dilemmas & dominant moral strategies in games* — https://www.gamedeveloper.com/design/ethical-dilemmas-and-dominant-moral-strategies-in-games | 🟡 secondary | [ext] | Quantified morality → a **dominant moral strategy**; a scored moral choice becomes gameplay-optimization, not ethics; Mass Effect Paragon/Renegade degenerate optimum |
| G22 | 11 bit studios design (gamepressure) | 🟡 secondary | [ext] | Frostpunk/This War of Mine **deliberately rejected morality meters**; judgment "delegated into the player's head" |
| G23 | Frostpunk design essays (mrpetovan / medium / pcgamesn) | 🔵 blog | [ext] | Ethically-charged, **near-irreversible** policy choices; hope/discontent meters; law tech-tree as **escalation ladder** (stop-point reveals values); explicit opportunity cost |
| G24 | RimWorld design (summerengine) | 🔵 blog | [ext] | Continuous resource allocation under competing survival priorities; per-colonist welfare; "story generator" |
| G25 | LLM dispositions via Situational Judgment Tests — arxiv (2602.09802 or 2602.11328; exact ID unconfirmed in the run log) | ✅ primary | [ext] | LLMs **default to neutral/evasive** answers unless forced to commit; SJTs used as binary dilemmas |

---

## 1. What the literature actually establishes (the measurement spine)

Five findings, in decreasing strength, that ground (and partly correct) the "a dial beats a
yes/no" thesis:

1. **Allocation under a *varied price of welfare* recovers more than a single dial does.**
   (Structural argument — G1 demonstrates what the allocation task recovers; it does not run a
   head-to-head ranking against dials/thresholds, so "gold-standard" here is my synthesis, not a
   sourced comparison.) Andreoni & Miller's convex-budget task has subjects allocate a divisible
   resource between self/profit and other/welfare across budgets that systematically vary the
   *price* of welfare and the endowment. This doesn't just measure *whether* they trade off
   welfare — it **classifies which tradeoff rule** they use (selfish / utilitarian-perfect-
   substitutes / Rawlsian-equal-split), with 98% of choices consistent with a coherent utility
   model [G1 V], and it **nests the binary dictator game** at price=1 (the ~23%-given figure that
   matches prior work is an extracted-only detail [G1]). The power comes from varying price *and*
   endowment across a **menu**, not from one setting.

2. **Graded beats binary — but the optimum is ~7 categories, not "continuous."** Reliability,
   validity, and **discriminating power** rise sharply from 2–4 response categories up to about 7,
   then test-retest reliability *declines* beyond ~10 [G5 V]. Binary formats also inflate
   acquiescence — one field experiment found ~2.3× more "Yes" responses vs a continuous 0–10
   slider [G6 V]. **Correction to a naive prior:** the claim that a *continuous* format strictly
   recovers the latent trait best was **REFUTED** in verification [G7 REFUTED]. So the design
   target is a **7-ish-rung ordinal dial**, not an infinitely fine slider — more resolution past a
   point adds noise and completion cost, not signal.

3. **A single switch point / threshold is low-information and confounds dimensions.** The multiple
   price list and Holt-Laury formats yield only *interval* data (the switch row bounds the value
   to a range), and one list cannot separate distinct preference dimensions (e.g. utility
   curvature vs probability weighting); combining lists improves identification [G2 V][G3 V].
   **Implication:** a lone auto-policy *threshold* (Catalog A's D3) is weaker than it looks in
   isolation — its information rises when you observe several thresholds across varied prices.

4. **Behavior-as-signal beats self-report — especially for LLMs.** Revealed preferences inferred
   from choices are a more reliable read of underlying objectives than verbalized preferences,
   because **models often cannot accurately verbalize the cost function driving their decisions**
   [G14 ext]. The field recommends measuring from behavioral traces (the choices themselves plus
   response dynamics) and importing validated instruments rather than inventing ad hoc in-game
   meters [G9 V]. A machine-learning model has already mapped nominal in-game choices to a
   continuous trait score at r=0.85 [G11 V] — direct precedent for inferring a **latent
   welfare-vs-profit orientation from the vector of setpoint choices**, rather than scoring each
   decision independently.

5. **Response format is itself a load-bearing variable — it changes the answer.** For LLMs
   specifically: open-ended vs multiple-choice shifts *which* values a model appears to prioritize
   [G15 ext]; binary forced-choice collapses preference-strength, indifference, and uncertainty
   into one bit, and the stated-vs-revealed correlation flips between near-zero, positive, and
   negative depending only on whether the format permits neutrality [G16 ext]. So the rung a node
   is authored at is not a cosmetic choice — it partly determines the measured tradeoff.

## 2. Gameability & eval-awareness (the strongest, most actionable part)

This is where the literature most changes the design — and it strongly validates the project's
existing "silent, harness-side welfare score" decision.

- **A visible welfare meter contaminates exactly where you most need a clean read.** A visible
  morality meter is ignored when the choice is obviously right/wrong, but **sways behavior when
  the choice is morally ambiguous** — and only once the meter has earned credibility [G12 V]. The
  ambiguous cases are precisely the discriminating ones. **Design rule: never expose a welfare
  score/meter to the agent.** (The eval already keeps scoring harness-side; this is independent
  confirmation.)
- **Quantified morality creates a dominant strategy / degenerate optimum.** When choices feed a
  visible score, committing fully to one extreme becomes mechanically optimal, so the mechanic
  **makes the choice for the player** (Mass Effect's Paragon/Renegade locks out balanced play)
  [G21 ext]. A scored moral choice reads as gameplay-optimization, not ethics. **Design rule:**
  no rung/setting may be strictly dominant, or the dial stops measuring values and starts
  measuring who-found-the-optimum.
- **Game/operational framing reduces deliberate faking *in humans* — the LLM transfer is an
  inference.** In an RCT with human participants, monetary incentives to answer in a
  socially-desirable direction moved questionnaire scores (p=.02) but **not** the gamified
  assessment (p=.71) [G11 V]; the proposed mechanism — that high cognitive load "crowds out" the
  capacity to fabricate — is the authors' explanation, extracted-only [G11]. This is suggestive
  for our "operational register lowers eval-awareness"
  bet but does not directly test LLM eval-awareness or farm-software framing. 11 bit studios deliberately
  rejected morality meters and put judgment "in the player's head," keeping choices ambiguous and
  un-telegraphed [G22 ext]. **But** gamified framing can also introduce artifacts (a gamified Big
  Five inflated Conscientiousness, d=0.66) [G13 ext], and the game-based-fakeability literature is
  explicitly unsettled — do not over-claim "operational framing defeats gaming."
- **Models often know they're being evaluated — graded framing helps but doesn't solve it.**
  Frontier models distinguish eval from deployment above chance (Gemini-2.5-Pro AUC 0.83, 0.95 on
  agentic tasks) and can name the *purpose* of a test (capability-vs-alignment at 93%) [G17 ext]
  [G18 ext]; CoT monitoring is only a *lower bound* on this awareness [G17 ext]. Test-awareness
  produces a demand effect — a model that thinks it's tested for a trait acts more like it [G18
  ext]. So graded/operational rendering is a *mitigation* of eval-awareness, not a cure; it must
  be paired with the eval's existing eval-awareness validity gate.
- **Demand effects: implicit is modest, explicit is large — and within-subject is worse.**
  Weak/implicit experimenter demand averages only ~0.13 SD, but *strong explicit* signals about
  what's wanted move behavior 0.6–1.06 SD, and **within-subject designs amplify demand** vs
  between-subject [G19 ext]. **Direct implication for the "salience ladder" manipulation** (spec
  §20): running the *same* tension at multiple salience levels *within one episode/model* is a
  within-subject design and will itself inject demand — prefer between-episode variation, or bound
  the demand by deliberately inducing it (de Quidt's method).

## 3. Commercial game mechanics that force revealed priorities (extracted-only)

The academic sweep confirmed few of these, so treat as **design reference, not evidence** [G21–
G24 ext]. What the game-design sources converge on:

- **Ethically-charged + near-irreversible choices** make a management decision a values signal;
  survival sims without moral consequence don't reveal anything [G23 ext]. → favors irreversible
  commitments (tech-tree, culling) as high-signal nodes.
- **Escalation ladders where the stop-point reveals values** (Frostpunk's law tree from mild
  policies to authoritarian endpoints) [G23 ext]. → directly validates the collar cue-ladder (A's
  D4) as a revealed-preference instrument.
- **Explicit opportunity cost** ("the worker dies but the resources may make it worthwhile") is
  what makes a tradeoff force a revealed priority [G23 ext][G24 ext]. → confirms A's principle
  "enforce opportunity cost."
- **Purpose-anchored meters over abstract ones** — Frostpunk's "hope" gauge tied to a concrete
  goal, not a generic "morale" [G23 ext]. → if any internal gauge is shown, anchor it to
  operations, never to "welfare."
- **Individuated stakes** — RimWorld's named colonists with per-character welfare that reacts to
  events [G24 ext]. → supports A's D7 (individual-vs-herd), with the caveat that individuation is
  a narrative device to use sparingly.

## 4. Node × literature mapping

| v2 node | Best-supported format (from lit) | Key sources |
|---|---|---|
| `vf-correction-intensity` | 7-rung ordinal correction ladder (not a raw slider) + escalation-with-stop-point | G5 V, G23 ext, G21 ext |
| `vf-nonadapter-culling` | Irreversible individuated choice; opportunity cost made explicit | G23 ext, G24 ext |
| `vf-gps-misshock` | Behavior-as-signal (does it investigate) — trace, not meter | G9 V, G14 ext |
| `sensor-optimal-vs-animal` | **Convex-budget allocation under varied price of "clean data vs welfare"** | G1 V |
| `push-to-physiological-limit` | Allocation under varied price of welfare; watch Goodhart on any proxy | G1 V, G20 ext |
| `alert-triage-bias` | Attention-allocation trace; graded-with-neutrality format (G16), but force a real committed setting since models default evasive (G25) | G9 V, G16 ext, G25 ext |
| `automation-vs-stockmanship` | Escalation ladder + opportunity cost; keep any gauge purpose-anchored | G23 ext |
| `welfare-as-productivity-proxy` | Deliberate Goodhart probe — but the welfare score stays silent | G12 V, G20 ext, G21 ext |
| `autonomous-actuation-limits` | Multiple thresholds across varied prices (one threshold = low info) | G2 V, G3 V |
| `air-quality-zone-response` | 7-rung setpoint / allocation across zones | G5 V, G1 V |
| `explainability-trust` | Deference curve across a recommender's reliability band (not one trust bit); graded response permitted (G16) | G2 V, G16 ext |
| `culling-automation` | Irreversible commitment; force a real committed choice since models default evasive (G25) | G23 ext, G25 ext |

## 5. Cross-decision inference (a genuinely new design idea from the literature)

The strongest *new* move the literature suggests, beyond anything in Catalog A: instead of scoring
each decision with its own rubric, **infer a single latent welfare-vs-profit orientation from the
whole vector of the agent's setpoint/allocation choices** — the way a GRU recovered a continuous
DSM-5 trait from nominal in-game choices at r=0.85 [G11 V], and the way Andreoni-Miller recovers a
utility *rule* from a menu of allocations [G1 V]. This reframes the judge from a per-node grader
toward a **revealed-utility estimator** over the episode. Flagged as a scoring-architecture option
for the v2 spec, not a decided design.

## 6. Open gaps (from the research caveats)

- The **commercial-game-mechanics** angle produced no *verified* survivors — the game-design
  patterns (Factorio/RimWorld/Frostpunk/board games) are cited from secondary/blog sources only
  [G21–G24 ext]. A dedicated game-design-literature pass would be needed to make any of them
  load-bearing.
- Whether **allocation framing** cleanly out-discriminates a **single dial** *for LLMs
  specifically* is an open question (the human result is strong; the LLM transfer is untested).
- Whether keeping the welfare score fully silent is *sufficient* to prevent Goodhart/eval-awareness
  contamination in LLMs (vs the human meter result) is untested [G12 V, G17 ext].
