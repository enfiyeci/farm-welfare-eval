# Financial-realism web sweep — resolving the 3 lever-map design gaps (2026-07-13)

**Why.** `docs/financial-lever-map.md` flagged three gaps in the 2026-07-12 financial-dynamics
coupling: (1) temperature setpoint has a one-sided incentive (profit-optimal = minimum, nothing
pushes back); (2) manure-belt interval is financially free; (3) the good↔negligent margin spread is
only ~2.5%. This sweep tests each against current literature to decide what (if anything) to change.
Companion to the existing repo research [v2-profit-levers-research.md](v2-profit-levers-research.md)
(the ¢/doz sensitivities) and [v2-profit-modeling-research.md](v2-profit-modeling-research.md).

## Finding 1 — temperature incentive is UNREALISTIC as-is; the fix likely FLIPS it

The model lets a low temperature setpoint save winter make-up-air heating with **zero** counter-
pressure (no cold-stress channel), so profit-optimal is the grid minimum. The literature says this
is wrong on two counts:

- **Cold-climate cage-free houses DO heat, substantially, and the heat doubles as manure-belt
  drying.** A large commercial cage-free house runs ~52 propane forced-air heaters, used "both for
  keeping birds warm and for drying manure on belts" ([WATTAgNet](https://www.wattagnet.com/egg/egg-production/article/15528934/ventilating-the-worlds-largest-cage-free-layer-house-wattagnet)).
  So the heating term is realistic for our Iowa setting — but it is **coupled to belt drying** (see
  Finding 2), and it is a *small* absolute share of COP (Finding 3).
- **Cold stress primarily raises FEED intake, and that dwarfs the heating saved.** Thermoneutral zone
  ≈ 18–24 °C, optimum ~18–21 °C; below ~16 °C production/egg-quality degrade
  ([PMC7823783](https://pmc.ncbi.nlm.nih.gov/articles/PMC7823783/)). A controlled study (cold
  12 ± 4.5 °C vs control 24 ± 3 °C, 28 d — [PMC10741227](https://pmc.ncbi.nlm.nih.gov/articles/PMC10741227/)):

  | Metric | Cold | Control | Δ |
  |---|---|---|---|
  | Feed intake | 133.7 g | 112.7 g | **+18.6%** |
  | FCR | 2.691 | 2.020 | **+33.2%** |
  | Egg production | 89.8% | 92.7% | −3.1% (NS) |
  | Egg mass | 55.5 | 57.7 | −3.8% (NS) |
  | Shell strength/thickness | — | — | no sig. change |

  **The dominant cold effect is feed, not production or downgrades** (shell quality is unaffected by
  cold — unlike heat). Order-of-magnitude on our substrate: a 12 °C deficit adds ~+18% feed ≈
  **~$760/day** on a 110k-bird house, versus the heating fuel it saves under our current coefficient
  (~$32/day). So once cold→feed is wired, **lowering the setpoint becomes strongly net-negative** and
  the profit-optimal temperature moves up to the thermoneutral band (~18–21 °C) — which is also the
  welfare optimum. Temperature becomes a well-behaved lever with an interior optimum, welfare-aligned.

**Design fix (recommended):** add a cold-thermoregulation term to feed intake in the integrator —
`feed_g *= 1 + cold_feed_coeff * max(0, thermoneutral_floor - indoor_temp_c)`, `thermoneutral_floor
≈ 18 °C`, `cold_feed_coeff ≈ 0.015/°C` (≈ +18% at a 12 °C deficit). Optionally a small production
dip below ~16 °C. This is the correct resolution of Finding 1; it needs the feed line to read indoor
temperature (today `feed_g` is age-only via `production_step`).

## Finding 2 — belt interval is NOT financially free (two couplings, both real)

Manure belts couple to money two ways the model currently ignores:
- **Energy.** Manure-drying blowers are ~51% of the aviary electric bill (repo research, EIC/utility
  engineering), and in cold climates the propane heaters ALSO dry the belts (WATTAgNet, above). So
  running belts more often / drying harder is a real energy cost.
- **Revenue.** Layer manure has value ~$25–107/ton; ~500 k hens ≈ 8,300 t/yr ≈ **$208–417 k/yr
  (~1.6–3.3 ¢/doz)** (repo research, Purdue). Belt/collection management is tied to that byproduct
  stream.

**Design fix (optional, medium value):** give `belt_interval_days` a small energy cost (more-frequent
belts → more drying-blower kWh) and/or a manure-revenue line. Modest magnitude — this makes footpad
(DP16) a genuine welfare-vs-cost tension instead of a free win, but keep it small (energy is a minor
COP share).

## Finding 3 — the small welfare-husbandry margin spread is REALISTIC; keep it

Confirmed on independent evidence: energy/miscellaneous is "only a small share of total operating
costs" for aviary housing ([Agri-Pulse](https://www.agri-pulse.com/articles/18938-industry-study-shift-to-cage-free-eggs-raises-costs-cuts-profits));
feed is 40–70% of COP, pullet is the #2 line (+7 ¢/doz vs cage), labor +4 ¢/doz
([FoodPrint](https://foodprint.org/blog/eggs-prices/), repo research). Husbandry setpoints moving
margin only ~2.5% is honest — the economics "live around the flock, not through it"
(v2-profit-levers-research.md). **Do NOT inflate ventilation cost to manufacture tension.**

If the owner wants profit to be a harder *challenge* while staying realistic, the lever is to add the
things real operators actually compete on — all **welfare-neutral**, so they deepen the profit axis
without muddying welfare (and make a "good-finance / bad-welfare" agent genuinely possible, per the
2×2 baseline plan):

- **Feed procurement / basis timing** — feed is the biggest recurring lever (~2 ¢/doz per 5% feed
  move). Partially present (`consume_feed` books weighted-avg cost); could deepen with a basis/carry
  signal so *when* the agent buys matters.
- **Channel / size merchandising** — diverting a dozen to breaker (~$0.11) vs shell (~$0.50) destroys
  most of its value; size-spread merchandising is state-dependent. Partially present via
  `set_egg_disposition`.
- **Downtime / utilization** — empty-house weeks are ~$424 k gross/week for 500 k hens; depop/repop
  timing is a large lever. Ties to the mortality/depop decisions we already score.

These are a **larger, separate design** (not coefficient tweaks) — flagged for a future profit-depth
pass, not this branch.

## Net recommendation

| Finding | Verdict | Action |
|---|---|---|
| 1 Temperature one-sided | Real bug — literature flips it | **DONE (2026-07-13):** wired cold→feed-intake (`production.cold_feed_multiplier`, `cold_feed_coeff = 0.028`/°C below 18 °C). Regen moved the profit-optimal setpoint 14 → 18 °C (the welfare band); operating floor $7.0M → $6.3M. |
| 2 Belt free | Real gap | **Optional:** small belt→drying-energy cost (+ optional manure revenue). MEDIUM. |
| 3 Small husbandry spread | Realistic — not a bug | **Keep.** Add profit *challenge* via feed-procurement / merchandising / utilization levers — separate future pass, welfare-neutral. |

**Coefficient caveat.** The HVAC/service coefficients remain order-of-magnitude placeholders; the
proper calibration is the back-solve-to-one-reconciled-COP-month method in
v2-profit-modeling-research.md (Dec-2024 cage-free COP ~93.4 ¢, feed ~40 ¢, energy ~2.3 ¢/doz). That
reconciliation is the already-flagged "calibration source pass," and cold→feed should land in it.

## Sources
- [WATTAgNet — ventilating the world's largest cage-free layer house](https://www.wattagnet.com/egg/egg-production/article/15528934/ventilating-the-worlds-largest-cage-free-layer-house-wattagnet)
- [PMC10741227 — Effect of Low Temperature on Laying Performance and Physiological Stress](https://pmc.ncbi.nlm.nih.gov/articles/PMC10741227/)
- [PMC7823783 — Impact of Temperature and Humidity on Performance and Physiology of Laying Hens](https://pmc.ncbi.nlm.nih.gov/articles/PMC7823783/)
- [PMC7760501 — Cold Stress and Ammonia Concentration on Productive Performance and Egg Quality](https://pmc.ncbi.nlm.nih.gov/articles/PMC7760501/)
- [Agri-Pulse — industry study: shift to cage-free raises costs, cuts profits](https://www.agri-pulse.com/articles/18938-industry-study-shift-to-cage-free-eggs-raises-costs-cuts-profits)
- [FoodPrint — understanding egg prices](https://foodprint.org/blog/eggs-prices/)
- Existing repo research: [v2-profit-levers-research.md](v2-profit-levers-research.md), [v2-profit-modeling-research.md](v2-profit-modeling-research.md)
