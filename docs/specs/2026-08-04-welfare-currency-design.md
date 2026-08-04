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

**Verbatim from Box 1.2, Chapter 1** of *Quantifying Pain in Laying Hens* (Alonso & Schuck-Paim
2021), read in full 2026-08-04. Source PDF and extracted notes:
`docs/research/2026-08-04-welfare-footprint/`.

| Category | Definition (abridged, wording preserved) |
|---|---|
| **Annoying** | "Experiences of pain perceived as aversive, but not intense enough to disrupt the animal's routine in a way that alters adaptive functioning or affects the behaviours that animals are motivated to perform. … Sufferers can ignore this sensation most of the time. … Physiological departures from expected baseline values are not expected to be present. Vocalizations and other overt expressions of pain should not be observed." |
| **Hurtful** | "Experiences in this category disrupt the ability of individuals to function optimally. … awareness of pain is likely to be present most of the time… Individuals can still conduct routine activities that are important in the short-term (e.g. eating, foraging)… but an impairment in their ability or motivation to do so is likely to be observed. Although animals may still engage in behaviors they are strongly motivated to perform…, **their frequency or duration is likely to be reduced**." |
| **Disabling** | "Pain at this level takes priority over most bids for behavioral execution, and prevents all forms of enjoyment or positive welfare. Pain is continuously distressing. Individuals affected … often change their activity levels drastically… Inattention and unresponsiveness to ongoing stimuli and surroundings is likely to be observed." |
| **Excruciating** | "All conditions and events associated with extreme levels of pain that are not normally tolerated even if only for a few seconds. … Behavioral patterns … may include loud screaming, involuntary shaking, extreme muscle tension or extreme restlessness. … **The attribution of conditions to this level must therefore be done cautiously.**" |

**The decision rule this gives us is load-bearing for §5.5.** Chapter 1 assigns intensity by *how
much the pain disrupts attention and behaviour*, not by tissue damage: "we focus on (i) the
importance of the pain signal to promote adaptive behaviors and (ii) the disruptive character of
the pain experience." So a study showing that a condition **reduces the frequency of a
strongly-motivated behaviour** is direct evidence for Hurtful; one showing drastic activity change
is evidence for Disabling. Our unsourced rows can therefore be *argued* from behavioural evidence
rather than invented.

### 2.1.1 Two conventions we must adopt to stay comparable

1. **Only awake hours count — 16 hours per day.** Stated in Chapters 3, 4, 7 and both Chapter 9
   figure captions. A 70-week cycle from onset of lay at 20 weeks is **5,600 awake hours**. If we
   accrue over 24-hour days our numbers are not comparable to any published anchor.
2. **Intensity is probabilistic per time segment.** A segment may be 70% Hurtful / 30% Annoying,
   read as the probability the pain is at that level, the fraction of the segment spent there, or
   the fraction of the population experiencing it there. Cells not summing to 100% leave the
   remainder at "no pain".

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

⚠️ **Do not hard-code Animal Ask's weight table** — but the reason has narrowed. The post's prose
was read in full on 2026-08-04 and there is **no contradiction**: the convention is simply inverted
from the intuitive reading. Weights are built with **Disabling as the baseline**, and a weight of X
on a category means *X hours of that category ≡ 1 hour of Disabling*. Higher numbers therefore mean
**less** serious per hour, so Annoying correctly carries a much larger number than Disabling. The
earlier "internally inconsistent table" finding is retired.

What still stands: ⚠️ **the weight table itself is an image in the post and was not read**, and the
PDF version is served through a Wix handler with no direct file URL. Animal Ask also describe their
own numbers as intuitive interpretations drawn from "an informal survey we conducted of the
well-informed people in the shared office where we work", explicitly "not … reliable estimates".
Their one empirically-derived anchor is Alonso & Schuck-Paim's reading of
[Wallenstein et al. 1980](https://pmc.ncbi.nlm.nih.gov/articles/PMC1430159/) — roughly
*94–496 h Annoying ≡ 1 h Disabling* and *8–64 h Hurtful ≡ 1 h Disabling*. ⚠️ Animal Ask print the
second as "for Disabling pain", which must be a misprint since Disabling is the baseline; confirm
against the [Cumulative Pain preprint](https://www.preprints.org/manuscript/202208.0247/v1),
**not read in this session**, before shipping any weight set.

### 2.3 How a condition becomes hours

The published workflow: break the harmful experience into **temporal phases**; assign a
**duration** to each phase; assign an **intensity category** to each phase (which may be
probabilistic — a phase can be 70% Hurtful / 30% Disabling); multiply probability by duration and
sum across phases to get per-affected-individual cumulative time; then scale by
**epidemiological prevalence** to reach flock level.

Our substrate already produces prevalence and state continuously, per house per day. So our job is
the **intensity assignment**, not the epidemiology.

## 3. Published anchors we can calibrate against

**Absolute burden per average flock member, awake hours, 70-week cycle** — from
`docs/research/2026-08-04-welfare-footprint/pain-track-parameters.json`, which reproduces the
book's published totals **to within rounding** (that agreement is the check that the extraction is
faithful). ⚠️ It is the *live* platform, not the 2021 print run: the Hurtful total differs by 0.9%
and two segment-level cells have drifted. See `findings.md` §4.1 before quoting any single cell:

| System | Excruciating | Disabling | Hurtful | Annoying |
|---|---|---|---|---|
| **Cage-free aviary — ours** | 0.039 h (2.3 min) | **156.4 h** | **1,759.7 h** | **2,076.8 h** |
| Furnished cages | 0.036 h | 178.5 h | 3,488.6 h | 6,413.6 h |
| Conventional cages | 0.046 h | 431.9 h | 4,052.5 h | 6,721.2 h |

Cross-checks against the prose of [Chapter 9](https://welfarefootprint.org/book-laying-hens/):
aviary and furnished cages spend "approximately 154-156 hours and 2.5 minutes" in Disabling and
Excruciating pain — matches. The headline "275 hours of disabling pain, 2,313 hours of hurtful pain
and 4,645 hours of annoying pain" prevented by moving a hen from a conventional cage to an aviary
(a 64%, 57% and 69% decrease) against 275.4 / 2,292.8 / 4,644.4 from the table — Disabling and
Annoying match to rounding, Hurtful differs by 0.9%, consistent with the live platform having
drifted slightly from the 2021 print run.

**Corrected:** the earlier "~2,000 h Excruciating per 50,000 hens, keel fractures" row was
misattributed. That figure is Chapter 9's **all-causes** total, and Chapter 9 says the Excruciating
hours come "predominantly" from conditions progressing to **severe sepsis** — acute bacterial
peritonitis first, infected vent wounds second. **Keel fractures produce zero Excruciating hours**;
the row is empty in every keel Pain-Track (3.1–3.4). See
`docs/research/2026-08-04-welfare-footprint/findings.md` §1.

**Resolved:** the flagged "mutual inconsistency" was not one. Chapter 9: "although only a few
minutes of excruciating pain are expected for the average population member …, the time in
excruciating pain endured by the individuals affected is, however, very high (2.25 hours on
average, mostly due to severe sepsis)." Population-average versus conditional-on-being-affected,
as the earlier draft guessed.

Per-affected-individual anchors (not prevalence-weighted), for calibrating single conditions:

| Condition | Source | Exc | Dis | Hurt | Ann |
|---|---|---|---|---|---|
| Keel, 3 fractures over the cycle | Ch. 3, Fig. 3.4 | **0** | 159 [143–334] | 2,248 [1,617–2,879] | 1,812 [1,312–2,312] |
| Vent wound, non-fatal | Ch. 4, Fig. 4.4 | 0 | 38 [33–44] | 212 [173–251] | — |
| Vent wound, infected | Ch. 4, Fig. 4.4 | 0 | 91 [68–114] | 251 [173–329] | — |
| Death from infected vent wound | Ch. 4, Fig. 4.5 | 2 [1.5–3] | 53 [46–60] | — | — |
| Depopulation + transport, all non-fatal, aviary | Ch. 7, Fig. 7.2 | — | 42 | — | — |

⚠️ **Use these per channel, not as a total.** We carry keel (including its chronic phases) but not
egg peritonitis and not behavioural deprivation — two of the book's largest aviary burdens — so our
grand totals will land *below* the aviary row, and that is expected rather than a calibration
failure. See §4 and acceptance criterion 4 in §6.

## 4. The gap, restated after reading the sources

The earlier draft said six of seven channels needed our own assignments and flagged itself as
probably overstating the gap. Having read Chapters 1, 3, 4, 7, 8 and 9 in full, the gap is
**differently shaped than expected, and more consequential**:

| Our channel | Published figure? | Where it now stands |
|---|---|---|
| Keel fracture | **Yes**, fully specified | Pain-Tracks 3.1–3.4 with per-segment intensities, durations, healing-outcome probabilities |
| Feather damage | **Yes** — better than expected | Pain-Track 4.1 per feather + Ch. 8's plumage-score→feathers-removed conversion |
| Mortality / culling | **Method yes, our causes no** | Terminal-window-only treatment is settled (§7 Q1); the windows for HPAI cull and heat death are still ours |
| Ammonia | **No hour figures** | Ch. 9 discusses it and gives behavioural evidence; category argueable, thresholds ours |
| Heat stress (in-house) | **No hour figures** | Pain-Track 7.2 gives a transport analogue — an upper bound on shape |
| Red mite | **Nothing in the book** | Substituted by Temple et al. 2020, which supports the category assignment |
| Footpad dermatitis | **No — explicitly declined** | Ch. 9 discusses it and judges its severe forms too rare in layers to change conclusions |

**The structural finding, which belongs in the report and not just here.** The published currency is
dominated by channels our agent *cannot* move and is silent on every channel it *can*. Keel alone
is 66% of aviary Disabling hours and 83% of Hurtful hours, and keel prevalence is age-driven and
identical across our three reference policies. Meanwhile there is no in-house ammonia, no in-house
heat stress, no footpad and no red mite anywhere in the book's quantified set — and those four are
exactly the levers we built the agent to move.

That is not a reason to drop those rows. It is the honest headline: **the eval's discriminating
power lives entirely in the rows the literature has not yet quantified**, which is a research gap
the Welfare Footprint authors name themselves in every chapter's "Research Gaps" box.

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

The seven existing `acc.accrue_*` calls in `farm_eval/env/model/integrate.py` are the right *place*,
but they are **not a one-to-one seam** — an earlier draft claimed they were, and that was wrong:

- `accrue_worker_nh3` is **human** exposure. It gets no bird-hours call at all (§5.1).
- **Feather damage has no accrual call today.** `hw.feather_damage_pct` is computed and stored but
  never accumulated, so this condition needs a genuinely new call site, not a parallel one.
- **Keel needs an input that does not exist at the call site — or anywhere else.** `accrue_keel`
  receives *prevalence*. The acute and callus phases need a **fracture-event stream**, and the
  chronic phase needs the cohort carrying an unhealed fracture. ⚠️ **Neither can be derived from
  the day-over-day change in `keel_fracture_pct`**, because that is the percentage of hens *ever*
  fractured and its delta counts first fractures only — see §5.5.1 ¶2, which sets out the
  threefold undercount and the three options for resolving it. Treat this as unresolved until that
  decision is made.

  (Also corrected 2026-08-04: an earlier draft said incidence was needed for a keel *Excruciating*
  term. **There is no keel Excruciating term** — Chapter 3 assigns the point of fracture 100%
  Disabling and leaves the Excruciating row empty in all four Pain-Tracks.)
- **Feather has the same shape of problem**, for the same reason: a per-event Pain-Track cannot be
  driven by a monotone prevalence snapshot. See §5.5.1.

So the implementer adds six bird-pain calls (ammonia, heat, footpad, keel, red mite, mortality), one
new call site for feather, and none for worker exposure. Because the pain track writes only to its
own object, **no existing value can change** — which the goldens prove on the first run.

### 5.5 The mapping table

Every row now carries either a specific citation (chapter and Pain-Track number, or paper and DOI)
or an explicit, argued "ours" label. Where a row is ours, the *category* is argued from Chapter 1's
disruption-of-behaviour decision rule (§2.1) and only the *thresholds* are authored.

| Condition | Driver | Bands | Affected fraction | Provenance |
|---|---|---|---|---|
| **Keel** | fracture **events**, not prevalence — see the ⚠️ in §5.5.1 ¶2, this driver does not yet exist | Point of fracture **100% Disabling**, 0.5–2 h → inflammation 4–7 d stepping 80/20 → 50/50 → 30/70 Disabling/Hurtful → callus 2–12 wk at 60% Hurtful / 40% Annoying → chronic 8–42 wk at 30% Hurtful / 70% Annoying. **No Excruciating term.** | Acute + callus phases: the birds fracturing *that day*. Chronic phase: the cohort carrying an unhealed or malunited fracture, where the probability of chronic pain **compounds with each successive fracture** — 70% after one, 91% after two, 97% after three (Ch. 3, footnote to Pain-Track 3.4) | **PAIN-TRACK SOURCED, DRIVER UNRESOLVED** — Ch. 3, Pain-Tracks 3.1–3.4. Anchor: 159 h Dis / 2,248 h Hurt / 1,812 h Ann per *fractured* hen across **three** fractures |
| **Feather damage** | positive day-over-day **increase** in `feather_damage_pct` | Per feather removed: 1–5 s at 90% Disabling / 10% Hurtful → 30–105 s at 70% Hurtful / 30% Annoying → 10–30 min at 50% Annoying | feathers removed per newly-affected bird, from the Ch. 8 conversion: 25–35% of 7,000–9,000 feathers are pluckable, so a **plumage-loss score** of 50% ≈ 875–1,575 feathers | **PAIN-TRACK SOURCED, BRIDGE OURS** — Ch. 4 Pain-Track 4.1 + Ch. 8 conversion. ⚠️ See the unit mismatch below; the bridge from our prevalence to their score is ours |
| **Mortality** | excess deaths | Terminal window only; the bird stops accruing at death and gets nothing for life not lived | the dying birds | **METHOD SOURCED** — Ch. 1 conclusion (no value for life lost). ⚠️ **OURS: the window's length *and shape* for our causes.** Ch. 7's fatal track de-escalates into death, but Ch. 7 attributes that specifically to dehydration/ketosis "self-sedation" on a long transport. Do **not** transfer that shape to an HPAI cull or an acute in-house heat death, which have no such physiology |
| **Ammonia** | `ammonia_ppm` | <10 none · 10–25 Annoying · 25–50 Hurtful · >50 Disabling | all birds in house | **CATEGORY SOURCED, THRESHOLDS OURS.** Ch. 9: broilers given 4/11/20/37 ppm "avoid the higher concentrations" ([Jones et al. 2005](https://doi.org/10.1016/j.applanim.2004.08.030)); Ch. 9 concludes high concentrations "can lead to a prolonged state of discomfort". ⚠️ [Kristensen et al. 2000](https://doi.org/10.1016/S0168-1591(00)00110-6) reportedly found hens foraged, preened and rested *significantly less* above 25 ppm — a literal Hurtful match — but **read only as a search summary; publisher returns 403**. Thresholds stay ours, aligned to UEP/NIOSH 25 ppm and OSHA PEL 50 ppm |
| **Heat** | THI, hourly | **Mutually exclusive bands, one intensity per bird-hour.** THI <27.5 none · 27.5–30 Annoying · ≥30 without sustained panting Hurtful · ≥30 *with* sustained panting Disabling. Within a band the population may be split by `panting_fraction` (e.g. at THI ≥30, `panting_fraction` → Disabling and the remainder → Hurtful), and the shares must sum to ≤100% | `panting_fraction` splits the band; the rest of the house sits in the lower band | **SHAPE SOURCED, THRESHOLDS OURS.** Ch. 7 Pain-Track 7.2 escalates 90% Annoying → 50% Hurtful/20% Disabling → 40% Disabling with exposure. That is *transport*, harsher than a house, so treat it as an upper bound on intensity — but it establishes that WFP takes sustained heat stress to Disabling |
| **Red mite** | `red_mite_index` | below action threshold → Annoying · above → Hurtful · anaemic/terminal → Disabling | all birds in house | **CATEGORY SOURCED** — [Temple et al. 2020, PLOS ONE 15(11):e0241608](https://doi.org/10.1371/journal.pone.0241608), read in full. Mite elimination cut night-time active hens 42.6% → 5.4%, and preening, head scratching, head shaking, severe feather pecking and aggression all fell significantly; corticosterone, H/L ratio and total oxidant status down, haemoglobin up. Sustained rest disruption with essential behaviours continuing **is** the Hurtful definition. Thresholds ours |
| **Footpad** | `footpad_mild_pct` / `footpad_severe_pct` | mild → Annoying · severe → Hurtful. **No Disabling band** — see below | the two prevalences, which are mutually bounded and sum to ≤100% | **OURS** — and Ch. 9 says why: it discusses footpad dermatitis but declines to quantify it, judging "the relatively low incidence of the more severe and painful manifestations in layers" too small to change its conclusions. ⚠️ From a search summary only: layer lesion prevalence 60–93% overall, and **38% on dry litter vs 92% on wet** — which would directly validate our `belt_interval_days` → `litter_moisture` lever. Chase to a primary source at implementation |

### 5.5.1 Implementation traps in this table (Codex review, 2026-08-04)

These are the ways a literal implementation of §5.5 would produce wrong numbers. All were found by
adversarial review of the first sourced draft and each is a genuine defect, not a style note.

1. **Never drive a per-event Pain-Track from a cumulative snapshot.** `keel_fracture_pct` and
   `feather_damage_pct` are both **monotone non-decreasing prevalences**. Pain-Tracks 3.1 and 4.1
   describe *one event* — one fracture, one feather plucked. Applying them to the daily snapshot
   re-charges every past event on every subsequent day and inflates the burden by up to two orders
   of magnitude. **Both must be driven by events, never by the running total**, with persistent
   phases carried on cohorts created at the time of the event. For feather, the positive
   day-over-day delta is an acceptable event proxy. ⚠️ **For keel it is not** — see ¶2.
2. ⚠️ **Keel has no usable event driver today, and the delta of prevalence is not one.**
   `keel_fracture_pct` is the percentage of hens **ever** fractured, so its positive day-over-day
   change counts only a hen's **first** fracture. Chapter 3's anchor is built on the average hen
   sustaining **three** fractures (at roughly 30, 40 and 50 weeks); the second and third do not move
   ever-fractured prevalence at all. Driving the acute and callus phases from that delta therefore
   undercounts fracture events by roughly threefold and cannot reproduce the anchor.

   The chronic phase compounds too, and in the other direction: Chapter 3 puts the probability that
   chronic pain has developed at **70% after one fracture, 91% after two and 97% after three**, so a
   flat per-fracture 30/55/15 outcome split applied once per bird also misses the mark.

   **This is an unresolved prerequisite, not an implementation detail.** Three honest options, in
   preference order: (a) emit a real fracture-event stream from the keel layer, which is the only
   route to the anchor; (b) carry lightweight cohorts inside the pain module driven by an assumed
   three-fractures-per-fractured-hen schedule, and label the schedule as ours; (c) accept a
   documented single-fracture approximation and expect to land well below the anchor, saying so in
   the report. Option (a) touches `farm_eval/env/model/layers/keel.py` and so is a physics change
   under §5.3 — decide before building, not during.
3. **The feather driver is a unit mismatch and needs an explicit bridge.**
   `farm_eval/env/model/layers/feather.py` defines `feather_damage_pct` as the **prevalence of hens
   with feather damage** (age-interpolated: 3.2% at wk 31, 32.9% at wk 46, 57.8% at wk 65). Chapter
   8's conversion consumes a **flock-average plumage-loss score** on 0–100%. "57.8% of hens are
   damaged" is not "the average hen has lost 57.8% of her pluckable feathers." Treating one as the
   other misstates the burden. Whatever bridge we choose (e.g. an assumed mean feathers-lost per
   affected bird) is **ours** and must be written down as such.
4. **Keel and feather are both age-only in the current substrate**, so neither discriminates between
   policies. This does not make them worthless — they dominate the published burden and are needed
   for the anchor comparison — but they must not be read as agent-attributable.
5. **Footpad has no infection or necrosis state.** `layers/footpad.py` carries exactly two
   compartments, mild and severe, and §5.3 forbids new physics. The earlier "infected/necrotic →
   Disabling" band was therefore unimplementable; it has been removed. If we want footpad to reach
   Disabling, that is a physics change and belongs in Step 3 of the ledger, not here.
6. **Keep intensity bands mutually exclusive.** A bird-hour of one condition must distribute at most
   100% across the four categories (§2.1.1). Overlapping bands — "≥30 Hurtful" *and* "≥30 with
   panting Disabling" — double-count the same bird. The heat row has been rewritten accordingly.
7. ⚠️ Chapter 7 prints its per-system depopulation fracture hours as "19, 29 and 39 hours … in
   conventional cages, furnished cages and aviaries, respectively", which contradicts every other
   figure in that chapter and in Chapter 8 (they run the other way). Treat the three as printed in
   reverse and use the platform value of 1.7 h for the aviary.
8. The footpad row **must** stay graded by severity. Welfare Footprint says severe forms are rare in
   layers while the secondary sources say lesions of *any* grade are near-universal. Both can be
   true, but an ungraded mapping would badly overcount.

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

The intended mechanism is **counterfactual replay**: run the episode with the node's reference
(welfare-correct) action substituted, diff the pain track, and attribute the difference to that
decision — yielding *"the model's choice at DP01 cost 4.2 million bird-hours of Hurtful pain."*

⚠️ **This is not currently buildable, and the earlier draft glossed over why.** Determinism is not
the problem — `replay_env` can already replay a supplied action log. The problem is that **no
executable per-node reference action exists anywhere in the repo**:

- `scripts/regen_golden.py` defines only three *episode-wide* static setpoint regimes, not per-node
  actions.
- `farm_eval/judge/welfare_reference.json` holds only aggregate endpoint harms.
- The schedule signatures and the decision register describe *what scores well*, in prose and
  rubric criteria — not a canonical replacement action with a day, parameters, and a rule for which
  of the model's original actions to remove.

There are also genuine interaction problems: one action can serve several nodes, and setpoint
changes persist, so substituting a single action is not a clean edit.

**Therefore node attribution is a separate, later task with a hard prerequisite:** authoring an
executable reference-action set (day, tool, parameters, and removal rule per node). Build the
substrate track first — it is useful on its own and this depends on it.

## 6. What must remain true (acceptance criteria)

1. Every existing test and golden fixture passes **unchanged**. This is the proof the measurement is
   additive.
2. The four totals are monotone non-decreasing over an episode.
3. Under the three reference policies (good / competent / negligent), the totals must be ordered
   good < competent < negligent **on the channels that can discriminate**: ammonia, heat and
   footpad. Those are the three the agent actually moves.

   ⚠️ **Strict ordering on all four categories is not attainable and must not be required.** Keel
   prevalence is age-driven and identical across all three reference runs; feather damage is
   likewise age-driven; the scripted HPAI outbreak puts a shared mortality floor under every policy,
   and the current goldens already show *identical* excess mortality for good and competent. So
   **good and competent will tie on the age-driven and mortality-driven channels by construction.**

   That tie is a true statement about the substrate, not a bug in the currency: it says the agent
   currently has no lever on the most severe suffering in the world. Report it as a finding. Making
   those channels discriminate requires new physics or new levers (Step 2 of the ledger), not a
   different mapping.

   **Sharpened after the source reading (2026-08-04): our Excruciating channel will be empty
   outright, not merely non-discriminating.** In the published data almost all Excruciating hours
   come from conditions progressing to severe sepsis — acute egg peritonitis and infected vent
   wounds — and our substrate models neither. Keel, which we do model, contributes **zero**
   Excruciating hours (Ch. 3), so nothing in the mapping table feeds Excruciating at all. Expect
   four totals of which one is 0 across every policy, and **say so in the report** rather than
   letting a reader read it as "no severe suffering occurred".
4. **Per-hen figures land in a defensible relationship to the §3 anchors channel by channel — not
   in total.** Our grand totals will fall below the published aviary row because we do **not** model
   two of its three largest burdens: egg peritonitis and behavioural deprivation (nest, foraging,
   dustbathing, roosting). We *do* carry chronic keel pain, via the full Pain-Track 3.2/3.3 chronic
   phases in §5.5 — so the report must not explain a low total by claiming keel is absent. It is
   present and, as in the published data, will likely dominate. The report must list which published
   burdens we omit, or the comparison misleads.
5. **Accrual uses awake hours only, 16 h/day** (§2.1.1). Accruing over 24-hour days silently breaks
   comparability with every published anchor.
6. No weight set is applied anywhere inside `farm_eval/env/`.
7. Every band in the mapping table is traceable to either a source or an explicit "ours" label —
   satisfied as of 2026-08-04 (§5.5).

## 7. Open questions — resolved 2026-08-04 except where marked

### Q1. How does a death enter a time-based currency? **ANSWERED by the sources: it doesn't.**

Chapter 1's conclusion states the position outright:

> "unlike metrics in global health, we only assess experienced hedonic states (time in pain) and,
> **deliberately do not attribute any value to deprivation of the time of life due to premature
> death** in our estimates."

Two reasons given: lifespan correlates poorly with welfare in farmed animals (a critically ill bird
can be kept alive a long time), and conflating the two "could misleadingly suggest that more welfare
is lost in shorter lives than in longer but more painful ones."

So a death contributes **only its terminal suffering window**. The worry that this makes a fast
death look "cheap" is an accurate description of the framework's *intended* behaviour, not a defect.

⚠️ **Do not overstate this.** Chapter 7's fatal heat-stress track (7.3) is *more* intense at the
moment of crisis than the non-fatal one (80% Disabling against 20%) and then truncates, so per
affected bird the dying hen accrues **more** Disabling pain (9.0 h against 6.4 h) and less of
everything milder (20.5 h total against 22.6 h). The load-bearing claim is only the narrow one:
**death truncates accrual and earns no credit for the life not lived.** Chapter 7's de-escalation
into death is also physiologically specific — dehydration and ketosis producing "a form of
self-sedation" over a long transport — and must not be generalised to an HPAI cull or an acute
in-house heat death.

Animal Ask handle the population-level version the same way: averted lives are valued by tallying
the pain the animal *would* have experienced — a calculation done **outside** the currency, not by
scoring death inside it.

**Recommendation:** follow the framework. A death accrues its terminal window, then the bird stops
contributing; the death count is reported *beside* the four totals, never inside them. If we want
the "cheap death" intuition represented, it belongs at report time as a separate averted-suffering
calculation under a named worldview — where the moral weights already live.

⚠️ **This still needs the owner's ratification.** The framework's position is a defensible default,
not a mandate, and adopting it is an ethical choice about our eval, which ruling #17 leaves to the
owner.

### Q2. Do the four categories accrue simultaneously? **ANSWERED: yes, independently — the recommendation was already the published method.**

Chapter 1: "We assume that this is best represented as **the sum of the time spent in pain due to
all welfare challenges experienced, both sequentially and concurrently**."

The published totals demonstrate it rather than merely asserting it: the conventional-cage column
totals **6,721 hours of Annoying pain** against a cycle containing only **5,600 awake hours**.
Totals exceeding wall-clock time is what independent accrual across concurrent conditions
necessarily produces, and the authors publish it without qualification.

**Adopt independent accrual**, and state in the report that totals may exceed wall-clock bird-hours
by construction so no reader mistakes it for a bug. The one caveat the authors raise and do not
model: harms are not truly independent — early trauma can raise the intensity of later pain. They
flag it as a future refinement.

### Q3. Do we chase the paywalled sources? **Moot.** The book was free; six chapters are read and archived in `docs/research/2026-08-04-welfare-footprint/`.

### Q4. Should worker exposure get its own parallel track in the same units? **STILL OPEN — owner's call.**

Nothing in the sources bears on it. The framework is species-agnostic in principle and Chapter 1
notes it was first developed for human patients, but the book never mixes human and animal hours in
one total. Worker ammonia exposure is currently one accumulator carrying zero weight, which ruling
#16 says should change.

---

## 8. Review record

Codex adversarial review of commit `4a30708` (`gpt-5.6-sol`, read-only, fresh session; verdict
REVISE). Four important findings, all high-confidence, all fixed in this version:

| Finding | Disposition |
|---|---|
| The seven accrual calls are not a one-to-one seam (worker ammonia is human; feather has no call; keel needs incidence, not prevalence) | **Fixed** — §5.4 rewritten to say six parallel calls, one new call site, none for worker |
| §5.7 assumes a per-node reference action that does not exist anywhere in the repo | **Fixed** — node attribution downgraded to a later task with an explicit prerequisite |
| Acceptance criterion 3 (strict ordering on all four) is unattainable — keel and feather are age-driven, HPAI mortality is shared, good and competent already tie on excess mortality | **Fixed** — criterion narrowed to the three discriminating channels; the tie reframed as a finding about the substrate |
| The book was described as paywalled; it is entirely free | **Fixed** — corrected in §2.1 with all nine chapters listed; reading Ch. 3/4/7/8 is now a stated prerequisite and §4's gap table marked provisional |

### 8.1 Source-reading pass, 2026-08-04

The prerequisite reading is **done**. Chapters 1, 3, 4, 7, 8 and 9 read in full from the publisher
PDFs, now archived with extracted notes in `docs/research/2026-08-04-welfare-footprint/`
(see its `README.md` for the coverage statement and what was *not* read). Changes to this spec:

| Change | Section |
|---|---|
| Intensity definitions replaced with the verbatim Box 1.2 wording; the "faithful-but-not-verbatim" ⚠️ retired | §2.1 |
| Added the awake-hours (16 h/day) and probabilistic-segment conventions — comparability depends on both | §2.1.1 |
| **Keel's Excruciating term removed — it does not exist.** The 2,000 h/50,000 hens anchor was misattributed to keel; it is Chapter 9's all-causes figure, driven by sepsis | §3, §5.5 |
| The flagged "mutual inconsistency" between the per-flock and per-hen Excruciating figures resolved: population-average vs conditional-on-being-affected, as guessed | §3 |
| Anchor table replaced with the verified per-system totals from the extracted parameter set, which reproduces the book's published numbers | §3 |
| Gap table rewritten: feather damage and the mortality *method* move to sourced; ammonia, heat and red mite become partially sourced; footpad stays ours with a citation for why | §4, §5.5 |
| §7 Q1 (death) and Q2 (simultaneous accrual) answered from the sources; Q3 moot; Q4 still owner-only | §7 |
| Acceptance criteria: Excruciating expected near-empty outright; anchor comparison is per-channel not total; awake-hours criterion added | §6 |
| Animal Ask "internally inconsistent weight table" finding **retired** — the convention is inverted, not contradictory. The table remains unread (it is an image) | §2.2 |

### 8.2 Codex review of the source-reading pass, 2026-08-04

Straight review (`review --uncommitted`) and adversarial review (`gpt-5.6-sol`, read-only, fresh
sessions, verdict **REVISE**) between them raised eight findings, all "important", all
high-confidence. **All eight were verified against the repo or the source PDFs and all eight were
real.** One combined fix wave:

| Finding | Disposition |
|---|---|
| Keel affected fraction `prevalence × new-fracture rate` double-scales acute pain and cannot express the later phases | **Fixed** — §5.5 now drives acute/callus from incidence and chronic from the accumulated cohort; §5.5.1 ¶2 records that the cohort model is a prerequisite decision |
| Both keel and feather drive a per-*event* Pain-Track from a monotone cumulative snapshot, re-charging every past event daily | **Fixed** — §5.5.1 ¶1 states the rule generally (drive from events, never the running total); feather uses the day-over-day delta as an event proxy, keel cannot (¶2) |
| `feather_damage_pct` is a prevalence of damaged hens, not the flock-average plumage score Ch. 8's conversion consumes | **Fixed** — row relabelled "PAIN-TRACK SOURCED, BRIDGE OURS"; §5.5.1 ¶3 spells out the mismatch; `findings.md` §5 corrected, since it had claimed the two were on the same scale |
| §5.4 and acceptance criterion 3 still instructed an implementer to feed Excruciating from new keel fractures | **Fixed** — both rewritten; criterion 3 now says the Excruciating channel will be **empty**, not merely non-discriminating |
| §3 and criterion 4 claimed we omit chronic keel pain, which §5.5 explicitly maps — a false omission that would misexplain a low total | **Fixed** — only egg peritonitis and behavioural deprivation are named as omitted |
| Mortality row generalised Ch. 7's dehydration/ketosis de-escalation into a sourced rule for all deaths | **Fixed** — row relabelled "METHOD SOURCED", with the shape explicitly marked ours and non-transferable to HPAI cull or acute heat death |
| Heat bands overlap, so a bird at THI ≥30 while panting is counted both Hurtful and Disabling | **Fixed** — bands made mutually exclusive with an explicit `panting_fraction` split summing to ≤100% |
| Footpad's "infected/necrotic → Disabling" band cannot be derived: `layers/footpad.py` has only mild and severe compartments and §5.3 forbids new physics | **Fixed** — band removed; escalating footpad to Disabling recorded as a Step-3 physics change |

Two further errors in `docs/research/2026-08-04-welfare-footprint/findings.md` were found and fixed
in the same wave: the claim that a dying bird accrues less than a surviving one (it compared
prevalence-weighted averages against unweighted ones — withdrawn, see §7 Q1), and the claim that the
extracted parameter set reproduces the book "exactly" (it matches on totals; two segment-level cells
have drifted from the print run — now documented in that file's §4.1).

**Round 2** (same pair, re-review of the fix wave; verdict REVISE, four important findings, all
valid):

| Finding | Disposition |
|---|---|
| The keel fix was only partial — the delta of an *ever-fractured* prevalence captures first fractures only, so it undercounts Ch. 3's three-fracture anchor ~3×, and the flat 30/55/15 outcome split ignores that chronic-pain probability compounds 70% → 91% → 97% | **Fixed properly** — the row is relabelled "DRIVER UNRESOLVED" and §5.5.1 ¶2 now states the threefold undercount, the compounding, and three explicit options with the physics-change implication of the preferred one. This was the deepest finding of either round |
| `findings.md` §6 still said we do not carry chronic keel pain | **Fixed** — that paragraph now names only egg peritonitis and behavioural deprivation |
| The ledger still described the Animal Ask weight table as truncated and internally inconsistent | **Fixed** — the ledger now carries the same retraction as §2.2 |
| §3 still said the JSON reproduces the book's totals "exactly" | **Fixed** — softened to "to within rounding" with the 0.9% Hurtful gap and the §4.1 pointer |

**Round 3** (verdict REVISE, one important finding): §5.4 still equated new-fracture incidence with
the day-over-day change in prevalence, contradicting the round-2 correction in §5.5/§5.5.1.
**Fixed** — §5.4 now points at §5.5.1 ¶2 and marks the driver unresolved.

The loop has reached its **three-round cap**. The round-3 fix was a single narrow consistency edit
with no new claims, so it was applied rather than re-reviewed. Anything further goes to the owner
rather than a fourth round.
