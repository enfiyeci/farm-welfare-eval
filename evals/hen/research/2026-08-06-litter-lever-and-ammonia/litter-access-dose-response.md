# Q1 — the dose-response between litter access hours and litter moisture

> **Re-run of the pass that died on the API session limit** (see
> [litter-access-hours-partial.md](litter-access-hours-partial.md)). Commissioned 2026-08-06 20:50 PT,
> after the limit reset. **Delegated subagent finding.** Its coverage statement and every ⚠️
> partial-read flag are preserved verbatim below. The orchestrating session has **not** independently
> re-read the primary sources. Trace item 1 of the fetch list before any coefficient is authored.

## Bottom line

**No study anywhere measures litter moisture at three or more levels of litter access time.** The
Oliveira pair is the only within-house controlled hours→moisture contrast that exists. The authored
straight line of ~1.9 percentage points of moisture per hour is arithmetically right for that pair
(31.3 − 20.3 = 11.0 pp over 16 − 10.17 = 5.83 h → 1.89 pp/h) but it is **an interpolation with zero
interior support**, and three findings say the true relationship is not a fixed linear offset:

1. **Oliveira's own effect vanished by the end of the trial.** At the final sampling the two regimens
   were statistically indistinguishable (20.6 ± 1.2% full access vs 19.6 ± 1.2% part access,
   P = 0.57). A constant 1.9 pp/h coefficient cannot reproduce that.
2. **The effect is mediated by accumulated litter depth and caking, not by hours directly.** Litter
   depth differed 2.3× (3.77 vs 1.64 cm) and caking 33.1% vs 0%. The paper attributes caking to
   depth, not to hours.
3. **A third house at 8.75 h/day sat at 14.6% moisture**, which does not lie on Oliveira's line — a
   between-house gap larger than the whole access-hours effect.

There **is** a well-supported, near-linear dose-response one stage upstream: **hours → share of manure
deposited on the litter floor.** That is where the authored line belongs, with moisture derived from a
water balance.

## The three real litter-moisture anchors

| Access (h/day) | Litter moisture | House / source |
|---|---|---|
| 8.75 (13:00–21:45) | **14.6 ± 2.4%** | Commercial Iowa aviary, 50,000 hens — [Zhao, Zhao, Wang & Xin 2013, ASABE 131618601](https://doi.org/10.13031/aim.20131618601) |
| 10–12 (reported range) | **10–15%** | US commercial aviary, field measurement reported by [Chai et al. 2017, Trans. ASABE 60(2):497–506](https://doi.org/10.13031/trans.12081) citing Zhao 2013 |
| 10.17 (10:50–21:00) | **20.3 ± 1.1%** | Iowa Cage Free, Big Dutchman Natura 60 — [Oliveira et al. 2019, Poult. Sci. 98:1664–1677](https://doi.org/10.3382/ps/pey525), part access |
| ~16 (lights 05:00–21:00, doors always open) | **31.3 ± 1.6%** | Same house, interleaved sections — Oliveira 2019, full access |
| Full day (with forced litter drying) | 14.4–20.1% | Tiered Wire Floor research aviary — [Groot Koerkamp 1998 PhD thesis, ch. 7](https://edepot.wur.nl/210633) |
| Not reported (barn / free-range) | ~29–30% | 28 German commercial flocks — [Spindler et al. 2023, Poult. Sci. 102:102705](https://doi.org/10.1016/j.psj.2023.102705) |

Read **across** houses the slope disappears. Zhao's 8.75 h house (14.6%) against Oliveira's 10.17 h
house (20.3%) implies 4.0 pp/h; Zhao against Oliveira full-access implies 2.3 pp/h; and Groot
Koerkamp's **full-access** house with litter drying was *drier* than Oliveira's 10-hour house.
**Between-house factors — belt removal frequency, forced litter drying, litter removal schedule,
ventilation, season — swamp the access-hours term.**

## Where the relationship IS well supported: hours → manure on the floor

| Access | Share of total manure dry matter landing on litter | Source |
|---|---|---|
| 8.75 h | **9.1 ± 0.9%** | Zhao et al. 2013 (direct measurement; total manure 35.8 ± 1.4 g DM/hen/d) |
| ~10.2 h | **~15%** | *Subagent inference*: Oliveira part-access 0.53 kg/100 hens/d ÷ Zhao's 35.8 g/hen/d |
| ~16 h | **~29%** | *Subagent inference*: Oliveira full-access 1.05 kg/100 hens/d ÷ 35.8 g/hen/d |
| Full day | **22.5%** | Groot Koerkamp et al. 1995, as reported in Zhao et al. 2013 |

Monotone and roughly linear at ~2.5–3 percentage points of manure share per hour over 8.75–16 h.

### The one clear non-linearity: morning hours are heavier than evening hours

Oliveira's deposition ratio is 1.98× while his hours ratio is only 1.57×. Per hour of access, full
access deposited 0.66 g DM/hen/h against part access's 0.52; **the marginal 5.8 morning hours carried
~0.89 g DM/hen/h, about 1.7× the part-access average** (*subagent's calculation from published
means*). Mechanistically expected: part-access hens spend the post-lights-on, post-feeding, peak-
defecation window emptying onto the manure belts instead. Feed was delivered at 05:30 and 09:30, both
inside the confinement window.

**Implication:** the hours→floor-manure curve is convex toward the morning. A symmetric linear lever
will **understate** the benefit of closing the first hours of the day and **overstate** the benefit of
closing the last hours.

## Two time constants, and conflating them is the main modelling risk

**Fast — moisture in a given litter bed: hours to ~2 days.**
Zhao measured litter moisture rising by 19:00 h within the access period. Groot Koerkamp's validated
water-balance model for a 1 cm bed (ch. 7, R²adj = 90%) fits
`C_water,t = 126.8 + 0.488·C_water,t−1 − evaporation`. The autoregressive coefficient of **0.488/day**
means ~51% of any perturbation decays per day; e-folding time ≈ 1.4 days. The gross wetting term alone
is **126.8 g water per kg litter per day** — the bed's water turns over almost completely each day.
Independent confirmation: in Chai et al. 2018's chambers, stopping a daily spray dropped moisture
16.1% → 14.7% in three days; building it up gave 10.3 → 13.9 (d4) → 15.2 (d7) → 16.1 (d10), a clearly
**saturating** approach with a ~3–5 day constant.

**Slow — litter depth, caking and drying resistance: weeks to months.**
Litter accumulates at 0.44–1.15 mm/d (full access) vs 0.22–0.31 mm/d (part access) in Oliveira;
0.17 mm/d in Zhao's 9.75 h house. Max depth 6.3 vs 2.2 cm. Oliveira attributes caking to depth, not
hours: increased caking "presumably arose from the thicker litter being more difficult to be dried by
the ventilation air." The three whole-house litter removals (37/38, 54/55, 77/78 weeks of age) reset
this variable, and the moisture gap had **closed entirely** by the post-cleanout final sampling.

**So an access-hours change should move litter moisture within a few days by an amount set by the
water balance, but the large gaps Oliveira measured are the accumulated months-scale divergence in bed
depth and structure, not the instantaneous response.**

### Do wetting and drying fight each other? Yes, and wetting wins

Two independent studies converge on the wetting side: stabilised water flow to litter of
**7.3 g/hen/day** (Groot Koerkamp ch. 8, full access, after 30 weeks) and **7.7 g/hen/day** (Zhao
2013, 8.75 h access). Droppings are 160–180 g/hen/d at 20–25% dry matter. Drying by scratching is real
but modest and two-edged — Chai et al. 2018 note mechanical tilling "accelerated the loss of moisture
from litter to air" *and* that it "is expected to accelerate NH₃ emissions, as the exchange between
the air and litter is enhanced." *Subagent inference*: the scratching-drying term scales with hens
present, the same driver as the wetting term, so it cannot flip the sign at commercial density — but
it flattens the slope.

### The age effect dwarfs the hours effect

Groot Koerkamp ch. 8 measured water flow to litter peaking at **~45 g/hen/day around 20 weeks of age**
and falling to ~7 g/hen/day by 30 weeks — a **6× swing driven purely by behaviour**, against roughly
2× from full-versus-part access. He ties this explicitly to the classic early-lay wet-litter
complaint. **If the eval has a flock cycle, this age term is a bigger lever on litter moisture than
the agent's access-hours setting.**

## Dependence on ventilation, season, density, depth

**Ventilation and season — strongly, and not in the obvious direction.** Oliveira: both regimens
exceeded 25 ppm NH₃ in Jan 2017; in Feb 2017 and Jan 2018 **only full access** exceeded; after March
2017 with warm-weather ventilation both fell below. **The lever is worth most under minimum
ventilation.** Groot Koerkamp ch. 7: evaporation ∝ **v_air^0.287** × vapour-pressure difference —
doubling air velocity over the litter raises evaporation only ~22%. **Air velocity is a weak drying
lever; the vapour-pressure difference dominates.** He therefore predicted drying conditions **worsen
from April to October** under Dutch conditions as outdoor vapour pressure rises. Summer is not
automatically drying. Zhao 2013 fitted a **U-shaped** indoor ammonia vs ambient temperature:
`[NH₃]in = 7.4 − 0.4·Ta + 0.01·Ta²` (R² = 0.52), minimum near 20 °C.

**Litter-area stocking density — multiplicative.** Water load per m² = (hens per m² of litter) ×
(g water/hen/day reaching the floor). Litter allowances: 525 cm²/hen (Oliveira), 510 (Zhao), 322
(Groot Koerkamp, 31 hens/m² litter). *Subagent inference*: density and access hours should enter as a
**product**, not a sum.

**Belt removal frequency is a competing lever of similar or greater size.** Groot Koerkamp's ammonia
model gives +0.76% per hour of belt-manure residence; Zhao 2013's regression found ambient temperature
(standardised coefficient 0.62) mattered more than floor manure accumulation time (0.38). Zhao's
cross-study table shows European all-day-access aviaries spanning **0.7 to 38 ppm** depending on
removal frequency and drying — a >50× range at constant access hours.

### 🔴 Calibration warning — lab curves overpredict the field by 4–5×

Groot Koerkamp's **field** coefficient is +0.32% NH₃ per g/kg water = **+3.2% per percentage point of
moisture**, which over Oliveira's 11 pp predicts +42%. Oliveira **measured +27%** (17.2 vs 13.5 ppm).
The lab chamber curves imply 4–5×. A model calibrated on lab moisture→ammonia curves will **massively
overpredict** the ammonia consequence of an access-hours change in a real house — because of shared
airspace, caking suppression in the wetter treatment, and concentration ≠ emission.

Moisture→ammonia is also **non-monotonic and convex below the peak**: peak release at **40–60%**
moisture (Groot Koerkamp Fig. 8), **~42% at 75 °F and ~46% at 95 °F**
([USDA ARS Livestock GRACEnet factsheet](https://www.ars.usda.gov/ARSUserFiles/np212/LivestockGRACEnet/LitterMoisture.pdf),
from Miles, Rowe & Cathcart 2011). Below the peak at 75 °F: 25% moisture = 1.4× the ammonia of 20%;
30% = 1.8×. **Caked litter suppresses release** — the factsheet is explicit that compacted litter
forms a physical barrier.

## Confounds in the Oliveira result itself

A genuinely good field study — same house, 32 interleaved sections, 8 replicates per treatment, 14
months, blinded welfare assessors. But the moisture contrast is **not a clean hours effect**:

1. **Litter depth is confounded with the treatment and mediates the result** (3.77 vs 1.64 cm; 2.3×
   more litter removed), and the authors say so.
2. **The treatments started at different ages.** Full-access hens got litter ~10 days after transfer
   at 17 weeks; **part-access hens were confined a full 4 weeks and got no litter until 22 weeks** —
   so their litter had ~3 fewer weeks of accumulation from the start, and that head start falls
   exactly in the 45 g water/hen/day peak-deposition window.
3. **The effect is not stable over time** — P = 0.57 at the end of the experiment.
4. **Ammonia was measured section-by-section in a shared airspace** (32 sections of one 153 m house
   with mixing fans), so the 3.7 ppm gap is a **lower bound** on what separate houses would show.
5. **Moisture sampling is coarse** — once a month, 3 locations, 4 sections per treatment. ⚠️ The
   monthly time series exists only as **Figure 3, a raster image the agent could not extract**, so
   whether the gap opened gradually or stepped after each cleanout is unreadable from the text.
6. **Whole-house litter removals interrupt the series three times**, with all hens locked in for 10
   days each — three natural "0 h access" episodes whose moisture response is not reported
   numerically.
7. **Cumulative mortality was 14.3%**, against a 4.8% Dekalb White breed reference. Not a pristine
   flock.
8. Author-stated caveat: the December 2017 ammonia point was collected on a mild 15 °C day and was
   "likely not reflective of the actual levels in the cold weather."

**Net:** the **direction** is solid and mechanistically over-determined. The **magnitude of 11 pp** is
a composite of hours, three extra weeks of confinement at the peak-deposition age, and the resulting
divergence in bed depth and caking. Treating 11 pp as the pure hours effect at any point in the cycle
overstates the lever.

## Implications for the model

1. **Do not author `litter_moisture = f(hours)` directly.** Author `floor_manure_share = f(hours)` —
   four supporting points, convex morning weighting — then derive moisture from a water balance.
2. **Two time constants**: ~1.5–3 days for moisture within a bed; weeks-to-months for depth and
   caking. Since `litter_moisture` already relaxes to a belt-frequency equilibrium
   (`farm_eval/env/model/layers/litter.py`), the access-hours lever belongs in the **source term of
   that same relaxation**, not as a separate offset.
3. **Weight the marginal hour by time of day** — morning hours carry ~1.7× the average manure load.
4. **Add the age term** or the sign of "wet litter season" comes out wrong.
5. **Ventilation's air-velocity exponent is 0.287** — a weak drying lever per unit of air. A model
   that makes summer automatically drying contradicts Groot Koerkamp.
6. **Cap the ammonia response** — use the field coefficient (~3.2% per pp of moisture), not a lab
   curve; remember the peak at 40–46% and caking suppression.
7. **Document the 1.9 pp/h line as an authored assumption**, sourced to a single confounded two-point
   contrast whose effect disappeared by end of cycle.

## Coverage statement (subagent's own, verbatim)

**Read end to end:** Oliveira et al. 2019 (full PMC6414038 text, all sections/tables/references);
Oliveira & Xin 2018 ILES conference paper ILES18-013 (full 8-page PDF text); Chai et al. 2018 Trans.
ASABE 61(1):287–294 (full PDF incl. all tables); USDA ARS GRACEnet litter-moisture factsheet (full
2-page text); Groot Koerkamp 1998 thesis **chapters 7 and 8** end to end, plus ch. 2 §3.

**Read in part — ⚠️ flagged:**
- ⚠️ Oliveira et al. 2019: **Figures 1–7 are raster images and were not readable.** Figure 3 (monthly
  litter moisture/depth time series) and Figure 5 (seasonal ammonia) contain interior data not
  extractable.
- ⚠️ Groot Koerkamp 1998 thesis (155 pp / 6,782 lines): abstract, contents, ch. 2 §3, ch. 7 and 8 read
  in full. **Chapters 1, 3, 4, 5, 6 and 9 not read.** Ch. 5 (degradation and volatilisation) and ch. 6
  (litter drying system performance) plausibly hold further quantitative dry-matter→ammonia
  relationships not retrieved. Figures are images throughout.
- ⚠️ Zhao et al. 2013 Trans. ASABE 56(3):1145–1156: introduction, Table 1, ammonia results/discussion
  and the regression (Table 4) read. **CO₂, thermal-environment and ventilation-rate sections skimmed
  by keyword, not read.**
- ⚠️ Zhao, Zhao, Wang & Xin 2013 ASABE 131618601: abstract, manure-production and moisture-content
  sections read in full. **CO₂-production sections and conclusions not read end to end.** Figures
  10–14 (incl. the within-day litter moisture curve) are images, not extracted.
- ⚠️ Chai et al. 2017: LMC/thermal section, Tables 4 and 6, ammonia discussion read. **Introduction,
  methods and PM sections not read in full.**
- ⚠️ Spindler et al. 2023: abstract, litter-condition and chemical-analysis methods, first four
  laying-month rows of Table 1 read. **Results, discussion, and laying months 5–12 not read.** No
  litter-height↔dry-matter correlation was established from this paper — only that each independently
  predicts integument condition.
- ⚠️ Alm et al. 2015 Poult. Sci. 94:565–573: **only the abstract, methods, and every line containing
  "litter"** read by keyword. The claim (no treatment-wise litter moisture reported) rests on that
  keyword pass, not a full read.
- ⚠️ Oliveira et al. 2026 (litter-restriction rebound): abstract read; whole text searched for
  "moisture", "dry matter", "ammonia" — **zero occurrences.** Not read end to end.

**Could not reach at all:**
- ⚠️ **Miles, Rowe & Cathcart 2011, Poult. Sci. 90:1397–1405** — ScienceDirect **HTTP 403**. This is
  the primary source behind the factsheet's multipliers and the 42%/46% peak; only the secondary
  reporting was used.
- ⚠️ **Liu, Wang, Beasley et al. 2007, J. Atmos. Chem. 58:41–53** — Springer paywall. Snippets suggest
  water applied to litter *initially suppresses* ammonia and only raises it after 1–2 weeks. **Not
  verified and not relied on above.**
- ⚠️ WATTAgNet "5 ways to minimize ammonia in aviary housing" — HTTP 403. **Not verified, not used.**
- ⚠️ Jofran Oliveira's PhD dissertation — **not present** in the Iowa State repository (DSpace
  discovery API queried directly; 18 results, no dissertation). May be undeposited or in ProQuest.
- ⚠️ `dr.lib.iastate.edu` HTML search UI returns 403 to fetches; worked around via the DSpace REST API.

## Fetch list — needs institutional access

1. **Oliveira, J.L. — PhD dissertation, Iowa State (ABE, ~2019)**, try ProQuest. *Would settle:* the
   monthly moisture series behind Figure 3, per-location values, and whether the gap opened gradually
   or stepped after each cleanout. **Highest value — the only place interior structure of the one real
   dose-response could exist.**
2. **[Miles, Rowe & Cathcart 2011, Poult. Sci. 90:1397–1405](https://doi.org/10.3382/ps.2010-01114).**
   (DOI corrected on claim 2026-08-07 — an earlier revision had `…-01144`.) **CLOSED:** the full PDF
   was claimed from the stocking-density archive branch into `evals/hen/research/sources/`, and the
   paper was read end to end at source (`../2026-08-07-litter-prep/02-source-traces.md` §2).
   *Would settle:* the exact ammonia-vs-moisture surface (20–46% × 75/95 °F) so the NH₃ layer uses the
   primary curve and places the suppression turnover correctly.
3. **[Liu, Wang, Beasley et al. 2007, J. Atmos. Chem. 58:41–53](https://doi.org/10.1007/s10874-007-9076-8).**
   *Would settle:* whether wetting transiently suppresses ammonia for 1–2 weeks. If true it explains
   the +27%-vs-+42% field/lab gap and means the moisture→NH₃ path needs a **lag**, not a map.
4. **Groot Koerkamp 1998 thesis, chapters 5 and 6** — free at
   [edepot.wur.nl/210633](https://edepot.wur.nl/210633), just unread. *Would settle:* the quantitative
   dry-matter→ammonia relationship and achievable drying rates and costs. **No access barrier — only
   reading budget.**
5. **Corresponding author of Oliveira et al. 2026** (the 1,152-bird rebound study). *Would settle:*
   whether litter moisture, depth or ammonia were recorded but unpublished — the only known second
   controlled full-vs-part-access experiment.
6. **Dekker et al. 2011** (Zhao 2013 Table 1: 8.3–11 h/d combined litter+outdoor, NH₃ 12.7–15.5 ppm).
   *Would settle:* whether litter moisture was measured alongside, giving a European anchor in the
   same hours band.
7. **Hayes et al. 2013, Trans. ASABE 56(5):1921–1932** (Midwest US aviary layer houses). *Would
   settle:* a fourth commercial aviary's hours and moisture, and whether the between-house scatter
   (14.6% vs 20.3% at ~9–10 h) is typical or anomalous.
