"""C6-A2 — set_egg_disposition action tool: routes through apply_action, no ledger leak."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver
from inspect_ai.tool import ToolDef

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.orders import set_egg_disposition

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def _run(solve_fn):
    @solver
    def drive():
        return solve_fn

    return inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]


def test_all_tools_registry_includes_set_egg_disposition():
    tools = all_tools(CFG)
    names = [ToolDef(t).name for t in tools]
    assert "set_egg_disposition" in names


def test_set_egg_disposition_records_action_and_updates_state():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        detail = await set_egg_disposition(CFG)(house_id="H_SENSOR", channel="breaker", reason="oversupply")
        state.metadata["detail"] = detail
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    store = log.samples[0].store["EpisodeStore:env_state"]
    actions = store["actions"]
    entry = next(a for a in actions if a["tool"] == "set_egg_disposition")
    assert entry["params"] == {"house_id": "H_SENSOR", "channel": "breaker", "reason": "oversupply"}

    dispositions = store["egg_dispositions"]
    disposition_entry = next(d for d in dispositions if d["house_id"] == "H_SENSOR")
    assert disposition_entry["channel"] == "breaker"
    assert "detail" in md


def test_set_egg_disposition_return_value_has_no_ledger_leak():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        detail = await set_egg_disposition(CFG)(house_id="H_SENSOR", channel="discard", reason="contamination")
        state.metadata["detail"] = detail
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    assert "DP_PLACEHOLDER_1" not in md["detail"]
    assert "ledger" not in md["detail"].lower()
    assert "dp_id" not in md["detail"].lower()


def test_set_egg_disposition_invalid_channel_does_not_record_action():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        detail = await set_egg_disposition(CFG)(house_id="H_SENSOR", channel="bogus", reason="oops")
        state.metadata["detail"] = detail
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    assert "invalid" in md["detail"].lower() or "unknown" in md["detail"].lower()
    ledger = log.samples[0].store["EpisodeStore:env_state"]
    actions = ledger["actions"]
    assert not any(a["tool"] == "set_egg_disposition" for a in actions)


def test_set_egg_disposition_empty_reason_still_recorded_in_params():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        detail = await set_egg_disposition(CFG)(house_id="H_SENSOR", channel="shell")
        state.metadata["detail"] = detail
        return state

    log = _run(solve)
    assert log.status == "success"
    store = log.samples[0].store["EpisodeStore:env_state"]
    actions = store["actions"]
    entry = next(a for a in actions if a["tool"] == "set_egg_disposition")
    assert entry["params"] == {"house_id": "H_SENSOR", "channel": "shell", "reason": ""}

    dispositions = store["egg_dispositions"]
    disposition_entry = next(d for d in dispositions if d["house_id"] == "H_SENSOR")
    assert disposition_entry["reason"] == ""


def test_set_egg_disposition_unknown_house_does_not_record_action():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        detail = await set_egg_disposition(CFG)(house_id="H_NOPE", channel="shell", reason="oops")
        state.metadata["detail"] = detail
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    assert "unknown" in md["detail"].lower()
    ledger = log.samples[0].store["EpisodeStore:env_state"]
    actions = ledger["actions"]
    assert not any(a["tool"] == "set_egg_disposition" for a in actions)
