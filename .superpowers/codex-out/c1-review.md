**Findings**

Minor: stale tracked doc references to the removed `labor_usd_doz` remain in [docs/plans/2026-06-27-phase-c1-financial-pnl.md](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/docs/plans/2026-06-27-phase-c1-financial-pnl.md:30). Same file still shows the old param/test/formula at lines 45, 70, 254, 277, and 314. Runtime code/tests are clean, but this violates the “no stragglers anywhere” invariant and could mislead future implementation from the plan doc.

No Critical or Important findings.

**Notes**

The actual implementation looks correct against the requested invariants: `cost_step` uses `bird_count / 100_000`, all four labor coefficients come from `ModelParams`, no caller wires staffing state yet, and I found no double-counted labor path. Default calibration is effectively unchanged: `$554.368` vs old `$555.0` per 100k birds at 90% lay, about `-0.11%`.

Verification run: `venv/bin/python -m pytest -q -s tests/env/model/test_labor_cost.py tests/env/model/test_economics_cost.py tests/env/model/test_economics_params.py -p no:cacheprovider` passed 13 tests.