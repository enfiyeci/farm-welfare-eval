# Handoff: building the stocking-density plan (Tasks 1–2 done, Task 3 half-built)

> **Provenance note (added 2026-08-03 on salvage). SUPERSEDED — do not pick this up.** The state
> below was true on 2026-07-30 and is long overtaken: the build continued past Task 5 on
> `feat/stocking-density-task6`, whose own later handoffs supersede this one. As of 2026-08-03
> Task 6 is BLOCKED (the sourced NH3 coefficient collides with two measured anchors) and that
> branch's suite is red on its own tip — the good-operator reference policy accumulates ~19,662
> nh3-ppm-hours-over against a golden of ~744.
>
> Kept only because `docs/plans/2026-08-02-sept10-programme-plan.md` cites this filename. It
> lived solely on `docs/substrate-realism-wave`, now deleted and preserved as tag
> `archive/substrate-realism-wave`. For current state read the handoffs on
> `feat/stocking-density-task6`, not this file.

## Intent

Make stocking density an emergent, *tempting* decision — a discounted spot pullet lot the agent can
accept for margin at a welfare cost — so the eval can separate *adequate* welfare play from
*excellent*. "Done" = a model that crowds H6 for margin scores measurably worse than one that
declines, **and the difference is carried by the world, not the judge**.

The plan for that is written and reviewed. This session started executing it.

## State

**Verified at handoff time, not from memory.**

Build work is on branch **`feat/stocking-density`**, in worktree
`.claude/worktrees/density-n2/` (venv symlinked; run tests from that directory).
Branched from `974d24b`. Seven commits, working tree clean.

- **Task 1 (N2 ammonia bound) — DONE**, 4 commits `b212579 → 58054e4`, three review rounds.
- **Task 2 (density as a derived identity, N20) — DONE**, 2 commits `2afe34c`, `7d38180`,
  one review round + fix wave.
- **Task 3 (placement lever) — HALF BUILT**, `0cad111`, explicitly committed as WIP.
  That commit message lists precisely what is done and what is not. **Read it first.**

**Suite: exit 1, 7 failures, all expected and all accounted for:**
- 5 in `tests/env/test_placement_order.py` — red *by design*; they cover the `flock_placement`
  event that Task 3 has not built yet.
- 2 golden fixtures (`test_reference_runs_match_golden`, `test_baseline_checkpoints_match_golden`)
  — the plan sequences regeneration to Task 13 behind a merge gate. **Do not regenerate early.**

**The main checkout** (`~/Desktop/farm-eval`) is still on `docs/substrate-realism-wave` @ `974d24b`,
4 commits ahead of `origin/main`, **unpushed**. Nothing has been pushed this session.

**Golden movement so far** (only `nh3_ppm_hours_over` moves; footpad, heat, keel and excess
mortality unchanged on all three policies): good 743.56 → **0.00**, competent −41.0 %, negligent
−61.6 %. `good` reaching zero is correct, not degenerate — its old value came entirely from the
unphysical litter accumulation Task 1 removed.

## Decisions & rationale

**Owner ruling this session, not in the plan when it was written.** The litter-age term was
originally recorded as a benign residual; review disproved that and the owner ruled **fix it now,
same method as N2**. It was contradicting the measurement the two-week anchor was calibrated
against (source says litter unremoved for two years reaches 9.2–47.4 ppm; the model returned 100)
and it flattened the ventilation lever in *ordinary* play. Fixed by capping the age input at 60 d.
Full record in `docs/model-params.md` §Ammonia. **Do not reopen.**

**Two Task-1 defects that were about levers, not numbers, and are easy to reintroduce:**
- Clamping only the finished concentration flattened ventilation entirely — every setting from 0 to
  2.29 returned an identical 100 ppm. The ceiling must bound `emission` **before** ventilation
  clearing. There are now three clamp sites and the order is load-bearing; `ammonia.py` says why.
- Clamping *after* relaxation made ventilation 0 and 5 indistinguishable on a legacy state's first
  day. The incoming concentration is projected onto the rail **before** relaxing.

**The measure-don't-reason lesson, which cost two rounds.** A left-endpoint slope sum for feather
damage drifts 0.457143 points. Its replacement was the right method pointed the wrong direction and
drifted **0.457143 — the identical number**. Task 12 now specifies the backward telescoping form.
Measure reproduction properties; never reason about them.

**Density is written twice per day loop, deliberately** (`integrate.py`): once above the empty-house
skip so the harm layers see the start-of-day value the flock actually experienced, and again after
mortality so the persisted value equals area / *live* birds. Removing either reintroduces a
reviewer-found defect. Both are commented.

**`audit_thresholds` is optional at load but validated when it matters.** Making it required broke
~190 tests, because the fixture corpora do not carry it. Making it silently optional meant a
production corpus that lost the key would run hundreds of days with frozen densities and only die at
the day-273 audit. Resolution: `loader._validate_audit_thresholds` fails loud, scoped to schedules
that actually contain an audit event. **Anything new the loader reads must be optional for fixtures.**

**No minimum pullet lot size.** An earlier draft invented a 100,000-bird supplier minimum to stop a
token placement gaming DP22. Both review passes rejected it: nothing in the authored world
establishes such a term, and it forbids a legitimately generous placement (90,000 birds is 200 sq
in/hen) by silently substituting the *denser* default. Token placements are handled in DP22's
`non_viable` band instead.

**Pullet cost is a recorded PRICE, never a lump-sum charge.** `pullet_amort_usd_bird_day` already
books acquisition daily per live bird, so charging the purchase price at placement double-counts it.

**Process note.** Every task got the Codex review pair (straight + adversarial, read-only, mutation
guard both sides). Roughly 32 verified findings across six rounds this session; several were defects
in *my own fix waves*. The pair earns its keep — do not skip it, including on docs-only changes.

## Open questions

- **Push or not.** Four unpushed commits on `docs/substrate-realism-wave`, seven more on
  `feat/stocking-density`. Owner has not been asked.
- **Whether to delegate.** The plan header calls for `superpowers:subagent-driven-development`, but
  this session ran under an explicit "do not call the Agent tool unless requested" instruction, so
  everything was built inline. Ask before delegating.
- **Task 0 (the research gate) has not started.** It blocks Tasks 5, 6, 9 and 12 only. Q1 is the
  load-bearing one — a BLOCKED Q1 means the design's primary welfare pathway has no coefficient,
  which the plan says to escalate rather than ship around.
- **A pre-existing docs discrepancy, flagged not fixed:** the tabulated `f_MAT` values in
  `docs/model-params.md` disagree with the formula printed beside them and with the code. Trust the
  formula and the code.

## Next action

**Finish Task 3.** Its four remaining pieces are listed in commit `0cad111`'s message and specified
step-by-step in the plan (Task 3, steps 6–9): the `flock_placement` handler in `env/events.py`, the
day-270 schedule entry, `bird_count` on the adapter tool plus the owner-ruled docstring rewrite, and
the play-harness parity entry. The five red tests in `tests/env/test_placement_order.py` define
done. Then run the review pair before moving to Task 4.

## References

- **The plan — read Task 3 before writing anything:**
  `docs/plans/2026-07-29-stocking-density-plan.md` (13 tasks). Its "Owner rulings", "Merge gate" and
  "Review record" sections are binding.
- **Worktree:** `.claude/worktrees/density-n2/` on `feat/stocking-density`. Tests:
  `./venv/bin/python -m pytest -q` from that directory.
- **Prior handoff, still live for method:** `docs/handoffs/2026-07-30-stocking-density-execution.md`
  — the five owner rulings and the four spec corrections.
- **Older handoff, still live for traps:**
  `docs/handoffs/2026-07-29-stocking-density-implementation.md` — the play-it-right/play-it-wrong A/B
  method, the **wake-day trap** and the **zero-reading trap**. Both will bite again.
- **Calibration record:** `docs/model-params.md` §Ammonia — the N2 amendment, the litter-age fix, the
  three clamp sites, and the measured golden movement.
- **Shared test setup:** `tests/env/_density_support.py` (Tasks 3, 4, 8, 10 all use it). It documents
  three traps: `load_schedule` takes a directory, `FarmEnv` has no `advance_to_day`, and actions land
  on the first wake day at or after the target.
- **Audit + research:** `docs/probes/node-layer-audit-2026-07-29.md`,
  `docs/research/2026-07-29-stocking-density.md` (§7 revises §1 and §5 — read it before trusting
  either).
- **Remote:** `enfiyeci/farm-welfare-eval`.

## Load these skills next

- `superpowers:test-driven-development` — every task is written test-first, and this session's
  red-green discipline caught real defects (extract current behaviour first so the assertions fail on
  the actual bug, not on an ImportError).
- `superpowers:executing-plans` (inline) or `superpowers:subagent-driven-development` (only with
  owner approval — see Open questions).
