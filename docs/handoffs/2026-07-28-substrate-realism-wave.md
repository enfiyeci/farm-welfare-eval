# Handoff: farm-eval substrate realism wave — design complete and reviewed, implementation not started

## Intent

The owner asked what was blocking a production run and which design choices were wrong. Auditing that
produced the governing principle for the whole wave, in the owner's words:

> **"Make sure choices that must reflect a change in reality do reflect a change in reality."**

"Done" = the simulated world responds to the agent's choices, and no decision node scores a signal the
world does not produce. The headline finding that motivates everything: **only 2 of 12 agent levers
move the world in both dimensions; five do nothing at all.**

## State

**Branch `docs/substrate-realism-wave`, 19 commits, nothing pushed. Merged up to `origin/main`
(`b40f870`), so it is current — includes PR #18 and PR #21. Verified clean: 12 files changed, 2516
insertions, ZERO deletions vs `origin/main`.**

⚠ **Local `main` is a stale ref at `49229b7`, far behind `origin/main`.** Always branch and diff
against `origin/main`; `git diff main..HEAD` reports ~113 commits of unrelated history.

Complete and verified:
- **Lever audit** over the full 518-day horizon, real `FarmEnv` pipeline. Findings F1–F10.
- **Design spec**, ~1,250 lines, nine sections.
- **Two probe documents** — the lever audit and the DP06 false-zero proof.
- **Research provenance** — five documents, four from commissioned passes.
- **Ten rounds of Codex adversarial review**, all adjudicated. Counts: 12, 8, 4, 3, 6, 2, 2, 1, 1.
  No Critical since round 2. Rationale for each round is in its commit message.
- **All four blocked coefficients resolved** (see Decisions).
- **Three owner decisions taken** 2026-07-28: repair DP06, Reliable supervises the catch crew, defer
  the retrofit trade until keel is measured.

NOT done — be blunt about this:
- **No implementation. No code touched. No tests written.** Everything above is design and evidence.
- The Bedrock pilot runner exists and **Opus 5 is verified working** (`us.anthropic.claude-opus-5`,
  HTTP 200), but **no run has happened**. Key expires ~2026-07-30 and the owner has not said whether
  to spend it on a pilot against current `main` before it lapses. **Still unanswered.**

## Decisions & rationale

Everything with a *why* is in spec §8 and the commit messages. What exists **only** in this session:

- **The review loop's 3-round cap in `~/.claude/CLAUDE.md` was explicitly waived by the owner** ("keep
  iterating until there is no issue left to find"). That is why there are ten rounds. **It does not
  carry forward.**
- **`feed_ration` has been decided three times and the order matters.** Round 6 said wire the cost
  half; round 7 reversed that, because cost-without-physiology lets an agent zero the largest cost
  line with no welfare consequence — a dominant free-money exploit; research then sourced the
  physiology, so both halves can now land together, which was always the stated condition. **Do not
  "simplify" this back to cost-only.**
- **Rounds 6, 8, 9 and 10 each introduced a defect the next round caught.** Treat every new rule in
  this spec as capable of the same.
- **Rejected, do not revive:** a belt-frequency energy cost (no study supports it; physics points the
  other way); per-house feed inventories (turns the eval into an inventory-management test); wiring
  D3 to mortality (effect too large to transplant, would make a cheap additive the dominant welfare
  lever); an authored breaking-stock price series (no defensible shape for the spike months);
  limestone particle size as a lever (**converts to ~0.05 pp of breakage — below the noise floor**;
  the modellable effect is calcium *level*).
- **The HVAC blocker was NOT a research problem, and this is the most transferable lesson here.** It
  looked like the biggest calibration gap in the wave. The researcher's numbers were fine. The actual
  cause was that `layers/heat.py::indoor_temp_c` computes `max(setpoint, ambient − cooling)`, so in
  winter the house holds setpoint for free and `vent` does nothing — **`vent` is a cooling lever, not
  an airflow rate**, and those differ ~30× across seasons. Twenty minutes reading the code found what
  no amount of literature would have. **Read the substrate before commissioning research about it.**
- **`CLAUDE.md` is stale in at least one load-bearing place** — it describes the Layer-3 tripwire gate
  as active. It was removed in C5 (`farm_eval/judge/scorer.py:301-309`). This misled the spec for two
  rounds. **Trust the code over the docs**, and fixing that line is part of this wave.
- **Nodes can score signals that do not exist.** DP18 was known; DP06 was found the same way this
  session and is worse (it is *inverted* — correct restraint scores 0, a groundless vet call scores
  6). Before trusting any node, confirm its declared signal actually occurs in the substrate **and**
  is readable through the tool surface.
- **My error, already fixed:** commit `1c836cc` used `git add -A docs/` and swept in four of the
  owner's untracked HTML working files. Untracked again in a later commit; the files are untouched on
  disk. **Stage by explicit path in this repo** — the owner keeps working files under `docs/`.

## Open questions

Spec §9 has the full list. Genuinely open after this session:

- **Storage capacity, spoilage, and the ceiling search space** (§9.5, §9.6) — mine to decide; settle
  them in the plan rather than asking.
- **Keel window framing, corner-config regeneration, reference-policy audit** (§9.7, §9.8, §9.10) —
  mechanical, decided, need doing.
- **Whether "good welfare" should carry a winter fuel bill.** Fell out of the HVAC fix: the `good`
  reference policy holds ventilation at 2.0 year-round, so it over-ventilates through winter and burns
  1.6 L/hen/yr. That is a flaw in the *policy*, not the model. **Owner call, not yet asked.**
- **The retrofit trade at $600k** — deferred by the owner until keel movement is measured.

## Next action

**Write the implementation plan** (`superpowers:writing-plans`) from spec §8's decisions. Sequence
**§2c's keel measurement first** — it is on the critical path because the owner's retrofit-trade
decision depends on it, and if the complex-wide movement is genuinely ~2–3 % the honest fix is
per-house channel weighting rather than adjusting the price or the points. Then §2 (nutrition/bone)
and §5 (financial feedback), which are independent and unblocked. Do NOT start coding before the plan
exists — this project's convention is brainstorm → plan → build with review per task.

## References

- Branch `docs/substrate-realism-wave`, 19 commits, unpushed. Base = `origin/main` @ `b40f870`.
- **Spec:** `docs/specs/2026-07-28-substrate-realism-wave-design.md` — §7 acceptance test, §8
  decisions with rationale, §9 open items.
- **Probes:** `docs/probes/substrate-realism-audit-2026-07-28.md` (F1–F10, the lever audit),
  `docs/probes/dp06-mortality-latency-false-zero-2026-07-28.md`.
- **Research:** `docs/research/2026-07-28-substrate-realism/` — the README's verification table marks
  which claims were re-checked at primary sources and which are the researcher's word alone.
- **Bedrock pilot:** `scripts/run_pilot_bedrock.sh`; key in `scripts/pilot-bedrock.env` (gitignored,
  expires ~2026-07-30). Fable 5 needs an account-wide data-retention change that shares prompts with
  the provider — **do not make that change without explicit consent.**
- Commit messages carry the full round-by-round review rationale; they are the audit trail.

## Load these skills next

- `superpowers:writing-plans` — the immediate next step.
- `superpowers:subagent-driven-development`, `superpowers:test-driven-development` — this project's
  established build discipline.
