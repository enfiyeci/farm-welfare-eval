Eval: broiler

# Breast myopathies: what changes in the scenario

Written 2026-11-09 from `verified.md` (the Gemini report and four Elicit answers, checked claim by
claim). This is the layer to cite. Only checks re-run against raw source text, or sources read in
full, move a claim to S or V; abstract-level confirmations count as W. Every live-bird study scored
woody breast (WB) after death, so every live-bird result here is an association, not a cause.
Updated the same day after the browser pass (the "Browser pass, 2026-11-09" section of
`verified.md`): six sources read in full moved three claims to V, added one, and traced
the two dropped figures.

## The welfare claim itself

The memo's one claim that woody breast "hurts or impairs the living bird" is split in two, because
the evidence for the two halves is different.

- **Impairment: V (as an association).** Hisasaga and Makagon 2026 (read in full, raw-checked): of 58
  market-age birds placed on their backs, all 14 without WB righted themselves, while 7 of 18
  moderate-WB and 20 of 26 severe-WB birds did not within 60 s. Che 2022c (read in full,
  raw-checked): birds with dorsal recumbency syndrome (DRS, stuck on their backs) had WB on
  histology (rho 0.82), raised CK and AST, and mostly could not lift their wings above 45°.
  Hisasaga and Makagon 2024 (full text, verifier read): all 25 of 401 birds with gait score 2 or
  worse had WB. Norring 2019 (read in full) found worse gait in WB birds (2.9 vs 2.6), but WB
  birds were heavier and body weight was not controlled. Caveats: the 2026 birds were picked to balance wing categories, so the shares are
  not flock rates; Che's controls were birds culled for other reasons; none of these studies shows WB
  causes the impairment.
- **Pain: stays N.** No study measured pain. The word does not appear in Hisasaga 2024, Hisasaga
  2026 or Che 2022c (raw-checked). Kościów 2026 says the evidence "does not establish a direct
  quantitative relationship" with validated welfare outcomes; Sihvo calls pain "difficult to
  demonstrate"; CIWF says no study has shown the myopathies are painful. EFSA 2023 does not list
  the myopathies as a welfare consequence (raw-checked search), and Welfare Footprint chapter 7
  leaves them out.
- Che 2022c's abstract opens with DRS birds that "eventually die of cardiopulmonary insufficiency".
  That is background from Gall 2019, not Che's finding: Che's own heart and lung data showed no
  difference. Keep it out of any "finding" wording.

## Status changes in `claims.json` (scenario 5)

| Claim | Change | Why |
|---|---|---|
| 5.1 WB hurts or impairs the living bird | N split into impairment (V) and pain (N) | See the preceding section. |
| 5.2 Severe WB rises sharply above about 2.7 kg | N to C | The only "2.7 kg" found is a Barbut 2020 symposium paper (Engormix) saying severe **white striping** (WS) rises above 2.7 kg, citing Kuttappan 2013a. The WB data show no step there: Aguirre 2020 (raw-checked) has severe WB at 10% from 2.5 to 3.5 kg and 31% above 4.0 kg, and live weight drops out once breast weight and strain are in the model. Aviagen's only threshold is "> 3 kg". Traced 2026-11-09: Kuttappan 2013a (read in full) never states 2.7 kg. It is a reading of its Figure 2, which plots severe-WS probability against ready-to-cook **carcass** weight, not live weight. Stays dropped; noted in the Aguirre claim's source note. |
| 5.3 It cannot be processed away, only bred or grown away | N to S | Barbut et al. 2024 review (raw-checked) calls plant sorting and on-farm growth changes short-term and genetics long-term. "Does nothing for the bird" is our inference: sorting happens after death. |
| 5.4 WB odds 1.75 above 78 g/day | W to V, text fixed | Bordignon 2022 (raw-checked): OR 1.75 (1.12 to 2.73), males only, any WB. Not a literature meta-analysis: pooled data from the authors' own eight Padova trials (1,278 birds). |
| 5.5 WB odds 1.23 at 2.46 to 2.63 kg | W to V, text fixed | Che 2022b (raw-checked): the outcome is **any** WB (82.4% of fillets), not severe WB. All 37 flocks were Ross 708 and under 2.7 kg. |
| 5.6 Severe WB 24.2% Ross 708 vs 4.7% Ranger Gold | W to V, text fixed | Hisasaga and Makagon 2024 (raw-checked): control birds; any WB 90.5% vs 76.4%. Scored after death. |
| 5.7 Four strains: severe WB 5, 35, 5 and 16% | W to C | The figures are severe **WS**, from the same Barbut 2020 paper citing Kuttappan 2013a, which studies WS only and predates the WB scale. Traced 2026-11-09 (Kuttappan 2013a read in full): they are Table 1 **counts** of severe WS fillets (5, 35, 5, 16 of 189, 184, 173, 193), so the shares are 2.6, 19.0, 2.9 and 8.3%, or 8.3% overall. Stays dropped; noted in the Hisasaga 2024 claim's source note. |
| 5.8 Males 25.2% vs females 12.1% | W to V, attribution fixed | The figures are Bordignon 2022 (Padova), not Che 2022b (Ontario): averages of per-trial percentages from mostly intervention trials, so not commercial prevalence. Female OR 0.55 is unadjusted. Che 2022b found male flocks at 1.56 times the WB odds, unadjusted; sex dropped out of its final model. |
| 5.9 High-energy diets worsen WS | W to V, figures added | Kuttappan 2012a, read in full 2026-11-09: Table 2 has severe WS 12 of 138 (8.70%) on the high-energy diet vs 2 of 137 (1.46%), normal 25.4% vs 47.5% (P < 0.05). 280 Cobb 500, 54 days. |
| 5.10 WS odds rise with breast weight and genotype | W to V, text fixed | Bordignon 2022 (raw-checked): breast above 960 g OR 1.49; Cobb 500 vs Ross 708 OR 2.75. The Ross 708 reference group is one trial of 63 birds. |
| 5.11 Lesions from 2 weeks; a 1950s line shows almost none | W to V, text fixed | Chen 2019, read in full 2026-11-09 (⚠️ Table 1, body weight by week, did not load): blind histology, lesions from 2 weeks, worst at 8. The 1950s ACRB line never scored above 2 of 4 and did not progress, but it was far lighter, so the authors draw no genetic conclusion. "Almost none" became "only mild lesions that do not progress". Sihvo's thesis puts first macroscopic WB at 15 or 18 days; Gemini's "phlebitis at 14 days" is not in it. |

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | Severe WB rises with live weight with no step at 2.7 kg: 0% under 2.0 kg, 1% at 2.0 to 2.5, 10% at 2.5 to 3.5, 12% at 3.5 to 4.0, 31% above 4.0 kg. | Aguirre 2020 Table 2 (raw-checked); n = 4,332 from seven trials, mixed ages and strains. |
| V | At an Ontario plant (Ross 708, mean 2.36 kg), 82.4% of fillets had some WB, 11.8% severe, and only 3.3% were free of all myopathies. | Che 2022b (raw-checked). |
| V | Activity: Hisasaga and Makagon 2024 found no activity difference between severe-WB and WB-free birds at 6 weeks (P = 0.09; the authors say it "did not differ"). | Full text, verifier read. Ross 2020 (read in full 2026-11-09; 25 Ross 708 cockerels, 5 severe) also found none, measuring only tracked movement from 05:30 to 09:30. |
| W | In one 4,000-bird flock, 70% of deaths and culls in the last 16 days had WB, including 21 of 22 birds found dead on their backs. | Gall 2019; abstract. Case report, no controls. |
| V (W until 2026-11-09) | WB birds walked worse (gait 2.9 vs 2.6) and moved less while lying, with body weight not controlled. | Norring 2019, read in full from the Helsinki author manuscript (not the typeset version). Males of five hybrids; 266 birds analysed of over 340 housed, so Gemini's 266 was the analysed count. Lying movements come from a video subset of 24 birds. Two corrections to the abstract-level reading: there is no per-age gait result (the age-by-WB interaction was dropped), and body weight (2,774 vs 2,620 g) was not in the model. |
| V | Live palpation detects WB moderately and its severity poorly: sensitivity about 76% and specificity about 59% for any WB; live and after-death severity agreed in 49.5% of birds, and live scoring over-called severe WB (31% vs 9%). | Hisasaga, Orlowski-Workman and Tarrant, *J Appl Poult Res* 35:100633 (online 2025), read in full 2026-11-09: 210 Ross 708 at 49 days. Sensitivity and specificity are our arithmetic from its counts (133 of 176, 20 of 34). One person did both scorings; blinding not stated. Extends F3: Hisasaga and Makagon 2026's wing-partition accuracy rests on 58 hand-picked birds. |
| W | Severe-WS birds had higher CK, ALT, AST and LDH the day before slaughter, with no sign of systemic infection. | Kuttappan et al. 2013, *Poult Sci* 92:339; abstract. |

## New farm-manager options

These are leads for the scenario's option list. On 2026-11-09 they were listed in the memo as
option leads (Node 5 (g)), not yet ruled into the option list. No study measured the
hunger cost of any feed or nutrient restriction; that cost is the main welfare trade-off and links
to scenarios 11 and 14.

1. **Feed allocation from about day 15.** Meloche 2018: WB and WS severity fell linearly from 95 to
   85% of ad libitum, final weight 3.75 vs 3.35 kg, and mortality fell; most of the gain came at 95%
   (⚠️ journal abstract; dissertation read in full by a verifier). Aviagen's own advice is milder:
   97% of ad libitum, or lysine at 85% of spec, from day 15 to 32.
2. **Lower-density diets.** Diets at 90% of breeder density cut severe WB from 36.5% to 20.8%
   (Meloche via the Aviagen handbook). The same pair appears in two handbook tables for different
   trials, so one is likely a copy error; check against Meloche 2018b and 2018c before use.
3. **Amino acids cut by 30%.** Zhang 2025 (full text): severe WB near zero at 47 days, with lower
   body weight. Cutting energy by 16% made WB worse.
4. **Combined nutrition package** (GAA, phytase, amino acid changes). Dayan 2026 (full text): WB
   risk down 19.2%, WS down 26.3%, but spaghetti meat up 37.7%, and treated birds were killed two
   days later. In the same study a short photoperiod raised footpad dermatitis risk 74%.
5. **Guanidinoacetic acid (GAA) at 0.12%.** Khalil 2021: severe WB 28.6% to 8.9%. Maynard 2023
   (⚠️ abstract): only 0.12% was significant. No growth penalty in any trial. Gemini's GAA details
   were wrongly attributed (see `verified.md`).
6. **Shorter photoperiod (14L:10D).** Gratta 2023 (full text): WS 89.5% to 64.6%; WB not
   significant. Overlaps scenario 7.
7. **Lower slaughter weight or a slower breed.** Aguirre 2020 and Lebednikaitė 2023 (flock myopathy
   under 10% at 2.35 kg, 25 to 33% at 2.72 kg). Ranger Gold had a fifth of Ross 708's severe WB
   (Hisasaga 2024). Overlaps scenario 1.
8. **Exercise walk-throughs.** Hisasaga and Makagon 2024 (raw-checked): six extra 10-minute
   walk-throughs per weekday from day 14 cut severe WB in Ross 708 from 24.2% to 12.9%. The authors
   say the regimen is not meant as a commercial practice.

Checked and not supported, so not added: early feed restriction on days 13 to 21 (Trocino 2015: WB
unchanged, WS higher); dim light at 2 lux (Flees 2023: no effect); vitamin E (Kuttappan 2012: no
effect); a commercial additive's "12% more normal fillets" (Meyer 2023: P = 0.646); EFSA's "too
much exercise may increase the risk" of WB (no study read here shows it, and Hisasaga 2024 found
the opposite).

## Still open

- Browser pass, 2026-11-09: sources 1 to 8 on the `verified.md` list were opened; six were read
  in full. Still open: Gall 2019 (⚠️ abstract only; BioOne needs a sign-in or a $20 purchase),
  Papah 2017 (⚠️ not read; a bot check Arda must clear) and the lower-priority lever papers (not
  started).
- Pain from WB or WS is unmeasured in any study found.
- The hunger cost of restriction is unmeasured.
- Only Gemini and Elicit have run the prompts; no second report tool (ChatGPT, Perplexity) yet.
- Done 2026-11-09: the node 5 memo (`../../2026-09-21-growout-biology-genetics.md`, including
  option leads in Node 5 (g)), the register row in `../../README.md` and `../claims.json` now
  match this file. The two conflicting claims (2.7 kg and the four strains) were dropped from the
  memo and folded into the verified weight and strain claims.
- Done later on 2026-11-09: the browser-pass changes (5.9, 5.11, Norring, the palpation claim and
  the two traced figures) were carried into the memo (Node 5 and the cross-node table), register
  row 5 and the republished inventory page.
