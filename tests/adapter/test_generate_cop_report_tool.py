"""Task 4 — generate_cop_report tool wrapper: thin @tool over FarmEnv.generate_cop_report."""

import json
from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import generate_cop_report

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def _run(solve_fn):
    @solver
    def drive():
        return solve_fn

    return inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]


def test_generate_cop_report_tool_returns_json():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        get_env(CFG).end_day()
        result = await generate_cop_report(CFG)()          # tool output (JSON string)
        expected = json.dumps(get_env(CFG).generate_cop_report())   # env method, same unmutated state
        state.metadata["cop"] = result
        state.metadata["cop_expected"] = expected
        return state

    log = _run(solve)
    assert log.status == "success"
    cop = json.loads(log.samples[0].metadata["cop"])
    expected = json.loads(log.samples[0].metadata["cop_expected"])
    assert cop == expected                              # tool delegates to the env method exactly
    assert isinstance(cop["cop_cents_doz"], (int, float))
    assert "vs_target" in cop and "revenue_cum" in cop
