"""The episode solver loop.

A single custom `@solver` (like PETRI's auditor `for i in range(max_turns)` body, but the tool
results come from the scripted env, not a second model): start the episode once, run a
generate -> execute-tools loop, advance in-world time when the agent calls `end_day`, enforce a
max-turns-per-day backstop so a model that never ends the day cannot stall the episode, and
terminate when `FarmEnv.is_over()`.
"""

from __future__ import annotations

from inspect_ai.model import execute_tools, get_model
from inspect_ai.solver import Generate, Solver, TaskState, solver
from inspect_ai.util import store_as

from farm_eval.adapter.context import EpisodeConfig, EpisodeStore, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.controller import end_day

# Absolute backstop on total model turns, so a pathological model cannot loop forever even if the
# clock somehow fails to advance. Far above any real episode's turn count.
_MAX_TOTAL_TURNS = 5000


@solver
def farm_solver(cfg: EpisodeConfig, *, max_turns_per_day: int = 30) -> Solver:
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        store = store_as(EpisodeStore)
        env = get_env(cfg)
        if not store.started:  # survives retry/replay
            env.start()
            store.started = True

        tools = all_tools(cfg) + [end_day(cfg)]
        state.tools = tools
        model = get_model(role="target", default=state.model)

        turns_today = 0
        total_turns = 0
        while not get_env(cfg).is_over() and total_turns < _MAX_TOTAL_TURNS:
            output = await model.generate(input=state.messages, tools=tools)
            state.messages.append(output.message)
            state.output = output
            total_turns += 1

            tool_calls = output.message.tool_calls or []
            if tool_calls:
                result = await execute_tools(state.messages, tools)
                state.messages.extend(result.messages)

            if any(tc.function == "end_day" for tc in tool_calls):
                turns_today = 0  # the agent ended the day; the end_day tool already advanced time
            else:
                turns_today += 1
                if turns_today >= max_turns_per_day:
                    # Backstop: force the day to advance so the episode cannot stall.
                    get_env(cfg).end_day(notes="(auto: max turns for the day reached)")
                    turns_today = 0

        return state

    return solve
