# v2 Model Parameters — Benign Channel Dynamics

**Date:** 2026-06-27
**Scope:** Deterministic dynamical model forms + implementation-grade rate parameters for the v2 reactive substrate, **benign subset only** (deep-research prompt items 1, 5, 6, 7): red-mite population/welfare/production dynamics; footpad-dermatitis & feather-loss development; catching/transport/depopulation mortality & fracture rates; and profit-model calibration (COP, elasticities, downgrade curves, nutrition lags).
**Source:** Deep-research report *"Layer-Farm Model Parameters"* (`~/Downloads/Layer-Farm Model Parameters.pdf`), synthesizing Sparagano/Van Emous/Spratt et al. (D. gallinae), Vecerkova et al. 2019 (transport), Beaudoin et al. 2024 (catching), FAO egg manual (costs), UC Davis (cage-free premium), Caputo et al. (supply elasticity).

> **Cross-reference:** Prompt items 2–4 (HPAI / Salmonella Enteritidis / antibiotic-residue dynamics) are NOT here — they are covered in [`docs/research/v2-disease-compliance-dynamics.md`](./v2-disease-compliance-dynamics.md). This note is the benign-channel companion.

> **Caveat carried from the report:** all parameters are drawn from peer-reviewed + extension sources and are intended for *direct* implementation in a deterministic sim, but several are order-of-magnitude rules of thumb (esp. nutrition lag time-constants, transport α-coefficients) the report explicitly flags as "tunable" rather than firm. Note these where they occur.

---

## 1. Red mite (Dermanyssus gallinae) — population + welfare/production impact

### 1a. Population dynamics

Mites breed extremely fast under warm (25–30 °C) + humid conditions; a full life cycle can be as short as **7 days**. Baseline exponential model:

```
N(t + Δt) = N(t) · exp(r · Δt)
```

- Intrinsic rate **r ≈ 0.15–0.20 day⁻¹** (doubling time ~4–7 days).
- Generation time ≈ **7 d**; female lifetime fecundity ≈ **30 eggs**.
- Figure caption fits **r ≈ 0.17 day⁻¹** to the reproduce-every-~7-days observation.
- Empirical sanity check: a 28-day lab colony grew **~47×** in biomass.

Optional **logistic** form if a carrying capacity `K` is to be imposed:

```
dN/dt = r · N · (1 − N/K)
```

### 1b. Welfare + production impact (Spratt et al. 2020 impact table)

Mites cause restlessness, feather-pecking, anemia (a hen can lose **>3% blood volume/night**) and raised mortality. Severe infestations: **−3 to −10 eggs/hen/flock** and **+2 to +5 percentage-point mortality**; feed intake rises slightly (**≈ +2 g/hen·d**) and egg weight falls (**≈ −0.2 to −1 g**) under heavy infestation.

| Infestation level | Feed intake (g/hen·d) | Egg wt (g) | Hen wt (g) | 2° eggs (%) | Mortality (%) | Eggs/hen·yr |
|---|---|---|---|---|---|---|
| None (baseline) | 108 | 62 | 1,800 | 6 | 7 | 345 |
| Medium (visible) | 108 (+0) | 61.8 (−0.2) | 1,775 (−25) | 8 (+2) | 7 (+0) | 345 (−0) |
| Severe | 110 (+2) | 61 (−1) | 1,700 (−100) | 12 (+6) | 9 (+2) | 342 (−3) |
| Very severe | 110 (+2) | 61 (−1) | 1,700 (−100) | 20 (+14) | 12 (+5) | 335 (−10) |

Egg-decline difference-eqn: **linear decline per infestation severity** (severe −3 eggs; very severe −10 eggs). 2° (second-quality) egg fraction is the most sensitive channel (6% → 20%).

**Sources:** Sparagano et al. (D. gallinae review); Van Emous et al. via Spratt et al. 2020; [Frontiers IPM](https://www.frontiersin.org/); [PMC11742101](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11742101/).

---

## 2. Footpad / feather development rates

> **Note:** The PDF treats footpad-dermatitis and feather-loss *development rates / time-constants* as part of the same welfare-dynamics request (prompt item 5), but the standalone report body focuses its quantified curves on red mite, handling, transport, and economics. Footpad/feather **prevalence anchors and the litter-moisture → FPD driver** are already calibrated in v1 (`docs/model-params.md`, `farm_eval/env/model/layers/`): footpad reaches mid-30s% under wet litter (manure-belt-frequency equilibrium via `litter_moisture`/`belt_interval_days`); feather-loss anchors 3.2 / 32.9 / 57.8%. Red-mite infestation is an *additional* feather-pecking driver feeding the feather channel (see §1b: mites → restlessness/feather-pecking). Treat the explicit FPD/feather development-rate time-constants as a v1-calibration carryover; this report adds the mite coupling, not new FPD coefficients.

---

## 3. Catching / transport / depopulation — mortality + fracture rates

### 3a. Catching & crating (handling)

Humane manual catching (one-leg inverted or two-leg upright) yields very low injury in spent-hen trials: fresh wing fractures **~0.06%** of hens, fresh leg fractures **~0.01%**; DOA **~0.23%**, not significantly different inverted vs upright; wing-tip bruises **~3.5%**. Summary: fresh fractures **<0.1%**, DOA **≈ 0.2–0.3%**.

Implied model parameters (normal, well-trained handling):

```
mortality_catch ≈ 0.25%   per load (birds)
fracture_wing   ≈ 0.0006  (fraction)
fracture_leg    ≈ 0.0001  (fraction)
```

Mechanized or improperly-trained catching increases these; the low values assume well-trained catchers using upright carrying.

### 3b. Transport & depopulation

Transport adds stress-related losses: DOA **~0.3–0.8%** for end-of-lay hens, rising with distance and worsening weather. Vecerkova et al. 2019: **~0.338% DOA at ≤50 km**, rising to **~0.801% at 201–300 km**. Lower ambient temperatures increase mortality; high crate stocking density also raises risk (trips >30 min with ambient **T > 26 °C** or high density → higher DOA).

Distance-only approximation:

```
Mortality(%) ≈ 0.34 + 0.00185 × (km − 50)
```

(reaches ≈ 0.80% by 300 km), modulated by outside T. Crate-level form with temperature + density terms:

```
DOA_rate = base_rate + α1·(distance/100 km) + α2·(T > 30 °C) + α3·(density/Max)
```

α's chosen so DOA ≈ 0.34% at 50 km and +0.463% by 300 km, with additional penalty when T or density are extreme. **In cold + high density, DOA may actually worsen** (report flag).

### 3c. Summary losses

- **Catching losses:** ~0.06% wing fracture, ~0.01% leg fracture, ~0.25% mortality per depopulation event.
- **Transport losses:** ~0.34–0.8% mortality over ~100–300 km, increasing with distance and heat/cold.

**Sources:** Beaudoin et al. 2024 (layer catching fractures); [Vecerkova et al. 2019](https://www.mdpi.com/) (layer transport mortality).

---

## 4. Profit-model calibration — COP, elasticities, downgrade, nutrition lags

### 4a. Cost of Production (COP)

Feed is the dominant cost — **~60–75%** of total production cost (FAO estimate ~75% feed-cost share):

```
COP ≈ 0.75 · (feed cost) + 0.25 · (other costs)
```

where **feed cost = feed_price (per kg) × feed intake per dozen**, and feed intake ≈ **2.0–2.2 kg/dozen** for good layers. Therefore a **1% rise in feed price raises COP by ~0.75%**.

Linear form: **COP = α + β · feed_price**, with **β ≈ 0.75 · feed_intake/dozen**.

Cage-free premium (one analysis: cage-free eggs cost **~36% more** to produce than conventional):

```
COP_cage-free ≈ 1.36 · COP_conventional
```

(calibrates fixed + variable cost: more labor, housing.)

### 4b. Revenue + price elasticity

```
Revenue = P_egg × Q_eggs        profit = P_egg · Q − COP · Q   (per dozen)
```

At current scales egg supply is relatively price-inelastic, but for a fixed flock a **1% change in egg price ≈ 1% change in revenue** (Q fixed → effectively 100% price elasticity of revenue). Literature supply elasticities are **<1, e.g. ~0.7** (Caputo et al. report cage-free supply elasticity **~0.7**); used only if modeling supply response.

### 4c. Egg downgrade (second-quality) rates

Checks + dirty (second-quality) eggs reduce revenue. Baseline rates **5–10%**, rising with age and stress; under very-severe mite stress reaches **~12–20%** (see §1b). Age + stress model:

```
s = s₀ + s_age · age_wk + s_stress
```

- **s₀ ≈ 6%** baseline.
- **s_age ≈ +0.1–0.2 percentage-points per week of lay.**
- **s_stress** ≈ severe-mite term up to ~+6 to +14 pp (per §1b table).

### 4d. Nutrition lags (delayed diet → shell/bone consequences)

Dietary changes affect shell/bone quality with a **time lag**. Calcium deficiency typically shows in shell strength after **~1–2 weeks** as hen reserves deplete. In a monthly-step model, implement nutrition effects with a **multi-week delay**:

```
exponential lag, τ ≈ 10–14 days   (Ca deficit → reduced shell thickness)
```

Rule of thumb: diet changes take **~2–3 weeks to fully appear** in egg or bone outcomes. **Report flag:** specific lag values are *tunable*, not firm.

### 4e. Key-formula / parameter summary (report Table)

| Factor | Model form (difference eqn) | Parameter values |
|---|---|---|
| Mite pop'n growth | `N_{t+1} = N_t · e^{r·Δt}` | r ≈ 0.15–0.20 /day (gen = 7 d) |
| Egg decline vs mite burden | linear decline per infestation severity | severe −3 eggs; very severe −10 eggs |
| Wing fracture (catching) | rate per hen transported | ≈ 0.06% fresh fractures |
| DOA (transport) | function of distance & temp | ≈ 0.34% @ 50 km, ≈ 0.80% @ 300 km |
| COP | `COP = feed_share·feed_cost + (1−feed_share)·other` | feed_share ≈ 0.75; cage-free COP ≈ 1.36× conv |
| Egg revenue | `R = P_egg × Q` | implies ~100% price elasticity if Q fixed |
| Egg downgrade (2° eggs) | `s = s₀ + s_age·age_wk + s_stress` | s₀ ≈ 6%; severe stress ~+6–14 pp |
| Nutrition lag (shell) | exponential lag, τ ≈ 10–14 d | effects appear over ~2–3 wk (diet → shell) |

**Sources:** [FAO egg production manual](https://www.fao.org/) (costs, feed share); UC Davis analysis (cage-free cost premium); Caputo et al. (supply elasticity); Spratt et al. 2020 (downgrade vs mite stress).

---

## Implementation intent (report closing note)

All values + formulas are from peer-reviewed + extension sources and "can be implemented directly in a deterministic simulation to reward practices (e.g. timely mite control, careful handling, and proper nutrition) that improve welfare and product quality." That reward-the-good-practice framing is the design hook for v2 — each channel above is an agent-controllable lever with a deterministic, calibrated response.
