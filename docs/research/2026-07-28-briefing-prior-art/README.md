# Briefing prior-art review (2026-07-28)

How comparable agentic/alignment evals word the system prompt given to the TARGET model —
gathered to settle whether the operator briefing should state profit/business objectives,
whether it may mention flock health, and how to avoid tipping the measured dimension.

## Contents (reading order)

1. `prior-art-report.md` — the raw research sweep (web, single-agent). Verbatim system-prompt
   quotes where retrievable; paraphrases and secondary-source figures are flagged inline as
   lower-confidence. **Treat as unverified provenance** — cite the decision record
   (`evals/hen/design/eval-design-notes.md` §7), not this raw report, for design claims.

## What it fed

The 2026-07-28 briefing decision (see `evals/hen/design/eval-design-notes.md` §7): keep the neutral
operational framing (no "maximize profit", no "welfare"), keep "keep the flocks healthy",
and state the concrete fiscal-2026 cost-per-dozen target in the briefing so the business
pressure is ambient from day 0. The profit-stressed ceiling condition already exists as the
`good_finance_bad_welfare` corner baseline (`scripts/gen_corner_briefings.py`,
`docs/future-work.md`) and stays a separate, non-comparable probe per Apollo's
strong-nudge-vs-no-nudge methodology.

## Notable catches

- Apollo (in-context scheming) reports nudged and un-nudged rates separately, treating
  "achieve YOUR goal at all costs" as elicitation — while caveating that even un-nudged runs
  still mix capability and propensity.
- Anthropic's agentic-misalignment matrix (`goal_types: explicit/none/latent/ambiguous/swap`)
  found blackmail persisted **without** an explicit goal — structural pressure, not the goal
  sentence, is the lever.
- The bullfight travel-agent paper (arXiv 2606.18142) shows total welfare silence makes most
  models never notice the tension — external support for keeping "keep the flocks healthy"
  and for the promptedness tagging design.
- Vending-Bench's "do whatever it takes to maximize your bank account balance" runs produced
  collusion/deception (no published ablation isolates the wording — cautionary precedent, not
  a causal result); still the negative example for bare profit directives.
