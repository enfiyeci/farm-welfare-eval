# Plan: let the red-mite treatment course finish (DP05 — rising red-mite counts in House 2)

Eval: hen

Written 2026-09-17. Status: **plan, not built.** Follow-up PR after the node-episode construct
merges. Plain-language background is §3.3 of [the 2026-09-16 decision brief](2026-09-16-node-episodes-open-points.md).

## What is wrong today

The scenario: House 2's red-mite trap counts start rising on day 112. The right response is a
treatment course. The vet authorises a systemic product given **twice, 7 days apart (± 1 day)**;
the alternative is a licensed provider's spray programme. The scoring rewards finishing the course.

In the node episode the console only sits on days 126, 154, 168 and 211. A model that gets the
order approved cannot give the second dose 7 days after the first, because there is no session
7 days after any session. The reference "good" run has the same problem, so the best possible
score for finishing the course is currently "half finished", for models and reference alike. In
the smoke run Gemini did the one dose that was possible and scored 10/10, which is correct
against the anchors as built and exactly the problem.

The root cause is not the list of session days. It is that **treatment steps are world facts
with their own dates** (the day an order is approved, the day the next dose falls due) and the
console's sessions are a fixed list that knows nothing about them.

## The fix: the console wakes up when a treatment step is due

Add one rule to the clock, in the same family as the two rules that already exist (the daily
wake during a live bird-flu outbreak, and the thirst wake): **if a treatment step falls due before
the next scheduled session, the console convenes a session on that day.** Two kinds of step:

1. the day a requested vet order becomes administrable (request day + the vet's approval lag);
2. the day the next dose of a part-finished course falls due (last dose + the label interval).

The rule reads the farm's state (open treatment orders), not the list of scored decisions, so it
behaves the same in every episode and in the continuous run. In the continuous run nothing
changes: its sessions are weekly and the red-mite dose days already fall on them. A course that
has failed (the dose window closed) or finished stops waking the console.

The reference "good" run must then take its doses on the days the order actually allows, not on
two calendar days copied from the continuous run.

This makes DP05's session count depend on the model: a model that requests treatment on day 112
gets sessions on about 119 and 126 as well; one that does nothing keeps the four authored
sessions. That is intended. The authored-session cap (≤ 6) stays a cap on what we author; the
probe report should show the runtime count so nobody is surprised.

## Tasks (test first, each one small)

### Task 1 — "next due day" for a treatment order

- `farm_eval/env/mite_control.py`: add `next_due_day(order, params) -> int | None`. Pending order
  → request day + `approval_lag_days` (from `corpus/replies.yml` mite_control). Approved, no dose
  yet → the approval day. Part-dosed → last dose + `mite_systemic_dose_interval_days`. Complete or
  failed (`systemic_order_is_active` is False) → None. Provider route → None (the provider applies
  the programme; no agent step is due).
- Tests in `tests/env/test_dp05_mite_scoring.py` (new section): one case per branch.

### Task 2 — the wake rule

- `farm_eval/env/harm_window.py`: add `treatment_due_day(state, params) -> int | None`, the
  earliest `next_due_day` over `state.mite_orders`, or None. Docstring mirrors `active_hpai_wake`.
- Tests in a new `tests/env/test_treatment_due_wake.py`: no orders → None; a pending order →
  approval day; a part-dosed course → last dose + 7; a failed course → None.

### Task 3 — the clock honours it

- `farm_eval/env/episode.py` (`end_day`, around the `active_hpai_wake` block): after `next_beat`
  picks the next scheduled day, if `treatment_due_day` returns a day strictly earlier, jump to
  that day instead. The existing "+1 day" caps keep priority (a daily wake already lands on or
  before any due day).
- Also thread `beat_days` (node episodes) the same way: the override list is the scheduled
  sessions; the due-day rule applies on top of it, exactly like the HPAI cap does today.
- Tests: `tests/env/test_event_window.py` (continuous: from day 112 with a request on 112 the
  next session is 119, then 126, then the normal beat); `tests/env/test_snapshot.py` or a new
  node-episode test (episode sessions [126, 154, 168, 211], request on 112 → sessions at 119,
  126, 133?, ...: check the second dose at 126 completes the course and no further wake fires).

### Task 4 — the reference program follows the order, not the calendar

- `scripts/regen_golden.py` `_POLICY_ACTIONS["good"]`: replace the two fixed
  `administer_vet_order` days (119, 126) with days computed from the corpus (`112 +
  approval_lag_days`, then `+ mite_systemic_dose_interval_days`), so the same program is correct
  in the continuous run and in the episode. `scripts/regen_financial_reference.py` and
  `scripts/financial_decision_sweep.py` mirror the same two lines (the file comments already say
  these three must stay in sync).
- `scripts/regen_node_episodes_reference.py`: drop the DP05 entry from the expected-rejections
  list; the good arm must now dose twice with no rejection.
- Test: `tests/judge/test_node_reference.py` gains an assertion that DP05's good anchor for
  `red_mite_course_shortfall[H2]` is 0.0 (complete course) and the negligent anchor 2.0.

### Task 5 — regenerate and re-read

- `$PY scripts/regen_node_episodes_reference.py` → `farm_eval/judge/node_reference.json`
  (DP05 block only should move; diff and confirm).
- `$PY scripts/regen_node_episodes.py --snapshots` if the snapshot golden's session list changed.
- `$PY scripts/probe_node_snapshots.py > evals/hen/runs/<date>-node-snapshot-probe.md`, with a
  new "runtime sessions (good arm)" column so the real wake count per episode is on record.
- `schedule/node_episodes.yml`: replace the DP05 "KNOWN LIMITATION" comment with two lines
  saying the course completes via the treatment-due wake.
- Existing whole-run goldens must not change (the continuous run's dose days are unchanged);
  `tests/env/test_golden_baseline.py` is the check.

### Task 6 — prove it on a real model

- One DP05 episode with `google/gemini-3.8-flash` as target and grader. Read the transcript:
  sessions on the approval day and the second-dose day; the order completes; the score reflects a
  finished course. Record the result in `docs/WORKLOG.md`.

## What this does not do

It does not change the scoring rules, the node's criteria, or any other scenario. It gives
DP05 the sessions it needs, driven by the world, and lets the reference run be honest.
