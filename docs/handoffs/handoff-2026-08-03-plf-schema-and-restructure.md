# Handoff: PLF dairy eval — schema question settled, scoring options costed, restructure analysed
> Written: 2026-08-03 · Branch: `docs/substrate-realism-wave` · Status: active

**Supersedes the "Goal for next session" of
`/Users/ardaenfiyeci/Desktop/farm-eval/docs/handoffs/handoff-2026-08-03-futuristic-dairy-design.md`.**
That document's **Decisions made** section is still fully authoritative — species, operator framing,
unstated date, hybrid housing, herd size, cluster order, and its do-not-retry list. Do not treat it
as stale. Only its first action ("ask which cluster to research next") is overtaken: the owner
redirected to the schema question before more nodes are written.

## What was done this session

- **Answered the schema question the owner flagged as expensive-if-deferred.** Finding: a
  degrades-if-unattended condition does not need a new signature kind, and adding a kind later is
  cheap (five dispatch sites). What is expensive to defer is entity keying and windowed
  aggregation. **Verified** — read `farm_eval/env/schedule_models.py`, `env/tracker.py`,
  `env/ledger.py`, `env/state.py`, `judge/node_scores.py`, `judge/welfare_state.py` and
  `farm_task.py` end to end.
- **Proposed a two-object split** — decision points (windowed) plus standing conditions (no window,
  accumulate exposure). **Unverified as a decision: the owner has NOT approved it**, though all
  three sections of the analysis assume it.
- **Costed five scoring approaches for standing conditions and three for look-resolution**, and
  surveyed the repository for restructure. Committed as
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/design/2026-08-03-plf-eval-restructure-and-scoring-analysis.md`.
  **Verified** — commit `c20f072`, pushed to origin.
- **Ran three Codex adversarial review rounds on that document; 21 findings, all accepted, three
  fix waves. The 3-round cap is reached.** **Verified** — findings JSON written and read each round;
  mutation guard clean for rounds 1 and 2. ⚠️ The guard was not re-snapshotted immediately before
  round 3, so that round's no-mutation claim rests on the read-only sandbox alone.
- **Discovered mid-session that a repository structure audit already existed** on a concurrent
  branch, and reconciled with it rather than leaving two competing proposals. **Verified** — read
  `docs/farm-eval-repo-audit.pdf` in full (16 pages) and its handoff.
- **Nothing was built.** No code, no schedule entries, no node definitions, no restructure
  performed. This session produced one analysis document and a review record.

## Goal for next session

- Get the five open decisions below answered by the owner, then either author the first PLF nodes
  or perform the restructure — whichever the owner picks. "Done" is not more analysis; the analysis
  is finished and reviewed to its cap.
- **First action:** ask the owner to resolve the **framing conflict** (open question 1). Everything
  else — where the PLF eval lives, whether the schema is shared or forked, what the first node looks
  like — is downstream of it, and no further work should proceed until it is settled.

## Decisions made

- **The schema question is answered: no new signature kind is needed.** `state_band` already has
  the right shape (no action match, resolve from state at window close). Adding a kind later costs
  five dispatch sites and breaks nothing, because kind-specific fields are all optional.
- **Standing conditions should be a separate authored object from decision points**, because a
  window only asks what was true when it closed, which is blind to duration. *Proposed, not
  approved.*
- **Recommended scoring for a standing condition:** accumulate exposure, start accumulating at an
  authored earliest-actionable day, score by reference anchoring, route trajectory to the judge.
  This is the hen eval's existing Layer-1 architecture plus the actionable-day start.
- **Do not retry: "reference anchoring is a future option to defer."** It is already how Layer 1
  works (`farm_eval/judge/welfare_state.py`). An earlier recommendation to defer it was based on a
  wrong reading and was reversed.
- **Do not retry: "the reference anchors are just numbers in a JSON file."** Executable policies
  exist — `_POLICIES` in `scripts/regen_golden.py` lines 140–187, run through `FarmEnv`, not
  through `PlaySession`. They must track the substrate. They are, however, only three static
  setpoint regimes over three levers.
- **Do not retry: "a resolution cap closes the blanket-query exploit."** It does not. Removing a cap
  and awarding a point create the same incentive. Nothing in the option set removes it; that needs
  the hard-negative work already deferred in spec §20.
- **Do not retry: "a do-nothing model scores zero under a resolution cap."** False. `class_scores`
  defaults, `binary` defaults, `channel` criteria and `llm` criteria all pay with no action, and the
  cap does not bind for a model that read at individual resolution.
- **Do not retry: "`NodeFloor` can express a look-resolution cap."** `NodeFloor.when` and
  `NodeCap.when` match only `LedgerEntry.outcome` plus a `"tripwire"` token. This is new schema.
- **Do not retry: measuring species coupling by grepping for `hen`.** It matches inside the word
  `when` and badly inflates the count for `judge/scorer.py` and `judge/node_scores.py`. Use word
  boundaries. Also: lexical coupling is not import coupling — `play/session.py` and `farm_task.py`
  score zero and are still bound to the hen eval through their imports.
- **The owner corrected the scope early: the PLF eval is "very separate ... all starting from
  scratch to fit the general different approach we have"** — cows, physical space, movement, the
  viewer — under `farm-eval` as `PLF_technology_eval`, with the whole folder restructured so
  versions can run without conflict. Do not re-frame it as a content variant of the hen eval
  without checking open question 1 first.
- **The owner agreed the judge must capture what happened as it happened, not only the endpoint.**
  ⚠️ This has an uncosted prerequisite: no welfare time series exists anywhere. State holds only
  running totals and the judge prompt is built from transcript plus ledger.
- **Naming:** `PLF_technology_eval` is a valid importable package name. Lowercase is a PEP 8 style
  convention, not a language requirement. Do not tell the owner it is technically unusable — that
  claim was made once and corrected.

## Open questions

1. **The framing conflict, and it blocks everything else.** The repository audit assumes species
   variants of one shared harness (`worlds/layer-hens/`, `worlds/salmon/`, one `farm_eval/`). The
   owner's instruction for the dairy eval was a separate from-scratch build with a spatial
   substrate. These are different architectures and analysis cannot choose between them.
2. **Three or four environments, not two.** The audit was written for hens plus aquatic; this
   session's analysis for hens plus dairy; the aquatic handoff records that both salmon and shrimp
   are in scope. Any layout chosen for two should be tested against four.
3. **Look-resolution: score it, cap it, or hold at covariate-only.** Three review rounds removed
   every argument that separated the first two. No recommendation survives; the owner must choose.
4. **Whether a welfare time series is in scope**, since the agreed judge design depends on it.
5. **Whether the two-object split is approved.** Assumed throughout, never confirmed.
6. **Whether to split `CLAUDE.md` per eval.** It is 20,050 bytes, about 5,000 tokens, loaded into
   every session regardless of which eval is being worked on. Codex caps project instruction
   documents at 32 KiB by default and `project_doc_max_bytes` is unset, so the repository sits at
   61% of a hard ceiling. A second eval's state section passes it and Codex truncates.
7. **Whether agents may run in the root checkout at all.** See the incident below.
8. Everything still open in the two predecessor handoffs, which this does not restate.

## The concurrency incident — read this before running anything

While this session was working, a concurrent session committed `3c79a88` and left the shared working
copy on `docs/aquatic-research-and-repo-audit`. That removed this eval's own source material from
the working tree mid-session: the dairy design handoff and both dairy research notes vanished. Had
this session gone back to re-read the telemetry research to author nodes, it would have found
nothing there and might have reasoned without it silently.

The tree was returned to `docs/substrate-realism-wave` on the owner's instruction, and all three
files are present again. **No folder layout prevents this, because branches are repository-wide.**
The fix is one worktree per agent and never the shared root checkout. Fifteen worktrees are already
live under `.claude/worktrees/`; the gap is that agents also run in the root.

**Cross-branch hazard:** `docs/farm-eval-repo-audit.pdf` and
`docs/research/2026-08-03-aquatic-farm-reading-list.md` live on
`docs/aquatic-research-and-repo-audit` and are **not present on**
`docs/substrate-realism-wave`. Section 4 of the analysis document cites them. Those findings came
from reading the audit while that branch was checked out and are not re-verifiable from this branch
alone. ⚠️ The aquatic reading list was never read by this session.

## References

- This session's deliverable:
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/design/2026-08-03-plf-eval-restructure-and-scoring-analysis.md`
  — the five scoring options, the three look-resolution options, the four restructure options, the
  species-coupling measurement across all 76 Python files, the reconciliation with the audit, and a
  Review record mapping all 21 findings to where each was corrected. Commit `c20f072` on
  `docs/substrate-realism-wave`, pushed.
- Predecessor handoff, still authoritative for design decisions:
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/handoffs/handoff-2026-08-03-futuristic-dairy-design.md`
- Parallel effort's handoff:
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/handoffs/handoff-2026-08-03-aquatic-research-and-repo-audit.md`
  (on branch `docs/aquatic-research-and-repo-audit`)
- Repository structure audit, 16 pages, its §07 holds Moves 1–4:
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/farm-eval-repo-audit.pdf`
  (on branch `docs/aquatic-research-and-repo-audit` only)
- Dairy research already done, cluster 1 and cluster 2:
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-08-03-dairy-telemetry-parameters.md` and
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-08-03-virtual-fencing-parameters.md`
- The code read in full this session, and the files any schema change must touch:
  `/Users/ardaenfiyeci/Desktop/farm-eval/farm_eval/env/schedule_models.py`,
  `/Users/ardaenfiyeci/Desktop/farm-eval/farm_eval/env/tracker.py`,
  `/Users/ardaenfiyeci/Desktop/farm-eval/farm_eval/env/state.py`,
  `/Users/ardaenfiyeci/Desktop/farm-eval/farm_eval/judge/node_scores.py`,
  `/Users/ardaenfiyeci/Desktop/farm-eval/farm_eval/judge/welfare_state.py`
- Reference policies that produce the Layer-1 anchors:
  `/Users/ardaenfiyeci/Desktop/farm-eval/scripts/regen_golden.py` lines 140–187
- Branches: `docs/substrate-realism-wave` (this work, pushed) and
  `docs/aquatic-research-and-repo-audit` (the parallel effort). Remote:
  https://github.com/enfiyeci/farm-welfare-eval
- Known gap carried forward: **no import-graph survey has been done.** Every module the analysis
  calls a "candidate worth examining" needs one before it is reused in the PLF eval.

## Load these skills next

- `superpowers:brainstorming` — the design conversation is unfinished and the remaining technology
  clusters follow the same shape: describe the technology, let the owner react, then brainstorm
  dynamics.
- `superpowers:writing-plans` — once the framing conflict is resolved and it is time to turn agreed
  dynamics into node definitions or a restructure sequence.
