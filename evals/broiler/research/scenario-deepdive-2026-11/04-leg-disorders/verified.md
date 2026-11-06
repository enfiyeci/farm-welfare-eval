Eval: broiler

# Leg disorders: the Gemini report, checked claim by claim

Written 2026-11-06. Input: `raw/2026-11-05-gemini.md` (Gemini Deep Research, "4 Argon", core prompt
from `prompts.md`). What changes in the scenario is in `adjudicated.md`; cite that, not this file or
`raw/`.

## How it was checked

Twelve Sonnet subagents each took one group of sources (A to L) and checked every Gemini claim that
rests on them. The brief: read the named source in full from the source itself, flag partial reads
with ⚠️, no browser tools, no pirate sites. Their unedited reports, each with a coverage statement,
are in `verifier-reports-raw.md`. Do not cite that file.

Their fetch tool (WebFetch) passes a page through a summarizing model, so even a "full read" through
it is not verbatim. Before any status changed in `claims.json`, I re-checked the figure against raw
text I downloaded myself (curl plus pdftotext, or the paper's table image). Those rows are marked
**raw-checked**. Everything else is the subagent's reading.

Many sources were paywalled or behind bot checks. Where only the abstract was read, the row says so
with ⚠️. An abstract-level confirmation counts as W (weak) in the inventory, never S or V.

## What the check found about the report itself

- **Citation numbers are partly wrong.** The `[n]` markers index Gemini's own "Sources used" list,
  and about 20 match their sentence. At least eight do not: Caplen 2013a is tagged [21] (a
  pharmacokinetics paper), Fodor 2025 is tagged [20] (Danbury's carprofen study), the multi-dose
  self-selection study is tagged [37] but is Siegel et al. 2011, and the wooden-breast figures are
  tagged [23] (Hothersall 2016) but come from Norring et al. 2019.
- **Wrong DOIs.** `10.1002/vetr.1039` is a short commentary by Louton; the Riber paper is
  `10.1002/vetr.454`. `10.3382/ps/pev298` is an incubation-lighting paper; the early-lighting paper
  (van der Pol 2015) is `10.3382/ps/pev276`.
- **Wrong authors.** The "Almeida Paz" SciELO paper is Alves et al. 2016; the "Liu 2022" probiotics
  review is Chen et al. 2022 (*Metabolites*); the "Guo 2020" PLOS ONE paper is Tang et al. 2020; the
  "Dinev 2014" review is Dinev 2012 (*J Poult Sci* 49:63).
- **Claims not in their source.** Six claims were checked as absent from the paper Gemini named (A8,
  A10, E6, J5, J6, L1c below). Several "full PDF accessed" notes in the report could not be
  confirmed.
- The report's honest parts held up: it said it could not find a source for "13.3% at high density"
  and could not open the Welfare Footprint PDF. Both were true.

## Part 1: the four prevalence claims in our memo

| ID | Gemini says | Verdict | What the source says | Read |
|---|---|---|---|---|
| A1 | 22% TD at 6 weeks (Shi 2024), falling at 8 and 10 weeks | Confirmed, **raw-checked** | 22%, 16%, 12% at 6, 8, 10 weeks, by digital X-ray, in 400 yellow-feathered broilers | Shi 2024 *Front Genet*, full text |
| A4 | Shi's birds were Chinese yellow-feathered cockerels | Confirmed, **raw-checked** | Methods: native Chinese yellow-feathered meat cockerels. Not Ross or Cobb. | Same |
| B1 | TD 27.7% Pureline, 26.5% Cobb 500, 24.22% Ross 308 | Confirmed, **raw-checked** | Dinev 2012 review, p. 65, citing "Dinev et al. unpublished" | Dinev 2012 *J Poult Sci* 49:63, full (5 pp). Primary (Dinev, Denev and Edens 2012, *JAPR*): ⚠️ abstract only |
| B2 | First TD lesions at about 24 days | Confirmed, **raw-checked** | "approximately 24 days" in modern hybrids; per-line means 19.6 to 28.8 days | Same |
| B3 | Necropsy, proximal tibia, Bulgaria; n not given | Partly | 20 flocks of about 17,000 birds; birds necropsied not stated | Same |
| C2 | Shim 2012: n = 585 fast, 581 slow | Confirmed | Abstract | ⚠️ Shim 2012 abstract only |
| C3, C4 | Shim 2012: TD 2.56% vs 1.03%; valgus 27.69 to 29.40% vs 18.93 to 19.97% at 4 weeks | Unreadable | The abstract gives mean lesion scores (valgus 0.40/0.38 vs 0.26/0.28; TD 0.06 vs 0.02), not prevalences. Gemini's percentages are consistent with those scores (implied mean grade about 1.4) but unverified. | ⚠️ abstract only; ScienceDirect shows a bot check |
| E1 | VVD 0.4% at 1 week, 5.4% at 5 weeks (Cruickshank and Sim 1986) | Confirmed as quoted, **raw-checked** | Tang 2020 and Chen 2022 both state it and cite Cruickshank and Sim 1986 | Tang 2020 and Chen 2022 full; primary ⚠️ abstract only |
| E2 | The 1986 study is Canadian | Not in source | None of the three modern papers says Canadian | Full texts |
| D2 | Leterrier and Nys 1992: varus 1 to 3%, onset days 5 to 20 | Partly | Varus 1 to 3%, but onset 5 to 15 days | ⚠️ abstract only |
| D4 | Severe valgus 0 to 5.5%, mild and intermediate 2 to 32% | Partly | Abstract: valgus in 30 to 40% of birds, severe in about 5% | ⚠️ abstract only |
| D3, D5 to D10 | Flock-level details (86% right leg, 25 of 33 bilateral, 33 to 47% TD co-occurrence, n = 33 and 21) | Unreadable | Not in the abstract. D6 is contradicted in part: tendon displacement in 60% of severe valgus. | ⚠️ abstract only |
| F1 | van den Brand 2022: 32.1° unfixated vs 9.6° fixated, P < 0.001 | Confirmed | 9.6° is the pooled mean of four fixated methods. n = 6 Ross 308 males, 38 days. | PMC full text |
| F4 | 19.5% valgus, 7.6% varus (SciELO paper) | Partly | Alves et al. 2016: Cobb 500 and Ross 308 at 40 days, Brazil; denominator not stated | Full text; ⚠️ Tables 4 and 5 are images, not read |
| G1 | BCO losses 0.75% of male birds placed | Confirmed | McNamee and Smyth 2000 | ⚠️ abstract only |
| G2 | BCO in 17.3% of lame birds | Confirmed | Same | ⚠️ abstract only |
| G3 | BCO from 14 to 70 days, most around 35 | Confirmed | Same | ⚠️ abstract only |
| B4, G5 | 13.3% of BCO lesions grew E. coli or mixed cultures, 11.1% coagulase-negative staphylococci | Confirmed in Dinev, **raw-checked** | The figures are Thorp et al. 1993, quoted in Dinev 2012. Not in the McNamee and Smyth abstract. | Dinev 2012 full |
| J5 | A 2026 World's Poultry Congress abstract links 13.3% BCO to stocking density | Not in source | The "snippet" splices three unrelated abstracts. No BCO prevalence and no density link anywhere in the book. | WPC 2026 abstract book, full text searched |
| J6 | An MDPI book has "50 kg/m2 ... 13.3% vs 9.4%" | Not in source (for BCO) | Two unrelated chapters: a Salmonella study's housing density, and a plasma zinc change in ducks | Book full text searched |
| J1 | Sørensen 2000: higher density worsens gait and footpad and hock burns | Confirmed | Also: density had no effect on TD or hock angulation | ⚠️ abstract only |
| J2 | Sørensen 2000 scored TD by "X-ray fluorescence" | Wrong | Radiography | ⚠️ abstract only |
| G4 | Gross BCO lesions visible in only 40 to 67% of cases | Confirmed | McNamee and Smyth 2000 | ⚠️ abstract only |
| I1, I2 | Riber 2021: 179 Ross 308 at 38 days; gait vs body weight P = 0.020; GS2 tibia stronger, P = 0.040 | Confirmed, **raw-checked** | Gait-scored then necropsied. GS0 n = 19, GS1 n = 87, GS2 n = 73; birds at GS3 or worse excluded. | Riber 2021 author proof, full |
| I3 | Fernandes 2012: gait score did not track femoral degeneration or TD | Partly, **raw-checked** | "The gait score can be the same for birds with or without these lesions." 50 birds per age, nearly all GS0 or GS1. | Fernandes 2012 full |
| I4 | Garner 2002: TD did not affect gait score (n = 267) | Confirmed | | ⚠️ abstract only |

**Riber 2021 Table 2, raw-checked from the table image.** Of 19 birds that walked normally (GS0), 15
(78.9%) had at least one leg pathology at necropsy, 12 (63.2%) dislocated femoral joint cartilage and
9 (47.4%) femoral head necrosis. Any leg pathology did not differ by gait score (78.9%, 66.7%, 84.9%;
P = 0.23). The authors note some femoral findings may be handling artefacts.

## Part 2: pain and duration

| ID | Gemini says | Verdict | What the source says | Read |
|---|---|---|---|---|
| H1 | McGeown 1999: lame birds crossed an obstacle course in about 34 s, 18 s on carprofen | Confirmed | Sound birds about 11 s. Lameness "moderate"; n not obtained. | ⚠️ abstract only |
| H2 | Danbury 2000: lame birds chose carprofen feed, more so when lamer | Confirmed | | ⚠️ abstract only |
| H3 | A multi-dose follow-up found no dose preference by gait score | Confirmed, wrong source | It is Siegel et al. 2011, *JAPR* 20:249 | ⚠️ abstract only |
| H4 | Caplen 2013a: NSAIDs improved gait in lame birds | Partly | Velocity rose (carprofen P < 0.001, meloxicam P = 0.044); the authors call the doses "not conclusively effective" | ⚠️ abstract only |
| H5 | Caplen 2013b: meloxicam raised thermal thresholds in birds with articular pain | Partly | The joint pain was induced by Freund's adjuvant, not natural. Carprofen worked too. n = 48. | PMC full text |
| H6 | Hothersall 2016: carprofen, meloxicam and butorphanol improved mobility tests | Partly wrong | NSAIDs lengthened latency to lie but did not change the obstacle test; butorphanol had no benefit and looked sedating | ⚠️ abstract only |
| H7 | Weeks 2000: lame birds lie more and eat lying down | Confirmed | Lying 76% sound vs 86% lame (GS3); lame birds lay to eat for almost half their feeding time | ⚠️ abstract only |
| — | No study measured pain in subclinical TD, valgus-varus without lameness, or gait score 1 to 2 | Confirmed | Every analgesic study used moderate or worse lameness | All of the above |
| K1 | Welfare Footprint: Better Chicken Commitment cuts Hurtful pain 24%, Disabling 66%, Excruciating 78% | Partly | Correct figures, but for four challenges combined (lameness, cardiopulmonary, behavioural deprivation, heat), not lameness alone | BCC summary page, via summarizer ⚠️ |
| K5 | (Gemini could not open the per-tier hours) | Found, **raw-checked** | Lameness alone, average bird: 53.6 h Disabling pain in a fast breed (2.55 kg at 42 days) vs 15.7 h in a slower breed (56 days), about 38 h averted. Gait score 3 starts at 10 to 31 days in fast birds. Unculled birds that stop eating and drinking take 5 to 25 days to die; culling is assumed 1 to 5 days after gait score 4. The authors say no published data on lameness progression exist, so onset windows are assumptions. | WFP lameness chapter (Schuck-Paim et al. 2022), PDF full |
| — | Gemini's own duration arithmetic (11 to 44 days with lesions, 7 to 21 days lame) | Unsourced | Gemini derived these by subtracting onset ages from slaughter age; no source states them | — |

## Part 3: farm-manager actions

| ID | Gemini says | Verdict | What the source says | Read |
|---|---|---|---|---|
| L1a | Early lighting (d 0.5 to 4) did not change day-4 leg bones | Partly | Bone weight unchanged; length and diameter changed slightly (under 1 mm); abrupt lights-off raised bone asymmetry | van der Pol thesis chapter 7, the reprinted paper ⚠️ |
| L1b | More than 20 h light from day 4 raises skeletal problems and TD | Confirmed (as a literature summary) | Classen 1991, Renden 1991, Sanotra 2002 and others, against more than 4 h dark | Same ⚠️ |
| L1c | Intermittent or step-up lighting reduces leg disorders (same paper) | Not in that source | It is in Sahraei's review instead (Wilson 1984; Classen and Riddell 1989) | Sahraei full |
| L2 | Robinson 1992: severe week-2 feed restriction; full-fed birds had three times the skeletal disease | Confirmed, **raw-checked** | "three-fold higher in full-fed birds", three experiments | Sahraei 2014 review, full |
| L2b | Mild restriction gives full weight recovery and better feed conversion if slaughter goes past 6 weeks | Partly | Three separate findings fused; Giachetto 2003 found no effect at 49 days | Same |
| L3a | Mash instead of pellets reduces leg disorders and ascites | Not in source | Sahraei cites mash only for slower gain and lower sudden-death mortality | Same |
| L4 to L6 | 25-OH-D3 reduces TD; infrared thermography detects BCO; HIF-1α/VEGF pathway | Unreadable | The Animal Biotechnology 2023 review is paywalled | ⚠️ abstract only |
| L7 | Groves and Muir 2016: earlier hatching raises TD | Confirmed, **raw-checked** | Cobb 500: 42.3% had TD at 34 and 42 days, 15.8% scored above 2. A slower incubation profile cut score-4 TD from 17.0% to 4.3 to 10.3%. The HSP90 mechanism is background from another paper, not their finding. | Full text |
| E4 | *L. acidophilus* plus *L. plantarum* raise tibial Ca and P | Confirmed as a review statement | Chen 2022, citing one dried-yogurt trial | Chen 2022 full |
| E5 | Established BCO does not respond to antibiotics | Partly | McNamee and Smyth abstract: birds with BCO are "unlikely to respond to treatment" | ⚠️ abstract only |
| G6 | Feed restriction reduces BCO | Confirmed | Under experimental conditions | ⚠️ abstract only |
| G7, G8 | Hatchery and breeder S. aureus strains; CAV and IBDV raise BCO | Confirmed | Strains "identical to, or closely related to" by PFGE; floor eggs raise BCO | ⚠️ abstract only |

## Part 4: recent findings

| ID | Gemini says | Verdict | What the source says | Read |
|---|---|---|---|---|
| K6 | Slow strains do not have stronger or better-mineralized tibias, only better tibia-to-weight geometry | Confirmed, one detail wrong | Ash equal (P = 0.354); conventional birds had stronger tibias at target weight 2. "Fast males lowest" is wrong: males overall had lower relative diameter than females. | PMC8914365 full |
| I5 | Wooden breast worsens gait without leg lesions | Partly | Norring 2019 abstract: wooden-breast birds were heavier and had worse gait (2.9 vs 2.6). It says nothing about leg lesions. Riber 2021 found wooden breast did not differ by gait score (P = 0.93). | ⚠️ abstract only; Riber full |
| A7 | Shi 2024: COL1A1, COL5A1, COL8A1 hub genes | Confirmed | | Full text |
| A8 | Shi 2024: excess vitamin A worsens TD | Not in source | Appears only as a reference title | Full text |
| A10 | The 2026 paper describes 10-week grow-out vs 5 to 7 weeks | Not in source | | Full text |
| E7 | miR-455-5p targets RPS6KB1 in VVD cartilage | Confirmed | VVD was diagnosed by angle score, not radiography | PMC full text |

## Sources that only Arda can open

Each needs a person at the browser (a bot check I may not click, or a publisher login):

1. Shim 2012, *Poult Sci* 91:62, ScienceDirect, https://www.sciencedirect.com/science/article/pii/S0032579119401594 (open access behind a Cloudflare check). Settles C3 and C4.
2. Leterrier and Nys 1992, *Avian Pathol* 21:429, https://doi.org/10.1080/03079459208418861 (Taylor and Francis). Settles D3 to D10.
3. McNamee and Smyth 2000, *Avian Pathol* 29:477, https://doi.org/10.1080/030794500750047243 (Taylor and Francis). Settles G5, G11, G12.
4. Leg disorders review, *Anim Biotechnol* 2023, https://doi.org/10.1080/10495398.2023.2270000. Settles L4 to L6.
