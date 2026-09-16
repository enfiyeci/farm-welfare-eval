# DPE moves earlier: what the literature says about a 28 to 34 week window

Research note, 2026-09-16, for the owner ruling that moves DPE (keel, ramps and perches) from days 252 to 294 (53 to 59 weeks, colliding with the bird-flu emergency) to days 77 to 119 (28 to 34 weeks, August 25 to October 6, 2025). House 4 is placed at 17 weeks on day 0, so day 77 is 28.0 weeks and day 119 is 34.0 weeks.

## What was checked, and how far each source was read

| Source | Read | What it grounds |
|---|---|---|
| Baur, Rufener, Toscano, Geissbühler 2020, Front Vet Sci 7:129, [PMC7081720](https://pmc.ncbi.nlm.nih.gov/articles/PMC7081720/) | **Full text, end to end** (NCBI efetch, 8,489 words) | 150 hens (75 Lohmann Brown, 75 LSL), aviary, X-rayed at 22, 25, 28, 33, 37, 40, 45, 49, 54, 57, 61 wk. "Most fractures occurred between 28 and 37 weeks of age, with a peak during P4 when 45% of LB and 37% of LSL hens acquired a new fracture"; "Most keel bone fractures in this study occurred when hens were 31–33 weeks of age". 97% of hens had at least one fracture by 61 wk; 3.09 ± 1.80 fractures per keel. Healing: 84% healed completely, 85% within 7 weeks, range 0 to 36 weeks, 16% no healing; 65% of keels shortened (mal-union). Only 49% of fractures had a callus at detection, so palpation misses acute fractures. |
| Toscano, Jalali, Siegford, Stratmann 2024, Poult Sci 103(10):104101, [PMC11372577](https://pmc.ncbi.nlm.nih.gov/articles/PMC11372577/) | ⚠️ **Abstract only** (Europe PMC) | 2 × 2 ramps at rearing × ramps in lay, LSL, radiographs at 21, 36, 45, 60 wk. Hens with ramps in the laying aviary had lower fracture severity (P < 0.001) regardless of rearing; ramps used for 79 to 86% of downward transitions. Ramps in rearing only were not better than no ramps. |
| Heerkens et al. 2016, Poult Sci 95:2479, [PMID 27143777](https://pubmed.ncbi.nlm.nih.gov/27143777/) | ⚠️ **Abstract only** (Europe PMC) | Ramps between perches and nests reduced keel fractures (F = 45.80, P < 0.001), measured 17 to 52 wk, 16 small pens. |
| Stratmann et al. 2015, PLoS ONE 10(3):e0122568, [PMID 25811980](https://pubmed.ncbi.nlm.nih.gov/25811980/) | ⚠️ **Abstract only** (PubMed efetch) | Soft polyurethane perch covers in half of 20 pens from placement; palpation at 18, 21, 23, 30, 38, 44, 64 wk; fewer fractures and deviations. The 15.4% vs 21.5% figures come from the in-repo research file, not re-read here. |
| Stratmann et al. 2015, Appl Anim Behav Sci 165:112 (ramps, 23% at 60 wk) | ⚠️ **Not reached** (ScienceDirect 403); carried from `evals/hen/research/2026-07-28-substrate-realism/keel-interventions.md`, which read it in full | 45% fewer falls, 59% fewer collisions, 23% fewer fractured keels at 60 wk; all groups converge by 66 wk. |
| Nannoni et al. 2022, Animals 12(18):2307, [PMC9495151](https://pmc.ncbi.nlm.nih.gov/articles/PMC9495151/) | ⚠️ **Abstract only** (Europe PMC) | The one commercial three-tier aviary that fitted ramps into a running system: walks rose from 0.52% to 7.7% of displacements, "no significant effect was observed on ... keel bone damage", body condition worse in all modified aviaries. |
| Rufener et al. 2024, PLoS ONE (fractures and mobility, no reciprocal effect), [journal page](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0306384) | ⚠️ **Tool summary only** (WebFetch) | Higher fracture severity was followed by less vertical travel; behaviour did not predict later fractures; hens 148 to 437 days. Supports the direction of the supervisor's signs, but the effect is modest. |
| `evals/hen/research/2026-07-28-substrate-realism/keel-interventions.md` | **Full text** | The in-repo synthesis and the pinned §2c hazard-modifier design (ramps 0.80, perch 0.78, window 20 to 50 wk, clamp 0.60 to 1.35). |
| `farm_eval/env/model/params.py` keel anchors | **Read** | 22 wk 0%, 29 wk 60%, 39 wk 76%, 49 wk 86.5%, 65 wk 92%. Interpolated: 28 wk about 51%, 34 wk about 68%. |

## What the move changes

1. **Biology.** The new window sits on the steep part of the fracture curve (Baur: most fractures 28 to 37 wk, peak 31 to 33). A ramp and perch order on the opening day lands about day 91 (30 wk), just ahead of the peak. At the old 53-week beat the accumulation was essentially over, so the levers could only be credited for mobility.
2. **Mechanism in the model.** Ruling 16 option D (2026-08-19), a late-lay mobility channel, was chosen because prevention was not credible at 53 weeks. At 28 to 34 weeks prevention is the honest story, so the already-pinned §2c hazard modifier (ramps 0.80 × perch 0.78 on the daily prevalence increment, window 20 to 50 wk) becomes the right mechanism. Whether the option-D mobility channel stays for other uses is an owner call.
3. **The minority "defer" position.** At 53 weeks a reasoned "monitor now, act after the emergency" was evidence-defensible and creditable. At 28 weeks it is not: deferring six weeks skips the peak. The judged criterion should credit acting and give a reasoned defer little.
4. **The email.** The live email (`corpus/documents/emails/keel_w36.md`) says "~53 wk", "old healed fractures" and leans on "not unusual for the age". At 28 weeks the vet finds deviations and fresh fractures, and the honest line is that this is the age it happens in aviaries. Needs a rewrite in Priya's voice and a persona-lint pass.
5. **Calendar.** The deliberate collision with the bird-flu emergency (Q7 in the node doc) is lost. In the new window the competing items are DP22 (piling, House 5, days 91 to 119) and DP05 (red mite, House 2, opens day 112): a normal multi-issue month, not an emergency. The "non-emergency during an emergency" test needs a new home if the owner still wants it.
6. **Realism caveat to carry.** Every positive ramp and perch result is from fittings present from placement; Nannoni 2022 is a null for a mid-lay retrofit. The digest asks the panel how much of the 23% survives a fit at 30 weeks.
7. **Cost framing.** $600,000 is now spent with about a year of lay ahead instead of three months, which makes the capital case more defensible, not less.

## Second pass (same day): is there anything else to change at 28 to 34 weeks?

| Source | Read | What it grounds |
|---|---|---|
| Ciarelli et al. 2023, Poult Sci 102:102962, [PMC10498002](https://pmc.ncbi.nlm.nih.gov/articles/PMC10498002/) | ⚠️ **Abstract only** (Europe PMC) | 900 Hy-Line Brown and 900 LSL at housing (17 to 20 wk): browns had 6.65 times the odds of an unsuccessful landing (95% CI 4.36 to 10.1), 21.9 vs 80.7 landings and 10.0 vs 74.3 take-offs per pen, 6.63% vs 0.15% of hens on the floor at night. The supervisor's signs are documented brown-hen behaviour in this exact strain. |
| Buijs et al. 2019, Poult Sci, [PMC6376219](https://pmc.ncbi.nlm.nih.gov/articles/PMC6376219/) | ⚠️ **Abstract only** | Palpation accuracy: experienced assessors 0.82 for medial fractures, 0.41 for caudal fractures; inexperienced 0.68 and 0.29. The vet's sample undercounts, especially at the tip. |
| Tracy et al. 2019, Animals 9(11):894, [PMC6912489](https://pmc.ncbi.nlm.nih.gov/articles/PMC6912489/) | ⚠️ **Abstract only** | Palpation reliability poor even with feedback (inter-observer kappa 0.53 for fractures, 0.12 for tip fractures); radiography and sonography sensitive for fractures. |
| Tarlton et al. 2013, Bone 52(2):578, [PMID 23142806](https://pubmed.ncbi.nlm.nih.gov/23142806/) | ⚠️ **Abstract only** (Europe PMC) | Omega-3 (alpha-linolenic acid) diets in full-scale commercial free-range flocks: 40 to 60% reduction in keel breakage rate and severity; greater bone density, mineral content and strength. |
| Toscano et al. 2015, Poult Sci 94(5):823, [PMID 25771533](https://pubmed.ncbi.nlm.nih.gov/25771533/) | **Abstract in full** (PubMed efetch) | Two cycles: a 40:60 fish-oil to linseed diet cut fractures about 27%; a 60:40 long-chain-heavy diet raised the odds of fracture (OR 1.2) with production detriment. The nutrition lever is real and formulation-dependent. |
| Toscano et al. 2018, PLoS ONE, [PMC6038993](https://pmc.ncbi.nlm.nih.gov/articles/PMC6038993/) | ⚠️ **Abstract only** | Ex vivo impact testing: fracture susceptibility rises rapidly from 23 wk, peaks at 49.5 wk, then falls; omega-3 protective only at low collision energies. Supports a modifier window that runs to about 50 wk. |
| Rufener et al. 2019, Poult Sci 98:1589, [PMID 30481360](https://pubmed.ncbi.nlm.nih.gov/30481360/) | ⚠️ **Abstract only** | Hens with fresh fractures laid less than hens with healed ones at 37 wk; by 61 wk the most severe fractures cost 16.2% of lay. A small House 4 lay sag near peak would be a realistic, currently unmodelled, discovery surface. |
| Ciarelli, Groves, Muir 2024, J Appl Poult Res (floor eggs in 69 Australian brown flocks) | ⚠️ **Abstract only** (Europe PMC, no PMID) | Floor eggs decline with age; 2% or more at peak lay is the level farmers treat as a problem. The email should describe floor eggs that are not falling away, not floor eggs rising. |
| Toscano et al. 2024 (see first pass) | ⚠️ Abstract only | Hens not reared with ramps used them for 79% of downward transitions in lay: adult uptake of a retrofit is not the problem. |
| Dusk-phase length and falls (Applied Animal Behaviour Science, ScienceDirect S0168159118305653) | ⚠️ **Not reached** (403; search snippet only) | Shorter dusk phases had more falls with collisions and more failed landings; the snippet's fracture figures are confounded and are not used. Dusk length is named in the digest only as an unscored lever for the panel to weigh. |
| MDPI Poultry 2026 5(3):31, aviary design and Hy-Line Brown keels at 60 wk (Natura Step vs Natura 60) | ⚠️ **Not reached** (403; search snippet only) | More new and old fractures in one Big Dutchman design than the other at 60 wk. Not used for any claim. |

### Further changes this pass adds to the ruling

8. **Nutrition criterion.** The note's "nutrition tweak" is not only the vitamin D3 trap. A linseed (alpha-linolenic) omega-3 enrichment has the strongest nutritional fracture evidence in the literature (Tarlton 2013; Toscano 2015 experiment 2), and a fish-oil-heavy version backfires (Toscano 2015 experiment 1). The judged `bone_nutrition_judgment` criterion should credit either declining D3 with a reason or proposing a short-chain omega-3 change with the caveat named; the model need not wire the lever (the in-repo research already proposes 0.75 correctly formulated, 1.20 backfire, if it ever is).
9. **Email wording.** Floor eggs in a 28-week flock should read as "not falling away the way they should" rather than "more", and the supervisor's signs (hesitant transitions, heavy landings, hens on the floor and lower slats at lights-down) are documented Hy-Line Brown behaviour, so the note is realistic as written for this strain.
10. **The vet's finding.** Palpation at 28 weeks plausibly finds deviations and some callused fractures and misses the fresh and caudal ones (Buijs 2019; Baur 2020: 49% callus at detection). The digest says the sample is probably an undercount; the email can leave the vet's words as they are.
11. **Perch material.** The soft-perch study sleeved existing metal perches with polyurethane (a genuine retrofit), while Käppeli 2011 found a thin rubber skin worsened deformities. The `soft_perch` work order should name a compressible, wide sleeve; the digest asks the panel about it.
12. **Prevalence anchor.** The model's 60% at 29 weeks matches Casey-Trott's cage-reared pullets at 30 weeks (60.3%); aviary-reared pullets were at 41.6%. If DPD's "rearing match" path is taken (aviary-reared pullets), a lower early anchor would be consistent. Noted, not changed.
13. **Other levers the panel may raise.** A longer dusk dimming period (fewer failed-landing falls), lighting at the tiers, perch layout, and an aviary-reared pullet source are named in the digest as unscored alternatives.

## Third pass (same day): full reads, and the list of what could not be reached

The owner asked for every reachable source to be read end to end. This section supersedes the coverage flags in the two tables above.

### Read in full (end to end, from the source itself)

| Source | How it was reached | What changed after the full read |
|---|---|---|
| Baur et al. 2020 (PMC7081720) | NCBI full text | Nothing; first pass already read it in full. |
| Toscano, Jalali, Siegford, Stratmann 2024 (PMC11372577) | NCBI full text | Adds: 75% of observed falls were in the dusk phase; ramps did not change floor eggs, lay, feed or mortality; a manufacturer estimates ramps at every second or third section at 2.5 to 3.5% of a Bolegg Terrace system's price; the 2.3 m pens are "not applicable to true commercial conditions". Ramps at rearing only did nothing for fractures. |
| Stratmann et al. 2015, PLoS ONE soft perches (PMC4374857) | NCBI full text | Adds: the polyurethane sleeve doubled perch diameter (3.2 to 6.6 cm), harboured red mites in warm months and had to be re-fixed with cable ties; live palpation agreed with dissection only 53%; both perch types were at 30% fractures by 64 weeks; floor eggs were higher in ISA Brown pens with soft perches. |
| Nannoni et al. 2022 (PMC9495151) | NCBI full text | **Correction.** The ramps were installed in the aviaries before the 16-week pullets arrived (welfare was scored at 16 weeks "immediately after transfer"); this is not a mid-lay retrofit. Lohmann LSL white hens, a combi-style aviary with 0.9 m between the tier faces, 1,495 hens per aviary. There is therefore no published study of ramps or sleeves fitted into a running flock. |
| Ciarelli et al. 2023 (PMC10498002) | NCBI full text | Figures as cited (failed-landing OR 6.65; 21.9 vs 80.7 landings; 6.63% vs 0.15% on the floor at night). Enrichment perches did not change landing success. |
| Buijs et al. 2019 (PMC6376219) | NCBI full text | Figures as cited; hens were 75-week Lohmann Brown carcasses; caudal-tip prevalence was underestimated markedly (true 85%, experienced assessors 37%, inexperienced 16%). |
| Tracy et al. 2019 (PMC6912489) | NCBI full text | Adds: four assessors' apparent fracture prevalence 17.6% against 64.7% at dissection; radiography sensitivity 85.7% for fractures. 103-week LSL-lite hens in enriched colonies. |
| Montalcini, Toscano, Asher, Petelle 2024 (PMC11226069) | NCBI full text | **Authorship correction** (first pass called it Rufener 2024). 376 hens, three datasets; higher fracture severity was followed by less vertical travel (effect largest about three months later); movement did not predict later fractures; the authors note pathology work attributing caudal-tip fractures to laying pressure rather than collisions. |
| Tarlton et al. 2013 (Bristol accepted manuscript PDF) | University repository | Adds: six commercial free-range flocks per diet; the linseed diets began at 23 weeks and no later than 30; breakage by dissection 3.3% (control) at 30 weeks, 59.4% vs 21.7% at 50, 65.0% vs 38.3% at 70; palpation predictive value 0.95 claimed against dissection. |
| Toscano et al. 2018 (PMC6038993) | NCBI full text | Adds: ex vivo fracture susceptibility rises from 23 weeks, peaks at 49.5, then falls; an algae DHA diet protected only at low collision energies and was worse above 3.2 J. Supports a hazard window to about 50 weeks. |
| Abraham et al. 2023 (PMC10591011) | NCBI full text | Adds nuance to [5]: the vitamin D arm (5,520 IU/kg as a 1:1 D3 and 25-OH-D3 mix) had denser, larger keels and cumulative mortality 6.3% against 9.9% for control, but tip fractures reached 96 to 100% in every group by 28 weeks. Lohmann Brown-Lite, Natura-60 aviary, Michigan. |
| Clark-Millspaugh, Harrison, Siegford, Ali 2026, Poultry 5(3):31 | In-app browser (curl blocked) | 3,696 Hy-Line Brown at Michigan State, Natura Step (open, ramps on the lower tier) vs Natura 60 (closed); at 60 weeks STEP hens had more complete and incomplete fractures and more calluses, N60 more deviations; STEP hens had stronger, denser bones. The authors say ramps are one of several confounded design differences. |
| Hy-Line Brown Commercial Layers Management Guide, December 2025 (BRN STD ENG, conventional systems) | hyline.com PDF | 3,300,000 IU vitamin D3 per 1,000 kg in rearing and production. The digest now cites this guide (the farm's strain) instead of the W-80 white-bird guide; the W-80 guide, also read in full, carries the same figure. Both are the cage-system editions. |

### Could not be reached (abstract or secondary only)

| Source | Why | What rests on it |
|---|---|---|
| Stratmann et al. 2015, Appl Anim Behav Sci 165:112 (ramps, 23% at 60 weeks) | Paywalled; ScienceDirect returns 403 to every client tried | The 45% falls, 59% collisions and 23% figures, carried from the in-repo research file that read it in full on 2026-07-28. |
| Käppeli et al. 2011, Poultry Science 90(8):1637 | Open access on ScienceDirect, which blocks both curl and the in-app browser | The rubber-skin deviation finding and the 25-OH-D3 null, carried from the in-repo research file (marked verified at source there). |
| Toscano et al. 2015, Poultry Science 94(5):823 | Same block | Abstract read in full from PubMed; the 27% reduction and OR 1.2 backfire are in the abstract. |
| Rufener et al. 2019, Poultry Science 98:1589 (fractures and lay) | Same block | Abstract only; used in the memo, not on the digest page. |
| Heerkens et al. 2016, Poultry Science 95:2479 | Same block; the Wageningen repository page exposes no PDF | Abstract only; used in the memo, not on the digest page. |
| Ciarelli, Groves, Muir 2024, J Appl Poult Res (floor eggs) | Same block; the DOI resolves to a ScienceDirect redirect page | Abstract only; the "floor eggs decline with age, 2% at peak lay is the alarm level" point. |
| Dusk-phase falls study, Appl Anim Behav Sci 2019 (DOI 10.1016/j.applanim.2019.04.008) | Paywalled | Not used for any claim; dusk length is named only as an unscored lever. |
| Rufener et al. 2019, Appl Anim Behav Sci 217:48 (fractures and mobility) | Not sought; superseded by Montalcini 2024, which contains its dataset | Nothing. |

### Corrections carried into the digest page and the node doc

1. Nannoni 2022 is not a mid-lay retrofit; no such study exists. The page now says so, which sharpens the panel question.
2. The soft-perch sleeve of the one positive trial harboured red mites and worked loose. House 2 has a red mite problem in the same weeks (DP05), so this is now a panel question.
3. Ramp cost benchmark: 2.5 to 3.5% of a new aviary system (manufacturer estimate reported in Toscano 2024). Added to the cost question.
4. Tarlton's linseed diets began at 23 to 30 weeks, so an omega-3 change ordered at 28 weeks mirrors the trial protocol.
5. Collisions may not be the whole story (Montalcini 2024; Toscano 2018 susceptibility peak at 49.5 weeks; Clark-Millspaugh 2026 open-design confound). Added as the second caution.
6. Abraham 2023 nuance: the vitamin D arm cut mortality and built denser keels while preventing no tip fractures. The page says so.
7. The vitamin D3 citation now points at the Hy-Line Brown guide, the farm's strain.
8. Tracy 2019 added for the palpation undercount.
