# Sources — stocking-density research pass (2026-07-29)

Citation-grade source list for the research behind
`docs/specs/2026-07-29-stocking-density-design.md`, kept separately so it can be lifted into a paper.

**Two warnings before this is cited anywhere.**

1. **Author and year metadata is incomplete.** The pass was run via web search, which returned titles,
   hosts and URLs but not always full bibliographic records. Fields marked `TO COMPLETE` are **not
   known to me** and must be filled from the article record itself. They are deliberately left blank
   rather than guessed — a fabricated author or year in a paper is worse than a gap.
2. **Verification level differs per source.** Only S1 and S2 were read in full. Everything else is
   abstract or search-summary level. The `Read` column is the honest status.

## Verification key

| level | meaning |
|---|---|
| **FULL** | Article body read; specific figures extracted and quoted |
| **ABSTRACT** | Abstract or search summary only; figures not confirmed in context |
| **SUMMARY** | Only a search-result snippet; treat as a pointer, not evidence |

---

## Primary sources (read in full)

### S1 — Space allowance and cage size in furnished cages, Part I
- **Title:** Effect of space allowance and cage size on laying hens housed in furnished cages, Part I: Performance and well-being
- **Authors / year:** `TO COMPLETE`
- **Journal:** Poultry Science (per host) · **DOI:** `TO COMPLETE`
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC5850468/
- **Read:** **FULL**
- **Design / n:** 1,218 LSL-Lite hens, 18→72 wk; 520 vs 748 cm²/bird; small (178×122 cm) and large (358×122 cm) furnished cages
- **Figures used:** hen-day production 93.0 ± 0.1 % (low SA) vs 94.4 ± 0.2 % (high SA), P = 0.21; mortality P = 0.55; feather condition significantly poorer at low SA, **P = 0.048**; feather cleanliness P < 0.0001
- **Supports:** the production-null claim underpinning the economics (§5/§7b), and the revised
  "density → feather condition is SUPPORTED in lay" verdict (§7a)
- **Caveat that must travel with any citation:** 520 and 748 cm² are **80.6 and 116 sq in/hen — both
  below** UEP's 144 sq in minimum, and these are furnished cages, not cage-free aviaries. The effect
  is demonstrated *below* this sim's operating range.

### S2 — Air quality in alternative housing systems, Part II — Ammonia
- **Title:** Air Quality in Alternative Housing Systems May Have an Impact on Laying Hen Welfare. Part II—Ammonia
- **Authors / year:** `TO COMPLETE`
- **Journal:** Animals (per host) · **DOI:** `TO COMPLETE`
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC4598711/
- **Read:** **FULL**
- **Figures used (measured in-house NH₃):** aviary with belt removal 5–30 ppm; **aviary with weekly belt removal (Jan–Apr) 32–38 ppm**; aviary, litter, no removal for two years 9.2–47.4 ppm; aviary winter cold days 40 ppm; deep-litter floor with indoor manure storage 85 ppm with daily peaks > 100 ppm; welfare threshold "above 25 ppm may have adverse effects on the health and production of poultry"; occupational limits Norway 25 ppm, France 10 ppm, EU 20 ppm
- **Supports:** the empirical ceiling for the N2 ammonia fix, the `belt_interval_days = 7` → 32–38 ppm
  calibration target, and confirmation of the 25 ppm welfare threshold
- **Important negative finding:** this review contains **no quantitative stocking-density → ammonia
  data**. An earlier draft of the memo implied it did; corrected in §7c.

---

## Secondary sources (abstract / summary level — NOT yet verified)

### S3 — Enrichment × stocking density in pullets
- **Title:** The influence of environmental enrichment and stocking density on the plumage and health conditions of laying hen pullets
- **Authors / year:** `TO COMPLETE` · **DOI:** `TO COMPLETE`
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6527515/
- **Read:** **ABSTRACT** (structured summary; figures below came from a fetch of the article page)
- **Figures used:** EG1 22–23 pullets/m² no enrichment, plumage triscore 10.40; EG2 18/m² enriched 10.61; EG3 22–23/m² enriched 10.55; body injuries 0.11–0.13 injured regions/bird, no significant density or enrichment effect; enrichment significant only in week 17 (9.45 vs 9.04, coefficient 0.55)
- **Supports:** the density → pecking null result in *rearing*, and the reason pecking is modelled
  conservatively rather than as the headline tension
- **Caveat:** pullets, not hens in lay; every arm above 17/m²

### S4 — Density, production, profitability and aggressive pecking in group cages
- **Title:** Effects of Stocking Density in Group Cages on Egg Production, Profitability, and Aggressive Pecking of Hens
- **Journal:** Journal of Applied Animal Welfare Science, Vol 26, No 3 · **DOI:** 10.1080/10888705.2021.1983723
- **Authors / year:** `TO COMPLETE`
- **URL:** https://doi.org/10.1080/10888705.2021.1983723
- **Read:** **SUMMARY**
- **Claim used:** reducing stocking density raised production cost but was "compensated for by a high
  egg income"; lower density gave higher hen-day production and better feed conversion
- **Role:** counter-evidence to net-profitable crowding. Note it runs through the pecking pathway,
  which S3 shows is weak — this is the reconciliation in §5.

### S5 — Adequate stocking density for laying hens in cage-free systems
- **Publisher:** EU CAP Network, practice abstract · **Authors / year:** `TO COMPLETE`
- **URL:** https://eu-cap-network.ec.europa.eu/projects/practice-abstracts/adequate-stocking-density-laying-hens-cage-free-systems_fr
- **Read:** **SUMMARY**
- **Claim used:** densities below the legal maximum (< 9 hens/m²) reduce feather-pecking risk, and the
  avoided losses can make lower density economically profitable
- **Role:** counter-evidence, same pathway caveat as S4. Practice abstract, not peer-reviewed — weight
  accordingly in a paper.

### S6 — End-of-lay postmortem findings in aviary-housed hens
- **Title:** End of lay postmortem findings in aviary housed laying hens
- **Authors / year:** `TO COMPLETE` · **DOI:** `TO COMPLETE`
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9720333/
- **Read:** **SUMMARY**
- **Claim used:** cannibalism ~18.6 % of layer mortality in litter-based and aviary systems, non-beak-trimmed, 18–78 wk; salpingitis and cannibalism the dominant causes in aviaries
- **Supports:** the feather-damage → cannibalism-mortality link, and why S1's null mortality result
  does not transfer to a cage-free setting

### S7 — Laying hen mortality meta-analysis, 16 countries
- **Title:** Laying hen mortality in different indoor housing systems: a meta-analysis of data from commercial farms in 16 countries
- **Journal:** Scientific Reports · **Authors / year:** `TO COMPLETE` · **DOI:** `TO COMPLETE`
- **URL:** https://www.nature.com/articles/s41598-021-81868-3
- **Read:** **SUMMARY**
- **Claims used:** cage-free cumulative mortality 5–12 %, reaching 15.6–20.9 % in some trials; Norway
  mean cumulative mortality 3.74 % at 71 wk (2020); each year of aviary experience associated with a
  0.35–0.65 % drop in cumulative mortality
- **Supports:** plausibility bounds for any density-driven mortality term

### S8 — Egg producer attitudes and the cage-free transition
- **Title:** Egg producer attitudes and expectations regarding the transition to cage-free production: a mixed-methods approach
- **Journal:** Poultry Science (per host) · **Authors / year:** `TO COMPLETE` · **DOI:** `TO COMPLETE`
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10514442/
- **Read:** **SUMMARY**
- **Claims used:** cage-free total costs ~36 % above conventional, attributed to higher fixed capital
  *and lower stocking densities*; operating costs ~23 % higher, driven by labour and feed
- **Supports:** the economic gradient — why lower density raises cost per dozen

### S9 — European vs North American housing design and ammonia emission factors
- **Title:** Effect of European and North American poultry housing design and manure management on ammonia emission factors
- **Journal:** Waste Management (per host) · **Authors / year:** `TO COMPLETE` · **DOI:** `TO COMPLETE`
- **URL:** https://www.sciencedirect.com/science/article/pii/S0956053X26000954
- **Read:** **SUMMARY — NOT VERIFIED**
- **Claim used:** ammonia emissions at low stocking density **27 ± 16 %** lower than high density per
  kg "as-is" manure and **31 ± 19 %** per kg dry manure; EU cage minimum 750 cm²/bird vs North
  American 474 cm²/bird giving higher manure volume and N load per m²
- **⚠ This is the single most load-bearing unverified number in the pass.** The revised design makes
  ammonia the *primary* density pathway, so this coefficient carries the node's welfare cost. It was
  originally mis-attributed to S2, which does not contain it. **Read in full before it ships.**

### S10 — Welfare and farm profitability, cage vs free-range, China
- **Title:** The Relationship between Animal Welfare and Farm Profitability in Cage and Free-Range Housing Systems for Laying Hens in China
- **Authors / year:** `TO COMPLETE` · **DOI:** `TO COMPLETE`
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9405104/
- **Read:** **SUMMARY**
- **Claims used:** free-range production efficiency lower than cage, but income per 10,000 hens higher;
  cage total and peak egg production higher with lower egg-loss rate
- **Role:** context on per-hen vs per-area profitability. Different regulatory and market setting —
  weight accordingly.

### S11 — Causes of feather pecking in relation to welfare
- **Title:** Importance of Basic Research on the Causes of Feather Pecking in Relation to Welfare
- **Authors / year:** `TO COMPLETE` · **DOI:** `TO COMPLETE`
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC7070775/
- **Read:** **SUMMARY**
- **Claims used:** pecking reported more often at higher densities in some studies but the link varies
  with age and group size, mechanisms undetermined; **density × genetic-line interaction** — high
  density with a pecking-prone line gives disproportionately high pecking
- **Supports:** modelling the density→pecking term as weak and **genetics-amplified**, which is what
  makes DPD's `genetics: low_pecking` a real interaction rather than a flat bonus
- **Also cited for:** correlation **0.60–0.80** between feather/skin damage and cannibalism mortality
  — ⚠ this figure appeared in a search summary spanning several results and its source attribution is
  **not confirmed**. Do not cite the 0.60–0.80 without locating it.

---

## Added by the 2026-07-30 coefficient-verification pass (Task 0)

Dispositions and derivations in `docs/research/2026-07-30-density-coefficients.md`. All five were
retrieved from publisher abstract/article pages by automated fetch — **stronger than a search
snippet, weaker than reading the paper**. Full texts are paywalled (ScienceDirect, ResearchGate and
HAL all returned 403).

### S12 — Ammonia emissions of laying hens by stocking density and manure accumulation time
- **Title:** Ammonia Emissions of Laying Hens as Affected by Stocking Density and Manure Accumulation Time
- **Authors / year:** L. B. Mendes, H. Xin, H. Li · 2010
- **Venue:** ASABE Annual International Meeting, Pittsburgh, 20–23 June 2010 · **DOI:** 10.13031/2013.29895
- **URL:** https://elibrary.asabe.org/abstract.asp?aid=29895
- **Read:** **ABSTRACT**
- **Design:** manure-belt laying-hen houses; HD **413 cm²/hen**, LD **620 cm²/hen**; MAT to 7 d
- **Figures used:** NH₃ emission 3rd–7th d MAT **41→307 mg/hen-d (HD)** vs **29→188 mg/hen-d (LD)**; daily NH₃ ER increases exponentially with MAT (P < 0.0001); night-time hourly ER as high as daytime
- **Supports:** **the density → ammonia coefficient (Q1).** The per-hen basis is what settles the sign question: each bird emits ~63 % more when crowded, and the crowded house also holds 1.5× more birds, so the two channels compound
- **Caveat:** 413 and 620 cm²/hen are **64.0 and 96.1 sq in/hen — far denser than the sim's 130–144 range**; and the study's per-hen floor allocation is not the same denominator as UEP's usable-area 144

### S13 — Same, journal version, adding pullets
- **Title:** Ammonia Emissions of Pullets and Laying Hens as Affected by Stocking Density and Manure Accumulation Time
- **Authors / year:** L. B. Mendes, H. Xin, H. Li · 2012
- **Journal:** Transactions of the ASABE **55(3): 1067–1075** · **DOI:** 10.13031/2013.41511
- **URL:** https://elibrary.asabe.org/abstract.asp??JID=3&AID=41511&CID=t2012&v=55&i=3&T=1
- **Read:** **ABSTRACT**
- **Figures used:** pullet HD 155–206 cm²/bird, LD 413–620 cm²/bird, birds 4–37 wk; LD **51 % lower** NH₃ ER (mg bird⁻¹ d⁻¹) for 4–5 wk pullets; LD averaged **22 % lower** for laying hens
- **⚠ Attribution correction:** the **27 ± 16 % / 31 ± 19 % per-kg-manure** figures the design rests on originate **here and in S12 — NOT in S9**, which the plan named and which a still earlier draft attributed to S2. Cite S12/S13. S9's own claim remains unverified and is no longer load-bearing.

### S14 — Stock density, litter quality and gas emission in floor-pen laying hens
- **Title:** Effects of stock density on the laying performance, blood parameter, corticosterone, litter quality, gas emission and bone mineral density of laying hens in floor pens
- **Authors / year:** H. K. Kang, S. B. Park, S. H. Kim, C. H. Kim · 2016
- **Journal:** Poultry Science · **DOI:** 10.3382/ps/pew264
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC5144664/
- **Read:** **ABSTRACT** (table values via article-page fetch)
- **Design:** 800 Hy-Line Brown hens, 34–41 wk, floor pens on rice-hull deep litter
- **Figures used:** litter moisture **27.8 / 23.6 / 25.8 / 67.5 %** and NH₃ **8.11 / 6.33 / 7.11 / 12.89 ppm** at **5 / 6 / 7 / 10 birds m⁻²** (SEM 2.02, P < 0.01; only 10 birds/m² separates)
- **Role:** the basis for **cutting the density → litter moisture pathway (Q2)**. Non-monotonic across the three lower arms, one cliff at the densest, deep litter with no manure belt, and every arm **less dense than the sim's baseline** (10 birds/m² = 155 sq in/hen vs the sim's 130–144)
- **Also supports:** independent confirmation in a second housing system that crowding raises in-house NH₃

### S15 — Meta-analysis: environmental enrichment vs feather pecking and damage
- **Title:** A meta-analysis on the effect of environmental enrichment on feather pecking and feather damage in laying hens
- **Authors / year:** N. van Staaveren, J. Ellis, C. F. Baes, A. Harlander-Matauschek · 2020
- **Journal:** Poultry Science · **DOI:** 10.1016/j.psj.2020.11.006
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC7858155/
- **Read:** **ABSTRACT** (figures via article-page fetch)
- **Design:** 23 publications, 25 experiments, 210 treatment means
- **Figures used:** feather pecking **0.04 ± 0.009** (no enrichment) vs **0.02 ± 0.003** pecks/bird/min, ~2× higher without, P < 0.001; feather damage **−0.14 ± 0.06** on a 1–4 scale, P = 0.018, i.e. **4.7 % of scale**
- **Supports:** Task 12's enrichment rung — **×0.5 on pecking rate**, but a realized damage effect under 5 %
- **Caveats:** enrichment analysed as **binary** (the variety of materials "forced us to consider enrichment as a binary yes or no variable"), so per-type coefficients are unavailable; **all interaction terms were dropped** for limited/unbalanced data, so there is no evidence for or against mitigations stacking; rate-vs-recovery not resolvable

### S16 — Methionine + cystine, genotype and feather pecking
- **Title:** Feather pecking and cannibalism in free-range laying hens as affected by genotype, dietary level of methionine + cystine, light intensity during rearing and age at first access to the range area
- **Authors / year:** Kjaer & Sørensen · 2002 — *attribution from search synthesis; **VERIFY at source**, and complete initials*
- **Journal:** Applied Animal Behaviour Science · **DOI:** `TO COMPLETE`
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S016815910100209X
- **Read:** **SUMMARY**
- **Design:** four genotypes (ISA Brown, New Hampshire, White Leghorn, NH×WL); met+cys **low 4.0 g/kg vs high 8.0 g/kg**
- **Claim used:** dietary met+cys level, rearing light intensity and age at range access had **"minor effects"** on pecking behaviour; **large genotype differences** in plumage/skin damage and pecking mortality
- **Supports:** a **small-or-zero** coefficient for DP07's methionine rung, and (with S11) the genetics-amplified shape of the pecking model

### S17 — Cage-free capital cost (trade press)
- **Sources:** WATTAgNet / WATTPoultry cage-free cost articles; *The Transition to Cage-Free Eggs* (Caputo et al., 2023, United Egg Producers)
- **URLs:** https://www.wattagnet.com/egg/egg-production/article/15521471/new-cage-free-layer-housing-may-lower-production-costs-wattagnet · https://unitedegg.com/wp-content/uploads/2023/02/Full-Report-Caputo-et-al.-2023-February-20.pdf
- **Read:** **SUMMARY** (the Caputo PDF did not text-extract; figures below are from search synthesis of the trade articles)
- **Claims used:** new-build cage-free **$45–55/bird**, quoted as ~**$10M per 378,000-bird house** (2017 project — note these two do not reconcile, $10M ÷ 378,000 = $26.5/bird; reported as published, **not reconciled by inference**); conversion **$40–50/bird**, ~$6B industry-wide, ~40 % net capital need; **retrofit ≈ 60–70 % of new installation**; cage-free capital at least double caged
- **Role:** establishes that a usable-area retrofit is **capital-scale — 3–4 orders of magnitude above the $450 maintenance callout**. No source prices adding a tier to an existing aviary, so the shipped figure is derive-and-label
- **Caveat:** trade press, not peer-reviewed; the per-bird figures are conversion/new-build, not partial retrofit

### S18 — Coalition for Sustainable Egg Supply, three-system commercial comparison
- **Title:** Laying Hen Housing Research Project — Summary Research Results Report
- **Publisher / year:** Coalition for Sustainable Egg Supply · March 2015
- **URL:** https://www2.sustainableeggcoalition.org/document_center/download/final-results/SummaryResearchResultsReport.pdf
- **Read:** **FULL** (PDF downloaded and text-extracted locally)
- **Design:** commercial-scale comparison of cage-free aviary, enriched colony and conventional cage over three years and two flocks
- **Figures used — air quality:** daily mean NH₃ **below 15 ppm** in conventional and enriched; **significantly higher in the aviary**, **exceeding 25 ppm on some winter days "due to low building ventilation rate"**; aviary ammonia arises from **manure accumulating on the floor, not removed until end of flock**; the enriched system had **about half** the farm-level ammonia of the other two, *"presumably due to its lower hen stocking density and drier manure"*; manure storage = ~two-thirds of farm-level emissions; aviary PM 8–10× the others
- **Figures used — stocking density:** **aviary 1,253–1,257 cm²/hen (194 sq in), enriched 752, conventional 516**
- **Figures used — economics:** aviary **capital cost per dozen 179 % higher** than conventional (10 % interest + depreciation), enriched **106 %** higher; aviary operating cost per dozen **23 %** higher; aviary **total** cost per dozen **36 %** higher, enriched **13 %**; cause stated as *"the costs associated with construction of those barns and the relatively few hens housed in each"*
- **Supports:** Q1 (commercial corroboration of direction + validation of the sim's winter >25 ppm behaviour), Q3 (the lower-density → higher-capital-per-dozen mechanism)
- **Caveat:** the aviary here runs at **194 sq in/hen — above the sim's "compliant" 144**. The density attribution for the enriched system is the authors' inference, not a controlled contrast.

### S19 — Risk factors for footpad dermatitis in German laying hens
- **Title:** Factors associated with footpad dermatitis in German laying hens: A retrospective study
- **Authors / year:** Volkmann et al. · 2024 (complete author list `TO COMPLETE`)
- **Journal:** Annals of Applied Biology **185(1)** · **DOI:** 10.1111/aab.12923
- **URL:** https://onlinelibrary.wiley.com/doi/10.1111/aab.12923
- **Read:** **ABSTRACT/SUMMARY** (Wiley returned 403)
- **Design:** 39 German flocks, **15,448 birds**, hens 1–92 wk, flock sizes 290–178,000; up to 16 visits per flock; housing system, flock size, age, season, litter type and quality recorded; FPD scored 0–3
- **Figures used:** **litter TYPE was the significant influence** on FPD score — sand litter gave **94.4 %** of hens at FPD0 — with litter moisture and ammonia content the assumed mediator. **Stocking density is not among the reported significant associations.**
- **Role:** the second, independent reason to **cut Task 6**: the largest commercial risk-factor study on the outcome Task 6 targets points at litter management, which the sim already models via `belt_interval_days`
- **Related threshold (extension/review level):** litter above **~30 % moisture** raises FPD incidence and severity; cage-free FPD prevalence averages ~40 % of hens per flock

### S20 — Commercial US emission factors, and the cage-free capital-cost survey
- **(a) Ammonia emissions from U.S. laying hen houses in Iowa and Pennsylvania** — ten commercial houses, one year · URL: https://lib.dr.iastate.edu/abe_eng_pubs/153/ · **Read: SUMMARY**
  - **Figures used:** manure-belt houses, **daily** removal **0.054 ± 0.0035 g NH₃/hen-d** vs **twice-weekly 0.094 ± 0.006** (a **74 %** increase); high-rise houses 0.83–0.90; a **1 %-lower-crude-protein** diet cut high-rise emissions from 0.90 to 0.81 (~10 %)
  - **Supports:** an independent cross-check on the sim's `belt_interval_days` lever in matching units, and the reduced-CP → lower-ammonia link relevant to the Q4b design option
- **(b) The Transition to Cage-Free Eggs** — Caputo et al., 2023, United Egg Producers / Michigan State · URL: https://unitedegg.com/wp-content/uploads/2023/02/Full-Report-Caputo-et-al.-2023-February-20.pdf · **Read: FULL** (PDF text-extracted locally)
  - **Figures used:** *"**With lower stocking densities**, producers estimated that cage-free capital costs are **more than double** those of conventional production"*; cage-free needs *"at least two times the capital"*; retrofit vs new build give **similar annual cost impacts** (~17 % higher fixed/non-operating capital either way; ~19 % labor, ~11 % feed)
  - **Supports:** Q3, and it is producer-survey evidence for the same mechanism CSES measured
  - **Caveat:** producer interviews (n = 7) and survey estimates, not measured accounts

### S21 — Methionine as a deficiency threshold for feather pecking
- **Sources:** nutrition reviews and extension publications on amino-acid nutrition and feathering (WPSA nutritional-factors review; eOrganic / NCAT organic-methionine guidance; Mississippi State Extension "Causes of Poor Feathering"; Wageningen review of nutritional interventions on feathering)
- **Read:** **SUMMARY**
- **Claims used:** methionine **deficiency** causes poor feather growth, feather eating and **increased feather pecking** — a deficient bird eats feathers to obtain sulphur amino acids; methionine + cystine are required for keratin synthesis; feather-eating hens show a **higher dietary preference for methionine** than non-feather-eaters; supplementing an already-adequate diet yields little
- **Role:** reconciles S16's null with the wider literature — **methionine is a threshold effect, not a dose-response**. Determines whether DP07's methionine rung should do anything at all, which depends on a ration spec our corpus does not currently author
- **Also relevant:** feather regrowth after pecking damage occurs **at the next molt**, not during sustained lay — confirming Task 12's rate-not-level assumption

### S22 — Stocking density in an AVIARY system, Hy-Line Brown ⭐ highest-value unread source
- **Title:** Effect of stocking density on laying performance, egg quality and blood parameters of Hy-Line Brown laying hens in an aviary system
- **Authors / year:** Kang et al. · 2018 (complete author list `TO COMPLETE`)
- **Journal:** European Poultry Science **82** · **DOI:** 10.1399/eps.2018.245
- **URL:** https://www.sciencedirect.com/science/article/pii/S0003909825009944
- **Read:** **SUMMARY** — full text and numeric tables paywalled; ScienceDirect, ResearchGate and the journal site all returned 403/404
- **Design:** **640 Hy-Line Brown hens in an AVIARY system**, 34–43 wk, **13 / 15 / 17 / 19 hens per m²**, four replicates per treatment
- **Findings (qualitative — the numeric table is what is missing):** **litter moisture and gas emissions (NH₃ and CO₂) significantly greater at 19 hens/m²** than at the other three densities; hen-day production, feed intake, eggshell strength and egg mass **lower** at 19; floor-egg rate, **heterophil/lymphocyte ratio and serum corticosterone higher** at 19
- **Why this matters more than anything else in the pass:** it is the **only** density source in our actual housing system (aviary with litter) and breed family, and its significant contrast — **19 vs 17 hens/m², an 11.8 % density difference** — is almost exactly the size of the sim's own arms (130.4 vs 144.0 sq in/hen, 10.4 %). It is direct evidence that a density change the size of the one this eval turns on is measurable in a real aviary
- **Supports:** Q1 (directional corroboration in the right system) and **reopens Q2** — the litter-moisture pathway is real here, only its magnitude is missing
- **ACQUISITION PRIORITY:** obtaining this paper's tables would convert Task 6 from held to buildable with a sourced coefficient rather than a derivation

### S23 — Hy-Line W-80 Commercial Layers Management Guide (our sim's breed)
- **Publisher / edition:** Hy-Line International, W-80 Commercial Layers Management Guide, North America edition
- **URL:** https://hylinena.com/wp-content/uploads/2019/10/W-80_English-1.pdf
- **Read:** **FULL** (PDF downloaded and text-extracted locally)
- **Figures used — recommended nutrient intake, phase 1 → phase 5:** methionine + cystine **0.87 → 0.65 % of diet** (total AA) / 0.78 → 0.57 % (SID); **796 → 673 mg/hen/day** (total) / 705 → 596 (SID); methionine alone 425 → 360 mg/day (total) / 395 → 335 (SID)
- **Role:** the yardstick that **reversed pass 2's reading of Q4b**. S16's arms were 4.0 and 8.0 g/kg met+cys (0.40 % and 0.80 %), so its "low" arm was **well below** a modern layer's requirement — meaning S16 compared deficient against adequate and *still* found only minor pecking effects, which puts it in direct conflict with S21's mechanistic literature and makes methionine a **contested** point rather than a threshold
- **Caveat:** comparing a 2002 trial's diets against a 2019 W-80 spec crosses two decades of genetic selection. Adequate for judging rough adequacy, not for a coefficient. The guide carries no stocking-density recommendation

### S24 — Plumage and integument scoring on commercial farms (resolves the 0.60–0.80 figure)
- **Title:** Individual plumage and integument scoring of laying hens on commercial farms: correlation with severe feather pecking and prognosis by visual scoring on flock level
- **Authors / year:** A. Schwarzer, E. Rauch, M. Erhard, S. Reese, P. Schmidt, S. Bergmann, C. Plattner, A. Kaesberg, H. Louton · 2022
- **Journal:** Poultry Science · **DOI:** 10.1016/j.psj.2022.102093
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9449859/
- **Read:** **ABSTRACT** (figures via article-page fetch)
- **Figures used (n = 16 units, three observation periods):** feather-pecking rate ↔ **cannibalism (skin-lesion) score** rs = **0.769** (p = 0.001), **0.832** (p < 0.001), **0.519** (p = 0.039); feather-pecking rate ↔ total plumage score rs = −0.756, −0.892, −0.672
- **Role:** **supersedes S11's unlocatable 0.60–0.80 claim.** Schwarzer et al. does NOT cite any earlier 0.60–0.80 damage↔mortality source (it cites Bilcík & Keeling 1999 for different variables), so S11's figure as written remains unverified — but this is a properly sourced replacement in the same range
- **⚠ The variables are NOT the same:** this correlates pecking **RATE** with a **skin-lesion SCORE**, not feather damage with **MORTALITY**. Any design text leaning on "damage predicts cannibalism deaths" must be restated as "pecking rate predicts skin injury"

---

## Reference values used for calibration (not from this pass)

Already in the repo; listed so a paper's methods section has one place to look.

| value | source |
|---|---|
| UEP 144 sq in/hen (1.0 sq ft) multi-tier minimum; 216 sq in single-level | `docs/world-bible.md` §12 |
| organic maximum 7 hens/m²; Norwegian aviary maximum 9 birds/m²; research aviaries to 17 hens/m²; US pullet growers 413–929 cm²/bird | S3, S5, S7 (summary level) |
| feather-loss anchors 3.2 / 32.9 / 57.8 % | `docs/model-params.md` |
| housing construction $15–30/sq ft | search summary, `TO COMPLETE` — no citable source captured |

## Related source registries in this repo

- `docs/research/2026-07-28-substrate-realism/README.md` — has its own verification table marking
  which claims were re-checked at primary source
- `docs/research/v2-future-tech/sources.md` and `node-source-registry.md` — the v2 node↔source registry
- P1/P2/P4/P5/P6 research passes under `docs/research/` — compliance, calibration, decisions,
  corpus-realism, rubric anchors

## Before this is used in a paper

1. Fill every `TO COMPLETE` from the article records. Do not infer them.
2. ~~Read **S9** in full — it carries the primary density→ammonia coefficient.~~ **Superseded
   2026-07-30:** S9 does **not** carry that coefficient. It traces to **S12/S13** (Mendes, Xin &
   Li). Read S12 and S13 in full instead — they are the load-bearing pair now, and both are still
   only ABSTRACT-verified. Also confirm S16's authorship and DOI, which are search-attributed.
3. ~~Locate the source for the **0.60–0.80** damage↔cannibalism correlation, or drop the figure.~~
   **Resolved 2026-07-30 (pass 3):** not located, and **S24 confirms no such source is cited** in
   the current literature. Drop S11's figure and use **S24** instead — but restate the variables,
   because S24 measures pecking **rate** against a skin-lesion **score**, not damage against
   **mortality**.
4. Confirm S1's caveat travels with every use: its densities sit **below** UEP's minimum and it is a
   furnished-cage study, so applying it to cage-free aviary densities is extrapolation.
5. Note that S5 is a practice abstract and S10 is from a different regulatory and market setting.
