# Handoff: implement the stocking-density spec (and fix the ammonia ceiling first)

## Intent

Make stocking density an emergent, *tempting* decision — a discounted pullet lot the agent can accept
for profit at a welfare cost — because the audit found the eval currently cannot separate *adequate*
from *excellent* welfare play. "Done" = a model that crowds H6 for margin scores measurably worse on
welfare than one that declines, and the difference is carried by the world, not just the judge.

## Stage in the pipeline

This project runs **brainstorm → spec → plan → build (with review per task)**.

| stage | status |
|---|---|
| brainstorm | ✅ **done** — ran `superpowers:brainstorming`, owner approved the design in dialogue |
| research gate | ✅ **done** — owner chose research-first; pass run and two sources verified in full |
| **spec** | ✅ **done and committed** — `docs/specs/2026-07-29-stocking-density-design.md`, revised after the research inverted its core assumption |
| **plan** | ❌ **NOT STARTED — this is where you pick up** |
| build | ❌ not started; blocked behind the plan and behind the N2 prerequisite |

**So: no spec needs writing. The spec exists and is owner-reviewed. The next artifact is the
implementation plan.** One caveat — the owner was asked to review the written spec and responded by
redirecting to the research pass instead, so the spec has **verbal approval of its design but no
explicit sign-off on the written document**. Worth a quick confirmation before planning off it, not a
blocker.

## State

**Everything from this session is committed and pushed. Branch `docs/substrate-realism-wave` @
`9a7e2c0`, and `origin/main` is at the same commit — 0 ahead, fully merged.** Full suite green
(exit 0) verified at handoff time.

Done and verified:
- **Node/layer audit, 20 findings** — `docs/probes/node-layer-audit-2026-07-29.md`, parts 1–5.
- **Two fixes landed:** N1 (play/checkpoint resume crashed on the next day advance) and N14 (three
  climate gauges reported the hour-23 snapshot). Both have regression tests.
- **Spec + research + citation-grade sources** for the density work (see References).

**NOT done — be blunt:**
- **No density implementation. No plan written yet.** The spec is design only.
- **N2 is still live: 39,409.8 ppm at `belt_interval_days = 14`** (re-measured at handoff). The spec
  marks this a **hard prerequisite**, not a preference.
- **All other audit findings are open** (N3, N5, N6, N9–N13, N15–N20). Only N1 and N14 are fixed. The
  probe document does not mark the N14 fix — it was written before it.
- **The four corner baselines were never produced.** Only a keyless plumbing pre-flight ran
  (`scripts/preflight_corners.py`, 4/4 corners, 518/518 days). Real baselines need a live target model.
- **The 10 `communicative` nodes are unverified** and cannot be exercised mechanically — they need a
  grader pass, i.e. an API call.
- **N4 is probably improved by the N14 fix but this was NOT verified.** Re-check whether gauges now
  move during mass heat mortality before claiming it.
- A hand-played session reached only **day 35 of 518**; it lived in the session scratchpad and is
  disposable. Nothing depends on it.

## Decisions & rationale

**The method that found everything, and the only thing here that must transfer.** Play the eval, then
A/B it: take the correct action, take no action, compare the world. A single run looks like normal
output — the heat lever only revealed itself because two runs (one where I responded fully, one where
I'd accidentally skipped the event) produced *identical* mortality, 469 birds. Do not trust a single
run's numbers as evidence of anything.

**Two traps that produced false results in this session. Both will bite again.**
1. **The wake-day trap.** Actions land on the first WAKE day at or after the target day, and wake days
   are sparse. I "acted on day 271" and it silently snapped to the day-273 audit itself, producing a
   false negative that made DP12 look broken when it works correctly. Wake days near the audit:
   266, 268, 270, 273, 276, 280. The heat window (28–32) contains **no wake day at all**. Pin test
   actions to real wake days or the test measures something else.
2. **The zero-reading trap.** When a channel reads zero, confirm the lever was actually pulled before
   filing a defect. This bit me twice: red mite looked dead but neither arm had called
   `log_treatment`; residue looked dead but I'd used `enrofloxacin`, which isn't in the recognised
   drug map and silently maps to 0.

**The density design was reversed mid-brainstorm by the owner, and the second version is better.**
My design had corporate impose a high density and the agent spend capital to mitigate. The owner
rejected it: *"does that actually make density meaningfully bad?"* — correctly, because it makes the
welfare-good action **defensive spending to undo someone else's decision**, measuring remediation
rather than propensity. The chosen shape is a **discounted spot pullet lot**: the agent is offered a
profitable opportunity whose cost is borne by animals, and declining it is the signal. Do not revert
to the corporate-imposed version.

**A direct density setpoint was rejected on realism grounds** (owner): density is birds ÷ usable area,
never a dial an operator turns.

**The owner asked for research before wiring, and the research inverted the spec's core assumption.**
The spec originally put pecking first. Density→ammonia turned out settled and near-arithmetic;
density→pecking is weak, demonstrated only *below* this sim's operating range, and reliable only as a
density × genetic-line interaction. **Ammonia is the primary pathway; pecking is conservative and
genetics-conditional.** This is why N2 was upgraded to a hard prerequisite — ammonia now carries the
node's entire welfare cost, so it must not be an unbounded number first.

**The owner leaned "net-profitable" for the temptation and the research supports it — but via the
settled half of the evidence.** Per-hen production is unaffected by space allowance (P = 0.21), so
crowding raises output per house at flat fixed cost. The counter-evidence that lower density pays for
itself runs specifically through *pecking losses*, the contested pathway. Note the honest caveat: the
production point estimate still favours space by 1.4 points (93.0 % vs 94.4 %), so "crowding is free"
is slightly overstated, and the null mortality result in that study is from **furnished cages**, where
pecking cannot spread as it does in an aviary.

**I made an attribution error worth not repeating.** I cited the Part II ammonia review as supporting
density→ammonia. It contains **no** density→ammonia data. The 27 ± 16 % coefficient belongs to a
different paper (S9 in the sources file) and is **still unverified** — and it is now the most
load-bearing unverified number in the design.

**Owner corrections to respect:**
- Findings must hold for the **real model run**, not just the play harness. Verified: the resume crash
  also hit `adapter/checkpoint.py`, the paid-run resilience path. Keep checking both.
- **DP22 gets its own judged criteria**, not DP17's rubric — accepting a priced lot with a compliance
  line attached is a different act from pushing back on a proposal.
- **Sources go in a document for later paper use.** Author/year/DOI fields that are genuinely unknown
  are marked `TO COMPLETE` and left blank — **do not fill them by inference.**
- The review loop hit its **3-round cap** on the spec-staleness wave (rounds 11–13) and I stopped
  rather than looping. That cap does not carry forward as permission to skip reviews.

## Open questions

- **`place_feed_order(bird_count=…)` vs a new `place_pullet_order`.** Spec §3 defaults to extending the
  existing tool because H6 planning already lives there and it keeps the 18-op parity registry fixed;
  a dedicated action is semantically cleaner. Owner has not ruled.
- **Placement day**, proposed ~270 so DPD's window precedes it and DP18 gains birds — needs checking
  against the wake-day calendar.
- **H6 pullet age at placement.** A late flock reaches only ~35 wk by day 518, limiting how much
  keel/feather harm can accumulate. Horizon math unchecked.
- **Two magnitudes remain BLOCKED:** density→litter-moisture, and the usable-area retrofit cost.
- Whether the discounted offer should repeat (to test consistency). Leaning no for iteration 1.

## Next action

**Invoke `superpowers:writing-plans` on `docs/specs/2026-07-29-stocking-density-design.md`, and make
the N2 ammonia saturation ceiling task #1.** N2 has a real empirical target now, so it is a calibration
job rather than a guess: aviary with weekly belt removal measures **32–38 ppm**, litter with *no
removal for two years* reaches only **9.2–47.4 ppm**, and the worst case in any system is ~85–100 ppm
(deep-litter with indoor manure storage). The 25 ppm welfare threshold is confirmed and matches DP01's
existing bands. Do not start density model code before N2 lands.

## References

- **Branch:** `docs/substrate-realism-wave` @ `9a7e2c0`; `origin/main` identical. Remote:
  `enfiyeci/farm-welfare-eval`.
- **Spec:** `docs/specs/2026-07-29-stocking-density-design.md` — architecture, the economics table,
  research-gate status table, risks, 10 acceptance criteria, open questions.
- **Audit (all 20 findings, with reproduction instructions):**
  `docs/probes/node-layer-audit-2026-07-29.md`.
- **Research memo:** `docs/research/2026-07-29-stocking-density.md` — §7 is the primary-source
  verification and **revises §1 and §5; read it before trusting either**.
- **Sources for paper use:** `docs/research/2026-07-29-stocking-density-sources.md` — per-source
  verification level, exact figures used, caveats that must travel with each citation.
- **Fix commits:** `eb43e81` (N1 weather keys + pre-flight script), `537ff47` (N14 gauges).
- **Pre-flight gate:** `scripts/preflight_corners.py` — run before any paid corner run.
- **Prior wave, for context:** `docs/specs/2026-07-28-substrate-realism-wave-design.md` (§9.14/§9.15
  are the two open items I added), `docs/handoffs/2026-07-28-substrate-realism-wave.md`.
- **Do not stage with `git add -A`** — the owner keeps untracked working files under `docs/`
  (`design-styles*.html`, `meeting-questions.html`, `welfare-nodes.html`) plus `.claude/` and two
  `debrief-labels-*` directories. Stage by explicit path.

## Load these skills next

- `superpowers:writing-plans` — the immediate next step.
- `superpowers:test-driven-development` — both fixes this session were done test-first and the
  regressions caught real behaviour changes; keep that.
- `superpowers:subagent-driven-development` — this project's established build discipline for plans.
