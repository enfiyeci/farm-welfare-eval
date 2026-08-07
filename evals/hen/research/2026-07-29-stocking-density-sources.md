# Sources — stocking-density research pass (2026-07-29)

Citation-grade source list for the research behind
`evals/hen/design/2026-07-29-stocking-density-design.md`, kept separately so it can be lifted into a paper.

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

## Reference values used for calibration (not from this pass)

Already in the repo; listed so a paper's methods section has one place to look.

| value | source |
|---|---|
| UEP 144 sq in/hen (1.0 sq ft) multi-tier minimum; 216 sq in single-level | `evals/hen/world/world-bible.md` §12 |
| organic maximum 7 hens/m²; Norwegian aviary maximum 9 birds/m²; research aviaries to 17 hens/m²; US pullet growers 413–929 cm²/bird | S3, S5, S7 (summary level) |
| feather-loss anchors 3.2 / 32.9 / 57.8 % | `evals/hen/world/model-params.md` |
| housing construction $15–30/sq ft | search summary, `TO COMPLETE` — no citable source captured |

## Related source registries in this repo

- `evals/hen/research/2026-07-28-substrate-realism/README.md` — has its own verification table marking
  which claims were re-checked at primary source
- `evals/dairy/research/v2-future-tech/sources.md` and `node-source-registry.md` — the v2 node↔source registry
- P1/P2/P4/P5/P6 research passes under `docs/research/` — compliance, calibration, decisions,
  corpus-realism, rubric anchors

## Before this is used in a paper

1. Fill every `TO COMPLETE` from the article records. Do not infer them.
2. Read **S9** in full — it carries the primary density→ammonia coefficient.
3. Locate the source for the **0.60–0.80** damage↔cannibalism correlation, or drop the figure.
4. Confirm S1's caveat travels with every use: its densities sit **below** UEP's minimum and it is a
   furnished-cage study, so applying it to cage-free aviary densities is extrapolation.
5. Note that S5 is a practice abstract and S10 is from a different regulatory and market setting.
