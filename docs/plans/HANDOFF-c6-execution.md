# Handoff: Execute Phase C6 (env levers) for the farm-welfare eval

## Intent
Build Phase C6 — the environment levers that make several C5 welfare/integrity nodes score on
**objective game-state actions** instead of LLM prose, plus the run-infrastructure the pilot proved we
need. "Done" = Phases A, B, C, D of the plan implemented task-by-task with reviews, full suite green,
branch ready for the merge decision.

**The plan (read it first, it is the authority):** `docs/plans/2026-07-01-phase-c6-env-levers.md`
(in THIS worktree — it was copied onto this branch so you need nothing outside it).

## Where you are
- **Worktree:** `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers`, branch
  `feat/phase-c6-env-levers`, based on `feat/phase-c5-judge-v2` @ `a4b52d2` (C5 judge v2 complete +
  pilot hardening). Baseline suite: **461 passed, 1 skipped** (the skip is `test_rubric_sync` —
  gitignored `rubric.yml` absent in worktrees, benign; 2 third-party deprecation warnings from
  websockets/uvicorn are pre-existing and NOT yours to fix).
- **venv:** symlinked at `./venv` (do NOT create one). Run everything from the worktree root:
  `./venv/bin/python -m pytest -q`. The shell cwd resets between commands — prefix with
  `cd /Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers &&`.
- **SDD ledger:** `.superpowers/sdd/progress.md` in this worktree — the durable task record. Read it
  FIRST on any resume; append one line per completed task. Never re-dispatch a task it marks complete.
- **⚠️ Task A1 may already be done or in flight** (a prior session dispatched it). Before starting:
  `git log --oneline -3` — if a commit like `feat(env): set_egg_disposition — standing per-house egg
  channel allocation…` exists, A1 is done (review it per the process below, then continue with A2). If
  absent, dispatch A1 yourself using its brief:
  `/private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-farm-eval/838d0c05-89a9-4547-989c-8ee2a6c38413/scratchpad/c6/task-a1-brief.md`
  (if that scratch file is gone, the plan's Task A1 section + the "Decisions" below fully specify it).

## Decisions already taken (do not re-litigate)
- **Dispositions are STANDING per-house allocations** (day-forward until changed), not one-off events —
  that's what makes "discard through the withdrawal window" a real, reversible, profit-costing lever.
  Default channel `shell`; audit log `EnvState.egg_dispositions`; multipliers from pricing DATA, never
  hardcoded in logic.
- **Task C3 (staffing→welfare coupling) is a HEURISTIC, deliberately** — the research
  (`docs/research/2026-07-01-daily-labor-staffing.md`, in this worktree) states no published
  dose-response exists. Build it as ONE monotone adequacy factor hitting the report's anchors (full
  adequacy ≥2.5 FTE/100k; nonlinear degradation below ~2.0; floor-eggs → 10–15%, mortality toward the
  7.2%-vs-3.1% gap, footpad/NH₃ worsen; plateau above ~3). Document it as heuristic-grounded-in-the-report
  in `docs/model-params.md`. Do NOT invent per-channel curves beyond the anchors.
- **Phase D is not optional** — the pilot lost a 93%-complete paid episode to a process kill (no flush)
  and salvage-re-scoring saved two other runs. D1 per-beat checkpointing, D2 deterministic replay +
  partial scoring, D3 the mis-keyed displayed metric.
- **Bounded authority** and **no farm content hardcoded in logic** are project invariants (see
  CLAUDE.md + the plan's Global Constraints).

## Process (the project's discipline — follow it exactly)
1. **superpowers:subagent-driven-development**: fresh implementer subagent per task (hand it a task
   brief FILE in the scratchpad, never the whole plan), then a task-reviewer subagent (spec + quality,
   diff via the review-package script), then fix→re-review loops until clean.
2. **superpowers:test-driven-development** inside every implementer: failing test first, RED for the
   right reason, then GREEN, full suite green + pristine before commit.
3. **Codex adversarial review after each task** — do NOT use the codex:rescue skill (it misfires; see
   the user's memory). Run the CLI directly, read-only, in the background:
   `codex exec -s read-only --skip-git-repo-check -C <this worktree> -o <scratch-out.md> "<review prompt
   naming the commit range and the specific defect classes to hunt>"`
   Adjudicate its findings yourself (it has caught real bugs — NaN fail-loud gaps — and also mis-judged;
   verify before acting). Batch small Minors to the final fix wave; fix Critical/Important immediately.
4. **Commit trailer (exact):** `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Commit per task.
5. **End of branch:** final whole-branch review (most capable model, fresh subagent, review package over
   the full range `a4b52d2..HEAD`), one batched fix wave, then STOP — present the merge decision to the
   user (C5 must merge first; this branch then rebases/merges after it).

## Task order (from the plan; sizes are guidance)
A1 env disposition (may be done — see above) → A2 adapter tool + `all_tools()` registration (mirror an
existing action tool; it must route through `apply_action` so `state.actions` records it) → A3 convert
DP13/DP21/DPN scoring criteria in `schedule/events.yml` to mechanical `action:` matchers (VERIFY each
`where` against what the tool records — a wrong `where` silently scores 0; keep Σ points == 10; coverage
meta-test must stay green) → B1 `enabled_nodes` node-selection (ledger seeding + headline filter, fail
loud on unknown ids) → C1 labor cost line → C2 staffing lever → C3 coupling (anchors above) → C4
mechanize DP20 → D1 checkpointing → D2 replay/partial-scoring → D3 metric key.
Keep tasks sequential (shared files); parallelize only genuinely independent pairs (e.g. B1 vs C1) if
you're confident about file separation.

## Traps the C5 build already hit (don't repeat them)
- Implementer/reviewer agents racing in ONE worktree report garbled test counts — run the full suite
  YOURSELF after concurrent work settles.
- `git` in a shared checkout while another session is active = collisions. This worktree is yours alone;
  never run git in the main checkout or other worktrees.
- Judge/grader code: fail-loud belongs at CONFIG time; grader-output handling must degrade-and-note.
  (Already fixed in C5 — preserve the pattern in anything you touch.)
- Non-finite floats: `min/max` clamps turn NaN into the max bound. Every numeric helper rejects
  non-finite loudly. There are meta-tests for this; keep the discipline in new code.
- The real `schedule/events.yml` must PARSE after any schedule edit (`tests/env/test_real_schedule.py`)
  and every node's criteria must sum to 10 (`tests/env/test_node_scoring_coverage.py`).

## What NOT to do
- Do not touch `.claude/worktrees/c5-judge-v2` (pilot re-scoring may be running there), the `v2-docs`
  worktree, or the main checkout.
- Do not run real-model evals or spend API credit — C6 is build+test only (keyless `mockllm` covers the
  adapter tests).
- Do not merge or push without the user's explicit go-ahead.
- Do not expose ledger/scoring/inspected data through any agent-facing tool.

## Report cadence
Work continuously (no per-task check-ins). Checkpoint to the user at phase boundaries (A done, B done,
…) with: commits, suite count, review outcomes, and anything that changed the plan. BLOCKED or a real
plan contradiction → stop and ask.
