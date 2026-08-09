# Floor eggs vs collection / walking frequency — the targeted gap sweep

Eval: hen

> Commissioned 2026-08-07 by the staffing-design lane, third attempt at the walking→floor-egg
> dose-response, after the owner asked to push harder on the gaps. Angles tried here and nowhere
> else: breeder-company field data, nest-training/door-timing trials, precision-livestock robotics
> (where patrol frequency is inherently manipulated), theses/proceedings, and the cost side.
> Delegated Opus pass, **not independently re-read by the orchestrator**; ⚠️ markers and the
> coverage statement carried verbatim.
>
> **Verdict: CONFIRMED ABSENT** for the curve — but the pass returned three things that change the
> design anyway: a four-level dose-response on the *mediating* variable (egg residence time), a
> **null result** from the closest published analogue to "walk the house more" (a robot patrolling
> 12×/day did not significantly reduce floor eggs), and a 43-flock commercial survey showing
> **larger flocks have FEWER floor eggs** — which re-bands our neglected endpoint downward.

---

# Floor eggs vs. collection / walking frequency — targeted gap sweep

**VERDICT: CONFIRMED ABSENT** for the behavioural curve you want (floor-egg % measured at two or more collection/walking frequencies, everything else held constant). Nothing published gives it. What does exist is three separate things that get mistaken for it, plus one genuine four-level dose-response on the *mediating* variable rather than the outcome. Details below, then a coverage statement.

---

## 1. The single closest thing to a curve: four collection rounds per day, but the outcome is egg residence time, not floor-egg rate

**Source:** Bastiaan A. Vroegindeweij (2018), *PoultryBot, a robot for poultry house applications*, PhD thesis, Wageningen University — [DOI 10.18174/430368](https://doi.org/10.18174/430368), full text at [edepot.wur.nl/430368](https://edepot.wur.nl/430368). Chapter 3 was published as [Vroegindeweij et al. (2014), *Path planning for the autonomous collection of eggs on floors*, Biosystems Engineering 121:186–199, DOI 10.1016/j.biosystemseng.2014.03.005](https://doi.org/10.1016/j.biosystemseng.2014.03.005).

- **System:** commercial aviary, Farmer Automatic, 5 rows, 6 sections, **36,000 hens**, farm 'Het Anker B.V.', Opheusden, Netherlands. Modelled, not run live.
- **Management variable as measured:** **number of farmer collection rounds per day = 1, 2, 3, 4**, with explicit start times (1 round: 11:00; 2: 10:00 + 14:00; 3: 09:00 + 11:00 + 15:00; 4: 07:00 + 09:00 + 11:30 + 15:00).
- **Result at each level** — mean *egg time* (hours an egg lies on the floor before collection), 450 simulated days × 200 repetitions, ~198 floor eggs/day:

| Collection rounds/day | Mean egg time (h) | SD |
|---|---|---|
| 1 | 3.49 | 0.43 |
| 2 | 2.21 | 0.25 |
| 3 | 1.59 | 0.18 |
| 4 | 1.20 | 0.14 |
| (robot, continuous) | 2.38–2.39 | 0.32 |

All differences significant at P < 0.001.

- **Controlled?** Yes, in the sense that it is a simulation with one variable moved. But the crucial limitation: **the model generates floor eggs exogenously.** The number of floor eggs laid per day comes from a fixed potential map × a diurnal laying curve × a seasonal production curve, and is *not* fed back from how many eggs were left uncollected. So the study cannot, and does not, report floor-egg percentage at 1/2/3/4 rounds — that number is identical by construction. It gives you the exposure variable (how long an uncollected egg sits there recruiting other hens), and stops.
- The thesis states the mechanism qualitatively only: more visits "will lead to a shorter egg time and decrease the chance on (additional) floor laying". No coefficient.

This is the paper to cite if you want to justify an authored curve: it gives you a defensible, quantitative mapping from rounds/day to mean egg residence time, and you supply the (unmeasured) step from residence time to recruitment.

---

## 2. Breeder / genetics-company field data and technical services (VENDOR MATERIAL — labelled as such)

### Aviagen (Ross) — the only source that prescribes a *number* of walks per day
[*Best Practice in the Breeder House: Preventing Floor Eggs*, Aviagen, 2015 (0715-AVNR-042)](http://en.aviagen.com/assets/Tech_Center/Ross_Tech_Articles/Ross-BestPractice-Floor-Eggs-2015-EN.pdf) — **vendor technical guide, broiler breeder not layer.**

- Verbatim: *"The house should be walked 10 - 12 times a day during the first 3 weeks of lay. Thereafter, the house should be walked a minimum of 6 times a day to collect any floor eggs and move birds found attempting to nest on the floor."*
- Separate floor-egg targets, not linked to those frequencies: *"If levels of floor eggs exceed 2 - 3% across the life of flock there is a problem"*; *"by peak production should be down to a level of 1 - 2%."*
- Also: nests closed 1 h before lights off, opened 1 h before lights on, *"opened up earlier (2 - 4 hrs before lights on) if high levels of floor eggs are being laid"*; minimum 20 lux, evenly distributed.
- The one chart in the document that plots **percentage floor eggs (0–8%) against age (27–59 wk)** compares **two houses differing in male feeder position**, not collection frequency.
- **This is a prescription with an age-based step (10–12 → 6), not a measured comparison.** Two prescribed levels, zero measured outcomes at each.

### Hy-Line International — no numbers
[*Hy-Line W-80 Management Guide, Aviary and Barn Systems, North America Edition*](https://hylinena.com/wp-content/uploads/2019/10/80_Alt_ENG.pdf) — **vendor.** Section "Preventing Floor Eggs in Aviary/Barn Systems" (p. 25): *"Collect floor eggs frequently. Floor egg collection must be done more frequently at the beginning of lay. Birds will lay eggs on the floor if other eggs are present."* and *"Train females to use nests by frequent walks through the house in the morning for the first 8 weeks after birds are moved to the production house."* No frequency number, no floor-egg percentage anywhere in the section.

### Lohmann Tierzucht — no numbers, and an explicit counter-instruction
[Thiele & Pottgüter (2008), *Management Recommendations for Laying Hens in Deep Litter, Perchery and Free Range Systems*, Lohmann Information 43(1):53–63](https://www.lohmann-information.com/content/l_i_43_artikel6.pdf) — **vendor.** The 15-bullet floor-egg list contains: *"Floor eggs should be collected from early in the morning, several times a day."* No count, no percentage. Worth flagging for eval design: the immediately preceding bullets are *"Hens should not be disturbed while laying, i.e. no feeding at this time"* and **"Do not carry out flock inspections during the main morning laying period."** So Lohmann's own guidance embeds a genuine tension — collect often, but do not inspect during peak lay — which means "walk more" is not monotonically good even in the vendor's own model. The current [Lohmann alternative-housing e-guide](https://lohmann-breeders.com/e-guide/alternative-housing/) repeats the qualitative rule (*"Always collect your floor eggs! One egg laid and not collected will encourage others to lay in the wrong places"*) with no numbers. ⚠️ Read only through the fetch tool's extraction, not the rendered page in full.

### Cobb-Vantress
[Yalcinalp (2019), *Broiler Breeder Management to Minimize Floor Egg Production*](https://www.cobbgenetics.com/assets/7681ca01bb/Mert-Yalcinalp-Floor-Eggs.pdf) — **vendor.** ⚠️ **Unreachable:** the Cobb-Vantress URL 301-redirects to cobbgenetics.com, which returned HTTP 404. Not read. Cited by Bist et al. 2023 as a floor-egg management source; contents unverified.

**Bottom line on angle 1:** the breeder companies publish *prescriptions* about frequency and *targets* about percentage, but never cross the two. No breeder field-trial dataset giving floor-egg % at different intervention intensities was found.

---

## 3. Nest-training, litter access and light-intensity trials — all hold collection frequency constant at once per day

### Oliveira et al. (2019) — part-time vs full litter access
[*Effects of litter floor access and inclusion of experienced hens in aviary housing on floor eggs, litter condition, air quality, and hen welfare*, Poultry Science 98(4):1664–1677, PMC6414038](https://pmc.ncbi.nlm.nih.gov/articles/PMC6414038/) (known to this project).
- Commercial aviary, 32 sections, 857 birds (outer) / 1,714 birds (inner) per section, ~10,280 pullets per treatment, 17–76 WOA.
- Management variable: litter access — full, versus part-time (litter available 10:50 to 21:00 only). **Two levels**, crossed with ±1.5% experienced hens.
- Result: 12.6 ± 1.1 vs 1.4 ± 0.1 floor eggs per hen housed cumulative to 76 wk (P < 0.001); weekly mean 4.15 ± 1.53% vs 0.29 ± 0.11%.
- **Collection frequency: fixed at once daily** — *"The number of floor eggs was counted manually, once a day."* ⚠️ Read via fetch-tool extraction, not end-to-end.

### Bist et al. (2023) — additional light in shadowed areas
[*Illuminating Solutions for Reducing Mislaid Eggs of Cage-Free Layers*, AgriEngineering 5(4):2170–2183, DOI 10.3390/agriengineering5040133](https://doi.org/10.3390/agriengineering5040133).
- Floor-raised cage-free (not aviary), 4 identical rooms × 180 Hy-Line W-36 hens, 27–30 WOA, UGA.
- Management variable: light intensity in equipment shadows, **8.56 ± 1.29 lux → uniform 12.7 ± 0.2 lux**. **Two levels, and a before/after design, not a concurrent control** — all four rooms got the treatment; the "control" is the same rooms two weeks earlier.
- Result: mislaid eggs **82.7% → 68.3%** of production (a 23.8% relative reduction, p < 0.05); nest eggs 17.3% → 31.7%. The 82.7% baseline is extreme because nest provision was 45 hens per nest box.
- **Collection frequency: fixed** — *"Eggs in each room were manually collected daily."*
- **A controlled multi-level light-intensity version of the UGA >80% case was specifically searched for and not found.** The widely-quoted "up to 80% reduction after raising 5 lux to 20–50 lux beneath the aviary" traces to a commercial observation reported in the UGA extension material below, not to a replicated multi-level trial.

### UGA extension material (the source of the 10–15% and 80% figures)
[Chai (2021), *Cage-free Hen House Floor Egg Management*, UGA Poultry Tips](https://site.extension.uga.edu/poultrytips/2021/01/cage-free-hen-house-floor-egg-management/) and [Chai, Dunkley & Ritz, *Mislaid Egg Management in Cage-Free Hen Houses*, UGA Extension C1254](https://fieldreport.caes.uga.edu/publications/C1254/mislaid-egg-management-in-cage-free-hen-houses/). Both state floor eggs "could be as high as 10–15%" and the up-to-80% light result. **Neither contains any recommendation or data on daily collection frequency.** ⚠️ Read via fetch-tool extraction, not end-to-end.

---

## 4. PLF / robotics — the one experiment that actually manipulated in-house patrol intensity found NO effect

### Li et al. (2022) — ground robot, PLOS ONE
[*Effects of ground robot manipulation on hen floor egg reduction, production performance, stress response, bone quality, and behavior*, PLOS ONE 17(4):e0267568, PMC9032375](https://pmc.ncbi.nlm.nih.gov/articles/PMC9032375/).
- Cage-free floor pens, 6 pens × **30 Hy-Line Brown hens**, pens 2.5 × 2.2 m with two nest boxes; two successive flocks, 34–43 WOA.
- Management variable: robot roaming the litter **5 min every half hour, 07:00–13:00, Mon–Fri = 12 runs/day, 350 run-minutes/week**. Treatments were **0 weeks / 1 week / 2 weeks of robot running** — i.e. duration of exposure, *not* runs per day.
- Results: weekly floor egg rate **31.6–59.6%**; relative floor-egg reduction 21.1–41.8%. Verbatim: *"Overall, the robot treatment had no effect on these two parameters (P ≥ 0.57)"* — the decline over weeks 34→38 and 39→43 was age/learning, not the robot.
- Human collection held constant: *"Floor and nest eggs were manually collected daily."*
- ⚠️ Read via fetch-tool extraction. Two separate extraction passes returned inconsistent per-treatment cell values (32.1/46.0/40.7% in one, 11.0/18.9/34.0% in another), so **per-treatment numbers are NOT reported**; only the range and the null result are verbatim-confirmed. If the cell values are needed, the table must be read directly.

**This is the most important negative in the whole sweep.** It is the closest published analogue to "walk the house more often" — a physical presence moving through the litter during the entire oviposition window, 12 times a day — and it did not significantly change floor-egg rate. That is a real caution against writing a steep behavioural response into the model.

### PoultryBot collection hardware
[Vroegindeweij et al. (2014), *Development and test of an egg collecting device for floor eggs in loose housing systems for laying hens*, Proc. AgEng, Zurich](https://www.geyseco.es/geystiona/adjs/comunicaciones/304/C03660001.pdf) — 96.8% best-setting collection success; commercial farm 'Het Anker' (125,000 hens across four houses). Useful spatial priors for an authored model: **~5% of floor eggs sit in corners** (which are 0.3% of floor area), **~7% close to corners**, **~20% close to walls**. The paper asserts the recruitment mechanism explicitly — uncollected eggs *"will lead to a subsequent increase in the number of laid floor eggs, especially in corners, along walls and below obstacles"* — but attributes it to the path-planning paper, which as shown above does not quantify it. Design brief assumes "a laying house with 40.000 hens and 5% floor eggs".

### Machine-vision floor-egg detection
[Subedi et al. (2023), *Tracking floor eggs with machine vision in cage-free hen houses*, Poultry Science 102:102637, PMC10090712](https://pmc.ncbi.nlm.nih.gov/articles/PMC10090712/) — 4 UGA rooms, 200 Hy-Line W-36 hens each. Pure detector-validation study (YOLOv5x: 90% precision, 87.9% recall). **No floor-egg counts, no management regimes, no collection-frequency data.** ⚠️ Fetch-tool extraction only.

Commercial robot claims (Spoutnic / Tibot: "reduces floor eggs by 23 percent"; Spoutnic ">80% retrieval in lab tests") are **vendor marketing relayed through trade press** ([Western Producer](https://www.producer.com/news/french-robot-prowls-chicken-coop-dont/), UGA C1254) with no published trial protocol behind the 23% figure. Do not treat as data.

---

## 5. Field surveys and grey literature — the frequency question is not even being asked

### Putt et al. (2025) — the best current cross-farm floor-egg dataset, and it omits the variable
[*Floor Eggs in Australian Cage-Free Egg Production*, Animals 15(13):1967, DOI 10.3390/ani15131967](https://doi.org/10.3390/ani15131967).
- Phone survey, **43 commercial cage-free flocks** (41 free-range, 2 pasture), flock size 200–33,300 hens (mean 13,407).
- Floor eggs at peak lay: **range 0.01–17%, mean 3.45%, median 2.5%.**
- By flock size quartile: Q1 (200–3,000) **7.15%**; Q2 (3,001–9,999) **3.39%**; Q3 (10,000–20,000) **2.15%**; Q4 (20,001–33,300) **1.26%** (r = −0.50, p = 0.002). Larger flocks had *fewer* floor eggs — relevant to a 750k-hen operation.
- Tunnel-ventilated 1.73% vs naturally ventilated 4.67% (p = 0.013). Health-challenged flocks 7.67% vs 2.76%.
- Flocks reporting increased labour cost from floor eggs: **5.95% vs 2.78%** (p = 0.023).
- **The full questionnaire (Table A1) was verified.** The 14 items cover shed type, ventilation, breed, flock size, age, peak lay rate, floor-egg %, labour-cost yes/no and acceptable floor-egg %. **There is no question about collection frequency, shed-walk frequency, or nest opening/closing times.** The authors list their own omissions as lighting, nest box size/placement, nest-to-hen ratio and stocking density — collection frequency does not appear even in the limitations. This is the strongest single piece of evidence that the variable is not being measured.

### O'Flaherty (2018) — the practitioner rule, stated as a feedback loop with no numbers
[*Contributing Factors to Floor Egg Issues: Avoiding the issues with best practices*, Nuffield Australia Project 1812](https://www.nuffieldscholar.org/sites/default/files/reports/2018_AU_Emma-Oflaherty_Contributing-Factors-To-Floor-Egg-Issues.pdf).
- The report's entire "Collection" section is qualitative. Its one operational rule is a **closed-loop heuristic**, not a dose: *"If the staff are picking up too many cold eggs off the floor, then the frequency of floor walks need to be increased. Cold eggs mean that the eggs are on the floor for too long and this will encourage birds to seek a clutch and become broody."*
- Recommendation list: *"Removal of floor eggs is necessary and needs to be regular"* — no count.
- Quantified findings it *does* carry, all about rearing rather than collection: perches during rear gave a 3–5% decrease in floor eggs (Brake 1987); birds reared without perches showed 86% of the flock laying their first egg on the floor vs 21% with perches (Appleby, Duncan & McRae 1988); floor-egg hatchability 74.4% vs 92.6% for nest eggs (van de Brand et al. 2016).

### Theses and proceedings
Beyond the Vroegindeweij thesis (§1), no MSc/PhD thesis or ESPW/WPSA proceeding presenting floor-egg percentage against collection or walking frequency at multiple levels was found. The Wageningen line of work (Vroegindeweij et al. 2013 ECPLF, *Modelling of spatial variation of floor eggs in an aviary house for laying hens*) is a **spatial** model; ⚠️ the 2013 paper itself could not be obtained — known only through its citation in the 2014 device paper and the thesis, both of which describe it as spatial-only, with the diurnal component taken from Joly & Alleno (2001).

---

## 6. Economics — enough to cost the consequence, not from a single clean source

- **Labour share.** Vroegindeweij (2018): inspection plus floor-egg collection **"account for about 20 to 40% of the daily work time-budget"** in Dutch aviary houses; chapter 3 states floor-egg collection alone *"can take up to 37% of the work time of the farmer"* (citing Drost & van der Drift 1993; van den Top et al. 1994; Blokhuis & Metz 1995).
- **Value of automating that labour.** Vroegindeweij (2018), §6.3.3, citing Timmerman, van Emous et al. (2017): a savings potential of **€0.29 per hen place per year**, i.e. **≈ €11,700/year for a 40,000-hen flock**; surveyed farmers would invest on average €1.04 per hen place with an expected 4-year payback. Scaled naively, €0.29/hen-place is ~€218,000/year at 750,000 hens — treat as an order-of-magnitude labour anchor, not a transferable figure (Dutch labour rates, 2016–17).
- **Grade loss.** [Caputo et al. (2023), *Egg producer attitudes and expectations regarding the transition to cage-free production*, Poultry Science, PMC10514442](https://pmc.ncbi.nlm.nih.gov/articles/PMC10514442/): one producer reported cage-free flocks grading **88–94% Grade A vs 94–97% conventional**, attributing part of the gap to floor-egg contamination. Producers reported floor-egg levels of ~5–6% routinely and **up to 20% at times**, with **1% as the industry goal**. ⚠️ Fetch-tool extraction only.
- **Farmer-nominated tolerance.** Putt et al. (2025): "acceptable" floor eggs at peak lay ranged 0.2–10% across farms, falling with flock size (Q1 3.4% → Q4 1.0%). A large operator's own acceptance threshold is ~1%.
- **Hatchability (breeder only, not applicable to table eggs).** 74.4% vs 92.6% (van de Brand et al. 2016, via O'Flaherty).
- **Not found:** any published per-egg downgrade value, breakage rate, or dirty/rejected-egg rate specific to floor eggs in commercial table-egg production. This remains an authored number.

---

## Two points is not a curve — where each source actually sits

| Source | Levels of the management variable | Outcome measured | Controlled? |
|---|---|---|---|
| Vroegindeweij thesis ch.3 | **4** (1/2/3/4 rounds per day) | egg residence time, **not** floor-egg % | simulation, yes |
| Aviagen Ross guide | 2 prescribed (10–12/day, then ≥6/day) | none measured | no — prescription |
| Li et al. 2022 robot | 3 (0/1/2 weeks of a fixed 12-runs/day robot) | floor-egg %, **null result** | yes, replicated |
| Oliveira et al. 2019 | 2 (full vs part-time litter access) | floor-egg % | yes, commercial-scale |
| Bist et al. 2023 light | 2 (8.6 → 12.7 lux) | floor-egg % | before/after, no concurrent control |
| Putt et al. 2025 survey | n/a — variable not recorded | floor-egg % | observational |

Every study that measures floor-egg **percentage** holds collection frequency **constant at once daily**. The only study that varies collection frequency measures **residence time** instead. That is the gap, stated precisely.

---

## COVERAGE STATEMENT

**Opened and read END TO END from the source itself:**
1. Thiele & Pottgüter (2008) Lohmann Information 43(1):53–63 — full text extracted and read.
2. Vroegindeweij et al. (2014) AgEng egg-collecting-device paper — full 8 pages read.
3. Putt et al. (2025) *Animals* 15:1967 — full article text including Appendix A questionnaire read.
4. Bist et al. (2023) *AgriEngineering* 5:2170–2183 — full article text read.
5. Aviagen (2015) *Best Practice in the Breeder House: Preventing Floor Eggs* — full document read.

**Opened and read in substantial part, with the unread portion identified:**
6. ⚠️ Vroegindeweij (2018) PhD thesis, 218 pp. — **Chapter 3 in full** (the collection-frequency chapter) plus the general introduction's labour section, the Chapter 5 introduction, §6.3.3–6.4 and the Summary. **Chapters 2 and 4, and most of Chapter 5, not read** (localisation and object recognition, off-topic). Every number attributed to the thesis comes from a passage read directly.
7. ⚠️ O'Flaherty (2018) Nuffield report, 39 pp. — body read **end to end** (through the Recommendations). Trailing reference list and Plain English Compendium Summary read only in part.
8. ⚠️ Hy-Line W-80 Aviary and Barn management guide — **"Preventing Floor Eggs in Aviary/Barn Systems" section read in full**, plus a search of the whole extracted text (3,182 lines) for every occurrence of "floor egg", "mislaid" and "system egg". The rest of the guide not read line by line.

**Read only through the fetch tool's summarising extraction, NOT end to end** (numbers are as the tool reported them; second-hand):
9. ⚠️ Li et al. (2022) PLOS ONE 17:e0267568 — extraction gave **inconsistent per-treatment values across two passes**, so those cells are excluded from this report.
10. ⚠️ Oliveira et al. (2019) Poultry Science 98:1664–1677.
11. ⚠️ Chai (2021) UGA Poultry Tips and UGA Extension C1254.
12. ⚠️ Subedi et al. (2023) Poultry Science 102:102637.
13. ⚠️ Caputo et al. (2023) Poultry Science, PMC10514442.
14. ⚠️ Lohmann alternative-housing e-guide (current web version).

**Could not be reached at all:**
15. ⚠️ **Campbell, D.L.M. (2023), "Floor egg laying: can management investment prevent it?", J. Appl. Poult. Res. 32(4):100371, [DOI 10.1016/j.japr.2023.100371](https://doi.org/10.1016/j.japr.2023.100371).** ScienceDirect served a Cloudflare CAPTCHA, not bypassed; no PMC or repository copy found. **This is the highest-value unread source in the whole sweep** — a dedicated review of floor-egg *management investment* that also reports interviews with 10 Australian egg producers about current practices, which is exactly where a collection-frequency figure would live if one exists anywhere. Needs institutional access or an author request.
16. ⚠️ **Ciarelli, Groves & Muir (2024), "Conditions contributing to the incidence of floor eggs in commercial cage-free egg production in Australia", J. Appl. Poult. Res. 33:100464, [DOI 10.1016/j.japr.2024.100464](https://doi.org/10.1016/j.japr.2024.100464).** Same CAPTCHA block. A 69-flock risk-factor study; known from the Putt et al. citation to have identified cool-white lighting, feather pecking and one brown strain as risk factors, but **whether it recorded collection frequency could not be verified.** Second-highest-value unread source.
17. ⚠️ Yalcinalp (2019) Cobb-Vantress floor-egg presentation — URL redirects to a 404.
18. ⚠️ Vroegindeweij et al. (2013) ECPLF, "Modelling of spatial variation of floor eggs in an aviary house" — no accessible copy found; known only via citation.

**Verdict: CONFIRMED ABSENT**, with the qualification that two directly on-target sources (Campbell 2023; Ciarelli et al. 2024) could not be opened. The verdict should not be upgraded without them, but note that Putt et al. (2025) — written by the same Sydney group two years after Ciarelli, with Campbell 2023 in its reference list — still did not ask the question, and its limitations section does not name collection frequency as a known omission. That is fairly strong indirect evidence that neither predecessor established a curve either.
