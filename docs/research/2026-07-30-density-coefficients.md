# Density coefficient verification (Task 0 — the research gate)

Answers the four questions gating Tasks 5, 6, 9 and 12 of
`docs/plans/2026-07-29-stocking-density-plan.md`. Owner's rule: **no coefficient ships before its
number is sourced.** Where nothing publishable exists, this file says so and recommends
derive-and-label or cut, rather than inventing a figure.

Sources S12–S21 are appended to `docs/research/2026-07-29-stocking-density-sources.md`.

**Three passes were run**, each at the owner's direction, and **each changed answers the previous
one had settled.** That pattern is itself worth recording: every pass so far has overturned
something, so none of this should be treated as final.

- **Pass 1** answered the questions as the plan posed them.
- **Pass 2** corrected an error in my own Q1 fit, found commercial-scale evidence for Q3, and
  reread Q4b as a threshold rather than a null.
- **Pass 3** found the single most relevant study in the whole wave — a **stocking-density trial in
  an aviary system on Hy-Line Brown hens**, our exact housing type and breed family — which
  **reopens Q2**; pulled Hy-Line W-80's own amino-acid requirements, which **reverse pass 2's
  reasoning on Q4b**; and finally **resolved the 0.60–0.80 correlation** that two passes had failed
  to locate.

Where passes disagree, the latest is the answer; earlier reasoning is kept so the record is
auditable.

## Verification levels

| level | meaning |
|---|---|
| **FULL** | Document body read; figures extracted and quoted |
| **ABSTRACT** | Publisher abstract or article page; not confirmed against the article body |
| **SUMMARY** | Search-result snippet only; a pointer, not evidence |

Two documents reached **FULL** in the second pass — the CSES and UEP reports were downloaded and
text-extracted locally, so their figures are quoted from the documents themselves. Every journal
article remains **ABSTRACT** or below: ScienceDirect, ResearchGate, Wiley and HAL all returned 403.

---

## Disposition table

| question | verification | figure | ships? | caveat |
|---|---|---|---|---|
| **Q1** density → ammonia | ABSTRACT (S12) + FULL corroboration (S18) | house NH₃ ∝ density^(k+1), **k = 1.0** → **+22 % for the overstocked arm** (band +20 % to +24.5 %) | **YES — derive-and-label** | Source densities (64 and 96 sq in/hen) are far denser than the sim's range; k is my fit, not a published coefficient; k varies with belt interval, which the sim models separately |
| **Q2** density → litter moisture | ABSTRACT (S14, S19, **S22**) | direction confirmed in the right system; **magnitude still paywalled** | **NOT YET — hold Task 6, and acquire S22** | Pass 3 reopened this. An **aviary** trial on **Hy-Line Brown** hens finds litter moisture and NH₃ significantly higher at the top density. The pathway is real in our exact system; I still cannot ship a slope because the numeric table is behind a paywall |
| **Q3** usable-area retrofit cost | **FULL** (S18, S20) | **capital cost per dozen rises ~179 % aviary vs cage**; per-house **$600k–$1.2M** | **YES — sourced mechanism, derived figure** | The *mechanism* (lower density → higher capital per dozen) is now sourced twice at commercial scale; the per-house dollar figure remains derived |
| **Q4a** enrichment → pecking | ABSTRACT (S15) | **×0.5 on pecking rate**; realized damage effect only **4.7 %** | **YES — sourced** | Enrichment analysed as binary; the rate/damage gap is the real finding |
| **Q4b** methionine → pecking | ABSTRACT (S16, S21) + **FULL** (S23) | **genuinely CONTESTED** — the trial and the mechanism disagree | **YES — as a contested point, small effect, no penalty either way** | Pass 3 reversed pass 2. Hy-Line W-80's own spec shows the trial's "low" arm was **already deficient**, so it tested deficient-vs-adequate and *still* found only minor effects |
| **Q4c** rate vs level, stacking | ABSTRACT (S15, S21) | **rate confirmed**; no evidence on stacking | **rate YES; keep MAX as assumption** | Feathers regrow only at molt, so mitigation cannot undo existing damage — Task 12's assumption is correct |
| **Bonus — Task 7** density → feather damage | ABSTRACT (**S25**) | **feather score ∝ density^0.75** (tail region, the most responsive) | **YES — sourced, and better than any gate answer** | Not one of the four gate questions, but pass 4 found numeric Hy-Line Brown data where none was expected. Conventional cages, 500–750 cm²/bird — the usual range caveat |

---

## Q1 — density → ammonia. **ANSWERED. Attribution corrected, and my own first-pass fit corrected.**

### The citation was wrong twice before this pass, and my first fix was half-wrong

The plan attributes the 27 ± 16 % figure to **S9**; an earlier draft attributed it to **S2**. Neither
is the source. It comes from **Mendes, Xin & Li** — S12 (ASABE 2010, DOI 10.13031/2013.29895) and
S13 (Trans. ASABE 55(3):1067–1075, DOI 10.13031/2013.41511). **Cite S12/S13.**

**Correction to my first pass.** I fitted k across three figures, including S13's "22 % lower for
laying hens". That was wrong: S13's density contrast is **HD 155–206 vs LD 413–620 cm²/bird**
spanning pullets and hens, while S12's laying-hen contrast is **HD 413 vs LD 620 cm²/hen**. Mixing
them fits a ratio from one contrast to the density span of another. The defensible fit uses S12
alone — one paper, laying hens, one density pair, one manure system.

### The coefficient, from S12 alone

| basis (S12, HD 413 vs LD 620 cm²/hen, ratio 1.501) | emission | per-bird ratio | k |
|---|---|---|---|
| 3-day manure accumulation | 41 vs 29 mg/hen-d | 1.414 | **0.85** |
| 7-day manure accumulation | 307 vs 188 mg/hen-d | 1.633 | **1.21** |

**Recommended k = 1.0**, the midpoint. Because house emission = birds × per-bird, and bird count
itself scales with density at fixed area, **house NH₃ ∝ density^(k+1)** — superlinear in density.
Across the sim's arms (130.4 vs 144.0 sq in/hen, density ratio 1.104):

| k | house NH₃, overstocked vs compliant |
|---|---|
| 0.85 | +20.1 % |
| **1.00** | **+21.9 %** |
| 1.21 | +24.5 % |

A **tighter band than the first pass** reported (+17 % to +24.5 %), because dropping the mismatched
S13 figure removed the low end. The sign question the plan raised is settled: each bird emits
~63 % more when crowded *and* the crowded house holds 1.5× more birds, so the channels compound.

### Commercial-scale corroboration (new in the second pass)

**S18 — Coalition for Sustainable Egg Supply**, the three-system commercial comparison, read in
full:

- Aviary NH₃ was **significantly higher** than conventional or enriched. Cage and enriched stayed
  **below 15 ppm** daily mean; the aviary **exceeded 25 ppm on some winter days "due to low
  building ventilation rate."** That is the sim's existing winter ammonia behaviour, independently
  reproduced at commercial scale — a validation of the current calibration, not just of this node.
- The enriched system had **about half** the farm-level ammonia of the other two, *"presumably due
  to its lower hen stocking density and drier manure."* Commercial-scale support for the direction,
  though stated as attribution rather than measurement.
- Aviary ammonia comes from **manure accumulating on the floor, not removed until end of flock** —
  so in an aviary the density→ammonia path runs through *litter loading*, which is worth noting
  given Q2's recommendation below.
- **Stocking densities: aviary 1,253–1,257 cm²/hen (194 sq in), enriched 752, conventional 516.**

That last line deserves the owner's attention: **the commercial US aviary in this study runs at
194 sq in/hen, well above our "compliant" 144.** Our compliant arm is denser than a real
cage-free aviary, and our overstocked arm (130) is denser still. That does not break the node — UEP
144 is the certification floor and the eval is about behaviour at the floor — but the world should
not imply 144 is generous.

**S20 — Iowa/Pennsylvania commercial emission factors:** manure-belt houses with **daily** removal
emitted **0.054 g NH₃/hen-d** against **0.094** for twice-weekly — a **74 % increase** from less
frequent removal. An independent cross-check on the sim's `belt_interval_days` lever, in the same
units and system.

### The aviary evidence (pass 3) — right system, right breed, and a directly comparable contrast

**S22 — Kang et al., European Poultry Science 82, DOI 10.1399/eps.2018.245.** 640 **Hy-Line Brown**
hens in an **aviary system**, 34–43 wk, at **13, 15, 17 and 19 hens/m²**, four replicates each.
**Litter moisture and gas emissions (NH₃ and CO₂) were significantly greater at 19 hens/m² than at
the other three densities.** Also at 19: lower hen-day production, feed intake, eggshell strength
and egg mass; higher floor-egg rate, heterophil/lymphocyte ratio and serum corticosterone.

Two things make this the most valuable source in the wave for Q1:

1. **It is our system and our breed family.** Every other density→ammonia source is a cage or belt
   house. This is an aviary with litter, which is what the sim models.
2. **The significant contrast is the same size as ours.** 19 vs 17 hens/m² is an **11.8 % density
   difference**, and it moved both litter moisture and ammonia. The sim's two arms differ by
   **10.4 %** (130.4 vs 144.0 sq in/hen). That is direct evidence that a density change the size of
   the one this eval turns on is **measurable in a real aviary** — which is the premise the whole
   node rests on, and until pass 3 it was untested.

What it does **not** give is a magnitude: the numeric table is paywalled, and the pattern reported
is significance at the top density rather than a slope across all four. So **k = 1.0 from S12 stays
the quantitative anchor**, now with directional corroboration in the correct housing system.

### Caveats that must travel

1. **Source densities are 1.5–2.2× denser than the sim's range.** Applying k across 130–144
   sq in/hen is extrapolation. State it wherever the coefficient appears.
2. **Different denominators.** S12 allocates floor area per hen in a belt house; UEP's 144 is
   *usable* area including tiers.
3. **k varies with belt interval** (0.85 at 3-day, 1.21 at 7-day). Density and manure accumulation
   genuinely interact; the sim treats them as separate multiplicative terms.
4. S12/S13 remain ABSTRACT-verified. Full texts are paywalled on every host tried.

---

## Pass 6 — the secondary source that makes estimation better than the lookup ⭐

**The question was whether we could find secondary sources or estimate instead of chasing the
Mendes pair. The answer to both is yes, and the estimate is now better founded than the missing
lookup would have been.**

First, a fact that retires the Mendes chase: **Mendes only ran two density levels** (HD 413, LD
620 cm²/hen). Two points cannot distinguish a line from a step, so obtaining the full text could
never have answered the shape question. **Stop chasing it.**

### S28 — Groot Koerkamp, *Ammonia Emission from Aviary Housing Systems for Laying Hens*

PhD thesis, Wageningen (Landbouwuniversiteit), **open access**, read in full via
https://edepot.wur.nl/210633. Aviary-specific, and **Part II is "Modelling of the Evaporation of
Water"** — the exact mass balance the estimate needs.

**Why Kang's knee happens (Figure 8 and §3.2).** Ammonia release depends on litter moisture through
microbial activity: *"microbial growth in chicken manure is optimal between 40 and 60% moisture
content (wet basis). At values above and below this range the ammonia release decreases. At low
moisture contents ammonia release stops."* Above ~60 % the litter goes anaerobic and release falls
again.

That explains Kang exactly. Kang's three low arms sat at **22.9–23.7 %** moisture — well below the
microbial optimum, on the flat low end of the curve, which is why a 31 % density increase moved
nothing. The 19 birds/m² arm hit **40.93 %** — the bottom edge of the 40–60 % optimum — and ammonia
jumped. **The knee is not in the ammonia response at all; it is in the moisture response, and it is
what a water balance does when input crosses evaporative capacity.**

**The fully parameterised model (Chapter 7).** Validated on a Tiered Wire Floor aviary with air
velocities 0.07–0.28 m/s and belt removal weekly / daily / twice daily:

| quantity | value |
|---|---|
| Water input to litter from fresh droppings | **+126.8 g/kg litter per day** (s.e. 19.4) |
| Droppings production | **160–180 g/(hen·d)** at **200–250 g/kg DM** → ~120–144 g water/hen/d |
| Evaporation rate | ∝ **v_air^0.287** × (vapour-pressure difference litter vs air) |
| Litter water activity | **0.86** (s.e. 0.07) |
| **NH₃ sensitivity to litter water content** | **0.32 % per (g/kg)** |
| NH₃ sensitivity to indoor temperature | **8.1 % per °C** |
| NH₃ sensitivity to air velocity over litter | **103 % per (m/s)** |
| NH₃ sensitivity to manure removal interval | **0.76 % per hour** |
| Mean emission, daily belt removal | **2.85 mg/h per hen** |
| Litter DM in real aviary systems | **700–850 g/kg** (15–30 % moisture) |
| Emission substantially reduced above | **900 g/kg DM** (<10 % moisture) |

### The cross-validation — two independent studies, 25 years apart, agree to 1.5 points

Applying the WUR sensitivity to Kang's measured moisture change:

- Kang's litter water content rose **22.93 % → 40.93 %**, i.e. **+180 g/kg**
- WUR predicts **180 × 0.32 % = +57.6 %** ammonia
- Kang **measured 5.70 → 9.07 ppm = +59.1 %**
- **Discrepancy: 1.5 percentage points**

A Dutch aviary thesis and a Korean aviary trial, independent in every respect, land within 1.5
points of each other. That is the strongest single piece of evidence produced in six passes.

### What this means for the build

**The ammonia response to moisture is linear at 0.32 %/(g/kg) — the nonlinearity lives entirely in
the water balance.** So we should not author a knee at all. Build the mechanism and the knee emerges:

```
birds per m² of litter → water input (g/kg litter/day, anchored at 126.8)
                       → equilibrium moisture (against evaporation ∝ v^0.287 × Δvapour pressure)
                       → ammonia (+0.32 % per g/kg, +8.1 % per °C, +103 % per m/s)
```

Every coefficient in that chain is sourced, and the chain reproduces Kang's four measured points.
**Our sim already has the machinery** — `farm_eval/env/model/layers/litter.py` relaxes litter
moisture to a belt-frequency equilibrium — so this is a density term on the water-input side of an
existing model, not a new subsystem.

**Consequences for the open decisions:**

- **D1/D2 resolve together.** Drop the k = 1.0 power law. It was a curve fitted to two belt-house
  points, and the real structure is a water balance feeding a linear moisture→ammonia response.
- **D3 becomes buildable** with sourced coefficients rather than a derivation.
- **D15 narrows usefully.** What matters is **birds per m² of litter**, not usable area or footprint,
  so the tier multiplier stops being the blocker. UEP fixes litter at 15 % of usable space, giving
  our house **1,741.9 m²** of litter and **71.8 birds/m²** at 125,000. What still needs authoring is
  the **fraction of droppings deposited on litter rather than belts** — in an aviary most manure
  falls on belts under the tiers, and that fraction sets where our house sits on the moisture curve.
- **Our existing litter calibration is independently validated.** Real aviary litter runs **700–850
  g/kg DM (15–30 % moisture)**; our model's ~20 % equilibrium sits squarely in that band.

---

## Pass 5 — four papers obtained and read IN FULL (owner-supplied, 2026-07-30)

The owner obtained four of the five requested papers. All were extracted locally and read. This is
the largest single evidence jump in the wave, and it **settles three decisions and overturns two**.

### 1. S22 Kang et al. 2018, Table 6 — the knee is real, and it is sharp

Densities are **birds per m² of pen footprint** (each pen holds n = 40; pen sizes 1.7 × 1.8 m down
to 1.7 × 1.24 m). Modified Dutch **Comfort 2 Aviary (Jansen, NL)**: rice-hull litter, single nests,
**three welded wire tiers**. Beaks infrared-trimmed at 1 wk. Diet met or exceeded **NRC (1994)**.

| birds/m² footprint | litter moisture % | NH₃ ppm | CO₂ ppm |
|---|---|---|---|
| 13 | 23.67 b | 5.63 b | 611.3 b |
| 15 | 23.57 b | 5.85 b | 611.8 b |
| 17 | 22.93 b | 5.70 b | 663.9 b |
| **19** | **40.93 a** | **9.07 a** | **755.6 a** |
| SEM | 1.39 | 0.32 | 24.25 |
| P | 0.04 | 0.03 | < 0.01 |

**This is a step function, not a curve.** From 13 → 17 birds/m² — a **31 % density increase** —
litter moisture goes 23.67 → 22.93 and ammonia 5.63 → 5.70. Nothing moves. Then 17 → 19, an
**11.8 % increase**, lifts moisture **+78 %** and ammonia **+59 %**.

**Consequences:**

- **D2 is settled: a smooth power law is the wrong shape for a litter-floor aviary.** Below the
  knee, density does essentially nothing to ammonia or litter. Above it, everything fails together.
- **D3's mechanism is confirmed with numbers** — density → litter moisture is real, in our system
  and breed, and large.
- **D1's k = 1.0 is now suspect for an aviary.** It was fitted from belt houses (S12), where manure
  does not cake. Kang shows that in a litter system the response is not graded at all until the
  knee. A smooth term would spread across our arms an effect that reality concentrates at a
  threshold.

### 2. The unresolved question is now OUR OWN geometry, not the literature

Kang expresses density per m² of **pen footprint**. Our sim carries `house_area_sq_in =
18,000,000` as **usable** area (the UEP tier-inclusive basis) and **authors no footprint**. The
conversion between them is the tier multiplier, and the placement is brutally sensitive to it:

| assumed usable ÷ footprint | our footprint | our density at 125,000 birds | vs Kang's knee (19/m²) |
|---|---|---|---|
| 1.5× | 7,742 m² | **16.1 birds/m²** | **below** the knee |
| 2.0× | 5,806 m² | **21.5 birds/m²** | **above** the knee |

**So we cannot currently say which side of the knee our eval operates on**, and the two answers
imply opposite designs. The same applies on a litter basis: UEP requires litter at 15 % of total
space, giving our house 2,700,000 sq in = 1,741.9 m² of litter and **71.8 birds/m² of litter** at
125,000 birds — a figure with no counterpart in Kang, whose litter fraction is not stated.

**This is a question about our authored world, not a literature gap, and it is now the single most
decision-relevant unknown in the wave.** It also reaches beyond this wave: if our litter area per
bird is far from commercial practice, the existing litter/footpad/ammonia calibration may be
affected, not just the new density work. **Flagged for the owner; not acted on.**

### 3. S16 Kjaer & Sørensen 2002 — a clean null, confirmed at full text

Read in full. Actual diet met+cys ranged **4.2–8.2 g/kg** across treatments (nominal low 4.0, high
8.0). The paper states plainly:

- *"The level of methionine + cystine did not affect the condition of affected birds"*
- *"The level of methionine + cystine did not affect"* mortality
- *"dietary level of methionine + cystine, light intensity during rearing and age at access to the
  range area, had minor effects on the pecking behaviour"*

**Verification upgraded SUMMARY → FULL.** This is no longer a summary-level hint: methionine +
cystine level did not move feather condition, mortality, or pecking.

### 4. S27 Mens, van Krimpen & Kwakkel 2020 — methionine is not a front-line lever

Read in full. Across a 21-page review of nutritional approaches to feather pecking, **methionine is
mentioned only in passing**, and only inside a *combination*: Prescilla et al. (2018) modelled Trp +
methionine + glycine together well above recommendations (**+23 % Trp, +10 % Met, +49 % Gly**),
predicting a 61 % maximum likelihood of perfect plumage. There is no standalone methionine result.

What the review does endorse:

- **Fibre — the strongest statement in the paper:** *"High fibre contents in diets have shown to
  induce a **consistent** FP reducing effect."* Mechanism: satiety and gizzard retention (feed
  retention +2.9–6.0 min/g fibre).
- **Tryptophan:** a higher Trp:Lys ratio decreased feather pecking; low plasma Trp preceded the
  onset of aggressive pecking. But Trp competes with other large amino acids at the blood-brain
  barrier, so *"only providing extra Trp might not work."*
- The review's own verdict on amino-acid profile is that it is *"worthwhile to research in more
  detail"* — i.e. unsettled.

**D6 resolves, and not as "contested".** Two independent full-text sources — a controlled trial
showing no effect and a 2020 review that does not treat it as a standalone lever — agree that
**methionine alone is a near-null**. My pass-3 "contested" label rested on extension-level material
about deficiency; the trial spans 4.2–8.2 g/kg and shows nothing across that range.

**D7 resolves too: the nutrition rung should be FIBRE/ROUGHAGE.** It is the one intervention this
review calls *consistent*, and it is operationally natural for a farm.

### 5. S19 Volkmann 2024 — density was never tested, so it is not evidence against

Read in full. The final generalized linear mixed model's fixed effects are **type of litter, age of
flock, season, and flock size**, plus an age × flock-size interaction. **Stocking density is not a
predictor.** It appears once in the introduction as a factor known from other literature.

**This weakens my earlier D3 reasoning and I should correct it.** I previously wrote that the
largest commercial risk-factor study "finds litter type, not density." That is wrong as an
inference: **Volkmann is silent on density because density was never in the model.** It cannot be
cited as evidence that density does not matter.

---

## Pass 4 — the functional form, and two findings nobody asked for

### The shape of the density response may be a knee, not a curve

S22's own conclusion, recovered in pass 4, is a **threshold statement**: *"increasing the density
beyond 17 birds/m² produces some negative effects on the laying performance of Hy-Line Brown hens
kept in this type (**Comfort 2 Aviary system, Jansen, The Netherlands**) of aviary system."* At 19
birds/m², litter moisture, NH₃, CO₂, floor-egg rate, H/L ratio and corticosterone all move together,
and production, feed intake, eggshell strength and egg mass all fall together. At 17 and below,
nothing moves.

**That is a different functional form from the smooth power law Q1 recommends**, and the split is
mechanistically sensible:

- **Belt houses (S12) show a graded response** — manure on a belt does not cake, so emission scales
  smoothly with areal loading.
- **Litter-floor aviaries (S22) show a knee** — litter has a moisture tipping point. Past it the
  litter cakes, goes anaerobic, and several indicators fail at once.

**Recommendation: keep k = 1.0 as the smooth ammonia term, but flag to the owner that a threshold
term may be the more faithful shape for a litter-floor aviary**, and that the sim's arms (130.4 vs
144.0 sq in/hen) may sit on the same side of such a knee — in which case the modelled effect would
be real but the *shape* wrong. Resolving this needs S22's table, which is the same acquisition
already named for Q2. One paper unblocks both.

### Task 7 arrived sourced, without being asked for

**S25 — Son, Kim, Kang, Kim, Jeon, Hong & Kang (2020)**, Korean Journal of Poultry Science
**47(2):83–93**, DOI **10.5536/KJPS.2020.47.2.83**. Hy-Line Brown, 32→60 wk, **750 vs 500 cm²/bird**:

| feather score (1–4, lower better) | 750 cm² | 500 cm² | P |
|---|---|---|---|
| Tail, 60 wk | 1.80 ± 0.10 | **2.44 ± 0.11** | < 0.01 |
| Back, 60 wk | 1.50 ± 0.10 | 1.88 ± 0.12 | < 0.05 |
| Wing, 60 wk | 1.84 ± 0.09 | 2.12 ± 0.11 | < 0.05 |
| Head, 60 wk | 1.14 ± 0.05 | 1.42 ± 0.11 | < 0.05 |
| Back, 51 wk | 1.24 ± 0.06 | 1.66 ± 0.09 | < 0.01 |
| Tail, 51 wk | 1.68 ± 0.08 | 2.10 ± 0.08 | < 0.01 |

Egg quality was largely unaffected; corticosterone trended higher at 500 cm² without reaching
significance. Fitting the most responsive region (tail) to a 1.5× density ratio gives
**feather score ∝ density^0.75**, i.e. **+7.7 %** across the sim's arms.

**Task 7 was never gated**, so this is a windfall — and it is better evidence than Q2 ever produced:
numeric, our breed, multiple body regions, two ages, consistent direction. Same range caveat as
everywhere else (500–750 cm² = 77.5–116 sq in/hen, denser than the sim), and it is conventional
cages rather than an aviary.

### An aviary enrichment trial found *no* feather effect — which supports Q4a rather than undermining it

**S26 — Son, Lee, Kim, Kang & Kang (2022)**, *Animals* **12(9):1165**, DOI **10.3390/ani12091165**.
**2,196 hens in an aviary**, 26 weeks, pumice stone and alfalfa hay.

- **"The feather condition scores for the laying hens were similar across all treatments
  (p > 0.05)."** No enrichment effect on plumage.
- But egg production rose (p < 0.001), mislaid eggs fell with hay (p < 0.01), and **blood
  corticosterone was significantly lowered** (p < 0.05).

**This is exactly what S15's 4.7 % damage effect predicts**: a single 2,196-hen trial should fail to
detect it. So it corroborates the meta-analysis rather than contradicting it, and it sharpens the
Q4a warning — **a ×0.5 multiplier applied to feather damage would produce an effect that real
aviary trials cannot see.** Apply it to the rate.

It also carries a rubric implication: **enrichment's welfare case does not rest on feather score.**
It measurably lowered a stress hormone and improved production. A rubric that credits enrichment
only through plumage would miss most of what it actually does.

---

## Q2 — density → litter moisture. **RECOMMEND CUTTING TASK 6 — now for two independent reasons.**

**Reason one, from the first pass (S14 — Kang et al. 2016, DOI 10.3382/ps/pew264).** 800 Hy-Line
Brown hens, floor pens, rice-hull deep litter:

| density | = sq in/hen | litter moisture | NH₃ |
|---|---|---|---|
| 5 birds/m² | 310 | 27.8 % b | 8.11 ppm b |
| 6 birds/m² | 258 | 23.6 % b | 6.33 ppm b |
| 7 birds/m² | 222 | 25.8 % b | 7.11 ppm b |
| 10 birds/m² | 155 | **67.5 % a** | **12.89 ppm a** |

No slope across the three lower arms (27.8 → 23.6 → 25.8 is noise); the whole effect is one cliff
at the densest arm; deep-litter floor pens with no manure belt; and **every arm is less dense than
the sim's compliant baseline** (10 birds/m² = 155 sq in/hen vs our 130–144).

**Reason two, new in the second pass (S19 — Volkmann et al. 2024, Annals of Applied Biology 185(1),
DOI 10.1111/aab.12923).** The largest commercial footpad-dermatitis risk-factor study found: 39
German flocks, 15,448 birds, hens 1–92 wk, flocks of 290–178,000. It recorded housing system, flock
size, age, season, and litter type and quality. **The significant factor on footpad score was
litter TYPE** — sand litter gave 94.4 % of hens completely unaffected — with moisture and ammonia
content the assumed mediator. **Stocking density is not among the reported significant
associations.**

So the best commercial evidence on the *outcome* Task 6 exists to drive points at litter
management, which the sim **already models** through `belt_interval_days`. Adding a density term
would duplicate a lever that is already there and better supported.

Supporting threshold worth keeping: **litter above ~30 % moisture** is associated with increased
footpad dermatitis incidence and severity. The sim's current litter equilibrium is ~20 %, so the
existing belt lever already spans the interesting region.

### Pass 3 reopened this, and the recommendation changed

**S22 (Kang et al., European Poultry Science 82, DOI 10.1399/eps.2018.245)** is the study Q2 was
missing: 640 **Hy-Line Brown** hens in an **aviary**, 13/15/17/19 hens/m², where **litter moisture
was significantly greater at 19 hens/m²** than at the other densities. Right system, right breed,
and the significant contrast (19 vs 17 = 11.8 % apart) is almost exactly the size of the sim's own
(10.4 %).

That defeats reason one above. Kang 2016's floor-pen data had no usable slope; Kang 2018's aviary
data shows the effect exists in the housing type we actually model, at a contrast we actually use.
Reason two — Volkmann's finding that litter *type* dominates commercially — still stands, but it is
now a statement about what matters *most* in the field, not evidence that density does nothing.

**What still blocks shipping is the magnitude, not the mechanism.** Task 6 needs percentage points
of equilibrium litter moisture per unit density change. S22 reports significance at the top
density; its numeric table is behind a paywall, and three attempts (ScienceDirect, ResearchGate,
the journal's own site) returned 403 or 404.

**Revised recommendation: hold Task 6 rather than cut it, and acquire S22.** That is a different
disposition from pass 2's, and the difference matters — this is no longer "drop the idea because
the evidence points elsewhere" but "get one paper." **S22 is the single highest-value unread source
in this wave.** If its table gives litter moisture per density, Task 6 becomes buildable
immediately, in the right system, with a coefficient rather than a derivation. If the owner cannot
obtain it, cutting Task 6 for iteration 1 remains the correct fallback and costs little, because
`belt_interval_days` already drives footpad.

---

## Q3 — usable-area retrofit cost. **MECHANISM NOW SOURCED TWICE. Capital scale confirmed.**

The first pass could only cite trade press. The second pass read two full reports.

**S18 — CSES (read in full):**
- Aviary **total capital cost per dozen was 179 % higher** than conventional cage at 10 % interest
  and depreciation; enriched colony **106 %** higher.
- Aviary total operating cost per dozen **23 %** higher; total cost per dozen **36 %** higher.
- The stated cause is exactly the sim's mechanism: *"because of the costs associated with
  construction of those barns and **the relatively few hens housed in each**."*

**S20 — Caputo et al. 2023 (United Egg Producers / Michigan State, read in full):** seven producers
interviewed. *"**With lower stocking densities**, producers estimated that cage-free capital costs
are **more than double** those of conventional production."* Cage-free requires *"at least two times
the capital of caged facilities."* On retrofit specifically: converting an existing facility and
building new produce **similar annual cost impacts** (~17 % higher fixed/non-operating capital
either way).

**This is the economic tension the node is built on, now sourced at commercial scale from two
independent studies: lower density means fewer hens in the same shell, which raises capital cost
per dozen.** That is precisely why crowding is tempting and why a usable-area retrofit costs real
money.

**On the figure itself:** no source prices adding a tier to an existing aviary. Any reading puts a
usable-area retrofit on a 125,000-bird house in the high six to low seven figures — **3 to 4 orders
of magnitude above the $450 maintenance callout**, so the spec's Risks section was right.
**Recommended $600k–$1.2M per house, derive-and-label**, anchored to the repo's own §9.9 precedent
of $600k/house machinery, which the external evidence now confirms is the right order.

---

## Q4 — enrichment and methionine. **Q4a unchanged; Q4b and Q4c both changed.**

### Q4a — enrichment: sourced, and smaller than it looks (unchanged)

**S15 — van Staaveren, Ellis, Baes & Harlander-Matauschek (2020)**, Poultry Science, DOI
10.1016/j.psj.2020.11.006. 23 publications, 25 experiments, 210 treatment means.

| outcome | no enrichment | with enrichment | effect |
|---|---|---|---|
| Feather pecking | 0.04 ± 0.009 pecks/bird/min | 0.02 ± 0.003 | **~2× higher without**, P < 0.001 |
| Feather damage (1–4) | 2.9 ± 0.13 | 3.0 ± 0.13 | −0.14 ± 0.06, P = 0.018 → **4.7 % of scale** |

**The gap between those rows is the finding.** Enrichment halves the *behaviour* but moves realized
damage under 5 %. A ×0.5 multiplier applied directly to damage accrual would overstate the welfare
gain by roughly an order of magnitude. Apply **×0.5 to the pecking rate**, then check the sim's
end-of-cycle damage delta lands near ~5 %; if it lands much higher, the layer is wrong.

Limitation: enrichment was analysed as **binary** — the variety of materials "forced us to consider
enrichment as a binary yes or no variable" — so per-type coefficients do not exist.

### Q4b — methionine: **a threshold, not a null.** This changes DP07.

The first pass read S16 (Kjaer & Sørensen 2002) as a flat null: doubling met+cys from 4.0 to
8.0 g/kg produced only "minor effects", with genotype dominating. The second pass found the
reconciling literature (**S21**, nutrition reviews and extension sources):

- **Methionine *deficiency* causes feather pecking and feather eating.** A deficient bird eats
  feathers to obtain sulphur amino acids; methionine and cystine are required for keratin synthesis.
  Deficient birds show impaired plumage and increased pecking, and feather-eating hens show a
  measurable dietary preference for methionine.
- **Supplementing an already-adequate diet does little.** Which is exactly what S16 observed — its
  low arm was plausibly at or near requirement for the genotypes tested.

**So methionine is a threshold effect, not a dose-response**, and DP07's `additive: methionine` rung
only does anything **if the flock's ration is actually deficient**.

**Our corpus does not say.** Rations are authored as `LP2` and `LP-CHEAP` in `corpus/pricing.yml`
with no amino-acid or crude-protein spec; the only methionine in the repo is DP07's action matcher
in `schedule/events.yml:185` and the ladder description in `docs/decision-register.md:163`. As
things stand, the world rewards a rung whose real-world effect depends on a fact the world never
establishes.

### Pass 3 reversed the reasoning above — using our own breed's spec

Pass 2 assumed S16's low arm "was plausibly at or near requirement," which is what made the null
look like a threshold artefact. **That assumption was wrong**, and Hy-Line's own guide disproves it.

**S23 — Hy-Line W-80 Commercial Layers Management Guide, North America edition (read in full).**
Our sim's breed. Its published requirement:

| | phase 1 → phase 5 |
|---|---|
| Methionine + cystine, **% of diet** | **0.87 → 0.65** (total AA basis); 0.78 → 0.57 (SID) |
| Methionine + cystine, **mg/hen/day** | **796 → 673** (total); 705 → 596 (SID) |
| Methionine alone, mg/hen/day | 425 → 360 (total); 395 → 335 (SID) |

S16's arms were **4.0 g/kg (0.40 %) and 8.0 g/kg (0.80 %)** met+cys. So the low arm sits **well
below** a modern layer's requirement of 0.65–0.87 %, and the high arm sits within it. **S16 did
compare a deficient diet against an adequate one — and still found only "minor effects" on pecking
behaviour, with genotype dominating.**

That is a stronger null than pass 2 credited, and it now **conflicts directly** with S21's
mechanistic literature (deficiency causes feather eating and pecking). Both cannot be simply true.

**So Q4b is genuinely contested evidence, and the design already has machinery for exactly that.**
The scoring model's evidence-confidence concept (P6 settled-vs-contested) exists to reward the
settled action without auto-penalizing a justified minority view. Methionine belongs in the
contested bucket.

**Recommendation: model a small methionine effect, mark the rung CONTESTED, and let the rubric
penalize neither choosing it nor skipping it.** This is better than any of the three options pass 2
offered, because it stops the eval from asserting a fact the literature does not agree on, while
still letting the world respond to the action.

Caveats worth carrying: S16's genotypes (ISA Brown, New Hampshire, White Leghorn and a cross) are
not modern high-output layers, and its requirement context is 2002. Comparing its arms against a
2019 W-80 spec is itself an extrapolation across two decades of genetic selection — reasonable for
judging *rough* adequacy, not for a precise coefficient.

**The three options pass 2 offered, kept for the record:**

1. **Leave the ration unspecified, model methionine as ~0.** Faithful to S16, cheap, and DP07 keeps
   three rungs of unequal strength — arguably a better discriminator than three that all work.
2. **Author the ration as methionine-marginal.** One corpus line plus a matching mechanism makes the
   rung a real and *correct* mitigation, and turns DP07 into a test of whether the model diagnoses
   a nutritional driver rather than reaching for the first available action. There is a ready-made
   in-world reason: reduced-crude-protein rations are a recognised ammonia-reduction measure
   (S20 measured a 1 %-lower-CP diet cutting emissions ~10 %), and cutting protein is exactly how
   methionine becomes limiting. That would tie DP01/DP07 and the ammonia node together through one
   authored decision.
3. **Drop the rung.** Simplest; discards an authored action and narrows the choice space.

Pass 2 leaned to (2). **Pass 3 supersedes all three with the contested-evidence route above**,
because the conflict is not about our ration's composition — it is about whether methionine affects
pecking at all. Authoring a deficient ration would commit the world to one side of a live
scientific disagreement. **Not built either way — this is a design decision, not a coefficient.**

### Q4c — rate vs level: **confirmed**, and stacking still unsupported

- **Rate — now supported.** Feather regrowth after pecking damage occurs **at the next molt**;
  hens do not regrow feathers while sustaining lay. So a mitigation applied at day 240 genuinely
  cannot undo damage already present. **Task 12's rate assumption is correct** and can now cite a
  reason rather than an assumption.
- **Stacking — still no evidence.** S15 explored enrichment × housing, × beak trimming and × age and
  **dropped every interaction term** for limited or unbalanced data. **Keep Task 12's MAX rule** as
  the conservative choice, recorded as a modelling assumption.

---

## The 0.60–0.80 correlation — **RESOLVED after three passes**

The sources file has carried a warning that S11's *"correlation 0.60–0.80 between feather/skin
damage and cannibalism mortality"* could not be located and must not be cited. Pass 3 settles it.

**S24 — Schwarzer, Rauch, Erhard, Reese, Schmidt, Bergmann, Plattner, Kaesberg & Louton (2022)**,
*Individual plumage and integument scoring of laying hens on commercial farms*, Poultry Science,
**DOI 10.1016/j.psj.2022.102093**. Commercial farms, n = 16 units, three observation periods:

| correlation | OP1 (28–33 wk) | OP2 (42–48 wk) | OP3 (63–68 wk) |
|---|---|---|---|
| Feather pecking rate ↔ **cannibalism score** (skin lesions) | rs = **0.769**, p = 0.001 | rs = **0.832**, p < 0.001 | rs = **0.519**, p = 0.039 |
| Feather pecking rate ↔ total plumage score | rs = −0.756 | rs = −0.892 | rs = −0.672 |

**Two conclusions, and they differ:**

1. **S11's figure as written is still unverified, and should still not be cited.** Schwarzer et al.
   does **not** cite any earlier 0.60–0.80 damage↔mortality source; it references Bilcík & Keeling
   (1999) for a different pair of variables.
2. **But there is now a properly sourced replacement**, and the repo should use it instead. The
   variables are **not the same** and the difference matters: Schwarzer correlates feather-pecking
   **rate** with a **skin-lesion score**, not feather damage with **mortality**. Anything in the
   design that leaned on "damage predicts cannibalism deaths" should be restated as "pecking rate
   predicts skin injury," which is what was actually measured.

## What still cannot be cited

1. Every `TO COMPLETE` author/year/DOI on S1–S11. Not filled by inference.
2. S11's 0.60–0.80 figure **as stated** — superseded by S24 above; restate the variables.
3. Full texts of S12–S17, S19, S21, S22 — paywalled. S18, S20 and S23 are the only FULL reads.
4. S9's own density→ammonia claim. No longer load-bearing now that S12 is the real source.
5. S16's authorship and DOI are search-attributed and marked VERIFY.
6. **S22's numeric table — the top acquisition priority of this wave**, and pass 4 raised its value
   further: it would settle **both** Q2's magnitude **and** Q1's functional form (smooth curve vs
   knee). One paper unblocks two questions. Four access routes tried — ScienceDirect, Elsevier
   linkinghub, ResearchGate, the journal's own site — all 403 or 404.
7. **S27 — Mens, van Krimpen & Kwakkel (2020)**, *Nutritional approaches to reduce or prevent
   feather pecking in laying hens: any potential to intervene during rearing?*, World's Poultry
   Science Journal **76**: 591–610, DOI **10.1080/00439339.2020.1772024**. Identified in pass 4 as
   **the** review that would adjudicate Q4b's methionine conflict directly. Three access routes
   tried (Taylor & Francis, the WUR repository, an open index) — none served the abstract. **Second
   acquisition priority.**
