# SWIM 1.0: the aggregation rule Laksvel withholds — and why the two cannot simply be combined

**Date:** 2026-08-03
**Source:** Stien, Bracke, Folkedal, Nilsson, Oppedal, Torgersen, Kittilsen, Midtlyng, Vindas, Øverli & Kristiansen (2013),
"Salmon Welfare Index Model (SWIM 1.0): a semantic model for overall welfare assessment of caged Atlantic
salmon", *Reviews in Aquaculture* 5, 33–57. doi:10.1111/j.1753-5131.2012.01083.x
**PDF:** https://www.vetinst.no/fagomrader/dyrevelferd/dyrevelferdsprotokoller/_/attachment/download/3bc450b9-5d32-44c0-8196-129a03b658a6:9a51e49701c9148e40deb4f23638bf835469ee1a/salmon_welfare_index_model_swim_1_0%20(1).pdf
**Coverage:** read in full, pages 33–50 (the complete body: abstract through Discussion, all nine tables,
Equations 1–5). Pages 51–57 are the reference list and were not read. Every figure below was taken from the
PDF, and every arithmetic claim was recomputed independently — see *Errata* for where the paper's own tables
disagree with each other.

**Why this source:** Laksvel supplies 20 operational welfare indicators with thresholds but states explicitly
that *"the severity of each of the different indicators is not weighted"* and that scoring results *"must
therefore never be presented as average values."* It therefore cannot serve as a Layer-1 welfare-state scorer
on its own. SWIM is the published model that does weight and aggregate. This note extracts the aggregation
rule, and records the conflict that surfaced when the two were compared directly.

---

## 1. The aggregation rule, in full

SWIM is a weighted sum of normalised indicator scores, with an override. Four equations, all verified to
reproduce against the paper's own worked examples.

**Indicator score** — position of the observed level within the indicator's level ladder (Eqn 1):

```
IS_ij = (NL_i − RL_ij) / (NL_i − 1)
```

`RL_ij` is the rank of level *j*, `NL_i` the number of levels. Best level scores 1.00, worst 0.00, intermediates
evenly spaced. **Knockout levels are excluded from `NL`.** Verified: temperature has six levels of which one is
knockout, and level 2 scores 0.75 = (5−2)/(5−1), not 0.80 = (6−2)/(6−1).

**Weighting factor** — from expert-assigned weighting-category scores at the best and worst level (Eqn 2):

```
WF_i = (Σ_wc max(WS_wcl))_ILbest,i − (Σ_wc min(WS_wcl))_ILworst,i
```

**Relative weighting factor**, **indicator welfare score**, and **overall welfare index** (Eqns 3–5):

```
RWF_i = WF_i / Σ_j WF_j
IWS_i = IS_i · RWF_i
OWI   = Σ_j IWS_j                    → 0 (worst) … 1 (best)
```

**The override:** any indicator observed at a *knockout* level sets `OWI = 0` outright, regardless of every
other indicator. Knockout levels are excluded from the `RWF` and `IWS` computation.

### Two models, not one

This is the structural point that matters most for reuse. SWIM is **two separate OWA models**, because most
indicators are measured on individual fish rather than on the cage:

| | indicators | Σ WF |
|---|---|---|
| **Sea-cage level** | temperature, salinity, oxygen, water current, stocking density, lighting, disturbances, daily mortality, appetite | **94** |
| **Individual-fish level** | sea lice, condition factor, emaciation, vertebral deformation, sexual maturity, smoltification, fin condition, skin condition | **89** |

They are combined by a WF-weighted average of the two indices:

```
OWI_total = (OWI_cage · 94 + OWI_fish · 89) / 183
```

The individual-fish term is the **median** OWI across the sampled fish. Verified against the paper's own
sampling: cage 0.59, median fish 0.79 → (0.59·94 + 0.79·89)/183 = **0.687**, which is the 0.69 the paper
reports.

---

## 2. The weighting table

Weighting factors and relative weights, Table 5. Both RWF columns verified to sum to 1.00.

| Sea-cage indicator | WF | RWF | | Individual-fish indicator | WF | RWF |
|---|---|---|---|---|---|---|
| Daily mortality | 21 | 0.22 | | Emaciation state | 16 | 0.18 |
| Oxygen saturation | 17 | 0.18 | | Skin condition | 15 | 0.17 |
| Temperature | 16 | 0.17 | | Fin condition | 13 | 0.15 |
| Disturbances | 11 | 0.12 | | Sea lice | 11 | 0.12 |
| Appetite | 11 | 0.12 | | Vertebral deformation | 10 | 0.11 |
| Stocking density | 8 | 0.09 | | Sexual maturity stage | 9 | 0.10 |
| Lighting | 4 | 0.04 | | Smoltification state | 9 | 0.10 |
| Salinity | 3 | 0.03 | | Condition factor | 6 | 0.07 |
| Water current | 3 | 0.03 | | | | |
| **Sum** | **94** | **1.00** | | **Sum** | **89** | **1.00** |

Daily mortality is the single heaviest indicator in the model, and salinity and water current the lightest —
the paper says so directly, and attributes the low weights to scarce direct evidence rather than to
established unimportance.

**These weights are expert judgement, and the paper says so.** *"The WSs are expert opinions based on the
reviews, but the reader is free to challenge these decisions."* They are a defensible published starting point,
not a measurement.

---

## 3. Indicator level bands — directly usable substrate thresholds

From Table 4. `K` = knockout. These are the most immediately reusable part of the paper: each is a banded
threshold on a state variable, which is the shape `state_band` decision signatures already take.

**Temperature (°C):** 10–15 · 7–10 · 16–17 · 3–6 · ≤2 or ≥18 short-term · **K** = ≤2 or ≥18 long-term

**Oxygen saturation (%):** >80% at all temperatures · 70–80% warm (≈18 °C) / 60–80% (≈12 °C) / 50–80% cold
(6 °C) · 60–70% warm / 40–60% / 30–50% cold · **K** = <60% warm / <40% (12 °C) / <30% cold

**Stocking density (kg m⁻³):** <22 · 22–26 · 26–32 · >32. Norwegian authorities cap sea cages at 25 kg m⁻³.
Underlying evidence: Turnbull et al. (2005) found an inflection at ≈22 kg m⁻³ and no substantial negative
effect below 32; Adams et al. (2007) found negative effects at 35 vs 25; Oppedal et al. (2011b) found declining
feed intake, growth and more cataracts above 26.5 kg m⁻³.

> **This closes a gap the reading list flagged.** The reading list recorded that RP's salmon overview lists
> stocking density as a welfare harm but gives no numbers, and that RP's dedicated stocking-density report is
> announced but unpublished. SWIM supplies banded thresholds and three primary studies behind them. Note the
> paper's own caveat: these three studies give limited information on cage oxygen saturation or endemic
> infection, both of which may be the real reason welfare declined at higher density — SWIM treats crowding as
> plausibly a *response* to an underlying limiting factor rather than a primary cause.

**Sea lice:** no lice · light infestation · ≥0.05 pre-adult/adult lice cm⁻² · ≥0.08 cm⁻² · **K** = ≥0.12 cm⁻²

**Water current (body lengths s⁻¹):** <0.9 · 0.9–U_crit · **K** = ≥U_crit. U_crit ≈1.35 BL s⁻¹, taken from
Sockeye rather than Atlantic salmon; the paper recommends assuming U_crit/1.3 for safe margin.

**Daily mortality (% day⁻¹):** scored against Soares et al. (2011) benchmark percentile curves — at/below the
10th percentile · below the benchmark · at the benchmark · above the benchmark · at/above the 90th · **K** =
at/above the 90th long-term. The 50th-percentile curve is >0.1% day⁻¹ in week 1 after transfer, 0.01–0.1%
weeks 2–40, then <0.01% to slaughter, giving ≈11% cumulative — better than the 17% Norwegian and 21% Scottish
industry figures the paper cites.

**Condition factor:** K = (W·L⁻³)·100; >1.1 · 0.9–1.1 · <0.9.

### The sea-lice unit conversion, and a caution about it

SWIM scores lice per **cm² of fish surface**, while every regulatory threshold in the reading list (Norway
<0.5 adult females per fish, Faroes 1, Chile 3 gravid, Canada 3 motile) is per **fish**. The paper supplies the
bridge, from Tucker et al. (2002):

```
surface_area_cm² = 0.6131 · weight_g + 86.144
```

Verified: a 15 g smolt gives 95.3 cm², and the ≈11 adult lice that Holst et al. (2003) found as the maximum
carried by wild salmon over ten years of sampling gives 11/95.3 = 0.115 ≈ the 0.12 cm⁻² knockout.

⚠️ **Do not extrapolate this formula to harvest-weight fish.** It is linear in weight, but surface area on a
geometrically similar body scales as weight^(2/3). It was fitted on smolts; applied to a 5 kg harvest fish it
returns 3,152 cm², which is implausibly large. Converting a per-fish regulatory limit into SWIM's per-cm²
bands for grow-out fish needs a source fitted at that size, not this one.

---

## 4. The conflict with Laksvel — the finding that matters

The reading list's mapping table proposed Laksvel for indicators and thresholds, and SWIM for "an aggregation
approach", noting only that the two indicator sets differ and would need reconciling rather than copying. That
understates the problem. **The two documents disagree about whether population-level aggregation is legitimate
at all.**

- **Laksvel forbids collapsing a population into a summary statistic.** Its stated rule is that results must be
  reported as the *proportion of the sampled population at each level*, never averaged, and its own worked
  example is that moving from 100 fish at level 1 to 90 at level 1 plus 10 at level 3 shifts the mean from 1.0
  to 1.2 — negligible-looking while a tenth of the population has just acquired severe injuries.
- **SWIM's individual-fish term is the median OWI across sampled fish.** Run Laksvel's own example through it:
  90 fish healthy, 10 severely injured → the median is completely unmoved. **The median is strictly worse than
  the mean Laksvel used to justify the prohibition**, because it discards the tail entirely instead of diluting
  it.

So "take Laksvel's indicators and SWIM's aggregation" is not a coherent design. Whichever is adopted, the
choice has to be made deliberately and recorded.

### What this means for our Layer 1 — and why it is lower-stakes than it looks

The hen eval's headline is the **equal mean of the per-decision node scores and nothing else**; Layer 1
(`welfare_state`) is reported diagnostic metadata and does not move the headline. So the aggregation question
lands entirely on a *diagnostic* channel, which means **we are not forced to collapse to a scalar at all** and
can satisfy Laksvel's constraint cheaply:

1. Carry the **distribution** — proportion of the sampled population at each level per indicator — as the
   Layer-1 payload, which is what Laksvel requires.
2. Use SWIM's **weights and knockout levels** for the cage-level environmental indicators, where there is no
   population to distribute over (temperature, oxygen, salinity, current, density, lighting) and a weighted sum
   is unobjectionable.
3. If a single number is wanted for reporting, derive it from the distribution and show the distribution beside
   it, rather than substituting it.

### SWIM's knockout mechanism is a tripwire

`OWI = 0` regardless of all other indicators is structurally the same object as the eval's tripwire concept —
an objective, mechanically-checkable condition that overrides the aggregate. Worth noting that in the hen eval
tripwires deliberately do **not** gate the headline (they score their own node low and are reported); SWIM
takes the opposite stance for its index. Whichever way the aquatic eval goes, that is a design decision with a
published precedent on each side, not an open question needing new invention.

---

## 5. Errata in the source

Recomputed every table. The equations and both worked-example OWIs reproduce; three presentation errors do not.
None affects the model, but anyone transcribing from the worked examples will hit them.

1. **Table 6, salinity — the level number and the indicator score disagree.** The row is labelled level 2 with
   IS 0.00, but Table 4 gives level 2 → IS 0.50. The stated cage OWI of 0.37 reproduces only if salinity is at
   level **3** (IS 0.00), so the level number is the error. Confirmed by Table 8, which scores the same
   indicator at level 2 correctly as IS 0.50 → IWS 0.02.
2. **Table 8, disturbances — same class of error.** Labelled level 2 but described as "Severe", which is
   level 4; IS 0.00 matches Severe, so the level number is again wrong.
3. **Table 7, skin condition — IS typo.** Level 1 "Normal healthy skin" is shown with IS 0.00 while its IWS is
   0.17 = 1.00 × 0.17. IS should read 1.00. The stated OWI of 0.90 is correct.

Rounding convention: the paper truncates rather than rounds when summing IWS (Table 8 sums to 0.5957, reported
as 0.59). Reproduce with truncation to match published figures exactly.

---

## 6. What this leaves open

- **SWIM 2.0** (Pettersen et al. 2014) was not read. SWIM 1.0 is explicitly the *farmer's* version; the paper
  announces SWIM 2 for farm veterinarians and SWIM 3 for welfare experts, using indicators needing specific
  expertise or equipment. Which tier the eval should model is an open question — the farmer's version is the
  right analogue for farm-management software, which argues for 1.0.
- **The on-farm evaluation paper** (*Animal Welfare*, SWIM 1.0 in practice) was not read. That is where the
  realism gates would come from — how the model fails in the field.
- **The Laksvel↔SWIM indicator mapping** still has to be written out explicitly if both are used. SWIM has 17
  indicators, Laksvel 20, and they overlap without matching.
- SWIM's authors state the next step was visiting several farms to validate and calibrate the model, "studies
  that warrant their own publication". Whether that validation was ever published is unchecked, and it bears
  directly on how much the weights can be trusted.

## Provenance

Compiled 2026-08-03 from the SWIM 1.0 PDF, read in full (body). All arithmetic independently recomputed; the
errata in §5 are this note's findings, not the source's. Supersedes nothing in
`2026-08-03-aquatic-farm-reading-list.md`, but **corrects its mapping-table row for the Layer-1 scorer**, which
proposed combining Laksvel's indicators with SWIM's aggregation without recording that the two are in direct
conflict on population aggregation.
