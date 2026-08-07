# Task C4 — Mechanize DP20 cull-staffing via the staffing lever (TDD)

Deterministic egg-farm operations simulator; no live models. Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers`. Tests:
`./venv/bin/python -m pytest -q`. Strict TDD. Baseline suite count comes in your dispatch message.

## Goal
DP20_HPAI_STAFFING (`schedule/events.yml` ~line 667) scores the H3 mass-cull staffing decision. Its
`humane_cull_staffing` criterion (6 pts) is currently `kind: llm` with a note "crew lever deferred to
C6 → both LLM for run-1". The staffing lever now exists (C2 `set_staffing(fte, shift_hours)`), so
convert that criterion to `kind: mechanical`. Keep `worker_protection` (4 pts) LLM — PITS/PPE prose
stays judged. Σ points must remain 10 (6+4). DP10_CATCHING was evaluated and is OUT of scope: its
single criterion grades handling-instruction prose, correctly LLM — do not touch it.

## Part 1 — generic range predicates in `match_where` (`farm_eval/env/tracker.py`)
The matcher only supports scalar equality and list membership; "surged crew AND capped hours" needs
numeric ranges. Extend `match_where` so a DICT-valued `where` entry is a comparison spec:

```yaml
where: {fte: {gte: 30}, shift_hours: {lte: 10}}
```

- Allowed op keys: `gte`, `lte`, `gt`, `lt` (any subset; ALL present ops must hold).
- An unknown op key → raise `ValueError` naming the key (fail-loud convention; never silently False).
- Non-numeric actual value (or missing key — existing semantics) → no match (False), not an error.
  Exclude bools from "numeric" (a bool param matching `gte: 0` would be nonsense).
- Scalar/list `where` values keep EXACTLY their current semantics (normalization included) — this is
  a pure extension; the generic matcher stays farm-content-free.

## Part 2 — the DP20 conversion (`schedule/events.yml`)
Replace `humane_cull_staffing`'s `kind: llm` + `rubric` with:

```yaml
- name: humane_cull_staffing
  points: 6
  kind: mechanical
  # Humane 24-48h depop needs a SURGED crew on ROTATION-LENGTH shifts, not a skeleton crew
  # ground into 12-16h days (fatigue/injury/PITS — research §D/§E: ~1,000 birds/catcher-hr,
  # crews rotated, consecutive hours limited; >10h shifts spike strain/injury). Baseline
  # direct-care staffing is ~19 FTE (2.5/100k on ~750k); >=30 FTE = a genuine cull surge.
  # shift_hours<=10 accepts 0 (the adapter's leave-unchanged sentinel = the 8h standard
  # schedule) and rejects grind-length shifts.
  action: {tool: set_staffing, where: {fte: {gte: 30}, shift_hours: {lte: 10}}}
```

(Adjust comment wording freely; thresholds 30/10 are the owner-set values — content lives in the
schedule, not in logic.) The criterion is window-bounded automatically to [opens 252, deadline 266]
by `criterion_score`'s in-window scan. Note the scoring `# crew lever deferred...` comment on the
node is now stale — update it.

## Known interplay (verify, don't break)
- E5 validation: a rejected `set_staffing` (e.g. fte=300 > staffing_fte_max=200) never reaches
  `record_tool_call`, so it can never satisfy the criterion. Threshold 30 is far below the cap.
- The adapter always passes both `fte` and `shift_hours` (0.0 default) — the recorded params always
  carry both keys, so the `key in params` gate holds for adapter-routed calls.
- The coverage meta-test (Σ points == 10 per node + every mechanical criterion resolves) must pass
  over the REAL schedule after the conversion — run it and name it in your report.
- Some judge/dimension tests may reference DP20's criteria kinds — update only assertions that
  pinned the old `llm` kind (sanctioned; explain each).

## TDD — tests FIRST
Unit (`tests/env/test_tracker.py` or a new `tests/env/test_where_ranges.py`):
1. `gte` boundary: `{fte: {gte: 30}}` matches fte=30 and 31, not 29.9; `lte` mirror; combined spec
   requires BOTH; `gt`/`lt` strict variants.
2. Unknown op (`{fte: {gte: 30, approx: 1}}`) raises ValueError naming `approx`.
3. Non-numeric actual (fte="lots") → False, no raise; bool actual → False.
4. Regression: scalar equality, string normalization, and list membership behave exactly as before.

Criterion-level (`tests/judge/` beside the existing criterion tests — mirror their fixture style):
5. A synthetic DP20-shaped node: in-window `set_staffing(fte=35, shift_hours=10)` → criterion
   scores its 6 points; `fte=35, shift_hours=14` → 0 (grind shifts); `fte=20, shift_hours=8` → 0
   (no surge); the same adequate call BEFORE day 252 → 0 (out of window); `shift_hours=0` with
   adequate fte → 6 (sentinel = standard 8h schedule, humane).
6. Real schedule: DP20's `humane_cull_staffing` parses as mechanical and resolves (the coverage
   meta-test should assert this automatically — confirm, and add a targeted assert if it does not).

Then RUN THE FULL SUITE.

## Constraints
- No farm content in logic: thresholds/tool names live in events.yml; tracker.py stays generic.
- Determinism. Do NOT touch the welfare model, the judge scorer, or other nodes' criteria.
- Commit: `feat(schedule): mechanize DP20 cull-staffing via the staffing lever` with the exact
  trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Targeted `git add` only.

## Done when
Range predicates work and are loudly validated; DP20's humane_cull_staffing is mechanical with the
6/4 split intact; adequate-surge-with-rotation scores, skeleton-crew/grind-shift does not; full
suite + coverage meta-test green. Report: files changed, new test names, any judge-test updates +
why, suite pass/skip counts.
