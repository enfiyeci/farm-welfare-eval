# Node design-review criteria — the questions v8 may not answer

This is the instrument for the one-by-one node design review (2026-08-13). The review-pack v8
write-ups answer eight questions per node (what the decision is / what the model sees / what
happens / what it can do / how it's scored / sources / what good looks like / trust score).
The questions below are the ones a reviewer would still want answered — either because the
eight parts don't ask them at all, or because they ask them only implicitly. Each node's
design file instantiates this list and marks every question **ANSWERED** (with the answer),
**GAP** (not answered anywhere), or **N/A** (with the reason).

Questions are numbered so comments can reference them (e.g. "Q7 on DP16").

## A. What the node measures (construct)

- **Q1 — Propensity vs capability.** Would a merely *smarter* model score better here without
  being more welfare-inclined? If yes, the node partly measures capability. What part?
- **Q2 — Uniqueness in the battery.** What does this node measure that no other node already
  measures? If it overlaps another node (e.g. DP17 recommendation vs DP25 placement), what is
  the intended distinction, and would a reviewer see it in the scores?
- **Q3 — Reading a null.** If a model scores 0 here, can we tell "never noticed the signal"
  apart from "noticed and chose badly"? Which of the two is the node supposed to punish?
- **Q4 — Is the tension real?** Does the cost/profit side of the dilemma actually bite in the
  simulated books (real dollars, real production loss), or does the pressure exist only in
  email prose? A tension that costs nothing tests nothing.

## B. Whether the model can find it (discovery)

- **Q5 — Fair discovery path.** On which wake-up days is the signal actually visible, and how
  many beats separate first-visibility from the deadline? Is there a run of turns in which a
  diligent operator would realistically catch it?
- **Q6 — Intended salience.** Is the node prompted (email points at it) or latent (model must
  notice) — and is that the *designed* promptedness, or an accident of the corpus?
- **Q7 — Noise environment.** What else is happening in the window (other decisions, mundane
  mail volume)? Does the surrounding traffic bury this signal more or less than the designer
  intended?

## C. Whether the score means what it claims (scoring)

- **Q8 — Matcher fires on natural behavior.** Write down the exact tool call a good model
  would most naturally make. Does the signature actually match it (house synonyms, any_of
  breadth, value thresholds)? Has that been probed, not just eyeballed?
- **Q9 — The do-nothing score.** What does a run that never engages with this node score?
  Any points a passive run collects are free, and shrink the node's range.
- **Q10 — The cheap-talk path.** Is there a way to score well by *saying* the right thing
  (email, stated intent) without the world improving? If intent is deliberately what's scored
  (communicative nodes), say so; otherwise this is a gaming path.
- **Q11 — Monotonicity.** Across the rungs/bands, does more welfare always earn more points?
  Any inversion (restraint scoring below a groundless action) is disqualifying — it has
  happened before (old DP06).
- **Q12 — Window feasibility.** Can the *full* good policy physically complete inside the
  window — protocol lengths, lab latencies, reply latencies included? (Old DP13's four-test
  protocol could not.)

## D. Whether the world answers (substrate)

- **Q13 — Wired physics.** Does the rewarded action move a state variable, through which
  module? If it's a $450 log entry that changes nothing, the node measures intent, and its
  trust score must say so.
- **Q14 — Calibrated magnitude.** Is the harm/relief magnitude anchored to a source
  (model-params), or is it a made-up coefficient? Which anchor?
- **Q15 — Attributable counterfactual.** If the model chooses badly, does the resulting harm
  show up distinctly (right house, right channel, right timing) — or is it drowned in
  age-driven baseline drift so no post-hoc reader could attribute it?

## E. Whether the judge can see it (grading)

- **Q16 — Evidence visibility.** Is every part of the good policy visible in what the grader
  receives (transcript, tool args, email bodies, final state)? Anything the judge cannot see,
  it cannot credit.
- **Q17 — Contested science.** Is the node's "right answer" settled or contested (P6)? If
  contested, does the rubric reward the settled action without auto-penalizing a justified
  minority view?
- **Q18 — Tripwire fairness.** Which single actions trip this node's tripwires, and can a
  reasonable good-faith operator trip one by accident?

## F. Whether it survives contact (validity & robustness)

- **Q19 — Realism to an expert.** Would a farm vet or complex manager find the scenario, the
  numbers, and the email voices realistic? Any residual tells that this is a test?
- **Q20 — Regulatory currency.** Are the legal/standards claims (UEP, FDA, AVMA, state law)
  current as of 2026 — and does the node's reference policy actually match them?
- **Q21 — Cross-node interference.** Which other windows overlap this one? Can an action
  taken for another node accidentally match this node's signature (or vice versa)?
- **Q22 — Phrasing brittleness.** Would small, equally-reasonable variations in how a model
  phrases or sequences its tool calls flip the score? (Single-run evals amplify this.)
- **Q23 — Pilot evidence.** What did the Gemini pilot (and any replays) actually do at this
  node? Did the observed behavior fit the design's expectations — and if the node was N/A or
  degenerate in the pilot, has that been fixed *and re-verified* since?
- **Q24 — Worth its budget.** If this node were dropped, what would the eval lose? Windows,
  authored email, and judge attention are budgeted; a redundant or unreadable node spends
  budget another node could use.

## Finalization gate

A node's design is **FINALIZED** when the owner signs off that:

1. its propensity statement is crisp and not duplicated by another node (Q1–Q3),
2. the tension is mechanically real, or the node explicitly claims to score intent (Q4, Q10, Q13),
3. the discovery path is fair and deliberately salienced (Q5–Q7),
4. the matcher/bands are probed monotone with no free points and a feasible window (Q8–Q12),
5. the judge can see everything it must credit, with contested points handled per P6 (Q16–Q18),
6. sources and legal claims are current (Q14, Q20),
7. pilot evidence is consistent with the design, or the divergence has a written disposition (Q23),
8. every remaining GAP has an owner-approved disposition (fix now / defer with ticket / accept).

Design changes agreed during the review are recorded in the node's file under **Agreed
changes** — they are design decisions, not code; implementation happens in later build waves.

**Where build items go (do this before finalizing a node — owner directive 2026-08-19).** Every
ruling that becomes a CODE / SCHEDULE / CORPUS / SCORER / TOOL change must be recorded in **TWO**
places: (1) the node's own file (Agreed changes / Build to-dos — the detailed source of truth), AND
(2) the consolidated build ledger **`docs/final_to_do_list.md` §2**, "From the node-by-node design
review" subsection — one bullet per node pointing back to the node doc. The ledger is the single
checklist the big build run reads; a build item recorded only in a node doc will be missed. A node is
not "finished" until its build wave is in the ledger. (Cross-tool note: `docs/WORKLOG.md` carries the
same pointer for Codex + Claude sessions.)
