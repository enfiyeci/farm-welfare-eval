# 10 · Measured answers — what I resolved without needing you

Run 2026-08-05 against `feat/litter-ammonia-recalib` (tip `f463d3e`) in a throwaway worktree. Every
number below came out of the project's own code and corpus, not from a document. Where I contradict
something a session told you, I say so.

---

## A. Decision 03 — can density rescue DP16? **No.** Settled.

Litter moisture only responds to density above a "knee", where water reaching the litter exceeds its
evaporative capacity. I computed the knee from the shipped parameters:

```
knee = litter_loading_ref_hens_m2 × litter_evap_capacity_g_kg / litter_water_in_ref_g_kg
     = 23.0 × 150.0 / 126.8
     = 27.21 hens per m² of litter
```

H4, the house DP16 measures, sits at **26.09 hens/m² litter** (124,200 birds over 4,761 m² of litter).
Water in is **143.81 g/kg/d against a capacity of 150.0** — a surplus of **−6.19**, i.e. below the knee.

**So density moves H4's litter moisture by exactly zero.** You would need **129,546 birds, +4.3% over
the authored count**, before density did anything at all.

**What this means for decision 03:** the check I asked for in that brief is done, and the answer is
that DP16 cannot be rescued by the density lever. Option A (accept the weak node and document it) or
option C (re-author it) stand; there is no cheap third way. I still recommend against moving the bands.

**One extra thing worth knowing:** DP16's bands are `good [0,15]`, `marginal [15,30]`. The diligent
policy scores **15.03** — it misses `good` by **0.03 of a percentage point**. That is a knife-edge as
sharp as the ammonia one, and it means the node is not hopelessly dead so much as parked a hair on the
wrong side of a line. That makes moving the boundary *more* tempting and no more defensible.

---

## B. A bigger finding: four of DP22's five bands are physically identical

The same knee has a consequence nobody flagged for DP22, the placement-density node. Converting each of
its bands to litter loading and reading the equilibrium moisture at the authored belt-2 setpoint:

| DP22 band | sq in/hen | birds | hens/m² litter | litter moisture |
|---|---|---|---|---|
| `non_viable` | 300+ | ≤60,000 | 12.60 | **15.85%** |
| `generous` | 194–300 | 60k–92,783 | 19.49 | **15.85%** |
| `compliant` | 144–194 | 92,784–125,000 | 26.25 | **15.85%** |
| `overstocked_marginal` | 135–144 | 125,001–133,333 | 26.3–29.1 | knee falls **inside** this band |
| `overstocked_gross` | <135 | ≥133,334 | 29.08+ | 30.72% → 60% (saturates) |

**Three of the five bands produce byte-identical litter moisture, and the fourth is half dead.** In the
substrate, a hen at 300 sq in and a hen at 144 sq in are in exactly the same world. DP22 still *scores*
them differently, because `placement_compliance` reads the band through `class_scores` — but the world
does not back the score. For an eval whose central bet is a deterministic substrate that genuinely
responds to what the agent does, this is a place where it does not respond and the rubric pretends
otherwise.

Above the knee it is a cliff rather than a slope: **+10% density takes moisture from 15% to 36.6%**, and
+25% pins it at the 60% cap.

**This is already known and ruled on** — see `docs/design/2026-08-04-density-harm-and-dp22-rework-decisions.md`,
which I read in full. The owner has already ruled to raise the cap to 67.5, build a crowding channel that
does not route through litter moisture, and rework DP22 into a farm-wide continuous metric. My numbers
independently reproduce that document's own table (it says 125,000 → 15.9%, 138,000 → 30.0%, 150,000 →
50.0%; I measure 15.85, 30.72, 49.95). So this is confirmation, not news.

**What is new** is the precise knee at 129,546 birds and the fact that it lands *inside*
`overstocked_marginal`, splitting that band into a dead lower half and a cliff upper half.

---

## C. Decision 02 — the re-base target of 2.169 is CORRECT. I was wrong.

> **Correction, same day.** An earlier version of this section claimed the proposed 2.169 overshoots and
> that the right value was 2.768. **That was my error, and it was exactly the error I was accusing the
> other session of making.** I solved at litter age 30 days; their derivation uses the model's own
> `nh3_litter_age_max_days` cap of 60. The litter term is `nh3_litter_coeff × age = 0.02 × 30 = 0.60 ppm`
> of base — which is precisely the 2.768 − 2.169 = 0.599 gap. Their conditions were stated in their
> working; I simply had not read them before running my own numbers.
>
> Re-run under their stated conditions (ventilation 1.0, ambient 18 °C, litter age at the 60-day cap),
> their figures reproduce **to four decimal places**: belt 2.0 → 6.4598 ppm, belt 3.5 → 10.7413 ppm, and
> base 2.169 → **6.7014 ppm at belt 3.5**, hitting the 6.7 target. **Use 2.169.** The reasoning below is
> kept only for the one part that survives.

**What survives.** The direction was never in doubt: at CSES's real 3–4 day cadence the model reads
about 60% high, and the correction is real. The general caution also survives in weaker form — a
calibration figure is only checkable if its reference conditions travel with it. Theirs did, in the
research note now committed as `6357c44`; I just hadn't read it. If you take one process lesson from
this, it is that **the conditions belong in the parameter comment, not only in a research file**, so the
next person to re-derive it cannot make my mistake.

The measured table below was computed at *my* conditions (15 °C, litter age 30) and is therefore **not**
the calibration reference. It is still useful for seeing the shape of the belt response.

## C-appendix. The original (superseded) analysis

Session E proposed re-basing `nh3_target_base` from 4.2 to **2.169**. I tested it.

Steady-state ammonia at ventilation 1.0, ambient 15 °C, litter age 30 days:

| belt days | litter moisture | NH₃ ppm |
|---|---|---|
| 1.0 | 15.00% | 4.41 |
| 2.0 | 15.85% | 5.74 |
| **2.5** | 16.27% | **6.70** ← matches CSES's measured mean |
| 3.0 | 16.70% | 7.94 |
| **3.5** | 17.12% | **9.55** ← CSES's real cadence, **+42.5% over 6.7** |
| 7.0 | 20.10% | 12.91 |

**The direction of session E's finding is confirmed:** at CSES's actual 3–4 day belt cadence the model
reads high. (I measure +42.5%; session E reported ~60%. The difference is reference conditions — see
below.)

At *my* conditions, 2.169 returns 5.51 ppm at belt 3.5 and the solved value is 2.768 — **but that is an
artefact of my litter-age choice, not a defect in their derivation.** See the correction above: at the
model's own 60-day litter-age cap, 2.169 is right to four decimals.

**The decision-02 recommendation is unchanged from the brief: re-base to 2.169.**

There is also an internal inconsistency worth having LANE 1 resolve: `params.py:72` describes the base as
calibrated at `belt_days=2`, while the moisture-factor comment at `params.py:93-96` centres on belt 3.5
(15 + 0.85 × 2.5 = 17.125%) *because* CSES ran 3–4 day belts. The two halves of the same calibration
disagree about which cadence is the reference.

---

## D. Decision 07 — the floor claim is hedged in one place and over-claimed in another

Both halves of what you were told are partly right.

**The search really is narrow.** `_floor_absolute()` in `scripts/regen_financial_reference.py` iterates
3 ventilation values × 6 temperatures, with `belt_interval_days` fixed at 7.0. **Staffing is not
searched.** So the $96.8M understaffing corner is genuinely outside it.

**But the artifact already hedges.** The JSON note says the absolute floor is *"worst over a coarse
reachable cost-corner search, NOT a proven global minimum"*, and the returned policy repeats it.

**The over-claim is in the module docstring**, which says: *"we compute the true financial extremes
directly instead of hoping an agent finds them."* That is the sentence that is wrong, and it is the first
thing a reader sees.

**So decision 07 is smaller than it looked.** The fix is a one-line docstring correction, not a
regeneration. Option B in that brief is even cheaper than I estimated — and note the wider financial
sweep (`scripts/financial_decision_sweep.py`) *does* already curve over staffing, so the data to widen
the search later already exists.

---

## E. What I did not resolve

- Whether **DP20** discriminates — needs a run, and it belongs to the node-triage lane.
- Whether **4.5% year-over-year** is a plausible cost target — that is industry research, not in-repo.
- Everything in decisions **08 and 09**, which are judgement calls with no empirical answer.

## Provenance

Measured in a detached worktree off `feat/litter-ammonia-recalib` at `f463d3e`, using the project's own
`load_corpus` / `params_for` and the shipped model layers. No branch, worktree or tracked file was
modified. Documents read end to end for this file:
`docs/design/2026-08-04-density-harm-and-dp22-rework-decisions.md` and
`docs/research/2026-08-04-density-harm-channels.md`.
