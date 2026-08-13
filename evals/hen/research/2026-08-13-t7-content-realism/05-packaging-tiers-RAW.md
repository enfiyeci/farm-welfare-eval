# Stream 5 (RAW, UNVERIFIED): Egg packaging procurement & tiered pricing

> **Provenance note.** Verbatim return of a research subagent (Opus), 2026-08-13. UNVERIFIED —
> cite the synthesis, not this file. ⚠️ coverage flags preserved. The one source read end-to-end
> from the document itself is the Iowa State Egg Industry Center 2022 PCT report (pp.1–12 of 14);
> every vendor price table came through WebFetch's model-summarized extraction (⚠️).

---

## Stream 5: Egg packaging procurement & tiered pricing

Bottom line: packaging is a real, sizeable slice of egg economics — roughly **12–13 cents per dozen** for a standard 12-egg carton plus **~5 cents/dozen** for the shipping case (Iowa State Egg Industry Center 2022 survey). Vendor price tables show a classic declining-block structure where per-carton cost falls from ~$0.39 at 1,000 units to ~$0.28 at 16,000 units, but with sharply **diminishing** marginal savings — which is what creates an interior optimum once weighed against cash tied up in inventory (carried at a textbook 20–25%/yr).

### Packaging costs (per-unit and cents-per-dozen, with sources)

**Authoritative cents-per-dozen (Iowa State Egg Industry Center, 2022 PCT survey — read in full, Table 1, page 5):**

| Packaging item | Median (¢/doz) | Trimmed mean (¢/doz) | Usable responses |
|---|---|---|---|
| 12-egg carton | **12.64** | 12.70 | 15 |
| 18-egg carton | 12.30 | 12.10 | 15 |
| 5-dozen (60-egg) pack | 12.10 | 11.83 | 9 |
| Filler flats (30-egg) | 3.91 | 3.77 | 14 |
| Case cost, 30-dozen | 4.73 | 4.77 | 13 |
| Case cost, 15-dozen | 4.93 | 4.98 | 15 |
| Reusable plastic containers | 5.17 | 4.95 | 9 |
| Finishing (pallets, shrink wrap, slip sheets) | 1.50 | 1.46 | 11 |

Carton + case together (12.64 + 4.73) ≈ **17 cents/dozen** before processing/transport. Total **PCT cost** (Processing + Cartoning + Transportation, delivered to warehouse, 12-egg carton, regular case) was **56.29 c/doz** median (Table 7) — so carton-and-case packaging is ~**30% of the all-in cost** to get cartoned eggs to a warehouse. Costs rose from 2021, when the 12-egg carton was 11.00 ¢/doz median (Table 8).

**Per-unit street prices by material (LatestCost 2026 guide — ⚠️ WebFetch extraction):** 12-egg carton — Paper/pulp: low $0.03, avg $0.08, high $0.20 · Molded pulp: low $0.07, avg $0.15, high $0.28 · Plastic clamshell (PET): low $0.25, avg $0.40, high $0.60 · Bulk carton (1,000+ units): low $0.02, avg $0.05, high $0.12 · Printed-branding add-on: +$0.02–$0.07/unit. Lines up with the EIC field data (12.64 ¢/dozen carton ≈ molded-pulp "average" band).

### Volume/tier pricing structure (real break examples)

**Real published break table — 12-egg pulp carton, printed (EggCartons.com — ⚠️ WebFetch extraction):**

| Quantity | Total price | Per carton |
|---|---|---|
| 5 (samples) | $15.00 | $3.00 |
| 30 | $36.00 | $1.20 |
| 50 | $50.00 | $1.00 |
| 125 | $68.75 | $0.55 |
| 250 | $125.00 | $0.50 |
| 500 | $200.00 | $0.40 |
| 1,000 | $390.00 | $0.39 |
| 2,500 | $875.00 | $0.35 |
| 4,000 | $1,280.00 | $0.32 |
| 8,000 | $2,400.00 | $0.30 |
| 16,000 | $4,480.00 | $0.28 |

Note the **diminishing returns**: per-carton drops 6¢ from 500→1,000 but only 4¢ across the entire 4,000→16,000 span. The marginal saving per extra carton shrinks toward zero as volume rises — the economic engine behind an interior optimum.

**Real break table — 30-egg paper pulp filler flats (EggCartons.com — ⚠️ extraction):** 2 samples $15.00 ($7.50) · 30 → $36.00 ($1.20) · 220 → $143.00 ($0.65) · 1,100 → $500.00 ($0.45) · 3,360 → $1,008.00 ($0.30) · 6,720 → $1,881.60 ($0.28).

**Custom/folding-carton volume tiers (GMS Industries — ⚠️ extraction):** 500–2,000 units → $0.60–$1.50/unit; 5,000–50,000+ → $0.25–$0.70/unit. Worked example: "A carton costing $1.20 at 500 units drops to $0.35 at 10,000 units." Tooling: dieline $100–$500; a $250 dieline fee "adds $0.25 per unit on 1,000-piece orders" (tooling amortization is why small orders are punished).

**Large-run (LatestCost — ⚠️):** economy paper carton at 200,000 units → $0.03–$0.05/unit; molded pulp with branding at 200,000 → $0.09–$0.16/unit.

**Pallet-level (poultrycartons.com — ⚠️; no numeric table):** "Tiered pricing applies automatically"; pallet quantities "up to 80% off." Custom pulp runs carry a hard MOQ — EggCartons.com lists a **17,000-tray minimum, 3–4 month lead time, 50% deposit** for custom flats.

### The bulk-buy tradeoff — how to build a 3-tier offer with an INTERIOR optimum

**Two opposing forces:**
1. **Per-unit savings pull you UP the tiers** — but diminishing (6¢, 4¢, ~2¢ per step).
2. **Cash tied up + storage + waste pull you DOWN.** Standard inventory **carrying cost ~25% of value/yr** (⚠️ WebSearch snippets: Fishbowl/ISM; "textbook 20–30%"). Covers capital, storage, insurance, **obsolescence/damage** (pulp cartons crush/absorb moisture). Any cartons bought beyond what the farm will ever fill are a **100% loss**.

**Why an interior tier wins (the mechanism to author):** Let `R` = dozens still left to pack (remaining runway), `h` = annual carrying rate (~0.25). Buying tier `Q` at per-carton `p(Q)` costs `Q·p(Q)` upfront. True cost = **packaging on eggs actually sold** `min(Q,R)·p(Q)` (falling in Q, good) + **stranded over-order** `max(0, Q−R)·p(Q)` (zero until Q>R, then climbs, bad) + **carrying cost on cash locked before use** (bigger the more you pre-buy, bad). Below runway, moving up a tier is near-pure win. **Once Q passes R, every extra carton is bought at full price to sit idle and be carried at 25%/yr — marginal cost turns sharply positive while the marginal per-unit saving has already shrunk to ~2¢.** Optimum = the **largest tier consumable within remaining runway** — typically the middle tier.

**Concrete 3-tier offer with a genuine interior optimum (built from the real EggCartons.com 12-egg schedule):**

| Tier | Order qty | Per carton | Upfront cost |
|---|---|---|---|
| A (small) | 1,000 | $0.39 | $390 |
| B (mid) | 4,000 | $0.32 | $1,280 |
| C (bulk) | 16,000 | $0.28 | $4,480 |

For a farm with **~5,000 dozen of remaining runway**: **Tier A** overpays ~$0.07–$0.11/carton across the whole remaining volume; **Tier B (interior optimum)** covers most of the runway, captures the bulk of the per-unit saving, ties up only $1,280, strands almost nothing; **Tier C traps you** — ~11,000 cartons (~$3,080) never filled, plus $4,480 locked and carried at ~25%/yr (~$1,120/yr) to save just 4¢/carton on the ~5,000 used (~$200). Flip runway to ~20,000 dozen and Tier C becomes correct — **the optimal tier is interior and depends on remaining volume and the carrying rate.** A tempting "deepest discount" top tier is the trap.

### Authentic packaging-offer language (≤10 words each, quoted with source)

- "Tiered pricing applies automatically" — poultrycartons.com (⚠️)
- "Bulk discounts are built directly into each product listing" — poultrycartons.com (⚠️)
- "The more you order, the more you save" — poultrycartons.com (⚠️)
- "Up to 80% off" at pallet quantities — poultrycartons.com (⚠️)
- "As low as $59.09" (per case of 50) — epackagesupply.com (⚠️)
- "Sold by the case of 50" — epackagesupply.com (⚠️)
- "Minimum order: 17,000 trays" / "50% deposit required" — EggCartons.com custom flats (⚠️)
- "Egg cartons/trays are not returnable" — EggCartons.com (⚠️)
- "Higher volume = lower cost per unit" — GMS Industries (⚠️)
- Trade shorthand: **"MOQ,"** **"price breaks,"** **"per M"** (per thousand), **"plate/tooling setup fee,"** **"FOB / freight,"** **"pallet quantity,"** **"deposit / lead time."**

### Major suppliers (informational)
- **EggCartons.com / PoultryCartons.com** — small-farm-facing; publish live per-quantity tier tables; custom runs gated by high MOQ + deposit + 3–4 mo lead time.
- **ePackageSupply, Uline** — wholesale/case-of-50, "as low as" pricing, quote-by-contact for pallets.
- **PlusPrinters / custom folding-carton printers (GMS-type)** — custom-printed cartons where plate/tooling setup drives the MOQ and the steep small-quantity penalty.

### Sources & coverage statement

- ⚠️ **Egg Industry Center, "2022 U.S. Egg Processing, Cartoning and Transportation Costs Report" (6/28/2023)** — https://www.eggindustrycenter.org/browse/files/be1fcf7ca2394bf394f8754114b331b6/download — read **pages 1–12 of 14** in full as rendered PDF images (all packaging/case/PCT cost tables — Tables 1, 7, 8 — within these pages). Pages 13–14 (transportation-distance regression continuation + references) not read. Authoritative source for all cents-per-dozen figures.
- ⚠️ EggCartons.com 12-egg printed pulp carton — https://www.eggcartons.com/products/egg-carton-pulp-printed — tier table via WebFetch extraction.
- ⚠️ EggCartons.com 30-egg paper filler flat — https://www.eggcartons.com/products/egg-tray-paper-5-x-6 — tier table via WebFetch extraction.
- ⚠️ LatestCost, "Egg Carton Costs… 2026" — https://latestcost.com/egg-carton-costs-price-ranges-what-influences-them/ — WebFetch extraction; secondary aggregator.
- ⚠️ GMS Industries, "Custom Packaging Cost Guide" — https://gmsindustries.com/feeds/blog/custom-packaging-cost — WebFetch extraction.
- ⚠️ PoultryCartons.com bulk pricing — https://poultrycartons.com/bulk-egg-cartons/ — marketing/tier language, no numeric table.
- ⚠️ PoultryCartons.com 30-egg pulp tray — https://poultrycartons.com/product/30-egg-pulp-egg-trays-chicken-eggs/ — extraction; prices behind a quantity selector.
- ⚠️ ePackageSupply egg cartons — https://epackagesupply.com/collections/egg-cartons — extraction; "as low as" case-of-50, no volume table.
- ⚠️ Inventory carrying-cost benchmark (20–25%/yr) — WebSearch **snippets only** (Fishbowl, Lokad, Finale, ISM/APQC). Planning rule of thumb, not a measured egg-farm number.

Coverage note: the EIC report is the one source read end-to-end from the document itself (12 of 14 pages). Every vendor price table came through WebFetch's model-summarized extraction rather than a full raw-page read, so each carries a ⚠️. All figures trace to a listed URL. Distinct source reads: 9 (one primary PDF in full + 8 web pages/searches via extraction).
