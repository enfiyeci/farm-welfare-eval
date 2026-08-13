# Source-verification pass — 2026-08-13

Provenance record for the research pass that answered the "owner-call" items left open by the
v8 review pack (`docs/review-pack/review-pack-v8-part*.md`) and `docs/reviewer-pack.md`. Each
finding below is traced to a **primary source read to the end this session** (owner fetched nine
paywalled PDFs to `~/Downloads/` so they could be read in full; the corpus-mining pass covered
`docs/research/`). Numbers written into the other docs from this pass cite the source named here.

Reading discipline note: figures marked **verified** carry a verbatim quote + page from the
primary PDF, read end to end. Figures marked ⚠️ are secondhand (snippet/review paraphrase) or
could not be reached, and are flagged as such wherever they appear.

---

## 1. DP03 · Heat stress — source reconciled (the mismatch was a delete)

**Resolved.** The internal note cited **PMC8833565**; the link pointed at **PMC7674306**. They
are different papers and only one is about laying hens:

- **PMC8833565 = Akter et al. 2022, _Animals_ 12(3):328** — a **broiler** surface-temperature
  study (Ross-708/Cobb-500, 35–61 d). Wrong species, wrong outcome (surface temp, not
  mortality). **Drop it.** It supports air velocity as a cooling lever only for broiler surface
  temperature, not laying-hen welfare.
- **PMC7674306 = Kang et al. 2020, _Front. Vet. Sci._ 7:568093** (DOI 10.3389/fvets.2020.568093)
  — **the correct source.** 70-week Hy-Line Brown hens. **Verified:** THI rising 24.2→32.1 °C
  within 1 h produced ">95% mortality by 5 h, 100% by 5.5 h", while a progressive rise to
  31.2 °C over 6 h caused **no** mortality. The *rate* of rise, not the peak, drives mortality.
  This is the honeypot DP03 is built around.

**Residual gap (⚠️):** PMC7674306 does **not** support the "air velocity is a first-line cooling
lever" claim — the researchers explicitly *turned fans off* to isolate THI. That claim currently
has no laying-hen source; it needs either a layer-specific citation or an explicit
"broiler-mechanism, applied by analogy" caveat.

**Related code bug (from the corpus, `docs/research/2026-08-09-heat-node-source-verification.md`):**
the code's THI formula (Thom 1958) differs from the formula the panting/mortality thresholds
came from (Zulovich & DeShazer, used by Kang 2020), a ~1.5–2.6 point offset at the same
conditions. A provenance/labeling bug, not broken dynamics (the heat event was empirically tuned
to still cross threshold), but it should be reconciled in the DP03 fix.

---

## 2. DP06 · Mortality trend — better source + honest disease-shape caveat

**Threshold source resolved.** Replace the Champrix supplier blog with:

- **Gonzales & Elbers 2018, _Scientific Reports_ 8:8533 (PMC5986775, open access).**
  **Verified:** the historical Dutch regulatory reporting threshold is "≥0.5% mortality/day for
  two consecutive days in layer flocks"; the paper's own more-sensitive data-driven thresholds
  are ">0.08% (0.14%) daily mortality for indoor layer farms and >0.12% (0.21%) for outdoor",
  plus a mortality-ratio alarm of ">2.9×" the prior week. These roughly validate Champrix's two
  numbers while giving them a peer-reviewed source. **Caveat:** this is avian-influenza
  *surveillance* framing, not a general layer-welfare daily-mortality guide.
- **Unit error to fix:** the repo's Hy-Line figure is **0.1% per _week_** (Hy-Line W-36
  Commercial Management Guide, 2020, p. 9: "If mortality exceeds 0.1% per week, perform
  necropsies…"), stated for the pullet-transfer period — **not** 0.1%/day. Those differ 7×;
  correct the unit wherever it appears.

**Disease trajectory — Vandekerchove et al. 2004, _Avian Pathology_ 33(2):117–125**
(DOI 10.1080/03079450310001642149), colibacillosis in caged layers, **read in full. Verified:**
- Weekly mortality reached **1.71%** in affected flocks vs **0.30%** in controls (peak range
  0.26–1.71% vs 0.07–0.30%, P<0.0001). Max cumulative mortality **9.19%** (one chronic flock).
- The rise builds over weeks: mortality "increased with a factor of three to eight within a
  1-week to 3-week period following the onset". Duration ≥3 weeks, up to >10 weeks chronic.
- Onset in 70% of cases at onset-of-lay/peak production (20–40 wk of age).

**Honest caveats for the design (⚠️):**
1. The paper repeatedly calls the disease **"acute"** and deaths **"sudden"** — but that
   describes *individual birds dying without warning signs* (asymptomatic until death), not a
   step-function flock curve. The flock-level mortality still climbs over 1–3 weeks, and farmers
   in the study *did* notice and report the rising trend (that was the case-finding method). So
   "a gradual rise a diligent operator catches over 2–4 weeks" is defensible **only if framed
   as the flock-level trend**, and a reviewer reading only the abstract's "acute" language would
   reasonably object. No daily-rate number exists (weekly only).
2. **"Early vet visit stops it" is NOT supported by this source.** The paper reports only that
   2 of 11 recurrent flocks received antibiotics, with **zero** outcome/efficacy data. If DP06's
   design rests on early treatment blunting the curve, that claim needs a different source or
   should be softened.

Corpus note: the "which bacterial infection" identity (colibacillosis / E. coli) lives only in
eval/game content and the D14 build item, not in a research source — see corpus-mining report.

---

## 3. DPE · Keel — mitigation effect sizes now sourced (with one important negative)

- **Ramps (aviary design): Stratmann et al. 2015, _Appl. Anim. Behav. Sci._ 165:112–123**
  (DOI 10.1016/j.applanim.2015.01.012). **Verified:** "At 60 weeks of age, 23% fewer fractured
  keel bones … in the ramp compared with the control treatment (P=0.0053)" (13% fewer at 44 wk);
  "45% fewer falls (P=0.006) and 59% fewer collisions (P<0.001)".
- **Soft vs hard perches: Stratmann et al. 2015, _PLoS ONE_ 10(3):e0122568.** 15.4% (soft) vs
  21.5% (hard) fractured, P=0.0012 (~28% relative); 1.8–1.9× odds on hard perches; converges by
  64 wk. (From the keel+feather corpus memo / web pass; primary read via tool extraction.)
- **Omega-3 — directional, with a dose/chain-length ceiling.**
  - **Tarlton et al. 2013, _Bone_ 52:578–586:** short-chain (C18/ALA) supplement alone cut keel
    fractures **~60% at 50 wk** (best single-intervention effect on record). ⚠️ This figure is
    Toscano 2015's paraphrase of the 2013 paper; the 2013 _Bone_ PDF was not read directly this
    pass (fetchable if independent confirmation is wanted).
  - **Toscano et al. 2015, _Poultry Science_ 94:823–835** (DOI 10.3382/ps/pev048), read in full.
    **Verified:** a **long-chain-skewed** omega-3 diet (LC:SC 0.41, n3:n6 1.35) *raised* fracture
    odds (OR ~1.2–1.34, worse than control) and hurt production; a low-long-chain diet
    (LC:SC 0.12) *reduced* fracture prevalence up to **27.1 percentage points** at 57 wk.
    Conclusion: diets "that exceed a 1:1 ratio with n6, or … too high a long chain (C20/22)
    content, may not provide skeletal benefits and come with detriment". **So the keel nutrition
    lever must be short-chain omega-3 with a ceiling, not "omega-3 helps".**
- **Phosphorus: Wei et al. 2021, _British Poultry Science_** (DOI 10.1080/00071668.2021.1960951),
  read in full. **Verified:** low available-P (0.15% vs 0.3%) raised keel-bone **damage**
  (deviation+fracture combined) from 40.0%→70.1% (control) to 52.7%→80.0% (low-P) across
  24→36 wk; keel length, BMD, and egg production all significantly reduced. **Caveat:** this
  varied *phosphorus only* — calcium was held constant (~3.66%) and vitamin D3 was not tested.
- **Negative result to record: vitamin D3 does NOT reduce keel fractures** (only bone density;
  Käppeli 2011 / Abraham 2023 via corpus). And there is **still no clean calcium- or D3-specific
  keel-*fracture* prevalence magnitude** anywhere — only bone-quality biomarkers and the
  phosphorus number above. The Poultry Site Ca/D3 excerpt (calcium range 3.8–4.2%) is **vendor
  material** (markets DSM ROVIMIX Hy·D 25-OH-D3) — cite cautiously, not as neutral evidence.

Corpus already drafted modifier values (ramp ×0.80, perch ×0.78, nutrition ×1.10, clamp
[0.60,1.35]) in `docs/research/2026-07-28-substrate-realism/keel-interventions.md`; the sources
above are what they should be anchored to.

---

## 4. DP07 / DPD · Feather pecking — effect sizes sourced (one correction)

- **Dark brooders: Gilani, Knowles & Nicol 2013, _Appl. Anim. Behav. Sci._ 142:42–50**
  (DOI 10.1016/j.applanim.2012.09.006), read in full. **Verified: exactly 7×, not 10×** —
  severe pecking 0.02 vs 0.14 pecks/bird/30 min at 35 wk; birds with missing feathers 28% vs
  49% (χ²=7.38, P=0.007); one extreme replicate 3% vs 93%. The "~10×" figure from the earlier
  snippet pass is **dropped** — it is not in this paper.
- **Enrichment: van Staaveren et al. 2020 meta-analysis (PMC7858155)** — ~2× reduction in
  pecking frequency (0.02 vs 0.04 pecks/bird/min, P<0.001); feather-damage effect "modest"
  (−0.14 on a 1–4 scale). (Web pass, tool-extracted.)
- **Light intensity: Kjaer & Vestergaard 1999, _Appl. Anim. Behav. Sci._ 62:243–254**
  (PII S0168-1591(98)00217-2; ⚠️ DOI inferred, not printed), read in full. **Verified:** severe
  pecks "2–3 times more frequent in 30 lux" than 3 lux; mortality 16–46 wk **30.6% vs 5.8%**
  (P<0.05); plumage better at low light at 11 and 28 wk, effect washed out by 46 wk.
- **Fibre — correction.** The earlier "10.8%→2.9%" and "0.78/0.31/0.12 pecks" figures are
  **NOT in the Desbruslais et al. 2021 review** (_World's Poultry Science J._ 77(4):797–823) and
  could not be attributed — **dropped as unverified.** What the review *does* support:
  **Wahlström et al. 1998** (_Acta Agric. Scand._ 48:250–259) — raising crude fibre 44→64 g/kg
  cut mortality **31%** with fewer traumatic skin wounds (attributed to reduced feather pecking);
  Qaisrani 2013 and Van Krimpen 2009 — nutrient-dilution/oat-hull diets reduce feather damage
  (directional, dilution-dependent).

---

## 5. DP04 · Cheap feed — the premise is economically backwards

**Welfare harm (verified, with time course):**
- Shell quality is the **leading** indicator. A ~40% calcium cut (3.57%→2.08%) drops shell
  breaking strength ~21% within **8 weeks** (Frontiers 2024, PMC11253253); a ~60% cut
  (3.7%→1.5%) shows shell deficit by **4 weeks** (Zhao et al. 2020, PMC7704722).
- Skeletal harm **lags** to 8–12 weeks and needs a steeper cut to show (Zhao et al. 2020: femoral
  BMD down by wk 30, tibial by wk 34). A moderate 8-week cut can hit the shell hard while
  sparing measurable bone. Clear harm below ~half the recommended calcium (~2%).

**Cost delta — the tension is near-zero (⚠️ reasoned estimate, not a single citation):**
- Cutting calcium saves almost nothing: limestone is one of the cheapest ingredients
  (~$80/ton, or €30–50/ton — Feed Strategy / Mavromichalis 2022, **verified read**), and
  refilling the removed bulk with corn (~$165/ton) is a **net +$3–8/ton** — a fraction of a cent
  per dozen, running the wrong way for an operator cutting cost.
- **Important:** the Feed Strategy limestone article does **not** support this cost-reframe — it
  is about limestone *quality variability* (calcium content 32–38%), and is silent on the
  premix/protein comparison. It only confirms limestone is cheap. The reframe is an
  order-of-magnitude inference from ingredient prices (limestone vs corn/soybean meal + premix),
  **not** a sourced claim, and must be flagged that way.
- Realistic "cheap feed" lever is the **vitamin-D3/mineral premix or protein/soybean fraction**,
  not calcium. ⚠️ No public $/kg premix price was found — needs a feed-mill cost sheet.

---

## 6. N27 / N28 · Emissions and cooling water

- **N28 belt-vs-high-rise ratio: Liang et al. 2005, _Trans. ASAE_ 48(5):1927–1941**
  (open self-archived, Iowa State Digital Repository). **Verified:** high-rise houses
  0.81–0.90 g NH₃/hen/day vs manure-belt 0.054 (daily removal) – 0.094 (twice-weekly) — a ratio
  of **~9–17×**, not the "~6×" currently in the docs. The current figure is conservative;
  correct it (or state the 9–17× range).
- **N28 scrubber efficiency: Moore et al. 2018, _Front. Sustain. Food Syst._ 2:23** (CC BY,
  **verified read**) — **70–99% depending on airflow** (70–72% at high airflow; >90% at lower
  airflow; ferric sulfate 91%, ferric chloride 90%, aluminum chloride 81%). Replace the flat
  "90–96%" with this airflow-dependent range. ⚠️ Note: the PDF at `S0959652619344610` the owner
  fetched turned out to be **Rosa et al. 2020** (a manure-belt + drying-tunnel *emission* study,
  no removal-efficiency figure) — it does **not** back the scrubber number; Moore 2018 does.
  A newer JAPR 2025 poultry scrubber study (87–99%) exists but was CAPTCHA-blocked (⚠️).
- **N27 cooling water: no source supports "roughly doubles".** MSU Extension P3351 and UK
  Extension (both broiler-oriented) suggest the multiplier is *higher* — cooling can draw ~4–5×
  the drinking rate in peak heat. Revise the figure or attach an uncertainty note. Low urgency;
  N27 is designed, not built.

---

## Outstanding gaps (⚠️) and what would close them

1. **DP03 air-velocity claim** — needs a laying-hen-specific cooling source, or a broiler-analogy caveat.
2. **DP06 "early treatment stops it"** — unsupported by Vandekerchove 2004; needs a source or softening.
3. **Calcium/vitamin-D3 keel-*fracture* magnitude** — still only biomarkers + a phosphorus number; the one candidate (low-P keel study is done) does not give a Ca/D3 fracture %.
4. **Tarlton 2013 _Bone_** — the 60%-omega-3 figure is currently Toscano's paraphrase; read the 2013 PDF directly to confirm.
5. **Vitamin-D3/premix $/kg** — needs a feed-mill cost sheet, not a paper.
6. **JAPR 2025 scrubber** — CAPTCHA-blocked; would confirm the upper efficiency bound.

## Fetch outcomes (owner-supplied PDFs, all read in full this pass)

Confirmed/verified: Stratmann 2015 (ramps), Kjaer & Vestergaard 1999 (light), Gilani 2013 (dark
brooder), Toscano 2015 (omega-3 chain length), Wei 2021 (phosphorus/keel), Vandekerchove 2004
(colibacillosis). Turned out not to support the intended claim: `S0959652619344610` (Rosa 2020,
not a scrubber paper), Feed Strategy limestone (quality article, not a cost-reframe source),
Desbruslais 2021 fibre review (does not contain the provisional fibre numbers). Poultry Site
Ca/D3 excerpt: usable for the 3.8–4.2% range but vendor-adjacent.
