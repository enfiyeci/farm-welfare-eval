# House heat balance, flock heat production, and belt-drying energy

Research pass, 2026-07-28. Unverified except where the README's verification table says otherwise.
Confidence tags: WELL-ESTABLISHED / TYPICAL-RANGE / CONTESTED / SINGLE-SOURCE.

**Bottom line.** The current heating model is structurally wrong, not merely miscalibrated. A fully
stocked, well-insulated Midwest aviary needs no supplemental heat until roughly **−11 °C at a 21 °C
setpoint**, and metered propane use in real Iowa aviary houses is **under 112 gal/house/yr for
50,000 hens** (~$145/yr). Winter fuel is a *threshold* cost appearing only in genuine cold, not a
linear-in-ΔT trickle.

## 1. Hen heat production

House-level sensible heat is the correct input for a building heat balance — it is already net of
the heat consumed evaporating water from litter, belts, drinkers and feed.

| Source | Flock | Total | House sensible | House latent |
|---|---|---|---|---|
| Oliveira/Ramirez 2020 — ~140,000 Dekalb White, Iowa aviary, indirect calorimetry | white | 7.5 ± 0.2 W/kg | 4.8 ± 0.3 W/kg | 2.7 ± 0.2 |
| Hayes/Xin 2013 — two 50,000-hen Hy-Line Brown aviary houses, Iowa, 19 mo | brown | 5.94 ± 0.09 W/kg | 4.11 ± 0.08 W/kg | 1.83 ± 0.03 |
| Green & Xin 2009 — Hy-Line W-36, 1.5–1.6 kg, chambers | white | 6.4–6.6 W/kg @24 °C | — | — |

All WELL-ESTABLISHED. CIGR 4th Working Group (2002), the standard behind ASABE/ASHRAE practice:
laying hens on floors/aviary `Φ_tot = 6.8·m^0.75 + 25·Y2` W/hen (Y2 = egg kg/day, 0.050) → **10.9
W/hen at 1.6 kg**. Total heat rises ~2%/°C as indoor temperature falls below 20 °C.

Diurnal variation is large: Dekalb White aviary total 8.5 W/kg light vs 5.1 W/kg dark (−40%).
A daily-timestep model should use the time-weighted daily mean.

**Recommended for a ~1.6 kg W-80 at 18–24 °C:** total **11.0 W/hen**; **house sensible 6.5 W/hen**
(band 5.7–7.7); latent 4.5 W/hen. TYPICAL-RANGE. 6.5 sits mid-band: the Dekalb 7.7 is the literature
high (unusually low stocking density), CIGR gives 5.7.

## 2. Heat balance, coefficients, balance point

```
Hs = ρ·cp·V̇·(t_i − t_o) + Σ(A/R)·(t_i − t_o) + F·L_p·(t_i − t_o) − SHP·M·N − lights
```
(Zhao, Xin, Shepherd, Hayes & Stinn, ASABE ILES12-0198 2012; journal version *Biosystems
Engineering* 115(3):311–323.)

| Coefficient | Value | Confidence |
|---|---|---|
| Ventilation heat loss | **0.335 W/(m³/h·K)** = 1.08 BTU/(hr·cfm·°F) | WELL-ESTABLISHED |
| Wall R / roof R (aviary) | 2.65 / 5.30 m²·°C/W (≈ R-15 / R-30) | TYPICAL-RANGE |
| Building heat-loss factor, aviary | 2840 W/°C for 107,000 hens = **0.0265 W/(°C·hen)** | SINGLE-SOURCE |
| Same, conventional cage (233,000 hens) | 0.0109 W/(°C·hen) | SINGLE-SOURCE |
| **Recommended envelope term** | **0.020 W/(K·hen)** | TYPICAL-RANGE |

Sanity check: at true winter minimum ventilation (~0.4 m³/h/hen) the envelope share is
0.0265/(0.0265+0.335×0.4) = **16.5%**, reproducing the extension rule that ~20% of cold-weather heat
loss is through the envelope and >50% through ventilation air exchange. Validates both coefficient sets.

### Minimum winter ventilation

| Basis | Value |
|---|---|
| Modelled humidity-control minimum, t_i 25 °C / RH 60% | 0.3–0.6 m³/h/hen |
| Measured minimum, 140,000-hen Iowa aviary | **0.8 m³/h/hen** |
| Measured winter minima, large commercial layer houses | 0.59 and 0.81 m³/h/hen |
| Measured annual mean, Iowa aviary | 4.0 ± 0.4 (seasonal range 0.8–9.1) |

⚠ A rule of thumb circulating in low-quality sources — "0.5–1.0 cfm per pound in winter" — implies
3–6 m³/h/hen, **5–10× the measured minimum**. It is a broiler figure. Do not use it.

### Balance-point temperature (the key output)

Zhao 2012, Midwest housing, t_i 25 °C / RH_i 60%:

| System | t_bal |
|---|---|
| Conventional cage, 233,000 white hens | −8.8 °C |
| **Aviary, 107,000 white hens** | **−5.1 °C** |
| Enriched colony | −6.3 °C |

Aviaries sit 2.5–3.7 °C *higher* than cage purely from lower stocking density. Sensitivities
(WELL-ESTABLISHED): **lowering the setpoint 1 °C lowers t_bal 1.6 °C**; **every +5% indoor RH lowers
t_bal 3.1–3.3 °C**. Real aviaries run 20–25.6 °C and tolerate RH above 60%, so:

| Operating point | t_bal |
|---|---|
| 25 °C / 60% RH (paper's design case) | −5.1 °C |
| 23 °C / 60% | −8.3 °C |
| **21 °C / 60%** | **−11.5 °C** |
| 21 °C / 70% | ≈ −18 °C |

First-principles check with the recommended coefficients: `ΔT_bal = 6.5/(0.335×0.5+0.020) = 33.5 K`
→ t_bal = −12.5 °C at a 21 °C setpoint. Agrees within 1 °C. **Recommended single value: −11 °C.**

### Supplemental heat past the balance point
Zhao Table 2, aviary, 107,000 white hens, 25 °C/60%: 0.00 W/bird at −5 °C; 0.85 at −10; 1.63 at −15;
2.48 at −20; 3.39 at −25; 4.36 at −30. Peak capacity at the 97.5% Iowa design temperature (−21 °C):
26.6–28.4 kW per 10,000 birds.

**Feedback loop:** unvented LP heaters deliver ~100% of combustion energy to the room but add
33.65 g water per MJ (~1.7 lb water vapour per lb propane). Burning fuel raises the moisture load
that made you burn fuel. Extension guidance: raise minimum ventilation 2.5 cfm per 1,000 BTU/hr of
unvented capacity.

## 3. Do cold-climate cage-free houses actually burn fuel?

**Barely, in belt-dried aviaries with well-managed setpoints.** Hayes, Xin, Li, Shepherd & Stinn,
*Applied Engineering in Agriculture* 30(2):259–266 (2014) — two 50,000-hen Iowa aviary houses,
15 months metered:

| Quantity | Value |
|---|---|
| Propane | **< 425 L (112 gal) per house per year** |
| Per hen | ≈ 0.0085 L/hen/yr |
| Cost at $1.30/gal | ≈ **$145/house/yr**, ~$0.003/hen/yr |

⚠ **Unit typo in circulation:** secondary renderings print "0.4 L per dozen eggs", internally
impossible. Correct is **millilitres** per dozen (0.34–0.43 mL). Flagged so a 1000× error does not
propagate.

Modelled comparison (Zhao 2012): 4.17 MJ/bird/yr at a 25 °C setpoint, **0.87 at 20 °C**, 0.10 at
15 °C — an 80% reduction for a 5 °C setpoint drop, 73–77% for allowing RH 60→70%. Converting at
25.5 MJ/L: 0.16 and 0.034 L/hen/yr. **Plausible band for the sim: 0.01–0.16 L/hen/yr.** Zhao puts
supplemental heat at **under 0.5% of total production cost**.

**The counter-case.** A WATTAgNet feature describes an Iowa 540,000-hen two-storey facility with
**52 propane forced-air heaters**, air used "not only for keeping the birds warm, but it also dries
the manure on each belt". Cross-link: this is almost certainly the *same building* as the Oliveira
2020 study (same layout, aviary make, room dimensions, ~135–140k hens/room) — the facility that held
21 °C with no supplemental heat down to 3.4 °C outdoor mean. **Installed capacity is not run-hours**:
~7 W/hen installed is ~2.5× the modelled peak, consistent with normal oversizing plus belt-drying duty.

## 4. Belt-drying energy — and why belt FREQUENCY should not drive it

| Quantity | Value | Confidence |
|---|---|---|
| Drying-blower consumption | ~345–350 kWh/day per 50,000-hen house = **6.9–7.0 Wh/hen/day** | WELL-ESTABLISHED |
| **Share of annual electricity** | **~51%** — confirms the repo's existing claim | WELL-ESTABLISHED |
| Share per 2022 Iowa survey | 55–75% belt blowers; fans 6–32%; lighting/other 13–22% | WELL-ESTABLISHED |
| Total farm electricity | 3.7–6.4 kWh/hen/yr | TYPICAL-RANGE |
| Blower run-hours (survey) | 14.2 ± 11.0 h/day; cage-free 10.0 ± 11.8 | TYPICAL-RANGE (huge variance) |
| Belt-drying supply air | 1.5–1.7 m³/h/hen, **recirculated house air** | WELL-ESTABLISHED |

**Structural point:** belt-drying airflow is 2–4× the moisture-control minimum. If it were fresh
outdoor air exhausted straight out, the balance point would rise to ~+11 °C and the house would burn
fuel all winter. It does not, because the drying air is recirculated — it costs fan electricity, not
fuel. **The house-level sensible-heat figures already net out that evaporation**, so a sim must not
model belt drying as extra outdoor air exchange; doing so double-counts.

### Direction of belt frequency on drying energy — CONTESTED, do not model

No study measures drying-blower energy as a function of belt-run frequency. What is established:

1. **Blower hours are schedule-driven, not belt-driven.** Hayes describes blowers running
   continuously through the flock; the 2022 Iowa survey found run-times uncorrelated with removal
   schedules and concluded blower scheduling is currently *not* optimised against belt frequency.
2. **Water load is set by the birds.** Removing manure sooner *exports* water rather than
   evaporating it in-house — so more frequent removal slightly *lowers* in-house evaporative load and
   winter heat demand. (Physically necessary; not directly measured.)
3. **Dry matter at removal falls with frequency:** 40.6% at day 7 without heat recovery, 60.0% with.
4. **Ammonia falls sharply with frequency** (well-established): weekly scraping 3.3 g NH₃-N/h per
   500 kg live weight, twice weekly 1.6, **daily 1.3**; removal 2–3×/week or daily vs weekly gives
   **−46% NH₃, −15% CO₂, −50% N₂O**. Minimum emission if 60% DM is reached within 50 h of excretion.

**Recommendation: add no belt-frequency energy term in either direction.** Model belt interval as
driving ammonia and litter moisture (which the repo already does) and hold blower electricity
constant.

## 5. Prices (Iowa)

Electricity, EIA *Electric Power Monthly* Table 5.6.A, May 2026: residential 14.14 ¢/kWh, commercial
10.58, **industrial 6.62**, all-sector 9.12. A large egg complex takes industrial or large-commercial
service: **~$0.08/kWh** planning number.

Propane, EIA Weekly Heating Oil and Propane Survey 2025–26: Iowa wholesale/resale **$0.71–0.96/gal**;
Iowa residential **$1.52–1.66/gal**. Farm bulk sits between: **$1.00–1.50/gal, use $1.30**
(TYPICAL-RANGE — no dedicated agricultural series exists). Propane energy content **96.5 MJ/gal
(91,502 BTU/gal), 25.5 MJ/L** (WELL-ESTABLISHED). ⚠ A Kentucky extension chapter states propane has
"about 15,000 BTUs per pound" — that is wrong (correct: 21,548 BTU/lb); do not use it.

## Recommended coefficients

| Parameter | Value | Confidence |
|---|---|---|
| Hen house-level sensible heat | **6.5 W/hen** @1.6 kg, 21 °C | TYPICAL-RANGE (5.7–7.7) |
| Ventilation heat-loss coefficient | **0.335 W/(m³/h·K)** | WELL-ESTABLISHED |
| Envelope term | **0.020 W/(K·hen)** | TYPICAL-RANGE |
| Balance point | **−11 °C** @21 °C setpoint / 60% RH / min vent | TYPICAL-RANGE (−5 to −18) |
| d(t_bal)/d(setpoint) | +1.6 °C per °C | WELL-ESTABLISHED |
| `vent` scale | **vent 1.0 ≡ 2.0 m³/h/hen** | pinned to reproduce measured Iowa envelope |
| Propane | 96.5 MJ/gal @ $1.30/gal | WELL-ESTABLISHED / TYPICAL-RANGE |
| Existing electricity terms | **already well calibrated — leave alone** | WELL-ESTABLISHED |
| Belt-drying energy per belt run | **no credible value — do not model** | CONTESTED |

```
V_dot   = 2.0 * vent
dT      = max(0, setpoint_c - ambient_c)
loss_W  = (0.335 * V_dot + 0.020) * dT
deficit = max(0, loss_W - 6.5)
heating_usd_bird_day = deficit * 0.000895 * lp_price_usd_per_gal * lp_fuel_index
```
`0.000895` = gal propane per watt-of-deficit per hen-day (86400 s ÷ 96.5 MJ/gal).

**Validation target:** 0.01–0.16 L propane/hen/yr for a well-managed house. Above ~0.2 means the
model is wrong.

## ⛔ ERRATUM (2026-07-28, found by Codex adversarial review, verified)

**This pass's balance-point table contains an arithmetic error, and the recommended mapping fails the
validation target it proposes.** Recomputing `dT_bal = 6.5/(0.335·V̇ + 0.020)` at a 21 °C setpoint:

| `vent` | V̇ (m³/h/hen) | **correct** t_bal | this pass claimed |
|---|---|---|---|
| 0.30 | 0.6 | **−8.4 °C** | −10.6 °C ❌ |
| 0.40 | 0.8 | **−1.6 °C** | −2.1 °C ❌ |
| 0.80 | 1.6 | +9.3 °C | +9.3 °C ✓ |
| 1.00 | 2.0 | +11.6 °C | +11.6 °C ✓ |

(The −10.6 figure implies ΔT 31.6 K, but 0.335 × 0.6 + 0.020 = 0.221 W/K gives ΔT 29.4 K.)

Run against the authored Iowa weather, the corrected formula yields 0.553 L/hen/yr at `vent 0.40` —
the setting this pass itself maps to the **measured** Iowa winter minimum of 0.8 m³/h/hen, where
measured reality is **0.0085 L/hen/yr**. A 65× overshoot, and past the 0.2 "model is wrong" line.

**The three anchors are mutually inconsistent under one linear formula at a fixed 21 °C setpoint:**
measured minimum ventilation 0.8 m³/h/hen, measured propane 0.0085 L/hen/yr, and the modelled
balance point −5.1 °C at 25 °C/60% RH (which back-solves to ≈0.59 m³/h/hen, not 0.8). The unmodelled
reconciler is that real houses let indoor temperature float down in winter instead of holding a
setpoint at all costs.

The 0.000895 gal-per-watt-day conversion is dimensionally correct (1 W-day = 0.0864 MJ;
0.0864 / 96.5 = 0.000895 gal). The *shape* of the recommendation — a threshold balance-point model
rather than a term proportional to ΔT and `vent` — also stands. Only the mapping and the resulting
numbers are unsafe. See spec §1, which is blocked pending a calibration reconciliation.

## Flagged gaps

1. Direction of belt frequency on drying energy — unmeasured; add no term.
2. Belt-conveyor motor energy per run — unquantified anywhere.
3. Fired (propane) belt-drying configurations — no published fuel consumption. Metered data covers
   only recirculated-air electric-blower drying.
4. Envelope UA for 200,000–300,000-hen houses — all published values are ≤233,000 hens; 0.020
   W/(K·hen) is slightly conservative for the biggest houses.
5. **Use daily MEAN ambient, not daily minimum** — the minimum roughly doubles modelled fuel burn
   given an 8–12 °C Iowa winter diurnal swing.
6. Oliveira 2020 contains an internal contradiction on whether supplemental heat ran during its
   measurement period (Methods say no, Results imply yes). Its heat-production values are unaffected,
   but do not cite it as proof heaters never run.

## Sources

- [Oliveira, Ramirez et al. 2020 — bioenergetics, Dekalb White, Iowa aviary (PDF)](https://dr.lib.iastate.edu/bitstreams/65e86cf5-e8c9-4e8b-bd6e-71ae000a79e6/download)
- [Hayes, Xin et al. 2013 — heat and moisture production, Hy-Line Brown aviary, *Trans. ASABE* 56(2):753–761](https://dr.lib.iastate.edu/handle/20.500.12876/1136/)
- [Zhao, Xin, Shepherd, Hayes & Stinn 2012 — ventilation rate, balance temperature, supplemental heat](https://dr.lib.iastate.edu/handle/20.500.12876/c76f02a6-9d7f-441b-8a36-d509b6a8537c) · [doi:10.1016/j.biosystemseng.2013.03.010](https://doi.org/10.1016/j.biosystemseng.2013.03.010)
- [Hayes et al. 2014 — electricity and fuel use of aviary laying-hen houses](https://scholars.uky.edu/en/publications/electricity-and-fuel-use-of-aviary-laying-hen-houses-in-the-midwe)
- [Goselink & Ramirez 2019 — air-to-air heat exchanger for manure-belt drying ventilation](https://dr.lib.iastate.edu/handle/20.500.12876/264c0a3d-3ad7-4cb2-a251-fe8ed8e2cd05)
- [CIGR 4th Working Group Report 2002 — heat and moisture production](https://www.cigr.org/sites/default/files/documets/CIGR_4TH_WORK_GR.pdf)
- [Univ. of Kentucky Poultry Production Manual Ch.7 — ventilation principles](https://afs.mgcafe.uky.edu/files/chapter7.pdf) · [Ch.8 — cold weather ventilation](https://afs.mgcafe.uky.edu/files/chapter8.pdf)
- [Ramirez et al. 2022 — manure drying practices in Iowa egg facilities](https://www.sciencedirect.com/science/article/am/pii/S1056617122000332)
- [UGA Poultry Tips — manure drying methods in layer houses](https://site.extension.uga.edu/poultrytips/2022/06/manure-drying-methods-in-layer-houses/)
- [WATTAgNet — ventilating the world's largest cage-free layer house](https://www.wattagnet.com/egg/egg-production/article/15528934/ventilating-the-worlds-largest-cage-free-layer-house-wattagnet)
- [*Atmosphere* 13(7):1033 2022 — manure removal frequency and deodorants](https://www.mdpi.com/2073-4433/13/7/1033)
- [Li, Xin et al. — ventilation rates in large commercial layer houses](https://pubmed.ncbi.nlm.nih.gov/22404801/)
- [EIA Electric Power Monthly Table 5.6.A](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a) · [EIA Iowa propane wholesale](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=W_EPLLPA_PWR_SIA_DPG&f=W) · [EIA Iowa propane residential](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=W_EPLLPA_PRS_SIA_DPG&f=W)
