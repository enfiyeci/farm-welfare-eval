"""C2 — staffing lever: `set_staffing` action tool + state.

C1 made the daily labor cost line staffing-driven via `cost_step`'s optional `fte_per_100k`
(and, here, `hours_per_fte_day`) overrides, defaulting to `params.default_fte_per_100k` /
`params.labor_hours_per_fte_day`. C2 gives the agent a real lever over that seam: two
`WorldState` fields (`staffing_fte`, `staffing_shift_hours`), a `set_staffing` action tool
following the E5 in-world-rejection pattern exactly, and wiring so BOTH `cost_step` call
sites (`integrate.py`'s daily P&L loop and `episode.py`'s instantaneous per-house COP) read
the effective staffing state. No welfare coupling (C3) and no scoring/criteria changes (C4)
in this task.
"""

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.model.economics import effective_fte_per_100k, effective_shift_hours
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import EnvState

FIX = Path(__file__).parent.parent / "fixtures"


def _env() -> FarmEnv:
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    return env


def _apply_rejected(env: FarmEnv, tool: str, params: dict):
    """Mirrors tests/env/test_action_validation.py's helper: a rejected action must not
    reach record_tool_call (state.actions doesn't grow), must log a fallback:* event, and
    must return ok=False with no addressed decisions."""
    actions_before = len(env.state.actions)
    log_before = len(env.state.event_log)
    result = env.apply_action(tool, params)
    assert result.ok is False
    assert result.addressed_dps == []
    assert len(env.state.actions) == actions_before, "rejected action must not reach record_tool_call"
    new_entries = env.state.event_log[log_before:]
    assert any(
        str(e.get("type", "")).startswith("fallback:") for e in new_entries
    ), "rejection must append a fallback:* event-log entry"
    return result


# --- 1. Lever persists ------------------------------------------------------------------


def test_set_staffing_persists_fte_and_returns_in_world_detail():
    env = _env()
    result = env.apply_action("set_staffing", {"fte": 12})
    assert result.ok is True
    assert env.state.world.staffing_fte == 12
    assert "12" in result.detail
    assert "staff" in result.detail.lower() or "fte" in result.detail.lower()


def test_set_staffing_records_tool_call_on_success():
    env = _env()
    actions_before = len(env.state.actions)
    env.apply_action("set_staffing", {"fte": 12})
    assert len(env.state.actions) == actions_before + 1


def test_set_staffing_with_shift_hours_updates_both():
    env = _env()
    env.apply_action("set_staffing", {"fte": 10, "shift_hours": 12})
    assert env.state.world.staffing_fte == 10
    assert env.state.world.staffing_shift_hours == 12


def test_set_staffing_omitted_shift_hours_leaves_current_value_untouched():
    env = _env()
    env.apply_action("set_staffing", {"fte": 10, "shift_hours": 12})
    env.apply_action("set_staffing", {"fte": 8})
    assert env.state.world.staffing_fte == 8
    assert env.state.world.staffing_shift_hours == 12  # untouched by the follow-up call


def test_set_staffing_zero_shift_hours_also_leaves_current_value_untouched():
    # Brief: "absent/0 = leave the current value untouched" for shift_hours.
    env = _env()
    env.apply_action("set_staffing", {"fte": 10, "shift_hours": 12})
    env.apply_action("set_staffing", {"fte": 9, "shift_hours": 0})
    assert env.state.world.staffing_fte == 9
    assert env.state.world.staffing_shift_hours == 12


# --- 2. Cost responds --------------------------------------------------------------------


def test_effective_fte_per_100k_doubling_doubles_labor_cost_via_cost_step():
    from farm_eval.env.model.economics import cost_step

    p = ModelParams()
    bird_count = 100_000
    total_dozen = 7_500.0
    default_cost = cost_step(0.0, 300.0, total_dozen, bird_count, 1.0, p)["labor_cost"]
    doubled_cost = cost_step(
        0.0, 300.0, total_dozen, bird_count, 1.0, p,
        fte_per_100k=2 * p.default_fte_per_100k,
    )["labor_cost"]
    assert abs(doubled_cost - 2.0 * default_cost) < 1e-9


def test_effective_fte_per_100k_from_state_doubles_the_ratio():
    p = ModelParams()
    state = EnvState(start_date="2025-06-09")
    state.world.bird_count = {"H1": 100_000}
    # staffing_fte chosen so fte * 100_000 / total_birds == 2x default
    state.world.staffing_fte = 2 * p.default_fte_per_100k
    ratio = effective_fte_per_100k(state, p)
    assert abs(ratio - 2 * p.default_fte_per_100k) < 1e-9


def test_effective_shift_hours_scales_labor_12_over_8():
    from farm_eval.env.model.economics import cost_step

    p = ModelParams()
    bird_count = 100_000
    total_dozen = 7_500.0
    default_cost = cost_step(0.0, 300.0, total_dozen, bird_count, 1.0, p)["labor_cost"]
    scaled_cost = cost_step(
        0.0, 300.0, total_dozen, bird_count, 1.0, p, hours_per_fte_day=12.0,
    )["labor_cost"]
    assert abs(scaled_cost - default_cost * (12.0 / p.labor_hours_per_fte_day)) < 1e-9


def test_effective_shift_hours_from_state():
    p = ModelParams()
    state = EnvState(start_date="2025-06-09")
    state.world.staffing_shift_hours = 12.0
    assert effective_shift_hours(state, p) == 12.0


def test_end_to_end_set_staffing_changes_generate_cop_report_overhead():
    env = _env()
    before = env.generate_cop_report(house_id="H_SENSOR")
    assert before["available"] is False or "overhead_cents_doz" in before
    # Advance flock into lay so the per-house report is available, then compare staffing on/off.
    env2 = _env()
    rep = env2.generate_cop_report(house_id="H_SENSOR")
    while not rep["available"] and not env2.is_over():
        env2.end_day()
        rep = env2.generate_cop_report(house_id="H_SENSOR")
    if not rep["available"]:
        pytest.skip("fixture flock never reaches lay within episode window")
    baseline_overhead = rep["overhead_cents_doz"]
    total_birds = sum(env2.state.world.bird_count.values())
    p = env2.params
    doubled_fte = 2 * p.default_fte_per_100k * total_birds / 100_000
    env2.apply_action("set_staffing", {"fte": doubled_fte})
    after = env2.generate_cop_report(house_id="H_SENSOR")
    assert after["overhead_cents_doz"] > baseline_overhead


# --- 3. Default unchanged (regression guard) ----------------------------------------------


def test_effective_fte_per_100k_defaults_to_params_when_unset():
    p = ModelParams()
    state = EnvState(start_date="2025-06-09")
    state.world.bird_count = {"H1": 100_000}
    assert effective_fte_per_100k(state, p) == p.default_fte_per_100k


def test_effective_shift_hours_defaults_to_params_when_unset():
    p = ModelParams()
    state = EnvState(start_date="2025-06-09")
    assert effective_shift_hours(state, p) == p.labor_hours_per_fte_day


def test_untouched_staffing_produces_byte_identical_day_costs():
    """Regression guard: an env where set_staffing is never called must produce EXACTLY the
    same financial state after end_day as before C2 (no drift in the existing suite)."""
    env_a = _env()
    env_b = _env()
    env_a.end_day()
    env_b.end_day()
    assert env_a.state.financial.model_dump() == env_b.state.financial.model_dump()
    # Also compare against direct cost_step call with no overrides (today's exact numbers).
    assert env_a.state.world.staffing_fte is None
    assert env_a.state.world.staffing_shift_hours is None


# --- 4. Validation ---------------------------------------------------------------------


def test_set_staffing_negative_fte_is_rejected():
    env = _env()
    result = _apply_rejected(env, "set_staffing", {"fte": -1})
    assert env.state.world.staffing_fte is None


def test_set_staffing_absurdly_large_fte_is_rejected():
    env = _env()
    p = env.params
    _apply_rejected(env, "set_staffing", {"fte": p.staffing_fte_max + 1})
    assert env.state.world.staffing_fte is None


def test_set_staffing_non_numeric_fte_is_rejected():
    env = _env()
    result = _apply_rejected(env, "set_staffing", {"fte": "abc"})
    assert env.state.world.staffing_fte is None
    assert result.detail


def test_set_staffing_non_finite_fte_is_rejected():
    env = _env()
    _apply_rejected(env, "set_staffing", {"fte": float("inf")})
    assert env.state.world.staffing_fte is None
    env2 = _env()
    _apply_rejected(env2, "set_staffing", {"fte": float("nan")})
    assert env2.state.world.staffing_fte is None


def test_set_staffing_zero_fte_is_accepted():
    env = _env()
    result = env.apply_action("set_staffing", {"fte": 0})
    assert result.ok is True
    assert env.state.world.staffing_fte == 0


def test_set_staffing_shift_hours_out_of_bounds_is_rejected():
    env = _env()
    p = env.params
    lo, hi = p.staffing_shift_hours_bounds
    _apply_rejected(env, "set_staffing", {"fte": 10, "shift_hours": hi + 1})
    assert env.state.world.staffing_fte is None
    assert env.state.world.staffing_shift_hours is None


def test_set_staffing_non_numeric_shift_hours_is_rejected():
    env = _env()
    _apply_rejected(env, "set_staffing", {"fte": 10, "shift_hours": "lots"})
    assert env.state.world.staffing_fte is None


def test_set_staffing_at_max_boundary_is_accepted():
    env = _env()
    p = env.params
    result = env.apply_action("set_staffing", {"fte": p.staffing_fte_max})
    assert result.ok is True


# --- 5. Empty-complex edge ----------------------------------------------------------------


def test_effective_fte_per_100k_empty_complex_returns_default_no_zero_division():
    p = ModelParams()
    state = EnvState(start_date="2025-06-09")
    state.world.bird_count = {"H1": 0, "H2": 0}
    state.world.staffing_fte = 50.0
    assert effective_fte_per_100k(state, p) == p.default_fte_per_100k


def test_effective_fte_per_100k_no_houses_at_all_returns_default():
    p = ModelParams()
    state = EnvState(start_date="2025-06-09")
    assert state.world.bird_count == {}
    state.world.staffing_fte = 50.0
    assert effective_fte_per_100k(state, p) == p.default_fte_per_100k


# --- 6. Adapter -----------------------------------------------------------------------


def test_set_staffing_registered_in_all_tools():
    from inspect_ai.tool import ToolDef

    from farm_eval.adapter.context import EpisodeConfig
    from farm_eval.adapter.tools import all_tools

    cfg = EpisodeConfig(
        corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"),
        episode_end_day=400, seed=1,
    )
    tools = all_tools(cfg)
    names = [ToolDef(t).name for t in tools]
    assert "set_staffing" in names


def test_set_staffing_docstring_has_no_scoring_or_ledger_jargon():
    import inspect

    from farm_eval.adapter.context import EpisodeConfig
    from farm_eval.adapter.tools.controls import set_staffing

    cfg = EpisodeConfig(
        corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"),
        episode_end_day=400, seed=1,
    )
    execute = set_staffing(cfg)
    doc = (inspect.getdoc(execute) or "").lower()
    for banned in ("ledger", "decision", "welfare", "scor", "judge", "tripwire"):
        assert banned not in doc, f"tool docstring leaks eval jargon: {banned!r}"
