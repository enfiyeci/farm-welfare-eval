**Findings**

Important: [farm_task.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/farm_task.py:36) collapses `enabled_nodes: []` to `None` because it uses `cfg.get("enabled_nodes")`. Failing input: YAML/config with `enabled_nodes: []`. Through `farm_task`, that silently becomes “all nodes enabled,” while direct `FarmEnv(..., enabled_nodes=[])` becomes `frozenset()` and seeds an empty ledger, later causing `welfare_headline` to raise at [headline.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/headline.py:45). This split is a footgun. If empty selection is unsupported, reject it loudly; if supported, preserve `[]` instead of treating it as `None`.

Minor: [test_node_selection.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/env/test_node_selection.py:68) only asserts `set(scores).issubset(set(enabled))`. That would pass if no enabled nodes scored at all. It should assert the expected scored ids exactly, assuming `DP01_AMMONIA_VENT` and `DP16_FOOTPAD` are intended to score under the fake grader. The exact ledger subset test at line 31 is good.

**Checked Clean**

Both `open_due_decision_points` call sites are updated: [episode.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/episode.py:133) and [episode.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/episode.py:157).

No shared schedule mutation found. `load_resources` still caches the full `(corpus, schedule)` at [context.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/adapter/context.py:55), and filtering is a skip in the seeding loop at [events.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/events.py:33).

Unknown ids fail loud against actual schedule DP ids at [episode.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/episode.py:90).

`enabled_nodes=None` preserves prior behavior: `open_due_decision_points` only filters when `enabled_nodes is not None`.

Subset ledgers do not break the tracker/scorer paths inspected. `record_tool_call`, `resolve_inspected`, and `evaluate_due_state_bands` iterate `state.ledger`; schedule is only used as a lookup. `window_from` is resolved from the full schedule loaded independently by the scorer at [scorer.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:640) and [node_scores.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/node_scores.py:161).

Back-compat looks fine: new parameters are added at the end with defaults.

I could not execute tests: `pytest` was not on PATH, and `./venv/bin/pytest` failed because the read-only sandbox has no usable writable temp directory for pytest capture.