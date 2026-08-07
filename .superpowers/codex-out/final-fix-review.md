**Finding**

- Low: [test_dp20_staffing_criterion.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/judge/test_dp20_staffing_criterion.py:134) is not a true pre-fix regression guard. It manually constructs the already-fixed `ActionRecord(... shift_hours: 14 ...)`, so it would pass before `1f357c5`. The env-level tests do catch the real bug, but this DP20 test does not prove the env recorded the sentinel correctly.

**Review Result**

Production code looks clean.

- `set_staffing` sentinel handling in [episode.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/episode.py:375) resolves recorded `shift_hours` via `economics.effective_shift_hours` only on the success path and does not mutate `world.staffing_shift_hours`.
- Rejection paths still return before `record_tool_call`.
- Param aliasing is safe: sentinel branch copies `params`, and `record_tool_call` copies again.
- I found no other consumer expecting literal recorded `shift_hours=0`; recorded actions are consumed by tracker/replay/scorer as copied params.
- Checkpoint `forced_advances` is written, loaded, defaults to `0` for old payloads, and does not alter atomic write, retention, or sample-id sanitization logic.
- `farm_eval/env` remains Inspect-free (`rg` found no `inspect_ai` imports).

**Verification**

- Full focused `pytest` could not run because the read-only sandbox has no usable temp directory for pytest capture/tmp fixtures.
- I ran write-free Python assertions for the staffing cases: prior 14 then omitted records 14, standing `None` records 8, explicit 9/12 record themselves, and rejection paths do not record.
- I also ran write-free DP20 scoring assertions for 9/12/14/8 recorded values.