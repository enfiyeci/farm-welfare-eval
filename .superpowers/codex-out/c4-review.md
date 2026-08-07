**Findings**

Important — [farm_eval/env/tracker.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/tracker.py:88): unknown range-op validation is still short-circuited when the action omits that param. `key in params and _matches(...)` returns `False` before `_matches_range()` can raise, so `where: {shift_hours: {lte_: 10}}` silently never matches for an accepted lower-level `set_staffing` call that omits `shift_hours`. Key-present numeric and nonnumeric actuals do raise; missing-key does not. This violates the fail-loud requirement for schedule typos. The new test at [tests/env/test_tracker.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/env/test_tracker.py:139) only covers the key-present case.

Minor — [farm_eval/env/schedule_models.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/schedule_models.py:53): `ActionMatch.where` docs still say only list values are special and “any other value type keeps exact-equality matching.” That is now false for dict values, and this model is the schema-facing guidance for YAML authors.

**Checks Performed**

No current blast-radius collision found: the only dict-valued YAML `where` entries in `schedule/events.yml` and `tests/fixtures/**` are the new DP20 `fte`/`shift_hours` specs, and I found no list-valued `where` entry containing dicts.

DP20 window scoring uses inclusive bounds via `entry.opened_day <= rec.day <= entry.deadline_day`, so days 252 and 266 should count. The public adapter path always sends `shift_hours` with default `0.0`; the lower-level `Episode.apply_action` accepts omitted `shift_hours`.

Ran: `./venv/bin/python -m pytest -s --capture=no tests/env/test_tracker.py tests/judge/test_dp20_staffing_criterion.py -q` — passed, with only `.pytest_cache` write warnings due read-only sandbox.