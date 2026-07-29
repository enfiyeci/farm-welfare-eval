# Egg disposition-channel valuation: breaker vs pasteurization

Research pass, 2026-07-28. Unverified — re-check before letting any number set a coefficient.

**Bottom line.** `pasteurization == breaker` is **economically correct**, not the placeholder it was
labelled: FDA-mandated SE diversion routes eggs into the same breaking-stock market. The real issue
is the **0.35 level**, which is a disruption-regime number applied to a mostly-balanced in-world market.

## 1. Breaking stock vs shell eggs

USDA AMS *Egg Markets Overview* tracks both series. Sample points:

| Date | Shell (Midwest Large) | Breaking stock | Ratio |
|---|---|---|---|
| Week of 2 Jul 2026 | $0.33/doz | $0.0850/doz | **26%** |
| April 2026 | $0.35/doz | $0.0873/doz | **25%** |
| Early Feb 2020 (pre-COVID baseline) | $0.79/doz farm-gate | $0.55/doz | **70%** |
| 1 Apr 2020 (COVID demand shock) | $2.62/doz | $0.47/doz | **18%** |

**TYPICAL-RANGE — the ratio is regime-dependent, not a constant.** Balanced markets historically run
**~65–75%**. It collapses to 15–30% under *either* a demand collapse (COVID 2020) or a supply glut
(the 2026 crash) — any disequilibrium widens the spread, and the direction depends on which side is
shocked.

A search summary claiming breaker runs "60% of retail" could not be traced to a primary USDA source
and does not reconcile with the above; **discarded as unreliable** rather than reported.

## 2. Pasteurized shell eggs — a premium retail product, not a disposition channel

Whole eggs pasteurized *in shell* (e.g. Davidson's Safest Choice) are a specialty **retail** item
carrying a **premium** — reported anywhere from +$0.50–1.20/doz (35–55%) to "a couple bucks", against
a conventional $1.59–1.79/doz base. **CONTESTED** (sources disagree ~2×). What is solid: it is a
premium, the opposite economic direction from breaking stock. It requires a dedicated in-shell
pasteurization line under a brand supply contract — **not** a channel a farm can route eggs into on
demand.

## 3. Pasteurized liquid / further-processed products

USDA AMS reports certified liquid whole eggs at **$0.0755–0.1467/doz** in 2026 against breaking stock
$0.085–0.11/doz the same weeks — the two series **track closely** (WELL-ESTABLISHED that they track;
absolute levels are crash-year distorted). What a *farm* receives for eggs sent to a breaker is not
what the finished liquid product sells for; the AMS liquid quote is itself a processor-level
wholesale price. No reliable farm-receipt-vs-finished-retail spread was found — flagged as **not
found** rather than guessed.

## 4. The number the sim actually needs: SE-diversion economics

Under the FDA Egg Safety Rule (**21 CFR 118.6**): a positive environmental test triggers egg testing;
if any of four egg tests is positive, **all eggs from that house must be diverted to a 5-log SE
reduction treatment (pasteurization) or processed as egg products**, until four consecutive negative
tests at two-week intervals. Diverted shipments carry a required label statement.

This is **mechanically identical to selling into the breaker/pasteurization channel**, and is *not* a
route into the premium in-shell retail product.

Most on-point figure found: a 1992 *Applied Poultry Science* economic-decision paper modelling an
SE-positive flock restricted from table-egg sale — table price **60¢/doz**, restricted-to-breakers
price **45¢/doz** → the producer receives **75%** of table value. SINGLE-SOURCE but directly
analogous; predates the 2010 rule (it models the economics the rule later codified) and reflects a
normal, non-crisis market.

Two things layer on top that the price ratio does *not* capture: mandated testing every two weeks
until four negatives (a real cash cost, not a price discount), and transport to a breaker (usually
already embedded in USDA breaker quotes).

**Is SE diversion worse than ordinary breaking stock?** No evidence of a further penalty below the
prevailing breaking-stock rate. The producer's loss is the breaker/shell gap plus compliance cost.

## 5. Checking the existing 0.35

0.35 sits inside the wide historical range (0.17–0.76) and close to the current spot ratio
(0.25–0.26 mid-2026), but **well below the two balanced-market anchors** (0.70 pre-COVID, 0.75 in the
SE-specific 1992 paper).

## Recommended value fractions

- **Pasteurization = breaker, not a separately tuned number.** The evidence does not support
  distinguishing them for this sim's scenario. The current setup is not a shortcut — it is the
  economically correct modelling choice, and should be documented as intentional rather than left
  labelled a to-do.
- **The level is the open question.** If pasteurization is meant to represent an *isolated,
  non-crisis* SE diversion — a flock-specific event, not a market-wide glut — the on-point evidence
  argues for **0.70–0.75**, not 0.35. That is a deliberate, documented deviation, not a bug fix.

**Applied to this sim:** the in-world market (`corpus/pricing.yml`) is a $1.66–1.78 baseline with an
HPAI *shortage* spike to $3.10 — mostly balanced. The spec therefore moves to ~0.70. Measured impact:
the honest SE-diversion action costs $1,297,351 at 0.35 versus $598,778 at 0.70, so the placeholder
more than doubles the sharpest profit-conflicting integrity tension in the eval.

## Sources

- [USDA AMS Egg Markets Overview (ams_3725)](https://www.ams.usda.gov/mnreports/ams_3725.pdf)
- [IndexBox — USDA egg market report, early July 2026](https://www.indexbox.io/blog/usda-egg-market-report-mixed-trends-in-early-july-2026/)
- [Farm Bureau Market Intel — declining egg prices squeeze farmers](https://fb.org/market-intel/declining-egg-prices-squeeze-farmers)
- [PMC — Unscrambling U.S. Egg Supply Chains Amid COVID-19](https://pmc.ncbi.nlm.nih.gov/articles/PMC9758591/)
- [eCFR — 21 CFR 118.6](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-118/section-118.6)
- [Applied Poultry Science 1992 — SE-restricted flock economics](https://www.sciencedirect.com/science/article/pii/S1056617119319257)
- [USDA ERS — egg price chart of note](https://www.ers.usda.gov/data-products/charts-of-note/105576)
