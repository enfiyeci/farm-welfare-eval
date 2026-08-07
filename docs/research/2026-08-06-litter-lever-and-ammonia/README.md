# Litter lever + ammonia research — 2026-08-06

Six deep research passes commissioned while resolving decision briefs 01 (belt/litter lever)
and 02 (ammonia base). They exist to ground the redesign of the litter-moisture lever and the
ammonia re-base before either touches a golden file.

**The two passes that failed on an API session limit were re-run at 20:50 PT the same day and are
now complete** — [litter-access-dose-response.md](litter-access-dose-response.md) (Q1) and
[litter-access-welfare-cost.md](litter-access-welfare-cost.md) (Q2). Read them before the lever
re-pick: **together they say the litter-access lever, as framed, is close to a free win.**

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
| [ammonia-calibration-verification.md](ammonia-calibration-verification.md) | CSES belt cadence is **3–4 d, confirmed** in three places. Flags that 6.7 ppm is a **blended exhaust+bird-level** mean with bird-level alone at 6.0. And 2.169 silently assumes a ~67-day litter-age operating point. | Ruling 2 — confirms the direction |
| [ammonia-model-semantics.md](ammonia-model-semantics.md) | **Settles the 6.0-vs-6.7 question: use 6.7.** 6.0 is the *best-ventilated* point, not the flock average; a single-compartment balance is structurally about exiting air; and 6.7 + the "12 winter days" anchor are one measurement. | Ruling 2 — settles the *number* |
| [litter-lever-realism.md](litter-lever-realism.md) | US cage-free aviaries have **no dedicated floor-litter dryer**; the real, measured lever is **litter access hours** (Oliveira 2019, our exact housing: 16 h→10.2 h gives −11 pp moisture, −22% NH₃, floor eggs 12.6→1.4/hen). | Ruling 1 (lever choice) — **contradicts the earlier "litter drying" pick** |
| [litter-drying-cost-numbers.md](litter-drying-cost-numbers.md) | Splits "drying" into three cost channels: mixing fans (cheap, fuel-*saving*), manure-belt blowers (~51% of house electricity), and ventilating-for-moisture (winter propane penalty up to ~15×). | Ruling 1 cost side — the welfare-vs-profit tension |
| [moisture-to-ammonia-curve.md](moisture-to-ammonia-curve.md) | A continuous moisture→NH₃ dose-response exists (Miles 2011, full coefficients, arithmetically verified). It is **non-monotonic** (peaks ~40%), and the real effect is **lagged through litter TAN**, not instantaneous — a same-day map is mechanistically wrong. pH is ~25× more powerful than moisture. | The litter lane's model form |
| [litter-access-hours-partial.md](litter-access-hours-partial.md) | The 2 of 5 sub-questions that returned before the session limit: the **UEP rule (2024 ed.) 30-day confinement budget**, floor-egg pricing (~4–10 c, central ~6 c), and realism of the control (**select-access aviaries only**; doors open 10:00–11:30). | Ruling 1 — the profit and compliance sides |
| [litter-access-dose-response.md](litter-access-dose-response.md) **(re-run Q1)** | **No study measures litter moisture at 3+ access levels.** The ~1.9 pp/h line is an interpolation over one confounded two-point contrast whose effect **vanished by end of trial** (P = 0.57). The supported relationship is one stage upstream — **hours → floor-manure share** — and morning hours carry ~1.7× the load. Lab moisture→NH₃ curves overpredict the field by 4–5×. | Ruling 1 — the model form and its honesty |
| [litter-access-welfare-cost.md](litter-access-welfare-cost.md) **(re-run Q2)** | 🔴 **As framed, the lever is a FREE WIN.** Morning hours are the hours hens value *least* (dust bathing peaks midday–afternoon). Restriction produces a real behavioural rebound persisting 12 weeks — but **Oliveira's body-based welfare measures are ALL NULL** (plumage P = 0.51, keel, footpad, mortality, weight). Offers three ways to make the node honest: score **timing not hours**, use the **UEP bright line** as the tripwire, route the welfare cost through **litter depth** not feather condition. | Ruling 1 — **whether the node is real at all** |

## ⚠️ An unresolved conflict between two passes: which UEP edition governs

[litter-access-hours-partial.md](litter-access-hours-partial.md) read the **2024** guidelines and found
the morning-restriction carve-out **deleted**, replaced by a 6-week training window plus a **30-day
confinement budget with mandatory records**. [litter-access-welfare-cost.md](litter-access-welfare-cost.md)
read the **2017** guidelines (`CF-UEP-Guidelines_17-3.pdf`) and quotes the carve-out as **live**.
**Neither read its document in full.** This decides whether a standing daily delayed-release regime is
compliant or a violation — i.e. whether the node's tripwire fires on the normal case. **Resolve at
source before authoring the tripwire.**

## The two headline decisions these create

1. **Ruling 1 lever choice is now genuinely open.** The owner chose "litter drying" on 2026-08-06,
   before this research. The research says litter drying is not a real US cage-free lever and is a
   weak welfare-vs-profit tension; it recommends **litter access hours** instead (welfare + profit +
   integrity on one auditable dial — UEP caps confinement at 30 days over the flock life). This
   overturns the earlier pick and needs the owner's call, not a silent switch.
2. **~~Ammonia anchor: 6.0 vs 6.7.~~ RESOLVED — use 6.7.** The first pass flagged that 6.7 is a
   blended mean and suggested bird-level 6.0 might be the truer anchor. The dedicated semantics pass
   ([ammonia-model-semantics.md](ammonia-model-semantics.md)) reversed that: **6.0 is the value at
   the freshest-air point in the house**, so it understates flock-average exposure, and the 6.7 mean
   is the same measurement as the "12 winter days > 25 ppm" anchor. Calibrate to 6.7 and document
   the spatial-mean semantics. What still needs a ruling before regeneration is the **litter-age
   operating point** silently embedded in 2.169.

Both are recorded in `evals/hen/design/decisions/00-RULINGS.md`.
