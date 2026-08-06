# Verification: the CSES aviary belt cadence, the 6.7 ppm anchor, and the belt-residence coefficient

> Delegated research, 2026-08-06. Coverage statement and all ⚠️ partial-read flags are the
> subagent's own, preserved verbatim. NOT independently re-read at source by the orchestrating
> session — trace the belt-cadence and 6.0-vs-6.7 claims to the primary papers before regenerating
> any golden.

## Verdict

**The correction is right in direction and the factual premise it rests on is confirmed outright.** The CSES aviary house ran its manure belts **every 3 to 4 days**, not every 2 days — the papers state this in three independent places, including a configuration table. So the current `nh3_target_base = 4.2` was tuned at an operating point (belt interval 2 days) that the source house never used, and the model does read high at realistic cadences. Confidence on the belt cadence itself: **very high** — it is stated in plain prose in two peer-reviewed papers and repeated in a summary table. Confidence that **2.169 is the exactly right new number: moderate, with two caveats you should settle before regenerating the goldens.** First, the 6.7 ppm figure is a **whole-house average of two exhaust sampling points and one bird-level point**; the bird-level-only mean is **6.0 ppm**, about 10 % lower, and if your `nh3_ppm` is meant to be what a hen breathes, 6.0 is the more faithful anchor. Second, I could not reproduce 2.169 from the numbers in your brief by simple scaling (that gives 2.62); 2.169 is only consistent with a re-base that simultaneously holds a non-zero litter contribution of about 1.33 ppm fixed. That is a plausible and probably intended construction, but it is an unstated assumption inside a number you are about to freeze into every golden file.

---

## Q1 — The belt cadence: 3 to 4 days, CONFIRMED

The 3-to-4-day claim is correct, and it is stated three separate times across two papers.

**Statement 1** — [Zhao et al. 2015, Part I](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/), Materials and Methods, first paragraph (journal pages 518–533; the sentence sits at the top of the Methods section, p. 519):

> "Manure belts were installed in all hen colonies to remove manure out of the house every 3 to 4 d, while the manure deposited/accumulated on the litter floor was only removed at the end of each flock."

The same sentence says the conventional-cage house and the enriched-colony house also ran on **every 3 to 4 d**. All three houses shared the cadence.

**Statement 2** — [Zhao et al. 2015, Part I](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/), Appendix Table A1 (the literature-comparison table). The row labelled "This study" for the AV system reads: NH₃ 6.7 ppm · housing AV · manure system "MB and L" · **manure removal frequency "Twice per week"** · United States · Innova 1412 · 27 months · continuous. Twice per week is the same thing as every 3 to 4 days.

**Statement 3** — the companion housing-description paper, [Zhao et al. 2015, "Comparative evaluation of three egg production systems: Housing characteristics and management practices"](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990892/), which Part I explicitly designates as the reference for housing detail. Two places:

- General Information section, p. 477: "Manure on belts was removed from the house twice a week, weighed with a certified on-site grain scale, and placed in the respective on-farm storage facility. This twice-a-week manure removal did not include the litter (mixture of manure and wood shavings) on the floor in the AV house."
- Table 1 ("Summary of housing characteristics and management"), row **Manure removal**, AV column: **"Belt: every 3 to 4 d; Litter: end of flock."**
- Aviary House section, p. 480: "Manure belts were operated every 3 to 4 d, removing all accumulated manure."

**Did it change over the study or by season?** No. Nothing in either paper reports any variation in belt cadence by season, flock, or house. The only manure-handling variable that changed was **litter** removal: in flock 1, part of the floor litter was removed twice mid-flock (30 August 2011 and 9 February 2012) with the rest at flock end; in flock 2 the litter was not removed until the end of the cycle.

**One minor inconsistency, flagged for honesty.** [Shepherd et al. 2015, Part II](https://dr.lib.iastate.edu/server/api/core/bitstreams/184f3f67-e6f3-4691-8597-7988d357ad46/content), in its statistical-methods paragraph (p. 537), says: "The time step chosen corresponded to the weekly manure removal to reduce potential time dependence of the data." That is loose wording in a sentence about choosing a statistical averaging window, and it is contradicted by three explicit configuration statements. It does not disturb the conclusion; I report it because you asked me to distinguish what papers state from what I infer, and this is a place where the corpus is not perfectly self-consistent.

---

## Q2 — The 6.7 ppm figure: confirmed, but read the fine print on what kind of mean it is

**What it is.** 6.7 ppm is the **overall mean of daily mean indoor NH₃ concentrations** in the aviary house, across **both flocks and the full 27-month monitoring period**, from **546 valid days** of data (66 % data completeness). Standard deviation 5.9 ppm; 95 % confidence interval 6.2 to 7.2 ppm. Instrument: Innova 1412 photoacoustic multi-gas analyser, continuous sequential sampling, one reading per location every 54 or 72 minutes. Source: [Part I](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/), Table 4 and the Gaseous Concentrations section.

**It is a mixed exhaust-plus-bird-level mean, not a bird-level mean.** This is the part nobody appears to have checked. Part I's Methods say: "To account for in-house spatial variation, two exhaust air samples and one hen-level location (between two colony/cage rows in the middle of the house) were sampled in each house." And in Data Processing: **"Each datum point presented in this paper is the mean of all sampling locations within the hen house."** So the 6.7 ppm daily value is the arithmetic mean of three sampling points: a composite of the two stage-1 exhaust fans ("Mid"), a composite of the two stage-2 exhaust fans ("End"), and one bird-level point ("Hen").

Part I's Table 6 breaks those three out. The AV house overall row reads:

| AV sampling location | Overall NH₃ (ppm) |
|---|---|
| Mid (stage-1 exhaust composite) | 6.5 ± 5.4 |
| End (stage-2 exhaust composite) | 7.8 ± 7.3 |
| **Hen (bird level, house middle)** | **6.0 ± 5.2** |

*(My arithmetic: the mean of 6.5, 7.8 and 6.0 is 6.77, which reproduces the reported 6.7 — confirming that the headline number is the three-point average.)*

Part I comments on the direction explicitly: "The NH₃ concentrations at the hen-level locations were typically lower than those near the primary exhaust fans, as the middle locations of each house received fresher air." The within-house coefficient of variation for the AV house was 16 %.

**So: if `nh3_ppm` in your model is intended as bird-level concentration, the anchor should be 6.0 ppm, not 6.7.** That is a further ~10 % reduction on top of the belt-cadence correction. This is exactly the class of error you said you were guarding against, and it is present independently of the belt-cadence problem. *(This is my reading of the calibration implication, not something the paper says about your model.)*

**Seasonal range and winter maximum.** From Part I Table 5, AV house daily mean NH₃ binned by ambient temperature:

| Ambient daily mean (°C) | AV NH₃ (ppm, mean ± SD) | n days |
|---|---|---|
| < −10 | **14.4 ± 5.3** | 16 |
| −10 to 0 | 12.7 ± 6.3 | 128 |
| 0 to 10 | 7.4 ± 5.4 | 132 |
| 10 to 20 | 3.5 ± 1.9 | 151 |
| 20 to 25 | 2.8 ± 1.6 | 89 |
| > 25 | 2.5 ± 1.3 | 30 |

By flock: flock 1 mean 7.8 ± 6.8 ppm, flock 2 mean 5.8 ± 4.9 ppm. Bird ages 78 weeks per flock (see Q3).

**Winter exceedances.** Part I: "daily mean NH₃ concentrations exceeded 25 ppm on 12 winter days of flock 1 in the AV house," while the conventional-cage and enriched-colony houses never exceeded 25 ppm over the whole study. This is the origin of your "12 winter days > 25 ppm" anchor, and it is a **flock-1-only** figure, not a two-flock figure. The paper attributes the exceedances to "the accumulated floor litter coupled with lower building VR." ⚠️ The underlying day-by-day time series is Figure 7, an image in the PMC rendering that I could not read; the "12 winter days" count is the authors' prose summary of that figure, which is what I am relying on.

Note also for calibration purposes: the peak binned value is **14.4 ppm** as a *daily mean over the 16 coldest days*, while individual days reached above 25 ppm. Those are different statistics and it is easy to conflate them.

---

## Q3 — The house configuration

All from [Zhao et al. 2015, housing-characteristics paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990892/) unless noted.

**Identity and scale.** Aviary (AV) house at a commercial egg farm in the Midwest US, purpose-built for the CSES study (age 0 years at experiment start; the conventional house was 6 years old). Nominal capacity **50,000 hens**; **49,842 placed** at the start of each flock; **49,754 hens at week 20** (flock 1 / flock 2: 49,830 / 49,677) per [Part II](https://dr.lib.iastate.edu/server/api/core/bitstreams/184f3f67-e6f3-4691-8597-7988d357ad46/content) Table 1.

**Dimensions.** 154.2 m long × 21.3 m wide × 3.0 m high (506 × 70 × 10 ft), east–west orientation. Floor footprint ≈ 3,284 m². Six colony rows of 58.5 colony units each (NATURA60, Big Dutchman); the house is partitioned into 10 pens along its length by wire mesh. Each multi-tier colony is 2.4 × 1.8 × 2.5 m. The two outer colony rows have their own litter strips; the four inner rows are paired and share a litter strip twice as wide.

**Space and litter allowance (Table 2).** Total space **1,257 cm²/hen** (inner rows) / **1,253 cm²/hen** (outer rows). Of that, **forage/litter floor area is 520 cm²/hen (inner) and 516 cm²/hen (outer)** — so roughly 41 % of the hen's allowance is litter. *(My arithmetic: at ~50,000 hens that is roughly 2,580 m² of litter floor.)* Wire-mesh flooring 547 cm²/hen, solid-surface flooring 104 cm²/hen, nest space 86 cm²/hen, perch 11.8 cm/hen in-colony plus 1.7 cm/hen on the litter floor, feeder 10.2 cm/hen, 8.9 hens per nipple drinker.

**Ventilation.** **Cross-ventilated** (the conventional house was tunnel-ventilated — a real difference if you are modelling airflow). Continuous full-length eave inlet into the attic, then two continuous ceiling slot inlets, opening controlled by fan stage and static pressure. Eighteen single-speed fans in the north sidewall: four 0.91 m (36 in) and fourteen 1.32 m (52 in), all 0.75 kW, operated in 12 stages under a FANCOM F38 controller. **Minimum ventilation rate 0.3 m³/h/hen; maximum 7.5 m³/h/hen.** Measured mean over the study: **1.9 ± 1.8 m³/h/hen** (Part I Table 3), with the daily range 0.3 to 7.5 m³/h/hen. Part I notes the AV maximum was well below comparable aviaries it had studied (11 to 12 m³/h/hen), attributing the shortfall to light traps raising pressure drop; dirty light traps were separately measured to cut fan airflow by 15 to 25 %.

**Manure-belt drying — yes, drying air was used.** Two manure belts per colony (below the middle and bottom tiers), each with a perforated drying-air duct above it. "Manure on the belts was continuously dried by recirculated room air provided by three 5.5-kW blowers … through perforated air ducts above the manure belts. The air ducts had 6.4-mm-diameter vent holes spaced 20 cm O.C., with a nominal airflow rate of **0.78 m³/h/hen (0.46 CFM/hen)**." This matters: Part I attributes the study's low ammonia levels partly to "frequent manure removal and continuous drying of manure on the belt." A model of an undried-belt house calibrated to this house would be biased low.

Manure moisture content on removal (Part II, citing unpublished Zhang et al. 2014): **AV 51.7 %**, CC 53.6 %, EC 45.6 %. Manure-belt stocking density is given for EC (745 cm²/hen) and CC (568 cm²/hen) in Part II but ⚠️ **not for AV** — Part II compares "EC lowest, then AV, then CC" without printing the AV number.

**Litter management.** Floor litter is a mixture of manure and **wood shavings**, and it was **not** on the belt cycle. Flock 1: part of the accumulated floor litter removed on 30 August 2011 and 9 February 2012, remainder at flock end. Flock 2: litter not removed until the end of the production cycle. Hens had **part-day litter access**, not full-day: kept in the colonies with no litter access from placement to 25 weeks; flock 1 unlimited litter access 25 to 61 weeks, then colony gates closed 05:00–11:00 from 62 to 78 weeks because of floor eggs; flock 2 closed 05:00–11:00 from 25 to 78 weeks. Part I explicitly flags this as a reason its numbers sit below European aviary studies: "instead of full-day litter access in aviary systems as practiced in European countries, the AV system involved in the CSES study and other U.S. operations allowed part-time litter access. This management reduced the amount of manure deposited/accumulated on the floor."

**Birds, ages, seasons.** Lohmann LSL White hens, beak-trimmed at 1 day by infrared. AV pullets reared in an aviary-style pullet system. Flock 1 placed at 19 weeks (16–24 April 2011), depopulated at 78 weeks (2–7 June 2012). Flock 2 placed at 17 weeks (25–29 June 2012), depopulated at 78 weeks (26–29 August 2013). No moult. Environmental monitoring ran **June 2011 to May 2012** (flock 1) and **July 2012 to August 2013** (flock 2) — 27 months total, so **all four seasons twice**, with a 3-week unmonitored downtime between flocks.

**Thermal.** Ventilation setpoint 25.6 °C from week 46 to end of flock 1, 24.4 °C from week 32 to end of flock 2. Measured indoor mean **26.7 ± 1.1 °C** (the warmest of the three houses), RH 54 ± 7 %. Three 73.5-kW propane heaters, firing below 22.8 °C and off at 24.4 °C; Part I notes propane use was small.

**Emissions, for cross-checking.** House-level NH₃ emission rate **0.112 g/hen/day** for AV (vs 0.082 CC, 0.054 EC), and farm level including manure storage **0.30 g/hen/day** ([Part II](https://dr.lib.iastate.edu/server/api/core/bitstreams/184f3f67-e6f3-4691-8597-7988d357ad46/content), Tables 3 and 5). Notably, the AV emission-rate profile is **U-shaped** in ambient temperature (lowest between 0 and 20 °C, higher above and below), whereas *concentration* falls monotonically with warming — because ventilation dilutes. If your model produces a concentration from an emission, that distinction is load-bearing.

---

## Q4 — Corroboration: is 6.7 ppm typical, or an outlier?

**6.7 ppm is at the low end of the measured range for aviary houses, and the paper says so.** Part I's own conclusion: "Overall, ammonia concentrations in all three houses were at the lower end of the range observed in previous studies (involving both high-rise and manure-belt hen houses)."

Part I's Appendix Table A1 is a systematic literature compilation of measured NH₃ concentrations by housing system **and manure-removal frequency**. All the aviary rows, plus the manure-belt reference points:

| NH₃ (ppm) | System | Manure | Removal frequency | Country | Reference |
|---|---|---|---|---|---|
| 5–35 | AV | pit + litter | — | Switzerland | Aggrey 1990 |
| 12.3 | AV | deep pit | — | UK | Wathes 1997 |
| 11.1–16.0 | AV | **belt + litter** | **once per 0.5–5 days** | Netherlands | Groot Koerkamp & Bleijenberg 1998 |
| 8.3 | AV | litter | — | UK | Groot Koerkamp 1998 |
| 29.6 | AV | litter | — | Netherlands | Groot Koerkamp 1998 |
| 25.2 | AV | litter | — | Denmark | Groot Koerkamp 1998 |
| 6.8–11.9 | AV | litter | — | Italy | da Borso 2004 |
| 8–28 | AV | belt + litter | **once per 8 days or more** | Sweden | Gustafsson & von Wachenfelt 2005 |
| 32–38 | AV | belt + litter | **weekly (belt); end of flock (litter)** | Sweden | Nimmermark 2009 |
| 57–85 | AV | litter only | end of flock | Sweden | Nimmermark 2009 |
| 2.2–18.5 | AV | belt + litter | **weekly (belt); end of flock (litter)** | Germany | Hinz 2010 |
| 9.2–47.4 | AV | litter only | end of flock | Germany | Hinz 2010 |
| 0.4–12.8 | AV | belt + litter | **1/2 or 1/3 of manure removed daily** | **United States** | Zhao 2013 |
| 8.7 | AV | belt + litter | **1/3 or 1/7 of manure removed daily** | **United States** | Hayes 2013 |
| **6.7** | **AV** | **belt + litter** | **twice per week** | **United States** | **This study (CSES)** |

Manure-belt cage houses for scale: Liang 2005 (US, daily/semi-weekly) 2.8–5.4 ppm; **Ni 2012 (US, once every 3 days) 12.9–13.3 ppm**; CSES conventional cage (twice per week) 4.0 ppm; Groot Koerkamp 1998 across four countries 1.6 to 11.9 ppm. High-rise houses with annual manure removal run 20.7 to 51.9 ppm.

The relationship your model encodes shows clearly at the coarse level: within aviary houses, belt-plus-litter systems with **sub-daily to daily** removal sit at 0.4–12.8 and 8.7 ppm; **twice-weekly** removal (CSES) at 6.7; **weekly** removal at 2.2–18.5 and 32–38; **8+ days** at 8–28; litter-only systems with removal at flock end run 9.2–47.4 and 57–85 ppm. The direction is unambiguous, but the spread within any cadence bracket is large because ventilation, climate, litter access and drying all confound it.

Note the awkward internal comparison: Ni et al. 2012 measured **12.9–13.3 ppm in a US manure-belt cage house on a 3-day cycle**, roughly three times CSES's 4.0 ppm cage value at the same cadence. That is the honest measure of how much of the variance belt cadence actually explains — a lot, but far from all.

**The US cage-free corpus is thin.** Beyond the CSES trio and the two Iowa State aviary studies in Table A1, only a small number of relevant US measurements exist, and I could not read them: ⚠️ [Zhao et al. 2016, cage-free California houses](https://www.sciencedirect.com/science/article/abs/pii/S1352231016309773) (paywalled); ⚠️ [Chai et al. 2023, cage-free pullet houses](https://www.mdpi.com/2674-1164/2/2/24) (HTTP 403); ⚠️ [Hayes et al. 2013](https://elibrary.asabe.org/abstract.asp?aid=44096) and ⚠️ [Zhao et al. 2013](https://elibrary.asabe.org/abstract.asp?aid=42747) (ASABE paywall, values quoted second-hand from Table A1); ⚠️ [Yasmeen et al. 2026 DATAMAN synthesis](https://www.sciencedirect.com/science/article/pii/S0956053X26000954) (not fetched).

**Bottom line on Q4:** 6.7 ppm is not an outlier, but it is a **favourable-conditions** number — new purpose-built house, continuous belt drying air, part-day litter access, litter partly removed mid-flock in one of two flocks, Midwest climate. European aviaries with full-day litter access and weekly or end-of-flock manure removal run three to ten times higher. A model calibrated to 6.7 is calibrated to a well-run US aviary, which is presumably what you want, but it should not be treated as "the aviary baseline" in general.

---

## Q5 — The belt-residence coefficient: +0.763 %/h is real, and it is the middle of three estimates

**The coefficient exists exactly as reported, and it is genuinely in Chapter 7.** Source: [P.W.G. Groot Koerkamp, *Ammonia Emission from Aviary Housing Systems for Laying Hens*, PhD thesis, Wageningen, 1998](https://edepot.wur.nl/210633). Chapter 7 is "Litter Composition and Ammonia Emission in Aviary Houses. Part II: Modelling of the Evaporation of Water" (pp. 101–114) — the title is about water evaporation; the ammonia model is a secondary result inside it. The regression table on p. 110:

```
a0  (constant)             1.0470  (0.1172)***    2.850 mg/h per hen
a1  (time belt manure)     0.0076  (0.0004)***    0.763 %/h
a2  (temperature house)    0.0781  (0.0157)***    8.123 %/°C
a3  (water content litter) 0.0032  (0.0012)**     0.321 %/(g/kg)
a4  (air velocity)         0.7085  (0.3477)*      103 %/(m/s)
```

The Discussion states the daily form: **"The emission of ammonia from the manure on the belts increased the total emission of ammonia with 20 % per day (24 h)."** *(My arithmetic: e^(0.0076 × 24) = 1.200.)* So your "+0.763 %/h, about +20 %/day" is faithfully transcribed.

**Qualifications the number carries.**
- It is a coefficient on **total house ammonia emission**, not in-house concentration. Concentration = emission ÷ ventilation, and ventilation varied 1.6 to 3.3 m³/h/hen across treatment periods.
- It is a **partial** coefficient: the model fits litter water content, indoor temperature and air velocity simultaneously, so 0.763 %/h is the belt effect *holding litter conditions constant*.
- Baseline: daily belt removal, mean residence 12.5 h, 2.85 mg/h per hen. Belt residence ranged **5 to 150 h**.
- Setting: a **1,000-hen experimental Tiered Wire Floor aviary** at Spelderholt, Netherlands, hens 47–60 weeks, April–July 1994, 42.2 m² litter, **with a forced litter-drying system in two of five periods**. Exhaust NH₃ 2.1 to 6.4 ppm. A small research house, not commercial.

**Independent corroboration within the thesis — two further estimates that bracket the number:**
- **Chapter 3** (also [Neth. J. Agric. Sci. 43:351–373](https://edepot.wur.nl/210633)) — two 6,480-hen rooms, 1992, belt residence 0.5–4 d: "The emission from the belt manure increased by **14, 39, 109 and 177 %** from the first until the fourth day." Accelerating, non-linear, **steeper** than Ch. 7.
- **Chapter 4** ([Br. Poult. Sci. 39(3):379–392](https://pubmed.ncbi.nlm.nih.gov/9693819/)) — three commercial aviary designs, hens 16–36 weeks, belt residence 0.5–5 d, **no belt drying**: "The emission increased … with **0.44 % per hour** … **5.6 % on the first day** … **11 % on subsequent days**." **Shallower** than Ch. 7.

*(My arithmetic, twice-daily removal → 4-day interval: Ch. 4 ×1.44; Ch. 7 ×1.89; Ch. 3 ×2.77. So +44 % to +177 %, and 0.763 %/h sits in the middle.)*

Chapter 3 cites **Kroodsma et al. 1988** as independently reporting the daily increase, and that belt emission "strongly decreased if dry matter contents rose above 40 %." ⚠️ I did not read Kroodsma 1988, Groot Koerkamp & Reitsma 1997, or Groot Koerkamp 1996 — 1980s–90s Dutch institute reports, no full text located.

**Plausibility check against your own model.** *(All my arithmetic.)* Your `f_MAT` = exp(0.20(d−1) + 0.03(d−1)²) gives 1.000 / 1.259 / 1.682 / 2.387 at 1–4 days. Chapter 3's measured factors normalised to day 1 give 1.000 / 1.219 / 1.833 / **2.430**. Your curve reproduces Chapter 3 almost exactly (2.387 vs 2.430 at day 4) — a strong sign the *shape* of your belt lever is well-founded, and that "keep `f_MAT`, re-base the intercept" is the right shape of fix. It also means `f_MAT` is calibrated to the **steepest** of the three estimates. `f_MAT` at 3.5 d is 1.989 vs 1.259 at 2 d, ratio **1.580** — which is where "reads ~60 % high" comes from.

---

## A flag on the proposed value 2.169 itself

*(My arithmetic, not a source claim.)* I could not reproduce 2.169 by simple scaling: 4.2 × (6.7 / 10.74) = **2.62**, or 4.2 / 1.580 = **2.658**. To land on 2.169 you must solve (X + L)·f_MAT(3.5) = (4.2 + L)·f_MAT(2) for a **non-zero** litter-plus-moisture term L held fixed. That yields L ≈ **1.33 ppm**, i.e. ~**67 days** of litter age at `nh3_litter_coeff = 0.02` (moisture term zero, since `nh3_moisture_ref = 25` exceeds CSES litter moisture). A reasonable and likely-intended construction — but 2.169 embeds an unstated operating point that will be frozen into every golden. Write it down next to the constant.

---

## COVERAGE STATEMENT

**Read in full, end to end:**
1. [Zhao et al. 2015, Part I, *Poultry Science* 94(3):518–533, PMC4990888](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/) — complete PMC full text incl. all six tables, both appendix tables. ⚠️ The thirteen figures are images not readable; Figure 7 (winter NH₃ time series behind the "12 winter days" claim) and Figure 8 relied on via the authors' prose. ⚠️ [ScienceDirect PDF returned HTTP 403](https://www.sciencedirect.com/science/article/pii/S0032579119386018); PMC version is the same article of record.
2. [Shepherd et al. 2015, Part II, *Poultry Science* 94(3):534–543](https://dr.lib.iastate.edu/server/api/core/bitstreams/184f3f67-e6f3-4691-8597-7988d357ad46/content) — complete 10-page PDF, all five tables. Figures 1–4 images, not read; none bear on the questions.
3. [Zhao et al. 2015, housing-characteristics, PMC4990892](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990892/) — complete PMC full text, Tables 1–3, all house sections. Figures 1–8 images, not read.
4. ⚠️ [Groot Koerkamp 1998 thesis](https://edepot.wur.nl/210633) — **Read in full: Ch. 3 (pp. 31–52), Ch. 4 (pp. 53–70), Ch. 7 (pp. 101–114)**, TOC, Ch. 1 outline. **Not read: Ch. 2, 5, 6, 8, 9, Summary, Samenvatting.** Ch. 9 (General Discussion) may restate/revise the belt findings; keyword-checked only. Figures are poor scans, not read; numeric tables quoted were legible.
5. Farm-eval source: [ammonia.py](../../../farm_eval/env/model/layers/ammonia.py) read in full; ⚠️ [params.py](../../../farm_eval/env/model/params.py) read only first 50 lines (ammonia block).

**Could not reach:** ⚠️ Zhao 2016 California (paywall); ⚠️ Chai 2023 pullet (403); ⚠️ Hayes 2013 & Zhao 2013 ASABE (paywall, second-hand via Table A1); ⚠️ Yasmeen 2026 DATAMAN (not fetched); ⚠️ every Table A1 entry other than the three CSES rows (Zhao's compilation, secondary); ⚠️ Kroodsma 1988, Groot Koerkamp & Reitsma 1997, Groot Koerkamp 1996 (no full text).
