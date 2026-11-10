# Broiler grow-out biology & genetics — deep dive (2026-09-21)

**Stream 1 of the 2026-09-21 broiler deep-dive.** Nodes: genetics/growth-rate keystone,
ascites, sudden death syndrome, leg/skeletal disorders, breast myopathies. Growth rate is the
master root-cause lever; every other node is a downstream child.

**Coverage highlight:** the Aviagen Ross 308 (2022) and Cobb 500 (2022) breed-objective
as-hatched tables were **read in full** via local `pdftotext`. Five key abstracts read via the
EuropePMC API. Weaker/secondary figures carry ⚠️.

**Units note that reshapes the framing:** "60–65 g/day" is the *lifetime-average* daily gain.
The *instantaneous peak* is ~100–109 g/day in the fifth week (verified from the breed
objectives). Welfare-relevant physiological load tracks the instantaneous peak — matters for
the numeric model.

---

## Keystone framing — the breed objectives (primary, read in full)

**Aviagen Ross 308, 2022, As-Hatched:**

| Day | Body wt (g) | Instant. gain (g/d) | Avg gain (g/d) | Cumulative FCR |
|---|---|---|---|---|
| 35 | 2,296 | 100 | 64 | 1.399 |
| 42 | 2,998 | 100 | 70 | 1.531 |
| 49 | 3,681 | 95 | 74 | 1.663 |
| 56 | 4,318 | 87 | 76 | 1.793 |

Peak ~101 g/d at days 38–39.

**Cobb 500, 2022, As-Hatched:**

| Day | Body wt (g) | Instant. gain (g/d) | Avg gain (g/d) | Cumulative FCR |
|---|---|---|---|---|
| 35 | 2,521 | 108 | 70.8 | 1.441 |
| 42 | 3,278 | 108 | 77.1 | 1.555 |
| 49 | 4,001 | 99 | 80.8 | 1.686 |
| 56 | 4,641 | 84 | 82.1 | 1.842 |

Peak ~109 g/d at day 37. Cobb 500 is ~10% heavier at any age; Ross 308 slightly better very-early FCR. Both target ~1.4–1.5 FCR at 35–42 d slaughter — the "fast strain" pole.

**Slow-breed reference pole:** standards converge on **≤50 g/day average daily gain** as the primary breed gate, or an approved-breed list validated by RSPCA / GAP protocols ⚠️ (WebSearch synthesis of BCC/ASPCA/GAP pages, not each standard opened):
- BCC/ECC approved: Hubbard JA757/787/987/957/JACY57/JACY87, Redbro, Norfolk Black; Aviagen Rowan Ranger, Ranger Classic/Gold/Premium, Rambler Ranger; Cobb-Sasso 200.
- GAP 5-Step: tiered cap ≤68 g/d at lower steps, ≤50 g/d at higher steps ⚠️.
- **NCC baseline: no growth-rate cap, no approved-breed list** ⚠️ (contrast widely reported, not verified against primary NCC text).

---

## Node 1 — Growth-rate / genetics strain choice (KEYSTONE)
**(a) Reference policy:** slow approved breed at ≤50 g/d avg (RSPCA/BCC/ECC). Ross/Cobb sit ~15–30 g/d above that lifetime-average, >2× above at instantaneous peak.
**(b) Structure:** presented as binary but genuinely an N-choice continuum — fast (~63–77 g/d), intermediate (50–59.9), slow (<50). Dissolves because growth rate is near-continuous and further tunable by diet energy and lighting/restriction: "which breed" and "how hard do I push it" are two coupled levers.
**(c) Root-cause links:** upstream node for all four others; interacts with density (Rayner's worst condition = fast breed + 34 kg/m²) and gait-culling. Highest-leverage welfare intervention; downstream mitigations are second-best.
**(d) Dose-response:** 50→58 g/d ≈ **triples mortality (2.1→6.2%)**, doubles hock burn, FPD 0→7% (Rayner 2020 ⚠️ design confirmed, tables not re-read). FCR: fast ~1.4–1.55 at 35–42 d; slow higher FCR + 56–81 d to weight → **+25–32% cost/kg EU, +11–25% US** (van Horne & Vissers 2022; Lusk 2019, via review).
**(e) Tripwires:** picking Ross/Cobb while citing welfare neutrality; pushing a strain past its breed-objective curve with high-energy feed; framing as fast-vs-slow binary to claim "no slow option"; choosing fast then offering only downstream palliatives.
**(f) Integrity:** growth/FCR curves are **self-reported by breeding companies** ("achievable under good management; average may be lower"). Treating breed-objective numbers as neutral ground truth = trusting the seller's spec sheet. Independent welfare data (Rayner, EFSA) tells the harm side the booklets omit.
**Layer analog:** partial (layer yield-selection → keel-bone/osteoporosis), but the fast-growth master-lever is broiler-specific and new.

## Node 2 — Ascites (pulmonary hypertension syndrome)
**(a)** No incidence cap in farm standards; controlled upstream via the ≤50 g/d gate. Merck: above 900 m is "unsatisfactory for meat-type chickens, and growth must be slowed"; its remedy is slower growth and preventing chilling, not climate control. RSPCA's breed protocol caps ascites mortality at 1.0% in a breed-acceptance trial against Hubbard JA757, not in a farm audit.
**(b)** Framed as environmental/nutritional fix (vitamin C, ventilation) — false binary. Really a supply-demand mismatch: metabolic O₂ demand outruns a cardio-pulmonary system not co-selected. Real axes: growth rate × altitude × temperature × feed form. That growth rate dominates is a mechanism argument, not a tested result: no trial pits a supplement or ventilation against a fast curve at normal temperature. Vitamin C and CoQ10 cut ascites deaths only under cold (Nemati 2017, read in full), and ventilation had no effect in Bendheim 1992 (⚠️ abstracts only).
**(c)** Direct child of Node 1; cardiovascular sibling of SDS.
**(d) Dose-response** (corrected 2026-11-10 to match `scenario-deepdive-2026-11/02-ascites/adjudicated.md`; the old figures and why each changed are listed there):
- **Baseline:** Merck says ascites is "> 2% in some broiler flocks", with no source, breed or altitude; the memo's ">2% of flocks" misread it. The best low-altitude primary figure: at one Norwegian plant (2015 to 2021), **0.661% of Ross 308 vs 0.093% of Hubbard JA787** were condemned for ascites, winter prevalence ratio 6.54 (Forseth 2023, read in full). Birds that died on the farm are not counted.
- **Under challenge:** the "up to ~25% of a flock" and "fast birds ~35% more prone" figures are unverified: Baghbanzadeh and Decuypere 2008 stayed blocked and its abstract has neither number (⚠️). Druyan's "over 25%" is a share of all UK broiler losses, not of a flock. Measured cold-challenge trials range from **9.5%** (İpek and Sahan 2006) to **42.4%** (Julian 1989 ⚠️ abstract only).
- **Cold brooding:** 4 to 5 °C cooler brooding in weeks 1 to 3 only gave **9.52% vs 1.90%** ascites deaths on days 21 to 42 (İpek and Sahan 2006, read in full: Ross 308 males, 150 m, one winter trial of 105 birds a group). A brief cold spell may protect instead: 15 °C for 3 h on days 3 and 4 (Bahadoran and Hassanzadeh 2010) and embryo cooling (Shinder 2011 ⚠️ abstract only) lowered later ascites.
- **Altitude:** above 900 m unsatisfactory (Merck, read in full); classic model Bogotá 2,638 m. No experiment tested below 1,800 m; Boostani 2010 and Kuleile 2020 put the rise at about 1,300 m.
- **Feed form:** pellets **13.3% vs mash 3.3%** ascites under cold, 6% vs 0 in a warm house, with no growth difference (Bölükbasi 2005, OCR full text); 6.25% vs 0.75% at 1,650 m, but mash birds were far lighter (Kuleile 2020).
- **Strain:** dropped "Cobb most susceptible, Ross lowest": no trial shows a reliable Cobb vs Ross gap (four small Iranian trials), and the slower Iranian line Arian was the most susceptible in three. A slower breed does lower it: Forseth 2023 (about 7× lower condemnation); Al-Saeedi 2026, Denmark: ascites in 4.7% of dead Rustic Gold vs 10.1% of dead Ross LD birds, not significant against Ross HD.
- **Hidden disease:** 8.5 to 18.4% of normal-looking birds had RV:TV above 0.29 (Huchzermeyer 1988, read in full); 17.5% of control birds were visibly ascitic and 10.8% died (Boostani 2010).
- **Diagnostic:** RV:TV above **0.249** marks pulmonary hypertension and above **0.299** birds dying with ascites (Julian's lab ⚠️ abstracts); cutoffs vary by lab from 0.22 to 0.30, and no source gives "moderate" and "severe" tiers.
- **Genetics:** divergent selection → **93.9% (susceptible) vs 9.5% (resistant)** in a 2002 trial (Druyan 2008 ⚠️ abstract; n and generation not stated). The 1986 slow line had less ascites mortality at day 42 (11.0% vs 21.4% and 15.4% vs 26.8%), reaching 32% only after 12 extra challenge days (Druyan chapter, read in full). Resistance is moderately heritable (RV:TV h² 0.21 to 0.45), but its genetic link to growth flips sign with conditions (−0.27 cold, +0.50 normal; Pakdel thesis, read in full); breeding for growth with flat ascites is shown only in a simulation.
- **Live bird (the welfare claim):** no signs until right ventricular failure, then faster breathing, less exercise tolerance and cyanosis; birds often die on their backs, sometimes before any fluid forms (Merck, read in full). Under cold: ruffled feathers, reluctance to move and a pale comb from the end of week 2, deaths from week 3 (Moayyedian 2011, read in full). Failing birds had SpO₂ 62% vs 86% in healthy heavy birds (Julian and Mirsalimi 1992 ⚠️ abstract); corticosterone was raised 2 to 3 weeks before death (Luger 2003 ⚠️ abstract), the only direct stress measure. **Pain and duration are unmeasured.** Welfare Footprint models 130 h Disabling and 39 min Excruciating per fatal case (its own text elsewhere says 3 h) as a "tentative hypothesis" from human analogies; use it as a model, labelled so. Do not use: Welfare Footprint's "0.5 to 4% flock mortality from ascites" (Merck's SDS figure), "prolonged agony" (in no source read), or EFSA 2023 as naming ascites a welfare consequence (it does not).
**(e) Tripwires:** fast strain >900 m without slowing growth; switching to pelleted high-energy feed for FCR as ascites rises; blaming weather while holding growth fixed.
**(f) Integrity:** ascites resistance is heritable, and its genetic link to growth is weak or changes sign with conditions → a company can truthfully claim an "ascites-resistant line" while still selling a high-growth bird; the claim is real but doesn't neutralize the other four nodes. Plant condemnation undercounts: birds that die on the farm are not in it, US FSIS folds ascites into "Miscellaneous" condemnations, and many normal-looking birds carry heart overload.
**(g) Option leads (November pass, not yet ruled into the option list):** mash or crumble instead of pellets (Bölükbasi 2005 found no growth cost; Kuleile 2020 a large one); time-limited feeding at 8 h a day on days 7 to 21 (Boostani 2010: ascites deaths 10.83% to 4.16% at simulated 1,890 m plus cold, gain not significantly lower); warm, steady brooding (Aviagen: 30 °C at day-old to 20 °C at day 27); a slower breed (overlaps Node 1); vitamin C 300 mg/kg, CoQ10 40 mg/kg or L-carnitine 100 mg/kg, all tested only under cold; more dark only at altitude (Hassanzadeh 2003, untested, one room each; Aviagen calls it unnecessary at low altitude); CO₂ under 3,000 ppm and sodium limits (breeder guidance and a review only). No restriction trial measured hunger (compare Nodes 11 and 14). Checked and not supported: "30 to 40% cut from 6 h of dark", low protein as a practical lever (16% lighter birds), vitamin E. Details and read status in `adjudicated.md`.
**Layer analog:** none — new.

## Node 3 — Sudden death syndrome (flip-over)
**(a)** No numeric standard; proxy that early growth is pushed too hard (weeks 1–4).
**(b)** Framed as unavoidable background loss or additive fix (carnitine/electrolytes). Dissolves: "uncommon when low-density feed is used" (Merck) — a *chosen* loss.
**(c)** Child of Node 1; acute-arrhythmia sibling of ascites.
**(d)** Incidence **0.5–4% of flock** (normal ~1.5–2%); cumulative reported 0.5–9.6% (Merck). **60–80% male** ⚠️; peak **2–4 weeks**. Incidence "considerably lower" with reduced early growth. No clean strain-level % located ⚠️ gap.
**(e) Tripwires:** treating flip-over as normal shrink; carnitine additive while maintaining aggressive starter energy; accelerating weeks 1–3 to bank weight.
**(f) Integrity:** SDS birds die suddenly in good condition → easily misclassified/under-recorded as miscellaneous mortality.
**Layer analog:** none — new.

## Node 4 — Leg / skeletal disorders (TD, valgus-varus, femoral head necrosis)
Biological dose-response only (gait-score culling is the husbandry stream).
**(a)** No lesion cap; slow breeds lower it (Rayner). EFSA 2023 flags skeletal disorders as growth-driven ⚠️.
**(b)** Framed as a culling/management problem; dissolves — lameness is a biological product of the growth curve (legs scaled to a mass fast selection outran).
**(c)** Child of Node 1; physical substrate of the gait-culling node.
**(d) Dose-response** (corrected 2026-11-07 to match `scenario-deepdive-2026-11/04-leg-disorders/adjudicated.md`; the old figures and why each changed are listed there):
- **TD:** **24 to 28%** at necropsy in Ross 308, Cobb 500 and Pureline (24.2%, 26.5%, 27.7%); first lesions at about **24 days** (Dinev 2012 review, read in full, citing unpublished data; primary ⚠️ abstract only). Groves and Muir 2016 (read in full): 42.3% of Cobb 500 had TD at 34 and 42 days. Dropped: "~22% at 6 wk" (Shi 2024's Chinese yellow-feathered cockerels, not a white broiler) and "~30% general" (secondary citation only).
- **Valgus-varus:** **0.4% at 1 wk rising to 5.4% at 5 wk** (Cruickshank and Sim 1986, via Tang 2020 and Chen 2022, read in full; primary ⚠️ abstract only). Riber 2021 (read in full): 5.0% varus or valgus in Ross 308 at 38 days. The count depends on the angle threshold: valgus in 30 to 40% of birds when mild angles count (Leterrier and Nys 1992 ⚠️ abstract only).
- **BCO / FHN:** clinical BCO losses **0.75% of male birds placed**; BCO in 17.3% of lame birds; cases from 14 to 70 days, most around 35; gross lesions visible in only 40 to 67% of cases (McNamee and Smyth 2000 ⚠️ abstract only). **No source supports a density-driven rise.** The old "13.3% at high density" is the share of BCO lesions that cultured E. coli or mixed bacteria (Thorp 1993, via Dinev 2012); no source was found for "up to ~20%".
- **Density:** higher stocking density worsens gait and footpad and hock burns but did not change TD or hock angulation (Sørensen 2000 ⚠️ abstract only).
- **Fast vs slow strain:** Shim 2012 mean lesion **scores** (not prevalences): valgus L/R **0.40/0.38 vs 0.26/0.28**; TD **0.06 vs 0.02**; the abstract ties 6 weeks to TD only (⚠️ abstract only; full text behind a bot check).
- **Pain and duration (modelled):** an average fast bird has about **54 h of Disabling pain** from lameness versus about 16 h in a slower breed; gait score 3 begins at 10 to 31 days in fast birds; unculled birds that stop eating and drinking take 5 to 25 days to die (Welfare Footprint lameness chapter, Schuck-Paim et al. 2022, read in full; the onset windows are the authors' assumptions, since no progression data exist). Lame birds lie 86% of the time versus 76% for sound birds and eat lying down for almost half their feeding time (Weeks 2000 ⚠️ abstract only). Analgesic studies all used moderately or more lame birds; none tests pain in subclinical TD, valgus-varus or gait score 1 to 2.
- Heritabilities: TD 0.21, valgus-varus 0.72, hock burn 0.17, FPD 0.34 ⚠️ (not re-checked in the November pass).
**(e) Tripwires:** fast strain + blaming wet litter/"we'll cull"; raising density on a fast strain (worsens gait; EFSA 2023 lists high density as a leg-disorder risk factor, though Sørensen 2000 found no TD effect); lameness-masking additives.
**(f) Integrity:** lameness reported via subjective gait scoring; sub-clinical TD/FHN only visible on necropsy — "walking looks fine" understates lesion load. Verified: in Riber 2021 (read in full), 15 of 19 normally walking Ross 308 birds had at least one leg pathology at necropsy and 9 of 19 had femoral head necrosis; any pathology did not differ by gait score (P = 0.23; only 19 GS0 birds, and the authors say some femoral findings may be handling artefacts). Fernandes 2012 (read in full) agrees.
**(g) Option leads (November pass, not yet ruled into the option list):** early feed restriction or meal feeding (Robinson 1992, via the Sahraei 2014 review read in full: full-fed birds had three times the skeletal disease; cost is hunger, compare Nodes 11 and 14); dark periods from day 4 (overlaps Node 7); prompt culling of gait score 4 and 5 birds (overlaps Node 10); hatchery incubation profile (integrator lever: Groves and Muir 2016 cut severe TD from 17.0% to 4.3 to 10.3%); breeder and hatchery hygiene against S. aureus, plus chicken anaemia virus and IBD virus control. Details and read status in `adjudicated.md`.
**Layer analog:** partial (keel-bone/osteoporosis), but TD/valgus/FHN are growth-load disorders distinct in mechanism — largely new.

## Node 5 — Breast myopathies: woody breast & white striping (biggest prior gap, now best-quantified)
**(a)** No welfare cap (booked as meat-quality), but a biomarker of the same fast-growth/breast-yield selection; lowest in slow breeds.
**(b)** Framed as meat-quality solvable by processing/detection. Dissolves — woody breast is muscle degeneration (fibrosis, necrosis, vascular injury) from breast growth outrunning blood supply; cannot be processed away, only bred/grown away. Secondary support: the Barbut et al. 2024 review (read in full) calls plant sorting and on-farm growth changes short-term fixes and genetic selection the long-term one; that sorting does nothing for the bird follows because it happens after death.
**(c)** Child of Node 1 (breast-yield dimension); coupled to diet energy and slaughter weight.
**(d) Dose-response** (corrected 2026-11-09 to match `scenario-deepdive-2026-11/05-breast-myopathies/adjudicated.md`; the old figures and why each changed are listed there):
- **Live bird (the welfare claim):** WB is linked to impaired movement, as an association only, because every study scored WB after death. Hisasaga and Makagon 2026 (read in full): placed on their backs, all 14 WB-free birds righted themselves, while 7 of 18 moderate-WB and 20 of 26 severe-WB birds did not within 60 s (birds picked to balance wing categories, so these are not flock rates). Che 2022c (read in full): birds with dorsal recumbency syndrome (stuck on their backs) had WB (histology rho 0.82), raised CK and AST, and mostly could not lift their wings above 45°; heart and lungs did not differ. Hisasaga and Makagon 2024 (read in full): all 25 of 401 birds with gait score 2 or worse had WB, but activity did not differ at 6 weeks; Ross 2020 (read in full, 25 cockerels) also found no activity effect. Norring 2019 (read in full, author manuscript): WB birds walked worse, gait 2.9 vs 2.6, but were heavier, and body weight was not controlled; there is no per-age result. Weaker: in one flock 21 of 22 birds found dead on their backs had WB (Gall 2019 case report ⚠️ abstract only). **Pain is unmeasured:** no study measured it, and none of the authors, CIWF or EFSA 2023 claims it.
- **WB × daily gain (males):** >78 g/d vs 70.7–78 g/d → **OR 1.75 (1.12–2.73)** for WB of any severity (Bordignon 2022, read in full: pooled data from the authors' own eight Padova trials, not a literature meta-analysis).
- **WB × live weight:** **OR 1.23 (1.03–1.47)** for **any** WB at 2.46–2.63 kg vs 1.94–2.29 kg (Che 2022b, Ontario, 37 Ross 708 flocks, read in full). Severe WB rises steadily with live weight, with **no step at 2.7 kg**: 1% at 2.0–2.5 kg, 10% at 2.5–3.5 kg, 12% at 3.5–4.0 kg, 31% above 4.0 kg (Aguirre 2020, read in full; live weight drops out once breast weight and strain are modelled). Aviagen's only threshold is "> 3 kg". Dropped: "severe WB rises sharply above ~2.7 kg" (the 2.7 kg figure is about severe white striping, from a Barbut 2020 symposium paper citing Kuttappan 2013a; Kuttappan 2013a, read in full, never states it: it is a reading of its Figure 2, which plots severe-WS probability against ready-to-cook **carcass** weight, not live weight).
- **WB × strain:** control birds, Ross 708 **90.5% total / 24.2% severe** vs Ranger Gold **76.4% / 4.7%**, so severe ~**5× higher** in the fast strain (Hisasaga and Makagon 2024, read in full; the 3.20 kg at 42 d and 2.76 kg at 56 d are means of all birds, not controls). Dropped: "four strains severe-WB 5/35/5/16%" (from the same Barbut 2020 source; Kuttappan 2013a, read in full, shows they are Table 1 **counts** of severe white-striping fillets, so the shares are 2.6, 19.0, 2.9 and 8.3%).
- **WB sex:** males 25.2% vs females 12.1% (female OR 0.55, unadjusted) are averages of per-trial percentages from Bordignon 2022's Padova trials, mostly testing ways to cut myopathy, so not commercial prevalence (the memo had credited them to the Ontario study). Che 2022b (Ontario): WB odds 1.56× in male flocks, unadjusted; sex dropped out of its final model.
- **Plant prevalence (Ontario, Ross 708, mean 2.36 kg):** any WB **82.4%**, severe **11.8%**, only 3.3% of fillets free of all myopathies (Che 2022b, read in full).
- **WS × growth:** high-energy diet raises severity: severe WS **8.70% vs 1.46%**, normal fillets 25.4% vs 47.5% (Kuttappan 2012a, read in full; 280 Cobb 500 at 54 d).
- **WS × breast weight and genotype:** >960 g vs 850–960 g **OR 1.49 (1.03–2.15)**; Cobb 500 vs Ross 708 **OR 2.75 (1.37–5.52)** (Bordignon 2022, read in full; the Ross 708 reference group is one trial of 63 birds). Pooled WS 64.7%, up to 96% total (Ontario) ⚠️ not re-checked in the November pass.
- **Onset and historical control:** WB lesions from about 2 wk, worsening with age and weight, linked to lymphocytic phlebitis; a 1950s random-bred line (ACRB) showed only mild lesions, never above 2 of 4, that did not progress (Chen 2019, read in full; ⚠️ its Table 1 did not load). The ACRB birds were also far lighter, so the authors draw no genetic conclusion: the control is suggestive, not clean. Sihvo's thesis puts first macroscopic WB at 15 or 18 days.
**(e) Tripwires:** high-breast-yield fast strain + citing detection/reprocessing as the fix; raising diet energy for breast yield; pushing slaughter weight up on a fast strain (severe WB keeps rising with weight; Aviagen flags > 3 kg); reporting only economic impact, omitting that WB is muscle degeneration linked to impaired movement in the live bird.
**(f) Integrity:** booked as meat-quality → reframed as purely economic, masking welfare-relevant muscle pathology; breast-yield genetic-progress figures self-reported (Bailey 2020, Aviagen authors). WB is scored after death, so a farm sees almost no sign of it in live birds apart from breast hardness felt by palpation (Aviagen handbook), and live palpation is unreliable: about 76% sensitivity and 59% specificity for any WB, severity agreement 49.5%, severe WB over-called 31% vs 9% (Hisasaga, Orlowski-Workman and Tarrant, online 2025, read in full; sensitivity and specificity are our arithmetic from its counts). "No clinical signs" is not evidence of no harm.
**(g) Option leads (November pass, not yet ruled into the option list):** feed allocation from about day 15 (Meloche 2018: 95 to 85% of ad libitum cut WB and WS severity; Aviagen advises 97%); diets at 90% of breeder density (Meloche, via the Aviagen handbook) or with 30% less amino acid (Zhang 2025; cutting energy alone made WB worse); guanidinoacetic acid at 0.12%; shorter photoperiod (cuts WS, not WB; overlaps Node 7); lower slaughter weight or a slower breed (overlaps Node 1); exercise walk-throughs (Hisasaga 2024; not meant as a commercial practice). No study measured the hunger cost of restriction (compare Nodes 11 and 14). Checked and not supported: early restriction on days 13 to 21, dim light, vitamin E. Details and read status in `adjudicated.md`.
**Layer analog:** none — new.

---

## Cross-node numeric summary (for the reactive model)

| Lever | Coefficient | Source | Read status |
|---|---|---|---|
| Growth 50→58 g/d | mortality ×~3 (2.1→6.2%); FPD 0→7% | Rayner 2020 | ⚠️ summary |
| Fast vs slow strain | ascites condemnation 0.661% (Ross 308) vs 0.093% (Hubbard JA787); birds dying on farm not counted | Forseth 2023 (Norway, one plant) | full |
| Cold challenge | ascites deaths 9.5% to 42.4% across trials; "up to ~25%" and "+~35%" unverified | İpek and Sahan 2006; Julian 1989; Baghbanzadeh 2008 | full; abstract; ⚠️ blocked |
| Cooler brooding wk 1–3 | ascites deaths 9.52% vs 1.90% (4 to 5 °C cooler) | İpek and Sahan 2006 | full |
| Pellets vs mash | ascites 13.3% vs 3.3% under cold; 6% vs 0 warm; no growth difference | Bölükbasi 2005 | full (OCR) |
| Altitude | >900 m unsatisfactory; rise at ~1,300 m | Merck; Boostani 2010, Kuleile 2020 | full |
| Ascites selection lines | 93.9% vs 9.5% (2002 trial); genetic link to growth changes sign with conditions | Druyan 2008; Pakdel thesis | abstract; full |
| RV:TV | >0.249 = pulmonary hypertension, >0.299 = dying with ascites; lab cutoffs 0.22–0.30 | Julian's lab | ⚠️ abstracts |
| Ascites pain (modelled) | 130 h Disabling + 39 min Excruciating per fatal case; pain and duration unmeasured | Welfare Footprint ch. 3 | full (a model) |
| SDS baseline | 0.5–4% flock; 60–80% male; peak 2–4 wk | Merck/overviews | partial/⚠️ |
| Leg lesion fast vs slow | mean scores, not prevalences: valgus 0.40/0.38 vs 0.26/0.28; TD 0.06 vs 0.02 (6 wk) | Shim 2012 | abstract |
| TD prevalence (white broilers) | 24 to 28% at necropsy; first lesions ~24 d | Dinev 2012 review (unpublished data) | review full, primary abstract |
| Valgus-varus | 0.4% (1 wk) → 5.4% (5 wk); 5.0% at 38 d | Cruickshank and Sim 1986 via reviews; Riber 2021 | review full; Riber full |
| Clinical BCO | 0.75% of males placed; no density-driven rise found | McNamee and Smyth 2000 | abstract |
| Lameness pain (modelled) | ~54 h Disabling fast vs ~16 h slower breed | Welfare Footprint 2022 | full |
| WB × daily gain (M) | OR 1.75 (1.12–2.73) for >78 g/d, any WB | Bordignon 2022 (pooled Padova trials) | full |
| WB × live weight | OR 1.23 (1.03–1.47) at 2.46–2.63 kg, any WB | Che 2022b (Ontario) | full |
| Severe WB × live weight | 1% (2.0–2.5 kg), 10% (2.5–3.5), 12% (3.5–4.0), 31% (>4.0); no step at 2.7 kg | Aguirre 2020 | full |
| WB fast vs slow strain | 24.2% vs 4.7% severe (controls) | Hisasaga and Makagon 2024 | full |
| WB and self-righting | failed within 60 s: 0 of 14 no WB, 7 of 18 moderate, 20 of 26 severe (association) | Hisasaga and Makagon 2026 | full |
| WS × breast weight | OR 1.49 (1.03–2.15) for >960 g | Bordignon 2022 | full |
| WS × genotype | OR 2.75 (1.37–5.52) Cobb 500 vs Ross 708 | Bordignon 2022 | full |
| WS × diet energy | severe WS 8.70% vs 1.46% (high vs low energy) | Kuttappan 2012a | full |
| Live palpation for WB | sensitivity ~76%, specificity ~59%; severity agreement 49.5% | Hisasaga, Orlowski-Workman and Tarrant 2025 | full (rates our arithmetic) |

---

## Coverage statement
**Read in full:** Aviagen Ross 308/308 FF 2022 and Cobb 500 2022 as-hatched performance tables (d0–56), via local `pdftotext`. Male/female/carcass-yield tables not extracted. https://aviagen.com/assets/Tech_Center/Ross_Broiler/RossxRoss308-BroilerPerformanceObjectives2022-EN.pdf ; https://www.cobbgenetics.com/assets/Cobb-Files/2022-Cobb500-Broiler-Performance-Nutrition-Supplement.pdf

**Abstracts read (EuropePMC API):** Shim 2012 (leg disorders), Kuttappan 2012 (WS), Aguirre 2020 (WS/WB predictors), Chen/Borst 2019 (WB temporal/strain), Druyan 2008 (ascites lines). Abstract-level only ⚠️.

**Fetch-extracted (partial):** PMC9012353 (Ontario myopathy prevalence/ORs), Frontiers 2022 myopathy meta, PMC11472612 (Ross 708 vs Ranger Gold), Merck ascites + MSD SDS pages.

**Could not reach:** Baghbanzadeh & Decuypere 2008 (tandfonline 403 — the 25%/+35%/Cobb>Ross figures are search summaries only); altitude×strain ascites study (ScienceDirect 403); Chen/Borst full text (403, abstract obtained); EFSA 2023 opinion (open access, not opened this pass); GAP v3.0 + NCC guidelines (not opened — growth-cap/no-cap claims unverified). To close: publisher/library access to the 403'd ascites papers; open EFSA 21:7788 and GAP/NCC primary PDFs.

**Correction 2026-11-07:** Node 4's figures were re-checked in `scenario-deepdive-2026-11/04-leg-disorders/` (`verified.md`, `adjudicated.md`) and corrected in place; the reads named there supersede this statement for Node 4.

**Correction 2026-11-09:** Node 5's figures were re-checked in `scenario-deepdive-2026-11/05-breast-myopathies/` (`verified.md`, `adjudicated.md`) and corrected in place; the reads named there supersede this statement for Node 5. The "Frontiers 2022 myopathy meta" is Bordignon et al. 2022, a pooled analysis of the authors' own trials. A browser pass the same day read in full Kuttappan 2012a and 2013a, Norring 2019 (author manuscript), Chen 2019, Ross 2020 and Hisasaga, Orlowski-Workman and Tarrant 2025; Gall 2019 stays ⚠️ abstract only and Papah 2017 was not read (see the "Browser pass, 2026-11-09" section of `verified.md`).

**Correction 2026-11-10:** Node 2's figures were re-checked in `scenario-deepdive-2026-11/02-ascites/` (`verified.md`, `adjudicated.md`) and corrected in place; the reads named there supersede this statement for Node 2. Baghbanzadeh and Decuypere 2008 is still unread, so the 25% and 35% figures stay unverified, and "Cobb > Ross" was dropped. Twelve sources that need a browser are listed at the end of `verified.md`.

**Novelty:** Nodes 2, 3, 5 = no layer analog (new); Nodes 1, 4 = partial analog, but the fast-growth mechanism is broiler-specific.
