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


# --- D8: the chick-sourcing crash shape (DP23, k=1 run 2026-09-22) ------------------------------
# gemini-3.8-flash wrote a prose "Operational Digest & Summary" (text, no tool call) in the FINAL
# session and the next request ended on that model turn; Vertex rejected it with 400
# INVALID_ARGUMENT "Requests ending with a model turn are not supported." after 124 minutes. The
# fix (c037654) nudges after every tool-less turn. This replays that shape against a target that
# enforces Vertex's rule on every request, so the regression fails exactly the way the run did.


class _ModelTurnRejected(RuntimeError):
    pass


def _vertex_like(outputs):
    """A mock target that, like Vertex/Gemini, rejects any request whose last message is the
    model's own turn. Records the role of each request's last message."""
    script = iter(outputs)
    last_roles: list[str] = []

    def generate(input, tools, tool_choice, config):
        last_roles.append(input[-1].role)
        if input[-1].role == "assistant":
            raise _ModelTurnRejected("Requests ending with a model turn are not supported.")
        return next(script)

    return get_model("mockllm/model", custom_outputs=generate), last_roles


def _summary():
    return ModelOutput.from_content(
        model="mockllm/model",
        content="Operational Digest & Summary\n\nAll houses checked; orders placed; nothing further today.")


def _run_vertex_like(outputs):
    target, last_roles = _vertex_like(outputs)
    log = inspect_eval(
        Task(dataset=[Sample(input="briefing", id="s", metadata={"episode_id": "DP_PLACEHOLDER_2", "arm": "neutral"})],
             solver=farm_solver(CFG, max_turns_per_day=5)),
        model="mockllm/model", model_roles={"target": target}, display="none",
    )[0]
    return log, last_roles


def _assert_every_request_ends_on_a_user_or_tool_turn(log, last_roles):
    assert log.status == "success", log.error
    assert last_roles and all(r in ("user", "tool") for r in last_roles), last_roles
    msgs = log.samples[0].messages
    for i, m in enumerate(msgs):
        if m.role == "assistant" and not m.tool_calls and i + 1 < len(msgs):
            assert msgs[i + 1].role == "user", f"tool-less assistant turn {i} not followed by a user turn"


def test_text_only_summary_in_the_final_session_is_followed_by_a_user_turn():
    # sessions [15, 20, 21]: two end_days reach the final session, the model writes its summary
    # with no tool call, and only then closes the session.
    log, last_roles = _run_vertex_like([_end_day(), _end_day(), _summary(), _end_day()])
    _assert_every_request_ends_on_a_user_or_tool_turn(log, last_roles)
    sample = log.samples[0]
    assert sample.store["EpisodeStore:env_state"]["day_index"] == 21
    assert sample.store["EpisodeStore:text_only_turns"] == 1
    assert sample.store["EpisodeStore:forced_advances"] == 0


def test_repeated_final_session_summaries_end_the_episode_without_a_model_turn_request():
    # The model never calls end_day in the final session, only summarises: the second tool-less
    # turn forces the close, which ends the episode — and no request ever ends on a model turn.
    log, last_roles = _run_vertex_like([_end_day(), _end_day(), *[_summary() for _ in range(6)]])
    _assert_every_request_ends_on_a_user_or_tool_turn(log, last_roles)
    sample = log.samples[0]
    assert sample.store["EpisodeStore:env_state"]["day_index"] == 21
    assert sample.store["EpisodeStore:forced_advances"] == 1
    assert sample.messages[-1].role == "user"
