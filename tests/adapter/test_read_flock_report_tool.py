# tests/adapter/test_read_flock_report_tool.py
from pathlib import Path
from inspect_ai import Task, eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import solver, TaskState, Generate
from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import read_flock_report

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"),
                    episode_end_day=400, seed=1)


def _run(solve_fn):
    @solver
    def drive():
        return solve_fn
    return inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model",
                        display="none")[0]


def test_read_flock_report_tool_returns_computed_json():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        hid = next(iter(get_env(CFG).state.welfare.houses))
        state.metadata["rep"] = await read_flock_report(CFG)(house_id=hid)
        return state
    log = _run(solve)
    assert log.status == "success"
    assert "footpad_affected_pct" in log.samples[0].metadata["rep"]   # welfare obs surfaced as JSON
