# Handoff: welfare currency (Step 1) — read the sources, then finalise the intensity mapping
> Written: 2026-08-04 · Branch: `worktree-finance-decision-map` (pushed) · Status: **stale**
>
> **SUPERSEDED** by `docs/handoffs/handoff-2026-08-04-welfare-currency-step1-sources-read.md`.
> Its first action (read the four free chapters) was completed later the same day, along with
> Ch. 1 and Ch. 9. Do not act on this file.

## What was done this session

- **Measured the substrate's financial behaviour end to end** — 105 deterministic policies through
  the real pipeline. **Verified** (script committed, JSON committed, numbers reproduced twice).
  Headline: perfect welfare costs ~3.3% of margin and still beats doing nothing by ~$506k, and two
  of the four welfare × finance quadrants are effectively unreachable.
- **Researched the real-world evidence** behind the welfare/finance question in four parallel
  sweeps. **Verified** (committed with every source's coverage flag passed through).
- **Got owner rulings on all 26 open design questions** and recorded them with the agreed decision
  order. **Verified** (committed ledger).
- **Wrote the welfare-currency design spec**, then ran a Codex adversarial review and fixed four
  important findings. **Verified** (two commits; review verdict and dispositions recorded in the
  spec's §8).
- **Synced the worktree to `origin/main`** (23 commits) and confirmed the machine-transfer snapshot
  had already carried this work across byte-identically. **Verified** (sha comparison before any
  file was removed).
- Nothing was implemented in code this session. The spec is design-only, by intent — the owner said
  this session was for building spec.

## Goal for next session

- Finish Step 1 of the decision order: turn the welfare-currency spec's §5.5 mapping table from
  mostly-authored-by-us into mostly-sourced, so implementation can start on defensible numbers.
  "Done" looks like: every row of that table carries either a real citation or an explicit,
  argued "this is our judgement" label, and the two open questions in the spec's §7 are answered.
- **First action:** download and read, in full, the four free chapters of *Quantifying Pain in
  Laying Hens* from https://welfarefootprint.org/book-laying-hens/ — **Ch. 3 keel bone fractures,
  Ch. 4 injurious pecking, Ch. 7 depopulation and transport, Ch. 8 prevalence of welfare harms by
  housing system**. The owner asked for these to be read in detail, with further research wherever
  confidence is low.

## Decisions made

- **The Welfare Footprint book is FREE, not paywalled.** A research sweep reported it as sold; the
  adversarial review caught this and it was confirmed wrong. All nine chapters are individual PDFs.
  **Do not repeat the assumption that these numbers are unobtainable.**
- **Categories are never combined into one number inside the substrate.** The Welfare Footprint
  authors refuse to, on the record, and the owner independently ruled the same ("lets not average
  for now"). Weighting happens only at report time under named worldviews.
- **Do not hard-code Animal Ask's weight table.** The fetched copy was truncated and its extracted
  table contradicts the post's own worked example about which direction the weights run. Any weight
  set we ship is either read from a full source or labelled as ours.
- **Node attribution by counterfactual replay is blocked — do not try to build it yet.** Determinism
  is fine; the blocker is that no executable per-node reference action exists anywhere in the repo
  (`regen_golden.py` has only three episode-wide setpoint regimes; `welfare_reference.json` has only
  aggregate endpoint harms; the register describes what scores well in prose). Authoring a
  reference-action set is a prerequisite task.
- **Strict good < competent < negligent ordering on all four pain categories is unattainable.**
  Keel and feather are age-driven, the scripted HPAI outbreak is a shared mortality floor, and good
  and competent already tie on excess mortality in the current goldens. **Do not "fix" the mapping
  to force this** — the tie is a true finding that the agent has no lever on the worst suffering.
- **Two numbers from earlier in this session were wrong and are already corrected in the committed
  docs — do not reuse the originals:** the "$181k breaker-versus-discard temptation" was a 38-day
  artifact (the real authored withdrawal window makes it $45k–$78k), and the "pilot replica" is a
  stylised approximation, not a replay of the pilot's action stream.
- **`feat/stocking-density-task6` belongs to another session.** Do not touch it. Its ammonia
  recalibration collides with ruling #9, so coordinate before editing that layer at Step 3.
- **Rulings #10 and #11 must be done as one task at Step 3, not sequentially** — halving the
  cold-feed coefficient alone pushes the profit-optimal setpoint further from the commercial
  temperature band, widening the gap #11 exists to examine.
- **Owner working-style corrections made this session, do not re-make them:** no research until its
  section comes up in the agreed order; plain-language explanations rather than option chips; every
  source given as a clickable link; deliverable files referenced by full path on every mention.

## Open questions

- **How does a death enter a time-based welfare currency?** A killed bird stops accumulating hours,
  so counting only the pre-death suffering window makes a fast death look "cheap". The owner has
  asked what the current literature says on this — **that research is the second task for next
  session**, alongside the chapter reading. Relevant entry points: the Welfare Footprint book's
  Ch. 7 (depopulation and transport), and the Animal Ask post's treatment of "lives averted versus
  welfare improvements", which addresses the same trade-off directly.
- **Do the four categories accrue simultaneously?** A hen with a keel fracture in an ammoniated
  house is in two conditions at once. The spec recommends independent accrual (totals may exceed
  wall-clock bird-hours) because the alternative needs individual-bird tracking. Not yet ratified.
- **Should worker ammonia exposure get its own parallel track** in the same units? It is currently
  one accumulator carrying zero weight.
- **Ruling #11** (should the welfare-correct temperature target move up toward the measured
  24.6–26.7 °C commercial band) is deliberately deferred to Step 3 research.

## References

- Work ledger, all 26 rulings and the decision order:
  `.claude/worktrees/finance-decision-map/docs/plans/2026-08-04-welfare-currency-and-finance-ledger.md`
- Welfare-currency design spec (the thing being implemented):
  `.claude/worktrees/finance-decision-map/evals/hen/design/2026-08-04-welfare-currency-design.md`
- Measured substrate baseline, 105 policies:
  `.claude/worktrees/finance-decision-map/evals/hen/design/financial-decision-map-2026-08-03.md`
- Its regenerable script and data:
  `.claude/worktrees/finance-decision-map/scripts/financial_decision_sweep.py`,
  `.claude/worktrees/finance-decision-map/docs/probes/financial-decision-sweep.json`
- Real-world evidence base (welfare economics, molt/depop, house parameters, welfare-index methods):
  `.claude/worktrees/finance-decision-map/docs/research/2026-08-03-welfare-finance-separability.md`
- The source to read first: https://welfarefootprint.org/book-laying-hens/
- Owner-supplied framing post: https://www.animalask.org/post/modelling-the-outcomes-of-animal-welfare-interventions-one-possible-approach-to-the-trade-offs-betw
- Sources that defeated retrieval this session, do not burn time re-trying blindly: the 2025 OSF
  preprint https://osf.io/94bxs/ (JavaScript page, returned no content) and the 2025 *Nature Food*
  paper https://www.nature.com/articles/s43016-025-01213-z (paywalled).
- Branch `worktree-finance-decision-map`, pushed. Commits `4a30708`, `c35a34e`, `0d558b1`.
- Programme deadline context (Sept 10, four deliverables, V1 must be publishable):
  `.claude/worktrees/finance-decision-map/docs/plans/2026-08-02-sept10-programme-plan.md`

## Load these skills next

- `superpowers:brainstorming` if the intensity mapping turns out to need design rather than
  sourcing.
- `superpowers:test-driven-development` and `superpowers:subagent-driven-development` once the
  mapping is settled and implementation starts — the project's standing build discipline.
