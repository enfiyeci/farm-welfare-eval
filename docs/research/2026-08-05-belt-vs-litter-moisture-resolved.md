# Belt frequency vs litter moisture — resolved at source, and the slope is ~14× too large

> Commissioned 2026-08-05 for decision 01. The researcher **broke the scan barrier**: the Groot
> Koerkamp thesis PDF has no text layer, so they rendered it with `pdftoppm` and OCR'd it with
> `tesseract` locally. Chapters 3, 4, 6, 7 and Chapter 8's front matter are now readable, including
> **Ch. 7 pp. 102–104**, the Materials-and-Methods pages every previous session was blocked on.
>
> ⚠️ Every thesis number below is OCR of a 1998 scan, not publisher text. Each load-bearing value was
> cross-checked against prose in the same chapter; the two critical ones are independently restated in
> the running text.

## Headline

**Belt removal frequency does not measurably drive litter moisture.** Forced litter drying moves it
~5 percentage points; belt frequency moves it 0.1–0.8 pp **with an inconsistent sign**. Our encoded
slope of **0.85 pp per belt-day is roughly 14× larger than anything defensible**, and it is attached to
endpoints belonging to a different treatment variable.

## The treatment design, from the page nobody could read

[Groot Koerkamp 1998 thesis](https://edepot.wur.nl/210633), Ch. 7 Table 1 (printed p. 104). It is a
**2-factor crossed design**, and the prose on the same page states it independently:

> "The litter drying system was switched on (2A and 2D) and off (2B, 2C and 2E), and the manure on the
> belts was removed once a week (2A and 2B), every day (2C and 2D) or two times a day (2E)."

| Period | Drying | Belt removal | Litter DM | **Moisture** | Air velocity | Litter temp |
|---|---|---|---|---|---|---|
| 2A | **ON** | weekly | 856 | **14.4%** | 0.28 m/s | 21.3 °C |
| 2B | OFF | weekly | 807 | **19.3%** | 0.07 m/s | 20.8 °C |
| 2C | OFF | daily | 799 | **20.1%** | 0.08 m/s | 20.6 °C |
| 2D | **ON** | daily | 855 | **14.5%** | 0.24 m/s | 24.0 °C |
| 2E | OFF | twice daily | 835 | **16.5%** | 0.08 m/s | 25.1 °C |

Confirmed in the chapter's own prose: *"The mean dry matter content of the litter varied between 799
(period 2C) and 856 g/kg (period 2A)."*

**Clean within-factor contrasts:**

- **Drying, holding belts fixed:** weekly 2A vs 2B = **−4.9 pp**; daily 2D vs 2C = **−5.6 pp**.
  Replicated at both belt frequencies, same sign, near-identical magnitude. **Mean −5.2 pp.**
- **Belts, holding drying fixed:** drying ON, weekly vs daily = daily **0.1 pp wetter** (slope −0.017
  pp/belt-day). Drying OFF, weekly vs daily = daily **0.8 pp wetter** — **the opposite sign to our
  model**. Both smaller than the within-period standard deviations (~1.5 pp).

The belt contrast is inside the noise, **flips sign** between drying states, and is non-monotonic
across three frequencies. That is a null result.

**Corroborated in Ch. 6** (same thesis, first half of the same cycle, drying on throughout): going from
5 to 7 belt removals per week, litter got **wetter, not drier** (7.5% → 8.3%). The monotonic driver
there is droppings accumulating as the flock matures — ash falls 93% → 60%, depth more than doubles.

**Confound, stated plainly:** the five periods ran sequentially April–July, so hen age, outdoor
temperature and litter temperature all trend across them. That weakens the belt contrasts (adjacent
periods) but **not** the drying contrast, measured twice at two belt frequencies at separate points.

## Where belt frequency demonstrably DOES act: ammonia

Ch. 7's fitted emission model (eq. 9) gives first-class coefficients:

| Driver | Coefficient |
|---|---|
| **Belt manure residence time** | **+0.763% emission per hour** (≈ +20% per day) |
| Indoor temperature | +8.12% per °C |
| Litter water content | +0.321% per g/kg (≈ +3.2% per moisture point) |
| Air velocity over litter | +103% per m/s |

Belt frequency also drives **belt manure** dry matter strongly (361 g/kg weekly vs 279–290 daily,
~7 pp). It simply does not propagate to the floor litter.

Note the tension in the last two rows: forcing air over litter cuts moisture (good for ammonia) but
directly accelerates volatilisation (bad). In this experiment the net was favourable because litter TAN
collapsed — a real tradeoff the model could represent honestly.

## What actually drives litter moisture, ranked

**Tier 1 — manipulated, replicated, large.**
1. **Air velocity over litter / forced drying** — −5.2 pp for 0.075 → 0.26 m/s. Costs ~0.5 m³/h per hen.
   Diminishing returns quantified: evaporation scales as **v^0.287**.
2. **Water input from droppings landing on litter** — 126.8 g/kg/day (s.e. 19.4), evaporation coefficient
   94.4, day-to-day carryover **λ = 0.488** (roughly a one-day memory). Independently confirmed in a
   modern US commercial aviary: [Ochs, Turner, Xin et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6414038)
   measured **31.3% moisture under full-day litter access vs 20.3% part-time** — an **11 pp swing from
   litter access hours alone**, with ammonia 17.2 vs 13.5 ppm.

**Tier 2 — measured, with confounds.**
3. **Bird age** — Ch. 8: water flow into litter peaks ~45 g/day/hen at 22 weeks, stabilising at ~7
   g/day/hen after 30 weeks, as the share of excreta landing on litter falls from ~50% to ~10%.
4. **Litter depth/mass** — Ch. 4: thinning below 1 cm dropped dry matter "up to about 10%".
5. **Stocking density** — [Kang et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5144664/): 27.8 /
   23.6 / 25.8 / **67.5%** at 5/6/7/**10** birds per m². Flat then a collapse. ⚠️ floor pens, not a belt
   aviary; evidence for a **threshold**, not a linear coefficient.
6. **Aviary geometry** — Ch. 4 equilibria: 20.5% (TWF), 23.3% (Natura), 36.2% (Boleg) under identical
   management. A 15 pp spread from design alone.
7. **Outdoor climate** — indoor vapour pressure = 0.700 kPa + 79% of outdoor.

**Tier 3 — universally asserted, unquantified for layers.** Drinker leaks and spillage
([USDA-ARS](https://www.ars.usda.gov/ARSUserFiles/np212/LivestockGRACEnet/LitterMoisture.pdf)); house
ventilation rate as distinct from litter-level air velocity.

**Architectural note:** in Groot Koerkamp's fitted water balance, **belt frequency does not appear as a
term at all**. If `layers/litter.py` relaxes toward a belt-interval equilibrium, it implements a
mechanism the source literature does not contain.

## If the slope stays: 0.06 pp/belt-day, range 0–0.15. The honest value is 0.

⚠️ **This is the researcher's inference from measured coefficients, not a measured value.** The one
mechanism by which belts could reach the litter is belt manure evaporating into house air, raising
indoor vapour pressure and shrinking the driving difference. Ch. 7 §3.5 fits it: β₃ = 2.55E-4
(s.e. 1.50E-4) over 5–150 h residence — and **the authors call this effect "small"** (β₃ is only ~1.7
standard errors from zero). Feeding it through their steady-state balance gives **0.05–0.08 pp per
belt-day**, agreeing with the measured null.

## The finding that matters most for DP16

**Our model's litter moisture only ever ranges 15–20%. The welfare literature says nothing happens
there.**

| Threshold | Moisture | Source |
|---|---|---|
| Caking begins | **~30%** | [Ochs 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6414038): 20.3% → 81.3% loose, 0% caked; 31.3% → 33.1% caked |
| Ammonia acceleration | ~25% | [USDA-ARS](https://www.ars.usda.gov/ARSUserFiles/np212/LivestockGRACEnet/LitterMoisture.pdf): 1.4× at 25%, 1.8× at 30%, max ~42% |
| Disease risk | **≥35%** | USDA-ARS |

**A footpad lever operating inside 15–20% is scoring a band in which the real-world answer is "the
litter is fine."** This is a deeper explanation of DP16's non-discrimination than the
evaporative-capacity knee: the node is not merely capped, it is **operating entirely below the region
where footpad harm begins**.

Whatever replaces the belt slope must be able to push moisture past ~28–30% under genuine neglect. The
evidenced levers that can: **litter access hours** (11 pp measured), **litter depth/refresh** (10 pp),
**stocking density above threshold**, **loss of litter-directed air movement** (5 pp).

**Footpad in layers, for the record:** [Ekstrand & Carpenter 1998](https://pubmed.ncbi.nlm.nih.gov/9649870/)
— White Leghorns, **38% FPD on dry litter vs 92% on wet**, with an explicit temperature gate: above
20 °C rising moisture raised incidence; **below 20 °C no new cases developed in any group**. ⚠️ Abstract
only — no numeric moisture percentages for the arms. *(This is the paper a previous session referred to
as "Wang 1998"; same PubMed ID.)* Our `fpd_moisture_ref` of 13.0% is not sourced to it.

## Is 14.4–20.1% a normal aviary range? Yes — normal to slightly dry

Groot Koerkamp Ch. 7 §4.4 states the general range: *"water content generally found in litter, being
100-250 g/kg"* — i.e. **10–25% moisture**. Our band sits inside it, at the dry end.

## URLs that could not be reached

- [MDPI: "Bedding Management for Suppressing Particulate Matter in Cage-Free Hen Houses", *AgriEngineering* 2023](https://www.mdpi.com/2624-7402/5/4/103) — **403**. ([DOI](https://doi.org/10.3390/agriengineering5040103)) Expected: measured litter moisture by bedding material and depth in US cage-free houses — a second modern US datapoint.
- [EFSA 2023, "Welfare of laying hens on farm"](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789) — not fetched, ~180 pp. **An open-access mirror exists and is worth trying:** [IRTA repository PDF](https://repositori.irta.cat/bitstream/handle/20.500.12327/2141/Nielsen_Welfare_2023.pdf?sequence=1&isAllowed=y)
- [Volkmann et al. 2024, layer footpad dermatitis, *Annals of Applied Biology*](https://onlinelibrary.wiley.com/doi/10.1111/aab.12923) — paywalled. The best candidate for a layer FPD coefficient.
- [Ekstrand & Carpenter 1998](https://pubmed.ncbi.nlm.nih.gov/9649870/) — abstract only. Would give the actual moisture percentages behind 38% vs 92%.
- [ScienceDirect: journal version of thesis Part III](https://www.sciencedirect.com/science/article/abs/pii/S0021863499904262) — not attempted; the thesis chapter carries the same figures.

## Coverage statement (carried through)

**Read end to end from source, via the researcher's own OCR:** thesis **Ch. 6** (pp. 87–99) complete;
**Ch. 7** (pp. 101–113) complete **including pp. 102–104 and Table 1**; [USDA-ARS litter moisture
PDF](https://www.ars.usda.gov/ARSUserFiles/np212/LivestockGRACEnet/LitterMoisture.pdf) complete.

⚠️ **Substantial but not cover to cover:** Ch. 3 (litter results and Table 5 read closely; ammonia
time-series modelling skimmed); Ch. 4 (design, litter results, discussion read; emission kinetics
skimmed); Ch. 8 (abstract, introduction and housing methods only — the 45 and 7 g/day/hen figures come
from its abstract, not its results tables).

⚠️ **Via WebFetch extraction, not an end-to-end read:** Ochs 2019; Kang 2016; the broiler
litter-moisture/FPD paper; two UGA extension pages.

⚠️ **Abstract only:** Ekstrand & Carpenter 1998. **Secondary summary only:** the 40% cage-free FPD
prevalence figure.

**Measured vs inferred:** every table value, fitted coefficient and treatment assignment is measured
and attributed. The steady-state arithmetic, the 0.05–0.08 pp/belt-day figure, and the "~14× too large"
reading are **inferences** from those measured coefficients.
