# 03 · DP16 footpad — a scored decision that can't be failed

**Blocks:** LANE 1 (the calibration session).
**Decide together with:** [01 belt slope](01-belt-slope.md), [02 ammonia base](02-ammonia-base.md).

## What this is about, plainly

DP16 is one of the 24 scored decisions. It asks, in effect: *does the model keep the litter dry
enough to protect the hens' feet?* Footpad dermatitis — painful sores on the underside of the foot —
is one of the most common welfare problems in cage-free housing, so it deserves to be a question.

The problem is that right now, **the answer is the same no matter what the model does.** Measured at
DP16's deadline day, house H4 reads:

| What the model did | `footpad_severe_pct` | Band it lands in |
|---|---|---|
| Nothing at all | 16.32 | `marginal` |
| Serviced the manure belt on **every beat** of the cycle | 15.03 | `marginal` |

All four measured service regimes land in the same band. So the node scores `marginal` whether the
model is diligent or completely absent. It is a question with one answer — which means it
contributes nothing to distinguishing a good model from a bad one, while still counting as one of the
24 nodes averaged into the headline score.

**Why it's stuck:** the cap is structural, not a tuning problem. The effective belt interval can't go
below one day, so there is only about 1.3 percentage points of range available in the whole lever.
You cannot fix this by turning a coefficient up.

## An important thing to check before you decide

DP16's named lever is the manure belt. But the recent density wave made **stocking density** a strong
litter-moisture lever — much stronger than belts. Nobody has measured whether DP16 discriminates on
*density* even though it doesn't on belts.

**If it does, this decision mostly dissolves**: the node works, it just works through a different
lever than its name suggests, and the fix is to rename or re-describe it rather than re-engineer it.

That check is cheap — it's one measurement LANE 1 can do in minutes. **I'd ask for it before
committing to any of the options below.**

## Your options

### A. Accept that it's weak, and say so

Leave the node. State plainly in the writeup that DP16 does not discriminate on its named lever, and
why (the structural floor on belt interval).

**For:** Free. Honest. The node still records the state of the birds' feet, which is real information
even if it doesn't separate models.

**Against:** One of 24 nodes is dead weight in the headline average. Every model gets the same
partial credit there, which slightly compresses the differences between them.

### B. Move the bands so 15–16.3% straddles a boundary

Redraw the band thresholds so the range that exists produces different outcomes.

**For:** Cheap, and it makes the node discriminate immediately.

**Against:** This is the option I would push back on. You would be choosing welfare thresholds to
manufacture a scoring difference, rather than because they reflect where welfare harm actually
changes. A 1.3-point spread in footpad prevalence is not a meaningful welfare difference in the real
world, so a band boundary drawn through it would be reporting a distinction that doesn't exist. If
anyone audits the rubric, this is the finding they will lead with — and unlike decision 01, there is
no honest label that rescues it.

### C. Re-author the node around a lever with real range

Point DP16 at stocking density, or at a litter-drying lever if you take option C in
[decision 01](01-belt-slope.md).

**For:** Fixes it properly. The node measures something the model can actually move.

**Against:** Content work — the node's description, its discovery path, possibly corpus emails so the
agent can tell the lever exists. Days, not hours.

### D. Drop DP16 from `enabled_nodes`

Take it out. You'd run 23 nodes.

**For:** The most honest cheap option — a node that can't discriminate isn't measuring anything, so
removing it makes the headline average cleaner rather than diluted.

**Against:** You lose footpad coverage entirely, and footpad is a genuinely important welfare
outcome. It also looks like you dropped an inconvenient question, which is a bad look even when the
reasoning is sound.

## My recommendation

**Ask LANE 1 to check the density lever first.** Then:

- **If DP16 discriminates on density** → keep it, re-describe it so its named lever matches reality.
  Nearly free, and the node is genuinely fine.
- **If it doesn't** → **A** for now (accept, document), with **C** queued for the content pass.

I'd avoid **B** for the reason above, and avoid **D** because footpad matters too much to drop while a
real fix (C) is available.

## Questions to ask yourself

**1. Would I be comfortable explaining this band boundary to a vet?**
This is the test that rules out B. Under A your explanation is "the lever is too weak, we said so."
Under B it's "we drew the line there so the numbers would differ," which doesn't survive the
question.

**2. For my first demo, do I need every node to discriminate, or do I need the ones I point at to
discriminate?**
If you're demoing a handful of decisions in detail, a weak DP16 you don't feature costs you nothing —
choose A. If you're showing a full 24-node scorecard and inviting scrutiny, the dead node will be
noticed, and you want C.

**3. How much does one dead node out of 24 actually distort the headline?**
Each node is roughly 4% of the equal-weighted average, and a dead node gives every model the same
score there. So it compresses the spread between models by about that much. That is small — which is
why A is defensible — but it is not zero, and it compounds with DP21 (also N/A) and DP18 (excluded).
**Three non-discriminating nodes out of 24 is worth caring about as a group**, even if no single one
is worth a design wave.

**4. Is footpad's importance a reason to keep it or a reason to fix it?**
Both — which is exactly why A-then-C is the shape, rather than A forever.

## What to say to unblock

*"DP16: first measure whether it discriminates on stocking density rather than belt interval. If yes,
re-describe the node to match. If no, accept the weak node and document why — option A — and queue a
re-author for the content pass. Do not move the bands."*
