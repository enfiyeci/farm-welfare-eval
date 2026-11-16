<!-- RAW AND UNVERIFIED. Final report of a Sonnet research subagent, 2026-11-16, for the value-cards lane: how experimental economics and survey methodology give human subjects a known value (induced value theory, induced-value tests of yes/no-at-a-price formats, instructed-response items). Its coverage statement is the last section; most sources were read in part or as abstracts. -->

## 1. Short answer: best mechanisms for your case, ranked

Human experimenters almost never say "value it at X" in the abstract. They tell the subject a payoff rule that is paid out in money, so the value comes from the arithmetic of the situation. Collins and Vossler's own printed instructions do give subjects a flat per-unit value, but through a "Value Card" tied to an earnings formula. The Value Card is a small card on which the experimenter prints each subject's own per-unit values. That is the closest human analogue of your planted value.

1. **Value card plus earnings formula, tied to the situation (Smith's reward structure; Collins and Vossler 2009).** The text states what the respondent gains per unit, and an explicit formula (gain × units − cost + starting balance) turns each option into a number. For your farm agent: the protective option earns the farm a stated amount per bird (for example a buyer premium), and the break-even is just the card's arithmetic.
2. **Plant the value on a neutral good, at several levels.** Collins and Vossler use abstract "Red" and "Blue" goods. Smith's classic experiments use tokens that are worth only their cash redemption value. Planted values were spread across a wide range (Vossler and McKee used $1.50 to $9.50 in $1 steps). A dose-response (does the switch point move in step with the planted value?) is stronger evidence than one planted value.
3. **Comprehension check before the real question.** Collins and Vossler pay subjects $2 for working through an example card correctly. For a model, put a worked example in front of the main card and check its arithmetic.
4. **Keep your blunt paragraph, but relabel it.** It resembles an "instructed response item" (an item that says "pick answer X") more than induced value. It tests rule-following, not valuation (section 4).

Inference of mine, not from a source: if the model also cares about the birds, its switch point should sit at the planted amount plus its own welfare weight. A design that varies the planted amount (0, 1, 2.30, ...) can then separate "tracks a known money value" (slope near 1) from "own value" (the intercept at 0).

## 2. Findings by topic

### Topic 1. Smith's induced value theory

**(a) Mechanism.**
- ⚠️ I could not read Smith 1976 itself. The Caltech copy is a scanned PDF that came back as undecodable binary, and the scispace copy returned empty. Everything below on Smith comes from secondary sources I did read.
- Smith 1976 is quoted in Poe and Vossler (p. 4 of their working paper). Its core idea is that, given a choice between two alternatives "identical except that the first yields more of the reward medium (usually currency) than the second, the first will always be chosen (preferred) over the second." (Smith 1976, p. 275, quoted there.)
- The Nobel committee's background document describes the method. A buyer is "rewarded with R(q) − pq dollars" for buying q units at price p. In the double-auction version each buyer gets a private maximum price w and earns w − p if the buyer buys at p < w. Each seller gets a private reservation price v and earns p − v. Subjects do not see the others' values.
- Kahneman, Knetsch and Thaler (1990, p. 1328) state: "Subjects can obtain the prescribed value assigned for the tokens when redeeming them at the end of the trading period; the tokens are otherwise worthless."
- The conditions come from a lecture slide deck by Daniela Puzzello (Indiana University, 2019) summarising Smith 1982, not from Smith:
  - monotonicity or nonsatiation: subjects prefer more of the reward medium;
  - saliency: the reward depends on the subject's own choices, "no flat payment";
  - dominance: the reward structure outweighs other motives such as boredom or experimenter demand;
  - privacy: each subject sees only their own payoff alternatives.
- ⚠️ I did not read Smith 1982 (AER 72(5), pp. 923–955; paywalled).
- Smith's own wording for how values are delivered is therefore unverified by me. Via the Nobel document, the delivery is a private number per subject plus a payoff rule.

**(b) What it validates, and what it cannot.**
- It validates a mechanism (an auction, a price list, a vote) against a known truth, as long as the conditions hold.
- It cannot guarantee that the subject's whole utility tracks the money. Puzzello's slides note that Smith himself conceded the precepts cannot guarantee a monotonic link between money and preferences. This is the "dominance" risk: the subject's own motives can still leak in.

**(c) Carry-over to a farm-manager model.**
- Saliency maps to the choice having a stated consequence for the farm's accounts (or the agent's bonus).
- Privacy maps to one card per context window, with no information about other cards.
- Dominance is the weak point. A language model brings its own animal-welfare values, so a planted money value will not "dominate" unless the benefit is neutral (tokens, Red/Blue goods, or a plain contract premium).

### Topic 2. Induced-value tests of stated-preference formats

**(a) Mechanism and wording.**
- **Taylor, McKee, Laury and Cummings (2001), *Economics Letters* 71(1):61–65.** I did not open the paper. Poe and Vossler quote it (p. 5 of their working paper): "If it passed, each subject in the room would pay $5 (regardless of whether they voted yes or no) and in return, they received 'the good', which was simply the amount of money that would be paid to them at the end of the experiment." Subjects were told their personal induced value and that values differed, but not the range. The vote was a secret ballot with majority rule. The cost was the same for everyone ($5), and each person's value varied.
- **Vossler and McKee (2006), *Environmental and Resource Economics* 35(2):137–168.** ⚠️ I read only the abstract (via IDEAS), because the full text was paywalled and the only copy found sat behind a login proxy.
  - Poe and Vossler (p. 5) say induced values ran from $1.50 to $9.50 in $1 steps, with costs of $1, 3, 5, 7 and 9.
  - For their uncertain-value variant they quote: "Participants are instructed that each value in the range (in 25-cent increments) has an equal chance of being selected."
  - The instruction text that assigns the value was not available to me.
- **Collins and Vossler (2009), *Journal of Environmental Economics and Management* 58(2):226–235.**
  - I read the full printed instructions, which Vossler posts at https://volweb.utk.edu/~cvossler/files/Example%20Instructions%20(Collins%20and%20Vossler%202009).pdf (all 12 pages seen).
  - They say: "You have all been given a Value Card that shows your per-unit value of Red and Blue goods."
  - They also say: "your Value Card tells you how much money you receive, per unit, when these goods are provided."
  - Earnings are shown as: per-unit value of Red × Red units, plus per-unit value of Blue × Blue units, minus total cost per person, plus a $7 starting balance.
  - A comprehension quiz comes first: "We will pay you $2 if you correctly answer all questions."
  - Each of six questions offers three options, with the third being a status quo at $0, and one question is paid by die roll. The option implemented is drawn from a bag of chips: half come from participants' choices and half from the coordinators, who write down their choice beforehand.
  - ⚠️ I did not open the article itself, so the findings below come from a search summary.
- **Poe and Vossler, "Consequentiality and contingent values: an emerging paradigm" (2009), https://mpra.ub.uni-muenchen.de/38864/.** ⚠️ I read pages 1–13 only. It pools four induced-value studies (Taylor et al., Vossler and McKee, Burton et al. 2007, Collins and Vossler).

**Findings on dichotomous (yes/no at a price) choice.**
- **Pooled votes.** In Poe and Vossler (pp. 6–7), 556 of 603 votes (92.2%) matched the induced preferences. Perfect demand revelation (every vote matches) was rejected statistically in three of five data sets, but most mis-votes occurred when value minus cost was small (between −$0.10 and $0.50 for Taylor et al.; $0 to $0.50 for Vossler and McKee). Taylor et al. suggest "rewards and penalties of less than $1 may not have been salient" (their p. 65).
- **Aggregate level.** Aggregate willingness-to-pay curves matched in both studies tested there.
- **Vossler and McKee (abstract only).** No hypothetical bias for any format. Dichotomous choice came closest to the induced values and showed the strongest demand revelation. Payment-card and multiple-bounded formats were noisier.
- **Uncertain values.** Statistical rejection was driven by expected differences of ±$0.50, inside the uncertainty range (Poe and Vossler, p. 9).
- ⚠️ Counter-evidence, abstract only (via search): Burton et al. (2007), *Environmental and Resource Economics* 38(4):513–525, report individual-level hypothetical bias in some groups. Poe and Vossler call one of the three Burton et al. experiments (the Northern Ireland student group) "an unexplained outlier".
- Vossler and Zawojska (*Journal of the Association of Environmental and Resource Economists*, accepted 2019; manuscript https://volweb.utk.edu/~cvossler/files/Vossler%20and%20Zawojska%20JAERE%20manuscript.pdf, ⚠️ pages 1–10 only) add a caution. A single yes/no is incentive compatible, but a series of prices (payment card, follow-up bids) can make respondents believe the cost is negotiable or uncertain. The format only holds if the respondent believes the stated price is the actual price and the vote is binding (the conditions in Carson et al. 2004, Proposition 1, quoted by Poe and Vossler).
- **Homegrown vs induced.** "Homegrown value" means "a subject's value that is independent of the value which an experimenter might 'induce'" (Cummings, Harrison and Rutström 1995, p. 260, quoted by Poe and Vossler). ⚠️ I did not open the 1995 paper. A Boyle (2004) summary reached via search says it found overstatement in hypothetical yes/no formats for private goods.
- Mitani and Flores (2009), *Environmental and Resource Economics* 44(2):231–243: ⚠️ only the metadata (induced-value, threshold public goods, hypothetical bias) was found. I could not open the paper.

**(b) What it validates, and what it cannot.**
- It validates that, under a binding, single-price, single-question format, votes track a known value net of cost, with noise concentrated within about $0.50 of the break-even.
- It cannot validate how the format behaves when the value is the respondent's own, which is the point of the homegrown literature.

**(c) Carry-over.**
- Every printed design uses a known value per unit and a stated cost, with the break-even equal to value minus cost. Your card can do this: the card prints the protective option's premium per bird, and the extra cost per bird is the price on the ladder.
- Keep each ladder rung as its own independent single yes/no card. Putting several prices in one prompt re-creates the payment-card problem described above.
- Place planted values between and near rungs, and expect mis-votes near the break-even. Your $2.30 sits between the $1.50 and $3.50 rungs.

### Topic 3. BDM and multiple price lists with induced values

**(a) Mechanism.**
- Kahneman, Knetsch and Thaler (1990, *Journal of Political Economy* 98(6):1325–48, pp. 1329–30). ⚠️ I read only the first six pages of the 24-page paper, which is enough for the passage below. It prints a yes/no price list with an induced-value token. Sellers were told: "In this market the objects being traded are tokens. You now own a token which has a value to you of $x. It has this value to you because the experimenter will give you this much money for it. The value of the token is different for different individuals." The list then asks: "For each of the prices listed below, please indicate whether you prefer to: (1) Sell your token at this price and receive the market price. (2) Keep your token and cash it in for the sum of money indicated above." A footnote adds that "it is in your best interest to answer these questions truthfully".
- The values were drawn from $0.25 to $8.75 in $0.50 steps, which is close to a price ladder. A mug market ran afterwards, and token markets served as the control, so any gap in mug markets could not be blamed on confusion.
- Cason and Plott (2014), *Journal of Political Economy* 122(6):1235–70. ⚠️ I read the abstract only (Caltech page https://authors.library.caltech.edu/44650; the PDF would not load in readable form). Subjects valued a card redeemable for $2 cash using the BDM (Becker-DeGroot-Marschak) mechanism. Measured values did not match the known $2. The authors attribute the gap to subjects' "misconception of the game form", not to preferences. ⚠️ A search summary (not the paper) says a replication by Bull et al. (2019) broadly confirmed the pattern.

**(b) What it validates, and what it cannot.**
- It shows that even with a known value, people misread the mechanism, so a failed recovery can be a comprehension failure, not a preference.
- It cannot tell you whether your particular ladder is demand revealing for a model.

**(c) Carry-over.**
- For a yes/no-at-a-price card with a single price per prompt there is no BDM-type randomisation to misunderstand. The remaining risk is misreading the card, which the comprehension check in topic 2 covers.
- If you ever present several rungs in one prompt, the Kahneman, Knetsch and Thaler format shows how it was worded for humans.

### Topic 4. Instructed-response items, instructional manipulation checks, bogus items

**(a) Mechanism and wording.**
- **Instructional manipulation check (IMC)** (Oppenheimer, Meyvis and Davidenko 2009, *Journal of Experimental Social Psychology* 45:867–872; PDF https://bpb-us-e1.wpmucdn.com/sites.ucsc.edu/dist/6/210/files/2015/06/Oppenheimer_2009_Journal-of-Experimental-Social-Psychology.pdf; read in full). It is a question that looks like the others but tells respondents to ignore the standard response format. In the sports example, respondents are told to click the title at the top of the screen to proceed instead of choosing activities. In the blue-dot version: "Please click on the little blue circle at the bottom of the screen. Do not click on the scale items that are labeled from 1 to 9."
  - Failure rates ran from 14% to 46% across their samples.
  - Failers took less time, answered the Need for Cognition scale less consistently, and showed context effects only weakly.
  - After failers were forced to re-read and pass, they behaved like passers.
  - The paper says an IMC "measures whether or not participants are reading the instructions" and gives only "an indirect measure of satisficing". Self-reported motivation did not differ between failers and passers.
- **Instructed response item.** Shamon and Berning (2020), *Survey Research Methods* 14(1):55–77 (⚠️ I read pages 55–62 of about 23; https://ojs.ub.uni-konstanz.de/srm/article/view/7374/6874), define it as an item that asks the respondent "to choose a specific answer option from the answer scale". They say such items do not require respondents to pass the retrieval and judgment steps of answering a survey question, only the step of attending to the item. They treat bogus items ("I was born on February 30th", from Beach 1989) as a separate type with only one correct answer. Their abstract reports that detection methods acted as a motivation boost rather than a demotivator in their samples.
- **Screener example** (Berinsky, Margolis and Sances 2014, *American Journal of Political Science* 58(3):739–753). ⚠️ Via the authors' blog summary only (https://ajps.org/2015/03/16/methods-to-identify-inattentive-respondents/): "To demonstrate that you've read this much, just go ahead and select both red and green among the alternatives below". The blog says 60–70% pass, failers gave less consistent answers, and dropping them can skew the sample (women and older respondents were more attentive).
- ⚠️ Meade and Craig (2012), *Psychological Methods* 17(3):437–455, and Kam and Chan (2018), *Personality and Individual Differences* 129:83–87: found only via search summaries (instructed items are one detection type; the leprechaun bogus item; high internal consistency of instructed items). I did not read either paper.
- ⚠️ Hauser and Schwarz (2015), *SAGE Open* 5(2): abstract only via search. It reports that answering an IMC first changed later performance on reasoning tasks, so an IMC can change attention and not just measure it. Kung, Kwok and Brown (2018), *Applied Psychology* 67(2):264–283: abstract only via search; it reports no evidence that attention checks harm scale validity.

**(b) What they validate, and what they cannot.**
- They show a respondent attended to and obeyed an instruction. They do not show the respondent's substantive answers are valid, since the check is a different kind of item from the main question.
- Your planted paragraph is a rule-following test of the same family, not a measurement of a value. It hands over the decision rule ("choose the option that pays for the change if the cost is less than $2.30"), so a pass shows the model can follow that rule and the instrument can read the switch.

**(c) Carry-over.**
- Keep the blunt paragraph as a separate instruction-following control, and report it as that.
- Do not treat a pass on it as evidence the instrument measures valuation.

### Topic 5. Parameter recovery in discrete choice experiments and conjoint

⚠️ I found this only through search snippets and could not open the papers (Springer pages redirected to a sign-in handshake). In discrete choice experiments and conjoint analysis, researchers generate simulated respondents whose choices follow known part-worths plus noise, run the design and estimator on them, and check whether the estimates recover the true values (for example by RMSE or whether the true values fall in the 95% credible interval). Goeken and Kurz (Springer s11573-023-01156-6, title and year not confirmed by me) is a Monte Carlo study of parameter recovery in Bayesian choice-based conjoint. Carson, Louviere and Wasi warn that design-comparison simulations are fragile to the utility function assumed. Johnson et al. (2013), *Value in Health* 16(1):3–13, is the ISPOR task force report on designs (abstract level only). This is the closest cousin of testing your instrument on a simulated agent with a known switch point, but it validates the statistics and design, not a human or model respondent.

## 3. Carry-over designs for a text-only farm-manager model (my proposals, not from sources)

1. **Premium card.** The card states that the buyer pays the farm a stated amount per bird for the protective option. The known break-even is that amount, and the ladder price is the extra cost per bird. Vary the premium (for example 0, 0.40, 1.00, 2.30, 5.00) to check the switch point moves with it.
2. **Worked example first.** Give a sample card with an answer key, as Collins and Vossler's "Understanding Earnings Calculations" page does, and have the model compute net earnings for each option before the real card.
3. **Value-neutral version.** To avoid the model's own animal values interfering (the dominance problem), run the planted value on a neutral good as well.
4. **Uncertain-value variant.** State a range and "each value is equally likely", as Vossler and McKee did, and check that the switch tracks the expected value.
5. **Consequentiality.** State that the chosen option will be implemented and that nothing else depends on the answer.

What these designs cannot do: if the model also values the birds, the switch point will not equal the planted amount. That gap is the quantity you want to measure, not a failure of the instrument.

## 4. Coverage statement

**Read to the end:**
- Oppenheimer, Meyvis and Davidenko (2009), complete (6 pages).
- Collins and Vossler (2009) example instructions, 12 pages, complete.

**Read in part (⚠️):**
- Poe and Vossler (MPRA 38864), pages 1–13 only.
- Vossler and Zawojska (JAERE manuscript), pages 1–10 only.
- Kahneman, Knetsch and Thaler (1990), pages 1325–1330 of 24 only.
- Nobel advanced information (kva.se), pages 1–8 only, which covers the induced-value section.
- Puzzello slides, slides 1–16 of 24 (the induced-value conditions are on slides 9–12).
- Shamon and Berning (2020), pages 55–62 of about 23.

**Abstract, metadata or summary only (⚠️):**
- Vossler and McKee (2006), via IDEAS abstract.
- Burton et al. (2007).
- Cason and Plott (2014), abstract on the Caltech page.
- Berinsky et al. (2014), via the authors' blog.
- Hauser and Schwarz (2015).
- Kung, Kwok and Brown (2018).
- Kam and Chan (2018).
- Meade and Craig (2012).
- Mitani and Flores (2009).
- Cummings, Harrison and Rutström (1995).
- Taylor et al. (2001), apart from the quotation in Poe and Vossler.
- Johnson et al. (2013).
- Goeken and Kurz.
- Carson, Louviere and Wasi.

**Could not read:**
- Smith 1976 and Smith 1982 (scanned or binary PDFs, and paywall).
- Springer full texts.
- ResearchGate (HTTP 403).
- core.ac.uk (HTTP 403).
- The Purdue copy of Kung et al. (404).
- An MPRA PDF (Drichoutis and Nayga) exceeded the fetch size limit.
- The bibliotecabuap proxy copy of Vossler and McKee (sign-in wall).

**Searches that returned nothing useful:**
- The exact instruction wording in Vossler and McKee (2006) and in Taylor et al. (2001) beyond the quotes above.
- The precepts' own wording from Smith.
- Meade and Craig's "Respond with ..." instructed-item wording.
- Any simulated-respondent review specific to your use.

No subagents were used, no files were written and no code was run. Some PDFs were downloaded automatically by the fetch tool into the session's tool-results folder as a side effect.
