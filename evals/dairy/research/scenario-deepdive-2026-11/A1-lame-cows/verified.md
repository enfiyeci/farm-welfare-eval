Eval: dairy

# Finding and treating lame cows: the Gemini answer, checked claim by claim

Written 2026-11-11. Input: `raw/2026-11-10-gemini.md` (Gemini Deep Research, core prompt from
`prompts.md`). What changes in the scenario is in `adjudicated.md`; cite that, not this file or `raw/`.

## How it was checked

An extractor cut the answer to 29 score-moving claims in four source groups (the claim key, IDs A1-A1
to A1-D10). Four Sonnet verifiers each took one group: A, prevalence, detection and stall comfort;
B, treatment, cure rate and recurrence; C, what the lame cow feels and for how long; D, US rules,
pain-relief drugs and costs. The brief: read each named source in full from the source itself,
prefer a raw download (Europe PMC XML, PubMed E-utilities, curl plus pdftotext) over WebFetch, flag
partial reads with ⚠️, no browser tools, no pirate sites, no clicking through bot checks. Their
unedited reports, each with a coverage statement, are the verifier reports; do not cite them.

Read in full from raw downloads: Thomsen 2023 (the prevalence review), Thomas 2015 (the treatment
trial), Randall 2018 (the recurrence paper), Bernhard 2020 (behaviour of mildly lame tie-stall
cows), the IntechOpen welfare chapter, Nagel 2016, the eCFR text of 21 CFR 524.970 and 522.970,
and the Farm Progress article (Wayback copy). The FARM v5 manual and EFSA 2023 dairy cows were read
in full on 2026-11-10 (`full-read-2026-11/checked-findings.md`); this pass read the relevant
passages again. Read only in part: Robcis 2023 (author copy, targeted reads), the Penn State
Extension page (the cost paragraphs), the FARM v5 Evaluation Prep Guide, the USDA meloxicam
petition and Cook's 2017 WDMC paper.

Many key papers are closed or bot-blocked: Beggs 2019, Cook 2016, Espejo 2006, Wells 1993,
Groenevelt 2014, Leach 2012, Whay 1998, Laven 2008, Tadich 2013, Passos 2017, Cutler 2013 and Cha
2010. Those rows rest on verbatim PubMed abstracts and carry ⚠️. The two studies that actually test
early against usual-care treatment (Groenevelt 2014, Leach 2012) are among them.

Before any figure that could change a status in `candidates.json`, I re-checked it myself against
the raw text the verifiers saved (grep of the saved file, then reading the passage): the Beggs,
Groenevelt, Leach, Espejo, Wells, Whay 1998, Whay 2005, Laven 2008, Tadich 2013, Cha 2010 and Mason
2025 abstracts; Thomas 2015 (abstract, results, Table 5 and the discussion on timing); Randall 2018
(read to its end, tables included; figures are captions only); the FARM v5 lameness pages
(protocol standard, cost sentence, footbath and analgesic sentences, the locomotion standard, its
scorecard and the CIP consequence); the EFSA passages at lines 1280 to 1283, 2036 to 2058 and 4886
to 4902; Thomsen 2023 (the summary and trend passages); the Bernhard 2020 abstract; the current eCFR
text of 21 CFR 524.970; the Robcis 2023 abstract and conclusion; and the Penn State cost paragraph.
Those rows are marked **raw-checked**. Everything else is the verifier's reading.

An abstract-level confirmation counts as W (weak), never S or V.

## What the check found about the raw answer

- **The central claim has no support in the paper the answer cites.** Gemini marks "treat early
  beats waiting for the routine trim" as Supports on the strength of Thomas 2015. That trial
  treated every cow 2 to 16 days after she became lame and compared only what was added to the
  trim (a block, ketoprofen, both). It has no late arm; the authors say they would not leave lame
  cows untreated for weeks (**raw-checked**). The two studies that do compare early with usual-care
  treatment, Groenevelt 2014 and Leach 2012, are UK trials Gemini never describes, although
  Groenevelt is its own source [30], cited only for block discomfort.
- **Wrong figures.** "Wisconsin herds average 13.2% to 22.2%" splices two Cook studies with
  different herds and scales (66 herds, 13.2%; 10 herds, 22.2%). "Ranging up to 36%" is in no
  source read. "Up to three-fold" for Wells 1993 is 2.5 times, and those herds were mostly tie-stall.
  The cost "$333 to $337 (Liang 2017 and Ohio State)" is Robcis 2023, a European simulation model
  reporting €307.50 a year per lame cow and €12.10 a week, converted by Penn State Extension to
  $336.91 and $13.26 (**raw-checked**). The "$120 to $216 for a sole ulcer episode" in FARM is the
  spread across three diagnoses in Cha 2010; sole ulcer alone is $216 (**raw-checked**).
- **Wrong papers.** [12] (a 2026 milk-yield paper) is cited for Thomas 2015. [17] (a 2024 genetics
  paper) is cited for Randall. The 79 to 83% recurrence figure is in Randall 2018, not in the Randall
  2016 heifer paper that both Gemini and EFSA name (EFSA's reference list gives the heifer paper,
  which has no attributable-fraction result). [9], a 2012 Massey thesis, is cited for two US
  studies. [3] is a South African study cited for Wisconsin. [20] (rumen boluses) is cited for the
  cost.
- **Overclaims.** "NSAID gives a significant advantage": in Thomas 2015 ketoprofen alone did not
  differ from trim alone; only block plus ketoprofen did, and under the looser "non-lame" outcome
  no arm differed (**raw-checked**). "Conclusively proven to shorten the episode": the trial
  measured one score at 35 days, not episode length. "Recent findings (2016 to 2026) unequivocally
  prove" cites the 2015 paper. All nine Part 1 verdicts were "Supports".
- **Unsupported claims.** No source read sets a 24 to 48 hour treatment deadline; FARM requires a
  written lameness protocol but no deadline, and the protocol standard carries no corrective action
  (**raw-checked**). No source says milk discard makes managers reluctant to give pain relief. The
  "1.5 to 2 hours to score a 250-cow herd" is not in the cited Farm Progress article. "No US
  federal law sets a lameness limit" is plausible and unsourced. "Moderately lame cows show more
  variable lying bouts" is not in the cited paper.
- **One answer statement was more careful than its own verdict.** For recurrence it says early
  treatment "theoretically" helps; no source read measures it.

## Part 1: the nine claims (C1 to C9)

| Prompt | Claim | Verdict | What the sources say | Read |
|---|---|---|---|---|
| C1 (A1.1) | 22.8% lame on average (5.1 to 45%), 7.0% severe, no improvement in 30 years | Figures confirmed; "no improvement" overstated | Thomsen 2023: 53 studies, 414,950 cows, 1989 to 2020; mean 22.8% (median 22.0%, between-study range 5.1 to 45%, within-herd 0 to 88%), lame typically score 3 to 5 of 5; severe 7.0%. Trend: studies from the last ten years 21.5% against 24.3% for older ones, P = 0.37; the authors say prevalence "changed very little", with "no clear trend". North America mean 24.2%. US rows: Cook 2016, 66 high-producing Wisconsin freestall herds, 13.2 ± 7.3% (score 3 or more), severe 2.5%; no range in the abstract or EFSA. North-East US 55%: EFSA text credits von Keyserlingk 2012 (high-yielding multiparous cows only, which Thomsen excluded) and its table credits Chapinal 2013, 40 herds. Other US studies in Thomsen: Wells 1993 15.2%, Cook 2004 17.5%, Espejo 2006 24.6%, Adams 2017 9.6% (191 herds), Salfer 2018 26.6%, Chapinal 2013 45%. | Thomsen: read in full, **raw-checked**. EFSA rows: **raw-checked**. Cook 2016 ⚠️ abstract only. |
| C2 (A1.2) | Staff find about a quarter of lame cows but every severely lame cow | Confirmed; Australian pasture farms | Beggs 2019: 19,154 cows on 50 Australian pasture-based farms, scored leaving the parlour on 0 to 3; "All very lame cows had been detected by the farmer, but overall, farmers detected only 24%". US evidence: Espejo 2006, 50 Minnesota freestall herds, 24.6% lame (score 3 or more of 5), 3.1 times the managers' estimate; Wells 1993, 17 Minnesota and Wisconsin herds (14 tie-stall), 13.7 to 16.7%, 2.5 times the managers' estimate. | Beggs, Espejo, Wells ⚠️ abstracts, **raw-checked**. Beggs full text was read in August (telemetry note). |
| C3 (A1.3) | Last 30% of the milking order holds 62% of lame cows | ⚠️ Discrepancy, not resolved | The Beggs abstract says "only 60% of lame cows appeared in the last 30% of cows to be milked". The August telemetry note, which records a full-text read of an owner-supplied PDF, gives 26%, 47% and 62% for the last 10, 20 and 30% of the order. The full text was blocked this time. Both say a tail-only check misses about 40%. The abstract adds that scoring the last 200 cows works as a herd-level screening test, not as a way to find individual cases. | Beggs ⚠️ abstract, **raw-checked**. Telemetry note read at the passage. |
| C4 (A1.6) | Treating a new case within days beats waiting for the routine trim | Not shown by the cited trial; supported by two UK trials at abstract level | Thomas 2015 (5 UK farms, 167 cows analysed, 93% mildly lame) is positively controlled: every cow was trimmed 2 to 16 days after becoming lame, then randomised to nothing more, a block, a 3-day ketoprofen course, or both. Sound (score 0) at 35 days: 24.4%, 35.9%, 28.6%, 56.1%; only block plus ketoprofen against trim alone was significant (Bonferroni P = 0.01). Non-lame (score 0 or 1): 68.8%, 71.8%, 76.2%, 85.3%, not significant. It has no timing comparison and no cost of waiting. Timing studies: Groenevelt 2014 (4 UK farms, fortnightly scoring): cows newly scored lame (2 of 0 to 3; score-3 cows excluded) were trimmed 3 to 48 h later or left to the farmer's usual approach; sound at 2 weeks 78% against 66%, at 18 weeks 41% against 13%, share of later scores sound 81% against 66.1% (P < 0.001); severe lesions at treatment 6.6% against 14%. Leach 2012 (4 UK farms): treatment within 48 h of detection at fortnightly scoring against the farmers' usual approach, where the median time from first scored lame to treatment was 65 days; early-treated cows had less severe lesions, were less often selected for further treatment and had lower prevalence 4 weeks after treatment; no clear milk effect. Neither abstract tests block or pain relief by timing, and neither compares against a scheduled trimmer visit specifically. | Thomas: read in full, **raw-checked**. Groenevelt, Leach ⚠️ abstracts, **raw-checked**. |
| C5 (A1.5) | Hyperalgesia lasts at least 28 days after a lesion is detected | Confirmed with caveats | EFSA (lines 1280 to 1283): 28 days after detection, "even after treatment". Whay 1998 (UK, 53 lame and 42 sound cows): all lame cows were trimmed and treated; 42 were re-tested once, 28 days after treatment. Sole ulcer and white line cows were still below sound cows; acute digital infection cows were not. So 28 days is the only re-test point, not a measured end. Laven 2008 (NZ, 149 treated cows on 9 pasture farms): gait and pain threshold were still improving between day 28 and day 100. Passos 2017 (Brazil, 34 cows): pain threshold rose one week after trimming in non-infectious lesions. | EFSA, Whay 1998, Laven: **raw-checked** (Whay and Laven ⚠️ abstracts). Passos ⚠️ abstract, verifier read. |
| C6 (new) | Previous lameness explained 79 to 83% of later lameness (Randall 2016); does early treatment cut recurrence? | Figure confirmed in a different paper; second half unmeasured | Randall 2018 (J Dairy Sci 101:1311), two UK herds (Herd A, a 200-cow Scottish research herd, 724 cows over 8 years, weekly scores; Herd B, a 600-cow Somerset freestall herd, 1,040 cows over 44 months, treatment records): median population attributable fraction (the share of lameness events that would disappear without the risk factor) for all previous lameness 80.69%, 78.75% (Herd A, two definitions) and 82.69% (Herd B). It counts earlier lameness at any time, and most is short-term persistence: at least 5 weeks earlier, 58.97%, 41.67%, 46.31%; at least 16 weeks earlier, 9.34%, 11.36%, 21.07%. In Herd A most lameness events lasted one week. Randall 2016 has no attributable fraction (grep finds none); EFSA cites it by mistake. Recurrence after early treatment: no study measured it. Randall 2018's discussion suggests early treatment "may also be crucial", citing Thomas 2015, which followed cows only 35 days. Leach 2012's "less likely to be selected for further treatments" is the nearest datum. | Randall 2018: read to its end, **raw-checked**. Randall 2016: grep only. Leach ⚠️ abstract. |
| C7 (A1.7) | Deep bedding beats mats; overstocking and time out of pen raise lameness; footbaths conflict | Bedding confirmed; footbath "conflict" is a difference in scope | EFSA conclusion 8: shallow beds or mats raise claw disorders and lameness against year-round deep-bedded cubicles (90 to 100% certainty); conclusion 5 compares against pasture; conclusion 7: dry, soft lying surfaces cut standing time and lameness (50 to 100%); hazard studies mostly observational (lines 2036 to 2042). FARM v5 agrees on bedding ("consistently associated"). Footbaths: EFSA names foot bathing only as a hazard area, with no effect size; it does not say footbaths failed. FARM v5 says footbaths "have been demonstrated to be effective in controlling digital dermatitis, with copper sulfate being effective in reducing prevalence", citing three studies, and does not claim an effect on sole ulcer or white line disease. Formalin is not named in FARM. Numbers: Espejo 2006, sand 17.1% against mattress 27.9% lame (abstract); Cook 2016 says deep loose bedding gave "significant advantages" without a figure in the abstract. | EFSA, FARM: **raw-checked**. Espejo ⚠️ abstract, **raw-checked**. Cook ⚠️ abstract. |
| C8 (A1.8) | $337 a case plus $13 a week (Ohio State); FARM cites $120 to $216 | Figures real, sources wrong | $336.91 and $13.26 are Penn State Extension's dollar versions of Robcis 2023, a European bioeconomic simulation: a lame cow (score 3 or more) costs €307.50 a year and each week in a lame state €12.10, from milk, reproduction and treatment, over simulated prevalences of 26 to 98%. Not Liang 2017 and not Ohio State. FARM's $120 to $216 is Cha 2010 (Cornell dynamic-programming model): sole ulcer $216.07, digital dermatitis $132.96, foot rot $120.70 per case. Labour time to score a 250-cow herd: no source (Farm Progress says only "once a month"). Routine trim cost: no source read. | Robcis abstract and conclusion, Penn State paragraph, Cha abstract, FARM sentence: **raw-checked**. Robcis ⚠️ read in part; Cha ⚠️ abstract. |
| C9 (new) | FARM v5: at most 5% score 3 and 15% score 2; a CIP of up to three years, not an MCAP | Confirmed | FARM v5 (July 2024 to June 2027): "5% or less of the lactating cows observed score 3" and "15% or less ... score 2" on its 3-point scorecard (1 normal, 2 moderate, 3 severe). "If either standard is not met, the farm will receive a Continuous Improvement Plan (CIP). Improvement towards meeting the standard benchmark must be made within three years"; evaluators may set shorter times. No combined 20% figure exists; Gemini's "20%" is the sum. The written lameness protocol required in the Herd Health Plan "is not associated with a corrective action" and sets no treatment deadline. No US law or processor contract with a lameness limit was found; none was searched beyond FARM. | FARM v5 pages 60 to 62 and 149 to 150: **raw-checked**. Prep Guide: verifier read, ⚠️ partial. |

## Part 2: what the lame cow experiences

| Question | Finding | Read |
|---|---|---|
| (a) How painful are the lesions? | Pain thresholds: sole ulcer, white line disease and acute digital infection all lowered the threshold at detection (Whay 1998); sole ulcer and white line were still lowered 28 days after treatment. Digital dermatitis: Cutler 2013 (Canada, 214 hooves) found withdrawal at 7.45 kg for active and 12.84 kg for healing lesions, but 19% of active lesions tolerated the 25 kg maximum, so pain is variable. Dyer 2007 (2 US farms, 263 cows): lateral claws much more often painful (27.1%) than medial (2.1%); painful claws also on sound limbs. No pain data for foot rot or joint infections were found. | Whay 1998 ⚠️ abstract, **raw-checked**. Cutler, Dyer ⚠️ abstracts, verifier read. |
| (b) Is a moderately lame cow in pain? | Tadich 2013 (Chile, 213 cows): pain threshold significantly lower at scores 3 to 5 of 5 than at 1, in a dose-response; haptoglobin (an inflammation marker) raised at every score above 1. Score 2 of 5 was not shown to have a lower threshold. Bernhard 2020 (Swiss tie stalls, 26 to 30 matched pairs, lame = 2.25 to 3.25 of 5): lame cows ate 27.7 min a day less and lay 64.7 min a day less, with fewer but longer lying bouts. Weigele 2018 (17 Swiss farms, 66 cows at score 3 of 5): moderately lame cows lay longer and ate less. So lying time moves in opposite directions between studies. FARM v5 states "Moderate lameness is painful" (its score 2, which may include cows below Tadich's cut-off). | Tadich ⚠️ abstract, **raw-checked**. Bernhard read in full, abstract **raw-checked**. Weigele ⚠️ abstract. FARM **raw-checked**. |
| (c) How long does an episode last, treated against untreated? | No source gives an untreated episode length. Treated: pain sensitivity persists past 28 days (Whay 1998) and was still improving at day 100 (Laven 2008). Usual care left cows a median 65 days from first scored lame to treatment (Leach 2012). In Groenevelt 2014, 13% of usual-care cows against 41% of early-trimmed cows were sound at 18 weeks. In Randall 2018 Herd A most scored lameness events lasted one week. | Whay, Laven, Leach, Groenevelt ⚠️ abstracts, **raw-checked**. Randall **raw-checked**. |
| (d) Does trimming or a block hurt? | FARM v5 (citing a review): trimming "may induce immediate painful sensation, stress, changes in lying down activities and reduction in milk yield". Thomas 2015 suggests blocks "may cause some discomfort" as a hypothesis; 17 cows lost blocks by day 8 and 5 cows were withdrawn as unduly stressed or collapsing in the crush. No study isolates block pain. | FARM, Thomas: **raw-checked**. |

## Part 3: farm-manager levers

| Lever | Evidence on lameness | Cost or welfare trade-off | Read |
|---|---|---|---|
| Score the whole herd every 2 weeks and treat new cases within 48 h | Groenevelt 2014 and Leach 2012 (above). | Labour of scoring: no figure found. One more trim and crush restraint per case. | ⚠️ abstracts. |
| Score only the tail of the milking order | Finds about 60% (abstract) or 62% (August full-text read) of lame cows. Valid as a herd-level screen, not for case finding. | Cheaper; misses about 40% of cases. | Beggs ⚠️ abstract. |
| Add a block and pain relief at the trim | Thomas 2015: 56.1% sound at 35 days with both against 24.4% with trim alone; neither alone significant. | Ketoprofen is not US-labelled for cattle; see pain relief. | **raw-checked**. |
| Pain relief at treatment | Mixed: Whay 2005 (UK, 40 cows, ketoprofen) reduced hyperalgesia at days 3, 8 and 28 but not gait; Laven 2008 (NZ, tolfenamic acid) no long-term benefit; Mason and Laidlaw 2025 (NZ, 241 cows, meloxicam after trim and block) no faster soundness (hazard ratio 0.78, 95% CI 0.56 to 1.03) but better conception (1.42). | US label: transdermal flunixin (21 CFR 524.970) for pain of foot rot in beef and dairy cattle, lactating cows included since the 2023 amendment (heifers 20 months or older and dry cows excluded); one topical dose; milk discarded 48 h; slaughter 8 days; veterinarian's order. Injectable flunixin is labelled for fever, not lameness. Meloxicam is extra-label; the USDA petition gives 96 h milk and 15 to 21 days meat withdrawal (not FARAD). | eCFR read in full, **raw-checked**. Whay 2005, Laven, Mason ⚠️ abstracts, **raw-checked**. Petition ⚠️ partial. |
| Deep or sand bedding | EFSA 90 to 100% certainty (observational); FARM agrees; Espejo sand 17.1% against mattress 27.9%. | Capital cost not sourced. | **raw-checked**; Espejo ⚠️. |
| Footbaths | FARM: copper sulfate effective against digital dermatitis (manual statement, studies unread); EFSA gives no effect. Penn State cites once weekly for four consecutive milkings with 5% copper sulfate (Speijers 2010, 2012, unread). | Copper loading and handling not sourced. | FARM **raw-checked**; Penn State verifier read. |
| Preventive trimming | Robcis 2023 (simulation): "preventive trimming allowed a better reduction in lameness prevalence than spending time on early detection"; cows were lame for longer without preventive trimming. A model result, not a trial. | Trimming may cause short-term pain (FARM). | Robcis abstract **raw-checked**, ⚠️ read in part. |
| Automated detection, hospital pen, culling | Not checked (cut by the extractor as not score-moving). | | |

## Part 4: other facts

- **US practice on treatment timing.** No US figure was found for how long lame cows wait for
  treatment. The 65-day median is UK (Leach 2012). In Randall 2018 Herd B, lame cows found by
  daily observation were treated "generally within 2 to 3 days".
- **Repeat lameness dominates the burden.** In Randall 2018, 93% of Herd A cows and 62% of Herd B
  cows were lame at least once; 96% (Herd A) and 72.6% (Herd B) of lame periods were repeat events.
- **Detection gap in US herds.** Managers' estimates run 2.5 to 3.1 times below scored prevalence
  (Wells 1993, Espejo 2006); FARM itself says farmers "consistently underestimate" prevalence,
  "particularly mild cases".
- **EFSA cites the wrong Randall paper** for the 79 to 83% figure (lines 2047 to 2049 against the
  reference at line 6546).
- **Cost scale.** Dolecheck and Bewley 2018 (quoted by Penn State, primary unread) give $76 to $533
  a case across studies.

## Sources that only Arda can open

Each would settle a figure the verifiers could not reach (bot-checked or paywalled):

1. Beggs et al. 2019, *J Dairy Sci* 102:1522 (https://doi.org/10.3168/jds.2018-14847): 62% or 60%
   of lame cows in the last 30% of the milking order (the abstract says 60%; the August full-text
   read says 62%), and which scores form the base of the 24%.
2. Groenevelt et al. 2014, *Vet J* 201:283 (https://doi.org/10.1016/j.tvjl.2014.05.017): cows per
   arm, how long usual-care cows waited, how many were treated by farmers, and what the treatment
   included (trim only, or block and pain relief).
3. Leach et al. 2012, *Vet J* 193:626 (https://doi.org/10.1016/j.tvjl.2012.06.043): the
   prevalence difference 4 weeks after treatment, the re-treatment counts and the lag per arm.
4. Whay et al. 1998, *Vet J* 156:23 (https://doi.org/10.1016/S1090-0233(98)80058-0): per-lesion
   numbers, threshold sizes at day 28, and whether treated cows got an NSAID.
5. Laven et al. 2008, *N Z Vet J* 56:210 (https://doi.org/10.1080/00480169.2008.36835): threshold
   values at days 28 and 100 against sound cows.
6. Tadich et al. 2013, *Vet J* 197:401 (https://doi.org/10.1016/j.tvjl.2013.01.029): whether
   score-2 cows (of 5) had a lower pain threshold than sound cows.
7. Cook et al. 2016, *J Dairy Sci* 99:5879
   (https://www.journalofdairyscience.org/article/S0022-0302(16)30215-6/fulltext): the lameness
   range across the 66 herds and the sand against mattress effect size.
8. "Lameness in Cattle", ResearchGate 380892767
   (https://www.researchgate.net/publication/380892767_Lameness_in_Cattle), probably the 2024
   Springer chapter by Bell and colleagues: what it says about early treatment and recurrence.

## Orchestrator re-check

On 2026-11-11 the orchestrating session re-read, in the verifiers' saved texts, the decisive passage behind each of the six changes to existing claims and the eight new claims (the `check` entries in the notes folder's `status-changes.json`): Thomsen 2023, the Beggs 2019, Groenevelt 2014, Leach 2012, Espejo 2006, Wells 1993, Whay 1998 and 2005, Laven 2008, Mason and Laidlaw 2025, Tadich 2013 and Cha 2010 abstracts, Thomas 2015, Randall 2018, Bernhard 2020, Robcis 2023 and the Penn State page, EFSA 2023 dairy cows and FARM v5 in the local texts, and 21 CFR 524.970. Each said what the tables above say. A1.3 keeps V on the August full-text read; the abstract's 60% against its 62% is recorded and the full text is on the browser list.
