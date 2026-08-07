**Findings**

Important: DP20 can score humane staffing while actual shifts remain >10h.  
[schedule/events.yml](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/schedule/events.yml:693) treats `shift_hours: 0` as satisfying `<=10`, but [episode.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/episode.py:375) defines `0` as “leave unchanged.” Failure scenario: agent previously sets `set_staffing(fte=20, shift_hours=14)`, then during DP20 calls `set_staffing(fte=35)` through the adapter, which records `shift_hours=0`; tracker awards the 6-point humane staffing criterion, while `world.staffing_shift_hours` remains `14.0`.

Important: E7 `forced_advances` is not checkpointed, so checkpoint resume can underreport run-health metadata.  
`forced_advances` lives on `EpisodeStore`, not `EnvState` ([context.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/adapter/context.py:49)); the solver increments it on forced backstop advances ([farm_solver.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/adapter/solver/farm_solver.py:86)), but checkpoints serialize only `env_state` plus `day/message_count` ([checkpoint.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/adapter/checkpoint.py:66)). Failure scenario: run has forced advances before crash, resumes from checkpoint, then scorer reports `forced_advances=0` or an undercount in metadata.

Minor: replay from actions+reads does not reproduce every `EnvState` field that checkpoints serialize when rejected attempts occurred.  
Rejected actions append `fallback:*` entries to `state.event_log` ([episode.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/episode.py:192)), but rejected attempts never enter `actions`, and replay explicitly drops those fallback entries ([replay.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/replay.py:17)). Failure scenario: invalid `set_staffing` attempt is present in checkpointed `EnvState.event_log`, but absent after replay reconstruction.

**No Breakage Found**

Staffing cost/coupling consistency: C1 cost and C3 adequacy both read the same once-per-day `fte_per_100k` and `hours_per_fte_day` hoisted at day start in `integrate.py`; per-house cost sums against day-start bird counts.

C3 clamps: mortality deaths are capped to live birds, excess mortality accrual is capped to available mortality fraction, floor-egg downgrade is clamped to `<=1.0`, and litter/footpad stay bounded. I did not find a crash path at `u=1`.

`match_where`: scalar and list matching still work, and dict range specs validate through all typed `ActionMatch` paths: root `any_of`, class `any_of/all_of`, ladder rungs, `root_cause`, `applies_if`, and criterion `action`.

Score surface: E7 counters stay in `Score.metadata`; `Score.value` remains float-only. Real schedule probe: 23 nodes, no missing scoring blocks, all point totals sum to 10, DP13/DPN/DP20/DP21 mechanical criteria resolve.

I could not run pytest because the sandbox has no usable temp directory for pytest capture, but I ran read-only Python probes for schedule loading, scoring invariants, `match_where`, and the DP20 sentinel scenario.