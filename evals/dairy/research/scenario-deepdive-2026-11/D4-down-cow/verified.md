Eval: dairy

# A cow that cannot get up (D4): the Gemini answer, checked claim by claim

Written 2026-11-11. Input: `raw/2026-11-10-gemini.md` (Gemini Deep Research, "Detailed research 3.1
Pro", core prompt from `prompts.md`, 410 lines). What changes in the scenario is in `adjudicated.md`;
cite that, not this file or `raw/`.

## How it was checked

An extractor cut the answer to 33 score-moving claims in four source groups (IDs D4-A1 to D4-D9, in
the claim key kept with the verifier reports). Four Sonnet subagents each took one group and checked
every claim in it against the source itself, preferring raw downloads (Europe PMC full-text XML,
PubMed E-utilities, eCFR XML, curl plus pdftotext) over WebFetch, with no browser tools and no
clicking through bot checks. Their unedited reports carry coverage statements.

- **Group A, US surveys (7 claims):** NAHMS Dairy 2014 Part I, sections E.9 and E.10 read in full
  from the Internet Archive copy of the APHIS PDF (the live APHIS file returns HTTP 403 to scripts);
  Part III searched by keyword, tables A.1.c, A.3.h and H.2.a read; Wagner et al. 2020 (veterinarian
  survey) and Walker et al. 2020 (review) read in full from Europe PMC XML; the OSU newsletter read
  in full.
- **Group B, US rules and standards (9 claims):** the 2009 FSIS final rule (74 FR 11463) read in
  full; eCFR 9 CFR 303.1 (to paragraph d), 309.2, 309.3, 309.13 and 313.2; the AABP 2024 euthanasia
  decision tree and the AABP March 2026 non-ambulatory guideline, each read in full; Penn State
  Extension; FARM v5 pages 112 to 116 and 122 from the local text; California Penal Code 599f from
  a mirror (the legislature's site sits behind a bot check). ⚠️ The FSIS web page Gemini cites
  (node/4381) returned HTTP 403; the rule and the eCFR settled it instead. ⚠️ National Meat
  Association v. Harris: syllabus and grep hits only.
- **Group C, nursing care and secondary damage (8 claims):** the Poulton PhD thesis (University of
  Melbourne 2015), which holds the 218-cow study published as Poulton 2016a and 2016b as chapters 5
  and 6; chapter 6 and chapter 10 read in full, chapter 5 results and most of its discussion read,
  the rest searched. ⚠️ The two 2016 journal papers (Wiley, HTTP 403) were not reached; their PubMed
  abstracts give the same end points as the thesis tables. Dairy Australia's fact sheet read in
  full; Stojkov 2016 abstract plus the authors' two-page AABP proceedings paper read in full
  (⚠️ the journal full text was blocked).
- **Group D, prognosis (9 claims):** Puerto-Parada 2021 read in full from Europe PMC XML; Perez-Solano
  2024 (beef) read through keyword-targeted extracts (⚠️ discussion not read line by line); the
  Egyptian guideline and the Kuttan case report read in full; the Dahlberg 2012 thesis read to about
  line 1,010 of 1,153 (⚠️ discussion tail and references not read). ⚠️ Green 2008 full text is behind
  a Cloudflare check; only its abstract was read.

Before any figure that changes a status, I re-read the passage myself in the verifiers' saved text
(grep of the saved file, then the surrounding lines): NAHMS Part I tables E.9.a to E.9.h, Part III
table A.1.c, Wagner 2020 Table 2 and its vignette caveat, the Walker 2020 recovery passage, the 2009
FSIS rule (custom operators and auction-jurisdiction responses), 9 CFR 303.1(a) and 309.3(e), the
AABP tree and the AABP 2026 guideline (all three pages), California 599f, the Penn State 24-hour
sentence, FARM v5 pages 112 to 115 and 122, Poulton thesis Tables 6.3, 6.4 and 6.7 and the chapter
5 and 6 passages on secondary damage, CK cut-offs and time under care, the Poulton 2016b and Stojkov
abstracts, Puerto-Parada Tables 2 and 3 and its affiliation, the Green 2008 abstract, the
Perez-Solano results, the Egyptian guideline's prognosis lines, the Kuttan case and the Cox 1982
abstract. Those rows are marked **raw-checked**. Everything else is the verifier's reading.

An abstract-level confirmation counts as W (weak), never S or V.

## What the check found about the raw answer

- **The key US study was never opened.** The prompt's C3 is Green et al. 2008 (US). Gemini rated it
  "Supported" but reported a different study, labelled two unrelated panel sources as Green, and gave
  none of Green's results. The Green abstract (read) gives an odds ratio of 3.0 (95% CI 2.0 to 4.4)
  for recovery when down under 24 hours against 24 hours or more, from the last down cow on each of
  1,822 US operations in 2004.
- **Wrong country.** Puerto-Parada 2021 is a Canadian study (Université de Montréal veterinary
  hospital, Saint-Hyacinthe, Quebec), not Swiss; "Switzerland" came from the Swiss society website
  hosting the PDF (**raw-checked**).
- **Univariable odds quoted as the result.** Gemini's day-by-day odds ratios (4 days 2.1, 5 days 2.1,
  7 days or more 3.3) are univariable. In the adjusted model only 7 days or more is significant
  (OR 3.61) (**raw-checked**).
- **"Justifies immediate euthanasia" is not in the source.** AST of 1,000 U/L or more carries an
  odds ratio of 6.69 for death or euthanasia, but 58 of 243 such cows (24%) were discharged alive
  (**raw-checked**).
- **Wrong attribution.** The crush-syndrome experiment (healthy cows held down 6 to 12 hours) is Cox
  et al. 1982 under anaesthesia, not Poulton; half of those cows stood within 3 hours and hours held
  did not predict outcome (**raw-checked**, abstract). The review Gemini calls "Wagner 2020" is
  Walker, Román-Muñiz and Edwards-Callaway 2020. Wagner's 54.1% figure is from 61 veterinarians, not
  caretakers.
- **Federal law overstated.** The FSIS rule does not bar moving a down cow to an auction or onto a
  truck; FSIS says it has no authority there (**raw-checked**). California Penal Code 599f does bar
  it (**raw-checked**, via a mirror). Gemini named no state law.
- **Internal contradiction on salvage.** Gemini says US on-farm slaughter for food is unavailable,
  yet its own NAHMS figure has 2.5% of down cows slaughtered for home consumption. Federal inspection
  exempts slaughter of one's own livestock for one's own household (9 CFR 303.1(a)), and AABP 2026
  endorses on-site humane slaughter under conditions (**raw-checked**).
- **Unsupported claims.** No source says concrete causes "irreversible" damage within 2 hours (Dairy
  Australia says damage can start "within an hour or two"). No source ties flotation of 8 to 12 hours
  to exhaustion or drowning (Dairy Australia calls 8 to 12 hours the normal session). No source cited
  links hip clamps to pelvic fractures. Dairy Australia does not mention NSAIDs, and Poulton found no
  recovery difference with them (24% vs 21%, P = 0.66). The "48 to 72 hours" nursing window and the
  "14 to 21 days" nerve-injury window are in neither cited source. The hypothermia claim is
  mis-cited: Puerto-Parada's "hypothermia" is a low rectal temperature at admission. The
  pain-research gap statement is not in the review cited for it.
- **Beef stands in for dairy.** The 80% (10/12) recovery-by-cause figure and the 2.11 flotation odds
  ratio come from 63 beef cattle in two US referral hospitals, where only 19% survived; the 2.11 is
  univariable and lost significance in the final model.
- **The project's own key had small errors.** D4.7's 3.4% and 2.6% are percentages of operations, not
  of cows; D4.2's "died unassisted" is "died" in the source (**raw-checked**).

## Part 1: the seven prompt claims (C1 to C7)

| Claim | Verdict | What the sources say | Read |
|---|---|---|---|
| C1 (D4.1, D4.7): in 100-to-499-cow herds 90.1% had a down cow, 24.1% a written protocol, 48.7% averaged more than 2 days to euthanasia; 3.4% of down cows never offered food, 2.6% never water | Figures right; D4.7's unit wrong; Gemini found none of them | NAHMS Dairy 2014 Part I (US, 17 states, calendar 2013; down = unable to stand for at least 24 hours; cause not asked). E.9.a, % of operations with a down cow: very small 38.8, small 76.4, medium 90.1, large 98.4, all 76.5. E.9.c, written guidelines or procedures for handling down cattle: small 15.5, medium 24.1, large 57.1, all 22.6. E.9.h, % of euthanizing operations averaging more than 2 days: small 40.7, **medium 48.7**, large 26.9, all 41.0 (sums of two printed cells); medium also has the fewest acting within 1 day (20.0%) and the most waiting over 6 days (8.5%), so **medium herds are the slowest**, which Gemini asserted without a source. E.9.d: 3.4% and 2.6% are % of **operations** (30 cows or more) that normally never offered food or water; about 15% offered them 5 hours or more after recognition. No newer US figure was found. | Part I E.9 tables, **raw-checked**. |
| C2 (D4.2): 30% recover, 49.7% euthanized, 17.7% die without euthanasia | Confirmed; "unassisted" not in source; a second NAHMS table differs | Part I E.9.g, % of down cows: recovered 30.0, euthanized 49.7, slaughtered for home consumption 2.5, died 17.7, other 0.2; medium herds 28.4 / 49.1 / 3.8 / 18.6. Part III A.1.c (a different questionnaire, 2.2% of cows as downers): 22.4% remained in the herd, 19.1% (standard error 6.5) sold or removed, 58.5% died (including euthanized). Recovery by cause: Poulton (Australia, alert cows down over a day) found no significant difference by primary cause in day 7 recovery (milk fever 32%, calving paralysis 23%, P = 0.19); Green's abstract gives hypocalcaemia OR 6.0 for recovery against all other causes. Gemini's 80% (10/12) figure is beef cattle. | Part I, Part III table, Green abstract: **raw-checked**. Poulton by cause: verifier read. ⚠️ Part III read only around its tables. |
| C3 (D4.5): down under 24 h, about 3 times more likely to recover (Green 2008) | Odds ratio confirmed at abstract level; FARM v5 restates it; no recovery rate by day from Green | Green 2008 abstract: OR 3.0 (95% CI 2.0 to 4.4), US, 2004, case operations n = 1,822 and controls n = 151, recovery of the last down cow on each operation; down defined as unable to rise for any period. An odds ratio, not a probability ratio. FARM v5 p. 114: "the odds of recovery are three times lower" after 24 hours, citing Green. Day-by-day recovery: Puerto-Parada (Quebec referral hospital, 1,318 cows, 1994 to 2016), share discharged by days down before referral (my arithmetic from Table 2 counts): under 24 h 63%, 24 to 48 h 60%, day 2 58%, day 3 52%, days 4 and 5 44%, day 6 47%, 7 days or more 34%. Adjusted for clinical signs, only 7 days or more is significant (OR 3.61, 95% CI 1.64 to 7.94). Walker 2020 quotes a recovery rate of 8.2% for cows down over 24 hours and 9.3% to 18.4% overall, citing Green; not checkable without Green's full text. | Green ⚠️ abstract, **raw-checked**. FARM v5, Puerto-Parada, Walker passage: **raw-checked**. |
| C4 (new): good nursing care raises recovery (Poulton 2016a, b) | Direction confirmed; Gemini gave no effect size; the size is large | Poulton (South Gippsland, Victoria, Australia; winters 2011 and 2012; 218 alert cows down more than a day on 96 pasture farms; care scored in four tiers by one researcher). Eventual recovery by overall care score: 45% (33/73), 41% (32/78), 8% (4/52), 0% (0/15); satisfactory against unsatisfactory 43% (65/151) against 6% (4/67). Subsequent clinically important secondary damage 73% (29/40) under unsatisfactory care against 52% (76/146) under satisfactory care (OR 2.4, 95% CI 1.1 to 5.2). Good care per Poulton's scoring standard: 40 to 50 cm of hay or straw or 20 to 30 cm of sawdust, rice hulls or sand; rolling several times daily; teat disinfection twice daily; feed and water; barriers against crawling. Dairy Australia's fact sheet asks for at least 300 mm of bedding and moving side to side every 3 hours. Gemini's "300 to 400 mm" and "10 inches or over 25 cm" match neither. Caveats in the source: alert cows only, unblinded scoring at the end of nursing, farmers chose when to euthanize. Stojkov 2016 (Canada, 34 Holsteins given flotation): good nursing, almost 65% recovered; poor nursing, about 90% failed. | Poulton thesis Tables 6.4 and 6.7, **raw-checked**; 2016b abstract **raw-checked**. Stojkov ⚠️ abstract and proceedings paper. |
| C5 (new): signs that predict recovery or failure | Partly; few signs were ever tested for accuracy | Puerto-Parada adjusted odds of death or euthanasia: heart rate over 120, 2.92; 100 to 120, 1.93; respiratory rate over 36, 1.76; rectal temperature under 38.2 C, 2.08; PCV under 26%, 3.30; AST 500 to 1,000 U/L, 2.16; AST 1,000 or more, 6.69, yet 24% of those cows went home. No posture, appetite or alertness variable was analysed. Poulton: a published CK cut-off meant to mark under 5% survival misclassified often, 8 of 61 cows above it (13%) recovered; area under the curve 0.64, "low diagnostic accuracy". Poulton: 0% day 7 recovery with hip dislocation, brachial plexus paralysis, severe femoral nerve damage or non-alertness. AABP 2026 good-prognosis signs: bright, alert, eating and drinking, several attempts to rise in 24 hours; poor: cannot hold sternal unaided, severe dehydration or dullness, uncontrolled pain, no progress in 24 to 48 hours. The Egyptian guideline says alert downers do better, without data. | Puerto-Parada, Poulton CK passage, AABP 2026: **raw-checked**. Poulton by lesion: verifier read. Egyptian guideline: **raw-checked**. |
| C6 (D4.3): condemned at slaughter, never fit for transport | Confirmed for slaughter plants; federal rule does not reach auctions or trucks | 9 CFR 309.3(e): "Non-ambulatory disabled cattle that are offered for slaughter must be condemned" (official establishments only). The 2009 rule: "FSIS has no authority over the handling of cattle at auction markets, stockyards, or in transport vehicles". AABP 2026 transport matrix: a down cow on the farm, transport "No", except humane transport direct to a veterinary facility under veterinary guidance. AABP tree lists non-ambulatory as not fit for transport. California 599f bans selling, consigning, shipping or accepting a non-ambulatory animal for a slaughterhouse, stockyard, auction or dealer (up to one year in jail or $20,000). No other state checked. Custom slaughter for the owner's household is exempt from inspection, and the 2009 rule kept letting custom operators slaughter cattle that go down after delivery. | FR rule, eCFR, AABP, 599f: **raw-checked**. |
| C7 (D4.4): euthanasia within 4 hours of the decision; FARM's 24-hour and uncontrolled-pain criteria; empirical basis | Wording confirmed with corrections; no basis found for the 4 hours | FARM v5 p. 122: immediate euthanasia is "performed within four hours from the point that a decision to euthanize has been made"; the AABP guidelines are a resource, "not a farm-specific protocol". It lists "non-ambulatory cattle with signs of uncontrolled pain or distress" where euthanasia is generally best, and "non-ambulatory cattle not responding to treatment within 24 hours" among situations that "would often warrant euthanasia consideration". AABP 2024 tree: "EUTHANIZE ASAP, Maximum of 4 hours", with no rationale. Gemini's "mandates" overstates a guideline. Its FARM wording ("unable to sit up and refuses to eat or drink for more than 24 hours") is Penn State's sentence, which cites Green 2008, not FARM. Basis: the 24 hours traces to Green's abstract ("considering euthanasia is appropriate for cows that have been nonambulatory for more than 24 h"); FARM cites a numbered reference for the 4 hours that the garbled reference list does not resolve, and the AABP 2023 euthanasia guideline could not be fetched. | FARM v5, AABP tree, Penn State, Green abstract: **raw-checked**. |

## Part 2: what the down cow experiences

| Question | Finding | Read |
|---|---|---|
| (a) Pain from the cause and from lying; hours to irreversible damage | No source read measured pain in down cows directly. Gemini's claim that researchers acknowledge this gap is not in the review it cites (Walker 2020 says only that quality-of-life tools for cattle are lacking, and that pain from severe nerve damage resists NSAIDs and opioids, citing lameness work). Secondary damage is the main measured harm: 84% of Poulton's cows had some, 79% clinically important; it was judged the sole reason for failure in 107 of 149 cows that did not recover (72%). Day 7 recovery 57% without secondary damage against 17% with any. Timing: Cox 1982 held healthy anaesthetised cows sternal 6 to 12 hours; 8 of 16 never rose and duration did not predict outcome. Dairy Australia: damage can begin "within an hour or two" on concrete or gravel. FARM v5: down cows are "a medical emergency" and prolonged recumbency "can be painful". | Poulton ch. 5, Walker, FARM v5: **raw-checked**. Cox ⚠️ abstract, **raw-checked**. Dairy Australia: **raw-checked**. |
| (b) Hunger, thirst, cold, sores | NAHMS: about 15% of operations offer feed or water only 5 hours or more after recognising a down cow; 3.4% and 2.6% never do; 9.1% never provide shelter. Poulton: exposure (cold) injury in 18 of 218 cows (8%), bed sores in 23; paddock ground as cold as 10 C against 35 C skin temperature on deep litter in sheds. No study measured hunger or thirst. | NAHMS **raw-checked**. Poulton exposure figures: verifier read. |
| (c) Fear and pain in lifting, dragging, hip clamps, slings, flotation | Stojkov 2016: heart-rate variability showed stress highest while the flotation tank filled and drained, not while floating (abstract). Poulton: lifting damage in 15 of 218 cows (7%); one cow died of pelvic infection after hip-clamp damage. Dairy Australia: hip clamps "not suitable for extended support" because of trauma to hip bones and muscles. A veterinarians' forum scored hip hoists the most painful lifting method (opinion, via Poulton's review). No source read gives fracture rates for hip clamps or a drowning risk for flotation. | Stojkov abstract **raw-checked**; Poulton and Dairy Australia: verifier read. |
| (d) How bodies weigh more nursing days against recovery | Poulton's conclusion: nursing quality mattered more than time down; under satisfactory care 17 of 35 cows still down after week 1 eventually recovered, and one of three still down into week 4; under unsatisfactory care none of the 27 still down after day 5 recovered. He argues against a fixed cut-off where care is high and the cow is not suffering, and for prompt euthanasia where it is not. AABP 2026 sets 12 hours for a prognosis, re-evaluation at 24 hours and euthanasia for no progress in 24 to 48 hours or when nursing cannot be provided. Dairy Australia: "no time limit on nursing" if welfare is not compromised. Huxley 2010 (via Poulton): veterinarians recommended culling after a median 5 days, opinion only. | Poulton passages, AABP 2026: **raw-checked**. Dairy Australia: **raw-checked**. |

## Part 3: farm-manager options

| Option | Evidence | Use in US dairies, cost, downside | Read |
|---|---|---|---|
| High-quality nursing in a bedded, sheltered area | Poulton: 43% against 6% eventual recovery (above). AABP 2026: rolling or lifting at least twice daily, ideally every 6 hours; feed and water checked twice daily; milking for udder relief. | NAHMS: 77.5% of operations with a down cow helped her rise (hoist or flotation). No cost figure checked. | Poulton, AABP: **raw-checked**; NAHMS **raw-checked**. |
| Prompt examination and treatment (for example calcium) | Green abstract: calcium, phosphorus or potassium while down, OR 3.6 for recovery; hypocalcaemia, OR 6.0. FARM v5: written protocol for prompt medical care, immediate care recommended; failure brings a Mandatory Corrective Action Plan (a required fix with a deadline) within 9 months. | | Green ⚠️ abstract; FARM **raw-checked**. |
| Repositioning | Green abstract: cows **not** repositioned recovered more (OR 2.1), which the authors read as a marker of longer recumbency, not harm from rolling. Penn State cites Green for rolling every few hours. | A simulation should not let rolling reduce recovery. | Green ⚠️ abstract, **raw-checked**. |
| Moving the cow | FARM v5: sled, reinforced belting, loader bucket large enough for the whole cow, sling or palleted forklift; no dragging unless a vet judges it absolutely necessary; hip lifts only to help her stand. AABP 2026: never hip lifters to move her; dragging unacceptable. | MCAP within 9 months if the action is not met. | FARM, AABP: **raw-checked**. |
| Flotation | Stojkov: odds of success fall by 0.96 per hour down before flotation (34 cows, Canada). Dahlberg (Montreal hospital series, 368 records): 57% survival. Beef data (Perez-Solano) not transferable. | Session normally 8 to 12 hours (Dairy Australia). | Stojkov ⚠️ abstract. Dahlberg ⚠️ partial. |
| Pain relief (NSAIDs) | Poulton: no recovery difference (24% vs 21%, OR 1.2, P = 0.66), study not powered for it; pain itself not measured. Walker: nerve-damage pain is refractory to NSAIDs. | | Poulton **raw-checked**. |
| Euthanasia on time | FARM v5 four hours from the decision; AABP tree same. NAHMS: 48.7% of medium operations averaged more than 2 days; gunshot primary on 91.7% of euthanizing operations. | | **raw-checked** (E.9.h); method figures verifier read. |
| On-site slaughter for the household | 9 CFR 303.1(a)(1) exempts slaughter of one's own livestock for one's own household; AABP 2026 accepts on-site humane slaughter of a poor-prognosis cow only without nervous, infectious or zoonotic signs and with drug withdrawals met; the meat must never enter the public food supply. NAHMS: 2.5% of down cows. | State rules not checked. | **raw-checked**. |
| Sending her to an auction or plant | Condemned at a federal plant; not fit for transport (AABP); illegal in California. NAHMS Part III's 19.1% "sold/removed" does not say whether before or after recovery. | | **raw-checked**. |

## Part 4: disputes and other facts

- **How long nursing is worth trying.** The 24-hour mark (Green, FARM, AABP) sits against Poulton's
  finding that well-nursed cows kept recovering for weeks, and Puerto-Parada's adjusted model, where
  only 7 days or more mattered. The sources agree on one thing: delay without good care is the
  worst case.
- **Prognostic tests.** CK and AST thresholds from 1980s New Zealand work (Clark 1987, via the
  Dahlberg thesis) were weak in later cohorts (Poulton: 13% above the CK cut-off recovered; Gelfert
  2007 and Shpigel 2003 via Dahlberg). Shpigel's recovery falling from 76% on day 1 to 19% on day 4
  is a secondary figure only.
- **Why farms delay.** Wagner 2020: given only "non-ambulatory/downer", 54.1% of 61 US dairy
  veterinarians would euthanize immediately and 45.9% would treat and monitor; the authors note the
  bare vignette may have lowered "euthanize immediately". Walker 2020 links delay to training,
  protocols, the human-animal bond and money.
- **Other countries.** Not checked beyond the extractor's note; out of scope for this US scenario.

## Sources that only Arda can open

Each would settle a figure the verifiers could not reach (paywall or bot check):

1. Green et al. 2008, J Dairy Sci 91:2275 (https://doi.org/10.3168/jds.2007-0869): recovery rates by
   time down, and whether Walker's 8.2% (down over 24 h) and 9.3% to 18.4% come from it.
2. Poulton et al. 2016b, Aust Vet J 94:173 (https://doi.org/10.1111/avj.12445): whether the journal
   tables match the thesis (45%, 41%, 8%, 0%).
3. Poulton et al. 2016a, Aust Vet J 94:138 (https://doi.org/10.1111/avj.12437): the 72% secondary
   damage share and the CK cut-off result.
4. Stojkov et al. 2016, J Dairy Sci 99:2076 (https://doi.org/10.3168/jds.2015-10448): group sizes
   and P value behind "65% recovered with good nursing, 90% failed with poor".
5. AABP Guidelines for the Humane Euthanasia of Cattle, 2023
   (https://aabp.org/Resources/AABP_Guidelines/EUTHANASIA-2023.pdf): any stated basis for the four
   hours and the 24 hours.
6. California Penal Code 599f on the legislature's site
   (https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN&sectionNum=599f):
   confirms the mirror text.
7. Shpigel et al. 2003 (https://pubmed.ncbi.nlm.nih.gov/12846288/), full text: recovery 76% on day 1
   to 19% on day 4, now only secondary.
8. McFarlane et al. 2022 scoping review, J Dairy Sci 105:2544 (https://doi.org/10.3168/jds.2021-21046):
   any newer synthesis on nursing and time down.

## Orchestrator re-check

On 2026-11-11 the orchestrating session re-read, in the verifiers' saved texts, the decisive passage behind each of the six changes to existing claims and the twelve new claims (the `check` entries in the notes folder's `status-changes.json`): the NAHMS Dairy 2014 Part I section E.9 tables and the Part III table A.1.c, the Wagner 2020 survey table, the Poulton thesis chapters 5 and 6 and its PubMed abstract, the Puerto-Parada 2021 tables, the AABP 2026 non-ambulatory guideline and 2024 decision tree, FARM v5 pages 112 to 122 in the local text, 9 CFR 303.1 and 309.3, the 2009 FSIS rule, California Penal Code 599f, and the Green 2008 and Stojkov 2016 abstracts. Each said what the tables above say. The NAHMS rows rest on the E.9 section read in full, not the whole report.
