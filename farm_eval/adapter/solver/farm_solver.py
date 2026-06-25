"""The episode solver loop.

A single custom `@solver` (like PETRI's auditor `for i in range(max_turns)` body, but the tool
results come from the scripted env, not a second model): start the episode once, run a
generate -> execute-tools loop, advance in-world time when the agent calls `end_day`, enforce a
max-turns-per-day backstop so a model that never ends the day cannot stall the episode, and
terminate when `FarmEnv.is_over()`.

Robustness (Codex review): the per-day counter resets on ACTUAL day advancement (not merely on a
tool *named* end_day — a malformed/erroring end_day call must still count toward the backstop);
forced advances are written into the transcript so the next turn and the judge see that time
passed; exhausting the total-turns cap before the episode ends is a loud failure, never a partial
"success".
"""

from __future__ import annotations

from inspect_ai.model import ChatMessageUser, execute_tools, get_model
from inspect_ai.solver import Generate, Solver, TaskState, solver

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.controller import end_day


class EpisodeStalled(RuntimeError):
    """Raised when the solver hits its total-turn cap before the episode ends (loud failure)."""


@solver
def farm_solver(cfg: EpisodeConfig, *, max_turns_per_day: int = 30, max_total_turns: int = 5000) -> Solver:
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(cfg).start()  # idempotent against the persisted EnvState

        tools = all_tools(cfg) + [end_day(cfg)]
        state.tools = tools
        model = get_model(role="target", default=state.model)

        turns_today = 0
        total_turns = 0
        while not get_env(cfg).is_over():
            if total_turns >= max_total_turns:
                raise EpisodeStalled(
                    f"solver exceeded {max_total_turns} turns at day {get_env(cfg).current_day()} "
                    f"before the episode end (day {cfg.episode_end_day})"
                )

            day_before = get_env(cfg).current_day()
            output = await model.generate(input=state.messages, tools=tools)
            state.messages.append(output.message)
            state.output = output
            total_turns += 1

            if output.message.tool_calls:
                result = await execute_tools(state.messages, tools)
                state.messages.extend(result.messages)

            # Reset the per-day counter only when time ACTUALLY advanced (an end_day call that
            # errored or was malformed leaves the day unchanged and must count toward the backstop).
            if get_env(cfg).current_day() > day_before:
                turns_today = 0
            else:
                turns_today += 1
                if turns_today >= max_turns_per_day:
                    advance = get_env(cfg).end_day(notes="(auto: max turns for the day reached)")
                    # Make the forced advance visible to the next turn and the judge.
                    state.messages.append(ChatMessageUser(content=f"[Time passes] {advance.summary}"))
                    turns_today = 0

        return state

    return solve
