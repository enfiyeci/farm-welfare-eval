Eval: dairy

# H5N1 bird flu in the herd (D5): the Gemini answer, checked claim by claim

Written 2026-11-11 (draft for the orchestrator). Input: `D5-h5n1/raw/2026-11-10-gemini.md` (Gemini Deep
Research, core prompt from `D5-h5n1/prompts.md`, 302 lines). The claim key that cut the answer down to the
claims that move the score is `dairy-verify/D5/claim-key.md` (ids D5-A1 to D5-D8). What changes in the
scenario is in `adjudicated.md`; cite that, not this file or `raw/`.

## How it was checked

Four Sonnet verifier groups each took one set of sources and checked every claim resting on them. The brief:
read each named source in full from the source itself, prefer a raw download (Europe PMC full-text XML,
eCFR, Federal Register text, curl plus pdftotext) over WebFetch, flag partial reads with ⚠️, no browser tools,
no clicking through bot checks. Their unedited reports, each with a coverage statement, are
`dairy-verify/D5/group-A.md` to `group-D.md`, with the saved texts in `work-A/` to `work-D/`.

- **Group A, federal response, reporting and testing rules, herd counts.** aphis.usda.gov and usda.gov
  returned HTTP 403 to scripts, so the verifier read Internet Archive copies of the APHIS pages and
  print-to-PDF copies of APHIS releases. Read in full: the Federal Order of 24 April 2024 and its FAQ, the
  APHIS NAHLN dairy FAQ (July 2025), the APHIS requirements document (updated 21 January 2026), three APHIS
  releases (8 October, 2 and 4 November 2026), a Texas Animal Health Commission release (2 June 2026), the
  CIDRAP article and the January 2025 USDA press release. ⚠️ WebFetch summaries only: the December 2024
  Federal Order (milk testing), the NMTS FAQ, a herd count in Medical Daily. ⚠️ Unreadable: the APHIS case
  table (a live map) and the BEACON page.
- **Group B, compensation and the size of the loss.** Read in full: the FSA ELAP fact sheet (May 2025), the
  ELAP final rule (89 FR 54331, 1 July 2024), Peña-Mosca et al. 2025 (Nature Communications, the Ohio
  herd), the Cornell Chronicle story, the APHIS producer-support flyer (May 2024, from a copy hosted by the
  AABP). ⚠️ The Bullvine category page was read only through searches. ⚠️ Unreachable: the APHIS H5N1 page
  [7] and the USDA ELAP guidance PDF [9] (both "Access Denied").
- **Group C, transport, slaughter, killing and isolation standards.** Read in full: AVMA Guidelines for the
  Depopulation of Animals, 2026 Edition, chapter 3 (Bovids), from the Internet Archive copy (22 October 2026)
  of the full 147-page PDF; 9 CFR 309.1 to 309.3; FARM v5 pages 41, 65 to 68, 73 to 76, 115 to 118 and 120
  to 125 from the local full text; the Calf-Tel author page. ⚠️ Unreachable: the January 2026 AVMA chapter 3
  intro PDF the answer cites, FSIS Directive 6100.1, the FSIS HPAI page and the NMPF page (all HTTP 403).
- **Group D, what the infected cow goes through.** Read in full: the AVMA dairy H5N1 page (Internet Archive
  copy of 22 December 2025; the live page is bot-blocked), the Kamel 2025 review [17], Oguzie 2024 [2],
  Burrough 2024 (main text), the Merck Veterinary Manual chapter on HPAI in cattle (October 2026).
  ⚠️ Partial: the DHS Master Question List [14] (cattle lines only), the EFSA 2025 report [15] (clinical
  signs, case counts and key messages only), the CowPainCheck paper [30] (keyword search only). ⚠️ Abstracts
  only: Olthof 2026 and Rodriguez 2025 (Michigan herds), Proudfoot 2014.

Before any figure that could change a status, I re-read the passage myself in the verifiers' saved text
(grep of the saved file, then the surrounding lines). Those rows are marked **raw-checked**. I read AVMA
chapter 3 myself from section 3.1 to the end of 3.5.2 (`work-C/avmafull/ch3.txt` lines 1 to 1089) and
searched its reference list for the foam papers. ⚠️ I did not read the rest of the reference list, and of the
other AVMA chapters I checked only the swine and poultry ventilation-shutdown headings. Everything not marked
raw-checked is the verifier's reading.

An abstract-level or WebFetch-only confirmation counts as W, never S or V.

## What the check found about the raw answer

- **The answer is right that AVMA 2026 lists foam for cattle, and that contradicts how the scenario was
  summarised.** Chapter 3 lists water-based foam for adult cattle under Tier 2 (methods used only when Tier 1
  methods cannot reasonably be used), applied in a modified rendering trailer (**raw-checked**). The answer
  left out the tier. The existing candidate D5.3 says "no gas, foam-in-barn or ventilation-shutdown method",
  which is literally true, but the prompt and `prompts.md` restated it as "no gas or foam method", which is
  false. No gas method and no ventilation shutdown appear in the bovid chapter.
- **Wrong figures.** FARM v5's fever line is "greater than 103° F", not "102.5°F to 103°F"
  (**raw-checked**). "Direct viral mortality consistently below 20%" is EFSA's morbidity figure; EFSA gives
  mortality averaging 2%, with industry reports up to 15% (**raw-checked**). "$367 over a 28-day viral
  period" is a co-author's quote about milk lost over 60 days by cows that recover (**raw-checked**); 28 days
  is the ELAP assumption. "$737,500 for a 1,000-cow dairy under a 60-day quarantine" is the total for the
  3,876-cow Ohio herd, 776 clinical cows over a 67-day window (**raw-checked**). Recovered cows giving "50%
  for the remainder of their lactation", compensated by ELAP, is not in the ELAP fact sheet, which assumes 7
  days at 50% after 21 days at zero (**raw-checked**).
- **Wrong sources.** The 10 to 20% morbidity "up to 40%" wording is the Merck Veterinary Manual's, not the
  cited review [17], which has no cattle morbidity figure. [28] is a CDC paper on cats. [30] (CowPainCheck)
  contains no H5N1 text. [32] (a calf-hutch vendor's author page) has no isolation content. The $950 per
  cow comes from Peña-Mosca 2025, not from Bullvine or unnamed "Cornell economic models". CIDRAP [11] says
  nothing about processors or culling; the June 2026 recall it mentions was Listeria in soft cheese.
- **Unsupported claims.** "No processor has mandated herd culling" (no source). Failing the testing or
  reporting mandates "disqualifies the producer from federal indemnification" (not in the ELAP fact sheet or
  rule; the real condition is an NVSL-confirmed positive test, and ELAP is a milk-loss payment, not an
  indemnity). FARM isolation of sick animals as "a fundamental, required standard" (FARM has only
  written-protocol and suggestion items, no corrective action). Supportive care as "the universal standard"
  (the Ohio herd gave NSAIDs and fluids only to severe cases, **raw-checked**). Secondary ketosis, fatty
  liver and displaced abomasum as "the actual causes of death or culling" (no source). Febrile cows "cannot
  legally be transported" (9 CFR 309.3 is a plant inspection rule; FSIS Directive 6100.1 was unreadable).
  Isolation causes "social stress, reduced lying, aggression" for sick cows (no source; FARM's own best
  practice on minimising isolation exempts ill animals).
- **Stale or mis-framed rules.** Pre-movement testing "before any interstate movement" was narrowed in
  January 2026: lactating cows from NMTS "Unaffected" states move without a test (**raw-checked**). The
  reporting duty in the April 2024 Federal Order sits on laboratories and state veterinarians, not on the
  farm owner (**raw-checked**). NMTS covering "roughly 65% of national milk production across 28 states" is a
  January 2025 figure, not a current one. NMTS is not "mandatory nationwide surveillance in participating
  states".
- **Correct.** The AVMA "2% or less" quote, the ELAP formula, and the cap: the extractor's guess that the
  Bipartisan Budget Act removed the ELAP limit was wrong; the fact sheet says the 2018 Farm Bill did
  (**raw-checked**). The CIDRAP herd counts (917, 171, 85). "At least 21 states" (APHIS, 2 November 2026).
- **Invented context.** The answer places the modelled farm in San Francisco (claim key note 2); the prompt
  names no place.

## Part 1: the eight prompt claims (C1 to C8)

| Claim | Verdict | What the sources say | Read |
|---|---|---|---|
| C1 (D5.1): no US dairy herd depopulated; response is quarantine, movement controls, testing, milk diversion, ELAP | Supported, re-dated; the cited page is silent | The cited APHIS livestock page (version of 25 September 2026) says nothing on depopulation, quarantine, diversion or ELAP. The APHIS NAHLN dairy FAQ (updated 25 July 2025): USDA pays for "depopulation and indemnity" for poultry, "which is not occurring for detections in livestock". DHS S&T Master Question List (20 August 2025): APHIS "does not currently recommend depopulation of cattle"; infected cattle should get palliative care. APHIS releases of 8 October and 2 November 2026: milk from impacted animals is "diverted from the commercial milk tank or destroyed". Quarantine is a state measure (Texas, June 2026: the dairy "is currently under quarantine"). No report of a whole-herd depopulation in 2025 or 2026 turned up in the verifier's news search; that part is absence of evidence. Individual sick cows are culled (Ohio herd, Part 2). "No processor has mandated culling": no source. | FAQ, DHS, both releases, Texas: **raw-checked**. News search: verifier only. |
| C2 (D5.2): most recover with supportive care; death plus culling 2% or less (AVMA, December 2025) | Quote confirmed; the figure is an average relayed from USDA, and single herds lose much more | AVMA page, "Last updated: December 16, 2025": most affected animals "reportedly recover with supportive treatment, and the mortality/culling rate has been low at 2% or less on average". EFSA 2025 traces it to a USDA national epidemiologic brief (morbidity under 20%, "mortality and culling was up to 2% on average") and adds industry reports of "up to 15% mortality". Merck (October 2026): average mortality under 5% across herds (USDA studies). Ohio herd (Peña-Mosca 2025, read in full): of 777 clinical cows, 6.8% died or were euthanized and 31.6% were culled within about three weeks of diagnosis on average, 7.7% of the whole herd. Michigan (Olthof 2026, abstract): clinical cows had 1.74 times the hazard of death and 2.61 times the hazard of culling. Recovery: clinical phase 7.9 days on average in Ohio; milk stayed 8.3 to 14.3 kg/day below unaffected cows for at least 77 days. | AVMA, EFSA, Merck, Peña-Mosca: **raw-checked**. ⚠️ AVMA live page after December 2025 not reached. ⚠️ USDA brief not read. ⚠️ Olthof abstract. |
| C3 (D5.4): 10 to 20% of cows show signs (Burrough 2024; Choices) | Supported as an average; herds range 10 to about 30% | Merck (October 2026): "up to 40%, with an average range of 10–20%"; within-herd morbidity "generally < 20%"; up to 40% of lactating cows in some outbreaks. Burrough 2024: "≈10%–15% illness and minimal death" on affected Texas and Kansas farms. Ohio: 20.0% (777 of 3,876) over 24 days; 776 of 777 were lactating; 485 of 637 sampled cows (76.1%) had antibodies without clinical signs, so most infections are silent. Michigan: 28.3% of lactating cows (Olthof 2026) and 32% (Rodriguez 2025), abstracts. Dry cows, heifers and calves: milder or subclinical (Merck; Peña-Mosca: 17 of 42 dry cows seropositive, 1 clinical). The Choices article was not checked. | Merck, Burrough, Peña-Mosca: **raw-checked**. ⚠️ Michigan abstracts. |
| C4 (D5.5): about 1,166 herds in 19 states by July 2026 | Partly; official count unreadable | CIDRAP (27 August 2026, citing APHIS): 917 herds in 2024, 171 in 2025, 85 so far in 2026; the 1,173 total is the answer's sum. APHIS release of 2 November 2026 (Indiana): "a total of 21 states". APHIS release of 8 October 2026 (first Washington herds): "a total of 19 states", so Indiana alone would make 20; the two releases do not reconcile. The July figure of "over 1,166 herds across 19 states" is in Medical Daily (WebFetch only). Detection route: Indiana was found by NMTS bulk-milk testing; the Washington herds, which had passed NMTS testing, and the Texas herd (May 2026) were found after cows fell sick. | CIDRAP, both APHIS releases: **raw-checked**. ⚠️ APHIS case table unreadable; Medical Daily WebFetch only. |
| C5 (D5.3): no gas, foam or ventilation-shutdown method for cattle at any AVMA tier | **Contradicted for foam**; true for gas and ventilation shutdown | AVMA 2026 Edition (Version 2026.0.1), chapter 3. Tier 1: commercial or private humane slaughter ("if the reason for depopulation does not present a human food safety concern, animals are fit for transport"), barbiturates (not feasible for large numbers), close-range gunshot, penetrating and nonpenetrating captive bolt ("preferred methods for the killing of adult cattle and calves"; penetrating recommended for adults). Tier 2: long-range gunshot, captive bolt poll shot, electrocution ("unlikely" to be usable), **water-based foam**: "for adult cattle was investigated by Capria et al and determined to be an efficacious method", in "a modified rendering trailer" with National Veterinary Stockpile equipment. AVMA adds that time to unconsciousness is unknown ("No such data exist yet for cattle") and "water-based foam will not induce immediate unconsciousness in comparison to PCB and gunshot". Tier 2 means methods "considered only when the circumstances of the emergency constrain the ability to reasonably implement a Tier 1 method". Tier 3: oral toxins. No inhaled (gas) method and no ventilation shutdown anywhere in chapter 3, though its introduction says "inhalant methods may be used" in general. Ventilation shutdown plus heat appears only for swine (Tier 3) and poultry (Tier 2). Foam is not validated in calves. Moribund or non-ambulatory animals are "killed in place" by the most practical humane method. The 2019 edition did not list foam for cattle (Capria 2023, describing it). | Chapter 3: **raw-checked**, read by me from 3.1 to 3.5.2. VSD headings in the swine and poultry chapters: **raw-checked** (headings only). Capria abstract: **raw-checked**. ⚠️ The January 2026 chapter 3 intro PDF the answer cites was unreachable. |
| C6 (new): reporting and testing rules | Partly; the reporting duty is on labs and state vets | Federal Order, 24 April 2024: before interstate movement dairy cattle need a negative influenza A test at a NAHLN lab; "Laboratories and state veterinarians must report positive Influenza A" results to APHIS; owners of herds whose cattle test positive must give epidemiological information. Order FAQ: noncompliance "carries a range of criminal and civil penalties" under the Animal Health Protection Act. APHIS requirements (updated 21 January 2026): lactating cows from NMTS "Unaffected" states move interstate without testing; others still need a test; "Lactating dairy cattle that have clinical signs are ineligible for interstate movement or movement to slaughter"; a herd with a positive sample cannot move lactating cows interstate for 30 days. APHIS releases ask producers to "immediately report" livestock with clinical signs to the state veterinarian (a recommendation). The December 2024 order requires raw milk samples to be shared on request (WebFetch only). State reporting rules were not checked. | Order, FAQ, requirements, releases: **raw-checked**. ⚠️ December 2024 order WebFetch only. |
| C7 (new): ELAP and other payments | ELAP confirmed; other payments confirmed as of May 2024 | ELAP fact sheet (May 2025) and final rule: per cow removed from milking for confirmed or suspected H5N1, in a herd with at least one positive test confirmed by APHIS at NVSL; 21 days of no milk plus 7 days at 50%; per-head rate from the monthly NASS all-milk price, times eligible cows, times producer share, times 90%; April 2024 example $367.55 per cow. "Payment limitation does not apply to ELAP benefits" (2018 Farm Bill); average AGI above $900,000 disqualifies. The rule says the payments "will encourage testing". APHIS flyer APHIS-24-025 (May 2024), for up to 120 days after confirmation: veterinary costs up to $10,000 per premises, biosecurity planning up to $1,500, heat treatment of waste milk up to $2,000 a month and $8,000 total, protective equipment up to $2,000 a month. The October 2026 APHIS release says only that "financial assistance is available". | Fact sheet, rule, flyer, release: **raw-checked**. ⚠️ Whether the 2024 amounts still apply was not checked (APHIS page [7] unreachable). |
| C8 (new): fever above 103 F unfit to transport; FSIS and APHIS rules | Confirmed for FARM; the federal line is 105 F, and it is a plant rule | FARM v5, PDF pages 67 and 68: "Do not transport animals with conditions that will not pass pre-slaughter inspection", including "Fever greater than 103° F". 9 CFR 309.3(c): cattle at 105 °F or higher "shall be identified as U.S. Condemned"; 309.3(e): non-ambulatory disabled cattle offered for slaughter "must be condemned". No federal text read bans transport of a febrile cow. APHIS: clinical lactating cows are ineligible for interstate movement or movement to slaughter (C6). Slaughter is AVMA Tier 1 only if animals are fit for transport. | FARM, 9 CFR, APHIS: **raw-checked**. ⚠️ FSIS Directive 6100.1 unreadable. |

## Part 2: what the infected cow experiences

| Question | Finding | Read |
|---|---|---|
| Clinical signs | Fever up to 105 °F (Oguzie 2024, one Texas farm); 39 to 42 °C (Merck). Sudden milk drop with thick, colostrum-like milk; reduced feed intake and rumination; lethargy, dehydration, dry or loose feces; mild respiratory signs in most reports (EFSA, Peña-Mosca), though DHS and Merck also list respiratory distress. EFSA lists neurological signs and abortions among signs seen as the outbreak widened; Merck calls abortions "anecdotally reported"; Olthof 2026 (abstract) found no difference in abortion odds. Not every sick cow has udder lesions (Burrough). | Oguzie, Merck, EFSA lines: **raw-checked**. Burrough, DHS: verifier read. |
| How hard and how long | Ohio herd: rumination fell by an average 160 min/day (lowest 12 days after the first herd case); milk fell from about 36 to 11.6 kg/day two days after diagnosis, rose to 20.8 to 24.0 kg/day in the next two weeks, and stayed 8.3 to 14.3 kg/day below unaffected cows for at least 77 days; clinical phase 7.9 ± 9.3 days, hospital pen 5.1 ± 9.3 days. Milk began falling 5 days before the farm diagnosed the cow. Cumulative loss 901 kg per cow over 60 days. DHS: signs "peak in about 3 to 4 days and last 10-14 days" (initial reports, herd level). USDA field data via EFSA: signs up to 21 days (average 6). Michigan (abstract): still 4.6 kg/day down at 224 days. | Peña-Mosca, DHS line: **raw-checked**. EFSA durations: verifier read. ⚠️ Michigan abstract. |
| Pain or distress | **Not measured.** No H5N1 study read uses a grimace scale, pressure algometry, lying time or a pain-relief response; they use rumination, milk, fever and clinical scores. The udder lesion is a severe mastitis (Peña-Mosca; Burrough: "moderate acute multifocal neutrophilic mastitis"). Bacterial clinical mastitis is painful and severe cases cause hyperalgesia (EFSA 2023 dairy, already S as A5.1), so mastitis is a reasonable proxy; "highly analogous to coliform mastitis" is the answer's own inference. A Europe PMC keyword search found no H5N1 pain study (not exhaustive). | Verifier read; mastitis-pain passage already checked in `checked-findings.md`. |
| Does supportive care help? | Merck (October 2026): "Treatment consists of supportive care", centred on hydration, rumen support and fever control (hay, oral drench and IV fluids, probiotics, B vitamins, flunixin per label). DHS: palliative care recommended. **No trial was found** testing whether it shortens illness or lowers deaths. Ohio: NSAIDs and fluids "provided only in animals with more severe clinical signs". The claim that it prevents ketosis, fatty liver and displaced abomasum, the "actual causes of death", has no source. | Merck, Peña-Mosca: **raw-checked**. DHS: verifier read. |
| Quarantine and isolation effects on the herd | No study found. The cited vendor page has nothing. FARM v5 page 41: isolation of cattle causes stress and should be minimised, with exceptions "when animals are ill". Proudfoot 2014 (abstract): ill cows seek a secluded corner after calving. Ohio: the farm isolated sick cows in a hospital pen, but the virus still spread through the herd in about three weeks. | FARM p.41 grep, Peña-Mosca: **raw-checked**. ⚠️ Proudfoot abstract. Cornell: verifier read. |

## Part 3: farm-manager actions

| Action | Evidence | Cost or downside | Read |
|---|---|---|---|
| Isolate sick cows in a hospital pen | Recommended, not required: APHIS "recommends isolating any sick cattle"; FARM's biosecurity standard lists separating sick animals as a suggestion and "is not associated with a corrective action". No effect size; in Ohio isolation did not stop spread. | None measured; FARM exempts ill animals from its minimise-isolation advice. | **raw-checked** |
| Supportive treatment | See Part 2. Veterinary costs reimbursable up to $10,000 per premises (May 2024). | Handling for drenching or IV fluids (unsourced). | **raw-checked** |
| Divert, heat-treat or dispose of milk; no raw milk to calves or cats | Dairies must send only milk from healthy animals for human consumption (APHIS). FDA recommends discarding milk from symptomatic cows and "strongly encourages" heat treatment before feeding calves or farm cats; these are recommendations. APHIS paid up to $2,000 a month for waste-milk heat treatment (May 2024). | Lost milk (ELAP covers about 24.5 cow-days of normal yield per cow, against 901 kg measured over 60 days in Ohio). | APHIS, FDA text in APHIS requirements: **raw-checked** |
| Report and test | Labs and state vets must report positives; farm reporting is recommended. Testing paid by APHIS at NAHLN labs; sample collection and shipping not paid. A voluntary Dairy Herd Status Program lets herds use weekly bulk-milk samples instead of pre-movement tests. | ELAP and APHIS support need an NVSL-confirmed positive, so hiding forfeits them. | **raw-checked** |
| Stop movement off the farm | APHIS recommends moving no animals off a premises with clinical animals; clinical lactating cows are ineligible for interstate movement or movement to slaughter. The Ohio herd was infected after 42 apparently healthy lactating cows arrived from Texas; Washington's herds came from Idaho, likely by cattle movement. | Keeps unsaleable cows on the farm. | **raw-checked** |
| Cull sick cows | Ohio culled 31.6% of clinical cows, on average 20.6 days after diagnosis (after the clinical phase); 6.8% died or were euthanized. A febrile cow fails FARM's transport rule; at 105 °F it is condemned at slaughter. Killing on farm: FARM lists gunshot, captive bolt with a second step, and intravenous injection by a vet; AVMA has no special method for moribund animals beyond "the most practical humane method". | Replacement cost $1,877 net per early-removed cow ($3,000 springer less $1,123 slaughter price; Peña-Mosca). Of the removals, 43 deaths and 177 culls were attributable to the disease, above background. | Peña-Mosca, FARM transport, CFR: **raw-checked**. FARM p.124: verifier read. |
| Vaccination | Not checked by any group (not score-moving per the claim key). | | |

Loss per case: $950 per clinical cow ($335 expected milk loss plus $615 expected replacement cost), $737,510
for the Ohio herd; with USDA's lower replacement price, $731 per cow (Peña-Mosca, **raw-checked** for $950
and $737,510). ELAP's formula pays about 81% of the measured 60-day milk volume and nothing for death or
replacement (group B's arithmetic, not raw-checked).

## Part 4: other facts

- **Most infections are silent.** In Ohio, 76.1% of sampled cows had antibodies without clinical disease,
  and subclinical cows kept normal milk yield (**raw-checked**). A farm that watches only sick cows misses
  most infected animals.
- **Detection is incomplete.** The Washington herds passed routine NMTS bulk-milk testing and were found
  only after cows fell sick (APHIS, 8 October 2026, **raw-checked**). NMTS covered 28 states and nearly 65%
  of US milk in January 2025 (press release, verifier read); no 2026 coverage figure was found.
- **Genotype.** The Indiana herd (November 2026) and the Washington herds were B3.13 (APHIS releases).
- **Ohio's economic text is internally inconsistent**: "$932 per clinically affected cow" in one section,
  $950 in the abstract and Table 2 (group B). Use $950.
- Not checked (not score-moving): reinfection, vaccine status, other countries' plans, worker PPE costs.

## Sources that only Arda can open

1. APHIS "HPAI Confirmed Cases in Livestock",
   https://www.aphis.usda.gov/livestock-poultry-disease/avian/avian-influenza/hpai-detections/hpai-confirmed-cases-livestock :
   the current cumulative herd count and state list with its date (settles D5.5 and the 19 against 21
   states question).
2. APHIS national epidemiologic brief, May 2024,
   https://www.aphis.usda.gov/sites/default/files/20240501-hpai-dairy-epi-brief.pdf : the primary of the
   "morbidity under 20%, mortality and culling up to 2%" average, its date and how many herds it covers
   (would move D5.2 back to V or to C).
3. APHIS H5N1 HPAI page [7], https://www.aphis.usda.gov/h5n1-hpai : whether the May 2024 producer payments
   (veterinary $10,000, biosecurity $1,500, milk heat treatment $8,000) still apply in November 2026.
4. FSIS Directive 6100.1 Rev. 3, https://www.fsis.usda.gov/policy/fsis-directives/6100.1 : anything on
   febrile cattle or cattle from a quarantined herd beyond 9 CFR 309.
5. AVMA chapter 3 intro PDF, January 2026,
   https://www.avma.org/sites/default/files/2026-01/CHAPTER3-BOVIDS-INTRO.pdf : whether it lacks the methods
   section, which would explain why the earlier read recorded no foam method.
6. AVMA dairy H5N1 page (live),
   https://www.avma.org/resources-tools/animal-health-and-welfare/animal-health/avian-influenza/avian-influenza-virus-type-h5n1-us-dairy-cattle :
   whether the "2% or less" statement changed after December 2025.
7. NMPF H5N1 resources, https://www.nmpf.org/resources/hpai/ : its lines on isolation, raw milk to calves
   and cats, and bulk-tank testing for ELAP.
8. Olthof et al., J Dairy Sci 2026;109(3):2944, https://doi.org/10.3168/jds.2025-27463 : Michigan
   morbidity, death and culling hazards, milk loss at 224 days (full text).
9. Rodriguez et al., J Dairy Sci 2025;108(6):6349, https://doi.org/10.3168/jds.2025-26377 : Michigan
   cumulative incidence and the 132-day yield recovery (full text).

## Orchestrator re-check

On 2026-11-11 the orchestrating session re-read, in the verifiers' saved texts, the decisive passage behind each of the five changes to existing claims and the seven new claims (the `check` entries in the notes folder's `status-changes.json`): the APHIS dairy HPAI FAQ, the DHS brief, the APHIS news releases of 8 October and 2 November 2026, the AVMA HPAI page (archived copy), the EFSA 2025 risk text, the Ohio herd paper (Nature Communications 2025), the Merck page and the Emerging Infectious Diseases report, the April 2024 Federal Order and its FAQ, the January 2026 interstate-movement requirements, the ELAP fact sheet and Federal Register rule, the May 2024 APHIS support flyer, FARM v5 pages 65 to 68, 9 CFR 309.3, and AVMA 2026 chapter 3 (sections 3.4.2.2 and the Tier 2 definition). Each said what the tables above say. The absence of any reported herd depopulation (D5.1) rests on not finding one; the verifiers' news search left no saved text.
