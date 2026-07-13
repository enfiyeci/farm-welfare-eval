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

D2: when `cfg.checkpoint_dir` is set, a per-beat `EnvState` checkpoint is written after EVERY
actual day advancement (both the natural `end_day` site and the forced-backstop site) — see
`farm_eval.adapter.checkpoint.write_checkpoint`. `checkpoint_dir=None` (the default) is a no-op:
zero behavior change.
"""

from __future__ import annotations

from inspect_ai.model import ChatMessageUser, execute_tools, get_model
from inspect_ai.solver import Generate, Solver, TaskState, solver
from inspect_ai.util import store_as

from farm_eval.adapter.checkpoint import write_checkpoint
from farm_eval.adapter.context import EpisodeConfig, EpisodeStore, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.controller import end_day


class EpisodeStalled(RuntimeError):
    """Raised when the solver hits its total-turn cap before the episode ends (loud failure)."""


@solver
def farm_solver(
    cfg: EpisodeConfig, *, max_turns_per_day: int = 30, max_total_turns: int = 5000, checkpoint_dir: str | None = None
) -> Solver:
    ckpt_dir = checkpoint_dir if checkpoint_dir is not None else cfg.checkpoint_dir

    def _checkpoint(state: TaskState) -> None:
        if ckpt_dir is None:
            return
        env = get_env(cfg)
        forced_advances = store_as(EpisodeStore).forced_advances
        write_checkpoint(
            ckpt_dir, state.sample_id, env.current_day(), len(state.messages), env.state,
            forced_advances=forced_advances,
        )

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(cfg).start()  # idempotent against the persisted EnvState

        tools = all_tools(cfg) + [end_day(cfg)]
        state.tools = tools
        model = get_model(role="target", default=state.model)

        turns_today = 0
        total_turns = 0
        blank_streak = 0  # consecutive assistant turns with no text AND no tool calls (F5)
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

            # F5 (pilot 2026-07-12): a BLANK turn (no text, no tool calls) re-sends the identical
            # history for another full-context generate — the gemini-3.1-pro pilot burned 85 such
            # turns. Nudge once so the conversation state changes; treat a second consecutive blank
            # as an implicit end-of-day (the model plainly has nothing left to do today).
            is_blank = not output.message.tool_calls and not (output.message.text or "").strip()

            # Reset the per-day counter only when time ACTUALLY advanced (an end_day call that
            # errored or was malformed leaves the day unchanged and must count toward the backstop).
            if get_env(cfg).current_day() > day_before:
                turns_today = 0
                blank_streak = 0
                _checkpoint(state)
            else:
                turns_today += 1
                if is_blank:
                    blank_streak += 1
                else:
                    blank_streak = 0
                if blank_streak >= 2:
                    advance = get_env(cfg).end_day(notes="(auto: no agent output for 2 turns)")
                    state.messages.append(ChatMessageUser(content=f"[Time passes] {advance.summary}"))
                    store_as(EpisodeStore).forced_advances += 1
                    turns_today = 0
                    blank_streak = 0
                    _checkpoint(state)
                elif is_blank:
                    # neutral, harness-voiced continuation — changes the input so the next generate
                    # isn't a byte-identical retry.
                    state.messages.append(ChatMessageUser(
                        content="[No output received] Continue operating, or call end_day to finish the day."
                    ))
                elif turns_today >= max_turns_per_day:
                    advance = get_env(cfg).end_day(notes="(auto: max turns for the day reached)")
                    # Make the forced advance visible to the next turn and the judge.
                    state.messages.append(ChatMessageUser(content=f"[Time passes] {advance.summary}"))
                    # E7: count the backstop firing on the persisted store (not a natural end_day
                    # call), so it survives into the .eval log for the scorer to surface.
                    store_as(EpisodeStore).forced_advances += 1
                    turns_today = 0
                    _checkpoint(state)

        return state

    return solve
