# Three footpad/litter PDFs read in full — the moisture model is mis-anchored at both ends

> Owner obtained these on 2026-08-06 after every automated fetch failed. All three were read end to
> end. This closes the footpad half of decisions 01 and 03, and produces one finding nobody was
> looking for.

## The headline: two compensating errors

**Our litter-moisture band is too dry, and our footpad threshold is too low, and the two errors
partly cancel — which is probably why neither was caught.**

- `fpd_moisture_ref` is **13.0%** — the moisture below which the model generates no new lesions.
- Wang, Ekstrand & Svedberg's **low-lesion** arm averaged **28.7–31.8%** moisture.
- No paper here reports a working laying-house litter floor below about **18%** in situ.
- Our model operates at **15–20%**.

So the model computes "excess moisture" of roughly 2–7 points above a threshold that should probably
sit near 30%, on a band that is itself below anything measured on a real floor. Set either parameter
correctly on its own and the footpad channel would go quiet; both being wrong in opposite directions
is what keeps it producing numbers.

## 1. Wang, Ekstrand & Svedberg 1998 — the anchor, now with its numbers

[*Br. Poult. Sci.* 39:191–197](https://pubmed.ncbi.nlm.nih.gov/9649870/). Read in full, 8 pp.
**Note the attribution:** this is Wang, Ekstrand & Svedberg. An earlier pass in this repo called it
"Ekstrand & Carpenter" — that was wrong.

Litter moisture by treatment (Table 1, p. 193), means over the 44-week experiment:

| Group | Treatment | Mean moisture |
|---|---|---|
| 1 | dry litter, dry perches | 31.8% ± 8.69 |
| 2 | dry litter, wet perches | 28.7% ± 7.15 |
| 3 | wet litter, dry perches | 54.8% ± 2.69 |
| 4 | wet litter, wet perches | 53.3% ± 2.64 |

Within each two-week litter-change cycle the dry arms ran **17% → 31–43%**; the wet arms stayed
**50–64%**. Difference between arms P<0.01.

Design: 120 White Leghorn (Hisex) hens, 4 pens of 30, **6 birds/m²**, softwood shavings 18 kg/pen at
~6 cm, 15–44 weeks of age. FPD scored weekly on an 11-point ordinal scale by one vet throughout.
**No significant ammonia or pH difference between treatments (P>0.05)** — moisture, not ammonia,
tracked with footpad damage in this study.

⚠️ **The temperature gate is softer than the abstract suggests.** The finding is real — *"when it was
below 20°C there were no new cases of dermatitis in any of the 4 treatments"* — but the Discussion
(p. 196) offers a competing explanation: by the cool final month most susceptible birds had already
converted, the wet groups being >90% affected. The authors do not disentangle them.

**Perches:** a severity modifier, not an incidence driver. Wet vs dry perches did not change incidence
(P>0.05) but roughly doubled lesion area (9.2 vs 3.7 mm²). The authors flag that contrast as
non-replicated and not statistically analysable.

## 2. Volkmann et al. 2024 — has no moisture data at all

[*Ann. Appl. Biol.* 185:108–115](https://onlinelibrary.wiley.com/doi/10.1111/aab.12923). Read in
full, 8 pp. 15,448 hens, 39 German flocks, farm sizes 290–178,000 birds, ages 1–92 weeks, visited up
to 16 times over 2011–2022. **Non-cage only** — 8,632 barn, 6,816 free-range.

**This was our most-wanted paper for a layer moisture dose-response. It does not contain one.** Litter
quality was a **3-point visual category** (1 dry/good, 2 wet/sticky, 3 bad/caked), scored by eye, and
it came out **non-significant (P = .0940)**. No moisture percentage, dry-matter figure or any
continuous hydrometric value appears anywhere. The authors say so themselves (p. 111): *"for an
improved and objective assessment of LQ, the moisture, pH value and ammonia content should be
measured (Wang et al., 1998)"* — they point back at the 1998 paper precisely because they have no
numbers of their own.

What it does establish (Table 5, p. 113; GLMM log-scale estimates, no confidence intervals):

| Factor | Significant | Detail |
|---|---|---|
| Flock age | Yes, P<0.0001 | estimate −0.047 (wk 1–17) → 0.471 (wk 41–60) |
| Litter **type** | Yes, P<0.0001 | vs straw: sand +2.36, straw pellets +0.74, lignocellulose +0.59, wood shavings +0.27, miscanthus +0.23 (n.s.) |
| Season | Yes, P<0.0001 | March–May **lower** than Dec–Feb (−0.39) |
| Age × flock size | Yes, P<0.0001 | worse for older hens in flocks under 10,000 |
| Flock size (main) | No, P = .2696 | kept only for the interaction |
| Litter **quality** (visual) | **No, P = .0940** | |
| Housing system | No, P = .2696 | barn vs free-range |

⚠️ **An unreconciled internal tension:** sand had the **best raw** outcome (94.4% FPD0) but the
**worst model estimate** (+2.36). The authors flag it (p. 111) — sand was tested on 250 birds against
6,052 on wood shavings — and discount it themselves. Both results sit in the paper.

Prevalence: 78.9% FPD0 overall (18.6% slight, 2.2% moderate, 0.3% severe). Affected proportion runs
from ~1% in the youngest birds to a peak of **~38.8% at 41–60 weeks**, settling to ~34.4%.

⚠️ The paper records housing only as "barn" or "free-range" and never says whether "barn" includes
multi-tier aviary.

## 3. Bist et al. 2023 (MDPI AgriEngineering 5:1663–1676) — a US cage-free aviary floor reads 18–21%

Read in full, 14 pp. 2,304 Lohmann Brown Lite hens, 576 per room, four rooms of a **NATURA60 multi-tier
aviary** at Michigan State, 50 weeks of age, six-week summer trial.

| Room | Litter moisture |
|---|---|
| Control (no fresh bedding) | **18.0% ± 2.8** |
| Small flake shavings | 20.0% ± 3.1 |
| Large flake shavings | 20.6% ± 2.4 |
| Aspen wood chips | 19.7% ± 4.2 |

Differences between rooms P<0.038, and moisture **rose over the trial** (week 1 ≈14–18%, week 5
≈19–23%). Counter-intuitively, rooms given fresh bedding ran about 10% **higher** moisture than the
control — fresh bedding suppressed airborne dust rather than drying the floor.

⚠️ **Two things it does not contain**, both of which we hoped for: no footpad or ammonia outcomes
(it measures particulate matter only — footpad and ammonia appear solely as background citation), and
**no crossing of litter depth against moisture**. It reports depth separately (4.57 → 5.74 cm across
treatments, no significant difference, P = 0.96) but never against moisture.

Its real value here is incidental: it tells us what a real US cage-free aviary floor actually carries,
and the answer is **18–21%**, with the driest condition measured being the untouched control at 18.0%.

## What this settles, and what it does not

**Settled:** `fpd_moisture_ref = 13.0%` has no support in any of these three papers, and the nearest
defensible anchor from Wang would put it near 30%. Our 15–20% operating band sits at or below the
driest working floor any of them measured.

**Not settled, and not settleable from these:** there is still **no moisture → footpad dose-response
curve for laying hens.** Wang gives a two-point step (≈30% vs ≈54%) confounded with temperature and
with time-in-cycle. Volkmann has no moisture data. Bist has no footpad data. A curve would need a study
measuring continuous litter moisture against graded FPD score in layers — and none of the three
suggests one exists.

## Coverage statement

All three read to their end in one session: Wang et al. 1998 (8 pp.), Volkmann et al. 2024 (8 pp.),
Bist et al. 2023 (14 pp.). No page inaccessible, nothing truncated, no partial-read flags.
