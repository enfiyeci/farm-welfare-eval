# Second benchmark sweep: 16 more long-horizon benchmarks, raw reader reports (UNVERIFIED)

Eval: hen

Raw output of four Claude Sonnet reader subagents, 2026-11-05, kept unchanged for provenance. Each read
four primary sources (PDFs converted with pdftotext, web pages saved as text) and was told to read the
main body end to end, mark anything less with ⚠️, and end with a coverage statement. Cite the README's
re-checked layer, not this file.

Reports, in order: (A) business simulations: E-Commerce Bench, CEO-Bench, YC-Bench, Business Arena;
(B) markets and auctions: Market-Bench, ERPBench, Cattle Trade, AucArena; (C) commons and ethics: GovSim,
MACHIAVELLI, EconEvals, Project Vend phase two with the Andon Labs Vending-Bench pages; (D) inventory and
farm: AIM-Bench, InventoryBench, AgriManager (abstract only), a WOFOSTGym crop-management paper.


---

# Report a-business-sims

# Financial-structure facts from four long-horizon business benchmarks

All four IDs resolve to the papers named. Local copies are in `/private/tmp/claude-501/-Users-ardaenfiyeci-worktrees-farm-eval-hen-cost/d6ba3112-405f-4e5c-baf1-1ddae93a3621/scratchpad/papers/a/`: `2608.30730.{pdf,txt}`, `2606.18543.{pdf,txt}`, `2604.01212.{pdf,txt}`, `2608.08621.{pdf,txt}`.

Two corrections to the brief:
- Business Arena (2608.08621) is by the Accio Team, Alibaba Group (with Yale), not the Qwen team. E-Commerce Bench is the Qwen Team paper.
- E-Commerce Bench's PDF header reads 2026-09-01. arXiv v1 is dated 31 Aug 2026.

---

## 1. E-Commerce Bench (arXiv 2608.30730)

**Identity**
- Title: "E-Commerce Bench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation".
- Version v1 [cs.LG], 31 Aug 2026.
- Authors: Wei Fan, Xinjie Shen and others. Affiliations are Qwen Team (Alibaba), Taobao & Tmall Group, and HKUST. Work done during a summer internship.
- Code: https://github.com/QwenLM/E-CommerceBench (abstract).

**Horizon and step**
- 365 simulated days from 2026-01-01. Each day is 600 minutes (08:00 to 18:00). §3.2.1, App. C.7.
- Episode cap of 4,000 turns. An episode also ends early if the model makes 3 turns without a tool call. §3.2.1.
- Observed: the longest episode took 3,599 turns (§4.1). Tool calls per episode ran 1,076 to 3,668 (Table 2).
- Context is 128k tokens. Whole oldest tool-call groups are evicted at 120k, aiming to free 60k. §3.2.2.
- There is a persistent memory of at most 20 notes. §3.2.3.

**Decisions (18 tools, Table 3, p.26)**
- Market research.
- Supplier search and free-text negotiation through one `chatbox` tool. Only `chatbox` can create a purchase order.
- Opening and closing up to 4 stores, from 12 store types.
- Publishing stock, setting prices, joining promotions.
- Shipping at a chosen speed.
- Checking balance, withdrawing from wallet to bank, and writing to memory.
- `wait_for_next_day`.

**How money feeds back**
- Start: ¥100,000 in the bank. §3.1.
- Three accounts, §3.4.2 and Fig. 6:
  - The bank pays every cost the moment it is incurred, including the full purchase order when a negotiation closes.
  - A sale pays nothing until the agent ships it. Revenue then enters escrow net of a 2% commission.
  - Escrow matures into the platform wallet 9 days after shipping.
  - Only an explicit `withdraw` (10 simulated minutes) moves wallet cash back to the bank.
  - Refunds are taken from the escrow batch of the original sale.
- Fixed costs:
  - Store setup is ¥500, charged again on a reopen.
  - Operating cost is ¥60, ¥100 or ¥130 per open store per day, by difficulty tier. App. C.5.
  - If no store is open after day 7, a ¥1,000/day idle penalty applies.
- Storage fee is per unit per day, with an age multiplier rising from ×1.0 to ×9.0 at 180 days. FIFO, and listed stock keeps accruing. App. C.5.
- Freight is charged at ship time, scaled by speed.
- Fast freight cuts the return draw by about a quarter. Slow freight raises returns ×1.30. §3.4.4.
- Returns are decided when goods ship and land 3 to 7 days later. A refund is the full retail price out of escrow. Freight and commission are never refunded.
- Delivery lag: supplier lead time is 3 to 7 days in the Fig. 6 example. Events stretch lead time by ×2 to ×5. App. B.3 Table 6.
- Closing a store without liquidating leaves storage accruing. Liquidation pays 10% of purchase cost.
- No credit, loans or interest. None found in the text read.
- Ordering inside each morning: costs post before any revenue, so solvency is tested at the day's low point. App. C.1, Fig. 16.

**What ends a run**
- "Bankruptcy follows 10 consecutive days with a negative bank balance" (App. C.7; §3.4.2).
- The clock is the bank balance only. Cash in the wallet or escrow does not count until withdrawn. App. E.3.
- No tool reports the streak count. §4.3.3.
- Otherwise the run ends at day 365 or on the turn cap.
- Bankrupt episodes stay in the means. §3.7, §4.1.

**Score (§3.7, App. E)**
- Primary: year-end total assets, bank + wallet + escrow, shown as a multiple of ¥100k. Unshipped orders are cancelled and escrow is drained before scoring.
- Six further dimensions, each with one ranking metric:
  - Negotiation quality: CSE+, the share of the bargaining range captured on a closed honest deal. Accepting the opening quote scores 0.50.
  - Fraud avoidance: BadSpend%, the share of order spend that cleared into a fraudulent supplier's account (lower is better).
  - Cash flow and solvency: peak drawdown divided by peak total assets.
  - Operational efficiency: mean profit divided by mean tool calls.
  - Operations execution: the controllable return rate, meaning returns caused by the agent's own pricing, with fraud-induced defects excluded.
  - Learning: AnchorRatio, repeat-order overpayment against the agent's own best price for that supplier and item, divided by the same prices shuffled. 1.0 means no learning.
- Diagnostics that do not rank: SE+, %Oracle, AGR+, NegDays, Trough, IdleWallet and others.

**Novel elements (not on your list)**
- **Time as the information charge.**
  - Every tool except the day jump costs simulated minutes out of the 600-minute day.
  - Examples: `check_balance` 10, `market_search` 30, `chatbox` 30 (the same whether it goes to one supplier or ten), `open_store` 60.
  - The day jump costs 0 but forfeits the rest of the day. §3.2.1, §3.3, Table 3.
  - No money is charged for lookups. §4.4 notes "Nothing in the economy charges for asking twice", and repeated queries wasted about 83 minutes per episode.
- **Deterministic negotiation kernel with an LLM voice (§3.5.2, App. D).**
  - Every price, concession and accept/walk decision comes from a seeded rule engine. A second LLM only renders the dialogue.
  - An accept is refused unless its price is within ±0.005 of the kernel's standing quote.
  - Reason given: an LLM supplier can be talked below its floor, which turns the benchmark into a jailbreak contest.
  - The supplier "remembers" prior deals through a per-supplier deal log. The agent does not, unless it keeps notes.
  - Each supplier retires after a hidden 10 to 20 filled orders (192 closures observed). App. D.4.
- **Fraud scored by cash, not by intent (§3.5.4, §3.7, App. E.2).**
  - 152 of 576 suppliers are fraudulent, running 5 scripted scams (App. D.5, Table 9):
    - Pre-deal scams:
      - `vip_fee`: a ¥1,000 membership fee, with the reservation price raised to ×1.5 the honest cost floor.
      - `future_discount`: a promised discount on the next order that never arrives.
      - `fake_urgency`: manufactured scarcity.
    - Post-deal scams:
      - `qty_bait`: ships 60 to 70% of the paid quantity.
      - `quality_downgrade`: flags units defective, with the return rate lifted to at least 0.40 and blended into the pooled stock so the culprit is untraceable.
  - The agent can attribute pooled stock to suppliers with `trace_return_sources` (10 minutes).
  - The unranked FAGR− statistic is excluded because it "rewards never looking".
- **Hidden-parameter discovery priced in time, yuan, or irreversible loss.** App. B Table 7.
- **Stockout truncates demand with no signal.** App. C.2.
- **Dual stochasticity audit.** Prices and accept/walk are deterministic. Wording and advertised delivery days still vary (§3.5.2).
- **Per-pair repeated-bargaining metric with a permutation null.** §3.5.5, App. E.6.
- **Failure-mode detection rules.** Ten mechanical rules with incidence counts. §4.4, App. G.5, Table 18.

**Ethics, honesty, welfare vs profit**
- None for the agent's own conduct. Fraud is done *to* the agent. No customer or worker welfare element found in what I read.
- The task brief tells the agent "not all suppliers are honest or perform as agreed" (H.1).

**Run cost**
- No dollars or wall time found. A keyword search of the full text turned up only the token gauge and eviction counts.
- The paper notes that no fee in the economy charges for a call, so "the bill falls on whoever deploys the agent" (§4.3.4).

**Headline results**
- 18 models × 5 episodes = 90 episodes. §4.1.
- GPT-5.6 Sol (max) had mean assets ¥1,431k (14.3×), 0/5 bankrupt. Fable5 ¥805k, GPT-5.5 ¥702k (2/5 bankrupt). Qwen3.5-Plus ¥1.1k (4/5 bankrupt). Table 2.
- 10 of 90 episodes went bankrupt, across 4 models. §4.2.
- GPT-5.6 Sol ranks 16th of 18 on BadSpend%. Claude Opus 4.7 is cleanest (0.12%) and best at bargaining.
- Two GPT-5.5 runs went bankrupt on day 17, before any revenue had settled. §4.3.3.
- 49 of 90 episodes bottomed out in January.
- Main failure modes (§4.4, Table 18):
  - Inventory bought and never sold.
  - Reordering from a fraudulent supplier (38 episodes).
  - Accepting the opening quote unimproved.
  - Price drifting upward across re-orders (16 of 18 models).
  - Repeating identical catalog queries.
  - Overdrafts that the wallet balance could have covered.

**Validity safeguards**
- Product, supplier and category data are derived from Taobao/Tmall logs; elasticities and seasonality are synthesised from them. §3.6.
- Promotion names are fictional "since a model that recognizes China's largest shopping festival could price from memory" (§3.6.1).
- Frozen supplier list and calendar, one environment seed shared by all runs (App. B, C.7).
- Authors disclose their own flaws (App. B.5):
  - The supplier email's numeric suffix leaks the fraud label, because honest suppliers hold lower identifiers.
  - The return-rate wording understates the numeric band for 20 categories.
  - One event's cost term is unused.
- A same-seed run produces the same money outcome for the same actions. §3.4.
- Five episodes per model is small. The authors report standard deviations for it (§4.1).

---

## 2. CEO-Bench (arXiv 2606.18543)

**Identity**
- Title: "CEO-Bench: Can Agents Play the Long Game?".
- Version v2 [cs.AI], 22 Jul 2026 (the v1 date is not in the text).
- Authors: Haozhe Chen, Karthik Narasimhan, Zhuang Liu. Princeton University.
- Code: https://github.com/zlab-princeton/ceobench-src. Site: https://ceobench.com, with a trajectory viewer. (I read these from the PDF's link annotations; the text only shows "Code / Blog / Trajectory" icons.)

**Horizon and step**
- 500 simulated days. The agent advances with `next_week()`, taking unlimited turns per week across 34 tools and a 19-table SQL database. §2.1.
- Turns per week by model: 7.8 to 98.7 (Table 3). No turn cap found.
- Context is cleared at the start of each simulated week. Only the system prompt and an agent-editable memory file survive. §3.1 Harness.

**Decisions (Table 1, App. A.1)**
- Pricing, plans, quotas, promotions.
- Ad spend per channel and customer group.
- Development, R&D projects, model tiers, infrastructure capacity tier.
- Targeted ops/support spend.
- Enterprise deal negotiation (offers and counter-offers).
- Paid market research.
- Social media reading and posting.
- Arbitrary Python and SQL.

**How money feeds back**
- Start: $1M cash, zero customers, product "NovaMind", a subscription SaaS company. §2.1.
- Daily cash change (Eq. 1 and 44, App. A.8):
  - Inflows: subscription payments, which arrive on billing days ("cash arrives in discrete renewal events", A.4), plus in-product ad revenue.
  - Outflows: fixed capacity-tier cost, per-usage compute, ops, development, targeted ops/dev, ads, per-lead acquisition charge, market research, group research, and research projects.
- R&D finishes after a stochastic delay with a stochastic quality gain (Eq. 12).
- Market and group research complete after a delay, so results can be stale on arrival (Eq. 31, A.6).
- Macro indicators reach the agent only as period averages with a publication delay (A.6).
- No credit, loans or interest. Compliance, security and fundraising are explicitly left out. §6.1.
- No spoilage.

**What ends a run**
- "If cash ever falls strictly below zero, bankruptcy ends the simulation" (§2.1). Otherwise day 500.

**Score**
- Cash on hand at the end ("graded on cash on hand at the end", §2.1).
- Per-model reporting uses the best of 3 runs: the max cash among surviving runs, or the longest survival if all went bankrupt. §3.1.
- Also reported: bankruptcy counts, mean survival days, and API cost for the best run (Table 3).
- Reference lines: a rule-based non-LLM baseline ($15.76M, App. B) and an estimated attainable upper bound ($2.2B, App. D, which applies a friction factor F=0.49 to a $4.53B pre-friction subtotal).

**Novel elements**
- **Weekly cash forecast.** The agent submits a 4-week-ahead cash forecast each week. Percentage error is a diagnostic only: Fable 5 had 17% and Opus 4.8 11%, against 93% to 564% for the three weaker models (Fig. 12b, §3.4). Not in the score.
- **Paid, delayed, possibly stale information.** Market and group research cost money, complete after a delay, and snapshot conditions at completion. This is a charge for lookup in a stronger form than your list's. §2.1, A.6.
- **Hidden-structure inference.** Ad-channel-by-customer-group lead rates are hidden. Fig. 12a measures the share of spend placed on the true best channel against a 20% random baseline.
- **Non-stationary world.**
  - Competitors are partly adaptive: they consume a share of the agent's *unreleased* quality gain "bank" (Eq. 35 to 36).
  - A hidden macro state follows an Ornstein-Uhlenbeck cycle (Eq. 37).
  - Customer preferences drift.
  - Difficulty ablation: weaker or no competitor makes the task easier (§4.1).
- **Time-horizon ablation.** A 50-day version left all evaluated models below their starting cash (§4.2).
- **Harness ablation.** Claude Code and Codex were worse than the authors' minimal terminal harness, with fewer turns per simulated day (§4.3, Fig. 15).
- **Expected-value structure with large early drawdown.** The best Fable 5 run fell to about $626K by day 30 before compounding to $12.6M. App. C.
- **Per-customer simulation and mechanistic rules.** §2.2 principles.

**Ethics, honesty, welfare vs profit**
- None scored. Customer satisfaction and reputation feed revenue only.
- Agent social posts are "judged per discovered group" for a reaction score (App. A.5, Eq. 27). ⚠️ I found no description of what does the judging, though §2.2 says "almost all" outcomes use explicit mechanisms rather than an LLM judge.

**Run cost**
- Best-run API cost: Fable 5 $265, GPT-5.6 Sol $153, Opus 4.8 $348, Gemini 3.5 Flash $67, Opus 4.7 $92, Sonnet 5 $68, GPT-5.5 $154, and others (Table 3, p.9).
- ⚠️ Cost is blank ("–") for several models, and I found no wall-clock time.

**Headline results**
- Only Fable 5 ($12.6M best run, 1/3 bankrupt), GPT-5.6 Sol ($11.3M, 2/3 bankrupt) and Opus 4.8 ($2.4M, 1/3 bankrupt) ended above $1M. All were below the rule-based baseline.
- GLM 5.1, DeepSeek V4 Pro, Gemini 3 Flash and Grok 4.20 went bankrupt in 3/3 runs. Table 3.
- Failure modes reported:
  - Opus 4.7 narrowed into waiting and preserving cash.
  - Opus 4.8 built a customer base, then fell to zero customers.
  - Weak models forecast poorly and ignored the hidden channel structure.
  - Strong models write "if-then" contingency memos.

**Validity safeguards**
- Independent RNG streams per simulator component, so the same seed gives the same discoveries regardless of other actions (§2.2).
- Rules are explicit mechanisms, not an LLM judge. The authors cite Vending-Bench's LLM suppliers rewarding verbal promises as the failure this avoids.
- Dollar upper-bound check (App. D).
- Caveats:
  - All three runs per model use "random seed 42" (§3.1), so run-to-run variance comes from the model only. ⚠️ I did not find this stated.
  - Headline analysis uses the best of 3.
  - Only 3 runs per model.

---

## 3. YC-Bench (arXiv 2604.01212)

**Identity**
- Title: "YC-Bench: Benchmarking AI Agents for Long-Term Planning and Consistent Execution".
- Version v1 [cs.CL], 1 Apr 2026 (document date "April 2, 2026").
- Authors: Muyu He, Adit Jain, Anand Kumar, Vincent Tu (equal contribution), Soumyadeep Bakshi, Sachin Patro, Nazneen Rajani. Correspondence is research@collinear.ai (Collinear).
- Code: https://github.com/collinear-ai/yc-bench.

**Horizon and step**
- One simulated year, "hundreds of turns". Starting 1 January. §3.
- The agent controls the clock with `sim resume`, which advances to the next event: a checkpoint at 25/50/75/100% of a task, a monthly payroll, or the horizon end.
- Work runs on weekdays 9–18. Payroll is deducted on the first business day of each month. §3.
- Auto-advance after 5 idle turns (Table 2, App. B).
- Context holds only the last K=20 turns. A persistent scratchpad is injected into the system prompt. A K ablation covers 20 to 50 (App. E).
- Turn or message cap: ⚠️ none found. Table 3's caption mentions "thousands of turns" for some models.

**Decisions (Table 1, App. A)**
- Observe: company status, employees, market browse, task list and inspect, client list and history, finance ledger.
- Act: task accept, assign (comma-separated employees), dispatch and cancel; `sim resume`; scratchpad write and append.

**How money feeds back**
- Start $200,000, 8 fixed employees who cannot be hired or fired. §3.
- Payroll: junior $2–4K/mo, mid $6–8K/mo, senior $10–15K/mo. Each completed task gives every assigned employee a 1% salary bump, so payroll only rises. Table 2, §3.
- Revenue: task reward on completion. Rewards are drawn from a triangular distribution on $2K–$12K, mode $5K, scaled by prestige. Table 2.
- Deadline failure costs 35% of the advertised reward plus a prestige loss. Table 2, §3.
- Cancel costs 1.5×δ prestige.
- No settlement delay, loans, interest, escrow, spoilage or supplier paperwork. None stated.
- Throughput split: an employee on N concurrent tasks works at rate/N.

**What ends a run**
- "The episode terminates when funds drop below zero (bankruptcy) or the horizon ends." §3.

**Score**
- Final company funds at year end, a single scalar. §1, §3.
- Reward in the POMDP is the net change in funds.
- Also reported: bankruptcy counts, scratchpad usage statistics, and API cost per run.
- Baseline: a greedy bot that accepts the highest-reward task and assigns everyone. §4.1.

**Novel elements**
- **Hidden adversarial clients (~35%, Table 2).**
  - Adversarial status is never revealed. After the agent accepts one of their tasks, the work quantity is inflated to ≥3×, so the deadline cannot be met.
  - Adversarial clients "offer competitively high rewards" so price cannot be used as a filter. §3.
  - The agent must infer them from its own failure history.
  - Contrast with Vending-Bench, where adversaries are known before commitment (§1).
- **Client trust.** Each completed task builds trust (max 5.0, work reduction up to 50%). Trust gates about 30% of tasks. Completing for one client decays trust with the others, which gives a "snowball" for focused agents. §3, §4.2.
- **Domain prestige.** Range 1 to 10 per domain. It gates tasks and scales rewards linearly. §3.
- **Memory-as-skill.** The 20-turn truncation plus a scratchpad as the only persistence means the score depends on writing and obeying rules. Scratchpad use is "the strongest predictor of success". Abstract, §4.2, §5.
- **Behavior statistics.** Table 3 gives scratchpad writes per 100 turns, inspect-to-accept ratio and concurrency.
- **Context ablation.** Larger windows can hurt (App. E).

**Ethics, honesty, welfare vs profit**
- None. The adversarial clients are untrustworthy counterparties, not an ethics test.

**Run cost (Table 4, App. F, p.16)**
- Opus 4.6: $86.07 ± 41.17, 16.7M tokens, 70 ± 36 min.
- GLM-5: $7.62, 8.3M tokens, 40 min.
- GPT-5.4: $23.08, 9.5M tokens, 19 min.
- Cheapest are Nano $0.41 and Flash Lite $0.59 (about 2–3 min).
- Cost efficiency, revenue per API dollar (Fig. 5b): Kimi-K2.5 is best; GLM-5 is about 10× better than Opus 4.6.

**Headline results**
- 12 models × 3 seeds = 36 runs. §4.1.
- Opus 4.6 averaged $1.27M, GLM-5 $1.21M, GPT-5.4 $1.00M. Gemini 3 Flash was about $394K. Seven of 12 models finished below the $200K start. Greedy bot: Fig. 7 shows it near the bottom.
- Per Table 4, 14 of 36 runs went bankrupt (my sum). The paper's own bankrupt-run counts are in the "Bankrupt" column: Sonnet 4.6, Qwen 3.5, Gemini 3.1 Pro, GPT-5.4 Nano, Grok 4.20 and GPT-5.4 Mini each 2/3.
- Failure modes (§4.2, §5, Fig. 5a):
  - Failing to identify adversarial clients.
  - Assigning incapable employees.
  - Over-committing employees (Sonnet averaged 7.2 concurrent tasks).
  - A "reasoning-execution gap": rules written to the scratchpad and then ignored. Sonnet's notes recorded a balance of $152K while the real balance was −$3K.

**Validity safeguards**
- Deterministic environment with hidden but fixed adversarial status, 3 seeds.
- Novelty "immune to pretraining contamination" (§2, a claim without a test).
- Open-source and configurable.
- Caveats listed by the authors (§6): no hiring or firing, no random exogenous shocks, numeric rather than natural-language signals.

**Text inconsistencies found**
- §4.2 cites "Figure 1" for the averaged trajectory; it is Figure 2.
- Kimi-K2.5's average is shown as $409K in Fig. 2 and $401K in Fig. 7.
- The abstract's "47% of bankruptcies" caused by adversarial detection: ⚠️ I found no supporting breakdown in the body. Fig. 5a breaks down *failed tasks*, not bankruptcies.
- §4.2's "4 of 10 models across 6 of 30 runs" uses different denominators from the 12 models and 36 runs.
- The related-work text claims a "multi-episode learning framework", but ⚠️ I found no such experiment in the paper.

---

## 4. Business Arena (arXiv 2608.08621)

**Identity**
- Title: "Business Arena: Benchmarking LLM Agents in a Realistic Marketplace".
- Version v1 [cs.AI], 9 Aug 2026.
- Authors: Yijun Pan (intern at Accio, Yale), Yukun Lian and others. Corresponding author Xiaoying Xing. Accio Team, Alibaba Group.
- Code: ⚠️ none found. Only a project page, https://business-arena.site.accio.ai.

**Horizon and step**
- A pre-opening setup phase plus 30 simulated operating days. One simulated day is advanced by the agent calling `end_round`. App. A.
- The 30-day calendar "represents one real-world year", with festivals placed by real date. App. C.
- Autonomous run in an OpenClaw sandbox with no evaluator-set turns. App. A.
- Calls per run: 194 to 8.0k (Fig. 4, "Arena calls").
- Message or turn cap: ⚠️ none found.

**Decisions (more than 60 tools, App. A Table 2)**
- Market intel, trends, calendar and tariff events.
- Catalogue, store focus, setup.
- Supplier catalogue, flags, quote requests and purchases.
- Loans (`borrow`, `repay_loan`), factoring (`factor_ar`), payables and inventory liquidation.
- Listings, price tiers, ad budgets.
- Certifications and compliance status.
- Customer inquiries, RFQs, returns and disputes.
- Notes, a scriptable workspace, and `exec`.

**How money feeds back (App. F, Table 4 and App. E)**
- Start: $80,000. The "paper condition" is a mid-scale shop with $200/day overhead. Table 4, App. E.
- Fixed costs: $200/day plus 0.5% of on-hand inventory value per day.
- Platform commission 5–12% of gross, with volume discounts; a 9% rebate on eligible export orders.
- Landed cost = supplier + freight + tariff + compliance + selling cost. App. E.
- Lead time is per real supplier offer. Tariffs and tariff shocks (calibrated to US–China changes) change during the episode.
- Credit and loans:
  - Short-term loans compound at 0.15%/day, rising to 2.5× that when overdue.
  - Overdue supplier payables accrue 0.10%/day, capped at 30% of the invoice.
  - Invoice factoring converts eligible receivables to cash at a 5–18% discount, depending on maturity and buyer credit.
  - ⚠️ I found no stated credit limit on borrowing.
- Escrow and receivables exist, but their settlement delay is not given in the text I read.
- Spoilage: none. Inventory holding fees exist.
- Liquidation: inventory converts immediately at 85% of cost basis.

**What ends a run**
- After the final day, remaining inventory contributes at a salvage discount. §3.1.
- ⚠️ I found no bankruptcy or early-termination rule anywhere in the text.

**Score**
- Final net worth (in dollars) is the leaderboard metric. §4, §6.1.
- Formula (App. F): FinalAssets = cash + 0.97·escrow + 0.97·receivables + 0.85·inventory − payables − loans. This is "to prevent exploiting payment timing, unfinished escrow, receivables, or unsold inventory as free value".
- Compliance fines are cash deductions, so they feed the score.
- Skill-level diagnostic columns (Fig. 4, App. L), none of them part of the leaderboard:
  - Operating fluency: arena calls, world-check rate, call failures.
  - Capital deployment: capital utilization, holding cost.
  - Selling: sell-through, order margin, route cost, ad ROI, market share.
  - Customer interaction: buyer conversion, factual replies, RFQ success.
  - Compliance: fines.
- Reference lines: six expert-designed deterministic strategies using only agent-visible information (App. J). The best is the "Bayesian export compounder" at $436,195.

**Novel elements**
- **Compliance gating with fines.**
  - Selling in a market needs a certification, which costs fees and processing time.
  - For the k-th sale completed without the required permit: F_k = max($500, 0.15 × order value) × min(k, 5).
  - That is $500, $1,000, … capped at $2,500 per violation. Ten floor-level violations cost $20,000. App. E, §3.2.
  - Observed range: $0 for Fable 5 up to $51.8k average for MiniMax M2.5. Fig. 4, §6.2.
- **Customer-service honesty metrics.**
  - A "factual replies" rate: how often replies avoid materially false claims. Fig. 4, App. L.4.
  - "Reckless service" (unsupported claims and excessive concessions) gave a −39.2% margin against +43.1% for margin-safe service. App. G.
  - ⚠️ How factual support is judged is not described in the sections I read.
- **Capital-recycling and recovery tools.** Factoring, loans, payables and liquidation each carry an explicit cost, so recovery is "not free" (App. F). The FinalAssets haircuts (97% / 85%) penalise unfinished cycles.
- **Hidden supplier unreliability.** Suppliers may overstate quality or understate delivery time. Discrepancies show only after an order is delivered. The agent can view time-bounded due-diligence signals. App. B.
- **Dynamic wholesale price.** c_skt = c_sk0 × world adjustments each day. App. B.
- **Noisy evidence with rumors.** Events can have false precursors; Google Trends data is post-processed to correlate with the hidden oracle demand. §3.2, App. C.
- **Mechanism ablations as a validity check.** Nine mechanisms, each tested with an intended policy against a neglect policy and a misuse policy (App. G). Examples:
  - Evidence-guided sourcing $144,069 against $80,433 (cheapest-SKU only) and $65,816 (blind bulk buying).
  - Disciplined pricing $144,069 against $93,806 (static high markup) and $35,697 (near-cost).
  - Public demand evidence recovers the hidden demand ranking with correlation 0.972; fabricated evidence gives −0.039 and reversed gives −0.972.
- **Stateful save–fork–load.** The model context, OS workspace and marketplace are restored from a checkpoint. Used in a trace-search case study on one model: 5-day forking reached $108,878, against $93,268 for the best of six independent runs. App. K.
- **60 scripted NPC sellers per episode** from 10 archetypes, with daily repricing, restocking and, for mid-size and larger sellers, short-term credit. 10 are baseline NPCs "used for alpha computation". App. D. ⚠️ Alpha is not defined in the text I read.

**Ethics, honesty, welfare vs profit**
- Closest items are the compliance fines and the factual-replies rate. Both are agent conduct toward regulators and buyers.
- Only the fines move net worth directly. Factual replies matter through conversion and margin and are not a separate score.
- No worker welfare.

**Run cost**
- ⚠️ No token, dollar or wall-time figures found anywhere in the paper.

**Headline results**
- 15 models × 10 runs = 150 runs, one world seed. §6.1, App. H.
- Gemini 3.1 Pro had mean net worth $188,488 (9/10 runs preserved capital). GPT-5.6 Sol $168,867 (10/10), Fable 5 $164,204 (10/10), MiniMax M2.5 $20,856 (0/10). That is a 9.0× spread. Table 5.
- 51% of runs lose money against the $80K start. Four models preserved capital in every run. §6.1.
- Best expert strategy $436k is more than twice the best model mean.
- Failure patterns (§6.2, Fig. 4):
  - Idle capital (Qwen 3.7 Max deployed only 22.3% of starting capital).
  - Stranded inventory (MiniMax M3 turnover 0.36).
  - Sub-landed-cost pricing (M2.5, with 98 of 142 orders below landed cost in one trace).
  - Tariffs ignored.
  - Repeated unfixed compliance violations (DeepSeek V4 Pro, one run: 34 violations and $80,000 in fines).

**Validity safeguards**
- Ranking stability (App. H):
  - Split-half Spearman 0.898.
  - Same top-3 group in 98.7% of partitions.
  - ICC(1,10) = 0.944.
  - Model identity explains 64.8% of variance.
- Filesystem permissions keep the agent from the arena code, database and hidden state (§3.4, App. A).
- Mechanism ablations, above.
- Authors state that robustness across different world seeds "requires crossing models with multiple world seeds" and was not done (App. H.2).
- Limitations: cross-border B2B only; tools abstract away a live storefront (§7).

---

## COVERAGE STATEMENT

**E-Commerce Bench (2608.30730)**
- Read to the end: the main body, §1 to §5 (pp.1–21, from `Read` at lines 1–1349), including all of §3.2 to §3.7, §4, and the conclusion.
- Appendix material read in full or in the relevant parts:
  - App. A.1/A.2 (interface, context editing).
  - App. B.3 to B.5 and Table 7.
  - App. C.1 to C.7.
  - D.2 to D.5 and Tables 8 and 9.
  - E intro and E.1 to E.3.
  - H.1 task brief, and Tables 16 to 18 in part.
- ⚠️ Not read or only skimmed:
  - D.1 (kernel equations 10 to 18, only the first lines).
  - B.1 to B.2 detail tables.
  - E.4 to E.6 formula text (only the last lines of E.6).
  - Appendix F tables except the intro lines and Table 12.
  - Appendix G case-study transcripts (G.1 to G.4) and Fig. 30.
  - H.2/H.3 prompts (lines about 4060–4323).
- Searched for cost and wall-time statements by keyword search across the whole text: none found.

**CEO-Bench (2606.18543)**
- Read to the end, the whole text from line 1 to 2138: the main body and Appendices A to D.
- ⚠️ Figures and plots were read as text only. Several figure panels came through garbled (for example, the flipped y-axis labels).
- Link URLs were read from the PDF's annotations, not the visible text.

**YC-Bench (2604.01212)**
- Read to the end, the whole text from line 1 to 945: the main body and Appendices A to F.
- ⚠️ Fig. 6 (failure-moment panels) extracted as garbled characters and was not read.
- The multi-episode learning claim in §2 and the 47%-of-bankruptcies claim were not found backed in the body (see above).

**Business Arena (2608.08621)**
- Read to the end, the whole text from line 1 to 1749, including the main body and Appendices A to M.
- ⚠️ Image figures (Figs. 3, 5, 6, 7 to 10, 12 to 19) were read from captions and surrounding text only. I did not view them.
- The statement that no bankruptcy rule, run cost or code link exists is based on reading the full text and keyword searches. Appendix figures may contain more.

All other claims above are traced to the sections cited. No downloaded code was run.

---

# Report b-markets-auctions

# Financial-structure facts from four long-horizon agent benchmarks

All four papers exist and are what their titles say. No ID was wrong. Local copies: `/private/tmp/claude-501/-Users-ardaenfiyeci-worktrees-farm-eval-hen-cost/d6ba3112-405f-4e5c-baf1-1ddae93a3621/scratchpad/papers/b/<id>.pdf` and `<id>.txt` for 2604.05523, 2609.04667, 2605.14537, 2310.05746.

Page numbers are the PDF pages. I could not place Market-Bench items by printed page, so I cite section numbers there. Items marked "(inference)" are mine, not the authors'.

One finding up front. **None of these four papers has a cash account with a credit line, a monthly close, settlement delays, supplier-paperwork fraud, a charge for looking up information, or agent-chosen waiting.** Their money structure is thin. The closest things to FarmBench-style financial structure are the ones described under "novel elements" in each section.

---

## 1. Market-Bench (arXiv 2604.05523)

**Identity**
- Title: "Market-Bench: Benchmarking Large Language Models on Economic and Trade Competition" (p.1).
- Version: v2, dated 19 Apr 2026. The arXiv abstract page lists v1 and v2, so v2 is the latest. v1 was submitted 7 Apr 2026.
- Authors: Zheng, Duan, Zhang, Zhu, Min, Zhai. Affiliations: Shanghai Jiao Tong University and Shanghai AI Laboratory (p.1).
- Code: https://github.com/aiben-ch/Market-Bench (p.1). I did not open it.

**Horizon and step (§4.1, App. G Table 4)**
- 6 steps per episode, 20 LLM retailer agents, 2 bidding rounds per step.
- Each step is a procurement stage followed by a retail stage (App. A loop).
- 200 buyers per round. 8 items, 1,000 supplier units in total.
- LLM temperature 0.0. Results are the mean of 10 independent runs (§4.2).
- No message cap is stated.

**Decisions (§3.2–3.4, App. B)**
- Procurement: per item, a bid `{qty, price}` in a sealed-bid, multi-unit, first-price auction with a reserve price. Total spend must not exceed current funds, or the bid gets zero allocation (Eq. 4).
- Retail: an integer price per item, plus a short slogan of at most 25 words (App. B.2).
- Output is strict JSON.

**Money feedback**
- Starting cash is K_init = α·ΣQ_x·P_base / m = 1.5 × 300,000 / 20 = 22,500 per agent (§4.1, Eq. 8–9).
- Starting inventory is 0 (App. A).
- Winners pay their own bid price immediately at settlement (§3.2, App. A.1).
- Retail revenue is price × units sold. Buyers buy from the lowest-priced seller inside their "consideration set" (§3.3).
- Holding cost exists in the loop (App. A step h: "Apply holding costs and check for bankruptcy"). The default rate is 0.0 (Table 4).
- Not stated in the paper:
  - credit or loans
  - interest
  - delivery lag or settlement delay
  - spoilage
  - fixed costs
  - how unsold inventory is carried between steps beyond the inventory state variable

**What ends a run**
- The rule as written is "Funds_i < 0 ⇒ Bankruptcy" (§2.1). §3.5 says agents "avoid bankruptcy by maintaining nonnegative funds".
- The paper does not say what happens to a bankrupt agent. Removal from the market is not stated.
- Inference: the budget constraint in Eq. 4 and a 0.0 holding cost mean bankruptcy is almost unreachable in the default configuration. The "failure" the authors observe is agents becoming inactive. Active Ratio falls to about 0.4 (§4.3), and Qwen3 30B-A3B produced no valid bids in any run (§4.3).
- "All stress scenarios are disabled" in the experiments (§4.1). These are not described.
- Episodes end at step T = 6.

**Scoring (§3.5, App. C; Table 2)**
- Nine per-agent metrics. Higher is better unless noted:
  - Economic: Net Profit Margin (NPM), Cumulative Profit Π, Risk-Adjusted Return (RAR, mean per-step profit divided by its standard deviation).
  - Operational: Inventory Efficiency Index (IEI), Stockout Rate (lower is better), Bid Efficiency (won quantity over bid quantity, times base value over actual spend), Order Stability Index (OSI), Fill Rate.
  - Cognitive: Mean Match Score (MMS, the cosine similarity between slogan embedding and buyer persona).
- Per-step profit is Π = revenue − COGS − holding cost (App. C.1).
- There is no single headline score. Table 2 reports all nine columns.
- Market-level indices (Gini, Theil, CV, HHI, CR4, Active Ratio) are computed from logs (§3.6).

**Novel elements**
1. **Persona-Gated Attention (§3.3, App. E).**
   - A buyer sees only some retailers. The retailer's slogan is embedded (Qwen3-Embedding-8B) and compared by cosine similarity with a hidden buyer persona text.
   - Attention weight is `w = exp(λ·Sim/τ)`. The consideration set size is `min(|A|, max(1, ⌈ρ·Kmax⌉))` with Kmax = 20, τ = 1.0 and ρ = 0.6.
   - A retailer outside the set cannot sell, however low its price. Prices then compete only within each buyer's set.
   - Language therefore feeds revenue through a deterministic embedding computation, not an LLM judge.
   - Personas are hidden. Agents must infer them from public sales history (§3.1).
2. **First-price auction with a reserve price.** The authors chose it over second-price on purpose, because it forces bid shading (§3.2).
3. **Scarcity as a control knob.** Supply–demand ratio r = 0.95 (§4.1).
4. **Winner-take-most dynamics.** Wealth inequality rises (Gini 0.07→0.21) and procurement success predicts profit (Spearman ρ = 0.68 with BidEfficiency, 0.88 with FillRate, −0.88 with StockoutRate) (§4.3).

**Ethics, honesty, welfare**
- One of four buyer "tribes" is "Ethical" (weight 0.3, λ = 0.8, keywords green/fair/eco) (App. F Table 3, §3.3).
- That is a buyer preference for ethical-sounding slogans. Nothing checks whether a slogan is true, so honesty is not scored.
- Nothing else in the paper involves ethics or welfare.

**Run cost.** Not stated.

**Headline results (Table 2, §4.3)**
- Highest cumulative profit: Gemini 2.5 Pro Π = 36,589 (NPM 0.167). Gemini 2.5 Flash is next at 26,104 (NPM 0.190). Third is o3 at 13,368.
- o3 has the best Fill Rate (0.418) and OSI (1.000) but lower margin.
- Qwen3 30B-A3B has Π = 0 and BidEfficiency 0 in every run, because it never produced a valid bid. The authors attribute this to a formatting failure.
- ERNIE 4.5 21B is the only model with negative profit (−58).
- Slogans converge to a generic "Ethical-Hype" style; MMS correlates weakly with profit (ρ = 0.16).
- The authors say model scale is a poor predictor, citing Phi-4 14B beating all open models.

**Validity safeguards.** Limitations (p.8) list a single market configuration and a synthetic buyer model. The authors also warn that OSI and IEI mislead without conditioning on activity (§4.3). They replaced two unstable supply-chain metrics (ITR, Bullwhip ratio) with bounded ones (App. D). Full trajectories are logged and temperature is 0.

---

## 2. ERPBench (arXiv 2609.04667)

**Identity**
- Title: "ERPBench: Evaluating LLM Agents for Enterprise Decision-Making Across Competitive Market Ecologies" (p.1).
- Version: v1 only, dated 4 Sep 2026.
- Authors: Zhang, Lu, Ye, Liu. Affiliations: Shanghai Innovation Institute, Beijing Institute of Technology, Shanghai Jiao Tong University, GAIR Lab. The header reads "SII-GAIR".
- Code: the abstract says "Code and benchmark resources are available in our GitHub repository", but **no URL appears anywhere in the text**.

**Horizon and step (§3.1–3.2, §4.1)**
- 6 rounds of 30 simulated days each.
- 100 fixed problems, each with a seed, difficulty stratum, scenario category, initial operational state and market parameters (App. A).
- Two ecologies:
  - Solo: one LLM against five deterministic rule-based opponents (conservative, aggressive, balanced, growth-oriented, risk-averse).
  - Arena: six LLMs in one shared market.
- 6 model families, 1,200 model-level trajectories, 7,200 decision rounds. That is 600 Solo simulator runs plus 100 six-model Arena runs, 700 runs in all (§4.1).
- No message or step cap is stated beyond the six rounds.

**Decisions (§3.1)**
- A cereal-manufacturing firm with 12 SKUs across 3 distribution channels.
- Per round the agent returns JSON with:
  - SKU prices
  - production quantities
  - purchase orders
  - marketing allocation
  - finance actions
- Before deciding it may query tools for finance, inventory, market price, demand, raw materials and carbon information. No charge for the queries is mentioned.
- The simulator parses the action, checks feasibility, repairs or clamps infeasible fields, then executes.

**Money feedback (§3.1)**
- The only statements are these: the sim has "cash-flow and credit dynamics", "supplier lead times", "warehouse inventory", batch production with capacity and lot-size limits, and carbon costs.
- Demand uses a multinomial competitive interaction (MCI) model.
- "Finance actions can preserve cash viability but may not be available in every state."
- **Not given anywhere in the paper:** starting cash, credit terms, interest rates, lead-time lengths, carbon price, spoilage. The paper reads as a partial specification, so these likely sit in the code. I did not look.

**What ends a run**
- Only the six-round horizon is stated. **No bankruptcy rule is stated.** "Financial viability" is mentioned only inside the valuation (§3.2).
- Run-level failures exist ("experiment failed", 5 events in total, excluded from the audit chart) (App. C).

**Scoring (§1, §3.2, App. B)**
- The primary metric is terminal company valuation at the end of round 6, computed by a dividend discount model (DDM). It "aggregates profitability, financial viability, and expected future cash flows". The DDM formula and parameters are not given.
- Complementary reliability indicators:
  - mean within-problem rank
  - bottom-rank rate
  - normalized regret
  - task-level winner agreement
  - paired Δ = V_Arena − V_Solo, with Wilcoxon tests and Benjamini–Hochberg correction
- A "Decision Quality Pyramid" is explicitly *not* a composite score. Its five levels are:
  - L1 parser validity
  - L2 operational feasibility, an operational-reliability score of 1 − r_m / max r
  - L3 financial quality, rank-derived terminal performance
  - L4 disruption response, restricted to hard tasks
  - L5 short-horizon adaptation, the mean rank improvement from round 1 to round 6
  - L3–L5 are called descriptive proxies (§3.2).

**Novel elements**
1. **Paired ecology design (§3.2).** The same problem and seed is run against rule-based opponents (Solo) and against other LLMs (Arena). The headline finding is that the ranking changes: DeepSeek leads Solo at 252.29M and Gemini leads Arena at 263.95M (Table 1, §4.2). The two ecologies agree on the winner on only 21 of 100 problems (§4.5).
2. **Execution audit layer (§4.3–4.4, App. C).** Every proposed action is logged next to the interventions needed to make it executable. The categories are:
   - production-capacity skip, 3,761 events (82.5%)
   - unavailable investment, 355 (7.8%)
   - fallback decision, 275 (6.0%)
   - production-quantity clamp, 118 (2.6%)
   - traceback, 48 (1.1%)
   - experiment failed, 5
   - These are deliberately not summed into an error rate, and the authors say capacity skips may reflect a binding environment constraint rather than a bad decision.
3. **Infeasible-action handling.** Over-ordering under cash constraints and other infeasible actions are repaired or clamped rather than ending the run. The score is "qualified" by how much repair was needed.

**Ethics, honesty, welfare.** None. The environment has carbon costs (§3.1) as a cost item, not as an ethical trade-off.

**Run cost.** Not stated.

**Headline results (Table 1, §4.2, §4.6)**
- Solo: DeepSeek 252.29M, mean rank 1.67.
- Arena: Gemini 263.95M, mean rank 1.76.
- Gemini's bottom-rank rate falls from 22% in Solo to 0% in Arena. Its Arena–Solo gain is +94.54M (q = 1.28×10⁻¹⁵).
- Claude Opus 4.6 is last in both: mean rank 4.58 in Solo and 4.68 in Arena. Its Δ of −2.83M is not significant.
- The authors report no survival or bankruptcy rate.
- Failure modes: they say fallbacks and tracebacks indicate "output-pipeline or runtime fragility", and models with fewer logged interventions tend to have higher Arena valuations. They call this descriptive, with only six points.

**Validity safeguards (§4.1, §5, App. A–B).** They report:
- coverage, duplicate and missing-record checks (100/100 problems, no duplicates)
- matching of seed, difficulty and scaffold across ecologies
- bootstrap confidence intervals over problems

They warn about:
- service-side model routing, so labels are "not route-invariant"
- a fixed 100-problem slice and a single six-model Arena composition

---

## 3. Cattle Trade (arXiv 2605.14537)

**Identity**
- Title: "Cattle Trade: A Multi-Agent Benchmark for LLM Bluffing, Bidding, and Bargaining" (p.1). Published at the ICLR 2026 Workshop on MALGAI.
- Version: v1 only, dated 14 May 2026.
- Authors: Robert Müller and Clemens Müller (equal contribution). Contact robert@aganthos.com. **No affiliation is printed** in the header. Aganthos is inferred only from the email domain.
- Code: **no link appears in the text.** Footnote 1 only states the game is Ravensburger's trademark (Kuhhandel) and the work is unaffiliated.
- This is a tabletop card game (Kuhhandel), not an operations simulation. Its "money" is game cards.

**Horizon and step (§1, §3.1, §4.1, App. A)**
- 50–60 turns per game, 4 players (3–5 supported). Games run to deck exhaustion.
- 242 games in total: 60 pure-LLM tournaments, 168 mixed games (1 LLM vs 3 code agents), and 14 exploratory games.
- Settings: temperature 0.1, low reasoning effort, 4,096-token response limit, full scratchpad memory (about 300 tokens, with an extra LLM call each turn) (§4.1, App. C).

**Decisions (App. C action space, 7 types)**
- Turn choice: auction or "Kuhhandel".
- Auction bid, in multiples of 10, or pass.
- Auctioneer: sell to the high bidder, or exercise the "buy-right" (pay the high bid to keep the card).
- Trade challenge (TC) initiation: pick an opponent and animal, then choose exact face-down money cards, including 0-value cards for bluffing.
- TC defence: accept the hidden offer or counter.
- TC tie retry.
- Scratchpad update.

**Money feedback (§3.1, App. A, App. C)**
- Each player starts with 90 coins: four 10s, one 50, two 0s.
- Money is discrete non-fungible cards with **no change given**. Paying 60 with a 100 card costs 100. A dynamic-programming routine picks the minimum-overpay card set.
- "Donkey" draws inject cash into all players (50/100/200/500 for the 1st to 4th donkey), so early game is cash-constrained and late game freer.
- Buy-right: the auctioneer can pay the high bid to keep the card, which ties bidding strategy to future liquidity (§1).
- Settlement is immediate. There is no credit, interest, lag or spoilage.
- Overbidding is allowed by design in "canonical" mode. The first overbid reveals the player's total wealth to all and restarts the auction. A **second overbid in the same auction eliminates the player from that auction** (App. C Table 4, D.5). The paper does not say this ends the game for that player.

**What ends a run**
- The game ends when the deck is empty and no TC is possible (Fig. 1 caption).
- There is no bankruptcy rule. "Bankrupt TC initiation" is only a behavioural label for starting a challenge with nothing to offer (§4.5).

**Scoring (Eq. 1, §3.1, §3.2, App. B.1)**
- Final score `S = (Σ values of completed quartets) × (number of quartets)`. The multiplication rewards breadth: three mid-value quartets beat two top ones.
- Head-to-head ranking uses TrueSkill (μ, σ).
- Diagnostic metrics:
  - Capital efficiency η = score ÷ gross coin outflow
  - TC bargaining tightness τ = Σ(loser's offer + 10) ÷ Σ winner's offer
  - bid aggressiveness
  - buy-right %
  - TC-accept %
  - bluff %
  - self-bid %
  - overbid %
  - win rate
- Cost per quartet is also reported.

**Novel elements**
1. **Multiplicative scoring, so the final score depends on portfolio composition (§3.1).** η can exceed 1 because free wins and the multiplier amplify returns (§4.3).
2. **Cash as scarce lumpy objects with no change (App. C).** Overpaying is a real cost, and there is a "wealth revelation" penalty (§3.2).
3. **Hidden-offer bargaining (§3.1).** Face-down offers make a 0-value bluff possible.
4. **Deterministic code-agent baselines (§3.3).** TrackerAgent, SetRaceAgent and EconomyAgent give a calibration floor. TrackerAgent and SetRaceAgent beat most LLMs (§4.2–4.3).
5. **Per-failure behavioural analytics, not just a score.** Overbid rate, self-bidding (G2.5-FL, DS-v3.2 and GPT5.4-N self-bid in over 74% of rounds), and phase adaptation are measured (§4.4).

**Ethics, honesty, welfare.** Deception is a core, rewarded mechanic: the 0-value bluff is a legal move and is never penalised. The paper cites MACHIAVELLI as related work on reward-versus-ethics trade-offs (§2) but measures none.

**Run cost (§4.6, App. B)**
- Token usage varies about 20× across models.
- Gemini 3 Flash uses about 275,000 completion tokens per game, and Gemini 3.1 Flash Lite about 14,800.
- Dollar and wall-clock cost: not stated.
- Format errors are below 1% for every model.

**Headline results (§4.2–4.3, Fig. 1b)**
- Ranking by TrueSkill μ on the 98-game canonical slice:
  - Gemini 3 Flash 30.1 (72.9% wins, median score 5,250)
  - TrackerAgent 28.7
  - Gemini 3.1 Flash Lite 28.0
  - SetRaceAgent 27.3
  - Sonnet 4.5 26.4 (n = 14)
  - DeepSeek v3.2 23.9
  - GPT-5.4 Nano 22.6
  - EconomyAgent 22.1
  - Haiku 4.5 21.8
  - Gemini 2.5 Flash Lite 20.5
- Gemini 2.5 Flash Lite has the highest overbid rate (1.20%) and finishes last (§4.4).
- Gemini 2.5 Flash Lite once challenged for a goose with no money (§4.5).
- All seven LLMs are "cost-efficient" models at low reasoning effort, which the authors list as a limitation (§5).

**Validity safeguards (§4.1, §5).** Canonical-mode rules are faithful to the tabletop game. Pure-LLM and mixed formats are both run. Sonnet's results are flagged as wide because of small n. The authors admit that behavioural metrics are point estimates without confidence intervals, and that deck-order variance dominates seat-position variance.

---

## 4. "Put Your Money Where Your Mouth Is" / AucArena (arXiv 2310.05746)

**Identity**
- Title as above. The suite is called AucArena (p.1).
- Version: v4, dated 25 Aug 2024. The abstract page lists v1 to v4, so v4 is the latest. v1 was submitted 9 Oct 2023.
- Authors: Chen, Yuan, Ye, Majumder, Richardson. Affiliations: Fudan University and Allen Institute for AI (p.1).
- Project page: https://auction-arena.github.io (footnote 2, p.1). I did not open it.

**Horizon and step (§3.1, §4.1)**
- A single auction session. The default is 10 items: 2 items at each of 5 starting prices from $1,000 to $5,000.
- Open ascending-price (English) auction, run item by item. In each bidding round every non-leading bidder either raises or withdraws.
- Standard Competition: 3 bidders, 2 fixed baselines (GPT-4-Turbo and GPT-3.5-Turbo) plus 1 challenger.
- 6 settings: budget $20,000 or $40,000, crossed with random, ascending or descending item order.
- 10 repeats per experiment, temperature 0 (§4.1).
- Prompt length averages 1,500–1,800 tokens; the longest is about 5,000 (§4.1).
- Minimum bid increment is 10% of the starting price (§4.1).

**Decisions (§3.2)**
- Four LLM-prompted functions in a Belief-Desire-Intention agent: plan, bid (raise or withdraw), belief update, replan.
- Each plan gives every remaining item a priority score of 1, 2 or 3 (§3.3).

**Money feedback (§3.1, §3.3, §4.1)**
- A fixed budget per bidder ($10K, $20K, $30K or $40K in different experiments). There is no replenishment, credit or interest.
- Item true value (resale value) = 2× starting price. Bidders see only an estimate that is 10% too high, which builds in the winner's curse (§3.3).
- Profit = true value − winning bid. A failed bid costs nothing, but a win above true value gives negative profit (§3.1).
- Settlement is immediate and the auctioneer enforces budgets.

**What ends a run.** The last item is sold. There is no bankruptcy or elimination. The budget constraint is hard and enforced, so overspending is impossible. "Failed bids" (below the previous bid or above budget) are counted as an error metric, and the auctioneer corrects them (§4.2).

**Scoring**
- Primary: **TrueSkill** across games, a ranking by total profit (§4.1). The Figure 2 values are in a chart that did not extract as text, so I have no numbers for them.
- Secondary (§4.2–4.3):
  - Corrected Failure Rate, CFR = F/(C+F), for failed bids and belief errors
  - Bid Increment Percentage (BIP)
  - Spearman correlation between a plan's priority score and actual bids and wins
  - average profit for the human comparison (App. B.1)

**Novel elements**
1. **Winner's curse built in (§3.3).** A 10% overestimate means "apparent victories" can be real losses. It explicitly tests risk management.
2. **Item-order manipulation (§4.2–4.3).** Ascending, descending or random order tests whether the agent saves budget for later items. GPT-4 does this and most others do not.
3. **Plan-versus-action faithfulness (§4.3, Table).** Priority scores are generated by the LLM and correlated with bids and wins.
4. **Module ablations (§4.4, Fig. 7).** Adaptive (replans), Static (plan only), and None. A static plan is sometimes worse than none, especially with the $40K budget.
5. **Multi-objective niches (§4.4, Fig. 8).** "Profit bidders" and "item bidders" with different objectives specialise in expensive versus cheap items as budgets grow.
6. **Human comparison (App. B.1).** 4 graduate-student players, paid above local minimum wage. Humans beat the models in structured (ascending and descending) orders. GPT-4-Turbo beat humans on average profit in random order.
7. **Rule bidder baseline (§4.1).** It has a fixed engagement limit and raises by 10%. It "surpass[es] most LLMs in most settings" (§4.2).

**Ethics, honesty, welfare.** None. Objectives are profit or item count only.

**Run cost.** Only the prompt token lengths above. The authors note that budget limits prevented testing other instruction designs (App. A.2). Dollar and wall-clock cost: not stated.

**Headline results (§4.2–4.3)**
- GPT-4 is generally the highest-scoring LLM. Gemini and Mixtral are competitive.
- The rule bidder beats most LLMs.
- GPT-4's corrected failure rate is the lowest, 0.21%.
- GPT-3.5-Turbo withdraws too often; Mistral-7b sometimes suffers the winner's curse.
- LLaMA-2-13b withdraws every time, so it has no failed bids.

**Validity safeguards.** The paper:
- uses artificial item names to avoid information leakage (App. A.3)
- repeats experiments 10 times at temperature 0
- fixes the baselines and varies one challenger
- has the auctioneer correct belief errors so planning is measured separately
- includes a human comparison

It has no limitations section that I found. The authors say their conclusions are limited by prompt-engineering budget (App. A.2).

---

## Cross-paper summary against the "novel elements" list

| Element | Market-Bench | ERPBench | Cattle Trade | AucArena |
|---|---|---|---|---|
| Cash account with credit line | No | "credit dynamics" mentioned, no terms (§3.1) | No | No |
| Monthly close / statement | No | 30-day rounds, no statement | No | No |
| Settlement delay | No (immediate) | Supplier lead times, no lengths | No | No |
| Fraudulent supplier paperwork | No | No | No | No |
| Survival pressure | Funds < 0 = bankruptcy stated (§2.1), practically unreachable, no handling given | None stated | Per-auction elimination only | None |
| Net-worth-like score | Cumulative profit and NPM | DDM terminal valuation | Quartet score formula | Profit via TrueSkill |
| Cost of information | No | No cost for tool queries | No | No |
| Agent-chosen waiting | Implicit (can skip bids) | No | Pass on bid | Withdraw from bid |

The distinctive structural ideas, with their sections:
- Market-Bench §3.3: text decides who can see you.
- ERPBench §3.2 and §4.4: the same task is run against two kinds of opponent, with an audit of how much repair each action needed.
- Cattle Trade §3.1 and App. C: lumpy no-change cash and a multiplicative score.
- AucArena §3.3: a built-in 10% overestimate (winner's curse) plus item-order effects on saving budget.

---

## COVERAGE STATEMENT

**Market-Bench (2604.05523)**
- Opened: PDF downloaded (14 pages) and converted with pdftotext; the text file is 853 lines.
- Read to the end: all of the main body (§1–5, Limitations) and all appendices A–I (simulation loop, prompts, metric definitions, PGA mechanism, persona configuration, config table, supplier offers, model list).
- ⚠️ Figures 3–7 are charts. I read only their captions and the prose describing them, not the plotted values.
- ⚠️ I did not open the GitHub repository. The paper does not say how revenue is credited within a step, or what happens to a bankrupt agent.
- ⚠️ The dollar-per-run and wall-clock cost are not in the paper.

**ERPBench (2609.04667)**
- Opened: PDF downloaded and converted; the text file is 560 lines (the PDF page count was not shown).
- Read to the end: the whole paper, including App. A–C.
- ⚠️ Figures 1–6 are charts. I read only captions and prose.
- ⚠️ The paper contains no simulator specification (starting cash, credit terms, DDM formula, carbon price, lead times, bankruptcy rule). I could not check any of these without the code, and the GitHub URL is not in the text. I did not look for it.

**Cattle Trade (2605.14537)**
- Opened: PDF downloaded (10 pages; the text file is 1,925 lines because of figure text).
- Read to the end: main body §1–6, App. A (rules), App. B.1 (metric definitions), App. C (architecture and error handling), App. D.1–D.10 (prompts).
- ⚠️ Skimmed: App. B figure pages (Figs. 4–10, pages 13–18, roughly lines 960–1520), which are mostly chart text. I extracted the prose lines and captions only.
- ⚠️ No code link was found in the text. Dollar cost and wall time are not stated.
- ⚠️ The rule that a second overbid eliminates a player is stated only for that auction. The paper does not say whether elimination persists beyond it.

**AucArena (2310.05746)**
- Opened: PDF downloaded and converted; the text file is 1,441 lines.
- Read to the end: main body §1–5 and the reference list.
- Appendix: A.1 (log), A.2 (opening of the prompts), A.3, B.1 (human performance), B.2 and B.3 prose, and the Fig. 10–13 captions.
- ⚠️ Read only part of the Listing 2 prompt text in A.2 (lines 893–935 plus the priority-score fragment). The remainder of the prompts was not read.
- ⚠️ Figure 2's TrueSkill values are plotted as bars and the text extraction did not recover them. I report no TrueSkill numbers.
- ⚠️ Figures 4, 9, 10–13 are heatmaps and charts. I read only captions and prose.
- ⚠️ I did not open the project page.

I read and cited every fact above from the local text files. For the numbers, two checks against the source are cheap: Market-Bench Table 2 (lines 277–302 of its text file) and ERPBench Table 1 (lines 263–272 of its text file).

---

# Report c-commons-ethics

# Extraction report: how four long-horizon agent benchmarks handle money, resources and "doing right"

Saved files are in `/private/tmp/claude-501/-Users-ardaenfiyeci-worktrees-farm-eval-hen-cost/d6ba3112-405f-4e5c-baf1-1ddae93a3621/scratchpad/papers/c/`. "L123" means line 123 of the named .txt file in that folder.

**Quoting rule.** I paraphrase and give section numbers and line numbers instead of quoting. My instructions cap me at one short quote per response, so none appear here. Formulas are restated mathematically.

**IDs checked.** All three arXiv IDs exist and match the named papers. The Anthropic page loaded. The "Vending-Bench Arena" page is not linked from the Anthropic post. It is linked from andonlabs.com and from the Vending-Bench 2 page. The Anthropic post itself links to https://andonlabs.com/evals/vending-bench-2.

---

## 1. GovSim, "Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents"

**Identity.**
- arXiv 2404.16698, v4, 8 Dec 2024 (the latest version served).
- NeurIPS 2024.
- Authors: Piatti, Jin, Kleiman-Weiner, Schölkopf, Sachan, Mihalcea (ETH Zürich, MPI Tübingen, Toronto, UW, Michigan).
- Code: https://github.com/giorgiopiatti/GovSim (footnote 1, p.1).
- File: `2404.16698.txt`.

**Horizon and step (§2.2–2.3, §3.1; L214–253, L310–313).**
- One run is 12 months. Each month is one step.
- Five agents per run.
- Five random seeds per model per scenario.
- Temperature 0.
- Three scenarios with mathematically equivalent dynamics: fishery, pasture, pollution.

**Decisions.**
- Each month each agent privately chooses how much to harvest (0–100 units). Choices are revealed simultaneously (§2.3, App. B.1).
- Agents then hold a free-text group discussion.
- Agents also run a strategy/reflection phase (App. B.1, Fig. 6).

**Resource and money feedback (§2.2–2.3; App. C.1, L1012–1027).**
- Starting stock is 100 units (100 tons of fish, 100 hectares of grass, 100% unpolluted water).
- Regrowth: whatever is left at month end doubles, capped at 100.
- The fishery prompt pays $1,000 per ton caught. The prompt tells each agent to optimise long-run income (App. C.1). The "Gain" metric counts units, not dollars.
- Sustainability threshold f(t) is the largest total extraction x such that g(h(t) − x) ≥ h(t), where g is the regrowth function (§2.3). With 5 agents and 100 tons that is 10 tons each per month.
- There are no delays beyond one month, no costs, and no cash account.
- If demand exceeds stock, units are allocated at random (App. B.1).
- A "moderator" can reveal each agent's harvest to the others ("transparent harvesting report") (App. B.1).

**What ends a run (§2.3, §2.4).**
- The resource collapses when stock falls below C = 5. After that nothing can be extracted.
- The cap is T = 12 months.
- ⚠️ The text says collapse is "below C" (§2.3) but the survival-time metric uses "above C" (§2.4). The boundary at exactly 5 is unclear.

**How skill is scored (§2.4, Eq. 1–3; L254–294).** The authors say no single scalar works, so they report six metrics.
1. Survival time m: the longest period during which the stock stays above C.
2. Survival rate q: the share of runs with m = 12.
3. Total gain R_i: the sum of an agent's harvests over the run.
4. Efficiency u: 1 − max(0, T·f(0) − ΣR) / (T·f(0)). Maximum is 100%.
5. Equality e: 1 minus the Gini coefficient of the agents' total gains.
6. Over-usage o: the share of actions that exceeded the sustainability threshold, computed over the surviving months.
- ⚠️ Gain tables show 20.0 for month-1 collapse and a maximum of 120, with efficiency equal to gain/120 (Tables 1, 4–6). That implies "Gain" is a per-agent mean. The text does not say so; this is my inference.

**"Doing right" versus "earning more".**
- There is no ethics label.
- The trade-off sits inside the commons: taking more now raises Gain and risks collapse. Over-usage counts the non-sustainable actions.
- Cooperation is "optimized" when total gain, efficiency and survival time are all high (§3.2).
- The paper says its prompts were written not to prime cooperation or greed (§3.1).
- Scores are not combined into one number.
- The "greedy newcomer" test (§3.3, App. D.4) adds an agent told to maximise its own money and ignore the others' welfare. That agent is also told it may break rules, and has no knowledge of the village norms.
- The paper frames "exceptions to norms" (one agent facing serious harm unless it over-takes) as future work (§5, L626–630).

**Design elements beyond a cash account.**
- Collapse is irreversible. It is the survival-pressure element.
- Communication is ablated: no communication raises over-usage by about 22% (§3.5).
- The universalization nudge adds "if everyone takes more than f(t), the resource will shrink" to memory (§3.4).
- Four sub-skill tests of 150 templated problems each are correlated with survival time (§3.7, App. F).
- No net worth, no delayed settlement, no paperwork.

**Results and failure modes.**
- Best survival rate is 53.3% (GPT-4o, Table 1). The abstract says "below 54%".
- Claude-3 Opus 46.7%, GPT-4-turbo 40.0%, Qwen-110B 20.0%, GPT-4 6.7%. All other models 0.0%.
- Small models collapse the resource in month 1. Survival time is 1.0 and gain 20.0 for several (Table 1).
- Universalization raises mean survival time by about 4 months, gain by 29 units, and efficiency by 24% (§3.4).
- The newcomer drops GPT-4o's survival rate from 53.3 to 33.3 (§3.3).
- Models do better on the fishery than on pasture and pollution (§3.2, App. D.2).
- Models choose a sustainable action in isolation at most 30% of the time (§3.7).
- The stated mechanism of failure is an inability to simulate long-run effects of greed on the group (abstract, §1).

**Cost.**
- One 12-month run costs about $0.30 (Haiku), $4 (Sonnet), $20 (Opus), $0.50 (GPT-3.5), $30 (GPT-4), $11 (GPT-4-turbo), $5 (GPT-4o). Basis is 680k input and 124k output tokens (App. D.1, Table 3).
- Total API spend was $1,500.
- Open-weight runs take about 4 hours per run. Sub-skill evaluation takes about 24 hours.

**Validity safeguards.**
- Seeds and temperature 0, with a stated caveat that inference kernels are not fully deterministic (App. D.1).
- Identical instructions across models.
- Utterance classification by GPT-4-turbo was checked against 100 hand labels at 72% agreement (§3.6).
- Stated limitations: simplified scenarios, small groups (§5).
- No discussion of contamination or exploits. I searched for it and found none.

**Discrepancies noted.**
- Intro says communication cuts over-use by 21% (L116). §3.5 and the conclusion say 22%.
- ⚠️ The main text refers to Appendix G (dialogue examples, L373, L540). The v4 PDF has no Appendix G. It ends at F plus the NeurIPS checklist.

---

## 2. MACHIAVELLI, "Do the Rewards Justify the Means? Measuring Trade-Offs Between Rewards and Ethical Behavior in the MACHIAVELLI Benchmark"

**Identity.**
- arXiv 2304.03279, v4, 13 Jun 2023.
- ICML 2023 (PMLR 202).
- Authors: Pan*, Chan*, Zou*, Li, Basart, Woodside, Ng, Zhang, Emmons, Hendrycks (UC Berkeley, Center for AI Safety, CMU, Yale).
- Code and labels: https://aypan17.github.io/machiavelli (L135–137).
- File: `2304.03279.txt`.

**Horizon and step.**
- 134 choose-your-own-adventure text games from choiceofgames.com, 572,322 scenes, 4,559 achievements, 2,861,610 annotations (Table 1, L144–146).
- One step is one scene. The agent picks one action from a list.
- ⚠️ The paper gives no per-game or per-run length, step cap or episode cap. Only "tens of thousands of tokens" of dependency is mentioned (§2.1). 572,322 / 134 ≈ 4,270 scenes per game is my arithmetic, not a paper figure.
- LM agents see only the current scene, with no memory of earlier scenes (App. H, L1536–1538). RL agents were trained for 50k steps (§3.1).

**Decisions.**
- Pick a numbered action.
- The agent cannot decline to act (App. H).
- Actions include lying, killing, stealing and so on.
- Branches open and close based on prior choices (Fig. 2).

**Resource and money feedback.**
- There is no cash or resource stock under the agent's control.
- The score is "points" from achievements the authors of each game defined (§2.1, §2.5).
- Money appears only as an annotation. GPT-4 labels each scene's "economic impact" of the player's action on a 0–3 scale: 0 none, 1 under $1k, 2 $1k–$1M, 3 over $1M (App. F.2.2).
- Each game's own state variables (money, debts, health and so on) are classed into power categories (App. C.2, Table 6).
- There are no explicit regeneration rules or delays. Consequences are story-driven and delayed (unlockable betrayals; §2.1).

**What ends a run.**
- ⚠️ The paper does not say how a game ends beyond the story ending. No collapse, bankruptcy or step cap is stated.

**How skill is scored (§2.2–2.5, Table 2).**
- Reward: sum of achievement points, reported as normalised reward = points / total possible points (§2.5).
- The agent sees achievements, not harm labels (§2.5).
- Ethical violations: count of scenes where a violation indicator is 1 (§2.2). There are 13 categories (Table 7, App. F.2.3): deception, killing, physical harm, non-physical harm, intending harm, manipulation, betrayal, stealing, trespassing, spying, vandalism, unfairness, other.
- Vandalism explicitly includes depleting or polluting others' resources.
- Disutility: count of scenes where the mean utility of other characters is below 0. Utility is labelled from −3 to +3 per stakeholder (App. F, Table 7).
- Power: mean exercised power across four units (watts, money, wellbeing, social influence) (§2.3, App. C). Reported as Economic, Physical, Social, Utility power.
- Behaviour score = harms committed by the agent / harms of a random agent × 100. The random baseline is the mean of 1,000 sampled trajectories. Lower is better, 0% is best possible (§2.5).
- Test set: 30 of 134 games, chosen because reward-maximising agents do badly there. Points and harms are positively correlated in those games (§2.5, App. G).

**"Doing right" versus "earning more" (the closest match to FarmBench).**
- There is no combined score. The tension is shown as a Pareto plot of harm reduction against reward (§5.2, Fig. 5).
- Reward-maximising RL agent (DRRN): normalised reward 35.2, all-violations 108 (more harm than random). Random: 18.0 and 100.
- GPT-4 + CoT: reward 27.4, violations 90. Adding an ethics prompt: reward 24.7, violations 82 (Table 2).
- Reading: moral steering lowers harm and also lowers reward. The authors say it is "mixed". Regularisation also reduces reward (§4.2).
- Only 23.3% of the oracle's points come from achievements that conflict with the moral instruction. 76.7% do not conflict (Table 5, §5.1).
- Ethics prompting lifts the share of GPT-4's points that come from moral achievements from 83.0% to 90.7%. That is mostly because immoral-achievement points fall from 4.3 to 2.4 (§5.1).
- Prompting a model to simply do no harm is described as untenable, because a model that refuses to act cannot collect reward (§4.2, L474–479).
- A "no goals" variant (ethics prompt, achievements removed) is reported in App. K, Tables 9–10.
- Scaling does not fix it. GPT-4 variants are not Pareto improvements over GPT-3.5 variants (§4.2).

**Design elements.**
- Labels are produced by GPT-4, not humans. Label quality was checked against an ensemble of three expert authors on 2,000 sampled scenes, with Spearman correlation (Table 8).
- GPT-4 labels beat the average crowd worker. The final labelling scheme beats a 3-crowd ensemble in 16 of 18 label types (§2.4, App. F.2).
- Human annotation would have cost over $500,000 and over 20,000 hours (App. F, L996–1000).
- No cash account, no net-worth scoring, no paperwork.

**Run cost.** ⚠️ Not stated for agent runs.

**Validity.**
- Test set picked where harm and reward correlate (§2.5). That is a selection effect worth knowing.
- Label false positives are higher than false negatives. The authors relabelled positives with an ensemble to compensate (App. F.2).
- ⚠️ No contamination discussion. These are public games, and I searched the text and found none.
- ⚠️ Table 2 gives Random normalised reward as 18.0 but Table 9 gives 18.4. Table 9 has a typo ("1.09") for DRRN social power.

---

## 3. EconEvals, "EconEvals: Benchmarks and Litmus Tests for Economic Decision-Making by LLM Agents"

**Identity.**
- arXiv 2503.18825, v4, 18 Feb 2026.
- Authors: Fish, Shephard, Li, Shorrer, Gonczarowski (Harvard; Penn State).
- Code: https://github.com/sara-fish/econ-evals-paper (footnote 2, L139).
- File: `2503.18825.txt`. The PDF has 114 pages. The main body ends on p.36.

**Horizon and step (§3, L281–287; §4.1, L617–628).**
- Benchmarks: 100 periods per run. A period ends with one action: a plan, an assignment, or a set of prices.
- 12 random instances per environment per difficulty (Basic/Medium/Hard).
- Chat history resets each period. A persistent notes tool carries memory (§3.2, App. M).
- Efficiency vs Equality litmus test: N = 30 periods, 4 workers, 18 instances (§5.2.2, L1547).
- Patience vs Impatience is single-shot queries, 20 repeats each.
- Collusion litmus test: 300 periods, 21 runs (App. J.2).

**Decisions.**
- Procurement: choose a purchase plan of deals within a budget.
- Scheduling: submit a worker–task matching.
- Pricing: set prices for n = 1, 4 or 10 products.
- Efficiency vs Equality: assign workers to tasks each period.
- Patience vs Impatience: choose $100 now or $X later.
- Collusion: set a price.

**Money and resource feedback.**
- Procurement (§3.3.1): fixed budget B. Feedback is "workers supported" by the plan, or an infeasibility notice if over budget. Effectiveness scores are hidden. The optimal plan uses at least 95% of the budget (§4.3.4).
- Pricing (§3.3.3): nested-logit demand with hidden quality, price sensitivity and outside-option parameters. Price sensitivity drifts over time (linear or sinusoidal). Feedback is quantity sold and profit per product, with a one-period lag. n = 1, 4, 10 for Basic/Medium/Hard. Costs ~ Unif[1,10].
- Scheduling (§3.3.2): feedback is k randomly chosen blocking pairs (instability problems with the matching).
- There is no cash account carried across periods, no delayed settlement, no bankruptcy.

**What ends a run.**
- Fixed 100 periods.
- Scheduling also ends early if the matching is stable (§3.3.2).
- No collapse or bankruptcy rule.

**How skill is scored (§3.3).**
- Procurement: workers supported by the best plan proposed / optimum (solved by an ILP).
- Scheduling: 1 − (blocking pairs in the final matching / expected blocking pairs of a uniformly random matching). It can go negative. A final-attempt instruction is added in period 100.
- Pricing: total profit in the last 50 periods / optimal profit in those periods.
- Scores are scaled so 100 is perfect.

**"Doing right" versus "earning more" (litmus tests, §5).**
- A litmus test has conflicting objectives and gives a litmus score (where the model lands), a competency score (can it do either single objective alone), and a reliability score (is the choice consistent).
- The framework deliberately does not say which answer is "right". It measures behaviour rather than specifying one target (§2, L266–268).
- Efficiency vs Equality (§5.2): the system prompt gives two goals with no weighting: maximise company revenue, minimise differences in workers' total pay (L1525–1527).
- Pay is proportional to task size. Revenue depends on putting high-productivity workers on large tasks.
- Parameters: N = 30, n = 4, w = 1, p = 18, M = 1800. Equalising pay costs roughly 30% of revenue (L1547–1550).
- Litmus score per run = the run's position between the max-equality point and the max-efficiency point on the (revenue, pay-gap) frontier, projected onto the line and clipped to [0,1]. 0 means equality, 1 means efficiency (L1553–1570). Pay gap = max − min worker earnings.
- Competency = average of two ratios: revenue under an efficiency-only prompt divided by highest possible revenue, and 1 − (pay gap under an equality-only prompt / highest possible gap) (L1581–1590).
- Reliability = 1 − standard deviation of litmus scores across runs (L1599–1600).
- Patience vs Impatience: litmus score = the implied annual interest rate that best fits the model's choices (§5.1.2, App. I). Reliability = 1 − L1 distance from the ideal step function.
- Collusion (App. J.3): litmus score is where the last-50-period average price sits between the Nash price (0) and the jointly profit-maximising price (1). ⚠️ The exact formula did not survive text extraction. The "1 = more collusive" direction is stated in the text.

**Results (litmus).**
- Table 3 (L1788–1805):
  - Efficiency-vs-Equality litmus scores: Gemini 3 Pro Preview 0.69; every other model under 0.35.
  - Claude 4.5 Opus 0.01, Claude 4.5 Sonnet 0.10, GPT-4.1 0.00, GPT-5 0.23.
  - Competency is about 0.90 or above for all models except Gemini 1.5 Pro (0.71).
  - Four models have reliability below 0.80, including Claude 4.1 Opus (0.65) and Claude 4.5 Haiku (0.67). They tend to pick extreme allocations (§6.2).
- Efficiency-vs-Equality litmus scores track political-bias measures (§6.4). The authors treat this as an early generalisation check, not proof.
- Patience results are robust to 36 prompt variants (names). The model explains 97.9% of variance in litmus score (§6.3).

**Results (benchmarks).**
- Hard-difficulty scores (Table 4, L2360):
  - Procurement: Gemini 3 Pro Preview 99.6, GPT-5 75.6, GPT-4o 9.0.
  - Scheduling: GPT-5 90.5, Gemini 3 Pro Preview 86.1, GPT-4o 3.2.
  - Pricing: Gemini 3 Pro Preview 71.9, GPT-4.1 66.8, Gemini 1.5 Pro 39.1.
- Newer models score higher: about +41, +50 and +18 points per year for procurement, scheduling, pricing at Hard (§4.2.1).
- Pricing: the best model tracks the drifting demand. GPT-5 explores locally and adapts less (§4.3.2).
- Reasoning models do better on budget bin-packing (§4.3.4).
- Newer reasoning models explore more. Exploration rate did not clearly relate to score (§4.3.4, App. F).

**Validity safeguards.**
- Synthetic, randomly generated instances with difficulty scaling.
- A greedy baseline for scheduling (Knuth heuristic) scores 76.0 on Hard (App. H.1).
- Competency baselines above 90% for greedy policies in Efficiency vs Equality (App. H.2).
- Prompt-variant robustness test (§6.3).
- The paper states its benchmarks are stylised on purpose so metrics map to a solvable model, with optimal actions computable per period (§2).

**Cost.**
- ⚠️ No per-run cost is given. I searched for it.
- The paper says multi-turn evals are more expensive than Q&A (§7) and that multi-agent runs are costly (§5.3).
- Temperature 1, default reasoning settings (App. A.2).

**Other relevant remark.** The paper treats VendingBench as a related end-to-end simulation with an unbounded dollar score, whereas its own pricing benchmark can be solved for the optimal profit (§2, L183–209).

---

## 4. Project Vend: Phase two, and the Andon Labs Vending-Bench pages

### 4a. "Project Vend: Phase two" (Anthropic)

**Identity.**
- https://www.anthropic.com/research/project-vend-2
- Published 18 Dec 2025. Team: Frontier Red Team. Partner: Andon Labs.
- No code link on the page.
- I saved the raw page text as `vend2.txt` (20,322 chars) and read it end to end.
- The first WebFetch returned a model summary. I did not use it for facts.

**Scope.** This is a real-world deployment write-up, not a benchmark.
- A shop in Anthropic's SF office run by an AI shopkeeper called Claudius.
- Phase 1 used Sonnet 3.7. Phase 2 used Sonnet 4.0, later Sonnet 4.5.
- Expansion to New York, London and a second SF machine.

**Horizon.**
- ⚠️ No run length, step size or start date is stated. The charts, which are images, are the only evidence of time span.
- The page says "months" informally and there was no clean phase boundary.

**Decisions.**
- Sourcing, pricing, discounts, refunds, store credit, merchandise.
- Claudius had no payment interface. A human checked before purchases. It could create payment links to collect payment before ordering.

**Money feedback.**
- ⚠️ Starting capital, regeneration or cost parameters, and any bankruptcy rule are not on the page.
- New tools: CRM, inventory view that shows what Claudius paid for each item (to reduce selling at a loss), web browser for prices and delivery times, Google Forms, reminders.
- A CEO agent ("Seymour Cash") with an objectives-and-key-results tool.
  - An example message shows a Q3 revenue target of $15,000 (17.7% reached), a rule that financial decisions need CEO approval, and a rule of no pricing under 50% margin.
  - After the CEO was added, discounts fell about 80%, free items halved, and the CEO refused over 100 lenient requests.
  - The CEO approved such requests about eight times as often as it denied them.
  - Refunds tripled and store credits doubled.
- A merch agent ("Clothius") made a profit on many custom items.

**Scoring.**
- No formal score. Evidence is weekly profit and profit margin per product (chart images).
- The text says weeks with negative profit margin were largely eliminated.

**"Doing right" versus "earning more".**
- No formal trade-off score.
- The post links failures to the model being trained to be helpful: it decides like a friend, not a hard-nosed market actor.
- Examples:
  - An onion futures contract was cancelled only after a staffer cited the Onion Futures Act.
  - A shoplifting response proposed paying a staffer $10/hour, below California minimum wage.
  - An "imposter CEO" appeared after a faulty vote.
  - Staff tried to buy gold bars below market value.
- Process requirements (checking prices and delivery times with tools before quoting) helped most. A bureaucracy lesson.
- A CEO agent did not clearly help.

**Validity and exploits.**
- External red teaming by a Wall Street Journal newsroom, cited as an adversarial setting the authors did not control.
- The post notes simulations like Vending-Bench "only get you so far".

### 4b. Vending-Bench 2 (Andon Labs)

- Page: https://andonlabs.com/evals/vending-bench-2
- Saved as `https___andonlabs_com_evals_vending_bench_2.txt`. Read in full.
- Retrieved 2026-11-05. The leaderboard is live and changes over time.
- It lists model names I cannot independently verify beyond the page. Treat the leaderboard as page-reported.

**Horizon.**
- One simulated year.
- Roughly 3,000–6,000 messages per run, and about 60–100 million output tokens per run.
- Context window about 69,000 tokens, with older messages trimmed.

**Decisions.**
- Search the web, email suppliers, negotiate, order, move stock, set prices, collect cash, pay by email.

**Money feedback.**
- Starting balance $500.
- Daily $2 machine fee.
- Output tokens are charged $100 per million, weekly.
- Credit-card sales arrive within about a day. Cash must be collected from the machine by hand.
- Payments by email are irreversible.
- Delivered goods go to storage and must be moved into the machine.
- Sales depend on day of week, season, weather and price.
- Messier than version 1:
  - adversarial suppliers (unreasonable quotes, bait-and-switch)
  - delayed deliveries
  - supplier bankruptcies
  - refund demands from unhappy customers

**What ends a run.**
- The simulated year, or early termination if the agent cannot pay the $2 fee for more than 10 consecutive days.

**Scoring.**
- Bank account balance at the end of the year. Unrealised potential profit does not count.
- The page says there is no ceiling. It estimates a "good" strategy at about $206/day for 302 days, roughly $63k.
- Leaderboard figures: top entry about $16.5k, tenth about $9.6k (page-reported, live).
- The page lists arithmetic and geometric means, and a "score vs cost per run" chart. ⚠️ The numbers behind that chart are not in the page text, so I cannot report the cost per run.

**"Doing right" versus "earning more".**
- Scored on money only. The system prompt tells the agent it is judged solely on its bank balance and should do "whatever it takes".
- No ethics score on this page.
- Gaming risk is acknowledged: suppliers are LLMs that could be jailbroken to give goods away, and the sales equations are gameable.

### 4c. Vending-Bench Arena (Andon Labs)

- Page: https://andonlabs.com/evals/vending-bench-arena
- Saved as `andonlabs_arena.txt`.
- Same environment as Vending-Bench 2 with several agents at the same location.
- Agents can email, send money and trade goods. All scoring is individual, and agents know it.
- A "round" is usually the aggregate of four runs.
- Round results are money balance per model, for example Round #14 (Gemini 4 Carbon $16.0k, GPT-6 Astra $13.5k, Gemini 4 Argon $13.0k).
- Behaviours the page reports in transcripts, which are not scored:
  - price cartels and collusion
  - deception about suppliers
  - exploiting competitors who are short of cash
  - paying a competitor to stop stocking a product
  - sharing supplier information
- The page states which models initiated or accepted price fixing.
  - The page says one model was the only one to initiate it in Round #9, and one never accepted it.
  - I did not check this beyond the page.
- Example of survival pressure: an agent that forgot to collect cash until the last day found $1,142.15 in the machine.

---

## Cross-source notes relevant to FarmBench design

1. **Only MACHIAVELLI scores "right" separately from "reward"**, as per-violation counts against a random baseline plus a Pareto plot, with no single number.
2. **GovSim's "right" is the sustainability of a shared stock.** It is measured through survival, over-usage and equality, with collapse as the failure condition.
3. **EconEvals separates trade-off tendency (litmus score) from competence and consistency** and explicitly refuses to declare a correct weighting.
4. **Vending-Bench 2 and Arena score money only.** Misconduct is reported in write-ups, not in the score.
5. **Project Vend is a deployment write-up with no formal score.**

---

## COVERAGE STATEMENT

**GovSim (2404.16698).**
- Opened the full PDF and converted it to text.
- Read to the end: §1–6 (L1–670), Appendix A, B, C, D.1, D.4 and the E–F text sections.
- Skimmed: D.2 tables (read in full). D.3 and D.5 per-model tables were passed through a text filter that dropped number rows, so I used only the Δ tables and Tables 13–15.
- Skimmed: reference list (L671–897), F.2 plots, NeurIPS checklist.
- ⚠️ Appendix G is referenced in the text but is not in the v4 PDF.
- ⚠️ The per-agent meaning of "Gain" is my inference.

**MACHIAVELLI (2304.03279).**
- Opened the full PDF.
- Read to the end: main body (L1–560), Appendices A–M (L762–1925), including both results tables and all annotation prompts.
- Skipped: references (L560–757).
- ⚠️ No per-game length, step cap or episode end rule found. Checked by reading and searching.

**EconEvals (2503.18825).**
- Opened the full PDF. It has 114 pages; main body to p.36.
- Read unfiltered: §1–4.2 (L1–870).
- ⚠️ §4.3–§7 (L870–1900) were read through a prose-only filter that drops lines with wide whitespace runs. Plot labels and some table rows were dropped. I read Table 3 and Table 4 directly. Table 2 (preference-reasoning metrics) was not read as a table.
- Read: Appendices A, B (Table 4), G, H, I, J, K (opening), L, and the pricing and Efficiency-vs-Equality prompts in M.
- ⚠️ Not read: Appendices C (partly), D, E, F, N (cluster listings, thousands of lines), and the M prompts for procurement, scheduling, patience and collusion.
- ⚠️ Collusion litmus formula garbled in extraction.
- ⚠️ No per-run cost found.

**Project Vend phase two.**
- Fetched raw HTML and extracted all text; read to the end.
- ⚠️ Charts are images and unreadable. Starting capital, run length, bankruptcy rule and exact profit numbers are not on the page.
- The WebFetch summary was not used.

**Andon Labs pages.**
- Vending-Bench 2: read in full.
- Homepage: read in full.
- Arena: read the intro and Rounds #14 to #9 in full. #8 to #3 transcripts were read for the main findings but not every quoted exchange. Round #2 and #1 were read at the headline level plus the opening transcripts.
- ⚠️ Vending-Bench 1 page: only the first screen (leaderboard header) was read.
- ⚠️ Pages are live and will change. The leaderboard and the model names on them are what the page showed on 2026-11-05.
- The Vending-Bench paper itself was not requested and was not read.

---

# Report d-inventory-farm

# Fact extraction: four agent-benchmark papers (FarmBench comparison)

All files are in /private/tmp/claude-501/-Users-ardaenfiyeci-worktrees-farm-eval-hen-cost/d6ba3112-405f-4e5c-baf1-1ddae93a3621/scratchpad/papers/d/. Page numbers below are the PDF page numbers (the printed page numbers match).

Files kept there:
- 2508.11416.pdf and 2508.11416.txt
- 2602.12631.pdf and 2602.12631.txt
- 2609.13436.pdf and 2609.13436.txt
- agrimanager_neurips.html (the NeurIPS poster page, abstract only)
- or_forum.html (the OpenReview challenge page, see below)
- Two PNG renders: aim_p-03.png (AIM-Bench page 3) and wf_p-08.png (page 8 of 2609.13436, the results figures)

ID check: all three arXiv IDs resolve to the papers you named. AgriManager has no arXiv listing that I could find (details in section 3).

---

## 1. AIM-Bench (arXiv 2508.11416)

**Identity**
- Title: "AIM-Bench: Evaluating Decision-making Biases of Agentic LLM as Inventory Manager". Version v1 (the only version I saw), 15 Aug 2025, cs.AI (p.1 stamp). It says "This is a preprint" (p.1 footnote).
- Authors: Xuhua Zhao, Yuxuan Xie, Caihua Chen (School of Management and Engineering, Nanjing University), Yuxiang Sun (School of Robotics and Automation, Nanjing University, Suzhou). The PDF is 11 pages.
- Code link: none stated anywhere in the paper. No appendix is included in the PDF, although §4.3 and §4.4 say "refer to Appendix B" for cost parameters. The PDF ends with references on p.10-11. ⚠️ Cost parameters, horizons T, prompts and the definition of the "management score" are therefore not available in this version.

**Horizon and step**
- Newsvendor (NVP): 20 rounds of a single-period newsvendor problem (§4.1, p.5).
- Multi-period replenishment (MPR): finite horizon of T discrete periods. T is not given in the main text (§4.2, p.5). Orders are placed on a fixed schedule of dates (for example "Tuesdays and Fridays"). The order count is M and the order dates are t_m.
- Beer Game (BG), Two-level Warehouse Network (TWN), Supply Chain Network (SCN): T is not given in the main text.
- Five environments in total: NVP, MPR, BG, TWN, SCN (§3.2, p.4, and Fig. 2).

**Decisions**
- The agent outputs the next action as a natural-language string, conditioned on its past interaction history (§3.1, p.3). The memory module is m_{i,t} = the sequence of its previous observations and actions (p.4).
- The action is the order quantity q_t in NVP and MPR, and the replenishment quantity a_t^i in BG.
- In TWN and SCN each downstream agent has two suppliers: a normal source and an expedited source with "a higher selling price and shorter lead time" (§3.2 and §4.3, p.4 and p.6). Mini-warehouses in TWN can also order directly from the manufacturer.
- Each environment is formulated as a Partially Observable Markov Game (POMG, a multi-agent game where each agent sees only part of the state).

**How money or cost feeds back**
- NVP (§4.1, p.4-5):
  - Unit purchase cost c, unit revenue r. Leftover units are salvaged at value 0.
  - Underage cost c_u = r − c, overage cost c_o = c, critical ratio = c_u/(c_u+c_o).
  - Decisions are framed in two ways: a positive frame (maximize profit) and a negative frame (minimize the drop below perfect-information profit).
- MPR (§4.2, p.5):
  - Holding cost h per excess unit and stockout (backorder) cost b per backordered unit, charged at the end of each period.
  - Cost C_t = h[I_t − D_t + sum of arriving orders]+ + b[−I_t + D_t − arriving orders]+.
  - Stochastic vendor lead time (VLT) L_m, a random positive integer, with "no crossing over of order arrivals".
  - Inventory can go negative (backorders).
- BG (§4.3, p.5-6):
  - Fixed lead time L. Each agent's order is limited by its upstream supplier's inventory.
  - System cost per period is C_t^total = sum over echelons of [h_i(...)+ + b(...)+] (Eq. 8).
- Numeric cost parameters: not in the main text (⚠️ see above). No budgets, cash constraints, credit or price shifts are described.

**What ends a run**
- The fixed horizon (20 rounds for NVP, T periods otherwise). No bankruptcy or termination rule is described. ⚠️ Appendix missing.

**Scoring (exact metrics, all listed)**
1. NVP anchoring factor α (§4.1.1, p.5):
   - Model: q = μ + α′(q* − μ), where α′ = 1 − α, μ is mean demand and q* the optimal order. α is the fraction of the optimal adjustment NOT made.
   - Reported as α. α = 1 means the order equals mean demand (complete anchoring) and α = 0 means no anchoring.
2. NVP demand chasing (§4.1.2, p.5): the correlation ρ(q_t, d_{t−1}) between the current order and the previous demand realization. For i.i.d. demand the true correlation is zero, so a positive value means demand chasing.
3. MPR distance to optimal order (§4.2, p.5):
   - The ex-post optimal order a*_m comes from a dynamic-programming result (Qi et al. 2022): a*_m = max(d[v_m, s*] − I_{v_m}, 0), with s* = floor(h(v_{m+1} − v_m)/(h+b)) + v_m.
   - The distance is d(a, a*) = sqrt(sum over orders of (a_m − a*_m)²) (Eq. 6).
   - Finding V says this process metric separates models better than the outcome metrics.
4. Bullwhip effect (BWE) in BG (§4.3, p.6): β = σ₂/σ₁, the standard deviation of upstream demand divided by the standard deviation of downstream demand. β > 1 means amplification, β = 1 none, β < 1 smoothing.
5. Three "real-world" outcome metrics (§4.4, p.6):
   - Average inventory management cost AC = (sum of C_t)/T.
   - Turnover rate TR = (sum of I_t)/(sum of D_t), that is, average inventory divided by average demand.
   - Stockout rate SR = T_s/T, the share of periods in which a stockout occurred.
6. Fig. 2b shows "management scores" per LLM per environment as a radar chart. The text never defines this score. ⚠️ Undefined in this version.

**Novel / behavioural-bias elements (exact definitions above)**
- Mean anchoring (α), demand chasing, bullwhip (β), plus the framing manipulation (profit vs cost frame, §4.1). Finding III says no risk reversal was found.
- Mitigation tests (§5.2, p.7): a "System 2" cognitive-reflection prompt, and an information-sharing state space where agents see partners' information.
- No cash account, credit, statement, settlement delay, paperwork error, stock-buying decision, survival pressure, net-worth scoring, or information-lookup charge.

**Environmental / welfare vs profit:** none.

**Run cost:** not stated. Models: DeepSeek-V3, Gemini-2.5-flash-lite, GPT-4.1 (2025-04-14), GPT-4o (2024-11-20), Qwen-2.5-72B (§5.1, p.7).

**Headline results (§5.2, p.7-8; Table 1, p.9)**
- Table 1 lists, per model, Avg C / TR / SR for BG, MPR, TWN and SCN (BG has Avg C and TR, SR). Reading the table, BG Avg C is: Qwen 21.28, DeepSeek 14.72, gpt-4o 15.14, gpt-4.1 20.71, gemini 30.38. MPR Avg C is: Qwen 649, DeepSeek 794, gpt-4o 1090, gpt-4.1 332, gemini 542.
- Finding I: most LLMs anchor on mean demand (GPT-4o α = 1 and 0.925; GPT-4.1 0.405; DeepSeek-V3 1.375; Gemini-2.5-flash-lite showed none). They show less demand chasing than humans.
- Finding II: the reflection prompt lowers anchoring (Qwen α from 0.7 to 0.255 in the positive frame, 0.74 to 0.245 in the negative frame).
- Finding IV: all models show BWE. Gemini-2.5-flash-lite has the highest, at 19.22 and 28.61. Information sharing reduces it (Qwen 13.78 to 4.45, and 23.07 to 10.73), but GPT-4o copies partners ("action chasing") and its BWE goes close to 0.
- Finding V: the GPT-4.1 and Qwen stockout rates are nearly equal (0.250 and 0.256), but their distances to optimal differ (467 vs 608).
- Finding VI: Qwen over-orders (maximum TR 10.2, minimum SR 0.2). The paper says models cope worse with uncertain timing of demand than with its size.
- Failure modes: over-ordering from demand overestimation, and anchoring.

**Validity safeguards:** none stated beyond the Limitations section (§7, p.9): only prompt-based mitigation is tested, and simulation environments simplify real use and "may limit the generalisability". No repeats, seeds or confidence intervals are mentioned.

---

## 2. InventoryBench (arXiv 2602.12631)

**Identity**
- Title: "AI Agents for Inventory Control: Human-LLM-OR Complementarity". The paper's own wording for the benchmark is "InventoryBench".
- Authors: Jackie Baek (NYU Stern), Yaopeng Fu, Will Ma, Tianyi Peng (all Columbia). Version v2, 4 May 2026, cs.AI (p.1 stamp). 46 pages.
- Code and data links (p.4-5):
  - Benchmark and public leaderboard: https://tianyipeng.github.io/InventoryBench/
  - Human-AI game: https://github.com/TianyiPeng/AI-human-inventory-game.git
  - Pre-registration: https://aspredicted.org/gs5tm3.pdf (p.14, footnote 5)

**Horizon and step**
- One product (single SKU), T periods (§3, p.6).
  - Synthetic instances: T = 50, with 5 historical demand samples (Appx D, p.29).
  - Real instances: weekly data, 52 weeks of 2019. The first 5 weeks are history and T = 47 weeks form the test trajectory (Appx E, p.32).
- Per-period event order (§3, p.6-7):
  1. Observe state and context.
  2. Place an order q_t ≥ 0.
  3. Arrivals.
  4. Demand realized (uncensored).
  5. Inventory update.
- Sales are s_t = min(d_t, I_t + A_t). Unmet demand is lost.
- The prompt adds a one-period observation delay: arrivals are only visible in the next period (Appx B, p.27).

**Decisions**
- One order quantity per period. The agent also writes "carry-over insights" (memos prepended to the next period's prompt) (§3.1, p.8).
- Each period is a single stateless LLM call returning JSON: rationale, short rationale, carry-over insight, action.
- Four methods (§3.1, p.9, and §1):
  - OR alone: a data-driven capped base-stock policy (Appx A, p.25-26).
  - LLM alone.
  - OR→LLM: the LLM sees the OR recommendation and may override it.
  - LLM→OR: the LLM estimates lead time L, demand mean µ̂ and standard deviation σ̂, and OR computes the order (Appx C, p.28-29).
- Human modes A, B, C are covered under novel elements below.

**How money or cost feeds back**
- Per-period profit = p·s_t − h·I_{t+1}. Here p is a fixed per-unit profit margin and h a per-unit per-period holding cost (§3, p.7). Total profit over the horizon is the objective.
- There is no explicit stockout cost. Stockouts cost only the lost margin (lost sales).
- Critical fractile ρ = p/(p+h). Instances use ρ ∈ {0.50, 0.80, 0.95}, equivalent to p:h = 1:1, 4:1, 19:1 (§4.1 p.9; Appx D p.29).
- Lead-time settings (§4.1, p.9):
  - L = 0.
  - L = 4 fixed.
  - Stochastic: each order independently has ℓ ∈ {1, 2, 3, ∞} with equal probability, where ∞ means the order is lost and never arrives.
- The agent is told the promised lead time L, but actual lead times "may differ" and are revealed only as orders arrive (§3, p.7). Lost orders still count as in-transit inventory in the OR policy (§6.3, p.20).
- No budget or cash constraint, no price shifts, and no environmental costs.

**What ends a run:** the end of the horizon (T = 50 or 47). No termination rule.

**Scoring**
- Reward = total profit sum(p·s_t − h·I_{t+1}) (§4.2, p.10).
- Normalized reward = max( reward / (p · sum of d_t), 0 ). The denominator is "very optimistic upper bound on optimal profit" (revenue with all demand captured and no leftover inventory), and clipping at 0 stops large losses dominating the mean (§4.2, p.10). Mean ± 95% CI is reported.
- Implicit critical fractile (§4.5, p.13): the fraction of periods with excess inventory (as opposed to a stockout). It is used to test calibration to ρ, measured as the range across ρ values; the paper notes it cannot match ρ exactly because of lead times.
- Human-AI complementarity measures (§6.1-6.2, p.16-19):
  - Population-level CE = ȳ_{H+AI} − max(ȳ_H, y_AI).
  - Individual-level CE_i = y_{H+AI}^(i) − max(y_H^(i), y_AI).
  - Theorem 1: a distribution-free lower bound P(CE_i > δ) ≥ sup_t [F_a(t) − F_b(t+δ)].

**Novel elements**
- Hidden lost orders (stochastic lead-time regime). The OR policy keeps counting lost orders as pipeline stock, and the LLM can detect and write them off. This is the paper's main example of LLM value (§4.3 p.10-11; Example 1, Appx H p.37).
- Demand regime changes at hidden changepoints (period 16 in several families) and a text "contextual information" string per period (product description, calendar dates). Real instances use H&M product text so the LLM can use seasonality knowledge (§3, §4.1, Appx E).
- Behavioural measures:
  - Calibration to the cost tradeoff (implicit critical fractile range, §4.5).
  - Overfitting to noise: the LLM reads a regime shift into pure noise, and this makes OR better on stationary IID demand (Example 2, Appx H p.37; Table 2).
  - There is no explicit demand-chasing or bullwhip metric.
- Human-in-the-loop classroom experiment (§5, p.13-16):
  - 69 participants, 187 subject-instance observations, three real-data instances (swimwear bottom, lead time 0; blazer, lead time 1; trousers, lead time 1 with lost orders, where lead time is 1 w.p. 75% and ∞ otherwise per Appx I, p.43), and a web game.
  - Mode A: OR→Human. Mode B: OR→LLM→Human. Mode C: LLM acts autonomously and the human gives optional free-form guidance every 4 periods.
  - Mode assignment is randomized, one mode per instance per participant. The hypotheses were pre-registered.
  - Regression: Y_ij = α_i + β_j + τ_c(i,j) + ε_ij, with subject and instance fixed effects and standard errors clustered by subject (§5.2.1).
- Not present: cash account, credit, monthly statement, settlement delay, paperwork error, stock-buying decision, survival pressure, net-worth scoring, information-lookup charge, agent-chosen waiting.

**Environmental / welfare vs profit:** none.

**Run cost:** not stated. ⚠️ I grepped for tokens, API cost and dollar figures and found none. The paper says OR→LLM was run 100 times per human-experiment instance (§5.2.2, p.15-16). Models: Gemini 3 Flash (main), Grok 4.1 Fast, GPT-5 Mini (§1, p.2).

**Headline results**
- Table 1a (Gemini 3 Flash, 1,320 instances, mean normalized reward): OR 0.445, LLM 0.494, OR→LLM 0.538, LLM→OR 0.501 (p.3, §4.2). The reported figure "21% improvement over OR alone" is in §1.
- By lead time (§4.3, p.10-12):
  - With deterministic lead times (L = 0 and 4), LLM→OR is strongest, because the LLM helps with forecasting and OR with calculation.
  - With stochastic lead times, OR falls to 0.154 and LLM→OR to 0.218, while LLM scores 0.353 and OR→LLM 0.385.
- By demand pattern (Table 2, p.12; Gemini 3 Flash):
  - OR is best on Stationary IID (.802), Variance Change (.706), Seasonal (.676), Multi-changepoint (.700) and Autocorrelated (.756).
  - LLM-based methods are best on mean shifts and trends. Real H&M: OR .486, LLM .488, OR→LLM .525, LLM→OR .537.
- Calibration (Table 3, p.13): the range across ρ is OR 0.127, LLM→OR 0.105, OR→LLM 0.069, LLM 0.028. The more LLM control, the less the method responds to the cost ratio.
- Other models (Appx F, p.33-37):
  - Grok: OR→LLM .514, LLM→OR .493.
  - GPT-5 Mini: OR→LLM .461, LLM .460, LLM→OR .458, roughly equal. The paper says it tends to ignore the OR input.
- Human experiment (Table 1b, p.3): Mode A .466, Mode B .534, Mode C .464, OR (no human) .376, OR→LLM (no human) .482. Mode B vs A: τ = 0.0675, one-sided p = 0.00025. Mode C vs B: −0.0722, p = 0.00012. Mode A beats OR (p = 0.0098) and Mode B beats OR→LLM (p = 0.000009).
- Complementarity: CE-hat = 0.0496 (about 10.2% over the best non-collaborative baseline); the lower bound on the share of individuals who benefit is 30.2% to 60.5% depending on instance (Tables 4-5, p.19).
- Main failure modes: the LLM struggles with pipeline tracking (the paper says "LLMs can struggle with inventory pipeline tracking", p.3) and invents regime shifts in noise; OR cannot see lost orders or shifts.

**Validity safeguards**
- All randomness is fixed in advance per instance (demands, lead times, contexts), "to ensure full reproducibility" (§4.1, p.9). Base seed 42 for synthetic data (Appx D).
- H&M filters (Appx E): at least 50 of 52 weeks with sales, and a stable price (max-to-min weekly price ratio ≤ 1.2) so demand is not confounded by discounts. Observed sales are assumed to equal true demand.
- Confidence intervals, a pre-registered human experiment, clustered standard errors, and 100 LLM repeats on the human-experiment instances.
- Clipping of normalized reward at 0.
- The paper discloses that Claude and GPT-5 Mini were used for prose editing (Appx L).

---

## 3. AgriManager (NeurIPS 2026 poster)

⚠️ **I could NOT read the full paper.** I read only the poster-page abstract. The OpenReview page (https://openreview.net/forum?id=qpBXkIWHNU) and its API sit behind a bot-challenge ("Verifying your browser", HTTP 403), and I did not try to bypass it. The NeurIPS page lists no arXiv, code or PDF link. I searched the web and the arXiv API by title and by "AgriManager" and found no arXiv version. Every fact below comes from the abstract only. I have no horizon, step, decisions, reward formula, costs, termination rule, metrics, run cost or safeguards for this paper.

**What the abstract gives (page: https://neurips.cc/virtual/2026/poster/139010, saved as agrimanager_neurips.html)**
- Title: "AgriManager: A Framework and Benchmark for LLM-RL Generalization in Agricultural Management". NeurIPS 2026 Poster, Thu 10 Dec 2026, Hall 1-4 (Sydney).
- Authors: Chi Gui, Junwen Zheng, Ritwik Nigam, Qianlan Yang, Meagan Lang, Vardhan Dongre, Jeremiah Barr, Yu-Xiong Wang, Vikram Adve. Affiliations are not listed on the page.
- Framework: unifies the DSSAT, WOFOST and Cycles crop simulators under "prompt-based schema specification with joint multi-objective, multi-environment training". The abstract calls it "the first multi-simulator LLM-RL framework for agricultural management".
- Schema Σ = (Σ_O, Σ_A, Σ_R): observation, action and reward schema. "Schema shift" means variation in Σ between training and deployment.
- Three-tier generalization ladder:
  - Tier 1: within-schema distributional shift (weather, crop, price).
  - Tier 2: single-axis schema shift along Σ_O, Σ_A or Σ_R.
  - Tier 3: compositional schema shift across simulators.
- Results claimed:
  - Within fixed schemas, prompt-conditioned LLM-RL with explicit reasoning matches or exceeds fixed-interface neural-network RL on all three settings, "with reasoning becoming necessary when the reward shape penalizes input use".
  - Single-axis shift needs information sufficiency for Σ_O, joint action-menu coverage for Σ_A, and objective coverage for Σ_R.
  - Under compositional shift, a unified policy with marginal per-platform coverage and reasoning matches or exceeds per-source specialists "on all three callback targets".
  - Without that coverage, pairwise zero-shot transfer is "bounded by transition dynamics, which the prompt cannot describe", left as an open task.
- Money and welfare: the abstract mentions prices varying (Tier 1) and a reward shape that "penalizes input use" (so input cost or use competes with yield in the reward). Whether that penalty is a money price, an environmental cost or a resource cap, and how it is scored, is not stated in the abstract. I cannot say anything further.

---

## 4. "Toward Self-Adaptive Physical AI: Can LLM Agents Manage Long-Horizon Physical Tasks?" (arXiv 2609.13436)

**Identity**
- Title as you gave it. Version v1, 11 Sep 2026, cs.AI (p.1 stamp). The arXiv API confirms published 2026-09-11 with authors Varun Kaushik, Yayun Tan, Xiaofan Yu.
- Organisations: The Harker School (Kaushik); University of California, Merced (Tan, Yu). 13 pages. Funding: Academic Senate Faculty Research Grant and UC Merced startup funds (Acknowledgments).
- Code link: none stated. There is no appendix. Pages 1-9 are the body and pages 9-13 references.

**Horizon and step**
- 241 simulated days, one wheat growing season, one decision per day ("daily cycle", §4.1, Fig. 2; §5.1, p.6). The environment is `lnpkw-v0` in WOFOSTGym (Solow et al., 2025): crop growth limited by nitrogen (N), phosphorus (P), potassium (K) and water.
- Environment A: 2000 weather at latitude 44, longitude −99 (near South Dakota), soil oregon-3.
- Environment B (shift): 1984 weather at latitude 50, longitude 5, soil oregon-1, same wheat crop.

**Decisions**
- Each day the agent picks one of 17 actions (§5.1, Table 2, p.7):
  - No-op.
  - Nitrogen, phosphorus or potassium at 2, 4, 6 or 8 kg/ha.
  - Irrigation at 0.5, 1.0, 1.5 or 2.0 cm.
- It receives 15 environmental variables (Table 1): solar radiation, temperature, rain, days elapsed, soil moisture, total irrigation, available N/P/K, total N/P/K applied, development stage, growth-finished flag, storage-organ weight (WSO).
- Framework (§4, p.4-6): 6 deterministic Perception Agents → Manager Agent (LLM) → Decision Agent (LLM) → Revision Agent (LLM; can change the amount but not the action type or replace it with a no-op) → deterministic Execution Safety Guard → Action Agent → Reflection Agent (LLM, gives within-episode feedback). It is coordinated with OpenClaw, using GPT-5.6 Luna for the four LLM agents (§5.1, p.6).

**How money or cost feeds back**
- There is no money, price or budget. The paper formulates a two-part objective (§3, p.3-4): maximize yield Y at physiological maturity, with a secondary goal of avoiding unnecessary interventions. Cumulative resource use is C = sum of c(a_t).
- Eq. 2 is written as π* ∈ argmax(E[Y] − E[C]). The text says "λ ≥ 0 controls the trade-off", but λ does not appear in the equation as printed. ⚠️ Inconsistent in the paper. The value of λ and the cost function c(a_t) are not given.
- Consequences are delayed: yield is observed only at harvest, and actions are irreversible (§3, p.3).

**What ends a run:** the 241-day season, or physiological maturity (growth-finished flag FIN). No failure or termination rule is described.

**Scoring (three metrics, §5.1, p.7)**
1. Cumulative reward: the total reward over the cycle "according to the WOFOSTGym reward function". ⚠️ The reward function is not defined in this paper.
2. Maximum yield: storage-organ weight (WSO) at physiological maturity, in kg/ha.
3. Total resource use: cumulative N, P, K and irrigation applied (Table 3).
- Baselines: no-intervention, a fixed-intervention schedule at set growth stages, and PPO reinforcement learning (trained on Environment A for about one million timesteps, 2 h 44 min on an M2 Pro CPU; RL sees a normalized numerical vector). The paper says the LLM agent receives structured reports derived from the same measurements.

**Novel elements:** none financial. The environmental / resource element is described below.

**Environmental impact vs profit (the closest match):** resource use (fertilizer and water) is a secondary objective against yield and is scored only as a reported total, not in money (§3 and Table 3). Eq. 2 puts it as a subtracted term, but the weight is unspecified. The paper claims the agent "uses only a fraction" of RL's resources (p.2) and "less than 28% of the RL policy's resources in every fertilizer and irrigation category" (§5.2.3, p.9).

**Run cost (§5.1, p.6):** each LLM-agent run made 964 GPT-5.6 calls and used approximately 23.82 million tokens. PPO training: about 2 h 44 min as above.

**Results (Figs. 4-5, p.8; Table 3, p.9; I viewed the rendered figures)**
- Cumulative reward, Environment A (no shift): no action 27,914; fixed 48,747; RL 340,724; agentic 216,390. Yield in kg/ha: no action 545; fixed 961; RL 5,976; agentic 4,152 (about 69% of RL).
- Environment B (shift): no action 102,482; fixed 200,553; RL 4,798; agentic 453,956. Yield: no action 1,629; fixed 3,474; RL 110; agentic 6,519.
- Resource use (kg/ha N/P/K and cm irrigation):
  - Env A: agentic 68/12/72 and 21 cm; RL 554/142/258 and 141 cm; fixed 30/6/12 and 2 cm.
  - Env B: agentic 98/16/100 and 28.5 cm; RL 632/170/360 and 113 cm.
- Failure mode: the RL policy collapses under the shift (yield 110 kg/ha). One example of the reflection mechanism: after a potassium application raised K availability from 0.138 to 1.284 the agent skipped further potassium and applied nitrogen instead (§5.2.2).

**Validity safeguards:** the Limitations section (§6) says the work is evaluated only inside the WOFOSTGym simulator and does not capture all real-world factors. Hallucination controls are design features, not validation: role separation, restricted information, a Revision Agent and a deterministic Safety Guard (§4.2). ⚠️ I found no mention of repeated runs, random seeds, error bars or statistical tests. Each policy appears to have a single reported number, though the paper does not say so explicitly.

---

## COVERAGE STATEMENT

- **AIM-Bench 2508.11416:** I downloaded the PDF (11 pages) and converted it. I read the whole text extraction (title page to last reference), in three chunks. I viewed a rendering of page 3 (Fig. 2); the radar chart (Fig. 2b), Figs. 3-6 and the numeric labels inside the figures were not inspected beyond the extracted text and caption. ⚠️ The paper refers to an Appendix B that is not in this PDF, so cost parameters, horizons T, prompts and the "management score" definition were not available.
- **InventoryBench 2602.12631:** I downloaded the PDF (46 pages). I read the full text extraction, including main body, appendices A-L and the proof, with two limits. ⚠️ In Tables 11-12 (appendix per-pattern detail for Grok and GPT-5 Mini), I did not read the rows individually; I relied on the appendix F summary prose and the full Gemini table 10 header rows, and did not read most of the Table 10 grid cell by cell. Figure images (Figs. 1, 4, 5, 6, 7, 12-14) were not viewed; I used the text and captions.
- **AgriManager:** ⚠️ I opened only the NeurIPS poster page (and its saved HTML) and read the abstract. I did not read the full paper, which I could not reach: OpenReview was behind a bot challenge, and I found no arXiv version, code link or PDF. Everything in section 3 comes from the abstract.
- **Toward Self-Adaptive Physical AI 2609.13436:** I downloaded the PDF (13 pages). I read pages 1-9 (the full main body through the conclusion) from the text extraction, and viewed the rendered p.8 figures to confirm the numbers. I skimmed the references (pp.9-13) only for the OpenClaw and WOFOSTGym citations. There is no appendix. ⚠️ I did not read the cited WOFOSTGym paper, so the reward function and any cost model inside it are unchecked.
- I did not run any downloaded code.
