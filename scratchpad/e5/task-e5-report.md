# Task E5 report — action-tool input validation with in-world rejections

## Status: DONE

Commit: `8a83d40` on `feat/phase-c6-env-levers`
(`feat(env): E5 action-tool input validation with in-world rejections`)

## Coordinator ruling incorporated

During pre-implementation research I found the brief's 5-system `setpoint_bounds` enum omitted
`belt_interval_days` — a real, live `adjust_setpoint` system (the calibrated footpad/litter
lever: `integrate.py:103` reads it from `world.setpoints`; `layers/litter.py` and the
`litter_moisture_*` params document it as agent-controllable; `tests/env/model/
test_substrate_properties.py:56` exercises it through `apply_action`). Implementing the brief
verbatim would have silently killed that scored welfare lever in production. I blocked and asked;
the coordinator ruled: add `belt_interval_days: (1.0, 14.0)` as a 6th entry (sub-1 is meaningless
because integrate.py floors via `max(1, int(...))` — reject loudly rather than clamp; 1–7 d is
the tested/operational range, 14 is generous headroom), plus a regression test (value=3 ok,
value=0/100 rejected). Everything else per the brief unchanged.

## Files changed

- `farm_eval/env/model/params.py` — new params (documented like the neighbors):
  - `feed_order_max_tons: float = 2000.0` (sanity ceiling; ~90 t/day complex consumption,
    catches the 124000-headcount-as-tonnage class of mistake)
  - `setpoint_bounds: dict[str, tuple[float, float]]` (pydantic `Field(default_factory=...)`):
    ventilation (0,5) · temperature (0,45) · lighting_lux (0,200) · lighting_hours (0,24) ·
    feed_ration (0,5) · belt_interval_days (1,14). Also added `Field` to the pydantic import.
- `farm_eval/env/episode.py`:
  - `import math`.
  - New module constant `_HOUSE_KEYED_TOOLS = {adjust_setpoint, schedule_maintenance,
    schedule_vet_visit, log_treatment}` (with a comment noting `set_egg_disposition`
    deliberately excluded — it validates its own house).
  - New private helper `FarmEnv._reject_action(fallback_type, tool, params, detail)` — the
    single rejection path: appends the `fallback:*` event-log entry (same shape as the existing
    pattern) and returns `ActionResult(ok=False, detail=..., addressed_dps=[])` WITHOUT
    `record_tool_call`. The pre-existing `fallback:unknown_tool` branch was refactored through
    it (byte-identical entry + detail; pure dedup).
  - `apply_action`:
    - Early unknown-house guard for the four house-keyed tools: present, non-empty `house_id`
      not in `state.welfare.houses` → `fallback:unknown_house`,
      `"No such house {house_id!r} at this complex."` Empty/omitted stays allowed.
    - `adjust_setpoint`: system-enum check (`fallback:unknown_setpoint_system`, detail lists the
      valid systems) then finite+range check (`fallback:setpoint_out_of_range`, detail names the
      range) BEFORE mutating the setpoint. Bounds read from `self.params.setpoint_bounds` (no
      literals in logic).
    - `place_feed_order`: `not math.isfinite(qty) or qty > self.params.feed_order_max_tons` →
      `fallback:feed_order_over_capacity`, "Supplier declines: order of {qty:g} t exceeds the
      complex's on-site storage capacity (max {cap:g} t per order). Confirm the quantity — did
      you mean tons?" — BEFORE booking inventory. The `qty <= 0` branch (spec-only orders,
      books nothing, returns ok) is untouched.
- `tests/env/test_action_validation.py` — NEW, 19 tests.

## New test names (all in tests/env/test_action_validation.py)

1. `test_place_feed_order_over_cap_is_rejected_and_books_no_inventory` (124000 t; asserts
   `feed_inventory_tons` unchanged + `addressed_dps == []`)
2. `test_place_feed_order_normal_quantity_is_accepted` (20 t; inventory grows)
3. `test_place_feed_order_non_finite_quantity_is_rejected` (inf; books nothing)
4. `test_place_feed_order_spec_only_zero_quantity_still_ok` (ration="LP2", qty=0 — DP04/DP08/
   DPD/DPE crediting guard)
5. `test_adjust_setpoint_out_of_range_value_is_rejected` (temperature 999; message names range)
6. `test_adjust_setpoint_valid_value_is_accepted` (temperature 21; setpoint actually written)
7. `test_adjust_setpoint_rejected_value_does_not_mutate_setpoint`
8. `test_adjust_setpoint_unknown_system_is_rejected` ("frobnicate")
9. `test_adjust_setpoint_feed_ration_zero_is_valid_tripwire_regression_guard` (DP08 tripwire)
10. `test_adjust_setpoint_non_finite_value_is_rejected` (NaN)
11. `test_adjust_setpoint_belt_interval_days_valid_value_is_accepted` (value=3; coordinator's
    regression guard for the calibrated footpad lever)
12. `test_adjust_setpoint_belt_interval_days_out_of_range_is_rejected` (0 and 100; in-range
    message)
13. `test_schedule_maintenance_unknown_house_is_rejected` ("no such house" message)
14. `test_schedule_maintenance_real_house_is_accepted`
15. `test_schedule_maintenance_omitted_house_still_allowed` (optional-house guard)
16. `test_adjust_setpoint_unknown_house_is_rejected`
17. `test_schedule_vet_visit_unknown_house_is_rejected`
18. `test_log_treatment_unknown_house_is_rejected`
19. `test_rejected_setpoint_matching_a_signature_credits_no_decision` (out-of-range value on
    the fixture DP's exact house/system; the pre-implementation failing run showed the old
    behavior crediting `DP_PLACEHOLDER_1` — now `ok=False`, `addressed_dps == []`)

## TDD evidence

Tests written first; 12 of 19 failed for exactly the right reason (`ok=True` under the old
silently-accept behavior — e.g. `ActionResult(ok=True, ..., addressed_dps=['DP_PLACEHOLDER_1'])`
for the signature-crediting test). The 7 that passed pre-implementation are the accept-side
regression guards (valid values must be accepted before AND after; they pin against
over-rejection). Then implemented; all 19 green.

## Existing tests changed

**None.** Full suite green with zero modifications to existing tests. Verified the risk areas:
- `tests/env/model/test_substrate_properties.py` fuzz values (ventilation 0–4, temperature
  12–32, belt 1–7) are all inside the generous bounds.
- Real `schedule/events.yml`: all `adjust_setpoint` signatures use recognized systems
  (ventilation/temperature/feed_ration); the only pinned value is `feed_ration: 0` (the DP08
  tripwire — valid, bounds include 0). All signature `house_id`s (H1–H6) exist in
  `corpus/company.yml`. No `place_feed_order` signature pins a `quantity_tons` (all spec-based:
  ration/additive/target/genetics). No scored decision becomes unreachable.

## Full-suite counts

- Baseline (confirmed before any change): **551 passed, 1 skipped**
- After E5: **570 passed, 1 skipped** (= 551 + 19 new; zero regressions)

## Self-review notes

- NaN is double-guarded on setpoints: `not lo <= value <= hi` is already True for NaN
  (comparisons are False), and the explicit `math.isfinite` states the intent per the brief;
  ±inf fall out of range either way. On feed orders the `isfinite` check is load-bearing
  (NaN > cap is False).
- Pre-existing crash behavior deliberately preserved: `float(params["value"])` on a non-numeric
  value and `params["house_id"]` KeyError on a missing adjust_setpoint house raise exactly as
  before (not in E5 scope; validation here covers range/enum/existence, per the brief).
- The `fallback:unknown_tool` refactor through `_reject_action` is a pure dedup — same event-log
  entry shape, same detail string.
- The adjust_setpoint success detail keeps the original raw-param formatting (`set to 21`, not
  `21.0`) so no message drift for existing consumers.
- Rejection paths all `return` before `record_tool_call`; the unknown-house guard runs before
  ANY side effect (including the `_TRACE_TOOLS` event-log trace and log_treatment's mite/drug
  state mutations, which previously no-op'd on unknown houses but still logged + credited).
- CRITICAL TRAPS all honored: `quantity_tons <= 0` never rejected (trap 1); `feed_ration=0`
  valid (trap 2, test 9); bounds generous (trap 3 — the fuzz suite's whole operational envelope
  passes untouched).

---

# E5 review-fix follow-up (commit `01cd334`)

## Status: DONE

Codex adversarial review of `8a83d40` found F1–F4; all fixed via strict TDD (the 5 new
behavior tests were written first and failed for the right reasons: raw KeyError, raw
ValueError, and silently-accepted `ok=True`).

## What changed (farm_eval/env/episode.py)

- **F1 (Critical):** `"place_feed_order"` added to `_HOUSE_KEYED_TOOLS` — its adapter
  (farm_eval/adapter/tools/orders.py) exposes an optional `house_id`, so
  `place_feed_order(house_id="H_TYPO", quantity_tons=20)` used to book inventory and reach
  `record_tool_call`. The shared guard only fires on a present, non-empty, unknown house, so
  spec-only DP04/DP08/DPD/DPE orders (no house) keep crediting untouched. Verified
  production-safe: the real schedule's `place_feed_order` signatures that use `house_id` pin
  `H1`, which exists in `corpus/company.yml`.
- **F2 (Critical):** `adjust_setpoint` now requires a present, non-empty `house_id`. Empty
  used to mutate phantom state `world.setpoints[""]`; missing raised a raw KeyError. Both now
  get the in-world rejection `"Controller rejects setpoint change: no house specified."` via a
  dedicated `fallback:missing_house` entry (chose the dedicated id over reusing
  `fallback:unknown_house` — "no house given" and "nonexistent house named" are different
  analysis buckets). The complex-wide tools (schedule_maintenance / schedule_vet_visit /
  log_treatment) keep empty/omitted allowed.
- **F3 (Important):** non-numeric coercion. `float(params["value"])` and
  `float(params.get("quantity_tons", 0.0))` are wrapped in `try/except (TypeError, ValueError)`
  → same in-world rejection path. Chose to REUSE the existing fallback ids
  (`fallback:setpoint_out_of_range` / `fallback:feed_order_over_capacity`) — coordinator's
  first-offered option; the event-log entry carries the raw params so the cases are
  distinguishable, and the detail messages are distinct ("not a numeric value" / "not a valid
  tonnage").
- **F4 (Minor), tests only:** every rejection test now routes through a `_apply_rejected`
  helper that asserts the FULL rejection contract: `ok is False`, `addressed_dps == []`,
  `len(env.state.actions)` did not grow (direct proof `record_tool_call` never ran), and a
  `fallback:*` entry was appended to the event log. The loose
  `"capacity" in detail or "ton" in detail` assertion tightened to `and`.

## New tests (tests/env/test_action_validation.py; now 25 total)

1. `test_place_feed_order_unknown_house_is_rejected_and_books_no_inventory` (F1)
2. `test_place_feed_order_known_house_is_accepted` (F1 accept-side guard)
3. `test_adjust_setpoint_empty_house_is_rejected_without_phantom_state` (F2; asserts
   `"" not in world.setpoints`)
4. `test_adjust_setpoint_missing_house_is_rejected_not_keyerror` (F2)
5. `test_adjust_setpoint_non_numeric_value_is_rejected` (F3; "abc"; no setpoint mutation)
6. `test_place_feed_order_non_numeric_quantity_is_rejected` (F3; "abc"; books nothing)

Plus the F4 strengthening applied across all 13 pre-existing rejection tests via
`_apply_rejected`.

## Suite counts

- Before follow-up: 570 passed, 1 skipped
- After follow-up: **576 passed, 1 skipped** (= 570 + 6 new; zero existing tests changed)

## Self-review notes (follow-up)

- `float(None)` → TypeError → caught (adapter can't send None past `_params`, but direct
  callers can).
- A completely missing `"value"` key on adjust_setpoint still raises KeyError — outside F3's
  scope (value is a required adapter arg); flagged here for completeness.
- The F2 guard runs INSIDE the adjust_setpoint branch (after the shared unknown-house guard),
  so the complex-wide tools' optional-house semantics are untouched
  (`test_schedule_maintenance_omitted_house_still_allowed` still green).
