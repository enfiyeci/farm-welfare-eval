Eval: broiler

# Breast myopathies: the Gemini and Elicit answers, checked claim by claim

Written 2026-11-09. Inputs: `raw/2026-11-09-gemini.md` (Gemini Deep Research, core prompt from
`prompts.md`) and `raw/2026-11-09-elicit-q1.md` to `-q4.md`. What changes in the scenario goes in
`adjudicated.md` (not yet written); cite that, not this file or `raw/`.

## How it was checked

Thirteen Sonnet subagents each took one group of sources (A to M) and checked every claim that rests
on them. The brief: read the named source in full from the source itself, prefer a raw download
(Europe PMC full-text XML, or curl plus pdftotext) over WebFetch, flag partial reads with ⚠️, no
browser tools, no pirate sites, no clicking through bot checks. Their unedited reports, each with a
coverage statement, are in `verifier-reports-raw.md`, with the brief and the claim key (IDs A1 to
M6) at its end. Do not cite that file.

Unlike scenario 4, most verifiers here read raw text rather than WebFetch summaries. Even so, before
any figure that could change a status in `claims.json`, I re-checked it against raw text myself:
seven papers re-downloaded from Europe PMC on 2026-11-09 (PMC13141717, PMC11472612, PMC9283645,
PMC9012353, PMC9720342, PMC7597843, PMC11259736), plus the local EFSA 2023 and Aviagen handbook
text. Those rows are marked **raw-checked**. Two rows rest on a verifier's own raw download, which I
grepped (the Engormix page and the Sihvo thesis PDF); they say so. Everything else is the
subagent's reading.

An abstract-level confirmation counts as W (weak) in the inventory, never S or V.

## What the check found about the raw answers

- **Live-bird evidence is thin but no longer absent.** Three primary studies measured something in
  living birds and linked it to woody breast found after death: self-righting and wing extension
  (Hisasaga and Makagon 2026), dorsal recumbency (Che 2022c), and gait (Norring 2019, abstract
  only). One small study found no activity difference (Ross 2020, abstract only), and Hisasaga and
  Makagon 2024 found none at 6 weeks. **No study in any group measured pain.** The word does not
  appear in Hisasaga 2024, Hisasaga 2026 or Che 2022c (raw-checked).
- **Wrong papers and spliced papers.** Gemini merged two 2026 *Animals* papers into one "Hoque et
  al. 2026" (Hoque is 16(10):1553; the URL it gave, 16(18):2959, is Kościów et al.). It credited
  Lorenzi 2014's medium-versus-heavy figures to Petracci 2013. Its GAA P-values (0.039, 0.015) come
  from de Souza 2024, which it never cites, and it reversed one of them: GAA raised the mild-WB
  share (20.5% to 26.8%), it did not reduce it. The vitamin E null result is Kuttappan 2012, not
  2013a. The DOI it gave for "Radaelli 2017" is Papah et al. 2017.
- **Wrong citation details.** Che 2022c is *Poult Sci* 102(2):102307 (raw-checked), not
  101(12):102207. Gall 2019 has no author "Sarsour". The lighting paper PMC10685017 used 2 lux, not
  5 lux. Norring 2019 used over 340 birds of five hybrids, not 266 Ross 308.
- **Overstatements.** Gemini calls live palpation, wing partition and serum CK "validated". Only
  Hisasaga 2026 reports diagnostic accuracy, in 58 hand-picked birds. Gemini's 76.9% "failure rate
  of pronounced wing partition" is the severe-WB failure rate; the wing-partition rate is 82.1%.
- **A false negative.** Gemini said no myopathy data exist for Hubbard JA757. They do
  (Składanowska-Baryza 2025, PMC12489921).
- **Elicit errors.** It reversed the Ranger Gold severe-WB pair in Hisasaga 2024 (it read the
  abstract, which prints the pair in the opposite order to the Ross 708 pair). It named arginine as
  Bodle 2018's best treatment; vitamin C scored lowest. It said Adewole 2021's strain was not
  reported (it is Ross 308) and undercounted Zamora 2022 (35 birds per week, 315 in all).

## Part 1: the ten memo claims (C1 to C10)

| Memo | Claim | Verdict | What the sources say | Read |
|---|---|---|---|---|
| C1 | Severe WB rises sharply above about 2.7 kg | No WB source; the figure is about **white striping** | The only "2.7 kg" found is a Barbut 2020 symposium paper (Engormix) saying that, per Kuttappan 2013a, the incidence of severe **WS** rises above 2.7 kg. The WB data show no cliff there. Aguirre 2020 Table 2, severe WB (score 3) by live weight: 0% under 2.0 kg, 1% at 2.0 to 2.5 kg, 10% at 2.5 to 3.0, 10% at 3.0 to 3.5, 12% at 3.5 to 4.0, 31% above 4.0 kg (n = 4,332, seven Texas A&M trials, mixed ages and strains). In Aguirre's adjusted model live weight is not significant once breast weight and strain are in. Mueller 2023 shows a steady rise in mean WB score to about 3.4 kg, then flat. Aviagen's only threshold is "> 3 kg or 6.6 lbs". | Aguirre PMC7597843, **raw-checked**. Aviagen handbook, **raw-checked**. Engormix: the verifier's raw HTML download, grepped. Kuttappan 2013a ⚠️ abstract only, no weight figure in it. Mueller: verifier read. |
| C2 | Plant sorting cuts the loss but does nothing for the bird; only genetics or growth management prevent it | Partly | Barbut et al. 2024 frames farm growth-rate changes and plant sorting as "short-term solutions" and genetic selection as long-term, and says non-genetic factors explain over 65% of variance. It never discusses the live bird, so "does nothing for the bird" is our inference (sorting happens after death). It says spaghetti meat "does not seem to occur in the live bird". The C2 figures are Barbut et al. 2024 (*Poult Sci* 103:103801, PMC11259736), not Barbut and Leishman 2022. Over US$1 billion is "later, when prevalence increased", with no "per year". The "deli loaves 25 to 50%" figure is in neither paper. | Barbut 2024, **raw-checked**. Barbut and Leishman 2022 grepped only ⚠️. |
| C3 | WB odds 1.75 above 78 g/day gain (males) | Confirmed, **raw-checked** | OR 1.75 (95% CI 1.12 to 2.73) vs 70.7 to 78.0 g/day, males only. Outcome is WB present or absent at any severity. Not a literature meta-analysis despite the title: a pooled dataset from the authors' own eight Padova trials (1,278 scored birds; Ross 708, Ross 308, Cobb 500; Italy; 41 to 48 days). | Bordignon 2022, PMC9283645, full text |
| C4 | WB odds 1.23 at 2.46 to 2.63 kg | Confirmed, wrong outcome, **raw-checked** | OR 1.23 (1.03 to 1.47) vs 1.94 to 2.29 kg, but the outcome is **any** WB (WB1 plus WB2 recoded to 1; 82.4% of fillets), not severe WB (11.8%). All 37 flocks were Ross 708. Every flock was under 2.7 kg, so the paper cannot test C1. Table 5 prints the band as "2,460–2,360", a typo. | Che 2022b, PMC9012353, full text |
| C5 | Severe WB 24.2% Ross 708 vs 4.7% Ranger Gold; total 90.5% vs 76.4% | Confirmed for controls, **raw-checked** | Control-group figures as stated. The 3.20 and 2.76 kg weights are means of all birds (control plus exercised), not of controls. Exercise cut severe WB to 12.9% (Ross 708) and to a value printed as "0.02%" (Ranger Gold), which is impossible for about 107 birds; most likely zero birds. Sex is not stated anywhere in the paper. WB was scored after death, not by live palpation. | Hisasaga and Makagon 2024, PMC11472612, full text |
| C6 | Four strains: severe WB 5, 35, 5 and 16% | Wrong label; secondary only | The four figures are severe **white striping**, from the same Barbut 2020 symposium paper citing Kuttappan 2013a. Kuttappan 2013a studies WS only and predates the WB scale. Its abstract gives 8.3% severe WS overall, which four equal strains at 5, 35, 5 and 16% (mean 15.25%) would not give. Table 1, which would settle it, was not reachable. | Engormix: verifier's raw download, grepped. Kuttappan 2013a ⚠️ abstract only. |
| C7 | Males 25.2% vs females 12.1% (Ontario) | Wrong attribution, **raw-checked** | The figures are Bordignon 2022 (Padova), not Che 2022b (Ontario). They are averages of per-trial percentages from experimental trials, mostly ones testing ways to cut myopathies. Female OR 0.55 (0.40 to 0.75) is univariable. Che 2022b collected flock sex: WB odds 1.56 times higher in male flocks, unadjusted, and sex dropped out of the final model. | Bordignon and Che 2022b, full texts |
| C8 | High-energy diets worsen WS | Confirmed at abstract level ⚠️ | Kuttappan 2012a: high-energy diet gave more severe WS fillets (P < 0.05); 280 straight-run birds, 54 days, FCR 2.08 vs 2.28. The percentages Gemini gives (8.70 vs 1.46% severe) are not in the abstract; they are consistent with counts out of 138 and 137 fillets. | ⚠️ abstract only |
| C9 | WS odds rise with breast weight and genotype | Confirmed, **raw-checked** | Breast weight above 960 g OR 1.49 (1.03 to 2.15) vs 850 to 960 g; Cobb 500 vs Ross 708 OR 2.75 (1.37 to 5.52). The Ross 708 reference group is one trial of 63 birds. | Bordignon 2022, full text |
| C10 | Lesions from about 2 weeks; a 1950s line shows almost none | Confirmed at abstract level ⚠️, timing supported by Sihvo | Chen 2019 abstract: lesions "as early as 2 weeks", worse with age in three commercial strains; the 1950s ACRB line had minimal lesions that did not progress. Its correlation coefficients and P-values are unreadable. Sihvo's thesis: no WB at 10 days, first macroscopic WB at 15 or 18 days depending on schedule, first degeneration about 12 to 15 days. Gemini's "phlebitis and degeneration at 14 days" for Sihvo is not in it, but the memo's "about 2 weeks" holds. | Chen ⚠️ abstract only. Sihvo thesis: verifier's raw PDF text, onset passage grepped and read. |

## Part 2: what the living bird experiences

The memo's N claim. Every live-bird study scored WB only after death, so all results are
associations.

| ID | Claim | Verdict | What the source says | Read |
|---|---|---|---|---|
| F1, F2 | Severe-WB birds often cannot right themselves | Confirmed, **raw-checked** | Hisasaga and Makagon 2026 (*Poult Sci* 105(7):106912): 58 market-age birds from three California farms, placed on their backs for up to 60 s. All 14 birds without WB righted (median 1.36 s); 7 of 18 moderate-WB birds and 20 of 26 severe-WB birds did not (median 60 s). Birds were picked to balance wing categories, so these are not flock rates. | PMC13141717, full text |
| F3 | Wing partition detects WB in live birds | Confirmed | Partition of 1.5 cm or more detected any WB with 93.1% accuracy; 5.5 cm or more detected severe WB with 82.8%. Specificity rests on 14 normal birds. | Same, verifier read |
| D1 to D9 | Dorsal recumbency syndrome (DRS) is linked to WB | Partly, **raw-checked** | Che 2022c: 64 Ross 708 birds (33 DRS, 31 controls culled for other reasons), four Ontario flocks. DRS correlated with WB histology (rho 0.82) and gross WB; DRS birds had higher CK and AST, and most could not lift their wings above 45°. Lungs and heart did not differ. The abstract's opening line says DRS birds "eventually die of cardiopulmonary insufficiency", but that is background from Gall 2019, not a Che finding. No pain or welfare measure; the authors say causation is unproven. | PMC9720342, full text |
| D10 | Gall 2019: WB in birds dying on their backs | Partly ⚠️ | One 4,000-bird teaching flock, last 16 days: 63 deaths and culls, 70% with WB; WB plus lung disease in 68% of mortality, "including 21 of 22 dead birds found on their backs". Case report, no controls. | ⚠️ abstract only |
| E1 to E4 | Norring 2019: WB birds walk worse | Partly ⚠️ | Over 340 birds of five hybrids, 22 to 43 days: gait 2.9 vs 2.6 pooled over ages; fewer movement bouts while lying. WB birds were also heavier. The authors call it an association. | ⚠️ abstract only |
| E5 | Ross 2020: no activity effect | Confirmed ⚠️ | 25 individually housed cockerels; no effect of WB on total activity. Only 5 severe birds. | ⚠️ abstract only |
| C7 (group C) | Hisasaga 2024: less activity in severe WB | Wrong framing | 21 vs 16 grid squares, P = 0.09; the authors say activity "did not differ". Every bird with gait score 2 or worse (25 of 401) had WB. | Full text, verifier read |
| E6 | Zamora 2022: blood markers and behaviour | Partly | CRP and H:L ratio not linked to WB grade. Behaviour was recorded per group, never per bird, so it cannot test a link. | Full text, verifier read |
| F5, F6 | Kawasaki 2016 and 2018: wing lift and enzymes | Partly | 2016 is three affected vs three control birds, no accuracy figure. 2018: 10 vs 10 hand-picked birds; affected birds lost back-to-back wing contact; 4 of 10 died. CK and AST were raised only at about 20 days. | Full texts, verifier read |
| H5 | Severe-WS birds have raised muscle enzymes | Confirmed ⚠️ | Kuttappan et al. 2013 (*Poult Sci* 92:339): higher CK, ALT, AST and LDH the day before slaughter; no sign of systemic infection. | ⚠️ abstract only |
| M1 | EFSA 2023 names breast myopathies as a welfare consequence | Not in source, **raw-checked** | Two passing mentions of "wooden breasts": as one trigger of locomotory disorders, and as an inflammation risk from too much enrichment-driven exercise. No hits for white striping, spaghetti meat or deep pectoral myopathy. | EFSA local text, searched |
| M2 | CIWF lists six welfare impacts | Confirmed (advocacy source) | Six impacts as stated. CIWF also says "no studies to date have definitively shown" that the myopathies are painful. The PDF dates from 2023, not 2022. | Wayback copy, verifier read |
| M3 | Welfare Footprint models breast myopathies | No | Chapter 7 lists muscle abnormalities, including wooden breast, as not analysed. | Verifier read in full |
| M5 | Aviagen on the live bird | Confirmed (breeder source) | "No clinical signs of BM on the farm" apart from WB hardness felt by palpation. | **raw-checked** |
| — | Authors on the gap | Confirmed | Kościów 2026: evidence "does not establish a direct quantitative relationship" between myopathy severity and validated welfare outcomes. Sihvo: pain is "difficult to demonstrate". Hisasaga 2026: "few studies" have looked at how WB affects the birds. | Kościów and Sihvo, verifier read; Hisasaga **raw-checked** |

## Part 3: farm-manager levers

| ID | Lever | Verdict | What the source says | Read |
|---|---|---|---|---|
| K2 | Feed allocation 95 to 85% of ad libitum | Confirmed | Meloche 2018: WB and WS severity fell linearly; final weight 3.75 vs 3.35 kg; mortality fell. Most of the gain came at 95%. | ⚠️ journal abstract; dissertation read in full |
| K3 | Diets at 90% of breeder density | Confirmed | Severe WB 20.8% vs 36.5%; starter-only reduction raised it. The same 20.8% and 42.3% pair appears in a different Meloche paper; one is likely a copy error. | ⚠️ abstract plus dissertation |
| K4 | Shorter photoperiod 14L:10D | Confirmed for WS | WS 89.5% to 64.6%; WB not significant (8.3% vs 4.2%). | Gratta 2023 full text |
| K5, J3 | Early feed restriction (days 13 to 21) | Does not work | WB unchanged; WS 10 points **higher** (trend). Benefit lasted only while restriction lasted. | Trocino 2015 and Gratta thesis |
| K6 | Dim light (2 lux) | No effect | No change in WB or WS at day 36; 100% of sampled birds had moderate or severe WB. | Flees 2023 full text |
| K7 | Combined package (GAA, phytase, amino acid changes) | Confirmed | WB risk −19.2%, WS −26.3%, spaghetti meat +37.7%; treated birds killed two days later. | Dayan 2026 full text |
| K8 | Amino acids −30% | Confirmed | Severe WB near zero at 47 days; lower body weight. Cutting energy 16% made WB **worse**. | Zhang 2025 full text |
| L1 | GAA 0.06 to 0.12% | Partly | Real effects, wrongly attributed (see the list earlier). Maynard 2023: only 0.12% was significant. Khalil 2021: severe WB 28.6% to 8.9% at 0.12%. No growth penalty in any trial. | Mixed; Cordova-Noboa and Maynard ⚠️ abstracts |
| L3 to L8 | Arginine, vitamins C and E, ethoxyquin, phytase, folic acid | Mostly partly | Bodle 2018: vitamin C best (score 1.27 vs 1.83). Meyer 2023: "12% more normal fillets" not significant (P = 0.646). Phytase cut WB severity about 5%, only at 1,000 FTU and above. Several trials are funded by the product maker. | See group L |
| C4 (group C) | Exercise | Lowers WB | Hisasaga 2024: exercise cut WB in both strains. EFSA's "too much exercise may increase the risk" cites older papers; no study read here shows it. | **raw-checked** |
| K9 | Hunger cost of restriction | Not in any source | No study measured hunger. The only measured welfare costs: short photoperiod raised footpad dermatitis risk 74% (Dayan 2026). | All group K sources |

## Part 4: prevalence, genetics and other facts

- **Heritability** (Bailey 2015, Aviagen lines): WB 0.02 to 0.10, WS 0.19 to 0.34. "More than 90%"
  of WB variance and "greater than 65%" of WS variance non-genetic is Bailey's own statement. Bailey
  2020: two years of selection cut WB 18.4%; breast yield rose 1.02% (abstract) or 2.4% (results),
  inconsistent within the paper. Authors are Aviagen employees.
- **Prevalence at the plant varies widely by scoring.** Che 2022b, Ontario, 2.36 kg: any WB 82.4%,
  severe 11.8%, only 3.3% of fillets free of all myopathies (raw-checked). Valenta 2023, Alabama,
  56-day males: severe WB 23.3%, 12% myopathy-free. Lebednikaitė 2023, Lithuania: flock myopathy
  rose from under 10% at 2.35 kg mean weight to 25 to 33% at 2.72 kg. Fraga 2021, Brazil: 0.73% of
  carcasses condemned, a condemnation rate, not prevalence.
- **Petracci 2013 vs Lorenzi 2014.** Petracci: 28,000 fillets, 56 flocks, 12.0% WS. Lorenzi: about
  35,000 fillets, 70 flocks, severe WS 2.7% (medium) vs 9.5% (heavy). Both ⚠️ abstracts only.
- **Sex at matched weight is unsettled.** Santos 2021: the male excess vanished when body weight
  was a covariate. Maynard 2023 found more WB in females.
- **Slower breeds.** Santos 2021: conventional strains had the most WB at 3.2 kg, but one slower
  strain (F) matched them; breast yield predicts better than growth rate. Hubbard JA757: 17 of 32
  breasts with some WB, 3 severe (organic, Poland).
- **Not visible at the plant is not absent.** Trocino 2015: 97% of examined breasts showed damaged
  fibres on histology; gross and histological scores correlated only r = 0.30.

## Sources that only Arda can open

Each needs a person at a browser (a bot check I may not click, or a publisher login). Ordered by
what they would settle for the memo.

1. Kuttappan et al. 2013a, *Poult Sci* 92:811, https://doi.org/10.3382/ps.2012-02506 (Table 1). Settles C1 and C6: whether 5, 35, 5, 16% and the 2.7 kg step are in the paper.
2. Norring et al. 2019, *Animal* 13:1690, Helsinki repository https://hdl.handle.net/10138/304509. Settles the gait result per age and whether body weight was controlled.
3. Gall et al. 2019, *Avian Dis* 63:514, https://doi.org/10.1637/11995-111218-case.1 (BioOne). Settles the cause-of-death claim for birds on their backs.
4. Hisasaga, Orlowski-Workman and Tarrant 2025, *J Appl Poult Res* 35:100633, https://doi.org/10.1016/j.japr.2025.100633 (open access behind a bot check). Settles how reliable live palpation is.
5. Chen et al. 2019, *Avian Pathol* 48:319, https://doi.org/10.1080/03079457.2019.1598541. Settles the rest of C10.
6. Papah et al. 2017, *Avian Pathol* 46:623, https://doi.org/10.1080/03079457.2017.1339346. Settles whether it reports wing movement or failure to right.
7. Kuttappan et al. 2012a, *Poult Sci* 91:2677, https://doi.org/10.3382/ps.2012-02259, or the author's thesis at https://scholarworks.uark.edu/etd/530. Settles the C8 percentages.
8. Ross et al. 2020, *Appl Anim Sci* 36:447, https://doi.org/10.15232/aas.2019-01953.
9. Lever papers, lower priority: Cruz 2017 (https://doi.org/10.3382/ps/pew310, UFRGS copy http://hdl.handle.net/10183/302618); Meloche 2018 (*Poult Sci* 97:1786 and 97:1794); Zhang 2018 (https://doi.org/10.22175/rmc2018.111); de Souza 2021 (https://doi.org/10.1016/j.livsci.2021.104659); Maynard 2023 (*J Appl Poult Res* 32:100324); Petracci 2013 and Lorenzi 2014.

## Browser pass, 2026-11-09

Sources 1 to 8 on the preceding list opened in Arda's Chrome (Claude in Chrome), with his
authorization. No bot check was clicked, nothing was bought, no file was saved to disk. Reading
notes, one file per source, are in
`~/claude-sync/handoffs/enfiyeci-farm-welfare-eval/artifacts/handoff-2026-11-09-broiler-deepdive-s5-browser-apply/`
(outside git).
"Read in full" means the article from abstract to end, from the publisher page or the author
manuscript.

| # | Source | Read | What it settles |
|---|---|---|---|
| 1 | Kuttappan 2013a, *Poult Sci* 92:811 | In full (ScienceDirect, open access), plus Figure 2 viewed | **C6:** the "5, 35, 5, 16%" are Table 1 **counts** of severe white-striping fillets per strain (A 5, B 35, C 5, D 16 of 189, 184, 173, 193), misread as percentages. The true shares are 2.6, 19.0, 2.9 and 8.3%; 61 of 739 = 8.3% overall. Strains are unnamed; Cobb-Vantress supported the work. **C1:** the paper never states "2.7 kg". Figure 2 plots modelled severe-WS probability against **ready-to-cook carcass weight**, not live weight: about 2 to 8% up to about 2.55 kg, then about 11% at 2.65, 17% at 2.85 and 37% at 3.13 kg (read by eye). Mean carcass weight of severe fillets was 2.77 kg. Both figures are white striping, 59 to 63-day birds. |
| 2 | Norring 2019, *Animal* 13:1690 | In full (Helsinki author manuscript, extracted with pdf.js) | Males only, five unnamed hybrids, Finland. 266 birds analysed of over 340 housed; WB by palpation after death in 100 (38%). Gait 2.9 vs 2.6 (P = 0.001); fewer movements while lying, 2.0 vs 3.2 per 10 min (P = 0.046), in a video subset of 24 birds. **No per-age gait result:** the age-by-WB interaction was not significant and was dropped. **Body weight was not controlled** (WB birds 2,774 vs 2,620 g); the authors say the effects are "difficult to tease apart". Latency to lie did not differ. Pain "remains to be studied". |
| 3 | Gall 2019, *Avian Dis* 63:514 | ⚠️ Abstract only. BioOne full text needs a sign-in or a $20 purchase; Unpaywall and Europe PMC list no open copy. | Nothing new. Stays W. |
| 4 | Hisasaga, Orlowski-Workman and Tarrant 2025, *J Appl Poult Res* 35:100633 | In full (ScienceDirect, open access; no bot check appeared) | 210 straight-run Ross 708 at 49 days, Fresno. Live palpation agreed with the after-death severity score in 104 of 210 birds (49.5%). For presence alone, 27.1% were misclassified: 20.5% scored normal alive but had WB after death, 6.7% the reverse. From the counts, sensitivity is about 76% and specificity about 59% (my arithmetic). Live scoring over-called severe WB (31% vs 9%). One person did both scorings; blinding is not stated. Authors: live palpation is "not an accurate indicator of WB severity". |
| 5 | Chen 2019, *Avian Pathol* 48:319 | In full (Taylor and Francis free access). ⚠️ Table 1 (body weight by week and strain) did not load. | **C10 holds.** Histology, scored blind, 608 sections from 960 birds (three unnamed commercial strains plus ACRB). Lesions from 2 weeks, worst at 8. WB score vs body weight by week rs = 0.29, 0.40, 0.41, 0.47; vs lymphocytic phlebitis rs = 0.68. No ACRB section scored above 2 of 4, and ACRB lesions did not progress; ACRB birds were also far lighter, so the authors draw no genetic conclusion. No sex or incubation effect. Gemini's author "Sarsour" is on this paper (Albarra H. Sarsour), not on Gall 2019. |
| 6 | Papah 2017, *Avian Pathol* 46:623 | ⚠️ Not read. Taylor and Francis showed a Cloudflare "verify you are human" checkbox, which I may not click. The tab is left open in Arda's Chrome. | Open. |
| 7 | Kuttappan 2012a, *Poult Sci* 91:2677 | In full (ScienceDirect, open access) | **C8 confirmed in full.** 280 straight-run Cobb 500, 54 days. Table 2: severe WS 12 of 138 (8.70%) on the high-energy diet vs 2 of 137 (1.46%) on the low-energy diet; normal 25.4% vs 47.5% (both P < 0.05). Live weight 3,042 vs 2,787 g; FCR 2.08 vs 2.28. |
| 8 | Ross 2020, *Appl Anim Sci* 36:447 | In full, abstract to acknowledgments (ScienceDirect) | **E5 confirmed, now from full text.** 25 Ross 708 cockerels in single pens, slaughtered at 55 days (mean 3.5 kg); WB scores 0/1/2 = 6/14/5. WB had no effect on activity (P > 0.05), measured only as tracked movement from 05:30 to 09:30. No histology, no pain behaviours. The results mention a "restrictive feeding protocol" that the methods never describe. |
| 9 | Lever papers (Cruz 2017, Meloche 2018, Zhang 2018, de Souza 2021, Maynard 2023, Petracci 2013, Lorenzi 2014) | Not started | Open. |

What this changes, for `adjudicated.md` and `claims.json` (applied to both on 2026-11-09, and the
same day to the memo, register row 5 and the inventory page):

- C1 and C6: the dropped "2.7 kg" and "5/35/5/16%" figures are now traced to their source. Both
  are severe **white striping**, and the 2.7 kg is carcass weight. The four strain figures are
  counts. Per the handoff, note this in the src notes of the Aguirre 2020 and Hisasaga 2024
  claims and in the memo; do not restore them as WB claims.
- C8 (Kuttappan 2012a) and E5 (Ross 2020) move from abstract-level to a full primary read.
- C10 (Chen 2019) moves to a full primary read.
- E1 to E4 (Norring 2019) move to a full read, with two corrections: no per-age result, and body
  weight not controlled.
- F3 gains a second, larger accuracy study (Hisasaga 2025): live palpation detects presence
  moderately and severity poorly.
