# Long-horizon financial benchmarks and real US egg-price data

Eval: hen

Written 2026-11-05 for the hen cost and finance assessment
(`evals/hen/design/2026-11-05-hen-cost-and-finance-assessment.html`, sections 3 and 4).

## Files

1. `2026-11-05-raw-agent-report.md`: the research agent's report (Claude Sonnet), unchanged.
   **Raw.** It carries its own ⚠️ marks and coverage statement.
2. `2026-11-05-raw-agent-report-sweep-2.md`: the second sweep, 16 more benchmarks, four Claude Sonnet
   reader reports unchanged. **Raw.** Each ends with its own coverage statement.

## Second sweep: re-checked by the orchestrator against the readers' downloaded text (2026-11-05)

- E-Commerce Bench (arXiv 2608.30730): ¥100,000 start; sales sit in escrow 9 days after shipping;
  bank below zero on 10 consecutive days ends the episode; 152 of 576 suppliers are fraudulent;
  fraud avoidance is scored as BadSpend%, the share of spend that cleared to a fraudulent supplier.
- CEO-Bench (arXiv 2606.18543): $1M start, graded on cash at the end, cash below zero ends the run;
  a four-week cash forecast is asked for each week and its error reported.
- YC-Bench (arXiv 2604.01212): 35% of clients adversarial, inflating work after acceptance; a missed
  deadline costs 35% of the reward; funds below zero end the run.
- Business Arena (arXiv 2608.08621): $80,000 start; fines F_k = max($500, 0.15 × order value) × min(k, 5);
  FinalAssets = cash + 0.97·escrow + 0.97·receivables + 0.85·inventory − payables − loans; each mechanism
  tested with intended, neglect and misuse policies; suppliers may overstate quality or understate delivery
  time; no bankruptcy rule found in the text.
- ERPBench (arXiv 2609.04667): Solo and Arena agree on the winner on only 21 of 100 problems.
- AucArena (arXiv 2310.05746): a deliberate overestimate of item value builds in the winner's curse.
- InventoryBench (arXiv 2602.12631): an order's lead time can be ∞, so the order never arrives.
- AIM-Bench (arXiv 2508.11416): scores distance from the ex-post optimal order quantity.
- GovSim (arXiv 2404.16698): stock doubles each month up to 100, collapses below C = 5; best survival 53.3%.
- MACHIAVELLI (arXiv 2304.03279): GPT-4 normalized reward 27.4, with an ethics prompt 24.7.
- EconEvals (arXiv 2503.18825): equalizing pay costs roughly 30% of revenue in the efficiency-vs-equality test.
- Project Vend phase two (anthropic.com/research/project-vend-2): weeks with a negative margin largely
  eliminated; the CEO agent cut discounts about 80% but approved lenient requests eight times as often as it
  denied them.

Not reachable: AgriManager's full paper (OpenReview bot check, no arXiv version). ⚠️ Facts not listed
here are the readers' claims.

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
