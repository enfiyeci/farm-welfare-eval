# Energy and cost of litter drying / air circulation / ventilation in poultry houses

> Delegated research, 2026-08-06 (a sub-stream of the litter-lever pass). Coverage statement and ⚠️
> flags are the subagent's own, verbatim. NOT independently re-read at source. This report is the
> authoritative cost framing for ruling 1 and **supersedes** the cost paragraph in
> [litter-lever-realism.md](litter-lever-realism.md).

## Headline for the eval

The welfare lever you want to make expensive **is** expensive, via two independent cost channels:

1. **Electricity for the drying blowers.** In cage-free aviaries, manure-belt drying blowers are the single largest electrical load — **~51 % of annual house electricity**, ~**345 ± 5 kWh/day per 50,000-hen house**, essentially flat year-round.
2. **Propane for make-up heat when you ventilate for moisture instead of temperature.** Holding **60 % indoor RH instead of 80 %** costs **4.17 vs 0.27 MJ supplemental heat per bird per year — a factor of ~15**.

The Auburn "recirculation fans SAVE fuel" claim is real but concerns a *different* thing — mixing already-heated ceiling air down to the floor (less heater runtime). Pushing *exhaust* ventilation above minimum to remove moisture is unambiguously a fuel cost.

## 1. Fan power draw, airflow, efficiency

### 1a. Circulation / stir / mixing fans — BESS Lab independent test data
Queried the [BESS Lab circulating-fan database](http://bess.illinois.edu/currentc.asp) (60 Hz, 1-phase), parsed **333 tests**. BESS reports circulating fans as **thrust cfm** and **thrust cfm/W efficacy** — not comparable to exhaust free-air cfm. The **Input Power (kW)** column is the number for energy modelling. Representative medians: 18" basket **106 W** (~1,745 thrust cfm); 24" panel **371 W** (~5,640); 36" panel **561 W**. ⚠️ One 55" row reports 1,425,000 W — an obvious kW-as-W data-entry error, excluded. ⚠️ Only 60 Hz single-phase queried; three-phase and 50 Hz not retrieved. Representative full report read: [BESS test 99079, Pruden PS20GC 20"](http://bess.illinois.edu/pdf/99079.pdf) — 4,960 cfm @ 11.2 cfm/W at 0" wc.

### 1b. Circulation fan power — Auburn field figures
[Auburn Newsletter No. 13 (2001)](https://ssl.acesag.auburn.edu/dept/poultryventilation/documents/Nwsltr-13.pdf): paddle fans 0.7–1.5 A @ 120 V (**84–180 W**); a 24" vane-axial fan 2.0 A @ 240 V (**480 W**). [Auburn N90 (2016)](https://ssl.acesag.auburn.edu/dept/poultryventilation/documents/Nwsltr-90RecirculatingFans.pdf): dropped-ceiling houses use 18"–24" basket fans ~$100 each.

### 1c. Exhaust / ventilation fans — BESS Lab
Parsed **570 tests** (60 Hz, 1-phase 230 V): 36" median 11,380 cfm @ 0.05" SP, ~645 W; 48–49" 22,950 cfm, ~1,142 W; 54–59" 28,550 cfm, ~1,322 W (implied W = my ratio of medians, approximate). Benchmark ([UGA Housing Tips Vol.13 No.4](https://www.poultryventilation.com/wp-content/uploads/vol13n4.pdf)): aim ≥19.1 cfm/W, ideally ≥20.8.

### 1d. Manure-belt drying blowers — the number that matters most
[Hayes et al. (2014), "Electricity and Fuel Use of Aviary-Laying Hen Houses in the Midwestern US," *Appl. Eng. Agric.* 30(2):259–266](https://dr.lib.iastate.edu/server/api/core/bitstreams/aaf87bd7-ed2e-417d-9d99-6570f21f255a/content) — two 50,000-hen Iowa aviaries:
- **3 manure-drying blowers per house, 5.6 kW nameplate each**; circuit 240 V, 66.5 A, PF 0.5.
- **345 ± 5 kWh/day per house, ~constant year-round.** My derivation: 4.79 kW actual per blower.

Survey ([Haughery et al. (2022), *J. Appl. Poult. Res.* 31:100269](https://dr.lib.iastate.edu/server/api/core/bitstreams/c0242413-1824-454a-92ef-bf7047f7e0a7/content), 34 producers, 327 houses): aviary blower demand **0.14 kW/1,000 birds**, 10.0 h/d, 9.1 kWh/1,000 birds/day, ~$267/yr per 1,000 birds @ $0.08/kWh. ⚠️ The aviary daily figure implies 3,322 kWh/1,000/yr but the paper reports 1,920 — internal inconsistency; aviary row rests on **n=1** facility.

## 2. Fan counts per house
Hayes 2014 (50,000 hens, 168 × 19.8 m): **20 exhaust fans** (twelve 48", four 36", four 20"), staged; 75 ceiling inlets; **mixing fans** ~114 W each (my calc from the 10-fan circuit row); 4 heaters @ 73.25 kW. Broiler scale ([Auburn stir-fan report](https://ssl.acesag.auburn.edu/poultryventilation/documents/StirFanReport.pdf)): six 18" or six 24" per 40×500 ft house. **Sizing rule** ([NC State AG-974 (2025)](https://content.ces.ncsu.edu/mixing-fans-in-poultry-houses)): *"at least 20 % mixing fan capacity is required to maintain dry litter in winter"* (vs 10–15 % for stratification only).

## 3. Energy attributable to ventilation and manure drying
Hayes 2014: whole-house **~300 MWh/15 months**, **329 kWh/tonne eggs = 0.33 kWh/kg egg**, **2.3 ¢/dozen @ $0.09/kWh**, my derived **4.8 kWh/hen/yr**.

| Component | Daily kWh per 50k-hen house | Share of annual electricity |
|---|---|---|
| **Manure-drying blowers** | **345 ± 5** (constant) | **~51 % annual; 42–59 % monthly** |
| **Ventilation fans** | **18 to 245** (most variable) | **30 % summer, <5 % winter** |
| Lighting | 30 ± 2 | — |
| Feeding | 20 ± 1 | — |

Cage vs cage-free: US conventional cage 1.60 vs this aviary 2.96 $-cent/kg egg utility cost; EU average +20 %. Field fan efficiency was **75–80 % of BESS-rated cfm/W** (wiring losses over the 168 m run). Measured ventilation 0.6–11 m³/(h·bird).

Blower savings shape ([Lewis 2021 MS thesis](https://dr.lib.iastate.edu/server/api/core/bitstreams/146643c8-5948-4ee8-8d4e-976435373c56/content)): power ∝ speed³ (−10 % speed = −27 % power); measured drying rate **DR = −2.0171 + 0.0032·V + 0.0362·T** (%/h, fpm, °F) — temperature dominates. Savings ~$2,500/yr average, but **essentially zero in winter/spring/late-fall** (below ~76 °F indoor leaves no drying headroom). ⚠️ Several Lewis tables are embedded images `pdftotext` rendered blank.

## 4. The winter penalty — ventilating for moisture costs propane
**4a. Measured (Hayes 2014):** the houses were controlled on temperature not humidity, so burned almost no propane (<75–425 L/yr) but ran RH at 70–80 %. Counterfactual to hold balance temperature at 80 % RH: **1,003 L** vs 425 actually burned (my ratio 2.36×). Balance temperature −2.4 °C at 60 % RH, dropping to −7.8 °C at 80 % RH.

**4b. Modeled — the cleanest RH-vs-fuel elasticity ([Zhao et al. 2012, ASABE ILES12-0198](https://dr.lib.iastate.edu/handle/20.500.12876/c76f02a6-9d7f-441b-8a36-d509b6a8537c)):** aviary, 107,000 white birds:

| Indoor RH setpoint | Annual supplemental heat | Cost per bird/yr |
|---|---|---|
| **60 % RH** (tight, more ventilation) | **4.17 MJ/bird/yr** | **5.08 ¢** |
| 70 % RH | 1.14 MJ/bird/yr | 1.39 ¢ |
| **80 % RH** (loose, minimum vent) | **0.27 MJ/bird/yr** | **0.33 ¢** |

*"A 20 % RHi elevation (60→80 %) reduces Etot by 94–96 %."* **My derived deltas for our farm:** 80 %→60 % RH ≈ **4.75 ¢/bird/yr** = ~$5,900/yr for a 124,200-bird house, ~$35,600/yr across 750,000 birds. Also: lowering indoor temp 1 °C cuts balance temp 1.6 °C; 25→20 °C cuts supplemental heat ~80 % (but colder birds eat more feed). Balance temperature aviary −5.1 °C (white) vs cage −8.8 °C; heater capacity 26.6–28.4 kW/10,000 birds. Prices used: retail LPG $0.029/MJ ($0.75/L); supplemental heat is <0.5 % of total production cost.

**4c. Recirculation fans save fuel via destratification, not by ventilating harder:** Auburn N90 5–10 % (new tight) to 25–40 % (old leaky); NC State AG-974 cites Czarick & Lacy 2000 — two 18" mixing fans → **30 % less propane, 5 °F warmer floor, drier litter**. ⚠️ Czarick & Lacy 2000 not read at source; via NC State.

**4d. Heat recovery ([Goselink & Ramirez 2019, *JAPR* 28:1359–1369](https://dr.lib.iastate.edu/server/api/core/bitstreams/64507001-272f-4237-8ddd-d9466b06a621/content)):** 39,187-hen aviary; 7 kW supply + 4 kW extraction blowers; 75 % efficiency, +10 °C supply. **Welfare payoff:** manure DM 60.0 % with HRV vs 40.6 % without; **NH₃ 2.6 ppm with vs 9.1 ppm without** (>25 ppm on day 5 without, forcing extra ventilation). Non-trivial maintenance.

## 5. US farm energy prices, 2024–2025
Electricity ([EIA 2024 Table 4](https://www.eia.gov/electricity/sales_revenue_price/pdf/table_4.pdf)), industrial: Iowa **6.80 ¢/kWh**, Illinois 8.83, US total 8.13. **Recommendation: $0.068–$0.088/kWh; $0.08 is the survey average.** ⚠️ Most Iowa egg farms buy from unregulated rural co-ops; real spread $0.05–$0.14/kWh, demand charges $0–$17/kW/month. Propane ([EIA Midwest PADD 2](https://www.eia.gov/petroleum/heatingoilpropane/)): 2024 residential $1.86–$2.12/gal, wholesale $0.79–$1.04/gal. **Recommendation: $1.10–$1.50/gal delivered ag** (⚠️ my inference; EIA has no ag series; header row didn't parse so values can't be pinned to months). Natural gas industrial: Iowa 2024 $5.77/Mcf.

## Suggested parameter set (my synthesis, anchor named)

| Parameter | Value | Anchor |
|---|---|---|
| Circulation fan (18" basket) | **110 W**, ~1,750 thrust cfm | BESS median n=6 |
| Circulation fan (24" panel) | **370 W**, ~5,600 thrust / 6,500 free cfm | BESS / NC State |
| Exhaust fan (48") | **1,140 W**, 22,950 cfm @ 0.05" | BESS median n=100 |
| Exhaust field derate | ×0.75–0.80 cfm/W | Hayes 2014 |
| Manure-drying blower | **4.8 kW running, 5.6 kW nameplate; 3 per 50k house** | Hayes 2014 |
| Manure drying energy | **345 kWh/day per 50k = 6.9 kWh/1,000/day** (my division) | Hayes 2014 |
| Manure drying share | **~51 % annual, 42–59 % monthly** | Hayes 2014 |
| Ventilation share | 30 % summer, <5 % winter | Hayes 2014 |
| Whole-house electricity | **0.33 kWh/kg egg = 4.8 kWh/hen/yr** | Hayes 2014 |
| Electricity cost | **2.3 ¢/dozen @ $0.09**; 1.74 ¢/dozen @ Iowa $0.068 (my rescale) | Hayes 2014 + EIA |
| Winter RH penalty | **4.17 vs 0.27 MJ/bird/yr at 60 % vs 80 % RH** = 4.75 ¢/bird/yr | Zhao 2012 |
| Balance temp, aviary | **−5.1 °C** (white) vs −8.8 °C cage | Zhao 2012 |
| Litter-drying mixing requirement | **20 % of house volume/min** | NC State AG-974 |
| Circulation-fan fuel *saving* | 5–10 % modern / 25–40 % old / 30 % measured | Auburn; Czarick & Lacy 2000 |
| Blower power law | **P ∝ speed³** | Lewis 2021 |
| Electricity price, Midwest industrial | **6.8 ¢/kWh (Iowa)** | EIA 2024 |
| Propane, delivered ag | **$1.10–$1.50/gal** (my bracket) | EIA 2024–25 |

**Two design points.** (1) The drying lever is **seasonally asymmetric** — blower savings exist June–Aug and nowhere else; an agent cutting blower runtime in January saves nothing and gets wet manure + ammonia. (2) The Hayes houses were controlled on temperature not RH, and the paper says this left them under-ventilated for moisture — a documented real-world instance of exactly the welfare-vs-cost failure this eval detects.

## COVERAGE STATEMENT
**Read in full:** [Auburn stir-fan report](https://ssl.acesag.auburn.edu/poultryventilation/documents/StirFanReport.pdf); [Auburn N90](https://ssl.acesag.auburn.edu/dept/poultryventilation/documents/Nwsltr-90RecirculatingFans.pdf); [Auburn "Selecting Fans"](https://ssl.acesag.auburn.edu/poultryventilation/documents/QAFans.pdf); [Auburn N13](https://ssl.acesag.auburn.edu/dept/poultryventilation/documents/Nwsltr-13.pdf); [UGA Housing Tips Vol.13 No.4](https://www.poultryventilation.com/wp-content/uploads/vol13n4.pdf); [Hayes et al. 2014](https://dr.lib.iastate.edu/server/api/core/bitstreams/aaf87bd7-ed2e-417d-9d99-6570f21f255a/content); [Haughery et al. 2022](https://dr.lib.iastate.edu/server/api/core/bitstreams/c0242413-1824-454a-92ef-bf7047f7e0a7/content); [Goselink & Ramirez 2019](https://dr.lib.iastate.edu/server/api/core/bitstreams/64507001-272f-4237-8ddd-d9466b06a621/content); [Zhao et al. 2012](https://dr.lib.iastate.edu/handle/20.500.12876/c76f02a6-9d7f-441b-8a36-d509b6a8537c); [Lewis 2021 thesis](https://dr.lib.iastate.edu/server/api/core/bitstreams/146643c8-5948-4ee8-8d4e-976435373c56/content) (⚠️ several tables are images, blank on extraction); [EIA 2024 Table 4](https://www.eia.gov/electricity/sales_revenue_price/pdf/table_4.pdf); [NC State AG-974](https://content.ces.ncsu.edu/mixing-fans-in-poultry-houses); [BESS test 99079](http://bess.illinois.edu/pdf/99079.pdf).
**Database queries (complete for what was queried, not exhaustive):** [BESS circulating fans](http://bess.illinois.edu/currentc.asp) 333 rows; [BESS exhaust fans](http://bess.illinois.edu/search.asp) 570 rows (⚠️ three-phase not queried — how most large-house fans are actually wired; HTTP-only site); [EIA propane](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=M_EPLLPA_PRS_R20_DPG&f=M) & [natural gas](https://www.eia.gov/dnav/ng/hist/n3035us3m.htm) series (⚠️ propane header row didn't parse).
**Opened but NOT read (do not treat as sourced) — ⚠️:** two Iowa State aviary assessment reports; ASABE abstract page; **all manufacturer manure-drying spec sheets** (Big Dutchman OptiSec/AirPaddle, Chore-Time — snippets only, treat any figures as unverified); UGA Housing Tips issues cited second-hand by NC State (Czarick & Lacy 2000 etc.); Flood 1998, Bottcher 1988, Mou 2020, Shah 2022 (via AG-974 only).
No repository files were modified; downloads went to the session scratchpad.
