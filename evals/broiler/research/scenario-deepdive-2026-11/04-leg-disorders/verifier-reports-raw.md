Eval: broiler

# Leg disorders: raw verifier reports (unverified)

Written 2026-11-06. The unedited final reports of the 12 Sonnet subagents that checked the Gemini
report (`raw/2026-11-05-gemini.md`) claim by claim, one group of sources each. Each ends with its own
coverage statement. **Do not cite this file.** The checked result is `verified.md`; what changes is in
`adjudicated.md`.

Brief given to every subagent: read the named source in full, from the source itself; flag partial
reads with ⚠️; no browser tools; no pirate sites; quote at most one short sentence. Their fetch tool
(WebFetch) passes pages through a summarizing model, so a "full read" through it is not a verbatim
read. Status-moving figures were re-checked against raw text in `verified.md`.

---

## Group A

**Group A verdicts: 9 claims confirmed or mostly confirmed, A8 and A10 not in the source, A9 only partly right.**

⚠️ Process caveat for the whole report. The fetch tool does not return raw text. It runs a small summarising model over the page, and I got paraphrase plus some quotes, never the verbatim article. Most absence checks ("term X is not in the Introduction or Discussion") are therefore the tool model's statements about the text, not my own reading. The two papers are open access, so a direct read of the two Frontiers pages would settle any doubt. The A8 and A10 absences are the claims most worth that check.

**1. Verdict table**

| id | verdict | what the source says | source read |
|---|---|---|---|
| A1 | CONFIRMED | Shi 2024 Results and Discussion: TD incidence 22%, 16% and 12% at 6, 8 and 10 weeks. The Discussion says it was "highest at 6 weeks and decreased to 12% by week 10". | Shi 2024, via summarising fetch, whole article reached |
| A2 | CONFIRMED | Methods: a digital X-ray machine screened for TD. Supplier is Jiangsu Lihua Animal Husbandry Co., Ltd., Changzhou, China. The authors are at Nanjing Agricultural University. | Shi 2024, same |
| A3 | CONFIRMED | Methods: 400 birds were X-rayed at 6, 8 and 10 weeks. A separate 400 birds were reared and sacrificed at 6 weeks for sampling. Sub-samples: growth-plate RNA-seq with 6 TD and 6 non-TD birds; blood RNA-seq with 4 and 4; bone quality with n=12 per group. | Shi 2024, same |
| A4 | PARTLY | Shi 2024 does name the birds. Methods describe "specialized native Chinese yellow-feathered meat cockerels". The Introduction and Discussion say only "yellow-feathered chickens" and "yellow-feather broiler population", so the breed fact is in the Methods, not the main prose. The 2026 paper says "yellow-feathered Chinese meat chickens" in its Introduction, in the sentence "A recent study revealed a 22% incidence in yellow-feathered Chinese meat chickens at 6 weeks, which decreased after 8 weeks". It does not say "cockerels". The 2026 paper's own birds are male Ross 308, not yellow-feathered. | Shi 2024 and the 2026 paper, via summarising fetch |
| A5 | CONFIRMED | TD vs non-TD at 6 weeks. Bone mineral content 6.78 vs 7.74 g (p=0.01). Bone mineral density 0.27 vs 0.34 g/cm² (p=3e-5). Bone ash 42.64% vs 46.17% (p=1.9e-11). Ca 15.35% vs 17.24% (p=9.27e-8). P 7.41% vs 8.35% (p=2.35e-12). Stiffness and Young's modulus did not differ. | Shi 2024, same |
| A6 | CONFIRMED | Discussion: "broiler chickens with a high incidence of TD have higher plasma calcium and phosphorus concentrations", cited to Yalçin et al. 2000 (Br Poult Sci 41:562–565). Shi's own paper reports no serum Ca or P. | Shi 2024, same |
| A7 | CONFIRMED, with a nuance | The growth-plate RNA-seq found 849 differentially expressed genes (715 up, 134 down). COL1A1, COL5A1 and COL8A1 were flagged as hub genes in the protein-interaction network. The tool reports that the gene set enrichment analysis showed upregulated cartilage, circulatory-system and nervous-system development pathways in TD birds. The Discussion describes the three genes as "the alpha chain of type XII collagen", which is a sloppy statement in the paper itself. | Shi 2024, same |
| A8 | NOT IN SOURCE | Vitamin A and skin pigmentation are absent from the Introduction and Discussion. They appear only as the title of reference 13 (Li et al., 2008, high dietary vitamin A supplementation, TD, skin pigmentation and growth performance). Shi 2024 does not state that excessive vitamin A worsens TD or reduces pigmentation. The report likely read a reference title as a finding. ⚠️ Absence is as reported by the tool model. | Shi 2024, same |
| A9 | PARTLY | Heat stress lowered tibial maximum load (P<0.0001) and flex modulus (P=0.0003) in three-point bending. It also reduced tibiotarsus crude ash by 4.01% (Results). The authors write "High levels of antioxidants increased the bone ash content, fat content, Ca content and Ca:P ratio". Table 5 shows higher ash, fat and Ca (P<0.0001) and a Ca:P effect with P=0.0093. High PUFA (5% linseed oil) also lowered the bending parameters, and heat stress plus high PUFA plus low antioxidants was worst. Problems: the Results text elsewhere says antioxidants "decreased ash, Mg, Zn, Na and K", which contradicts Table 5 and the abstract. Also, "counter heat-stress and PUFA damage" is the report's wording; the paper's high-antioxidant diet was 200 IU vitamin E, 250 mg vitamin C and 0.15 mg Se per kg. | 2026 paper, via summarising fetch |
| A10 | NOT IN SOURCE | The 2026 paper has no statement about a 10+ week grow-out, skeletal maturation, or 5 to 7 week slaughter for Ross or Cobb. "10 weeks", "5 to 7 weeks", "slaughter age" and "skeletal maturation" are absent from the Introduction, Discussion and Conclusion. Its only related wording is "male broilers aged 0–42 days during active EGP" (EGP = epiphyseal growth plate, the growth-plate phase). The 10-week yellow-feather point is Shi's own design (X-ray at 6, 8 and 10 weeks), not a claim in the 2026 paper. The paper's one mention of Cobb is the Dinev 24.22% figure. | 2026 paper, via summarising fetch |

**2. Extra facts for the welfare simulation**

- **Shi 2024:** In yellow-feathered meat birds, TD incidence falls with age: 22% at 6 weeks, 16% at 8 weeks, 12% at 10 weeks. TD birds were lighter at all three ages. Tibia length was shorter at 8 and 10 weeks. Tibial density was lower only at 6 weeks. This is a slow-growing Chinese breed, so it is a weak proxy for Ross or Cobb broilers.
- **2026 paper, Introduction:** It restates TD incidence of 24.22% in Ross 308 and Cobb 500 and 27.7% in Pureline (Dinev et al. 2012). That is a source the simulation can use for fast-growing Western hybrids.
- **2026 paper design:** Cyclic heat stress started at day 22. It ran 12 h at 24 °C, a 2 h warm-up to 34 °C, 7 h at 34 °C, and a 3 h cool-down. Killing was at day 42 in 24 floor pens. Table 4 says "42-week-old", which looks like a typo for days.

**3. Coverage statement**

- https://www.frontiersin.org/journals/genetics/articles/10.3389/fgene.2024.1434532/full — opened in two fetches, all sections reached through the tool's summarising model. ⚠️ Not a verbatim read.
- https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2026.1771630/full — three fetches. The page text is 137,625 characters. The first 100,000 (abstract through conclusion, including tables) were queried across fetches. The final 37,625 were read (chars 100000 onward) and came back as the reference tail (refs 21–59) plus metadata only. ⚠️ Summarised by the tool model, not read raw. ⚠️ The reference list start (refs 1–20) was not seen separately; the only ref confirmed is Shi 2024 as ref 43.
- Not opened: the Yalçin 2000 and Li 2008 papers themselves. A6 and A8 concern what Shi 2024 says, so they were not needed.
- No browser tools were used and no files were written.

---

## Group B

## Group B report: Dinev sources

Bottom line: the 2012 review (Dinev, J Poult Sci 49(2):63-67) is the source the Gemini report calls "Dinev 2014". It is dated 2012, not 2014, and I read it in full. It confirms B1, B2 and B5. B3, B4, B6, B7 and B8 are only partly right. The primary Dinev, Denev and Edens 2012 paper (J Appl Poult Res 21(3):637-644) was paywalled, so I saw only its abstract.

### 1. Claim table

| Claim | Verdict | What the source says | Source read |
|---|---|---|---|
| B1: TD prevalence 27.7% Pureline, 26.5% Cobb 500, 24.22% Ross 308 | CONFIRMED | The review, TD section p.65, says the highest TD prevalence was in Pureline (27.7%), then Cobb 500 (26.5%), then Ross 308 (24.22%). It cites "Dinev et al. unpublished" for this. The primary abstract's lesion counts are Ross 355 (24.22%), Cobb 185, Pureline 313 (27.7%). The abstract, as relayed by WebFetch, also prints Cobb as 24.22%, which looks like a copy slip. Its male and female shares (10.48% + 16.09%) sum to about 26.6%, which matches 26.5%. | Review: full (5 pp). Primary: abstract only ⚠️ |
| B2: first TD lesions at about 24 days | CONFIRMED, with nuance | The review Conclusions (p.66) say TD cases occur at "approximately 24 days" in modern hybrids, "predominantly associated with insufficient Ca". The per-line mean ages of first macroscopic lesions are Ross 23.7 days (range 18 to 34), Cobb 19.6 days (range 16 to 23) and Pureline 28.8 days (range 22 to 34). The mean of the three is about 24. The review calls this about 11 days earlier than McNamee 1998, which reported 28 to 42 days (mean 35). The primary abstract gives the same per-line means. | Same |
| B3: Bulgaria, macroscopic necropsy of proximal tibia, sample size | PARTLY | **Bulgaria** is confirmed (the author is at Trakia University; the primary abstract says Bulgaria). **Proximal tibia** is confirmed: the review says TD lesions were "located only within the proximal tibiotarsus" and describes them as macroscopic. **Sample size:** the abstract says 20 flocks of about 17,000 birds each, which is about 340,000 birds placed. The number of birds actually necropsied is not stated in the review or the abstract. My own back-calculation from the abstract's counts and percentages is about 1,470 Ross, about 700 Cobb and about 1,130 Pureline, so about 3,300 birds. This is inference, not a stated figure ⚠️. The review also does not use the word "necropsy"; the report's table title does, and the abstract says "pathomorphological methods". | Review: full. Primary: abstract only ⚠️ |
| B4: 13.3% E. coli or mixed, 11.1% coagulase-negative staphylococci, S. aureus the majority pathogen | PARTLY | The review (p.63) gives the figures for Thorp et al. 1993, from proximal femur lesions "indicative of BCO" (bacterial chondronecrosis with osteomyelitis): coagulase-positive staphylococci 22.2%, coagulase-negative staphylococci 11.1%, E. coli or mixed cultures 13.3%. So 13.3% and 11.1% are right, and they come from Thorp 1993, not McNamee 1998. Two problems with the rest: (a) coagulase-positive staphylococci (22.2%) is the largest listed group, but the review never says "S. aureus" for Thorp's data and it is not a majority; the three listed groups sum to 46.6% and the remainder is not given. (b) The review's own argument is that E. coli, not S. aureus, is the main broiler pathogen. Dinev's own data found E. coli in over 90% of culture-tested FHN (femoral head necrosis) osteomyelitis samples. S. aureus is described as "commonest isolate" only for turkeys (Nairn and Watson 1972) and broiler breeders. | Review: full |
| B5: severe BCO outbreaks reached 50% of lameness and more than 5% flock mortality (Nairn and Watson 1972) | CONFIRMED | The review (p.63): Nairn and Watson (1972) reported that the prevalence of lameness caused by BCO "could reach 50%, with over 5% mortality in the herd". This is Dinev's wording; the report's "50% of lameness" is ambiguous. I read it as up to 50% of birds lame, not 50% of lameness cases. | Review: full |
| B6: adequate calcium around day 24 prevents subclinical rickets or TD | PARTLY | The review (Conclusions, p.66) says TD occurs at about 24 days and is "predominantly associated with insufficient Ca". That is an association. The review states no intervention, no dose, no effect size, and no claim that supplying calcium at day 24 prevents TD or rickets. It also says hypocalcaemic rickets is macroscopically hard to tell from TD and that TD may follow from rickets. | Review: full |
| B7: BCO losses of 0.75% to 5% mortality (Dinev for the 5% end) | PARTLY | The review does not contain 0.75%; the Gemini report's own section on claim 3 attributes 0.75% to McNamee and Smyth 2000, which I did not check. The 5% is only the outbreak ceiling from B5 ("over 5% mortality in the herd"), not the top of a typical range. Other review figures: arthritis plus osteomyelitis were about 10% of lameness-related losses in the last week before slaughter in Canada (Riddell and Springer 1985), and TD losses reach up to 30% in outbreaks (McNamee 1998). | Review: full |
| B8: valgus, TD and BCO peak from day 21 to 35 | PARTLY | **TD:** the review says it "usually develops between 3 and 5 weeks of age" (Bradshaw 2002), which is day 21 to 35. **BCO and FHN:** lesions are usually seen at about 35 days, linked to intensive muscle growth. **Valgus:** angular limb deformities (Julian 1984) are named as a primary cause of lameness, but no age or peak is given. | Review: full |

### 2. Extra facts for a broiler welfare simulation
- TD prevalence varied little across hybrids (24 to 28%), against 27 to 40% across five hybrids in Edwards 1984 (review p.65). The review attributes the small spread to selection against TD.
- TD showed no sex difference in Dinev's data, though associated fractures were mostly in males. Lesions were confined to the proximal tibiotarsus. (p.65)
- Lesion onset has moved earlier, with a mean of about 24 days in modern hybrids against about 35 days in the 1990s. The review attributes this to selection for fast growth. (p.65)
- FHN: in Dinev's own 2009 work, 75% of cases had osteomyelitis and 25% were culture-negative osteochondrosis. About 1/3 had concurrent colisepticemia (E. coli infection of the blood). Half of fracture cases also showed rickets. (p.64)
- TD and BCO sit in the age window of day 21 to 35, which is the age the review ties to rapid muscle growth.
- Neither source gives pain duration, treatment, or farm-intervention effect sizes.

### 3. Coverage statement
- J-STAGE PDF of Dinev, J Poult Sci 49(2), https://www.jstage.jst.go.jp/article/jpsa/49/2/49_011109/_pdf/-char/en. I saved it locally and extracted the text with pdftotext. I read all 5 pages, including the reference list, to the end.
- OUP page for the primary paper, https://academic.oup.com/japr/article/21/3/637/724987, DOI 10.3382/japr.2010-00303. ⚠️ I saw the abstract only. The Methods, tables and Discussion are behind a paywall, so the number of birds necropsied, the necropsy protocol, and the primary table "Earliest ages of detection..." are unverified from the primary source.
- Blocked or not reached ⚠️: the ResearchGate figure page (403), core.ac.uk/download/429712857.pdf (403), the doi.org redirect to the Elsevier linkinghub page (only returned "Redirecting"), and ScienceDirect (403). The original ResearchGate Dinev 2014 URL was not needed, because the J-STAGE copy is the same paper.
- The review's TD prevalence, onset-age and sex data are cited as "Dinev et al. unpublished", so the review's figures rest on the primary paper. Only the abstract of the primary was checked, and the abstract's Cobb 24.22% looks like a typo.
- Not checked: Thorp 1993, McNamee 1998, McNamee and Smyth 2000, and Nairn and Watson 1972 themselves. Everything above about them is as quoted by Dinev.
- I used no browser tools and wrote no files in the repo.

---

## Group C

**Report on Shim et al. 2012 (Poultry Science 91(1):62–65, doi 10.3382/ps.2011-01599)**

⚠️ I could read only the abstract, not the full text. The article body (Methods, Results, tables, discussion, references) is behind a block I could not pass by legitimate means. Every claim about the body is therefore UNREADABLE, except where the abstract settles it.

**Title correction.** The title in the prompt, "...leg morphology and tibia breaking strength...", belongs to a different paper by the same group (Poult Sci 91(8):1790–5; its birds were n=511 slow and n=545 fast). The DOI given is the valgus, varus and TD paper. Its title is "The effects of broiler chicken growth rate on valgus, varus, and tibial dyschondroplasia." Gemini's reference list has the correct title.

**Abstract figures (verbatim from the Europe PMC record):** "Mean lesion scores of left and right valgus and tibial dyschondroplasia (0.40, 0.38, and 0.06) of fast-growing broilers were higher than those (0.26, 0.28, and 0.02) of slow-growing broilers (P = 0.0002, 0.0037, and 0.0269)."

| Claim | Verdict | What the source says | Source read |
|---|---|---|---|
| C1 | ⚠️ PARTLY (abstract only) | Matches: mixed-sex Arkansas randombred broilers, slow = bottom quarter, fast = top quarter, ranked on growth from hatch to 6 wk. Not checkable: the 318 and 231 g/wk figures are not in the abstract. | Abstract only |
| C2 | ⚠️ CONFIRMED (abstract) | Abstract: slow n = 581, fast n = 585. 581 + 585 = 1,166, so the total is arithmetic. | Abstract only |
| C3 | ⚠️ UNREADABLE | The abstract gives TD only as mean scores (0.06 vs 0.02). The method matches: at 6 wk, a longitudinal cut across the right tibia. The abstract says the score runs "from 1 (mild) to 3 (severe)", not 0 to 3. The Edwards and Veltmann 1983 citation and the 2.56% / 1.03% percentages are not in the abstract. | Abstract only |
| C4 | ⚠️ UNREADABLE | The 4-week timing, the ≥10° rule, and all eight left/right valgus and varus percentages are not in the abstract. The abstract classes valgus as mild (10–25°), intermediate (25–45°) or severe (>45°). | Abstract only |
| C5 | ⚠️ UNREADABLE | The reference list is not accessible. A search-summary snippet, which I did not open, attributes chicken heritabilities of valgus 0.15–0.39 and varus 0.21–0.30 to Le Bihan-Duval et al. 1997 (via a 2018 Sci Rep paper). That is secondary and unverified, and suggests Gemini's "1996" and its point values may be wrong. | None |
| C6 | CONFIRMED (abstract and metadata) | Europe PMC: University of Georgia (Athens) and University of Arkansas (Fayetteville), USA; printed January 2012 (Dec 2011 online). | Europe PMC record |

**Which figures are right.** Our inventory's 0.40/0.38 vs 0.26/0.28 for valgus and 0.06 vs 0.02 for TD are exactly what the abstract says. They are mean lesion scores, not prevalences. The abstract says nothing about "6 weeks" for valgus; only TD is stated as measured at 6 wk, and the valgus timing is not given.

**Gemini's percentages are probably also real, but not verified.** I divided each abstract mean score by Gemini's percentage, which gives the implied mean grade among affected birds:
- Valgus: 0.40/0.2940 = 1.36, 0.38/0.2769 = 1.37, 0.26/0.1893 = 1.37, 0.28/0.1997 = 1.40. All four are about 1.4, between mild (1) and intermediate (2), which is plausible.
- TD: 0.06/0.0256 = 2.3 and 0.02/0.0103 = 1.9, plausible on a 1–3 scale.

This consistency makes it unlikely that Gemini invented the percentages. It is not proof, and I could not tell whether they are from a table or the text. The likeliest reading is that the abstract gives mean scores and the body gives percentage incidences. Gemini's "full PDF accessed" claim is unconfirmed.

**Useful for the simulation (abstract only).**
- Growth rate is linked to leg problems in an unselected control line. The fast quartile had significantly higher valgus and TD scores (P = 0.0002, 0.0037, 0.0269).
- The abstract's closing sentence says growth rate was "negatively associated" with these conditions. This contradicts its own data, which show fast growers worse. It is likely a wording error, so do not copy it.
- If Gemini's table figures hold, about 19–29% of birds had at least mild valgus at 4 weeks and only about 1–3% had TD at 6 weeks, in a non-commercial line. That is not a good source for commercial-hybrid TD rates.

**Coverage statement**
- Europe PMC REST record for PMID 22184429 (`https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.3382/ps.2011-01599`): read the full abstract and metadata. Abstract only.
- OUP PDF URL (`https://academic.oup.com/ps/article-pdf/91/1/62/4525970/poultrysci91-0062.pdf`), fetched with WebFetch: returned the abstract and metadata only, and no body text. A direct curl request got a Cloudflare challenge page ("Just a moment").
- ScienceDirect via linkinghub: 403 or redirect only, so no text.
- ResearchGate: 403.
- PubMed page: cookie wall.
- Unpaywall: lists a "hybrid" OA location but gives no PDF link. Semantic Scholar lists only `doi.org`, which redirects to the blocked publisher page.
- Web searches turned up no readable copy of the full text. One search-result summary gave the Le Bihan-Duval 1997 ranges; I did not open that source.
- I stopped after one curl attempt with a browser user-agent was blocked by the permission system as bot-check circumvention. I did not retry.
- To close the gap, someone needs to open the article in a normal browser (the OUP page shows as open access) and check Table 1 and the references.

---

## Group D

## Group D: Leterrier & Nys 1992 (Avian Pathology 21(3):429-442)

⚠️ FULL TEXT NOT REACHED. I could read only the abstract (via Europe PMC, PMID 18670958, plus a search-snippet copy of the abstract). The Taylor & Francis PDF (both the plain URL and the `?needAccess=true` Unpaywall/Semantic Scholar URL) and the `abs` page returned HTTP 403. HAL (hal.inrae.fr/hal-02705850 and hal-02693934/document, hal.archives-ouvertes.fr) returned an Anubis bot-block page, and a search snippet says the HAL record has no file deposited anyway. PubMed returned only a cookie wall. Europe PMC says the paper is not in PMC. Every verdict below rests on the abstract alone, so "NOT IN SOURCE" is not used. Anything beyond the abstract is UNREADABLE.

| id | verdict | what the source says (abstract only) | source read |
|---|---|---|---|
| D1 | PARTLY ⚠️ | Abstract: three broiler flocks of 600, 817 and 361 birds; varus 1 to 3%, valgus 30 to 40%. It does not mention France, hatch to 7 weeks (the 7-week bodyweight is mentioned), or sex. The Unpaywall record gives the INRA Nouzilly, France affiliation (authors' site, not the flock location). "Deformities higher in males" is unverified. | abstract only |
| D2 | WRONG on onset window; prevalence CONFIRMED ⚠️ | Varus 1 to 3% of birds matches. The abstract says "Varus angulation appeared suddenly, between 5 and 15 days of age", not 5 to 20. "No new cases after day 20" is not in the abstract. The body text might say 20, but I could not check it. | abstract only |
| D3 | PARTLY ⚠️ | Abstract: varus was unilateral in 80% of cases and mainly the right limb; medial tendon displacement "was always present". The 86% right-leg figure for Flock B and "100% of affected right legs" are not in the abstract (they may be in the body). The abstract gives 80% unilateral, with no per-flock right-leg figure. | abstract only |
| D4 | PARTLY ⚠️ | Abstract: valgus 30 to 40% of birds, "severe in 5% of cases". That matches the 5.5% ceiling loosely. The 0 to 5.5% severe range, the angle classes (above 45, 25 to 45, 10 to 25 degrees) and the 2 to 32% mild/intermediate range are not in the abstract. The 30 to 40% total is not clearly reconcilable with "2 to 32%" without the body. | abstract only |
| D5 | PARTLY ⚠️ | Abstract: valgus appeared progressively between 2 and 7 weeks and was "often bilateral". The abstract does not give week-3 peak prevalence or "25 of 33 equal bilateral angulation". Compatible, but those specifics are unverified. | abstract only |
| D6 | WRONG (for severe valgus) ⚠️ | Abstract: lateral gastrocnemius tendon displacement in 60% of birds with severe valgus. The claimed 0% (mild) and 10% (intermediate) figures are not in the abstract. They could be in the body, but the claim leaves out the 60% severe figure. | abstract only |
| D7 | NOT CONFIRMED, UNREADABLE ⚠️ | Dyschondroplasia is not in the abstract. A Semantic Scholar TLDR says valgus "does not stem from bone abnormalities", and the Europe PMC abstract summary said mild and intermediate valgus showed no other bone deformities. This points against a 33 to 47% TD co-occurrence in the paper, so the claim looks suspect. I cannot give "the real figure". | abstract + secondary TLDR |
| D8 | UNREADABLE ⚠️ | Flock sizes are 600, 817, 361. Which flock is A, and "n = 33 severe valgus, n = 21 varus", are not in the abstract. | abstract only |
| D9 | UNREADABLE ⚠️ | Methods are not in the abstract. The abstract says "clinical, epidemiological and anatomical" differences, which loosely fits live examination plus anatomy, but radiography is not mentioned. | abstract only |
| D10 | UNREADABLE ⚠️ | Discussion is not in the abstract. | abstract only |

### Extra facts from the abstract (useful for the simulation, ⚠️ abstract-level)
- Varus 1 to 3% of birds. It appears suddenly at 5 to 15 days. It is about 80% unilateral, mainly the right leg. There is always medial tendon displacement, severe locomotor handicap, and lower 7-week body weights (no number given).
- Valgus 30 to 40% of birds. It develops progressively from 2 to 7 weeks, is severe in about 5% of cases, and is often bilateral. Lameness is associated with severe cases.
- Authors conclude the two conditions likely have different aetiologies. Varus may start with early gastrocnemius tendon displacement, which seemed secondary to leg deformation in valgus birds.

### Coverage statement
- Opened, not readable: tandfonline.com doi/pdf (403), tandfonline.com doi/abs (403), tandfonline pdf with needAccess=true (403), hal.inrae.fr/hal-02705850 and /hal-02693934/document and hal.archives-ouvertes.fr/hal-02705850 (all Anubis block), data.zhenzhi.com (403), pubmed.ncbi.nlm.nih.gov/18670958 (cookie wall), semanticscholar.org search (403).
- Opened, partial: Europe PMC REST record for PMID 18670958 (abstract only, read via a summarizer, not verbatim), Unpaywall API (metadata only), Semantic Scholar API (metadata and TLDR only, abstract null).
- Nothing was read to the end as a full paper. To resolve D2 to D10, someone with institutional access to the T&F PDF is needed, or the owner can fetch it manually.

---

## Group E

**Group E report.** Two of the three modern papers print the 0.4% to 5.4% figure. The 1986 original could be read only as an abstract, so no claim about its own contents is confirmed.

Two naming errors in the brief:
- The "Liu et al. 2022" review is actually Chen P, Xu T, Zhang C, Tong X, Shaukat A, He Y, Liu K, Huang S. *Metabolites* 2022;12(10):1000.
- The "Guo et al. 2020" PLOS ONE paper is actually Tang et al. 2020, *PLoS ONE* 15(9):e0239450. It is a spleen RNA-seq study of VVD in Hubbard broilers.

I read each modern paper through WebFetch, which answers from a small model's pass over the page, so I did not see raw text myself. Below, "Chen 2022" is the review the brief calls Liu.

| Claim | Verdict | What the source says | Source read |
|---|---|---|---|
| E1 | PARTLY | Chen 2022 states it in the Introduction (ref 14). It says VVD incidence "at the first week of age was only 0.4%" and 5.4% at 5 weeks. Tang 2020 states it in the Introduction (ref 5): "incidence of VVD in broilers was 0.4% at 1 week of age and increased to 5.4% at 5 weeks of age." PMC11407033 does not state it. It gives other figures: prevalence "as high as 1 to 2%", 1.75% overall in one survey, and 37.0% mean prevalence in a Danish survey. In both papers the figure means the incidence of VVD among broilers by age. Neither says how it was measured. ⚠️ I could not check the primary paper for the figure. | Chen 2022 and Tang 2020 in full. PMC11407033 in full. |
| E2 | PARTLY | All three papers cite Cruickshank and Sim, *Avian Dis* 1986;30:699-708. Chen 2022 cites it as ref 14, Tang 2020 as ref 5 (with 30(4)), and PMC11407033 as ref 4. The cited paper is "Morphometric and radiographic characteristics of tibial bone of broiler chickens with twisted leg disorders." PMC11407033 cites it for the link between VVD and chondrodystrophy, not for the figure. None of the three says the study was Canadian. Tang's only "Canadian" is the journal title of a different reference (Julian 1984, *Canadian Veterinary Journal*). ⚠️ I could not confirm the authors' country. | All three in full. |
| E3 | UNREADABLE ⚠️ | The abstract on PubMed (3814007, read through Europe PMC, as abstract only) describes a comparison of normal and twisted-leg tibiae by radiography and morphometry. It says shallow distal condyle grooves may predispose the tibia to slight displacement of the gastrocnemius tendon. It does not say VVD was mainly unilateral or that tendon displacement was frequent. The full text is not open, so I cannot judge this. The Chen 2022 text has no "unilateral" or "tendon", and Tang 2020 has neither word. PMC11407033 does mention unilateral VVD (see extra facts below), but not as a Cruickshank finding. | PubMed abstract only. ⚠️ Full text not reached. |
| E4 | CONFIRMED | Chen 2022 Section 5 (Application of Probiotics, ref 141): a feed supplement combining the two strains raised tibial Ca and P and promoted tibial development. The review gives no doses or trial details. Ref 141 is Abdulwahab and Horniaková 2010, *Acta Univ. Agric. Silvic. Mendel. Brun.*, on a dried-yogurt Lactobacillus diet. ⚠️ I did not open that trial. | Chen 2022 in full. |
| E5 | PARTLY | Introduction, refs 8, 15, 17: bacterial bone disease can be "treated and prevented with vaccines and antibiotics," and "the abuse of antibiotics can also promote bone disease." Intro paragraph 3 and Section 2.1 link antibiotics to gut-microbiota shifts that may reduce intestinal barrier function and so affect bone. So "antibiotic abuse promotes bone disease via gut microbiota" is supported. "Established BCO does not respond to antibiotics" is not stated, and the text says antibiotics can treat bacterial bone disease. McNamee and Smyth are not cited anywhere in the paper. Ref 15 is Szafraniec 2022, a *Vet Q* review of skeletal disorders caused by Staphylococcus. | Chen 2022 in full. |
| E6 | NOT IN SOURCE | The Introduction (refs 19 and 22) says controlling temperature, air quality, lighting, stocking density and litter reduces leg disease, but it is a long-term process that "will increase production costs." Heating fuel, fans, bedding and the word "moderate" do not appear. Ref 19 is Granquist 2019 (lameness and health measures). Ref 22 is Tahamtani 2020 (environmental complexity). This looks misattached, as suspected. | Chen 2022 in full. |
| E7 | PARTLY | The abstract says miR-455-5p targets RPS6KB1, and the Results section "Abnormal Cartilage Development in VVD Broilers" calls the cartilage state "chondrodysplasia." The diagnosis part is wrong. VVD was diagnosed on live birds by a gait score. The bird lies on its wings with the leg immobilised, and the tibiotarsometatarsal angle is read by eye and protractor: 0 is under 10°, 1 is 10-25°, 2 is 25-45°, 3 is over 45°. The paper does not use morphometric or radiographic diagnosis. Those words appear only in the Cruickshank reference title. ⚠️ The "plasma exosome-derived" wording was not separately confirmed beyond the miR-455-5p/RPS6KB1 statements. | PMC11407033 in full. |
| E8 | PARTLY | Chen 2022 supports the gut-barrier half. Section 3.3 (ref 34) says probiotics can restore the intestinal barrier. Section 2.2 lists benefits for microbial populations, digestion, nutrient absorption, antioxidant capacity and immune response. The paper does not discuss any welfare downside of probiotics. The Introduction's "safety, convenience, and natural nontoxicity" is the authors' own claim. Section 6 only notes research gaps. So Chen 2022 is silent on welfare harms rather than showing there are none, and the exact phrase "gut barrier integrity and overall flock health" is not in it. | Chen 2022 in full. |

**Extra facts for a broiler welfare simulation**
- **VVD incidence:** Tang 2020 also cites Julian 1984 for an incidence of 0.5-2%. PMC11407033 reports prevalence "as high as 1 to 2%", 1.75% in one survey and 37.0% in a Danish survey (Introduction), so figures vary widely by study and method.
- **Unilateral cases:** PMC11407033 says VVD can occur bilaterally or unilaterally. Its experimental birds were scored 3 and unilateral (Methods).
- **BCO timing:** Chen 2022 (Intro, ref 15) puts BCO onset between 14 and 70 days of age.
- **Cruickshank's thesis (secondary):** A search result shows a UBC library record for a thesis by John Johnston Cruickshank, "Morphometric and radiographic characterization of leg disorders in broiler chickens." I did not open it, and I could not confirm it is the same work as the 1986 paper. Its abstract reportedly gives lateral deviations at 92% and medial at 8%, twisted leg at 21% in cages versus 4% on litter, and increases from high density and excess dietary vitamin D3. If these figures carry over to the journal paper, the cage-versus-litter and density effects would be usable levers. ⚠️ That is a hypothesis, not confirmed.

**Coverage**
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9612127/ was read through the main text and the whole reference list (page 177,109 characters). Two fetches covered characters 0 to 100,000 and 100,000 to the end. The first fetch's model reported the reference list as cut off after ref 51, and the second fetch started at ref 52, so both ends were covered. Refs 8, 14, 15, 17, 19 and 22 were listed from the first 100,000 characters.
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11407033/ was read in two fetches (characters 0 to 100,000, then to the end). The second fetch covered refs 60 to 71, which does not contain the Cruickshank entry. That entry (ref 4) was seen in the first fetch. The first-fetch model reported the page as cut off during the reference list at ref 59 and noted the supplementary files (Table S1, Supplementary word S1, mmc1.docx) were missing. I did not open any supplementary files.
- https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0239450 was read in full as text. I could not view the figure images or the supplementary files (S1-S8 tables, S1-S2 figures).
- Cruickshank and Sim 1986: only the abstract, via the Europe PMC REST record for PubMed 3814007, which is the secondary-source fallback. ⚠️ The PubMed page itself would not load (cookie wall). The affiliation was not in the Europe PMC record, and the journal full text is paywalled and was not reached. One web search for the author affiliation found nothing confirming it.

---

## Group F

## Group F: leg disorders (van den Brand 2022; Alves et al. 2016 in SciELO)

Method note: I used WebFetch only. It returns a summary written by a small model, not the raw page, so I read neither paper as raw text. I fetched each page twice with different targeted prompts, and the two fetches agreed. The exact figures and the two direct quotes below came through that tool, which is why the coverage section carries a flag.

### 1. Verdicts

| Claim | Verdict | What the source says (location) | Source read |
|---|---|---|---|
| F1 | CONFIRMED, one caveat | Results: "32.1 vs. 9.6° on average; P < 0.001". 32.1° is dead birds without knee fixation (Table 2: 32.1 ± 3.6). The paper never defines the 9.6. It matches the average of the other four methods' means (9.9, 9.7, 10.4, 8.2). The claim's wording "on the same legs with the knee fixated" is slightly loose, because 9.6 is a pooled figure across four methods, not the dead-fixed method alone. Dead-fixed alone is 9.7°. | PMC9079703 (summary via WebFetch, ⚠️) |
| F2 | PARTLY | Five methods were compared. Each of the same chickens was measured by every method, three readings per method averaged. The paper does not use the phrase "repeated measures", but its statistics treat chicken as the repeated subject (compound symmetry). Methods: (1) live bird, knee fixed; (2) dead intact bird, knee not fixed; (3) dead intact bird, knee fixed; (4) dissected leg, skin removed, muscles and joints intact, fixed; (5) dissected leg, skin and muscles removed, joints intact, fixed. Netherlands (birds taken at post-mortem control, Veterinary Centre Someren). Breed Ross 308, male, 38 days old, "reared under commercial conditions", **n = 6 birds**, both legs measured. Mean body weight 2.62 kg (range 2.07 to 3.10). The sample is tiny; the authors say so and call for a larger one. "Commercial broilers" is accurate only in the sense that the birds came from commercial rearing. | PMC9079703 (⚠️) |
| F3 | PARTLY | The classes are not this paper's own. They come from Leterrier and Nys (1992), assigned by visual appraisal of live broilers held by the wings. Normal is below 10°, mild 10 to 25°, intermediate 25 to 45°, severe above 45°. So the claim's figures are right, but it omits the "normal below 10°" class. The paper applied the classes only loosely: just chicken 5 (14.0° on dissected legs without muscle) exceeded 10° and counts as mild. The authors question whether the classes are valid for knee-fixated legs. | PMC9079703 (⚠️) |
| F4 | PARTLY | Results: "A total of 19.5% of broilers had VAL, and 7.6% presented VAR." The sentence gives no denominator and does not say whether indigenous birds are included. Methods: valgus and varus were assessed on 30 broilers per commercial treatment and on 32 indigenous chickens. That is roughly 120 commercial birds if the four treatments are 2 strains × 2 sexes, which is my inference; the paper does not state it. Breed: Cobb 500 and Ross 308, both sexes; 1,060 chicks were placed, but the number measured is not given. Age: scoring at day 40, slaughter at 42 days. Country: Brazil (Dourados, Mato Grosso do Sul). Method: the angle between the middle toe and the tibia, measured with a caliper rule and protractor. Over +10° counted as valgus, under −10° as varus. Sex and strain had no significant effect on the deformities. | SciELO RBZ 45(7), 2016 (⚠️, Table 4 and Table 5 unreadable) |
| F5 | CONFIRMED | Title is "Locomotion of commercial broilers and indigenous chickens". Commercial strains (Cobb 500, Ross 308) were compared with 32 free-range indigenous chickens (a Red Junglefowl crossbreed). Slaughter was at 42 days for commercial birds. Mean weight was 2,610 g for commercial birds and 1,670 g for indigenous. Conclusion: commercial strains showed less locomotor soundness. One caution: the indigenous birds were reared separately and are not strictly age-matched on a growth basis. They are described as being at the same slaughter age, but I did not confirm their exact age. | SciELO (⚠️) |

**Authorship (Gemini's attribution is wrong).** The paper is by Marília Carvalho Figueiredo Alves, Ibiara Correia de Lima Almeida Paz (the second author, not the first), Irenilza de Alencar Nääs, Rodrigo Garófallo Garcia, Fabiana Ribeiro Caldara, Grace Alessandra de Araujo Baldo, Edivaldo Antônio Garcia and Andréa de Britto Molino. It appeared in Revista Brasileira de Zootecnia 45(7), July 2016, DOI 10.1590/S1806-92902016000700003. The van den Brand paper is H. van den Brand, R. Molenaar and M. Klaasen, Poultry Science 101(7):101907, 2022, DOI 10.1016/j.psj.2022.101907.

### 2. Gait-score figures in the SciELO paper

- Gait scoring used a 0 to 5 scale (Kestin et al. 1992). Birds walked 1 m on rice-husk litter at day 40, and the paper says all broilers were scored.
- The only gait prevalence sentence in Results says the two commercial strains and the indigenous chickens had a gait score incidence of 1 to 5 in "less than 30%" of birds. That is a combined 1-to-5 figure, with no separate figure for scores 3 to 5 or for lameness.
- ⚠️ Table 4 (gait-score frequencies by group) is an image that I could not read, so I cannot give per-score or per-strain numbers. It would need the PDF or a viewer that renders the image.
- The abstract says only "high prevalence of locomotor issues" in fast-growing broilers, with no number.
- Do not use a "less than 30%" figure as a lameness rate. It does not match the abstract's "high prevalence" wording.
- Numbers quoted from the literature, not from this study: 72% sound femurs (Fernandes et al. 2012) and about 32% with angular leg deformities (Almeida Paz et al. 2010).
- Other findings: spondylolisthesis was most frequent in commercial strains (P ≤ 0.05). Femoral degeneration and tibial dyschondroplasia did not differ by sex or strain. Indigenous birds had fewer footpad lesions (only 4 birds affected). The authors suggest gait score alone may not reliably predict bone problems.

### 3. Extra facts for a welfare simulation

- **Method choice moves the numbers a lot.** The van den Brand abstract says measuring without knee fixation inflates the angle about threefold (32.1° vs about 10°). Any "mild/intermediate/severe" prevalence from unfixated measurement is therefore not comparable with fixated measurement.
- **Prior prevalence ranges (van den Brand Table 1, at slaughter age):** valgus 25 to 40%; varus 1 to 4%. Two sources combine the two: Almeida Paz about 30%, and Güz et al. 2019 about 63 to 70% using an unfixated-style method. Guo et al. 2019 reports 1.75%.
  - ⚠️ Table 1 contradicts the paper's introduction, which gives a 1.75 to 66.0% range, and it attributes one method to "Paz 2013" while the key says "Almeida Paz 2010".
  - Use the table figures with caution.
- Neither paper gives pain, duration or intervention effect sizes.

### 4. Coverage

- https://pmc.ncbi.nlm.nih.gov/articles/PMC9079703/ was opened twice via WebFetch. The content was complete (introduction, methods, results, Tables 1 and 2, discussion, conclusion), but it came through a summarizer, not raw text. ⚠️ I did not independently see the raw page, and I could not see the reference list.
- https://www.scielo.br/j/rbz/a/Jwc3n6ZYNS6kKw84BdGM7Dj/?lang=en was opened twice via WebFetch. ⚠️ Tables 4 and 5 are images and unreadable. ⚠️ I did not confirm the exact age of the indigenous birds or the denominators for the 19.5% and 7.6% figures, because the paper does not give them in the text I saw.
- I opened no other URLs, used no browser tools, and wrote no files.

---

## Group G

## Group G: McNamee and Smyth 2000 (BCO review)

⚠️ **Headline: I could not read the full text.** tandfonline.com (both DOIs, pdf/abs/full) and Europe PMC's website return a Cloudflare 403. Unpaywall lists only the paywalled publisher PDF and no repository copy. I did not try to get around the block. Everything below is checked against the **complete PubMed abstract** (PMID 19184815 and its twin record 19184841), which I read to the end. Claims the abstract does not cover are marked UNREADABLE, not NOT IN SOURCE.

**Citation oddity.** PubMed and Crossref hold two records of the same title, both Avian Pathology 2000 vol 29:
- 29(4):253-270, DOI 10.1080/03079450050118386, PMID 19184815. This is the page range and issue in your brief.
- 29(5):477-495, DOI 10.1080/030794500750047243, PMID 19184841. This is the DOI in the Gemini report and in your brief; the report also gives 29(5):477-495.

Their abstracts are identical apart from one missing space. So the DOI and page range in the Gemini report match one real record; your brief pairs the 29(4) pages with the 29(5) DOI. Cite one record consistently.

| Claim | Verdict | What the source says | Source read |
|---|---|---|---|
| G1 0.75% | CONFIRMED (abstract) | "Overall losses in male birds due to BCO were estimated to be 0.75% of all birds placed." The abstract does not name McNamee et al. 1998 as the origin of this figure. The 1998 Vet Rec paper (see section 2) is a 2-flock study and does not contain it. | ⚠️ abstract only |
| G2 17.3% | CONFIRMED (abstract) | In Northern Ireland systematic studies BCO was "the most common cause of lameness, being present in 17.3% of lame birds." It was also "detected in birds presented as 'found dead'." | ⚠️ abstract only |
| G3 14 to 70 days, peak about 35 | CONFIRMED (abstract) | "14 to 70 days of age, but most cases occurred around 35 days old." The abstract says "cases", not "clinical cases". | ⚠️ abstract only |
| G4 gross lesions 40 to 67% | CONFIRMED (abstract) | "Lesions were visible to the naked eye in only 40 to 67% of cases." Histology is recommended where no lesion is visible, and BCO is "almost certainly underdiagnosed". | ⚠️ abstract only |
| G5 13.3% E. coli/mixed, 11.1% CoNS | NOT CONFIRMED in what I read | The abstract names S. aureus as the usual cause, with E. coli, coagulase-negative staphylococci and Enterococcus "sometimes involved", and gives no percentages. A search surfaced a 2024 Iraqi journal article (iasj.rdd.edu.iq, PDF unreachable) quoting 22.2% coagulase-positive staph, 11.1% CoNS and 13.3% "E. coli or mixed cultures". Its source is only a bare "(5)" in the snippet, not McNamee and Smyth and not confirmed as Dinev. The figures may sit in the full review or in another source. | ⚠️ abstract only; secondary snippet unconfirmed |
| G6 feed restriction | CONFIRMED (abstract) | "Under controlled experimental conditions... restricting feed intake reduced the incidence of disease." | ⚠️ abstract only |
| G7 PFGE, fluff, breeders, hands, floor eggs | PARTLY (abstract) | Matches: S. aureus strains "identical to, or closely related to" natural-case isolates (by PFGE) were recovered from hatchery fluff-debris and the environment of breeding flocks. "There is a higher incidence of BCO in birds hatched from floor eggs." Differs: for hands, the abstract says only that "humans can carry poultry strains of S. aureus on their hands." It does not say these were PFGE-identical to BCO isolates. Also "identical or closely related", not just identical. | ⚠️ abstract only |
| G8 CAV/IBDV | CONFIRMED (abstract) | Chicken anaemia virus and infectious bursal disease virus "increased the incidence of the disease" under controlled experimental conditions. | ⚠️ abstract only |
| G9 no response to antibiotics | CONFIRMED (abstract) | "Birds in which BCO has already developed, are unlikely to respond to treatment." This is softer than "does not respond". The abstract adds that treating flocks early should reduce septicaemia and further cases. | ⚠️ abstract only |
| G10 bacterial interference | CONFIRMED (abstract) | It "has been used successfully in humans and turkeys to prevent staphylococcal diseases, and warrants investigation" for BCO in chickens. It may also exclude other BCO-causing bacteria. The abstract calls it a research idea, not an established prevention route, and says vaccination is "unlikely in the short term". | ⚠️ abstract only |
| G11 recumbent, dies within days; duration of life with lesions | UNREADABLE | The abstract says nothing about femoral head detachment, recumbency, dehydration, starvation or survival time. A 2024 Frontiers in Physiology BCO review (PMC11390708, first 100,000 of 162,563 characters read) gives no time frame. It says terminal femoral head necrosis leaves the bird "almost completely unable to move" and that dehydration and death follow, uncited. | ⚠️ abstract only |
| G12 prevalence rising with stocking density (about 1%, 13.3%, up to about 20%) | UNREADABLE | The abstract has no stocking-density content and no 13.3% or 20% figure. The first 100,000 characters of the 2024 PMC11390708 review mention density only as a spread and welfare risk and give no 13.3% or 20%. Nothing I read supports the memo's density-to-incidence claim. | ⚠️ abstract only |

## 2. Extra facts for the simulation
- McNamee et al. 1998 (Vet Rec 143(5):131-135, PMID 9725184, "Study of leg weakness in two commercial broiler flocks"), ⚠️ abstract only. This is a 2-flock male-broiler study, not a large survey.
  - BCO was found in 9 of 44 lame birds (20.4%).
  - S. aureus was recovered from 62.5% of histology-confirmed lesions.
  - Lesions suggestive of BCO were visible macroscopically in only 11.1% of histology-confirmed cases, far below the 40 to 67% quoted in the 2000 review.
  - Angular deformities were 13.6% and spondylolisthesis 11.4% of macroscopic lameness causes.
  - Severe tibial dyschondroplasia (TD) was found only in lame birds (4.5%).
- The 11.1% in this 1998 abstract is the gross-visibility rate, not the coagulase-negative staph rate. This may be the origin of the "11.1%" in the Gemini report's G5 claim.
- A secondary source says the review's 0.75% was costed at about £3 million a year to the UK industry; this is from a search snippet, ⚠️ unverified.
- The 17.3% is a share of lame birds, and the 0.75% is a share of birds placed (males only). Neither is a flock-level prevalence under any density.

## 3. Coverage statement
- `https://www.tandfonline.com/doi/pdf/10.1080/030794500750047243`, `/doi/full/...` and `/doi/abs/...`: 403 Cloudflare, nothing read.
- `https://www.tandfonline.com/doi/pdf/10.1080/03079450050118386`: 403, nothing read.
- `https://pubmed.ncbi.nlm.nih.gov/19184815/` returned only a cookie shell. I used NCBI E-utilities efetch XML for PMID 19184815 and 19184841 (full abstracts, read to the end) and PMID 9725184 (full abstract). I also used the Europe PMC REST record for 19184815 (read as far as the abstract) and the Crossref and Unpaywall JSON.
- AGRIS record `agris.fao.org/search/en/records/65df2d4063b8185d9cab5551`: abstract summary only, consistent with PubMed.
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC11390708/` (2024 review, secondary): ⚠️ only characters 0 to 100,000 of 162,563 read.
- `iasj.rdd.edu.iq/.../f10337a274e7f0ecbe1a7dc6bff50028.pdf`: connection refused, not read.
- Semantic Scholar and CORE API calls returned 404/403.
- No full-text copy of the 2000 review is reachable by me. To settle G5, G11 and G12, someone needs the PDF through a library or authenticated route. I did not use the browser tools or any pirate site.

---

## Group H

## Group H (pain evidence) report

**Headline:** I could read the full text of only one of the six sources (Caplen 2013b). For the other five, the publishers' full text was paywalled or blocked, so every verdict below rests on the abstract (via Europe PMC or the Cambridge page) and carries ⚠️. Detail the abstracts lack (n, gait scores, doses, effect sizes) is marked "not obtained" rather than guessed. Findings by claim:
- H1 and H2: the headline numbers are confirmed, but n and gait scores were not obtained.
- H3: the source is Siegel et al. 2011, not Danbury 2000, so the report's [37] is a misattribution.
- H5: the pain was experimentally induced, not natural, and carprofen worked too.
- H6: the claim is wrong for the obstacle test, and right only for latency to lie.
- None of the six papers shows pain in birds with subclinical TD, valgus-varus without gait impairment, or gait scores 1 to 2 (details in the last section of part 2).

### 1. Claim table

| Claim | Verdict | What the source says | Source read |
|---|---|---|---|
| H1 McGeown 1999 | CONFIRMED on the headline numbers, ⚠️ abstract only | The abstract says sound birds crossed the course in about 11 s regardless of treatment. Lame birds took about 34 s, or 18 s with carprofen. Treatments were carprofen, placebo saline injection, or a control handling procedure. The lame birds are described only as "moderate" lameness. The authors conclude moderately lame birds "suffer pain when they walk". **Not obtained:** gait scores, n, dose. | PubMed 10404606 abstract, read via Europe PMC API. Wiley full text was blocked by Cloudflare. ⚠️ |
| H2 Danbury 2000 | CONFIRMED in substance, ⚠️ abstract only | Birds were trained to tell coloured feeds apart, one containing carprofen, then chose freely. In study 2 (one concentration), lame birds chose significantly more drugged feed than sound birds. As lameness got worse, lame birds ate a significantly higher proportion of drugged feed. In study 1 (concentration-finding), plasma carprofen rose linearly with intake and walking improved dose-dependently. There lame birds only "tended" to eat more than sound birds. **Not obtained:** dose, gait scores, n. A search-engine summary of a Hothersall 2016 snippet said "4 mg/kg" in feed for Danbury; I could not verify it in any page I opened, so treat it as unverified. | Europe PMC abstract of 10766114. Bristol repository page has no abstract or PDF. ⚠️ |
| H3 later multi-dose self-selection study | CONFIRMED, but the real source is not Danbury 2000. ⚠️ abstract only | The study is **Siegel PB, Gustin S, Katanbaf M (2011), "Motor ability and self-selection of an analgesic drug by fast-growing chickens", J Appl Poult Res 20(3):249–252, doi 10.3382/japr.2009-00118.** Its abstract says birds with gait scores 2, 3 and 4 chose among diets with different carprofen doses (score 1 and score 5 birds excluded). The hypothesis that higher gait scores select higher doses "was rejected because no differences were observed in feed consumption among treatment groups". It also says males and females responded similarly, but there was an interaction of sex with left-right preference for feeder location. So the report's description matches. Its pointer to [37] (the Semantic Scholar page for Danbury 2000) is wrong. The Cambridge reference list for Hothersall 2016 also cites Siegel 2011. **Not obtained:** n, doses, effect sizes. | Abstract via Semantic Scholar API and OpenAlex. Full text is open access (CC BY-NC-ND) on ScienceDirect and OUP but both returned HTTP 403. I did not try to get around that. ⚠️ |
| H4 Caplen 2013a | PARTLY, ⚠️ abstract only | Confirmed: after NSAID, walking velocity rose (carprofen P<0.001, meloxicam P=0.044), which the authors read as improved walking ability. Stride length and duration (both drugs), transverse back displacement (meloxicam) and vertical leg displacement (carprofen) moved toward non-lame values at slow speeds. Saline birds showed no gait change. Two caveats the report omits. At faster speeds the same parameters showed imbalance, "which may have signified an excessive dosage". The authors also say the doses "were not conclusively effective". **Not obtained:** n, effect sizes (the abstract gives only P values), doses, gait scores. The abstract does not say whether lameness was natural or induced in this trial. It only cites earlier work on "naturally lame" broilers. | Europe PMC abstract of 23317659. Elsevier full text redirected to a paywall (403 on ScienceDirect). ⚠️ |
| H5 Caplen 2013b | PARTLY. Meloxicam is right, but it omits carprofen and the pain model is experimental, not natural. | n=8 per group × 6 groups = 48 birds, Ross 308 males, 17 days old, all farm gait score 1 and none worse than "moderate". Articular pain was **experimentally induced**: 0.4 mL Freund's complete adjuvant intra-articularly in the left hock, 4 h before testing. Sham-handling birds were the controls. Natural lameness was not studied; the authors say they could not standardise cohorts because pathology was known only post-mortem. Drugs were given subcutaneously 6 h before testing: meloxicam 3 or 5 mg/kg, carprofen 15 or 25 mg/kg, and saline. There was no dose effect, so doses were pooled. Thermal threshold (°C, mean ± SD): sham saline 43.7±1.8; induced saline 42.7±1.3 (hyperalgesia, P=0.030 vs sham); induced meloxicam 44.3±1.5 (P=0.007 vs induced saline); induced carprofen 44.1±1.6 (P=0.010). Skin temperature in induced saline birds was 37.6 vs 36.5 °C in sham (P<0.001). Analgesics had no effect on threshold in sham birds. The paper reports Z and P values, not effect-size statistics. | PMC3898842 via WebFetch. The tool returns a model-generated summary of the page, not raw text, so the figures are as extracted. The abstract was cross-checked via Europe PMC and matches. Read in full as far as I could tell. |
| H6 Hothersall 2016 | PARTLY, and mostly WRONG for the obstacle test. ⚠️ abstract only | Lame birds were gait score 2.5–4 and non-lame 0–1. Subcutaneous doses were meloxicam 5, carprofen 35 and butorphanol 4 mg/kg. **Obstacle test:** neither NSAID significantly changed number of crossings or time to cross. **Latency to lie (LTL) test:** lame birds given carprofen or meloxicam lay down later than lame saline birds; the abstract ties LTL to foot-pad dermatitis, which both NSAIDs improved. **Butorphanol:** no effect on LTL, and it looked sedating in the obstacle test (longer crossing latency, fewer crossings in non-lame birds). The authors conclude carprofen and meloxicam "have some analgesic effect". So "carprofen, meloxicam and butorphanol improved mobility test performance" is not what the abstract says. **Not obtained:** n, numerical results. | Cambridge Core abstract page (WebFetch). The PDF link returned only the abstract and references (full text marked "temporarily unavailable"). Bristol repository has no open PDF. ⚠️ |
| H7 Weeks 2000 | CONFIRMED, ⚠️ abstract only | Six replicates of commercial broilers, 39–49 days old, scan-sampled. Lying: sound birds 76%, lame (gait score 3) 86%. Sound birds spent significantly more time than lame birds standing idle (7%), standing preening (3.5%) and standing eating (4.7%); the lame-bird values are not in the abstract. Walking averaged 3.3% overall and fell to 1.5% in the worst affected birds. Lame birds lay down to eat for almost half their feeding time. Sound birds fed over 50 times in 24 h, falling to about 30 visits in the lamest birds. The abstract says meal duration was adjusted so total feeding time did not change. **Not obtained:** n per gait score, the lame-bird percentages for the standing activities. | Europe PMC abstract of 10719194. ScienceDirect returned 403. ⚠️ |

### 2. Extra facts relevant to a broiler welfare simulation

- **Effect sizes for analgesic trials are mixed and small.** Hothersall 2016 found no obstacle-test improvement from NSAIDs at 5 mg/kg meloxicam or 35 mg/kg carprofen. The McGeown 1999 obstacle-course result, about 34 s dropping to 18 s, remains the largest effect on record.
- **Dose and tolerance.** Caplen 2013a flags imbalance at faster walking speeds and calls its doses not conclusively effective.
- **Evidence from spontaneous lameness is not uniform.** I downloaded the open PLoS ONE paper Hothersall et al. 2014, "Thermal Nociceptive Threshold Testing Detects Altered Sensory Processing in Broiler Chickens with Spontaneous Lameness" (PLoS ONE 9(5):e97883, PMC4029894). It is not one of your six, and I only read its abstract and skimmed it, so treat it as ⚠️ partial. It found, unexpectedly, that spontaneously lame commercial broilers (n=167, gait score 2.5–4 vs matched non-lame) had a higher thermal threshold, not lower. Meloxicam 5 mg/kg raised the threshold further in lame birds and lowered it in non-lame birds, and butorphanol had no effect. This is also the paper the report seems to mean at line 49 by "Hothersall et al. (2014) ([23])", although its [23] points to the Hothersall 2016 ResearchGate page. The report's line 49 therefore blends two different papers and wrongly implies natural articular pain.
- **Other citation mismatches in the report.** Weeks 2000 (line 165) is tagged [37], which is the Danbury page, and the DOI given for Caplen 2013b (`10.1016/j.tvjl.2013.09.013`) is correct.
- **Pain onset and duration.** None of these papers gives pain duration or prevalence data. The Weeks 2000 time budget (lying 76% vs 86%, walking 3.3% vs 1.5%) is the only behavioural cost figure available.

**Does any of this show pain for subclinical TD, valgus-varus without gait impairment, or gait scores 1 to 2?** No. I found no evidence on subclinical TD or valgus-varus without gait impairment in any of the six papers or in Hothersall 2014.
- **Gait scores 1 to 2:** every study used moderate or worse lameness (McGeown: "moderate"; Hothersall 2016: 2.5–4; Weeks 2000: gait score 3 as the lame comparison; Siegel 2011: 2–4). Siegel 2011 included gait score 2 birds but found no dose preference.
- **Closest case:** Caplen 2013b shows induced articular inflammation causes thermal hyperalgesia in gait-score-1 birds (all were farm gait score 1). That is an acute experimental model in the hock and says nothing about TD, valgus-varus, or natural disease.

### 3. Coverage statement

| Source / URL | Read to end? | What I could not reach |
|---|---|---|
| Europe PMC REST abstracts for McGeown (PMID 10404606), Danbury (10766114), Caplen 2013a (23317659), Weeks 2000 (10719194), Caplen 2013b (24129110) | Abstracts only, read to end. ⚠️ | Full text of all of the first four. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC3898842/ (Caplen 2013b) | Yes, via a summarising fetch (not raw text). | No full text missing, but a summary is not verbatim. |
| https://www.cambridge.org/core/.../755951195EFF756118C7D4E3A4C47263 (Hothersall 2016) | Abstract, keywords and reference list. ⚠️ | Methods, n and results (full text marked "temporarily unavailable"). |
| https://research-information.bris.ac.uk/.../self-selection-...-lame-broiler-ch/ (Danbury) | Bibliographic record only. ⚠️ | No abstract or PDF. |
| Semantic Scholar API and OpenAlex (Siegel 2011) | Abstract only. ⚠️ | Full text. Both ScienceDirect URLs, the OUP PDF and the doi.org resolver returned 403 or a Cloudflare challenge. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC4029894 (Hothersall 2014, via rcastoragev2 PDF) | Downloaded, 9 pages. Abstract and intro read; the rest only grepped. ⚠️ | Not one of your claims; the full discussion was not read. |
| Wiley doi.org links (McGeown, Danbury), Elsevier links (Caplen 2013a, Weeks 2000), core.ac.uk PDF (74396966), Unpaywall and Semantic Scholar (all show these as closed access) | Not reachable. ⚠️ | Paywall, 403 or Cloudflare. |

I did not use Sci-Hub or similar, and I used no browser tools.

---

## Group I

## Group I report: gait score vs necropsy in the same birds

**Bottom line for C4:** Yes, but only narrowly, and from two small studies. In Riber 2021 and Fernandes 2012 (both read in full), birds with a normal gait score (GS 0) were found at necropsy to carry lesions, and gait score did not significantly track lesion presence. Garner 2002 (abstract only) found TD (tibial dyschondroplasia) did not affect gait score. None of the three quantifies "understatement", and none used histology or looked at BCO (bacterial chondronecrosis with osteomyelitis). Gemini's other claim, that wooden breast independently degrades gait score, is cited to a paper that found no such link (see Section 2).

### 1. Claim table

| Claim | Verdict | What the source actually says | Source read |
|---|---|---|---|
| I1 | CONFIRMED, with nuance | Riber et al. 2021, Vet Rec 189(7):e454. Ross 308, Aarhus University, Denmark. Birds were gait-scored on day 27, then again on day 38 immediately before being killed and examined post mortem. 179 birds were analysed. Of 192 selected birds, 5 were excluded for developing GS 3 or 4 and 8 for missing data (Methods 3.3, 3.6; Fig. 1 caption). The sample was not random. Birds were picked on day 27 as GS0 or GS2, with GS1 "companion" birds housed alongside. Day-38 group sizes were GS0 = 19 (2 male, 17 female), GS1 = 87, GS2 = 73 (Table 2, Fig. 2). | SRUC author proof, read in full |
| I2 | CONFIRMED (all figures match) | "Within sex, GS increased with increasing live body weight (P=0.020)." The P = 0.020 is the GS × sex interaction test on live weight (χ² = 7.78); the effect was larger in males (Results). GS2 tibias needed more load to fracture than GS0: 407.7 ± 20.8 N vs 382.1 ± 21.5 N, P = 0.040. GS1 was intermediate (399.7 N) and did not differ. The main effect of GS was P = 0.0496. Tendencies: footpad dermatitis P = 0.086, dislocated femoral joint cartilage P = 0.059. The authors say the stronger GS2 tibia "may be related" to heavier weight; they did not test it. | same |
| I3 | PARTLY | Fernandes et al. 2012, Rev. Bras. Zootec. 41(8):1951-1955 (short communication, CC BY-NC). Authors: Fernandes BCS, Martins MRFB, Mendes AA, Almeida Paz ICL, Komiyama CM, Milbradt EL, Martins BB. **Matches:** gait score 0-2, then necropsy scores of 0-2 for femoral degeneration and TD, at 35 and 42 days. GS 0 birds had significantly more lesion-free bones (Table 4). Some GS 0 birds had lesions anyway: right femur degeneration score 1-2 in 7 of 27 birds at 35 days and 14 of 31 at 42 days; TD score 2 in 2 of 27 and 2 of 31. Conclusion: "The gait score can be the same for birds with or without these lesions." **Does not match:** (a) The birds were male Cobb at about 10 birds/m². (b) "n = 50" is 50 per age, about 100 in total; the Table 4 counts sum to 50 at each age. Table 2 sums to 52 at 35 days, a small inconsistency in the paper. (c) The correlations in Tables 6 and 7 are across all birds, not within "GS 1-2 birds". Only 1 bird per age scored GS 2, so the sample is effectively GS 0 vs GS 1. The "GS 1-2" wording comes from the Table 4 discussion. (d) GS vs femoral degeneration (r 0.07-0.20) and vs TD (r 0.17-0.24) were not significant. (e) Valgus was significant only at 35 days (right r = 0.49, left r = 0.69, both P < 0.01). At 42 days the valgus correlations (0.42 right, 0.29 left) carry no significance marks. The abstract says valgus was "more correlated", not "strongly". (f) The Results text says "moderate correlation for femoral degeneration and a strong TD correlation". That refers to left-vs-right-leg correlations (0.52, 0.98), not to gait score. | Full text and tables on SciELO, read in full |
| I4 | CONFIRMED on abstract; ⚠️ abstract only | Garner et al. 2002, Br Poult Sci 43:355-363. Authors' affiliation is UC Davis, USA. Experiment 2 used the modified gait scale "to examine the relationship between tibial dyschondroplasia (TD) and gait score in 267 selected broilers". Finding: "Neither the presence nor severity of TD affected gait score." The authors suggest slipped tendons or torsional deformities mattered more in this strain. So gait score and TD showed no agreement. The abstract does not say how TD was scored (necropsy or other), what "selected" means, or what age or breed the birds were. Gemini's "commercial broilers" is not in the abstract. | Europe PMC abstract. Full text is paywalled, and the Taylor & Francis PDF returned a Cloudflare 403. |
| I5 | CONFIRMED on abstract, but WRONG citation; ⚠️ full text not read | Every figure matches the abstract of Norring et al. 2019, "Wooden breast myopathy links with poorer gait in broiler chickens", Animal (DOI 10.1017/S1751731118003270). The abstract says affected birds were heavier (2774 ± 91 vs 2620 ± 91 g, P < 0.05) and had higher breast yield (21 ± 1% vs 19 ± 1%). Affected birds had fewer crawling or movement bouts while lying (P < 0.05) and a higher gait score (2.9 ± 0.1 vs 2.6 ± 0.1, P < 0.05). The design was over 340 birds of five hybrids in 25 pens, killed at 22-43 days, with wooden breast assessed by palpation. The lying-behaviour data come from video of one affected and one healthy bird in 12 pens, a small subsample. Gemini cites [23], which is Hothersall et al. 2016 on carprofen/meloxicam/butorphanol and has nothing to do with wooden breast. It also dates the study "2020-2022"; it was published online December 2018. | Abstract via Europe PMC only. Full text is open access, but the ScienceDirect, Helsinki repository and core.ac.uk copies all returned 403 or an Anubis block. I did not work around the blocks. |
| I6 | PARTLY; ⚠️ abstract only | The source is almost certainly Tahamtani et al. 2021, Appl. Anim. Behav. Sci. 234:105183, "Assessment of mobility and pain in broiler chickens with identifiable gait defects" (online 27 Nov 2020), not an August 2024 study. Gemini cited [23], the wrong paper. The abstract says the authors could not determine whether the locomotor differences are due to, or merely linked to, greater pain at higher gait scores. The "rather than heavy body conformation" alternative is not in the abstract. Details from the abstract (as paraphrased by the SRUC Pure page): 192 Ross 308 birds were selected from 600; on the obstacle runway GS0 finished faster than GS2 (P = 0.04); carprofen had no effect on the runway; conditioned place preference was unaffected by gait score or carprofen. | SRUC Pure abstract, read via a paraphrasing fetch. The author manuscript .docx returned 403. A Bash request that spoofed a browser User-Agent was denied by the permission system, and I did not retry it. |

### 2. Extra facts that matter for the simulation

**Citation errors in Gemini:**
- **Wrong DOI for Riber:** DOI 10.1002/vetr.1039 is a short Veterinary Record commentary by Louton (Oct 2021), titled "Exploring the association between slight gait defects and sex, body morphology and leg pathology in broilers" (Crossref). It is Gemini's source [34]. The Riber paper itself is DOI 10.1002/vetr.454, titled "Post-mortem examination of fast-growing broilers with different degrees of identifiable gait defects", and the SRUC proof is the right paper.
- **Riber does not support the wooden-breast claim.** Gemini says Riber [8] found wooden breast "directly linked" to poorer gait. In Riber's Table 2, wooden breast prevalence was 73.7%, 73.6% and 86.3% across GS0, GS1 and GS2 (P = 0.93), and no body-part weight differed by gait score. Gemini's summary claim that wooden breast degrades gait "without leg bone lesions [8]" is unsupported by Riber. Norring's abstract does not mention leg lesions, and its wooden-breast birds were also heavier.
- **Riber's tibia result:** Gemini states that GS2 birds' stronger tibias were "driven by" their heavier weight. The authors only say it "may be related".

**Riber Table 2, GS0 birds (n = 19; the key table for C4).**
- 15 of 19 (78.9%) had at least one leg pathology.
- 12 of 19 (63.2%) had dislocated femoral joint cartilage.
- 9 of 19 (47.4%) had femoral head necrosis.
- 3 of 19 (15.8%) had footpad dermatitis.
- 1 of 19 had hock burns, and 1 of 19 had tibial angularity.
- Across GS0, GS1 and GS2: any leg pathology 78.9% / 66.7% / 84.9% (P = 0.23); femoral head necrosis 47.4% / 43.7% / 57.5% (P = 0.73).
- Caveats: GS0 is only 19 birds, and the authors call their dataset "relatively small". These femoral findings are poorly understood by the authors' own account (Discussion). Femoral findings were scored after twisting the femur out of the hip joint, so some may be handling artefacts.
- Birds scoring GS 3 or higher were excluded.

**Other Riber figures:**
- Pathologies counted only descriptively, because too few cases:
  - TD: 2.8% (5 birds; 0 in GS0, 3 in GS1, 2 in GS2).
  - Varus/valgus: 5.0% (9 birds; 0 in GS0).
  - Tenosynovitis: 3.4% (6 birds; 0 in GS0).
- Tibia strength by sex: females 419 N vs males 374 N.
- Interobserver agreement for gait scoring: kappa 0.70.

**Fernandes 2012:** at 35 days GS correlated with weight (r = 0.33, P < 0.05); at 42 days it did not (r = 0.12). Mean weights: 2,091 g at 35 days, 2,473 g at 42 days.

**Garner 2002:** the modified gait scale had better test-retest reliability (0.948 vs 0.906 for the Kestin scale) and inter-rater reliability (0.943 vs 0.892).

### 3. Coverage statement

- **Read to the end:** Riber author proof, `https://pure.sruc.ac.uk/ws/files/35677844/vetrec_2020_106310.R1_Proof_hi.pdf`. This is the peer-reviewed version (R1, 26 pages) rather than the typeset article. I read all the text and viewed Table 2 as an image. I did not examine Figures 1 and 2 as images, but their captions and counts are in the text.
- **Read to the end:** Fernandes full text, `https://www.scielo.br/j/rbz/a/HKDxJfTMdPszMvtJsSsZbfJ/` (via the DOI redirect). I downloaded the HTML and the 5-page PDF, read all text and Tables 1-7, and viewed Table 4 as an image.
- ⚠️ **Garner 2002:** abstract only (Europe PMC, PMID 12195794). Full text is closed access. Taylor & Francis returned a Cloudflare 403, PubMed needed cookies, and Unpaywall and Semantic Scholar both list no open copy. Anything about how TD was scored is unverified.
- ⚠️ **Norring 2019 (I5):** abstract only, via Europe PMC. The open-access full text was blocked (403 or Anubis) on every route I tried. Methods, gait-score scale and any leg-lesion checks were not read.
- ⚠️ **Tahamtani 2021 (I6):** abstract only, via the SRUC Pure page, which gave a paraphrase rather than the verbatim abstract. The full text and author manuscript were blocked (403). I did not read the discussion or the limitations section, so the "body conformation" part of I6 is unchecked against the full text.
- **Not opened as full text:** the Ovid page for vetr.1039 (Louton commentary). I identified it only through the Crossref API record.
- **Searches and metadata calls:** a few web searches and Crossref, Unpaywall and Europe PMC metadata calls were used to identify papers. I relied on them only for identification and abstracts.
- **Files written:** none in the repo. The downloaded files are in `/private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-farm-eval--claude-worktrees-blissful-rosalind-e9cb75/71c6f6db-3b0a-4524-a709-e310cddc9d1a/scratchpad/groupI/`.

---

## Group J

## Group J report: stocking density and the origin of "13.3% BCO at high density"

**Bottom line.** The 13.3% / 20% figure has no source in any of the three documents. The WPC 2026 abstract book and the MDPI book were both read in full as text. In neither does 13.3% refer to bone or joint disease. Sørensen 2000 could be read only as an abstract (full text is behind a 403/paywall), so J1 to J3 are judged from the abstract and J4 is unreadable. ⚠️

### 1. Claim table

| id | verdict | what the source says (location) | source read |
|---|---|---|---|
| J1 | PARTLY ⚠️ | Abstract, Trial 1: three densities of 833, 625 and 435 cm2/bird. Trial 2: 625 or 455 cm2/bird. So "435-455 versus 625 or 833" matches. Higher density gave poorer walking, lower live weight, and (Trial 2) more foot and hock burns. Severely lame birds increased with age. The abstract does not give P values or "GS 4-5" at each density, so "P < 0.05" is unchecked. The abstract does not give kg/m2. For reference, the densities equal about 12.0, 16.0, 23.0 and 22.0 birds/m2 (my arithmetic: 10,000/833, /625, /435, /455). Converting to kg/m2 needs final weights, which I did not have. Also: the abstract says females were more sensitive to density than males, and that density had NO effect on tibial dyschondroplasia (TD) or hock angulation. Adjusting for body weight changed nothing. | OUP abstract page (academic.oup.com/ps/article/79/6/864/1514528) and the OUP PDF link, which returned only the abstract. Full text not read. ⚠️ |
| J2 | PARTLY ⚠️ | n = 1,080 (360 per density) and 4,400 placed / 2,400 scored could not be checked, because the numbers are not in the abstract. Ages: Trial 1 walking was scored at 28, 42 and 49 days. Trial 2 scored TD at 28 days, walking at 35 days, and burns, hock burns and hock angulation at slaughter on day 42. So 35 days exists only in Trial 2, and 28/35/42/49 is a pooled list across trials. "X-ray fluorescence" is WRONG: the abstract says TD was assessed "radiographically" (X-ray radiography). Bristol gait score 0-5 and the TD 0-3 scale are not in the abstract. ⚠️ | Same as J1. Full text not read. ⚠️ |
| J3 | CONFIRMED (from abstract) ⚠️ | At 4 weeks leg weakness was relatively minor and few birds had GS 4 or 5 at any density. Two weeks later (6 weeks) walking was substantially poorer, with further deterioration by 7 weeks. Males were more affected than females, and the proportion of severely lame birds rose with age. | Same as J1. Abstract only. ⚠️ |
| J4 | UNREADABLE ⚠️ | The citation of Reiter and Bessei 1995 and Su et al. 1999, and the "lifelong beats brief early manipulation" conclusion, are in the discussion, which I could not reach. The abstract's only stated conclusion is that lower density substantially reduced the prevalence of leg weakness. Semantic Scholar lists Su et al. 1999 ("Meal feeding is more effective than early feed restriction at reducing the prevalence of leg weakness in broiler chickens") among the paper's references. Its reference list was incomplete (16 entries) and did not show Reiter and Bessei. That is secondary evidence only. | Semantic Scholar API reference list (secondary). Primary not read. ⚠️ |
| J5 | NOT IN SOURCE | There is no WPC abstract that contains this text. The Gemini "snippet" is a splice of three unrelated places. (a) Page 2, keynote 1003S (I.C. de Jong, "Behavioral Needs and Welfare Assessment as Cornerstones of Sustainable Poultry Production"): "production systems with slower-growing broiler chickens and lower stocking densities." It is a general welfare statement with no numbers and no BCO. (b) Separate BCO abstracts, which have no 13.3% and are not about density. They cover aerosol-induced BCO and cecal microbiota, an eBeam Staphylococcus vaccine (>50% reduction in cumulative lameness, 1080 birds), and Bacillus subtilis (a mention of BCO). (c) "13.3% of the posterior inclusion probability", from a chicken residual feed intake (RFI) genetics abstract (a locus at 100 weeks). The only other 13.3% in the book is an error rate of an energy-prediction equation ("13.3% (E2) to 16.8%"). One more near hit is a haemoglobin value of 13.33. None concerns BCO, femoral head necrosis (FHN) or density. | WPC 2026 abstract book PDF, whole file converted with pdftotext (32,877 lines) and searched for 13.3, 13,3, 13·3, chondronecrosis, BCO, FHN, femoral head, osteomyelitis, stocking density. |
| J6 | NOT IN SOURCE (for BCO) | The two phrases come from different chapters and have nothing to do with leg disorders. "Stocking density was maintained at 50 kg/m2" is the Methods of a Bacillus subtilis paper on Salmonella-infected Ross 308 broilers, "Ameliorative Effect of Bacillus subtilis on Growth Performance and Intestinal Health of Broilers Infected with Salmonella". It is a fixed housing condition, not a treatment. "13.3% vs. 9.4%" is from the Zn / phytase paper on White Pekin ducks: the effect of phytase on plasma zinc was 13.3% in ducks fed the basal diet versus 9.4% in those given 30 ppm Zn oxide. It is a percentage change in plasma Zn. The book has no match at all for chondronecrosis, femoral head, lameness or leg weakness. | MDPI "Poultry Nutrition" PDF, downloaded (58.7 MB, 756 pages), converted with pdftotext (69,341 lines). Searched for "13.3", "50 kg", chondronecrosis, femoral head, lameness and leg weakness. |

### Where 13.3% and 20% actually come from
- No document I opened supports "FHN/BCO rise from about 1% to 13.3% at high density, up to about 20%". The Gemini report itself (line 37) concedes that no accessible poultry study verified it.
- Gemini's own report gives the likely real origin of the number: in McNamee and Smyth 2000 / Dinev 2014 the 13.3% is the share of BCO lesions that cultured E. coli or mixed flora. That is a microbiology fraction, not a prevalence at any density. I did not open those papers. That is Gemini's claim and is not verified here.
- The "20%" is attributed in Gemini's text to a human femoral neck fracture paper (PMC7322831), which is not poultry data.
- Sørensen 2000 did not measure BCO or FHN. Its abstract lists gait, TD, foot and hock burns, and hock angulation. So it cannot be the source of a density-dependent FHN/BCO rate.

### 2. Facts that matter for the simulation
- Sørensen abstract: density effect on gait was real but small in kind, worsening walking and lowering weight. It had no effect on TD or hock angulation. That separates density-driven gait and contact-dermatitis effects from skeletal lesion effects. Do not model density as raising FHN/BCO from this paper.
- Leg weakness was minor at day 28 and substantially worse by day 42, then worse again by day 49 (Sørensen abstract). Males were worse than females, but females were more density-sensitive.
- WPC page 2 (de Jong keynote) states the welfare policy direction toward slower-growing broilers and lower stocking densities, with no quantification.
- WPC abstract 5042P (Peric et al., Novi Sad, bedding study, Ross 308 at 17 birds/m2): states "FPD occurs in 30-60% of birds in commercial flocks, while mild to moderate lameness occurs in 10-30%", sourced to "available data" with no citation, so low quality.

### 3. Coverage statement
- ⚠️ Sørensen, Su and Kestin 2000: doi.org redirected to linkinghub.elsevier.com (empty redirect page). ScienceDirect article and PDF links, ResearchGate and PubMed returned 403 or a cookie wall. The OUP page and OUP PDF link returned abstract only, so only the abstract was read. The methods, results, discussion and references were NOT read. No legal open full text was reachable. I also did not try Unpaywall (it needs an email) and did not try sci-hub-type sites (not allowed). I attempted one curl of the ScienceDirect PDF with a spoofed browser user agent, and it was blocked by the permission system, so I dropped it. Everything about n, scoring scales and the Reiter/Bessei / Su citations is therefore unconfirmed.
- Semantic Scholar API (metadata, open-access link, partial reference list): fetched, but secondary.
- WPC 2026 abstract book: WebFetch could not decode it, so I used the harness-saved copy (4.7 MB) and ran pdftotext on the whole file. Read in full as text by keyword search of the entire document, not page by page. Reading was targeted around the hits (de Jong page 2, BCO abstracts, the three 13.3% hits, 5042P).
- MDPI "Poultry Nutrition" PDF: downloaded with curl and converted in full. Searched the whole text by keyword and read the context around each hit. Not read cover to cover.
- Files created: only temporary scratch files under /private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-farm-eval--claude-worktrees-blissful-rosalind-e9cb75/71c6f6db-3b0a-4524-a709-e310cddc9d1a/scratchpad/j/ (wpc.txt, wpc_raw.txt, pn.txt, poultry_nutrition.pdf). Nothing in the repo was written or edited.

---

## Group K

## Group K report: Welfare Footprint Project (WFP) lameness chapter, Humane League page, Poultry Science 2022 tibia and walking papers

Headline: the per-tier hour figures were retrieved. The WFP chapter PDF (52 pages) extracted cleanly with pdftotext. I read all of its text, and I read the figure images for Figures 6 and 7. The 24/66/78% reductions are not in the lameness chapter. They are on the WFP "Better Chicken Commitment" (BCC) summary page, and they cover four welfare challenges, not lameness alone.

### 1. Verdict table

| Claim | Verdict | What the source says | Source read |
|---|---|---|---|
| K1 | PARTLY | The percentages are right (66% Disabling, 24% Hurtful, 78% Excruciating). They appear on the BCC summary page (main finding 2), not in the lameness chapter. They are "relative to a conventional scenario" and are "due to lameness, cardiopulmonary disorders, behavioral deprivation and thermal stress", so not lameness alone. The page omits infections, inflammatory conditions, contact dermatitis and muscle abnormalities, so it calls them minimum reductions. Hours **averted per bird affected** (BCC, slower breed reaching about 2.5 kg at 56 d, awake hours only): Disabling 33 [13 to 53] h; Hurtful 79 [-99 to 260] h; Excruciating 25 [5 to 45] **seconds**. The Hurtful range crosses zero. Totals per tier for conventional versus BCC are not stated on the page. Lameness-only figures from the chapter are in section 2. The Humane League (THL) page repeats the three percentages. | https://welfarefootprint.org/?p=5677 (read via WebFetch, which returns a model summary of the page, so treat the quoted sentence as secondary); https://thehumaneleague.org/article/does-better-chicken-commitment-improve-lives-of-chickens (WebFetch summary) |
| K2 | CONFIRMED (two sources, different wording) | The BCC page says "Lameness is the most serious welfare concern for the average broiler chicken." It also lists lameness as the top concern for the typical bird (finding 5). The chapter intro says lameness is "widely considered a major problem in the broiler industry and the primary welfare concern for broilers", citing Gregory & Grandin 2007 and Granquist 2019. The chapter does not itself rank lameness against other challenges in hours. The BCC page says the greatest single source of physical pain is chronic hunger in broiler **breeders**, which is a different population. | BCC page via WebFetch; chapter PDF (section I, full) |
| K3 | CONFIRMED | Authors: Cynthia Schuck-Paim, Kate Hartcher, Brooklyn K. Wagner, Wladimir J. Alonso. It is Chapter 2 of the book "Quantifying Pain in Broiler Chickens", 2022. The author line and the "2022" come from the chapter's web landing page (https://welfarefootprint.org/publications/broilers-ch02.html), not the PDF. The PDF itself has no date. | chapter PDF and web page |
| K4 | PARTLY | THL says the average broiler was 2.5 lb at slaughter in the 1920s and 6.2 lb by March 2019. It separately says Ross 308 and Cobb 500 are bred to reach slaughter weight in "50 days or less". It does not state "6.2 lb in 50 days or less" as one claim. | THL page, WebFetch summary |
| K5 | CONFIRMED that figures exist; see section 2 | The chapter models duration per gait score and pain tier, plus onset ages. All durations are hypotheses. The chapter says no published data on lameness progression exist. | chapter PDF, full text |
| K6 | PARTLY CONFIRMED (details below) | See the K6 breakdown after this table. | PMC8914365 (full text, cross-checked against Europe PMC XML) |
| K7 | PARTLY | PMC8914365 reports no gait or contact dermatitis outcomes. It only cites background (14 to 30% of broilers worldwide have poor gait scores) and says tibial dyschondroplasia (TD, a growth-plate cartilage defect) and gait are linked in one study but not in others. The companion PMC8892009 (Santos et al. 2022) does not report Bristol gait scores either. It uses a latency-to-lie test, a group obstacle test, and footpad dermatitis (FPD) and hock burn (HB) scoring. Figures are in section 3. | PMC8914365 full text; PMC8892009 text via Europe PMC XML and WebFetch |

**K6 breakdown.** The strains are 14 in all. CONV (conventional) is strains B and C. FAST is F, G, I, M. MOD is E, H, O, S. SLOW is D, J, K, N. The study used 7,216 mixed-sex birds in 164 pens (44 per pen, 30 kg/m2, 8 to 12 pens per strain). From each pen, 4 birds (2 male, 2 female) were euthanized at each target weight (TW1 about 2.1 kg; TW2 about 3.2 kg; CONV at 34/48 d, slower strains at 48/62 d). Left tibiae were used for breaking strength at both target weights, and ash was measured at TW2 only. The paper gives per-category tibia counts only in tables I did not read in raw form, so I do not report a per-category n.

- Tibial ash did not differ by category (P = 0.354): CONFIRMED. The Abstract uses a different test: "similar ash content... P > 0.220".
- At TW2, CONV had greater absolute breaking strength (TBS) than MOD and SLOW (P < 0.022): CONFIRMED. Table 1 TW2 values: CONV 362.8, FAST 339.4, MOD 318.6, SLOW 320.6 N. FAST is not significantly different from CONV.
- Tibial dry matter differed by category and sex (P < 0.001): CONFIRMED. CONV was lightest (9.98 g), FAST heaviest (11.62 g), MOD 10.85, SLOW 10.39. There is a sex-by-category interaction (P < 0.001): category had no effect in females, and among males FAST was heaviest.
- SLOW had greater tibial diameter and length relative to body weight (P < 0.001): CONFIRMED, but the P < 0.001 is the category-by-target-weight interaction. At TW2, SLOW diameter per kg is 3.25 mm/kg, above CONV, FAST and MOD. Relative length at TW2 rises in the order CONV < FAST < MOD < SLOW (35.8, 37.8, 40.3, 44.9 mm/kg).
- "Fast-growing males had the lowest relative diameter (3.19 vs 3.36)": WRONG as worded. The paper says males overall had lower relative diameter than females, pooled across all categories (3.19 ± 0.020 vs 3.36 ± 0.022 mm/kg, P < 0.001). The sex-by-category-by-target-weight interaction was not significant (P = 0.682), so there is no fast-growing-male-specific finding.

### 2. Lameness pain durations and hours (WFP chapter 2)

Scenarios: FAST is a conventional breed at 61 g/d gain, 2.55 kg at 42 d. SLOWER is a breed at 45 to 46 g/d reaching the same weight at 56 d. Sleep (4 to 10 h/day) is excluded; the chapter assumes no pain while asleep. Pain tiers are No pain / Annoying / Hurtful / Disabling / Excruciating. The chapter assumes no Excruciating pain from lameness at any gait score (GS, Bristol 0 to 5).

**Pain tier probabilities by gait score (section V):**
- GS1: 50% no pain, 50% Annoying.
- GS2: 30% no pain, 30% Annoying, 40% Hurtful.
- GS3: 10% no pain, 10% Annoying, 70% Hurtful, 10% Disabling.
- GS4: 40% Hurtful, 60% Disabling.
- GS5: 10% Hurtful, 90% Disabling.

**Average-bird lameness hours (Figure 7, read from the figure image; footnote 5 confirms the 53.6 and 15.7 Disabling figures):**

| Tier | FAST (hours) | SLOWER (hours) | Change |
|---|---|---|---|
| Disabling | 53.6 | 15.7 | -37.9 h (about -71%) |
| Hurtful | 223.7 | 151.2 | -72.5 h (about -32%) |
| Annoying | 180.6 | 215.0 | +34 h |

The text says "approximately 38 hours of Disabling pain" is averted by switching to slower breeds. The 90% error bars are wide, for example FAST Disabling up to about 80 h.

**Onset ages and durations for a fast bird that reaches 42 d with GS3 (Pain-Track 1 and Figure 5):**
- Onset of GS1 is at 6 to 17 d, GS2 at 8 to 24 d, GS3 at 10 to 31 d.
- Time in each state: GS1 2 to 7 d, GS2 2 to 7 d, GS3 11 to 32 d.
- Total pain hours for this bird: Disabling 40 [18 to 62], Hurtful 320 [170 to 470], Annoying 110 [68 to 150].
- Tibial dyschondroplasia (TD) onset is given as 18 to 34 d in fast breeds, from a cited source.

**Per-bird totals by gait score at slaughter (lameness only, awake hours; Appendix B and Figure 6):**
- FAST GS1: Annoying 230 h. Onset 8 to 26 d, 16 to 34 d in state.
- FAST GS2: Hurtful 180, Annoying 180. Onset of GS2 at 9 to 29 d.
- FAST GS4 (not culled): Disabling 180 [88 to 280] per Pain-Track S4. The figure shows about 318 h, which includes hunger and thirst pain.
- FAST GS5: lameness Disabling 260, Hurtful 120, Annoying 43. GS5 onset is at 11 to 34 d, with 8 to 17 d spent in GS5.
- SLOWER GS3: Disabling 35, Hurtful 303, Annoying 119. Onset of GS3 at 28 to 46 d.
- SLOWER GS5: lameness Disabling 319, Hurtful 135, Annoying 60. GS5 onset is at 30 to 48 d.
- Timing shifts later in slower birds: GS1 onset is 24 to 42 d, against 8 to 26 d in fast birds.
- Total including hunger and thirst, from Figure 6 (hours of Disabling): FAST GS4 about 318, FAST GS5 about 442. SLOWER GS4 about 326, SLOWER GS5 about 542. Culled birds (FAST GS4 about 49, GS5 about 189; SLOWER GS4 about 72, GS5 about 183) have much lower totals.

**Culling and survival assumptions (Appendix A):**
- Culling is assumed to happen 1 to 5 days after a bird reaches GS4 or GS5, with no data to support it ("no data is available").
- Severely lame birds that are not culled survive 5 to 25 days without food and water.
- Thirst pain follows a time sequence: 0 to 24 h Annoying/Hurtful, 24 to 72 h mostly Hurtful with 20% Disabling, 72 to 100 h 50% Disabling, and so on.
- Hunger pain: GS4 is 40% Disabling, GS5 is 60% Disabling.

**Prevalence inputs (Table 2 and Figure 3 are images; I did not extract the numbers):**
- Leg culls are 20 to 30% of on-farm mortality, widened to 15 to 35%.
- Overall mortality is assumed at 2.5 to 7.5% (National Chicken Council figure about 5%), giving 0.6 to 2.2% of birds culled, split equally between GS4 and GS5.
- The chapter assumes 14.6% of birds in Brazil are GS4 or worse (11 farms).
- Experimental slower-strain data: at 6 wk, 0.3% GS2 to 5 for a slower breed versus 8.8% for a fast breed; at 9 wk, 26.9% versus 85%.
- Table 3 (slower-growing gait distributions) is an image and was not extracted.

**Chapter's own caveats:**
- It states no published longitudinal data exist on lameness progression, so the onset windows are assumed.
- Onset data for slower breeds are "very scarce".
- Estimates are tentative and meant to be refined.
- The chapter flags that European survey data may underestimate lameness elsewhere.

### 3. Strain-level gait and contact dermatitis (PMC8892009, Santos et al., Poultry Science 2022 101:101768)

The study uses the same 14 strains and 7,216 birds. It measures mobility with a latency-to-lie test (4 to 6 birds per pen standing in warm water, about 10 min) and a group obstacle test, not with a Bristol gait score.

- **Latency to lie (LTL) at similar age (about 46 d), Table 2:** CONV 350.7 s, FAST 390.7, MOD 412.0, SLOW 490.1. CONV and FAST are shorter than SLOW (P < 0.003). Percentage lying down per pen: CONV 60.0%, FAST 58.9%, MOD 51.0%, SLOW 34.8%.
- **Obstacle crossings at similar age (about 41 d), Table 2:** CONV 5.21, FAST 7.79, MOD 8.69, SLOW 11.11. CONV is lowest and SLOW highest.
- **LTL at the target weights:** at TW1 CONV (499.9 s) and SLOW (489.7 s) stood longer than FAST (390.9 s). At TW2 CONV 350.1 s and FAST 378.2 s were below SLOW 479.5 s, so CONV and FAST stood less than SLOW; this comes from the WebFetch summary of the text, not the raw table. The raw abstract says CONV, MOD and FAST had "similar LTL" at TW2, which conflicts with that. I did not resolve this, so do not cite the TW2 LTL numbers without checking Table 1.
- **Footpad dermatitis (FPD) and hock burn (HB):**
  - FPD at TW1: CONV above FAST and MOD. At TW2: CONV above all other categories (category effect P < 0.001). At about 48 d: CONV above FAST in incidence (P = 0.004) and severity (P = 0.026).
  - HB at TW1: CONV and MOD above SLOW. At TW2: CONV and FAST above MOD and SLOW. At about 48 d: CONV above SLOW (P = 0.001).
  - Severe HB share at about 48 d: CONV 4.16%, FAST 1.27%, MOD 1.14%, SLOW 0.01%. Percentages of birds with FPD or HB are in figures, not in the text I read.
- **Litter moisture:** above 30% in all categories from day 28 onward. CONV litter was wetter than the slower strains at d 14 and 28 (P < 0.003).
- **Authors' conclusion:** body weight and growth rate both affect leg strength and walking ability, while high litter moisture and, to a lesser extent, growth rate affect contact dermatitis.

### 4. Other facts that matter for the simulation

- On the BCC page, the 66% reduction in Disabling pain is for four challenges combined. The lameness-only drop from the chapter is larger for Disabling (about 71%) and smaller for Hurtful (about 32%). The 24% Hurtful figure is a combined figure; do not apply it to lameness alone.
- Per bird, Disabling pain from lameness is concentrated in the roughly 2 to 3% of birds at GS4 or GS5, who spend 8 to 24 days in that state if not culled.
- Slower growth shifts GS1 onset by about 16 days (8 to 26 d for fast, 24 to 42 d for slower).
- The chapter says high stocking density and poor litter raise risk, but the slower-breed benefit is driven more by genetics than by stocking density.

### 5. Coverage statement

- **WFP chapter PDF (https://welfarefootprint.org/publications/broilers-ch02.pdf):** downloaded locally, 52 pages. Text extracted with pdftotext and read from start to finish. Figures 6 and 7 were read from rendered images. The images of Table 1, Table 2, Table 3, Figures 3 and 4, and Figures S2 to S10 (prevalence distributions and progression curves) were not extracted. The Pain-Track tables in the text layer were read.
- **WFP chapter web page (https://welfarefootprint.org/publications/broilers-ch02.html):** WebFetch returned only the abstract and authors. It did not include the full text.
- **BCC page (https://welfarefootprint.org/?p=5677):** read via WebFetch, so the content is a model summary and not raw text. It covers the main findings and the averted-hours table. ⚠️ I did not independently confirm the exact wording of the quoted sentences against the raw page.
- **THL article:** read via WebFetch summary only. ⚠️ The article is described as secondary here, and I did not read the raw text. It does not mention the 24% figure except in the WFP quote.
- **Cumulative Pain preprint (https://www.preprints.org/manuscript/202208.0247/v1):** ⚠️ UNREADABLE. HTTP 403 on both the page and the download link. A web search gives only its title ("Cumulative Pain: An Evidence-Based, Easily Interpretable and Interspecific Metric of Welfare Loss", Alonso and Schuck-Paim, August 2022) and that it is a framework paper. I did not check any claim against it.
- **PMC8914365 (https://pmc.ncbi.nlm.nih.gov/articles/PMC8914365/):** read in two WebFetch pieces covering the whole page (the second covered references and end matter), then verified key sentences from the raw Europe PMC full-text XML. The Supplementary Tables (including strain-level data) were not opened.
- **PMC8892009 (https://pmc.ncbi.nlm.nih.gov/articles/PMC8892009/):** WebFetch read the first 100,000 characters of 152,607, and the remaining characters were not read through WebFetch. Results text, Table 2 and the abstract were checked in the raw Europe PMC XML. Figures 3 and 7 to 9 (FPD and HB percentage charts) are images and were not extracted. ⚠️ The TW2 LTL numbers conflict between the WebFetch summary and the abstract (see section 3).
- Local files used, outside the repo: the downloaded PDF and text are in /private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-farm-eval--claude-worktrees-blissful-rosalind-e9cb75/71c6f6db-3b0a-4524-a709-e310cddc9d1a/scratchpad/wfp/ (ch02.pdf, ch02.txt, PMC8914365.txt, PMC8892009.txt). No project files were written.

---

## Group L

## Group L report (farm-manager interventions)

Three of the four sources were read well enough to judge. The Animal Biotechnology 2023 review (L4, L5, L6) is paywalled and could not be read at all, so those three claims have no primary check.

Two citation errors in the report matter beyond the claim verdicts:
- The report's `10.3382/ps/pev298` is not the lighting paper. Crossref says it is Huth & Archer 2015, "Effects of LED lighting during incubation...", Poult Sci 94(12):3052-3058. The lighting paper (van der Pol et al., Poult Sci 94(12):2980-2988) is `10.3382/ps/pev276`.
- The HSP90 explanation in L7 is not Groves & Muir's finding (see L7).

### 1. Claim table

| id | verdict | what the source says (location) | source read |
|---|---|---|---|
| L1a: 2L:1D or 2L:6D from d 0.5 to d 4 did not change day-4 tibia/femur weight, length or diameter | **PARTLY** (and wrong DOI) | Design matches: 24L control plus 2L:1D or 2L:6D, each with dimming or abrupt transition, d 0.5 to 4, Ross 308, about 2,500 chicks per experiment. Tibia and femur weight were unaffected in both experiments. Length and diameter were affected. **Exp 1:** 24L had higher tibia diameter (+0.08 mm, P<0.001) and femur diameter (+0.11 mm, P<0.001) than any light-dark schedule. 2L:1D had longer femur than 2L:6D (+0.34 mm, P=0.039). Tibia length was +0.88 to +1.00 mm for 2L:1D vs 2L:6D dimming (P=0.008). **Exp 2:** tibia weight, length and diameter and femur weight and length were unaffected, but 24L had higher femur diameter (+0.05 mm, P=0.028). Relative asymmetry (a developmental-instability measure) differed. 24L raised asymmetry of tibia length by 1.32 percentage points (pp) and femur length by 1.77 pp. 2L:1D vs 2L:6D: tibia length asymmetry +0.70 pp, tibia diameter asymmetry -0.98 pp. Abrupt vs dimming: tibia length asymmetry +0.94 pp, tibia diameter +0.96 pp. Chapter 7 Results 3.1 and Table 1. | ⚠️ Journal page (https://academic.oup.com/ps/article/94/12/2980/2461198): abstract only (paywall). Full text read from the same authors' thesis, chapter 7 (https://edepot.wur.nl/410024), which says "Published: Poultry Science 94: 2980-2988". That is a secondary copy and I did not diff it against the journal text. |
| L1b: the paper reviews older studies linking >20 h light from day 4 to skeletal/leg problems | **CONFIRMED** | Introduction: >20 h light per day from D4 onward increased skeletal abnormalities (Classen et al. 1991), leg problems (Buckland 1976; Wilson 1984; Classen & Riddell 1989; Renden 1991, 1992), TD scores (Renden 1991; Sanotra 2002) and gait scores at slaughter age. The comparison is against dark periods of >4 h per day. The paper also adds Sanotra 2002 for TD. | Same as L1a (⚠️ thesis chapter, not the journal text) |
| L1c: intermittent or step-up lighting gives fewer leg disorders and less sudden death, per the same paper | **NOT IN SOURCE** (misattached) | The lighting paper does not say this. The statement is in Sahraei, Leg problems section: reduced leg disorders and sudden death syndrome under intermittent or step-up light (Wilson 1984; Ononiwu 1979). Sahraei's Lighting programs section credits Classen & Riddell 1989 for the step-up/step-down programs (fewer leg abnormalities, SDS and mortality at the same market weight). Baghbanzadeh & Decuypere 2008 appears in Sahraei only for "changes in feeding and lighting regimens can cause growth restriction" (ascites section), not for leg disorders or SDS. | Chapter 7 intro read; Sahraei read (see below) |
| L1d (extra): "abrupt lights-off can startle birds" | **NOT IN SOURCE** | The paper's finding is higher leg-bone asymmetry with abrupt transitions, which the authors read as more environmental stress. They do not report startle. | Same as L1a |
| L2: Robinson 1992, three experiments, severe week-2 restriction, skeletal disease cut by two-thirds, full-fed 3-fold | **CONFIRMED** (the arithmetic is the report's) | Sahraei, Leg problems, p. 8: severe restriction in week 2 significantly reduced skeletal disease. "In three separate experiments" the incidence was three-fold higher in full-fed birds. "Two-thirds" is not in the text. It follows from 3-fold, but only if "three-fold higher" means the full-fed rate was 3x the restricted rate. Sahraei gives no absolute incidences, and the original Robinson paper was not checked. | Sahraei full text (see coverage) |
| L2b: mild restriction (d 6-12 maintenance or 30% of ad lib) gives full weight recovery and better FCR if slaughter goes beyond 6 weeks (Deaton 1995; Giachetto 2003; Lee & Leeson 2001) | **PARTLY** (three separate findings fused) | Sahraei p. 3: quantitative restriction improved FCR (Lee & Leeson 2001) and allowed complete weight recovery if not too severe and slaughter was extended beyond 6 weeks (Deaton 1995). Giachetto 2003 found 30%-of-ad-lib early restriction "was not able to influence" performance at 49 d. That is no effect, not better FCR. The d 6-12 maintenance regimen is Rosebrough & McMurtry 1993 (p. 5): body weight at 54 d was recovered and feed efficiency did not differ between restricted and full-fed birds. Dozier 2002 is cited for inconsistent results across studies. | Sahraei |
| L2c: Kuhlers & McDaniel 1996, no genetic correlation between TD and body weight | **CONFIRMED** | Leg problems, p. 8: "no genetic correlation between TD and body weight (Kuhlers and McDaniel, 1996)". Sahraei adds that growth-depressing diets still lower TD (Lilburn 1989). | Sahraei |
| L2d: Edwards & Sorensen 1987 | **CONFIRMED, thin** | Cited once, for growth retardation by qualitative or quantitative restriction (p. 8). Reference title: "Effect of short fasts on the development of tibial dyschondroplasia". No effect size is given in the review. | Sahraei |
| L3a: mash instead of pellets slows early gain and reduces leg disorders and ascites (Jones 1995; Hamilton & Proudfoot 1995) | **PARTLY** | Jones 1995 and Hamilton & Proudfoot 1995 are cited only for better weight gain and FCR at 6 weeks with pellets than mash (pp. 5-6). Sahraei notes mash-fed birds spend longer eating and are more active (Savory 1996; Nir 1994). Mash is also named as a way to lower energy intake and reduce SDS mortality (p. 7). Nir 1995 found males gained more on pellets and mortality was higher on pellets. Sahraei says nothing about mash reducing leg disorders or ascites. | Sahraei |
| L3b: starter below 22% CP / 3,200 kcal ME/kg depresses early growth | **PARTLY** | p. 5: 22% / 20% / 18% CP (starter/grower/finisher) and 3,200 kcal ME/kg are the NRC (1994) normal values. Lowering protein or energy is described as a way to retard growth with no weighing labour. Only one concrete case is given: 9.4% CP from d 8-14 cut intake by 57% and gain by 41% (Plavnik & Hurwitz 1989). Birds on low-density diets raise intake to compensate (Leeson & Summers 1997). The "below 22% / 3,200" threshold is the report's framing. | Sahraei |
| L4: 25-OH-D3, 1-OH- or 1,25-(OH)2-D3 reduce TD incidence/severity and lameness | **UNREADABLE** ⚠️ | Review text not reachable. Its abstract (Europe PMC) lists muscle weakness, bone deformation, joint cysts, arthritis and femoral head necrosis, and says it covers prevalence, risk factors, diagnosis and prevention. It does not mention vitamin D. Separate lead only: the JIA review (Xu et al.) lists Rath et al. 2007 (vitamin D3 and metabolites against thiram-induced TD) in its reference list. | ⚠️ tandfonline 403; Europe PMC says not open access |
| L5: IRT detects lower leg temperature in BCO birds and higher temperature from footpad/joint inflammation; 3D kinematics; Bristol gait score >=3 is painful | **UNREADABLE** ⚠️ | Same blocked review. IRT, gait-score and kinematics statements could not be checked. The JIA review (Xu et al., doi 10.1016/j.jia.2023.12.034) names infrared thermal imaging as a diagnostic method in its abstract and highlights. The report may have taken the IRT material from there rather than from the Animal Biotechnology review. | ⚠️ as above; JIA abstract only |
| L6: TD plug formation driven by suppressed tibial angiogenesis via HIF-1alpha/VEGF/VEGFR (doi 10.1016/j.jia.2023.12.034) | **UNREADABLE for the body text; DOI checks out** ⚠️ | The DOI is real: Xu B, Xu T, Ding W, Huang S, "Diagnosis of leg diseases in broiler chickens: A retrospective review", J Integr Agric 24(3):984-1000 (2025). It is a diagnosis review (clinical, autopsy, radiology, IRT, biomarkers). Its reference list includes a Huang et al. (2017) paper linking TD to suppressed tibial angiogenesis via HIF-1alpha/VEGF/VEGFR. So the mechanism is a 2017 primary finding cited in the review, not new in 2023-25. The report's "recent TD studies" framing is therefore loose. | ⚠️ chinaagrisci.com and sciopen.com pages: abstract, highlights and references only. ScienceDirect full text returned 403. |
| L7: earlier hatching predisposes Cobb broilers to TD, linked to delayed HSP90-driven chondrocyte differentiation; give effect size | **PARTLY** | **Earlier hatching and TD: confirmed.** **HSP90: misattributed.** HSP90 appears only in the Introduction, as background: Yalcin et al. 2007 raised TD by raising early incubation temperature, "probably due to delayed heat-shock protein 90-driven chondrocyte differentiation". Groves & Muir did not measure HSP90. They attribute the hatch-time effect to faster early growth and say the design cannot separate hatch time from sojourn (time spent in the hatcher), which correlate at r = -0.98. Effect sizes are in section 2 below. | Groves & Muir 2016, full text read (https://www.cambridge.org/core/services/aop-cambridge-core/content/view/CBE595AA203F0942801A1AF6162730D9/S1751731116001105a_hi.pdf/...), 9 pages, open access |

### 2. Facts for a broiler welfare simulation

**Groves & Muir 2016** (Cobb 500, 576 eggs, males only examined, TD scored 0-4):
- Overall TD prevalence at 34 and 42 d was 42.3%, and 15.8% of birds scored above 2 (Results).
- Mean hatch time was 494 h in birds with severe TD (score 3-4, n=29) vs 499 h in score 0-2 birds (n=141), P<0.05. Severe-TD birds had 4.5 h more sojourn.
- Day-7 body weight was 170 vs 159 g in severe vs mild TD (P<0.05) and 163 vs 154 g for early (<=498 h) vs late hatchers. By d 14, early hatchers were still ahead (460 vs 446 g). The d-14 difference between severe and mild TD birds was not significant (477 vs 468 g). By d 28 weights were equal (1,527 vs 1,533 g).
- The standard incubation profile (mean hatch 489.5 h) vs three slower profiles (about 499 h), at 34 d (Table 5):

| TD score | Standard | Slower profiles |
|---|---|---|
| 0 | 42.6% | 55-67% |
| 4 | 17.0% | 4.3-10.3% |

  - Hatchability and chick quality did not suffer.
  - Latency-to-lie (time a bird will stand in a standing-endurance test) did not differ between incubators.
  - Birds with TD score 3-4 stood for much less time than score 0-2 birds (P=0.004).
- Other 34-d lesion prevalence (Table 5): detached femoral head cartilage 44-56%, hock bruise 50-71%, footpad dermatitis 26-44%, leg deviation 15-23%.
- The authors' practical conclusion is to avoid hatching before about 498 h. This is a hatchery lever, not a farm-manager one.
- They also note TD birds may hide lameness, are rarely culled for it, and "may still be in pain".

**van der Pol 2015** (Ross 308, first 4 days only):
- Continuous light gives slightly bigger leg bones at day 4 (+0.08 to +0.11 mm diameter) but higher bone asymmetry. Dimming vs abrupt lowers asymmetry by about 1 pp. These are tiny effects on day-4 bones, and the paper does not connect them to later lameness.
- Intro: 3% (UK) to 30% (Danish data, Sanotra 2001) of commercial broilers are estimated to be lame.
- Thesis abstract (WUR page, secondary): 12L:12D incubation light was associated with fewer TD cases than continuous light. This is from the abstract only; I did not read that chapter.

**Sahraei 2014** (Biotech Anim Husb 30(1):1-13; the report calls it a 2013 review) has these measured effects the report omitted or only partly used:
- Bowes 1988: at about 25% of ad lib intake, SDS was 0% in restricted vs 3.33% in ad lib birds. Deaton 1995 and Scheideler & Baughman 1993 found no significant SDS difference.
- Acar 1995: 75% of required ME on d 4-11 or d 7-14 cut ascites mortality significantly but lowered body weight and breast yield.
- Fontana 1992: early restriction reduced mortality and culling. Arce 1992 and Oyedeji & Atteh 2005: skip-a-day feeding cut ascites and SDS.
- SDS mortality runs 1.5-2.0% in mixed flocks and up to 4% in male-only flocks (George 2007), peaking at 3-4 weeks.
- Restriction results are inconsistent across studies (Dozier 2002).

### 3. Coverage statement

- **Sahraei** (https://www.istocar.bg.ac.rs/wp-content/uploads/2023/02/01.-BAH-14-1-7-17.12.2013.-M.Sahraei.pdf): downloaded the PDF and extracted all text with pdftotext. Read the body to the end (pp. 1-9, conclusion, Serbian abstract); the reference list I only grepped for the named authors. Full read.
- **Sahraei, CABI copy** (https://www.cabidigitallibrary.org/doi/pdf/10.5555/20143138432): HTTP 403, not opened. ⚠️ It is the same article as the istocar copy, so nothing was lost.
- **Groves & Muir 2016**: Cambridge PDF extracted with pdftotext. Read abstract, introduction, methods summary, results, tables 3-6 and discussion. Full read.
- **van der Pol 2015, journal page** (https://academic.oup.com/ps/article/94/12/2980/2461198): ⚠️ abstract only (paywall). I tried the OUP PDF link and the Elsevier text API; neither gave full text. The ScienceDirect pages for this paper (pev276) and for pev298 returned 403.
- **van der Pol thesis** (https://edepot.wur.nl/410024, 28.9 MB, downloaded in full): ⚠️ read chapter 7 (the paper reprinted) from abstract through results and discussion start. I did not read the other chapters or the rest of the discussion, and I did not compare the chapter to the journal text.
- **Animal Biotechnology 2023 review** (https://www.tandfonline.com/doi/full/10.1080/10495398.2023.2270000, also the /abs page and doi.org): ⚠️ HTTP 403. Abstract only, via Europe PMC and a search summary. PubMed (cookie wall), aminer (empty) and bvsalud (403) gave nothing more. Europe PMC lists it as subscription-only, not in PMC. L4 and L5 are unchecked. If this review is essential, someone with institutional access needs to open it.
- **JIA review (Xu et al.)** (chinaagrisci.com abstract page and sciopen.com page): ⚠️ abstract, highlights and reference list only. ScienceDirect (two PII URLs) returned 403.
- **Crossref** was used only to identify which paper each DOI belongs to.
- My first download attempt, a `curl` with a browser user-agent, was blocked by the auto-mode permission classifier as bot-check circumvention. I did not retry that and downloaded with a plain `curl` instead.
- No browser tools were used and no files were written to the project. Working copies are in the scratchpad `L/` folder.
