# Litter lever + ammonia research — 2026-08-06

Four deep research passes commissioned while resolving decision briefs 01 (belt/litter lever)
and 02 (ammonia base). They exist to ground the redesign of the litter-moisture lever and the
ammonia re-base before either touches a golden file.

## Provenance and trust

**These are delegated subagent findings.** Each pass returned an explicit coverage statement, and
those statements plus every ⚠️ partial-read flag are preserved verbatim in the files below — do not
treat a claim as fully sourced where its ⚠️ says otherwise. **I (the orchestrating session) have not
independently re-read the primary sources.** Per the owner's research-discipline rule, any finding
about to move a frozen number (the ammonia base, a golden regeneration, the lever choice) must be
traced back to the primary source directly before it is relied on. The load-bearing ones to trace
first are flagged in each file.

## Reading order

| File | What it settles | Decision it feeds |
|---|---|---|
| [ammonia-calibration-verification.md](ammonia-calibration-verification.md) | CSES belt cadence is **3–4 d, confirmed** in three places. But 6.7 ppm is a **blended exhaust+bird-level** mean; **bird-level alone is 6.0 ppm**. And 2.169 silently assumes a ~67-day litter-age operating point. | Ruling 2 (ammonia base) — reopens the *number*, not the direction |
| [litter-lever-realism.md](litter-lever-realism.md) | US cage-free aviaries have **no dedicated floor-litter dryer**; the real, measured lever is **litter access hours** (Oliveira 2019, our exact housing: 16 h→10.2 h gives −11 pp moisture, −22% NH₃, floor eggs 12.6→1.4/hen). | Ruling 1 (lever choice) — **contradicts the earlier "litter drying" pick** |
| [litter-drying-cost-numbers.md](litter-drying-cost-numbers.md) | Splits "drying" into three cost channels: mixing fans (cheap, fuel-*saving*), manure-belt blowers (~51% of house electricity), and ventilating-for-moisture (winter propane penalty up to ~15×). | Ruling 1 cost side — the welfare-vs-profit tension |
| [moisture-to-ammonia-curve.md](moisture-to-ammonia-curve.md) | A continuous moisture→NH₃ dose-response exists (Miles 2011, full coefficients, arithmetically verified). It is **non-monotonic** (peaks ~40%), and the real effect is **lagged through litter TAN**, not instantaneous — a same-day map is mechanistically wrong. pH is ~25× more powerful than moisture. | The litter lane's model form |

## The two headline decisions these create

1. **Ruling 1 lever choice is now genuinely open.** The owner chose "litter drying" on 2026-08-06,
   before this research. The research says litter drying is not a real US cage-free lever and is a
   weak welfare-vs-profit tension; it recommends **litter access hours** instead (welfare + profit +
   integrity on one auditable dial — UEP caps confinement at 30 days over the flock life). This
   overturns the earlier pick and needs the owner's call, not a silent switch.
2. **Ammonia anchor: 6.0 vs 6.7 ppm.** If `nh3_ppm` means what a hen breathes, the anchor is the
   bird-level 6.0, not the published whole-house 6.7 — a further ~10% on top of the cadence
   correction. Needs a ruling before any golden regeneration.

Both are recorded in `docs/decisions/00-RULINGS.md`.
