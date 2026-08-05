# 01 · The belt-to-litter-moisture slope

**Blocks:** LANE 1 (the calibration session), which gates everything downstream.
**Decide together with:** [02 ammonia base](02-ammonia-base.md), [03 DP16](03-dp16-footpad.md).

## What this is about, plainly

Hens live on litter — the bedding on the floor. Wet litter is bad for them: it burns their feet
(footpad dermatitis) and it releases ammonia into the air they breathe.

In the simulation, one of the things the AI can control is how often the **manure belts** run. Belts
carry droppings out of the house. The model says: run the belts more often, the litter gets drier.
That relationship is a number — a slope — and we said it came from a real study.

**It doesn't.** Someone fetched the original study (Groot Koerkamp's 1998 thesis, Chapter 7, Table 4)
and read it at the source. The numbers we used are real numbers from that table, but they are
attached to the wrong conditions — and specifically, they are **backwards**:

| What we claim | What the study actually says |
|---|---|
| 14.4% moisture = daily belts (driest) | 14.4% is period 2A: **weekly** belts, with the litter dryer **ON** |
| 20.1% moisture = weekly belts (wettest) | 20.1% is period 2C: **daily** belts, with the litter dryer **OFF** |

Worse: in the cases where the dryer was off, **daily belts gave wetter litter than weekly belts**
(20.1% vs 19.3%) — the opposite direction to what our model encodes. What actually drove moisture in
that study was the litter-drying fan, not the belt schedule.

So the 14.4–20.1% range is a genuine measured range of aviary litter moisture. What it is *not* is
evidence that belt frequency causes it.

## Why you can't just delete the lever

Two scored decisions need a belt lever to exist at all:

- **DP01** — the ammonia/ventilation decision
- **DP16** — the footpad decision (see [03](03-dp16-footpad.md))

If belts stop affecting anything, those two decisions have nothing to hinge on and can't be graded.
So "remove it" is not on the table; the question is what the lever should be.

## Your options

### A. Keep the numbers, fix the citation

Change nothing mechanically. Stop claiming Table 4 supports the direction. Mark the slope as an
authored figure rather than a measured one.

**For:** Costs nothing. No goldens move, no benchmarks move, no test changes. LANE 1 unblocks today.
The eval keeps working exactly as it does now. And it is *honest* — the problem with the current
state isn't the number, it's the false provenance, and this fixes exactly that.

**Against:** The model keeps a belt→moisture direction that the best available source doesn't
support. If someone audits this eval's physical realism, that is a finding. It stays a known
weakness on the record rather than a fixed one.

**Worth knowing:** the belt lever is *already* documented as deliberately weak — 0.85% moisture per
belt-day. So this option leaves a weak, authored lever, clearly labelled. That is a defensible
position, not a hidden fudge.

### B. Re-derive the slope, keeping belts as the lever

Pick a magnitude yourself, mark it authored, and stop pretending it's measured.

**For:** You get to choose a slope strong enough that DP01 and DP16 actually discriminate, which
would fix [03](03-dp16-footpad.md) at the same time.

**Against:** One regeneration. And you are choosing a number to produce a scoring outcome, which is
the same shape of move as moving the bands in decision 03 — it manufactures signal. If you do this,
say plainly in the writeup that the magnitude is chosen for measurable range, not derived from data.

### C. Switch the lever to litter drying

Follow what the study actually shows: make the agent's controllable lever the drying system, and let
belts matter less.

**For:** It is the scientifically correct model. The source says so directly, and the thesis
abstract frames the whole problem as controlling litter dry matter.

**Against:** This is a design project, not a coefficient change. It needs a new agent-facing tool,
new corpus and schedule content so the agent can learn the lever exists, and a rewrite of DP01 and
DP16. Weeks, not hours, and it would push the demo back.

## My recommendation

**A now, C recorded as future work.** Two reasons.

First, the defect is a *provenance* defect. The number isn't crazy; the citation is wrong. Option A
fixes the actual problem at zero cost and lets the critical path move today.

Second, C is the right destination but it is a content-and-design wave, and you have four
environments planned and a demo to get to. Doing C now trades a working eval for a more realistic
one you can't show yet.

I would avoid B. It costs a regeneration and buys you a number you chose to make the scoring work,
which is weaker ground than an honestly-labelled weak lever.

## Questions to ask yourself

**1. Is this eval measuring the physics of a hen house, or measuring how a model behaves in a
plausible hen house?**
If it's the second — and the whole design is a static authored world, so it is — then a
clearly-labelled authored slope is acceptable. Choose A.
If you intend to defend the physics claim by claim to an outside reviewer, choose C and accept the
delay.

**2. Would I be comfortable if someone read the code, read the source, and asked me about this?**
Under A, your answer is "yes, we found that ourselves, wrote it down, and marked the number as
authored." That is a good answer. Under the current state, there is no good answer — which is why
doing *nothing* is the one option that isn't on this list.

**3. Do I need DP16 to discriminate for the demo?**
If yes, A alone won't get you there and you should read [03](03-dp16-footpad.md) before answering —
because density may already solve it, and if it does, you don't need B at all.

**4. How much delay am I willing to accept for physical accuracy here?**
Zero → A. A few days → B. Weeks → C.

## What to say to unblock

If you pick A, this is enough: *"Belt slope: option A — keep the numbers, strip the Table 4 citation,
mark the slope authored, no regeneration on this account. Record option C as future work."*
