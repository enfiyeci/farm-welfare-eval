# Long-horizon financial benchmarks and real US egg-price data: raw research report (UNVERIFIED)

Eval: hen

Raw output of a Claude Sonnet research subagent, 2026-11-05, kept unchanged for provenance. Cite the
README's re-checked layer, not this file. ⚠️ marks and the coverage statement are the subagent's.

---

Part A found that every long-horizon business benchmark except RetailBench and the stock-trading ones uses a synthetic demand model, and most use a "daily/monthly fixed cost + cash-below-zero = out" bankruptcy rule. Part B found free USDA/EIA/BLS data for almost everything you need, but the cage-free wholesale price history, the Egg Industry Center cost study, and the APHIS per-head indemnity table were NOT retrievable as numbers. Both parts and the coverage statement are below.

Papers were downloaded as PDFs and converted to text locally. "Read" means I read that text in this session. Where I read only sections, I say so.

# PART A: Long-horizon financial / business-simulation agent benchmarks

**1. Vending-Bench (arXiv 2502.15840, Andon Labs, Feb 2025). Read in full.**
- Step and horizon: no fixed day count. A run stops after 2,000 messages. Each tool call advances simulated time by 5 min, 25 min, 75 min or 5 h. The `wait_for_next_day` tool is the sleep/skip mechanism. Runs reached about 18 to 222 simulated days.
- Decisions: email suppliers to order stock, set prices, restock via a sub-agent, collect cash from the machine, use memory tools.
- Cash: starts at $500. A fixed $2/day machine fee is charged. The run ends if the fee goes unpaid for 10 consecutive days. Orders are paid by giving the supplier an account number, and delivery arrives "a few days later". Unlimited credit is not mentioned.
- Data: synthetic. GPT-4o generates elasticity, reference price and base sales, then day-of-week, month, weather and noise multipliers are applied. Supplier replies are LLM-written from real supplier info fetched with Perplexity.
- Delayed consequences: delivery lag and fee drain. The dominant failure was agents assuming an order had arrived on its email date when it had not.
- Score: end net worth (cash, cash left in the machine, and unsold stock at wholesale cost). Claude 3.5 Sonnet's mean was $2,218 (min $476). The human baseline was $844.
- Cost: about 25M tokens and 5 to 10 real hours per run, 5 runs per model. No dollar cost is given. Context is cut to the last 30k tokens.
- Experiment on starting cash: $100 start gave fewer sales. A $5 daily fee ended every run before day 100. A $0 daily fee did not help; agents idled in wait loops.

**2. Vending-Bench 2 (Andon Labs web page, Nov 2025).** ⚠️ Read through a page-summarizer tool, not the raw page. It says the leaderboard shows 10 of 73 rows, charts had no numbers, and the sales equations and exact day count are not stated.
- Horizon: one simulated year (the ceiling estimate uses 302 days).
- Cash: $500 start, $2/day fee. The system prompt also charges $100 per million output tokens, billed weekly. Failing to pay the fee for 10 consecutive days ends the run. Card payments settle within a day, and cash must be collected by hand. Customers can demand refunds.
- Data: synthetic sales driven by day, season, weather and price (same equations as v1). Suppliers are adversarial: bait-and-switch, delays, bankruptcies. The agent is expected to sleep at night.
- Score: end bank balance only; unrealized value does not count.
- Volume: 3,000 to 6,000 messages and 60 to 100M output tokens per run. The page charts cost per run but gives no number. Context is about 69k tokens.
- Headroom estimate: about $63k per year.
- Leaderboard model names on the page (for example "GPT-6", "Gemini 4") are not ones I can verify. Top mean was $16,484.
- The related Vending-Bench Arena (a ⚠️ summary of the Andon page) puts several agents at one location, with individual scoring.

**3. CoffeeBench (arXiv 2606.16613, Sakana AI and KPMG, Jun 2026). Read the method and results sections; appendix prompts and tool catalogue not read.**
- Horizon: 90 days, one decision loop per day. Each tool call costs 30 minutes within a 09:00 to 19:00 day. `wait_for_next_day()` ends the day. A pre-scheduled demand surge runs on days 40 to 53.
- Decisions: six firms (2 farmers, 2 roasters, 2 retailers). The tested model plays one roaster. Actions are posting listings, making offers, pricing, roasting, messaging and paying invoices.
- Cash: $15,000 start. Fixed daily costs are $25 (farmer), $30 (roaster) and $50 (retailer). Trade is on net-30 credit, with 0.1%/day late interest. Shipments are delayed by one day and can be lost. Inventory decays 0.5%/day. Negative cash means bankruptcy and removal.
- Data: fully synthetic (elasticity demand with noise). The paper's own limitations section says it is far from real markets.
- Delayed consequences: net-30 receivables, production lag, spoilage, and bad debt written off on counterparty bankruptcy.
- Score: cumulative net income (revenue minus COGS, OpEx and interest). Best result was GPT-5.5 at +$3,109. A passive baseline scored -$2,765.
- Cost: about $250 API per run across all six firms, about 8 hours, about 1,000 evaluated-agent tool calls at about 90k tokens each. Context is summarized once it passes 160k tokens.
- Failure mode: Claude Haiku 4.5 spent about 40 of 90 days only calling `wait_for_next_day` ("idle-drift").

**4. EnterpriseArena, "Can LLM Agents Be CFOs?" (arXiv 2603.23638 v2, May 2026). Read about 60% (main body through the main results table, the fundraising/dynamics appendix tables, the compute section); the failure analysis and ablation text were only grepped.**
- Horizon: 132 monthly steps (11 years), one action per month: `book_closing`, `fund_raising_request`, or `pass`. Up to 20 tool calls per month for observation (cash check, records, market data, cash-flow projection).
- Cash: $15M start, 5,000 borrowers, zero debt. Cash below zero at any step ends the episode with a score of 0. Fixed fee, opex and payables mechanics are not detailed in what I read.
- Financing: a raise succeeds with a probability that depends on the market regime and the firm's state. The amount raised is 70% to 100% of the request. Funds arrive 1 to 6 months later. The debt interest rate is fixed at settlement time, not at request time.
- Data: hybrid. Firm operating indicators get Gaussian noise each month. Macro, rates, VIX and similar series follow a fixed anonymized real path (Jan 2015 to Dec 2025) with dates relabeled so agents cannot recognize events like COVID.
- Delayed consequences: the settlement delay is the dominant factor. Removing it gave the largest improvement in the ablation.
- Score: survival, then RevTTM×5 + cash − $5,000 per tool call.
- Results: 15.4% of trials survive all 132 months (v1 said about 16%). 12 of 23 ReAct backbones never survive. Best agent score was $34.7M (Codex + GPT-5.5) against a human-expert $476.7M.
- Cost: 15 to 45 minutes per run, about $2,000 API total across all experiments. Tokens per run are not reported in what I read.

**5. RetailBench (arXiv 2606.15862, Jun 2026). Read the main body; parts of the appendix.**
- Horizon: a day-level loop, 180 days evaluated, with a design target of thousand-day runs. Time advances only when the agent calls `end_today`.
- Decisions: pricing, replenishment orders, supplier choice (5 suppliers per product), shelf assortment, notes.
- Cash: $30,000 start, $600/day rent, 15,000-unit inventory cap, 40-product shelf cap. The oracle policy's rule terminates the run after 10 consecutive days of negative funds.
- Data: real. Products, prices, sales and traffic come from the Dominick's grocery dataset (1991 to 1995, 96 products). Reviews come from Amazon Reviews 2023. News events come from a financial-news corpus. Supplier quality is hidden.
- Delayed consequences: delivery lag, expiry, returns and reviews arrive later.
- Score: final net worth (cash plus stock plus pending orders) and survival days. Oracle policy: 131,510. Best LLM (GPT-5.5): 24,351. Only 2 of 7 LLMs survive 180 days.
- Cost: 176k to 1.05M tokens per simulated day.

**6. StockBench (arXiv 2510.02209, Oct 2025). Read through Section 3.1 and the results table; the rest not read.**
- Horizon: 82 trading days (Mar 3 to Jun 30, 2025), one decision per day.
- Decisions: increase, decrease or hold positions in 20 top-weighted Dow stocks.
- Cash: $100,000 start. It uses real open prices, fundamentals and news from the previous 48 hours. Orders that exceed cash are sent back to the agent to revise.
- Score: return, max drawdown, Sortino. The passive baseline returned +0.4% with a -15.2% drawdown. Most models did not beat it.
- ⚠️ "No transaction costs" is from a search snippet, not from the paper text I read.
- Cost and tokens per run: not read. Context is 32,768 tokens; 3 seeds per model.

**7. InvestorBench (arXiv 2412.18174, Dec 2024).** ⚠️ Only the abstract, setup and period sections were grepped, not read through.
- Daily real data across three tasks: one stock, crypto and ETFs. Stock test period 2020-10-01 to 2021-05-06; crypto 2023-04-05 to 2023-11-05; ETF 2020-01-02 to 2020-09-21, each with a warm-up window.
- Metrics: cumulative return, Sharpe ratio and others.
- No fees, cash-below-zero rule or sleep mechanism found by grep.

**8. Beer-game paper (arXiv 2605.17036, v4 Sep 2026).** ⚠️ Read the abstract, introduction and grepped excerpts only.
- Weekly orders in a four-tier chain (retailer to factory). Shipments take about two weeks. The score is total holding plus backlog cost; there is no cash account or bankruptcy rule.
- Demand uses the standard fixed MIT pattern for evaluation and synthetic distributions for post-training. LLM agents show an "agent bullwhip" (decision instability that grows upstream and over time).
- Horizon length and cost per run: not confirmed.

**Comparison table**

| Benchmark | Step | Horizon | Starting cash | Fixed cost | Termination | Demand/prices | Score | Cost per run |
|---|---|---|---|---|---|---|---|---|
| Vending-Bench | event-driven, days | up to ~222 days (2,000 msgs) | $500 | $2/day | 10 days unpaid fee | synthetic | net worth | ~25M tokens, 5-10 h |
| Vending-Bench 2 ⚠️ | same | 1 year | $500 | $2/day + token charge | 10 days unpaid fee | synthetic | end balance | 60-100M output tokens |
| CoffeeBench | day | 90 days | $15,000 | $25-50/day | cash < 0 | synthetic | net income | ~$250, ~8 h |
| EnterpriseArena | month | 132 months | $15M | not read | cash < 0 | real macro, anonymized, plus noise | valuation | ~$2,000 total, 15-45 min/run |
| RetailBench | day | 180 days | $30,000 | $600/day rent | 10 days negative funds (oracle rule) | real retail data | net worth | 0.18-1.05M tokens/day |
| StockBench | day | 82 days | $100k | none | none | real prices | return, drawdown, Sortino | not read |

**What this means for FarmBench (my reading, not from the sources):**
- Monthly steps with a fixed settlement delay (1 to 6 months in EnterpriseArena) are the closest precedent for a monthly farm.
- Real macro series with relabeled dates (EnterpriseArena) is the closest precedent for loading real egg history without letting models recognize it.
- The 10-consecutive-days-unpaid-fee rule recurs in three benchmarks.

# PART B: Real data a static eval could load

**Source rows** (unless marked ⚠️, I opened the source itself)

| Source | Series / content | Granularity, span | Cost, format | Notes |
|---|---|---|---|---|
| USDA AMS, "Egg Markets Overview" (AMS_3725), https://www.ams.usda.gov/mnreports/ams_3725.pdf | Weekly: national negotiated loose white Large, NY formula, Midwest warehouse, California benchmark, retail ad prices by system, flock losses, charts | Weekly, 3-page PDF; I opened the Oct 30 2026 and Feb 2025 editions. Archive via esmis.nal.usda.gov | Free, PDF | Prose numbers only; the cage-free negotiated price is a chart with no printed values. Retail ad prices are printed: Feb 7 2025 UEP cage-free $2.50 to $2.99 vs conventional caged $1.87 to $2.68; Oct 30 2026 cage-free $2.98 vs conventional $1.42. |
| USDA AMS, National Shell Egg Index (report 2843), https://mymarketnews.ams.usda.gov/viewReport/2843 | National index | ⚠️ Not read: the PDF was unreadable to the fetch tool, and the page timed out | Free; MARS API / CSV mentioned by search snippets | ⚠️ Whether it still publishes daily is unconfirmed. |
| USDA AMS cage-free monthly report | Wholesale cage-free shell eggs, contract and negotiated spot | ⚠️ A search snippet says monthly, first Monday; I did not open the report | Free | ⚠️ Exact report ID and history depth not confirmed. |
| BLS via FRED, APU0000708111 (US) and APU0200708111 (Midwest urban), https://fred.stlouisfed.org/graph/fredgraph.csv?id=APU0000708111 | Retail Grade A Large $/dozen | Monthly, Jan 1980 to Sep 2026 | Free CSV, downloaded and read in full | Best long clean series, but retail not wholesale. |
| Expana / Urner Barry (paid) | Midwest Large daily quote; Large White and Brown Cage-Free Graded Loose Index, weekly (Thursdays), from Dec 1 2021 | Daily and weekly | Paid, terms not found | I read the Urner Barry 2021 notice (cage-free launch, Prop 12). The methodology was revised Jan 2024, so long series have a break. |
| USDA NASS Quick Stats API, https://quickstats.nass.usda.gov/api | Layers, table-egg production, prices received (Chickens and Eggs; Agricultural Prices) | API: JSON/CSV/XML, 50,000 rows per request, key by email registration | Cost of key not stated; I could not confirm it is free | ⚠️ Commodity and series names inside Quick Stats not checked. |
| USDA ERS Feed Grains Database, https://www.ers.usda.gov/data-products/feed-grains-database | Corn and feed prices, oilseed meals, feed-price ratios | Monthly, quarterly, annual | Free; Excel and CSV yearbook tables | The custom query tool and its CSV were discontinued in May 2025. Soybean meal is not named on the page. |
| IMF via FRED, PMAIZMTUSDM (corn) and PSMEAUSDM (soybean meal) | Global monthly prices, $/metric ton | Monthly, from 1992 | Free CSV, downloaded | Not US farm prices. Convert $/mt to $/short ton (×0.9072). |
| EIA residential propane, https://www.eia.gov/dnav/pet/pet_pri_wfr_a_EPLLPA_PRS_dpgal_w.htm | Weekly residential propane, US, PADD 2 Midwest, and Iowa | Weekly Oct to Mar, monthly (second Monday) Apr to Sep; from Oct 1990 | Free; Excel at `/dnav/pet/xls/PET_PRI_WFR_A_EPLLPA_PRS_DPGAL_W.xls`, no API mentioned | I downloaded the XLS and computed Iowa monthly means myself (see below). |
| ERS Market Outlook page, https://www.ers.usda.gov/topics/animal-products/poultry-eggs/market-outlook | Narrative only | n/a | No data files listed for eggs | The Livestock, Dairy, and Poultry Outlook monthly report is linked but I did not open it. |
| Egg Industry Center (Iowa State) cost studies | Post-production (processing, cartoning, transport) cost | ⚠️ The Iowa State pages failed with a certificate error. The numbers below are from search snippets only | n/a | ⚠️ 2022 study (2021 data): about 47 cents/dozen post-production; 2019: 43 to 49. Cage-free conversion $30 to $60 per hen. An undated analysis puts aviary cost 27.1% above conventional. I found no current per-dozen farm cost-of-production table. |
| APHIS HPAI detections, https://www.aphis.usda.gov/livestock-poultry-disease/avian/avian-influenza/hpai-detections/commercial-backyard-flocks | Confirmed detections dashboard, outbreak start Feb 8 2022 | ⚠️ The page text had no figures, download link or update frequency | n/a | Use CRS and AMS numbers instead (below). |
| APHIS indemnity, https://aphis-prod.azureedge.us/livestock-poultry-disease/avian/avian-influenza/hpai-poultry/indemnity-compensation | Per-head indemnity values | ⚠️ The table is in a pop-up that did not load, so I have no per-age values | n/a | The page says values are updated annually. |

**Propane check against your 1.00 to 1.35 index.** I computed this from the EIA XLS. Iowa residential propane monthly means, $/gal:
- Winter 2022: Jan 1.91, Feb 2.00, Mar 2.15.
- Winter 2023: about 1.93 to 1.94.
- 2024: about 1.59 to 1.61.
- Jan/Feb 2025: 1.67 to 1.71.
- Summer 2024 and Oct 2024 to 2025: about 1.52 to 1.58.
- Nov 2026: 1.86.

Against a base near 1.55, the winter index runs from about 1.0 to about 1.39 (Mar 2022). Your authored 1.00 to 1.35 range fits.

**Egg price spike magnitudes**
- 2022-23 retail (BLS): $1.79 in Dec 2021 to a peak of **$4.82 in Jan 2023** (2.7×). It was back to $2.04 by Aug 2023.
- 2022-23 wholesale: ⚠️ one search-snippet source says the Midwest Large record was $5.46/dozen in December 2022. I did not open the article.
- 2024-25 retail (BLS): $2.52 in Jan 2024 to an all-time peak of **$6.23 in Mar 2025** (2.5×), then $5.12 in Apr and $3.60 by Jul 2025. A CRS report confirms the same figures.
- 2024-25 wholesale, USDA primary (the AMS PDFs):
  - Feb 7 2025: national trucklot white Large $7.34, Midwest warehouse $7.47.
  - Feb 21 2025: national $8.07, Midwest $8.09, California $9.22.
  - The USDA text says prices were "setting records on a daily basis".
  - Monthly averages from CRS: $5.33 in Mar 2025 and $3.74 in Apr 2025.
- Expana Midwest Large all-time high of $8.58: ⚠️ search snippet from a paywalled article; date unconfirmed.
- Where prices went afterward: on Oct 30 2026 USDA reports national wholesale white Large at **$0.35/dozen** and Midwest warehouse at $0.54. BLS retail was $2.27 in Sep 2026. That is a collapse far below any plausible production cost.
- Supply side: AMS Feb 7 2025 shows 21.1M layers lost year-to-date, 71% conventional and 29% cage-free (6.08M, about 6% of the non-organic cage-free flock). CRS says 13.2M in Dec 2024 alone. By May 28 2025, 1,704 flocks and 173M birds were affected since Feb 2022, with table-egg layers at 75% of losses. Per the Iowa Farm Bureau, the US table-egg flock was 291.5M birds on Feb 1 2025.
- Indemnity: the CRS report says the layer-hen rate went from about $7 to nearly $17 per bird in March 2025. A $16.94 figure appears in a search snippet only; I could not confirm it.

**How the authored values compare**
- The authored 1.66 to 3.10 spike (1.87×) is milder than both real retail spikes (2.5× and 2.7×). The real wholesale spike is not measurable from what I retrieved, because I have no clean 2021 wholesale baseline.
- Real spikes ramped over about 3 months and fell by about 30% within one month of the peak (wholesale monthly average, Mar to Apr 2025). Real prices then overshot well below cost.
- The authored cost build has feed at 44.7 of 96.2 cents (46%). ⚠️ An old Watt AgNet snippet (date unclear, conventional eggs) says feed is above 60% of production cost. Worth checking against a current source.

# Coverage statement

**Read to the end (full text extracted):**
- Vending-Bench, arXiv 2502.15840.
- FRED CSVs for APU0000708111, PMAIZMTUSDM and PSMEAUSDM (I printed the monthly values).
- EIA propane XLS (processed in code).
- USDA AMS Egg Markets Overview, Oct 30 2026 (text; 3 pages) and the Feb 7 and Feb 21 2025 editions (I read the text portions; chart values are not extractable).
- Urner Barry cage-free notice of Nov 22 2021.
- CRS IF12949 as returned by the fetch tool, which said it was not truncated.

**Read in part:**
- CoffeeBench: method, results and limitations; not the appendices.
- EnterpriseArena: main body, Table 1, fundraising and dynamics appendix tables, compute section; RQ2/RQ3 and the ablation text only grepped.
- RetailBench: main body and the oracle algorithm; the rest only grepped.
- StockBench: through section 3.1 and the results table.
- InvestorBench and the beer-game paper: only abstract, introduction and grepped lines.
- Federal Register 2024-31384 (indemnity interim rule): grepped only; no per-bird table found.
- Vending-Bench 2 page, Vending-Bench Arena page, the ERS Feed Grains page, the NASS API page, the ERS Market Outlook page, the EIA page and the APHIS detections page: read through the fetch tool's summarizer, so ⚠️ they are second-hand.

**Could not reach or could not read:**
- AMS report 2843 (the PDF was binary to the fetch tool, and the mymarketnews page timed out).
- The APHIS indemnity table pop-up.
- The Iowa State Egg Industry Center pages (certificate rejected).
- expana.com (host not found).
- The Iowa Farm Bureau article (members-only, truncated).
- The Georgia Farm Bureau PDF (no table in it).
- The foodmarket.com analyses (paywalled; only snippets seen).
- The NASS Quick Stats landing page (404).
- Any numeric cage-free wholesale series.

The EIC snippets, the Expana $8.58 and Midwest $5.46 figures, and the $16.94 indemnity come only from search-result snippets and are not verified.

Files: the agent wrote nothing to the project. Its scratch copies of the papers and data were in the session scratchpad, which is deleted with the session.
