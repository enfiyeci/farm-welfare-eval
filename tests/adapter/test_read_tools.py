"""B2 — read tools: thin @tool wrappers over FarmEnv reads (computed, never canned prose)."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.controller import get_datetime, list_houses, read_sensor
from farm_eval.adapter.tools.email import list_emails, read_email
from farm_eval.adapter.tools.finance import query_pricing, read_financials

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def _run(solve_fn):
    @solver
    def drive():
        return solve_fn

    return inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]


def test_read_tools_return_computed_data():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()  # deliver day-0 email + open day-0 DP
        state.metadata["datetime"] = await get_datetime(CFG)()
        state.metadata["houses"] = await list_houses(CFG)()
        state.metadata["sensor_ok"] = await read_sensor(CFG)(house_id="H_SENSOR", metric="ammonia_ppm")
        state.metadata["sensor_missing"] = await read_sensor(CFG)(house_id="H_NOSENSOR", metric="ammonia_ppm")
        inbox = await list_emails(CFG)()
        state.metadata["inbox"] = inbox
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    assert "2025-06-09" in md["datetime"]
    assert "H_SENSOR" in md["houses"]
    assert "ammonia_ppm" in md["sensor_ok"]  # raw "metric: value" data
    assert "handheld" in md["sensor_missing"].lower()  # verbatim availability message
    assert "H_SENSOR" not in md["sensor_missing"] or "handheld" in md["sensor_missing"].lower()
    assert "evt-0" in md["inbox"]  # the day-0 email is listed by id


def test_read_email_marks_read():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        listing = await list_emails(CFG)()
        # first email id appears as "evt-0-..."; read it
        body = await read_email(CFG)(email_id="evt-0-0")
        state.metadata["body"] = body
        # after reading, it is no longer unread
        env = get_env(CFG)
        state.metadata["unread_count_after"] = len(env.list_emails(unread_only=True))
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    assert "evt-0-0" in md["body"] or "subject" in md["body"].lower()
    assert md["unread_count_after"] == 0


def test_pricing_tools_registered_and_computed():
    assert len(all_tools(CFG)) == 15  # 9 reads (incl. generate_cop_report) + 6 actions

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        state.metadata["pricing"] = await query_pricing(CFG)()
        state.metadata["financials"] = await read_financials(CFG)()
        return state

    log = _run(solve)
    assert log.status == "success"
    md = log.samples[0].metadata
    assert "egg_wholesale_usd_doz" in md["pricing"]
    assert "1.66" in md["pricing"]  # fixture corpus Jun-2025 egg price, computed
    assert "feed_inventory_tons" in md["financials"]  # honest current-state field
