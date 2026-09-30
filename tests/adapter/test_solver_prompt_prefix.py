# tests/adapter/test_solver_prompt_prefix.py
"""B2 guard: every target request is the previous request plus appended messages.

Provider prompt caches (Gemini implicit caching, Anthropic/OpenAI prefix caching) only pay off if
the harness never rewrites an earlier message, reorders the tool list or changes the generate
config between turns. The 2026-09-30 investigation of the real 2026-09-22 logs found the prefix
byte-stable in every consecutive pair; this pins that property for the solver paths a node
episode goes through: tool turns, a text-only turn (nudge), natural `end_day` advances, and the
max-turns forced advance.

The requests are fingerprinted AT CALL TIME, at the model-API boundary. A ModelEvent's `input`
shares message objects with `state.messages`, so an earlier message rewritten in place would show
up rewritten in every recorded event and the event-based check alone would stay blind to it.
"""
from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.model import ModelOutput, get_model
from inspect_ai.model._providers.mockllm import MockLLM

from farm_eval.adapter.context import EpisodeConfig
from farm_eval.adapter.solver.farm_solver import farm_solver
from farm_eval.report.cost import prefix_changes, request_shape, request_shape_of

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "node_schedule"),
                    episode_end_day=400, seed=1, node_episodes=True)


def _tool(name: str, **args) -> ModelOutput:
    return ModelOutput.for_tool_call(model="mockllm/model", tool_name=name, tool_arguments=args)


def test_target_requests_only_ever_append_to_the_previous_request(tmp_path, monkeypatch):
    sent = []  # one fingerprint per request, taken when the request is made
    real_generate = MockLLM.generate

    async def recording_generate(self, input, tools, tool_choice, config):
        sent.append(request_shape_of(input, tools, config, tool_choice))
        return await real_generate(self, input, tools, tool_choice, config)

    monkeypatch.setattr(MockLLM, "generate", recording_generate)
    outputs = [
        _tool("adjust_setpoint", house_id="H_NOSENSOR", system="ventilation", value=1.2),
        ModelOutput.from_content(model="mockllm/model", content="PLACEHOLDER summary, no tool call"),
        _tool("end_day"),
        # three non-advancing turns hit max_turns_per_day=3 -> forced advance
        _tool("list_houses"), _tool("list_houses"), _tool("list_houses"),
        *[_tool("end_day") for _ in range(6)],
    ]
    target = get_model("mockllm/model", custom_outputs=outputs)
    log = inspect_eval(
        Task(dataset=[Sample(input="briefing", id="s", metadata={"episode_id": "DP_PLACEHOLDER_2", "arm": "neutral"})],
             solver=farm_solver(CFG, max_turns_per_day=3)),
        model="mockllm/model", model_roles={"target": target}, display="none", log_dir=str(tmp_path),
    )[0]
    assert log.status == "success"
    sample = log.samples[0]
    assert sample.store["EpisodeStore:forced_advances"] >= 1, "the forced-advance path was not exercised"
    assert sample.store["EpisodeStore:text_only_turns"] >= 1, "the text-only nudge path was not exercised"
    target_events = [e for e in sample.events if e.event == "model" and (e.role or "target") == "target"]
    assert len(target_events) >= 6
    assert len(sent) == len(target_events)
    assert prefix_changes(sent) == [], "a request rewrote, dropped or reordered what the previous one sent"
    assert prefix_changes([request_shape(e) for e in target_events]) == []
