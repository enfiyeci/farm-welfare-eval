"""B1 — the episode context: EnvState lives in the Inspect store; FarmEnv binds to it."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver

from farm_eval.adapter.context import EpisodeConfig, get_env, load_resources
from farm_eval.adapter import context as ctx

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def test_load_resources_caches_by_path():
    ctx._resources.clear()
    a = load_resources(CFG)
    b = load_resources(CFG)
    assert a is b  # same cached (corpus, schedule) tuple — loaded once
    assert a[1].decision_points  # schedule parsed


def test_double_start_does_not_duplicate_day0_events():
    # get_env rebuilds a fresh FarmEnv each call; start() must be idempotent against the persisted
    # EnvState, not a transient instance flag, or day-0 events re-fire on re-entry/replay.
    @solver
    def drive():
        async def solve(state: TaskState, generate: Generate) -> TaskState:
            get_env(CFG).start()
            get_env(CFG).start()  # a second fresh wrapper — must NOT re-fire day-0 events
            env = get_env(CFG)
            state.metadata["mailbox"] = len(env.state.mailbox)
            state.metadata["event_log"] = len(env.state.event_log)
            return state

        return solve

    log = inspect_eval(
        Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none"
    )[0]
    md = log.samples[0].metadata
    assert md["mailbox"] == 1  # the single day-0 email, delivered once
    assert md["event_log"] == 1


def test_get_env_binds_store_and_persists_mutation():
    @solver
    def drive():
        async def solve(state: TaskState, generate: Generate) -> TaskState:
            env = get_env(CFG)
            env.start()
            result = env.apply_action(
                "adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 2.5}
            )
            state.metadata["addressed"] = result.addressed_dps
            env2 = get_env(CFG)  # a second accessor in the same sample sees the SAME state
            state.metadata["same_state"] = env2.state is env.state
            return state

        return solve

    log = inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]
    assert log.status == "success"
    sample = log.samples[0]
    assert sample.metadata["addressed"] == ["DP_PLACEHOLDER_1"]
    assert sample.metadata["same_state"] is True
    # The welfare/ledger state persisted into the .eval store (serialized EnvState).
    env_state = sample.store["EpisodeStore:env_state"]
    assert env_state is not None
    ledger = env_state["ledger"]
    addressed = [e for e in ledger if e["dp_id"] == "DP_PLACEHOLDER_1"]
    assert addressed and addressed[0]["status"] == "addressed"
