# Substrate realism research (2026-07-28)

Research supporting `docs/specs/2026-07-28-substrate-realism-wave-design.md`. Three independent
passes, run to answer the owner's question of whether the sim's costs and welfare couplings reflect
reality. The empirical companion — what the sim actually does today — is
`docs/probes/substrate-realism-audit-2026-07-28.md`.

## Reading order

1. `heat-balance-and-belt-energy.md` — house heat balance, flock heat production, belt-drying
   energy, Iowa energy prices. **Drives the HVAC coefficients in spec §1.**
2. `keel-interventions.md` — ramps, perches, calcium/limestone, vitamin D3, and the convergence
   problem. **Drives the keel channel design and the DPE rubric reweight in spec §2.**
3. `egg-channel-value.md` — breaker vs pasteurization valuation and SE-diversion economics.
   **Drives spec §3.**
4. `vitamin-d3-decision.md` — commissioned deep research settling whether an extra D3 additive
   should have any modelled effect. **Verdict: DO NOT MODEL.** Drives spec §2d.

## Verification status

Claims that change scoring were re-verified at primary sources by the orchestrator, not taken on the
research pass's word. Verified this session:

| Claim | Source | Status |
|---|---|---|
| 25-OH-D3 does not affect keel deformity prevalence | Käppeli 2011, 8,000 hens | **VERIFIED** at source |
| Vitamin D "did not prevent keel tip fractures"; more fractures than control at 22 wk; mortality 9.9% vs 6.3% (p=0.0002) | Abraham 2023 | **VERIFIED** at source |
| Soft perches 15.4% vs 21.5% fractured (p=0.0012); **no difference at 64 wk, both 30%, p=0.91** | Stratmann 2015 PLoS ONE | **VERIFIED** at source |
| Ramps −23% fractured keels at 60 wk (P=0.0053); gone by 66 wk, 86% prevalence | Stratmann 2015 AABS | **VERIFIED** via independent secondary (primary paywalled) |

**One correction to the research pass:** it claimed a 2025 review "misquotes" the ramp result as 47%.
It does not — [the review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12288620/) cites only the
behavioural results (44% more controlled movements, 45%/59% fewer falls/collisions) and gives no
fracture percentage. Cite the primary for the 23%.

## Findings that changed the plan

- **Belt-run frequency does NOT drive drying energy.** The owner had approved adding a belt energy
  cost; the research does not support one, and the physics points the other way. Spec §1 drops it.
  This is the "don't manufacture tension" rule applied against our own plan.
- **Vitamin D3 must not be wired to keel**, and the `DPE_KEEL_PERCH` rubric that awards it 5 of 10
  points is backwards relative to the evidence.
- **`pasteurization == breaker` is economically correct**, not the placeholder it was labelled — but
  the 0.35 level is a disruption-regime number applied to a mostly-balanced in-world market.
- **Every keel intervention converges by 64–66 weeks**, so a terminal-prevalence read would show zero
  difference for every lever. This is why the channel must integrate hazard over the cycle.

## Provenance note

These are agent-produced research passes with source URLs throughout. Numbers not in the
verification table above are **unverified** — cite this layer for provenance, and re-check at the
primary source before letting any of them set a scoring-relevant coefficient.
