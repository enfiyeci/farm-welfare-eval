**Findings**

Critical - `farm_eval/env/episode.py:49`, `farm_eval/env/episode.py:206`, `farm_eval/env/episode.py:249`  
Unknown-house rejection is incomplete. `place_feed_order` accepts `house_id` via the adapter (`farm_eval/adapter/tools/orders.py:21`) but is omitted from `_HOUSE_KEYED_TOOLS`, so `place_feed_order({"house_id": "H_DOESNT_EXIST", "quantity_tons": 20, ...})` can book inventory and reach `record_tool_call`. Also, the guard only rejects truthy IDs, so `adjust_setpoint({"house_id": "", ...})` skips rejection and mutates `world.setpoints[""]` at `episode.py:233`. Both violate unknown-house rejection, no mutation on invalid action, and no credit-before-rejection invariants.

Important - `farm_eval/env/episode.py:225`, `farm_eval/env/episode.py:236`  
`float(...)` conversion happens outside the rejection path. Non-finite numeric values are handled, but non-numeric strings like `"abc"` raise `ValueError` before `_reject_action`, so there is no `ok=False`, no `fallback:*` event, and the simulator can throw instead of returning an in-world rejection. This affects both `adjust_setpoint.value` and `place_feed_order.quantity_tons`.

Minor - `tests/env/test_action_validation.py:33`, `tests/env/test_action_validation.py:71`, `tests/env/test_action_validation.py:159`  
The new tests mostly assert `ok=False` and sometimes no domain mutation, but they do not assert that rejection paths append a `fallback:*` event or leave `state.actions` unchanged. `addressed_dps == []` is not equivalent to “did not call `record_tool_call`”, since `record_tool_call` appends an action before matching decisions (`farm_eval/env/tracker.py:160`). A regression that silently records rejected actions but matches no DP would pass many of these tests.

**Checks**

I did not find legitimate schedule/test values that the new bounds would reject: the real schedule’s `feed_ration=0` remains within bounds, `belt_interval_days` usages are 1-7, and existing ventilation/temperature/feed quantities are within the new limits. I could not run pytest in this shell because bare `python3` lacks installed project deps (`pydantic`).