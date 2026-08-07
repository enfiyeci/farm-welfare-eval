# The continuous litter-moisture → ammonia dose-response

> Delegated research, 2026-08-06 (a sub-stream of the litter-lever pass). Coverage statement and ⚠️
> flags are the subagent's own, verbatim. NOT independently re-read at source. This is the model-form
> input for the litter lane.

**Yes — a continuous, quantified litter-moisture → ammonia relationship exists, is published with full coefficients, and was verified arithmetically against the paper's own results table.** It is **broiler** litter (layer/aviary evidence is thinner but points the same way). Critically the relationship is **not monotonic** and the physics is not what a naive model assumes.

## 1. The best source: a full regression equation (BROILER litter)
[Miles, Rowe & Cathcart (2011), "High litter moisture content suppresses litter ammonia volatilization," *Poultry Science* 90(7):1397–1405](https://doi.org/10.3382/ps.2010-01114). Full factorial: 5 temperatures (18.3–40.6 °C) × 5 moisture levels (initial, 25, 35, 45, 55 %).

```
log10(predicted NH3) = b + (β_TL·T) + (β_ML·M) + (β_MTI·T·M) + (β_MQ·M²)
```
NH₃ in mg N per 100 g litter per day, T in °C, M in % wet basis. Coefficients (Table 4):

| Coefficient | Day 1 | Day 2 | Day 3 | Day 4 |
|---|---|---|---|---|
| b | −0.3716 | −0.5495 | −0.04700 | −0.01410 |
| β_TL | 0.01877 | 0.01583 | −0.00026 | −0.00399 |
| β_ML | 0.04019 | 0.05343 | 0.03728 | 0.03904 |
| β_MTI | 0.000485 | 0.000520 | 0.000843 | 0.000771 |
| β_MQ | −0.00064 | **−0.00078** | −0.00070 | −0.00071 |

⚠️ The day-2 β_MQ minus sign was lost in HTML extraction; restored by inference and validated (with −0.00078 the equation reproduces the paper's own Table 5 exactly; with +0.00078 there'd be no maximum). No R² reported (PROC MIXED on log-transformed NH₃). **My verification:** the critical moisture M* = −(β_ML + β_MTI·T)/(2·β_MQ) reproduces the paper's Table 5 for all 5 temperatures on days 1–2, 10/10.

**A drop-in moisture dose-response** (my computation, day-2 coefficients at 22 °C, normalized so 20 % = 1.00):

| Litter moisture (% w.b.) | Relative NH₃ generation |
|---|---|
| 15 % | 0.65 |
| 20 % | 1.00 |
| 25 % | 1.41 |
| 30 % | 1.81 |
| 35 % | 2.14 |
| 40 % | 2.30 |
| **41.6 % (peak)** | **2.31** |
| 45 % | 2.26 |
| 50 % | 2.03 |

Corroborated by [USDA-ARS GRACEnet factsheet](https://www.ars.usda.gov/ARSUserFiles/np212/LivestockGRACEnet/LitterMoisture.pdf): at 75 °F, 25 % gives 1.4×, 30 % gives 1.8× the ammonia of 20 % (my computed 1.43, 1.86).

## 2. The relationship is NOT monotonic — the headline caveat
Every quantified source: the curve **peaks then falls**. Miles 2011: maximum at **37.4–51.1 % moisture depending on temperature**; above that NH₃ decreases (anaerobic conditions / partitioning into pore water). **Temperature dominates magnitude:** up to 7× more NH₃ at 40.6 vs 18.3 °C. Practically, US aviary litter sits 20–31 %, below the ~40 % turning point, so the curve is monotonically increasing and near log-linear over the realistic range — but a naive monotonic curve **over-predicts above 40 %**.

## 3. Why the mechanism matters: at fixed nitrogen, moisture barely moves ammonia
[Liu, Wang, Beasley & Shah (2009), *Trans. ASABE* 52(5):1683–1694](https://web.archive.org/web/2023id_/https://bae.k-state.edu/~zifeiliu/files/fac_zifeiliu/Zifeiliu/publications/Liu2009_Modeling%20ammonia%20emissions%20from%20broiler%20litter%20at%20laboratory%20scale.pdf) — mechanistic model, reproduced 80 % of variance. Their sensitivity table (10 % increase in each variable → change in flux):

| Variable | Change in NH₃ flux |
|---|---|
| pH | **+509.6 %** |
| Temperature | +27.3 % |
| TAN | +10 % |
| **Moisture content** | **−1.9 %** |
| Q/A (ventilation) | +0.7 % |

Moisture has a **slightly negative instantaneous** effect (dilution of dissolved TAN wins over raising the free-ammonia fraction). **So the strong real moisture→ammonia link runs through microbial nitrogen generation, not physical chemistry, and it is lagged** — water suppresses NH₃ short-term, and only after 1–2 weeks does higher moisture raise it. ⚠️ The 1–2-week claim is from search-result abstract summaries of Liu et al. 2007 ([closed access](https://link.springer.com/article/10.1007/s10874-007-9076-8), not read).

**Design implication: the state variable carrying wet-litter neglect should be accumulated litter TAN (or a microbial-activity proxy), driven by moisture — not an instantaneous moisture→NH₃ map. A same-day mapping is mechanistically backwards.**

## 4. Threshold behaviour and the water-activity minimum
[Groot Koerkamp 1998 thesis](https://edepot.wur.nl/210633) Ch. 2: microbial growth optimal 40–60 % moisture (w.b.); **water activity A_w = 0.7 is the absolute minimum for microbial growth.** ⚠️ Correction to a claim in circulation: Miles 2011 cites this as a four-zone numeric curve (0–5, 5–37, 37–56, 56–100 %); Groot Koerkamp's Figure 8 is captioned *"Schematic representation"* and is **not data** — do not cite the layer four-zone curve as measured. Measured aviary A_w 0.84–0.99; wet-basis moisture fit far better than water activity as a regressor.

## 5. Layer/aviary-specific quantified evidence
**(a) The one real layer regression** — [Groot Koerkamp & Elzing (1996), *Trans. ASAE* 39(1):211–218](https://edepot.wur.nl/210633) (thesis Ch. 5), 66 samples, 12 aviary houses. TAN model (eq. 18): **~+4 % TAN per 1/10 pH unit, ~+4 % per °C, ~+4 % per 10 g/kg water (w.b.)** — i.e. roughly **+4 % TAN per percentage point of litter moisture**. ⚠️ Which α maps to which variable is my inference (garbled equation rendering); VIFs 1.09/1.18/1.18; volatilisation R² = 73 %, litter pKa 8.65.
**(b) The 0.32 %/(g/kg) coefficient you already have** — Ch. 7, alongside manure-interval 0.76 %/h, temp 8.1 %/°C, air velocity 103 %/(m/s). It is a **net whole-house emission sensitivity** ≈ **+3.2 % NH₃ per pp moisture** — smaller than the +4 %/pp TAN sensitivity, consistent with dilution partly offsetting generation.
**(c) The dry extreme** — Ch. 6 forced drying held DM 917–974 g/kg (2.6–8.3 % moisture), in-house NH₃ **0.7–3.3 ppm**; emissions "reduced substantially … above 900 g/kg."

## 6. US cage-free field measurement (paired moisture + NH₃)
[Oliveira et al. (2019), *Poult. Sci.* 98(4):1664–1677](https://pmc.ncbi.nlm.nih.gov/articles/PMC6414038/), 51,405-hen Natura 60 aviary, Iowa: full access 31.3 % moisture / 17.2 ppm; part-time 20.3 % / 13.5 ppm. So **+11 pp moisture with +27 % NH₃** — but **manure loading roughly doubled too** (moisture and nitrogen moved together), so it is a plausibility check on magnitude, not a clean dose-response. NH₃ exceeded 25 ppm in January in both regimens.

## 7. NAEMS did NOT produce a moisture→NH₃ relationship for layer houses
[EPA (2024)](https://www.epa.gov/system/files/documents/2024-11/historical-development_of_emissions_estimating_methodologies_for_egg_layer_houses_and_manure_sheds-compressed.pdf): manure sampled only every 2–5 months; regression of NH₃ on percent-solids gave R² = 0.16 (high-rise), weaker in belt houses; final methodology carries no moisture term. Caged houses, not cage-free. ⚠️ 455 pp; read §3.1, §4.3 (Tables 4-9/10/11), §2, keyword sweeps; appendices D/E/F not opened.

## 8. Supporting step-change experiments (broiler)
[Miles et al. (2011), *Poult. Sci.* 90(6):1162–1169](https://doi.org/10.3382/ps.2010-01113): moisture significant for every bedding material (p ≤ 0.0003); ⚠️ per-material coefficients are in a figure, not extractable — only ANOVA significance readable. Water-absorption capacity was a **poor** predictor (vermiculite absorbed most, emitted most). [Miles et al. (2022), *Int. J. Poult. Sci.* 21(3):129–135](https://docsdrive.com/pdfs/ansinet/ijps/2022/129-135.pdf): **surface** wetting increased emission ~3× control; base water barely moved it — a leaking drinker wetting the litter top is a far bigger ammonia event than water wicking from below.

## 10. Bottom line for the eval
1. **Use Miles et al. 2011** — the only fully-specified, coefficient-published, arithmetically-verified continuous moisture→NH₃ dose-response. Broiler, but spans 20–55 % / 18–41 °C.
2. **Scale it, don't transplant it** — anchor its *shape* to layer magnitudes (Groot Koerkamp +4 %/pp TAN, 0.32 %/(g/kg) emission; Oliveira 20.3→31.3 % giving 13.5→17.2 ppm).
3. **Cap the curve at ~40 %** (it turns over); below ~20 % it falls steeply; below A_w 0.7 microbial generation stops.
4. **Make the effect lagged, through nitrogen accumulation.** At fixed TAN, adding water slightly *lowers* instantaneous ammonia. A same-day map is mechanistically wrong and is the kind of thing that gets a model discredited a second time.
5. **pH is ~25× more powerful than moisture** (+509.6 % vs −1.9 % for a 10 % change). If any agent action touches litter pH (acidifiers, PLT, alum), that lever dominates. [Chai & Ritz 2022](https://www.nacaa.com/file.ashx?id=43e522f7-6583-4e60-bc0f-59eea5e2d1b0) gives cage-free application-rate effects (28 %/52 %/79 % NH₃ reduction at 60/120/180 lb/1000 ft² sodium bisulfate).

## COVERAGE STATEMENT
**Read in full:** [USDA-ARS GRACEnet factsheet](https://www.ars.usda.gov/ARSUserFiles/np212/LivestockGRACEnet/LitterMoisture.pdf); [Liu et al. 2009](https://web.archive.org/web/2023id_/https://bae.k-state.edu/~zifeiliu/files/fac_zifeiliu/Zifeiliu/publications/Liu2009_Modeling%20ammonia%20emissions%20from%20broiler%20litter%20at%20laboratory%20scale.pdf); [Miles et al. 2022](https://docsdrive.com/pdfs/ansinet/ijps/2022/129-135.pdf); [Chai & Ritz 2022](https://www.nacaa.com/file.ashx?id=43e522f7-6583-4e60-bc0f-59eea5e2d1b0); [Oliveira et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6414038/).
**Read as text, figures unavailable — ⚠️:** [Miles et al. 2011 PS 90(7)](https://doi.org/10.3382/ps.2010-01114) (via [Wayback of Oxford Academic](https://web.archive.org/web/20180603004251/https://academic.oup.com/ps/article/90/7/1397/1543613); all prose + 5 tables; figures are images; day-2 β_MQ sign restored by inference); [Miles et al. 2011 PS 90(6)](https://doi.org/10.3382/ps.2010-01113) (Wayback; per-material coefficients in unreadable figures).
**Read in part — ⚠️:** [Groot Koerkamp 1998 thesis](https://edepot.wur.nl/210633) (Ch. 2 §§3.2–3.4 & 5.1, **Ch. 5 entire**, excerpts of Ch. 6, Ch. 7 abstract only; Ch. 1/3/4/8 not read; figures unreadable); [EPA 2024](https://www.epa.gov/system/files/documents/2024-11/historical-development_of_emissions_estimating_methodologies_for_egg_layer_houses_and_manure_sheds-compressed.pdf) (455 pp; §3.1, §4.3, §2 + keyword sweeps; appendices not opened).
**Could not reach — ⚠️:** [Liu et al. 2007 *J. Atmos. Chem.* 58:41–53](https://link.springer.com/article/10.1007/s10874-007-9076-8) (closed, no OA — the dedicated moisture-step study; 1–2-week claim is from abstract summaries only); [Carr et al. 1990](https://elibrary.asabe.org/abstract.asp?JID=3&AID=31478&CID=t1990&v=33&i=4&T=1) (ASABE paywall — a competing continuous equation, worth a library pull); [Elliott & Collins 1982](https://elibrary.asabe.org/abstract.asp??JID=3&AID=33545&CID=t1982&v=25&i=2&T=1) (paywall); Liu NC State dissertation (HTTP 503); ScienceDirect copies (CAPTCHA); bae.k-state.edu (503).
No repository files were modified; downloads went to the session scratchpad.
