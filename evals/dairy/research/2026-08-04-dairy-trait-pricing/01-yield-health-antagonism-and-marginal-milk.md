# The yield–health antagonism, quantified — and what it does to catalog Option D

> Swept 2026-08-04 · **DELEGATED sweep** (Opus subagent, which itself dispatched three sub-sweeps marked
> `[del]`). These are the subagent's findings with its ⚠️ notices passed through **verbatim**, not
> re-verified by the orchestrating session except where noted. The one source the orchestrator read
> directly is USDA NM$ 2025, in `03-usda-net-merit-2025-read-in-full.md`.
>
> **Read this before pricing catalog §4.3 Option D.** The sweep's headline contradicts the catalog.

## The headline the sweep returned

**The antagonism is real but far smaller and far more trait-specific than catalog §4.3 assumes.** It is
strongest as a **genetic** correlation with **milk volume** specifically (not fat or protein), it
**reverses sign phenotypically** and **at herd level**, and modern US selection has largely defused it —
milk volume now carries 3% of Net Merit emphasis, and US Holsteins gained milk *and* productive-life
breeding value simultaneously over 2015→2020.

**Catalog §4.3 currently says** Option D's harm mechanism is "well-documented conventional dairy
science, not a gene-editing speculation — so nothing about the welfare cost is invented," listing
ketosis, metritis, mastitis, lameness and reduced fertility. That is **too strong as written**: for
ketosis, metritis and displaced abomasum the sourced genetic correlation runs the *favourable* way.

---

## 1. Genetic correlations with milk yield

### 1a. Modern meta-analysis

**Maskal, Pedrosa, de Oliveira & Brito 2024**, *J. Dairy Sci.* 107(5):3062–3079,
[doi:10.3168/jds.2023-23879](https://www.journalofdairyscience.org/article/S0022-0302(23)00823-8/fulltext)
— peer-reviewed; 926 heritability and 362 genetic-correlation estimates from 209 studies, worldwide
Holstein, 3-level random-effects model. Traits are **incidence of** the disorder, so **positive = unfavourable**.

| Pair | pooled rg ± SE | N est. | Direction |
|---|---|---|---|
| Milk yield × **lameness** incidence | **+0.174 ± 0.06** | 9 | unfavourable |
| Milk yield × **mastitis** incidence | **+0.130 ± 0.07** (CI 0.00–0.25) | 21 | unfavourable |
| Milk yield × somatic cell score | **+0.075 ± 0.04** | 27 | unfavourable |
| Milk yield × rectal temperature | +0.203 ± 0.11 | 6 | unfavourable |
| Milk yield × **metritis** incidence | **−0.126 ± 0.02** (CI −0.17 to −0.08) | 3 | **favourable** |
| Milk yield × **displaced abomasum** | −0.066 ± 0.04 | 5 | favourable/nil |
| Milk yield × retained placenta | −0.027 ± 0.05 | 3 | nil |
| Milk yield × milk BHB | −0.154 ± 0.10 | 5 | favourable/nil |
| Milk yield × milk acetone | −0.004 ± 0.04 | 5 | nil |
| Fat:protein ratio × ketosis | +0.463 ± 0.15 | 15 | unfavourable |
| Protein content × ketosis | −0.330 ± 0.26 | 6 | favourable |

**The hole in the table:** milk yield × **ketosis incidence** could not be pooled — fewer than 3 usable
estimates. Pooled heritabilities: ketosis 0.036, mastitis 0.044, lameness 0.032, metritis 0.036, DA
0.087, productive life 0.077.

### 1b. The older, wider range — why single numbers mislead

**Pryce, Parker Gaddis, Koeck et al. 2016** invited review, *J. Dairy Sci.* 99(9):6855–6873,
[fulltext](https://www.journalofdairyscience.org/article/S0022-0302(16)30392-7/fulltext). Genetic
correlations of milk/fat/protein yield with ketosis, DA and milk fever range **−0.49 to +0.65 (linear
models)** and **−0.67 to +0.77 (threshold models)**. Extremes: rg(milk, ketosis) **+0.65** (Simianer
1991) and **+0.77** (Uribe 1995); rg(milk, milk fever) **−0.67** (Uribe 1995, same study). Verbatim
conclusion: "there is a lack of consistency in genetic correlation estimates between metabolic diseases
and yield."

⚠️ *Subagent's note: read from the abstract through the "Genetic and Genomic Evaluations" section; browser
text **truncated at 40,000 characters**, so the predictor-traits sections and reference list were not read.*

### 1c. The single most important row in the sweep

**Donnelly, Hazel, Hansen & Heins 2023**, *Front. Genet.* 14:1254183,
[doi:10.3389/fgene.2023.1254183](https://doi.org/10.3389/fgene.2023.1254183) — 8 high-performance
Minnesota herds, 2008–2015, 2,214 first-parity cows. Table 7:

| Trait vs total health treatment cost | **Genetic** rg (SE) | **Phenotypic** r (SE) |
|---|---|---|
| Milk (305-d) | **+0.44 (0.18)** — significant | **−0.07 (0.02)** |
| Fat | +0.07 (0.21) — n.s. | −0.08 (0.02) |
| Protein | +0.28 (0.20) — n.s. | −0.10 (0.02) |
| Fat + protein | +0.18 (0.21) — n.s. | −0.09 (0.02) |
| SCS | +0.93 (0.13) | +0.14 |

Authors' conclusion, verbatim: "historical selection for increased fluid milk production may have caused
a correlated increase of THC in modern Holstein cows; however, our results suggest selection for fat (kg)
and protein (kg) has a reduced association with THC."

🚩 **rg = +0.44 but the phenotypic correlation is −0.07 — genetically antagonistic, phenotypically the
opposite, because sick cows produce less.** These two numbers must never be presented as measuring the
same thing. **This is the fork the eval has to choose on** (see the README's design consequence 2).

⚠️ *Subagent's note: full article text extracted (80,506 characters); abstract, Table 3, Table 7 and every
"genetic correlation" passage read; not read linearly.*

### 1d. Per 1,000 kg of extra yield, cow level

**Emam, Abdallah, Shepley & Caixeta 2025**, *Dairy* 6(3):28,
[doi:10.3390/dairy6030028](https://doi.org/10.3390/dairy6030028) — 2,336 multiparous Holsteins, 7 herds;
hyperketonemia = blood BHB ≥1.2 mmol/L in week 1 postpartum.

- **OR 1.19 (95% CI 1.05–1.35) per +1,000 kg of previous-lactation total milk.**
- ⚠️ *Subagent's note: this OR came **only from a search-result summary**. MDPI returned HTTP 403 to
  WebFetch, to curl, and the browser refused the domain; the full abstract was retrieved via the Crossref
  API, which confirms the direction and the "each additional 1,000 kg" finding but does **not** contain
  the OR. **Treat 1.19 as unverified until the PDF is obtained.***
- Verified from the abstract: dry period >60 d, days open >130 d and parity 3+ all raise risk.

### 1e. Fertility, and the herd-versus-cow reversal

**JDS 2017**, "Fertility traits of Holstein, Brown Swiss, Simmental, and Alpine Grey cows are differently
affected by herd productivity and milk yield of individual cows,"
[fulltext](https://www.journalofdairyscience.org/article/S0022-0302(17)30720-8/fulltext) — 91,865
lactations, NE Italy, 2011–2014, Cox models. Hazard ratios for days open (higher = pregnant sooner):

| | lowest class | mid (ref) | highest class |
|---|---|---|---|
| Holstein, **cow within herd** | 1.16 | 1.00 | **1.04** |
| Brown Swiss, cow within herd | 1.41 | — | 1.14 |
| Brown Swiss, **herd level** | 0.89 | — | **1.14** |

Verbatim: "A better production environment could lead to better overall fertility responses, whereas an
increase in the milk yield of individual cows within a herd leads to worsening fertility. These
associations … are nonlinear … more evident moving from low to medium milk yields than moving from medium
to high." **For Holsteins the highest-yielding within-herd class (HR 1.04) is essentially back at the
reference** — the within-cow penalty is not monotone.

⚠️ *Subagent's note: abstract, Results, Discussion and Conclusions read in full; Materials and Methods and
references not read.*

Corroboration: **JDS 2025**, German Holsteins, 32,352 primiparous cows in 5 yield strata,
[fulltext](https://www.journalofdairyscience.org/article/S0022-0302(25)00200-0/fulltext) — rg from
**−0.436 (milk × metritis, high-yield subset)** to **+0.435 (milk × retained placenta, same subset)**;
verbatim: "did not demonstrate a straightforward linear relationship between milk yield and the analyzed
reproduction parameters." ⚠️ *abstract and Introduction only.*

VanRaden et al. 2004: rg(days open, milk) ≈ **0.35**; h²(daughter pregnancy rate) = 4%. ⚠️ *Search-summary
only — the paper was not opened.*

### 1f. Evidence that high-yielding cows do **not** show elevated disease

- **Gröhn, Eicker & Hertl 1995**, *J. Dairy Sci.* 78:1693–1702,
  [doi:10.3168/jds.S0022-0302(95)76794-7](https://www.journalofdairyscience.org/article/S0022-0302(95)76794-7/fulltext)
  — 8,070 cows, 25 New York Holstein herds. Verbatim: "**higher milk yield was not a risk factor for any
  disease except mastitis. However, the association between higher previous milk yield and mastitis does
  not necessarily imply causation.**" ⚠️ *Abstract read in full; PDF-only body not accessible.*
- **Fleischer et al. 2001**, *J. Dairy Sci.* 84:2025–2035,
  [fulltext](https://www.journalofdairyscience.org/article/S0022-0302(01)74646-2/fulltext) — 2,197
  lactations, 10 German herds. Verbatim: "**No relationship to milk yield existed for metritis**";
  correlations only "probable" for retained placenta, mastitis and milk fever, "possible" for ketosis and
  DA. ⚠️ *Abstract read in full; PDF-only body not accessible.*
- **Pralle, Amdall, Fourdraine, Oetzel & White 2021**, *Animals* 11(5):1291,
  [PMC8145167](https://pmc.ncbi.nlm.nih.gov/articles/PMC8145167/) — **240,714 lactations, 174,690 cows,
  335 Midwest US farms**; FTIR-predicted hyperketonemia, overall prevalence 15.8%. **By rolling-herd-average
  milk quartile: Q1 (<11,137 kg) 16.6%, Q2 15.8%, Q3 16.4%, Q4 (≥13,265 kg) 14.9%.** Verbatim: "Across RHA
  quartiles, linear modeled pHYK **decreased linearly (p = 0.02)** as RHA milk yield quartiles increased."
  🚩 **But the immediately following sentence, also verbatim: "Prevalence of predicted HYK was positively
  associated with RHA milk production (p = 0.01; data not shown)."** These two statements contradict each
  other in direction and sit back-to-back in the same paragraph; the subagent verified both from raw
  article text. **Cite the quartile table (which is shown), not the "data not shown" continuous
  association.** Parity dominates everything: 4.0% (L1) → 35.0% (L5+).
- **Zhou et al. 2025**, *Animals* 15(17):2495,
  [PMC12427238](https://pmc.ncbi.nlm.nih.gov/articles/PMC12427238/) — 8,708 Holsteins, 6 farms,
  Heilongjiang, China. Verbatim: "**The somatic cell count (SCC) in high-yielding cows was significantly
  lower than that in low-yielding cows (p < 0.0001).**" 🚩 Reverse causation unaddressed — subclinically
  infected cows are low-yielding *because* of the infection. Not a US population. ⚠️ *WebFetch summarizer only.*
- **Zwald et al. 2004**, *J. Dairy Sci.* 87:4295–4302,
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/15545393/) — 272,576 lactations, 161,622 US cows, 646 herds.
  Verbatim: "correlations between predicted transmitting abilities for the aforementioned health traits and
  existing production, type, and fitness traits were low." ⚠️ *Abstract only — JDS served a Cloudflare bot
  challenge after ~15 successful article reads.*
- ⚠️ **Ingvartsen, Dewhurst & Friggens 2003**, *Livest. Prod. Sci.* 83:277–308 — the canonical "yield or
  metabolic imbalance?" paper. **NOT REACHED.** ScienceDirect served a Cloudflare challenge to WebFetch,
  curl and the browser. **Nothing is cited from it.**

### 1g. Has the antagonism weakened under genomic selection?

Yes, on every measured axis — while the health traits themselves carry almost no index weight.

- **García-Ruiz, Cole, VanRaden, Wiggans, Ruiz-López & Van Tassell 2016**, *PNAS* 113(28):E3995–E4004,
  [PMC4948329](https://pmc.ncbi.nlm.nih.gov/articles/PMC4948329/). Milk gain **50 → 109 kg/yr**
  (2006–2010 → 2011–2015). Daughter pregnancy rate gain "close to zero" before genomic selection,
  "dramatically increased" after. Productive life: "essentially no trend in PL before 2005," then 3–6×
  and 2–3× increases. Generation interval for sires of bulls "~7 y to less than 2.5 y." Verbatim:
  "There is a genetic antagonism between fertility and milk yield, and that negative genetic correlation
  has resulted in a steady decline in fertility in Holsteins until 2005" — then reversed. ⚠️ *WebFetch
  summarizer on the PMC copy, not raw text.*
- **[del] Guinan et al. 2023**, *J. Dairy Sci.* 106(2):1110–1129,
  [doi:10.3168/jds.2022-22205](https://doi.org/10.3168/jds.2022-22205) — Holstein bull PBV milk
  **34.71 kg/yr (2000–2008) → 62.30 kg/yr (2009–2017), +79.5%**; productive life 0.51 → 0.77 mo/yr
  (+50.1%). *Read end to end by the sub-delegate; reference list not read.*
- **Health traits are in the index but tiny.** **Parker Gaddis, VanRaden, Cole, Norman, Nicolazzi & Dürr
  2020**, *J. Dairy Sci.* 103(6):5354–5365,
  [fulltext](https://www.journalofdairyscience.org/article/S0022-0302(20)30310-6/fulltext) — 6 direct
  health traits entered US genomic evaluation April 2018 and Net Merit August 2018 at "**a total weight of
  approximately 2%**." US incidence (~2,000 herds, Aug 2019): milk fever 1.0%, DA 1.6%, ketosis 3.4%,
  **mastitis 9.3%**, **metritis 5.3%**, retained placenta 2.7%; observed-scale h² 0.6–3.1%. ⚠️ *Full body
  and all six tables read; browser text truncated inside the reference list.*
- **Selection pressure has moved off milk volume** — verified independently by the orchestrator in
  `03-usda-net-merit-2025-read-in-full.md` §3: milk emphasis 52% (1971) → 0/−1% (2003–2021) → **3%
  (2025)**, against fat 25%.
- **[del]** CDCB base change 2015→2020 Holstein cows: **+1,504 lb milk breeding value and +4.62 months
  productive-life breeding value simultaneously**
  ([2025 Base Change Resources](https://uscdcb.com/wp-content/uploads/2025/03/2025-Base-Change-Resources.pdf)).

### 1h. Per genetic standard deviation — derived, not published

**No published per-genetic-SD figure was sourced.** Both inputs exist: SD of true transmitting ability
for milk = **566.88 lb**, and for the disease resistances 2.9 (mastitis), 1.6 (ketosis), 1.6 (metritis),
0.6 (DA), 0.4 (milk fever), 1.0 (retained placenta) percentage points (NM$ 2025, read in full by the
orchestrator).

**DERIVED BY THE SUBAGENT, not published:** per **+1 genetic SD of milk (≈567 lb / 257 kg)**, roughly
**+0.38 percentage points of mastitis incidence** (0.130 × 2.9), i.e. 9.3% → ~9.7%; and **−0.20 points of
metritis** (−0.126 × 1.6), i.e. 5.3% → ~5.1%. This assumes the SD of genetic merit for *incidence* equals
the TTA SD of the *resistance* PTA, and mixes a worldwide-pooled rg with US SDs. **Order-of-magnitude
sanity check only** — but note what it implies: the disease consequence of a large yield gain is a
fraction of a percentage point, which is the finding that threatens Option D.

**NOT SOURCED:** any disease-incidence table stratified by herd yield quartile other than Pralle 2021
(hyperketonemia only).

---

## 2. Cost per case, USD — two families that differ 3–5× on scope alone

**Never mix them.** Family A is the treatment bill; Family B is the treatment bill plus every downstream
consequence. The orchestrator's recommendation, and the reason, is in the README.

### Family A — direct treatment cost only
USDA NM$ 2025, 2025 price basis: **DA $256 · metritis $146 · clinical mastitis $98 · retained placenta
$88 · milk fever $44 · ketosis $36.** Formula `(direct cost + yield adjustment) × 1.3`. Full detail and
the report's own scope statement are in `03-usda-net-merit-2025-read-in-full.md` §2 (read in full by the
orchestrator, no ⚠️).

Underlying per-cow (not per-case) treatment costs, **Donnelly et al. 2023** Table 3, first parity,
**February 2016 prices**, 8 Minnesota herds — vet labour, supplies, pharmaceuticals, owner labour only:
total $55.18/cow; reproduction $15.28 (13.3% treated), lameness $12.89 (26.7%), mastitis $10.88 (26.5%),
metabolic $8.02 (7.7%); metritis $9.95 (8.2%), DA $4.91 (1.7%), retained placenta $2.12 (2.7%), ketosis
$0.60 (1.5%).

### Family B — total economic cost per case **[del]**

| Disorder | Cost/case | Scope | Source | Price basis |
|---|---|---|---|---|
| Clinical mastitis | **$521** (90% CI 435–581); primi $374, multi $587 | drugs, labour, discard, post-treatment milk loss, culling, mortality, reproductive loss, **plus transmission to herdmates (11%)**; no vet labour | Rodriguez, Cabrera, Hogeveen & Ruegg 2024, *JDS* 107:4634–4645, [doi:10.3168/jds.2023-24311](https://doi.org/10.3168/jds.2023-24311) | milk $0.44/kg (2018–23), heifer $1,762 |
| Clinical mastitis | **$444** = $128 direct + $316 indirect | first 30 DIM only | Rollin, Dhuyvetter & Overton 2015, *Prev. Vet. Med.* 122:257–264 ⚠️ *abstract only, full text blocked* | milk $0.461/kg |
| Clinical mastitis | **$325.76** (P1) / **$426.50** (P2+) | 7 categories incl. milk loss $162–165 | Liang et al. 2017, *JDS* 100:1472–1486, [doi:10.3168/jds.2016-11565](https://doi.org/10.3168/jds.2016-11565) | 2015 |
| Clinical mastitis | **$192.36 ± 8.90** (farm range $118–337) | **drugs + discarded milk ONLY**; 20,625 real cases, 37 Wisconsin herds | Leite de Campos et al. 2023, *JDS* 106:9276–9286, [doi:10.3168/jds.2023-23412](https://doi.org/10.3168/jds.2023-23412) | milk prices 2016–17 |
| **Subclinical** mastitis | **$170**/case/lactation incl. transmission ($70 excl.); *S. aureus* **$767** | CMT, treatment, milk loss, culling, repro loss, progression, transmission | Rodriguez et al. 2024 | as above |
| Lameness, non-specific | **$185.10** (P1) / **$333.17** (P2+) | 7 categories | Liang et al. 2017 | 2015 |
| Lameness, per lesion | digital dermatitis **$64 ± 24** · sole ulcer **$178 ± 29** · white line **$152 ± 26** | therapeutics, trimmer + labour, discard, milk loss, days open, culling, death, recurrence | Dolecheck, Overton, Mark & Bewley 2019, *JDS* 102:715–730, [doi:10.3168/jds.2018-14901](https://doi.org/10.3168/jds.2018-14901) | 2018 |
| Metritis | **$511 mean, $398 median**, herd range **$156–948** | Δ 305-d gross profit: milk −$322, treatment +$118, replacement +$148, residual −$125, salvage +$82, feed −$121 | Pérez-Báez et al. 2021, *JDS* 104:3158–3168, [doi:10.3168/jds.2020-19125](https://doi.org/10.3168/jds.2020-19125) | milk $0.395/kg |
| Left displaced abomasum | **$432.48 ± 101.94** (P1) / **$639.51 ± 114.10** (P2+) | vet+treatment $197, milk loss $170/$281, culling, days open, death | Liang et al. 2017 | 2015 |
| Ketosis | **$289** avg ($375 P1, $256 P2+) | partial budget | McArt, Nydam & Overton 2015 via the 2022 review | ~2014 |
| Ketosis | clinical **€709** (5–95th €64–1,196); subclinical **€150** | milk loss, treatment, vet labour, DA + CM treatment, insemination, calf, culling net of salvage | Steeneveld et al. 2020, *PLoS One* 15:e0230448, [doi:10.1371/journal.pone.0230448](https://doi.org/10.1371/journal.pone.0230448) | Netherlands 2018 |
| Ketosis, all studies | **€19 to €812/case**; farm level €3.6–29/cow-yr | 9 of 10 studies 2015+ | 2022 systematic review, *JDS*, [fulltext](https://www.journalofdairyscience.org/article/S0022-0302(22)00272-7/fulltext) | mixed |

The 2022 systematic review is explicit that pooling is invalid: "the systematic approach review does not
allow combination of the cost estimates into a single figure."

### Per cow-year — a third unit, do not compare to either family
**Rasmussen, Barkema, Osei et al. 2024**, *J. Dairy Sci.* 107(9):6945–6970,
[fulltext](https://www.journalofdairyscience.org/article/S0022-0302(24)00821-X/fulltext) — 183 countries,
comorbidity-adjusted, **2021 prices, valued only through forgone milk + extended calving interval +
premature culling; treatment cost excluded**. **North America, $/cow-year:** subclinical ketosis 216.17,
clinical mastitis 153.99, subclinical mastitis 119.38, lameness 61.64, metritis 58.53, ovarian cysts
55.76, retained placenta 35.89, dystocia 10.05, DA 4.56, milk fever 4.33, clinical ketosis 1.18;
**total 765.64**. Comorbidity-adjusted annual milk loss (%): SCK 7.11, SCM 5.58, dystocia 3.48, metritis
2.87, lameness 2.62, CM 1.36, DA 1.18. Culling hazard ratios: DA 2.75, milk fever 2.64, CM 1.90, SCK
1.67, lameness 1.40, metritis 1.03. *Read in full by the subagent — body, all 7 tables, Notes; reference
list not read.*

### One premature cull
**No published US 2024–2026 "cost per cull" figure exists at peer-reviewed, government or extension
tier — NOT SOURCED.** Components are government-sourced but on incompatible units. See `02-...` §4 for
NASS replacement and salvage prices, and `03-...` §5 for NM$'s internal $1,794 rearing cost and $0.90/lb
salvage (and the 🚩 that NM$'s salvage assumption is stale against market).

---

## 3. How much extra yield is realistically deliverable **[del]**

**Annual genetic trend, US Holsteins** — CDCB base changes:

| Interval | PTA milk shift | Breeding-value shift | Phenotypic | Environment |
|---|---|---|---|---|
| born 2010 → 2015 | +492 lb/5 yr | **+984 lb/5 yr** | +1,077 lb | +93 lb |
| born 2015 → 2020 | +752 lb/5 yr | **+1,504 lb/5 yr** | +793 lb | **−711 lb** |

91% of the 2010→2015 Holstein phenotypic milk change was attributed to genetics.
[April 2020 base change](https://www.uscdcb.com/wp-content/uploads/2020/02/Norman-et-al-Genetic-Base-Change-April-2020-FINAL_new.pdf) ·
[April 2025 base change](https://uscdcb.com/wp-content/uploads/2025/03/2025-Base-Change-Resources.pdf).
🚩 Not comparable to bull-cohort PBV trends (Guinan's 62.30 kg/yr) — different populations, ~2× apart.

USDA NM$ 2025 (orchestrator read in full): expected progress from selecting on NM$ is **PTA milk
+76.856 lb/yr, breeding value +1,537 lb/decade.**

Phenotypic, USDA NASS: **2025 = 24,390 lb/cow/yr, "218 pounds above 2024," up 7.2% from 2016**
([Milk Production, Feb 2026](https://www.nass.usda.gov/Publications/Todays_Reports/reports/mkpr0226.pdf),
read end to end by the sub-delegate). 🚩 NASS is all breeds, all herds, per cow-year; CDCB is Holstein-only
DHI on the PTA/BV scale.

**Average versus top-decile herds** — CDCB DHI Report K-3, 2021,
[haall.html](https://queries.uscdcb.com/publish/dhi/current/haall.html), Holstein, 6,306 herds,
lb/cow-year, **herd-weighted**: 99th 32,709 · **90th 29,534** · 80th 28,016 · **50th 24,760** · 10th
18,594. **Top decile − median = +4,774 lb (+19%).** 🚩 The same report's Holstein "average" of 26,691 lb
is cow-year-weighted — do not compute "top decile minus average" across the two weightings. **NOT
SOURCED:** any K-3 percentile table for 2022–2025 (`dhi23`/`dhi24`/`dhi25` return 404).

### The clean negative — and it matters most

**A gene-edited dairy cow for increased milk yield does not exist, and the largest documented
single-locus effects on milk volume are small and mostly point the wrong way.**

- **DGAT1 K232A:** the lysine allele's substitution effect in German Holstein is **−260 to −320 kg milk
  yield** across lactations 1–3, with **+0.28% fat content**, +7.6 to 10.7 kg fat yield, −4.8 to −5.2 kg
  protein yield (Thaller et al. 2003, *J. Anim. Sci.* 81:1911–1918,
  [doi:10.2527/2003.8181911x](https://doi.org/10.2527/2003.8181911x)); in Fleckvieh −242 to −180 kg.
  Independent confirmation of direction in *JDS* 99:3113–3123: "the K allele was consistently associated
  with lower milk yields." ⚠️ *Direction and magnitude confirmed by the orchestrator from a search summary
  of the Thaller abstract; the paper itself was not read in full — it is paywalled.*
- **ABCG2 Y581S:** allele-substitution effect **−341 kg milk, +0.16% fat, +0.13% protein** on 335 Israeli
  sires' genetic evaluations; −226 kg on 670 daughters (Cohen-Zinder et al. 2005, *Genome Res.* 15:936–944,
  [doi:10.1101/gr.3806705](https://doi.org/10.1101/gr.3806705)) ⚠️ *abstract only.* 🚩 Breeding-value scale,
  not raw phenotype — not the same kind of number as Thaller's.
- **GHR F279Y:** "a strong effect on milk yield and composition" (Blott et al. 2003, *Genetics*
  163:253–266) ⚠️ *abstract only; PMC PDF and Oxford full text both unreachable. A "≈320 kg/305 d" figure
  appeared in a search snippet — **NOT SOURCED, do not use.***
- **Cattle edits actually in the literature:** POLLED, MSTN, PRLR/SLICK, PRNP, NRAMP1, BLG knockout,
  human-lysozyme knock-in — **none for yield**
  ([*Gene editing in livestock*, PMC11452096](https://pmc.ncbi.nlm.nih.gov/articles/PMC11452096/), 2024
  review) ⚠️ *WebFetch extraction only.* FDA's only low-risk determination for a food-use cattle intentional
  genomic alteration is **PRLR-SLICK** (heat tolerance, March 2022) ⚠️ *the FDA document was not opened.*

**Framing the subagent drew, and it is the right one:** the largest sourced single-locus effects on milk
*volume* are ~180–341 kg (≈400–750 lb) per lactation, and the two best-characterised **reduce** volume.
One five-year CDCB base interval delivered **+1,504 lb** of breeding value — **polygenic selection over
five years already beats the biggest known single gene by 2–4×.**

---

## 4. The marginal value of extra milk

**The US figure exists inside USDA NM$ 2025 and the orchestrator verified it directly** — see
`03-usda-net-merit-2025-read-in-full.md` §1. Marginal feed cost is **39% of the value of extra
production** versus **58% on an average basis**, marginal feed cost **$7.48–7.49/cwt** of standardized
milk, milk price after hauling **$18.50/cwt**, lifetime multiplier **2.70 lactations**. Derived:
**$11.01/cwt = $0.110 per marginal pound.**

**The complication, and it must not be dropped [del].** **Bach, Terré & Vidal 2020**, *J. Dairy Sci.*
103(6):5709–5725,
[fulltext](https://www.journalofdairyscience.org/article/S0022-0302(19)31086-0/fulltext), Table 2,
640-kg cow, milk €0.32/kg:
- Scenario A (fixed feed efficiency): marginal IOFC **€0.216/kg**, constant at 28→29, 35→36 and 49→50 kg/d.
- Scenario C (empirically increasing marginal nutrient requirement): marginal IOFC **falls from €0.173 to
  €0.078/kg** as yield rises 29 → 50 kg/d.
- Authors, verbatim: "the dilution of maintenance requirements associated with increases in production is
  **partially overcome by a progressive diminishing marginal biological response** … profits associated
  with improving milk yield might, in some cases, be considerably lower than expected."
- 🚩 The authors label Scenario A "a common scenario found in popular press." **Marginal IOFC stays
  positive but is not constant and is not uniformly better than average at high yields.**
- ⚠️ *Subagent read the abstract, efficiency/economics sections, Table 2 and the group-feeding simulation;
  not all ~17 pages.*

**The maintenance-dilution coefficient [del].** NASEM 2021, *Nutrient Requirements of Dairy Cattle*, 8th
rev. ed., Ch. 3, [NCBI Bookshelf NBK600598](https://www.ncbi.nlm.nih.gov/books/NBK600598/):
`NEL_maint (Mcal/d) = 0.10 × BW_kg^0.75` (Eq. 3-13, raised from 0.08 in NRC 2001) and
`NEL (Mcal/kg milk) = 0.360 + 0.0969 × Fat%` (Eq. 3-14c). Derived by the sub-delegate (unit conversion
only): 0.317 Mcal NEL/lb at 3.5% fat, 0.295 at 3.0%; 13.3 Mcal/d maintenance for a 1,500-lb cow.
⚠️ *Chapter extracted in full (102,427 chars); energy/maintenance/lactation sections and Eqs. 3-10 to
3-14c read to their ends, not the whole chapter.*

**Older US marginal figures — wrong price era, useful for the shape [del].** Eicker, Fetrow & Stewart
2006, *WCDS Adv. Dairy Technol.* 18:137–155,
[PDF](https://wcds.ualberta.ca/wp-content/uploads/sites/57/wcds_archive/Archive/2006/Manuscripts/Eicker.pdf)
(read in full by the sub-delegate): NY dairy 1996, marginal feed cost **$3.00/cwt** against $12.00/cwt
milk → marginal IOFC **$9.00/cwt**, 4:1; CA dairy 1997 → **$11.22/cwt**, 5:1. In the same table **average**
feed cost per cwt falls 8.00 → 6.00 → 5.14 → 4.88 across 30/50/70/80 lb/d while **marginal** feed cost
stays flat at $3.00/cwt. 🚩 **Do not rescale these to today's milk price and present the result as
sourced.**

⚠️ **A stand-alone published 2024–2026 US marginal-IOFC $/lb figure: NOT SOURCED.** The USDA 39%-vs-58%
split is the closest thing and it is a percentage. 🚩 DMC margin ($/cwt, whole-herd formula feed) and
extension IOFC ($/cow/day, lactating-cow feed only) are not inter-convertible.

---

## 5. Do higher-yielding cows have shorter productive life? **[del]**

**No — within herd the relationship runs the other way.** The "high producers die young" intuition is not
supported by the US data.

**Current US average — four different quantities with four different denominators:**
1. **CDCB Productive Life is a PTA in months relative to the breed base, not a duration**
   ([CDCB Individual Traits](https://uscdcb.com/services/genetic-evaluations/individual-traits/)). A PL of
   0 means "average," not zero months.
2. **Observed cohort productive herd life:** Hare, Norman & Wright 2006, *J. Dairy Sci.* 89(9):3713–3720,
   [fulltext](https://www.journalofdairyscience.org/article/S0022-0302(06)72412-2/fulltext) — 13.8 million
   US cows calving 1980–2005. Holstein mean **32.7 months**; 36.5 (1980 cohort) → **31.9 (1994)**. Mean
   parities **2.94**. Survival to parity 2/3/4 = **73% / 50% / 32%**.
3. **Steady-state from cull rate:** De Vries 2020, *J. Dairy Sci.* 103(4):3838–3845,
   [fulltext](https://www.journalofdairyscience.org/article/S0022-0302(20)30120-X/fulltext) — DRMS 2018,
   9,158 herds: annual cull rate **38%** (4% dairy sales) → 34% involuntary → **35.3 months, "equivalent
   to fewer than 3 lactations"**; the paper's own economics say ~**5 yr** would be optimal. Herd cull
   rates ranged <10% to >60%. 🚩 A reciprocal-of-cull-rate estimate is structurally different from Hare's
   cohort measure.
4. Trade press: 28.4 months "in 2018" ⚠️ *trade tier, birth-year vs calendar-year ambiguous — do not put
   on the same axis as (2) or (3).*

**Yield versus longevity:**
- **Within herd, US:** Hadley, Wolf & Harsh 2006, *J. Dairy Sci.* 89(6):2286–2296,
  [fulltext](https://www.journalofdairyscience.org/article/S0022-0302(06)72300-1/fulltext); probit on
  1,126,610 Upper Midwest + 332,326 Northeast lactations. Verbatim: "A cow that produced one additional
  hundredweight more than the average 305ME milk yield was **1.7% less likely to be culled** … in the
  Upper Midwest region and about **0.5% less likely** in the Northeast." Same models: SCC +8.81%/+7.84%;
  each additional lactation +31.4%/+21.0%. ⚠️ *Read truncated at 40,000 characters — end of Discussion and
  Conclusions not read.*
- **Herd level, same paper — the sign flips on definition.** Average annual cull rate by rolling herd
  average, **including** dairy sales: 34.6% (RHA ≤8,182 kg) → **40.9%** (≥12,273 kg). **Excluding** dairy
  sales: 30.8% → **32.2%**, essentially flat. 🚩 "High-producing herds cull more" is largely an artefact of
  counting heifer and dairy-cow sales as culls.
- **Genetic correlations:** Tsuruta, Misztal & Lawlor 2005, *J. Dairy Sci.* 88(3):1156–1165,
  [fulltext](https://www.journalofdairyscience.org/article/S0022-0302(05)72782-X/fulltext); 392,800 cows.
  rg(305-d milk, PL305) = **−0.11**; PL500 **+0.08**; PL999 **+0.14**; herd life **+0.04**. 🚩 **The sign is
  an artefact of the 305-d truncation, not a biological constant** — any citation must state which PL
  definition it belongs to. Authors: "low milk production may not be a primary reason for voluntary culling."
- **Other populations** ⚠️ *second-hand from a review* ([PMC8369829](https://pmc.ncbi.nlm.nih.gov/articles/PMC8369829/),
  WebFetch extraction, contains at least one typo): +0.43 to +0.61 down to −0.25. Review's verdict: "the
  correlation between longevity and milk yield remains unclear."
- **Both improve together in the real US population:** 2015→2020 Holstein cohorts gained **+1,504 lb milk
  BV and +4.62 mo PL BV simultaneously**, while realised phenotype moved only +793 lb and +1.39 mo — the
  environment contributed **−711 lb and −3.23 mo**. **Management, not genetic antagonism, is what erodes
  realised productive life.**
- Hare et al. 2006, verbatim: "**US dairy producers keep cows with high yield the longest** … milk yield
  was by far the most important factor influencing survival."
- De Vries 2020, verbatim: "**Increases in the genetic trait productive life have not led to marked
  increases in phenotypic productive lifespan**"; and "The reductions in fertility and health that were
  observed when selection was primarily directed to selection for milk yield **have since reversed**."

**NOT SOURCED:** a US survival analysis stratified by yield quartile with hazard ratios; the mean and SD
of *observed* PL in CDCB's dataset (the public genetic-trend query is retired, 404).

---

## 6. Non-comparability flags — each has already caused an error in this literature

1. **Genetic vs phenotypic correlation.** rg(milk, health cost) **+0.44** vs r_p **−0.07** — opposite
   signs, same cows, same table.
2. **Direct-treatment vs total-economic cost.** Ketosis **$36** (NM$ 2025) vs **$289** (McArt) vs **€709**
   (Steeneveld). Mastitis **$192** (drugs + discard only) vs **$521** (everything incl. transmission) —
   2.7× on scope alone.
3. **Per case vs per cow-year vs per lactation vs per cow treated.** Rasmussen's $153.99 mastitis is per
   **cow-year** across the herd, production losses only; Rodriguez's $521 is per **case**; Donnelly's
   $10.88 is per **cow in the herd**, treatment only.
4. **Price-basis year ≠ publication year.** Every Family-B model sits below current cost levels because
   replacement price rose from ~$1,600–1,760 in those models to $2,860–3,260/head now, and every one of
   them shows cost rising with replacement price.
5. **Cow-within-herd vs herd-level yield.** Higher **herd** productivity improves fertility; higher
   **individual** yield within a herd worsens it. Hyperketonemia prevalence *falls* across herd RHA
   quartiles. Treating "high-yielding" as one variable is an ecological-fallacy trap.
6. **Milk volume vs fat/protein.** rg with health cost: milk **+0.44** (significant) vs fat **+0.07**
   (n.s.), against NM$ 2025 emphasis of 3% milk and 25% fat. Any claim about "selection for production"
   must say *which* production trait.
7. **Bull-cohort PBV trend vs cow-population base change** — 62.30 kg/yr vs ~301 lb BV/yr, ~2× apart by
   construction.
8. **Herd-weighted vs cow-year-weighted herd averages** — K-3 median 24,760 lb vs "average" 26,691 lb,
   same report.
9. **Liang 2017 and Dolecheck 2019 are not independent** — same model lineage (Bewley 2010 + @Risk).
10. **Pralle 2021 contradicts itself internally** on the RHA–hyperketonemia direction, in consecutive
    sentences.
11. **The brief mis-titled a source:** there is no Rollin/Dhuyvetter/Overton 2015 paper called "The cost of
    clinical disease in transition dairy cows." The real one is *"The cost of clinical mastitis in the
    first 30 days of lactation."* The $330–386 metritis figure often attributed to that line is **Overton
    & Fetrow 2008**, cited second-hand.

---

## Coverage statement (the subagent's, passed through)

**Read end to end by the subagent** (article body and all tables; reference lists not read unless noted):
USDA NM$9 (01-25) — all 19 pages including references *(independently re-read in full by the
orchestrator)* · Rasmussen et al. 2024 · Parker Gaddis et al. 2020 (truncated inside reference list) ·
Maskal et al. 2024 (later heterogeneity subsections read in part) · the 2022 ketosis systematic review ·
USDA NASS *Agricultural Prices* January 2026 (Milk Cows / All Milk / Cows tables and footnotes; the other
~90 pages of commodity tables not read) · Steeneveld et al. 2020 ⚠️ *via the WebFetch summarizer on the
PMC copy, raw text not seen.*

**Read substantially but ⚠️ NOT to the end:** Pryce et al. 2016 (truncated at 40,000 chars) · Donnelly et
al. 2023 (not read linearly) · JDS 2017 herd-vs-cow fertility (Methods and references not read) · Pralle
et al. 2021 (RHA passages from raw text, rest via summarizer) · García-Ruiz et al. 2016 (summarizer only)
· JDS 2025 German Holstein (abstract and Introduction only) · Zhou et al. 2025 (summarizer only) · CDCB
evaluation-changes and Impact pages (summarizer only).

**Abstract-only, body inaccessible:** Gröhn et al. 1995 · Fleischer et al. 2001 (both PDF-only on the JDS
site) · Zwald et al. 2004 (Cloudflare challenge after ~15 successful reads).

**Could not reach at all:**
- ⚠️ **Ingvartsen, Dewhurst & Friggens 2003** — ScienceDirect Cloudflare challenge to all three tools.
  Nothing cited from it. Needs an institutional ScienceDirect session or a library PDF.
- ⚠️ **Emam et al. 2025** full text — MDPI 403 to fetch and curl, browser refused the domain. Abstract via
  Crossref API only; the OR 1.19 rests on a search summary. Needs the open-access PDF from a non-blocked
  network.
- ⚠️ **Liang et al. 2017** full cost tables — JDS and ScienceDirect both 403; per-case figures come from
  the PubMed abstract, the 2022 review's Table 3, and **[del]** a sub-delegate's browser read.

**Delegation note.** Three sub-subagents produced the material marked **[del]** (cost-per-case, trends
and productive life, marginal milk). All three returned explicit coverage statements, passed through above
as per-claim ⚠️ notices rather than dissolved into synthesis. **These are the subagents' claims.** The
ones that would drive a design decision — Liang's cost table, Rodriguez's $521, the CDCB base-change
figures, and Bach's Table 2 — should be traced to source directly before being relied on. The two that
already drive the pricing decision (the NM$ marginal-feed split and the single-locus effect ceiling) were
traced by the orchestrator: NM$ read in full (`03-...`), DGAT1 direction confirmed from a search summary
of Thaller et al. 2003 ⚠️ *(abstract-level only; the paper is paywalled)*.
