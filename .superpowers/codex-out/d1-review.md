**Findings**

**Critical** - `farm_eval/env/replay.py:38`, `farm_eval/env/replay.py:79`
Replay ignores `EnvState.reads`, but reads are state-bearing in this repo. `get_sensor()` and `read_flock_report()` append to `state.reads`, and `end_day()` calls `resolve_inspected()`, which mutates ledger entries based on those reads. A normal rejection-free run that only reads a relevant surface will have `ledger[].inspected=True` and non-empty `reads`; replaying from `actions` alone returns `reads=[]` and `inspected=False`. That violates the advertised bit-identical `EnvState` contract and changes score metadata recognition output. The new tests miss this because the “realistic” episode never performs read tools.

**Important** - `farm_eval/env/replay.py:66`, `farm_eval/env/replay.py:90`
`to_day < 0` is not guarded. Replay still builds/starts day 0, fires day-0 events, and applies day-0 actions before checking whether the target day is before the first beat. That contradicts “returned state is the last beat <= to_day”; for negative `to_day` there is no such beat, so this should fail loudly or define/clamp behavior. As written it returns a plausible state at day 0, which is already past the requested target.

**Notes**

I did not find a peek/advance disagreement: replay uses `next_beat(env.state.day_index, schedule.event_days(), episode_end_day)` exactly like `FarmEnv.end_day()`. Current action handlers also do not appear to mutate `rec.params` in place, and same-day action ordering matches the live solver’s “events for beat, then agent actions, then end_day” lifecycle.