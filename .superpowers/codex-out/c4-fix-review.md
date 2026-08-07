Clean: no findings in `1f1810a`.

Verified:
- `ActionMatch` parse-time validator rejects `{}`, `{lte_: 10}`, and bool bounds, with errors naming the `where` key and op where relevant: [schedule_models.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/schedule_models.py:78).
- Scalar, string, list, `transient_before`, and valid range forms still parse.
- The real `schedule/events.yml` parses: 23 decision points, 112 events.
- Nested schema paths are covered because `Signature.any_of`, `ClassMatch.any_of/all_of`, `Rung.match`, `Signature.root_cause`, `Applicability.action`, and `Criterion.action` all type through `ActionMatch`: [schedule_models.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/schedule_models.py:122).
- Import direction is `tracker -> schedule_models`; no circular import observed. The drift guard imports cleanly: [tracker.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/tracker.py:21).

I could not run pytest because the repo `.venv` does not have `pytest` installed, but I ran focused inline validation/import probes through `.venv/bin/python`.