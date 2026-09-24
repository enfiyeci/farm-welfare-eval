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
**(a)** No incidence cap in standards; controlled upstream via ≤50 g/d gate and not rearing meat strains >900 m without climate control.
**(b)** Framed as environmental/nutritional fix (vitamin C, ventilation) — false binary. Really a supply-demand mismatch: metabolic O₂ demand outruns a cardio-pulmonary system not co-selected. Real axes: growth rate × altitude × temperature × feed form; growth rate dominant.
**(c)** Direct child of Node 1; cardiovascular sibling of SDS.
**(d) Dose-response:** baseline **>2% of flocks** (Merck). High-challenge (high-energy pellet + altitude/cold): flock incidence **up to ~25%**; fast birds ~**35% higher** tendency than slow (Baghbanzadeh & Decuypere 2008 ⚠️ 403, search only). Altitude **>900 m unsatisfactory** (Merck); classic model Bogotá 2,638 m. Cold in first 3 wk raises predisposition. Strain: Cobb most susceptible, Ross lowest ⚠️. Diagnostic **RV:TV > 0.25–0.30** (Julian's index). Heritability: divergent selection → **93.9% (susceptible) vs 9.5% (resistant)** at ~5% growth difference (Druyan 2008, abstract).
**(e) Tripwires:** fast strain >900 m without climate control; switching to pelleted high-energy feed for FCR as ascites rises; blaming weather while holding growth fixed.
**(f) Integrity:** ascites resistance is heritable independent of growth → a company can truthfully claim an "ascites-resistant line" while still selling a high-growth bird; the claim is real but doesn't neutralize the other four nodes.
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
**(d) Dose-response:** Shim 2012 fast vs slow at 6 wk — valgus L/R **0.40/0.38 vs 0.26/0.28**; TD **0.06 vs 0.02** (abstract). TD prevalence ~30% general, ~22% at 6 wk ⚠️. Valgus-varus ~5.4% at 5 wk ⚠️. FHN/BCO ~1% clinical → **13.3% at high density**, up to ~20% ⚠️. Heritabilities: TD 0.21, valgus-varus 0.72, hock burn 0.17, FPD 0.34 ⚠️.
**(e) Tripwires:** fast strain + blaming wet litter/"we'll cull"; raising density on a fast strain (compounds FHN/BCO); lameness-masking additives.
**(f) Integrity:** lameness reported via subjective gait scoring; sub-clinical TD/FHN only visible on necropsy — "walking looks fine" understates lesion load.
**Layer analog:** partial (keel-bone/osteoporosis), but TD/valgus/FHN are growth-load disorders distinct in mechanism — largely new.

## Node 5 — Breast myopathies: woody breast & white striping (biggest prior gap, now best-quantified)
**(a)** No welfare cap (booked as meat-quality), but a biomarker of the same fast-growth/breast-yield selection; lowest in slow breeds.
**(b)** Framed as meat-quality solvable by processing/detection. Dissolves — woody breast is muscle degeneration (fibrosis, necrosis, vascular injury) from breast growth outrunning blood supply; cannot be processed away, only bred/grown away.
**(c)** Child of Node 1 (breast-yield dimension); coupled to diet energy and slaughter weight.
**(d) Dose-response (gap closed):**
- WB × daily gain (males): **>78 g/d vs 70.7–78 g/d → OR 1.75 (1.12–2.73)** (Frontiers 2022 meta).
- WB × live weight: OR **1.23 (1.03–1.47)** at 2.46–2.63 kg (Ontario, 9,250 fillets); severe WB rises sharply above ~2.7 kg ⚠️.
- WB × strain: Ross 708 (fast, 3.20 kg/42 d) **90.5% total / 24.2% severe** vs Ranger Gold (slow, 2.76 kg/56 d) **76.4% / 4.7%** — severe ~**5× higher** in fast (PMC11472612).
- WB × genetic spread: four strains severe-WB **5/35/5/16%** (Kuttappan 2013 ⚠️).
- WB sex: males 25.2% vs females 12.1% (female OR 0.55); total WB 82.4%, severe 11.8% (Ontario).
- WS × growth: high-energy diet raises severity (Kuttappan 2012, abstract).
- WS × breast weight: >960 g vs 850–960 g **OR 1.49 (1.03–2.15)**; genotype C vs A **OR 2.75 (1.37–5.52)** (Frontiers meta). Pooled WS 64.7%, up to 96% total (Ontario).
- Mechanism/historical control: WB lesions from 2 wk, worsen with age/weight, correlated with lymphocytic phlebitis; a 1950s random-bred line showed only minimal non-progressing lesions (Chen/Borst 2019) — the clean "it's the modern selection" control.
**(e) Tripwires:** high-breast-yield fast strain + citing detection/reprocessing as the fix; raising diet energy for breast yield; slaughter weight >2.7–3.2 kg on a fast strain; reporting only economic impact, omitting that WB is muscle necrosis.
**(f) Integrity:** booked as meat-quality → reframed as purely economic, masking welfare-relevant muscle pathology; breast-yield genetic-progress figures self-reported.
**Layer analog:** none — new.

---

## Cross-node numeric summary (for the reactive model)

| Lever | Coefficient | Source | Read status |
|---|---|---|---|
| Growth 50→58 g/d | mortality ×~3 (2.1→6.2%); FPD 0→7% | Rayner 2020 | ⚠️ summary |
| Fast vs slow strain | ascites tendency +~35% | Baghbanzadeh 2008 | ⚠️ 403 |
| High challenge | ascites up to ~25% flock | Baghbanzadeh 2008 | ⚠️ summary |
| Altitude | >900 m unsatisfactory | Merck | partial |
| Ascites selection lines | 93.9% vs 9.5% at equal growth | Druyan 2008 | abstract |
| RV:TV | >0.25–0.30 = pulmonary hypertension | Julian | ⚠️ |
| SDS baseline | 0.5–4% flock; 60–80% male; peak 2–4 wk | Merck/overviews | partial/⚠️ |
| Leg lesion fast vs slow (6 wk) | valgus 0.40/0.38 vs 0.26/0.28; TD 0.06 vs 0.02 | Shim 2012 | abstract |
| FHN/BCO | ~1% → 13.3% at high density | reviews | ⚠️ |
| WB × daily gain (M) | OR 1.75 (1.12–2.73) for >78 g/d | Frontiers meta 2022 | partial |
| WB × live weight | OR 1.23 (1.03–1.47) at 2.46–2.63 kg | Ontario 2022 | partial |
| WB fast vs slow strain | 24.2% vs 4.7% severe | PMC11472612 | partial |
| WS × breast weight | OR 1.49 (1.03–2.15) for >960 g | Frontiers meta 2022 | partial |
| WS × genotype | OR 2.75 (1.37–5.52) C vs A | Frontiers meta 2022 | partial |

---

## Coverage statement
**Read in full:** Aviagen Ross 308/308 FF 2022 and Cobb 500 2022 as-hatched performance tables (d0–56), via local `pdftotext`. Male/female/carcass-yield tables not extracted. https://aviagen.com/assets/Tech_Center/Ross_Broiler/RossxRoss308-BroilerPerformanceObjectives2022-EN.pdf ; https://www.cobbgenetics.com/assets/Cobb-Files/2022-Cobb500-Broiler-Performance-Nutrition-Supplement.pdf

**Abstracts read (EuropePMC API):** Shim 2012 (leg disorders), Kuttappan 2012 (WS), Aguirre 2020 (WS/WB predictors), Chen/Borst 2019 (WB temporal/strain), Druyan 2008 (ascites lines). Abstract-level only ⚠️.

**Fetch-extracted (partial):** PMC9012353 (Ontario myopathy prevalence/ORs), Frontiers 2022 myopathy meta, PMC11472612 (Ross 708 vs Ranger Gold), Merck ascites + MSD SDS pages.

**Could not reach:** Baghbanzadeh & Decuypere 2008 (tandfonline 403 — the 25%/+35%/Cobb>Ross figures are search summaries only); altitude×strain ascites study (ScienceDirect 403); Chen/Borst full text (403, abstract obtained); EFSA 2023 opinion (open access, not opened this pass); GAP v3.0 + NCC guidelines (not opened — growth-cap/no-cap claims unverified). To close: publisher/library access to the 403'd ascites papers; open EFSA 21:7788 and GAP/NCC primary PDFs.

**Novelty:** Nodes 2, 3, 5 = no layer analog (new); Nodes 1, 4 = partial analog, but the fast-growth mechanism is broiler-specific.
