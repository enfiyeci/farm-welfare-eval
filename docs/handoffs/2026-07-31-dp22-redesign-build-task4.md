# Handoff: DP22 redesigned and reviewed — Task 4 build is the pickup point

## Intent

Make stocking density an emergent, *tempting* decision so the eval can separate *adequate* welfare
play from *excellent*. "Done" = a model that crowds H6 for margin scores measurably worse than one
that declines, **and the difference is carried by the world, not the judge**.

This session wrote no product code. It closed the last research questions, redesigned DP22 after
review found three defects in it, and put the design through three Codex rounds.

## State

**Verified at handoff time, not from memory.**

Branch **`feat/stocking-density`** in worktree `.claude/worktrees/density-n2/`, branched from
`974d24b`. **24 commits, working tree clean.** Suite: **3 failed, 1265 passed, 1 skipped** — the
same three expected failures sequenced to Task 13 behind the merge gate. Do not regenerate early.

Four commits this session, all docs:

| commit | what |
|---|---|
| `fe9441d` | research closing D15/D7/D11 + Kang 2018 obtained in full |
| `a936bb9` | the DP22 redesign spec |
| `85147c3` | Task 4 superseded from the spec; Task 4B (DP23) added |
| `dfd76dc` | two stale `CLAUDE.md` scoring claims corrected |

- **Tasks 1, 2, 3 — DONE** (earlier sessions).
- **Task 4 — DESIGNED, NOT BUILT.** No DP22 node, no `enabled_nodes` entry, no
  `tests/env/test_dp22_signature.py`, no emails.
- **Tasks 4B, 5–13 — NOT STARTED.** The research gate that blocked 5, 6 and 12 is **closed**: Task 5
  has its litter fraction (0.45), Task 6 its mechanism, Task 12 van Krimpen's fibre coefficient.
- **Nothing pushed.** 24 commits here plus 5 on `docs/substrate-realism-wave` in the main checkout.
  **Push was offered and NOT selected — do not push without asking.**

**A dangling reference is already waiting for you:** `schedule/events.yml:868` carries
`links_dp: DP22_PLACEMENT_DENSITY` on the day-270 `flock_placement` event. Task 3 pointed it forward
at a node that does not exist yet. Task 4 creates the target.

## Decisions & rationale

**Read `docs/specs/2026-07-31-dp22-redesign-design.md` before touching anything.** It is the
authority for Task 4 and it records every rejected alternative with its reasoning. The plan's Task 4
keeps only its step structure and its verified tracker notes; **the spec wins on any disagreement.**

Only what is *not* already written down there:

**Owner's standing principle, given 2026-07-31:** *"I don't want to drop stuff off, we will measure
every little thing / behavior we can measure."* Coverage beats parsimony. This is why DP23 survived a
proposal to fold it into DP22, and it should govern future scope calls on this wave. It does **not**
license measuring one behaviour three times — that inflates weight without adding information, which
is why overlap discipline is a hard build requirement.

**Owner does not want reasoning weighted highly** — *"i dont really care what its reasoning"* — hence
the 6/2/2 split favouring the action. Accepted consequence: passive compliance scores 4.0, because
the deliberate-vs-accidental distinction lives entirely in the judged criteria.

**Two rationales I wrote were FALSE and were withdrawn.** Both came from stale `CLAUDE.md` text (now
fixed in `dfd76dc`). Do not reintroduce either: Layer 1 does **not** carry severity into the
headline, and a tripwire does **not** zero the headline. The headline is the equal mean of the node
scores and nothing else.

**The overstock split went declined → split → reverted → split.** The final answer is `cap` +
`floor` used *together* (they are two independent fields). My revert rested on believing only `floor`
existed. The full history is in the spec's disposition section so neither wrong version returns.

**Round 4 of review was offered and skipped**, by owner choice, to reach pilots sooner. The wave is
therefore reviewed to round 3, not to APPROVED.

**Commits here use `Co-Authored-By: Claude Opus 5`**, while `CLAUDE.md:33` still says Opus 4.8.
Deliberate — the line records which model wrote the commit. Flagged, not changed.

## Open questions

- **Push or not.** 24 commits here, 5 on `docs/substrate-realism-wave`. Owner has not approved a push.
- **`CLAUDE.md:42` may hold a third stale claim** — it describes judge dimensions as "5 headline
  weight>0". Under C5 v2 no dimension affects the headline; those weights feed a diagnostic
  composite. Not verified, not changed.
- **DP17 overlap.** `DP17_STOCKING_DENSITY`'s `next_flock_placement` criterion (4 of its 10 points)
  already scores the very placement DP22 executes. Left as-is; the spec requires DP23's rubrics to
  respect the boundary, but narrowing DP17 was never decided.

## Next action

**Build Task 4** from `docs/specs/2026-07-31-dp22-redesign-design.md`, test-first, then run the Codex
review pair. Start with the failing test (`tests/env/test_dp22_signature.py`) — note the plan's
90,000-bird assertion now expects **`generous`**, not `compliant`.

Three things that will bite if skipped: `config.yml` `enabled_nodes` must gain DP22 (22 → 23) or the
node never opens; `tests/env/test_node_scoring_coverage.py:55` must be **narrowed, not relaxed** (all
three conditions are in the spec) or `class_scores` on a band node fails the suite; and
`class_scores` needs its `default` key or an unresolved band **raises** rather than scoring 0.

## References

- **Spec (the authority):** `docs/specs/2026-07-31-dp22-redesign-design.md`
- **Plan:** `docs/plans/2026-07-29-stocking-density-plan.md` — Task 4 (superseded banner + delta
  table), **Task 4B (DP23, new)**, merge gate, owner rulings
- **Research:** `docs/research/2026-07-31-density-decision-research.md` (D15/D7/D11 + the Kang
  denominator derivation), `docs/research/2026-07-30-density-coefficients.md` (read pass 6 first),
  `docs/research/sources/Kang-2018-EPS-aviary-stocking-density.pdf`
- **Prior handoffs, still live for traps:**
  `docs/handoffs/2026-07-30-density-task3-done-research-gate-complete.md`,
  `docs/handoffs/2026-07-30-stocking-density-build-tasks1-3.md` (wake-day trap, zero-reading trap,
  the measure-don't-reason lesson)
- **Shared test setup:** `tests/env/_density_support.py` — three documented traps
- **Worktree:** `.claude/worktrees/density-n2/` · tests `./venv/bin/python -m pytest -q` from there
- **Remote:** `enfiyeci/farm-welfare-eval` (unpushed)

## Load these skills next

- `superpowers:test-driven-development` — every task on this wave is written test-first, and the
  red-green discipline has caught real defects each time.
- `superpowers:subagent-driven-development` — **delegation is approved by the owner** for this build.
