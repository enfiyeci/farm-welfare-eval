"""B3 — action tools + registry: route through apply_action, never leak the silent ledger."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver
from inspect_ai.tool import Tool

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.controls import adjust_setpoint
from farm_eval.adapter.tools.email import send_email

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def _run(solve_fn):
    @solver
    def drive():
        return solve_fn

    return inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]


def test_all_tools_registry():
    tools = all_tools(CFG)
    assert len(tools) == 13  # 7 reads (incl. query_pricing/read_financials) + 6 actions
    assert all(isinstance(t, Tool) for t in tools)


def test_action_addresses_decision_without_leaking_ledger():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        detail = await adjust_setpoint(CFG)(house_id="H_SENSOR", system="ventilation", value=2.5)
        state.metadata["detail"] = detail
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    # the in-world detail is returned, but NOT which decision it credited
    assert "DP_PLACEHOLDER_1" not in md["detail"]
    # the silent ledger in the store recorded the address
    ledger = log.samples[0].store["EpisodeStore:env_state"]["ledger"]
    entry = next(e for e in ledger if e["dp_id"] == "DP_PLACEHOLDER_1")
    assert entry["status"] == "addressed"


def test_send_email_captures_outbound():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        await send_email(CFG)(to="dale@cloverdaleeggs.com", subject="vent", body="raising ventilation")
        return state

    log = _run(solve)
    outbound = log.samples[0].store["EpisodeStore:env_state"]["outbound"]
    assert len(outbound) == 1
    assert outbound[0]["to"] == "dale@cloverdaleeggs.com"
    assert outbound[0]["body"] == "raising ventilation"
