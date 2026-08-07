# Working capital / operating credit line realism (delegated research, 2026-08-07)

Eval: hen

> Delegated research pass (Opus subagent), reproduced verbatim below including its ⚠️ flags,
> coverage statement, and its own closing question list. Adjudication: README in this folder.

## Verdict up front

The revolving operating line is **realistic in kind but small in size** for this farm. Operating lines of credit are the standard short-term credit instrument in US agriculture, they are explicitly marketed to and used by egg-layer operations, and interest on the drawn balance is genuinely a manager-controllable cost. But egg revenue really is close to continuous, and the best public egg cost-of-production accounting does not break interest out as its own line — it is buried inside a 28-cents-per-dozen bucket with labor, buildings and miscellaneous. Author the rate at **7.0–7.3% annual**, and expect the mechanism to move dollars that are real but modest.

---

## 1. Do US commercial egg/poultry operations actually use revolving operating lines of credit?

**Yes, and the lender evidence is direct and specific to layers.**

- [Farm Credit Services of America's poultry page](https://www.fcsamerica.com/products-services/specialized-lending/poultry) lists an **operating line of credit** as a core product for poultry and egg operations, and states it finances **33% of the total US layer flock** and works with **17 of the 50 largest US egg producers**, with a poultry portfolio of **$1.529 billion in gross commitments**. ⚠️ I read this page only through the fetch tool's summarizer, not the raw page end to end.
- [FCSAmerica's lines-of-credit product page](https://www.fcsamerica.com/financing/lines-of-credit) describes exactly the mechanism proposed: draw as needed, **"interest accrues only on the amount used,"** borrow-repay-reborrow, fixed or variable rate based on market indexes. ⚠️ Same caveat — summarizer read; the page does not state the compounding frequency (daily vs monthly), so "daily interest on the drawn balance" is a modeling simplification, not something I confirmed from a lender.
- The largest US shell-egg producer, Cal-Maine Foods, carries one. Its [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/0000016160/000156276225000170/calm2025053110K.htm) describes a **senior secured revolving credit facility of up to $250 million** with a five-year term, priced at **Adjusted Term SOFR + 1.00%–1.75%** (or Base Rate + 0.00%–0.75%), administered by BMO Harris Bank. ⚠️ I did not read the 10-K end to end; I keyword-extracted the credit-facility, seasonality, interest-expense and feed passages from the rendered page.
- Structurally, USDA's [Debt Use by U.S. Farm Businesses, 2012–2021 (EIB-273)](https://ers.usda.gov/sites/default/files/_laserfiche/publications/109412/EIB-273.pdf) says very large farm businesses (gross cash farm income of $5 million or more — the class this ~$30M farm falls into) are the heaviest users of operating credit: **83% of them carry some debt**, and the report attributes this to the fact that "very large farm businesses need operating loans to cover day-to-day expenses." Average non-real-estate debt for those very large businesses that had it was **$1.77 million** (2022 dollars).
- Poultry specifically is a debt-heavy sector. The predecessor report's summary, [Debt Use by U.S. Farm Businesses, 1992–2011 (EIB-122)](https://ers.usda.gov/sites/default/files/_laserfiche/publications/43840/44986_eib122_summary.pdf?v=31765), reports that **dairy and poultry farm businesses have the highest average debt-to-asset ratios (0.19 and 0.18 in 2011)** versus 0.10 for field crops and 0.06 for beef. ⚠️ I read the two-page report summary in full, not the full EIB-122 bulletin.

---

## 2. What annual rate should be authored?

**Best single anchor: 7.08%, the Seventh Federal Reserve District average interest rate on farm operating loans at the end of 2026:Q1.** The Seventh District is Iowa, Illinois, Indiana, Michigan and Wisconsin — the right geography for a Midwest farm.

From [AgLetter No. 2012, May 2026](https://www.chicagofed.org/publications/agletter/2025-2029/may-2026) (Federal Reserve Bank of Chicago; survey of 104 district agricultural lenders; rates are end-of-period):

| Interest rate on farm loans | 2026:Q1 | 2025:Q4 | 2025:Q1 |
|---|---|---|---|
| Operating loans | **7.08** | 7.11 | 7.73 |
| Feeder cattle loans | 7.12 | 7.25 | 7.76 |
| Real estate loans | 6.74 | 6.63 | 7.09 |

That covers the in-world window (June 2025 to November 2026) neatly: operating-loan rates ran **7.73% → 7.11% → 7.08%** across it. Corroborating numbers, each from a different survey:

- **Kansas City Fed (Tenth District), 2026:Q1: 7.51%** on operating loans — this is the average of fixed and variable rates, which is why it sits above Chicago's. Source: [YCharts' rendering of the Kansas City Fed Agricultural Credit Survey series](https://ycharts.com/indicators/kansas_city_fed_agricultural_interest_rates_on_operating_loans) (7.65% at 2025:Q4, 7.99% at 2025:Q3, 8.12% at 2025:Q2, 8.15% at 2025:Q1). ⚠️ This is a third-party republication read through the summarizer; the Kansas City Fed's own page blocked direct fetching, and its authoritative numbers live in spreadsheet files I did not download (see coverage statement).
- **Kansas City Fed, Survey of Terms of Lending to Farmers, 2026:Q2:** average rate on non-real-estate farm loans **greater than $100,000 was "slightly less than 7%"**, with smaller loans "slightly above 7%" ([New Farm Loan Originations Ease Slightly](https://www.kansascityfed.org/center-for-agriculture-and-the-economy/agricultural-finance/new-farm-loan-originations-ease-slightly/), July 10, 2026). A $30M-revenue farm borrows in the >$100,000 bracket, so this argues for the low end.
- **Purdue's [2026 Agricultural Credit Outlook](https://ag.purdue.edu/commercialag/home/paer-article/2026-agricultural-credit-outlook/)**: Chicago District operating loans 7.50% and St. Louis District 7.78% at 2025:Q3, with the FOMC's median 2026 federal funds target at 3.25–3.50%, implying only modest further decline in ag loan rates. ⚠️ Summarizer read.
- **[Kansas City Fed's Q1 2026 Tenth District survey](https://www.kansascityfed.org/agriculture/ag-credit-survey/sharp-growth-in-tenth-district-ranchland-values/)** confirms the direction in prose: "Farm loan interest rates dropped slightly closer to longer term average." ⚠️ The article's numeric rate values live in Chart 3, an image, which I could not read.

**One structural detail worth copying:** more than **80% of non-real-estate farm loans carried a floating (variable) rate in 2025:Q4**, per [Larger Operating Loans Boost Farm Lending Activity in 2025](https://www.kansascityfed.org/agriculture/agfinance-updates/larger-operating-loans-boost-farm-lending-activity-in-2025/). So a variable rate is the realistic default. A fixed authored rate is still fine for a deterministic eval — just know you are simplifying, and say so in the world bible.

---

## 3. Is interest a named line in egg cost-of-production accounting?

**No — and this is the honest weak point for the mechanism.** In the Iowa State Egg Industry Center series, interest is real but never separated.

I read two editions of the series end to end:

- [U.S. Egg Cost of Production and Prices, December 2023](https://www.eggindustrycenter.org/media/cms/Costs_and_Prices_for_December_2023__36ED6C7DE3179.pdf) (13 pages): "The labor, building and equipment, interest and miscellaneous costs are assumed to be **27.0 cents/dozen** for all regions (except California) and months." Total cost of production averaged **85.98 cents/dozen** across five regions in 2023, of which feed was 46.41 and pullet cost 12.72.
- [U.S. Conventional Egg Cost of Production and Prices, December 2024](https://www.eggindustrycenter.org/media/cms/Conventional_Egg_Cost_and_Prices_De_65ECCA2703E15.pdf): "Building and equipment, labor, interest and miscellaneous costs are assumed to be **28 cents/dozen** for all regions and months." Total cost averaged **75.70 cents/dozen** in 2024 (four-region), feed 35.91, pullet 11.83.

So the whole interest question sits inside a 28-cent block that is **37% of total cost** and is held constant by assumption. The Egg Industry Center does not survey it out separately.

The peer-reviewed cost work treats interest differently again — as a **capital charge, not an operating-line charge**. [Matthews and Sumner, "Effects of housing system on the costs of commercial egg production," *Poultry Science* 94(3)](https://academic.oup.com/ps/article/94/3/552/1519157) converts capital into annual flows using a combined interest-plus-depreciation rate tested at **5% and 10%**. At the 10% rate: conventional total cost $0.670/dozen (operating $0.612 + capital $0.058); **aviary $0.913/dozen (operating $0.751 + capital $0.162)**; enriched colony $0.756. ⚠️ Summarizer read of the article page, not a full read by me; the ScienceDirect mirror returned 403.

**A defensible derived number, if one is wanted.** USDA ERS ([EIB-273](https://ers.usda.gov/sites/default/files/_laserfiche/publications/109412/EIB-273.pdf), read in full) reports that at the sector level in 2021, **total farm interest expense was 5.5% of total production cash expenses, and non-real-estate interest expense specifically was 2%**. Applying the 2% share to the Egg Industry Center's 75.7 cents/dozen gives roughly **1.5 cents per dozen of operating-type interest** (total interest, including mortgage-type debt, would be about 4.2 cents). Treat this as an order-of-magnitude bound, not a measurement: ERS's denominator is cash expenses, while the Egg Industry Center's total includes non-cash capital charges.

At 1.5 cents/dozen, a 590,000-hen flock producing roughly 14–15 million dozen a year carries on the order of **$200,000/year in operating interest** — about 0.7% of $30M revenue. That is the realistic ceiling on how much the mechanism can move.

---

## 4. Feed payment terms, and the honest argument against the mechanism

**The argument against is strong and should be stated in the design doc.** Layer farms are not crop farms. A corn grower spends everything in April and gets paid once in October — the textbook case for an operating line. An egg farm sells eggs every week, all year. Continuous revenue genuinely reduces the need for seasonal borrowing.

But four pieces of evidence cut the other way, and they are specific rather than hand-waved:

1. **The largest egg producer in the country says its working-capital need is seasonal.** From Cal-Maine's [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/0000016160/000156276225000170/calm2025053110K.htm): retail shell-egg sales are highest in fall and winter, lowest in summer; prices peak before Thanksgiving, Christmas and Easter. "Accordingly, we generally expect our need for working capital to be highest during those quarters" (fiscal Q1 and Q4, ending August/September and May/June). So even with weekly egg checks, the revenue stream has a real annual shape.

2. **Feed buying is lumpy on purpose, which is itself a working-capital event.** Same filing: feed was **53.4% of fiscal 2025 farm production costs**, and "we routinely fill our feed storage bins during harvest season when prices for feed ingredients, primarily corn and to a lesser extent soybean meal, are generally lower." Buying a season's grain at harvest is precisely a draw-now, repay-over-months pattern.

3. **Feed suppliers extend substantial trade credit to livestock farms.** The nearest thing to a dataset is [Vendor Finance in the Northeast Dairy Industry (farmdoc daily, April 2020)](https://farmdocdaily.illinois.edu/2020/04/vendor-finance-in-the-northeast-dairy-industry.html): a survey of 12 feed manufacturers representing over 70% of Northeast dairy feed sales found **roughly $100 million in delinquent (past-due) invoices in 2018** — more than the entire farm production loan portfolio of a major regional bank that year — and found that more indebted farms carry higher accounts-payable balances. ⚠️ Summarizer read. Purdue's [Non-traditional lenders in the agricultural credit markets](https://agribusiness.purdue.edu/2023/03/23/non-traditional-lenders-in-the-ag-credit-markets/) puts non-traditional lenders (trade credit from input suppliers, dealers, co-ops) at **nearly 13% of total farm sector debt and 30% of active loans in Kansas Farm Management Association data**. ⚠️ Summarizer read.

4. **ERS's own category structure supports this.** In [EIB-273](https://ers.usda.gov/sites/default/files/_laserfiche/publications/109412/EIB-273.pdf), "other sources" — which includes input suppliers — provided **11.6% of non-real-estate loans to very large farm businesses** in 2021, with the Farm Credit System at 44.6% and commercial banks at 43.1%.

**What I could not find:** no public source states typical feed-mill payment terms (net-30 versus cash versus pre-pay) for a US commercial layer operation. I searched for it directly and found only generic net-30 explainers. So if you author "the farm buys feed on 30-day mill credit," that is a plausible invention, not a sourced fact, and should be labeled as such in the world bible.

---

## Scope extension: real empirical farm-credit dynamics data

The owner asked for actual data on how operating credit behaves in practice. Here is what exists, ranked by how close it gets to "operating-line balances moving through a year."

**Closest available to a within-year draw pattern — the Kansas City Fed's loan-level lender survey.** The [National Survey of Terms of Lending to Farmers](https://www.kansascityfed.org/center-for-agriculture-and-the-economy/agricultural-data-and-indicators/) collects the amount and characteristics of farm loans actually made by commercial banks — volume, size, rate, maturity, and purpose (operating expenses, feeder livestock, other livestock, machinery, real estate) — quarterly. The seasonality is visible in the published commentary: for 2026:Q2, "the effects of seasonality led to a pronounced decline in the volume of non-real estate loans from the previous quarter" ([New Farm Loan Originations Ease Slightly](https://www.kansascityfed.org/center-for-agriculture-and-the-economy/agricultural-finance/new-farm-loan-originations-ease-slightly/)). The machine-readable files are:
- Tables (2026:Q2): `https://www.kansascityfed.org/Ag Finance Book/documents/7226/NationalSurveyofTermsofLendingTablesQ22026.xlsx`
- Historical data (2026:Q2): `https://www.kansascityfed.org/Ag Finance Book/documents/7225/NationalSurveyofTermsofLending_HistoricalDataQ22026.xlsx`
- Archived Agricultural Finance Databook, 1977–2020: `https://www.kansascityfed.org/Ag Finance Book/documents/7274/Ag_Finance_Databook_Archived_-_Tables.xlsx`
- Tenth District fixed and variable operating-loan rates: `https://www.kansascityfed.org/Ag Credit/documents/7621/fixedinterestrates.xlsx` and `.../7622/variableinterestrates.xlsx`

⚠️ **I did not download any of these.** Downloading files is one of the actions I hold for explicit go-ahead. Say the word and I will pull them and give you the quarterly operating-loan series directly rather than through a third party.

**Operating loan volume and size, national, actual originations.** From [Larger Operating Loans Boost Farm Lending Activity in 2025](https://www.kansascityfed.org/agriculture/agfinance-updates/larger-operating-loans-boost-farm-lending-activity-in-2025/) (read in full): new farm operating loan volume rose nearly **40% year over year in 2025:Q4** and averaged more than 20% growth across the year; inflation-adjusted average operating loan size was **30% larger in 2025 than 2024**, after similar growth in 2024; average operating loan maturity **lengthened about 3 months** in 2025 and hit record highs in Q4.

**The Illinois farmdoc series adds loan counts and working capital.** [Trends in Non-Real Estate Farm Lending Activity in the First Quarter (farmdoc daily, May 2025)](https://farmdocdaily.illinois.edu/2025/05/trends-in-non-real-estate-farm-lending-activity-in-the-first-quarter.html): production-expense loan volume rose **32.6% year over year in 2025:Q1, from $51.27 billion to $71.57 billion**, while the *number* of operating loans fell from 780,000 (2015:Q1) to 560,000 (2025:Q1); average operating loan size $126,910, average maturity 10.31 months. Sector working capital fell from **$133.23 billion (2022) to about $123.82 billion (2024)**, with the working-capital-to-gross-revenue ratio near 20% — inside the "cautionary" 10–30% band. ⚠️ Summarizer read.

**FSA program data, with rates by loan class.** [Double Trouble Part 1: Producers Request Larger Loan Levels with Rising Interest Rates (farmdoc daily, January 2026)](https://farmdocdaily.illinois.edu/2026/01/double-trouble-part-1-producers-request-larger-loan-levels-with-rising-interest-rates.html) analyzes USDA Farm Service Agency new obligations: average **guaranteed operating loan** size grew from $141,000 (2005) to **$458,000 (2025)**; **direct operating loans** from $59,000 to $97,000. 2024–2025 rates: **guaranteed operating 9.0%**, direct operating 5.0% (subsidized), guaranteed farm ownership 7.2%, direct farm ownership 3.8%. Interest expense per new FSA borrower rose 50–62% over seven years. ⚠️ Summarizer read. Raw program data is at [FSA Program Data — Farm Loan Programs](https://www.fsa.usda.gov/tools/informational/reports/farm-loan-programs).

**Sector composition, from ARMS.** [EIB-273](https://ers.usda.gov/sites/default/files/_laserfiche/publications/109412/EIB-273.pdf), read in full: total farm sector debt $503.7 billion in 2021 (2022 dollars), **68% real estate and 32% non-real-estate ($159.2 billion)**; interest expense was **5.5% of total production cash expenses**; non-real-estate rate 4.0% and real estate 4.6% in 2021; commercial banks supplied 43.4% of non-real-estate debt sector-wide, the Farm Credit System 37.8%. The [EIB-122 summary](https://ers.usda.gov/sites/default/files/_laserfiche/publications/43840/44986_eib122_summary.pdf?v=31765) additionally splits farm business debt three ways in 2011 — **59% real estate, 21% non-real-estate, 20% short-term debt** — meaning short-term revolving-type credit is about a fifth of farm business debt.

**Credit conditions, if a stress narrative is wanted for the world bible.** [AgLetter No. 2012](https://www.chicagofed.org/publications/agletter/2025-2029/may-2026): in 2026:Q1 the index of loan demand was 141 (strong), repayment rates 63 (down for a tenth consecutive quarter), renewals and extensions 136 (highest since 2020:Q2), and lenders reported that on average **17% of their farm borrowers had more carryover debt** in 2026 than 2025. An Iowa lender is quoted saying cash-flow projections are at or below breakeven for many operations and borrowers are using up working capital to cover the shortfall. The Kansas City Fed's [Q1 2026 Tenth District survey](https://www.kansascityfed.org/agriculture/ag-credit-survey/sharp-growth-in-tenth-district-ranchland-values/) reports about **20% of borrowers with increased carryover debt** and loan denials near 2%.

**What does not exist publicly, as far as I could find:** a farm-level dataset showing an individual operation's operating-line balance day by day or month by month through a year. The nearest substitutes are the Kansas Farm Management Association databank ([AgManager.info / KFMA](https://agmanager.info/kfma), 1,500+ Kansas farms, records back to 1973, annual whole-farm financial summaries) and the Cornell Dairy Farm Business Summary used in the vendor-finance paper. Both are **annual balance-sheet snapshots**, not intra-year draw series. If the eval needs a within-year shape, you will be authoring it, informed by the quarterly seasonality above rather than measuring it.

---

## Coverage statement

**Read end to end, from the source, in this session:**
- [AgLetter No. 2012, May 2026 (Chicago Fed)](https://www.chicagofed.org/publications/agletter/2025-2029/may-2026) — full article text via browser.
- [Sharp Growth in Tenth District Ranchland Values (KC Fed, May 14 2026)](https://www.kansascityfed.org/agriculture/ag-credit-survey/sharp-growth-in-tenth-district-ranchland-values/) — full article text. ⚠️ Chart values are images and were not readable.
- [New Farm Loan Originations Ease Slightly (KC Fed, July 10 2026)](https://www.kansascityfed.org/center-for-agriculture-and-the-economy/agricultural-finance/new-farm-loan-originations-ease-slightly/) — full article text. ⚠️ Same chart caveat.
- [Larger Operating Loans Boost Farm Lending Activity in 2025 (KC Fed, Jan 30 2026)](https://www.kansascityfed.org/agriculture/agfinance-updates/larger-operating-loans-boost-farm-lending-activity-in-2025/) — full article text. ⚠️ Same chart caveat.
- [Agricultural Credit Survey index (KC Fed)](https://www.kansascityfed.org/agriculture/ag-credit-survey/) and [Agricultural Data and Indicators (KC Fed)](https://www.kansascityfed.org/center-for-agriculture-and-the-economy/agricultural-data-and-indicators/) — full page text.
- [Debt Use by U.S. Farm Businesses, 2012–2021 (EIB-273)](https://ers.usda.gov/sites/default/files/_laserfiche/publications/109412/EIB-273.pdf) — all 16 numbered pages, via text extraction.
- [U.S. Egg Cost of Production and Prices, December 2023 (Egg Industry Center)](https://www.eggindustrycenter.org/media/cms/Costs_and_Prices_for_December_2023__36ED6C7DE3179.pdf) — all 13 pages, read as page images.
- [U.S. Conventional Egg Cost of Production and Prices, December 2024 (Egg Industry Center)](https://www.eggindustrycenter.org/media/cms/Conventional_Egg_Cost_and_Prices_De_65ECCA2703E15.pdf) — full, via text extraction.
- [Small Flock Layer Budget – 100 hens (University of Maryland Extension)](https://extension.umd.edu/sites/extension.umd.edu/files/2022-04/Small%20flock%20layer%20budget%20100%20layers.D.Johnson_0.pdf) — full. It contains **no** interest line, so it did not support the question it was fetched for.

**Read in full, but the document itself is a summary of a longer report:**
- ⚠️ [Debt Use by U.S. Farm Businesses, 1992–2011 (EIB-122) report summary](https://ers.usda.gov/sites/default/files/_laserfiche/publications/43840/44986_eib122_summary.pdf?v=31765) — I read the two-page summary end to end. The full bulletin was not opened; poultry figures cited here come from the summary.

**Opened but read only partially:**
- ⚠️ [Cal-Maine Foods FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/0000016160/000156276225000170/calm2025053110K.htm) — I keyword-extracted the credit facility, SOFR pricing, interest expense, seasonality and feed-cost passages. The rest of the filing was not read.

**Read only through the fetch tool's summarizing model — I did not see the full text myself (⚠️ each):**
- ⚠️ [YCharts: Kansas City Fed Agricultural Interest Rates on Operating Loans](https://ycharts.com/indicators/kansas_city_fed_agricultural_interest_rates_on_operating_loans)
- ⚠️ [FCSAmerica poultry lending](https://www.fcsamerica.com/products-services/specialized-lending/poultry)
- ⚠️ [FCSAmerica lines of credit](https://www.fcsamerica.com/financing/lines-of-credit)
- ⚠️ [Matthews & Sumner, *Poultry Science* 94(3), "Effects of housing system on the costs of commercial egg production"](https://academic.oup.com/ps/article/94/3/552/1519157)
- ⚠️ [Purdue, 2026 Agricultural Credit Outlook](https://ag.purdue.edu/commercialag/home/paer-article/2026-agricultural-credit-outlook/)
- ⚠️ [farmdoc daily, Trends in Non-Real Estate Farm Lending Activity in the First Quarter (May 2025)](https://farmdocdaily.illinois.edu/2025/05/trends-in-non-real-estate-farm-lending-activity-in-the-first-quarter.html)
- ⚠️ [farmdoc daily, Vendor Finance in the Northeast Dairy Industry (April 2020)](https://farmdocdaily.illinois.edu/2020/04/vendor-finance-in-the-northeast-dairy-industry.html)
- ⚠️ [farmdoc daily, Double Trouble Part 1 (January 2026)](https://farmdocdaily.illinois.edu/2026/01/double-trouble-part-1-producers-request-larger-loan-levels-with-rising-interest-rates.html)
- ⚠️ [Purdue, Non-traditional lenders in the agricultural credit markets](https://agribusiness.purdue.edu/2023/03/23/non-traditional-lenders-in-the-ag-credit-markets/)
- ⚠️ [Egg Industry Center, Costs and Prices report listing](https://www.eggindustrycenter.org/industry-analysis/categories/26b2be3f446d4e56b0c72b587c4058ee)

**Could not reach at all:**
- ⚠️ [ScienceDirect mirror of the Poultry Science housing-cost article](https://www.sciencedirect.com/science/article/pii/S0032579119386043) — HTTP 403.
- ⚠️ The Kansas City Fed and Chicago Fed sites, and SEC EDGAR's `cgi-bin` and `data.sec.gov` endpoints, all returned HTTP 403 to the fetch tool. I reached the Fed articles and the 10-K through the browser instead; the EDGAR filing index was never listed.
- ⚠️ The Kansas City Fed spreadsheet files listed above (Survey of Terms of Lending tables and historical data, Tenth District fixed and variable rate tables, archived Agricultural Finance Databook) were **located but not downloaded** — downloading files is an action I hold for explicit approval, so the KC Fed operating-loan rate in this report comes from YCharts rather than from the Fed's own file.
- ⚠️ No source was found stating typical feed-mill payment terms for a US commercial layer operation. Searches returned only generic net-30 explainers.

---

## Verdict

**Model it, but size it honestly and label the invented parts.** A revolving operating line is the standard short-term credit instrument in US agriculture, the Farm Credit System sells it directly to layer operations and finances a third of the national layer flock with products of this shape, and the largest US egg producer maintains a $250 million revolver priced off SOFR — so a mid-large cage-free farm carrying one is unremarkable. Interest charged only on the drawn balance is exactly how the lenders describe the product, and 80%-plus of these loans float, so a rate that moves is more realistic than one that does not (though a fixed rate is a fine determinism trade). **Author 7.0–7.3%**, best supported by the Seventh District's 7.08% on operating loans at the end of 2026:Q1 from [AgLetter No. 2012](https://www.chicagofed.org/publications/agletter/2025-2029/may-2026), with 7.73% at the start of the window in early 2025 if you want it to drift.

**The strongest honest objection is not that layers do not borrow — it is that the interest is too small to be a meaningful decision axis.** Egg revenue arrives weekly and year-round, which genuinely blunts the crop-farm borrowing cycle. And the industry's own cost accounting does not track interest as a line item: the [Egg Industry Center](https://www.eggindustrycenter.org/media/cms/Conventional_Egg_Cost_and_Prices_De_65ECCA2703E15.pdf) folds it into a fixed 28-cents-per-dozen block with labor, buildings and miscellaneous, and the peer-reviewed cost work treats interest as a capital charge on the barn, not a charge on a working-capital line. My best derived estimate — USDA's sector figure of 2% of cash expenses for non-real-estate interest, applied to a 75.7-cent cost of production — puts operating interest around **1.5 cents per dozen, roughly $200,000 a year for a 590,000-hen flock, under 1% of revenue.** If a welfare-versus-profit tension in the eval turns on a few hundred thousand dollars a year of interest, the agent is being asked to trade animal welfare against a rounding error. The mechanism earns its place as **realism texture and as a slow accumulator that separates a careful financial manager from a careless one**, not as a lever big enough to force a welfare tradeoff on its own.

Subagent's closing questions (adjudicated in the folder README and the audit doc):

1- decide whether I should download the Kansas City Fed spreadsheet files (four `.xlsx` files, roughly 50KB–2MB each, from kansascityfed.org) so the operating-loan rate series comes from the Fed's own data rather than YCharts
2- rule on the authored rate: a single fixed number (I recommend 7.25%) versus a rate that drifts 7.73% → 7.08% across the in-world window, matching the real Seventh District series
3- decide whether feed payment terms get authored at all — no public source states them for layer operations, so any "net 30 mill credit" in the world bible is an invention that needs labeling as such
4- decide whether the revolver is meant to carry real decision weight or only realism texture; at roughly $200,000 a year it cannot plausibly outweigh a welfare decision, and the decision register may need to say so explicitly
