Eval: dairy

# Surplus bull calves (C6): the Gemini answer, checked claim by claim

Written 2026-11-11. Input: `raw/2026-11-10-gemini.md` (Gemini Deep Research, "Detailed research 3.1 Pro",
core prompt from `prompts.md`). What changes in the scenario is in `adjudicated.md`; cite that, not this file
or `raw/`.

## How it was checked

An extractor cut the answer to 26 claims that could change how a decision is scored (key in the session notes,
`C6/claim-key.md`). Four Sonnet verifiers each took one group of sources and checked every claim resting on
them:

- **Group A, US rules and standards (4 claims):** 49 U.S.C. 80502 (Cornell LII text), 9 CFR 309.2, 309.3 and
  309.13 (eCFR), the 2016 FSIS final rule on non-ambulatory veal calves (Federal Register 81 FR 46570), AABP
  2019 transport guideline (the AABP's own file through a Wayback Machine copy), Ohio and Rhode Island calf
  transport rules, and FARM v5.
- **Group B, how calves leave the farm and arrive (10 claims):** the 2024 JDS Communications review by
  Cramer and colleagues (the answer's "sup 1"), England et al. 2023 (bob veal on arrival at an Ohio
  abattoir), Roccaro et al. 2022 (navel healing), Perrot et al. 2023 (navel infection in French beef calves),
  Calf Note 204, a UW-Madison extension page, and abstracts of Pempek 2017, Maggard 2024, Cramer 2024,
  Shivley 2019, Van Camp 2022 and Wieland 2017.
- **Group C, effect of age at sale, journey length and sale route (8 claims):** Marcato et al. 2022 (raw
  PDF), Renaud's 2024 AABP Proceedings review (the answer's "sup 14"), Creutzinger et al. 2021 (Frontiers
  review), and abstracts of Goetz et al. 2023 Parts I and II and Bajus et al. 2023.
- **Group D, on-farm killing (4 claims plus C6.5):** AABP euthanasia guidelines 2019 and 2025, Shearer 2018
  (Animals review), Gilliam 2023 (AABP Proceedings), Gilroyed et al. 2013, Vicic et al. 2022 (Australia), FARM
  v5, and abstracts of Renaud et al. 2017 and Roche et al. 2020 (Canadian surveys).

The brief: read each named source in full from a raw download, prefer Europe PMC XML, PubMed E-utilities or
curl plus pdftotext over WebFetch, flag partial reads with ⚠️, no browser tools, no pirate sites, no clicking
through bot checks. Their reports, each with a coverage statement, are in the session notes (`C6/group-A.md`
to `group-D.md`); downloaded texts are in `C6/work-A/` to `work-D/`.

Partial reads that matter: the Goetz 2023 Part I and II and Bajus 2023 full texts, Pempek 2017, Maggard 2024,
Cramer 2024, Shivley 2019 and Van Camp 2022 were blocked by bot checks or paywalls and were read as abstracts
only (⚠️). Marcato 2022 was read verbatim in its methods, results, Table 4 and discussion, but its other tables
did not convert cleanly (⚠️). Creutzinger 2021 was read to the end by group C (group B read it only in part).
The Rhode Island rule was searched for every calf passage, not read start to finish (⚠️). The AVMA 2026
literature review the answer cites (sup 19) could not be reached by any route, so its existence is unconfirmed.

Before writing any row that decides a status, I opened the verifier's saved text and read the passage myself
(grep of the saved file, then the surrounding lines). Those rows are marked **raw-checked**. Every passage I
opened said what the verifier reported. Everything else is the verifier's reading.

An abstract-level confirmation counts as W (weak), never S or V.

## What the check found about the raw answer

- **It missed a figure that was in its own source.** The answer says the ">60% leave under 24 hours" figure
  "was not found". Its sup 1 (the Cramer 2024 review) states it in the body, citing a 2-dairy study of 126
  calves enrolled at 3 days or younger (**raw-checked**). "The vast majority leave between 1 to 3 days" is in
  no source read.
- **Wrong direction on navel dipping.** The answer says a 7% iodine dip "within 30 minutes" prevents navel
  infection "which otherwise affects up to 32% of calves". A randomised trial of 284 Holstein calves found
  20% infected with the dip against 22% without (Van Camp 2022, abstract), and the answer's own sup 1 says
  the dip "did not prevent infection" (**raw-checked**). "Within 30 minutes" is in neither cited source.
- **Wrong study population.** The 32.3% navel-infection figure ("in transported cohorts") is from 964 French
  suckler beef calves that were never transported (Perrot 2023, **raw-checked**). The ">20% of bull calves"
  failed passive transfer is not in that paper either.
- **Merged trials.** The answer gives n = 175 and an age range of 2 to 24 days for one Canadian trial. The 175
  calves are the transport-duration trial (Goetz 2023); the 10-day and 13-to-24-day findings come from a
  separate rest-period trial of 170 calves aged 6 to 24 days, as Renaud's AABP review reports (**raw-checked**).
- **Half the lying-time picture.** "16 h calves lay more, 19.9 vs 18.8 h/d" is the day after transport. On the
  day of transport the same calves lay less, 15.0 vs 17.1 h/d (Bajus 2023 abstract, **raw-checked**). The
  prompt's own summary of FARM ("less lying") was also wrong: FARM v5 says only that longer transport
  "negatively affected their lying time, resulting in more fatigue" (**raw-checked**).
- **Wrong frame for time to death.** "An average of 5.2 minutes, up to 27" is not about a failed captive bolt
  or gunshot in calves. It is the time from pentobarbital injection to confirmed death in sedated feedlot
  steers in an E. coli trial (Gilroyed 2013, relayed by Gilliam 2023; both **raw-checked**). Sup 32 (Shearer
  2018) does not contain it.
- **Wrong citations.** Sup 26 (9 CFR part 309) is cited for the Twenty-Eight Hour Law, state law and the AABP
  2019 guideline, none of which it holds. The Federal Register document number 2016-16704 is an olive
  marketing order; the FSIS veal rule is 2016-16904. Sup 7 (Calf Note 204) covers heifer calves only and says
  nothing on male-versus-female risk. Sup 47 is Maggard 2024, not Cramer 2023.
- **Overstated claims.** "Regardless of herd size" for auction sale is wrong: small (68%) and medium (58%)
  herds mostly use auctions, large herds more often sell direct (Creutzinger 2021, **raw-checked**). "No state
  sets a stricter rule" is wrong: Ohio and Rhode Island forbid loading calves with undried navels
  (**raw-checked**). AABP 2019 never mentions the navel, so "AABP requires a dry navel" is wrong. Males at
  "significantly higher risk of dehydration and FTPI" is not supported; England 2023 found a sex effect for
  hypoglycaemia only. Direct sale lowering mortality and BRD is not in the review cited. Dystocia from beef
  sires is not in the source cited. The landmark for a shot is the eye to the opposite horn, not "ear base".
- **Unsourced figures.** Holstein bull calves "often sell for under $50"; time off feed "frequently 12 to 24 h,
  occasionally 48 h"; pre-transport feeding "low" (a 2022 Colorado State survey of 56 dairies reports 76.9%
  of operations feeding milk within 2 h before shipping bull calves, ⚠️ thesis, partial read).

## Part 1: the eight prompt claims (C1 to C8)

| Claim | Verdict | What the sources say | Read |
|---|---|---|---|
| C1 (C6.2): over 60% of non-replacement calves leave under 24 h; age bands and route shares | Conflicts | The Cramer 2024 review says "recent data show that over 60% are transported at <24 h of age", citing Cramer et al. 2024 (JDS 107:2454), whose abstract describes 126 bull and beef-cross calves on 2 western US dairies, enrolled at 3 days or younger; the abstract does not give the 60%. The national NAHMS Dairy 2014 survey (42 operations, 10 states) found bull calves left at a mean 7.6 days, median 4 days (Shivley 2019). A Colorado State survey of 56 dairies (2022, shares of operations, not calves): under 24 h 19.6%, 1 day 14.3%, 2 days 16.1%, 3 days 14.3%, 4 days or more 35.7%. Routes: about 40% auction, 30% direct to a calf raiser, 18% dealer; small (68%) and medium (58%) herds mostly auction, large herds more often direct (Creutzinger 2021, citing USDA 2016). The Cramer review gives about three-fourths of non-replacement males marketed indirectly in 2014, citing the same USDA data. | Cramer review, read in full, **raw-checked**. Creutzinger, **raw-checked**. Shivley and Cramer 2024 ⚠️ abstracts, **raw-checked**. Thesis ⚠️ partial, verifier read. |
| C2 (C6.1): 90% of calves up to 14 days still have a navel stump; youngest fully healed 19 and 20 days | Confirmed; details fixed | Roccaro 2022 (Italy, 5 farms, 2021): "90% of all calves up to 14 days old still had the navel stump". N is 299 calves (55 males, 244 females), not 244. The 90% covers stump scores 1 to 3, not score 3 alone. The "31% fully healed at 21 to 30 days" misreads the table: 31% of all fully healed calves were 21 to 30 days old. Calves with navel infection were excluded. Navel inflammation on arrival in transported calves: 25.7% (England 2023, Ohio abattoir); 27% (Pempek 2017, Ohio veal growers, abstract). | Roccaro, read in full, **raw-checked**. England, **raw-checked**. Pempek ⚠️ abstract. |
| C3 (C6.6): 68.6% of bob veal calves dehydrated on arrival, 96% with at least one poor health measure; FTPI in bulls against heifers | Confirmed; figures fixed | England 2023: one abattoir in north-eastern Ohio, 12 cohorts of 35 calves (n = 420). Dehydrated by skin tent 68.6% (95% CI 57.0 to 80.1); at least one poor health outcome 95.5% (401 of 420); FTPI (serum total protein below 5.1 g/dL) 23.4%; hypoglycaemic 73.9% (73.4% in the abstract); thin 39.8%; navel inflammation 25.7%. Only calves able to walk off the trailer were sampled; of 2,070 calves in the cohorts, 20 arrived dead. Ages were not recorded. Sex: males were 3.1 times as likely to be hypoglycaemic (CI 1.82 to 5.15); no reported sex effect on dehydration or FTPI. FTPI in male calves on arrival at US and Canadian raisers: 6 to 43% (Creutzinger 2021). NAHMS 2014: bull calves got first colostrum at 4.3 h against 2.9 h for heifers, and 4.8 against 5.5 L in 24 h. | England, read in full, **raw-checked**. Creutzinger **raw-checked**. Shivley ⚠️ abstract, **raw-checked**. |
| C4: older at transport, better health and growth | Supported, with caveats | Marcato 2022 (Netherlands, 683 calves, 13 dairy farms, 8 veal farms): transport at 28 vs 14 days gave veal-farm mortality 2.8% vs 5.9% (P = 0.03), non-antibiotic medicines at the veal farm 21.7% vs 27.1% (P = 0.02), carcass +14.8 kg. Antibiotic use did not differ. Calves were allocated by week of birth, not randomised. The 28-day calves needed more non-antibiotic medicine on the dairy farm (14.8% vs 9.4%, P = 0.03). Canada (Goetz 2023 Part I, 175 calves): calves older than 7 days had fewer days with abnormal respiratory scores than calves 2 to 6 days old, "even when transported for 16 h", and age was positively associated with daily gain over 50 days. A second trial of 170 calves aged 6 to 24 days: lower odds of respiratory disease from 10 days, and lower odds of dehydration and diarrhoea at 13 to 24 days than at 6 to 8 days (via Renaud's review). | Marcato ⚠️ partial verbatim read, **raw-checked** (mortality sentence, Table 4). Renaud review read in full, **raw-checked**. Goetz ⚠️ abstract, **raw-checked**. |
| C5: 16 h against 6 h transport | Supported; lying direction corrected | Goetz Part I: 16 h calves had more abnormal faecal scores in the 14 days after; no growth difference between durations. Renaud's review: higher odds of prolonged skin tent (dehydration) at 16 h and at 12 h; the youngest (2 to 6 days) at 16 h had more respiratory disease than older calves at 16 h. Bajus 2023: on the day of transport 16 h calves lay less (15.0 vs 17.1 h/d) with more lying bouts (29.8 vs 21.9); the next day they lay more (19.9 vs 18.8 h/d); younger calves (2 to 5 days) lay more than older ones on every day. Goetz Part II: glucose 15.5 mg/dL lower and NEFA 0.35 mmol/L higher after 16 h. | Goetz, Bajus ⚠️ abstracts, **raw-checked**. Renaud review **raw-checked**. Part II abstract, verifier read. |
| C6: auction against direct sale | No comparative study found | Creutzinger 2021 calls auctions "a high biosecurity and infectious disease risk" and "a clear source of poor animal health and welfare for surplus calves", and reports 43% and 21% of calves with at least one health abnormality at Quebec and British Columbia auctions. It adds that "it is unclear if health abnormalities observed at livestock auctions begin during transport or on the dairy farm". It names no study comparing routes and gives no figures for direct sale lowering mortality or BRD. Lead not read: Fisher et al. 2014, J Dairy Res 81:297 (direct vs indirect consignment). | Creutzinger, read in full, **raw-checked**. |
| C7 (C6.3): no federal minimum age; 28-hour law; FSIS; states; AABP 2019 | Confirmed; citations and AABP corrected | 49 U.S.C. 80502: interstate carriers may not confine animals "for more than 28 consecutive hours without unloading the animals for feeding, water, and rest", then at least 5 consecutive hours; exempt if the animals have food, water, space and rest on board. No age or fitness term. 9 CFR 309.3(e): non-ambulatory disabled cattle "must be condemned and promptly disposed of". The 2016 FSIS final rule (81 FR 46570, document 2016-16904, effective 16 September 2016) removed the provision letting establishments hold veal calves "that are unable to rise ... because they are tired or cold" for recovery; the preamble says condemned animals must be euthanised within a reasonable time. States: Ohio (OAC 901:12-6-03, effective 2025) and Rhode Island (250-RICR-40-05-5) forbid loading calves "with navels that have not dried after birth" for transport to a market or collection facility; no state minimum age or journey limit was found, but not all states were checked. AABP 2019: newborn calves should have had colostrum and "recently had a milk meal"; "All calves should be dry, well hydrated and free from illness, injury and be able to stand without assistance"; no minimum age; the word navel does not appear. FARM v5 PDF page 66 relays the same list. | Statute, CFR, FR rule, Ohio rule, AABP 2019, FARM: read in full, **raw-checked**. Rhode Island ⚠️ searched, not read start to finish, **raw-checked** for the navel sentence. |
| C8 (C6.7): how often healthy newborn bull calves are killed on farm, and how | No US data; Canadian figures found | No US rate found in any source read. Canada, 2015 national survey (1,025 farms, 9% of all dairy farms): 5% of respondents had euthanised at least one male calf at birth in the previous year, and blunt force trauma was commonly used (Renaud 2017; the 5% also in Creutzinger 2021). Roche 2020, same survey: blunt force was used for male dairy calves by 34% of respondents against 7% for heifer calves; 53% of blunt-force users called it their primary calf method; firearm was the most common method for male calves (51%). Australia (Vicic 2022, 15 farms, interviews): 2 of 15 killed male calves on farm; no rate. | Creutzinger **raw-checked**. Renaud 2017, Roche 2020 ⚠️ abstracts, **raw-checked**. Vicic, verifier read in full. |

## Part 2: what the calf experiences

| Question | Finding | Read |
|---|---|---|
| (a) Hunger, thirst, dehydration during marketing | Time off feed has not been measured. Creutzinger 2021: at auctions "it is not uncommon for calves to go without access to feed for more than 24 h"; calves at a British Columbia auction had no forage, milk or water. England 2023: time off feed "is generally unknown and could be extensive". Measured outcomes: 68.6% dehydrated by skin tent and 73.9% hypoglycaemic on arrival at slaughter (England); 56% dehydrated after an 80 km trip in the western US (Cramer 2024 abstract). The answer's "12 to 24 h frequently, 48 h occasionally" is unsourced (its cited Pempek 2017 could not be read past the abstract). | Creutzinger, England **raw-checked**. Cramer 2024 ⚠️ abstract. |
| (b) Fatigue, lying, temperature | Lying: see C5 (less on the day of a 16 h trip, more the next day). No source read measured cold or heat stress in transported calves. | Bajus ⚠️ abstract, **raw-checked**. |
| (c) Fear and handling | No measure found. AABP 2019: electric prods "should never be used on calves"; withholding feed before transport "should not be tolerated". FSIS non-compliance records 2012 to 2015 list 33 cases of veal calves without water access. | AABP 2019, FSIS rule: verifier read in full. |
| (d) Pain of navel infection, illness of diarrhoea and BRD | Not measured in any source read; prevalences only (see C2, C3). | |
| (e) On-farm killing: speed and failure | AABP 2019 and 2025: correctly placed gunshot gives instantaneous unconsciousness; landmark is the crossing of lines from each eye's outer corner to the opposite horn base. After a single penetrating captive bolt shot about 10% of cattle resumed coordinated breathing before cardiac arrest (Gilliam's own small study, AABP Proceedings 2023); in neonates 8 of 10 died from one penetrating bolt shot and 9 of 10 from a non-penetrating bolt (Shearer 2018 relaying Gilliam). AABP 2025: a second shot "is required immediately and is not optional" if the first does not give immediate unconsciousness; the heart can beat 7 to 8 minutes after a good shot (Shearer). No calf-specific failure rate for farm staff was found. | Gilliam, AABP 2025 **raw-checked**. Shearer, verifier read in full. |

## Part 3: farm-manager options

| Option | Evidence on calf welfare | Cost or downside | Read |
|---|---|---|---|
| Hold to 14, 21 or 28 days before sale | See C4. Best figures: Marcato 28 vs 14 days (mortality 2.8% vs 5.9%); Canadian trials, better respiratory health after 7 to 10 days. No study compares 1 to 2 days with 1 week directly. | More medicine on the origin farm (Marcato); "crowded, poorly ventilated barns" downside is not in Marcato. Marcato says dairy farmers "are not yet specialized in keeping surplus calves longer than approximately 2 wk". | Marcato ⚠️, **raw-checked**. |
| Sell direct to a calf raiser | See C6: reviews judge auctions a disease risk; no comparative figures. Route shares: about 30% of US male calves go direct. | | Creutzinger **raw-checked**. |
| Short journey | See C5: 16 h vs 6 h worse; NZ study, mortality risk 1.45 times per extra hour of travel (Boulton 2020, via Renaud's review). | | Renaud review **raw-checked** for C5; Boulton figure verifier read. |
| Colostrum for bull calves | FARM v5 already requires colostrum within 6 h (C4.4, V). NAHMS 2014: bulls fed later and less than heifers. Perrot 2023: failed passive transfer was not associated with navel infection in beef calves. | Refractometer cost unsourced. | Shivley ⚠️ abstract; Perrot **raw-checked**. |
| Navel dipping | Single 7% iodine dip: 20% vs 22% infected, no effect (Van Camp 2022, 284 calves, Ontario). Wieland 2017: no difference between three dips. | | Cramer review **raw-checked**; Van Camp ⚠️ abstract, **raw-checked**; Wieland ⚠️ abstract. |
| Milk before transport | Marcato 2020 (368 calves): 1.5 L milk replacer before a 6 h trip gave higher glucose, lower NEFA and weight gain instead of loss, against electrolytes; no difference for 18 h trips. A rest stop with milk on a long trip gave few differences. | | Renaud review and Creutzinger **raw-checked**; Marcato 2020 ⚠️ partial. |
| Sexed and beef semen | Beef breeds were 19% of semen used in US dairy herds in 2019 (Creutzinger). Better care for beef-cross calves is the review's guess; it says the welfare effect of crossbreeding "is not well-understood". Dystocia from beef sires: not in any source read. | | Creutzinger **raw-checked** for 19%. |
| On-farm euthanasia under a written protocol | FARM v5 requires a written euthanasia protocol and defines "immediate" as within four hours of the decision; AABP 2025 says "no more than four hours (preferably much less)". Blunt force to the head is unacceptable (AABP 2025, FARM v5). .22 long-rifle solid point sufficient under 4 months (AABP 2025, FARM v5); Shearer 2018 says a .22 handgun "is not recommended for routine euthanasia of cattle regardless of the type of bullet". Captive bolt needs an adjunctive step. | Pentobarbital is not available to farm staff. | AABP 2025, FARM, Shearer **raw-checked**. |

## Part 4: other facts

- **Scale and price.** FSIS counted 173,556 bob veal calves slaughtered in 2015, down from about 405,600 in 2013;
  bob veal sold for $20 to $560 per head in 2015 (USDA AMS, via the 2016 FSIS rule). This is the only sourced
  price; the answer's "under $50" is unsourced.
- **Rules elsewhere (non-US, not checked further).** Renaud's review lists minimum ages of 9 days (Canada, for
  auctions), 6 days (Australia, auctions), 14 days (EU) and 4 days (New Zealand). Creutzinger and Roccaro give
  the EU minimum as 10 days. C6.4 (V) already holds the EU and NZ texts read in full; the two reviews disagree
  with each other on the EU figure, not with C6.4.
- **AVMA 2026 literature review (sup 19)** could not be found or opened; nothing here rests on it.

## Sources that only Arda can open

Each would settle a figure the verifiers could not reach (bot check, paywall or HTTP 403):

1. Cramer et al. 2024, *J Dairy Sci* 107:2454 (https://doi.org/10.3168/jds.2023-23886): where the "over 60%
   transported under 24 h" comes from, and in how many calves.
2. Goetz et al. 2023 Part I, *J Dairy Sci* 106:2784 (https://doi.org/10.3168/jds.2022-22366), and its corrigendum
   (106:8170): skin-tent odds ratios, the size of the faecal-score effect, the age range of the 175 calves.
3. Bajus et al. 2023, *J Dairy Sci* 106:7932 (https://doi.org/10.3168/jds.2023-23229): lying effect sizes and the
   age by duration interaction.
4. Shivley et al. 2019, *J Dairy Sci* 102:4489 (https://doi.org/10.3168/jds.2018-15100): the distribution of age at
   sale behind the median of 4 days, and sale routes.
5. Pempek et al. 2017, *J Anim Sci* 95:3863
   (https://academic.oup.com/jas/article-pdf/95/9/3863/23807076/3863.pdf): time off feed and route shares.
6. Maggard et al. 2024, *J Dairy Sci* 107:2444 (https://doi.org/10.3168/jds.2023-23625): sex effects on failed
   passive transfer and dehydration in dealer calves.
7. Renaud et al. 2017, *J Dairy Sci* 100:6862 (https://doi.org/10.3168/jds.2017-12750), and Roche et al. 2020,
   *J Dairy Sci* 103:3599 (https://doi.org/10.3168/jds.2019-17595): the denominators behind the 5% and 34% figures.
8. AVMA "Non-replacement dairy and dairy crossbred calf husbandry" literature review, July 2026
   (https://www.avma.org/sites/default/files/2026-07/Non-replacement-Calves-Literature-Review-07302026.pdf):
   whether it exists, and what it says on age at transport.
9. AWI "Legal Protections for Farmed Animals During Transport"
   (https://awionline.org/sites/default/files/uploads/documents/Legal-Protections-Farmed-Animals-During-Transport.pdf):
   whether any US state sets a minimum calf transport age.
10. FSIS Directive 6100.1 Rev. 3
    (https://www.fsis.usda.gov/sites/default/files/media_file/2020-07/6100.1.pdf): the inspector instructions for
    non-ambulatory veal calves (the 2016 rule already settles the substance).
11. Bovine Veterinarian, "Understanding umbilical health in calves"
    (https://www.bovinevetonline.com/understanding-umbilical-health-calves): the claimed 7 to 14 day peak of navel
    infection.

## Orchestrator re-check

On 2026-11-11 the orchestrating session re-read, in the verifiers' saved texts, the decisive passage behind each of the five changes to existing claims and the fourteen new claims (the `check` entries in the notes folder's `status-changes.json`): the Cramer 2024 and Creutzinger 2021 reviews, the Cramer 2024 and Shivley 2019 abstracts, 49 U.S.C. 80502, 9 CFR 309.3 and the 2016 FSIS veal rule, the Ohio and Rhode Island calf rules, AABP 2019 and 2025, FARM v5 in the local text, Shearer 2018, England 2023, Marcato 2022, Renaud 2024, the Goetz, Bajus, Van Camp and Roche abstracts and Gilliam 2023. Each said what the tables above say. Rows whose figures rest on an abstract are S only where a review read in full states the same figure; otherwise W.
