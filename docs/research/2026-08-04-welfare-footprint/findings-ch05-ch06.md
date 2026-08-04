# Chapters 5 and 6 — the two burdens we do not model

**Read:** 2026-08-04, in full, from the publisher PDFs now archived in `sources/`.
**Question they were read to answer:** should egg peritonitis and behavioural deprivation enter our
substrate at all? The owner asked for this reading as the opener of the session that follows
`findings.md`; the decision is the owner's and is **not** taken here.

Companion: `findings.md` (the six-chapter pass), the design spec
`docs/specs/2026-08-04-welfare-currency-design.md`, the work ledger
`docs/plans/2026-08-04-welfare-currency-and-finance-ledger.md`.

---

## 0. Coverage statement

| Chapter | Pages of text | Status |
|---|---|---|
| Ch. 5 — Egg Peritonitis Syndrome: A Painful and Prevalent Disease in Commercial Layers | 20 | **text read in full**, including both Pain-Tracks, through the reference list. ⚠️ Figures not inspected as images |
| Ch. 6 — The Burden of Psychological Pain in Laying Hens: Behavioral Deprivation | 33 | **text read in full**, including all twelve Pain-Tracks, through the reference list. ⚠️ Figures not inspected as images |

⚠️ **"Read in full" here means the full text layer, not the figures.** Wherever this document says a
chapter was read in full, that claim excludes its images — see the paragraph below.

Both were downloaded from the publisher's own chapter links on
<https://welfarefootprint.org/book-laying-hens/> and are archived beside the other six in
`sources/`.

⚠️ **The figures in both chapters are images and were not read as images.** That includes the two
results charts — **Figure 5.3** (time in each pain category for chronic and acute peritonitis) and
**Figure 6.4** (time in each category per deprived bird, per behaviour, per housing system).
Every numeric result quoted below therefore comes from the chapters' **prose**, which states the
headline totals, and from `pain-track-parameters.json`, which carries the same burdens as data.
The Pain-Track tables themselves extracted as text and were read directly.

---

## 1. Why these two chapters matter more than "two burdens we omit"

`findings.md` §6 recorded a structural finding: *the published currency is dominated by channels our
agent cannot move, and is silent on every channel our agent can move.* Chapter 6 **partly reverses
that**, and this is the most consequential thing in either chapter.

Chapter 6 does not treat behavioural deprivation as a property of the housing system. It gives each
aviary Pain-Track an **affected fraction**, and then names what determines that fraction. Two of
those named drivers correspond to fields our substrate already carries — ⚠️ though only one of the
two is actually live, as the limits below set out:

> "in aviaries with only plastic or wire floors, or where litter is non-friable, shallow or
> **becomes too wet**, proper dustbathing is not possible" (Ch. 6, dustbathing)

> "In addition to **high stocking densities** and the **lack of proper litter material**, movement
> may be restricted by the use of divisions between units or limited points of entry between the
> litter and the aviary tiers" (Ch. 6, foraging)

Wet litter is `litter_moisture`, which relaxes to a manure-belt-frequency equilibrium and is driven
by `belt_interval_days` — the same agent lever that already drives footpad. That connection is
**explicit for dustbathing only.**

⚠️ **Two limits on this, both found in review and both real.**

1. **The foraging passage does not say "wet".** It says *"lack of proper litter material"*. Wet
   litter is arguably improper litter, but the chapter does not make that step and neither should
   we: treating `litter_moisture` as a foraging driver is **ours**, on a weaker footing than the
   dustbathing link, and it must be labelled that way if it is used at all.
2. **Stocking density is not an agent lever today.** `stocking_density` exists on `HouseWelfare`
   as a stored field and nothing reads it: no model layer consumes it, and no agent tool sets it
   (verified by search, 2026-08-04). It is the Step-2 lever under rulings #1 and #6, and the
   density wave is **currently blocked**. So of the two variables Chapter 6 names, exactly one —
   litter — is live in our substrate right now.

With those limits stated, the finding still stands and is still the most useful thing in either
chapter: Chapter 6 contains the **first published Pain-Tracks in this book whose affected fraction
is a function of something our agent can control at all.** Everything sourced so far — keel,
feather, depopulation — is age-driven or scripted and cannot discriminate between models.

Chapter 5 matters for a different and narrower reason, stated in its own words:

> "sepsis is the only welfare harm (of those explored in the book) associated with such an extreme
> level of pain for such a long time"

⚠️ **But do not read that as "the only Excruciating harm in the book" — it is not, and an earlier
draft of this document said so wrongly.** The chapter's claim is narrower: sepsis is the only harm
at that intensity *for such a long time*. In the aviary column of `pain-track-parameters.json`,
four burdens carry Excruciating hours:

| Aviary burden | Exc h per affected bird | Exc h per average flock member | Share of aviary Excruciating |
|---|---|---|---|
| Acute peritonitis (fatal) | 2.25 | 0.0304 | 78% |
| Vent wound (fatal) | 2.25 | 0.0082 | 21% |
| Depopulation & transport: fractures | 0.0022 | 0.0002 | <1% |
| Fatal cannibalistic attack | 0.075 | 0.00006 | <1% |
| **Total** | | **0.0389** | (matches the published 0.039) |

The first two are the same 2.25 h severe-sepsis phase reached by two different routes, which is why
they must never be added as if they were independent anchors. (The bottom two rows are computed
from prevalence × per-affected hours rather than read off the JSON's rounded display, which shows
fatal cannibalism as 0.0001; either way they are rounding noise against the 0.0389 total.)

Our spec's acceptance criterion 3 says our **Excruciating channel will be empty outright**. What
remains true is that **our substrate models none of these four** — no peritonitis, no vent wounds,
no cannibalism, no depopulation physics.

⚠️ **Nor is peritonitis the only one reachable by the method §4.2 proposes.** That method assigns a
literature share of baseline deaths to a cause and runs its Pain-Track; **fatal vent wounds and
fatal cannibalism are reachable exactly the same way**, and Chapter 8 supplies aviary prevalences
for both. The defensible claim is narrower and quantitative: peritonitis is the **largest** such
route, carrying 78% of published aviary Excruciating hours against the vent wound's 21%, and it is
the one whose underlying condition is the leading cause of layer mortality. If the goal is simply a
non-empty Excruciating column, vent wounds would also do it — at about a quarter of the magnitude
and, being the same 2.25 h sepsis phase, with no additional physiology to model.

---

## 2. Chapter 5 — egg peritonitis syndrome

### 2.1 What it is and how prevalent

Salpingo-peritonitis is reported as the **most common production disease in modern laying breeds**
and, per Chapter 8, **the leading cause of mortality in laying hens.** Egg material reaches the
abdominal cavity by reverse peristalsis or by retention/rupture in the oviduct; yolk alone causes
only mild inflammation, but it is an excellent bacterial growth medium, so secondary *E. coli*
infection is common. The chapter uses "egg peritonitis syndrome" (EGPS) as an umbrella term.

Three outcomes (Figure 5.2, an image — the branching is described in the prose):
**aseptic peritonitis** (yolk reabsorbed; explicitly "unlikely to be associated with pain", not
tracked), **acute bacterial peritonitis** progressing to sepsis and death, and **chronic
peritonitis** persisting to depopulation.

### 2.2 Pain-Track 5.1 — acute bacterial peritonitis, fatal

| | i. Infiltration of egg material | ii. Inflammation | iii. Sepsis (initial) | iv. Severe sepsis (organ failure) | v. Septic shock |
|---|---|---|---|---|---|
| Excruciating | | | | **30%** | |
| Disabling | | 20% | 90% | 40% | 10% |
| Hurtful | | 70% | 10% | 30% | 80% |
| Annoying | 25% | 10% | | | 10% |
| **Duration** | 2–7 days | 2–8 weeks | 12–24 h | 5–10 h | 2–4 h |

The Excruciating cell is argued, not asserted: in severe sepsis human patients describe the pain as
extreme, and the authors cap it at 30% of a 5–10 h segment — "affected hens would spend from 1.5 to
3 hours at a level of pain equivalent to that of severe burning events - we consider that longer
durations would not be possible without the neurological system shutting down." The de-escalation at
septic shock is likewise argued from evidence (small-fibre deterioration, critical illness
polyneuropathy), not assumed.

**Burden per affected bird:** 131 [64–199] h Disabling and **over 2 [1.5–3] h Excruciating.** This
is the same 2 h figure `findings.md` already carries for death from an infected vent wound, and the
same mechanism — sepsis.

### 2.3 Pain-Track 5.2 — chronic peritonitis

| | i. Infiltration of egg material | ii. Acute episode | iii. Chronic inflammation |
|---|---|---|---|
| Disabling | | 10% | 10% *(see below — the platform says 1%)* |
| Hurtful | | 80% | 20% |
| Annoying | 25% | 10% | 60% |
| **Duration** | 2–7 days | 2–8 weeks | 12–48 weeks |

⚠️ **A third print-versus-platform divergence, and this one is decisive.** The printed table assigns
**10%** Disabling to the chronic-inflammation phase; `pain-track-parameters.json` assigns **1%**.
Only 1% reproduces the chapter's own published burden: phase ii at 10% of a mean 560 awake hours is
56 h, plus phase iii at 1% of a mean 3,360 h is 33.6 h, totalling **89.6 h** — the quoted 89
[50–129]. At the printed 10% the total would be ~392 h, more than four times the figure the chapter
prints two pages later. **Use 1%.** This adds to the two divergences already recorded in
`findings.md` §4.1, which must now read three.

Columns deliberately do not sum to 100% — the remainder is "no pain". The chronic phase runs to
depopulation; with onset at mid-lay (30–40 wk) and depopulation at 60–80 wk, an average affected
bird carries it for 12–48 weeks.

**Burden per affected bird:** 89 [50–129] h Disabling, 1,120 [636–1604] h Hurtful, 2,090
[880–3300] h Annoying — "nearly half of the laying cycle" in Annoying alone, and the chapter says
this is "almost on par with that due to the keel fractures endured over a hen's life."

### 2.4 What Chapter 5 does *not* give us

No prevalence and no case-fatality ratio. The chapter says so outright in its Research Gaps:
"little information is available on its prevalence, and case-fatality ratio." The aviary prevalence
used in the published totals comes from Chapter 8, not here.

---

## 3. Chapter 6 — behavioural deprivation

Estimates are given as **time in pain per day**, over an assumed 280–420 days (depopulation at
60–80 wk, lay from 20 wk), awake hours only. Each behaviour gets a per-system affected fraction.

### 3.1 The aviary Pain-Tracks and their affected fractions

| Behaviour | Aviary affected fraction | Pain-Track (aviary) | What the chapter says drives the fraction |
|---|---|---|---|
| **Nest building** (6.1) | **2–8%** | search 30–60 min at 50% Dis / 50% Hurt → pre-oviposition sitting 25–45 min at 80% Dis / 20% Hurt → oviposition 5–15 min at 50/50 | floor-laying rate: competition for boxes, or boxes not judged suitable |
| **Roosting at height** (6.4) | **5–25%** | search 30–60 min at 50% Hurt / 50% Ann → dark hours 6–8 h at 15% Ann | hens unable to reach the top-level perch; the rest use lower perches |
| **Foraging / exploration** (6.7) | **5–20%** | 4–12 h/day at 40% Hurt / 60% Ann | stocking density, lack of proper litter, movement restricted by divisions/entry points, and impaired health late in lay |
| **Dustbathing** (6.10) | **10–50%** | 2.5–7.5 h/day at 50% Ann | plastic or wire floors; litter non-friable, shallow, **or too wet** |
| **Movement restriction** (6.11/6.12) | **not present in aviaries** | — | the chapter writes no aviary track for it |

⚠️ **The affected fraction is not unambiguously a fraction of birds.** For foraging the chapter
says the 5–20% figure "can also be interpreted as the average proportion of **time** that hens are
unable to forage (when they were supposed to), despite a strong motivation to engage in this
behavior", and for dustbathing the same 50/50 intensity split is offered as either a share of birds
or "a temporal distribution of frustration levels". Both readings are sanctioned by the authors and
they give the same flock total under a linear map, but an implementer must pick one and say which,
because they differ the moment anything non-linear (a threshold, a cap) is applied to the fraction.

Converted to cycle totals per **affected** bird (platform values, 350-day mid-range cycle):

| Aviary behaviour | Disabling h | Hurtful h | Annoying h |
|---|---|---|---|
| Nest building | **324** | 201 | 0 |
| Foraging / exploration | 0 | **1,120** | 1,680 |
| Dustbathing | 0 | 0 | **875** |
| Roosting at height | 0 | 131 | 499 |

Note that the nest track is the **only** aviary behavioural track reaching Disabling, and it is
severe: the chapter reports **324 hours of disabling pain over one laying cycle** for a hen without
a suitable nest — *"more than any other source of disabling pain analysed in this book."* Nearly an
hour a day, from a behaviour whose window is under two hours a day.

### 3.2 How the intensities are argued

The same decision rule as everywhere else: disruption of behaviour, not tissue damage. Two examples
worth keeping because they show the standard of evidence:

- **Nest → Disabling.** Hens 20 minutes from oviposition worked about **three times harder** to push
  through a weighted door than hens 40+ minutes out, and "significantly higher than the rate to
  access food after 4 hours of food deprivation"; in earlier work the price paid matched that for
  food after **28 hours** of deprivation.
- **Foraging → Hurtful, not Disabling.** Explicitly bounded: "because hens deprived of the ability
  to forage do not refrain from activities such as eating, drinking, and reacting to external
  stimuli, the degree to which foraging deprivation affects them is unlikely to be of a disabling
  (or more intense) nature."
- **Dustbathing → half-weighted.** The evidence is openly conflicting, so the authors assign "a 50%
  probability that the welfare of hens is not negatively impacted in any way". That honesty is why
  the aviary dustbathing track is Annoying-only.

---

## 4. What it would take to add each, and what it would buy

Neither chapter maps onto an existing channel, so both are additions rather than remappings. Sorted
by value for the eval.

### 4.1 Behavioural deprivation — the highest-value addition, because it can discriminate

⚠️ **An earlier draft of this section said "no new physics" for all four tracks. That was wrong and
is corrected here.** Only the dustbathing track can be bridged from live state today. The four
split cleanly into two kinds, and the difference is the whole cost question:

**Bridgeable from state we already compute** (a mapping, in the same "category sourced, thresholds
ours" shape as the ammonia row):

- **Dustbathing** — the affected fraction can be mapped from `litter_moisture`, which the agent
  already drives through `belt_interval_days`. The book gives the 10–50% range and names wet litter
  as a cause, but gives **no function**, so the map itself is ours.
- **Foraging** — the book names stocking density, improper litter, physical access restrictions,
  temporal crowding and poor health. Of those, **stocking density is inert in our substrate today**
  and improper-litter-means-wet-litter is our inference, not the chapter's. So this one is
  bridgeable only on an assumption we have to declare, and it becomes genuinely policy-sensitive
  only once the blocked density wave lands.

**Not bridgeable — there is no state to bridge from:**

- **Roosting** (5–25%) — we carry no perch-access state at all. It would be a constant unless perch
  design becomes a Step-2 lever.
- **Nest** (2–8%) — we carry no floor-laying or nest-suitability state at all. It would likewise be
  a constant. But it is the book's single largest source of Disabling pain, so leaving it out
  understates the aviary total badly.

**So the honest cost is:** one sourced-ish bridge (dustbathing), one bridge resting on a declared
assumption plus a blocked lever (foraging), and two constants (roosting, nest). Authoring a
prevalence function is itself authored model dynamics and should be reviewed as such — it is
cheaper than new physics, but it is not free, and it is not "just accounting".

**What it buys:** the first sourced, published Pain-Tracks in the currency whose totals differ
between a good and a negligent policy. That directly addresses the §4 structural finding and
ruling #20 ("agents action MUST make changes there").

**What it costs:** the authored prevalence functions above, plus the honesty burden of labelling
them ours. There is also a real amplification risk to watch — `litter_moisture` would then drive
**footpad** (existing) *and* **dustbathing deprivation**, and, if the foraging inference is taken,
**foraging deprivation** as well. These are genuinely different harms so it is not double counting,
but one agent action would move up to three lines in the totals. That must be stated, or the
belt-interval lever will look stronger than the evidence supports. It is also the main argument for
**not** taking the foraging inference: two lines from one variable is defensible, three on the back
of a step the chapter does not make is not.

### 4.2 Egg peritonitis — lower value, but the only route to a non-empty Excruciating channel

⚠️ **The two halves of this chapter are not equally cheap, and an earlier draft of this section
blurred them.**

- **Pain-Track 5.1, the fatal acute cohort — genuinely no new physics.** EGPS is the leading cause
  of layer mortality, so a literature share of our baseline (non-HPAI, non-heat) deaths is
  peritonitis by construction. Those birds run 5.1 off mortality we already compute.
- **Pain-Track 5.2, the chronic non-fatal cohort — not derivable from mortality.** These birds do
  not die, so nothing in our substrate identifies them. Scoring 5.2 needs an **incidence** rate, an
  onset time and a duration, none of which mortality supplies and none of which Chapter 5 supplies
  either: its Research Gaps say outright that "little information is available on its prevalence,
  and case-fatality ratio." The platform's own aviary prevalence (2–8% chronic, 0.3–2.4% fatal)
  comes from Chapter 8, not Chapter 5. Adding 5.2 therefore means authoring a disease incidence
  term — small, but it is model dynamics and must be declared as such.

**What it buys:** Excruciating stops being structurally zero, which comes entirely from the cheap
half (5.1). ⚠️ Note that fatal vent wounds would buy the same thing by the same method at ~27% of
the magnitude (§1) — peritonitis is the larger and better-motivated choice, not the only one. Acceptance criterion 3 currently has to warn a reader not to read an empty Excruciating
column as "no severe suffering occurred"; with this channel the column is populated and the warning
becomes unnecessary. ⚠️ **It does not close most of the gap to the published aviary row on its own**
— the bulk of the peritonitis burden (1,120 h Hurtful, 2,090 h Annoying per affected bird) sits in
the chronic half, which is the expensive half.

**What it costs:** it is **non-discriminating**, like keel — baseline mortality is age-driven, so
good and negligent policies would tie on it. The fatal/non-fatal split is **ours**, and so is the
chronic incidence term if 5.2 is included.

### 4.3 What neither buys

Neither chapter quantifies in-house ammonia, in-house heat stress, footpad or red mite. The core of
`findings.md` §6 stands: the four levers we built the agent to move remain unquantified by the
literature. Chapter 6 narrows the finding rather than overturning it — it gives us *published*
tracks whose **prevalence** our agent moves, not published hour-figures for the harms our agent
causes.

---

## 5. Corrections to the existing record

- `findings.md` §0 and the `README.md` both say Ch. 5 and Ch. 6 were not read and that "neither maps
  onto a channel our substrate models today." The second half stays true; the first half is now
  stale and both files are updated to point here.
- `findings.md` §3 Q1 quotes 2 [1.5–3] h Excruciating for death from an infected vent wound. Ch. 5
  gives the same figure for fatal acute peritonitis. These are **not** two independent anchors —
  both are the severe-sepsis phase, and Ch. 9 says the Excruciating hours come predominantly from
  sepsis reached by either route. Do not add them as if they were separate.

---

## 6. Review record

Codex pair (`gpt-5.6-sol`, read-only, fresh sessions, run against this worktree), round 1: **seven
findings — six important, one minor, all high-confidence. All seven were verified against the
chapter PDFs, `pain-track-parameters.json` or the repo before being fixed; none was dismissed.**

| Finding | Disposition |
|---|---|
| A **third** print-versus-platform divergence was missed: printed Pain-Track 5.2 gives 10% Disabling in the chronic phase, the platform gives 1%, and only 1% reproduces the chapter's own 89 h burden | **Fixed** — §2.3 now carries the divergence and the arithmetic; `findings.md` §4.1 and the folder README updated from two divergences to three. Verified: 56 h + 33.6 h = 89.6 h at 1%, ~392 h at 10% |
| "Chapter 5 is the only route to a non-empty Excruciating channel" is false — fatal vent wounds, fatal cannibalism and depopulation fractures also carry Excruciating, and Ch. 5 only claims sepsis is unique *for such a long time* | **Fixed** — §1 now tables all four aviary Excruciating sources with their shares (peritonitis 78%, vent wound 21%) and narrows the claim to the only *practically available* route. Verified against the parameter set |
| The foraging bridge overclaims the chapter: wet litter is named for **dustbathing**, while foraging names stocking density, improper litter, access restrictions, crowding and poor health | **Fixed** — §1 and §4.1 now mark the wet-litter→foraging step as **ours**, and §4.1 argues against taking it |
| "Our agent already moves stocking density" is false — `stocking_density` is a stored field on `HouseWelfare` that no model layer reads and no tool sets | **Fixed** — verified by search; §1 now says only litter is a live lever and names the blocked density wave |
| "Adding the four aviary tracks needs no new physics" is inaccurate — nest and roosting have no substrate state at all, and authoring a prevalence function is itself model dynamics | **Fixed** — §4.1 rewritten to split the four into bridgeable (dustbathing; foraging on a declared assumption) and not-bridgeable (nest, roosting would be constants) |
| The same claim for peritonitis does not cover Pain-Track 5.2 — mortality can identify only the fatal cohort, so the chronic cohort needs an authored incidence term | **Fixed** — §4.2 split into the cheap fatal half and the expensive chronic half; the "closes most of the gap" claim withdrawn |
| (minor) "Read in full" sits beside an admission that no figure was inspected as an image | **Fixed** — §0 now says "text read in full" and states the exclusion explicitly |

**Round 2** (verdict REVISE, four findings — one important, three minor, all verified real):

| Finding | Disposition |
|---|---|
| The ledger's own summary still said neither chapter needs new physics, contradicting the corrected per-track split | **Fixed** in the ledger — the blanket claim is replaced by a pointer to the per-track split |
| §1's opening still said the agent "already moves" both named drivers, contradicting the stocking-density correction eight lines later | **Fixed** — the opening now says the drivers correspond to fields we carry, and defers to the limits below |
| The ledger still called both chapters "read in full" without the text-only qualification | **Fixed** |
| The fatal-cannibalism Excruciating share was taken from the JSON's rounded 0.0001 display; prevalence × per-affected gives 0.00006, so ~0.2% not 0.3% | **Fixed** — the two negligible rows now read "<1%", computed from prevalence × per-affected, with the rounding difference noted. The other shares, the 0.0389 total, the §3.1 cycle totals and the 89.6 h arithmetic were re-checked and stand |

**Round 3** (straight review: **no actionable defect**. Adversarial: three findings, all verified
real — one important, two minor):

| Finding | Disposition |
|---|---|
| "Peritonitis is the only *practically available* route to Excruciating" is still an overclaim: §4.2's own method (a literature share of baseline deaths, run through a Pain-Track) works identically for fatal vent wounds and cannibalism, and Ch. 8 supplies aviary prevalences for both | **Fixed** — §1 and §4.2 now say peritonitis is the **largest** route (78% against the vent wound's 21%) and note that vent wounds would populate the column by the same method at ~27% of the magnitude. Propagated to the README and the ledger |
| `findings.md` §6 still said peritonitis and behavioural deprivation are "the rest of the published aviary burden", excluding vent wounds, cannibalism and depopulation, which we also do not model | **Fixed** — a pre-existing error this pass exposed; §6 now calls them the two largest omitted blocks and names the others |
| A second ledger occurrence still said "read in full" without the text-only qualification | **Fixed** |

⚠️ **This loop reached its three-round cap.** All three round-3 items were propagations or
precision corrections of positions already adjudicated in earlier rounds, and the straight reviewer
returned clean, so they were applied rather than escalated. Across three rounds, **fourteen findings
were raised and fourteen were verified real and fixed; none was dismissed.** No fourth pass was run.
