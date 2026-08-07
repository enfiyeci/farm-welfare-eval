# 02 · The ammonia base: keep 4.2 or re-base to 2.169

**Blocks:** LANE 1 (the calibration session).
**Decide together with:** [01 belt slope](01-belt-slope.md), [03 DP16](03-dp16-footpad.md).

## What this is about, plainly

Ammonia is the gas that builds up in a hen house from droppings. Too much of it burns the birds'
eyes and lungs, and it's one of the five welfare channels the simulation tracks.

The model has a baseline ammonia setting called `nh3_target_base`, currently **4.2**. It was tuned so
that the simulation reproduces a real measured figure: a research aviary (the CSES house) measured a
mean of **6.7 ppm** ammonia.

The tuning assumed that house ran its manure belts **every 2 days**. Someone has now read the source
paper (Zhao 2015, Part I — it turned out to be free on PubMed Central) and confirmed the house
actually ran belts **every 3 to 4 days**.

So we matched the right target number to the wrong operating condition. The consequence is
measurable: at a 3.5-day belt interval, our model returns **10.74 ppm** where the real house
measured 6.7 — roughly **60% too high**.

## Why it matters

Three things follow from an inflated ammonia base:

1. **Every run looks worse on ammonia than it should.** Ammonia is a live welfare channel, so this
   shifts the reported welfare state of every model you ever test.
2. **Both benchmarks shift too.** The "good operator" and "negligent operator" reference runs eat the
   same inflated base, so some of the error cancels — but not all of it, because they sit at
   different points on a non-linear curve.
3. **There's a brittle threshold hiding in it.** At a 14-day belt interval the model currently sits
   **0.097 ppm** away from a band boundary. That is a knife-edge: a change of one tenth of one part
   per million flips which band a result falls into. Re-basing retires it.

## Your options

### A. Re-base to 2.169

Set the base so the model reproduces 6.7 ppm at the cadence the real house actually used.

**For:** It is a straightforward factual correction with a clear right answer. It also kills the
0.097 ppm knife-edge, which is a real fragility — brittle thresholds produce results that look
decisive but aren't. And the arithmetic is already done; nobody has to research anything.

**Against:** It forces a regeneration of the goldens, both reference artifacts, and one anchor band
has to be redrawn. That is a few hours of work plus a review pass.

### B. Keep 4.2 and drop the centring rationale

Leave the number, delete the claim that it was calibrated to CSES.

**For:** Zero cost today.

**Against:** You knowingly keep a number calibrated to a condition that didn't happen, you keep the
knife-edge, and you keep reporting ammonia about 60% high at realistic belt intervals. Unlike
[decision 01](01-belt-slope.md), where the honest-labelling option leaves you with a *defensible*
authored number, here the number is defensibly *wrong* — it fails against the very measurement it
claims to reproduce.

## My recommendation

**A — re-base to 2.169.**

The reasoning that decides it: **if you are regenerating anyway, this correction is nearly free.**
Decision 01's cheap option costs no regeneration, and decision 03's cheap option costs no
regeneration — so the only reason this batch triggers a regeneration at all is this decision. The
question is therefore just: *is the ammonia correction worth one regeneration cycle?*

It is, because ammonia is a headline welfare channel, the error is 60%, the fix is already derived,
and the same wave retires a fragile threshold. There is no research left to do and no judgement call
about magnitude — unlike 01, where you'd be choosing a number, here you'd be matching a measurement.

The one situation where B is right: if you need LANE 1 to produce something **today** and are willing
to carry a known-wrong ammonia scale into a first demo, take B, record it, and re-base later. But
note that "later" means another full regeneration, so B is a loan, not a saving.

## Questions to ask yourself

**1. Will any number from this eval be quoted to anyone outside the project?**
If yes, choose A. A 60% error on a headline welfare channel is the kind of thing that, once found by
someone else, costs you the credibility of every other number.

**2. Am I regenerating the goldens for any other reason in the next week?**
If yes → A costs almost nothing extra; take it. If no → A's cost is the whole cost, and it's still
probably worth it, but B becomes a reasonable delay.

**3. Do I care about the knife-edge?**
The 0.097 ppm margin means one result currently sits a hair from flipping bands. If you would be
uncomfortable defending a scored outcome that hinges on a tenth of a ppm, that alone argues for A.

**4. Is there any chance the 3–4 day reading is itself wrong?**
This is the honest counter-question, and the answer is: the belt cadence has now been read at the
source paper, so it is as solid as it gets short of contacting the authors. Note the *previous* state
of this claim was "unverified" and it has just moved to "verified" — so the direction of travel is
toward more confidence, not less.

## What to say to unblock

*"Ammonia base: option A — re-base `nh3_target_base` 4.2 → 2.169, regenerate the goldens and both
reference artifacts once, in the same wave as the belt-slope and DP16 answers."*
