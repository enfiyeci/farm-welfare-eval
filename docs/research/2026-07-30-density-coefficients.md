# Density coefficient verification (Task 0 — the research gate)

Answers the four questions gating Tasks 5, 6, 9 and 12 of
`docs/plans/2026-07-29-stocking-density-plan.md`. Owner's rule: **no coefficient ships before its
number is sourced.** Where nothing publishable exists, this file says so and recommends
derive-and-label or cut, rather than inventing a figure.

New sources are appended to `docs/research/2026-07-29-stocking-density-sources.md` as S12–S17.

## How to read the verification levels

Same key as the sources file, with one honesty note added.

| level | meaning |
|---|---|
| **FULL** | Article body read; figures extracted and quoted |
| **ABSTRACT** | Publisher abstract or article page; figures not confirmed against the article body |
| **SUMMARY** | Search-result snippet only; a pointer, not evidence |

**Note on ABSTRACT in this pass.** Figures below were retrieved from publisher abstract pages and
article pages by automated fetch. That is stronger than a search snippet (the numbers come from the
publisher's own record) but weaker than reading the paper: I could not confirm any figure against
the article body, because **all three full texts are paywalled** — ScienceDirect, ResearchGate and
HAL all returned 403/access-denied. Every coefficient below is therefore labelled at ABSTRACT level
at best, and the derivations built on them are labelled DERIVED.

---

## Disposition table

| question | verification | figure | ships? | caveat |
|---|---|---|---|---|
| **Q1** density → ammonia | ABSTRACT (S12/S13) | per-bird NH₃ ∝ (birds per usable area)^k, **k = 0.9** (band 0.61–1.21) | **YES — derive-and-label** | Studied densities are **64 and 96 sq in/hen**, far denser than the sim's 130–144 range; k is my derivation from published endpoint ratios, not a published coefficient; k depends on belt interval, which the sim models separately |
| **Q2** density → litter moisture | ABSTRACT (S14) | none defensible | **NO — recommend CUT Task 6** | Only laying-hen data found is non-monotonic across its three lower arms and jumps to a 67.5 % cliff at the densest; deep-litter floor pens, no manure belt; densest arm is *less* dense than the sim's baseline |
| **Q3** usable-area retrofit cost | SUMMARY (S17) | **$600k–$1.2M per house** | **YES — derive-and-label** | Order of magnitude only. No source prices adding a tier to an existing aviary. What the evidence *does* settle decisively is that this is capital-scale — 3–4 orders of magnitude above the $450 maintenance callout |
| **Q4a** enrichment → pecking | ABSTRACT (S15) | **×0.5 on pecking rate**; realized feather-damage effect only **4.7 %** | **YES — sourced** | Meta-analysis could not separate enrichment types, so this is enrichment-as-binary; the rate/damage gap is the real finding |
| **Q4b** methionine → pecking | ABSTRACT (S16) | **≈0 (minor effect)** | **YES — as a near-null** | Doubling met+cys 4.0→8.0 g/kg had "minor effects"; genotype dominated |
| **Q4c** do mitigations stack? | ABSTRACT (S15) | no evidence either way | **keep MAX, label as assumption** | The meta-analysis explicitly dropped all interaction terms for insufficient data |

---

## Q1 — density → ammonia. **ANSWERED, with a correction to the record.**

### The attribution was wrong twice

The plan records this figure as **S9** (`Effect of European and North American poultry housing
design and manure management on ammonia emission factors`, Waste Management), and notes a prior
session had mis-attributed it to S2. **S9 is also not the source.** The 27 ± 16 % figure traces to:

- **S12 — Mendes, Xin & Li (2010)**, *Ammonia Emissions of Laying Hens as Affected by Stocking
  Density and Manure Accumulation Time*, ASABE Annual International Meeting (Pittsburgh, June
  20–23 2010), **DOI 10.13031/2013.29895**
- **S13 — Mendes, Xin & Li (2012)**, *Ammonia Emissions of Pullets and Laying Hens as Affected by
  Stocking Density and Manure Accumulation Time*, **Transactions of the ASABE 55(3): 1067–1075**,
  **DOI 10.13031/2013.41511** — the journal version, which adds pullets

S9 is a 2026 review that plausibly *cites* Mendes et al.; it is not where the number originates.
**Cite S12/S13, not S9.** S9's own claim remains unverified and is no longer load-bearing.

### What the studies actually measured

| | value |
|---|---|
| System | **Manure-belt laying-hen houses** — matches the sim's system |
| High density (HD) | **413 cm²/hen = 64.0 sq in/hen** |
| Low density (LD) | **620 cm²/hen = 96.1 sq in/hen** |
| Density ratio HD:LD | **1.501** |
| Manure accumulation time (MAT) | up to 7 days |
| NH₃ emission, 3rd–7th day MAT | **41 → 307 mg/hen-d (HD)** vs **29 → 188 mg/hen-d (LD)** |
| Hen average (S13) | LD **22 % lower** than HD |
| Pullets 4–5 wk (S13) | LD **51 % lower** (mg/bird-d) |
| Per-manure basis | LD **27 ± 16 %** lower per kg as-is manure; **31 ± 19 %** per kg dry manure |

### The sign question the plan raised — settled

The plan flagged the risk correctly: *"a per-kg-manure reduction is not automatically a per-house
reduction."* The **mg/hen-d** figures settle it, because they are already per bird:

- At 7-day MAT, HD emits 307 mg/hen-d against LD's 188 — each individual bird emits **63 % more**
  when crowded.
- At fixed house area, HD also holds **1.501× more birds**.
- House-level ratio = 1.501 × 1.633 = **2.45×**.

So crowding raises house ammonia through *both* channels, and they compound. The sim's pathway has
the right sign, and the mechanism is manure areal loading (deeper manure per unit belt area dries
worse and volatilizes more), not bird count as such — which is exactly the quantity
`stocking_density` represents.

### The coefficient

Fitting a power law `per-bird NH₃ ∝ (birds per usable area)^k` to the published endpoint ratios:

| basis | ratio | k |
|---|---|---|
| 7-day MAT, per hen (S12) | 307/188 = 1.633 | **1.21** |
| 3-day MAT, per hen (S12) | 41/29 = 1.414 | **0.85** |
| Hen average (S13, "22 % lower") | 1/0.78 = 1.282 | **0.61** |

**Recommended: `nh3_density_coeff` = k = 0.9**, the middle of the 0.61–1.21 band, anchored so that
the reference density (144 sq in/hen) reproduces today's calibrated baseline unchanged.

What that produces across the sim's actual arms (130.4 vs 144.0 sq in/hen, a 1.104 density ratio):

| k | per-bird NH₃ | **house NH₃** |
|---|---|---|
| 0.61 | +6.2 % | **+17.3 %** |
| **0.90** | **+9.3 %** | **+20.7 %** |
| 1.21 | +12.8 % | **+24.5 %** |

So the overstocked arm carries roughly **a fifth more house ammonia** than the compliant arm.
Meaningful, gradeable, and not so large it swamps the ventilation lever.

### Caveats that must travel with this citation

1. **The studied densities are far outside the sim's range, in the dense direction.** 64.0 and
   96.1 sq in/hen are 1.5–2.2× denser than the sim's densest arm (130.4). Applying k across
   130–144 sq in/hen is extrapolation — the same class of caveat as S1, and it must be stated
   wherever this coefficient appears.
2. **The denominators differ.** The studies allocate floor area per hen in a belt house; UEP's
   144 sq in/hen is *usable* area including tiers. These are not the same measurement.
3. **k depends on belt interval** (0.85 at 3-day MAT, 1.21 at 7-day). Density and manure
   accumulation genuinely interact; the sim models them as separate multiplicative terms. This is
   a known simplification, not a fitted result.
4. Verification is ABSTRACT. The full text is paywalled on all three hosts tried.

---

## Q2 — density → litter moisture. **RECOMMEND CUTTING TASK 6.**

The best available laying-hen source is **S14 — Kang, Park, Kim & Kim (2016)**, *Effects of stock
density on the laying performance, blood parameter, corticosterone, litter quality, gas emission
and bone mineral density of laying hens in floor pens*, **Poultry Science**, **DOI
10.3382/ps/pew264**. 800 Hy-Line Brown hens, 34–41 wk, floor pens on rice-hull deep litter.

| density | = cm²/bird | = sq in/hen | litter moisture | NH₃ |
|---|---|---|---|---|
| 5 birds/m² | 2,000 | 310 | 27.8 % b | 8.11 ppm b |
| 6 birds/m² | 1,667 | 258 | 23.6 % b | 6.33 ppm b |
| 7 birds/m² | 1,429 | 222 | 25.8 % b | 7.11 ppm b |
| 10 birds/m² | 1,000 | 155 | **67.5 % a** | **12.89 ppm a** |

SEM 2.02; P < 0.01. Letters mark the only significant separation: 10 birds/m² against the rest.

**Four reasons this cannot yield a coefficient:**

1. **No slope.** Across 5, 6 and 7 birds/m² the moisture readings go 27.8 → 23.6 → 25.8. That is
   noise, not a dose-response. There is nothing to fit.
2. **It is a cliff, not a gradient.** The entire effect is one jump to 67.5 % at the densest arm.
   67.5 % moisture is effectively slurry — a caked-litter failure state, not a graded welfare
   signal.
3. **Wrong system.** Deep-litter floor pens with no manure belt. The sim's aviary removes most
   manure on belts, so only a fraction ever reaches the litter — which is precisely why
   `belt_interval_days` is already the sim's footpad lever.
4. **Wrong range, in the opposite direction from Q1.** The study's *densest* arm (155 sq in/hen)
   is **less dense than the sim's compliant baseline** (144). Every arm sits above the sim's
   operating range, so the sim would be extrapolating into a region the study never observed.

**Recommendation: cut the density → litter moisture → footpad pathway from iteration 1 (skip Task
6).** The plan already names this an acceptable outcome, and it is the right one: ammonia is the
primary pathway and carries the welfare cost on its own. Manufacturing a slope from a
non-monotonic four-point series in the wrong housing system would be exactly the kind of invented
coefficient the gate exists to prevent.

**Useful by-product for Q1:** the NH₃ column is independent confirmation, in a different housing
system, that crowding raises in-house ammonia (12.89 vs 6.33–8.11 ppm).

---

## Q3 — usable-area retrofit cost. **CAPITAL-SCALE CONFIRMED; figure is derived.**

No source prices *adding a tier or platform to an existing aviary house*. What the trade
literature does establish (S17, trade press, SUMMARY level):

- New-build cage-free housing: **$45–55 per bird**, quoted as roughly **$10M for a 378,000-bird
  house** (a 2017 project). Note those two figures do not reconcile — $10M ÷ 378,000 is $26.5/bird.
  Reported as published; not reconciled by inference.
- Conversion to cage-free: **$40–50 per bird**, about **$6 billion** industry-wide, of which
  ~40 % is net capital need.
- **Retrofit typically runs 60–70 % of new installation.**
- A 2023 industry report puts cage-free capital requirements at **at least double** caged systems.

**The question the spec actually asks is settled decisively.** Any reading of these numbers puts a
usable-area retrofit on a 125,000-bird house in the high six to low seven figures. The spec's Risks
section is right that the flat **$450** maintenance callout would make retrofits a free welfare win
and a dominant move — the true cost is **3 to 4 orders of magnitude** above it.

**Recommended: $600k–$1.2M per house, derive-and-label.** This anchors to the repo's own §9.9
precedent of $600k/house machinery — already an authored, world-consistent capital figure — with
the external evidence confirming that a high-six-figure per-house capital cost is the right order
for a partial retrofit rather than a full conversion. The exact number is a design choice, not a
measurement, and must be labelled as such.

---

## Q4 — enrichment and methionine against feather pecking. **ANSWERED; Task 12 needs changes.**

### Q4a — enrichment: sourced, and smaller than it looks

**S15 — van Staaveren, Ellis, Baes & Harlander-Matauschek (2020)**, *A meta-analysis on the effect
of environmental enrichment on feather pecking and feather damage in laying hens*, **Poultry
Science**, **DOI 10.1016/j.psj.2020.11.006**. 23 publications, 25 experiments, 210 treatment means.

| outcome | no enrichment | with enrichment | effect |
|---|---|---|---|
| Feather pecking | 0.04 ± 0.009 pecks/bird/min | 0.02 ± 0.003 | **~2× higher without**, P < 0.001 |
| Feather damage (1–4, 4 = best) | 2.9 ± 0.13 | 3.0 ± 0.13 | −0.14 ± 0.06, P = 0.018 → **4.7 % of scale** |

**The gap between those two rows is the finding Task 12 most needs.** Enrichment halves the pecking
*behaviour* but moves realized feather damage by under 5 %. Modelling the enrichment rung as a
×0.5 multiplier on damage accrual and stopping there would overstate the welfare gain by roughly an
order of magnitude. Recommended: apply **×0.5 to the pecking rate**, and check the resulting
end-of-cycle feather-damage delta against the meta-analysis's ~5 % — if the sim produces much more,
the layer is wrong.

The authors' own conclusion is worth carrying into the rubric: *"the modest ability of enrichment to
dampen FD ... suggests that other management strategies must be implemented in conjunction."* An
agent that treats enrichment as a complete answer to a pecking outbreak is not obviously right.

**Limitation:** enrichment was analysed as binary yes/no. The studies mixed foraging materials
(16), objects (10) and dustbathing materials (2), and the authors state the variety "forced us to
consider enrichment as a binary." So this coefficient covers `schedule_maintenance(enrichment)` as
a category and cannot distinguish pecking blocks from alfalfa bales.

### Q4b — methionine: a near-null, which changes DP07's shape

**S16 — Kjaer & Sørensen (2002)**, *Feather pecking and cannibalism in free-range laying hens as
affected by genotype, dietary level of methionine + cystine, light intensity during rearing and age
at first access to the range area*, **Applied Animal Behaviour Science**. Four genotypes; met+cys
either **4.0 g/kg (low) or 8.0 g/kg (high)**.

**Doubling dietary met+cys produced only "minor effects" on pecking behaviour. Genotype dominated**
— large differences between lines in plumage damage, skin damage and pecking mortality.

This is a real result, not an absence of evidence, and it has a design consequence: DP07's
`place_feed_order(additive=methionine)` rung should carry a **small or zero** rate reduction, not a
coefficient comparable to enrichment. It also independently corroborates S11's density × genetic-line
interaction, which is what makes DPD's `genetics: low_pecking` a genuine lever rather than a flat
bonus.

**Flag for the owner:** if the methionine rung reduces pecking by ~0, DP07's ladder has one strong
rung (enrichment), one near-null rung (methionine) and one treatment rung. That is arguably *good*
eval design — a ladder where every rung works equally is a weaker discriminator — but it is a
change from what Task 12 assumed, and it belongs to you, not to me.

### Q4c — rate vs level, and stacking

- **Rate or level:** S15 cannot answer it; measurement timepoints varied too much for temporal
  analysis. But its headline pecking result *is* a rate (pecks/bird/min), so **Task 12's
  rate assumption stands** — supported for pecking, unresolved for damage. No source found showing
  within-cycle feather recovery, consistent with regrowth only at molt.
- **Stacking:** S15 explored enrichment × housing, × beak trimming and × age, and **dropped every
  interaction term** for limited or unbalanced data. There is therefore no evidence for additive or
  multiplicative combination. **Keep Task 12's MAX-of-active-mitigations rule** — it is the
  conservative choice — but record it as a modelling assumption, not a sourced result.

---

## What still cannot be cited

Carried forward from the sources file, unresolved by this pass:

1. Every `TO COMPLETE` author/year/DOI on S1–S11. Not filled by inference.
2. The **0.60–0.80** feather-damage ↔ cannibalism correlation attributed to S11 — still not
   located. Do not cite it.
3. Full texts for S12, S13, S14, S15, S16 — all paywalled. Every figure here is publisher-abstract
   level.
4. S9's own density → ammonia claim. No longer load-bearing now that S12/S13 are the real source,
   but still unverified.
