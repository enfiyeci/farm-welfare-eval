"""Task 5 — flock + CoP read tools: registered in all_tools() and return computed JSON."""

import json
from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.flock import generate_cop_report, read_flock_report

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def _run(solve_fn):
    @solver
    def drive():
        return solve_fn

    return inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]


def test_flock_tools_registered():
    tools = all_tools(CFG)
    # Inspect @tool wrappers store the name in __registry_info__.name, not __name__
    names = {t.__registry_info__.name for t in tools if hasattr(t, "__registry_info__")}
    assert "read_flock_report" in names
    assert "generate_cop_report" in names
    assert len(tools) == 15  # 13 existing + 2 new flock tools


def test_read_flock_report_tool_returns_json():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        state.metadata["flock"] = await read_flock_report(CFG)(house_id="H_SENSOR")
        return state

    log = _run(solve)
    assert log.status == "success"
    rep = json.loads(log.samples[0].metadata["flock"])
    assert rep["house_id"] == "H_SENSOR"
    assert "daily_series" in rep


def test_generate_cop_report_tool_returns_json():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        state.metadata["cop"] = await generate_cop_report(CFG)(house_id="H_SENSOR")
        return state

    log = _run(solve)
    assert log.status == "success"
    rep = json.loads(log.samples[0].metadata["cop"])
    assert rep["house_id"] == "H_SENSOR"
    assert "total_cents_doz" in rep
