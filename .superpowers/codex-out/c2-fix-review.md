Clean. I found no new issues in `edecae4`.

F1 is closed: `effective_fte_per_100k` and `effective_shift_hours` are computed once per simulated day at [integrate.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/model/integrate.py:51), before the per-house loop at line 65. They are still inside the elapsed-days loop, so multi-day depletion drift is preserved.

F2 is closed: the adapter docstring states `standard schedule: 8` at [controls.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/adapter/tools/controls.py:39), and the new test pins that text to `ModelParams().labor_hours_per_fte_day`.

F3 is closed: the new non-100k-bird test at [test_staffing_lever.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/env/test_staffing_lever.py:118) uses 250,000 birds, so the inverted formula would fail.

I could not run the focused tests because `pytest` is not installed in the active environment (`pytest: command not found`, `python3 -m pytest: No module named pytest`).