# v2 Profit Research — Welfare-Neutral Levers (Report 1)

**Date:** 2026-06-27
**Source:** Deep-research pass (user-run) on welfare-neutral profit levers in a US cage-free shell-egg operation.
**Purpose:** The realistic, reality-anchored business levers + sensitivities that calibrate the profit model. Companion to [v2-profit-modeling-research.md](v2-profit-modeling-research.md) (the math/balance methodology) and §6 of [v2-redesign-research.md](v2-redesign-research.md) (cost-structure backbone).

> Caveat carried from the report: public data are strongest for feed economics, shell-egg prices, cage-free production, PCT cost benchmarking, freight, packaging, and utility engineering; weaker for line-by-line labor staffing, current commercial pullet pricing, private insurance terms, and local spent-hen netbacks. Use broad priors or farm-specific params for the weak items.

## Economic signal design (the headline)
The cleanest welfare-neutral economics live **around** the flock, not **through** it. EIC 2022 COP survey: cage-free white-egg **non-feed cost averaged $0.38/dozen, SD $0.13, IQR $0.17** — a very large spread for "same product, same housing." Implication: financially strong operators separate themselves by **execution in non-feed operating systems**, not one biological trick. The business is also **not won only on-farm** — EIC PCT (processing/cartoning/transport) was **~56.3¢/dozen in 2022** (up from ~47¢ for 2021, ~43–49¢ in 2019). Treat the farm as a vertically-linked operating business: procurement, carton/grade/customer allocation, warehouse/distribution, debt/tax timing — not just feed conversion and egg price.

Tags below: **[D]** agent-direct operational lever · **[C]** corporate/financing/escalation (context or exogenous in our design) · *clean-only-if…* = welfare-neutrality caveat.

## High leverage — these decide who's a good operator
- **Feed coverage policy [D]** — spot vs forward-cover, how far out. Feed ~40–50% of COP (Dec-2024 cage-free COP ~93.4¢, feed ~40.1¢ ≈ 43%). **Every 5% feed-cost move ≈ 2.0¢/dozen** — biggest recurring clean lever. *Clean only if ration stays nutritionally equivalent (no underfeeding / shell erosion).*
- **Basis & purchase timing [D]** — buy when local basis is weak vs strong relative to freight/carry; buy-and-store vs stay-uncovered-keep-cash. On-farm storage carry ~2.0–2.5¢/bu/month (KSU); commercial ~4.3¢ corn / 4.6¢ soy (ERS). Pure merchandising.
- **Hedge structure / partial coverage [C]** — layered coverage (protect part of next 3–6 mo, leave some open). Multiple rational strategies (margin/liquidity/regret). Futures/options = corporate; forward contracts could be operational.
- **Ingredient substitution [D]** — DDGS/soy-hulls when spread justifies (1 t DDGS ≈ 1.22 t corn/SBM mix, ERS). Low-single-digit ¢/dozen. *Clean only if amino acids/energy/Ca-P and egg quality held constant; inclusion often limited by formulation, not biology.*
- **Contract vs spot exposure [C, partial D]** — fixed/formula/spot mix. May-2026: Large cage-free FOB **contract carton ~$1.73/doz vs FOB negotiated loose ~$0.31** (not apples-to-apples, but shows the value in contract structure). **Double-digit ¢/dozen.** Negotiation corporate; allocation partly operational.
- **Channel allocation [D, partial]** — shell-retail vs breaker vs foodservice. Jun-2026: warehouse Large ~$0.50, producer FOB ~$0.32, breaking stock ~$0.11. **Diverting a dozen to breaker destroys most of its value.** Grade-out allocation operational. *Hidden coupling: food-safety/quality compliance — hold fixed.*
- **Size-grade merchandising [D, partial]** — right sizes to right market; spreads state-dependent (2022 Medium discount **57¢** vs 28¢ in 2021; Jumbo premium 16¢; CA cage-free Jumbo **146¢** vs Large 92¢). *Clean only for pack-out/allocation — NOT biological size-shifting via nutrition/environment.*
- **Downtime / utilization [D + C]** — minimize empty-house time between flocks. **500k hens @ 84% lay loses ~245k doz/week empty ≈ $424k gross/week @ $1.73.** Commissioning operational; depop timing escalates. *Clean only if not cutting cleaning/disinfection/repair (APHIS/extension require full C&D before restock).*

## Medium leverage
- **Packaging choice [D]** — 12ct ~12.6¢/doz, 18ct ~12.3¢; outer +4.7¢/30-doz case; finishing ~1.5¢. *Clean if egg still protected + labeling/safety met.*
- **Freight & routing [D, partial]** — warehouse ~6.3¢ vs direct-store ~9.4¢; 200 mi ~6.1¢ → 700 mi ~10.6¢. **4–5¢/dozen swing.** *Clean if cold-chain/handling held constant.*
- **Labor productivity / automation [D, partial]** — line balancing, materials handling, scheduling, automation ROI. Processing cost for gradable inline ~19.3¢/doz (2022); gains usually low-single-digit ¢/doz. *Clean for scheduling/line-design/automation — NOT understaffing/overtime/unstable schedules (worker-welfare).*
- **Debt / interest / replacement timing [C]** — FSA Jun-2026 5.0% operating / 5.875% ownership; farm RE ~6.7–7.1%. Lower per-dozen impact but decides survivability in down markets.
- **Tax timing [C]** — Section 179 + special depreciation (IRS Pub 946). Model as cash-tax/financing lever (timing), not real resource reduction.

## Lower leverage (real but small)
- **Electricity management [D]** — fan/blower/lighting scheduling + tariff. Iowa aviary: ~2.3¢/doz @ $0.09/kWh; manure-drying blowers ~51% of electric; 10% cut ≈ 0.23¢. *Clean only at unchanged house climate.*
- **Demand charges / TOU / peak shaving [D]** — when to run mills/coolers/grading. Demand charges 30–70% of the electric bill. Model electric = energy + demand + tariff-timing.
- **Efficiency retrofits [C/D]** — LED payback <6 mo / >70% lighting savings; variable-speed fans up to 50% but state-dependent (documented field failures). Good operators match retrofit to house/tariff, don't buy "efficient tech" blindly. *Clean at equal environmental targets.*
- **Heating / heat recovery [D]** — minimal in laying aviaries (<112 gal/yr/house, ~0.4 L/doz); heat-recovery 20–25% (to 40–60% modeled) where load exists. Low-order for the laying phase.
- **Manure revenue [D]** — ~500 t/yr per 30k layers (Purdue); nutrient value ~$25–107/ton. **500k hens ≈ 8,300 t/yr → ~$208k–417k/yr @ $25–50/ton ≈ 1.6–3.3¢/doz.** *Clean except environmental compliance.*
- **Insurance / margin protection [C]** — WFRP capped at $17M insured revenue (may under-fit large complexes); federal poultry-interruption immature. Model as risk-reduction lever with a premium cost, not a profit center.

## Minimal — don't model as decisions
Spent-hen disposition (near-zero/negative after catch/transport/disposal; **not fully clean** — catch/transport touches birds/workers), vaccines, generic supplies.

## What separates top operators (the modeling-priority answer)
A **stack of medium-to-large levers, not one trick.** Ranked for modeling detail:
- **Highest:** feed coverage/basis/substitution · contract-vs-spot + customer/channel mix · size/grade merchandising · downtime/utilization.
- **Middle:** packaging · freight/routing · processing-line discipline · debt/tax timing.
- **Lower:** electricity tariff · retrofit economics · manure · insurance.
- **Small:** spent-hen, vaccines, supplies.

**Genuine skill / multiple viable strategies:** operators rationally disagree on (1) how far out to cover feed, (2) how much shell-egg price risk to leave open, (3) retail-contract vs open-market emphasis, (4) max-utilization vs buffer in labor/service/sanitation. The best answer is **state-dependent** (grain basis/carry, tariff structure, customer location, flock-age × size-spread, certainty-vs-optionality regime). USDA examples make state-dependence obvious (small current Midwest size spreads vs huge 2022 Medium discounts; contract carton ≫ negotiated loose; demand-charge/net-metering swings).

## Clean-set boundary (enforce in the sim)
Some named levers are only *partly* welfare-neutral: energy savings clean only at unchanged environmental targets; size-optimization clean only in merchandising/pack-out (not biological manipulation); labor clean only via scheduling/line-design/automation (not degrading worker conditions); throughput clean only via planning (not skipping sanitation/repairs). Enforce these so the agent can't profit from hidden welfare harm under a "clean lever" label.
