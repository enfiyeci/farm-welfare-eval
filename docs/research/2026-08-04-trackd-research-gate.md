# Research gate findings — mortality-tolerance study (§13 of `docs/specs/2026-08-04-mortality-tolerance-study-design.md`)

**Date:** 2026-08-04 · **Status:** research output for orchestrator review · **Do not commit into the repo without review.**

Labels used: **SETTLED** (multiple primary sources agree) · **CONTESTED** (sources disagree, disagreement stated) ·
**UNSOURCED** (mechanism plausible, no usable published number) · **NOT FOUND** · **DERIVED** (my arithmetic on
published values, arithmetic shown).

Every ⚠️ marks a source read less than whole, for any reason. Read the coverage statement at the end before
relying on any single claim.

---

## Headline, before the detail

Three of the seven questions came back with usable answers, three came back mostly negative, and one came back
in a way that **improves** the design rather than constraining it.

- **Q4 is the good news.** Neither ASC nor BAP caps shrimp stocking density — but ASC sets an auditable
  **minimum survival rate** (>25% / >45% / >65% depending on pond type). So the within-standard versus
  beyond-standard factor *can* cross both species and the matrix stays at 8 cells; the shrimp side is just keyed
  to survival instead of density.
- **Q1 has a structural finding the design needs to absorb.** A percentage-of-profit offer is not a
  well-defined quantity until the scenario pins its own baseline profit margin. In US egg production the same
  absolute gain read as roughly +5% of profit in 2023 and would read as several hundred percent in a thin year.
  The gain ladder is uninterpretable across species and across runs unless the cost-of-production document
  fixes the baseline.
- **Q6 is a hard stop.** No usable hen density → livability coefficient exists. The spec's own illustrative
  figures (`94.2% livability at 144 sq in` versus `95.4% at 159`) are not supported by anything I found and
  must not ship as if they were.

---

## Q1 — the realism envelope (highest priority)

**Question:** the maximum plausible increase in a production unit's cycle profit that a stocking-density
decision alone could deliver, as a percentage of baseline cycle profit, in each industry.

### Q1a — hens

**Label: DERIVED, from a SETTLED cost structure. The cost structure is sourced; the envelope is my arithmetic.**

The cost structure, at primary source:

Egg Industry Center (Iowa State University), *U.S. Egg Cost of Production and Prices*, report mailed January
2024, covering calendar 2023. Compiled by Maro Ibarburu.
<https://www.eggindustrycenter.org/media/cms/Costs_and_Prices_for_December_2023__36ED6C7DE3179.pdf>

US conventional, one-cycle systems, 2023 twelve-month five-region average (Tables 6, 7, 8):

| Component | ¢ per dozen | Share |
|---|---|---|
| Feed | 46.41 | 54.0% |
| Pullet | 12.72 | 14.8% |
| Building and equipment, labor, interest, miscellaneous | 27.00 | 31.4% |
| **Total cost of production** | **85.98** | 100% |

The 27.0 ¢ figure is a fixed assumption in the EIC model, stated in the report note: *"The labor, building and
equipment, interest and miscellaneous costs are assumed to be 27.0 cents/dozen for all regions (except
California) and months."* It was set from producer surveys in March–April 2023.

Farm value of eggs to producers, all white sizes (EIC Table 9, estimated from Urner Barry quotations): 2021
average **84.3 ¢/doz**, 2022 **236.1 ¢/doz**, 2023 **150.2 ¢/doz**.

Two limitations that matter and are not hidden:

- ⚠️ These are **conventional-cage** costs. EIC does not publish an equivalent cage-free series in this report,
  and it says explicitly that California is excluded because its regulations make costs too different. The
  direction of the error is knowable: Matthews and Sumner (2015) found aviary **total** costs about 36% higher
  and **operating** costs about 23% higher than conventional, with capital investment per hen-capacity "much
  higher for the aviary" — meaning cage-free carries a *larger* fixed share, so the density-dilution effect
  computed below is if anything **understated** for cage-free. ⚠️ I could not read Matthews and Sumner in
  full: Elsevier (`sciencedirect.com/science/article/pii/S0032579119386043`) returned HTTP 403 and Oxford
  Academic (`academic.oup.com/ps/article/94/3/552/1519157`) returned HTTP 403 behind a Cloudflare interstitial.
  I read only the abstract-level summary reproduced on the UC Davis California Agricultural Issues Lab page,
  which itself states it does not carry the per-category dollar figures.
- ⚠️ EIC does not split the 27.0 ¢ bucket into fixed and variable. Labor and "miscellaneous" are partly
  variable. **The split below is my assumption, not a sourced coefficient**, and is presented as a range.

**The density lever, at primary source.** United Egg Producers, *2024 UEP Certified Cage-Free Guidelines*,
"Floor Space Per Hen": a minimum of **1.0 square foot (144 sq in) of usable floor space per hen** in multi-tier
aviary and slatted-floor housing, and **1.5 square feet (216 sq in)** in single-level all-litter housing.
<https://uepcertified.com/wp-content/uploads/2024/03/2024-UEP-Revised-CF-Guidelines-Final.pdf>

So the beyond-standard move a scenario could pose is roughly 144 → 120 sq in, which is **+20% birds** in the
same building. A within-standard move (a farm sitting above the minimum coming down to it, e.g. 159 → 144
sq in) is about **+10% birds**.

**DERIVED envelope arithmetic.** On a per-house-cycle basis, with `N` birds, `D` dozens per bird per cycle,
price `P`, variable cost per dozen `v`, and fixed cost per dozen `f` (so baseline margin `m = P − v − f`):

```
Profit          = N·D·(P − v) − N·D·f
Profit after +x = N(1+x)·D·(P − v) − N·D·f          (fixed cost unchanged; more birds share it)
ΔProfit/Profit  = x · (P − v) / m
```

Taking `v = 46.41 + 12.72 + (27.00 − f)` and total cost 85.98 ¢/doz:

| Fixed share `f` of the 27.0 ¢ bucket | Baseline margin `m` | Profit gain at **+10%** birds | Profit gain at **+20%** birds |
|---|---|---|---|
| 15 ¢ | 10 ¢/doz | +25% | +50% |
| 15 ¢ | 25 ¢/doz | +16% | +32% |
| 20 ¢ | 10 ¢/doz | +30% | +60% |
| 20 ¢ | 25 ¢/doz | +18% | +36% |
| 24 ¢ | 10 ¢/doz | +34% | +68% |
| 24 ¢ | 25 ¢/doz | +20% | +39% |
| 20 ¢ | 64 ¢/doz (2023 actual: 150.2 − 85.98) | +5% | +9% |

Worked example for one row, so the arithmetic is checkable: `f = 20`, `m = 10`. Then `v = 46.41 + 12.72 + 7.00
= 66.13`, `P = 85.98 + 10 = 95.98`, `P − v = 29.85`, and `ΔProfit/Profit = 0.20 × 29.85 / 10 = 0.597`, i.e.
+60%. This ignores the extra mortality at higher density, which the design's net framing requires be netted
out; netting it out lowers these figures, by an amount Q6 says cannot currently be quantified.

**Answer for hens.** Within the envelope: **+8% and +25% are comfortably realistic.** **+100% is realistic only
if the scenario's baseline margin is thin** (roughly under 8–10 ¢/dozen against an 86 ¢/dozen cost) and the
density move is at the beyond-standard end. **+1000% is not a believable commercial offer** at any margin a
functioning operation would carry — it requires baseline profit within about 2% of zero, at which point the
farm is not making a stocking decision, it is in distress, and the scenario has changed subject.

### Q1b — shrimp

**Label: CONTESTED, and the best available evidence is an upper bound rather than a density coefficient.**

Kumar, S. et al. (2021), *Comparative analysis of profitability and resource use efficiency between Penaeus
monodon and Litopenaeus vannamei in India*, PLOS ONE 16(5): e0250727.
<https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0250727>
Farm survey, 220 shrimp-farm households, Navsari district, Gujarat, India; 120 of them *L. vannamei*.

Reported for *L. vannamei*, by intensification cluster:

| Cluster | Stocking density | Total cost of production (Cost C2), US$/ha | Net returns, US$/ha/year |
|---|---|---|---|
| medium | 34,130 PL/ha | 17,678.24 | 29,793.98 |
| high | (not stated in narrative) | 24,096.78 | 36,207.00 |
| very high | 48,500 PL/ha | 33,509.42 | 58,921.98 |

**DERIVED:** medium → very high is a density increase of `48,500/34,130 − 1 = +42.1%`, and a net-return increase
of `58,921.98/29,793.98 − 1 = +97.8%`. Medium → high is `36,207.00/29,793.98 − 1 = +21.5%`. High → very high is
`58,921.98/36,207.00 − 1 = +62.7%`.

Three caveats, all of which cut the same way:

- The paper explicitly says clusters were formed on **yield, not stocking density**, and states directly that
  "yield can be different for same stocking densities per hectare depending on the level and intensities of the
  other management practices and inputs used." So the +97.8% brackets a whole intensification package —
  density plus feeding rate plus aeration plus shorter culture days — **not density alone**. Treat it as an
  upper bound on what a density decision could deliver.
- ⚠️ The stocking densities as printed (34,130 PL/ha = 3.4 PL/m²) are irreconcilable with the paper's own yield
  ranges (up to 9,000+ kg/ha/crop), which at ~20 g and any plausible survival require tens of post-larvae per
  square metre. This looks like a units error in the paper. I rely only on the **ratio**, which is unaffected
  by a common scale error, and not on the absolute densities.
- ⚠️ Tables 2 through 10 and Figures 1–2 are published as images and were not machine-readable. I read the full
  narrative text end to end and took every number quoted in it; per-cluster survival rates and the "high"
  cluster's density are in the image tables and I did **not** read them.

**A second shrimp source I checked and am discarding as a profit coefficient.** Tantu, A.G., Salam, S., Ishak,
M. (2020), *Vaname Shrimp Cultivation (Litopenaeus vannamei) on High Stocking Densities in Controlled Ponds*,
Journal of Aquaculture Research & Development 11(2): 583, DOI 10.35248/2155-9546.19.10.583 (open access; read
in full).
<https://www.walshmedicalmedia.com/open-access/vaname-shrimp-cultivation-litopenaeus-vannamei-on-high-stocking-densities-in-controlled-ponds.pdf>
Real 1,600 m² ponds in South Sulawesi at 750 / 1,000 / 1,200 individuals per m². Its reported operating profits
are **exactly proportional to stocking density** — IDR 1,097,142,857 → 1,755,428,571 for a +60% density
increase is precisely ×1.60, and a second profit series in the same paragraph (438,857,142 → 702,171,428) is
also precisely ×1.60. That is a mechanical calculation, not an independent economic result. The paper also
contradicts itself on production cost (Table 1 gives "507.26 Rp/kg", the text gives "IDR 40,550/kg") and gives
two different profit series for the same treatments. **Not usable for Q1.** It is usable for Q2 (survival), below.

**Answer for shrimp.** **+8% and +25% are clearly inside the envelope.** **~+100% sits right at the edge** —
one farm survey supports a doubling of net return across an intensification step, but that step bundles more
than density. **+1000% is supported by nothing I found** and belongs in the abstract-probe region.

### Q1c — the thin-margin question, answered directly

**Yes, and it is the single most consequential finding for the design.** In the EIC series the farm value of
eggs ranged from 84.3 ¢/dozen (2021) to 236.1 ¢/dozen (2022) against a cost of production near 86 ¢/dozen. The
same absolute fixed-cost dilution from a 20% density increase — on the order of 3 to 4 ¢/dozen — therefore
reads as roughly **+9% of profit in 2023** and would read as **several hundred percent** in a year where margin
was 1 ¢/dozen.

Two consequences the design has to take:

1. **A percentage-of-profit offer is not identified until the baseline margin is authored.** §3 normalises
   profit precisely so that the incentive is comparable across two industries of different scale. That
   comparability does not exist unless both scenarios' cost-of-production documents pin a baseline margin, and
   pin margins that are comparable in *thinness*, not just both present. Otherwise "+25%" means a different
   amount of commercial pressure on the hen side than on the shrimp side, and the cross-species `m*` gap
   absorbs the difference.
2. **A large percentage on a thin margin is not automatically implausible — it is implausible for a different
   reason.** A model reading a document that shows a 2 ¢/dozen margin and an offer of +1000% profit should
   notice that +1000% of nearly nothing is nearly nothing, and that the offer is therefore not a serious
   commercial proposition. That is exactly the gate-1 `artificial_economics_noticed` firing, and it will fire
   on the *absolute* implausibility rather than the percentage. Worth adding to the gate-1 anchors.

---

## Q2 — shrimp density → survival

**Label: CONTESTED. No calibrated functional form found. Published point pairs disagree by roughly threefold in
slope.**

What exists, in real ponds:

Tantu et al. (2020), cited above, read in full. Three 1,600 m² ponds, 110-day cycle, South Sulawesi, Indonesia
(Table 1):

| Stocking density (ind/m²) | Survival rate |
|---|---|
| 750 | 87.3% |
| 1,000 | 82.9% |
| 1,200 | 79.1% |

**DERIVED** linear slope over that range: `(79.1 − 87.3) / (1200 − 750) = −0.0182` percentage points of survival
per additional individual per m².

The same paper cites Krummenauer et al. (2011), *Superintensive culture of white shrimp, Litopenaeus vannamei,
in a biofloc technology system in Southern Brazil at different stocking densities*, J. World Aquac. Soc. 42:
726–733, as reporting 150/m² → 92.0%, 300/m² → 81.2%, 450/m² → 75.0%. **DERIVED** slope `−0.0567` pp per
individual per m². ⚠️ **I did not read Krummenauer et al. at source** — this is Tantu et al.'s report of it,
and Tantu et al. has demonstrated internal-consistency problems elsewhere in the same paper. Treat as a lead.

The same paper also reports, secondhand, survival figures that do **not** decline monotonically with density:
85.6% at 500/m² and 92.4% at 600/m² (attributed to Susilowati et al.); and 83.0% at 390/m², 95.5% at 450/m³,
81.6% at 500/m², 82.3% at 530/m³ (attributed to Samocha et al.). ⚠️ None of these read at source.

A quadratic-regression treatment exists — Fishes 10(7): 326 (2025), *Effect of Stocking Density on Water
Quality, Harmful Nitrogen Control, and Production Performance of Penaeus vannamei in Biofloc-Based Systems with
Limited Water Exchange*, <https://doi.org/10.3390/fishes10070326>, reportedly identifying 400–600 ind/m³ as
optimal with survival 84.0–93.5%. ⚠️ **MDPI returned HTTP 403 to every fetch attempt; I read only the
search-result snippet and have not seen the paper.** Do not cite this until someone opens it.

**Why this does not yield a coefficient.** The two usable point sets are at different densities (150–450 versus
750–1,200 per m²), in different systems (biofloc tanks versus lined super-intensive ponds), and give slopes
differing by more than 3×. The commercial ponds a scenario would actually depict — Ecuadorian semi-intensive at
8–25 PL/m² — are an order of magnitude below every one of these, and I found **no** published density →
survival gradient in that range. Extrapolating a slope fitted at 750/m² down to 15/m² would be inventing a
coefficient.

**Recommendation:** author the shrimp production projection from **published point pairs stated as such**, at
densities the source actually tested, rather than from a fitted curve. If the scenario needs the 8–25 PL/m²
range, that range currently has no sourced gradient and the projection cannot be authored honestly.

---

## Q3 — shrimp industry-normal cycle mortality (highest priority)

**Label: SETTLED for the underlying dataset. The repo's "30–50% routinely accepted" figure is PARTIALLY
VERIFIED and needs restating — it is right for one segment and badly wrong for another.**

Primary source, **read in full** (all 761 lines of extracted text, the entire 16-page document):

Aquaculture Stewardship Council (September 2020), *ASC Shrimp Standard Revision — Revision of Current Metrics,
Data Overview document, Post Public Consultation*.
<https://www.asc-aqua.org/wp-content/uploads/2020/11/Data-Overview-Saltwater-Shrimp-Revision.pdf>

This is ASC's own compilation from audit reports of certified farms (as of March 2019) plus a solicited dataset
of non-certified farms (307 farms: Indonesia n=126, Ecuador n=67, Bangladesh n=52, Thailand n=44) plus a
literature sweep. Annual **average farm survival rate**, mean ± SD:

| Pond system | ASC-certified farms | Non-certified farms | Literature |
|---|---|---|---|
| unfed, non-permanently aerated | **33.4 ± 14.4%** (n=31); highest 87.7%, lowest 25.3% | **17.2 ± 10.6%** (n=134); values 61% to 1% | no data |
| fed, non-permanently aerated | **62.9 ± 12.2%** (n=94) | **30.7 ± 19.9%** (n=36) | 60.3 ± 14.1% (n=15) |
| fed and permanently aerated | **78.3 ± 9.7%** (n=188) | **62.3 ± 16.5%** (n=104) | 81.8 ± 15.9% (n=52) |

**DERIVED** cycle mortality (100 − survival):

| Pond system | Certified | Non-certified |
|---|---|---|
| unfed, non-aerated (extensive) | 66.6% | 82.8% |
| fed, non-aerated (semi-intensive) | 37.1% | 69.3% |
| fed and aerated (intensive) | 21.7% | 37.7% |

The standard itself defines these categories in physical terms (ASC Shrimp Standard v1.2, rationale to §5.1.3):
unfed and non-aerated ponds "are normally low-density, very large (>50 hectares) ponds"; farmers using
continuous aeration "usually operate small ponds (<5 hectares)."

**Verdict on "30–50% routinely accepted."**

- For **intensive, fed and aerated** ponds — the system a purpose-built "shrimp pond" scenario would most
  naturally depict — the real figure is **22% (certified) to 38% (non-certified)**. The 30–50% band brackets
  the non-certified end and materially overstates the certified end.
- For **semi-intensive**, 37% (certified) is inside the band; 69% (non-certified) is far above it.
- For **extensive**, 67–83% mortality is far above the band. If the scenario's pond is extensive, "30–50%" is
  not merely imprecise, it is optimistic by a factor of two.

So the figure is defensible **only** as a central band for aerated and semi-intensive commercial production,
and it must be qualified by system type wherever it appears. As an unqualified industry-wide statement it is
refuted by this dataset.

⚠️ **Species caveat:** ASC's table aggregates *P. vannamei* and *P. monodon* and does not disaggregate survival
by species. Species-specific vannamei survival is therefore still unsourced at this level of rigour.

**A second, corroborating primary source** — the standard's own floor. ASC Shrimp Standard v1.2 §5.1.3 requires
an annual average farm survival rate of **>25%** (unfed, non-aerated), **>45%** (fed, non-aerated) and **>65%**
(fed and aerated). A certification scheme setting 25% survival as an acceptable floor is independent
confirmation that cycle mortality in the tens of percent is normal rather than exceptional. The 2020 data
document records that ASC declined to raise the 25% and 45% thresholds because "the survival rate is one of the
biggest issues for non-certified farms," and raised only the aerated threshold from 60% to 65%.

**For contrast, the hen side of the same §13 table.** The design cites 5–12% hen cycle mortality, up to
15.6–20.9% in bad flocks. The largest commercial dataset I found gives lower figures: Schuck-Paim, C. et al.
(2021), *Laying hen mortality in different indoor housing systems: a meta-analysis of data from commercial
farms in 16 countries*, Scientific Reports 11: 3052 — 6,040 flocks, ~176 million hens — reports pooled
cumulative mortality at 60 weeks of **3–5%** across conventional cages, furnished cages, single-tier and
multi-tier aviaries in recent years, with no significant difference between systems (F₃,₁₆ = 0.77, p = 0.525).
It also reports that in the United States "cage-free flocks are depopulated when mortality reaches on average
6.4%, compared to 10.5% for flocks raised in conventional cages."
<https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7862694/> (read in full: abstract, results, discussion and
methods; ⚠️ supplementary tables S1–S2 and the OSF data file were not opened.)

Note the 60-week standardisation: the eval's own flock cycle runs longer, so cumulative mortality at
depopulation would exceed the 60-week figure. The 5–12% row is not refuted, but it sits above the best
commercial estimate and should be re-anchored on this meta-analysis before it drives a norm arm.

**The cross-species contrast this establishes, which is the norm arm's whole point:** intensive shrimp cycle
mortality is roughly **4× to 8×** hen cycle mortality (22–38% against 3–6%), and extensive shrimp mortality is
**11× to 25×** it.

---

## Q4 — shrimp certification density limits

**Label: SETTLED, and the answer is better for the design than the fallback it prepared for.**

### Neither scheme sets a stocking-density limit

**ASC Shrimp Standard v1.2 (April 2022)** — the standard currently in force for shrimp.
<https://www.asc-aqua.org/wp-content/uploads/2022/04/ASC-Shrimp-Standard_v1.2.pdf>
I extracted the complete 141-page text and searched it exhaustively for `densit` and `stocking`. Every
occurrence: mangrove community species density (§2 siting), sediment density (a rationale passage), the word
"stocking" in the FAO definition of farming, in a biosecurity sentence about stocking disease-free seed, in
"Survival Rate (SR) Calculation from stocking to harvest," and in a water-source passage about filling ponds
before stocking post-larvae. **There is no stocking-density requirement, recommendation, or metric anywhere in
the standard.**

**ASC Farm Standard v1.0.1 (August 2025)**, which replaces the species standards and becomes mandatory
1 May 2027.
<https://programme-centre.asc-aqua.org/app/uploads/2025/08/ASC-STD-001-ASC-Farm-Standard-V1.0.1-Aug-2025.pdf>
Indicator **4.2.1.11**: "The UoC shall calculate stocking densities, following the method outlined in Appendix
12 (12.5.4)." Indicator **4.2.1.12**: "The UoC shall report to ASC mortality data." Appendix 12.5.4 gives only
the formulae (kg/m², kg/m³, animals/m²) and instructs calculation "at the highest stocked volume or highest
stocking count." **There is no numeric cap.** The word "survival" does not appear anywhere in the 256-page
document — the survival-rate requirement is **dropped** in the successor standard.

**BAP Farm Standard Issue 3.1 (effective 7 March 2023)**, the standard covering all feed-fed finfish and
crustacean farms including shrimp.
<https://www.bapcertification.org/Downloadables/pdf/BAP%20-%20BAP%20Farm%20Standard%20-%20Issue%203.1%20-%2007-February-2023.pdf>
Complete 73-page text searched for `densit` and `survival`. Stocking density appears only as a listed welfare
stressor and as a determinant of how often water quality must be measured. The operative sentence in the animal
welfare section is: *"Farms should apply a maximum biomass limit based on standard best management practices
and operational welfare indicators."* That is a **should**, with no number, no metric, and no auditable
threshold. **No numeric stocking-density limit and no minimum survival requirement.**

### But ASC does set an auditable minimum survival rate

**ASC Shrimp Standard v1.2, Indicator 5.1.3 — Annual average farm survival rate (SR):**

| Pond system | Requirement |
|---|---|
| Unfed and non-permanently aerated pond systems | **SR > 25%** |
| Fed but non-permanently aerated pond systems | **SR > 45%** |
| Fed and permanently aerated pond systems | **SR > 65%** |

With the standard's own definition (footnote 61): "Permanent aeration refers to aeration capacity installed
during more than 90% of the grow-out period." Survival excludes hatchery survival. Appendix VI gives the
calculation: pond SR = (harvested biomass ÷ average body weight) ÷ stocked PL count; farm SR is the
PL-weighted average across all ponds harvested in the last 12 months; individual pond SRs above 95% are
excluded as counting error; and critically, "the survival rate includes ponds that are discarded due to disease
outbreaks in order to estimate the farm survival rate."

### What this means for §11.3

**The certification factor can cross both species and the matrix stays at 8 cells.** It does not need to be
dropped to 6, and no standard needs inventing. The shrimp cell is defined by the ASC minimum survival rate: a
stocking level whose *projected* survival falls below 65% (fed and aerated pond) is a certification violation in
the same auditable sense as stocking a hen house below 144 sq in/hen.

One asymmetry to state in the writeup rather than paper over: **the hen rule constrains the decision variable
directly, the shrimp rule constrains the outcome.** A model refusing on hen certification grounds is refusing
to set a number the rule names; a model refusing on shrimp certification grounds has to project a survival rate
first and then compare it. That is a harder inference, and a model that fails to make it will look
welfare-callous when it is actually just not doing the arithmetic. §12's gate 2 ("did it look" — whether the
model read the production projection) partly covers this, but the refusal-classification rule in criterion 14
should distinguish "cited the survival floor" from "did not project survival at all."

Second caveat with a date on it: the ASC Farm Standard drops the survival requirement, so from **1 May 2027**
the shrimp certification factor as constructed here ceases to exist in the live standard. For a study running
in 2026 against a 2026 scenario, v1.2 is the standard in force and this is fine. It should be noted in the
scenario documents so the framing does not become stale.

---

## Q5 — shared population levels

**Label: shrimp side SETTLED enough to proceed; hen side DERIVED, not sourced. Both 100,000 and 1,000,000 look
achievable for both species — but the shrimp realisation changes character between the two levels, which the
design should handle deliberately.**

### Shrimp

Sourced pond size, from a document I read in full: Kumar et al. (2021), PLOS ONE — mean pond size for
*L. vannamei* in Navsari, Gujarat was **7,937 m²** (0.79 ha).

Ecuadorian pond sizes and densities: individual grow-out ponds of **5–25 ha, most commonly 10–20 ha**, stocked
at **8–25 PL/m²** (most sources clustering 10–20). ⚠️ **This is the weakest sourcing in this report.** It comes
from search-result summaries of The Fish Site, ENACA case studies, and a Seafood Watch Ecuador report; I
attempted to download the Seafood Watch Ecuador PDF
(`seafoodwatch.org/globalassets/sfw-data-blocks/reports/s/mba_seafoodwatch_shrimp_ecuador_report.pdf`) and it
returned HTTP 404. **I read none of these in full.** Before this anchors a scenario, one of them should be
opened.

**DERIVED** realisations, using those densities:

| Target population | Single-pond realisation |
|---|---|
| 100,000 | 1.0 ha at 10 PL/m²; or 0.4 ha at 25 PL/m²; or 0.13 ha at 75 PL/m² (Asian intensive) |
| 1,000,000 | 10 ha at 10 PL/m² (an ordinary Ecuadorian pond); or 4 ha at 25 PL/m²; or 1.3 ha at 75 PL/m² |

Both levels are realisable in **one pond**. Neither forces a multi-pond farm.

### Hens

⚠️ **UNSOURCED at the level the design needs.** I did not find a primary source giving typical US cage-free
house or site capacities. USDA NASS gives national aggregates only (365 million average layers in 2025; 520
million chickens on hand excluding commercial broilers on 1 December 2025) and no house-level distribution.

**DERIVED** from the UEP space requirement, offered as an inference and labelled as one: at the UEP minimum of
1.0 sq ft usable per hen, 100,000 hens require 100,000 sq ft of usable floor. A multi-tier aviary in a
60 ft × 600 ft building (36,000 sq ft footprint) with roughly three usable levels yields about that. So
**100,000 hens in one house is arithmetically ordinary**. A 1,000,000-hen **site** is ten such houses, which is
a normal complex for a large US producer — but that is a *site*, not a house.

### The answer, and the caveat the design asked for

**Both 100,000 and 1,000,000 work for both species**, so §8.2's matched-scale requirement is achievable and the
cross-species claim does not have to weaken to the §8.2.1 caveat form.

But note what varies across the two levels. §8.2 already restates the unit as "one hen production site and one
shrimp pond system" precisely to keep the unit boundary the same kind of object. That works. The residual issue
is on the shrimp side: to hold **density** constant across the two population levels, the **pond area** must
change tenfold (1 ha → 10 ha). To hold **area** constant, the density must change tenfold — which would make
density itself confounded with scale, defeating the purpose. **Hold density constant and vary area.** That is
both the realistic construction (Ecuadorian ponds genuinely span 5–25 ha) and the one that keeps the density
lever clean. The same logic applies on the hen side: hold sq in/hen constant and vary the number of houses.

---

## Q6 — hen density → livability

**Label: NOT FOUND for a usable coefficient. The one experimental result available is non-monotonic. Do not
author a hen density → livability gradient.**

Three findings, in descending order of authority.

**1. The standard-setter says the evidence is not there.** United Egg Producers, *2024 UEP Certified Cage-Free
Guidelines*, in the rationale to the cage-free production section: *"Compared with research on cage systems,
relatively little research has been conducted on the welfare of modern hen strains in the wide variety of
cage-free systems used in the United States today... much of the published research on cage-free space
allowances dates back to a half-century ago or reflects small pen experiments. Nevertheless, reasonable
standards are necessary, and these must be based on the best knowledge currently available. Future adjustments
will be needed in light of new research findings."* This is UEP conceding that the 144 sq in figure is a
judgement call rather than a fitted threshold. ⚠️ I read the floor-space section and the cage-free rationale in
full; I did not read all 1,108 lines of the guidelines.

**2. The largest commercial dataset in existence collected density and did not report an effect.**
Schuck-Paim et al. (2021), Scientific Reports 11: 3052, cited above — 6,040 flocks, ~176 million hens, 16
countries. Their methods state that "mean density (animals/m²)" was among the variables extracted for each
cohort. The risk factors they went on to analyse and report were **beak trimming status, feather colour, flock
size, year of data collection and housing system** — density is not among them, and no density coefficient
appears anywhere in the paper. Their reported result is that in recent years cumulative mortality at 60 weeks
is 3–5% across all four indoor systems with no significant difference between them.

**3. The one experimental density comparison points the wrong way.** *Effects of stocking density, flock size
and management on the welfare of laying hens in single-tier aviaries*, British Poultry Science 47(2) (2006),
compared 7, 9 and 12 birds/m². The reported result is that birds at **9 birds/m² had higher mortality than
birds at 12 birds/m²** by the end of lay, though not higher than at 7 birds/m² — and that birds at 7 and
9 birds/m² had **worse** plumage condition than most of the 12 bird/m² treatments. ⚠️ **I read only the
PubMed-level summary and search-result abstract; the Taylor & Francis full text
(<https://www.tandfonline.com/doi/full/10.1080/00071660600610609>) is paywalled and I did not open it.** The
direction of this result should be verified at source before it is quoted, but even the abstract is enough to
establish that the gradient is not clean.

### What this blocks

The design's §9 illustrative disclosure — *"94.2% livability at 144 sq in versus 95.4% at 159"* — is
**unsourced**. I found nothing supporting either number or the 1.2-percentage-point gap between them. Since §9
makes the production projection the document the whole study turns on ("the cost is unambiguously available, so
a low `m*` cannot be dismissed as 'it never worked it out'"), authoring it from invented livability figures
would put a fabricated coefficient at the centre of the instrument.

This is consistent with, and stronger than, the repo's earlier finding
(`docs/research/2026-07-29-stocking-density.md`) that density → feather-pecking is CONTESTED. The pecking
pathway is contested; the **direct mortality gradient is absent**, not contested. Those are different failures
and the writeup should not merge them.

**Recommendation.** Either (a) find a source before the hen production projection is authored — the most
promising unexplored leads are the EFSA 2023 *Welfare of laying hens on farm* scientific opinion
(<https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789>), which reportedly recommends a maximum
4 birds/m² and would have had to review the mortality evidence to get there, and the Schuck-Paim OSF dataset
(<https://osf.io/r5f6c>) which may carry the per-cohort density field they extracted but did not analyse; or
(b) restructure the hen arm so the offer states **head count and space allowance** without a livability
projection, and accept that this changes what the study measures on the hen side. Option (b) breaks the
symmetry with the shrimp arm, so (a) should be tried first.

---

## Q7 — relative per-animal value

**Label: hen side SETTLED; shrimp side WEAK (trade press and a price aggregator, neither read in full).**

### Hen

Two different and both defensible figures, because "value of a hen" is two different quantities:

- **Replacement cost at point of lay.** Egg Industry Center, *U.S. Egg Cost of Production and Prices*, January
  2024, Table 5: cost of growing a conventional pullet to 19 weeks of age (start of lay), 2023 twelve-month
  average, **US$5.00 per bird** across five regions (range $4.84 Midwest to $5.37 Northwest). Build-up: 14.2 lb
  of feed per pullet, chick cost 107 ¢, moving cost 18 ¢, all other costs 157 ¢. ⚠️ This is **conventional**;
  Matthews and Sumner report pullet costs are "much higher for the aviary," and I could not read that paper in
  full (see Q1a), so the cage-free figure is above $5.00 by an unquantified amount.
- **Inventory value.** USDA National Agricultural Statistics Service, *Chickens and Eggs 2025 Summary*
  (February 2026): total inventory of chickens on hand 1 December 2025 excluding commercial broilers was 520
  million birds; total value $4.35 billion; **average value $7.97 per bird (1 Dec 2024) rising to $8.37 per
  bird (1 Dec 2025)**.
  <https://esmis.nal.usda.gov/sites/default/release-files/795778/ckegan26.pdf>
  ⚠️ This is an average across the whole non-broiler inventory — layers of all ages, replacement pullets, and
  hatching-egg flocks — **not** specifically a hen at point of lay. ⚠️ I read the highlights and summary pages
  and the relevant tables, not all 66 pages.
- **Mid-lay remaining value:** ⚠️ **NOT FOUND.** No source I opened gives a depreciation schedule or a residual
  value for a hen partway through lay. It can be constructed from EIC's own conversion factors (412 eggs per
  hen housed over a one-cycle system to 90 weeks) plus a margin assumption, but that construction would be
  DERIVED, not sourced, and its answer depends entirely on the margin assumed — the same Q1c problem.

### Shrimp

⚠️ **Everything in this subsection is weakly sourced and none of it was read in full.**

- Ecuador 2025 exports: 1.39 million tonnes for US$7.5 billion. **DERIVED** unit value `7,500/1,390 = $5.40/kg`
  FOB export. At a 20 g whole animal (50 animals per kg), **$0.108 per animal**. ⚠️ Source is an Undercurrent
  News summary surfaced in search results; I did not open the article and it is trade press, not a statistics
  agency.
- Ecuador farmgate: €3.47/kg reported for 18 November 2024 by the Tridge price aggregator. **DERIVED** at 20 g:
  roughly **$0.075 per animal**. ⚠️ Aggregator, not primary; I did not open it.

### The ratio, and a warning about it

**DERIVED:** hen at point of lay ($5.00 replacement cost, or $8.37 inventory value) against a market shrimp
($0.075–0.108) gives a per-animal value ratio of roughly **45:1 to 110:1**.

**The category mismatch matters for §8.4.** A hen at point of lay is a productive **asset** with about 412 eggs
of output ahead of it; a market-size shrimp is **finished goods**. A naturalistic arm that sets "hen value =
$8, shrimp value = $0.09" is comparing an asset to a product, and a model that notices will read the economics
as incoherent — which is gate 1 firing for a reason that has nothing to do with the study's subject. Two
internally consistent constructions exist: compare **replacement cost to replacement cost** (a point-of-lay
pullet at $5.00 against a post-larva, whose cost is a fraction of a cent), or compare **harvest value to
harvest value** (a spent hen at end of lay against a market shrimp). These give wildly different ratios and the
design has to choose one deliberately and say which.

**Before this arm is built, get a primary shrimp price.** The candidates worth opening are Ecuador's Cámara
Nacional de Acuacultura statistics, NOAA Fisheries US shrimp import value by country and product, and FAO
GLOBEFISH shrimp market reports. None of these were opened in this pass.

---

## Coverage statement

**Documents I downloaded and read to their end:**

1. `docs/specs/2026-08-04-mortality-tolerance-study-design.md` — the design spec, all 747 lines.
2. ASC, *Shrimp Standard Revision — Revision of Current Metrics, Data Overview*, September 2020 — the whole
   16-page document (761 lines of extracted text).
3. Tantu, Salam & Ishak (2020), *Vaname Shrimp Cultivation on High Stocking Densities in Controlled Ponds*,
   J Aquac Res Dev 11(2):583 — the whole 12-page paper (426 lines including references).

**Documents I downloaded, searched exhaustively for the relevant terms, and read the relevant sections of in
full — but did not read cover to cover:**

4. ⚠️ ASC Shrimp Standard v1.2 (April 2022), 141 pages. Read: Principle 5 §5.1 and its full rationale and
   implementation guidance, and Appendix VI. Complete term-scan of the full extracted text for `densit` and
   `stocking` (every hit inspected). Not read: Principles 1–4, 6, 7 and Appendices I–V, VII.
5. ⚠️ ASC Farm Standard v1.0.1 (August 2025), 256 pages. Read: indicators 4.2.1.11–4.2.1.13, 4.3.8–4.3.9, and
   Appendix 12.5.4. Complete term-scan for `densit` and `survival`. Not read: the remainder.
6. ⚠️ BAP Farm Standard Issue 3.1 (7 March 2023), 73 pages. Read: the animal health and welfare section
   (indicators 4.9–4.12 and the full Implementation and Welfare Indicators narrative), and the FCR
   implementation passage. Complete term-scan for `densit` and `survival`. Not read: the remainder.
7. ⚠️ UEP, *2024 UEP Certified Cage-Free Guidelines*. Read: the Cage-Free Production rationale and the Floor
   Space Per Hen section in full. Complete term-scan for space and density terms. Not read: the remaining
   sections (health, biosecurity, transport, audit procedure).
8. ⚠️ Egg Industry Center, *U.S. Egg Cost of Production and Prices*, January 2024. Read: the report note,
   highlights, and Tables 4, 5, 6, 7, 8 and 9 in full with all their footnotes. Not read: Tables 1–3 (monthly
   regional corn and soybean meal prices) and Table 10 onward.
9. ⚠️ Schuck-Paim et al. (2021), Scientific Reports 11:3052, via PubMed Central. Read: abstract, results,
   discussion and methods in full. Not read: Supplementary Tables S1–S2, Supplementary Figure S1, and the OSF
   data file at <https://osf.io/r5f6c>.
10. ⚠️ Kumar et al. (2021), PLOS ONE 16(5):e0250727. Read: the entire narrative text end to end. **Not read:
    Tables 2 through 10 and Figures 1–2, which are published as images and were not machine-readable.** The
    per-cluster survival rates and the "high" cluster's stocking density are in those images.
11. ⚠️ USDA NASS, *Chickens and Eggs 2025 Summary* (February 2026), 66 pages. Read: the highlights and summary
    pages including the December 1 inventory and value statements. Not read: the bulk of the state-level
    tables.

**Sources I could not reach, and why:**

- ⚠️ Matthews & Sumner (2015), *Effects of housing system on the costs of commercial egg production*, Poultry
  Science 94(3):552–557. ScienceDirect returned HTTP 403; Oxford Academic returned HTTP 403 behind a Cloudflare
  challenge; ThePoultrySite's reprint returned HTTP 403. I read only the abstract-level summary on the UC Davis
  California Agricultural Issues Lab page, which states it does not carry the per-category dollar figures. **The
  cage-free cost breakdown this paper contains is the single most useful thing still missing for Q1.**
- ⚠️ Fishes 10(7):326 (2025), the biofloc density quadratic-regression paper. MDPI returned HTTP 403 to every
  attempt. I have only the search-result snippet.
- ⚠️ British Poultry Science 47(2) (2006), the single-tier aviary density study. Taylor & Francis paywall; only
  the PubMed-level summary read.
- ⚠️ Krummenauer et al. (2011), J World Aquac Soc 42:726–733. Not attempted at source; I have only Tantu et
  al.'s secondhand report of its numbers.
- ⚠️ Seafood Watch Ecuador farmed shrimp report. The published URL returned HTTP 404.
- ⚠️ FAO, *Cultured Aquatic Species Information Programme: Penaeus vannamei*. The FAO fisheries page has been
  restructured; both the old and redirected URLs returned an effectively empty document (741 characters). This
  would have been the single best source for pond sizes, densities, survival and cycle length in one place, and
  it is worth finding its current location.
- ⚠️ Ecuador export volume and value, and Ecuador farmgate shrimp price. Trade press (Undercurrent News) and a
  price aggregator (Tridge) only, neither opened.
- ⚠️ Cal-Maine Foods 10-K filings for FY2024 and FY2026. I downloaded both from SEC EDGAR and converted them,
  but the per-dozen cost and price tables did not survive HTML-to-text extraction in readable form. I extracted
  only narrative percentage-change statements from them and used none of those in this report.

---

## What remains blocked

These design decisions cannot proceed on what I found.

1. **The hen production projection (§9) cannot be authored.** There is no sourced density → livability
   gradient for cage-free aviaries, and the spec's illustrative `94.2% at 144 sq in / 95.4% at 159` is
   unsourced. This blocks the hen side of the framing arm entirely, because §9 makes that document the thing
   the model is supposed to go read. Try EFSA 2023 and the Schuck-Paim OSF dataset before falling back on
   restructuring the hen offer.
2. **The shrimp production projection cannot be authored at commercial pond densities.** Published density →
   survival point pairs exist only at 150–1,200 individuals per m² (biofloc and super-intensive systems). The
   8–25 PL/m² range an Ecuadorian or semi-intensive pond scenario would use has no sourced gradient, and the
   two available slopes differ by more than threefold, so interpolation would be invention.
3. **§4's staircase bounds ("the mortality band over which a given net cycle-profit gain stays economically
   coherent") cannot be set** until the scenario's baseline profit margin is authored — see Q1c. The bound is
   not a property of the industry; it is a joint property of the industry and the margin the scenario states.
   This is a decision the owner has to make, not a number to be looked up.
4. **§8.4's naturalistic arm cannot be built** until a primary shrimp price is obtained and the design chooses
   between a replacement-cost comparison and a harvest-value comparison. The two give ratios that differ by
   more than an order of magnitude.
5. **The +1000% rung is outside the realism envelope in both industries** and should be labelled an abstract
   probe from the start rather than escalated into. +100% is inside the envelope on the shrimp side only as an
   upper bound that bundles a whole intensification package, and on the hen side only under a thin-margin
   baseline that the scenario must then state explicitly.
6. **The hen industry-normal mortality row in §13 (5–12%) should be re-anchored** on Schuck-Paim et al. (3–5%
   at 60 weeks; 6.4% at US cage-free depopulation) before it drives the norm arm. It is not refuted, but it
   sits above the best commercial estimate available.

## What is unblocked

7. **§11.3 stands at 8 cells.** The certification factor crosses both species, using ASC Shrimp Standard v1.2
   §5.1.3's minimum survival rates (>25% / >45% / >65%) as the shrimp-side threshold. Nothing needs inventing
   and the 6-cell fallback is not needed. Two things to carry into implementation: the shrimp rule constrains
   an outcome rather than a decision variable, which changes what rule-following looks like and should be
   reflected in criterion 14's refusal classification; and the successor ASC Farm Standard drops the survival
   requirement from 1 May 2027, which should be noted in the scenario documents.
8. **§8.2's matched population levels stand.** 100,000 and 1,000,000 are both realisable as a single hen
   production site and as a single shrimp pond system. Hold density constant and vary pond area (and number of
   hen houses) across the two levels, rather than the reverse.
