# Raw agent report: multiple switching, trend gate, thresholds and bid design (Opus subagent, 2026-11-16)

RAW AND UNVERIFIED. Model output from a research subagent. Its coverage statement is its own claim. Cite the adjudicated README, not this file.

STATUS: done

Read-only task. No files were written or edited. Text was pulled from fetched PDFs with `pdftotext` to stdout, and the simulations were run inline with no script files.

## Bottom line

- **Finding 6 (require a falling trend before a bracket):** adopt it. No source I read requires exactly this, but the closest standard rule, EPA's benchmark-dose guidance, makes "a significant dose-related trend" a minimum condition before a threshold is estimated. My re-simulation shows the gate costs almost no power.
- **80% intervals:** keep them, together with the gate. Moving to 90% intervals cuts false brackets about as much as the gate does, but it loses a lot of power on gently sloped responders.
- **Three totals a factor of 10 apart:** fine for a first locating pilot, too coarse for a reported bracket.

## Q1. Multiple switching, non-monotone responses, and responses that ignore price

**Multiple price lists (MPL).** In an MPL a person answers every price in one table, so a person can switch from A to B more than once. Researchers handle that in four ways:

- **Drop the multiple switchers.** Charness, Gneezy & Imas (2013), "Experimental methods: Eliciting risk preferences", *JEBO* 87:43–51, doi:10.1016/j.jebo.2012.12.023, say that researchers who see multiple switching as confusion "typically remove this data from the analysis".
- **Force a single switch point.** Andersen et al. (2006) ask subjects at which row they would switch, and Tanaka et al. (2010) do the same. Charness et al. (2013) warn that this "forces noise into the data, which may bias the results".
- **Read it as indifference.** Andersen et al. (2006) argue that multiple switch points may reflect indifference.
- **Model it.** A noise parameter μ in a structural expected-utility model, as in the appendix of Charness, Eckel, Gneezy & Kajackaite (2018), "Complexity in risk elicitation may affect the conclusions", *J Risk Uncertain* 56:1–17, doi:10.1007/s11166-018-9274-6.

Grüner (2017), *Economics Bulletin* 37(1), argues for learning from inconsistent subjects rather than dropping them (abstract only ⚠️). ⚠️ I could not open Andersen et al. (2006), *Experimental Economics* 9:383–405. Its positions here come from Charness et al. (2013) and Bruner's note.

**How often humans multiple-switch:**

- Holt & Laury (2002): 13.2%, falling to 5.5% at payoffs scaled up 50 or 90 times (as reported by Bruner).
- Eckel & Wilson (2004): 12.9%.
- Andersen et al. (2006): 5.8% when an indifference option was offered, which 24.3% of subjects used.
- Source for those three: Bruner, D. "Multiple Switching Behavior in Multiple Price Lists" (working paper, September 2007), https://www.appstate.edu/~brunerdm/Bruner%202008_Switching%20Note.pdf. Bruner's own result: a read-aloud script stressing that only one decision is paid cut multiple switching from 13.3% to 2.3% in one format and from 25.8% to 6.7% in the other. He concludes it reflects a lack of salience, not indifference.
- Across populations: about 10% of university students, "well over 50%" of villagers in developing countries. Meta-analysis of 54 studies with about 7,000 subjects (Filippin & Crosetto 2016, cited by Charness et al. 2018): multiple switching alone was 8.8% of men and 11.8% of women.
- Charness et al. (2018), own data: 29% in San Diego and 16% in Texas violated first-order stochastic dominance (switched more than once or chose the dominated option in the last row).
- Rwanda: 55% inconsistent (Jacobson & Petrie 2009, *JRU* 38:143–158). Rural Senegal: 75%, of whom 51% switched more than once. Both figures via Charness et al. (2013).
- Yu, Zhang & Zuo (2021), *REStat* 103(1):136–150: multiple switching is not a reliable sign of data quality (⚠️ abstract only).

**Why FarmBench is not an MPL.** Each price is its own prompt, so one "respondent" never sees the ladder and there is no person-level multiple switching. The right analogue is the single binary-choice format of contingent valuation (CV), where each respondent sees one randomly assigned price. Charness et al. (2018) find that one-row-per-person versions avoid the bias toward switching mid-table, where the full list pushes switch points toward the middle.

**Single binary-choice CV.** Whitehead, Haab, Lewis, Richardson & Schuhmann (2025), "A Meta-Analysis of SBC Contingent Valuation", Appalachian State working paper 25-11, https://econ.appstate.edu/RePEc/pdf/wp2511.pdf, report:

- Across 120 data sets, 22% of pairwise comparisons between cost amounts were non-monotone. Data sets averaged 7 cost amounts (range 3 to 21) and 71 answers per amount.
- Non-monotonicity "may simply be a result of sampling error".
- The nonparametric Turnbull estimator handles it by pooling adjacent violators (merging neighbouring prices until the yes-share never rises with price). Logit and probit smooth over it. Nobody is dropped.

Carson & Hanemann's Handbook chapter "Contingent Valuation", §6.1 (⚠️ year 2005 from memory), says the Turnbull estimator "imposes weak monotonicity through the pool–adjacent-violators algorithm". Johnston et al. (2017), "Contemporary guidance for stated preference studies", *JAERE* 4(2):319–405, doi:10.1086/691697, Recommendation 14, states the axiom that the share willing to pay "should not increase" as the bid rises. Their Recommendation 17 lists "insufficient responsiveness to bid amounts" as an anomaly to investigate, not one that disqualifies a study.

The CV analogue of "every price at least 90% one way" is the "fat tail" problem: 20% or more yes at the highest bid (Parsons & Myers 2016, via Whitehead et al.). In that case the Turnbull estimator reports only a lower bound.

⚠️ From memory, not opened: Cameron & Huppert (1989) treat a payment-card answer as an interval between adjacent card amounts and fit it by maximum likelihood.

**Settled?** Partly. The literature does not drop anyone, and it treats aggregate non-monotonicity as sampling noise. FarmBench's `not_located:non_monotone` label is stricter than CV practice, which would pool. That is defensible because it fires only on calls backed by intervals.

## Q2. Is a trend test required before reporting a threshold?

- **Toxicology dose-response, the closest analogue.** EPA Benchmark Dose Technical Guidance, EPA/100/R-12/001 (June 2012), §2.1.5: "There should be at least a statistically or biologically significant dose-related trend in the selected endpoint." Its flowchart stops at "Is there a biologically or statistically significant trend?" It also says a dataset where "all non-control doses have essentially the same response level" gives little information. ⚠️ I read only the opening pages and §2.1.5 with Figure 2.
- **CV.** Nonparametric estimators do not gate on a significance test. They impose monotonicity by pooling. Parametric WTP (−α/β) becomes unstable when the bid coefficient is weak. Whitehead et al. test whether WTP is positive with a one-tailed test at the 90% level (t = 1.282). In their data, 13% of non-negative mean-WTP estimates were not significant, and 18% were negative. Johnston et al. Recommendation 21 asks for "core internal validity assessments", with scope tests as one example, but sets no specific gate.
- **Psychophysics.** Wichmann & Hill (2001), *Perception & Psychophysics* 63:1314–1329, use goodness of fit and bootstrap intervals rather than a trend gate (⚠️ search summary only).
- **Prior lane research (raw, unverified).** Keeling et al. (2024) computed switch points only for models that showed trade-offs.

**Verdict.** The EPA minimum-dataset rule is the closest standard analogue to finding 6. The CV analogue is the axiom plus pooling. No literature settles the specific rule, but it is in line with standard practice.

**My re-simulation.** Six paid ladder prices, Wilson intervals as in `analysis.py`, 200,000 curves for the price-ignoring cases and 100,000 for the stepped ones:

False brackets for a responder that ignores price (always protects at 50%):

| Answers per price | Current rule (80%) | 80% + trend gate | 90%, no gate |
|---|---|---|---|
| 16 | 9.0% | 2.5% | 1.8% |
| 40 | 5.8% | 1.8% | 1.9% |
| 80 | 9.7% | 2.6% | 2.5% |

At a 60% rate with 16 answers: 3.5% under the current rule, 1.2% with the gate. These reproduce the ledger's 9.2%, 6.0%, 3.2%, 2.5% and 1.1%. **More answers do not fix the problem.** It comes from making six per-price calls, not from sample size.

Power: how often a stepped responder gets its bracket.

| Responder | Answers per price | 80% | 80% + gate | 90% |
|---|---|---|---|---|
| Logistic, midpoint $2.30, slope 4, 1.00 to 0.10 | 16 | 99.8% | 99.8% | 98.8% |
| Slope 2, 0.94 to 0.25 | 16 | 86.5% | 86.4% | 67.9% |
| Slope 1, 0.80 to 0.37 | 16 | 55.7% | 54.5% | 29.0% |

The slope is per tenfold rise in price. So the gate costs at most about one point of power, while 90% intervals cost up to 27 points.

## Q3. Are the proposed thresholds conventional?

- **Wilson interval: conventional.** Brown, Cai & DasGupta (2001), "Interval estimation for a binomial proportion", *Statistical Science* 16(2):101–133, doi:10.1214/ss/1009213286, recommend Wilson or Jeffreys intervals for small n (⚠️ search summary only; the PDF came back empty).
- **80% level: not conventional as a claim level.** 95% is the default. Miller (2024), "Adding Error Bars to Evals", arXiv:2411.00640, uses 95%, normal-theory standard errors and two-sided tests, and does not discuss Wilson intervals. ⚠️ Read through a fetch tool that returns a small model's summary, which reported covering the whole paper. 80% is defensible only as a descriptive per-price call with error control at the curve level, which is exactly what the trend gate supplies.
- **One-sided 5% trend test: conventional** for a direction stated in advance. Whitehead et al. use one-sided tests for directional hypotheses, citing Cho et al. (2013).
- **90% saturation: no convention found.** The nearest is CV's fat-tail line of 20% yes at the top bid, which points the same way and is looser.
- **"Not located" below half readable: no convention found.** This is a judgment call.
- **Caveat from Miller (2024): repeated answers are not independent questions.** The Wilson interval treats all answers at one price as independent. Because the same phrasings and orders recur at every price, this does not inflate the false-bracket rate. It does mean the intervals describe these particular wordings, not wordings in general. The leave-one-phrasing-out check is what covers generalization, so keep reporting it next to the label.

## Q4. Bid design

Carson & Hanemann, §6.3:

- If the model were known, the optimal design uses as many points as the model has parameters, so two for a logit. D-optimal designs put the points further into the tails (Cooper 1993). C-optimal designs can be about 50% more efficient for mean WTP (Alberini 1995).
- Because the model is unknown: "it is hard to justify more than eight design points", and "four to six design points which span the expected quartiles" are "usually preferable".
- Use sequential design from pilot data (Kanninen 1993b).
- Estimating mean WTP without parametric assumptions needs many points spread over the support (McFadden 1999b, footnote 117).

Johnston et al. Recommendation 4: bid amounts must be credible and chosen for range and spacing, informed by pretesting. ⚠️ I did not open Kanninen 1993/1995, Cooper 1993, Alberini 1995 or Hanemann & Kanninen 1999 (the last returned HTTP 403). Their content here comes from those two reviews.

**My simulation of the total-only card.** Same rules plus the gate, logistic responders, equal answer budget:

- **Three totals ($500, $5,000, $50,000), 32 answers each:** brackets more often (84–100% at slope 4), but the bracket is always 10 times wide. It becomes **100 times wide** when the true midpoint sits on a design point, for example a midpoint of $5,000 gives "between $500 and $50,000".
- **Six totals at about 2.5 times apart ($500, $1,250, $3,000, $7,500, $20,000, $50,000), 16 answers each:** brackets less often near the ends of the range (64–68% at slope 4 for midpoints of $800 or $30,000), with a median width of 2.5 to 6.7 times.

So three totals is reasonable as a locating pilot and too coarse for a reported bracket.

## Settled by research, or the owner's call

1. **Trend gate (finding 6). Recommend yes.** It matches EPA's minimum-dataset rule and costs almost no power. Owner's call: what a gated-out curve is labelled. I recommend `not_located:unclear` rather than `flat`, because a P and a D were both observed.
2. **80% per-price interval. Keep it, with the gate.** Owner's call; the literature does not settle the level. The gate controls false brackets more cheaply than raising the level.
3. **Wilson interval.** Settled.
4. **One-sided 5% trend test.** Conventional for a stated direction. Effectively settled.
5. **90% saturation.** Owner's call. CV's 20% fat-tail line is the nearest precedent.
6. **"Not located" below half readable.** Owner's call. I also recommend reporting whether the unreadable share changes with price, because a price-linked refusal rate would bias the rates computed from readable answers only.
7. **Non-monotone label versus pooling.** Owner's call. CV would pool adjacent violators and still report an estimate. Consider printing a pooled bracket beside the label.
8. **Total-only card. Recommend 5 or 6 totals spaced 2.5 times apart**, matching the per-hen ladder's ratios of 2.3 to 2.5 and spanning the plausible range. Alternatively, run the three totals as a pilot and add points around the switch. The literature supports four to six points spanning the expected quartiles.

## Coverage statement

**Opened and read to the end** (raw text via `pdftotext`): Charness, Gneezy & Imas 2013 (body and references; Table 3 skimmed); Charness et al. 2018 (body to Appendix 1, whose final equations were cut off; table values were not extracted); Bruner 2007 note (table values not extracted); Whitehead et al. 2025 (main text through the conclusions; tables and references not read). All four lane input files, `analysis.py`, and spec section 5 were read in full.

**Read in part ⚠️:**
- Carson & Hanemann chapter: §§6.1–6.3 only. The year 2005 is from memory; the PDF did not show it.
- Johnston et al. 2017: Recommendations 4, 14, 17 and 21 only.
- EPA BMD guidance: opening pages, §2.1.5 and Figure 2 only.
- Miller 2024: read through a fetch tool's summary, not the raw text.
- Kajackaite's name as fourth author of Charness et al. 2018 is from memory; the extracted text cut off after "Gneezy &".

**Abstract or search summary only ⚠️:** Andersen et al. 2006, Jacobson & Petrie 2009, Yu, Zhang & Zuo 2021, Haab & McConnell 1997, Kanninen 1993, Brown, Cai & DasGupta 2001, Wichmann & Hill 2001, Grüner 2017.

**Unreachable or not opened ⚠️:** Holt & Laury 2002 (HTTP 401; its figures come via Bruner); Hanemann & Kanninen working paper 798 (HTTP 403); Cooper 1993, Alberini 1995, Kanninen 1995, Cameron & Huppert 1989 and the Haab & McConnell 2002 textbook (not found open; Cameron & Huppert is described from memory). An & Ayala 1996 was opened but not used.
