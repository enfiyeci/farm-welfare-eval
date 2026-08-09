# Worker fatigue → animal-care quality — the cross-domain evidence sweep

Eval: hen

> Commissioned 2026-08-07 by the staffing-design lane, targeting the third gap after the owner asked
> to push harder. **Angles:** slaughterhouse handling quality by shift position, vigilance/inspection
> decrement, healthcare shift-length studies with *patient* outcomes, agricultural-worker fatigue,
> and quantified worker-state → animal-welfare links. Delegated Opus pass, **not independently
> re-read by the orchestrator**; ⚠️ markers and coverage statement carried verbatim.
>
> **Headline for the design:** no study anywhere measures a stockperson's inspection quality against
> hours-into-shift (still absent). But two things arrived that the design can use: a same-species
> commercial study where *which humans did the work* changed bird injury rates by ~60% relative, and
> a convergent cross-domain finding that the operative variable is **continuous hours on duty under
> load**, not clock hour.

---

# Worker fatigue → animal-care quality: cross-domain evidence sweep

**Bottom line up front.** The gap is real and remains largely unfilled. After this pass there is **no study anywhere that measures a stockperson's inspection or husbandry quality against hours-into-shift.** What was found is one genuinely close analogue — a 4,219-load commercial poultry study where *human work rate crossed with time of day* predicts *bird injury rate* — plus a well-quantified inspection-decrement literature (radiology, X-ray screening, colonoscopy) that can ground a **direction and a rough magnitude band**, not a barn-specific coefficient. The slaughterhouse angle, expected to be the closest analogue, turned out to be the weakest: fatigue is repeatedly *named* as a cause of mis-stunning and never *measured* against shift position.

---

## Target 1 — Slaughterhouse / abattoir handling quality by time-in-shift

### 1a. The one real quantitative hit is not stunning, it is catching and loading

**[Cockram MS, Dulal KJ, Stryhn H, Revie CW (2020). Rearing and handling injuries in broiler chickens and risk factors for wing injuries during loading. *Canadian Journal of Animal Science* 100(3):402–410.](https://doi.org/10.1139/cjas-2019-0204)** — open access, [full PDF](https://strathprints.strath.ac.uk/72004/7/Cockram_etal_2020_Rearing_and_handling_injuries_in_broiler_chickens.pdf). **All 9 pages read end to end.**

- **Design:** retrospective observational study of processing-plant records, January 2009 – July 2010, Canada. Three-level mixed model (producer n=86, handling event n=1,694, load n=4,219 of 4,494 total). Outcome: square-root-transformed percentage of wing injuries per load attributed to handling.
- **Exposure as measured:** *speed of loading* (<5,000 vs ≥5,000 birds h⁻¹), *time of day loading began* (0000–0700 / 0701–1700 / 1701–2359), *catching team* (10 teams, A–J), plus bird weight, sex, season. Median loading duration 1.67 h; median speed 4,061 birds h⁻¹.
- **Outcome:** median 5.7% of birds per load with recent wing injuries (Q1 4.0, Q3 7.7, max 20.7); 99.6% of loads had at least one injured bird.
- **Effect sizes (Table 4, coefficients on the √-transformed percentage, 95% CI):**
  - Fast loading (≥5,000 birds h⁻¹) during daytime: **+0.20 (0.09 to 0.31), overall speed term p = 0.001**
  - Time-of-day × speed interaction, **p < 0.001**: morning × fast **−0.35 (−0.48 to −0.22)**; evening × fast **−0.17 (−0.31 to −0.03)**. In plain terms: going fast only hurts the birds during the *daytime* window.
  - **Catching team, p < 0.001**, coefficients from **+0.22 (team D)** to **+0.69 (team C)** against team I as reference. Translated to predicted prevalence (Fig. 5, all else fixed): **4.6% for the best crew vs 7.3% for the worst** — a ~60% relative difference in bird injury attributable to *which humans did the work*, holding bird weight, sex, season, speed and time of day constant.
  - Predicted percentages by speed × time (Fig. 6): daytime fast ≈7.6% vs daytime slow ≈6.8%; morning fast ≈6.2% vs morning slow ≈6.9%; evening ≈6.2% for both.
  - Univariate: longer *loading duration* was associated with **fewer** injuries (coeff −0.05, p = 0.046) — slower work, better handling.
  - Variance components: load 0.28 (0.26–0.29), handling event 0.08 (0.07–0.10), producer 0.01 (0.01–0.03).
- **What the authors say about fatigue:** they explicitly invoke it as a candidate mechanism but do not measure it — "the risk of injury is not simply due to loading the birds too fast but might also be related to other factors, e.g., handling problems that delay loading or fatigued catchers."

**Domain distance:** one step away. Same species, same commercial context, humans physically handling birds, and the exposure is a *work-rate × clock-time* variable rather than hours-into-shift. It cannot ground a fatigue coefficient — time of day here is confounded with light level in the barn, which the authors argue is the more likely mechanism. It **can** honestly ground two things: (i) that *who* does the husbandry and *how fast* they are pushed produces injury differences of the same order as bird-level biological factors, and (ii) a defensible magnitude anchor of roughly **1.1× to 1.6× relative difference in a handling-injury outcome** between well-resourced and pressured/poor human execution.

### 1b. Stunning: fatigue is asserted, never quantified

- **[Grandin T (1998). Objective scoring of animal handling and stunning practices at slaughter plants. *JAVMA* 212(1):36–39.](https://pubmed.ncbi.nlm.nih.gov/9426775/)** — 24 federally inspected plants, 10 states; >1,000 pigs and >1,000 cattle observed. Only 4 of 11 beef plants rendered 95% of cattle insensible with one shot. **Abstract read in full; ⚠️ full article not readable — the fatigue statement lives in the Discussion, behind AVMA's paywall.** Via the author's own [summary page](https://www.grandin.com/references/scoring.ab.html) (⚠️ extraction, not verbatim full text): ineffective first-attempt stuns with two captive-bolt stunners "increased late in the shift, when operators were fatigued," with a recommendation to evaluate at the beginning and end of shifts. **No numbers, no denominator, no test.**
- **[Grandin, USDA survey report](https://www.grandin.com/survey/usdarpt.html)** — 11 plants using captive bolt, 100–200 animals each; misses 0% to 20%. Recommends monitoring "at both the beginning and near the end of each shift" but **presents no beginning-vs-end data**. ⚠️ Read via extraction.
- **[Grandin, Animal Welfare Audits using HACCP principles (2013)](https://www.grandin.com/welfare.audit.using.haccp.html)** — searched in full for fatigue/shift/rotation content: **none present.**
- **[Kautto AH, Steen M, Vågsholm I, Berg C (2026). Factors affecting the effectiveness of captive-bolt stunning of reindeer at commercial slaughter in Sweden. *Acta Vet Scand* 68:12.](https://doi.org/10.1186/s13028-026-00852-x)** — 1,590 reindeer, 8 slaughter days, 2 abattoirs. Mis-stun rate 1.3%; 5.3% of effective stuns exceeded the 60 s guideline. Variables modelled included **operator experience (1/3/5 years)** — but **no time-within-day, no cumulative-animals, no session-duration variable.** Read in full via extraction.
- **[Pastrana-Camacho AP et al. (2025). Effectiveness of electrical stunning and bleeding in finishing pigs, two modern Colombian abattoirs. *Trop Anim Health Prod* 57:341.](https://doi.org/10.1007/s11250-025-04583-5)** — 959 pigs. Post-stunning reflexes 38.5% (33.8–43.4) in Abattoir A vs 0.2% (0.0–1.0) in B. **No time-of-day, shift-position, batch-order or operator-fatigue analysis.** Read in full via extraction.
- **EFSA slaughter opinions.** ⚠️ **Unreachable.** Wiley returns HTTP 403 to every route; efsa.europa.eu redirects there. Secondary reporting states that 29 of 30 pig-slaughter hazards and 39 of 40 cattle-slaughter causes of distress are attributed to staff, "mainly because of lack of appropriate skill sets … or because of fatigue." **Unverified against [the opinion itself](https://doi.org/10.2903/j.efsa.2020.6275); should not be quoted as sourced.** Even if verified, this is expert hazard attribution, not measurement.
- **[Jacobs L, Delezie E, Duchateau L, Goethals K, Tuyttens FA (2017). Impact of the separate pre-slaughter stages on broiler chicken welfare. *Poult Sci* 96(2):266–273.](https://doi.org/10.3382/ps/pew361)** — 81 commercial Belgian transports; wing-fracture prevalence rose 0.1% → 1.9% during catching (p = 0.003); catching crew named a risk factor. ⚠️ **Abstract only** — the reported positive correlation between catching-and-loading *duration* and wing-fracture prevalence is known only second-hand via Cockram et al.'s citation.

**Verdict, Target 1: CONFIRMED ABSENT for stunning-quality-by-shift-position. PARTIALLY FILLED for animal-handling-quality vs human work variables** (Cockram et al. 2020). The audit literature has *recommended* measuring beginning-vs-end-of-shift stunning for nearly thirty years and, as far as this search reaches, nobody has published the comparison. That absence is itself a citable finding for the design record.

---

## Target 2 — Vigilance / inspection-task decrement

### The strongest single number: radiologists, whole workday, real detection task

**[Krupinski EA, Berbaum KS, Caldwell RT, Schartz KM, Kim J (2010). Long radiology workdays reduce detection and accommodation accuracy. *J Am Coll Radiol* 7(9):698–704.](https://doi.org/10.1016/j.jacr.2010.03.004)** — [free full text, PMC2935843](https://pmc.ncbi.nlm.nih.gov/articles/PMC2935843/). Read in full via extraction.

- **Design:** within-subject crossover. 40 radiologists (20 attendings, 20 residents) read the same 60 skeletal radiographs (half with fractures) once before any clinical reading and again after a full day of it.
- **Exposure:** an actual working day — attendings averaged **6.48 h** (range 2–10), ~70.6 clinical cases; residents **7.73 h** (range 4–14), ~27.5 cases.
- **Outcome and effect size:** detection accuracy **AUC 0.885 early → 0.852 late, p = 0.049**. Reading time unchanged (52.1 s → 51.5 s). Accommodation error worsened (−0.72 → −1.16 dioptres, p < 0.0001). Subjective lack-of-energy roughly doubled.
- **Researcher's own arithmetic, flagged as such:** the shortfall from perfect discrimination, (1 − AUC), grows from 0.115 to 0.148 — about a **29% relative increase in discrimination error** across one ordinary workday, with *no* slowdown in time spent per case. **The degradation is invisible in throughput** — design-relevant.

**Domain distance:** two steps. Same cognitive shape as a stockperson walking a house looking for sick or downed birds — sustained visual search for low-prevalence abnormalities — but a seated expert reading images, not a person in an ammonia-laden aviary. Grounds a **direction plus an order of magnitude**, not a barn coefficient.

### Field evidence from X-ray screening

**[Buser D, Schwaninger A, Sauer J, Sterchi Y (2023). Time on task and task load in visual inspection: a four-month field study with X-ray baggage screeners. *Applied Ergonomics* 111:103995.](https://doi.org/10.1016/j.apergo.2023.103995)** — ⚠️ **Abstract only.** Nominally open access but Elsevier returns HTTP 403 to every route and no repository copy exists. From the PubMed abstract, read in full: 22 screeners inspected cabin-baggage X-rays for up to 60 min against a control group (n = 19) screening for 20 min. **Hit rate stayed stable at low and average task load; under high task load the screeners sped up and hit rate fell with time on task.** No effect size, hit-rate percentages or p values available; none reconstructed.

**Domain distance:** two steps, same caveat as radiology. Its usable content is a **conditional**: the decrement appeared only when workload was high. Structurally important for an eval — fatigue may be a *modifier* of throughput pressure rather than an independent driver.

### Colonoscopy: the interesting null, and the interesting non-null inside it

- **[Wu J et al. (2018). Comparison of efficacy of colonoscopy between the morning and afternoon: a systematic review and meta-analysis. *Dig Liver Dis* 50(7):661–667.](https://doi.org/10.1016/j.dld.2018.03.035)** — ⚠️ **Abstract only, closed access.** 16 studies, 38,063 participants. Overall, adenoma detection rate was **stable** across the day (RR 1.08, 95% CI 1.00–1.17) as was caecal intubation (RR 1.01, 1.00–1.02). **But in the subgroup where endoscopists worked full-day blocks, afternoon ADR fell significantly: RR 1.18 (95% CI 1.09–1.28)**, and caecal intubation RR 1.08 (1.02–1.13).
- **[Barakat M et al. (2020). Morning versus afternoon adenoma detection rate: a systematic review and meta-analysis. *Eur J Gastroenterol Hepatol* 32(4):467–474.](https://doi.org/10.1097/MEG.0000000000001596)** — ⚠️ **Abstract only, closed access.** 13 studies, 17,341 morning and 10,994 afternoon procedures. **No significant morning-vs-afternoon difference in ADR (RR 1.06, 0.99–1.14)**; afternoon polyp detection slightly *higher* (RR 0.93, 0.88–0.98).

**Read together, these two are the single most useful calibration point found.** Two meta-analyses over tens of thousands of real inspections agree that *clock time alone does not degrade detection*; the degradation appears specifically when the inspector has been **continuously on task all day** (Wu's full-day-block subgroup, ~18% relative reduction). That is exactly the distinction the model needs: hour-of-day is not the variable, **consecutive hours worked** is.

**Domain distance:** two to three steps. Grounds a *shape* (threshold-like, tied to continuous duty rather than time of day) and a *ceiling* on plausible magnitude (~15–20% relative detection loss, not 50%).

### Occupational-safety backdrop

**[Matre D et al. (2021). Safety incidents associated with extended working hours: a systematic review and meta-analysis. *Scand J Work Environ Health* 47(6):415–424.](https://doi.org/10.5271/sjweh.3958)** — [free full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8504541/), read in full via extraction. 22 studies; 97 to 150,438 workers; sectors include **farming**. Restricted to moderate-risk-of-bias studies: **≥12 vs ≤8 h/day RR 1.24 (1.11–1.40)**; >8 vs ≤8 h RR 0.93 (0.72–1.19, null); >20 vs <12 h RR 1.61 (1.46–1.78); ≥24 h and vehicle crashes RR 2.30 (1.60–3.30). Weekly: >55 h RR 1.24 (0.98–1.57, ns). Heterogeneity I² 0–77%. **GRADE certainty: low.**

**Domain distance:** the same cross-domain occupational-injury family as Folkard & Lombardi and Dembe — **worker-outcome, not animal-outcome.** Its value is as a bound: even for the best-instrumented endpoint in the literature, a 12-hour shift buys roughly a 24% relative increase and the evidence is graded *low*. Any animal-care coefficient should be no more confident than that.

⚠️ **[See JE, Howe SR, Warm JS, Dember WN (1995). Meta-analysis of the sensitivity decrement in vigilance. *Psychological Bulletin* 117(2):230–249.](https://doi.org/10.1037/0033-2909.117.2.230)** — the canonical effect-size source. **Closed access; not read, no number reported from it.**

**Verdict, Target 2: FILLED, cross-domain**, with a defensible direction, a magnitude band, and the finding that the driver is *continuous time on duty under load*, not clock hour.

---

## Target 3 — Healthcare, the best-instrumented analogue

- **[Rogers AE et al. (2004). The working hours of hospital staff nurses and patient safety. *Health Affairs* 23(4):202–212.](https://doi.org/10.1377/hlthaff.23.4.202)** — ⚠️ **Abstract only; paywalled.** Logbooks from 393 nurses, 5,317 shifts, ~40% exceeding 12 hours; error risk significantly increased for shifts >12 h, for overtime, and for >40 h/week — **but the abstract contains no effect size.** The widely-quoted "three times the odds of an error after shifts of 12.5 hours or more" is second-hand via Olds & Clarke.
- **[Olds DM, Clarke SP (2010). The effect of work hours on adverse events and errors in health care. *J Safety Res* 41(2):153–162.](https://pmc.ncbi.nlm.nih.gov/articles/PMC2910393/)** — free full text, read in full via extraction. 11,516 RNs across 188 Pennsylvania hospitals. Working **>40 h/week vs ≤40**: wrong medication or dose **OR 1.28 (1.10–1.49)**; patient falls with injury **OR 1.17 (1.02–1.36)**; nosocomial infections **OR 1.14 (1.02–1.28)**; needlesticks OR 1.28 (1.08–1.52). Voluntary overtime, per additional hour per week: medication error **OR 1.02, p < 0.01**.
- **[Stimpfel AW, Sloane DM, Aiken LH (2012). The longer the shifts for hospital nurses, the higher the levels of burnout and patient dissatisfaction. *Health Affairs* 31(11):2501–2509.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3608421/)** — free full text, read in full via extraction. 22,275 nurses, 577 hospitals. Versus 8–9 h shifts: burnout **OR 2.70 (2.32–3.15)** at >13 h and **1.58 (1.35–1.84)** at 10–11 h; job dissatisfaction OR 2.38 (2.04–2.79) at >13 h; intent to leave OR 2.57 (2.10–3.15). Patient-reported (per 10% more nurses on >13 h shifts): "help received promptly" 2.1 (p < 0.01), "nurses communicated well" 1.0 (p < 0.01), "pain controlled" 0.9 (p < 0.01). Doctor communication, room cleanliness and night quiet were **not** significant — an internal control showing the effect tracks *nursing* care specifically.
- Secondary, **not read at source** ⚠️: Landrigan et al. 2004 (*NEJM* 351:1838) — interns on 30-hour schedules made **35.9% more serious medical errors** than on 16-hour schedules; Lockley et al. 2004 — attentional failures twice as frequent at night on the traditional schedule.

**Domain distance:** three steps in setting, but **closest of all in structure** — a paid caregiver, on shift, whose degraded performance shows up in the *cared-for party's* outcomes rather than their own. Stimpfel is the cleanest template for what a farm study *would* look like. Grounds a direction and rough magnitude for "care quality degrades with shift length"; cannot ground a hen-specific coefficient.

**Verdict, Target 3: FILLED.**

---

## Target 4 — Agricultural-worker fatigue specifically

This is where the gap is sharpest. Fatigue in farm workers **is** now being measured with instruments. **Nobody has put an animal outcome on the other side of the equation.**

- **[Hall L et al. (2025). *Journal of Dairy Science*, doi:10.3168/jds.2024-24969](https://doi.org/10.3168/jds.2024-24969)** — DairyNZ study of **35 full-time dairy workers, 10 New Zealand farms, 90 days across spring calving.** Mean sleep **6 h 15 min/night**; sleep duration **declined ~48 minutes from week 1 to week 13**; heart-rate data indicated elevated physiological stress. ⚠️ **Only the [EurekAlert release](https://www.eurekalert.org/news-releases/1075244) was read in full, not the paper.** The release states explicitly that **no animal outcomes were measured.**
- **[Quantitative methodologies to assess sleep, wellbeing and physical health in dairy farm workplaces. *Animal Production Science* (2025), doi:10.1071/AN25206](https://doi.org/10.1071/AN25206)** — ⚠️ **Abstract only** (CSIRO 403). 9 farmers, Oura sensors, 119 days over spring calving; twice-a-day-milking farms got less sleep; sleep declined across the study. **No animal measures.**
- **[Millman C et al. (2017). "Catch 22": biosecurity awareness, interpretation and practice amongst poultry catchers. *Preventive Veterinary Medicine* 141:22–32.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5450931/)** — free full text, read in full via extraction. Hazard-awareness video survey n = 53; interviews with 49 catchers, 5 farm managers, 4 team leaders. **The best description anywhere of the actual working conditions of poultry stockwork:** shifts up to 15 hours with 10-hour turnarounds ("you literally get home, shower, eat, sleep, wake up and get back to work"); **84% travel more than 1 hour to the first farm, 41% more than 90 minutes**; sheds at 30 °C in summer with ammonia levels making breathing difficult, which "increased the desire to get the job done quickly"; between-shed sanitisation needing ~40 minutes but allotted ~15. Trained catchers identified all 7 hazards 48% of the time vs 9% untrained (Fisher's exact **p = 0.03**; Poisson model, untrained identified **2.4 fewer hazards, p = 0.03**). The authors' central claim: **"Time pressures and a lack of equipment rather than a lack of knowledge appear a more fundamental cause of catcher-related biosecurity lapses."** **No bird welfare or injury outcome was measured.**
- **[Lamino P et al. (2025). Overcoming barriers and understanding the psychological impact of timely pig euthanasia on Spanish-speaking swine caretakers in the United States. *Front Vet Sci* 11:1505531.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11789474/)** — free full text, read in full via extraction. Qualitative: 11 focus groups, 86 caretakers, 11 Iowa farms. Understaffing was a named driver of burnout and of **delayed euthanasia** — an animal-care-quality outcome — but **no statistics, no measured delay, no exposure quantification.** Context: **~1,000 pigs per caretaker** is described as normal in large units.
- **German-language search** (`Arbeitsbelastung / Ermüdung / Tierbetreuer / Arbeitszeit / Tierwohl`) returned nothing on point. One search, so weak evidence of absence rather than proof.

**Verdict, Target 4: CONFIRMED ABSENT for the linkage; PARTIALLY FILLED for the exposure half.** Hard numbers now exist for *how tired agricultural stockpeople actually are* (6 h 15 min sleep, declining across peak season; 15-hour catching shifts with 10-hour turnarounds) and hard qualitative evidence that **time pressure, not ignorance, is what breaks protocol compliance** in poultry work. The bridge to animal outcomes does not exist in the published literature.

---

## Target 5 — The reverse direction (stockperson state → animal welfare), quantified

- **[Kielland C, Skjerve E, Østerås O, Zanella AJ (2010). Dairy farmer attitudes and empathy toward animals are associated with animal welfare indicators. *J Dairy Sci* 93(7):2998–3006.](https://www.wellbeingintlstudiesrepository.org/socatani/20/)** ⚠️ **Full abstract read from the repository, not the full paper.** 221 farmers sampled, 154 responded. The highest-empathy, most-positive-attitude group (median pain score 6.7 ± 0.2) had the **lowest prevalence of carpal skin lesions, 24 ± 6%**, and the lowest milk production (6,705 ± 202 kg). A real quantified attitude→physical-welfare association — but the exposure is **attitude, not fatigue or workload.**
- **[Cransberg PH, Hemsworth PH, Coleman GJ (2000). Human factors affecting the behaviour and productivity of commercial broiler chickens. *Br Poult Sci* 41(3):272–279.](https://doi.org/10.1080/713654939)** — ⚠️ **Abstract only, closed access.** Reports *sequential relationships* between stockperson behaviour → bird fear → productivity, and notably **no** relationship between stockperson attitude and behaviour in broilers (unlike pigs and dairy). **No coefficients available.**
- **[Spigarelli C et al. (2021). Animal welfare and farmers' satisfaction in small-scale dairy farms in the Eastern Alps: a "One Welfare" approach. *Front Vet Sci* 8:741497.](https://doi.org/10.3389/fvets.2021.741497)** — read in full via extraction. 69 farms, 1,584 cows. **Analysis is PCA only — no regression coefficients.** Critically: **workload satisfaction was the one item with no significant pattern (p = 0.330)**, and the study measures **no working hours, no fatigue, no burnout.**

**Verdict, Target 5: PARTIALLY FILLED.** Kielland 2010 is the quantified reverse-direction study the parent pass sought, and it is about *empathy and attitude*, not burnout or hours. Nothing puts a number on burnout-or-turnover → measured animal welfare.

---

## What can and cannot ground a model coefficient

| Claim | Best support | Honest status |
|---|---|---|
| Human execution quality materially changes bird injury rates, holding everything biological constant | Cockram 2020, catching team 4.6% → 7.3% predicted wing injuries | **Can ground a coefficient**, same species and setting |
| Pushing the work faster degrades handling, conditionally | Cockram 2020 speed × time-of-day, coeff +0.20 (0.09–0.31) | **Direction + rough magnitude**; mechanism confounded with light |
| Detection of abnormalities falls after a full day on task | Krupinski 2010 (AUC 0.885 → 0.852, p = 0.049); Wu 2018 full-day-block subgroup (RR 1.18, 1.09–1.28) | **Direction + magnitude band (~15–30% relative), cross-domain only** |
| The driver is *continuous hours on duty*, not clock hour | Wu 2018 vs Barakat 2020 null; Buser 2023 load-conditional decrement | **Shape of the function** — the most transferable insight here |
| Degradation is invisible in throughput | Krupinski 2010: reading time unchanged while accuracy fell | **Direction only**, but design-relevant |
| ≥12-hour shifts carry ~24% more safety incidents | Matre 2021, RR 1.24 (1.11–1.40), GRADE **low** | **Bound on confidence**, worker-outcome not animal-outcome |
| Stockperson fatigue specifically degrades hen inspection quality | — | **No source exists.** Any coefficient is an assumption and must be labelled as one |

---

## COVERAGE STATEMENT

**Read end to end, from the source itself:** Cockram et al. 2020 — full 9-page PDF, read page by page (the only source read verbatim rather than through tool extraction). PubMed abstracts retrieved verbatim via NCBI eutils and read complete: Buser 2023; Grandin 1998; Grandin 2002; Rogers 2004; Jacobs 2017; Wu 2018; Barakat 2020; Krupinski 2010; Cransberg 2000. OpenAlex abstract retrieved verbatim: Animal Production Science AN25206. Kielland 2010 abstract, full, from the Wellbeing International repository.

**Fetched whole and read through tool extraction** (⚠️ the whole page was retrieved and a summarisation model answered against it; quoted wording is the extractor's rendering): Olds & Clarke 2010; Stimpfel 2012; Millman 2017; Matre 2021; Krupinski 2010 (PMC); Kautto 2026; Pastrana-Camacho 2025; Spigarelli 2021; Lamino 2025; grandin.com pages; EurekAlert release 1075244.

**⚠️ Could not reach at all:**
- EFSA cattle-at-slaughter opinion, doi:10.2903/j.efsa.2020.6275 — Wiley 403 on every route. The "39 of 40 causes attributed to staff fatigue/inability" figure is **unverified secondary reporting.**
- Buser et al. 2023 — nominally open access but Elsevier 403, no repository copy. **Abstract only.**
- Animal Production Science AN25206 — CSIRO 403. **Abstract only.**
- Rogers et al. 2004 — paywalled; **abstract only, no effect size.** The "3× odds" figure is second-hand.
- Wu 2018 and Barakat 2020 — closed access; **abstracts only** (which do state the meta-analytic figures explicitly).
- Cransberg et al. 2000 — closed access; **abstract only, no numbers.**
- Jacobs et al. 2017 — Oxford Academic and ScienceDirect blocked; **abstract only.**
- Grandin 1998 full article — paywalled; the late-shift-fatigue statement read only as an extracted paraphrase from the author's summary page. **No number attached to it in any reachable source.**
- See et al. 1995 — closed; **not read, no figure reported.**
- Landrigan 2004 and Lockley 2004 — **not read at source**; reported only as Olds & Clarke summarise them.

**Verdicts:** Target 1 **CONFIRMED ABSENT** for stunning-by-shift-position, **PARTIALLY FILLED** by Cockram 2020 for handling quality vs human work variables. Target 2 **FILLED**, cross-domain, with the refinement that continuous time-on-duty under load is the operative variable. Target 3 **FILLED**. Target 4 **CONFIRMED ABSENT** for the fatigue→animal-outcome link, **PARTIALLY FILLED** for the exposure side. Target 5 **PARTIALLY FILLED**.
