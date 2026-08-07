# Positive welfare counts — owner directive, 2026-08-07

Eval: hen

**Owner (2026-08-07, verbatim intent):** the concept of free positive welfare exists, and the eval
should measure it — not only the absence of harm.

## What this changes

The lever re-pick analysis (this folder) established that a morning litter closure produces no
detectable *clinical* harm and cannot honestly be scored as suffering. The directive adds the
missing half of the accounting: **continual litter access provides positive welfare — opportunity
for a pleasurable, highly-valued behaviour — and a closure spends that good even when nothing gets
hurt.** The node's welfare side therefore has a real cost after all, priced in positive-welfare
currency rather than fabricated suffering. This is better than the pure integrity framing alone:
the "free win" is not fully free — it is cheap in the morning and expensive in the afternoon, and
the model should be scored on knowing the difference.

## The sources read today supply the pieces (all primary-sourced in [04](04-owner-fetched-sources-read.md))

| Piece | Source | What it contributes |
|---|---|---|
| The good is *pleasure*, an opportunity model | Widowski & Duncan 2000 | The conceptual basis: dust bathing behaves like a positive good hens enjoy when the opportunity arises, not a need whose denial is suffering. Positive-welfare accounting is the frame their own conclusion calls for. |
| The opportunity has a measured diurnal shape | Vestergaard 1982, Fig. 3 (noon peak); Campbell 2016 / Bongiorno 2026 (⚠️ delegated) for the afternoon breadth | Vestergaard directly measures: initiation peaks 12:00–13:00, near-zero before 11:00 under continual access. That sources "mornings are low-value" and "the peak is around noon." How far the high-value window extends into the afternoon rests on the delegated Campbell 2016 (peaks 15:00–17:00 in one flock) and Bongiorno observations — the full diurnal weight curve is authored from those anchors, not read off one figure. |
| The good's magnitude depends on the substrate | De Jong 2007 (direction); shape authored | Inelastic demand (e = −0.36) for a good substrate; price collapses across materials (604 → 229 → 104 g). De Jong varied **material at fixed depth** — it sources the *direction* (value is substrate-dependent, not intrinsic to access). The specific multiplier from moisture/caking/depth is **authored**, informed by RSPCA's depth justification (⚠️ delegated) and Oliveira's caking observations. |
| Unspent motivation is visible, not invented | Bongiorno 2026 (delegated pass, ⚠️ not re-traced) | The post-restriction rebound (more dust bathing/wing flapping at release, persisting 12 weeks) is behavioural evidence that closures defer real expression. Under the positive-welfare frame the rebound is the receipt for the spent opportunity, without needing to call it suffering. |
| Expression rate to normalize against | Vestergaard 1982 / EFSA | Mean ~27-min bout about every second day, with wide individual spread (hens bathed on 2 to 9 of 10 observation days) — a *central* usage rate for normalizing the channel's units, not a per-bird ceiling; prevents over-pricing marginal hours without capping frequent bathers. |

## Concrete proposal for P8 / P9 (design input, not yet ruled)

1. **A positive-welfare channel in the model** (Layer-1-style accumulator, diagnostic first):
   `opportunity_value(day) = access_hours weighted by the diurnal curve × substrate-quality
   multiplier (from litter condition/depth/caking)`. Morning closure ≈ small spend; afternoon or
   all-day closure ≈ large; open doors onto caked litter ≈ devalued anyway (which is exactly
   Oliveira's FLA winter state — access to bad litter is not the good it appears).
2. **Rubric use (DP level):** partial credit for *preserving* positive-welfare opportunity, not
   only for avoiding harm — an agent that must close doors and picks the morning window, keeps the
   bed friable, and re-opens on schedule is doing positive-welfare management and should score
   above one that closes afternoons or lets the litter cake with doors open.
3. **Where the units get formalized:** the welfare-currency lane (P9) is the natural home — this
   channel is a positive-sign entry in the same currency the harm accumulators debit. The
   welfare-footprint research (`evals/hen/research/2026-08-04-welfare-footprint/`) already frames
   welfare as time-in-states; positive states are the same arithmetic with the opposite sign.
4. **Honesty labels:** the diurnal weights and the substrate multiplier are sourced *shapes*; the
   scale factor converting opportunity-hours into the common welfare currency is **authored** and
   must be labelled as such in `model-params.md` (same discipline as every authored coefficient).

## Effect on the R3 recommendation

None structural — it strengthens it. The lever stays litter access hours; the tripwire stays UEP
2024; the timing rule gains a *positive* foundation (it is now "protect the opportunity peak," not
merely "avoid an unevidenced harm claim"); and the depth/condition route now carries both signs
(condition degradation removes positive welfare before it ever causes footpad harm). The node
scores welfare judgment on both ledgers: harms avoided AND goods preserved.
