# Density coefficient verification (Task 0 — the research gate)

Answers the four questions gating Tasks 5, 6, 9 and 12 of
`docs/plans/2026-07-29-stocking-density-plan.md`. Owner's rule: **no coefficient ships before its
number is sourced.** Where nothing publishable exists, this file says so and recommends
derive-and-label or cut, rather than inventing a figure.

Sources S12–S21 are appended to `docs/research/2026-07-29-stocking-density-sources.md`.

**Two passes were run.** The first answered the questions as the plan posed them. The second went
deeper at the owner's direction and **changed three of the four answers** — it corrected an error in
my own Q1 derivation, found commercial-scale evidence that strengthens the Q2 cut and the Q3
figure, and split Q4b into a threshold effect that the first pass had read as a flat null. Where
the two passes disagree, the second is the answer; the first is recorded so the reasoning is
auditable.

## Verification levels

| level | meaning |
|---|---|
| **FULL** | Document body read; figures extracted and quoted |
| **ABSTRACT** | Publisher abstract or article page; not confirmed against the article body |
| **SUMMARY** | Search-result snippet only; a pointer, not evidence |

Two documents reached **FULL** in the second pass — the CSES and UEP reports were downloaded and
text-extracted locally, so their figures are quoted from the documents themselves. Every journal
article remains **ABSTRACT** or below: ScienceDirect, ResearchGate, Wiley and HAL all returned 403.

---

## Disposition table

| question | verification | figure | ships? | caveat |
|---|---|---|---|---|
| **Q1** density → ammonia | ABSTRACT (S12) + FULL corroboration (S18) | house NH₃ ∝ density^(k+1), **k = 1.0** → **+22 % for the overstocked arm** (band +20 % to +24.5 %) | **YES — derive-and-label** | Source densities (64 and 96 sq in/hen) are far denser than the sim's range; k is my fit, not a published coefficient; k varies with belt interval, which the sim models separately |
| **Q2** density → litter moisture | ABSTRACT (S14, S19) | none defensible | **NO — recommend CUT Task 6** | Two independent reasons now: the one laying-hen dataset has no usable slope, and the largest commercial risk-factor study finds **litter type**, not density, is what predicts footpad dermatitis |
| **Q3** usable-area retrofit cost | **FULL** (S18, S20) | **capital cost per dozen rises ~179 % aviary vs cage**; per-house **$600k–$1.2M** | **YES — sourced mechanism, derived figure** | The *mechanism* (lower density → higher capital per dozen) is now sourced twice at commercial scale; the per-house dollar figure remains derived |
| **Q4a** enrichment → pecking | ABSTRACT (S15) | **×0.5 on pecking rate**; realized damage effect only **4.7 %** | **YES — sourced** | Enrichment analysed as binary; the rate/damage gap is the real finding |
| **Q4b** methionine → pecking | ABSTRACT (S16, S21) | **threshold, not dose-response** — ~0 above requirement, real effect below it | **YES — as a threshold** | Changes DP07's design: the rung only works if the ration is actually deficient, and our corpus does not say |
| **Q4c** rate vs level, stacking | ABSTRACT (S15, S21) | **rate confirmed**; no evidence on stacking | **rate YES; keep MAX as assumption** | Feathers regrow only at molt, so mitigation cannot undo existing damage — Task 12's assumption is correct |

---

## Q1 — density → ammonia. **ANSWERED. Attribution corrected, and my own first-pass fit corrected.**

### The citation was wrong twice before this pass, and my first fix was half-wrong

The plan attributes the 27 ± 16 % figure to **S9**; an earlier draft attributed it to **S2**. Neither
is the source. It comes from **Mendes, Xin & Li** — S12 (ASABE 2010, DOI 10.13031/2013.29895) and
S13 (Trans. ASABE 55(3):1067–1075, DOI 10.13031/2013.41511). **Cite S12/S13.**

**Correction to my first pass.** I fitted k across three figures, including S13's "22 % lower for
laying hens". That was wrong: S13's density contrast is **HD 155–206 vs LD 413–620 cm²/bird**
spanning pullets and hens, while S12's laying-hen contrast is **HD 413 vs LD 620 cm²/hen**. Mixing
them fits a ratio from one contrast to the density span of another. The defensible fit uses S12
alone — one paper, laying hens, one density pair, one manure system.

### The coefficient, from S12 alone

| basis (S12, HD 413 vs LD 620 cm²/hen, ratio 1.501) | emission | per-bird ratio | k |
|---|---|---|---|
| 3-day manure accumulation | 41 vs 29 mg/hen-d | 1.414 | **0.85** |
| 7-day manure accumulation | 307 vs 188 mg/hen-d | 1.633 | **1.21** |

**Recommended k = 1.0**, the midpoint. Because house emission = birds × per-bird, and bird count
itself scales with density at fixed area, **house NH₃ ∝ density^(k+1)** — superlinear in density.
Across the sim's arms (130.4 vs 144.0 sq in/hen, density ratio 1.104):

| k | house NH₃, overstocked vs compliant |
|---|---|
| 0.85 | +20.1 % |
| **1.00** | **+21.9 %** |
| 1.21 | +24.5 % |

A **tighter band than the first pass** reported (+17 % to +24.5 %), because dropping the mismatched
S13 figure removed the low end. The sign question the plan raised is settled: each bird emits
~63 % more when crowded *and* the crowded house holds 1.5× more birds, so the channels compound.

### Commercial-scale corroboration (new in the second pass)

**S18 — Coalition for Sustainable Egg Supply**, the three-system commercial comparison, read in
full:

- Aviary NH₃ was **significantly higher** than conventional or enriched. Cage and enriched stayed
  **below 15 ppm** daily mean; the aviary **exceeded 25 ppm on some winter days "due to low
  building ventilation rate."** That is the sim's existing winter ammonia behaviour, independently
  reproduced at commercial scale — a validation of the current calibration, not just of this node.
- The enriched system had **about half** the farm-level ammonia of the other two, *"presumably due
  to its lower hen stocking density and drier manure."* Commercial-scale support for the direction,
  though stated as attribution rather than measurement.
- Aviary ammonia comes from **manure accumulating on the floor, not removed until end of flock** —
  so in an aviary the density→ammonia path runs through *litter loading*, which is worth noting
  given Q2's recommendation below.
- **Stocking densities: aviary 1,253–1,257 cm²/hen (194 sq in), enriched 752, conventional 516.**

That last line deserves the owner's attention: **the commercial US aviary in this study runs at
194 sq in/hen, well above our "compliant" 144.** Our compliant arm is denser than a real
cage-free aviary, and our overstocked arm (130) is denser still. That does not break the node — UEP
144 is the certification floor and the eval is about behaviour at the floor — but the world should
not imply 144 is generous.

**S20 — Iowa/Pennsylvania commercial emission factors:** manure-belt houses with **daily** removal
emitted **0.054 g NH₃/hen-d** against **0.094** for twice-weekly — a **74 % increase** from less
frequent removal. An independent cross-check on the sim's `belt_interval_days` lever, in the same
units and system.

### Caveats that must travel

1. **Source densities are 1.5–2.2× denser than the sim's range.** Applying k across 130–144
   sq in/hen is extrapolation. State it wherever the coefficient appears.
2. **Different denominators.** S12 allocates floor area per hen in a belt house; UEP's 144 is
   *usable* area including tiers.
3. **k varies with belt interval** (0.85 at 3-day, 1.21 at 7-day). Density and manure accumulation
   genuinely interact; the sim treats them as separate multiplicative terms.
4. S12/S13 remain ABSTRACT-verified. Full texts are paywalled on every host tried.

---

## Q2 — density → litter moisture. **RECOMMEND CUTTING TASK 6 — now for two independent reasons.**

**Reason one, from the first pass (S14 — Kang et al. 2016, DOI 10.3382/ps/pew264).** 800 Hy-Line
Brown hens, floor pens, rice-hull deep litter:

| density | = sq in/hen | litter moisture | NH₃ |
|---|---|---|---|
| 5 birds/m² | 310 | 27.8 % b | 8.11 ppm b |
| 6 birds/m² | 258 | 23.6 % b | 6.33 ppm b |
| 7 birds/m² | 222 | 25.8 % b | 7.11 ppm b |
| 10 birds/m² | 155 | **67.5 % a** | **12.89 ppm a** |

No slope across the three lower arms (27.8 → 23.6 → 25.8 is noise); the whole effect is one cliff
at the densest arm; deep-litter floor pens with no manure belt; and **every arm is less dense than
the sim's compliant baseline** (10 birds/m² = 155 sq in/hen vs our 130–144).

**Reason two, new in the second pass (S19 — Volkmann et al. 2024, Annals of Applied Biology 185(1),
DOI 10.1111/aab.12923).** The largest commercial footpad-dermatitis risk-factor study found: 39
German flocks, 15,448 birds, hens 1–92 wk, flocks of 290–178,000. It recorded housing system, flock
size, age, season, and litter type and quality. **The significant factor on footpad score was
litter TYPE** — sand litter gave 94.4 % of hens completely unaffected — with moisture and ammonia
content the assumed mediator. **Stocking density is not among the reported significant
associations.**

So the best commercial evidence on the *outcome* Task 6 exists to drive points at litter
management, which the sim **already models** through `belt_interval_days`. Adding a density term
would duplicate a lever that is already there and better supported.

Supporting threshold worth keeping: **litter above ~30 % moisture** is associated with increased
footpad dermatitis incidence and severity. The sim's current litter equilibrium is ~20 %, so the
existing belt lever already spans the interesting region.

**Recommendation: cut Task 6.** The plan already names this acceptable. Ammonia carries the density
welfare cost alone, and it now does so on a tighter coefficient than before.

---

## Q3 — usable-area retrofit cost. **MECHANISM NOW SOURCED TWICE. Capital scale confirmed.**

The first pass could only cite trade press. The second pass read two full reports.

**S18 — CSES (read in full):**
- Aviary **total capital cost per dozen was 179 % higher** than conventional cage at 10 % interest
  and depreciation; enriched colony **106 %** higher.
- Aviary total operating cost per dozen **23 %** higher; total cost per dozen **36 %** higher.
- The stated cause is exactly the sim's mechanism: *"because of the costs associated with
  construction of those barns and **the relatively few hens housed in each**."*

**S20 — Caputo et al. 2023 (United Egg Producers / Michigan State, read in full):** seven producers
interviewed. *"**With lower stocking densities**, producers estimated that cage-free capital costs
are **more than double** those of conventional production."* Cage-free requires *"at least two times
the capital of caged facilities."* On retrofit specifically: converting an existing facility and
building new produce **similar annual cost impacts** (~17 % higher fixed/non-operating capital
either way).

**This is the economic tension the node is built on, now sourced at commercial scale from two
independent studies: lower density means fewer hens in the same shell, which raises capital cost
per dozen.** That is precisely why crowding is tempting and why a usable-area retrofit costs real
money.

**On the figure itself:** no source prices adding a tier to an existing aviary. Any reading puts a
usable-area retrofit on a 125,000-bird house in the high six to low seven figures — **3 to 4 orders
of magnitude above the $450 maintenance callout**, so the spec's Risks section was right.
**Recommended $600k–$1.2M per house, derive-and-label**, anchored to the repo's own §9.9 precedent
of $600k/house machinery, which the external evidence now confirms is the right order.

---

## Q4 — enrichment and methionine. **Q4a unchanged; Q4b and Q4c both changed.**

### Q4a — enrichment: sourced, and smaller than it looks (unchanged)

**S15 — van Staaveren, Ellis, Baes & Harlander-Matauschek (2020)**, Poultry Science, DOI
10.1016/j.psj.2020.11.006. 23 publications, 25 experiments, 210 treatment means.

| outcome | no enrichment | with enrichment | effect |
|---|---|---|---|
| Feather pecking | 0.04 ± 0.009 pecks/bird/min | 0.02 ± 0.003 | **~2× higher without**, P < 0.001 |
| Feather damage (1–4) | 2.9 ± 0.13 | 3.0 ± 0.13 | −0.14 ± 0.06, P = 0.018 → **4.7 % of scale** |

**The gap between those rows is the finding.** Enrichment halves the *behaviour* but moves realized
damage under 5 %. A ×0.5 multiplier applied directly to damage accrual would overstate the welfare
gain by roughly an order of magnitude. Apply **×0.5 to the pecking rate**, then check the sim's
end-of-cycle damage delta lands near ~5 %; if it lands much higher, the layer is wrong.

Limitation: enrichment was analysed as **binary** — the variety of materials "forced us to consider
enrichment as a binary yes or no variable" — so per-type coefficients do not exist.

### Q4b — methionine: **a threshold, not a null.** This changes DP07.

The first pass read S16 (Kjaer & Sørensen 2002) as a flat null: doubling met+cys from 4.0 to
8.0 g/kg produced only "minor effects", with genotype dominating. The second pass found the
reconciling literature (**S21**, nutrition reviews and extension sources):

- **Methionine *deficiency* causes feather pecking and feather eating.** A deficient bird eats
  feathers to obtain sulphur amino acids; methionine and cystine are required for keratin synthesis.
  Deficient birds show impaired plumage and increased pecking, and feather-eating hens show a
  measurable dietary preference for methionine.
- **Supplementing an already-adequate diet does little.** Which is exactly what S16 observed — its
  low arm was plausibly at or near requirement for the genotypes tested.

**So methionine is a threshold effect, not a dose-response**, and DP07's `additive: methionine` rung
only does anything **if the flock's ration is actually deficient**.

**Our corpus does not say.** Rations are authored as `LP2` and `LP-CHEAP` in `corpus/pricing.yml`
with no amino-acid or crude-protein spec; the only methionine in the repo is DP07's action matcher
in `schedule/events.yml:185` and the ladder description in `docs/decision-register.md:163`. As
things stand, the world rewards a rung whose real-world effect depends on a fact the world never
establishes.

**Three options, and this one is genuinely yours:**

1. **Leave the ration unspecified, model methionine as ~0.** Faithful to S16, cheap, and DP07 keeps
   three rungs of unequal strength — arguably a better discriminator than three that all work.
2. **Author the ration as methionine-marginal.** One corpus line plus a matching mechanism makes the
   rung a real and *correct* mitigation, and turns DP07 into a test of whether the model diagnoses
   a nutritional driver rather than reaching for the first available action. There is a ready-made
   in-world reason: reduced-crude-protein rations are a recognised ammonia-reduction measure
   (S20 measured a 1 %-lower-CP diet cutting emissions ~10 %), and cutting protein is exactly how
   methionine becomes limiting. That would tie DP01/DP07 and the ammonia node together through one
   authored decision.
3. **Drop the rung.** Simplest; discards an authored action and narrows the choice space.

I lean to (2) as the most interesting eval design and (1) as the cheapest honest option. Either is
defensible; (3) loses something. **Not built either way — this is a design decision, not a
coefficient.**

### Q4c — rate vs level: **confirmed**, and stacking still unsupported

- **Rate — now supported.** Feather regrowth after pecking damage occurs **at the next molt**;
  hens do not regrow feathers while sustaining lay. So a mitigation applied at day 240 genuinely
  cannot undo damage already present. **Task 12's rate assumption is correct** and can now cite a
  reason rather than an assumption.
- **Stacking — still no evidence.** S15 explored enrichment × housing, × beak trimming and × age and
  **dropped every interaction term** for limited or unbalanced data. **Keep Task 12's MAX rule** as
  the conservative choice, recorded as a modelling assumption.

---

## What still cannot be cited

1. Every `TO COMPLETE` author/year/DOI on S1–S11. Not filled by inference.
2. The **0.60–0.80** feather-damage ↔ cannibalism correlation attributed to S11 — still not located
   after two passes. **Do not cite it.**
3. Full texts of S12–S17, S19, S21 — paywalled. S18 and S20 are the only FULL reads.
4. S9's own density→ammonia claim. No longer load-bearing now that S12 is the real source.
5. S16's authorship and DOI are search-attributed and marked VERIFY.
