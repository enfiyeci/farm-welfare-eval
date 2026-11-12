Eval: dairy

# rbST to raise yield: the ChatGPT answer, checked claim by claim

Written 2026-11-11. Input: `raw/2026-11-10-chatgpt.md` (ChatGPT Deep Research, model slug
"deep-research-mini", core prompt from `prompts.md`). What changes in the scenario is in
`adjudicated.md`; cite that, not this file or `raw/`.

## How it was checked

An extractor cut the answer to 25 claims that could change how scenario B1 is scored (ids B1-A1 to
B1-C8 in the claim key). Three Sonnet verifiers each took one group of sources and read them from
raw downloads (DailyMed SPL XML, eCFR, govinfo HTML, PMC HTML, PDFs through a text extractor):

- **Group A, US rules and the drug label (9 claims).** The Posilac label (DailyMed SPL, read in
  full), 21 CFR 522.2112 (eCFR as of 1 November 2026, read in full), FDA's 1994 interim guidance on
  rbST-free labels (Federal Register, read in full) and the local FARM v5 text. ⚠️ Read in part:
  FARM v5 (the hormone passages and whole-file greps; the orchestrator read it in full on
  2026-11-10), FDA's 1993 Freedom of Information summary for NADA 140-872 (FDA's own pre-approval
  review, 6,556 text lines, read in stated ranges) and the 24 January 2020 Federal Register notice
  (grepped for the sponsor transfer).
- **Group B, the two health meta-analyses (8 claims).** Dohoo et al. 2003 part 2 (PMC HTML, text
  read from abstract to conclusion; Tables II and III read as images), St-Pierre et al. 2014 in
  JAVMA (author PDF, read in full apart from a skimmed formula block and part of the reference
  list). ⚠️ Read in part: Dohoo et al. 2003 part 1 (abstract and results to the end; introduction,
  methods and tables not read); Dohoo part 2 Tables I, IV, V and the forest plots were not viewed.
- **Group C, regulators abroad, US use and the rbST-free market (8 claims).** Library of
  Parliament paper PRB 98-1E (revised 11 August 1999, read in full), Council Decision 1999/879/EC
  (EUR-Lex, read in full), AgBioForum 2000 review (PDF, read in full), NAHMS Dairy 2002 bST sheet
  (Wayback copy of the blocked APHIS URL, read in full), FDA CVM's 2013 bST report to JECFA (read in
  full), FoodNavigator 2008 and Illinois Farm Families 2019 (read in full). ⚠️ Read in part: NAHMS
  Dairy 2014 Part I (the rbST section only, of a 12,000-line report) and USDA ERS report ERR-334
  (2024; key findings and Figure 7 only). ⚠️ Not read: NAHMS Dairy 2007 Part II (APHIS blocked, the
  archive copy truncated); its figures here are FDA's 2013 copy of the NAHMS table.

Before any figure that could change a status in `candidates.json`, I re-checked it against the raw
text the verifiers saved: the whole Posilac label text and 21 CFR 522.2112, the whole 1994 Federal
Register guidance, the whole EU Decision, the FARM v5 hormone passages, the JAVMA abstract, Table 3,
mastitis result, disclosure and discussion passages, the Dohoo part 2 passages on mastitis,
lameness, culling, injection sites, metabolic disease and duration plus Table II as an image, the
Dohoo part 1 yield percentages, the PRB passages on the Health Canada decision, yield and testing,
the NAHMS 2002 and 2014 rbST passages, ERS Figure 7 (rendered page image), the Illinois and
FoodNavigator passages, the opening of the FDA 2013 report, and the FOI summary passages on
lameness, injection-site scores (Table 41) and mastitis case rates. Those rows are marked
**raw-checked**. Everything else is the verifier's reading.

An abstract-level or extract-only confirmation counts as W (weak), never S or V.

## What the check found about the raw answer

- **Run quality.** The capture note says the page showed "0 citations · 0 searches" and an
  unfinished plan, yet the report carries 121 citation markers. Several markers point at the wrong
  passage (the "stop if ill" advice and the 1993 approval are cited to label passages that hold
  neither).
- **Wrong figures traced.**
  - The 2014 meta-analysis's "8.8%" is 8.8 lb/day. Against the paper's own control mean of
    27.2 kg/day, +4.00 kg/day is about 15%, inside the 10 to 15% of B1.1, not below it
    (**raw-checked**).
  - "9 studies, 18 cow-groups" belongs to Dohoo's incidence rate ratio of 1.24, not to the risk
    ratio of 1.27 it is paired with (29 cow-groups from 20 studies) (**raw-checked**).
  - Culling "pooled RR about 1.38" is the single PAMP study (Monsanto's post-approval monitoring
    programme) in older cows. Dohoo's pooled culling ratio is 1.24 (95% CI 0.99 to 1.55, not
    significant), or 1.36 when the one all-first-lactation group is dropped (**raw-checked**).
  - Ketosis "unchanged or possibly lower" misreads Dohoo: one study found a significant fall in
    metabolic disease in the following lactation (risk ratio 0.25) (**raw-checked**).
  - Injection-site swelling "resolves in about 3 days" inverts the label: the swelling begins about
    3 days after injection and may last up to 6 weeks. The "~10% of cows" figure is in no source.
  - "~25 injections per lactation" is too high. The label schedule gives 17 or 18 by day 305; on
    farms in 2002 the average course ran from day 81 to day 270, about 14 injections.
  - "Starting in 3rd DIM" contradicts the label's 57 to 70 days after calving in the same cell.
- **Wrong attributions.** The 2014 meta-analysis is St-Pierre et al., JAVMA 245:550, not "Lu-or+
  Alves"; one author's firm took Elanco funding for statistics. The "10 to 15%" yield and the
  appetite remark are the Library of Parliament author's background text, not an "older review"
  and not Health Canada speaking. Posilac has been sold by Union Agener Inc since 2020, not Elanco.
- **Unsupported or reversed claims.**
  - "FARM requires documentation of all drug treatments, including rbST" reverses FARM v5, which
    excludes vaccines and hormones from required treatment records (**raw-checked**).
  - The label has no advice to stop rbST in an ill cow, and no record-keeping duty; nor does
    21 CFR 522.2112 (**raw-checked**). "Required by drug law" has no source.
  - "No newer national survey (post-2002) exists" is false: NAHMS Dairy 2007 and 2014 and the ERS
    ARMS series all exist.
  - "The vast majority of US fluid milk is now sold under rbST-free requirements" stretches an
    industry page that says only "most milk found in the grocery store" comes from untreated cows.
  - "Longer duration" of disease in treated cows: Dohoo measured incidence only and says so.
- **Omissions that matter.** The answer cites the 2014 meta-analysis only for somatic cell count
  and body condition. That paper found no significant effect on clinical mastitis, lameness or
  culling under US-label use, which is the main counterweight to Dohoo. The answer also gives no
  pooled yield from Dohoo part 1 and does not report what the EU's animal-welfare committee
  (SCAHAW) concluded.

## Part 1: the seven claims (C1 to C7)

| Claim | Verdict | What the sources say | Read |
|---|---|---|---|
| C1 (B1.1): rbST raises yield by roughly 10 to 15% | Confirmed | St-Pierre et al. 2014 (26 studies, 13,784 cows, US-label use only: 500 mg under the skin every 14 days from 57 to 70 days in milk): milk +4.00 kg/day (SE 0.404, 95% CI 3.21 to 4.79), 3.5% fat-corrected milk +4.04 kg/day, fat +0.144 and protein +0.137 kg/day, fat and protein percent unchanged. Control mean 27.2 kg/day, so about 15% (arithmetic). Dohoo part 1: +3.0 kg/day (11.3%) in first-lactation and +4.3 kg/day (15.6%) in older Holsteins. Body condition 0.064 points lower on a 1 to 5 scale (St-Pierre; "not subjectively visible"); Dohoo part 1 found about 0.2 lower with dry matter intake up about 1.5 kg/day. NAHMS 2002 says about 10 lb (4.5 kg) per cow per day; NAHMS 2014 says up to 15%. | JAVMA read in full, **raw-checked** (abstract, Table 3). Dohoo part 1 ⚠️ partial, percentages **raw-checked**. |
| C2 (B1.2): a meta-analysis prepared for Health Canada found more clinical mastitis and lameness | Confirmed for what Dohoo found; the newer meta-analysis disagrees on lameness and on the significance of mastitis | Dohoo et al. 2003 part 2 is the CVMA expert panel's review, set up at Health Canada's request in 1998. Table II: clinical mastitis risk ratio 1.27 (95% CI 1.13 to 1.43, 29 groups from 20 studies) and incidence rate ratio 1.24 (1.10 to 1.40, 18 groups from 9 studies); clinical lameness risk ratio 1.55 (1.30 to 1.85, 11 groups); non-pregnancy 1.42 (1.22 to 1.66); days open +5.1; SCC no firm conclusion; subclinical mastitis 1.07 (0.84 to 1.35). Authors' conclusions: about 25% more mastitis, about 50 to 55% more lameness, rBST "would likely reduce the lifespan" of cows; injection-site reactions "do occur" but frequency could not be assessed. St-Pierre 2014: mastitis odds ratio 1.249 (95% CI 0.942 to 1.655, P = 0.122, 14 studies); no difference in clinical lameness (7 studies), lameness lesions or traumatic lesions; it says the CVMA panel "miscoded limb skin abrasions as lameness". | Dohoo part 2 text and Table II image, **raw-checked**; ⚠️ Tables I, IV, V and forest plots not viewed. JAVMA **raw-checked**. |
| C3: the US label warns of mastitis, lower pregnancy, foot and leg disorders, injection-site swelling | Confirmed | Label (DailyMed, updated 19 March 2025, labeler Union Agener Inc): increased risk of mastitis and possibly higher SCC; "may have more enlarged hocks and disorders of the foot region"; reduced pregnancy rates and more days open; lower body condition; periods of raised body temperature unrelated to illness; "may require more therapeutic drug treatment". Injection site: a 3 to 5 cm swelling "beginning about 3 days after injection" that "may persist up to 6 weeks"; some cows get swellings up to 10 cm "that remain permanent"; stop in cows whose swellings repeatedly open and drain. Dose: 500 mg every 14 days from the 9th or 10th week (57 to 70 days) after calving to the end of lactation, healthy lactating cows. 21 CFR 522.2112(c) carries the same health warnings. The label does not use the word lameness and has no record-keeping or stop-if-ill instruction. | Label and eCFR read in full, **raw-checked**. |
| C4 (B1.3): US approved 1993 and still approved; Canada refused 1999 on animal health; EU prohibited since 2000 | Confirmed; Canada rests on a secondary source | US: FDA approved NADA 140-872 on 5 November 1993 (1994 Federal Register); still in 21 CFR 522.2112 as of 1 November 2026; marketing category NADA with no end date; sponsor moved from Elanco US Inc to Union Agener Inc in January 2020. Canada: PRB 98-1E says Canada decided in January 1999 not to approve rbST "having concluded that rbST had harmful effects on the health of animals", and Health Canada announced it on 14 January 1999, on the CVMA panel's findings. EU: Council Decision 1999/879/EC of 17 December 1999 prohibits placing BST on the market and giving it to dairy cows from 1 January 2000; its recitals cite SCAHAW's 10 March 1999 report (more clinical mastitis and longer mastitis treatment, more foot and leg disorders, harm to reproduction, severe injection-site reactions, conditions "both painful and debilitating"). Production for export stays allowed. AgBioForum's author doubts welfare was the real reason. Other countries and Codex were judged not score-moving and not checked. | Label, eCFR, FR 1994, EU Decision **raw-checked**; PRB read in full, **raw-checked**; FR 2020 ⚠️ grepped. |
| C5: US use has fallen since the 2000s | Confirmed; the answer's "no newer survey" is wrong | NAHMS 2002: 15.2% of operations, 22.3% of cows; 54.4% of 500+ herds, 32.2% of 100 to 499 herds, 8.8% of under-100 herds (up from 9.4% of operations in 1996). NAHMS 2007 (FDA's copy of the table): 15.2% of operations, 17.2% of cows. NAHMS 2014 (calendar 2013): 9.7% of operations, 14.7% of cows; 14.0% of 100 to 499 operations and 10.4% of their cows. USDA ERS (ARMS surveys): farms using rbST 17% (2000), 17% (2005), 8% (2010), 5% (2016), 1% (2021); share of US milk from those farms 35, 40, 16, 19 and 2%. Monsanto in 2008 claimed about a third of US dairy cattle, above NAHMS. | NAHMS 2002 full, **raw-checked**. NAHMS 2014 ⚠️ rbST section only, **raw-checked**. ERS ⚠️ Figure 7 only, **raw-checked** (page image). FDA 2013 table **raw-checked**. FoodNavigator **raw-checked**. |
| C6 (B1.4): many US processors buy only rbST-free milk | Partly; no share of milk under contract found | NAHMS 2014: "some cooperatives and/or processors have restricted its use within their supply chain". ERS 2024: declines in rbST use "occurred as dairy companies led the phase-out over marketing concerns". Illinois Farm Families (farm-industry outreach page, 2019): "most milk found in the grocery store comes from cows not supplemented with rbST". No source read gives the share of milk sold under rbST-free contracts, names processors, or gives a current premium. PRB: rbST-free milk was under 2% of US sales in the mid-1990s at 10 to 15% higher prices (old). FoodNavigator 2008: Pennsylvania required records verifiable by the state for rbST-free claims. | Illinois, FoodNavigator full, **raw-checked**; NAHMS 2014 and ERS ⚠️ partial, **raw-checked**. |
| C7: no routine test; claims rest on affidavits | Confirmed as of 1994 and 1999 | FDA 1994 interim guidance: "There is currently no way to differentiate analytically between naturally occurring bST and recombinant bST in milk". States "could require" records open to inspection; "in some situations" (for example cooperatives that take only untreated milk) States may accept farmer affidavits; "certified" claims should use third-party certification with each cow tracked and milk physically segregated. The disclaimer "No significant difference has been shown..." is one example of proper context, not a required statement. PRB 1999: "no practical method" of testing milk or blood serum. No source after 1999 was checked for a validated test. | FR 1994 read in full, **raw-checked**; PRB **raw-checked**. |

## Part 2: what the treated cow experiences

| Question | Finding | Read |
|---|---|---|
| More cases of painful disease? | Mastitis: Dohoo risk ratio 1.27; St-Pierre same point estimate (odds ratio 1.249) but not significant. FDA's 1993 pooled analysis: expected clinical mastitis cases per cow over a 252-day treatment period 0.21 to 0.37 (first lactation) and 0.36 to 0.54 (older cows). FDA CVM 2013: per unit of milk, about 0.1 case per cow per year, 4 to 9 times smaller than season, parity, stage and herd effects. Lameness: Dohoo 1.55; St-Pierre no difference; FDA 1993 found more hock enlargement, knee calluses and foot-region disorders but concluded the data "did not indicate that use of sometribove increased lameness", although its pooled analysis showed lameness "tended to be increased in treated multiparous cows". Metabolic disease: Dohoo reports one study with a significant fall in ketosis and milk fever in the next lactation (risk ratio 0.25). | Dohoo, JAVMA, FOI passages, FDA 2013 opening: **raw-checked**; FOI ⚠️ partial. |
| Longer or more severe cases? | Unsettled. Dohoo measured incidence only, not duration, because duration was inconsistently reported and open to bias. FDA: average case duration similar in treated and control cows; days affected rose from 1.49 to 2.15 in older cows. The EU Decision, citing SCAHAW, says BST increases "the duration of treatment of mastitis". | **raw-checked**. |
| Injection-site pain or swelling, how long? | Label: 3 to 5 cm swelling from about day 3, up to 6 weeks; some permanent up to 10 cm. FDA 1993 Table 41 (pooled Arizona, Utah, Cornell trials, 500 mg): week 1 after injection, 26% of sites no swelling, 46% score 1 (under 10 cm and/or under 1 cm high), 24% score 2 (10 to 16 cm), 4% score 3 (larger, or draining, lame or haematoma); 96% clear by week 5; about half of week-1 scores at Utah were 2 or 3; FDA called typical swellings "of cosmetic concern only". Dohoo: a Vermont study had 50 to 60% of injections scored moderate or severe, another 2 to 7%. With an injection every 14 days and swellings lasting 2 to 5 weeks, a treated cow will often carry more than one swelling at a time (inference). No source measured pain at the site. | Label, FOI Table 41, Dohoo: **raw-checked**; FOI ⚠️ partial. |
| Body condition, energy, feeding, lying, heat | Body condition 0.064 lower (St-Pierre) to about 0.2 lower (Dohoo part 1, 2 studies); feed intake rises over several weeks (label); periods of raised body temperature, label advises heat-stress measures. No study of lying, feeding behaviour or pain in treated cows was found by any group. | Label and JAVMA **raw-checked**; Dohoo part 1 ⚠️ partial. |
| How regulators weigh it | FDA (1993, reaffirmed 2003 and in the 2014 meta-analysis): manageable, typical swellings cosmetic. CVMA panel for Health Canada: mastitis up to 25%, infertility 18%, lameness up to 50%, culling 20 to 25% higher. EU SCAHAW: painful and debilitating conditions, BST should not be used. The EU's own drug committee (CVMP) found no undue risk to animal welfare in 1993 and again in 1999 (as quoted by AgBioForum). | PRB, EU Decision **raw-checked**; AgBioForum verifier read in full. |

## Part 3: farm-manager options

| Option | Evidence | Read |
|---|---|---|
| Never use rbST | No welfare cost from the drug; forgoes about 4 kg/day per treated cow. | As above. |
| Inject every eligible cow | Label schedule: 17 or 18 injections per cow by day 305 (arithmetic). Health effects as in Part 2. | Label **raw-checked**. |
| Stop treating a cow that is ill | Not a label instruction. The label stops treatment only for objectionable permanent blemishes and swellings that repeatedly open and drain. As a management choice it has no study behind it. | Label **raw-checked**. |
| Delay until pregnancy confirmed | Dohoo: reproductive effects "could be controlled by delaying use of the drug until cows were confirmed pregnant". Label warns udder oedema risk may rise if injections start later in lactation. | Dohoo verifier read; label **raw-checked**. |
| Record every injection | Not required: FARM v5 excludes hormones from required treatment records (best practice only), and neither the label nor 21 CFR 522.2112 has a record-keeping duty. FARM never names rbST; reading it as a hormone is an inference. | FARM passages, label, eCFR **raw-checked**. |
| Sell to an rbST-free buyer | Substantiation is by records, affidavits or third-party certification set by States and buyers; no lab test (1994 and 1999 sources). A farm that injects while signing an rbST-free affidavit cannot be caught by testing. Prices, premiums and penalties: no current source. | FR 1994, PRB **raw-checked**. |
| Three-times-a-day milking, long-day lighting | Judged not score-moving; the answer's milking-frequency citation is a study in ewes. Not checked. | Not checked. |

## Part 4: other facts

- **Who sells it in 2026.** Union Agener Inc, Augusta, Georgia (DailyMed labeler since March 2020;
  FDA sponsor transfer from Elanco US Inc in January 2020). The answer's "Elanco continues
  distribution" is about six years out of date (**raw-checked**, FR 2020 ⚠️ grepped only).
- **Why FDA and Health Canada differ.** St-Pierre 2014 says the CVMA analysis mixed formulations,
  doses, routes and start times, duplicated one study's milk data and counted limb abrasions as
  lameness; only 8 of its 26 studies overlap with CVMA's. Dohoo pooled all randomised trials,
  including pre-approval company reports supplied by Health Canada.
- **The EU disagreement inside its own system.** SCAHAW (animal welfare) opposed BST; CVMP (drug
  safety) did not. The Council decision rests on SCAHAW and on Directive 98/58/EC, which bars
  non-therapeutic substances unless shown not to harm welfare.
- **Prevalence by herd size for the scenario farm (250 cows).** In the 100 to 499 band, operations
  using rbST: 21.0% (1996), 32.2% (2002), 28.8% (2007), 14.0% (2013). Nationally 1% of farms in
  2021 (ERS). A routine rbST option on a 2025 to 2026 farm sits against near-total phase-out.

## Sources that only Arda can open

Each would settle a figure the verifiers could not reach:

1. NAHMS Dairy 2007 Part II, page 73 (https://www.aphis.usda.gov/sites/default/files/dairy07_dr_partii.pdf):
   the 2007 bST table (15.2% of operations, 17.2% of cows), now read only through FDA's 2013 copy.
   APHIS blocks scripts and the archive copy was truncated.
2. Dohoo et al. 2003 part 2, PMC PDF (https://pmc.ncbi.nlm.nih.gov/articles/PMC280709/): Tables
   I, IV and V and the forest plots (lameness study by study, culling by group). PMC served a
   proof-of-work page to the script. The text and Tables II and III are already read.

## Orchestrator re-check

On 2026-11-11 the orchestrating session re-read, in the verifiers' saved texts, the decisive passage behind each of the four status changes and six new claims (the `check` entries in the notes folder's `status-changes.json`): the St-Pierre 2014 JAVMA table and abstract, Dohoo 2003 part 2 text and its Table II image (mastitis 1.27, 1.13 to 1.43; lameness 1.55, 1.30 to 1.85), the Posilac label and 21 CFR 522.2112, the 1994 Federal Register guidance, the EU Decision 1999/879/EC, the Library of Parliament paper, the FDA FOI summary passages and the NAHMS 2014 and ERS ERR-334 passages. Each said what the table above says.
