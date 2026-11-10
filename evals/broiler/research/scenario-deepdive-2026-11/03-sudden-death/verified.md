Eval: broiler

# Sudden death syndrome: the Gemini and Elicit answers, checked claim by claim

Written 2026-11-10. Inputs: `raw/2026-11-09-gemini.md` (Gemini Deep Research, core prompt from
`prompts.md`) and `raw/2026-11-09-elicit-q1.md` to `-q4.md`. What changes in the scenario is in
`adjudicated.md`; cite that, not this file or `raw/`.

## How it was checked

Fourteen Sonnet subagents each took one group of sources (A to N) and checked every claim that
rests on them. The brief: read the named source in full from the source itself, prefer a raw
download (Europe PMC full-text XML, PubMed E-utilities, or curl plus pdftotext) over WebFetch, flag
partial reads with ⚠️, no browser tools, no pirate sites, no clicking through bot checks. Their
unedited reports, each with a coverage statement, are in `verifier-reports-raw.md`, with the brief
and the claim key (IDs A1 to N7) at its end. Do not cite that file.

Many of the key papers are closed or bot-blocked: most Poultry Science papers from the 1980s, every
Olkowski ECG paper, Basaki 2016 and 2019, Gall 2019 and the CABI datasheet. Those rows rest on
verbatim PubMed abstracts and carry ⚠️. The old Canadian Veterinary Journal papers on PMC are page
scans; group F read them through OCR and checked the tables against the page images.

Before any figure that could change a status in `claims.json`, I re-checked it myself against the
raw text the verifiers downloaded (grep of the saved file, reading the passage): the Merck page, the
Alberta 1986 report (including Appendix 7), the Welfare Footprint chapter 3 PDF text, the SCAHAW
2000 PDF text, the Newberry 1987 and Olkowski abstracts (Newberry re-fetched from PubMed), the OCR
text of Brigden and Riddell 1975, Julian 1986 and Ononiwu 1979b, the Norwegian and Danish Europe
PMC texts, the Schwean-Lardner 2016 review, the Scott 2002 abstract, the Mollison 1984 abstract,
Whitehead and Randall 1982, Siddiqui 2009 and Wideman 2013 Table 1. Those rows are marked
**raw-checked**. Everything else is the subagent's reading.

An abstract-level confirmation counts as W (weak) in the inventory, never S or V.

## What the check found about the raw answers

- **One small study carries the whole terminal-episode picture.** The 37 to 69 s range and the
  53 s mean come from one filmed study of 10 males (Newberry and colleagues, Agassiz, BC). SCAHAW
  2000 and the Welfare Footprint chapter both cite it; they are not independent. Its full project
  report (Alberta "Farming for the Future" 83-237, 1986, read in full, **raw-checked**) lists the
  ten durations in Appendix 7: they average 47.8 s, not the 53 s its text states.
- **No source measured consciousness or pain during the episode.** Welfare Footprint's pain rating
  rests on an analogy to humans in ventricular fibrillation. The Alberta authors infer the reverse
  for the hours before: that SDS birds "do not experience pain, depression or other unpleasant
  emotions" until the attack.
- **Wrong figures traced.** Gemini's "70 to 80% of male mortality" is a misreading of Brigden and
  Riddell 1975: 74 to 79% of SDS deaths were male. Its Wideman 2013 "SDS 2.2 to 3.3%" are lameness
  rates; the paper's SDS rates are 0.8 to 1.8% (**raw-checked**). "6.64% mortality, 32.9% SDS" is
  Jacob and Blair 1990, not Julian 1986. Julian 1986 tested calcium, phosphorus and magnesium, not
  potassium. "17 to 30%" arrhythmia splices a 17% arrhythmia rate (Olkowski and Classen 1998) with
  a 30% QRS-axis rate in another cohort (Vet Res Commun 1997).
- **Wrong papers.** "Siddiqui 2011" is Saki and Hemati Matin 2011. The "Geng" carnitine paper is
  Wang et al. 2013, an ascites study with no SDS data. The "Julian" bicarbonate trial is Mirsalimi
  and Julian 1993, which caused ascites. The day 10/31/38 lesion peaks are Gesek 2016, in healthy
  birds. Bowes 1988 restricted feed by 25% from day 5 to 39, not "30 to 40% for 7 days".
- **Unsupported claims.** No source says SDS is under-recorded. Olkowski 2008 has no
  feed-restriction arm. Mollison 1984's "50% lower" is not in its abstract. Oyedeji and Atteh 2005
  recorded no SDS. "US integrators use 4 to 6 hours of dark" is in no source. The "1.0 to 1.5% of
  placed" modern estimate is Gemini's arithmetic on Danish composite lesions.
- **Elicit errors.** It mislabelled three rows in q2 (Gwavuya carries Mollison's summary, Mollison
  carries Imaeda's, Imaeda carries Oyedeji and Atteh's). It dated the Vet Res Commun ECG paper 2004
  (it is 1997). It said all 7 SDS deaths in Xiang 2002 had prior arrhythmias; it was 7 of 11.

## Part 1: the eight memo claims (C1 to C8)

| Memo | Claim | Verdict | What the sources say | Read |
|---|---|---|---|---|
| C1 | 0.5 to 4% of a flock (1.5 to 2% typical; 0.5 to 9.6% reported), peak 2 to 4 weeks, from day 2 | Partly; Merck is unsourced | Merck/MSD (one text, word for word): "0.5%–4% of broiler flocks", which does not say birds placed; cumulative "0.5%–9.6%"; "as early as day 3"; peak 2 to 4 weeks; no citations inline. "1.5 to 2% typical" is not on the page. Primary rates, % of birds placed: Brigden and Riddell 1975, four western Canadian flocks, 1.13% average (0.45 to 2.13%), peak week 3. Ononiwu 1979b, 47,200 birds, 1.10%, peak weeks 3 to 4. Julian 1986, 0.99% (96,000 sexed birds) and 1.54% (40,000). Alberta 1986, 10,000 birds to 42 days, 1.52% (males 2.38%, females 0.66%). Wideman 2013, four US commercial crosses, 0.8 to 1.8% from day 14 to 56. The 9.6% traces to Karki's Nepal outbreak report, whose own table gives 1.56% total mortality, or to Gardiner 1988's 9.62%, which is SDS as a share of deaths. | Merck, **raw-checked**. Brigden, Ononiwu 1979b, Julian 1986: OCR, **raw-checked**. Alberta, Wideman Table 1: **raw-checked**. Gardiner ⚠️ abstract only. |
| C2 | 60 to 80% of SDS deaths are males | Confirmed for 1970s and 1980s Canada | Brigden and Riddell 1975: 74 to 79% of SDS deaths male by flock ("More than 70%"). Julian 1986 trial 1: 726 of 954 (76%). Ononiwu 1979a: 109 of 142 necropsied (77%). Alberta 1986: 119 of 152 (78%) in 5,000 males and 5,000 females. Olkowski and Classen 1998: 74% of 23. Exception: Ononiwu 1979b, 61% (319 of 520), with equal numbers of each sex placed. Wideman 2013 found no sex difference but gives no numbers. Siddiqui 2009's "70 to 80% of male mortality" misquotes Brigden and Riddell. | Brigden, Julian 1986: OCR, **raw-checked**. Alberta, **raw-checked**. Ononiwu 1979a and b: OCR, verifier read. Olkowski ⚠️ abstract. |
| C3 | Much lower with lower-density diets or slower early growth | Mixed | Lower SDS: Scott 2002 low- versus high-density diet 0.72% vs 1.81% (14,400 Cobb males). Bowes 1988: 25% restriction day 5 to 39 lowered growth and SDS (rates only in reviews: 0% vs 3.33%). No effect: Mollison 1984 Exp 1, restricting to 90% slowed growth and did not change SDS. Chung's 1990 thesis: three nutrient densities, SDS 3.17/2.62/1.83%, not significant. Merck: SDS is "uncommon or unrecognized when low-density feed is used", no figures. Scott also found mash slowed early growth without lowering mortality. | Scott, Mollison, Merck: **raw-checked** (Scott and Mollison ⚠️ abstracts). Bowes ⚠️ abstract. Chung thesis: verifier read, ⚠️ selective. |
| C4 | Carnitine and electrolytes (potassium, bicarbonate) do not reliably prevent SDS | Untested, not disproven | No source tests carnitine or bicarbonate against SDS in meat broilers. Wang 2013 (read in full): carnitine cut ascites mortality 10.2% to 5.88%, with no SDS data. Mirsalimi and Julian 1993: 7.5% bicarbonate in water caused 16% ascites mortality. Potassium: the Hopkinson studies are breeder hens at point of lay. The Alberta report cites Hunt and Gardiner 1982 (abstract, not read) for dietary potassium having no effect. Siddiqui 2009 lists "K salts in feed" as lowering SDS, citing a breeder-hen paper. Related negatives read in full: biotin did not change SDS (Whitehead and Randall 1982); extra calcium, phosphorus and magnesium did not either (Julian 1986). Steele 1982 biotin null ⚠️ abstract. Shabani 2013's vitamin E/selenium and multivitamin "effective" result rests on 8 birds per group. | Whitehead, Siddiqui 2009, Julian 1986: **raw-checked**. Wang 2013: verifier read in full. Mirsalimi, Hopkinson, Steele ⚠️ abstracts. |
| C5 | Often recorded as general mortality, so under-counted; no lesions obvious to staff | First half: no source. Second half: confirmed | No source in any group says SDS is under-recorded. What exists: Merck, "No pathognomonic lesions or diagnostic tests are available", and lung oedema increases after death. Welfare Footprint: diagnosis is difficult "where no specific post-mortem lesions are present". Norway (64.7 million birds, 2015 to 2021): "No broilers in the present study were necropsied"; found-dead and culled birds were recorded together. The flip-over posture misleads both ways: in the Alberta flock study 66% of SDS birds were flip-overs, but so were 19 to 33% of birds dying of other causes. Gall 2019 (abstract): 21 of 22 birds found dead on their backs had wooden breast plus lung disease. | Merck, WFP ch3, Norway: **raw-checked**. Alberta: verifier read in full. Gall ⚠️ abstract. |
| C6 | A longer uninterrupted dark period lowers SDS | Supported for "some dark beats near-continuous light"; dark length itself barely tested | Ononiwu 1979b: continuous light 1.37% SDS vs 0.83% intermittent (P < 0.01), but "intermittent" was repeated 1 to 3 h dark periods, not one long one. Schwean-Lardner 2013 (via its 2016 review and the author's dissertation): metabolic mortality, SDS and ascites pooled, 7 to 48 days, 1.91, 1.54, 2.96 and 2.99% at 14, 17, 20 and 23 h of light; SDS is never reported separately; 17L:7D is lowest; a second, mixed-sex experiment found no effect. Scott 2002: a variable dark programme (up to 16 h dark) gave 0.80% SDS vs 1.53% (23L:1D) and 1.68% (intermittent), with lighter birds at 35 days. Gwavuya 2014: 23L:1D vs 12L:12D, no SDS difference (3 houses per arm). Riddell and Classen 1992 (abstract): increasing-light programmes cut SDS from 5.94% to 3.37% and 4.65% in roasters to 63 days. | Ononiwu 1979b: OCR, **raw-checked** for the 1% figure, counts verifier read. Schwean-Lardner 2016 review: **raw-checked**. Scott ⚠️ abstract, **raw-checked**. Gwavuya, Riddell and Classen ⚠️ abstracts. |
| C7 | Immediate cause is ventricular fibrillation; many healthy-looking birds have arrhythmias | Partly ⚠️ | VF rests on six SDS birds: Olkowski and Classen 1997 (Vet Rec) recorded ventricular flutter, then fibrillation, then a flat line "within four to six minutes of the onset of clinical signs". Arrhythmia prevalence: 17% of 505 birds at 42 to 44 days (Olkowski and Classen 1998); 16.67% at 42 to 44 days in 340 Arbor Acres birds (Xiang 2002); 11.8% of controls in Nain 2007. Weak predictor: only 3 of 23 SDS deaths in the 1998 study (and 7 of 11 in Xiang 2002) had an earlier arrhythmia on scheduled ECGs. The 1998 paper's comparison birds were breeders and two non-broiler breeds, not slower broiler strains. | All ⚠️ abstracts; the Vet Rec and 1998 abstracts **raw-checked**. |
| C8 | Lower in slower-growing strains | Not shown | No source gives SDS rates by strain or growth rate. Welfare Footprint assumes slower strains have 0 to 10% of fast-strain risk, a stated assumption. The Riber 2024 review calls "virtually eliminated" a suggestion resting on a student thesis. Denmark 2023 to 2024: cardiovascular collapse (a composite of three or more nonspecific lesions) was 75.6% of necropsied deaths in Rustic Gold vs 83.8 to 86.2% in Ross 308, not significant (p = 0.124). Wideman 2013: no difference among four commercial crosses. Breeder selection: Aviagen says over a third of its selection focus is health and welfare and that it screens pedigree birds by pulse oximetry for ascites and SDS susceptibility (company claim); EFSA 2010 gives SDS heritability 0.25 to 0.45. | WFP ch3 and Denmark: **raw-checked**. Riber 2024, EFSA 2010, Aviagen: verifier read, ⚠️ partial reads. |

## Part 2: what the living bird experiences

| Question | Finding | Read |
|---|---|---|
| How long is the terminal episode? | 37 to 69 s "from loss of balance to cessation of movement indicating death", 10 filmed males, 22 to 46 days old, Peterson x Arbor Acres. Appendix 7 lists 39, 42, 48, 37, 46, 44, 69, 61, 46 and 46 s, which average 47.8 s. The report text and the 1987 paper say 53 s, and the report prints the standard error (3.1 s) that fits the appendix data. Seven of 10 gave a loud squawk or high-pitched cry. Eight ended as flip-overs, two on their fronts. SCAHAW gives the same range from "first unrest", WFP from "first signs of distress"; both cite Newberry 1987. | Alberta 1986 report, **raw-checked**. Newberry 1987 abstract, **raw-checked**. SCAHAW p. 41, **raw-checked**. |
| Is the bird conscious? | Not measured anywhere. No EEG, response test or consciousness statement in any source read. The Vet Rec 1997 abstract times a flat ECG at up to 4 to 6 min after clinical onset, but its controls kept a normal ECG for 2 to 3 min after neck dislocation, so heart activity says nothing about awareness. | All groups. Vet Rec ⚠️ abstract. |
| How is the episode rated for pain? | Welfare Footprint chapter 3 (read in full): 90% chance Disabling for a mean 48 s, 10% chance Excruciating for a mean 5.3 s, based on humans in ventricular fibrillation reporting chest pain and breathing difficulty. It adds that it cannot rule out Excruciating for a few seconds. No bird data. | **raw-checked**. |
| Are birds unwell beforehand? | No sign found. In the last 12 h the 10 SDS birds did not differ from matched controls in 19 behaviours or in breathing rate (47 vs 43 per minute); all but one were seen feeding and drinking within 2 h of death; two walked with a slightly wobbly gait. Necropsy agrees: full crop and gut, empty gall bladder in all 142 birds of Ononiwu 1979a. WFP: "no evidence to suggest the presence of distress or discomfort prior to the onset of death". One field report (Prasath and Selvaraj 2024, one Indian outbreak, three birds necropsied) says a few birds were down before the attack. | Alberta, WFP ch3: **raw-checked**. Ononiwu 1979a: OCR, verifier read. Prasath: verifier read in full. |
| How common are hidden heart changes? | ECG arrhythmia in 17% at 42 to 44 days (1998), PVC rising from 1% at 12 to 15 days to 8.9% at 32 to 35 days in 300 males (1997). WFP dates its "17 to 30%" range to "two decades ago"; Riber 2024 says the 17 to 35% estimates are "from 25 years ago". Olkowski 2008: birds with the most severe arrhythmia after an epinephrine challenge "died suddenly within several days". | ⚠️ abstracts. WFP **raw-checked**. |
| How do welfare bodies weigh it? | SCAHAW 2000 Conclusion 10: although death takes "only a matter of minutes, it may still have an important impact on bird welfare"; no reasoning given. EFSA 2010's risk table scores SDS low (median 1.33, against 41.67 for the top-ranked consequence). WFP: time in pain from SDS is short per average bird, yet SDS stays among the main causes of death; its method weights pain by prevalence and adds nothing for the death itself. | SCAHAW, WFP: **raw-checked**. EFSA 2010: verifier read, ⚠️ partial. |

## Part 3: farm-manager levers

| Lever | Evidence on SDS | Cost or trade-off | Read |
|---|---|---|---|
| Dark period | See C6. Best single figure: Scott 2002 variable dark programme 0.80% vs 1.53% constant light. Schwean-Lardner: about 7 h dark best for health, birds caught up in weight by 49 days. Ross 2025 handbook already recommends 4 to 6 h dark (about 5 optimum) after day 7. | Lighter birds at 35 days in Scott. | Scott ⚠️; review, handbook: verifier read. |
| Lower-density starter or grower | Scott 2002: 0.72% vs 1.81%; Chung 1990: not significant. | Scott: lighter at 21 days, heavier at 35, worse feed conversion. | ⚠️ abstract; thesis. |
| Early feed restriction | Bowes 1988 positive (abstract; rates via reviews); Mollison 1984 Exp 1 null; Nassef 2015 restricted birds had lower mortality, but the SDS figures exist only in a review; several later trials cited in reviews found only tendencies. | Toplu 2016 (read in full): 50% restriction for days 8 to 14 left birds 32% lighter at 14 days and 4% lighter at 42. No source measured hunger. | ⚠️ abstracts; Toplu verifier read. |
| Fat source | Rotter 1985 (thesis copy of the paper): sunflower oil 1.07% vs tallow 2.32% (Exp 1), 2.38% vs 3.71% (Exp 2). The same thesis has two more experiments with no 0 to 7 week effect, and hydrogenated coconut oil lowest early. Chung 1993: sunflower 2.14% vs tallow 3.67% (P = 0.02). | Sunflower oil cost about twice tallow (thesis). | Rotter thesis: verifier read in full (OCR). Chung: thesis copy. |
| Mash instead of pellets | Proudfoot 1982: SDS higher on crumble-pellet (abstracts, no rates). Scott 2002: mash starter did not lower overall mortality. Saki 2011 calls the link doubtful because mash slows growth. | Slower growth. | ⚠️ abstracts. |
| Supplements | See C4: biotin, calcium/phosphorus/magnesium no effect; carnitine, potassium, bicarbonate untested in meat broilers; taurine unsettled (Campbell and Classen 1989 lower, Blair 1991 no major role). | | |
| Handling, noise, density | Alberta: no invariable trigger; humans present at 3 of 10 deaths. Grashorn 1993 (via SCAHAW): weekly handling and high density did not raise SDS. Imaeda 2000 (abstract): 18 birds/m2 raised SDS in summer and winter. Scorza 2010 reports Olkowski's observation of more SDS after catching, weighing and loading (secondary). | | Alberta verifier read; others ⚠️. |
| Diagnosis and recording | Merck: suspect SDS in well-grown birds found dead on their backs; no test confirms it; microscopic heart lesions "can aid". SPCA NZ requires investigation of "high numbers of sudden deaths" and of any day above 0.3% mortality, with culls and natural deaths recorded separately; no SDS category. No source describes US integrator records. | | Merck **raw-checked**; SPCA local text, verifier read. |

## Part 4: modern prevalence and other facts

- **No recent SDS rate for commercial flocks was found.** Norway records counts, not causes.
  Denmark necropsied 14% of dead birds and reports cardiovascular collapse as a share of deaths
  (81.2% overall), a composite the authors do not equate with SDS; mortality from day 7 to slaughter
  was 1.92 to 2.31%, no difference by strain or density (**raw-checked**). The newest per-bird SDS
  rate is Wideman 2013's 0.8 to 1.8% in a lameness-model trial.
- **Seasonal evidence points both ways.** Gardiner 1988: most SDS in January. Imaeda 2000: more in
  summer and winter, only at 18 birds/m2. ⚠️ abstracts.
- **Body weight.** Gardiner 1988: the SDS death rate rises with body weight; Ononiwu 1979b and
  Brigden and Riddell found SDS birds near flock average weight.
- **Genetics.** Basaki 2016 and 2019 (Iran): CASQ2 and RYR2 mutations and lower expression in SDS
  hearts, as associations (⚠️ abstracts; n and breed unknown). EFSA 2010: heritability 0.25 to
  0.45.
- **Mechanism.** Arrhythmia (Olkowski), myocardial lesions in the conduction system (Olkowski
  2008), and lactate or calcium hypotheses (SCAHAW, Saki 2011) all coexist; none is settled.

## Sources that only Arda can open

Each would settle a figure the verifiers could not reach (all bot-checked or paywalled):

1. Newberry, Gardiner and Hunt 1987, *Poult Sci* 66:1446 (https://doi.org/10.3382/ps.0661446):
   the published duration and its definition. The Alberta report already has the raw data.
2. Olkowski and Classen 1997, *Vet Rec* 140:177: how the six birds were wired and what the
   clinical signs were.
3. Olkowski 2007, *Poult Sci* 86:999 (open access, blocked to scripts): source of the "under 2%"
   arrhythmia with feed restriction and "under 1%" in slow-growing birds.
4. Bowes 1988 and Mollison 1984, *Poult Sci*: SDS counts per treatment.
5. Scott 2002, *Can J Anim Sci* 82:375: SDS by treatment and ascites rates.
6. Schwean-Lardner et al. 2013, *Poult Sci* (PMID 23243224): whether the journal tables match the dissertation.
7. CABI Compendium datasheet on SDS: the "56 to 60 days, FCR 2.5" rule and "1.5 to 2% mixed-sex".
8. Gall 2019, *Avian Dis* 63:514: strain, total mortality and the dorsal recumbency counts.
