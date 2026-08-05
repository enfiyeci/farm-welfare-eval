# Zhao 2015 Part I read at source — the cadence is confirmed, and it convicts `nh3_target_base`

**Date:** 2026-08-05 · **Branch:** `feat/litter-ammonia-recalib` · **Status:** finding recorded, no code changed

Settles the open question escalated in the **Task 6 review record** of
`docs/plans/2026-08-03-litter-ammonia-footpad-recalibration.md`. That record said the ammonia centring
`nh3_moisture_ref = 17.12 %` rested on an unverified fact — CSES's manure-belt cadence — and flagged that
nobody on the wave had read the source. It has now been read.

**The premise is confirmed. The centring is not the defect. `nh3_target_base` is.**

---

## 1. The source, and what it says

[Zhao, Shepherd, Li & Xin 2015, "Environmental assessment of three egg production systems – Part I:
Monitoring system and indoor air quality", *Poultry Science* 94(3):518–533](https://doi.org/10.3382/ps/peu076).
**Open access on PubMed Central** — [PMC4990888](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/) — so this
one never needed to be requested. Also on [Oxford Academic](https://academic.oup.com/ps/article/94/3/518/1522659)
and [PubMed 25737567](https://pubmed.ncbi.nlm.nih.gov/25737567/).

Verbatim on the aviary's manure handling:

> "Manure belts were installed in all hen colonies to remove manure out of the house **every 3 to 4 d**,
> while the manure deposited/accumulated on the litter floor was only removed at the end of each flock."

The conventional cage and enriched colony houses ran the same 3-to-4-day cadence.

Indoor ammonia, 27-month monitoring across two single-cycle flocks (June 2011 – May 2012, July 2012 –
August 2013):

| House | Mean NH₃ | 95 % CI |
|---|---|---|
| **Aviary** | **6.7 ppm** | 6.2 – 7.2 |
| Conventional cage | 4.0 ppm | 3.8 – 4.2 |
| Enriched colony | 2.8 ppm | 2.7 – 3.0 |

**The paper does not report litter moisture or litter dry matter for the aviary.** That matters — see §4.

The 3-to-4-day figure was already in this repo at
`docs/research/2026-08-03-nh3-moisture-decomposition.md:196`, which even notes it is "not 2". What was
missing is the consequence below; the access table there is updated by this commit from PARTIAL to read.

## 2. The consequence: the base is calibrated at the wrong belt interval

`nh3_target_base = 4.2` was tuned so that a **2-day** belt returns the CSES aviary's measured 6.7 ppm.
CSES's aviary ran **3–4 day** belts. Measured against the real code at mild baseline
(ventilation 1.0, ambient 18 °C, litter age at its 60-day cap):

| Belt interval | Model NH₃ | Note |
|---|---|---|
| 2 d (our corpus default) | **6.4598 ppm** | inside the 5.0–8.5 anchor band — but this is not CSES's cadence |
| **3.5 d (CSES's actual cadence)** | **10.7413 ppm** | **~60 % above the 6.7 ppm the paper measured**, and outside the band |

`f_MAT(3.5) = 1.98874` against `f_MAT(2) = 1.2586`, and that ratio is the whole discrepancy. This is the
same class of error the wave was built to remove — **a number carried without its operating point** — sitting
in the one coefficient every other ammonia figure is anchored to.

## 3. What re-basing would cost, measured

To make the model reproduce 6.7 ppm at CSES's own cadence:

```
nh3_target_base = 6.7 / f_MAT(3.5) − nh3_litter_coeff × nh3_litter_age_max_days
                = 6.7 / 1.98874 − 0.02 × 60
                = 2.169          (currently 4.2)
```

Downstream, at mild baseline:

| Belt | Now (base 4.2) | Re-based (base 2.169) |
|---|---|---|
| 2 | 6.4598 | **4.0302** — below the current 5.0 anchor floor, so the band must be redrawn |
| 3.5 | 10.7413 | **6.70** — matches the source, by construction |
| 7 | 14.5210 | 9.0594 |
| 14 | 18.4230 | **11.4938** |

**A side benefit worth weighing.** Belt 14 currently clears Hinz's measured 18.52 ppm aviary maximum by
only **0.0970 ppm**, a margin that depends on rounding the sourced 0.40 %/(g/kg) down to exactly 0.0040
(the largest coefficient that still passes is ~0.004059). Re-basing retires that knife-edge entirely.

**The cost:** every ammonia value in the episode drops, so the goldens and both reference artifacts
regenerate again, and `test_baseline_aviary_mean_near_6_7`'s band has to be re-drawn around a different
operating point.

## 4. This is COUPLED to the belt-slope question — do not decide it alone

`nh3_moisture_ref = 17.12 %` is not read from Zhao. It is derived by pushing CSES's 3.5-day cadence
**through this model's own belt curve**: `15 + 0.85 × 2.5 = 17.125 %`. Zhao reports no litter moisture at
all, so the belt curve is the only bridge from cadence to moisture.

That bridge is exactly what
`docs/research/2026-08-04-groot-koerkamp-ch7-table4-at-source.md` undermines: Ch. 7 Table 4's endpoints are
**inverted by treatment**, and the belt→moisture direction is unsupported. So:

- If the belt slope changes, **17.12 % changes with it**, and the re-base target changes again.
- Deciding the ammonia base before the belt slope means computing 2.169 twice.

Two independent reads (this session's and `da9ae39`'s) agree the belt slope is the upstream question. The
belt slope, the ammonia base and DP16's banding should be ruled on **as one batch, then regenerated once**.

## 5. The residual fork, stated plainly

Either operating point can be defended; the current state defends neither, because it centres the moisture
factor at CSES's cadence while anchoring the base at our default cadence.

- **(a) Keep base 4.2.** The claim becomes "our default-managed house sits at the measured aviary mean",
  which is a legitimate modelling choice — but then the centring's own stated reasoning ("centred where the
  base was calibrated") points at belt 2's **15.85 %**, and 15.85 puts belt 14 at **19.3830 ppm**, breaking
  Hinz's 18.52 measured ceiling. Option (a) therefore requires *dropping the centring rationale*, not just
  keeping the number.
- **(b) Re-base to 2.169.** Internally coherent, matches the source at the source's own operating point,
  and retires the belt-14 knife-edge. Costs a regeneration and a redrawn anchor band.

## 6. Coverage

- ⚠️ **Zhao 2015 Part I: NOT read end to end.** Read the manure-handling description and the indoor
  air-quality results (ammonia means and confidence intervals for all three houses) plus the monitoring
  period. The monitoring-system methods, the particulate-matter and CO₂ sections, and every figure were not
  read. The two claims this note rests on — the 3-to-4-day cadence and the 6.7 ppm aviary mean — are quoted
  above.
- ⚠️ Part II (*Poultry Science* 94(3):534–543) and Part III were **not** consulted. If the aviary's litter
  moisture is reported anywhere in the series it would most likely be there, and it would replace the belt
  curve as the bridge in §4 — worth checking before acting on §3.
- All model figures in §2 and §3 were computed from the real code in this session, not carried from the plan.
