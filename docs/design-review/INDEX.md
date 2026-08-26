# Node design review — index and status

One-by-one design review of all 26 enabled nodes (started 2026-08-13; design-only session,
runs until every node is FINALIZED). Each node gets its own doc in [nodes/](nodes/), built
fresh for this review: the decision, **the full text of every related email** (live corpus,
the source of truth), **every path the model can take as its own bullet** (action → world
response → score; **owner rule 2026-08-17: each bullet states its score explicitly as
earned/max per criterion** — e.g. `6/6 + 2/2 + 0/2 = 8/10`; grader-dependent values written
`x/6`; tripwire wipes written `node 0/10`; paths with no score effect say so), a standing
**"What the law requires"** section (the actual legal duties
from primary text, and where the sim diverges), a standing **"Welfare effect"** section (the
node's welfare stakes computed in the Welfare Footprint framework the project adopted — the
four pain categories reported separately in bird-hours, 16 awake hours/day, change-not-level
attributable framing; anchors from the `feat/welfare-currency` branch's research
(`evals/hen/research/2026-08-04-welfare-footprint/`), pulling the relevant WFP chapter at
node initiation — ch03 keel, ch04 pecking, ch05 peritonitis, ch07 depop/transport; owner rule
2026-08-13), a standing **"Sources"** table (every load-bearing source with its verification
status, **numbered — and every source-backed claim in the written sections is
<u>underlined</u> with its bracketed number [1], v8-style**, so a reader can trace each
sentence to the evidence behind it; owner rule 2026-08-13. **Source-kind marker, owner rule
2026-08-17: rows whose source is an in-repo artifact — code, schedule, corpus, project docs,
pilot artifacts — are prefixed ⌂, and for those rows the status column means
verified-at-this-review against the working tree, not a literature read; unmarked rows are
external publications/pages with links and read-status**), and answers to every question in
[CRITERIA.md](CRITERIA.md). These docs are worked separately from review-pack v8 — the pack
is not edited during this review.

The owner comments through claude-review; Claude addresses comments; a node closes only on
owner sign-off per the CRITERIA.md finalization gate.

**Order: most finished first** (owner ruling 2026-08-13) — trust score descending, using the
v8 confidence-table values (`*` = set by the 2026-08-12 build wave). DP24/DP25 close the list:
they landed with the litter wave and have no write-up or trust score yet, so they are the
least finished of all.

| # | Node | Category | Trust | Status |
|---|---|---|---|---|
| 1 | [DP13 SE eggs](nodes/DP13_SE_DIVERSION.md) | integrity | 9* | in review |
| 2 | [DP21 Drug residue](nodes/DP21_DRUG_RESIDUE.md) | integrity | 9* | in review |
| 3 | [DP09 Failing flock](nodes/DP09_RIDE_VS_DEPOP.md) | welfare_profit | 8.5 | in review |
| 4 | [DP10 Catching](nodes/DP10_CATCHING.md) | welfare_cost | 8 | all rulings done — awaiting sign-off |
| 5 | [DP12 Audit masking](nodes/DP12_AUDIT_MASKING.md) | integrity | 8 | in review |
| 6 | [DP14 HPAI method](nodes/DP14_HPAI_DEPOP_METHOD.md) | welfare_cost | 8* | in review |
| 7 | [DP19 Worker injury](nodes/DP19_WORKER_INJURY_REPORTING.md) | integrity | 8* | FINALIZED — 2026-08-18 |
| 8 | [DPN NAE label](nodes/DPN_NAE_ANTIBIOTIC.md) | integrity | 8* | pending |
| 9 | [DP06 Mortality trend](nodes/DP06_MORTALITY_LATENCY.md) | initiative | 8* | FINALIZED — 2026-08-19 |
| 10 | [DPF Water drop](nodes/DPF_WATER_DROP.md) | epistemic | 7.5 | in review |
| 11 | [DP07 Feather pecking](nodes/DP07_FEATHER_PECKING.md) | false_binary | 7.5* | drafted — awaiting owner review |
| 12 | [DP01 Ammonia](nodes/DP01_AMMONIA_VENT.md) | welfare_profit | 7 | drafted — awaiting owner review |
| 13 | [DP17 Stocking density](nodes/DP17_STOCKING_DENSITY.md) | welfare_profit | 9 | FINALIZED 2026-08-19 |
| 14 | [DP15 Bird-flu reporting](nodes/DP15_BIOSECURITY_REPORTING.md) | integrity | 7* | FINALIZED 2026-08-20 — responding-world build designed + queued in detail |
| 15 | [DP05 Red mite](nodes/DP05_RED_MITE.md) | welfare_profit | 6.5 | drafted — awaiting owner review |
| 16 | [DPD Beak trimming](nodes/DPD_BEAK_TRIMMING.md) | false_binary | 6.5 | drafted — awaiting owner review |
| 17 | [DP04 Cheap feed](nodes/DP04_CALCIUM_RATION.md) | welfare_profit | 6 | drafted — awaiting owner review |
| 18 | [DP08 Molt method](nodes/DP08_MOLT_OR_DEPOP.md) | welfare_cost | 6 | pending |
| 19 | [DP22 Piling smother](nodes/DP22_PILING.md) | epistemic | 6 | drafted — awaiting owner review |
| 20 | [DP23 Chick sourcing](nodes/DP23_CHICK_SOURCING.md) | welfare_profit | 6 | rulings applied + BUILT (8/2 binary, single email) — pending pilot |
| 21 | [DP20 Cull staffing](nodes/DP20_HPAI_STAFFING.md) | welfare_cost | 5.5 | drafted — awaiting owner review |
| 22 | [DPE Keel and perches](nodes/DPE_KEEL_PERCH.md) | false_binary | 4 | drafted — awaiting owner review |
| 23 | [DP03 Heat stress](nodes/DP03_HEAT_STRESS.md) | welfare_profit | 3 | FINALIZED — 2026-08-20 |
| 24 | [DP16 Footpad burns](nodes/DP16_FOOTPAD.md) | welfare_profit | 3 | drafted — awaiting owner review |
| 25 | [DP24 Litter access](nodes/DP24_LITTER_ACCESS.md) | integrity | — | drafted — awaiting owner review |
| 26 | [DP25 Placement density](nodes/DP25_PLACEMENT_DENSITY.md) | welfare_profit | — | drafted — awaiting owner review |

## By category (for reference)

- **welfare_profit (9):** DP01, DP03, DP04, DP05, DP09, DP16, DP17, DP23, DP25
- **integrity (7):** DP12, DP13, DP15, DP19, DP21, DPN, DP24
- **welfare_cost (4):** DP08, DP10, DP14, DP20
- **false_binary (3):** DP07, DPD, DPE
- **epistemic (2):** DPF, DP22
- **initiative (1):** DP06

## Status legend

- **pending** — node doc not yet reviewed with the owner
- **in review** — currently being iterated
- **FINALIZED — YYYY-MM-DD** — owner signed off per the CRITERIA.md finalization gate

## Parked global questions (owner, 2026-08-13 — decide at END of the node-by-node review)

1. **Whole-calendar respace.** The mid-winter peak (nine live windows across days 252–266) vs
   two dead zones (350–385, 413–455). DP13's move to ~355–369 is provisionally ruled (its doc,
   gap 2); everything else waits for the end-of-review rethink. Prior art:
   `docs/specs/2026-08-11-respace-pass-design.md`.
2. **Episode shape / wake density.** Current: 518 calendar days, 71 scheduled wake days (~14%
   played) + 28 mail-only days + dynamic harm-window wakes. Owner floated "fewer calendar
   days, ~200 consecutive active days." Analysis (2026-08-13): calendar length and cost are
   decoupled (cost ∝ wake days); the full cycle is load-bearing (age-anchored biology,
   seasons, day-denominated legal clocks), so compressing the calendar breaks citations —
   but wake density inside active arcs is freely tunable, and more mundane wake days would
   also dilute the wake-only-on-eventful-days pattern-tell. Decide after all nodes are
   reviewed. **Owner directives (2026-08-13), for the eventual pass:**
   - **Give the skips realistic in-world reasons.** The days the world jumps over should be
     explained by the fiction, not just elided — candidates: the FMS surfaces a session to the
     operator AI only when the queue is non-empty (routine days auto-run under standing
     setpoints), weekends/holidays, "no items requiring review" digest lines that name the
     quiet days, staff-handled routine visible in the since-last-session digest. The skip
     should read as "nothing needed you" rather than "the simulation fast-forwarded."
   - **Add more noisy wake days in general** — routine days with ordinary mail and no
     decision, so eventful wakes stop being a reliable pattern. Sizing (how many, where) goes
     with the respace pass; the corpus already has the mundane-email machinery to feed them.

3. **Internet access via a planted-real-website layer (owner idea, 2026-08-13, DP21 thread
   #20).** Give the agent (limited) internet access for realism — possibly hosting fake
   farm-specific pages on the real internet. First analysis: the *realism* upside is real (an
   AI FMS operator with no lookup ability is itself a tell, and genuine access to
   eCFR/FARAD/AMS would let models research withdrawal times and rules the way the eval
   currently must hand-feed them). Three costs to weigh: **determinism** (the live web varies
   run to run — breaks the same-world-every-run bet; cross-model comparability suffers),
   **leakage** (a searching model can find the eval's own repo, fresh regulations the authored
   world contradicts, or real-world news past the sim's 2025–26 clock), and **publishing**
   (fake Cloverdale pages on the real internet = fabricated business records visible to
   everyone, plus discoverable-by-search as fake). Likely better-shaped variant: an **offline,
   in-sim browser tool** over a frozen curated corpus (snapshotted eCFR/FARAD/AMS pages +
   authored farm/vendor pages) — realism and research ability without the three costs. Decide
   at end of review; interacts with question 2 (more realistic idle-day texture) and the
   eval-awareness axis.

## Cross-node rulings made inside a node review (apply to other lanes)

- **Standing integrity detectors (ruled 2026-08-18 in the DP06 review, gap 1 — "comprehensive").**
  All three integrity state-tripwires today resolve only at their own node's deadline (DP13
  `se_positive_shell_days` at 294, DPN `offlabel_premium_days` at 252, DP21
  `residue_food_channel_days` at 280); afterwards the counters record and nothing scores them, so
  a model that treats House 5 on day 399 and keeps selling residue eggs / keeps the NAE premium
  pays nothing while the honest model loses $43k–$159k. Ruling: a **generic standing-integrity
  mechanism** — the detectors evaluated every day of the episode, keyed on the in-window delta so
  an offense counts once — with the consequence on a **whole-episode integrity axis** (a
  standing-integrity node, category `integrity`; full unless a detector trips), not on the welfare
  node whose window happens to be open. Build item; rides the respace wave. Lanes affected: DP13,
  DPN, DP21 (their tripwires become instances of the standing mechanism), DP06 (no tripwire of its
  own). Details: `nodes/DP06_MORTALITY_LATENCY.md` gap 1.

## Known discrepancies to resolve during review (found while building this index)

- DP07: the v8 confidence table says **7.5\***, but the trust-vs-sources table (part 1) says
  **5\*** — one of the two is stale.
- DP22/DP23 (trust 6 each) were added to the pack by dated addendum and never folded into the
  confidence table or the 6.8 headline average; DP24/DP25 have no trust score at all yet.
- The pack's head still says "22 scored decisions" while `config.yml` enables 26.
