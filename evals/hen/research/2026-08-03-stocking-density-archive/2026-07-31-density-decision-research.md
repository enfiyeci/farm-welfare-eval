# Density wave — research pass on the three open owner decisions (2026-07-31)

Three targeted passes run to close **D15**, **D7** and **D11** from
`docs/plans/2026-07-30-density-wave-decision-register.md`. Each was a narrow, decidable question
rather than an open-ended coefficient hunt.

**Status: research complete, owner has NOT ruled.** Nothing here is a decision. The recommendations
are mine and are marked as such.

Verification levels used throughout: **FULL** (primary document read), **ABSTRACT** (abstract or
summary only), **SECONDARY** (someone else citing it).

---

## D15 — the litter area fraction and tier multiplier

**Question.** What fraction of UEP "usable area" is litter floor in a US commercial multi-tier
aviary, and what is the tier multiplier (usable ÷ footprint)?

**Answer.** `litter_area_frac` ≈ **0.45** (band 0.41–0.50). Tier multiplier ≈ **1.85** (band
1.78–2.00). Litter share of building footprint ≈ **0.82**.

### Evidence

| source | system | litter fraction | tier multiplier | verification |
|---|---|---|---|---|
| Zhao et al. 2015, *Poultry Science* 94:475–484, Table 2 | CSES Midwest aviary, 154.2 × 21.3 m, ~50,000 hens, Big Dutchman NATURA60 | 41.4 % incl. nest / **44.4 %** excl. | **1.91×** | FULL |
| PMC6414038, same facility, 153 × 21 m, 51,405 hens | US aviary, litter-access treatments | **45.9 %** | **1.83×** | FULL |
| Campbell et al. 2016, *Poultry Science* 95:164–175 | same facility, Lohmann White | gives litter's 40/60 open-vs-under split | — | FULL |
| Big Dutchman NATURA 70 brochure | manufacturer rule of thumb, EU density | **50 %** (derived) | **2.0×** (derived) | FULL |
| Groot Koerkamp (existing anchor, §S28) | EU | 47 % | — | prior pass |

Key tabulated figures (Zhao Table 2, aviary inner rows, cm²/hen): wire mesh 547, solid surface 104,
**forage/litter floor 520**, nest 86, total **1,257**. PMC6414038 states *"525 cm2 hen−1 on the
litter floor and 620 cm2 hen−1 in the aviary system"* → 45.9 %, and a litter loading of
**19.0 hens/m²**.

### Does litter_frac = 1 / tier_multiplier?

**No — use `0.82 / tier_multiplier`.** In a true multi-tier aviary the ground floor is essentially
all litter; the mesh and slats are up in the elevated tiers. The missing ~18 % of footprint is
inspection aisles, end zones and walls, not slat. Four independent confirmations:

1. Campbell et al. 2016, quoted directly: litter comprised *"open litter in front of the tiered
   enclosures (40% of total litter area) and the litter area underneath the enclosures (60%)"*.
2. Section arithmetic at the Iowa house is exact: outer sections 15 × 3 m holding 857 birds →
   857 × 525 cm² = 44.99 m² against a 45 m² section floor. Litter = **100 % of section floor**.
3. Campbell's under-system litter width works out to 1.86 m — exactly the NATURA60 profile width
   (73.23") in the US brochure.
4. The NATURA60 legend lists an *"Interior scratch area"* and offers a raised inspection aisle
   *"to utilize 100% of the house surface as a scratching area"*.

Naive substitution overestimates: 1/1.83 = 55 % against an actual 46 %.

### What UEP actually requires

**UEP 2017**, read directly: *"the littered area should cover at least 15% of the usable floor area
of the house (including the floor area of tiers)."* So the denominator is tier-inclusive usable
area — the premise in the register was correct.

**UEP 2024** replaced the percentage with an absolute: *"at least 21.6 square inches per hen of
scratch area."* 21.6 ÷ 144 = exactly 15.0 %, so the two coincide at the multi-tier floor. **Our
episode window (2025-06 → 2026-11) sits under the 2024 revision**, and `docs/world-bible.md` does
not currently carry the 21.6 sq in/hen scratch figure at all. Flagged, not fixed.

Triangulation: Certified Humane also sets 15 % of available floor space. EU Directive 1999/74/EC
requires 250 cm²/hen littered area with litter over **one third of the ground surface** — note the
EU uses a *ground-surface* denominator for that rule, the cleanest confirmation the two denominators
genuinely differ. The EU's 250 cm²/hen = 40 hens/m² litter against the US floor's 139.4 cm²/hen
(21.6 sq in) = 71.8 hens/m² — **the US regulatory floor permits litter loading 1.8× denser than the
EU's.**

SECONDARY only, unverified wording: a UEP scientific advisory committee has reportedly proposed
raising the minimum to **30 %** and excluding nest area from usable living area (WATTAgNet article
body inaccessible). Direction corroborated by everything else; do not quote the wording.

### Where this puts our house

Usable 18,000,000 sq in = 11,613 m².

| litter frac | litter m² | hens/m² litter @125,000 | @138,461 | vs Groot Koerkamp's measured 21.4 |
|---|---|---|---|---|
| 41 % | 4,761 | 26.3 | 29.1 | 1.23× |
| **45 %** | **5,226** | **23.9** | **26.5** | **1.12×** |
| 50 % | 5,806 | 21.5 | 23.8 | 1.01× |

| tier mult | footprint m² | birds/m² footprint @125,000 | @138,461 | vs Kang's knee at 19 |
|---|---|---|---|---|
| 1.78 | 6,524 | 19.2 | 21.2 | 1.01× |
| **1.85** | **6,277** | **19.9** | **22.1** | **1.05×** |
| 2.00 | 5,806 | 21.5 | 23.8 | 1.13× |

**Two findings that matter more than the parameter itself.**

1. **The Groot Koerkamp water-input coefficient transfers.** At 45 % we sit at 23.9 hens/m² of
   litter against his measured 21.4 — within 12 %, so `+126.8 g/kg litter/day` is applied at
   essentially its measurement point rather than extrapolated 3.4× as the 15 % figure would have
   required.
2. **Our compliant, UEP-floor house sits AT Kang's knee — robustly.** (Kang's denominator was an
   *assumption* when this was first written; it is now **verified as pen footprint** — see the Kang
   section below, which also lists five caveats that weaken the anchor.) Across the entire researched
   tier band (1.78–2.00) the compliant arm lands at 19.2–21.5 birds/m² of footprint against Kang's
   measured knee of 19. This is not a knife-edge artifact of one parameter choice. The overstocked
   arm moves to 21.2–23.8, clearly past it. The wave's primary pathway should therefore bite — but
   the "good" reference policy cannot reach a pristine litter state, because operating at the
   certification floor is already marginal. That is arguably true of real UEP-floor farms.

### Internal consistency check (repo-side, not from the literature)

Our default belt interval is 2 days (`integrate.py:175`), giving a litter moisture equilibrium of
**20 %** (`params.py:222-223`, 15 % floor + 5 %/day), against a footpad threshold of **30 %**
(`fpd_moisture_ref`). Groot Koerkamp's real aviary at 21.4 hens/m² litter ran litter DM 700–850
g/kg = **15–30 % moisture**. Our 20 % sits inside that band *only* at a high litter fraction. At the
15 % fraction we currently imply (71.8 hens/m²) we would be 3.4× his loading yet reporting litter
drier than his house and drier than Kang's least-crowded arm (23 %) — physically incoherent. **The
existing, already-calibrated footpad and ammonia behaviour implicitly assumes a generously-littered
house.** Authoring ~45 % should therefore preserve the existing calibration rather than break it.

### Confidence

**High:** the denominator question; that a multi-tier ground floor is essentially all litter; that
15 % is a regulatory floor and not a description of real houses.

**Moderate:** the 45 % value itself. Three papers agree closely (41.4 / 44.4 / 45.9 %) **but all
three describe the same facility** — the CSES Midwest research farm. N = 1 house, N = 3 papers.

**NOT FOUND:** any litter-fraction figure for a US aviary other than CSES; explicit litter
percentages in Vencomatic, Jansen, Farmer Automatic, Valli or Tecno specs; GAP's laying-hen
litter percentages.

**Flagged mismatch:** combi/convertible systems are a genuine low-litter class (possibly under
30 %). If our house is meant to be a combi rather than a true aviary, 45 % is wrong.

**My recommendation.** Author `litter_area_frac: 0.45` in `corpus/company.yml`, with 0.41–0.50 as
the sensitivity band, and treat the Task 5 no-regression test (equilibrium unchanged at 144 sq
in/hen for belt intervals 1–14) plus the Kang flat-then-jump shape test as the joint arbiters.

---

## Kang 2018 — OBTAINED IN FULL, denominator resolved (the fourth pass)

**Why this pass ran.** Everything in D15 above rested on the claim that Kang's "13/15/17/19 hens per
m²" is measured per m² of **pen footprint**. That claim was an **assumption made by an earlier
session, never read from the paper** — S22 had only ever been read at SUMMARY level. The two
readings differ by the tier multiplier (~1.85×) and invert the conclusion: on a footprint basis our
house sits at 19.9 hens/m², at/past the knee; on a tier-inclusive basis it sits at 10.8, below even
Kang's lowest arm, and Tasks 5–6 would have no basis at all.

**The paper is now READ IN FULL.** Kang et al. 2018, *European Poultry Science* 82,
DOI 10.1399/eps.2018.245. Open access (CC-BY-NC-ND). Persisted at
`docs/research/sources/Kang-2018-EPS-aviary-stocking-density.pdf`.

**Acquisition note worth reusing.** Three prior passes failed because they went at the publisher's
*current* host (ScienceDirect/Elsevier — 403/CAPTCHA). The publisher's **former** host is archived
in the Wayback Machine with the free PDF, and the whole 2013–2024 EPS DOI-era back catalogue (~360
article PDFs) is archived the same way, under the pattern
`european-poultry-science.com/artikel.dll/EPS-10-1399-eps-<year>-<no>-<author>_<hash>.PDF`. The
**OpenAlex API** (`api.openalex.org/works/doi:<doi>`) also returned the full abstract — which alone
contained the pen dimensions and would have answered the question. Try both before declaring a
paper unobtainable.

### The answer: pen FLOOR footprint. Tiers are NOT counted.

**Verification: DERIVED, confidence ~0.97.** The paper never writes "floor area" or "usable area"
about its own densities, so this is arithmetic, not a quotation. Methods state:

> "the hens were randomly assigned to one of four stocking rates: 13 (pen size = 1.7 × 1.8 × 2.7 m;
> water nipple = 8; n = 40), 15 (pen size = 1.7 × 1.57 × 2.7 m; water nipple = 7; n = 40), 17 (pen
> size = 1.7 × 1.38 × 2.7 m; water nipple = 6; n = 40), or 19 (pen size = 1.7 × 1.24 × 2.7 m; water
> nipple = 5; n = 40) hens per m², with each treatment replicated four times."

16 pens × 40 hens = 640, matching the stated total. Taking 2.7 m as pen **height** and 1.7 × W as
footprint (verified independently in this repo):

| nominal | W (m) | footprint 1.7×W | 40 ÷ footprint | error | W × nominal |
|---|---|---|---|---|---|
| 13 | 1.80 | 3.060 m² | 13.07 | +0.6 % | 23.40 |
| 15 | 1.57 | 2.669 m² | 14.99 | −0.1 % | 23.55 |
| 17 | 1.38 | 2.346 m² | 17.05 | +0.3 % | 23.46 |
| 19 | 1.24 | 2.108 m² | 18.98 | −0.1 % | 23.56 |

All four arms close within 0.6 %. `W × density` is constant at ≈ 23.5 = 40 ÷ 1.7 — the authors'
own construction rule made visible.

**The tier-inclusive reading is refuted, not merely disfavoured.** At the 19 arm it requires usable
area = 40 ÷ 19 = 2.105 m², while the pen footprint is 1.7 × 1.24 = 2.108 m². Equal — so the **three
welded wire tiers the methods describe would contribute zero area.** Impossible. Same in all four
arms.

Corroboration: implied floor space is 765 cm²/hen at the 13 arm and **527 cm²/hen at the 19 arm**.
527 cm² is less than a conventional battery-cage allowance — inconceivable as *usable* space in an
approved welfare trial, entirely ordinary as *footprint* in a three-tier aviary. Separately, the
authors benchmark against a Korean standard of 17 birds/m², which is that rule expressed on a floor
basis (9 birds/m² usable ÷ an implied 1.89× tier multiplier), bracketing their top arm just above
the national legal maximum.

**So the D15 conclusion above HOLDS, now on verified footing:** compare footprint to footprint —
our 19.9 (using our own researched 1.85× multiplier) against their 19. Do the comparison in that
direction; converting *their* arms up to a usable basis requires borrowing a tier multiplier the
paper never reports.

### Table 6, obtained — and the shape is a step

Least-squares means, n = 4 pens/treatment; superscripts differ at P < 0.05.

| item | 19 birds/m² | 17 | 15 | 13 | SEM | P |
|---|---|---|---|---|---|---|
| litter moisture, % | **40.93 a** | 22.93 b | 23.57 b | 23.67 b | 1.39 | 0.04 |
| NH₃, ppm | **9.07 a** | 5.70 b | 5.85 b | 5.63 b | 0.32 | 0.03 |
| CO₂, ppm | **755.6 a** | 663.9 b | 611.8 b | 611.3 b | 24.25 | <0.01 |

Previously-known values confirmed exactly. Flat at ~23 % across 13/15/17, then a **17.3 percentage
point jump** at 19. This is a threshold, not a dose-response — Task 5's "do not author the knee, let
it emerge from the water balance" instruction is correct.

Other tables: hen-day production 75.6 / 78.9 / 82.3 / 83.1 % (19/17/15/13); floor eggs 4.48 / 2.49 /
2.18 / 2.04 %; feed intake 119.9 / 130.8 / 131.8 / 131.1 g/bird/d; eggshell strength 3.92 / 3.96 /
3.97 / 4.07 kg/cm² (P = 0.04); H/L ratio 0.46 / 0.38 / 0.31 / 0.32 (P = 0.03); serum corticosterone
757.0 / 461.4 / 393.4 / 337.4 pg/ml.

### Five caveats that WEAKEN this anchor — carry these forward

The denominator question is settled, but reading the paper in full showed it is a thinner reed than
the summary suggested. **Do not treat 19 hens/m² as a clean spatial-crowding threshold.**

1. **Water access is confounded with density.** Nipples per pen fall 8 / 7 / 6 / 5 as density rises,
   with group size fixed at 40 — so hens per nipple goes 5.0 / 5.7 / 6.7 / **8.0**, a **60 % rise in
   water competition** at the top arm. The 19-arm result is crowding *plus* resource restriction,
   not pure spatial crowding. (Realistic, since equipment scales with pen length in a real house,
   but not a clean manipulation.)
2. **The gas figures are LITTER gas, not house air.** Sampled with a Gastec detector-tube pump at
   the litter, once at trial end. 9.07 ppm is **not** interchangeable with a house NH₃ sensor
   reading at bird height, which is what our sim models.
3. **Litter moisture is a single end-of-trial timepoint** (4 cores/pen, AOAC 934.01). No time series.
4. **n = 4 pens per treatment** for all production, litter and gas outcomes; n = 8 birds for blood.
5. **Editorial quality is weak,** which should temper the precision we attribute to these numbers:
   Table 5 reports **P = 1.25** (impossible), the diet table lists available P at 32.0 g/kg (almost
   certainly 3.2), and "Avairy"/"Neatherlands" are misspelled in the abstract and methods.

Scope: 34–43 wk only, one house, one genotype (Hy-Line Brown), one system. It does not speak to a
full flock cycle.

### The gap that blocks using Kang for Task 5 directly

**Kang reports NO litter area** — no litter fraction, no litter depth, no split of footprint into
litter versus tier-covered. Litter material is rice hulls. **Ventilation rate is not reported**
(only 20 ± 3 °C and 65–70 % RH), and **no manure-belt regime is reported at all.**

Consequence: Kang gives the moisture *outcome* and the *shape*, but neither the evaporation side
nor the manure-removal side, so **a litter water balance cannot be closed from this paper**, and its
knee cannot be placed on a hens/m²-of-litter axis — which is the axis Task 5 uses. Kang constrains
the shape and confirms our house is in the affected regime on a footprint basis; Groot Koerkamp
remains the only source for the water-input coefficient itself.

---

## D7 — is fibre the right nutrition rung, and does it have a magnitude?

**Question.** Does a quantified dietary-fibre → feather-pecking or feather-damage effect exist?
Without one, switching DP07's rung from methionine to fibre would trade a sourced null for an
invented number.

**Answer: YES, with a dose-response.**

> **van Krimpen et al. 2009**, *Poultry Science* 88(4):759–773 (= Wageningen ASG Report 146),
> read FULL. Dietary insoluble NSP 72 → 115 g/kg moved feather damage score **0.58 → 0.30** on a
> 0–5 scale (0 = intact, higher = worse), SE 0.083, **P < 0.001**. That is **−0.28, 5.6 % of
> scale**. Dose-response: **FCS = 0.75 − 0.025 × insoluble NSP intake (g/hen/day)**, P < 0.001,
> **R² = 0.55**, valid over an observed intake range of 9.3–18.9 g/hen/day.
> 576 laying hens, non-cage floor pens, ISA Brown, 18–49 wk, 6 pens/treatment.

### The structural catch

**Fibre did not change measured pecking behaviour** in the same experiment: gentle P = 0.883,
severe P = 0.383. It improved the feather *outcome* without a detectable change in the pecking
*rate*. Energy dilution — the other arm of the same factorial — did nothing (P = 0.418), so the
active ingredient is specifically **insoluble NSP concentration**.

**Consequence for Task 12:** the two DP07 rungs act at different points in the chain. Enrichment
(D5) halves the pecking rate; fibre must reduce damage accrual **directly**. Modelling fibre as a
pecking-rate multiplier would encode a mechanism the source explicitly failed to find.

### Cross-check against the enrichment anchor

van Staaveren 2020 (enrichment): feather damage −0.14 on a 1–4 scale = **4.7 % of scale**.
van Krimpen (fibre): −0.28 on a 0–5 scale = **5.6 % of scale**. Two independent literatures, two
scales, two interventions, same magnitude. The suspicion test passes.

### The roughage trap — do NOT use these numbers

Steenfeldt, Kjaer & Engberg 2007, *Br Poult Sci* 48(4):454–468 (FULL) reports far larger effects
from roughage provision: plumage total score 13.9 → 18.3/19.2/16.3 on a 5–20 scale (**29–35 % of
scale**), severe pecking 0.60 → 0.03–0.09 pecks/bird/hour, mortality **15.3 % → 0.5–2.5 %**
(P < 0.02). Reasons to exclude it as a fibre coefficient:

- The control pens had a **full cannibalism outbreak** (15.3 % mortality, ~half cannibalism). This
  measures disaster-versus-normal, not a marginal improvement in a healthy flock.
- A **lighting accident** applied 23L:1D from wk 27–39 before anyone noticed. Long photoperiod is
  itself a feather-pecking risk factor and plausibly manufactured the outbreak the roughage rescued.
- **4 pens per treatment**, SEM 1.24 on a 15-point range.
- Effects were **absent at 24 and 38 wk**, appearing only at 53–54 wk.
- The intervention replaced **33–48 % of total as-fed intake** with wet forage delivered on the
  floor — simultaneously fibre, foraging substrate, occupation, and dietary dilution. Inseparable
  from enrichment.

**Practical note for content authoring:** the small-dose version — an alfalfa bale hung as
enrichment — does *not* reproduce Steenfeldt. On-farm studies of bales and pecking blocks find
heavy use but feather condition similar to control.

### Other sources checked

| source | finding | verification |
|---|---|---|
| Hartini et al. 2002, *J Appl Poult Res* 11(1):104–110 | cannibalism mortality 28.9 % → 14.3/15.9/17.8 %, P < 0.01 | ABSTRACT — and **caged**, 5 birds/cage, transfer questionable |
| Bearse et al. 1940 via van Krimpen 2007 | crude fibre 29 → 123 g/kg, direction only | SECONDARY, magnitude not reported |
| Desbruslais et al. 2021, *WPSJ* 77(4):797–823 | dedicated fibre review | **NOT RETRIEVED** — paywalled (403) |

**NOT FOUND:** any meta-analysis of dietary fibre for feather pecking (no pooled effect size
comparable to van Staaveren's for enrichment); any quantified pecking-*rate* reduction from dietary
fibre inclusion; any post-2010 replication of Steenfeldt's plumage effect.

**Limits on the coefficient:** single experiment, pen-level, one strain (ISA Brown), one 33-week
laying period, R² = 0.55. Do not extrapolate the slope outside 9–19 g/hen/day insoluble NSP intake.

**My recommendation.** Switch DP07's nutrition rung to **dietary fibre** (`place_feed_order` with a
fibre additive — a drop-in for the existing matcher shape, and the operationally correct action).
Encode van Krimpen's dietary coefficient. **Model it on damage, not pecking rate.**

**Open conversion, for Task 12 not now:** our sim tracks feather damage as **prevalence** (% of
birds affected, 0 → 57.8 % over the cycle, `layers/feather.py`), while both coefficients are
**severity scores** on 0–5 and 1–4 scales. Reading "5 % of scale" as "5 percentage points of
prevalence" is an assumption, not a derivation. Both anchors agreeing at ~5 % makes it defensible;
it must be labelled as a conversion.

---

## D11 — where to put the "better than the floor" boundary

**Question.** What stocking density do certification schemes above the UEP cage-free floor require?

**Two findings that overturned the framing.**

1. **GAP is not a tiered density ladder.** Standard 4.3.2 sets **1.5 sq ft/hen (216 sq in)** for
   indoor housing identically at every Step, 1 through 5+. GAP's steps differentiate on
   outdoor/pasture access, enrichment and beak-trimming — not indoor density. There is no
   "Step 2 = X, Step 3 = Y" table to borrow. FULL, read from the primary PDF.
2. **UEP's 144 is not a uniquely lax floor.** Certified Humane and American Humane Certified both
   land on exactly 144 sq in/hen for multi-tier systems. The US welfare-label schemes converged on
   the same number; the standards clearly exceeding it are European.

### The landscape, mapped onto our house (18,000,000 sq in)

| threshold | sq in/hen | birds in H6 | vs the 125,000 default | verification |
|---|---|---|---|---|
| UEP / Certified Humane / American Humane, multi-tier | 144 | 125,000 | — | FULL |
| EU Directive 1999/74/EC, RSPCA Assured, UK legal min (9 hens/m²) | 172.2 | 104,516 | −16 % | FULL |
| measured US commercial aviary (CSES) | 194 | 92,784 | −26 % | FULL |
| the plan's own "generous" exemplar | 200 | 90,000 | −28 % | — |
| **GAP, all Steps** (= UEP's own single-level all-litter figure) | 216 | 83,333 | −33 % | FULL |
| EU organic Reg. 889/2008 / Soil Association (6 hens/m²) | 258.3 | 69,677 | −44 % | FULL / SECONDARY |

**Denominator caveat.** All US scheme figures and the EU conventional directive use tier-inclusive
*usable area* and are mutually comparable. EU organic's "net area available to animals" was not
confirmed to treat tiers the same way — treat 258.3 as probably-comparable, flagged. RSPCA's
additional **15 birds/m² of ground footprint** cap for multi-tier houses (= 103.3 sq in/hen of
footprint) is a different quantity and must never be merged into the same column.

**My recommendation.** Sub-band at **216 sq in/hen, anchored to GAP** — a real US certification the
farm could credibly pursue, and a 33 % flock cut is serious but conceivable. I differ from the
researcher's recommendation of the EU organic 258.3 on two grounds: our farm is conventional
cage-free, not organic, so an organic density standard grades the model against a standard that
does not apply to the operation it is running; and 258.3 means placing 69,677 birds, a 44 % cut,
which is not a generous placement decision but a different business.

**Consequence if adopted:** the plan's authored "genuinely generous" exemplar of 90,000 birds
(200 sq in/hen) falls just short of 216, so that Task 4 test expectation changes. If the exemplar
should be preserved, the defensible alternative anchor is **194 — what a real US commercial aviary
actually runs** — empirical rather than a published standard, but arguably the more honest
benchmark for "better than the floor in practice".

---

## The caveat that spans all three

Our entire empirical picture of "a real US commercial cage-free aviary" — the 194 sq in/hen figure
used in D10 and D11, the 1,253–1,257 cm²/hen in the register, and all three litter-fraction papers
in D15 — traces to **one facility**: the CSES Midwest research farm, ~50,000 hens, Big Dutchman
NATURA60. It is the best-documented US commercial-scale aviary in the literature and the papers are
independent of each other, but it is **N = 1 house, not a sample**. Every "real commercial practice"
claim in this wave rests on it. Worth stating in any writeup that leaves the repo.

## Provenance

Three parallel research passes, 2026-07-31, run against the open decisions in
`docs/plans/2026-07-30-density-wave-decision-register.md`. Sources are linked inline above.
Supersedes nothing in `docs/research/2026-07-30-density-coefficients.md`; it extends it, and
pass 6 there remains the authority on the density→ammonia mechanism.
