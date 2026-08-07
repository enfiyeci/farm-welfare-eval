Clean. No findings in commit `813b4de`.

Verified against the `venv` symlink’s `inspect_ai 0.3.241`:

- Bare `metrics={...}` is accepted by `scorer()` and registers as a plain `dict`.
- In `compute_eval_scores`, bare mapping routes only to `scorers_from_metric_dict`; the old `metrics=[{...}]` path first calls `scorer_for_metrics([])`, which emits `EvalScore(name="welfare_judge", metrics={})`.
- Direct branch check showed:
  - bare form: `welfare_headline`, `a`, `b`
  - old list form: empty `welfare_judge` plus `welfare_headline`, `a`, `b`
- `welfare_headline` mean remains `7.0` in both forms, so this is display/result-shaping only.
- The code change is limited to the decorator metadata at [farm_eval/judge/scorer.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:632); the score value assembly at [farm_eval/judge/scorer.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:743) is unchanged.
- The new assertions at [tests/adapter/test_task.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/adapter/test_task.py:95) would fail on the old list form because it produces `welfare_judge {}`.

Test note: `tests/judge/test_scorer_metrics.py` passed under the attempted pytest run, but the adapter smoke test could not complete in this read-only sandbox because Inspect tried to write `~/Library/Application Support/inspect_ai/traces/trace-*.log`. I verified the affected Inspect result path directly instead.