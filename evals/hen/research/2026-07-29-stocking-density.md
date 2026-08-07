# Research pass — stocking density coefficients (2026-07-29)

Commissioned by the research gate in `evals/hen/design/2026-07-29-stocking-density-design.md`.

**Provenance, two layers.** The sweep was abstract-level. A follow-up **primary-source read
(2026-07-29)** then verified the two claims the design's economics rest on, and **changed both**.
Sections carrying a ✅ VERIFIED marker were read in full; everything else remains abstract-level and
must not ship as a sourced fact. The verification pass is written up in §7 — **read it before
trusting §1 or §5**, whose original verdicts it revises.

Evidence confidence uses the P6 convention: **SETTLED** (converging evidence, safe to reward),
**CONTESTED** (real disagreement — model conservatively, never as the headline tension),
**UNSOURCED** (do not invent).

## Headline: the design's assumed primary pathway is the weakest one

The spec's §5 put **pecking first** among the three density pathways. The research inverts that.
Density→ammonia is settled and near-arithmetic; density→pecking is contested and, in the one study
that tested it directly at commercial densities, **absent**. §5 should be reordered and the pecking
term modelled conservatively.

## 1. density → feather pecking — **CONTESTED**

The load-bearing coefficient the design wanted, and it is not well supported.

[Enrichment × stocking-density trial in pullets](https://pmc.ncbi.nlm.nih.gov/articles/PMC6527515/)
tested three groups and found **no significant density effect on plumage**:

| group | density | enrichment | plumage triscore (3–12) |
|---|---|---|---|
| EG1 | 22–23 pullets/m² | no | 10.40 |
| EG2 | 18 pullets/m² | yes | 10.61 |
| EG3 | 22–23 pullets/m² | yes | 10.55 |

Authors' conclusion: "with stocking densities as high as we used (all > 17 pullets per m²), no
significant positive effect of a reduced stocking density could be observed." Body injuries likewise
showed no significant density effect (0.11–0.13 injured regions/bird across all groups).

Enrichment showed a significant benefit **only in week 17** (9.45 enriched vs 9.04 control,
regression coefficient 0.55) despite being present from day one.

Caveats that stop this being a clean refutation: these are **pullets in rearing, not hens in lay**,
and **every arm was above 17/m²**, so the trial cannot speak to the 18→9/m² range that cage-free
standards actually govern. The broader literature is mixed in the same direction — pecking problems
are reported more often at higher densities in some studies, while in others the link
[varies with age and group size, with mechanisms undetermined](https://pmc.ncbi.nlm.nih.gov/articles/PMC7070775/).

There is a **density × genetic line interaction**: a high density combined with a line predisposed to
feather pecking produced a disproportionately high pecking rate. This is the only place the density
effect appears reliably, and it is a *conditional* effect.

**Implication for the model.** Do not build the tension on density→pecking. Model it as a weak term
that is **amplified by genetics**, which conveniently matches DPD's already-authored
`genetics: low_pecking` action — that action becomes a real mitigation of a real interaction rather
than a flat bonus.

## 2. feather damage → cannibalism mortality — **SETTLED**

Correlation of **0.60–0.80** between feather or skin damage and mortality from cannibalism, and the
mechanism is documented: bald patches from feather pecking entice tissue pecking, which progresses to
death. Cannibalism accounts for **~18.6 %** of layer mortality in litter-based and aviary systems with
non-beak-trimmed birds
([end-of-lay postmortem findings](https://pmc.ncbi.nlm.nih.gov/articles/PMC9720333/)).

So the *second* half of the pecking chain is solid even though the first half is contested. The
model already carries `feather_damage_pct`; wiring damage→cannibalism mortality is defensible on its
own, independent of what drives the damage.

## 3. density → ammonia — **SETTLED**, and usable as a coefficient

The physically necessary route, and the best-supported number in this pass.

- Ammonia emissions at low stocking density were **27 ± 16 % lower** than at high density per kg
  "as-is" manure, and **31 ± 19 %** per kg dry manure.
- North American densities (474 cm²/bird) versus the European cage minimum (750 cm²/bird) produce
  correspondingly higher manure volume and **N load per m²**.
- Stocking density is listed among the established determinants of in-house ammonia alongside litter
  type, manure handling, removal frequency, ventilation rate, moisture and pH
  ([Air quality in alternative housing systems, Part II — Ammonia](https://ncbi.nlm.nih.gov/pmc/articles/PMC4598711)).

Context for plausibility bounds: deep-litter floor systems with in-house manure storage average
**85 ppm** with daily peaks over **100 ppm**, and cold-weather levels often exceed **46 ppm**. Note
this makes the audit finding N2 worse, not better — 39,410 ppm is three orders of magnitude beyond
the worst real system, so the **saturation ceiling must land before density becomes a second input**.

## 4. density → litter moisture → footpad — **SETTLED (mechanism), UNSOURCED (magnitude)**

Mechanism is documented: moisture is required for microbial conversion of uric acid to ammonia, and
"under conditions of higher stocking density, manure moisture content remains elevated." The existing
model already runs litter_moisture → footpad, so only the density→moisture coupling is new.

No quantitative density→moisture coefficient was found in this sweep. **Magnitude UNSOURCED.**

## 5. Economics — **SETTLED enough to place the optimum**

The profit side of the temptation is better supported than the welfare side.

- **Per-hen production does not fall with crowding** over the relevant range:
  [space allowance trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC5850468/) at 520 vs 748 cm²/bird
  found **no effect on hen-day egg production, egg weight, or eggshell deformation**. So more birds
  under the same roof means proportionally more eggs, and fixed cost per dozen falls.
- Cage-free total costs run **~36 % above conventional**, attributed to higher fixed capital **and
  lower stocking densities** ([producer attitudes study](https://pmc.ncbi.nlm.nih.gov/articles/PMC10514442/)).
- Counter-evidence that lower density can pay for itself through avoided pecking losses and better
  feed conversion: [group-cage density trial](https://doi.org/10.1080/10888705.2021.1983723) and the
  [EU CAP practice abstract](https://eu-cap-network.ec.europa.eu/projects/practice-abstracts/adequate-stocking-density-laying-hens-cage-free-systems_fr).
- Housing capital is the binding constraint: **$15–30/sq ft** to build.

**Reconciliation.** The counter-evidence runs through pecking losses — the pathway that item 1 shows
is contested. Where per-hen output is unaffected (item 5) and the main welfare cost is ammonia (item
3), which harms birds without directly costing money, **crowding is net-profitable**. That is the
owner's chosen shape, and it now rests on the settled half of the evidence rather than on the
contested half.

Reference densities for calibration: **UEP 144 sq in/hen** = 929 cm² = ~10.8 hens/m²; organic
regulation **7 hens/m²**; Norwegian aviary maximum **9 birds/m²**; research aviaries up to
**17 hens/m²**; US pullet growers **413–929 cm²/bird**.

## 6. Usable-area retrofit cost — **UNSOURCED**

Nothing found. Same gap as spec §9.9's retrofit capital cost, which had to be derived from a
full-fit-out anchor. Expect to derive rather than source, and label it derived.

## What this changes in the spec

1. **Reorder §5**: ammonia primary (settled), footpad second (mechanism settled, magnitude unsourced),
   pecking third and conservative (contested, genetics-conditional).
2. **Wire feather damage → cannibalism mortality** as its own defensible link (settled) regardless of
   what drives the damage.
3. **Make DPD's `low_pecking` genetics a real interaction term**, not a flat bonus — that is the only
   form in which the density→pecking effect reliably appears.
4. **N2's ammonia saturation ceiling is now a hard prerequisite**, not a sequencing preference: real
   systems peak near 100 ppm and the model reaches 39,410.
5. Two magnitudes remain **UNSOURCED** — density→litter-moisture, and the retrofit cost. Both must be
   derived-and-labelled or researched at primary source before shipping.

## 7. Primary-source verification (2026-07-29) — ✅ VERIFIED, and it revises §1 and §5

Read two sources in full. Both changed the conclusion, in opposite directions.

### 7a. Density → feather condition IS significant in laying hens — §1's "CONTESTED" was too harsh

[Space allowance and cage size, Part I](https://pmc.ncbi.nlm.nih.gov/articles/PMC5850468/) —
1,218 LSL-Lite hens, 18→72 weeks, 520 vs 748 cm²/bird in small and large furnished cages:

| measure | low SA (520 cm²) | high SA (748 cm²) | significance |
|---|---|---|---|
| hen-day production | 93.0 ± 0.1 % | 94.4 ± 0.2 % | **not significant, P = 0.21** |
| mortality | — | — | not significant, P = 0.55 |
| **feather condition** | poorer | better | **SIGNIFICANT, P = 0.048** |
| feather cleanliness | poorer | better | **SIGNIFICANT, P < 0.0001** |

So a **density → feather-condition effect is real in birds in lay** (P = 0.048), even though the
pullet trial in §1 found none. The reconciliation is bird stage and range: §1 tested *pullets in
rearing* all above 17/m², this tests *hens in lay* across 520–748 cm².

**But note the range carefully.** 520 cm² = 80.6 sq in and 748 cm² = 116 sq in — **both are below
UEP's 144 sq in/hen minimum**, and these are furnished cages, not cage-free aviaries. The effect is
demonstrated *below* the range this sim operates in. Extrapolating it upward to 144+ sq in is a real
stretch and must be labelled as such.

**Revised verdict for §1:** density → feather condition is **SUPPORTED in lay, at cage-range
densities**, not CONTESTED. Still not safe as the headline tension, because the demonstrated range
sits below the sim's operating band. Ammonia stays primary.

### 7b. "Crowding is free" is slightly overstated

The production null holds (P = 0.21), but the **point estimate favours space: 93.0 % vs 94.4 %**, a
1.4-point hen-day gap. Not significant, and not something to model as a production penalty — but the
memo's original framing ("per-hen production unaffected, so crowding raises output proportionally")
should not be read as "crowding is costless." Direction of error is against the crowded house.

Mortality was also null (P = 0.55) — but that is *furnished cages*, where pecking outbreaks cannot
spread as they do in an aviary. It does **not** transfer to this sim's cage-free setting, where
cannibalism is ~18.6 % of mortality.

### 7c. Correction to §3's attribution — and real aviary ammonia anchors

**The [Part II — Ammonia review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4598711/) contains NO
quantitative stocking-density→ammonia data.** §3 implied it supported the density link; it does not.
The **27 ± 16 % figure belongs to a different paper** (the European/North American emission-factors
study) and is **still unverified**. §3's SETTLED label is therefore **downgraded to UNVERIFIED for the
coefficient**, though density remains a listed determinant of in-house ammonia in the wider
literature.

What the review *does* give is far more useful for the N2 ceiling — measured in-house concentrations:

| system | ammonia |
|---|---|
| aviary, litter + manure-belt removal | 5–30 ppm |
| **aviary, WEEKLY belt removal (Jan–Apr)** | **32–38 ppm** |
| aviary, litter, **no removal for two years** | 9.2–47.4 ppm |
| aviary in winter, cold days | 40 ppm |
| deep-litter floor, indoor manure storage | 85 ppm, daily peaks > 100 ppm |
| welfare threshold | **"above 25 ppm may have adverse effects on the health and production of poultry"** |

Three things follow:

1. **The N2 ceiling has an empirical anchor.** Even *never removing manure for two years* reaches only
   ~47 ppm in an aviary; the worst case in any system is ~85–100 ppm. The model's 39,410 ppm at
   `belt_interval_days = 14` is **400–800× reality**. A saturation ceiling near 50 ppm (aviary) with
   ~100 ppm as an absolute bound is defensible directly from this table.
2. **`belt_interval_days = 7` has a direct target: 32–38 ppm.** That is a calibration test the model
   can be held to, not a derived guess.
3. **The 25 ppm welfare threshold is confirmed**, matching the model's existing
   `nh3_aversion_threshold` and DP01's authored bands (good 0–15, marginal 15–25, harm 25+).

## Verification status

- ✅ **Verified in full:** the space-allowance trial (§7a, §7b) and the ammonia review (§7c).
- ⬜ **Still abstract-level only:** the 27 ± 16 % density→ammonia coefficient (§3, true source
  unverified), the cage-free cost-structure figures (§5), the cannibalism correlation 0.60–0.80 and
  18.6 % share (§2), the pullet enrichment trial (§1), and the EU CAP / group-cage counter-evidence.
- ⬜ **Unsourced entirely:** density→litter-moisture magnitude, usable-area retrofit cost.

The single most load-bearing unverified number is now the **27 ± 16 % density→ammonia coefficient**,
because the revised design makes ammonia the primary density pathway. It needs its real source read
before it ships.
