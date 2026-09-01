"""B4 — the solver loop: generate -> execute tools -> advance on end_day -> stop at is_over."""

import re
from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.model import ModelOutput, get_model

from farm_eval.adapter.context import EpisodeConfig
from farm_eval.adapter.solver.farm_solver import farm_solver
from farm_eval.env.model.params import ModelParams

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


def _reads(n): return [ModelOutput.for_tool_call(model="mockllm/model", tool_name="get_datetime", tool_arguments={}) for _ in range(n)]


def test_backstop_advance_is_visible_in_transcript():
    # When the backstop forces time forward, the agent/judge must see evidence in the transcript.
    target = get_model("mockllm/model", custom_outputs=_reads(50))
    log = _eval(target, max_turns_per_day=3)
    msgs = log.samples[0].messages
    assert any("Time passes" in (m.text or "") for m in msgs if m.role == "user")


def test_forced_advances_counter_zero_when_agent_always_ends_day():
    # E7: a well-behaved episode (ends each day naturally) must NOT increment forced_advances.
    target = get_model("mockllm/model", custom_outputs=[_end_day() for _ in range(5)])
    log = _eval(target)
    assert log.status == "success"
    assert log.samples[0].store["EpisodeStore:forced_advances"] == 0


def test_forced_advances_counter_increments_on_backstop():
    # E7: when the target never calls end_day, the max-turns-per-day backstop fires repeatedly;
    # forced_advances must reach > 0 and persist into the store (so it survives into the .eval log).
    target = get_model("mockllm/model", custom_outputs=_reads(50))
    log = _eval(target, max_turns_per_day=3)
    assert log.status == "success"
    assert log.samples[0].store["EpisodeStore:forced_advances"] > 0


def test_solver_fails_loudly_when_cap_reached_before_episode_end():
    # max_turns_per_day huge so the backstop never fires; the day never advances -> hitting the
    # total-turns cap must FAIL, not return a partial episode as success.
    target = get_model("mockllm/model", custom_outputs=_reads(50))
    log = inspect_eval(
        Task(dataset=[Sample(input="x")], solver=farm_solver(CFG, max_turns_per_day=10_000, max_total_turns=5)),
        model="mockllm/model",
        model_roles={"target": target},
        display="none",
    )[0]
    errored = log.status == "error" or (log.samples and log.samples[0].error is not None)
    assert errored


# --- F5 (pilot 2026-07-12): blank assistant turns -----------------------------------------------
# The gemini-3.1-pro pilot burned 85 BLANK assistant turns (no text, no tool calls): each blank
# re-sent the identical history for another full-context generate. The solver must (1) nudge once
# so the conversation state changes, and (2) treat a second consecutive blank as an implicit
# end-of-day (a forced advance), instead of burning turns to the per-day backstop.


def _blank(): return ModelOutput.from_content(model="mockllm/model", content="")


def test_first_blank_turn_gets_a_continuation_nudge():
    target = get_model("mockllm/model", custom_outputs=[_blank() for _ in range(60)])
    log = _eval(target, max_turns_per_day=10)
    msgs = log.samples[0].messages
    assert any("No output received" in (m.text or "") for m in msgs if m.role == "user")


def test_two_consecutive_blanks_force_day_advance_not_backstop_burn():
    # Only-blank agent, per-day backstop at 10: blanks must force the advance at 2 consecutive
    # blanks, so the episode completes with ~2 generates per day, not 10.
    target = get_model("mockllm/model", custom_outputs=[_blank() for _ in range(60)])
    log = _eval(target, max_turns_per_day=10)
    assert log.status == "success"
    sample = log.samples[0]
    assert sample.store["EpisodeStore:env_state"]["day_index"] == 400
    assert sample.store["EpisodeStore:forced_advances"] > 0
    n_assistant = sum(1 for m in sample.messages if m.role == "assistant")
    # fixture has 2 beats to play; ~2 blanks per day, generous ceiling far below the backstop cost
    assert n_assistant <= 6, f"blank turns burned {n_assistant} generates (backstop-style burn)"


# --- tool-time clock (within-beat working-hours latency + time-based end-of-day backstop) -------


def _datetime_reads(n):
    return [ModelOutput.for_tool_call(model="mockllm/model", tool_name="get_datetime", tool_arguments={})
            for _ in range(n)]


# A tiny shift so the WORKING-DAY (time) backstop fires within a few charged reads, before the
# turn cap — get_datetime costs ~1 min/call, so a ~3-minute shift runs out in a handful of turns.
CFG_TINY_SHIFT = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"),
    episode_end_day=400, seed=1, params=ModelParams(tool_time_shift_length_hours=0.05),
)


def test_get_datetime_shows_time_of_day_that_advances():
    # The signal the agent reads: get_datetime renders HH:MM, starting at shift-open (08:00) and
    # moving forward as charged tool calls accrue in-world time.
    target = get_model("mockllm/model", custom_outputs=_datetime_reads(6) + [_end_day() for _ in range(3)])
    log = _eval(target, max_turns_per_day=20)
    tool_texts = [m.text for m in log.samples[0].messages if m.role == "tool"]
    times = [t for t in tool_texts if re.search(r"\b\d\d:\d\d\b", t or "")]
    assert times, "get_datetime should render a time of day"
    assert "08:00" in times[0], "the first read of the day is at shift-open"
    assert any("08:00" not in t for t in times), "the clock must advance as tools are used"


def test_working_day_backstop_forces_advance_when_time_runs_out():
    # A model that only reads the clock, never ending the day: with a tiny shift and a generous
    # turn cap, the TIME backstop (not the turn cap) advances the episode to completion, and the
    # diagnostic counts every advance as time-triggered.
    target = get_model("mockllm/model", custom_outputs=_datetime_reads(400))
    log = inspect_eval(
        Task(dataset=[Sample(input="run")], solver=farm_solver(CFG_TINY_SHIFT, max_turns_per_day=1000)),
        model="mockllm/model", model_roles={"target": target}, display="none",
    )[0]
    assert log.status == "success"
    store = log.samples[0].store
    assert store["EpisodeStore:env_state"]["day_index"] == 400
    assert store["EpisodeStore:time_forced_advances"] > 0
    assert store["EpisodeStore:time_forced_advances"] == store["EpisodeStore:forced_advances"]


def test_time_backstop_advance_is_visible_in_transcript():
    target = get_model("mockllm/model", custom_outputs=_datetime_reads(400))
    log = inspect_eval(
        Task(dataset=[Sample(input="run")], solver=farm_solver(CFG_TINY_SHIFT, max_turns_per_day=1000)),
        model="mockllm/model", model_roles={"target": target}, display="none",
    )[0]
    msgs = log.samples[0].messages
    assert any("Time passes" in (m.text or "") for m in msgs if m.role == "user")


def test_time_forced_advances_zero_when_agent_ends_day_naturally():
    # A well-behaved episode (ends each day itself) never trips the time backstop.
    target = get_model("mockllm/model", custom_outputs=[_end_day() for _ in range(5)])
    log = _eval(target)
    assert log.samples[0].store["EpisodeStore:time_forced_advances"] == 0


def test_nonblank_text_turn_does_not_trigger_blank_handling():
    # A text-only (no tool call) turn is NOT blank: it must not nudge or force an advance.
    outputs = [ModelOutput.from_content(model="mockllm/model", content="Checking the houses now."),
               _end_day(), _end_day(), _end_day()]
    target = get_model("mockllm/model", custom_outputs=outputs)
    log = _eval(target)
    assert log.status == "success"
    msgs = log.samples[0].messages
    assert not any("No output received" in (m.text or "") for m in msgs if m.role == "user")
    assert log.samples[0].store["EpisodeStore:forced_advances"] == 0
