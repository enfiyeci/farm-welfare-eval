# Long-horizon financial benchmarks and real US egg-price data

Eval: hen

Written 2026-11-05 for the hen cost and finance assessment
(`evals/hen/design/2026-11-05-hen-cost-and-finance-assessment.html`, sections 3 and 4).

## Files

1. `2026-11-05-raw-agent-report.md`: the research agent's report (Claude Sonnet), unchanged.
   **Raw.** It carries its own ⚠️ marks and coverage statement.

## Re-checked by the orchestrator against the agent's downloaded text (2026-11-05)

- Vending-Bench (arXiv 2502.15840): $500 start, $2 daily fee, run ends after 10 consecutive unpaid days.
- CoffeeBench (arXiv 2606.16613): $15,000 start, net-30 terms, negative cash means bankruptcy.
- EnterpriseArena (arXiv 2603.23638): 132 months, 15.4% of trials survive, anonymized data.
- RetailBench (arXiv 2606.15862): Dominick's grocery data.
- BLS retail Grade A Large (FRED `APU0000708111`): $1.788 (2021-12), $4.823 (2023-01), $2.522 (2024-01),
  $6.227 (2025-03), $2.272 (2026-09).
- USDA AMS Egg Markets Overview, October 30, 2026: national white Large $0.35/doz, Midwest $0.54.

Everything else in the raw report is the agent's claim.

## Notable catches

- No free numeric series for cage-free wholesale eggs was found; Expana's index is paid.
- Real 2024–25 wholesale prices passed $8/doz, then fell to $0.35 by October 2026, far below cost.
- The authored propane index (1.00–1.35) fits Iowa EIA data; the authored feed band ($277–291/ton) does not.
