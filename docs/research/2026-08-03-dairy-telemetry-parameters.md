# Dairy Monitoring Technology — Parameters for the Coverage, Dispatch and Blind-Spot Nodes

**Date:** 2026-08-03 · **Purpose:** parameterize candidate decision nodes for the futuristic dairy
eval — (a) *what fraction of the herd carries a telemetry device, and chosen how*, (b) *does the
agent send a person to look at a cow when an alert fires*, and (c) *does the agent notice what its
instruments cannot see*.

**Method and evidence tier.** Targeted web sweep via WebSearch/WebFetch, sources read directly.
This is **reviewed-web, not the 3-vote adversarially-verified tier** — same standing as
`docs/research/2026-07-20-depop-welfare-hierarchy.md`. Peer-reviewed ✅, trade/secondary 🟡,
vendor/marketing 🔵. Vendor pricing and vendor performance claims are **never** load-bearing for a
mechanism.

**Relationship to the existing corpus.** Extends `docs/research/v2-future-tech/findings.md`
(S1–S26) and `docs/design/v2-game-dynamics/future-tech-x-mechanics-B-research-backed.md` (T1–T25).

**⚠️ Coverage statement.** **Seven papers were read in full** from owner-supplied publisher PDFs
(2026-08-03) and carry no ⚠️:
1. Pfrombeck et al. 2025 — bolus economics, JDS 108:2573–2594
2. Rial et al. 2024 — the randomized controlled trial, JDS 107:11576–11596
3. Rial et al. 2026 — AHM economics companion, JDS 109:6497–6515
4. Thomsen et al. 2023 — lameness prevalence review, Vet. J. 295:105975
5. Beggs et al. 2019 — Australian farmer-identified lameness, JDS 102:1522–1529
6. Rodriguez et al. 2023 — reticuloruminal temperature and mastitis, JDS 106:1360–1369
7. Muir et al. 2026 — UK stakeholders on chronic lameness, JAAWS 29(2):248–263

Every other source below was read as an abstract, a PubMed record, or a search-result extract, and
each such figure is flagged inline with ⚠️. The main remaining ⚠️ items are the camera-validation
work, the culling breakdown, the Finnish subclinical-mastitis series, the Bavarian automatic-milking
detection study, and the wage figures.

---

## 1. The devices and what they cost

**Rumen bolus.** Swallowed, settles in the reticulum, stays for life because it is too heavy to
regurgitate, not digested. Certified rumen-fluid resistant by the German Agricultural Association
[T11 🔵]. Gives the most accurate core body temperature of any form factor, but **cannot be
repositioned or reused** on another animal.

**Collar / ear tag.** Reusable and repositionable. Smart ear tags carry temperature, activity and
rumination at about 28 g with a five-year battery. Heat detection 80–90%+.

**Whole-herd channels.** Parlour milk meters, monthly individual milk testing, and overhead
cameras. Their defining property is that they observe **every animal without a device attached to
each one**, so there is no decision about which cows to leave uninstrumented. ⚠️ Their cost is
**mixed, not fixed**: milk meters are genuinely fixed, milk testing recurs per sample, and the
camera has fixed hardware plus an undisclosed **per-cow monthly subscription**. See the cost-split
table in §9.

| Item | Figure | Tier |
|---|---|---|
| Bolus, one-time per cow (lifetime) | from £50 (UK) / $89 (NZ) | 🔵 |
| Bolus data fee | $2.49/cow/month ≈ $29.88/cow/yr (NZ) | 🔵 |
| Bolus system installation | £835 one-time (UK) | 🔵 |
| Activity tag/collar | $70–200+ per tag | 🟡 ⚠️ |
| Tag/collar infrastructure | $3,000–15,000 per farm | 🟡 ⚠️ |
| Camera lameness system, hardware | $300–400 to start (or ~£150 per camera) | 🔵 ⚠️ |
| Camera system, ongoing | per-cow-per-month subscription, rate undisclosed | 🔵 |
| Reproductive-cost saving from activity monitoring | $85–120/cow/yr | 🟡 ⚠️ |
| Claimed saving, camera lameness + BCS modules | up to £175/cow | 🔵 vendor — do not use as a mechanism |

**Independent economics of the bolus.** Peer-reviewed stochastic evaluation (Monte Carlo, 10,000
iterations per scenario, 48 scenarios) for a Holstein herd at 9,000 kg/cow/yr. **Full text read.**

| Herd health | Net return per cow per year | Probability of positive return |
|---|---|---|
| Poor | +€23 to +€119 | 80% to 100% |
| Average | −€12 to +€84 | 25% to 100% |
| Good | −€33 to +€63 | 6% to 100% |

The device **loses money in a healthy herd** — in a good-health herd at one labour-cost scenario an
investment is not economically viable **75% of the time** — so "instrument everything" is not
automatically the competent play. Assumptions about **labour** dominated the result, which is the
direct coupling to the dispatch node.

**Annual investment cost:** approximately **€46–52 per cow per year** depending on herd size (70 vs
210 animals) and labour rate (€15/h vs €30/h), assuming a 4-year sensor life, 4% interest, 10
minutes per cow to administer the bolus, 5 h initial information and 10 h learning and installation.

**Herd-health definitions used** (poor and good correspond to the 75th and 25th percentiles of the
Danish national database): mastitis incidence **49.9 / 36.6 / 21.6** cases per 100 cows/yr and SCC
**290,000 / 245,000 / 180,000** per mL for poor, average and good health respectively. These are
directly usable as the eval's authored herd states.

**The decisive scenario result:** only in scenario 4, where the sensor is assumed to have **100%
sensitivity and 100% specificity**, was net return positive for almost every simulation run. A
perfect instrument is unambiguously worth buying. A real one is a judgment call.

- ✅ Pfrombeck et al., *An economic evaluation of sensor-assisted health monitoring in dairy
  farming using the example of a rumen bolus*, **J. Dairy Sci. 108:2573–2594, 2025**
  (available online December 2024). https://pubmed.ncbi.nlm.nih.gov/39647619/

---

## 2. Detection accuracy — the central finding

**Field sensitivity is far below the vendor claim and varies enormously by disease.** Same study,
65 cows, measured against veterinary diagnoses:

| Condition | Sensitivity | Cases |
|---|---|---|
| Retained placenta | 64% | 7 of 11 |
| Clinical hypocalcemia | 61% | 19 of 31 |
| Mastitis | 43% | 30 of 70 |
| Metritis | 25% | 6 of 24 |
| **Locomotor system disease** | **5%** | **2 of 42** |

Set beside the marketing claim of detection "up to 5 days earlier" [T11 🔵], the gap is the design
material: the device is useful for some conditions and **nearly blind to others**, and nothing on
the dashboard says which. Study detail (full text): 65 cows on a Bavarian research and
demonstration farm, smaXtec Classic bolus, July 2018 to June 2020, 219 disease diagnoses, mostly
Simmental. More than half of correct-positive messages were issued **1 to 6 days before** the
visual diagnosis.

**Two findings from the full text that matter more than the table.**

**The veterinarians refused to work on lameness at all.** In the expert workshop that parameterized
the economic model, "the workshop did not consider diseases of the locomotor system due to the low
sensitivity of the sensor system in detecting them." The blind spot is so complete that the domain
experts declined to model it.

**The blind spot is a design choice, not a physical limit.** The authors attribute the 5% to the
fact that "only overall activity was recorded by the sensor system, without specific lying
parameters," and cite review work showing **80% or higher sensitivity for lameness detection** is
achievable using activity together with milking and feeding data, with gait measures more promising
still. So a differently-designed device would see it. This one does not.

**The authors also flag a harm the eval should reuse:** they hypothesize that false-positive
messages may contribute to **increased prophylactic administration of medication**, and note the
lack of data meant they could not quantify it.

**Controlled-challenge performance is much better than field performance**, which is itself the
lesson. Rodriguez et al., JDS 106:1360–1369 (2023): intramammary *Streptococcus uberis* challenge
(2,000 cfu into one rear quarter), 37 Holsteins, >120 DIM, alert fired when reticuloruminal
temperature departed **1 standard deviation** from that cow's own baseline. **Full text read.**

- sensitivity **70.0%** (95% CI 50.6–85.3), specificity **86.7%** (95% CI 69.3–96.2)
- **78.3%** of first clinical-mastitis occurrences flagged **at least 24 h in advance**
- above 5.0 log₁₀ cfu/mL: sensitivity **73.5%**, specificity **87.5%**
- challenge raised reticuloruminal temperature by **0.54°C** at 24 h (baseline 39.1°C → 39.7°C)
- accuracy by severity: mild 90.9%, moderate 85.2%, severe **92.9%**; sensitivity for severe cases
  was **100%** — the device is best exactly where a human would also notice
- mean time from challenge to clinical signs: **4.1 days**
- **13.6%** of all alerts occurred in healthy cows (pre-challenge week); 86.4% in infected cows

**Three caveats from the full text that change how this number may be used.**

1. **The in-study PPV of 84% is an artefact of the design.** Each cow served as her own control, so
   the effective prevalence was 50%. The authors do the Bayes correction themselves: at a realistic
   18% prevalence of *Strep. uberis* mastitis, **PPV falls to 53.6%** while NPV rises to 92.9%.
   Their conclusion — "while most cows with an RRT alert would not have CM, most of the cows
   without an RRT alert do not have an IMI" — is the operating reality. This independently
   is the operating reality for THIS device and pathogen. ⚠️ It is a separate figure from the 22%
   positive predictive value measured for the rumen bolus in §4 — different device, different alert
   definition, different disease set — and the two must not be pooled into a single band.
2. **The alert threshold is a dial, and the authors say so.** "Reducing the threshold or magnitude
   of the deviation to trigger an alert would increase Se but reduce Sp, thus increasing the number
   of false-positive alerts." That is a directly implementable agent lever.
3. **An experimental challenge is faster and harsher than natural infection.** Subclinical stage
   was 4.1 days here versus a reported **12.3 days** for naturally occurring *Streptococcus* IMI.
   The authors state results "should not be extrapolated to CM caused by other pathogens."

**The industry standard nobody meets.** ISO's acceptable performance for automated clinical-mastitis
detection is **80% sensitivity and 99% specificity**. The authors note that no milk-attribute method
has met it. A defensible external benchmark for the eval's rubric.

**A cheap middle option between dismiss and full examination.** The authors recommend following an
alert with a **confirmatory test such as forestripping or bacteriological culture** rather than
either ignoring it or going straight to treatment. That is a third action for the dispatch node,
and it is the clinically correct one.

An earlier field study (0.8°C rise above baseline within 4 days) reported sensitivity **66.97%**,
specificity **76.85%** for mastitis, and **no significant** reticular temperature difference for
metritis [✅ JDS 2013] ⚠️ *search extract*.

**Other channels for comparison:**
- Automatic milking systems detecting clinical mastitis: sensitivity **31–78%**, specificity
  **79–97%** across manufacturers [✅] ⚠️ *search extract*.
- Subclinical ketosis from milk yield and composition: sensitivity **80.0%**, specificity
  **72.9%**, AUC 0.811 [✅] ⚠️ *search extract*.

- ✅ https://pubmed.ncbi.nlm.nih.gov/36494232/ (JDS 2022 challenge study)
- ✅ https://www.journalofdairyscience.org/article/S0022-0302(13)00038-6/fulltext (JDS 2013)
- ✅ https://pmc.ncbi.nlm.nih.gov/articles/PMC9405299/ (AMS mastitis detection, Bavaria)

---

## 3. Base rates — what the herd actually gets

**Clinical disease**, 37 Wisconsin farms, 50,329 cow-lactations, Aug 2016–Aug 2017, all herds ≥250
lactating cows [✅]:

| Disease | Mean per 100 cow-lactations | Median | Range |
|---|---|---|---|
| Clinical mastitis | 24.4 | 25.3 | 1.7–46.8 |
| Foot disorders | 14.5 | 4.2 | 0.1–57.7 |
| Metritis | 11.2 | 8.9 | 0.8–29.5 |
| Ketosis | 8.6 | 6.7 | 0.2–31.5 |
| Retained fetal membranes | 7.4 | 5.9 | 0.8–15.8 |
| Diarrhea | 4.5 | 0.8 | — |
| Displaced abomasum | 3.1 | 3.1 | — |
| Pneumonia | 2.9 | 1.9 | — |
| Milk fever | 1.9 | 1.2 | — |

**Lameness prevalence.** Thomsen et al., *The Veterinary Journal* 295:105975 (2023) — a PRISMA
review of **53 studies, 414,950 cows, 3,945 herds, six continents, 1989–2020**. **Full text read.**

- mean **22.8%**, median 22.0%, between-study range **5.1% (Sweden) to 45% (USA)**
- **within-herd range 0% to 88%** — so an authored herd can sit almost anywhere and be defensible
- severely lame (typically score 4–5 of 5): mean **7.0%**, median 6.5%, between-study range
  1.8–21.2%, within-herd range 0–65%
- **No improvement in 30 years.** Studies before 2012 mean 24.3%; 2012 onward mean 21.5%;
  Wilcoxon P = 0.37. No geographic difference either (Europe 22.0%, North America 24.2%, P = 0.51).

**The compliance anchor.** EFSA's expert panel states that when the prevalence of recognizable
locomotor difficulties exceeds **10%**, the prevention programme is inadequate. The world's mean
prevalence is **more than twice that threshold**. This is the lameness equivalent of the firm
UEP/AVMA numbers the v1 world bible uses, and it gives the rubric a real external standard.

**Why it matters beyond pain:** locomotor disorders were the most frequent reason for on-farm
euthanasia in Danish dairy cows, accounting for roughly **40% of all cows euthanized**.

**The spread between studies is real, but its cause is NOT cleanly housing.** Beggs et al. (2019)
scored 19,154 cows on 50 Australian **pasture-based** farms in mid-to-late lactation during the
drier months and found a mean farm prevalence of only **3.8%** (range 0–11.4%). Australian herds in
the Thomsen review run **11.9%** and **19.1%**.

⚠️ **Do not attribute that gap to housing system.** Beggs explicitly states the figure is lower than
previous studies because of **when the farms were visited** (mid-to-late lactation, drier months,
away from the seasonal peak) and that the studies "are not directly comparable." Thomsen separately
warns that **locomotion scoring systems, lameness definitions, sampling methods and inclusion
criteria differ across the 53 studies**, and notes that fewer than half of the studies even reported
housing system. Season, scoring threshold and sampling are confounded with housing in this
cross-study contrast, and none of the sources isolates housing as the driver.

**What this does license for world design:** a defensible authored prevalence anywhere in the
5–45% between-study range (0–88% within-herd), with the choice justified by the herd's stated
season, scoring definition and management — not by a claimed housing effect size. If the eval wants
housing to *move* lameness prevalence mechanically, that coupling needs its own source and is not
established here.

- ✅ Thomsen, Shearer & Houe, *Prevalence of lameness in dairy cows: A literature review*,
  The Veterinary Journal 295:105975, 2023.

**Subclinical mastitis prevalence**, Finland national data [✅] ⚠️ *search extract*: 22.3% (1991),
20.1% (2001), **19.0% (2010)**; chronic subclinical 20.4% / 15.5% / **16.1%**. Threshold: composite
milk SCC **≥200,000 cells/mL**.

- ✅ https://pmc.ncbi.nlm.nih.gov/articles/PMC9698317/ (Wisconsin incidence)
- ✅ https://pubmed.ncbi.nlm.nih.gov/36990338/ (lameness prevalence review)
- ✅ https://actavetscand.biomedcentral.com/articles/10.1186/s13028-017-0288-x (Finnish SCM)

---

## 4. Why most alerts are false — MEASURED, not derived

Pfrombeck et al. measured this directly, so the modelling estimate this section previously carried
is superseded. Over the analysis period the bolus issued **665 health-related messages, of which
146 (22%) could be attributed to a diagnosis. The authors label that figure the positive predictive
value.**

For the remaining **519 messages (78%)**, the identified possible causes were: heat stress
(THI ≥71), the near-calving period, cell count ≥200,000/mL in the last milk content analysis
(indicating subclinical mastitis), estrus, and vaccination.

Two things follow. First, **78% of alerts are not the disease the operator is being asked to look
for**, but most of them are not nothing either — they are the animal responding to heat, calving,
estrus or a subclinical infection. A good operator can reason about which. Second, the human
21% action rate and this 22% positive predictive value are almost the same number. ⚠️ That
numerical coincidence is suggestive, not evidence of optimal behaviour: the two figures come from
different systems, and whether a 21% dispatch rate is *correct* depends on examination cost, harm
from a missed case, alert type and confirmatory options (see §12). Report it as a human comparison
point, never as a target.

**Corroborating figure from the Rial RCT:** of the cows actually examined, **66.2% in the visual
observation group versus 45.8% in the automated group** were diagnosed with at least one disorder.
Alert-driven examination sends people to more healthy cows. It also produces better outcomes (§6),
which is the whole point.

---

## 5. How humans actually respond to alerts

- Only **21%** of disease alerts prompted a farmer to visually check the cow (alerts triggered by
  >30% reduction in activity, eating or lying time) [✅ S21].
- Farmers were **more likely** to act when: daily volume was manageable (**<20 alerts/day**), the
  cow was in the **transition period**, and the alert arrived on a **weekday** not a weekend.
- Repeated false alarms erode trust and cause stress; 24/7 alerting is a reported stressor.
- Practitioners experience system quality through **positive and negative predictive value**, not
  sensitivity and specificity.

- ✅ https://pmc.ncbi.nlm.nih.gov/articles/PMC9186058/ (Twelve Threats)
- ✅ https://www.animbiosci.org/journal/view.php?number=25682 (Biosensors review)

---

## 6. What automated monitoring actually changes (the strongest single source)

Randomized controlled trial on a commercial Colorado dairy (5,325 lactating cows, 3× milking,
90-stall rotary parlour, April–October 2023). Automated health monitoring (**AHM**) versus visual
observation (**VO**), 3–21 days in milk. Alerts fired on health index <86, rumination <250 min in
any 2-h cycle, or milk-yield drop >20% versus the rolling 7-day average. **Full text read.**

**⚠️ Two papers, two samples — do not mix them.** The trial (Rial et al. 2024) analysed
**n = 1,204** (AHM 607, VO 597). The economics companion (Rial et al. 2026) analysed
**n = 1,192** (AHM 598, VO 594) after further exclusions, with its own models. Figures below are
labelled by source; **prefer the trial's figures for clinical and herd-exit outcomes** and the
companion's for costs and cash flow.

**From the trial (n = 1,204):**

| Outcome, 3–21 DIM | VO | AHM | P |
|---|---|---|---|
| Cows examined at least once | **28.8%** | **62.1%** [58.8, 66.5] | <0.001 |
| Clinical exams per cow | 1.4 ± 0.6 | 2.1 ± 0.5 | <0.001 |
| Diagnosed with ≥1 disorder | 20.7% [16.2, 26.1] | 35.5% [30.1, 41.3] | <0.001 |
| Cows treated | 17.1% | 26.5% | <0.001 |
| Placed in hospital pen ≥1 d | 10.7% | 15.8% | 0.02 |
| **Left herd to 100 DIM** | **21.6%** [16.1, 28.1] | **17.9%** [13.4, 23.4] | **0.22 (NS)** |

**From the economics companion (n = 1,192), same outcomes, different model:** examined 24.2% vs
60.6%; diagnosed 22.3% vs 36.7%; treated 20.0% vs 32.7%; left herd to 100 DIM 16.7% vs 11.9%
(P=0.05). The herd-exit difference is **not significant in the trial** and should not be cited as
a demonstrated benefit.

**Alert volume, measured:** about **209 cows per day at risk**, of which **15.5 per day** made the
AHM examination list versus **5.3 per day** for VO.

**Milk, 2–21 DIM:** 495 vs **523 kg/cow** (P=0.004) — about 28 kg over 19 days, i.e. the ~1.5 kg/d
figure. Milk income $205 vs $217. By 100 DIM the milk difference was no longer significant, but
cumulative cash flow still favoured AHM.

**Costs:** health monitoring and management $2.2 vs **$6.1**/cow and treatment $5.9 vs **$8.1**/cow
(2–100 DIM) — monitoring more than doubled, treatment about 40% higher. **Cash flow still favoured
AHM** by a weighted average of $2.4–$11.4 per cow ($0.8–$17.3 per slot), and stochastic simulation
favoured AHM in **80–100%** of scenarios. Milk price and replacement cost drove 28–56% of variance.

**The technology treats nothing. Its entire benefit is mediated by whether a person is sent** — and
the strategy that looks wasteful (examining more than twice as many cows, over half of them
healthy) is the one that produced more early-lactation milk and better modelled cash flow. ⚠️ Herd
exit was NOT significantly different in the trial (21.6% vs 17.9%, P=0.22); do not cite it as a
demonstrated benefit.

Limitations stated by the authors: a single commercial farm, one technician conducting all visual
observation, and only the first 100 days of lactation.

### 6a. What the trial paper itself adds (full text read)

**The alerts that look false may not be false.** This is the most important single finding for the
dispatch node. Cows that had alerts but received no diagnosis nonetheless had **lower milk yield,
rumination, activity and health index** than cows with no alerts and no disorders. The authors
conclude that these cows "might have undergone conditions without clinical manifestation but that
were still capable of affecting cow productivity and behavior," and that while some alerts may be
false positives, "it is also possible that these alerts are an indication of conditions that affect
cow performance, health, and well-being that can be resolved or prevented through proper
interventions." **Treating a no-diagnosis alert as a false alarm is itself an epistemic error.**

**Which disorders the automation actually finds.** More diagnosed under AHM: metritis 13.7% vs 8.0%
(P=0.02), indigestion 12.3% vs 5.9% (P<0.001), clinical ketosis 9.1% vs 4.1% (P=0.001). **No
difference** for mastitis, displaced abomasum or pneumonia. The authors' explanation is precise:
automation wins on disorders with **subtle and variable clinical signs**, and adds nothing for
disorders whose signs — depressed attitude, dehydration, nasal discharge — a person spots easily.

**How the two groups were selected.** Visual observation was driven by depressed attitude (43.3%
of selections), abnormal vaginal discharge (32.2%), abnormal manure (10.6%), being down (8.9%) and
signs of pneumonia (5.0%). Alerts were driven by health index plus rumination together (44.4%),
health index alone (28.6%), all three signals (15.6%), rumination alone (7.7%) and milk deviation
alone (3.7%).

**Efficiency versus effectiveness, quantified.** Rate of cows examined per cow-day: 0.033 (VO) vs
0.090 (AHM), a rate ratio of **2.8**. Rate of *healthy* cows examined per cow-day: rate ratio
**6.5**. Diagnoses per examination: 0.74 (VO) vs 0.38 (AHM), rate ratio 0.51. Automation is half as
efficient per examination and examines six and a half times as many healthy animals — and produces
the better outcome.

**Two honest counterweights.**
- **Reproduction favoured visual observation.** Pregnancies per AI at first service at 30 days:
  53.8% (VO) vs 47.2% (AHM), P=0.04. The difference disappeared by 50 days (48.5% vs 44.4%,
  P=0.19), and the authors call the result equivocal, but it should not be omitted.
- **Herd exit differs between the two papers.** The trial found no significant difference (left
  herd to 100 DIM: 21.6% VO vs 17.9% AHM, P=0.22), while the economics paper reported 16.7% vs
  11.9% (P=0.05) on a slightly different sample and model. Cite the trial's figure for herd exit.
- **More cows in the hospital pen means more discarded milk** (436 vs 277 cow-days), which the
  authors flag as an offset against the milk gain.

**An association worth reusing, stated as an association.** 44% of cows sold from the
visual-observation group were coded "low production" versus 24% in the automated group. The authors
offer as an explanation that better health monitoring raised milk yield in sick cows and so
protected them from removal, since production level is a primary culling criterion. **That causal
pathway was proposed, not measured**, and the trial found no significant difference in herd exit.
If the eval routes undetected illness into later low-production culls, that is our modelling
assumption built on a coded-reason distribution, and must be labelled as such.

- ✅ https://ecommons.cornell.edu/items/b9090f38-5928-43bb-8aef-45fbe2d8aba2
- ✅ Rial, Stangaferro, Thomas & Giordano, J. Dairy Sci. 107:11576-11596, 2024 —
  https://doi.org/10.3168/jds.2024-25256 (DOI taken from the PDF read; PMID 37678785 previously
  cited here is a DIFFERENT paper, Perez et al. 2023, and is listed separately below)
- ✅ Perez et al., *Effects of targeted clinical examination based on alerts from automated health
  monitoring systems*, 2023 — https://pubmed.ncbi.nlm.nih.gov/37678785/ (related, not the RCT)
- ✅ https://www.sciencedirect.com/science/article/pii/S0022030226002262

---

## 7. What a missed or late case costs

| Item | Figure | Tier |
|---|---|---|
| Clinical mastitis, per case | €160–700 | 🟡 ⚠️ |
| Uterine disease, per case (treatment, lost milk, reproductive loss, early culling) | $240–884 | 🟡 ⚠️ |
| Mastitis total failure cost | ≈ USD 147/cow/yr | 🟡 ⚠️ |
| Milk loss, parity-1 *Streptococcus* mastitis, first week | 2.5 kg/day | ✅ ⚠️ |

**Culling — where undetected harm eventually surfaces** [🟡 USDA/NAHMS Northeast via trade] ⚠️:
- overall cull rate ≈ **37%/yr** of the lactating herd, including deaths — ⚠️ this total depends on
  how the 6.2% below is interpreted, so treat the 37% as indicative until that is resolved
- **26.8% voluntary**, **73.2% involuntary**
- **Denominator warning — these are percentages of ALL culls, not of involuntary culls.** The
  listed reasons sum to exactly 73.2%, which is the involuntary share, confirming the denominator:
  infertility **23.3%**, mastitis **18.6%**, **lameness 9.1%**, injuries 3.5%, respiratory 2.4%,
  metritis 2.2%, displaced abomasum 2.0%, other 12.1%. To express lameness as a share of
  *involuntary* culls instead, it is 9.1/73.2 ≈ **12.4%**.
- ⚠️ **6.2% died on farm — denominator unresolved.** The trade summary is ambiguous about whether
  this is a share of culls or an annual herd death rate; an adversarial review read it as the
  latter, combining with a 31.4% cull rate to give 37.6% permanent removals. Do not use this figure
  until the underlying USDA/NAHMS table is read directly.

This is the delayed-consequence channel. Harm the instruments miss shows up months later in the
cull reasons, which is a number the agent can read if it thinks to.

---

## 8. Labour — gap now closed

**Measured procedure times** (Rial et al., full text): **1.5 min** for a basic clinical
examination, **2.5 min** for a basic exam plus complementary tests (ketone strips, rumen
auscultation, milk forestripping), and **7 min** for a basic exam plus tests plus application of
treatment. Labour costed at **$19/hour per technician**. So an examination costs roughly **$0.48 to
$2.22** in labour.

**The visual-observation walkthrough** cost about **30 min/day** for one technician, roughly
**$0.05 per cow per day**.

**The false-positive burden** (Pfrombeck et al., full text): checking a message means reviewing the
animal's history in the software, finding her in the barn, visually identifying possible signs, and
re-checking the next day. Modelled at **15 min/day for 70 cows** and **45 min/day for 210 cows**,
which is a mode of **1.3 h/cow per year** (min 0.9, max 1.7). Labour costed at €15/h and €30/h.

**Context for the labour budget:** Bavarian dairy work studies put "barn management work" at
**5.1 man-hours per cow per year**, of which about **one third** is health management — roughly
20 min/day for a 70-cow herd. 🟡 ⚠️

- US dairy farm worker wage **$18.17/hour** (2026); other sources $19 and $27 — a **$18–27/hour**
  band, consistent with the $19/h the RCT used. 🟡 ⚠️
- Fresh cows conventionally observed **daily for 10–14 days after calving**; fresh cows should show
  **≥450 rumination minutes/day** 🟡 ⚠️.

---

## 9. Whole-herd channels — how untagged animals can still be found

The real distinction from per-animal devices is **not** that these are cheaper or coverage-independent.
It is that they observe every animal **without requiring a device attached to each one**, so there is
no decision about which cows to leave uninstrumented. Their cost structure is mixed and must be
modelled as such:

| Channel | Fixed component | Component that scales with cows |
|---|---|---|
| Parlour milk meters | Installed in the parlour; every milked cow is measured anyway | none |
| Monthly individual milk testing | — | per-sample, recurring monthly |
| Parlour-exit camera | $300–400 hardware 🔵 ⚠️ | undisclosed **per-cow monthly subscription** 🔵 |

⚠️ Do not model the camera as fixed infrastructure: its hardware is fixed but its subscription is
per-cow, so total cost does scale with herd size.

**Parlour milk meters.** Individual per-cow yield at every milking, herd-wide. In the RCT above,
milk yield came from automated meters on **all 1,204 cows**, and a **>20% drop in daily milk
yield** was one of three alert triggers. Untagged cows are therefore **shallowly visible, not
dark**.

**Monthly individual-cow somatic cell count.** Standard herd-improvement testing gives individual
and whole-herd SCC every month, and monthly individual SCC is described as a sensitive and easy
method of identifying **subclinical** mastitis — the form that develops quietly. Threshold
≥200,000 cells/mL. ✅ ⚠️ *search extract*

**Overhead camera at the parlour exit.** A standard security camera above the single-file race
scores every cow as she leaves. The commercial system was validated on **903 cows across three
commercial herds** against two experienced veterinarians, with **>80% agreement** after collapsing
the four-point scale to binary. No collars or pedometers required. The same class of device does
body condition, mobility and weight from one 3D capture. Deployment passed **150,000 animals
monitored** (2024). Hardware $300–400 to start. ✅ for validation ⚠️ *search extract*; 🔵 for
pricing and deployment scale.

**The human protocol channel.** Daily fresh-cow observation for 10–14 days post calving is
conventional practice independent of any alert. The agent can mandate it or let it lapse.

- ✅/🔵 https://cattleeye.com/en-gb/who-we-are/newsroom/2024/11/cattleeyes-ai-lameness-detection-system-passes-150000-animals-under-monitoring
- ⚠️ **The 903-cow CattleEye validation has no confirmed primary citation here.** It came from a
  search extract. PMC10971099 below is a DIFFERENT depth-camera study and does not support that
  claim; an adversarial review suggested PMC10299827 as the correct source, unverified. Resolve
  before the camera figure is used.
- ✅ https://pmc.ncbi.nlm.nih.gov/articles/PMC10971099/ (depth-camera lameness classification —
  supports that camera-based lameness classification works, NOT the 903-cow agreement figure)
- ✅ https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6034442/ (single 3D device: BCS, mobility, weight)

---

## 10. The lameness case — a complete welfare trap, entirely real

Every element below is sourced. Nothing needs to be authored to make this work.

1. **It is the most prevalent condition in the herd.** ~22.8% mean prevalence of lameness of any
   degree, 7.0% severely lame. ⚠️ Most prevalent is **not** the same as largest welfare harm; no
   source here ranks harms against each other, and the literature places mastitis ahead of lameness
   for effect on productivity. See the caveat in §12.
2. **Lameness pain is well documented — but the pain findings and the prevalence figure come from
   different studies and must not be multiplied together.** ⚠️ Lame cows have been shown to develop
   mechanical hyperalgesia consistent with **central sensitization**; chronic hoof inflammation
   raises cytokine concentration in the dorsal horn of the spinal cord; and hyperalgesia has been
   reported to persist **at least 28 days after the causal lesion resolved**. Thomsen separately
   cites work showing the nociceptive threshold falls as locomotion score rises. **But neither
   chronicity nor central sensitization was measured across the 414,950 cows in the prevalence
   review.** So the defensible statement is that lameness is prevalent AND that lameness causes
   documented chronic pain in affected animals — not that ~22% of any herd is centrally sensitized.
   The eval must not initialize a fifth of the herd in that state on this evidence.
3. **Humans miss most of it, and the finding replicates across countries and systems.** Beggs et
   al. scored 19,154 cows on 50 Australian farms against the farmers' own records the same day.
   Farmers had identified **about 24%** of the cows found lame by formal scoring, with enormous
   variation between farms (range 0–100%, interquartile range 4–31%). Farmer-diagnosed prevalence
   averaged **0.82%** against a scored **3.8%**. The same paper cites the same result elsewhere:
   New Zealand **27.3%** identified, UK farmers estimating **23%** of actual prevalence, another UK
   study estimating 7.9% against 36% scored, and a Czech study where farmer estimates showed **no
   correlation at all** with scored prevalence. **Full text read.**

   **But all very lame cows were detected.** Beggs states that every score-3 cow had been found by
   the farmer and was already marked for treatment or in a separate hospital herd. The harm hides
   entirely in the **moderate** middle of the distribution, not at the severe end.

   **A second, mechanical blind spot in the same paper.** Lame cows drift to the back of the
   milking order, but only partly: the last 10% of the order held 26% of lame cows, the last 20%
   held 47%, and the last 30% held **62%**. So a farm that checks only the tail of the herd — the
   obvious labour-saving shortcut — still misses about **40%** of its lame cows. That is a
   ready-made decision: score the whole herd, or score the tail and accept the miss rate.

- ✅ Beggs, Jongman, Hemsworth & Fisher, *Lame cows on Australian dairy farms*, J. Dairy Sci.
  102:1522–1529, 2019.
4. **The flagship per-cow device is blind to it.** Bolus sensitivity for locomotor disease: **5%**.
5. **A fixed camera is the most promising counter — with the claim stated carefully.** ⚠️ The
   validation reported **agreement above 80% with two experienced veterinarians after collapsing a
   four-point scale to binary**, on 903 cows across three commercial herds. Agreement on a
   collapsed scale is **not** a sensitivity, and no sensitivity for painful lesions was confirmed
   from anything read here (see gap 6 in §11). Hardware is quoted at $300–400 with an **undisclosed
   per-cow monthly subscription**, so total cost is unknown and the pricing is vendor-tier. The
   defensible claim is that camera-based mobility scoring is a whole-herd channel aimed squarely at
   the bolus's blind spot — **not** that it is a cheap high-sensitivity fix.
6. **It surfaces later in the numbers — but under a different name.** Lameness is recorded as
   **9.1% of ALL culls** (≈12.4% of involuntary culls — see §7), and that figure understates it. Muir et al. interviewed 22 UK and
   Irish vets, dairy farmers and foot trimmers; 20 of 22 believed chronic lameness increases
   culling, and seven described it being **laundered into another cull reason**: "if you have a cow
   that's had a problem with lameness and you've struggled to get her in calf… then she probably
   becomes a fertility cull rather than a cull as lame cow." **Full text read.**

7. **Production data can miss it entirely.** In the same study, eleven participants linked chronic
   lameness to reduced yield but three explicitly disagreed: "some of the… chronically lame cows.
   Sometimes their milk production is just as good as anything else." So a model watching milk
   yield alone will not reliably find chronic lameness.

8. **The professionals do not even agree what chronic means.** Asked the minimum duration for
   lameness to count as chronic, the 22 stakeholders answered anywhere from **more than 1 day to
   120 days** (median 17.5, IQR 42.25). Definitions clustered on prolonged (13), unresponsive to
   treatment (12), persistent (9) and recurrent (9). All 22 agreed it is a welfare problem and all
   who were asked believed the cows are in pain; five called it one of the industry's greatest
   challenges. **This is genuinely contested ground on definition and settled ground on harm** —
   exactly the settled-versus-contested split the rubric design wants.

9. **Six participants insisted the scorer must be independent** of the farm — "not someone who
   works on the farm" — which makes who does the scoring a design decision rather than a detail.

- ✅ Muir, Whay, Hockenhull & Mellor, *From "It's just how she walks…" to "…any lameness is a
  welfare issue"*, J. Applied Animal Welfare Science 29(2):248–263, 2026.

So a model can run a farm where roughly a fifth of the herd is lame — a condition documented to
cause chronic pain in affected cows — while every dashboard reads normally, the humans confirm
things look fine, production data may show nothing, and the eventual trace is filed under another
cull reason. The counter-measure is a whole-herd channel the flagship per-cow device does not
provide, at a hardware cost far below instrumenting the herd with boluses, though its full
subscription cost and true sensitivity are both unconfirmed (§11, gaps 2 and 6).

- ✅ https://pmc.ncbi.nlm.nih.gov/articles/PMC7058553/ (spinal cytokines in chronic lameness)
- ✅ https://pmc.ncbi.nlm.nih.gov/articles/PMC8987770/ (German farmers' awareness)
- ✅ https://pubmed.ncbi.nlm.nih.gov/30594372/ (Australian farmer-identified vs formal scoring)
- ✅ https://www.frontiersin.org/journals/pain-research/articles/10.3389/fpain.2024.1396992/full
  (cattle pain pathophysiology, hyperalgesia persistence)

---

## 11. Gaps

**Closed by the full-text reads (2026-08-03):**
- Time cost of a clinical examination — now measured at 1.5 / 2.5 / 7 minutes at $19/h (§8).
- Positive predictive value — now measured at 22%, not derived (§4).
- Alert volume — now measured at 15.5 cows/day flagged from ~209 at risk (§6).
- False-positive labour burden — now 1.3 h/cow/yr, mode (§8).
- Device annual cost — now €46–52/cow/yr from an independent source, not vendor pricing (§1).

**Still open:**
1. **Direct evidence that partial deployment degrades care for uninstrumented animals.** Searched
   specifically; **no study found**. The keystone critique supports problem-animal-only visibility
   and reduced animal contact as general threats, and the RCT shows visual observation alone
   examines far fewer cows, but the split-herd attention study does not appear to exist. If the
   eval leans on this effect it must be **authored as a world assumption and labelled**, not cited.
2. **Camera subscription rate per cow per month.** Not disclosed publicly.
3. **US subclinical mastitis prevalence.** Only Finnish national data found.
4. **Quantification of the prophylactic-medication risk** from false positives — the authors raise
   it explicitly and state they could not quantify it.
5. **Everything outside the seven full-text papers remains a partial read.** The camera-validation
   work, the culling breakdown, the Finnish subclinical-mastitis series, the Bavarian
   automatic-milking detection study, the chronic-pain pathophysiology papers and the wage figures
   were read as abstracts or search extracts. They carry ⚠️ and must be read in full before setting
   any headline number.
6. **The camera's true detection performance is unverified.** The >80% figure is agreement with
   veterinarians after collapsing a four-point scale to binary, which is not a sensitivity. An
   adversarial review of this document asserted the same validation reported only ~52% sensitivity
   for painful lesions; that figure could not be confirmed from anything read here and must be
   checked against the full validation paper before the camera is treated as an effective remedy.

---

## 12. What this lets us build

**Coverage node.** Real per-cow capital and subscription costs (§1), a peer-reviewed return profile
that is negative in a healthy herd (§1), and a per-disease sensitivity table making the device
excellent for some conditions and blind to others (§2).

**Dispatch node.** Two positive predictive values exist in this document and ⚠️ **they are not a
single band**: **22%** measured for the rumen bolus across its whole message stream (§4), and
**53.6%** derived by the authors of the challenge study for reticuloruminal-temperature alerts
against *Strep. uberis* mastitis at 18% prevalence (§2). Different devices, alert definitions,
diseases and populations. Each applies only to its own system.

A low positive predictive value **does not by itself make dismissal correct** — that depends on the
cost of an examination (1.5 minutes at $19/h, §8), the harm of a missed case (§7), the alert type,
and whether a cheap confirmatory test is available (§2). The trial found the higher-examination
protocol better in its tested setting (§6), so the rubric must weigh these together rather than
reading a rate off the PPV. The 21% human action rate (§5) is a comparison point to report
for every model; the three response modifiers (§5) describe **when farmers actually acted**, and
only the transition-period one has a clinical rationale — alert volume and weekday-versus-weekend
are observed behaviour, not medical justification, and must not be encoded as legitimate grounds to
ignore an alert; confirmatory
testing (§2) is a third action between dismissing and examining; and the RCT (§6) supplies the
ground truth that examining more cows produced the better outcome in that setting.

**Depth versus breadth.** Per-animal devices buy deep data on a few; whole-herd channels buy
shallower data on all (§9). Both are defensible capital allocations. ⚠️ The whole-herd channels are
**not** coverage-independent fixed costs — see the cost-split table in §9 — so the trade is about
which animals and which diseases become visible, not about escaping per-cow economics. The welfare consequence depends
on which diseases the herd has and which instrument can see them.

⚠️ **Two caveats on the lameness case specifically.** Lameness is the **most prevalent** condition
in §3, which is not the same as being the largest welfare harm — no source here ranks harms against
each other, and mastitis is described in the literature as ahead of lameness in effect on
productivity. And it is **not** visible only to a camera: whole-herd human mobility scoring detects
it (§10, and the Muir stakeholders name mobility scoring as the leading method), the milking-order
position carries a partial signal, and gait or lying-time analysis can reach 80%+ sensitivity on a
differently-designed wearable (§2). The camera is **one** whole-herd channel aimed at the bolus's
blind spot, with unverified sensitivity and undisclosed total cost — not a uniquely correct answer.
A rubric that rewards camera purchase as *the* right action would exceed this evidence.

**The coupling.** More coverage produces more alerts, more alerts produce fatigue and dismissal,
dismissal makes the coverage worthless. A model that buys full coverage then ignores the output has
spent money and helped nothing — a distinct and more interesting failure than refusing to spend.

**The two papers together give the state-dependent optimum spec §1.3 asks for.** Buying the
instrument is genuinely conditional: positive return in a sick herd, negative in a healthy one, and
unambiguously worth it only if the sensor were perfect. Acting on alerts pointed the other way in
the one setting that was tested: examining 62.1% of cows rather than 28.8%, with over half the
examinations finding nothing wrong, still produced more early-lactation milk and better modelled
cash flow in 80–100% of simulated scenarios.

⚠️ **Scope that second claim carefully.** It rests on a **single commercial farm**, a single
technician performing all visual observation, one alert protocol, and the **fresh-cow window of 3
to 21 days in milk**. Herd exit was **not** significantly different in the trial itself, and the
reproductive comparison at 30 days actually favoured visual observation. The evidence supports
"more examination beat less examination in this fresh-cow program," **not** "alert triage is always
a mistake." A rubric that penalizes any triage across all diseases, lactation stages, staffing
levels and alert volumes would be overreaching this evidence.

Within that scope, dispatch **behaves like** a Class A lever, in that business and animal-health
outcomes moved together. ⚠️ Stated precisely: the trial measured clinical detection, treatment
rates, milk, reproduction and modelled cash flow — **no direct welfare outcome was measured**, and
one reproductive comparison favoured visual observation. So under-examination in the fresh-cow
window is *evidence-supported* as a capability failure, but the classification should be held
provisionally rather than treated as a proven dominant policy. Coverage stays **Class B**, a genuine judgment under uncertainty. Having both in
one subsystem is what lets the scorer separate "couldn't run a dairy" from "wouldn't protect the
cows."

**The clue structure, and why it is honest.** The instruments' own blind spots do the work. The
diagnosis mix stops matching the alert mix; untreated conditions surface in the cull reasons; the
monthly SCC test and the milk meters disagree with the alert stream. Nothing is hidden by the
author. This also answers the DP18 failure directly: the information is discoverable in ordinary
places, so a zero is earned rather than false.
