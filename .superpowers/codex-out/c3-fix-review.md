Findings:

- **Low** [tests/env/model/test_staffing_coupling.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/env/model/test_staffing_coupling.py:204): stale docstring still uses the old `staffing_belt_lag_max=2.0` math: `3*(1+0.5*2)=6 -> equilibrium moisture 40%`. With the new default `3.0`, this case is `eff=7.5 -> equilibrium 47.5%`. The assertions are qualitative and still pass conceptually, but the docstring fails the “consistent everywhere” check.

Notes:

- The new default is consistent in code and primary docs: [params.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/model/params.py:267) is `3.0`, and [docs/model-params.md](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/docs/model-params.md:199) documents `3.0` with correct default-belt math.
- The daily-belt corner is not float-sensitive under current equations: `belt=1, u=1 -> eff=4 -> eq=30`, and finite integration approaches 30 from below (`29.99999999294492` after 200d), so footpad remains zero. It is parameter-threshold brittle by design: tiny changes to the litter floor/slope, `fpd_moisture_ref`, or lag max can flip it.
- I did not find other test magnitude assertions depending on the old `2.0`; the old value appears only in the stale docstring.
- No remaining fabricated research quotes found in the touched files. The remaining quoted research snippets are traceable to `docs/research/2026-07-01-daily-labor-staffing.md`; a couple use ellipsis/bracket or dash normalization rather than byte-for-byte quoting.

Could not run pytest fully: the read-only sandbox has no writable temp dir for pytest capture. I verified the key calibration values with direct imports.