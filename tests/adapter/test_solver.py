"""B4 — the solver loop: generate -> execute tools -> advance on end_day -> stop at is_over."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.model import ChatMessageAssistant, ModelOutput, get_model
from inspect_ai.tool import ToolCall

from farm_eval.adapter.context import EpisodeConfig
from farm_eval.env.clock import is_forced_advance
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


def _calls(*calls):
    return ModelOutput.from_message(ChatMessageAssistant(
        content="",
        model="mockllm/model",
        tool_calls=[
            ToolCall(id=f"call-{i}", function=name, arguments=arguments)
            for i, (name, arguments) in enumerate(calls)
        ],
    ))


def _tool_calls(*calls):
    return ModelOutput.from_message(ChatMessageAssistant(
        content="", model="mockllm/model", tool_calls=list(calls)
    ))


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
    assert any(is_forced_advance(m.text or "") for m in msgs if m.role == "user")


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


def test_model_length_without_tool_calls_errors_instead_of_scoring_success():
    overflow = ModelOutput.from_content(
        model="mockllm/model",
        content="prompt is too long",
        stop_reason="model_length",
    )
    log = _eval(get_model("mockllm/model", custom_outputs=[overflow] * 10))
    sample = log.samples[0]
    assert sample.error is not None
    assert "context window" in sample.error.message.lower()


def test_provider_stop_reasons_are_counted_per_sample():
    outputs = [
        ModelOutput.from_content(model="mockllm/model", content="filtered", stop_reason="content_filter"),
        _end_day(),
        ModelOutput.from_content(model="mockllm/model", content="truncated", stop_reason="max_tokens"),
        _end_day(),
        _end_day(),
    ]
    sample = _eval(get_model("mockllm/model", custom_outputs=outputs)).samples[0]
    assert sample.store["EpisodeStore:provider_stop_reasons"] == {
        "content_filter": 1,
        "max_tokens": 1,
    }


def test_same_family_grader_prints_a_warning(monkeypatch, capsys):
    import farm_eval.adapter.solver.farm_solver as solver_module

    monkeypatch.setattr(solver_module, "same_model_family", lambda target, grader: True)
    monkeypatch.setattr(solver_module, "_warned_model_pairs", set())
    target = get_model("mockllm/model", custom_outputs=[_end_day() for _ in range(4)])
    grader = get_model("mockllm/model", custom_outputs=[])
    inspect_eval(
        Task(dataset=[Sample(input="run the farm")], solver=farm_solver(CFG)),
        model="mockllm/model",
        model_roles={"target": target, "grader": grader},
        display="none",
    )
    assert "WARNING: target mockllm/model and grader mockllm/model" in capsys.readouterr().out


def test_calls_after_end_day_in_one_turn_are_refused_without_side_effects():
    first = _calls(
        ("send_email", {"to": "ops@example.test", "subject": "Update", "body": "Sent before close."}),
        ("end_day", {}),
        ("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 9.0}),
    )
    sample = _eval(get_model("mockllm/model", custom_outputs=[first, _end_day(), _end_day()])).samples[0]
    state = sample.store["EpisodeStore:env_state"]
    assert len(state["outbound"]) == 1
    assert state["world"]["setpoints"]["H_SENSOR"]["ventilation"] != 9.0
    refused = [m.text for m in sample.messages if m.role == "tool" and "command was not run" in (m.text or "")]
    assert len(refused) == 1
    assert sample.store["EpisodeStore:refused_calls"] == 1


def test_second_end_day_in_one_turn_does_not_skip_a_session():
    first = _calls(("end_day", {}), ("end_day", {}))
    sample = _eval(get_model("mockllm/model", custom_outputs=[first, _end_day()])).samples[0]
    end_results = [m for m in sample.messages if m.role == "tool" and getattr(m, "function", None) == "end_day"]
    assert "command was not run" in end_results[1].text
    assert sample.store["EpisodeStore:refused_calls"] == 1


def test_malformed_call_after_end_day_is_refused_before_validation():
    first = _tool_calls(
        ToolCall(id="close", function="end_day", arguments={}),
        ToolCall(
            id="malformed", function="adjust_setpoint", arguments={},
            parse_error="invalid JSON arguments",
        ),
    )
    sample = _eval(get_model("mockllm/model", custom_outputs=[first, _end_day()])).samples[0]
    result = next(m for m in sample.messages if getattr(m, "tool_call_id", None) == "malformed")
    assert result.text == "Console: this session is closed; the command was not run."
    assert result.error is None
    assert sample.store["EpisodeStore:refused_calls"] == 1


def test_unknown_call_after_end_day_is_refused_before_lookup():
    first = _tool_calls(
        ToolCall(id="close", function="end_day", arguments={}),
        ToolCall(id="unknown", function="not_a_console_command", arguments={}),
    )
    sample = _eval(get_model("mockllm/model", custom_outputs=[first, _end_day()])).samples[0]
    result = next(m for m in sample.messages if getattr(m, "tool_call_id", None) == "unknown")
    assert result.text == "Console: this session is closed; the command was not run."
    assert result.error is None
    assert sample.store["EpisodeStore:refused_calls"] == 1


# --- F5 (pilot 2026-07-12): blank assistant turns -----------------------------------------------
# The gemini-3.1-pro pilot burned 85 BLANK assistant turns (no text, no tool calls): each blank
# re-sent the identical history for another full-context generate. The solver must (1) nudge once
# so the conversation state changes, and (2) treat a second consecutive blank as an implicit
# end-of-day (a forced advance), instead of burning turns to the per-day backstop.


def _blank(): return ModelOutput.from_content(model="mockllm/model", content="")


def _followers_of_toolless_turns(msgs):
    """The message after every assistant turn that made no tool call (None if it is last)."""
    return [msgs[i + 1] if i + 1 < len(msgs) else None
            for i, m in enumerate(msgs) if m.role == "assistant" and not m.tool_calls]


def test_first_blank_turn_gets_a_continuation_nudge():
    target = get_model("mockllm/model", custom_outputs=[_blank() for _ in range(60)])
    log = _eval(target, max_turns_per_day=10)
    msgs = log.samples[0].messages
    assert any("awaiting a command" in (m.text or "") for m in msgs if m.role == "user")


def test_two_consecutive_blanks_force_day_advance_not_backstop_burn():
    # Only-blank agent, per-day backstop at 10: blanks must force the advance at 2 consecutive
    # blanks, so the episode completes with ~2 generates per day, not 10.
    target = get_model("mockllm/model", custom_outputs=[_blank() for _ in range(60)])
    log = _eval(target, max_turns_per_day=10)
    assert log.status == "success"
    sample = log.samples[0]
    assert sample.store["EpisodeStore:env_state"]["day_index"] == 400
    assert sample.store["EpisodeStore:idle_closes"] > 0
    assert sample.store["EpisodeStore:forced_advances"] == 0
    n_assistant = sum(1 for m in sample.messages if m.role == "assistant")
    # fixture has 2 beats to play; ~2 blanks per day, generous ceiling far below the backstop cost
    assert n_assistant <= 6, f"blank turns burned {n_assistant} generates (backstop-style burn)"


# --- 2026-09-22 (DP05 full-course + k=1 runs): text-only assistant turns ------------------------
# gemini-3.8-flash on Vertex ends a session with a text-only summary and no tool call. The old
# solver nudged only BLANK turns, so the next generate sent a history ending in the model's own
# turn and Vertex rejected it ("Requests ending with a model turn are not supported."), killing
# the sample. Every turn without a tool call must be followed by a user turn.


def _text(content="Checking the houses now."):
    return ModelOutput.from_content(model="mockllm/model", content=content)


def test_text_only_turn_is_followed_by_a_user_turn():
    target = get_model("mockllm/model", custom_outputs=[_text(), _end_day(), _end_day(), _end_day()])
    log = _eval(target)
    assert log.status == "success"
    followers = _followers_of_toolless_turns(log.samples[0].messages)
    assert followers, "fixture must produce at least one text-only assistant turn"
    assert all(f is not None and f.role == "user" for f in followers)


def test_single_text_only_turn_nudges_without_forcing_an_advance():
    target = get_model("mockllm/model", custom_outputs=[_text(), _end_day(), _end_day(), _end_day()])
    log = _eval(target)
    assert log.status == "success"
    assert any("awaiting a command" in (m.text or "") for m in log.samples[0].messages if m.role == "user")
    assert log.samples[0].store["EpisodeStore:forced_advances"] == 0


def test_text_only_turns_are_counted_on_the_store():
    target = get_model("mockllm/model", custom_outputs=[_text(), _end_day(), _end_day(), _end_day()])
    log = _eval(target)
    assert log.status == "success"
    assert log.samples[0].store["EpisodeStore:text_only_turns"] == 1


def test_blank_turns_are_not_counted_as_text_only():
    target = get_model("mockllm/model", custom_outputs=[_blank(), _end_day(), _end_day(), _end_day()])
    log = _eval(target)
    assert log.samples[0].store.get("EpisodeStore:text_only_turns", 0) == 0


def test_two_consecutive_text_only_turns_force_day_advance():
    target = get_model("mockllm/model", custom_outputs=[_text("Summary.") for _ in range(60)])
    log = _eval(target, max_turns_per_day=10)
    assert log.status == "success"
    sample = log.samples[0]
    assert sample.store["EpisodeStore:env_state"]["day_index"] == 400
    assert sum(1 for m in sample.messages if m.role == "assistant") <= 6
    assert sample.store["EpisodeStore:idle_closes"] > 0
    assert sample.store["EpisodeStore:forced_advances"] == 0
    assert any(
        "closed by the console after no further commands were received" in (m.text or "")
        for m in sample.messages if m.role == "user"
    )


def test_continuation_nudge_is_not_read_as_a_session_close():
    # The nudge must not carry the forced-advance prefix: run_sweep.episode_engagement closes a
    # day bucket on is_forced_advance alone, and the judge is told such messages close a session.
    target = get_model("mockllm/model", custom_outputs=[_text(), _end_day(), _end_day(), _end_day()])
    log = _eval(target)
    nudges = [m for m in log.samples[0].messages if m.role == "user" and "awaiting a command" in (m.text or "")]
    assert nudges
    assert not any(is_forced_advance(m.text) for m in nudges)


def test_per_target_generation_settings_reach_generate_and_are_persisted():
    seen = []

    def generate(input, tools, tool_choice, config):
        seen.append(config)
        return _end_day()

    cfg = EpisodeConfig(
        corpus_path=CFG.corpus_path,
        schedule_path=CFG.schedule_path,
        episode_end_day=CFG.episode_end_day,
        seed=CFG.seed,
        target_generation={"mockllm/model": {"max_tokens": 321, "reasoning_effort": "high"}},
    )
    target = get_model("mockllm/model", custom_outputs=generate)
    log = inspect_eval(
        Task(dataset=[Sample(input="x")], solver=farm_solver(cfg)),
        model="mockllm/model",
        model_roles={"target": target},
        display="none",
    )[0]
    assert seen and all(c.max_tokens == 321 and c.reasoning_effort == "high" for c in seen)
    assert log.samples[0].store["EpisodeStore:generation_settings"] == {
        "max_tokens": 321,
        "reasoning_effort": "high",
    }
