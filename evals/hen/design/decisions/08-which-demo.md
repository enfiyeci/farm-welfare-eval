# 08 · Which demo are you aiming for

**Blocks:** nothing directly. Shapes the schedule of everything else.
**This is the decision that changes how much the other eight matter.**

## What this is about, plainly

There are two very different things you could show, and they have different requirements. Deciding
which one you're building toward tells you how much of the rest of this list you actually need.

### Demo 1 — the mechanism

You show the eval *working*. A model plays the farm across a full flock cycle. You watch it live on the
Henhouse spectator dashboard — mail arriving, tool calls with costs, the welfare state of each house
moving. You point at three or four decisions and explain what the model did and how the judge graded it.

**What this needs:** the merges done, the calibration wave landed, and a run to show. That's roughly
where you already are.

**What it does NOT need:** human labelling, an out-of-family grader, or every node discriminating.

### Demo 2 — the result

You show a *finding*: model A treats animals better than model B, on this axis, by this much, and here
is why you should believe the number.

**What this needs, on top of Demo 1:**
- **An out-of-family grader.** The current 6.804 anchor is Gemini judging Gemini. Your own notes flag
  this as a bias to remove or measure before any cross-model claim.
- **The judge-validation gate.** Hand-labelled transcripts, and a Spearman correlation between the
  judge's scores and a human's. The labelling pack exists (`docs/expert-labeling-pack.md`); no labels
  have been filled in.
- **The eval-awareness gate.** A separate instrument: 15 blind sheets, 120 cells, needing Cohen's κ ≥
  0.6. Its own guide states that until that passes, no probe output is trustworthy. Also unfilled.
- **Nodes that discriminate.** DP18 is excluded, DP21 resolves N/A, DP16 doesn't discriminate, DP20 may
  not. A comparison resting on 20 working nodes out of 24 needs to say so.
- **At least two or three models run over the same world.**

## The honest gap between them

Demo 1 is **weeks** away — mostly the calibration wave plus a run.

Demo 2 is **considerably further**, and the long pole isn't engineering. It's that **someone has to sit
down and hand-label transcripts** — ideally a vet or welfare specialist, because the whole point of the
gate is that a domain expert agrees with the judge. That is the only item on any of these lists that
needs a person who isn't you and isn't a model.

## Why this decision matters more than it looks

Almost every other decision here changes weight depending on your answer:

| Decision | Under Demo 1 | Under Demo 2 |
|---|---|---|
| [02 ammonia base](02-ammonia-base.md) | nice to fix | **must** fix — you'd be quoting the number |
| [03 DP16](03-dp16-footpad.md) | fine to accept as weak | needs to work, or be excluded and declared |
| [05 DP20](05-dp20.md) | fine undocumented | **must** be documented — labellers grade from the deck |
| [06 briefing target](06-briefing-cost-target.md) | apply whenever | must be settled **before** the anchor pilot |
| [07 financial floor](07-financial-floor.md) | document the caveat | fix the search |

So answering this one first makes five of the others easier.

## Your options

### A. Aim for Demo 1, and treat Demo 2 as the next milestone

Get something real and watchable in front of people soon. Be explicit that the numbers are provisional
and the validation gates are pending.

**For:** Achievable on a known timeline. Shows the hard part — that a static, deterministic world can
produce genuine welfare decisions — which is the actual bet this project makes. And a watchable demo is
persuasive in a way a table of numbers isn't.

**Against:** You cannot make a claim about any model's welfare behaviour. Someone will ask "so which
model is kindest?" and the answer has to be "we can't say yet."

### B. Hold until Demo 2 is ready

Don't show anything until the numbers are defensible.

**For:** The first thing anyone sees is a real result with real backing.
**Against:** Much longer, gated on expert labelling time you don't control, and you get no feedback in
the meantime. You also risk building toward a result while a design flaw sits undiscovered — exactly
what a demo would surface.

### C. Demo 1 now, with the validation gates shown as an explicit roadmap

Same as A, but you present the pending gates as part of the story: here is the instrument, here is what
it takes to trust it, here is where we are on that.

**For:** Honest, and it turns the missing validation from a weakness into evidence of rigour. For an
alignment eval, "here is how we'd know if our judge is wrong" is a strength, not an admission.
**Against:** Requires you to be comfortable presenting unfinished work.

## My recommendation

**C.** Show the mechanism soon, and be explicit that the validation gates are the difference between a
demo and a result.

Reasoning: the risky, novel claim in this project is that a *static, pre-authored, deterministic* world
can elicit real welfare decisions from a model — that is the bet written into the architecture. Demo 1
tests that bet and gets you feedback on it. Waiting for Demo 2 means waiting on expert scheduling
before you've validated the premise, which is the wrong order of risk.

And the spectator dashboard exists as of today. The thing that makes Demo 1 compelling is already built.

## Questions to ask yourself

**1. Who is the audience, and what would convince them?**
A funder or collaborator usually wants to see the instrument work and understand what it will show. A
reviewer wants the result. Answer this and the rest follows.

**2. Do I have a vet or welfare specialist who could label transcripts, and when?**
This is the real gate on Demo 2. If you don't have a name, Demo 2 has no date, and planning for it is
planning against an unknown. Finding that person is the highest-leverage thing you could do for the
Demo 2 timeline — and it's independent of every engineering task, so it can start now.

**3. Am I comfortable saying "we don't know yet" out loud?**
If yes, C is strictly better than A — same work, more credibility. If it would undermine the
conversation you need to have, A.

**4. What happens if the demo reveals a design flaw?**
Under A or C, you find out early and cheaply. Under B, you find out after investing in validation of a
possibly-flawed instrument. This asymmetry is the strongest argument against B.

## What to say to unblock

*"Aiming for the mechanism demo (option C) — show the eval working with the validation gates presented
as an explicit roadmap. Treat the labelling gates as the Demo 2 milestone, and I'll work on finding a
labeller in parallel."*
