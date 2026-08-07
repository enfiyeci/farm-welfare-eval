# 07 · The $96.8M gap in the reported "worst case"

**Blocks:** nothing. This is a correctness claim, not a gate.
**Related:** [04 staffing](04-staffing-and-stakeholders.md) — the gap runs through the staffing lever.

## What this is about, plainly

The eval reports a **financial floor**: the worst possible money outcome, the number that says "no
strategy in this world loses more than this." It's used as a bound — a way of saying how much money is
actually at stake in the decisions the model faces.

The code that finds that floor (`floor_absolute`) searches only two levers: **ventilation and
temperature**. It doesn't search staffing. And there is a reachable staffing strategy — understaffing
— that lands roughly **$96.8 million below** the number currently reported as the floor.

So the reported floor is not the floor. It's the floor *of a two-lever search*, presented as if it were
the floor of everything.

The module's docstring doesn't say that. It presents the number without the caveat.

## Why it matters, and how much

**It matters because a bound that isn't a bound is worse than no bound.** If you ever say "the largest
financial stake in this eval is $X," and someone finds a strategy $96.8M worse, the claim collapses —
and so does confidence in the surrounding numbers.

**It matters less than the size suggests**, for two reasons. First, nothing in the *scoring* depends on
the floor — it is a reported reference figure, not an input to any node score or the headline. Second,
$96.8M is a wildly unrealistic outcome; it's what you get by pushing a lever to a corner no plausible
operator would go near. That's exactly what a floor is *for*, but it means the number is a theoretical
bound rather than a business scenario either way.

So: a real correctness defect, in a number that is presented but not load-bearing.

## Your options

### A. Fix the search — add staffing to `floor_absolute`

Extend the search to include the staffing lever so the reported floor is actually the floor.

**For:** The number becomes true. It's a bounded piece of work — you're adding one dimension to an
existing search, not designing anything new.
**Against:** It changes a reported figure, so both financial analyses get regenerated, and anything
quoting the old floor needs updating. Also: adding one lever raises the obvious question of whether
*other* unsearched levers hide deeper corners, which you'd want to answer rather than leave hanging.

### B. Fix the claim — document the limitation

Leave the search. Change the docstring and the analyses to say plainly: this is the floor over
ventilation and temperature, and a deeper corner exists via staffing, approximately $96.8M lower.

**For:** Cheap, honest, and immediately removes the misleading claim. The number stays useful for what
it actually is.
**Against:** You knowingly ship a "floor" that isn't one, relying on a caveat being read. Caveats get
dropped when numbers get quoted.

### C. Stop reporting an absolute floor

Report the operating floor (the realistic worst case) and drop the absolute one.

**For:** Removes the problem at the root. Arguably the absolute floor was never the interesting number
— a $96.8M theoretical corner tells you less about the eval than the realistic range does.
**Against:** You lose the bound entirely, and bounds are genuinely useful for saying how much is at
stake.

## My recommendation

**B now, A when the staffing lane runs.**

Reasoning: the defect is that the docstring over-claims. Fixing the sentence takes minutes and removes
the misleading part today. Fixing the search properly belongs with the staffing work anyway — the same
session will already be measuring that lever, so it can extend the search while it's in there, and you
avoid touching the financial analyses twice.

This is the one decision here where the cheap option and the proper option genuinely compose instead of
competing: B is not a substitute for A, it's the honest holding position until A is convenient.

I'd only pick C if you find you never actually use the absolute floor for anything — worth checking
where it's quoted before deciding.

## Questions to ask yourself

**1. Do I quote the absolute floor anywhere someone would rely on?**
If it appears in a report, a deck, or a paper draft, fix the claim today (B) and the search soon (A).
If it exists only in an internal analysis nobody reads, this drops to housekeeping.

**2. Is "the floor over these two levers" a number I actually want?**
If yes, B is a complete answer and A is optional. If you want "the floor, full stop," only A gives you
that — and then you should also ask which levers *remain* unsearched, because the same argument will
apply to them.

**3. How many levers are there in total?**
Worth asking the staffing session. If it's ventilation, temperature, staffing and a couple more, then A
is nearly complete once staffing is in. If there are a dozen, then a true absolute floor may not be
computable and C becomes the honest answer.

**4. Does anything score off this number?**
No — I checked; it's reported, not scored. That's what makes it safe to hold at B for now rather than
treating it as urgent.

## What to say to unblock

*"Financial floor: option B now — correct the docstring and both analyses to say it's the floor over
ventilation and temperature only, and name the ~$96.8M staffing corner. Then fold option A into the
staffing lane, and tell me how many levers remain unsearched."*
