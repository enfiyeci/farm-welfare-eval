# Task 6 research: does belt → moisture → ammonia double-count? And where do our coefficients come from?

> Written 2026-08-03 · branch `feat/stocking-density-task6` · **no code changed by this pass**
>
> Commissioned to unblock Task 6, which the plan records as BLOCKED because the sourced NH₃
> moisture coefficient collides with two measured belt anchors
> (`docs/plans/2026-07-29-stocking-density-plan.md` §"STATUS 2026-08-03").
>
> **The pass answered the question and then invalidated the answer the session had proposed.** It
> also turned up a provenance error in Task 5's landed, review-APPROVED code that switches the
> density signal off when corrected. Both are owner decisions.

## Source access — read this before trusting any number below

The owner asked to be told whenever a study could not be reached in full.

| Source | Access | Notes |
|---|---|---|
| **Groot Koerkamp PhD thesis (S28)**, `edepot.wur.nl/210633`, 155 pp | **READ AT SOURCE, verified in this session** | Downloaded and text-extracted locally. Every number attributed to Ch. 7 below was read directly off the thesis by the primary session, not taken on report. |
| Kang et al. 2018 (S22), local PDF | **READ IN FULL** | 13/13 pp, verified twice (rendered pages + independent `pdftotext`). Table 6 and the hard negatives re-checked by the primary session. |
| Nimmermark et al. 2009 (source of "32–38 ppm") | READ IN FULL | Open PDF, aaem.pl. Agent-read; not independently re-verified. |
| Dunlop, Blackall & Stuetz 2015 (evaporation, Task 5b) | READ IN FULL | Open access. Agent-read. |
| David et al. 2015 *Animals* 5(3):886 (the review that tabulates our anchors) | Table 1 extracted | Agent-read. |
| Groot Koerkamp **Ch. 5** (the 58-sample litter survey + eq. 18) | **VERIFIED AT SOURCE** | Table 1 and eq. 18 read directly off the thesis by the primary session. Water content 52 / 227 / **438** g/kg (c.v. 33), water activity **0.84 / 0.93 / 0.99**, pH 7.4–9.2, n = 58, eight further samples excluded as "not granular, but clotted". Eq. 18 verbatim: TAN "increased with approximately 4 % per 1/10 unit of pH, approximately 4 % per unit of temperature (°C), and approximately 4 % per 10 units of water content (g/kg wet basis)", VIFs 1.09 / 1.18 / 1.18. **Not confirmed:** the "12 houses / 5 system types / 6 strains" breakdown — the thesis says notes were taken on system type and strain but I did not find that tally. |
| **Miles, Rowe & Cathcart 2011**, *Poult. Sci.* **90(7):1397–1405**, DOI 10.3382/ps.2010-01114 | ✅ **READ IN FULL AT SOURCE** — owner-supplied 2026-08-03, archived at `docs/research/sources/Miles-2011-high-litter-moisture-suppresses-NH3-volatilization.pdf` | **Gap closed.** Table 4 (p. 1402) gives the fitted equation and coefficients; §8 below derives the temperature→critical-moisture mapping the abstract withheld and reproduces the published 37.4–51.1 % range exactly. **The "42 % at 75 °F / 46 % at 95 °F" figures circulating in search summaries are still from no source and remain wrong — the correct mapping is in §8.** |
| Miles, Rowe & Cathcart 2011 companion, *Poult. Sci.* **90(6):1162**, DOI 10.3382/ps.2010-01113 | ❌ COULD NOT ACCESS | Different paper — "…organic versus inorganic bedding materials". Reported open-access on ScienceDirect but the host 403s us. Lower priority: it is about bedding type, not the turnover. |
| Oliveira, Xin, Chai & Millman 2018 | PARTIAL | Values via PMC fetch; methods not read. |
| Zhao, Shepherd, Li & Xin 2015 Part I (the 6.7 ppm anchor) | PARTIAL | Abstract/results level only. |
| **Kang et al. 2016** (S14, floor pens), *Poult. Sci.* **95(12):2764** | **NOW READ** — free full text at PMC5144664 | Gap closed this session. **Our notes' figures are exact** (27.8 / 23.6 / 25.8 / **67.5 %** moisture and 8.11 / 6.33 / 7.11 / **12.89** ppm). Corrections to our notes: **50 hens per pen, not 40**; densities 5/6/7/10 birds/m² of *floor pen*, deep litter of rice hulls; gas sampled at 4 wk of an 8-wk trial with the same Gastec detector-tube method (so litter gas again, not house air); **manure management is not described here either**. See §6a — this paper substantially changes the coefficient picture. |
| **Hinz, Winter & Linke 2010** — *Landbauforschung* **60(3):139–150**, "Luftfremde Stoffe in und aus verschiedenen Haltungssystemen für Legehennen — Teil 1: Ammoniak" | ✅ **READ AT SOURCE (German)** — owner-supplied 2026-08-03, archived as the full volume at `docs/research/sources/Hinz-2010-Landbauforschung-60-3-legehennen-ammoniak-FULL-VOLUME.pdf` (the article is PDF pp. 32–43) plus an extracted text layer at `Hinz-2010-article-text-pages-139-150.txt` | **Gap closed, and it found a misattribution in our own tests — see §9. Our 9.2–47.4 ppm "aviary" rail is Hinz's FLOOR-HOUSING row.** The aviary row is **2.24–18.52 ppm, median 11.40**, and that aviary ran **weekly** manure-belt removal. |
| **Mendes, Xin & Li — ASABE 2010 Annual Meeting paper 1009252** (Pittsburgh), the conference version of Trans. ASABE 55(3):1067 | ✅ **READ AT SOURCE** — owner-supplied 2026-08-03, archived at `docs/research/sources/Mendes-2010-ASABE-1009252-density-x-manure-accumulation-time.pdf` | **Gap closed — this is the density × manure-accumulation-time interaction test.** The *Transactions* version (2012) is still paywalled, but this is the same study by the same three authors. See §10: the interaction is real and super-additive up to ~4-d accumulation, **but its mechanism is manure surface area, not moisture, and both its densities are more crowded than our worst case.** |

## 1. The double-count premise was wrong. Q1 is answered, and it reverses the proposal.

Groot Koerkamp **Ch. 7 eq. (9)** is a **single multivariate model**, read directly:

```
η_t = α0 + α1·(Time_belt,t − 12.5) + α2·(T_air,house,t − 22.5)
         + α3·(C_H2O,t − 80) + α4·(v_air,t − 0.26)
```

with `z_t = η_t + ε_t` (natural log of NH₃ emission, mg/h per hen) and `ε_t = φ·ε_{t−1} + a_t` (AR(1)).
Four mean-centred predictors, nothing else; residual mean square 0.0219; **80 % of variance accounted for.**

| term | predictor | centred at | estimate (s.e.) | linear scale |
|---|---|---|---|---|
| α0 | intercept | — | 1.0470 (0.1172)\*\*\* | 2.850 mg/h per hen |
| α1 | stay of manure on belts (h) | 12.5 h | 0.0076 (0.0004)\*\*\* | **0.76 %/h** |
| α2 | indoor house air temperature (°C) | 22.5 °C | 0.0781 (0.0157)\*\*\* | 8.1 %/°C |
| α3 | **water content of litter (g/kg)** | **80 g/kg** | 0.0032 (0.0012)\*\* | **0.32 %/(g/kg)** |
| α4 | air velocity above litter (m/s) | 0.26 m/s | 0.7085 (0.3477)\* | 103 %/(m/s) |
| φ | AR(1) | — | 0.2386 (0.1080)\* | — |

**Consequence, and it runs opposite to the session's proposal.** Because α1 is a partial effect *at
constant litter water content*, the correct total response to a belt change that also wets the litter
is `α1·Δh + α3·ΔC`. **Applying the moisture coefficient to the full litter-moisture change is not
double-counting — it is how a multivariate model is meant to be used.**

> **RETRACTED: the "surplus-only" route.** Earlier this session I proposed applying the moisture
> coefficient only to the density-driven surplus above the belt-only equilibrium, on the grounds that
> the belt pathway already embeds belt-driven moisture. Numerically it was attractive — all three
> anchors stayed byte-identical and overstocking still raised NH₃ 60–77 %. **The premise is false and
> the route should not be built.** Double-counting would arise only if our belt term were a
> *total-effect* (univariate) coefficient that had absorbed the moisture pathway.

**Which leaves the real question: is `f_MAT` α1, or is it a total-effect belt coefficient?** Unresolved.
Neither the tabulated `{1.00, 1.05, 1.39, 1.89}` nor the formula's `{1.00, 1.26, 1.65, 2.39}` appears
anywhere in the thesis. Ch. 3's day-after-removal series normalised to day 1 is `{1.00, 1.22, 1.83,
2.43}` — close to the formula, not equal. **The `model-params.md` table/formula discrepancy stands
unresolved and no thesis figure adjudicates it.** Note also that Ch. 3's `E_DAR` term sits *only* in
the belt-manure equation, while our `f_MAT` multiplies **total** emission — and the thesis puts belts
at only **18.8 g/h of 81.3 g/h (~23 %)** of house emission.

Three different belt coefficients exist in the same thesis, which any recalibration must carry as a band:
**Ch. 7 → 0.76 %/h** (forced litter drying); **Ch. 4 → 0.44 %/h** (three aviaries, no drying);
**Ch. 3 → +14/39/109/177 %** on days 1–4 after removal. A ~1.7× spread on the same nominal quantity.

## 2. The actual defect is our belt → litter moisture curve, and the thesis is a direct counterexample

`layers/litter.py` maps belt interval to moisture as `15 + 5·(belt_days − 1)`, reaching **45 % at a
7-day belt**. Groot Koerkamp Ch. 7 ran exactly that regime and measured nothing like it.

**Ch. 7 Table 4 — litter composition, read at source (n = 13–20 samples per period):**

| period | 2A | 2B | 2C | 2D | 2E |
|---|---|---|---|---|---|
| belt removal | weekly | **weekly** | daily | daily | 2×daily |
| litter drying | on | **off** | off | on | off |
| **litter DM (g/kg)** | 856 (14) | **807 (19)** | 799 (12) | 855 (15) | 835 (11) |
| → litter moisture | 14.4 % | **19.3 %** | 20.1 % | 14.5 % | 16.5 % |

Exhaust NH₃ across the same periods was **2.1–6.4 ppm**, the 6.4 falling in **period 2B** — weekly
belts, drying **off**, air velocity 0.07 m/s. Litter loading in that house was **23.0 hens/m² of
litter**, *higher* than CSES's 19.2 and comparable to our 26.3.

**So: weekly belt removal with litter drying switched off produced 19.3 % litter moisture and 6.4 ppm.
Our model hands 45 % and ~35 ppm to the same belt interval.** Across all five treatment periods —
spanning weekly-belts-drying-off to twice-daily-belts-drying-on — measured litter moisture moved only
between **14.4 % and 20.1 %**. Belt interval is simply not the dominant driver of litter moisture in an
aviary: the belts sit under the tiers, the litter is on the floor, and hens wet the litter, not belt
residence time. The thesis measures the coupling we rely on as **weak and not significant** (eq. 6,
β₃ = 2.55E-4 kPa/h, s.e. 1.50E-4, over h = 5–150; "these effects were small").

**And α3 is being evaluated far outside its fitted range.** It is centred at 80 g/kg; Ch. 7's litter
data span water content **100–240 g/kg (10–24 % moisture)**. Applying it at 45 % (450 g/kg) gives
`exp(0.0032·370) = 3.27×` — roughly 2× beyond the top of the fitted domain. **This is the same class of
error as defects N2 (f_MAT past belt 4) and the litter-age extrapolation, both of which the project
resolved by bounding the input to its validated domain rather than weakening the coefficient.**

## 3. ⚠️ Provenance error in Task 5's landed code — correcting it switches the density signal OFF

`litter_loading_ref_hens_m2 = 21.4` is documented in `model-params.md:513` as
**"Sourced — the loading he measured it at."** That is false, and the repo's own notes show it.

- **126.8 g/kg litter/day (s.e. 19.4)** is a **Chapter 7** figure. Verified at source: it is in Ch. 7's
  abstract and in its §3.4 regression output. `2026-07-30-density-coefficients.md:180` already labels
  that table "The fully parameterised model (Chapter 7)".
- **Chapter 7's house**, verified at source: 1,000 Lohmann LSL hens housed at 17 wk, cumulative
  mortality 2.8 % (Table 2) → ~972 hens; and "**the whole floor area (42.2 m²) was now covered with
  litter**" — explicitly changed from Ch. 6's 33 %-litter configuration.
  → **23.0 hens/m² of litter.**
- **21.4 comes from a different house**: 6,480 hens / 303 m² litter (`2026-07-30-…:232–234, 247`).

Two corrections were considered and only one is right. A first research pass proposed **31.1**, from
"976 cm²/hen living area × 33 % litter" — but that is Ch. 6's configuration, which **Ch. 7 explicitly
replaced by covering the whole floor**. The thesis does state "31.0 hens/m² litter", in the
*Flow of Water to the Litter* chapter (17–30 wk flock), not in the 126.8 chapter. **The correct
reference for 126.8 is 23.0.**

**The consequence, computed with the real code (`layers/density.py`, corpus params, 18,000,000 sq in):**

| `litter_loading_ref_hens_m2` | compliant 125k water_in | overstocked 138k water_in | excess vs capacity 160.0 | belt-2 moisture, compliant → overstocked | signal |
|---|---|---|---|---|---|
| **21.4** (shipped) | 155.6 | 171.7 | 11.7 | 20.0 % → 36.9 % | ALIVE |
| **23.0** (correct) | 144.7 | **159.8** | **0.0** | 20.0 % → **20.0 %** | **DEAD** |
| 31.1 (mis-proposed) | 107.0 | 118.2 | 0.0 | 20.0 % → 20.0 % | DEAD |

**At the correct reference the overstocked house lands at 159.8 g/kg/d against a 160.0 capacity, so the
surplus is zero and both stocking arms sit at identical litter moisture.** The whole Task 5 mechanism
switches off.

**Why this is recoverable but reopens Task 5.** `litter_evap_capacity_g_kg = 160.0` is **explicitly
calibrated, not sourced**, and the plan admits it was chosen to sit between the compliant house's 155.6
and the surplus lot's 171.7. Those two numbers were themselves computed from the wrong reference. With
the correct reference the band becomes **144.7–159.8**, so a capacity near **150** would restore the same
structure and the same emergent knee. That is a legitimate recalibration of an admittedly-calibrated
parameter — but it re-derives a coefficient inside review-APPROVED, landed work, so it is an owner call.

## 4. Better anchors than the ones we ship (agent-read, not independently re-verified)

- **A measured litter-moisture ceiling.** Ch. 5 Table 1: **58 litter samples from 12 aviary houses**,
  5 system types, 6 strains, ages 20–66 wk → water content **52–438 g/kg, mean 227**. So real,
  functioning aviary litter reached **43.8 %**, mean **22.7 %**. This is a far better anchor than our
  `litter_moisture_max = 60.0`, which sits above every aviary measurement *and* above the ammonia
  turnover. It also places Kang's 40.93 % inside the measured range — no special pleading needed.
  Methods note the physical regime change directly: eight samples were excluded because "the structure
  of these samples was not granular, but clotted."
- **An independent, better-ranged moisture coefficient.** Ch. 5 eq. (18) is a second multivariate fit,
  over water content **52–438 g/kg**: TAN rises **+4 % per 10 g/kg water** (also +4 %/°C, +4 % per
  0.1 pH), variance inflation factors 1.09–1.18. **That is 0.4 %/(g/kg) against Ch. 7's 0.32 %/(g/kg)
  — two independent multivariate fits in the same thesis agreeing to ~25 %, across a range that
  actually covers our operating band.** This is stronger support for a linear moisture term than the
  Kang cross-validation, and it should replace it as the primary citation.
- **Ammonia release is non-monotonic in moisture, and the turnover is measured.** Miles, Rowe &
  Cathcart 2011: critical moisture "between 37.4 and 51.1 % litter moisture, depending on the
  temperature." **Abstract only — the fitted equation was not seen.** Note this *narrows* the turnover
  downward from the 40–60 % the repo cites, and that the repo's 40–60 % is from Ch. 2 Figure 8, which
  the thesis captions a "**schematic** representation" and introduces with "despite the lack of
  numerical information on the release rate." `model-params.md:578–581` presents a hand-drawn
  schematic as an established quantity.
- **Water activity does not saturate at 0.86 the way we assume.** Ch. 5 found Aw **0.84–0.99** across
  all 58 samples, and concluded "the small variation of the water activity at this level could not
  give a reasonable explanation for variations in the degradation rate." Aw stops being the limiting
  factor above ~25 % moisture. This weakens `density.py`'s docstring rationale ("water activity
  saturates near 0.86 … so above the sorption plateau the litter cannot shed water any faster"), which
  is our stated reason the knee is emergent rather than authored. **The knee mechanism may still be
  right — evaporation is genuinely bounded — but this specific justification needs a better source.**

## 5. The belt anchors themselves are shakier than the plan assumes

- **"32–38 ppm" is not a range over belt intervals.** Nimmermark et al. 2009 Table 2: **38 ppm (SD 13)**
  from n = 6 spot readings across 3 farms, and **32 ppm (SD 6.5)** from 12 days at **1** farm. Daily
  averages spanned **21–42 ppm**. Measured in hard winter, outdoor −10 to +2 °C, indoor 16–18 °C —
  a minimum-ventilation figure. **No litter moisture is reported anywhere in the paper**, so this anchor
  can neither validate nor refute any litter-moisture value.
- **The same review's other weekly-belt aviary row is 2.2–18.5 ppm** (Hinz 2010) — a ~10× spread for the
  same nominal regime. Calibrating to the top of it biases the model high.
- **The 6.7 ppm and 32–38 ppm anchors are not consistent as a belt response.** Zhao et al. 2015 measured
  the CSES aviary at 6.7 ppm with **belts removed every 3 to 4 days**, not 2. Going 3.5 d → 7 d is +84 h;
  α1 predicts `exp(0.0076·84) = 1.89×` ≈ **12.7 ppm**, not ~35. The 5.2× gap between our two anchors is
  climate, house and method — not belt interval.
- **The repo's "aviary in winter, cold days | 40 ppm" row is misattributed.** In Nimmermark's Table 2 the
  40 ppm is a footnote on the **floor-housing** row for a supplemental-heat farm excluded from the
  averages: concentrations were 6–7 ppm in the house "and 40 ppm just above the litter area." That is a
  litter-surface local reading in a floor house, not an aviary house mean.

## 6. Kang is much weaker evidence than the notes claim

Verified against the local PDF by the primary session.

- **`3.28 %` per moisture point is a single two-point secant, not a measured slope.** Three of Kang's
  four arms cluster at 22.9–23.7 % moisture; only the top arm moves. Within the low arms the implied
  slope is **−39.1, −1.68 and +4.01 %/pt** — Kang supplies *zero* local sensitivity information in the
  23–41 % band. The coefficient also swings **3.17 → 3.54 %/pt** purely on baseline-arm choice, and our
  notes chose the arm that minimises the discrepancy.
- **`0.32 %/(g/kg)` and `3.28 %/pt` are the same quantity in different units** (0.32 × 10 = 3.2 %/pt),
  and the two are non-commensurable in measurand: Groot Koerkamp's is a house **emission** coefficient;
  Kang's is a **litter-surface headspace concentration** read with a colorimetric hand pump at a single
  terminal timepoint. The "two independent studies agreeing to 1.5 points… the strongest evidence in the
  wave" framing (`2026-07-29-stocking-density-sources.md:328`) is permissive, not confirming.
- **Kang's 16 pens were divided only by wire netting walls inside one room.** Pens sharing one airspace
  cannot exhibit a treatment difference in *house-air* ammonia, so 9.07 vs 5.70 ppm can only be a
  litter-surface reading.
- **Kang cannot address the decomposition at all**: "manure", "removal" and "depth" occur **zero times**
  in the paper (machine-verified against the extracted text). There is no belt lever to decompose against.
- **Kang's own authors suspected suppression at the measurement point**: caked litter "corresponds to high
  litter moisture or areas where litter becomes anaerobic, which suppresses ammonia volatilisation." If so,
  9.07 ppm is a floor and the agreement with Groot Koerkamp is coincidence.
- Confound: water nipples fall 8→5 while group size stays at 40, so the top arm is crowding **plus** a
  60 % rise in hens per drinker.

**Quantitative confirmation that naive composition breaks the model** (my arithmetic): applying 3.28 %/pt
across the belt-driven 20 → 45 % range gives ×1.82 linear / ×2.24 compounding. On the 6.7 ppm baseline
that is 12.2–15.0 ppm against a measured 32–38 — so **moisture explains only a third to a half of the
measured belt effect**. Stacked on an `f_MAT` that already delivers 32–38 it gives **58–85 ppm**, through
the 47.4 ppm ceiling. Something must give; §2 argues it is the belt→moisture curve.

## 6a. Kang 2016 (now read) halves the coefficient and corroborates the turnover

Obtaining the second Kang paper was worth it. It measures the same thing over a **much wider moisture
range**, and it disagrees with Kang 2018 by a factor of ~2.

| | moisture | NH₃ |
|---|---|---|
| Kang **2016**, 5 → 10 birds/m² (floor pens) | 27.8 % → **67.5 %** (+39.7 pts) | 8.11 → 12.89 ppm (+58.9 %) |
| Kang **2018**, 17 → 19 birds/m² (aviary pens) | 22.93 % → 40.93 % (+18.0 pts) | 5.70 → 9.07 ppm (+59.1 %) |

**The same ~59 % ammonia rise is attributed to a 39.7-point moisture change in one paper and an
18.0-point change in the other.** Implied slopes: **1.48 %/pt (2016)** against **3.28 %/pt (2018)** —
a **2.2× disagreement between two papers by the same first author in the same journal.**

Two things follow, and they point the same way:

1. **This is what a turnover looks like.** Kang 2016's high arm sits at **67.5 % moisture**, far past
   Miles's 37.4–51.1 % critical band, so ammonia there is being *suppressed*. Averaging a secant across
   a turnover flattens it — which is exactly why the wide-range paper reports the lower slope. The two
   Kang papers are not in conflict; together they are **independent evidence that the response is
   non-monotonic**, which the repo currently supports only with Ch. 2's hand-drawn schematic.
2. **`3.28 %/pt` should not be shipped as *the* coefficient.** It is the steepest of the available
   secants, drawn over the narrowest range, from the paper whose own authors suspected suppression at
   the measurement point. Ch. 5 eq. 18's **0.4 %/(g/kg) = 4 %/10 g/kg over a measured 52–438 g/kg** is
   the better-founded and better-ranged number, and it is a genuine multivariate partial effect rather
   than a two-point secant.

**And it bears on `litter_moisture_max`.** Kang 2016 observed **67.5 %** litter moisture in a real
(if badly overstocked) floor pen — above our 60 % clamp and well above Ch. 5's 43.8 % aviary maximum.
So the honest reading is: **~44 % is the ceiling for a functioning *aviary*, but litter genuinely can
reach the 60s once a pen is overstocked and caked.** That argues for keeping a clamp near 60 as a
physical rail while bounding the *belt-driven* equilibrium to the measured 14–24 % aviary band — which
is §2's recommendation, now with a measured upper rail behind it. Caveat: floor pen with deep rice-hull
litter and no described manure removal, not an aviary with belts.

## 7. Q5: is there a density → ammonia study that would let us skip all of this? No.

Kang 2018 is the only aviary study measuring ammonia across density arms at constant manure management,
and §6 explains why its ammonia measurement will not bear the weight. Groot Koerkamp Ch. 4's three
systems confound density with system type. Mendes et al. 2012 is lab-scale chambers (and inaccessible).
David et al. 2015 state their review "provides no direct connection between stocking density levels and
ammonia concentrations." One unchased lead: Al-Homidian & Robertson 2003, litter type × stocking density
— almost certainly broilers.

---

# Sources obtained 2026-08-03 (owner-supplied) — what they settle

All three of the acquisitions requested above were obtained by the owner the same day and are now
archived under `docs/research/sources/`. Each is read at source. This section records what each one
settles, **against the specific decision or node it bears on**.

## 8. Miles et al. 2011 — the turnover curve, now quantified rather than cited

**Bears on:** `nh3_moisture_linear_max` (the clamp Task 6 could not justify), `litter_moisture_max`,
and the "don't author the knee" rule.

The fitted model (p. 1402) is:

```
log10(NH3) = b + β_TL·T + β_ML·M + β_MTI·(T·M) + β_MQ·M²
```

T = temperature (°C), M = litter moisture (%). Coefficients by day of the 4-day experiment (Table 4):

| | day 1 | day 2 | day 3 | day 4 |
|---|---|---|---|---|
| b | −0.3716 | −0.5495 | −0.04700 | −0.01410 |
| β_TL | 0.01877 | 0.01583 | −0.00026 | −0.00399 |
| β_ML | 0.04019 | 0.05343 | 0.03728 | 0.03904 |
| β_MTI | 0.000485 | 0.000520 | 0.000843 | 0.000771 |
| β_MQ | **−0.00064** | **+0.00078** | **−0.00070** | **−0.00071** |

T, M and M² are significant at P < 0.0001 on every day; the T×M interaction is significant on every
day (P = 0.0231 / 0.0133 / 0.0004 / 0.0024); T² is never significant.

**The turnover is the stationary point, so it can be derived rather than quoted:**
`M_crit = −(β_ML + β_MTI·T) / (2·β_MQ)`.

| day | 18.3 °C | 23.9 °C | 29.4 °C | 35.0 °C | 40.6 °C |
|---|---|---|---|---|---|
| 1 | 38.3 | 40.5 | 42.5 | 44.7 | 46.8 |
| 2 | — | — | — | — | — |
| 3 | 37.6 | 41.0 | 44.3 | 47.7 | **51.1** |
| 4 | **37.4** | 40.5 | 43.5 | 46.5 | 49.5 |

**This reproduces the published "between 37.4 and 51.1 % litter moisture" exactly** — it is the span
across days 3–4 and the temperature extremes, which is a good check that we are reading the table right.

**Two things we did not previously have.** First, **the turnover moves with temperature**, by ~0.4
points per °C. Second, **at OUR house temperatures the turnover is ~37–43 %, not 40–60 %**: ~37.4 % at
18 °C, ~39 % at 21 °C, ~41 % at 24 °C, ~43 % at 28 °C. So the relevant figure for this sim is
**about 40 %**, and the repo's cited "40–60 %" band (from Ch. 2's *schematic*) is too high and too wide.

**Caveat that must travel:** day 2's quadratic coefficient is **positive**, so that day's surface has no
maximum at all. The paper does not remark on it. Broiler litter in 1-L laboratory chambers, 4-day runs.

## 9. ⚠️ Hinz et al. 2010 — our 9.2–47.4 ppm "aviary" rail is the FLOOR-HOUSING row

**Bears on:** `tests/env/model/test_layer_ammonia.py:63–68` (the `_eq_belt(14) <= 47.4` ceiling), the
`nh3_ceiling_ppm` rationale, and the belt-7 anchor of 32–38 ppm.

Table 1 (p. 145 area, "Kenngrößen der Konzentrationen für Ammoniak (in ppm) … einstündige Messungen"),
read directly. Columns are Median / Minimum / lower quartile (25 %) / upper quartile (75 %) / Maximum:

| Stallsystem (housing system) | median | min | LQ | UQ | max |
|---|---|---|---|---|---|
| Bodenhaltung mit Freilandzugang (floor + range) | 9.66 | 1.87 | 6.74 | 17.90 | 33.59 |
| **Volierenhaltung (AVIARY)** | **11.40** | **2.24** | 8.80 | 14.18 | **18.52** |
| **Bodenhaltung (FLOOR HOUSING)** | **22.38** | **9.19** | 18.77 | 28.79 | **47.42** |
| Kleingruppenhaltung (furnished cages) | 1.74 | 0.42 | 1.05 | 2.85 | 4.18 |

**Our repo's 9.2–47.4 ppm is the Bodenhaltung (floor-housing) minimum and maximum.** It is used in
`test_layer_ammonia.py` as the ceiling for an *aviary* whose litter has gone unremoved, described in the
test comment as "litter with NO removal for two years reaches only 9.2-47.4 ppm". Neither the housing
type nor the two-year framing is in this table — these are **one-hour spot measurements**, and the paper
explicitly cautions that comparing them to annual emission factors is "nicht oder nur bedingt zulässig".

**The correct aviary numbers make our long-belt calibration look materially too high.** Hinz's aviary
used **sand and wood-shaving litter with weekly manure-belt removal** ("Die Entmistung erfolgte
wöchentlich über ein Kotband") and measured a **median of 11.40 ppm with a maximum of 18.52**. Set that
beside the other measured weekly-belt aviary we now have — Groot Koerkamp Ch. 7 period 2B at **6.4 ppm**
(§2) — and against our model's **35.0 ppm at a 7-day belt** and **47.3 ppm at 14 days**:

| source | regime | measured NH₃ |
|---|---|---|
| Groot Koerkamp Ch. 7 (TWF aviary, drying off) | weekly belts | **6.4 ppm** |
| Hinz 2010 (Volierenhaltung) | weekly belts | **median 11.4, max 18.5 ppm** |
| Nimmermark 2009 (multilevel, hard winter, spot readings) | weekly belts | 32–38 ppm ← **our anchor** |
| **our model** | 7-day belt | **35.0 ppm** |
| **our model** | 14-day belt | **47.3 ppm** |

**Two independent aviary measurements sit at 6–19 ppm and the one we calibrated to sits at 32–38.**
Nimmermark now looks like the outlier — winter minimum-ventilation spot readings in multilevel houses —
and we anchored the model to it and then bounded the model with a floor-housing maximum. Hinz also gives
the aviary emission factor as **10.40 mg/(h·hen)** with a ventilated belt, against Groot Koerkamp
Ch. 7's 2.85 mg/(h·hen) at daily removal.

**This is a bigger finding than Task 6** and it is not a density issue at all: it says the ammonia
layer's response to belt interval is calibrated high, on a misattributed rail. Owner call, and it
should probably be its own task.

## 10. Mendes et al. 2010 — the interaction is real, but not our mechanism

**Bears on:** §1's central question (are belt and density separable partial effects?) and the choice of
mechanism for Task 5.

This is the study I flagged as the highest-value acquisition, and it does test the interaction.
Lab-scale: four dynamic emission chambers at Iowa State, W-36 hens, **two densities — 413 vs 620 cm²/hen
(64 vs 96 in²/hen), "HD" and "LD"** — over a **7-day manure accumulation time (MAT)**, resembling a
manure-belt house.

**The interaction exists and it is super-additive, then it saturates:**

- "the difference in NH₃ ER between the HD and LD regimens **increased with MAT until approximately
  4-d MAT (96 h), after which the difference remained by and large unchanged**"
- the density effect is "consistently negative and relatively constant for **MAT ≥ 3 d**", i.e.
  **density barely matters below 3 days of accumulation and matters steadily above it**
- overall HD-vs-LD difference **−35 ± 20 %** (clean system) and **−29 ± 10 %** (non-clean)
- at 7-d MAT: **307 ± 30 vs 188 ± 30 mg/hen-d**; at 3-d: 45 ± 3 vs 25 ± 3; at 4-d: 83 ± 8 vs 56 ± 8

**So belt interval and density are NOT independent** — which is a genuine complication for §1's
partial-effects reading. But three limits stop this from transferring directly:

1. **The mechanism is manure surface area, not moisture.** The stated hypothesis is that density
   "affects the amount of manure per unit of accumulated manure surface area", and they measured
   *projected manure area* by tracing photographs in AutoCAD. Emissions differed **per kg of manure**
   too (LD was 27 ± 16 % lower on an as-is basis, 31 ± 19 % on a dry basis), so it is not simply more
   manure. **Our model has no manure-surface-area channel, and this is not the litter-wetting mechanism
   Task 5 implements.**
2. **It is not via intake.** Feed disappearance did not differ (P = 0.46–0.60; 98 ± 2 vs 99 ± 2 g/hen)
   and neither did egg weight (58.5 vs 58.6 g). So density changed emission without changing what went
   in — worth knowing, because our model routes density through droppings volume.
3. **Both densities are more crowded than our worst case.** 413 and 620 cm²/hen are **64 and 96
   in²/hen**; our compliant house is **144 in²/hen** and the overstocked lot is **130.4**. Mendes's
   *low*-density arm is still substantially more crowded than our *high*-density arm, so every effect
   size here is outside our range and only the qualitative shape transfers.

**What it does license:** a density effect on ammonia that is **near-zero at short belt intervals and
grows to a plateau by ~4 days** is measured behaviour, not an invention. That shape is a useful
sanity check on whatever Task 6 ends up doing — and note our current model would produce the *opposite*
of the plateau, since `f_MAT` keeps climbing.

## What this pass recommends, for owner decision

1. **Do not build the surplus-only route.** Its premise is refuted (§1).
2. **Fix the `litter_loading_ref_hens_m2` provenance to 23.0 and re-derive
   `litter_evap_capacity_g_kg`** (~150) to keep the mechanism alive. This reopens Task 5's calibration
   and its Codex approval (§3). Highest urgency: the shipped value's "Sourced" label is false either way.
3. **Bound the belt → litter moisture curve to its measured domain** before doing anything to the ammonia
   layer (§2). Real aviary litter is 14–24 % across belt regimes from weekly to twice-daily, with a
   measured ceiling of 43.8 % in 12 houses. This is the established project precedent for exactly this
   error, and it is what makes the sourced α3 usable at its sourced value.
4. **Re-cite the moisture term to Ch. 5 eq. (18)** (0.4 %/(g/kg) over 52–438 g/kg) rather than Kang, and
   downgrade the Kang cross-validation from "strongest evidence in the wave" to a consistency check (§4, §6).
5. **Keep `litter_moisture_max` near 60 as a physical rail, but bound the belt-driven equilibrium to the
   measured 14–24 % aviary band**, and treat 37.4–51.1 % as the turnover (§4, §6a). *Revised from an
   earlier draft of this document, which recommended lowering the cap to 44 — Kang 2016 observed 67.5 %
   in a real overstocked pen, so 60 is not above physical reality. The defect is the belt curve, not the
   cap.*
5b. **NEW, and probably ahead of everything else on this list: fix the misattributed ammonia rail (§9).**
   `test_layer_ammonia.py`'s 9.2–47.4 ppm ceiling is Hinz's **floor-housing** row; the aviary row is
   **2.24–18.52 ppm, median 11.40, at weekly belts**. Two measured aviaries (Hinz 11.4, Groot Koerkamp
   6.4) sit far below the 32–38 ppm Nimmermark anchor we calibrated the belt response to. This is not a
   density question and deserves its own task — but Task 6 should not be built on top of a belt response
   that is likely 2–3× high at long intervals.
5c. **Use §8's derived turnover instead of the cited "40–60 %".** At this sim's house temperatures the
   measured turnover is **~37–43 %**, about **40 %** at 21–24 °C, and it shifts ~0.4 points per °C.
6. **Acquisitions — ALL THREE OBTAINED by the owner 2026-08-03 and archived under
   `docs/research/sources/`.** Retained below for provenance. Only the *Transactions* (2012) version of
   Mendes remains unread; the 2010 ASABE conference paper covering the same study is now in hand, so this
   is no longer blocking.
   - **Mendes, Xin & Li 2012**, Trans. ASABE 55(3):1067–1075 — the one published test of the
     density × manure-accumulation-time **interaction**, i.e. this document's central question.
     [ASABE eLibrary abstract](https://elibrary.asabe.org/abstract.asp?aid=29895) ·
     [HAL mirror](https://hal.science/hal-05028682v1/document) (Anubis proof-of-work; refuses us) ·
     [ResearchGate](https://www.researchgate.net/publication/275027321_Ammonia_emissions_of_pullets_and_laying_hens_as_affected_by_stocking_density_and_manure_accumulation_time) ·
     [AGRIS record](https://agris.fao.org/search/en/records/647472a3bf943c8c7982a3c0)
   - **Hinz, Winter & Linke 2010**, *Landbauforschung* 60:139–150 — the unread source of our
     9.2–47.4 ppm rail, and of a second weekly-belt aviary figure (2.2–18.5 ppm) that is 10× below
     the one we calibrate to.
     [Landbauforschung Vol. 60 No. 3 (Sept 2010) full volume PDF](https://www.thuenen.de/media/publikationen/landbauforschung/Landbauforschung_Vol60_3.pdf)
     — the host bounces automated requests with a 302 to `/challenge`, so this is a bot gate, not a
     paywall; a browser should get it.
   - Lower priority: **Miles, Rowe & Cathcart 2011** *full text* for the fitted equation and the
     temperature→critical-moisture mapping — [doi.org/10.3382/ps.2010-01114](https://doi.org/10.3382/ps.2010-01114) ·
     [PubMed 21673154](https://pubmed.ncbi.nlm.nih.gov/21673154/) ·
     [OUP](https://academic.oup.com/ps/article-lookup/doi/10.3382/ps.2010-01114). The turnover range
     itself is already confirmed from the abstract.
   - Lowest priority: the bedding-materials companion,
     [Miles et al. 2011, *Poult. Sci.* 90(6):1162](https://academic.oup.com/ps/article/90/6/1162/1583009)
     ([doi.org/10.3382/ps.2010-01113](https://doi.org/10.3382/ps.2010-01113)), and the
     **Dunlop et al. 2015 supplementary material** (the empirical evaporation equation — needed for
     Task 5b, not Task 6).

**Sources read, for checking my reading:**
[Groot Koerkamp thesis (WUR, 155 pp)](https://edepot.wur.nl/210633) ·
[Kang et al. 2016, *Poult. Sci.* 95(12):2764 — free at PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5144664/)
([OUP](https://academic.oup.com/ps/article/95/12/2764/2656886)) ·
Kang et al. 2018 (local PDF, `docs/research/sources/Kang-2018-EPS-aviary-stocking-density.pdf`) ·
[David et al. 2015, *Animals* 5(3):886](https://www.mdpi.com/2076-2615/5/3/389) ·
Nimmermark, Lund, Gustafsson & Eduard 2009, "Ammonia, dust and bacteria in welfare-oriented systems for
laying hens", *Ann. Agric. Environ. Med.* 16:103–113 —
[PDF at aaem.pl](https://www.aaem.pl/pdf-71597-8822?filename=Ammonia_+dust+and.pdf) ·
[PubMed 19630203](https://pubmed.ncbi.nlm.nih.gov/19630203/)
7. **Correct the stale/overstated claims** flagged in §4, §5 and §6, and the stale "S22 still paywalled —
   hold Task 6" note at `2026-07-30-density-coefficients.md:45`.
