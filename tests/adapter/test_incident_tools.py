"""DP19 build — the FMS records tools: log_incident (action) + read_incident_log (read).

Both route through FarmEnv; the action drops empty optionals (they must not spuriously
satisfy a decision signature's where-clause) and never leaks the silent ledger.
"""

import json
from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver
from inspect_ai.tool import ToolDef

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.records import log_incident, read_incident_log

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def _run(solve_fn):
    @solver
    def drive():
        return solve_fn

    return inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]


def test_all_tools_registry_includes_records_tools():
    names = [ToolDef(t).name for t in all_tools(CFG)]
    assert "log_incident" in names
    assert "read_incident_log" in names


def test_log_incident_records_and_drops_empty_optionals():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        detail = await log_incident(CFG)(
            category="injury",
            description="crew laceration during catch",
            date_of_event="2025-06-08",
        )
        state.metadata["detail"] = detail
        return state

    log = _run(solve)
    assert log.status == "success"
    store = log.samples[0].store["EpisodeStore:env_state"]
    entry = next(a for a in store["actions"] if a["tool"] == "log_incident")
    # Empty house_id / injured_party dropped — they must not satisfy a where-clause.
    assert entry["params"] == {
        "category": "injury",
        "description": "crew laceration during catch",
        "date_of_event": "2025-06-08",
    }
    assert store["incident_log"][0]["category"] == "injury"
    detail = log.samples[0].metadata["detail"]
    assert "incident logged" in detail
    assert "dp" not in detail.lower() and "ledger" not in detail.lower()


def test_read_incident_log_returns_entries_json():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        state.metadata["empty"] = await read_incident_log(CFG)()
        await log_incident(CFG)(
            category="equipment",
            description="belt jam",
            date_of_event="2025-06-10",
            house_id="H_SENSOR",
        )
        state.metadata["after"] = await read_incident_log(CFG)()
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    assert json.loads(md["empty"]) == []
    entries = json.loads(md["after"])
    assert len(entries) == 1
    assert entries[0]["category"] == "equipment"
    assert entries[0]["house_id"] == "H_SENSOR"
