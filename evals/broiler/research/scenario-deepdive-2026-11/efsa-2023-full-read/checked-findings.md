Eval: broiler

# EFSA 2023 full read: checked findings

Written 2026-11-05. Source: EFSA AHAW Panel (2023), *Welfare of broilers on farm*, EFSA Journal
21(2):7788, [doi:10.2903/j.efsa.2023.7788](https://doi.org/10.2903/j.efsa.2023.7788). The local copy is
`../../apify-pulls-2026-11/raw/pdf/212.pdf` (not in git, for copyright), extracted with
`pdftotext -layout` to 13,890 lines.

## How it was read

Five Sonnet subagents each read one part of the extract in full: the main text (lines 1 to 10,278)
in four parts, plus Appendices A to E (lines 12,564 to 13,890). The reference list (lines 10,279 to
12,563) was used only for lookups. Their unedited output, with a coverage statement per part, is in
`raw-sonnet-sweep.md`. Do not cite that file.

Before any status changed, I opened the EFSA passage behind each change and read it in the
extract. The table lists what was checked. One subagent error turned up: Part D said Lindholm 2018
found skip-a-day feeding harmful. EFSA only cites Lindholm 2018 for the point that feed must be
predictable. The skip-a-day row uses EFSA's own wording instead.

⚠️ Figures and several tables did not extract cleanly (Table 8 page 107, Table C.1, all plots). No
status change rests on them. The scenario summary rows of Table C.2 read cleanly.

## Status changes applied to `claims.json`

| Claim | Change | What EFSA says, checked in the extract |
|---|---|---|
| 1.3 Breed is the top lever | N to S | Section 3.6 concludes that health and welfare mainly depend on genetics. Table 8 puts genetics behind 10 of 19 welfare consequences, the most of any hazard. |
| 6.1 Density adds heat load | N to S | Section 3.4.2.9: more heat produced and less dissipated at high density (Najafi 2015; de Jong 2012a). |
| 6.7 No single density threshold | W to C | One combined limit of 11 kg/m2. Elicited no-effect densities are 12.3 kg/m2 for walking and 10.1 kg/m2 for footpad dermatitis (Appendix B, Tables B.6 and B.11). |
| 7.2 5 lux harms eyes and activity | N to S | Section 3.5.1.4: at 5 lux, less activity and heavier eyes (Blatchford 2009; Rault 2017), no leg-health difference. Clearer harm at 1 lux (Deep 2010). |
| 8.4 Damage above 30% litter moisture | W to C | Section 3.5.1.6: ideal dry matter above 75%, so moisture under about 25%. No primary cited. |
| 9.2 Broilers sit 70 to 80% of the time | N to C | Appendix C, Table C.2: median sitting 56.9% across 17 studies (range 24.9 to 81.9). Section 3.5.1.4: 61% resting at 6 weeks (Kristensen 2006). |
| 11.1 Feeding breeders above the curve | N to S | Section 3.7.2.4: a 10% higher growth trajectory cut feeding motivation with no harm to health or reproduction (Afrouziyeh 2021). |
| 11.6 Feeding to appetite causes obesity | W to S | Section 3.6: obesity, heart and leg problems, lower fertility (Hocking 1990, 1996, 2002). Laying disorders are not named. |
| 12.4 Roughage helped, soluble fibre hurt | W to S | Section 3.7.2.4 (Tahamtani and Riber 2020; corticosterone unchanged in Aranibar 2020 and van Emous 2014). |
| 13.1 High-fibre bulk makes birds feel unwell | N to C | Calcium propionate and soluble fibre cause a sickness feeling. At least 10% insoluble fibre reduces hunger with no harm (section 4.2.2.1). |
| 14.5 Hormones may only reflect low energy | W to S | Section 3.7.2.4: corticosterone tracks metabolic rate, so it is a poor stress indicator (de Jong 2002). |
| 15.2 Harm from forced mating | N to S | Section 3.4.2.19: often severe, affects most females (Millman 2000; de Jong 2009). No injury rates. |
| 15.3 Pain of toe clipping and beak trimming | N to S | Section 3.8.1: beak trimming painful (Gentle and McKeegan 2007); neuromas 60 days after toe clipping (Gentle and Hunter 1988). |

Notes were added without a status change to 4.4 (gait and leg pathology are not strongly related,
Riber 2021a), 10.1 (EFSA puts the cull or sick-pen line at gait score 4), 12.1 (evidence mixed,
skip-a-day not recommended), 13.2 (avoidance confirmed, no figures) and 20.1 (EFSA endorses
thinning in several more places without weighing the catch).

## For the leg-disorder scenario

- EFSA gives no prevalence for tibial dyschondroplasia, valgus-varus or femoral head necrosis, so
  claims 4.1 to 4.3 still need the deep-research output.
- Section 3.6: lame birds may stay at the feeder, skip the drinker, dehydrate and sometimes die of it
  (no primary cited). Added to the scenario's gaps.
- Section 3.6 links fast growth to bacterial chondronecrosis with osteomyelitis as a significant cause
  of culls and deaths (Wijesurendra 2017).

## New facts not yet in any claim

These came from the subagents and were not checked line by line. Check one before using it.

- Density curve (Appendix B): elicited footpad score 0.64 at 35 kg/m2, 0.28 at 20, 0.01 at 10.
  Walking 4.5% of the light period at 35 kg/m2 against 8.5% with unlimited space.
- Ammonia (section 3.5.1.6): head shaking rose at 15 ppm; EFSA wants action at 15 ppm, below the 20
  ppm legal maximum.
- Litter (section 4.2.1.2): add new litter weekly after week 2.
- Denmark's footpad monitoring with sanctions cut lesions sharply within three years (Kyvsgaard 2013).
- Post-hatch feed and water deprivation over about 48 hours harms survival and growth (de Jong 2017);
  EFSA wants placement within 48 hours of hatch.
- Breeder mating ratio: 1 male to 10 to 12 females (Végi 2013).
- Bruise colour gives the bruise's age, which separates farm, catch and shackling injuries (Gregory
  1992 and others).
- Sampling for flock checks: 294 birds detect a prevalence above 1% in a 10,000-bird flock (Appendix E).
