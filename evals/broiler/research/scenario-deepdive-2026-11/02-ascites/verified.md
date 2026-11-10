Eval: broiler

# Ascites: the Gemini and Elicit answers, checked claim by claim

Written 2026-11-10. Inputs: `raw/2026-11-09-gemini.md` (Gemini Deep Research, core prompt from
`prompts.md`) and `raw/2026-11-09-elicit-q1.md` to `-q4.md`. What changes in the scenario is in
`adjudicated.md`; cite that, not this file or `raw/`.

## How it was checked

Sixteen Sonnet subagents each took one group of sources (A to P) and checked every claim that rests
on them. The brief was scenario 5's: read the named source in full from the source itself, prefer a
raw download (Europe PMC full-text XML, or curl plus pdftotext) over WebFetch, flag partial reads
with ⚠️, no browser tools, no pirate sites, no clicking through bot checks. Their unedited reports,
each with a coverage statement, are in `verifier-reports-raw.md`, with the brief and the claim key
at its end. Do not cite that file. All 16 reports were read in full for this file.

Access was the weak spot. Taylor and Francis, Oxford (Poultry Science), ScienceDirect, JSTOR and
ResearchGate blocked scripted downloads, so many verdicts rest on abstracts. An abstract-level
confirmation counts as W in the inventory, never S or V.

Before any figure that changes a status in `claims.json`, I re-checked it against raw text on
2026-11-10. Four sources I re-downloaded myself: the Merck ascites page, Forseth 2023 (Europe PMC
XML, PMC10015030), İpek and Sahan 2006 (animbiosci.org PDF) and the Druyan 2012 InTech chapter
(cdn.intechopen.com PDF). Those rows say **raw-checked**. Seven more rest on a verifier's own raw
download, which I grepped for the figure: Namakparvar 2014, Boostani 2010, Kuleile 2020, the OCR
text of Bölükbasi 2005, EFSA 2010, Welfare Footprint chapter 3 and Hassanzadeh 2003. Those rows say
**grepped**. Everything else is the subagent's reading.

## What the check found about the raw answers

- **No study measured what ascites feels like.** Welfare Footprint chapter 3 models pain hours from
  human analogies and calls its model a "tentative hypothesis" (grepped). No source gives a
  measured time from first sign to death.
- **A wrong figure in the welfare model.** Welfare Footprint's "0.5 to 4% flock mortality from
  ascites" cites the Merck page on sudden death syndrome (SDS), which gives 0.5 to 4% for SDS. Do
  not use it as an ascites figure.
- **Wrong authors and spliced papers.** "Fathi 2012" is Feizi 2012. "De Ruyck 1988" is
  Huchzermeyer, De Ruyck and Van Ark 1988. "Druyan 2012, Poult Sci 91:556" is Closter et al. 2012.
  "Özdemir" is Akşit et al. 2008 (Özdemir is last author). "Wang 2007" is Li Jinchun et al. 2007.
  Elicit's "Hassanzadeh 2010" 18%-protein row is Bölükbasi and Emsen 2006. The SciELO paper Gemini
  calls Molenaar is İpek, Sahan and Sözcü 2015. "2 to 7 times" stitches a 2x figure (Baxter, via a
  BCC report) to a 7x figure (Forseth 2023, via another BCC report).
- **Things Gemini put in Merck that Merck does not say.** Up to 300 mL of fluid (it is in the Acta
  Agric Serbica review), culling, brooding temperatures (Aviagen), and 0.5% early deaths from septal
  defects (in none of the group A sources).
- **A duck paper's summary passed off as a trial.** "Wideman 1998: 23 to 53% under cold vs 4 to 6%
  on well-managed farms" is a Muscovy duck paper (PMC8486373) summarising four citations.
- **EFSA misquoted.** EFSA 2023 never says fast-growing broilers "should no longer be kept"; that is
  Animal Law Europe's paraphrase. EFSA 2023 recommends a growth cap of 50 g/day and lists no ascites
  welfare consequence among its 19.
- **Reversed or overstated effects.** Hassanzadeh 1997's abstract says vitamin C did not change
  haematocrit; Gemini says it did. Geng 2004's abstract says CoQ10 had no growth effect; Gemini says
  it improved feed conversion. Maatjens 2016 has no ascites outcome, and its "0.7% fewer
  second-grade chicks" is Molenaar 2011's 0.7% more. Bahadoran's and Moayyedian's mortality
  differences were never tested, though abstracts call them "marked" or "clearly higher".

## Part 1: the ten memo claims (C1 to C10)

| Memo | Claim | Verdict | What the sources say | Read |
|---|---|---|---|---|
| C1 | More than 2% of flocks at baseline | Merck says something narrower | Merck: "The incidence of ascites syndrome is > 2% in some broiler flocks." No citation, breed, age or altitude. The best low-altitude primary figure is Forseth 2023 (Norway, one company, 2015 to 2021): ascites condemnation 0.661% of Ross 308 (190,537 of 28,804,890) vs 0.093% of Hubbard JA787 (31,865 of 34,404,525). It counts only birds that reached the slaughter line. | Merck **raw-checked**. Forseth PMC10015030 **raw-checked** (Table 3). |
| C2 | Up to 25% under challenge; fast birds 35% more prone | Not checkable | Baghbanzadeh and Decuypere 2008 was blocked; its abstract has no number, and Gemini's own coverage note says it never found 25% or 35%. Druyan's "over 25%" is a share of all UK broiler losses (Maxwell and Robertson 1998), not of a flock. 4.7% is the 1996 world survey average (Maxwell and Robertson 1997). Measured cold-challenge trials range from 9.5% (İpek 2006) to 42.4% (Julian 1989, abstract). | Baghbanzadeh ⚠️ abstract only. Druyan chapter **raw-checked**. |
| C3 | Above 900 m is unsatisfactory | Confirmed in Merck, with a different remedy | Merck: "Altitudes > 3,000 feet (900 meters) are unsatisfactory for meat-type chickens, and growth must be slowed to prevent mortality." Its remedy is slower growth and preventing chilling, not "climate control". No experiment in groups A, H or P tested below 1,800 m. Boostani 2010 and Kuleile 2020 give 1,300 m as the point where ascites rises. The Ethiopia paper repeats 900 m, citing Merck, so it is not independent. | Merck **raw-checked**. Group P ⚠️ mostly abstracts. |
| C4 | Cold in weeks 1 to 3 raises later ascites | Confirmed by one primary trial, **raw-checked** | İpek and Sahan 2006: Ross 308 males, Turkey, 150 m, brooding 4 to 5 °C cooler in weeks 1 to 3 only (29.0, 26.4, 23.1 vs 33.3, 30.2, 27.5 °C), both groups at 21 °C after. Ascites deaths on days 21 to 42: 9.52% (10/105) vs 1.90% (2/105), p < 0.05. Merck states the claim with no citation. Caveats: one trial of 105 birds a group, pelleted feed, winter. Two studies found brief early cold **protective**: Bahadoran and Hassanzadeh 2010 (15 °C for 3 h on days 3 and 4, 8 vs 16 deaths of 125, no test, OCR) and Shinder 2011 (embryo cooling, abstract only). So sustained cooler brooding raises risk; a short cold spell may not. | İpek PDF **raw-checked** (Table 3). Merck **raw-checked**. |
| C5 | Cobb most susceptible, Ross least | Not supported | No trial shows a significant Cobb vs Ross difference. Namakparvar 2014: Ross 1.25%, Cobb 4.58%, Arian 13.33%; Ross and Cobb share a letter (not different). Azizian 2013: Cobb and Ross tied at 2.94% (3 birds each). Varmaghany 2021: Ross 0%, Cobb 3.84%, p = 0.54 (about 0 vs 2 birds). Feizi 2012: Ross 4, Cobb 6, "not statistically different". The slower Iranian line Arian was the most susceptible in three trials. All small, mostly unchallenged, all Iranian. | Namakparvar **grepped**. Others full text, verifier read. |
| C6 | Growth rate outweighs ventilation or vitamin C | No test exists | Every supplement trial used a challenge (cold, T3 dosing or low ventilation); none tests a supplement against a fast curve at normal temperature. Nemati 2017 (full text): under cold, vitamin C 300 mg/kg and CoQ10 cut ascites mortality from 20.0% to 13.7% and 11.6%; the combination lost the effect. Bendheim 1992a,b: ventilation "had no role" (abstracts). Julian and Wilson 1992: pen air in high- and low-ascites pens at about 300 m did not differ in O2 (abstract). | Nemati, verifier read. Others ⚠️ abstracts. |
| C7 | Divergent lines 93.9% vs 9.5% with 5% growth difference | Confirmed at abstract level; the 1986 comparison needs a fix | Druyan 2008 abstract confirms 93.9 vs 9.5%, 2002 trial only; n and generation not stated. The 1986 slow line's 32% came only with 12 extra challenge days (to day 54). At day 42 it had significantly less ascites mortality: 11.0% vs 21.4% (2002) and 15.4% vs 26.8% (2006). Pavlidis 2007 (abstract): divergent selection cut day-42 body weight in both lines. | Druyan 2008 ⚠️ abstract. Druyan chapter Table 1 **raw-checked**. |
| C8 | RV:TV above 0.25 to 0.30 marks pulmonary hypertension | Cutoffs real, tiers not found | Julian's lab used RV:TV above 0.249 (Julian et al. 1992, Can Vet J) and above 0.299 for birds dying with ascites (Walton 2001; Wilson 2016). The "moderate" and "severe" tiers were in no source read. Cutoffs vary by lab: Yang 2002 used above 0.30 and 0.27 or less; Azizian 2013 used above 0.22. | ⚠️ abstracts; Azizian and Yang PDFs grepped by verifier. |
| C9 | Pelleted or high-energy feed raises ascites | Confirmed | Bölükbasi 2005: 208 male Ross, cold 16 °C from day 21: pellets 13.3% vs mash 3.3%; warm house: pellets 6% vs mash 0; no growth difference. Kuleile 2020, Lesotho, 1,650 m: pellets 6.25% vs mash 0.75% (p = 0.033), with mash birds far lighter. Arce 1985 (15% vs 4%) is seen only second-hand. da Silva 1988 (abstract): no ascites on mash at 730 m. | Bölükbasi OCR **grepped**. Kuleile **grepped**. |
| C10 | Ascites resistance is heritable apart from growth | Heritable, yes; "apart from growth" is mixed | Heritability is moderate: RV:TV 0.45 under cold (Pakdel 2002, full text), 0.21 to 0.27 (Lubritz 1995, abstract). The genetic link to growth changes sign with conditions: -0.27 under cold vs +0.50 at normal temperature (Pakdel); +0.22 and +0.35 in male records (Moghadam 2001, full text); Closter 2012 shows the same drift by age (abstract). Pakdel's "+111.4 g with no rise in ascites" is a deterministic simulation, not a selection experiment. Druyan 2008 found no genetic correlation (abstract); Pavlidis 2007 found selection cut body weight in both lines (abstract). | Pakdel thesis ch. 2, 3, 6 and Moghadam, verifier read. Others ⚠️ abstracts. |

## Part 2: what the living bird experiences

No source measured pain, breathlessness or distress in an ascitic bird. Everything here is signs,
blood values or modelled hours.

| ID | Claim | Verdict | What the source says | Read |
|---|---|---|---|---|
| A4 | Signs before death | Confirmed (standard) | Merck: no clinical signs until right ventricular failure; then faster breathing, less exercise tolerance, cyanosis; birds "frequently die on their backs"; death can come before signs or fluid. Not all ascites deaths have fluid; a thick right ventricle is enough for the diagnosis. | Merck **raw-checked**. |
| G4 | Signs and timing under cold | Confirmed | Moayyedian 2011, Cobb 500, Iran: ruffled feathers, reluctance to move and a pale shrunken comb from the end of week 2; venous pO2 down and pCO2 up only from week 4; deaths weeks 3 to 6 (17 vs 9, no test; cold confounded with a richer diet). | Full text, verifier read. |
| O1, O2 | Field case reports | Confirmed, with context | Liu 2016 (China, 27-day flock, poor ventilation): depressed, drooping wings, penguin-like stance, fast breathing, less eating and drinking, then squatting still until death; fluid 500 to 600 mL. Pati 2015 (India): "frog-like" posture because the belly stopped the legs bearing weight, so birds could not reach feed or water; but the flock was an aflatoxin case with deaths by day 15. | Both full text, verifier read. |
| K1, K2 | Welfare Footprint pain hours | Confirmed as a model | Fatal ascites: 130 h Disabling (whole track, not only the fluid phase), 39 min Excruciating (an assumed 1% share of 28 to 100 h). The chapter text elsewhere says 3 h Excruciating. Non-fatal pulmonary hypertension: 84 h Disabling. "Tentative hypothesis", from human analogies. | Chapter 3 **grepped**; tables viewed by verifier. |
| K3 | "0.5 to 4% flock mortality from ascites" | Wrong | Cites Merck's SDS page, which gives 0.5 to 4% for SDS. | Verifier downloaded the SDS page; chapter **grepped**. |
| N1 | Live oxygen saturation | Confirmed ⚠️ | Julian and Mirsalimi 1992, 6-week males: SpO2 62.1% in birds with right ventricular failure vs 86.0% in heavy and 91.6% in light birds. The light birds were stunted or leg-deformed, not a slow strain. | ⚠️ abstract only. |
| N7 | Stress hormone before death | Confirmed ⚠️ | Luger 2003: corticosterone raised 2 to 3 weeks before death in ascitic birds. The only direct stress measure found. | ⚠️ abstract only. |
| N8 | Haematocrit 26 to 28% normal vs 33 to 40% ascitic | Not in source | Azizian 2013 reports haematocrit by hybrid in healthy males (25.4 to 33.3%). | Full text, verifier read. |
| O8 | Time from first sign to death | No figure anywhere | Only Welfare Footprint (citing Julian 2005) says birds "may survive for a few days with visible ascites symptoms". Gemini's "several days" (cited to Gupta 2011) could not be read. | All groups. |
| M3d | EFSA 2010's scoring | New fact | EFSA 2010's expert ranking gave ascites from fast growth a welfare-impact median of 0.40 (0.24 to 0.60), low against leg and mobility problems; scores are not on a linear scale. EFSA 2010 also says prevalence "may have decreased" (industry data, "anecdotally"). | EFSA 2010 **grepped** (table line). |
| M4 | RSPCA breed protocol | Confirmed, with fixes | Ascites mortality capped at 1.0% (2017: after week 1; 2026: after day 12); Hubbard JA757 is the control breed. Birds found dead on their backs must be recorded, not investigated. It guides a breed-acceptance trial, not a farm audit, and is not an automatic pass or fail. | Both protocols read in full, verifier. |
| M5 | "Prolonged agony" | Not in source | The phrase is in no source read. Welfare Footprint credits it to Olkowski and Classen 1998, an arrhythmia paper whose abstract lacks it; Kalmar 2013's abstract lacks it. RSPCA "Eat. Sit. Suffer. Repeat." says ascites "develops gradually, causing the birds to suffer for an extended period", citing a review. | RSPCA report ⚠️ partial; abstracts. |

Hidden disease is common. Julian 1987 (abstract): 32% of 925 males had marked right ventricular
hypertrophy at 48 days, but 3.5% died. Boostani 2010 (**grepped**): 17.50% of control birds were
visibly ascitic, 10.83% died of it. Huchzermeyer 1988 (full text): 8.5 to 18.4% of normal-looking
birds had RV:TV above 0.29.

## Part 3: farm-manager levers

| ID | Lever | Verdict | What the source says | Read |
|---|---|---|---|---|
| H3, H2 | Mash instead of pellets | Works | See C9. Bölükbasi 2005 found no growth cost; Kuleile 2020 found a large one (2,470 vs 1,698 g at 28 days). | **grepped** |
| H4 | Time-limited feeding | Works under challenge | Boostani 2010, 480 male Cobb, simulated 1,890 m plus cold: feed 8 h a day on days 7 to 21 cut ascites deaths from 10.83% to 4.16%; gain 2,224 vs 2,286 g, not significant; feed conversion better (1.93 vs 1.99). Later windows cost significant gain. | **grepped** (Table 2) |
| H6a | Low protein (18%) | Works, at a large cost | Bölükbasi and Emsen 2006: zero ascites deaths under cold, but 1,823 vs 2,160 g at 42 days (16% lighter). | OCR, verifier read |
| J3 | Lighting with more dark | Weak evidence | Hassanzadeh 2003, 2,000 m: ascites deaths 18 (continuous) vs 6 (intermittent) vs 7 (increasing) of 120; one room per treatment, no test; same feed conversion. The other lighting trials (Buys 1998, Hassanzadeh 2000) used T3 dosing. Aviagen says extra dark for ascites is "unnecessary" at low altitude for its birds. | Hassanzadeh 2003 **grepped** (18); tech note, verifier read |
| J7 | "30 to 40% cut from 6 h dark" | Not in source | Welfare Footprint's figure, citing two T3-dosed intermittent-lighting trials and a body-fat paper; neither ascites abstract gives a percentage. | Chapter 3, verifier read |
| I2, I4 | Vitamin C, CoQ10, L-carnitine | Work under cold only | Nemati 2017 (see C6). Wang 2013: L-carnitine 100 mg/kg cut ascites mortality 10.2% to 5.88% (p = 0.037) under a cold cycle; no growth effect. | Full texts, verifier read |
| I5 | Arginine, furosemide | Partly | Wideman 1995: 1% arginine cut mortality in one of two experiments; furosemide 0.015% depressed weight in one of two. Drug, not a farm lever. | ⚠️ abstracts |
| A5 | Brooding temperatures | Breeder guidance | Aviagen whole-house profile: 30 °C at day-old down to 20 °C at day 27. Deaton 1996 minimums 29.4, 26.7 and 24.4 °C in weeks 1 to 3 (via Aftab and Khan, second-hand). | Tech note and handbook, verifier read |
| A6 | CO2 limit | Breeder guidance | Aviagen: above 3,500 ppm "causes ascites"; ideal under 3,000 ppm. No primary study read. | Verifier read |
| A7 | Sodium limits | Secondary | 0.12% in water and 0.20% in feed (Acta review quoting Julian 1992). Julian 1992's own abstract (truncated) is thin: two cases at those levels, no significant difference. | Review full text; ⚠️ Julian abstract |
| P6 | Incubation temperature | One direction supported | Molenaar 2011 (abstract): eggshell 38.9 vs 37.8 °C from day 7 raised ascites mortality 3.8% (points or relative not stated). İpek, Sahan and Sözcü 2015 (full text) found no ascites death difference. | ⚠️ Molenaar abstract |
| L1, L4 | Slower breed | Works | Forseth 2023 (see C1). Al-Saeedi 2026, Denmark: ascites in 10.1% of dead Ross LD birds vs 4.7% of Rustic Gold (PR 2.12); vs Ross HD 1.72, not significant; flock mortality did not differ. | Forseth **raw-checked**; Al-Saeedi full text, verifier read |
| H7 | Hunger cost of restriction | Not in any source | No author of a restriction trial mentions hunger or welfare cost. | All group H sources |

## Part 4: prevalence, genetics and other facts

- **Condemnation data.** USDA FSIS and NASS fold ascites into "Miscellaneous" post-mortem
  condemnations (2023: 1,600,400 young chickens, 0.017% of 9.38 billion slaughtered, an upper bound).
  NASS October 2026 release: young-chicken live weight 6.67 lb. Neeteson 2023 shows a falling
  Canadian ascites-related condemnation rate from 1995 to 2022 as a figure only, credited to
  breeding and management together.
- **Norway.** Forseth 2023 (**raw-checked**): ascites was the top condemnation cause in Ross. Winter
  prevalence ratio Ross vs Hubbard 6.54. Ross ascites rose with slaughter age, which is why Norsk
  Kylling could not keep Ross past 32 to 33 days. Forseth 2024: transport deaths 0.063% vs 0.015%.
- **Natural incidence with ECGs.** Olkowski and Classen 1998 (abstract): 13 ascites cases in 505
  commercial broilers (the abstract prints 2.25%; 13/505 is 2.57%).
- **Breeder claims.** Aviagen has used pulse oximetry in selection since 1991 (Neeteson 2023) and
  says SaO2 rose as body weight rose; breeder-authored.
- **Sex.** Moghadam 2001: female hazard about 0.24 of males. Huchzermeyer 1988 and Namakparvar 2014
  found no sex difference.
- **Altitude physics.** Druyan 2012's "7 mmHg per 1,000 m" (**raw-checked** as quoted) looks too
  small; inspired oxygen pressure falls about 18 mmHg from sea level to 1,000 m. Treat it as a
  quoted figure.
- **Two Bahadoran 2010 papers.** Group G's (Int J Vet Res 4(1):11, 3 h at 15 °C on days 3 and 4,
  8 vs 16 deaths) and group P's (Iran J Vet Res 11(1):64, incubation at 1,800 m, 8 vs 15 deaths of
  125) are different studies.

## Sources that only Arda can open

Each needs a person at a browser (a bot check I may not click, or a publisher login). Ordered by
what they would settle for the memo.

1. Baghbanzadeh and Decuypere 2008, *Avian Pathol* 37:117, https://www.tandfonline.com/doi/pdf/10.1080/03079450801902062. Settles C2 (25% and 35%).
2. Kalmar, Vanrompay and Janssens 2013, *Vet J* 197:169, https://doi.org/10.1016/j.tvjl.2013.03.011 (closed). Settles "prolonged agony" and prevalence.
3. Druyan, Hadad and Cahaner 2008, *Poult Sci* (PubMed 18420980; ScienceDirect open copy, PII S0032579119388716). Settles C7's n and generation. Also Druyan 2007a and 2007b.
4. Pavlidis et al. 2007, *Poult Sci* (PubMed 18029797, OUP). Settles C10's growth cost per generation.
5. Closter et al. 2012, *Poult Sci* 91:556, https://academic.oup.com/ps/article/91/3/556/1554649. Settles the 12.2% vs 6.6% sex figures.
6. Julian, McMillan and Quinton 1989, https://www.tandfonline.com/doi/pdf/10.1080/03079458908418641; Julian 1988 and Diaz 1994 on the same site. Settles the cold and diet split and the RV:TV tiers (C8).
7. Julian 2000, *Avian Pathol* 29:519, https://www.tandfonline.com/doi/pdf/10.1080/03079450020016751, and Wideman et al. 2013, https://www.sciencedirect.com/science/article/pii/S003257911939827X/pdf.
8. Bendheim 1992a,b, https://www.tandfonline.com/doi/pdf/10.1080/03079459208418855 and `...418856`. Settles C6 (ventilation) and the pellet figures.
9. Hartcher and Lum 2020, https://doi.org/10.1080/00439339.2019.1680025.
10. CIWF Norsk Kylling case study, https://www.compassioninfoodbusiness.com/media/7455910/norsk-kylling-pioneers-of-higher-welfare-and-sustainable-chicken-production.pdf.
11. Lee 2022 dissertation, https://scholarworks.uark.edu/cgi/viewcontent.cgi?article=6220&context=etd.
12. Lower priority: Daneshyar 2009 and Shinder 2011 (early cold), Buys 1998 and Hassanzadeh 2000 (lighting), Molenaar 2011 (incubation), Orr 1986 (https://pmc.ncbi.nlm.nih.gov/articles/PMC1680187/), Gupta 2011 (duration of signs).
