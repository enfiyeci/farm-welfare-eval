**Findings**

Important: [farm_eval/env/episode.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/episode.py:398) changes the complex path for non-current periods. `generate_cop_report(period="2024-01")` previously returned the cumulative complex P&L with `period: "2024-01"`; now the top-level guard returns `available: false` with no P&L fields. That contradicts “complex path unchanged” and can break existing complex-report callers.

Important: [farm_eval/env/episode.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/episode.py:446) hardcodes the corporate target as `0.955`. That is farm-specific business content in logic. If the corpus/world target changes from -4.5%, `vs_target` silently reports stale arithmetic. Lay onset is correctly sourced from `self.params.breed_age_wk[0]`.

Important: `tests/env/test_cop_per_house.py` is untracked. `git --no-pager diff HEAD --stat` reports only:

```text
farm_eval/env/episode.py | 81 +++++++++++++++++++++++++++++++++++++++++++++++-
```

So the E3 test coverage is not actually in the tracked diff as-is. `git status --short` shows `?? tests/env/test_cop_per_house.py`.

**Clean Checks**

I did not find a per-house numeric fabrication bug in the main compute branch. COP uses house bird count, age via `flock_age_weeks`, `production_step(age, params)`, current market ration/fuel, and `economics.cost_step`. `feed_cents_doz + overhead_cents_doz` reconciles to `cop_cents_doz` before normal rounding. Empty, pre-lay, unknown-house, and non-current-period paths avoid reporting `cop_cents_doz`.

Determinism looks clean: no wall-clock or random in this method; `current_date()` is state-derived.

I could not run pytest normally because the sandbox has no writable temp directory for pytest capture. A direct Python sanity check did run and confirmed per-house variance plus the complex non-current-period regression above.