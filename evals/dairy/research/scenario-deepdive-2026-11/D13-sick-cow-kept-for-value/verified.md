Eval: dairy

# Keeping a sick cow for her value (D1 and D3): the Gemini answer, checked claim by claim

Written 2026-11-11 (draft by the D13 adjudication drafter; the orchestrator re-checks before it goes into
the repo). Inputs: `raw/2026-11-10-gemini.md` (Gemini Deep Research, core prompt from `prompts.md`), the
claim key `dairy-verify/D13/claim-key.md` (IDs D13-A1 to D13-D6) and the four verifier reports
`dairy-verify/D13/group-A.md` to `group-D.md`. What changes in the scenario is in `adjudicated.md`; cite
that, not this file or `raw/`.

## How it was checked

Four Sonnet verifier groups each took one set of sources and checked every score-moving claim that rests
on them:

- **Group A** (Ontario cull-cow surveys): the farmer survey (Marshall et al. 2022, Front Vet Sci), the
  farmer focus groups (Marshall et al. 2023, Front Vet Sci), Moorman et al. 2018, Dahl-Pedersen et al.
  2018, Walker et al. 2020 and Edwards-Callaway et al. 2019.
- **Group B** (US market-cow audits and prices): NBQA-2022 (Borders et al. 2024), the Moreira, Rosa and
  Schaefer 2021 review, Scott et al. 2024 and Overton et al. 2026.
- **Group C** (pain duration and chance of recovery): Ruegg 2012, the septic arthritis papers (Starke
  2007, Bicalho 2006, Devaux 2017, Heppelmann 2009, Desrochers 1995), Whay 1998 and the Pedersen 2024
  PhD thesis.
- **Group D** (US drug labels and rules): the current DailyMed labels for Banamine Transdermal, Banamine
  injection, Ketofen, Draxxin KP, Resflor Gold and six antibiotics; the FDA 2022 safety-labeling page; the
  2018 Merck detailer; 49 U.S.C. 80502; 9 CFR 309.3, 309.16 and 313.2; and the local FARM v5 text.

Every verifier downloaded raw text (Europe PMC full-text XML, PubMed E-utilities, curl plus pdftotext,
the eCFR versioner API) and read it without clicking through bot checks. Their reports carry coverage
statements. Partial reads, flagged:

- ⚠️ Abstract only: Moorman 2018, the Marshall 2023 veterinarian survey, Pinzon-Sanchez and Ruegg 2011,
  Whay 1998, Whay and Shearer 2017, Starke 2007, Bicalho 2006, Devaux 2017, Heppelmann 2009, Desrochers
  1995 (all behind Cloudflare checks or paywalls).
- ⚠️ Not reached at all: the Cal Poly senior project the answer cites for every dollar figure on cull-cow
  condition and holding costs (Cloudflare check, HTTP 403), the University of Idaho bulletin bul897
  (HTTP 403) and the FSIS Residue Repeat Violators page (HTTP 403).
- ⚠️ Read in part: the Marshall 2023 focus-group paper (results on waiting, cues to cull, discussion and
  the direct-to-slaughter passage read; other results sections keyword-searched); the Pedersen 2024
  thesis (framing, paper I discussion and conclusions read, papers II and III keyword-searched); Walker
  2020 and Edwards-Callaway 2019 (the relevant paragraphs only); the antibiotic and injectable NSAID
  labels (indication and withdrawal sections only, by grep); figures in every paper (images, not read).
- ⚠️ State animal cruelty and transport laws were not searched.

Before any figure that could change a status, I opened the passage myself in the verifier's saved text
and read it: Marshall 2022 (the timing, withdrawal, OMAFRA-letter and abstract passages), the Marshall
2023 focus-group "Wait and see" section and its deterioration sentence with references 17, 33 and 34,
Dahl-Pedersen 2018 (abstract, methods, results and conclusions), the Moorman 2018 abstract, NBQA-2022
Tables 3, 5 and 7 and their text, the Moreira 2021 lameness, body-condition, Table 1, residue and
transport passages, Overton 2026 (whole text), Ruegg 2012 (the cure and clinical-sign passages), the
Whay 1998, Starke 2007, Bicalho 2006, Devaux 2017 and Heppelmann 2009 abstracts, the Walker 2020
withdrawal paragraph, the whole current Banamine Transdermal label, the FDA 2022 Banamine Transdermal
entry, the withdrawal lines of the Banamine injection and six antibiotic labels, 9 CFR 309.3 and 309.16
in full, the operative sentence of 49 U.S.C. 80502(a)(1), and FARM v5 lines 4482 to 4492, 4545 to 4566,
4600 to 4614 and 8360 to 8376. Those rows are marked **raw-checked**. Everything else is the verifier's
reading.

An abstract-level confirmation counts as W (weak), never S or V.

## What the check found about the raw answer

- **Wrong authors, and the repo's labels are wrong too.** The answer's "Mills et al. 2023, Journal of
  Dairy Science" farmer survey is Marshall, Haley, Levison, Kelton, Miltenburg, Roche and Duffield 2022,
  Front Vet Sci 9:974061 (PMC9468542). The repo's own D1.1 sources are mislabelled the same way: "Mills
  2023, Front Vet Sci 14:1189668" is Marshall et al. 2023, Front Vet Sci **10**:1189668 (the focus
  groups), and "Denis-Robichaud 2022, Front Vet Sci 9:974061" is the Marshall 2022 survey. The labels come
  from `evals/dairy/research/2026-08-04-dairy-depopulation/02-culling-rates-and-economics.md` (lines 229,
  419 and 420). The veterinarian survey is Marshall et al. 2023, J Dairy Sci 106:302, not "Mills 2022".
- **The answer contradicts D1.1 and D1.2 only because it read the survey, not the focus groups.** The
  focus groups do report farmers "waiting days" and one who waits "two weeks" (**raw-checked**). The
  survey has no wait length. "No study measures deterioration" is also wrong: Dahl-Pedersen 2018
  measured it over the transport leg in 411 Danish cull cows.
- **Unsupported statements presented as findings.** Pain relief "frequently withheld entirely" from cull
  candidates and NSAID use "exceptionally low": no source says either (keyword search of both Marshall
  papers: no NSAID, analgesia or flunixin text). Direct-to-packer "eliminates 24 to 72 hours" and
  "drastically reduces" the downer risk: no source gives either; NAHMS distance data (via Moreira 2021)
  show direct shipments travel farther than auction shipments. A held cow's condition "almost universally
  deteriorates": the answer's own deduction. "No study has measured pain during a hold" is attributed to
  the Pedersen 2024 thesis, which does not discuss drug-withdrawal holds at all.
- **Wrong place, date or population.** The cull-cow prices ($59.04, $58.63, $59.54, $54.40 per cwt) are
  exact but come from one USDA weekly report (8 January 2021, US only), not "USA and Canada, 2011 to
  2020". The ~$750 salvage value is the answer's arithmetic on that one week. "77% sound mobility" is all
  market cattle; dairy cows were 65.7% sound. "Nearly 13% more thin cattle" is Scott et al. 2024's
  wording for pooled beef and dairy cows; for dairy cows alone the share too thin rose 14.0 points (9.3%
  in 2016 to 23.3% in 2022). "64.6% of defects were udder problems" is the paper's own label but cannot
  be a share of cows (only 58.3% had any defect).
- **Figures not in the named sources.** Mastitis: the 7-fold cure figure is real (Ruegg 2012) but
  "recurrent = 3 or more cases" is not in it. Septic arthritis: only "13.5 months" is in the named paper
  (Starke 2007, Germany); "44.9% failure within 60 days", "32 months", "nearly half culled within a year"
  and "Austria" were not found. Whay 1998: "persists more than 28 days after detection" is wrong twice;
  the study ended 28 days after treatment, and one lesion type (acute digital infection) had recovered by
  then.
- **Drug facts.** "Banamine Transdermal is the only FDA-approved NSAID for cattle" is wrong: Banamine
  injection and Ketofen are approved cattle NSAIDs. Of the labels read, it is the only one with a pain
  indication (foot rot). Its approval for lactating dairy cows is right (since 23 December 2022), but the
  answer cites a 2018 Merck detailer that shows the old label, which excluded lactating cows. "Pain relief
  adds a minimum of 8 days to a hold" is wrong as stated: each drug's withdrawal runs from its own last
  dose, so a same-day NSAID adds nothing when the antibiotic's withdrawal is longer (this overlap is
  arithmetic, not a sourced statement).
- **Unreadable dollar figures.** $140 lost per BCS point, $68.82 for a "bad image" cow, and $2.34 a day
  to keep a cull cow against $1.23 a day of weight gain all rest on a Cal Poly student paper that could
  not be opened, and appear in no source that could be. The Overton 2026 model, read in full, points the
  other way: feeding a thin cull cow for 60 days returned a net gain.
- **Mis-cited rule.** The residue-condemnation statement is cited to a laying-hen meloxicam paper; 9 CFR
  309.16 does condemn carcasses with violative residues, but "immediate" overstates it, and the farm-side
  "regulatory scrutiny" could not be checked.

## Part 1: the nine prompt claims (C1 to C9)

| Claim | Verdict | What the sources say | Read |
|---|---|---|---|
| C1 (D1.1) Ontario farmers wait days to weeks for a lame or high-cell-count cow to improve before selling her | Confirmed, qualitative only; source labels wrong | Marshall 2023 focus groups (4 groups, 21 Ontario farmers, December 2021 to January 2022): for high somatic cell counts or lameness, participants "discussed waiting days before choosing whether to and when to cull a cow", frequently for cows they wanted to cull but felt were not yet fit to ship; one farmer waits "two weeks - until she is good to go". Another: "We're all guilty of hanging onto those cows too long". No share of farms or cows and no measured wait length. The Marshall 2022 survey (224 respondents) gives no wait length; 74.6% say staff re-assess fitness if there is a delay between the cull decision and shipping. No US data on delayed culling was found. | Focus group, survey: **raw-checked** (focus group ⚠️ results sections other than these keyword-searched). |
| C2 (D1.2) Cull cows get worse between the cull decision and slaughter | Confirmed for the transport leg; on-farm wait unmeasured | Dahl-Pedersen 2018 (Denmark, 411 cull cows judged fit, examined at loading and on arrival, trips under 8 h): lame cows 31% before, 41% after; 19% became lame or more lame (15.8% of sound cows became lame, 26.6% of lame cows got worse); wounds 22% to 34%; milk leakage 1% to 17%; 9 cows lame at loading arrived severely lame (score 5); low BCS (2.5 or less) raised the odds of worse lameness 3.7-fold. Journey length was not a risk factor. The sentence in Marshall 2023 that the repo cited ("at risk for deterioration ... between being placed on a culling list to arriving at an abattoir") is a literature statement citing Stojkov 2020a, De Vries 2006 and Langford and Stott 2012. No study measured change during the wait on the farm. | Dahl-Pedersen: Europe PMC XML, **raw-checked**. Marshall 2023 sentence: **raw-checked**. |
| C3 Share of US cull dairy cows arriving in poor condition | Confirmed (new claim) | NBQA-2022 (20 US plants in 12 states, September 2021 to May 2022): dairy cows' mean BCS 2.3 on the 5-point scale (n = 2,728); 7.8% at BCS 1.0 and 15.5% at 1.5 (23.3% "too thin"), 44.5% at 2.0 or less. Mobility at unloading, dairy cows (n = 1,357): 65.7% sound, 25.8% minor stiffness, 7.3% obviously lame (score 3), 0.9% extremely reluctant to move (score 4), 0.3% down. Dairy cows (n = 2,440): full udder ("full bag") 74.9%, swollen joints 14.5%, foot abnormality 9.1%, mastitis 2.5%; 21.2% had no visible defect. Of 103 cattle condemned at ante-mortem (all types), 39.2% were non-ambulatory. Ontario auctions (Moorman 2018, 4,460 cows): 27.2% unacceptable hock injuries, 40.5% BCS 2 or less, 72.7% abnormal gait. | NBQA: Europe PMC XML read to the end, tables **raw-checked** (⚠️ Figures 1 and 2 not viewed). Moorman ⚠️ abstract, **raw-checked**. |
| C4 (D1.3) Auction price falls with thin condition, lameness and illness | Confirmed, through a review and abstracts | Ahola 2011b (western US auctions, via Moreira 2021): against a BCS-3.0 cow, discounts of $20.47, $12.19, $5.82 and $2.81 per 45.4 kg (100 lb) at BCS 1.0, 1.5, 2.0 and 2.5. Moorman 2018 (Ontario): BCS 2 or less sold $0.20/kg lower (about $117 a cow), abnormal gait $0.05/kg lower (about $32.45), hock score and tail no effect. Stojkov 2020 (British Columbia, via Moreira): non-lame cows Can$1.35/kg, cows at locomotion score 4 or more Can$0.35/kg. The answer's "$140 per BCS point" and "$68.82 per bad-image cow" could not be checked. Overton 2026's text gives the Moorman and Stojkov discounts as "Can$0.63/kg and Can$0.20/kg" in an order that conflicts with Moorman's abstract. | Moreira review (PMC page HTML; prose read to the end): **raw-checked**. Moorman ⚠️ abstract, **raw-checked**. Cal Poly ⚠️ not reached. |
| C5 Chronic lameness and repeat mastitis rarely resolve | Partly; depends on the lesion | Mastitis: in one Wisconsin study (Pinzon-Sanchez 2011, via Ruegg 2012) bacteriological cure was 7 times more likely for first cases than recurrent ones; "recurrent" is not defined. Clinical signs of mild cases "normally abate within 4-6 days, regardless of treatment", often leaving a subclinical infection with raised cell count. Septic arthritis of the coffin joint: after digit amputation, median survival in the herd 68 days against 585 for matched cows (Bicalho 2006, New York, 49 cows); mean life span 13.5 months after amputation (Starke 2007, Germany, randomised, 26 cows) and 15 months, range 1 to 34 (Devaux 2017, Switzerland, 20 cattle). The Heppelmann 2009 review says adequately treated cows need not have a shorter life; Desrochers 1995 (12 mostly beef cattle, facilitated ankylosis) found all walking normally after 1 to 7 months. Lameness pain: see Part 2. | Ruegg: raw PDF read to the end, **raw-checked**. Septic arthritis papers ⚠️ abstracts, **raw-checked**. |
| C6 (D3.1) Cows are held until withdrawal is met, then shipped even when unfit | Pattern stated in a commentary; no prevalence | Walker 2020 (commentary): futile treatment continues and "the cow is kept on farm until the drug withdrawal period has been met" and then sent "even if not fit for transport"; no rate or duration. Nearest primary data, Marshall 2022 survey: 52.2% of 224 Ontario farmers name drug withdrawal times as a factor in when a cull cow leaves; 21.9% have had a provincial letter about at least one cow judged unfit at a sales yard; 27.7% do not assess fitness before loading. Nothing links the two. | Walker paragraph and Marshall 2022 passages: **raw-checked** (Walker ⚠️ paragraph only). |
| C7 (D3.3) How long holds last and how often | No measurement found; label times bound the length | No study measures hold length or the share of cull cows held. Current label meat withdrawal after the last dose: ceftiofur sodium or hydrochloride (Naxcel, Excenel RTU EZ) 4 days, no milk discard; flunixin injection (Banamine) 4 days, milk 36 h; ampicillin (Polyflex) 6 days, milk 48 h; flunixin pour-on (Banamine Transdermal) 8 days, milk 48 h; ceftiofur crystalline free acid (Excede) 13 days, no milk discard; penicillin G procaine (Norocillin) 14 days, milk 48 h; oxytetracycline (Liquamycin LA-200, Bio-Mycin 200) 28 days, milk 96 h. Labels warn that higher doses, longer courses or other routes can leave residues beyond these times. | Banamine Transdermal label read in full, **raw-checked**. Other labels: withdrawal lines **raw-checked**, ⚠️ whole labels not read. |
| C8 Flunixin is the only approved pain or fever drug; the pour-on is not for lactating cows; withdrawal discourages pain relief | Wrong on two points; third unstudied | Banamine Transdermal (NADA 141-450, label Rev. 01/2024, DailyMed version effective 19 February 2026): indicated for fever with bovine respiratory disease and acute mastitis, and for pain of foot rot, in beef cattle 2 months and older and dairy cattle; not for dry dairy cows, replacement heifers over 20 months, breeding bulls over 1 year, dairy or veal calves; one topical dose only; milk 48 h, meat 8 days. FDA added lactating dairy cows on 23 December 2022. Banamine injection: fever with BRD, endotoxemia and acute mastitis, and inflammation in endotoxemia (no pain indication); intravenous only; meat 4 days, milk 36 h; not for dry cows. Ketofen (ketoprofen) is approved for fever with BRD but "Not for use in lactating dairy cattle". Efficacy on the transdermal label, 6 h after one dose: foot-rot lameness fell by at least one score in 15/15 against 1/15 controls (Nebraska) and 14/15 against 8/15 (Kansas), induced infection in young cattle; fever success 61/64 against 23/66 in mastitis cows. No study was found on whether withdrawal concerns reduce pain relief in cull cows. | Transdermal label and FDA 2022 entry, **raw-checked**. Injection label lines **raw-checked** ⚠️ partial. Ketofen: verifier read, ⚠️ grep only. List of cattle NSAIDs ⚠️ not exhaustive. |
| C9 US federal law has no fitness-to-transport standard; nothing limits how long a sick cow may be kept | Confirmed for the federal text read; state law unchecked | 49 U.S.C. 80502(a)(1): a rail, express or common carrier (except by air or water) or vessel "may not confine animals in a vehicle or vessel for more than 28 consecutive hours" without unloading for food, water and rest; no sick-animal provision. 9 CFR 309.3: cattle at 105 F or higher, plainly diseased, or non-ambulatory disabled are condemned at the plant. 9 CFR 309.16: carcasses with adulterating residues are condemned; live suspect animals may be held until the residue clears. Nothing in these sections acts on the farm. FARM v5 (voluntary, industry): do not transport until all withdrawal times are met, nor cows that are non-ambulatory, at BCS generally below 2, lame at 3 or more on the FARM scale, or with fever above 103 F or drug residues; "Make the decision to treat, cull, or euthanize animals promptly". Moreira 2021 states there is no US definition or regulation of fitness for transport (citing Edwards-Callaway 2019). | Statute, CFR, FARM lines: **raw-checked**. ⚠️ State law not searched; ⚠️ that the 28-hour law covers trucks is USDA's reading, not in the statute text read. |

## Part 2: what the cow experiences

| Question | Finding | Read |
|---|---|---|
| How long does lameness pain last? | Whay 1998 (UK, 53 lame and 42 sound cows): lame cows had lower pain thresholds on day 1; 42 with one lame hind claw were retested 28 days after trimming and treatment and were still lower than sound cows overall; by lesion, sole ulcer and white line disease were still lowered at day 28, acute digital infection was not. The study ended at day 28, so "more than 28 days" is not shown. EFSA 2023's paraphrase ("28 days after detection of the lesion") is where the "after detection" wording in repo claim A1.5 comes from. | ⚠️ abstract, **raw-checked**. |
| Is repeat mastitis prolonged pain? | Not shown. The sources give bacteriological cure, not pain: mild clinical signs fade in 4 to 6 days whatever the treatment; recurrent cases cure less often (7-fold in one study). Pain evidence for mastitis is repo claim A5.1 (S, EFSA). Pedersen 2024 cites Fogsgaard 2015 for udder signs and behaviour changes lasting a week after antibiotic treatment (secondary, not read). | Ruegg **raw-checked**; thesis: verifier read. |
| What happens to the cow during a withdrawal hold? | No study measured pain, condition or behaviour during a hold (Groups A and C searched; a few Europe PMC searches found none, which is weak evidence). Whether pain relief is usually given during a hold: no data. The only analgesic labelled for pain in cattle acts for one dose (label; Walker 2020 says NSAID effect lasts 6 to 24 h, verifier read). | Negative finding; ⚠️ short searches only. |
| What does the trip do to a compromised cow? | Dahl-Pedersen 2018: see C2; trips under 8 h already worsen lameness, wounds and milk leakage, worst in thin cows. NBQA-2022: mean 6.3 h and 490.6 km to the plant, none over 24 h; 55.3% of trailer loads came from auction markets; 78.6% harvested the same day. British Columbia (Stojkov 2020a and b, via Overton 2026): over half of market cows spent more than 3 days in the marketing system, up to 16 days, and their condition declined. US routes (NAHMS 2014, via Moreira 2021): 77% of shipments to markets travelled under about 80 km, but 49.3% of direct-to-slaughter shipments travelled 80 km or more. | Dahl-Pedersen, Moreira, Overton: **raw-checked**. NBQA transport: verifier read. |

## Part 3: farm-manager options

| Option | Evidence on welfare | Cost or trade-off | Read |
|---|---|---|---|
| Dry off and feed a thin cull cow before sale | Overton 2026 model (Ontario, one farm's trial data): 60 days of feeding from BCS 2.0 to 3.0 raised value by Can$664 against Can$442 costs (net about Can$222; benefit-to-cost 1.5, range 0.6 to 1.9). In the trial behind it (Berdusco 2024a and b), BCS rose 1.2 points on average (0.5 to 2.0), but 8.7% of held cows fell ill and 4.3% died (median 14 days to death); mortality is 25% of the model's cost. The authors say lame or sick cows "may be less suitable for prolonged pre-shipping periods". | Assumes spare housing; ignores crowding costs. Contradicts the answer's "net loss of $1.11 a day". | Overton read in full, **raw-checked**. Berdusco ⚠️ not read (S via Overton). |
| Pain relief during a hold | Flunixin pour-on is approved for lactating cows; one dose cut foot-rot lameness at 6 h (see C8). No data on chronic lameness, on repeat doses (not approved) or on cull cows. | Its 8-day meat withdrawal runs from its own dose; given with a longer-withdrawal antibiotic it does not lengthen the hold (arithmetic, not a source). | Label **raw-checked**. |
| Choose short-withdrawal drugs for a likely cull | Labels: ceftiofur sodium or hydrochloride 4 days against oxytetracycline 28 and penicillin G procaine 14 (see C7). No study of the practice. | Drug choice must still fit the disease; extra-label use is vet-set (not read). | ⚠️ label extracts. |
| Euthanize now instead of holding | FARM v5 and AABP list "treatment will not be pursued due to cost" as a euthanasia criterion (repo D3.2, V). A held cow that still fails FARM's fitness list when withdrawal ends cannot be shipped under FARM. | Salvage value lost; no verified US figure (the answer's ~$750 is its arithmetic on one week's price). | FARM lines **raw-checked**. |
| Sell direct to a packer, not through an auction | Not shown to cut transit: NAHMS distance data run the other way (above). Strappini 2012 (Chile, via Moreira): direct-from-farm carcasses were 28 kg heavier and more often free of bruises, which the review says does not prove cause. Marshall 2022: 54.5% of Ontario respondents send most cull cows to a sales barn; direct is available to 73.2%. | Plant capacity limits direct shipping (Marshall 2023 focus groups). | Moreira **raw-checked**; Marshall 2022 survey destinations: verifier read. |
| Re-assess fitness at shipping; written cull triggers; vet consult | No effect sizes found. 74.6% of Ontario farmers re-assess fitness after a delay; 61.6% have a written cull-cow SOP and 48.4% of those always use it. | | Survey: verifier read; 74.6% **raw-checked**. |

## Part 4: other facts

- **Drug residues in US dairy cows.** In-plant lab-confirmed violations fell from 1.1% (2000) to 0.38% (2019)
  (FSIS data via Moreira 2021, **raw-checked**). Violations usually come from not observing withdrawal
  times, over-dosing or poor records (verifier read).
- **No US culling or on-farm death figure newer than NAHMS Dairy 2014** was found (D1.4 stays V).
- **Productive life** (D1.5): the answer's figures come from a Swiss paper (Gazzarin 2025), not De Vries;
  not score-moving, stays W.
- **Canada and the EU.** Canada's 2022 transport rules treat cows with udder engorgement and lameness as
  compromised and unfit (Overton 2026, citing the Government of Canada). Outside the scenario's US rule
  set; not adjudicated.

## Sources that only Arda can open

Each would settle a figure the verifiers could not reach (bot-checked, paywalled or HTTP 403):

1. Cal Poly senior project, "A Literature Review on Injection-site Lesions in Dairy Cows and ...",
   https://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1132&context=dscisp : where "$140 per
   BCS point", "$68.82 per bad-image cow" and "$2.34 / $1.23 / $1.11 a day" come from, and their primary
   sources.
2. Moorman et al. 2018, J Dairy Sci 101:10580, https://doi.org/10.3168/jds.2018-14519 : the BCS and gait
   scale definitions, collection dates, and the price discounts in Canadian dollars.
3. Marshall et al. 2023 veterinarian survey, J Dairy Sci 106:302,
   https://www.journalofdairyscience.org/article/S0022-0302(22)00769-0/fulltext : whether vets report
   withholding pain relief from cull candidates because of withdrawal.
4. Pinzon-Sanchez and Ruegg 2011, J Dairy Sci 94:3397, https://doi.org/10.3168/jds.2010-3925 : the
   definition of "recurrent" mastitis and the odds ratio behind "7 times".
5. Whay et al. 1998, Vet J 156:23, https://doi.org/10.1016/S1090-0233(98)80058-0 : day-28 threshold
   values by lesion and how long cows had been lame before enrolment.
6. Bicalho et al. 2006, J Dairy Sci (PubMed 16772579), https://doi.org/10.3168/jds.S0022-0302(06)72336-0 : whether
   "44.9% culled within 60 days of amputation" is in it.
7. Heppelmann et al. 2009, Vet J 182:162, https://doi.org/10.1016/j.tvjl.2008.06.009 : survival after
   coffin-joint surgery and reasons for culling ("32 months", "nearly half culled within a year").
8. Berdusco et al. 2024a, J Dairy Sci 107:7267, https://doi.org/10.3168/jds.2023-24525 : the 8.7% disease
   and 4.3% death risk while feeding cull cows (would move that claim from S to V). Not attempted by the
   verifiers; probably behind the same Cloudflare check.
9. Ahola et al. 2011, J Anim Sci 89:1484, https://doi.org/10.2527/jas.2010-3171 : the primary price
   discounts by BCS and lameness at western US auctions (would move D1.3 from S to V for the US rows).
10. FSIS Residue Repeat Violators list,
    https://www.fsis.usda.gov/science-data/data-sets-visualizations/residue-repeat-violators : what happens
    to a farm after a violative residue.
11. University of Idaho bulletin bul897,
    https://www.uidaho.edu/-/media/UIdaho-Responsive/Files/Extension/publications/bul/bul897.pdf : a
    possible home of the US dollar figures in item 1.

## Orchestrator re-check

On 2026-11-11 the orchestrating session re-read, in the verifiers' saved texts, the decisive passage behind each of the four changes to existing claims and the ten new claims (the `check` entries in the notes folder's `status-changes.json`): the Marshall focus-group and survey texts on Europe PMC, Dahl-Pedersen 2018, the Moreira 2021 review and the Moorman abstract, the 2022 National Beef Quality Audit tables, the Overton 2026 model tables, the Ruegg extension text, the Whay 1998 and amputation abstracts, the FDA drug labels and the Banamine Transdermal supplement record, 49 U.S.C. 80502 and 9 CFR 309.3 and 309.16. Each said what the tables above say. Rows resting on abstracts stay W.
