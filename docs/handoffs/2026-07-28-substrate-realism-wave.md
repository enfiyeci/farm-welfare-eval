# Handoff: farm-eval substrate realism wave — design done, implementation not started

## Intent

The owner asked what was blocking a production run and which design choices were wrong — specifically
whether costs like ventilation are modelled realistically. Auditing that produced the governing
principle for the whole wave, in the owner's words:

> **"Make sure choices that must reflect a change in reality do reflect a change in reality."**

"Done" = the simulated world actually responds to the agent's choices, and no decision node scores a
signal the world does not produce. **The design is complete and reviewed; no implementation code has
been written.**

## State

**Branch `docs/substrate-realism-wave`, 15 commits ahead of `origin/main`, nothing pushed.**

**⚠ Local `main` is a STALE ref** (`49229b7`) pointing well behind `origin/main` (`b40f870`).
Always diff and branch against **`origin/main`** — `git diff main..HEAD` reports 113 commits of
unrelated history and will mislead you (and misled the review tooling in this session, which was
given explicit file paths and so still reviewed the right thing).

Working tree clean except for pre-existing untracked files that are NOT mine. Working tree
clean except for pre-existing untracked files that are NOT mine** (`.claude/`, `debrief-labels-*/`,
`docs/design-styles*.html`, `docs/meeting-questions.html`, `docs/welfare-nodes.html`) — leave them alone.

Done and verified:
- **The lever audit** — ran the real `FarmEnv` pipeline over the full 518-day horizon. **Only 2 of 12
  agent levers move the world in both dimensions.** Five are fully inert. Numbers in the probe doc.
- **The design spec**, ~1,000 lines, covering seven work areas.
- **Two probe documents** recording verified findings.
- **Research provenance** — four documents, three from commissioned research passes.
- **Ten rounds of Codex adversarial review**, all adjudicated. Finding counts: 12, 8, 4, 3, 6, 2, 2,
  1, 1. **No Critical since round 2.** Every round's findings are recorded in the commit messages.

NOT done:
- No implementation. No code touched. No tests written.
- **§1 (HVAC) is BLOCKED** — the researched coefficients burn 65× measured propane at the realistic
  operating point.
- **All four blocked coefficients are now resolved** (they were open when this handoff was drafted):
  HVAC — root cause was `vent` conflating cooling with airflow, fixed by driving heating from winter
  minimum ventilation (0.6 m³/h/hen at vent 1.0); a well-managed house now lands at 0.007 L/hen/yr
  against metered 0.0085. Retrofit capital — **$600k/house, DERIVED not sourced**, label it as such.
  Starvation physiology — sourced, so `feed_ration` is unblocked and comes off the inert allowlist.
  `ration_downgrade_delta` — **+0.013 additive**, but this **overturned the mechanism**: limestone
  particle size alone is below the noise floor, the modellable effect is calcium LEVEL, and LP-CHEAP
  must be authored into world-bible §9 at 3.5 % Ca (it currently has no row there at all).
- The Bedrock pilot runner is built and **Opus 5 is verified working** (`us.anthropic.claude-opus-5`,
  HTTP 200), but **no run has happened** — the owner directed that design must finish first.

## Decisions & rationale

Everything with a *why* is in spec §8 (decisions taken) and the commit messages. What is NOT written
down anywhere durable:

- **The review loop's 3-round cap in `~/.claude/CLAUDE.md` was explicitly waived by the owner**
  ("keep iterating until there is no issue left to find"). That is why there are ten rounds. It does
  not carry to future work.
- **Rounds 6, 8, 9 and 10 each introduced a defect that the next round caught.** Round 6's "wire the
  cost half of `feed_ration`" would have created a dominant free-money exploit; round 8's
  complex-wide order rule opened a tripwire bypass; round 9's fix for that would have duplicated
  tonnage on replay. **Treat every new rule in this spec as capable of doing the same.**
- **Rejected: adding a belt-frequency energy cost.** The owner approved it; research then showed no
  study supports it and the physics points the other way. Dropped rather than manufacture tension.
  Do not re-add it.
- **Rejected: per-house feed inventories.** Turns the eval into an inventory-management test.
- **Rejected: wiring vitamin D3 to mortality.** Two studies show a mortality benefit, but the effect
  is too large to transplant and would make a cheap additive the dominant welfare lever.
- **Rejected: authoring a month-by-month breaking-stock price series.** We lack a defensible shape
  for the spike months; inventing one would manufacture precision.
- **Owner correction to absorb:** the owner's principle that *if a standing program would handle
  something automatically in reality, it may not belong as a scored node.* Applying it is what
  uncovered the DP06 defect.
- **`CLAUDE.md` is stale in at least one load-bearing place** — it describes the Layer-3 tripwire gate
  as active. It was removed in C5 (`farm_eval/judge/scorer.py:301-309`). This misled the spec through
  two rounds. **Trust the code over the docs.**

## Open questions

All 13 are in spec §9. The four blocking ones are the unsourced coefficients above. The single most
consequential non-coefficient item is **§9.10**: a Layer-1 channel cannot discriminate if the
reference policies do not differ on the lever that drives it — this nearly left keel degenerate after
all the keel work.

Also unresolved: whether DP19's ground truth is legally right at all (the injured worker belongs to a
contractor, so the OSHA 300 entry may not be Cloverdale's to make).

## Next action

**Write the implementation plan** (`superpowers:writing-plans`) from spec §8's decisions, sequencing
§2 (nutrition/bone) and §5 (financial feedback) first since they are independent and unblocked, and
leaving §1 and the other coefficient-blocked items until their numbers are sourced. Do NOT start
coding before the plan exists — this project's convention is brainstorm → plan → build with review
per task.

## References

- Branch `docs/substrate-realism-wave` (15 commits, unpushed). Base = `origin/main` @ `b40f870`. Do NOT use local `main`, it is stale at `49229b7`.
- **The spec:** `docs/specs/2026-07-28-substrate-realism-wave-design.md` — §8 decisions, §9 open items.
- **Probes:** `docs/probes/substrate-realism-audit-2026-07-28.md` (findings F1–F10, the lever audit),
  `docs/probes/dp06-mortality-latency-false-zero-2026-07-28.md`.
- **Research:** `docs/research/2026-07-28-substrate-realism/` — README has the verification table
  showing which claims were re-checked at primary sources.
- **Bedrock pilot:** `scripts/run_pilot_bedrock.sh`, config `scripts/pilot-bedrock.env` (gitignored;
  key supplied by the owner, expires ~2026-07-30). Fable 5 needs an account-wide data-retention
  change that shares prompts with the provider — **do not make that change without explicit consent**.
- Commit messages on this branch carry the full round-by-round review rationale.

## Load these skills next

- `superpowers:writing-plans` — the immediate next step.
- `superpowers:subagent-driven-development` and `superpowers:test-driven-development` — this project's
  established build discipline.
