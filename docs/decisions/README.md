# Decisions waiting on you — 2026-08-05

Nine decisions, one file each. Written to be read cold, in plain language, with the tradeoffs
spelled out and questions you can answer yourself at the end of each.

## The single most important thing to understand first

**Three of these are one decision, not three.** The belt slope (01), the ammonia base (02) and DP16
(03) all feed the same chain:

```
belt interval → litter moisture → footpad damage AND ammonia
                                → every golden test file
                                → both reference artifacts (the "good" and "negligent" benchmarks)
```

Any one of them, decided on its own, forces a full regeneration of those files. Decided together,
one regeneration covers all three. Decided one at a time, you pay three times **and** each
regeneration invalidates the financial analysis the previous one produced.

So read 01, 02 and 03 together and answer them in one message. They come as two coherent packages:

| | 01 belt slope | 02 ammonia base | 03 DP16 | Cost | What you get |
|---|---|---|---|---|---|
| **Cheap package** | keep numbers, fix the citation | keep 4.2, drop the rationale | accept it's weak, say so | zero regeneration | Unblocked today. Three honest caveats on the record. |
| **Correct package** | keep numbers, fix the citation | re-base to 2.169 | move bands or accept | one regeneration | Ammonia is right. The brittle threshold goes away. |

My recommendation is the **correct package**, because the ammonia correction has a clear right
answer and, once you are regenerating anyway, it is the only one of the three that actually costs
something. Details and reasoning are in each file.

## Reading order

| # | Decision | Blocks | Reversible? |
|---|---|---|---|
| [01](01-belt-slope.md) | Belt-to-litter-moisture slope | LANE 1 — the critical path | Yes, cheaply |
| [02](02-ammonia-base.md) | Ammonia base: 4.2 or 2.169 | LANE 1 | Yes, at one regeneration |
| [03](03-dp16-footpad.md) | DP16 footpad: a dead node | LANE 1 | Yes |
| [04](04-staffing-and-stakeholders.md) | Staffing fork + who the eval is about | the staffing lane | Design-level, harder to undo |
| [05](05-dp20.md) | DP20: document it or drop it | part of node triage | Yes |
| [06](06-briefing-cost-target.md) | Apply the FY26 cost target to the briefing | a one-commit branch | **No** — invalidates run comparability |
| [07](07-financial-floor.md) | The $96.8M floor gap | nothing; a correctness claim | Yes |
| [08](08-which-demo.md) | Which demo you are aiming for | the whole schedule | Yes, but it re-plans everything |
| [09](09-housekeeping.md) | Two pushes and three archives | small | Yes |

**If you only have ten minutes:** answer 01, 02 and 03 as one batch. That unblocks the critical path
and everything downstream of it. The rest can wait a day without cost.

## One thing that is not a decision

You do not need to decide anything about the four branches that are only history now
(`feat/stocking-density`, `feat/stocking-density-task6`, `fix/model-params-finiteness`,
`fix/reference-policy-h6`). All four are provably contained in the calibration branch, all four are
pushed to origin, and they get deleted automatically when that branch merges. Nothing is at risk and
there is nothing to weigh.
