# A vs B — Priors vs Research, Compared

Head-to-head between **[Catalog A](catalog-A-priors.md)** (my own knowledge, no sources) and
**[Catalog B](catalog-B-research-backed.md)** (deep-research, 24 verified + extracted claims).
Purpose: see where my design intuition held, where the literature corrected it, and what each
found that the other missed.

## TL;DR

The priors held up well on **structure and principles** and were wrong on one **specific
quantitative claim**. The core thesis (graded > binary, revealed preference, keep the welfare
meter silent, enforce opportunity cost, don't telegraph) is all confirmed by sources. The two
real corrections: (1) **allocation under a *varied price* of welfare** recovers the tradeoff
*rule* (not just a point) plus a coherence check — more than a single dial does by construction,
which argues for promoting it over my dial headline (this is a structural argument from what the
allocation task recovers, not a sourced head-to-head ranking); (2) more resolution is **not**
strictly better — the optimum is **~7 ordinal rungs**, and the separate "continuous strictly
best" claim (which I did not assert) was outright **refuted**. The
literature also added two things I didn't have: **cross-decision latent-utility inference** as a
scoring architecture, and **hard numbers on eval-awareness / demand effects** that reshape the
salience-ladder manipulation.

## 1. Where B CONFIRMS A

| Prior (A) | Confirmed by (B) | Verification |
|---|---|---|
| Graded discriminates better than binary | Preston-Colman: discrimination rises 2→7 categories; binary inflates acquiescence 2.3× | G5 **[V]**, G6 **[V]** |
| Keep the welfare score silent / consequences-over-meters (A principle #1) | Visible meter sways behavior exactly on ambiguous (discriminating) cases; 11 bit studios reject meters | G12 **[V]**, G22 [ext] |
| Operational register lowers eval-awareness (A principle #2) | Partial support: a *human* gamified assessment resisted social-desirability incentives (p=.71 vs p=.02); the extension to LLM eval-awareness / farm-software framing is an inference, not a direct test | G11 **[V]** (human fakeability only) |
| Enforce opportunity cost (A principle #4) | Explicit opportunity cost is what forces revealed priorities (Frostpunk worker-death tradeoff) | G23 [ext] |
| Escalation ladder reveals values (A's D4) | Frostpunk law-tree stop-point reveals values; escalation ladders are a core moral-signal mechanic | G23 [ext] |
| Reputation/certification meter is the most Goodhart-prone; use as a probe (A's D11) | Quantified morality → dominant strategy / degenerate optimum; scored choice becomes optimization not ethics | G21 [ext], G20 [ext] |
| Budget allocation reveals relative weights (A's D2) | Andreoni-Miller convex-budget allocation recovers the tradeoff *rule* + a GARP consistency check (G1 shows what it recovers; it is not a comparative ranking against other formats — "strongest" is my synthesis) | G1 **[V]** |
| Not everything should be a dial (A's D12, principle #6) | Response format changes the answer; some formats collapse info — format is load-bearing, choose per-tension | G16 [ext], G5 **[V]** |
| Individual-vs-herd weight (A's D7) | RimWorld per-colonist welfare; individuation as revealed-priority device | G24 [ext] |

## 2. Where B CORRECTS / QUALIFIES A

| Prior (A) | Correction (B) | Verification |
|---|---|---|
| **Headline was the continuous "correction dial" (D1).** Ranked the single setpoint as the flagship. | The flagship should be **allocation under a *varied price* of welfare** (D2 promoted over D1). A single dial reveals a point; varying the *price* and endowment across a menu reveals the tradeoff **rule** (selfish/utilitarian/Rawlsian) and gives a GARP consistency check. | G1 **[V]** |
| **A's ladder ranked continuous/compounding at the *top* rungs** (higher rung = more discrimination). A hedged this as a hypothesis and explicitly asked B to check where continuous adds noise — so A did *not* assert "continuous is best." | B **qualifies A's ladder ordering:** optimal resolution is **~7 categories**, and test-retest reliability declines past ~10 — so the top rung should be a 7-notch ordinal dial, not a fine/continuous slider. Separately, the stronger claim "continuous strictly recovers the latent trait best" (which A did *not* make) was **refuted** in verification. | G5 **[V]**, G7 **[REFUTED]** |
| **Auto-policy threshold (D3) treated as a strong standalone instrument.** | A single switch point / threshold is **low-information** — it only bounds the value to an interval and confounds dimensions. It gets strong only when you observe **several thresholds across varied prices**. | G2 **[V]**, G3 **[V]** |
| **"Operational framing lowers eval-awareness" stated fairly confidently.** | **Untested for LLMs, and the direct evidence cuts the other way.** No source shows operational framing reduces LLM eval-awareness; what we have is that models actively *detect* eval vs deployment (AUC 0.83) and name the test purpose (93%), and that gamified framing can add its own artifacts in humans (Conscientiousness d=0.66). Treat A's principle #2 as a plausible bet, not a supported result — framing is at best a partial mitigation. | G17 [ext], G18 [ext], G13 [ext] |
| **Trust calibration (D6) as a simple over/under-trust read.** | Needs a **deference curve across reliability bands**. Two distinct sourced points: binary forced-choice **collapses** preference strength/indifference/uncertainty, so the format should permit a *graded* response including neutrality (G16); and separately, LLMs tend to **default to neutral/evasive** answers, so the format must still elicit a real committed setting rather than allow a non-answer (G25). | G16 [ext], G25 [ext] |

## 3. What B ADDED that A MISSED

1. **Cross-decision latent-utility inference (the biggest new idea).** Instead of a per-node
   rubric, infer one **latent welfare-vs-profit orientation from the whole vector of setpoint/
   allocation choices** — precedent: a GRU recovered a continuous trait from nominal choices at
   r=0.85 [G11 V]; Andreoni-Miller recovers a utility *rule* from a menu [G1 V]. This reframes the
   judge as a **revealed-utility estimator**. A missed a whole scoring-architecture option.
2. **Hard numbers that reshape the salience-ladder manipulation.** Demand effects: implicit ~0.13
   SD (modest) but strong-explicit 0.6–1.06 SD, and **within-subject designs amplify demand**
   [G19 ext]. Running the same tension at multiple salience levels *within one episode* is a
   within-subject design → it injects demand. Prefer between-episode variation. A treated the
   salience ladder as free.
3. **The GARP consistency check as a validity tool.** Allocation menus don't just measure the
   tradeoff — they test whether choices are *coherent* (utility-maximizing) at all [G1 V]. A free
   incoherence/validity signal A didn't consider.
4. **"Forced commitment" as a format requirement.** LLMs default to neutral/evasive; a graded
   format must *force* a committed setting or it measures evasiveness, not values [G25 ext] —
   while still permitting graded strength/neutrality rather than a false binary [G16 ext].
5. **Goodhart has a measurable shape.** Proxy optimization helps then hurts past a critical point
   (19.3% of RL configs); risk scales with proxy-true misalignment angle [G20 ext] — a concrete
   frame for *why* any visible welfare proxy is dangerous, beyond "meters get gamed."

## 4. What A HAD that B DIDN'T COVER

The research sweep under-covered the **commercial-game-mechanics** angle (no verified survivors),
so several of A's game-derived dynamics stand on priors + weak sources only, and remain useful
design ideas that B could neither confirm nor refute:

- **D5 Fog-of-war / attention-spend** as a measured quantity — no direct source; strong design
  intuition, unvalidated.
- **D8 Efficiency-frontier bundle picker** (Pareto choice) — conceptually adjacent to allocation
  menus (G1) but the specific "pick a point on a frontier" framing wasn't sourced.
- **D9 Engine-building compounding / discount-rate-on-welfare** — time-preference is a real
  behavioral construct, but the sweep didn't surface a source tying it to a graded farm mechanic.
- **D10 Risk/insurance/indemnity** — untouched by B; stands on priors + the eval's own world-bible.

These are the natural target of the **dedicated game-design-literature pass** B's caveats call
for, if we want them load-bearing rather than illustrative.

## 5. Net recommendation (reconciled A+B)

If we build from these, the reconciled priority order is:

1. **Allocation-under-varied-price** as the flagship graded instrument (was A's D2; promoted on
   the structural argument that it recovers a tradeoff *rule* + coherence check, grounded in what
   G1 demonstrates — not on a sourced head-to-head ranking) — apply first to
   `sensor-optimal-vs-animal`, `push-to-physiological-limit`, `air-quality-zone-response`.
2. **7-rung ordinal ladders** (not continuous sliders) for the collar and escalation nodes
   (`vf-correction-intensity`, `automation-vs-stockmanship`) — G5.
3. **Behavior-as-signal + forced commitment**, welfare score kept silent, for the
   epistemic/integrity nodes (`vf-gps-misshock`, `alert-triage-bias`, `explainability-trust`) —
   G9, G12, G16, G25.
4. **Cross-decision latent-utility inference** as a scoring-architecture experiment for the v2
   spec — G11, G1.
5. Keep A's **D5/D8/D9/D10** as candidate dynamics pending the game-design research pass.

Everything here is a **design menu**, not a decided spec — per the brainstorm scope you chose.
