"""Op registry parity: the play surface must be exactly the model's tool surface (spec §4)."""

import inspect as pyinspect
import json
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.play.ops import OPS, run_op

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

# The frozen 18-op contract: 9 reads + 8 actions + end_day, in all_tools() order.
EXPECTED_OPS = [
    "get_datetime", "list_houses", "read_sensor", "list_emails", "read_email",
    "query_pricing", "read_financials", "read_flock_report", "generate_cop_report",
    "adjust_setpoint", "set_staffing", "place_feed_order", "schedule_maintenance",
    "schedule_vet_visit", "log_treatment", "set_egg_disposition", "send_email",
    "end_day",
]


def _env() -> FarmEnv:
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", episode_end_day=400, seed=1)
    env.start()
    return env


def test_registry_is_exactly_the_model_surface():
    assert list(OPS) == EXPECTED_OPS


def test_registry_signatures_match_adapter_tools():
    # all_tools() order is fixed in farm_eval/adapter/tools/__init__.py; zip against it and
    # compare parameter names + defaults from the adapter execute closures. end_day is served
    # by controller.end_day (not in all_tools) — checked separately.
    from farm_eval.adapter.context import EpisodeConfig
    from farm_eval.adapter.tools import all_tools
    from farm_eval.adapter.tools.controller import end_day as adapter_end_day

    cfg = EpisodeConfig(
        corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"),
        episode_end_day=400, seed=1,
    )
    tools = all_tools(cfg) + [adapter_end_day(cfg)]
    for name, tool_fn in zip(EXPECTED_OPS, tools, strict=True):
        sig = pyinspect.signature(tool_fn)
        adapter_params = {
            p.name: (p.default if p.default is not pyinspect.Parameter.empty else None)
            for p in sig.parameters.values()
        }
        ops_params = {k: v.default for k, v in OPS[name].params.items()}
        assert ops_params == adapter_params, f"param drift on {name}"


def test_read_ops_return_adapter_shaped_strings():
    env = _env()
    dt = run_op(env, "get_datetime", {})
    assert dt == f"day {env.current_day()} | {env.current_date()}"
    houses = json.loads(run_op(env, "list_houses", {}))
    assert isinstance(houses, list) and "house_id" in houses[0]
    # read_sensor mirrors the adapter's two branches: message verbatim vs JSON record.
    hid = houses[0]["house_id"]
    out = run_op(env, "read_sensor", {"house_id": hid, "metric": "temp_c"})
    assert json.loads(out)["metric"] == "temp_c"
    missing = run_op(env, "read_email", {"email_id": "nope"})
    assert missing == "No email with id 'nope'."


def test_action_ops_route_through_apply_action():
    env = _env()
    hid = json.loads(run_op(env, "list_houses", {}))[0]["house_id"]
    out = run_op(env, "adjust_setpoint", {"house_id": hid, "system": "ventilation", "value": 1.0})
    assert out == f"ventilation on {hid} set to 1.0"
    # rejected actions surface the in-world detail string, exactly as the adapter does
    bad = run_op(env, "adjust_setpoint", {"house_id": "NOPE", "system": "ventilation", "value": 1.0})
    assert "No such house" in bad


def test_place_feed_order_drops_empty_optionals():
    # The adapter's _params() drops ""/None/0-quantity so they can't satisfy a decision
    # signature's where-clause; the mirror must too. Verify via the recorded action params.
    env = _env()
    run_op(env, "place_feed_order", {"ration": "R1", "quantity_tons": 0.0, "house_id": "",
                                     "additive": "", "target": "", "genetics": ""})
    rec = env.state.actions[-1]
    assert rec.params == {"ration": "R1"}


def test_run_op_rejects_unknown_and_end_day():
    env = _env()
    with pytest.raises(KeyError):
        run_op(env, "read_ledger", {})
    with pytest.raises(ValueError, match="end_day"):
        run_op(env, "end_day", {})
