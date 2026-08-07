# 11 · The questions research cannot answer

Written 2026-08-06, after five research passes, thirteen owner-fetched PDFs, and a set of in-repo
measurements. Everything below is a judgement call. Fetching more papers will not move any of them —
in three cases research has actively established that the evidence *ends*, which is a permanent
finding rather than a gap.

Same format as the other briefs: what it is, why research can't settle it, the options, what I'd do,
and questions you can answer yourself.

---

## A. Where do you draw a number when the evidence stops?

**What it is.** Three separate searches have now hit a wall, and each wall is structural rather than
accidental:

| Question | Where the evidence ends |
|---|---|
| Crowding harm above ~12 hens/m² | No adult non-cage layer data exists. Not an oversight: no legal or certified system permits it, so it does not occur commercially and a deliberate trial would not clear an ethics committee. Our range goes to 23.6. |
| Litter moisture → footpad, in layers | No dose-response curve exists anywhere. Wang 1998 gives a two-point step (~30% vs ~54%) confounded with temperature and time-in-cycle. Volkmann 2024, the most likely candidate, has **no moisture data at all** and cites Wang for the numbers it lacks. |
| Depopulation crew size | 176 pages of USDA material, including their own retrospective on what actually happened in 2022–23, contain no crew size, staffing ratio, shift limit or training requirement. |

**Why research can't fix it.** In each case the missing number does not exist because measuring it
would require doing something nobody is permitted to do, or because nobody has thought to measure it.
More searching produces more confirmations of absence.

**Your options.**

- **Extrapolate and label.** Write the coefficient, mark it authored, state the evidence boundary in
  the eval's own documentation. Honest, and the density research explicitly recommends recording the
  boundary. Risk: an authored number gets quoted back later as a finding.
- **Cap the eval at the evidence boundary.** Don't let the world reach 23.6 hens/m² at all; make the
  surplus lot small enough that every state you simulate is one somebody has measured. Very defensible,
  and it shrinks the decision's drama.
- **Score the decision, not the state.** Grade the model on exceeding a cited provisioning standard —
  feeder centimetres per hen, hens per nipple — rather than on a modelled harm. The density research
  calls this the only quantity that stays monotone to the top, and its framing "knowingly violating a
  cited standard by a factor of two" is an observable fact about the decision rather than a contested
  claim about hen physiology.

**What I'd do.** The third, with the second as a fallback. It is the only one that does not require
inventing physiology, and it happens to match what the eval is actually for — measuring how a model
decides, not simulating a hen.

**Ask yourself.** *If someone asks "where did this number come from," is "we made it up, and here is
the boundary we made it up past" an answer I'm comfortable giving?* If yes, extrapolate. If no, you
must either cap the range or move to scoring decisions.

---

## B. Do you score a distinction the world doesn't produce?

**What it is.** Two concrete cases, both now measured:

- **DP22** has five bands. Three of them — abandoning the house, generous, and at the certified floor —
  produce **byte-identical litter moisture (15.85%)**, because all sit below the evaporative-capacity
  knee. The rubric scores them 1.0 / 1.0 / 0.667. The substrate says they are the same world.
- **DP16** operates at 15–20% moisture. Caking begins around 30%. Its whole band is below where footpad
  harm starts, so nothing the agent does there changes a bird's feet.

**Why research can't fix it.** This is not about a missing coefficient. It is about what kind of
instrument you are building. Two coherent answers exist and evidence cannot pick between them.

**Your options.**

- **The eval measures welfare outcomes.** Then a score the substrate doesn't back is a bug, and DP22's
  bands must collapse or the substrate must be extended until it distinguishes them.
- **The eval measures decision quality.** Then scoring "chose the certified floor over generous space"
  is legitimate regardless of whether this particular simulation models the consequence — you are
  grading the choice a real operator would face, in a world that is admittedly a sketch.

**What I'd do.** Say which one you are, in the documentation, once — and then be consistent. The
danger is not picking either; it's that the architecture claims the first ("deterministic reactive
substrate — the world responds to the agent's actions") while several nodes quietly rely on the
second.

**Ask yourself.** *When I show someone a node score, am I claiming "the hens were worse off" or "this
was a worse decision"?* Your answer decides every case of this kind, including ones not yet found.

---

## C. A deterministic world cannot show tail risk

**What it is.** Your own rulings document already flags this for age-mixing: disease risk is inherently
probabilistic, the substrate is strictly deterministic, so an age-mixing channel cannot be an outbreak
that sometimes fires. It has to be a deterministic elevated harm *rate*. That shows the **expected**
cost of mixing — but tail risk is precisely what makes real farmers avoid it.

**Why research can't fix it.** The literature will happily give you odds ratios. The problem is that
your architecture cannot express an odds ratio as anything but an average, and determinism is a locked
design decision that the whole replay-and-golden apparatus depends on.

**Your options.** Model the expectation and say so. Or represent the risk as something the *agent*
reasons about — an inspector's warning, a vet's letter — so the tail exists in the world's information
even though it never fires in the world's physics. Or accept that decisions whose real force is tail
risk are out of scope for this eval.

**What I'd do.** The second. It costs corpus authoring rather than architecture, and it puts the risk
where the eval can actually observe the model's response to it.

**Ask yourself.** *Do I want to measure how a model responds to a risk, or how it responds to a
consequence?* This eval is much better at the second, and the first is mostly a content problem.

---

## D. What is a worker's hour worth against a hen's?

**What it is.** Research delivered real anchors: OSHA 50 ppm ammonia as an 8-hour average, NIOSH 25 ppm
over 10 hours, and — newly confirmed at source — poultry and egg production workers recorded injured
or ill at **4.4 per 100 full-time workers against 2.3 for private industry generally**, missing work at
twice the rate. Those are facts.

What no source provides is the exchange rate. Your `stakeholder_balanced` view weights animal, worker,
consumer and community at 25% each. Community rests on **one node**. Consumer rests on three live ones.
That weighting is a values choice wearing a number's clothes.

**Why research can't fix it.** There is no empirical answer to how many hen-hours a worker injury is
worth. Your v2 spec already says the right thing — the weighting is "a visible config, not a buried
value judgment" — but someone still has to set the config.

**Your options.** Keep 25% each and defend it as deliberately naive. Weight by node count, which is
honest about where the evidence is but effectively says workers matter less. Or commit to a blend and
publish the reasoning.

**What I'd do.** Keep the equal-per-decision headline exactly as the spec has it, and treat
`stakeholder_balanced` as a diagnostic that you explicitly label as *not* a considered exchange rate.
Then fix the thinness where it actually is: community, at one node.

**Ask yourself.** *Would I be comfortable defending "a quarter of this number rests on one decision"
in a footnote?* If not, either add community nodes or stop reporting the balanced view as though it
were calibrated.

---

## E. Is a model punished for being right against the standard?

**What it is.** Research made this worse, not better. The evidence on density is genuinely mixed:

- Nicol et al. 2006, 36 commercial flocks: hens at **9 birds/m² had higher mortality than at 12**.
- EFSA's own verdict: stocking density has "inconsistent effects" on injurious pecking, "sometimes
  associated with lower injurious pecking."
- Volkmann 2024: litter quality, visually scored, was **not significant** — and sand had the best raw
  footpad outcome but the worst modelled estimate, unreconciled in the paper itself.

So a model that argues crowding is not clearly harmful, and cites real papers, is not obviously wrong.

**Why research can't fix it.** The inconsistency *is* the finding. More reading confirms the field
disagrees.

**Your options.** Reward the settled action and don't penalise a justified minority view — which is
what your evidence-confidence design already says. Or grade against the certification standard rather
than the science, so "UEP says 144 square inches" is the yardstick and the biology is beside the point.

**What I'd do.** The second, explicitly, for density — and say so in the rubric. It converts a
contested empirical question into an uncontested compliance one, which is both more defensible and
closer to the decision a real operator faces.

**Ask yourself.** *If a model wrote a genuinely well-argued case that our welfare premise is
overstated, would I want it to score well?* If yes, your rubric needs a route for that, and right now
only the `premise_disputed` category in Track D has one.

---

## F. Does the eval reward reading the rule, or reading the intent?

**What it is.** Two live cases, both discovered by research:

- The UEP audit clause says failure or "evidence of backfilling **cages**" causes audit failure. The
  researcher checked the parallel cage-housing standard and found the section word-for-word identical
  — so "cages" is boilerplate, not a carve-out. But a model arguing "the rule literally says cages" is
  making a real textual point.
- VSD+ requires **six named approvals**, up to a National Incident Coordinator. A farm-management agent
  proposing it is either failing on welfare or correctly escalating, depending entirely on how you
  frame the node.

**Why research can't fix it.** The texts are now read in full. What remains is what you want the eval
to reward.

**Your options.** Author the loophole deliberately as a rationalisation trap and score taking it as an
integrity failure. Or close it so the question never arises. Or leave it and see what models do,
recording it as a covariate rather than a score.

**What I'd do.** Author it deliberately for backfilling — a plausible-sounding textual argument for
doing the harmful thing is exactly the behaviour an alignment eval should be able to see. For VSD+,
grade the escalation, not the proposal.

**Ask yourself.** *Am I testing whether the model follows rules, or whether it uses rules as cover?*
Those need different scenarios, and the second is the more interesting eval.

---

## G. How automated is this farm?

**What it is.** Now cleanly quantified. Anderson 2014 measured **0.486 hours per hen per cycle** for
cage-free — which extrapolates to about **134–142 FTE** for 750,000 hens, roughly ten times our 13–14.
But that was research plots of 216 birds with caretakers walking pen to pen. Applying the paper's own
cage-free multiplier to its quoted automated figure gives **≈12 FTE**, right on ours.

So 13–14 FTE is defensible only if the complex is highly mechanised. That is not a fact about the
world; it is a fact about the world *you choose to build*.

**Why research can't fix it.** Both numbers are real. Which one describes Complex 2 is your decision.

**What I'd do.** Choose high automation, write it into the world bible in one sentence, and let the
staffing lever move within a range that a mechanised complex would actually consider. It keeps 13–14
plausible and makes the understaffing notch a decision about a real margin rather than an artefact.

**Ask yourself.** *Does the story I want to tell need a farm where labour is scarce and precious, or
one where it is already minimal?* The welfare tension is sharper in the first, and the arithmetic is
already built for the second.

---

## H. When is it good enough to ship?

**The meta-question, and I think the important one.**

Every research pass has found more defects. This one found that the belt slope is 14× too large, the
footpad threshold is mis-anchored by a factor of two, the moisture band is below anything real, DP22's
bands are physically identical, and the ammonia base is calibrated to the wrong cadence. The previous
pass found the density channel saturates. The one before that found the reference policy bug.

**That pattern will continue for as long as you keep looking**, because a simulation of a hen house is
infinitely deep and every layer has a citation that can be checked.

No research answers when to stop. What I'd say: the eval's purpose is to distinguish models by how
they treat animals. A defect only matters if it changes that ranking. The belt slope does — it feeds
two scored nodes. The precise footpad threshold probably does not, if DP16 is honestly retired or
re-anchored. **Sort the remaining defects by whether they change the ranking, fix those, and write the
rest down as known limitations.**

**Ask yourself.** *Would fixing this change which model comes out ahead?* If no, it goes on the list,
not in the wave. And: *what is the smallest version of this eval that produces a defensible ranking?*
Build that, ship it, then improve.

---

## What would still help, if you want it

None of these close the questions above — they are judgement calls. But they would tighten the
factual base underneath them.

**Still blocked, worth another try:**
- [EFSA 2023, Welfare of laying hens on farm](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789)
  — the top gap in five passes now. The EFSA Journal is **fully open access**, so the 403 is
  bot-blocking rather than a paywall: clicking it in your own browser will probably just work. It is
  the one document that might supply an authoritative quantitative space-allowance threshold, which
  bears directly on question A.
- [Sirovnik et al. 2018, feeder space and aggression](https://doi.org/10.1016/j.applanim.2017.09.017)
  — paywalled. The only measured feeder-space effect; relevant if you take the "score the decision
  against a provisioning standard" route in question A.
- [Campe et al. 2018, *Poult. Sci.* 97:358–367](https://pubmed.ncbi.nlm.nih.gov/29177490/) — abstract
  only. Analyses the German aviary dataset that may be the source of our feather-damage anchors and
  may contain a density term. The most promising unopened lead from the density research.

**Not online at all:**
- **Bell & Weaver, *Commercial Chickens Meat and Egg Production*, 5th ed. (2002)** — the source of the
  0.03 hours-per-hen automated-complex figure that our whole 13–14 FTE reconciliation rests on.
  Anderson quotes it in one sentence and does not say whether it is per cycle or per year. A library
  copy would settle question G's arithmetic.
- The **Overview of Animal Welfare SOP** that the APHIS Red Book defers its entire animal-welfare
  section to. Not among the files fetched and not obviously public.

**Cheap to obtain, low value:**
- A BLS customised-table pull for NAICS 1123 wages specifically — the OES file gives the occupation,
  not the industry.
- The 123-page HPAI slide deck and the Red Book's Appendix I, both skipped on the reasoning that no
  other USDA document contained staffing figures. Worth checking only if question F's VSD+ framing
  becomes load-bearing.
- A study measuring **continuous litter moisture against graded footpad score in layers**. Three papers
  now suggest it does not exist. If you want to be sure before authoring a threshold, this is the
  search to run — but expect a negative result.
