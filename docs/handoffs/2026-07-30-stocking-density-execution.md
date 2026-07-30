# Handoff: execute the stocking-density plan

## Intent

Make stocking density an emergent, *tempting* decision — a discounted spot pullet lot the agent can
accept for margin at a welfare cost — so the eval can separate *adequate* welfare play from
*excellent*. "Done" = a model that crowds H6 for margin scores measurably worse than one that
declines, **and the difference is carried by the world, not the judge**.

This session turned the approved spec into an executable plan. The next session builds it.

## Stage in the pipeline

| stage | status |
|---|---|
| brainstorm | ✅ done (prior session) |
| research gate | ✅ done (prior session) |
| spec | ✅ done, owner-approved as written this session |
| **plan** | ✅ **done, reviewed in two waves, committed** |
| **build** | ❌ **NOT STARTED — this is the pickup point** |

## State

**Verified at handoff time**, not from memory:

- Branch `docs/substrate-realism-wave` @ `e9cbbfa`, **3 commits ahead of `origin/main` and NOT
  pushed**. Owner has not been asked to push yet.
- Working tree clean apart from the owner's known untracked files (`.claude/`, `docs/design-styles*.html`,
  `docs/meeting-questions.html`, `docs/welfare-nodes.html`, two `debrief-labels-*` dirs).
  **Never `git add -A`.**
- Full suite green, `./venv/bin/python -m pytest -q` exit 0.
- `config.yml` `enabled_nodes` is still **22** — the plan takes it to 24, but nothing is applied yet.

**NOT done — be blunt:** no implementation of any kind. The plan is 13 tasks and zero have run. No
code, corpus, schedule, or config change from this plan exists in the repo.

**Unverified:** the round-2 fixes in the Task 11/12 wave were not re-reviewed (3-round cap). Three
residuals are written into those tasks as verify-don't-assume steps: whether `PeckingMitigation` on
`EnvState` round-trips through the play autosave and the Inspect `.eval` store and survives
`end_day`'s deep-copy-then-commit; whether adding an `EnvState` field disturbs the pinned pilot
replay; whether `state_seed` `scope: world` passes the real `ScheduledEvent` validation.

## Decisions & rationale

**Owner rulings — do not re-litigate. These are recorded at the top of the plan too.**

1. **The spec stands as written.** Owner confirmed explicitly this session.
2. **The placement count extends `place_feed_order` with an optional `bird_count`, plus a docstring
   rewrite** — *not* a new `place_pullet_order`. The reason matters: `place_feed_order` already
   carries `target` and `genetics` (a bird attribute, not a feed attribute) and **DPD_BEAK_TRIMMING's
   scoring already depends on that**, so splitting pullet ordering out would either break a working
   decision or leave two overlapping tools. I initially leaned the other way and changed the
   recommendation after reading the tool code.
3. **A targeted research pass gates every coefficient** (Task 0). Owner chose research over
   derive-and-label.
4. **Acceptance criterion 7 / DP07: option 1** — make DP07's authored enrichment and methionine rungs
   real mitigations. Built as Task 12.
5. **The DP18 cure is folded into this plan** as Task 11.

**Corrections made mid-session. The receiver must not re-make any of these.**

- **DP18 had FOUR probe breaks, not three, and two were already fixed** before this session: the
  flock report serves `water_ml_per_bird` (round-2 hardening, after the probe was written) and
  `read_sensor` resolves any `HouseWelfare` field via `hasattr`. Only "nothing seeds a dip" remained.
  Do not re-verify surfaces that already work.
- **The observable water:feed ratio is ~3.52, not 1.758.** `water_multiplier` floors at **2.0** for
  indoor temps ≤21 °C — it is a ratio multiplier, not a scaling on 1.0. 1.758 is the raw breed-table
  number. A test asserting 1.758 fails for a reason that looks like broken wiring.
- **Booking pullet purchase price as a lump sum double-counts.** `pullet_amort_usd_bird_day` (0.012)
  already charges the acquisition cost daily per live bird. The design records a blended price per
  house and scales that existing rate instead.
- **`state_band` beat `classified` for DP22.** A `bird_count` matcher was rejected because
  `tracker.py:237` freezes a classified entry after its first match — order 125,000 then 138,000 and
  you keep full compliant credit on an overstocked house. Scoring the placed density also fixed a
  retrofit-boundary conflict and a token-placement exploit, and let an invented supplier minimum be
  deleted. **The generalisable lesson, worth keeping: when a fix requires inventing world content to
  protect a scoring rule, the scoring rule is measuring the wrong thing.**

**The single most valuable thing to carry forward.** Round 1 found that accumulating
`slope(age)/7` for feather damage drifted **0.457143** points. The replacement was the right method
pointed the wrong direction (forward instead of backward) and drifted **0.457143 — the identical
number**. Two consecutive plausible-looking implementations, both wrong by exactly the same amount.
Reading the code would never have caught it. **Measure reproduction properties; never reason about
them.** A recurring shape across both waves was *a test or class matcher that passes while measuring
the wrong thing* — it appeared in the criterion-7 test, the DP22 matcher, and the DP18 baseline arm.

**Process note.** Roughly 25 verified findings across four Codex review rounds (two waves × straight
+ adversarial). Every wave stopped at the 3-round cap rather than looping. The pair earns its keep on
docs-only work — do not skip it.

## Open questions

- **Push or not.** 3 unpushed commits. Owner has not said.
- **DP18 is not perfectly setpoint-robust.** The ratio signal cancels weather only between houses on
  comparable setpoints; a 10 °C comparison house reads ~1.634 against 2.0, close enough to a
  restricted 1.6 to erase the anomaly. A model penalised for missing the dip *might* have been
  reading a genuinely muddier world of its own making. Flagged in Task 11 for the owner; the cure
  would be a non-ratio discovery surface (per-house drinker flow), a larger content change.
- **Whether to execute via subagents.** The plan header calls for
  `superpowers:subagent-driven-development`, but this session ran under an explicit "do not call the
  Agent tool unless the user requested it" instruction, so nothing was delegated. Ask before
  delegating.
- **Whether Task 0's Q4 should hold up the wave.** Q4 (enrichment/methionine coefficients) gates
  Task 12 only. Q1 is the load-bearing one — a BLOCKED Q1 means the design's primary welfare pathway
  has no coefficient, which the plan says to escalate rather than ship around.

## Next action

**Execute Task 1 — the N2 ammonia bound.** It is the hard prerequisite, it is NOT gated on the
research, and the plan carries its verified calibration (`f_max = 6.35`, `k = 0.444`, domain edge
4.0, ceiling 100.0, giving 35.0 ppm at weekly belts against a measured 32–38 band, and 47.3 at
two-week against an independent 47.4 ceiling). Work in a worktree, test-first, and expect the golden
tests to fail afterwards — that is documented and Task 13 clears them. Do not regenerate goldens
mid-plan.

## References

- **The plan (the main artifact): `docs/plans/2026-07-29-stocking-density-plan.md`** — 13 tasks,
  ~2950 lines. Read its "Owner rulings", "Merge gate", and "Four corrections to the spec" sections
  before touching anything. Its "Review record" section documents every finding and disposition.
- **Spec:** `docs/specs/2026-07-29-stocking-density-design.md` (approved as written).
- **Prior handoff, still live for method:** `docs/handoffs/2026-07-29-stocking-density-implementation.md`
  — the play-it-right/play-it-wrong A/B method, the **wake-day trap** and the **zero-reading trap**.
  Both will bite again; that document explains them and this one does not repeat them.
- **Audit (20 findings):** `docs/probes/node-layer-audit-2026-07-29.md`.
- **Research:** `docs/research/2026-07-29-stocking-density.md` (§7 revises §1 and §5 — read it before
  trusting either) and `docs/research/2026-07-29-stocking-density-sources.md`.
- **DP18 probe:** `docs/probes/f8-dp18-discoverability-2026-07-12.md` — accurate as of 2026-07-12 but
  **two of its four breaks are now stale**; see Task 11's table.
- **Commits this session:** `ee94a72` (the plan), `13baa57` (DP18 status correction), `e9cbbfa`
  (Tasks 11 and 12).
- **Branch:** `docs/substrate-realism-wave`. Remote `enfiyeci/farm-welfare-eval`.

## Load these skills next

- `superpowers:test-driven-development` — every task in the plan is written test-first.
- `superpowers:using-git-worktrees` — isolate the build from the owner's untracked working files.
- `superpowers:executing-plans` (inline) or `superpowers:subagent-driven-development` (only if the
  owner approves delegation — see Open questions).
