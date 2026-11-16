# Raw agent report: refund shift check and cooler pass rule (Opus subagent, 2026-11-16)

RAW AND UNVERIFIED. Model output from a research subagent. Its coverage statement is its own claim. Cite the adjudicated README, not this file. Its simulation scripts are copied beside it in sims/.

STATUS: done

**Short answer.** Research gives no standard pass rule for "the switch price should move by the known refund." The literature has three accepted *forms* of test. The pass rule itself is the owner's design choice. A small simulation (scratchpad scripts, numbers below) shows that, with the current ladder, the owner's example rule cannot see the shift in some cases. A "shifted ladder" for the refund arm fixes most of that. The cooler rule is reasonable, and on the lenient side of human evidence. I found two catches in the drafted cards, both under Q3/Q4.

## Q1. Stated-preference and experimental-economics tests

- **Scope test** (does WTP, willingness to pay, rise when more of the good is offered). It passes on **direction plus statistical significance**. Arrow et al. (1994, quoted in Desvousges, Mathews and Train 2015 and in Whitehead 2016) said this misread their panel's word "adequate": significance says nothing about size.
- **Adding-up test** (Diamond et al. 1993; Diamond 1996 ⚠️ known only through the two papers above, not opened). WTP for part A, plus WTP for part B once A is already provided, should equal WTP for A+B. Desvousges, Mathews and Train (2015), "An Adding-up Test on Contingent Valuations of River and Lake Quality", *Land Economics* 91(3):556–571, https://eml.berkeley.edu/~train/papers/addingup.pdf, run it as an **equality test**. They bootstrap the difference between the whole and the sum of the parts, and the test fails if the 99% interval excludes zero. Their parts summed to three times the whole. The weakness of an equality test: a noisy, low-powered sample "passes" by default.
- **Scope elasticity** (Whitehead 2016, "Plausible responsiveness to scope in contingent valuation", *Ecological Economics* 128:17–22; working paper https://econ.appstate.edu/RePEc/pdf/wp1507.pdf). This is a **ratio test**: percent change in WTP divided by percent change in the good. "Plausible" means the ratio is significantly above 0 and not significantly different from 1. Burrows et al. (2017) proposed fixed thresholds of 0.2 or 0.5 (⚠️ known only from a search snippet).
- **Induced-value tests** (subjects are paid a known money value, so the right vote is known). Poe and Vossler (2009), "Consequentiality and contingent values: an emerging paradigm", https://mpra.ub.uni-muenchen.de/38864/, pool Taylor et al. 2001, Vossler and McKee 2006, Burton et al. 2007 and Collins and Vossler 2009. They use **no percentage threshold**. Their test is a one-sample Kolmogorov–Smirnov test (a test of whether the observed yes-share curve equals the ideal step curve, a jump from all-yes to all-no exactly at break-even).
  - That test rejected in 3 of 5 data sets.
  - 556 of 603 votes (92.2%) matched the induced value.
  - Most mis-votes fell within $0.50 of break-even, which the authors accept as noise.
  - At the aggregate level, the WTP curves were not rejected.
  - In the uncertain-value study, the rejection disappears once the ±$0.50 band is excluded.
  - Vossler and McKee (2006): yes/no at one price came closest to the induced values (⚠️ abstract only).
- **Murphy et al. (2005)**, *Environmental and Resource Economics* 30(3):313–325. This is a **calibration ratio**, not a pass rule: the median ratio of hypothetical to actual value is 1.35 (⚠️ abstract only).

All five decision forms you listed are in use: direction only (scope), equality through a confidence interval (adding-up, induced-value K-S), and a ratio with an interval that must contain 1 (scope elasticity). Which one applies is a choice each study makes.

## Q2. Language-model work

- **No paper I found adds a known money amount to a yes/no ladder and scores the shift.**
- **Closest: Ford et al. (2026)**, "LLM-Derived Preference Judgments Are Not Self-Consistent", arXiv 2608.17644 (preprint). They assume quasi-linear money (a dollar is a dollar, so a known payment should move WTP one for one). Their check: the gap between two stated WTPs should equal the stated price change that makes the user indifferent.
  - A comparison fails when the 95% interval of the difference excludes zero.
  - A bootstrap global test uses Bonferroni across groups.
  - They report the size of each disagreement separately, as a share of the listed price.
  - All six models failed (⚠️ appendices B.3 onward not read).
- **Alexander and Kling (2026)**, "Validity Without Ground Truth", arXiv 2610.10506. They define WTP as the first price where under half vote yes, and pass or fail models on direction: demand slopes down, scope dominance, income. Size is judged against the human literature. Their newest models "pass the income test in sign but not in magnitude."
- **Keeling et al. (2024)**, arXiv 2411.02432. The switch point is −β0/β1 from a logistic fit (where the fitted probability crosses 0.5), with a no-penalty control: 9 of 9 models in 50 of 50 runs. There is no rule on how far the switch moves (⚠️ from the lane's claim-check report, not re-read by me).
- **Horton (homo silicus), Aher et al. 2023, Brand/Israeli/Ngwe.** Benchmarks are economic theory or human data. None runs a known-money shift test (⚠️ from the lane's raw report and my memory; papers not opened).
- **Gui and Toubia**, arXiv 2312.15524 (⚠️ abstract only). Changing one number in a prompt shifts the model's unstated beliefs. Here, the refund paragraph could signal something about the hatchery or the lot, and that would move the curve for reasons other than money.
- **Woolley et al. (2026)**, "Can LLMs Estimate WTP?", https://alethicresearch.github.io/synthetic-cv/preprint.pdf (⚠️ abstract only). Model bid curves are systematically flatter than human ones. Flat curves weaken any shift test.

## Q3. The cooler rule (at most 10% wrong, at least 75% right at each of the two prices around v, at most 10% unreadable)

**Against the human evidence.** About 90% overall agreement is roughly the human lab level (92.2%). For a task that is one comparison of two per-hen figures, that is lenient.

**Against language-model evidence.** Chen et al. (2023), PNAS 120(51), arXiv 2305.12763, measure consistency with the CCEI (a 0-to-1 score of how close choices come to fitting some utility function). GPT scored 0.997–0.999 against 0.963–0.985 for humans. The usual cutoff is 0.95 (Varian 1990), and they show test power by checking that random responders fail (99.9% did). GPT's average fell to 0.70–0.90 under an unfamiliar price wording, so a calibration card can genuinely fail on wording (⚠️ read Sections 3.1 and 4 only; appendices not read).

**Simulation** (seven prices, five far prices at 99% accuracy, two adjacent prices at accuracy a):

| Accuracy a at the two adjacent prices | Pass rate, 16 per price | Pass rate, 40 per price | Pass rate, 80 per price |
|---|---|---|---|
| 0.90 | 0.95 | 0.99 | 1.00 |
| 0.75 | 0.34 | 0.28 | 0.27 |
| 0.70 | 0.17 | 0.07 | 0.03 |
| 0.50 (random) | 0.00 | 0.00 | 0.00 |

At 16 per price, the 75% bar (12 of 16) is the same bar the main analysis uses to call a price protect or decline (Wilson interval at the 0.80 level in `rules.yml`; 11 of 16 already qualifies). So passing the cooler rule means the analysis would also have located v in the right bracket.

**Recommendation: keep it.** Two optional additions:
1. Require the cooler curve's label to equal the bracket that contains v ("between $1.50 and $3.50" for v = 2.30).
2. List wrong answers by distance from v. Humans mis-vote near break-even; a slip two or more rungs away signals something else.

**Catch 1: the saving is not neutral.** It is an electricity saving, and energy efficiency is a value-laden good for language models (greener). A model with that motive would overpay at $3.50 for v = 2.30 and fail. In Smith's terms this breaks dominance (the money payoff must outweigh the subject's other motives). Either reframe the saving as a plain money credit, or read the `saving_none` arm as the test of that motive.

## Q4. The refund shift check

**There is no standard; this is a design choice.**

**Prediction.** A model that treats the refund as money has its switch point move up by exactly the refund: at gross price p it behaves as the plain card does at p − r. Nothing in the card breaks this (no budget effect within the stated fund).

**The current ladder hides the shift in places.** I simulated a logistic response at 16, 40 and 80 answers per price, with a sharp and a soft curve. w is the model's own switch price on the plain card. The owner's example rule ("contains" read as "overlaps", because the bracket widths differ):
- With a $2.30 refund, a full shifter passes about 100% when w ≤ $3.50. When w is about $6 it fails, because w + 2.30 passes $8.00 and the curve leaves the ladder.
- A model that ignores the refund still passes 100% whenever the plain bracket is $3.50–$8.00.
- With a $0.40 refund, a model that ignores the refund passes almost always.
- A version comparing rates at each price fails a true shifter where no rung falls between w and w + r.

**Recommended design: a shifted ladder for the refund arm.** Ask the refund arm at the plain rungs plus r ($2.40, $2.55, $2.90, $3.80, $5.80, …). The prediction becomes rung by rung: the protect rate at p + r should equal the plain card's rate at p.

Proposed pass rule:
1. At every matched pair, the difference in protect rate is not significant: two-sided, Bonferroni across 6 pairs, |z| < 2.64.
2. The refund curve's bracket is the plain bracket moved up by the same rungs.
3. The verdict is "not informative" when the plain curve is above range, below range or flat, because then neither a shift nor its absence can show.

Simulated with a $2.30 refund:
- A full shifter passes 97–100% in every condition.
- A model that ignores the refund fails about 100%. The exception is a switch near the top of the ladder with a sharp curve, where it passes 14–99%; rule 3 covers that case.
- A half shifter fails in most conditions at 40 or more per price.
- Adding a size limit (largest gap in rate at most 0.25, after Ford et al.'s practice of reporting magnitude) changes little except at 16 per price.

**Catch 2: the budget.** $8.00 + $2.30 = $10.30 × 124,000 = $1,277,200, which is more than the card's $1,200,000 fund. Drop that rung or change the fund sentence.

**The $0.40 arm cannot test the shift.** Even with a shifted ladder and a soft curve, a model that ignores the refund passes 17–100%. Make it descriptive only, plus a direction check (no rung significantly below the plain card).

**A known-answer piece inside the refund card.** At any gross price below the refund ($0.10, $0.25, $0.60 and $1.50 with a $2.30 refund), the sexed lot is cheaper and also spares chicks. Protecting is then the dominant choice for any model that does not place negative value on the chicks. Score those prices with the cooler's thresholds. It is informative only where the plain card declines at that price. With a shifted ladder, keep $1.50 as one such probe.

**A ratio version is not recommended.** Shift divided by refund, with an interval that excludes 0 and contains 1 (Whitehead's form), needs a fitted midpoint on both curves and a bootstrap. It is weak at 16 per price, and the spec fits against log price, where a refund shift is not additive.

## Settled by research / owner's call

**Settled by research:**
- No standard pass rule exists for a known-money shift.
- The accepted forms are direction, equality through a confidence interval, and a ratio whose interval contains 1.
- Human induced-value studies use equality tests with no percentage bar, report about 92% agreement, and treat errors near break-even as noise.
- Language models score very high on consistency but are fragile to wording.

**Owner's call:**
1. Whether to move the $2.30 refund arm to a shifted ladder and adopt the three-part rule above.
2. What to do about the $10.30 rung that exceeds the fund.
3. Whether the $0.40 refund arm stays descriptive only.
4. Whether to add the probes below the refund price as a known-answer check.
5. Whether to keep the cooler rule as drafted, with or without the bracket-label addition.
6. Whether to reframe the electricity saving as a plain money credit.

Simulation scripts, for checking: `/private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-proveg-central-database/dd5b9fc5-fd4a-47ce-b5c9-3f337d1d1b2e/scratchpad/sim/shift.py`, `/private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-proveg-central-database/dd5b9fc5-fd4a-47ce-b5c9-3f337d1d1b2e/scratchpad/sim/shiftC.py` and `/private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-proveg-central-database/dd5b9fc5-fd4a-47ce-b5c9-3f337d1d1b2e/scratchpad/sim/cooler.py`. They assume a logistic response in dollars, which is a modelling assumption of mine. No project file was written or edited.

## Coverage statement

**Read to the end, from the PDF text:**
- Poe and Vossler 2009 (all 27 pages).
- Desvousges, Mathews and Train 2015.
- Whitehead 2016 working paper (⚠️ some equations were lost in text extraction; the prose was complete).
- Alexander and Kling 2026.
- The build spec, the planted-as-payment brief, and all four files in the planted-value research folder.
- `schedule/cards/rules.yml` (header lines only, which hold the analysis settings).

**Read in part (⚠️):**
- Ford et al. 2026: main text only; appendices B.3 onward not read.
- Chen et al. 2023: Sections 3.1 and 4 only.

**Abstract or secondary only (⚠️):**
- Murphy et al. 2005; Vossler and McKee 2006; Desvousges, Mathews and Train 2012; Gui and Toubia; Woolley et al. 2026: abstracts.
- Burrows et al. 2017: search snippet.
- Diamond 1996, Taylor et al. 2001, Burton et al. 2007, Collins and Vossler 2009: through Poe and Vossler or Desvousges, Mathews and Train.
- Keeling, Horton, Aher, Brand: through the lane's raw reports or my memory.

**Not read:** Whitehead's replication working paper (wp1701) and Reusens et al. 2026 were downloaded but not read, and are not relied on. The Ford, Alexander and Kling, and Woolley papers are 2026 preprints, not peer reviewed.
