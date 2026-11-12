Eval: dairy

# Buying gene-edited cattle: the Gemini answer, checked claim by claim

Written 2026-11-11. Input: `raw/2026-11-10-gemini.md` (Gemini Deep Research, core prompt from
`prompts.md`). What changes in the scenario is in `adjudicated.md`; cite that, not this file or
`raw/`.

## How it was checked

An extractor cut the answer to 26 score-moving claims in four source groups (the claim key, ids
G1-A1 to G1-D4). Four Sonnet verifier subagents each took one group:

- **A**, US rules and regulators: the three FDA risk assessment summaries (PRLR-SLICK, March 2022;
  its supplement, September 2025; Celtic polled, March 2026), FDA's list of risk-reviewed genomic
  alterations, the FDA approval summary for PRRS-resistant pigs, FDA guidance GFI #187B, and the
  local full-read texts of FARM v5 and EFSA 2023 calves.
- **B**, slick heat tolerance and side effects: Pozzebon et al. 2024, Dikmen et al. 2014, Cuellar et
  al. 2024 and 2026 (the two studies of gene-edited slick cattle), Sosa et al. 2022, and the review
  Gemini cited for farms cutting cooling.
- **C**, editing errors and how founder animals are made: Norris et al. 2020 (preprint,
  supplement, Author Correction), Young et al. 2020, the 2025 National Academies report on heritable
  genetic modification in food animals (NASEM), Hennig et al. 2020, Ryu et al. 2025, a chapter on
  cloned pregnancies (Chavatte-Palmer et al. 2014), the AAVS cloning comments (advocacy) and a
  MedCrave cloning overview.
- **D**, disease-resistance lines and the polled merit gap: Gao et al. 2017, Workman et al. 2023,
  Richt et al. 2007, a Bullvine article (trade press) and Mueller et al. 2019.

The brief: read each source in full from a raw download, flag partial reads with ⚠️, no browser
tools, no clicking through bot checks. Their reports, each with a coverage statement, are in
`verifier-reports-raw.md`. Do not cite that file.

Partial reads that matter: ⚠️ Sosa 2022 (abstract only; ScienceDirect blocked scripts); ⚠️ the
review Gemini cited for "studies note" farms cutting cooling (Nath, Roy and Basu 2026, abstract
only); ⚠️ the published Norris letter (paywalled after its first paragraph; the preprint and
supplement were read in full); ⚠️ GFI #187B (molecular sections and keyword searches only);
⚠️ Mueller 2019 (abstract, introduction and base-population methods); ⚠️ the AAVS comments, the
MedCrave piece and the NASEM report (targeted passages only).

Before any figure that could change a status in `candidates.json`, I opened the verifier's saved
text and read the passage myself. I read these in full: the three FDA risk assessment summaries,
the FDA risk-reviewed list page, Cuellar 2024 (the verifier had stopped before its Discussion), the
cloning chapter by Chavatte-Palmer (the verifier had read it by keyword), and the PRRS-pig approval
summary (the verifier had read 330 of 986 lines; I read the rest). I also fetched FDA's main page on
animal genomic alterations, which lists every approval (content current as of 2025-09-30; saved in
`work-drafter/fda-iga-parent/`). I read these passages: FARM v5 pages 38 to 39 and 105 to 106,
Dikmen 2014's design and results, the Pozzebon passages on FDA, lameness, prolactin, introgression
and cooling, Cuellar 2026's vaginal temperature methods and results and its funding note, the
Norris preprint passage on why the plasmid was missed and Supplementary Figure 1 (as an image), the
Author Correction page, the Young 2020 passages on health, plasmid inheritance and fate, the NASEM
methods table, the Gao, Workman and Richt passages named below, the Bullvine table line, the
Mueller merit passage and the Sosa abstract. Those rows are marked **raw-checked**. Everything else
is the verifier's reading. ⚠️ I did not re-read the raw Gemini answer; what it says comes from the
claim key, whose extractor read it in full.

An abstract-level confirmation counts as W (weak), never S or V.

**Relays.** Before this check every G1 status was a relay, not a check. G1.1, G1.2, G1.3, G1.4, G1.6
and G1.7 carried the read depth the August 2026 technology catalog records for Pozzebon, Norris and
Ishii (none of the FDA documents, Sosa, or the introgression studies had ever been opened). G1.6's
market claim and G1.8 carried the trait-pricing README's delegated sweep (web extraction; the FDA
document not opened). G1.5 was copied from C5.1, which had been checked on 2026-11-10. C5.4, the same
claim as G1.4, was a catalog relay too. This pass reads Pozzebon and the Norris preprint in full again
and, for the first time, the FDA documents and the edited-animal studies themselves.

Scope note: this file stays at the level of a farm purchase decision. Where a source goes into
editing technique, the table gives one plain sentence on what it means for the buyer's risk.

## What the check found about the raw answer

- **It denied a fact FDA reports.** Gemini said the FDA summary holds no heart-defect death, so that
  part of G1.1 "cannot be verified". It read only the 2025 supplement. The March 2022 summary reports
  the death, FDA's tracing of the risk markers to the unedited parents, and FDA's finding of
  unintended alterations the developer had not reported (**raw-checked**).
- **Wrong date and scope.** The Celtic polled determination is dated March 3, 2026, not
  "2024/2025", and covers four beef bulls (two Black Wagyu, two Hereford), no dairy breed. The 2025
  slick supplement reviewed purebred Holstein founders, not only "Holstein crosses"
  (**raw-checked**).
- **A wrong figure.** "Top polled sires trail top horned sires by 37 TPI points, a $299 Net Merit
  deficit" comes from a Bullvine table note giving the spread between the number 1 and number 10
  TPI bulls; the article never compares polled with horned sires on Net Merit and never mentions
  NAAB sales (**raw-checked** for the table line).
- **Quotes not in the sources.** The Norris Author Correction only adds that two authors contributed
  equally; it holds no "complex, multimeric integration events" (**raw-checked**). The disbudding
  sentence ("acute pain, tissue damage, and prolonged inflammatory discomfort") is not in the
  Bullvine page cited. "Studies note that relying solely on genetics while abandoning environmental
  cooling severely compromises holistic welfare" is not in Pozzebon and could not be checked in the
  review cited. "Minimal severe health detriments" is not in Cuellar 2026. Pozzebon writes that
  reduced lying "may end up causing lameness", not that it "drastically increases" it
  (**raw-checked**).
- **Mis-numbered and wrong citations.** [5], the pig approval summary, is cited for GFI #187B. [15],
  a 2025 laboratory paper on bovine zygotes, is cited for cloning practice and for a $300 to $600
  sequencing price that appears in no source read. Norris is given as 38:225 to 232, which is Young
  et al. 2020; Norris is 38:163 to 164. Hennig is dated 2023; it is 2020.
- **Overstatements.** GFI #187B is nonbinding guidance for the approval pathway and recommends
  whole-genome sequencing only "in some cases" (⚠️ partial read). FARM requires "pain mitigation"
  for disbudding; a local anaesthetic plus an NSAID is its stated best practice, not the requirement
  (**raw-checked**). The tuberculosis "challenge studies" measured immune markers, not disease. The
  edited-calf temperature result Gemini cites compares slick heifers with heifers carrying a
  nonfunctional receptor variant, not with normal-coated ones (**raw-checked**).
- **A premise that does not hold for slick.** Gemini framed all edited founders as cloned. The 2022
  slick founders came from edited embryos (**raw-checked**), as did the Cuellar herds and the 2025
  Jersey and Angus founders. Cloning applies to the 2025 Holstein slick founders, the original
  hornless bulls, the Wagyu polled founders and every disease-resistance line.
- **Unsourced.** "Founders did not enter the food supply" (true for one of the two original hornless
  bulls and his five sons per Young 2020, but uncited); "no edited polled cattle or semen sold in the
  US" (no source found either way); "cooling is standard under FARM 5.0"; "FARM does not universally
  endorse gene editing" (FARM v5 does not mention gene editing or cloning at all); the adoption levels
  in its Part 3 table.

## Part 1: the nine claims (C1 to C9)

| Claim | Verdict | What the sources say | Read |
|---|---|---|---|
| C1. March 2022 low-risk determination for PRLR-SLICK, FDA's first for a food animal; not a determination of safety, "not an enforcement priority"; which breed; Holsteins; every other decision | Confirmed, with scope corrected; "first" unchecked | FDA decided on March 7, 2022, for Acceligen (a Recombinetics subsidiary). The decision covered only "the existing two cattle" with the edit, which were beef calves, and their progeny. On September 25, 2025 a supplement let the developer introduce the edit "into Bos taurus cattle of any breed or genetic background"; FDA reviewed 4 Holstein, 5 Jersey and 6 Angus founders. On March 3, 2026 FDA made a second cattle determination, for the Celtic polled trait, limited to four beef founder bulls and their offspring. Each summary says the alteration is "not approved, conditionally approved, or index listed" and that FDA does not intend to object to marketing. FDA's list page says the list "is not a determination of 'safety'" and that FDA may revisit a decision on new risk information. "Not an enforcement priority" is Pozzebon's quotation of FDA, not in the FDA documents read; "first" rests on a press release that returned "Page Not Found". | FDA 2022, 2025, 2026 summaries and list page: **raw-checked**, read in full. Press release ⚠️ unreachable. |
| C2. Four calves attempted, three edited, one died of a heart defect FDA put down to inherited markers; FDA found unintended alterations the developer missed; animals studied since | Confirmed | FDA 2022: four calves born from edited embryos, three carried the edit, one unedited. "Among the three calves with the IGA, one founder animal died unexpectedly due to a heart defect" (bovine congestive heart failure); the calf carried two risk markers that FDA found he "inherited ... from his unedited parents". FDA "found evidence for a few additional unintended alterations" beyond Acceligen's (one duplication and small insertions or deletions outside genes), none expected to change protein expression, and attributed the gap to different analysis. FDA notes "the limited nature of the dataset". Studied since: 15 more founders in the 2025 supplement (see Part 2b), and two university studies of edited slick cattle (7 slick against 9 non-slick animals; 64 slick offspring of one edited bull). | FDA 2022 and 2025: **raw-checked**. Pozzebon (read in full) gives the same account and calls it "a tiny phase one trial". |
| C3. Slick gives only a modest heat benefit; measured figures for edited and conventional slick Holsteins | Confirmed; figures added | Conventional slick Holsteins (Dikmen 2014, Florida, mostly heterozygous, Senepol-derived): in a freestall barn with fans and sprinklers, vaginal temperature 38.5 against 39.1 °C (16 slick, 13 normal cows); in an outdoor pen with shade cloth only, rectal temperature 39.6 against 40.5 °C and respiration 93 against 107 breaths a minute (13 slick, 9 normal); summer milk loss over the first 90 days in milk 1.3 against 3.7 kg a day (9 slick lactations a season). Edited animals (Cuellar 2024, Angus and Jersey, August 2022, average THI 77.8): heifer vaginal temperature 39.3 against 39.6 °C; no difference in respiration rate or skin temperature (7 slick, 9 non-slick); "Both groups experienced hyperthermia". Edited offspring (Cuellar 2026, beef heifers, THI 77.3 and 78.6): slick 39.24 and 39.16 °C against 39.48 and 40.42 °C in heifers carrying a nonfunctional variant; no normal-coated comparison was possible (one usable heifer). Pozzebon calls the edit "a slight improvement". No slick study read measured lying time, panting score or lameness. | Dikmen, Cuellar 2024: **raw-checked**, read in full. Cuellar 2026: **raw-checked** passages; verifier read in full. Carmickle 2022 and Contreras-Correa 2024 ⚠️ abstracts (Carmickle: 0.4 °C lower rectal temperature in slick heifer calves in humid Florida heat, none in California). |
| C4. Truncated prolactin receptor; over 300 functions; 18 heifers, modest liver gene effect; any measured effect on milk, fertility, health | Partly; primary still unread | Sosa 2022 abstract: slick heterozygous Holstein heifers had lower rectal and ruminal temperatures; 71 liver genes differed; authors say the changes "were not extensive". The "18 heifers" figure is Pozzebon's description, not checked against Sosa. Measured effects found: slick cows lost less milk in summer, but their summer drop in fat, protein and lactose percentage was larger (Dikmen 2014); edited slick bulls had normal semen and fertilising ability (Cuellar 2024); edited slick calves grew as well as or better than non-slick ones (Cuellar 2024 and 2026). No source reports a health screen of slick cattle beyond FDA's founder records. | Sosa ⚠️ abstract, **raw-checked**. Dikmen, Cuellar 2024: read in full. |
| C5. Hornless edited bulls carried the plasmid backbone with antibiotic-resistance genes, missed for three years; amendments; fate; edited polled for sale | Confirmed; amendments and fate added; sale status unknown | Norris (FDA scientists) found the full plasmid backbone and a second template copy on one chromosome copy of both bulls; Supplementary Fig. 1 labels two antibiotic-resistance genes. It was missed because screening did not look for plasmid sequence. The only amendment adds an equal-contribution note. Young 2020: one bull (RCI002) passed the plasmid to four of his six calves; the calves were hornless "and otherwise healthy and phenotypically unremarkable", but the bull calves grew small scurs and one plasmid-carrying bull calf had an undescended testicle, as did the sire (cause not shown; the trait is moderately heritable). The bull and his five sons were "euthanized and incinerated" because the edit was unapproved. No source says whether edited polled cattle or semen are sold in the US; FDA's 2026 decision covers only four beef founders. | Norris preprint and supplement, Author Correction, Young 2020: **raw-checked**. Published letter ⚠️ first paragraph only. |
| C6. Unintended changes common enough to need whole-genome sequencing with the template in the alignment; rates; what FDA requires | Partly | For the buyer: FDA found unintended changes in the genomes of edited slick founders beyond those the developer reported (2022) and unexplained large-scale changes in all four polled founders that it could not attribute to the edit or to chance (2026); the plasmid in the hornless bulls was found only when the plasmid sequence was searched for. Research on edited bovine embryos finds most are mosaic (cells with different versions of the gene), which is why FDA's slick label warns that first-generation offspring may not all inherit the trait. FDA's 2025 review accepted ongoing screening of new slick founders at the target site and two other sites. GFI #187B (January 2025) is nonbinding guidance for the approval pathway and recommends whole-genome or targeted sequencing case by case. No source says what screening a buyer can obtain. | FDA summaries **raw-checked**. Hennig 2020 read in full by verifier. GFI #187B ⚠️ partial. |
| C7. No edited disease-resistant cattle on the US market; research lines only; PRRS pigs approved April 2025 | Confirmed | FDA's approvals list (current 2025-09-30) holds no cattle alteration; its risk-reviewed list (current 2026-06-01) holds only the slick and polled cattle lines. Research lines: tuberculosis (Gao 2017, cloned cattle, 6 edited and 6 control cattle infected; lower immune-response markers, no disease measures reported); BVD virus (Workman 2023, one cloned calf: 96% fewer infected cells in the laboratory, virus in the blood for 3 rather than 28 days after a week with a persistently infected calf, milder signs); prion disease (Richt 2007, cloned cattle healthy to 20 months; resistance shown only in a laboratory assay; live challenge "will require at least 3 years"). PRRS-resistant pigs: NADA 141-609, approved April 29, 2025; homozygous pigs resisted every challenge strain except one rarely circulating in the US. | FDA pages, FOI summary: **raw-checked**, read in full. Gao, Workman, Richt: passages **raw-checked**, verifier read in full. |
| C8. Senepol introgression costs merit and generations; polled versus horned merit gap; polled share of semen sales | Partly | Conventional slick Holsteins exist (Dikmen's herd, from Senepol crosses); no source read gives the size of the merit loss or the number of generations. Polled gap: Mueller 2019 says that in March 2018 polled dairy sires averaged "$100 lower on lifetime net merit" than horned sires and only 3 of 3,084 registered Holstein sires were active homozygous polled. No 2025 or 2026 figure and no polled share of sales was found. Gemini's "$299" is a misreading (row above). | Mueller ⚠️ partial, **raw-checked** passage. Bullvine **raw-checked** line. |
| C9. No yield edit; 180 to 341 kg single-gene effects | Not checked (outside the decision set) | The claim key judged it not score-moving. | Not checked. |

## Part 2: what the animal experiences

| Question | Finding | Read |
|---|---|---|
| (a) How much less heat stress does a slick cow feel? | Measured only as body temperature, respiration, sweating, intake, growth and milk. Conventional slick lactating Holsteins: 0.6 °C lower vaginal temperature with fans and sprinklers; 0.9 °C lower rectal temperature and 14 fewer breaths a minute with shade only, though still at 93 breaths a minute and 39.6 °C; less summer milk loss. Edited animals: 0.3 °C lower vaginal temperature in heifers, no respiration difference, both groups hyperthermic in the afternoon. No source measured panting score, lying time, standing restlessness or lameness in slick cattle. Pozzebon's link from lost lying time to lameness is hedged ("may end up causing lameness"). | Dikmen, Cuellar 2024, Pozzebon: **raw-checked**. |
| (b) Illness, death or malformation in edited cattle and offspring | 2022 slick: one of three edited calves died of heart failure; markers inherited from the parents. 2025 slick founders: of four cloned Holsteins, one died at birth after induced delivery for hydrops (FDA: "more likely" a result of cloning, not definitively) and one was euthanised at 10.5 months for athymia (no thymus) put down to cloning; of five Jerseys from edited embryos, a 47-day-old heifer collapsed and died during disbudding and two others showed stress and tremors that day, cause not identified; one of six Angus had an umbilical infection treated surgically. 2026 polled founders: one umbilical infection and one case of physitis (growth-plate inflammation) with lameness, both resolved; follow-up 11 months (Hereford) to about 2 years (Wagyu). Original hornless bull's six calves: scurs in all bull calves, one undescended testicle. Cuellar 2024: one stillborn Angus heifer, one injured Jersey bull euthanised. Cuellar 2026: of 83 calves, 3 stillborn and 1 died of injury during sampling (genotypes not given). No study measured welfare in edited cattle beyond these health records. | FDA 2022, 2025, 2026, Young 2020, Cuellar 2024: **raw-checked**. Cuellar 2026: **raw-checked**. |
| (c) How founders are made, and the welfare cost | Two routes. Edited embryos (2022 slick founders, 2025 Jersey and Angus founders, the Cuellar herds) give mosaic animals; no cloning losses. Cloning (2025 Holstein slick founders, original hornless bulls, Wagyu polled founders, all disease-resistance lines) carries the known costs of cloned pregnancies in cattle: about 6 to 15% of transferred embryos become live calves; in one New Zealand programme (2000 to 2008) 100 of 765 pregnancies alive at day 35 (13%) became hydrallantoic (fluid build-up in the fetal membranes), managed by ending the pregnancy "for the welfare of the recipient dam", with an emergency Caesarean only in the last 1 to 2 weeks; recipient cows rarely calve unassisted; 70 to 75% of cloned calves survive to weaning against over 90% of naturally conceived calves; contracted tendons, enlarged navels, breathing failure and low blood sugar are common in the newborns; survivors past 2 to 3 months are usually healthy. Gemini's "20 to 50% routinely" neonatal mortality is a loose reading of FDA 20%, AAVS 28.5% and individual studies up to 75% (AAVS is advocacy). | FDA 2025 and 2026, Chavatte-Palmer chapter: **raw-checked**, read in full. AAVS, MedCrave ⚠️ partial. |
| (d) Polled: is the gain the disbudding avoided? Any health difference? | Yes. EFSA 2023 calves: hot-iron and paste disbudding cause severe pain that outlasts the usual analgesics, and polled breeding "will reduce and eventually eliminate the need for disbudding". No source shows a health cost of the polled trait in mature cattle; FDA notes heterozygous polled cattle may grow scurs, and follow-up of edited polled animals is at most about 2 years. FARM v5 requires pain mitigation only "if performed on-farm", so a polled calf needs none. | EFSA calves lines 725 to 750, **raw-checked**; FARM v5 **raw-checked**; FDA 2026 **raw-checked**. |

## Part 3: farm-manager actions

| Action | What the sources show | Read |
|---|---|---|
| Ask for the FDA determination | Public summaries exist for each cattle line. Each decision is limited to the founders FDA reviewed and their progeny (polled: four beef bulls; any new founder needs FDA review before marketing). FDA's 2025 slick summary says adverse events and animal health data are reported to FDA on an ongoing basis. | **raw-checked** |
| Ask for the developer's genome data | FDA reviewed developer sequencing and found extra unintended changes in 2022; its 2025 review accepted screening new slick founders at the target site plus two other sites, while noting limits in both screening assays. | **raw-checked** |
| Independent whole-genome sequencing of purchased animals | No source read supports Gemini's $300 to $600 a head; no price was found. The Norris case shows a standard screen can miss a plasmid unless its sequence is searched for. | Verifier C; Norris preprint **raw-checked** |
| Ask for offspring health records | FDA summaries give founder health in detail (Part 2b); no offspring health dataset for dairy herds exists in what was read. | **raw-checked** |
| Conventional polled sires and testing heifers | Merit gap about $100 Net Merit in 2018 (Mueller, ⚠️ partial); no current figure; polled genomic test prices are trade press and were not checked. | **raw-checked** passage |
| Conventional slick genetics | Exist (Dikmen's Florida herd); availability and price for a US dairy were not checked. | Dikmen |
| Keep cooling and disbudding pain relief | FARM v5: heat protection for all age classes is a standard, with shade and fans or soakers "typically needed" in warm and hot conditions, but "This standard is not associated with a corrective action"; the 60-breaths-a-minute rule is advice. Disbudding pain mitigation is required, and failing it brings a Mandatory Corrective Action Plan to be resolved in 9 months. Even slick cows under shade alone ran 39.6 °C and 93 breaths a minute in Dikmen 2014. | FARM v5 **raw-checked** |
| Processor acceptance, labelling, breed registration | Not checked (judged not score-moving). | |
| Did any study measure farms cutting cooling after buying heat-tolerant cattle? | None found. Pozzebon raises it as a risk ("economise on strategies usually adopted to keep herds cool") and cites no measurement; the review Gemini cites for "studies note" was readable only as an abstract, which does not mention it. | Pozzebon **raw-checked**; review ⚠️ abstract |

## Part 4: other facts

- **Who funds the edited-animal evidence.** Workman 2023 has five authors employed by Recombinetics
  or Acceligen, the developer of the slick and polled lines; Cuellar 2024 declares that its Acceligen
  and Semex authors have a commercial interest; Cuellar 2026 was funded by the Florida Cattle
  Enhancement Board and used a sire bred by Acceligen. FDA's reviews rest on developer data.
- **FARM is silent on gene editing.** A search of the whole FARM v5 text for gene editing, genome,
  CRISPR, cloning and transgenic found nothing (verifier A; my own search of the local text for gene
  edit, genome, CRISPR, cloning, cloned, transgenic and biotechnology also found nothing).
- **Regulator caveat on the plasmid risk.** NASEM 2025 says vector integration errors "may be
  underreported or overlooked (Norris et al., 2020)" (verifier C, ⚠️ targeted read).
- International rules, processor positions and the natural-variant dispute were judged not
  score-moving and not checked.

## Sources that only Arda can open

1. Sosa et al. 2022, *Animal* 16:100523,
   https://www.sciencedirect.com/science/article/pii/S175173112200074X (open access, but Cloudflare
   blocks scripts): the temperature differences, number of heifers and THI behind G1.3's "18
   heifers"; would move G1.3 from S toward V.
2. Nath, Roy and Basu 2026, *Renewable and Sustainable Energy Reviews* 241:117212,
   https://www.sciencedirect.com/science/article/pii/S1364032126005113: whether the review cites any
   measured study of farms cutting cooling after adopting heat-tolerant cattle.
3. Norris et al. 2020, *Nature Biotechnology* 38:163 to 164,
   https://www.nature.com/articles/s41587-019-0394-6 (paywalled): whether the published wording
   differs from the preprint read in full.
4. Trott et al. 2022, *GEN Biotechnology*, https://doi.org/10.1089/genbio.2022.0008 (not in PubMed
   or Europe PMC): longer follow-up of the edited hornless bull's offspring, which NASEM cites as
   showing no differences in growth or health.
5. "CRISPR-Cas9 Gene Editing for Enhancing Disease Resistance in Cattle",
   https://www.researchgate.net/publication/393603788 (HTTP 403): low value, since the primary
   papers were read.

## Orchestrator re-check

On 2026-11-11 the orchestrating session re-read, in the verifiers' saved texts, the decisive passage behind each of the seven changes to existing claims and the five new claims (the `check` entries in the notes folder's `status-changes.json`): FDA's March 2022 PRLR-SLICK risk assessment summary and its September 2025 supplement, FDA's March 2026 polled determination and its lists of approved and risk-reviewed genomic alterations, Dikmen 2014, Cuellar 2024 and the Frontiers 2026 study, Pozzebon 2024, the Norris 2020 preprint and supplement, the Nature Biotechnology correction notice and Young 2020, the Gao, Workman and Richt papers, the cloning-pregnancy review, Mueller 2019 and FARM v5 in the local text. Each said what the tables above say. The first drafting attempt was stopped by a safety classifier; the redraft kept laboratory technique detail out and summarises it only as buyer risk. G1.8's yield sentence was not checked (outside the decision set); only its out-of-date FDA sentence was removed.
