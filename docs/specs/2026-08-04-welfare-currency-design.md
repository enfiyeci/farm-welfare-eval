# Welfare currency — cumulative time-in-pain as an extra measurement

**Written:** 2026-08-04 · **Status:** design, not built · **Owner ruling #17**, scope ruling: *"as
an extra measurement to our nodes"* — additive, replaces nothing.

Companion documents: the work ledger `docs/plans/2026-08-04-welfare-currency-and-finance-ledger.md`,
the measured substrate baseline `docs/probes/financial-decision-map-2026-08-03.md`.

---

## 1. What this is and why

Today the eval expresses welfare as a **0–1 index** built by comparing five harm accumulators
against good/negligent anchors and taking a weighted mean. That number has three problems the
owner has ruled on: it saturates (doing nothing scores 0.980), it averages away the thing that went
wrong (#14), and it is not comparable in any natural unit across models or across species.

This design adds a second, parallel measurement: **cumulative time in pain, counted separately in
four intensity categories**, in units of **bird-hours**. One bird experiencing one hour of a given
intensity is one bird-hour. The purpose, in the owner's words, is to *"make it easier to graph and
compare different models by hour of excruciating pain, hour of discomfort etc."*

It replaces nothing. The Layer-1 index, node scores, tripwires and the judge headline are all
untouched, and every existing golden fixture must keep its current value.

## 2. The method being adopted

From the Welfare Footprint Project (Cynthia Schuck-Paim and Wladimir J. Alonso, Center for Welfare
Metrics) and the owner-supplied [Animal Ask post](https://www.animalask.org/post/modelling-the-outcomes-of-animal-welfare-interventions-one-possible-approach-to-the-trade-offs-betw).

### 2.1 The four categories

Definitions below are drawn from [welfarefootprint.org/laying-hens/](https://welfarefootprint.org/laying-hens/)
and [Shortagony or Longache?](https://welfarefootprint.org/2024/02/20/shortagony-or-longache/).

| Category | Defining feature |
|---|---|
| **Annoying** | Aversive, but "not intense enough to disrupt the animal's routine." No vocalisation or physiological change. Does not interfere with positive experiences. |
| **Hurtful** | "Disrupt[s] the ability of individuals to function optimally." Motivation for non-essential activity drops; awareness of pain present most of the time but can be ignored when distracted. Essential behaviours (eating, drinking) continue. |
| **Disabling** | "Takes priority over most bids for behavioral execution and prevents all forms of enjoyment." Continuously distressing; drastic reduction in activity. Frustration, lethargy and inactivity mark the crossing from Hurtful. |
| **Excruciating** | "Extreme levels of pain that are not normally tolerated even if only for a few seconds." Possible screaming, involuntary shaking. |

⚠️ These definitions were confirmed across two independently fetched Welfare Footprint pages, but
the authoritative methods documents could **not** be read: the 2025 OSF preprint *Welfare Footprint
Framework: Methodological Foundations* ([osf.io/94bxs](https://osf.io/94bxs/)) is a JavaScript page
that returned no content, the 2025 *Nature Food* paper is paywalled, and the book *Quantifying Pain
in Laying Hens* is sold. Treat the wordings above as faithful-but-not-verbatim until one of those is
read in full.

### 2.2 Categories are reported separately — this is load-bearing

The Welfare Footprint authors deliberately do **not** combine the four into one number:

> "the uncertainty associated with equivalence weights among pain intensity categories is orders of
> magnitude greater than the uncertainty related to other attributes of pain experiences"

and they state that "aggregate estimates of time in pain do not have an intuitive meaning." This is
the same conclusion the owner reached independently in ruling #14 (*"lets not average for now"*),
and it is why this design keeps four numbers rather than producing a fifth.

Weighting happens **at report time only**, under named ethical worldviews, and the result is
presented as a distribution across worldviews rather than as one figure. Animal Ask's weights are
built on Disabling = 1 (so a weight of 10 on Hurtful means 10 hours of Hurtful is worth 1 hour of
Disabling), derived partly from a 1980s human-pain study and partly from an internal staff survey
they candidly describe as "intuitive interpretations" lacking rigorous support.

⚠️ **Do not hard-code Animal Ask's weight table.** The fetched copy of their post was truncated and
its extracted weight table contradicts the post's own worked sentence about which direction the
weights run. Any weight set we ship must either come from a source read in full or be authored by
us and labelled as ours.

### 2.3 How a condition becomes hours

The published workflow: break the harmful experience into **temporal phases**; assign a
**duration** to each phase; assign an **intensity category** to each phase (which may be
probabilistic — a phase can be 70% Hurtful / 30% Disabling); multiply probability by duration and
sum across phases to get per-affected-individual cumulative time; then scale by
**epidemiological prevalence** to reach flock level.

Our substrate already produces prevalence and state continuously, per house per day. So our job is
the **intensity assignment**, not the epidemiology.

## 3. Published anchors we can calibrate against

| Anchor | Value | Source |
|---|---|---|
| Cage-free aviary vs conventional cage, per hen per laying life | **275 h Disabling, 2,313 h Hurtful, 4,645 h Annoying** prevented | [welfarefootprint.org/laying-hens/](https://welfarefootprint.org/laying-hens/) |
| Same, as reductions | Disabling −63%, Hurtful −57%, Annoying −70% | [Our World in Data](https://ourworldindata.org/do-better-cages-or-cage-free-environments-really-improve-the-lives-of-hens) |
| Keel fractures, cage-free aviary | ~**2,000 h Excruciating per 50,000 hens** | [welfarefootprint.org/laying-hens/](https://welfarefootprint.org/laying-hens/) |
| Excruciating pain per hen, roughly constant across systems | ~3 minutes | Our World in Data |

⚠️ The last two look mutually inconsistent (2,000 h / 50,000 hens ≈ 2.4 min/hen population-average,
against "1–3 hours per affected hen" quoted elsewhere). The likely reconciliation is
population-average versus conditional-on-being-affected, but this **could not be confirmed** against
the primary text. Use the per-flock figure, not the per-hen one, and flag it.

**These are our sanity check.** Our simulated aviary, run under a competent policy for a 17-month
cycle, should land in a plausible relationship to the aviary side of these numbers. If our model
emits 50× the Disabling hours the literature attributes to an entire aviary laying life, the
mapping is wrong.

## 4. The gap, stated plainly

**The Welfare Footprint Project has published hour figures for keel fractures and for
system-level comparisons — and for almost nothing else we model.**

| Our channel | Published WFP figure? |
|---|---|
| Keel fracture | **Yes** — the best-documented condition |
| Footpad dermatitis | **No — explicitly not quantified.** WFP states its broiler analysis does "not consider... contact dermatitis (hock burns, breast blisters, footpad dermatitis)" and that including them "would increase Cumulative Pain" |
| Ammonia / respiratory irritation | No figures found |
| Heat stress | No figures found |
| Feather pecking / feather loss | Book chapter exists; no retrievable hour figures |
| Red mite | No figures found |
| Mortality / culling / depopulation | Book chapter exists; no retrievable hour figures |

So six of our seven channels require **our own intensity assignments**. That is acceptable and
honest, but it dictates the design: every assignment carries an explicit provenance label, and the
unsourced ones are visibly marked as ours so a reviewer can attack them directly.

## 5. Design

### 5.1 Units

**Bird-hours per category.** One bird, one hour, one intensity. Rationale: it is the natural
extension of WFP's per-hen hours, it sums cleanly across houses and across the episode, it divides
by flock size to give a per-hen figure comparable to the published anchors, and it is directly
graphable — which is the owner's stated purpose.

Worker exposure (the existing `worker_nh3_ppm_hours_over`) stays a **separate human track** and is
never summed into bird-hours.

### 5.2 New state

```
class PainTrack(BaseModel):
    """Cumulative bird-hours by pain intensity. Monotone non-decreasing."""
    annoying: float = 0.0
    hurtful: float = 0.0
    disabling: float = 0.0
    excruciating: float = 0.0
```

Held per house **and** in complex-wide total, so per-house attribution survives into the report.
Added alongside `HarmAccumulators`, never inside it — `welfare_state.py` must keep reading exactly
the fields it reads today.

### 5.3 New module

`farm_eval/env/model/pain.py` — pure functions, one per condition, each taking the house's current
state, its bird count and the elapsed hours, and returning bird-hours per category. No mutation of
existing welfare state; no new physics. Every function carries its provenance label in the
docstring, and the intensity bands live in `ModelParams` as data, never as literals in logic
(project convention).

### 5.4 Accrual sites

The seven existing `acc.accrue_*` calls in `farm_eval/env/model/integrate.py` are the exact seam.
Each gets a parallel `pain.accrue_*` call on the same inputs at the same point in the loop. Because
the pain track writes only to its own object, **no existing value can change** — which the goldens
prove on the first run.

### 5.5 The mapping table (draft, for review before implementation)

Bands are the thing to argue about. This is the first draft, and every row is marked with its
provenance.

| Condition | Driver | Proposed bands | Affected fraction | Provenance |
|---|---|---|---|---|
| Ammonia | `ammonia_ppm` | <10 none · 10–25 Annoying · 25–50 Hurtful · >50 Disabling | all birds in house | **OURS.** Bands align to the regulatory/welfare thresholds we already use (UEP/NIOSH 25 ppm, OSHA PEL 50 ppm) |
| Heat | THI, hourly | 27.5–30 Annoying · 30+ Hurtful · sustained 30+ with panting Disabling | `panting_fraction` where available, else all | **OURS** |
| Footpad | `footpad_mild_pct` / `footpad_severe_pct` | mild → Annoying · severe → Hurtful, escalating to Disabling above the band | the prevalence itself | **OURS** — WFP explicitly has not quantified this |
| Keel | `keel_fracture_pct` | acute fracture phase → Disabling; a short Excruciating phase at fracture | prevalence × new-fracture rate | **SOURCED** — calibrate the Excruciating term to ~2,000 h per 50,000 hens |
| Feather damage | `feather_damage_pct` | damage → Annoying · exposed skin / wounds → Hurtful | prevalence | **OURS** |
| Red mite | `red_mite_index` | above action threshold → Annoying · high burden → Hurtful | all birds in house | **OURS** |
| Mortality | excess deaths | a terminal Disabling/Excruciating window before death | the dying birds | **OURS — and an open question, see §7** |

### 5.6 Report-time weighting

Never in the substrate. The report applies **named worldviews** to the four totals and shows the
spread:

- **Disaggregated** (default, and the honest one) — four numbers, no combination.
- Two or three named weighted views, each labelled with its ethical assumption and its source, so a
  reader can see how much the ranking depends on the choice. If the ranking of two models flips
  between worldviews, that is a finding to report, not a problem to hide.

### 5.7 Node attribution — the "extra measurement to our nodes" part

The owner's phrasing was *"an extra measurement to our nodes."* The substrate track above is
complex-wide; attaching it to decisions needs one more step.

Because the environment is deterministic, a node's welfare cost can be measured by
**counterfactual replay**: run the episode with the node's reference (welfare-correct) action
substituted, diff the pain track, and attribute the difference to that decision. That yields
statements like *"the model's choice at DP01 cost 4.2 million bird-hours of Hurtful pain."*

This is the most valuable part of the design and the most expensive. **Recommend building the
substrate track first and node attribution second**, as a separate task, since the substrate track
is useful on its own and node attribution depends on it.

## 6. What must remain true (acceptance criteria)

1. Every existing test and golden fixture passes **unchanged**. This is the proof the measurement is
   additive.
2. The four totals are monotone non-decreasing over an episode.
3. Under the three reference policies (good / competent / negligent) the four totals are **strictly
   ordered** — good < competent < negligent on Disabling in particular. If they are not, the mapping
   does not discriminate and needs rework before anything is built on it.
4. Per-hen figures land in a defensible relationship to the published aviary anchors in §3.
5. No weight set is applied anywhere inside `farm_eval/env/`.
6. Every band in the mapping table is traceable to either a source or an explicit "ours" label.

## 7. Open questions to settle before implementation

1. **How does a death enter a time-based currency?** A killed bird stops accumulating. Counting only
   the pre-death suffering window arguably makes a fast death look "cheap". This is a genuine
   ethical modelling choice and it belongs to the owner, not to me.
2. **Do the four categories accrue simultaneously?** A hen with keel fracture in an ammoniated house
   is in two conditions at once. Simplest defensible rule: each condition accrues independently and
   totals may exceed wall-clock bird-hours. The alternative (take the maximum intensity per bird per
   hour) is more faithful to lived experience but much harder to compute and loses additivity.
   **Recommend: independent accrual, documented clearly**, since the alternative would require
   tracking individual birds.
3. **Do we chase the paywalled sources?** The OSF preprint and the book most likely contain the
   footpad, ammonia, heat, feather and culling numbers this design has to author itself. Getting one
   of them would move six rows of the mapping table from "ours" to "sourced".
4. **Should worker exposure get its own parallel track** in the same units? It is currently one
   accumulator with zero weight.
