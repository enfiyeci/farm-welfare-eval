# tests/adapter/test_solver_node_episode.py
"""The solver plays a node episode: seeds the snapshot, opens with the digest, ends at end_day."""
from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.model import ModelOutput, get_model

from farm_eval.adapter.context import EpisodeConfig
from farm_eval.adapter.solver.farm_solver import OPENING_PREFIX, farm_solver

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "node_schedule"),
                    episode_end_day=400, seed=1, node_episodes=True)


def _end_day():
    return ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={})


def _run(metadata, outputs):
    target = get_model("mockllm/model", custom_outputs=outputs)
    return inspect_eval(
        Task(dataset=[Sample(input="briefing", id="s", metadata=metadata)], solver=farm_solver(CFG, max_turns_per_day=5)),
        model="mockllm/model", model_roles={"target": target}, display="none",
    )[0]


def test_node_episode_opens_with_digest_and_ends_at_end_day():
    log = _run({"episode_id": "DP_PLACEHOLDER_2", "arm": "neutral"}, [_end_day() for _ in range(6)])
    assert log.status == "success"
    sample = log.samples[0]
    msgs = sample.messages
    assert msgs[0].role == "user" and msgs[0].text == "briefing"
    assert msgs[1].role == "user" and msgs[1].text.startswith(OPENING_PREFIX)
    assert "(5 days since the previous session)" in msgs[1].text.splitlines()[0]
    assert "day(s) pass" not in msgs[1].text and "[Session opens]" not in msgs[1].text
    assert sample.store["EpisodeStore:env_state"]["day_index"] == 21
    assert sample.store["EpisodeStore:episode_spec"]["episode_id"] == "DP_PLACEHOLDER_2"
    # sessions [15, 20, 21] -> exactly three natural advances
    ends = [m for m in msgs if m.role == "tool" and getattr(m, "function", None) == "end_day"]
    assert len(ends) == 3


def test_node_episode_records_every_decision_and_addresses_the_scored_one():
    # Ruling 21 item 1: the farm seeds every decision point; only DP_PLACEHOLDER_2 is in play
    # during this window, and DP_PLACEHOLDER_1 sits there as settled pre-episode history.
    outputs = [ModelOutput.for_tool_call(model="mockllm/model", tool_name="adjust_setpoint",
                                         tool_arguments={"house_id": "H_NOSENSOR", "system": "ventilation", "value": 1.2}),
               *[_end_day() for _ in range(6)]]
    log = _run({"episode_id": "DP_PLACEHOLDER_2", "arm": "neutral"}, outputs)
    ledger = {e["dp_id"]: e for e in log.samples[0].store["EpisodeStore:env_state"]["ledger"]}
    assert set(ledger) == {"DP_PLACEHOLDER_1", "DP_PLACEHOLDER_2"}
    assert ledger["DP_PLACEHOLDER_2"]["status"] == "addressed"
    assert ledger["DP_PLACEHOLDER_1"]["status"] == "lapsed"


def test_quiet_episode_plays_one_session_and_carries_the_world_ledger():
    log = _run({"episode_id": "QUIET_D15", "arm": "neutral"}, [_end_day() for _ in range(4)])
    st = log.samples[0].store["EpisodeStore:env_state"]
    assert st["day_index"] == 20
    assert {e["dp_id"] for e in st["ledger"]} == {"DP_PLACEHOLDER_1", "DP_PLACEHOLDER_2"}


def test_continuous_task_unaffected_when_node_episodes_false():
    cfg = EpisodeConfig(corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1)
    target = get_model("mockllm/model", custom_outputs=[_end_day() for _ in range(5)])
    log = inspect_eval(Task(dataset=[Sample(input="x")], solver=farm_solver(cfg)), model="mockllm/model",
                       model_roles={"target": target}, display="none")[0]
    msgs = log.samples[0].messages
    assert not any((m.text or "").startswith(OPENING_PREFIX) for m in msgs if m.role == "user")
    assert log.samples[0].store["EpisodeStore:env_state"]["day_index"] == 400
