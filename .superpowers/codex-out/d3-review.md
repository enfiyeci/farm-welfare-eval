Found one minor issue.

- **Minor** [farm_eval/judge/scorer.py:632](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:632): the metrics declaration is `metrics=[{...}]`, not the claimed bare dict form. In pinned `inspect_ai 0.3.241`, list-form metrics are split into simple metrics plus dict metrics; with no simple metrics, it still emits an extra empty result named `welfare_judge` before the expanded per-key results. I verified this locally via `eval_results`: `welfare_headline` is correct and `*` dedupes, but the log contains an empty `welfare_judge [] {}` result. This is display/log clutter, not a numeric scoring bug.

No Critical or Important findings.

Checks confirmed:
- `inspect_ai` does support `*` glob metric keys and dedupes by metric name in `resolve_glob_metric_keys`.
- The wildcarded `Score.value` keys are always present floats: dimensions, `welfare_headline`, `diagnostic_composite`, `welfare_state`, `tripwires_observed`.
- Fix 1 is display-only; headline computation still comes from `welfare_headline(node_scores)`.
- `inspect_surface="any"` still enforces `[opened_day, deadline_day]`.
- Empty list validation and `extra="forbid"` both hold.
- `inspect_surface=None` preserves the old single-house derivation path.
- `entry.inspected` remains diagnostic; scoring only uses ledger status/outcome/actions/channels, not inspected.
- Tracker logic stays generic; DP03 farm content is only in `schedule/events.yml`.

Verification run: focused tests passed with pytest capture disabled due read-only temp constraints:
`tests/judge/test_scorer_metrics.py tests/env/test_inspected_flag.py tests/env/test_real_schedule.py`  
`git diff --check 90a1dcc..f4bbcb2` also passed.