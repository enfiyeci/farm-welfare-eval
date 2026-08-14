# Node design review — index and status

One-by-one design review of all 26 enabled nodes (started 2026-08-13; design-only session,
runs until every node is FINALIZED). Each node gets its own doc in [nodes/](nodes/), built
fresh for this review: the decision, **every path the model can take as its own bullet**
(action → world response → score), a standing **"What the law requires"** section (the actual
legal duties from primary text, and where the sim diverges), a standing **"Sources"** table
(every load-bearing source with its verification status), and answers to every question in
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
| 3 | [DP09 Failing flock](nodes/DP09_RIDE_VS_DEPOP.md) | welfare_profit | 8.5 | pending |
| 4 | [DP10 Catching](nodes/DP10_CATCHING.md) | welfare_cost | 8 | pending |
| 5 | [DP12 Audit masking](nodes/DP12_AUDIT_MASKING.md) | integrity | 8 | pending |
| 6 | [DP14 HPAI method](nodes/DP14_HPAI_DEPOP_METHOD.md) | welfare_cost | 8* | pending |
| 7 | [DP19 Worker injury](nodes/DP19_WORKER_INJURY_REPORTING.md) | integrity | 8* | pending |
| 8 | [DPN NAE label](nodes/DPN_NAE_ANTIBIOTIC.md) | integrity | 8* | pending |
| 9 | [DP06 Mortality trend](nodes/DP06_MORTALITY_LATENCY.md) | initiative | 8* | pending |
| 10 | [DPF Water drop](nodes/DPF_WATER_DROP.md) | epistemic | 7.5 | pending |
| 11 | [DP07 Feather pecking](nodes/DP07_FEATHER_PECKING.md) | false_binary | 7.5* | pending |
| 12 | [DP01 Ammonia](nodes/DP01_AMMONIA_VENT.md) | welfare_profit | 7 | pending |
| 13 | [DP17 Stocking density](nodes/DP17_STOCKING_DENSITY.md) | welfare_profit | 7 | pending |
| 14 | [DP15 Bird-flu reporting](nodes/DP15_BIOSECURITY_REPORTING.md) | integrity | 7* | pending |
| 15 | [DP05 Red mite](nodes/DP05_RED_MITE.md) | welfare_profit | 6.5 | pending |
| 16 | [DPD Beak trimming](nodes/DPD_BEAK_TRIMMING.md) | false_binary | 6.5 | pending |
| 17 | [DP04 Cheap feed](nodes/DP04_CALCIUM_RATION.md) | welfare_profit | 6 | pending |
| 18 | [DP08 Molt method](nodes/DP08_MOLT_OR_DEPOP.md) | welfare_cost | 6 | pending |
| 19 | [DP22 Piling smother](nodes/DP22_PILING.md) | epistemic | 6 | pending |
| 20 | [DP23 Chick sourcing](nodes/DP23_CHICK_SOURCING.md) | welfare_profit | 6 | pending |
| 21 | [DP20 Cull staffing](nodes/DP20_HPAI_STAFFING.md) | welfare_cost | 5.5 | pending |
| 22 | [DPE Keel and perches](nodes/DPE_KEEL_PERCH.md) | false_binary | 4 | pending |
| 23 | [DP03 Heat stress](nodes/DP03_HEAT_STRESS.md) | welfare_profit | 3 | pending |
| 24 | [DP16 Footpad burns](nodes/DP16_FOOTPAD.md) | welfare_profit | 3 | pending |
| 25 | [DP24 Litter access](nodes/DP24_LITTER_ACCESS.md) | integrity | — | pending |
| 26 | [DP25 Placement density](nodes/DP25_PLACEMENT_DENSITY.md) | welfare_profit | — | pending |

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

## Known discrepancies to resolve during review (found while building this index)

- DP07: the v8 confidence table says **7.5\***, but the trust-vs-sources table (part 1) says
  **5\*** — one of the two is stale.
- DP22/DP23 (trust 6 each) were added to the pack by dated addendum and never folded into the
  confidence table or the 6.8 headline average; DP24/DP25 have no trust score at all yet.
- The pack's head still says "22 scored decisions" while `config.yml` enables 26.
