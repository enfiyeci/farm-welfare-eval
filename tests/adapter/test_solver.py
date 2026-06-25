"""B4 — the solver loop: generate -> execute tools -> advance on end_day -> stop at is_over."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.model import ModelOutput, get_model

from farm_eval.adapter.context import EpisodeConfig
from farm_eval.adapter.solver.farm_solver import farm_solver

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def _eval(target_model, *, max_turns_per_day=10):
    return inspect_eval(
        Task(dataset=[Sample(input="run the farm")], solver=farm_solver(CFG, max_turns_per_day=max_turns_per_day)),
        model="mockllm/model",
        model_roles={"target": target_model},
        display="none",
    )[0]


def _end_day(): return ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={})


def test_solver_advances_episode_to_completion_on_end_day():
    # fixture beats are {0, 5}; episode_end_day=400 -> two end_day calls reach is_over().
    target = get_model("mockllm/model", custom_outputs=[_end_day() for _ in range(5)])
    log = _eval(target)
    assert log.status == "success"
    env_state = log.samples[0].store["EpisodeStore:env_state"]
    assert env_state["day_index"] == 400  # reached the episode end


def test_solver_backstop_forces_day_advance_when_agent_never_ends_day():
    # The agent only ever reads; the max-turns-per-day backstop must still advance time to is_over().
    reads = [ModelOutput.for_tool_call(model="mockllm/model", tool_name="get_datetime", tool_arguments={}) for _ in range(50)]
    target = get_model("mockllm/model", custom_outputs=reads)
    log = _eval(target, max_turns_per_day=3)
    assert log.status == "success"
    assert log.samples[0].store["EpisodeStore:env_state"]["day_index"] == 400
