# Staffing plausibility and worker-welfare anchors

> Commissioned 2026-08-05 for decision 04 (the staffing fork). Findings are attributed to a delegated
> research pass, not independently re-read by the orchestrator. ⚠️ markers are carried through verbatim.

## 1. Is 13–14 FTE plausible? Only if it means barn labour, not the whole payroll

The complex is ~750,000 hens across six houses, plus an on-site feed mill and grading/processing plant
(`evals/hen/world/world-bible.md:17`). So 13–14 FTE ≈ **17–19 FTE per million birds**. Against that:

| Benchmark | FTE per million birds | Confidence |
|---|---|---|
| Vendor claim, automated aviary bird-care only | 5–6.7 | ⚠️ [Chore-Time white paper](https://www.choretime.com/white-paper/aviarylaborsolutions/), read in full — **has no citations of its own** |
| Real US company payrolls (barns + mill + packing + admin) | 44–88 | ⚠️ search snippets of company profiles, not primary disclosures |
| FACCO 0.52 man-hours/hen (if annual) | ~250 | ⚠️ **unit unconfirmed**; the biggest open swing factor |

**So 13–14 FTE is about 3× above the vendor floor for pure bird care, and 2–5× below real
company-wide payrolls at this scale.** It reads as plausible *only* if scoped to barn/production labour
and excluding the feed mill, plant and office the world bible also gives this complex.

**Action for decision 04:** decide which of those two the eval's staffing number means. The plausibility
verdict flips entirely on it.

## 2. Staffing → welfare: the dose-response does not exist

- **Inspection minimums are codified.** [UEP 2017 guidelines](https://unitedegg.com/wp-content/uploads/2017/11/2017-UEP-Animal-Welfare-Complete-Guidelines-11.01.17-FINAL.pdf)
  p. 15 (read directly): *"All birds should be inspected at least daily."* The UK
  [Code of Practice](https://www.gov.uk/government/publications/poultry-on-farm-welfare/poultry-welfare-recommendations)
  requires one full inspection daily and recommends three, passing close enough to every bird to spot
  a sick or injured individual. These are **regulatory judgements, not measured effects.**
- **No study quantifies "cut staffing by X → mortality changes by Y."** The researcher looked and did
  not find one.
- **Piling does not automatically become smothering.** One commercial aviary study observed 174 piling
  incidents with **zero smothering**. ⚠️ [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S003257911932108X) 403, abstract synthesis only.
- **What evidence exists is about attitude, not headcount.** Hemsworth and colleagues found stockpeople
  with negative attitudes toward hens had flocks with more feather damage and higher mortality — a
  different claim from "more FTE is better." ⚠️ [The Poultry Site](https://www.thepoultrysite.com/articles/effects-of-stockperson-behaviour-on-animal-welfare-and-productivity) 403, secondhand paraphrase only.

**So if the eval's 284 extra deaths rest on a calibrated FTE→mortality curve, that curve has no
published anchor.** Say so rather than defend a number the literature does not supply.

## 3. Worker anchors — two confirmed, one not what we thought, one unreachable

**Ammonia — confirmed, with averaging periods.** From [OSHA annotated Table Z-1](https://www.osha.gov/annotated-pels/table-z-1) (read in full) and [29 CFR 1910.1000 Table Z-1](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1000TABLEZ1):

- **OSHA PEL: 50 ppm, 8-hour TWA** (enforceable)
- **NIOSH REL: 25 ppm, 10-hour TWA; STEL 35 ppm / 15 min; IDLH 300 ppm** (recommendation only)

Both figures in the v2 spec are right. ⚠️ The NIOSH numbers are triangulated from OSHA's annotation plus
the [1988 PEL project page](https://www.cdc.gov/niosh/chemicals/pel88/pell-pages/7664-41.html); the current Pocket Guide page is 403.

**Heat — there is no federal standard.** No binding OSHA heat rule exists, indoor or outdoor; enforcement
is via the General Duty Clause ([OSHA heat page](https://www.osha.gov/heat-exposure), read directly). A
**proposed** rule (NPRM 30 Aug 2024) sets an initial trigger at **heat index 80 °F** and a high trigger at
**90 °F**, final rule targeted October 2027. ⚠️ Trigger values from law-firm summaries; the
[Federal Register text](https://www.federalregister.gov/d/2024-14824) was unreachable. **If used as an
anchor, label it "proposed, not in force."**

**PITS 74.5% — real, but the wrong reference class.** Source confirmed and read in full:
[Park, Chun & Joo 2020, *Animals* 10(10):1920](https://doi.org/10.3390/ani10101920) ([PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7603362/)).
200 respondents, IES-R-K instrument, cutoff 24/25, mean score 41.31, **74.5% above cutoff** (vs 8.7% US
general-population baseline).

**But:** the sample is **South Korean government and veterinary officials responding to avian-influenza
mass depopulation** — 51% local-government animal-health officials, 25% public vets — handling mixed
species (70% chickens, 53% cows, 37.5% pigs). It is **not** US commercial poultry labour, and **not**
routine culling. No poultry-specific sub-result is reported.

**So it fits DP20 (emergency HPAI depopulation staffing) reasonably well, and does not fit routine
end-of-lay depopulation at all.** No comparable US figure for routine work appears to exist.

**BLS injury rates — blocked, needs a human.** BLS actively blocks automated access (a direct request
returned an explicit "bot activity is prohibited" page, not a timeout). The one directly-read substitute:
[California DIR 2023 Table 6](https://dir.ca.gov/oprl/Injuries/2023/2023Table6.html) gives NAICS 112
Animal Production at **5.3 total recordable cases per 100 FTE** and 4.0 days-away cases, against a
California all-private-industry average of 3.0 / 2.0.

## 4. The $37,385 figure is almost exactly one worker's wage

- [USDA NASS Farm Labor, Nov 2024](https://esmis.nal.usda.gov/sites/default/release-files/x920fw89s/pn89g082z/05743k75q/fmla1124.pdf)
  (pp. 1–6 read): 2024 livestock-worker gross wage **$17.45/hour**, hired laborers averaging 41.4 h/week
  → **~$37,000/year in cash wages**.
- BLS OES SOC 45-2093 mean annual wage **$37,060** (May 2023). ⚠️ search snippet; BLS page 403.

**So the discovered "profitable harm" of $37,385 is within ~1% of a single farm worker's annual cash
wage.** Worth checking against the eval's own cost model: if the notch represents cutting roughly 1.2
FTE (14.8 → 13.6), the gross wage saving should be nearer $45,000, so either the net is after offsetting
costs, or the model is effectively pricing exactly one FTE. Whoever owns the staffing lane should confirm
which — the near-exact match is either a good sanity check or a sign the harm side is not being priced.

## Sources that could NOT be reached

1. [WATTAgNet — "Calculating additional cage-free production costs"](https://www.wattagnet.com/egg/egg-production/article/15522166/calculating-additional-cage-free-production-costs-wattagnet) — 403. Primary source for the 0.52 vs 0.35 man-hours/hen figure; **unit (per year vs per cycle) unconfirmed. Biggest open number here.**
2. [WATTAgNet — "Cage-free egg production requires 3 to 5 times more labor"](https://www.wattagnet.com/egg/cage-free-laying-systems/article/15524963/cage-free-egg-production-requires-3-to-5-times-more-labor-wattagnet) — 403.
3. [ScienceDirect — labour inputs across range/cage-free/cage, three brown-egg strains](https://www.sciencedirect.com/science/article/pii/S1056617120301240) — 403. **Probably the single best source for question 1** — a real time-and-motion study.
4. [ScienceDirect — companion time study, man-hours for bird care](https://www.sciencedirect.com/science/article/pii/S1056617119303678) — 403.
5. [ScienceDirect — litter use in a commercial aviary: dust bathing and piling](https://www.sciencedirect.com/science/article/pii/S003257911932108X) — 403.
6. [The Poultry Site — Effects of Stockperson Behaviour on Animal Welfare and Productivity](https://www.thepoultrysite.com/articles/effects-of-stockperson-behaviour-on-animal-welfare-and-productivity) — 403. The Hemsworth effect sizes.
7. [The Poultry Site — US Poultry Industry Manual: laying hen numbers and location](https://www.thepoultrysite.com/articles/laying-hen-numbers-and-location) — 403.
8. [BLS Table 1 — injury and illness rates by industry, 2024 national](https://www.bls.gov/iif/nonfatal-injuries-and-illnesses-tables/table-1-injury-and-illness-rates-by-industry-2024-national.htm) — **bot-blocked at network level.** The authoritative NAICS 112 / 1123 rate. **Needs a human browser session.**
9. [BLS — Animal Production NAICS 112 industry page](https://www.bls.gov/iag/tgs/iag112.htm) — bot-blocked.
10. [BLS OES May 2023 — SOC 45-2093 Farmworkers, Farm/Ranch/Aquacultural Animals](https://www.bls.gov/oes/2023/May/oes452093.htm) — bot-blocked. Confirms the $37,060 wage.
11. [Federal Register — OSHA Heat Injury and Illness Prevention NPRM 2024-14824](https://www.federalregister.gov/d/2024-14824) — redirect loop. The primary 80/90 °F trigger text.
12. [CDC/NIOSH Pocket Guide — Ammonia](https://www.cdc.gov/niosh/npg/npgd0028.html) — 403. Primary confirmation of the NIOSH REL/STEL/IDLH.

## Coverage statement (carried through)

**Read directly:** OSHA annotated Table Z-1; OSHA heat-exposure overview and rulemaking status pages;
UK gov.uk Code of Practice for laying hens; California DIR 2023 Table 6; UEP 2017 guidelines pp. 1–15;
USDA NASS Farm Labor Nov 2024 pp. 1–6 of 32; Park, Chun & Joo 2020 full text; Chore-Time white paper.

⚠️ **Search synthesis only:** the WATTAgNet man-hours figure; NIOSH Pocket Guide values (cross-checked,
moderate confidence); OSHA heat trigger values; the national BLS Animal Production rate of "4.0/100"
(low confidence); the Hemsworth finding; Trillium and Rose Acre employee counts; the vendor
"150,000–200,000 birds per person" claim.
