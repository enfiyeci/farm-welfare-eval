# Welfare Footprint source reading — what the book actually says

**Read:** 2026-08-04 · **Purpose:** move the welfare-currency spec's §5.5 mapping table from
mostly-authored-by-us to mostly-sourced, and answer its §7 open questions.

Companion: the design spec
`docs/specs/2026-08-04-welfare-currency-design.md`; the work ledger
`evals/hen/design/decisions/2026-08-04-welfare-currency-and-finance-ledger.md`.

---

## 0. Coverage statement

Read **end to end, from the PDFs in `sources/`**, in this session:

| Chapter | Pages | Status |
|---|---|---|
| Ch. 1 — The Comparative Measurement of Animal Welfare: the Cumulative Pain Framework | 29 | read in full |
| Ch. 3 — Quantifying the Pain due to Keel Bone Fractures | 28 | read in full |
| Ch. 4 — Welfare Implications of Injurious Pecking | 27 | read in full |
| Ch. 7 — The Last Day of a Hen's Life: Depopulation and Transport | 19 | read in full |
| Ch. 8 — Prevalence of Welfare Harms by Housing System | 30 | read in full |
| Ch. 9 — Impact of the Transition from Caged to Cage-free Housing | 31 | read in full |

Ch. 1 and Ch. 9 were **not** in the owner's list of four but were added deliberately: Ch. 1 is the
only place the intensity categories are defined verbatim and the only place the treatment of death
is stated, and Ch. 9 is where the system-level anchor numbers in the spec's §3 actually come from.

Also read in full:

- The **Animal Ask** post, *Modelling the outcomes of animal welfare interventions*
  ([link](https://www.animalask.org/post/modelling-the-outcomes-of-animal-welfare-interventions-one-possible-approach-to-the-trade-offs-betw)) — all prose.
  ⚠️ **Its tables are images, not text.** The category-definition table and the worldview weight
  table (worldviews A–N) could not be read. The linked PDF version is served through a Wix document
  handler that exposes no direct file URL, so it was not retrieved either. Every claim below about
  Animal Ask rests on its prose only.
- Temple et al. 2020, *Assessment of laying-bird welfare following acaricidal treatment…*,
  PLOS ONE 15(11):e0241608 ([open access](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0241608))
  — read in full through the Conclusion; the reference list was not read line by line.

Retrieved but **not** a document read: `https://pain-track.org/hens`. Its embedded
`__NEXT_DATA__` payload is the machine-readable parameter set behind the whole book, extracted
verbatim to `pain-track-parameters.json` in this folder. It is data, not prose.

⚠️ **Not read in THIS pass:** Ch. 2 (life of commercial layers), Ch. 5 (egg peritonitis), Ch. 6
(psychological pain / behavioural deprivation). Claims below that touch peritonitis or behavioural
deprivation come from Ch. 8 and Ch. 9, which cite them. **Ch. 5 and Ch. 6 were subsequently read in
full on the same day** — see `findings-ch05-ch06.md` in this folder, which supersedes this
paragraph for those two chapters and revisits §6's structural finding. Ch. 2 remains unread.

⚠️ Kristensen et al. 2000 (hen ammonia preference) was read **only as a search-result summary**;
the publisher page returns HTTP 403. See §5 for exactly which claim depends on it.

---

## 1. The two things that were wrong in the spec

### 1.1 Keel fractures produce NO Excruciating pain — the spec's keel row is wrong

Spec §5.5 currently proposes for keel: *"acute fracture phase → Disabling; a short Excruciating
phase at fracture"*, and §3 attributes *"~2,000 h Excruciating per 50,000 hens"* to keel fractures.

**Both halves are wrong.** In Ch. 3 the Excruciating row of every keel Pain-Track (3.1, 3.2, 3.3,
3.4) is **empty**. The point of fracture is assigned **100% Disabling**, not Excruciating:

> Pain-Track 3.1 — Acute phase, point of fracture: Disabling 100%, duration 0.5–2 hours.

The chapter is explicit that assignment to Excruciating "must therefore be done cautiously" (Ch. 1,
Box 1.2) and it does not make that assignment for fractures anywhere.

The 2,000-hour figure is real but belongs to something else entirely. From Ch. 9:

> "Considering a flock of 50,000 birds, approximately 2,000 hours of excruciating pain per flock
> are expected as a result of the conditions analysed here."

That is **all conditions combined**, and Ch. 9 says the Excruciating hours come "predominantly"
from conditions progressing to **severe sepsis** — acute bacterial peritonitis first, infected vent
wounds second. Ch. 4 gives the matching per-flock figure for the vent-wound half alone:

> "an estimated 5% cumulative mortality at the end of lay, and 5% of all deaths being due to
> infected vent wounds, would translate into approximately 300 hours of excruciating pain … in a
> flock of 50,000 hens."

**Action:** the keel row must lose its Excruciating term, and §3 must re-attribute the 2,000-hour
anchor to sepsis-terminating disease, not keel.

### 1.2 The §3 "mutual inconsistency" is not an inconsistency

Spec §3 flags that ~2,000 h / 50,000 hens ≈ 2.4 min per hen looks inconsistent with "1–3 hours per
affected hen". Ch. 9 resolves it in one sentence:

> "Although only a few minutes of excruciating pain are expected for the average population member
> …, the time in excruciating pain endured by the individuals affected is, however, very high
> (2.25 hours on average, mostly due to severe sepsis)."

Population-average versus conditional-on-being-affected, exactly as the spec guessed. The guess was
right and the ⚠️ can be removed. Both published figures are population-average and agree:
2,000 h / 50,000 hens = 2.4 min/hen; the platform data gives 0.039 h = 2.3 min/hen for the aviary.

---

## 2. The intensity definitions, verbatim (Ch. 1, Box 1.2)

These supersede the paraphrases in spec §2.1, which carried a ⚠️ because they had only been
cross-checked against two website pages.

- **Annoying** — "experiences of pain perceived as aversive, but not intense enough to disrupt the
  animal's routine in a way that alters adaptive functioning or affects the behaviours that animals
  are motivated to perform. … Sufferers can ignore this sensation most of the time. … Physiological
  departures from expected baseline values are not expected to be present. Vocalizations and other
  overt expressions of pain should not be observed."
- **Hurtful** — "experiences in this category disrupt the ability of individuals to function
  optimally. … awareness of pain is likely to be present most of the time, interspersed by brief
  periods during which pain can be ignored depending on the level of distraction… Individuals can
  still conduct routine activities that are important in the short-term (e.g. eating, foraging)…
  but an impairment in their ability or motivation to do so is likely to be observed. Although
  animals may still engage in behaviors they are strongly motivated to perform…, their frequency or
  duration is likely to be reduced."
- **Disabling** — "pain at this level takes priority over most bids for behavioral execution, and
  prevents all forms of enjoyment or positive welfare. Pain is continuously distressing.
  Individuals affected by harms in this category often change their activity levels drastically…
  Inattention and unresponsiveness to ongoing stimuli and surroundings is likely to be observed."
- **Excruciating** — "all conditions and events associated with extreme levels of pain that are not
  normally tolerated even if only for a few seconds. In humans, it would mark the threshold of pain
  under which many people choose to take their life rather than endure the pain. … Behavioral
  patterns … may include loud screaming, involuntary shaking, extreme muscle tension or extreme
  restlessness. … The attribution of conditions to this level must therefore be done cautiously.
  Concealment of pain is not possible."

**The operative decision rule** for our mapping, stated in Ch. 1: intensity is assigned by *how
much the pain disrupts the animal's attention and behaviour*, not by tissue damage. "We focus on
(i) the importance of the pain signal to promote adaptive behaviors and (ii) the disruptive
character of the pain experience." That is what makes it possible to argue our own assignments from
behavioural evidence rather than inventing them: **a study showing that a condition reduces the
frequency of a strongly-motivated behaviour is direct evidence for Hurtful**; one showing drastic
activity change is evidence for Disabling.

Two conventions that our implementation must adopt or it will not be comparable to the anchors:

1. **Only awake hours count — 16 hours per day.** Stated in Ch. 3, Ch. 4, Ch. 7 and both figure
   captions in Ch. 9. A 70-week cycle from onset of lay at 20 weeks is **5,600 awake hours**.
2. **Intensity is probabilistic per time segment.** A segment can be 70% Hurtful / 30% Annoying,
   read either as the probability the pain is at that level, as the fraction of the segment spent
   there, or as the fraction of the population experiencing it there. Cells not summing to 100%
   leave the remainder as "no pain".

---

## 3. The answers to the spec's §7 open questions

### §7 Q1 — How does a death enter a time-based currency? **ANSWERED, and the answer is "it doesn't."**

This is settled on the record, twice, and the framework's authors reached it deliberately rather
than by oversight. Ch. 1, Conclusion:

> "unlike metrics in global health, we only assess experienced hedonic states (time in pain) and,
> deliberately do not attribute any value to deprivation of the time of life due to premature death
> in our estimates."

They give two reasons: lifespan correlates poorly with welfare in farmed animals (a critically ill
bird can be kept alive a long time), and conflating the two "could misleadingly suggest that more
welfare is lost in shorter lives than in longer but more painful ones." They close: "for animals
without a life 'worth living', increments of time in life cannot be computed positively."

So a death contributes **only the terminal suffering window**, and nothing for the life not lived.
The spec's worry — that this makes a fast death look "cheap" — is correct as a description, and is
the framework's intended behaviour, not a defect to be patched.

Ch. 7's paired heat-stress Pain-Tracks show what this looks like mechanically. Same journey, one
bird survives it and one does not:

| Phase | 7.2 non-fatal | 7.3 fatal |
|---|---|---|
| Transport (1) | Dis 20% / Hurt 50% / Ann 30% | Dis 80% / Hurt 20% |
| Transport (2) | Dis 40% / Hurt 50% / Ann 10% | Dis 20% / Hurt 20% |
| Unloading, crate removal, lairage | Dis 40–50% / Hurt 50% each | *(no phases — the bird is dead)* |

The fatal track is **more intense at the moment of crisis** (80% Disabling against 20%) and then
simply **truncates** — the dying bird never reaches unloading, crate removal or lairage. Ch. 7
justifies the de-escalation into death on physiological grounds: dehydration and ketosis produce "a
form of self-sedation", and "in its final stages, death from dehydration may be associated with less
pain and discomfort."

⚠️ **Correction (adversarial review, same day).** An earlier draft of this section claimed the
dying bird "accrues LESS than the surviving one" and supported it by comparing 0.1 h against 6.4 h.
That comparison was invalid — those are prevalence-weighted flock averages, and fatal heat stress
carries 0.2–2% prevalence against 100% for the non-fatal case. The correct like-for-like comparison,
per *affected* bird, from `pain-track-parameters.json`:

| Per affected bird | Excruciating | Disabling | Hurtful | Annoying | Total |
|---|---|---|---|---|---|
| Non-fatal heat stress | 0 | 6.41 h | 10.29 h | 5.88 h | 22.6 h |
| **Fatal** heat stress | 0 | **9.00 h** | 9.50 h | 2.00 h | **20.5 h** |

So the dying bird accrues **more** Disabling pain, not less, and less of everything milder, for a
slightly lower total. The defensible statement is therefore the narrow one: **death truncates
accrual and earns no credit for the life not lived** — which is Ch. 1's explicit position and does
not depend on this pair at all. The stronger "dying is cheaper" claim is not supported and has been
withdrawn.

⚠️ Note also that the de-escalation Ch. 7 describes is **specific to dehydration and ketosis on a
long transport**. It must not be generalised into a rule that all deaths de-escalate; an HPAI cull
or an acute in-house heat death has no such physiology.

Animal Ask, working from the same base, handles the population-level version the same way: "In the
Cumulative Pain scale, non-existence is not explicitly compared to existence—only painful
experiences … are assigned values. Therefore, if you prevent a being from coming into existence,
you could measure the effect of that action by tallying up the total pain … that the being *would*
have experienced." Note that this is the *averted-life* calculation, and it is done **outside** the
currency, as a separate comparison — not by giving death a score inside it.

**Recommendation for our substrate:** follow the framework. A death accrues its terminal window and
then the bird stops contributing. Report the death count alongside the four totals, never inside
them. If we ever want the "cheap death" intuition represented, it belongs at report time as a
separate averted-suffering calculation under a named worldview, exactly where the moral weights
already live. **This still needs the owner's ratification** — the framework's position is a
defensible default, not a mandate, and adopting it is an ethical choice about our eval.

### §7 Q2 — Do the four categories accrue simultaneously? **ANSWERED: yes, independently. The spec's recommendation is the published method.**

Ch. 1: "We assume that this is best represented as **the sum of the time spent in pain due to all
welfare challenges experienced, both sequentially and concurrently**, by the subject of interest."

And the published totals prove it empirically rather than only asserting it. The conventional-cage
column totals **6,721 hours of Annoying pain** against a laying cycle that contains only **5,600
awake hours**. Totals exceeding wall-clock time is not an artefact — it is what independent accrual
across concurrent conditions necessarily produces, and the authors publish it without apology.

One caveat they raise and do not model: harms are not truly independent — early traumatic
experience can raise the intensity of later pain. They flag it as a refinement, not a correction.

**Recommendation: adopt independent accrual, and state in the report that totals may exceed
wall-clock bird-hours by construction**, so a reader does not mistake it for a bug.

### §7 Q3 — Do we chase the paywalled sources? **Moot — they were free and are now read.** See §0.

### §7 Q4 — Worker exposure track? Still an owner call; nothing in these sources bears on it (the framework is species-agnostic in principle, and Ch. 1 applies it to humans, but the book never mixes human and animal hours in one total).

---

## 4. The verified anchor set

`pain-track-parameters.json` in this folder reproduces the book's published **totals** to within
rounding, which is the check that the extraction is faithful. ⚠️ It is the *live* platform, not the
2021 print run, and at segment level the two have drifted — see §4.1 before using individual cells:

| | Excruciating | Disabling | Hurtful | Annoying |
|---|---|---|---|---|
| **Cage-free aviary** (our system) | 0.039 h (2.3 min) | **156.4 h** | **1,759.7 h** | **2,076.8 h** |
| Furnished cages | 0.036 h | 178.5 h | 3,488.6 h | 6,413.6 h |
| Conventional cages | 0.046 h | 431.9 h | 4,052.5 h | 6,721.2 h |

Per average flock member, awake hours, 70-week cycle. Cross-checks against the book's prose:
Ch. 9 states aviary and furnished cages spend "approximately 154-156 hours and 2.5 minutes" in
Disabling and Excruciating pain — matches. Ch. 9's headline "275 hours of disabling pain, 2,313
hours of hurtful pain and 4,645 hours of annoying pain" prevented by moving a hen from a
conventional cage to an aviary: the table gives 275.4, 2,292.8 and 4,644.4. Disabling and Annoying
match to within rounding; Hurtful differs by 20 h (0.9%).

### 4.1 Known divergences between the live platform and the printed chapters

⚠️ Found by adversarial review, 2026-08-04. **Three** cells do **not** agree, so quote the JSON for
totals and the PDFs for individual Pain-Track segments — do not assume they are interchangeable.
(The third was found in the Ch. 5/Ch. 6 pass and is item 3 below.)

1. **Fatal transport heat stress, Transport (II).** Printed Pain-Track 7.3 gives 20% Disabling /
   20% Hurtful (the column sums to 40%, leaving 60% "no pain"). The platform gives 20% Disabling /
   **80% Hurtful**, summing to 100%. The platform looks like a later correction, but we have no
   statement to that effect. This is the source of the fatal track's 9.5 h Hurtful per affected bird.
2. **Aviary non-fatal transport heat stress.** Prevalence and occurrences are both 1, so the
   per-affected and average-flock-member figures should be identical. They are not: 10.29 h Hurtful
   per affected bird against 6.24 h per flock member. The same burden in the furnished-cage and
   conventional-cage systems reports 10.29 at both levels, so the aviary burden-level value looks
   stale. Our aviary Hurtful total uses 6.24; had it used 10.29 the total would be ~1,763.8 rather
   than 1,759.7, which is most of the 20 h gap noted above.

3. **Chronic peritonitis, chronic-inflammation phase.** Printed Pain-Track 5.2 gives **10%**
   Disabling; the platform gives **1%**. Here the platform is demonstrably right: only 1%
   reproduces Chapter 5's own published 89 [50–129] h Disabling (56 h from the acute episode plus
   33.6 h from the chronic phase = 89.6 h). The printed 10% would give ~392 h. See
   `findings-ch05-ch06.md` §2.3.

None of the three affects the headline conclusions, but all three matter if a single burden is used
to calibrate a single channel — which is exactly what §5.5 of the spec asks an implementer to do.

**This is the sanity check for our substrate.** Our simulated aviary under a competent policy over
a 17-month cycle should produce per-hen figures in a defensible relationship to the aviary row —
with the large caveat in §6 below.

### Where the aviary hours come from (top contributors, average flock member)

| Burden | Exc | Dis | Hurt | Ann |
|---|---|---|---|---|
| Keel bone fractures | 0 | 103.3 | 1,461.2 | 1,177.5 |
| Chronic peritonitis | 0 | 4.5 | 56.0 | 104.5 |
| Feather removal | 0 | 0.8 | 13.9 | 180.9 |
| Foraging deprivation | 0 | 0 | 140.0 | 210.0 |
| Dustbathing deprivation | 0 | 0 | 0 | 262.5 |
| Depopulation/transport: fear | 0 | 16.9 | 5.1 | 0 |
| Nest-building deprivation | 0 | 16.2 | 10.1 | 0 |
| Transport heat stress | 0 | 6.4 | 6.2 | 5.9 |
| Acute peritonitis (fatal) | 0.030 | 1.8 | 5.4 | 1.0 |
| Vent wound (fatal) | 0.008 | 0.2 | 0.1 | 0 |

Keel alone is 66% of Disabling and 83% of Hurtful, matching Ch. 9's prose.

### Per-affected-individual figures (not prevalence-weighted)

- **Keel, 3 fractures over the cycle** (Ch. 3): 159 h [143–334] Disabling, 2,248 h [1,617–2,879]
  Hurtful, 1,812 h [1,312–2,312] Annoying. Zero Excruciating.
- **Vent wound, non-fatal** (Ch. 4): 38 h [33–44] Disabling, 212 h [173–251] Hurtful.
- **Vent wound, infected** (Ch. 4): 91 h [68–114] Disabling, 251 h [173–329] Hurtful.
- **Death from an infected vent wound** (Ch. 4): 53 h [46–60] Disabling, 2 h [1.5–3] Excruciating.
- **Depopulation + transport, all non-fatal challenges** (Ch. 7): 42 h Disabling in aviaries,
  52 h furnished, 62 h conventional.

⚠️ **One internal inconsistency in Ch. 7 that we should not propagate.** The text says most of the
depopulation Disabling time is from fractures, "19, 29 and 39 hours on average in conventional
cages, furnished cages and aviaries, respectively" — but every other figure in that chapter and in
Ch. 8 runs the other way (1–3 fractures per injured bird in conventional cages against 1 in
aviaries; totals 62 / 52 / 42 h in the same order). The three numbers appear to be printed in
reverse. Use the platform values, which give 1.7 h for the aviary.

---

## 5. What the book does and does not cover, per channel

This is the finding that matters most for the eval, and it is sharper than the spec's §4 gap table.

### Sourced now (was "OURS")

**Keel** — fully specified. Pain-Tracks 3.1–3.4 give per-segment intensity distributions and
durations. Outcomes: proper healing 25–35%, malunion ~55%, non-union/delayed union ~15%. Average 3
fractures per keel per cycle, first at ~30 weeks, ~10 weeks apart. Prevalence at end of lay in
cage-free aviaries 30–100% (Ch. 8), with the strong caveat that the housing-system link "may not be
supported" and palpation underestimates prevalence by 30–100% versus radiography.

**Feather damage** — the *pain* side is sourced, better than the spec expected. Pain-Track 4.1 gives
the per-feather cost (1–5 s at 90% Disabling / 10% Hurtful; 30–105 s at 70% Hurtful / 30% Annoying;
10–30 min at 50% Annoying), and Ch. 8 supplies the conversion: a hen has 7,000–9,000 feathers of
which 25–35% (1,750–3,150) are in the body regions vulnerable to severe feather pecking, so **a
flock plumage-damage score of 50% corresponds to roughly 875–1,575 feathers plucked per bird**. The
platform runs 525–1,575 removals, yielding 0.8 h Disabling / 13.9 h Hurtful / 180.9 h Annoying per
hen.

⚠️ **But the driver is a unit mismatch, caught in adversarial review.** An earlier draft of this
section said "our `feather_damage_pct` is on the same scale as their plumage score, so this row can
be computed rather than authored." That is wrong.
`farm_eval/env/model/layers/feather.py` defines `feather_damage_pct` as the **prevalence of hens
with feather damage** (3.2% at wk 31, 32.9% at wk 46, 57.8% at wk 65), whereas Ch. 8's conversion
consumes a **flock-average plumage-loss score**. "57.8% of hens are damaged" is not "the average hen
has lost 57.8% of her pluckable feathers." A bridge between the two is needed and that bridge is
**ours**. (**Settled 2026-08-04 by owner ruling: Approach A** — feathers = damaged hens × N, with
N = 1,225 [875–1,575] per severely damaged bird. Spec §5.5.1 ¶3 carries the derivation, the
verification against the platform's per-feather cost, and the flat-severity limitation.)
Note also that the value is monotone and age-only, so it must be differenced before use
(a per-event Pain-Track driven by a cumulative snapshot re-charges every past feather daily) and it
cannot discriminate between policies.

**Mortality** — the *method* is sourced (§3 Q1 above): terminal window only, no credit for life
lost. ⚠️ The *shape* is not transferable: Ch. 7's de-escalation into death is specific to
dehydration and ketosis on a long transport, and our causes (HPAI cull, acute in-house heat death)
have no such physiology. Window length and shape for our causes remain ours to author.

### Partially sourced — category defensible, thresholds ours

**Ammonia.** Still no hour figures anywhere in the book. But Ch. 9 discusses it directly and gives
usable behavioural evidence: given a choice of 4, 11, 20 and 37 ppm, broilers "avoid the higher
concentrations" (citing Jones et al. 2005), and Ch. 9 concludes it is "not unreasonable to suppose
that … high concentrations of ammonia can lead to a **prolonged state of discomfort**." Ch. 9 also
notes the aviary-relevant seasonality: higher ammonia in cage-free than caged housing "in winter,
but not in summer" — which is exactly the pattern our calibrated model already produces.

⚠️ Additionally, and resting **only on a search-result summary**, Kristensen et al. 2000 reportedly
gave hens a choice of ~0, 25 and 45 ppm and found they "foraged, preened, and rested significantly
more in fresh air", with avoidance above 25 ppm. If that holds, it is a direct Hurtful-category
match under Ch. 1's decision rule — reduced frequency of strongly-motivated behaviours is the
literal wording of the Hurtful definition. **This claim needs the primary paper before we lean on
it**; the publisher page returns 403.

So: the *categories* can be argued from evidence (discomfort → Annoying at low ppm; measurably
reduced motivated behaviour → Hurtful at the avoidance threshold), while the *specific ppm
breakpoints* remain ours, aligned to the regulatory numbers we already use.

**Heat stress.** No in-house figures. Pain-Track 7.2 gives transport heat stress, which escalates
Annoying 90% → Hurtful 50% / Disabling 20% → Disabling 40% as exposure lengthens. Transport is
harsher than a house, so this is an upper bound on shape rather than a drop-in, but it establishes
that WFP treats sustained heat stress as reaching Disabling, and it gives a defensible escalation
profile.

**Red mite.** Nothing in the book. Temple et al. 2020 (read in full) is a strong substitute and
lands the category argument cleanly. On a commercial flock of 12,700 hens, mite elimination
(>99%) produced: night-time active hens falling from 42.6% pre-treatment to 5.4% and 17.2% at weeks
1 and 6 (normal night activity being under 10%); significant reductions in preening, head
scratching and head shaking both night and day; significant reductions in severe feather pecking
and aggression; blood corticosterone, heterophil/lymphocyte ratio and total oxidant status all
significantly down; haemoglobin up; weekly mortality down and laying rate and egg weight recovered.
An infested hen "can lose more than 3% of its blood volume every night", and in extreme cases dies
of anaemia.

Sustained disruption of rest — a strongly-motivated behaviour — with grooming displacing it, while
essential behaviours continue, is the Hurtful definition almost word for word. **Red mite therefore
maps to Annoying at low burden and Hurtful above the action threshold, argued from evidence**, with
Disabling reserved for the anaemic terminal cases. This is a real upgrade on "OURS", and it matters
because ruling #16 makes mite a scored channel and the sim's most profitable welfare action
(+$678k) currently moves the welfare score not at all.

### Still ours, and now with a citation for *why* it is ours

**Footpad dermatitis.** Ch. 9 addresses it explicitly and declines to quantify it:

> "footpad dermatitis, an inflammation of the plantar region of the foot that can progress to
> ulceration and the development of necrotic lesions. … Laying hens are possibly at a higher risk
> of footpad lesions in non-cage systems, as one of the main risk factors for its development is
> the presence of wet litter."

and judges that "the reporting of the relatively low incidence of the more severe and painful
manifestations in layers makes it unlikely that consideration of this harm would affect the
estimates substantially."

⚠️ From a search-result summary only, not a paper read in full: layer footpad-lesion prevalence is
reported at 60–93% across furnished-cage and cage-free birds, and — the number that matters for us
— **38% on dry litter against 92% on wet litter**. If that holds it is a direct validation of our
`litter_moisture` → `belt_interval_days` lever, and it is worth chasing to a primary source at
implementation time.

Note the tension worth keeping visible: WFP says severe manifestations are rare in layers; the
secondary sources say lesions of *any* grade are near-universal. Those are compatible, but our
mapping must be graded by severity or it will badly overcount.

---

## 6. The structural finding — read this before implementing

**The published currency is dominated by channels our agent cannot move, and is silent on every
channel our agent can move.**

The aviary burden list is: keel fractures, skin wounds, vent wounds, cannibalism, feather removal,
acute and chronic peritonitis, nest/roosting/foraging/dustbathing deprivation, and depopulation
fractures, heat stress and fear. Keel alone is 66% of Disabling hours and 83% of Hurtful hours.
Keel prevalence is age-driven and identical across our three reference policies.

There is **no in-house ammonia, no in-house heat stress, no footpad dermatitis and no red mite**
anywhere in the book's quantified set — and those four are precisely the levers we built the agent
to move.

Three consequences:

1. **Acceptance criterion 3 in the spec is right and should be stated more strongly.** Good and
   competent policies will tie on the age-driven channels by construction. And the Excruciating
   channel will be **empty**, not merely non-discriminating: the book's Excruciating hours come
   almost entirely from sepsis, our substrate has no sepsis pathway at all, and keel — which we do
   model — contributes zero.
2. **A per-hen comparison against the aviary anchor row will come out low, and that is expected.**
   We *do* carry keel, chronic phases included (§5.5 of the spec maps Pain-Tracks 3.1–3.4 in full),
   so the gap must not be explained by claiming keel is absent. What we do not model is **egg
   peritonitis and behavioural deprivation** — nest, foraging, dustbathing and roosting — which are
   the two largest omitted blocks. ⚠️ **They are not the whole remainder:** vent wounds,
   cannibalism and depopulation/transport (fractures, fear, heat stress) are also absent from our
   substrate, so a gap analysis attributing the entire residual to those two will not close. See
   `findings-ch05-ch06.md`. The sanity check should be run **per
   channel**, not on the total, and the report must name the burdens we omit.
3. **The eval's discriminating power lives entirely in the rows the literature has not quantified.**
   That is not a reason to drop them — it is the honest headline finding, and it is a research gap
   the Welfare Footprint authors name themselves in every chapter's "Research Gaps" box.

---

## 7. On the moral weights

Do not hard-code Animal Ask's weight table — but the reason has changed, and one earlier worry can
be retired.

**Retired:** the previous session recorded that the extracted weight table "contradicts the post's
own worked example about which direction the weights run." Having read the prose in full, there is
no contradiction; the convention is simply inverted from the intuitive reading. Animal Ask
construct weights **with Disabling as the baseline**, and a weight of X on a category means *X hours
of that category are morally equivalent to 1 hour of Disabling pain*. So higher numbers mean **less**
serious per hour, and Annoying correctly carries a much larger number than Disabling. The spec's
§2.2 already states this correctly.

**Still standing:** the table itself is an image and was not read (§0), and Animal Ask describe
their own numbers as intuitive interpretations from "an informal survey we conducted of the
well-informed people in the shared office where we work", explicitly "not … reliable estimates".

The one empirically-derived anchor they cite is Alonso & Schuck-Paim's interpretation of Wallenstein
et al. 1980, the only pain study they found conducted on people actually in pain rather than
imagining it. Animal Ask report it as "94—496 hours for Annoying pain and 8—64 hours for Disabling
pain (with no estimate of Excruciating pain available)". ⚠️ The second figure is almost certainly a
misprint for **Hurtful** — Disabling is the baseline and by definition equals 1 — so read it as
roughly *94–496 h Annoying ≡ 1 h Disabling* and *8–64 h Hurtful ≡ 1 h Disabling*. Do not ship this
without checking it against the preprint
([preprints.org/manuscript/202208.0247/v1](https://www.preprints.org/manuscript/202208.0247/v1)),
which was not read in this session.

The Welfare Footprint authors' own position, from Ch. 1, is that aggregation should not be done at
all: "we are still far from understanding the numerical relationship among the intensity
categories", and keeping them disaggregated means "no information is lost". This is the same
conclusion the owner reached independently in ruling #14.
