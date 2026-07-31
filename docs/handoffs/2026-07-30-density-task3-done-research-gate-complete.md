# Handoff: Task 3 done, research gate complete, plan rewritten — decisions are the bottleneck

## Intent

Make stocking density an emergent, *tempting* decision so the eval can separate *adequate*
welfare play from *excellent*. "Done" = a model that crowds H6 for margin scores measurably
worse than one that declines, **and the difference is carried by the world, not the judge**.

This session finished Task 3, ran the Task 0 research gate to completion, and rewrote the plan
where the evidence contradicted it. **No welfare-pathway code was written** — Tasks 5–12 are
still unbuilt.

## State

**Verified at handoff time, not from memory.**

Branch **`feat/stocking-density`** in worktree `.claude/worktrees/density-n2/`, branched from
`974d24b`. **20 commits, working tree clean.** Suite: **3 failed, 1265 passed, 1 skipped**.

The 3 failures are expected and sequenced to Task 13 behind the merge gate — `test_reference_runs_match_golden`, `test_baseline_checkpoints_match_golden`, and
`test_competent_anchor_reproduces_from_pipeline`. **Do not regenerate them early.** The third
joined the list this session because repopulating H6 moved the competent anchor
8,025,923 → 8,901,745; the plan already names that file (Task 13's regeneration list).

- **Task 3 — DONE**, `825a5ea` + three review-wave commits. Full Codex pair (straight +
  adversarial, read-only, mutation guard clean) run **three rounds to the cap**; 8 findings
  across the rounds, all verified against running code before fixing, all fixed. 22/22 tests in
  `tests/env/test_placement_order.py`.
- **Task 0 research gate — DONE**, six passes, 9 commits. All four questions answered.
- **Plan Tasks 5 and 6 — REWRITTEN** (`a9b5c8c`). Tasks 7, 9, 12 amended. Task 0 marked done;
  Tasks 9 and 12 gate markers flipped to open.
- **Tasks 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 — NOT STARTED.**

**Nothing has been pushed.** 20 commits here, plus 5 unpushed on `docs/substrate-realism-wave`
in the main checkout. `origin/main` has moved to `7be85e3` (PR #24, `farm_eval/play/session.py`)
— **verified no overlap**: this branch touches `farm_eval/play/ops.py` only, never `session.py`.

## Decisions & rationale

**The owner declined to answer the decision questions when asked mid-session** and said "research
deeper" instead. Decisions in `docs/plans/2026-07-30-density-wave-decision-register.md` are
**open, not settled**. Do not treat my recommendations there as rulings.

**Every research pass overturned something the previous one settled — including my own errors.**
Do not reintroduce these:

- **`k = 1.0` power law for density→ammonia is DEAD.** It was my own pass-1 recommendation. The
  mechanism is a litter water balance; ammonia's response to moisture is *linear* at 0.32 %/(g/kg)
  and all nonlinearity lives in the balance. Plan Tasks 5/6 now encode this.
- **Do not author a knee.** Kang measured flat 23 % litter moisture at 13/15/17 birds/m² then
  40.93 % at 19. That step must *emerge* from the water balance, not be hardcoded.
- **The Mendes chase is RETIRED.** They ran only two density levels; two points cannot distinguish
  a line from a step. Obtaining them could never have answered the shape question.
- **Do not cite Volkmann 2024 as evidence density doesn't matter.** I made that error and
  corrected it: its model tested litter type, flock age, season, flock size. **Density was never
  a predictor.** The study is silent on density.
- **Methionine is a near-null, not "contested."** I labelled it contested in pass 3 and disproved
  that in pass 5 with two full-text sources. The nutrition rung should be **fibre**.
- **Do not "fix" `play/ops.py` by casting `bird_count`.** The real parity break was
  `apply_action` truncating floats; that is fixed at the integrality check. Casting in ops.py
  would raise inside the play server where the world should reject in-world.
- **Event-identity fragility: flag, do not tail-append.** `fired_event_ids` stores list indices,
  so inserting events shifts them. Appending at the tail would protect only this one insertion and
  make the problem *look* solved. Pre-existing architecture; Tasks 4/11/12 all insert events too.
- **No minimum pullet lot size** (carried from the prior session, still live). Token placements
  are handled in DP22's `non_viable` band, not by inventing a supplier term.

**Two owner-supplied inputs this session:** the owner obtained four paywalled papers as PDFs
(in `~/Downloads`), which is what unlocked passes 5–6. `pdftotext` is installed and is how every
full read was done.

## Open questions

**15 decisions, all open**, in `docs/plans/2026-07-30-density-wave-decision-register.md` with
evidence-strength grades. The four that change what gets *built* next:

- **D7** — switch DP07's nutrition rung from methionine to fibre? (content change, affects Task 12)
- **D10** — does any corpus text imply 144 sq in/hen is generous? A real commercial aviary runs
  **194**. Needs an audit.
- **D11** — sub-band DP22's `compliant` (currently 144–500, so 90,000 and 125,000 birds score
  identically). **This shapes Task 4's signature.**
- **D15 / Task 5 Step 0** — author the litter area fraction. The sim implies UEP's 15 % minimum,
  putting us at 71.8 hens/m² of litter against a measured aviary's 21.4. **This is a prerequisite
  for Task 5 and a live realism question about the existing calibration**, not just this wave.

Also unresolved and owner-only: push or not, and whether to delegate (the plan calls for
`superpowers:subagent-driven-development`; this session ran inline under a standing instruction
not to use the Agent tool unrequested).

## Next action

**Ask the owner to rule on D7, D10, D11 and D15 in
`docs/plans/2026-07-30-density-wave-decision-register.md`** — those four gate what Tasks 4, 5 and
12 build. Then execute **Task 4 (DP22_PLACEMENT_DENSITY)** per the plan, which consumes exactly the
surfaces Task 3 built, followed by the Codex review pair.

## References

- **Plan:** `docs/plans/2026-07-29-stocking-density-plan.md` — Tasks 5/6 rewritten, 7/9/12 amended.
  Its "Owner rulings", "Merge gate" and "Review record" sections remain binding.
- **Decision register:** `docs/plans/2026-07-30-density-wave-decision-register.md` — 15 decisions,
  evidence + strength grades + options. Read the "PASS 5 SUPERSEDES" block first.
- **Research:** `docs/research/2026-07-30-density-coefficients.md` (six passes; read pass 6 first,
  it supersedes) and `docs/research/2026-07-29-stocking-density-sources.md` (S1–S28).
- **Worktree:** `.claude/worktrees/density-n2/` on `feat/stocking-density`. Tests:
  `./venv/bin/python -m pytest -q` from that directory.
- **Prior handoffs, still live for method and traps:**
  `docs/handoffs/2026-07-30-stocking-density-build-tasks1-3.md` (the wake-day trap, the
  zero-reading trap, the measure-don't-reason lesson),
  `docs/handoffs/2026-07-30-stocking-density-execution.md`.
- **Shared test setup:** `tests/env/_density_support.py` — documents three traps (`load_schedule`
  takes a directory; `FarmEnv` has no `advance_to_day`; actions land on the first wake day at or
  after the target).
- **Calibration record:** `docs/model-params.md` §Ammonia — the N2 amendment, litter-age fix, and
  the **three clamp sites whose order is load-bearing**.
- **Remote:** `enfiyeci/farm-welfare-eval`. `origin/main` at `7be85e3`.

## Load these skills next

- `superpowers:test-driven-development` — every task is written test-first, and this session's
  red-green discipline caught real defects (five of the eight review findings were reproduced as
  failing tests before being fixed).
- `superpowers:executing-plans` (inline) or `superpowers:subagent-driven-development` (only with
  owner approval — see Open questions).
