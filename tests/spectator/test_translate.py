"""Tests for the spectator translator: Inspect transcript events -> feed events.

Generic placeholder content only -- no farm content in tests (house key `H_X`, dp id `DP_X`,
`PLACEHOLDER_*` prose). Every Inspect event is a REAL `ModelEvent`/`ToolEvent`/`StoreEvent`
instance, not a stub, so the translator is tested against the shapes it will actually see.
"""

from __future__ import annotations

import pytest
from inspect_ai._util.json import JsonChange
from inspect_ai.event import InfoEvent, ModelEvent, StoreEvent, ToolEvent
from inspect_ai.model import (
    ChatMessageAssistant,
    ContentReasoning,
    ContentText,
    GenerateConfig,
    ModelOutput,
    ModelUsage,
)
from inspect_ai.tool import ToolCall

from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.state import (
    Email,
    EnvState,
    HouseWelfare,
    WelfareState,
    WorldState,
)
from farm_eval.spectator.events import (
    AssistantText,
    DayEnd,
    DayStart,
    DecisionResolved,
    DecisionWindow,
    EmailDelivered,
    EmailRead,
    EmailSent,
    EpisodeEnd,
    RunHealth,
    RunMeta,
    StateSnapshot,
    ToolCallEvent,
)
from farm_eval.spectator.shadow import ENV_STATE_KEY
from farm_eval.spectator.translate import Translator

TARGET = "mockllm/target"
GRADER = "mockllm/grader"

# A two-month normals table is all `make_ambient` needs (it reads months 1 and 7).
WEATHER = {
    "monthly_normals_f": {1: {"high": 40.0, "low": 20.0}, 7: {"high": 90.0, "low": 70.0}},
    "diurnal_swing_f": 20.0,
}


# --- fixtures ------------------------------------------------------------------------


def _email(email_id: str, **over) -> Email:
    payload = {
        "id": email_id,
        "day": 0,
        "date": "2025-01-01",
        "from": "sender@x.test",
        "to": "operator@x.test",
        "subject": "PLACEHOLDER_SUBJECT",
        "body": "PLACEHOLDER_BODY",
    }
    payload.update(over)
    return Email.model_validate(payload)


def _state(**over) -> EnvState:
    kwargs = dict(
        start_date="2025-01-01",
        welfare=WelfareState(
            houses={
                "H_X": HouseWelfare(
                    ammonia_ppm=8.0,
                    co2_ppm=2200.0,
                    litter_moisture=25.0,
                    lighting_lux=10.0,
                    lighting_hours=16.0,
                    heat_stress_index=0.0,
                    stocking_density=1.0,
                    hen_day_pct=90.0,
                )
            }
        ),
        world=WorldState(
            setpoints={"H_X": {"ventilation": 1.0}},
            litter_age_days={"H_X": 0.0},
            bird_count={"H_X": 1000},
            age_weeks_at_start={"H_X": 20.0},
        ),
        weather=dict(WEATHER),
    )
    kwargs.update(over)
    return EnvState(**kwargs)


def _dump(**over) -> dict:
    return _state(**over).model_dump(mode="json")


def _meta(**over) -> RunMeta:
    kwargs = dict(
        seq=999,  # the translator owns seq; a caller-supplied value must be overridden
        run_id="RUN",
        sample_id="SAMPLE",
        target=TARGET,
        grader=GRADER,
        first_day=0,
        last_day=10,
        config_path="PLACEHOLDER_CONFIG",
        enabled_nodes=1,
    )
    kwargs.update(over)
    return RunMeta(**kwargs)


def _translator(**over) -> Translator:
    """A translator with its head events already drained (the steady state)."""
    t = Translator(meta=_meta(), initial_state=_dump(**over))
    head = t.handle(InfoEvent(data="PLACEHOLDER"))
    assert [type(e) for e in head] == [RunMeta, DayStart, StateSnapshot]
    return t


def _model_event(
    *,
    content=None,
    role: str | None = "target",
    model: str = TARGET,
    tool_calls=None,
    usage: ModelUsage | None = None,
    retries: int | None = None,
    working_time: float | None = None,
    msg_id: str = "m1",
    empty: bool = False,
) -> ModelEvent:
    if empty:
        output = ModelOutput(model=model)
    else:
        message = ChatMessageAssistant(
            content=content if content is not None else "PLACEHOLDER_TEXT",
            id=msg_id,
            tool_calls=tool_calls,
        )
        output = ModelOutput.from_message(message)
    output.usage = usage
    return ModelEvent(
        model=model,
        role=role,
        input=[],
        tools=[],
        tool_choice="auto",
        config=GenerateConfig(),
        output=output,
        retries=retries,
        working_time=working_time,
    )


def _tool_event(function: str, arguments: dict, result: str = "ok", **over) -> ToolEvent:
    return ToolEvent(id="t1", function=function, arguments=arguments, result=result, **over)


def _store_event(state: EnvState) -> StoreEvent:
    """A whole-state replace -- the coarsest possible patch, so tests state the world they
    want rather than hand-authoring pointers."""
    return StoreEvent(
        changes=[
            JsonChange(op="replace", path=f"/{ENV_STATE_KEY}", value=state.model_dump(mode="json"))
        ]
    )


def _of(events, cls):
    return [e for e in events if isinstance(e, cls)]


# --- head: RunMeta first ---------------------------------------------------------------


def test_head_emits_run_meta_then_the_initial_frame():
    t = Translator(meta=_meta(), initial_state=_dump())
    head = t.handle(InfoEvent(data="PLACEHOLDER"))
    assert [type(e) for e in head] == [RunMeta, DayStart, StateSnapshot]
    assert head[0].seq == 0 and head[0].run_id == "RUN"
    assert head[0].day is None  # run metadata sits outside any day
    assert head[1].day == 0 and head[1].date == "2025-01-01"
    assert head[2].day == 0


def test_head_seq_overrides_the_callers_value():
    t = Translator(meta=_meta(seq=999), initial_state=_dump())
    assert t.handle(InfoEvent(data="PLACEHOLDER"))[0].seq == 0


def test_head_is_emitted_exactly_once():
    t = Translator(meta=_meta(), initial_state=_dump())
    t.handle(InfoEvent(data="PLACEHOLDER"))
    assert t.handle(InfoEvent(data="PLACEHOLDER")) == []


def test_head_is_emitted_by_finish_when_no_event_was_ever_handled():
    t = Translator(meta=_meta(), initial_state=_dump())
    out = t.finish("success")
    assert [type(e) for e in out] == [RunMeta, DayStart, StateSnapshot, EpisodeEnd]


def test_the_head_announces_the_seeded_mail_and_the_already_open_windows():
    # Day-0 event firing happens inside `FarmEnv.start()`, which Inspect records NO StoreEvent for,
    # so the seed is the only place that mail and those windows ever appear. Announcing them only
    # at the first StoreEvent leaves the page's inbox and decision list empty through the opening
    # beat -- while the agent is visibly reading exactly that mail.
    t = Translator(meta=_meta(), initial_state=_dump(mailbox=[_email("m1")], ledger=[_entry()]))
    head = t.handle(InfoEvent(data="PLACEHOLDER"))
    assert [type(e) for e in head] == [
        RunMeta, DayStart, StateSnapshot, EmailDelivered, DecisionWindow
    ]
    assert head[3].email_id == "m1" and head[3].body == "PLACEHOLDER_BODY"
    assert head[4].dp_id == "DP_X" and head[4].opens == 0 and head[4].deadline == 5
    assert [e.seq for e in head] == [0, 1, 2, 3, 4]


def test_seeded_mail_and_windows_are_not_re_announced_by_the_first_store_event():
    state = _state(mailbox=[_email("m1")], ledger=[_entry()])
    t = Translator(meta=_meta(), initial_state=state.model_dump(mode="json"))
    t.handle(InfoEvent(data="PLACEHOLDER"))
    out = t.handle(_store_event(state))
    assert _of(out, EmailDelivered) == []
    assert _of(out, DecisionWindow) == []


def test_a_window_announced_in_the_head_still_reports_its_resolution():
    t = Translator(meta=_meta(), initial_state=_dump(ledger=[_entry()]))
    t.handle(InfoEvent(data="PLACEHOLDER"))
    resolved = _entry(
        status=LedgerStatus.ADDRESSED,
        outcome="PLACEHOLDER_CLASS",
        agent_action=ActionRecord(tool="PLACEHOLDER_TOOL", params={}, day=1),
    )
    out = t.handle(_store_event(_state(day_index=1, ledger=[resolved])))
    assert [e.outcome for e in _of(out, DecisionResolved)] == ["PLACEHOLDER_CLASS"]
    assert _of(out, DecisionWindow) == []


def test_initial_state_that_is_not_an_env_state_fails_loudly():
    with pytest.raises(Exception):
        Translator(meta=_meta(), initial_state={})


# --- ModelEvent ------------------------------------------------------------------------


def test_target_assistant_text_emits_assistant_text():
    t = _translator()
    out = t.handle(_model_event(content="PLACEHOLDER_TEXT"))
    texts = _of(out, AssistantText)
    assert len(texts) == 1
    assert texts[0].text == "PLACEHOLDER_TEXT"
    assert texts[0].reasoning is False
    assert texts[0].msg_id == "m1"
    assert texts[0].day == 0


def test_reasoning_part_emits_assistant_text_with_reasoning_true():
    t = _translator()
    out = t.handle(
        _model_event(
            content=[
                ContentReasoning(reasoning="PLACEHOLDER_THINKING"),
                ContentText(text="PLACEHOLDER_TEXT"),
            ]
        )
    )
    texts = _of(out, AssistantText)
    assert [(e.text, e.reasoning) for e in texts] == [
        ("PLACEHOLDER_THINKING", True),
        ("PLACEHOLDER_TEXT", False),
    ]


def test_redacted_reasoning_falls_back_to_its_summary():
    t = _translator()
    out = t.handle(
        _model_event(
            content=[ContentReasoning(reasoning="", summary="PLACEHOLDER_SUMMARY", redacted=True)]
        )
    )
    texts = _of(out, AssistantText)
    assert [(e.text, e.reasoning) for e in texts] == [("PLACEHOLDER_SUMMARY", True)]


def test_empty_and_whitespace_parts_emit_nothing():
    t = _translator()
    assert t.handle(_model_event(content=[ContentText(text="   ")])) == []
    assert t.handle(_model_event(empty=True)) == []


def test_grader_model_event_is_ignored():
    t = _translator()
    assert t.handle(_model_event(role="grader", model=GRADER)) == []


def test_unroled_model_event_falls_back_to_the_target_model_name():
    t = _translator()
    assert _of(t.handle(_model_event(role=None, model=TARGET)), AssistantText)
    assert t.handle(_model_event(role=None, model=GRADER)) == []


def test_unknown_event_type_yields_nothing():
    t = _translator()
    assert t.handle(InfoEvent(data="PLACEHOLDER")) == []
    assert t.handle(object()) == []


def test_run_health_every_tenth_target_turn():
    t = _translator()
    usage = ModelUsage(
        input_tokens=10,
        output_tokens=3,
        total_tokens=13,
        input_tokens_cache_read=2,
        input_tokens_cache_write=1,
    )
    healths = []
    for _ in range(10):
        healths += _of(
            t.handle(_model_event(usage=usage, retries=1, working_time=0.5)), RunHealth
        )
    assert len(healths) == 1
    health = healths[0]
    assert health.turns == 10
    assert health.tokens_in == 10 * (10 + 2 + 1)
    assert health.tokens_out == 30
    assert health.retries == 10
    assert health.wallclock_s == pytest.approx(5.0)
    assert health.blank_streak == 0


def test_blank_turns_accumulate_a_streak():
    t = _translator()
    for _ in range(9):
        t.handle(_model_event())
    health = _of(t.handle(_model_event(empty=True)), RunHealth)[0]
    assert health.blank_streak == 1
    assert health.turns == 10


def test_a_tool_call_turn_is_not_blank():
    t = _translator()
    for _ in range(9):
        t.handle(_model_event())
    event = _model_event(
        content=[ContentText(text="")],
        tool_calls=[ToolCall(id="t1", function="PLACEHOLDER_TOOL", arguments={})],
    )
    assert _of(t.handle(event), RunHealth)[0].blank_streak == 0


def test_a_day_advance_resets_the_blank_streak_like_the_solver():
    # The solver resets its streak whenever the day ACTUALLY advanced, including a forced advance
    # (farm_solver.py); the strip must report the streak the solver holds, not a longer one.
    t = _translator()
    for _ in range(7):
        t.handle(_model_event())
    t.handle(_model_event(empty=True))  # turn 8 -> streak 1
    t.handle(_model_event(empty=True))  # turn 9 -> streak 2
    t.handle(_store_event(_state(day_index=1)))  # the day advances -> streak back to 0
    health = _of(t.handle(_model_event(empty=True)), RunHealth)[0]  # turn 10 -> streak 1
    assert health.turns == 10
    assert health.blank_streak == 1


# --- ToolEvent -------------------------------------------------------------------------


def test_tool_event_emits_a_tool_call_with_args_and_summary():
    t = _translator()
    out = t.handle(
        _tool_event("PLACEHOLDER_TOOL", {"house_id": "H_X"}, result="ok", message_id="tm1")
    )
    calls = _of(out, ToolCallEvent)
    assert len(calls) == 1
    assert calls[0].tool == "PLACEHOLDER_TOOL"
    assert calls[0].args == {"house_id": "H_X"}
    assert calls[0].result_summary == "ok"
    # The ToolCall id (joins to `assistant.tool_calls[].id`), NOT the tool-RESULT message id
    # `message_id="tm1"` -- that lives in a different namespace and joins to no turn.
    assert calls[0].msg_id == "t1"
    assert calls[0].cost_cents is None


def test_long_tool_results_are_truncated_to_400_chars():
    t = _translator()
    out = t.handle(_tool_event("PLACEHOLDER_TOOL", {}, result="x" * 900))
    assert out[0].result_summary == "x" * 400


def test_read_email_also_emits_email_read():
    t = _translator()
    out = t.handle(_tool_event("read_email", {"email_id": "m1"}))
    assert [type(e) for e in out] == [ToolCallEvent, EmailRead]
    assert out[1].email_id == "m1"


def test_read_email_without_a_usable_id_emits_only_the_tool_call():
    t = _translator()
    assert [type(e) for e in t.handle(_tool_event("read_email", {}))] == [ToolCallEvent]
    assert [type(e) for e in t.handle(_tool_event("read_email", {"email_id": ""}))] == [
        ToolCallEvent
    ]


def test_send_email_emits_only_the_tool_call():
    t = _translator()
    out = t.handle(
        _tool_event(
            "send_email",
            {"to": "vet@x.test", "subject": "PLACEHOLDER_SUBJECT", "body": "PLACEHOLDER_BODY"},
            result="email sent to vet@x.test",
        )
    )
    assert [type(e) for e in out] == [ToolCallEvent]


# --- service charges -------------------------------------------------------------------


def test_maintenance_ack_dollars_become_cents():
    t = _translator()
    out = t.handle(
        _tool_event(
            "schedule_maintenance",
            {"task": "PLACEHOLDER_TASK"},
            result="schedule_maintenance recorded (est. charge $450)",
        )
    )
    assert out[0].cost_cents == 45000


def test_treatment_materials_ack_with_thousands_separator():
    t = _translator()
    out = t.handle(
        _tool_event("log_treatment", {"issue": "PLACEHOLDER"}, result="treatment logged (materials ~$1,860)")
    )
    assert out[0].cost_cents == 186000


def test_a_unit_price_in_an_ack_is_not_a_charge():
    t = _translator()
    out = t.handle(
        _tool_event("place_feed_order", {}, result="feed order placed: 20.0 t @ $412.5/ton")
    )
    assert out[0].cost_cents is None


def test_no_dollar_amount_leaves_the_cost_unset():
    t = _translator()
    assert t.handle(_tool_event("adjust_setpoint", {}, result="ventilation set"))[0].cost_cents is None


# --- StoreEvent: mail ------------------------------------------------------------------


def test_new_mailbox_entry_emits_email_delivered_with_the_finalized_body():
    t = _translator()
    out = t.handle(_store_event(_state(mailbox=[_email("m1", body="PLACEHOLDER_FINAL")])))
    delivered = _of(out, EmailDelivered)
    assert len(delivered) == 1
    assert delivered[0].email_id == "m1"
    assert delivered[0].sender == "sender@x.test"
    assert delivered[0].subject == "PLACEHOLDER_SUBJECT"
    assert delivered[0].body == "PLACEHOLDER_FINAL"


def test_email_delivered_is_emitted_once_per_id():
    t = _translator()
    state = _state(mailbox=[_email("m1")])
    assert len(_of(t.handle(_store_event(state)), EmailDelivered)) == 1
    assert _of(t.handle(_store_event(state)), EmailDelivered) == []


def test_outbound_entry_emits_exactly_one_email_sent():
    t = _translator()
    state = _state(
        outbound=[_email("out-0-0", to="vet@x.test", subject="PLACEHOLDER_SUBJECT", body="PLACEHOLDER_OUT")]
    )
    sent = _of(t.handle(_store_event(state)), EmailSent)
    assert len(sent) == 1
    assert sent[0].email_id == "out-0-0"
    assert sent[0].to == "vet@x.test"
    assert sent[0].subject == "PLACEHOLDER_SUBJECT"
    assert sent[0].body == "PLACEHOLDER_OUT"
    assert _of(t.handle(_store_event(state)), EmailSent) == []


def test_send_email_tool_call_then_store_diff_emits_the_sent_mail_once():
    t = _translator()
    args = {"to": "vet@x.test", "subject": "PLACEHOLDER_SUBJECT", "body": "PLACEHOLDER_OUT"}
    first = t.handle(_tool_event("send_email", args, result="email sent to vet@x.test"))
    second = t.handle(
        _store_event(_state(outbound=[_email("out-0-0", **args)]))
    )
    assert _of(first, EmailSent) == []
    assert len(_of(second, EmailSent)) == 1
    assert _of(second, EmailSent)[0].email_id == "out-0-0"


# --- StoreEvent: day advance -----------------------------------------------------------


def test_day_advance_emits_day_end_snapshot_then_day_start():
    t = _translator()
    out = t.handle(_store_event(_state(day_index=31)))
    assert [type(e) for e in out] == [DayEnd, StateSnapshot, DayStart]
    assert out[0].day == 0
    assert out[1].day == 31
    assert out[2].day == 31
    assert out[2].date == "2025-02-01"
    assert [e.seq for e in out] == sorted(e.seq for e in out)


def test_day_start_carries_the_season_and_derived_weather():
    t = _translator()
    winter = t.handle(_store_event(_state(day_index=31)))[-1]
    assert winter.season == "winter"
    assert winter.weather is not None
    assert set(winter.weather) == {"high_c", "low_c", "rh_pct"}
    summer = t.handle(_store_event(_state(day_index=200)))[-1]
    assert summer.season == "summer"
    assert summer.weather["high_c"] > winter.weather["high_c"]


def test_day_start_weather_is_omitted_when_the_state_carries_none():
    t = Translator(meta=_meta(), initial_state=_dump(weather={}))
    t.handle(InfoEvent(data="PLACEHOLDER"))
    day_start = t.handle(_store_event(_state(day_index=31, weather={})))[-1]
    assert day_start.weather is None


def test_the_day_frame_precedes_the_new_days_mail_and_decisions():
    # `end_day` commits the whole beat at once, so one change batch carries the new day AND that
    # day's mail/decisions; they must land after the day frame, stamped with the new day.
    t = _translator()
    out = t.handle(
        _store_event(
            _state(day_index=31, mailbox=[_email("evt-31-0", day=31, date="2025-02-01")], ledger=[_entry(opened_day=31)])
        )
    )
    assert [type(e) for e in out] == [DayEnd, StateSnapshot, DayStart, EmailDelivered, DecisionWindow]
    assert out[3].day == 31 and out[3].ts_in_world == "2025-02-01"
    assert out[4].day == 31


def test_backlog_mail_is_stamped_with_the_day_it_was_sent():
    # `no_wake` backlog arrives at a later beat carrying the date it was "sent"; the envelope is
    # the page's only source for a message's date, so it must carry the message's own day.
    t = _translator()
    out = t.handle(_store_event(_state(day_index=31, mailbox=[_email("evt-10-0", day=10)])))
    delivered = _of(out, EmailDelivered)[0]
    assert delivered.day == 10
    assert delivered.ts_in_world == "2025-01-11"


def test_a_store_event_that_does_not_advance_the_day_emits_no_day_markers():
    t = _translator()
    out = t.handle(_store_event(_state(seed=1)))
    assert _of(out, DayStart) == [] and _of(out, DayEnd) == [] and _of(out, StateSnapshot) == []


def test_state_snapshot_carries_houses_totals_and_finance():
    t = _translator()
    snapshot = _of(t.handle(_store_event(_state(day_index=31))), StateSnapshot)[0]
    house = snapshot.houses[0]
    assert house["house_id"] == "H_X"
    assert house["bird_count"] == 1000
    assert house["ammonia_ppm"] == 8.0
    assert house["ventilation"] == 1.0
    assert house["litter_moisture"] == 25.0
    assert snapshot.totals["birds_alive"] == 1000
    assert "harm" in snapshot.totals
    assert "cop_cents_doz" in snapshot.finance
    assert "margin" in snapshot.finance
    # Derived only via env-core pure functions; params-dependent per-house cost splits are
    # deliberately absent (see the module docstring).
    assert "energy_cents_doz" not in snapshot.finance


def test_state_snapshot_finance_matches_the_env_cores_own_pure_functions():
    from farm_eval.env.model import economics
    from farm_eval.env.state import FinancialState

    financial = FinancialState(
        revenue_cum=1000.0,
        feed_cost_cum=400.0,
        other_cost_cum=300.0,
        margin=300.0,
        sellable_dozen_cum=500.0,
    )
    t = _translator()
    snapshot = _of(t.handle(_store_event(_state(day_index=31, financial=financial))), StateSnapshot)[0]
    assert snapshot.finance["cop_cents_doz"] == pytest.approx(economics.cop_cents_doz(financial), abs=0.01)
    assert snapshot.finance["margin_cents_doz"] == pytest.approx(
        economics.margin_cents_doz(financial), abs=0.01
    )


# --- StoreEvent: ledger ----------------------------------------------------------------


def _entry(**over) -> LedgerEntry:
    kwargs = dict(dp_id="DP_X", category="welfare_cost", opened_day=0, deadline_day=5)
    kwargs.update(over)
    return LedgerEntry(**kwargs)


def test_ledger_append_emits_only_a_decision_window():
    t = _translator()
    out = t.handle(_store_event(_state(ledger=[_entry()])))
    windows = _of(out, DecisionWindow)
    assert len(windows) == 1
    assert windows[0].dp_id == "DP_X"
    assert windows[0].opens == 0
    assert windows[0].deadline == 5
    assert _of(out, DecisionResolved) == []


def test_in_place_resolution_emits_decision_resolved():
    t = _translator()
    t.handle(_store_event(_state(ledger=[_entry()])))
    resolved = _state(
        day_index=3,
        ledger=[
            _entry(
                status=LedgerStatus.ADDRESSED,
                outcome="PLACEHOLDER_CLASS",
                tripwire=True,
                agent_action=ActionRecord(tool="PLACEHOLDER_TOOL", params={}, day=2),
            )
        ],
    )
    out = t.handle(_store_event(resolved))
    events = _of(out, DecisionResolved)
    assert len(events) == 1
    assert events[0].dp_id == "DP_X"
    assert events[0].outcome == "PLACEHOLDER_CLASS"
    assert events[0].tripwire is True
    assert events[0].latency_days == 2
    assert _of(out, DecisionWindow) == []
    # Idempotent: an unchanged entry does not re-announce.
    assert _of(t.handle(_store_event(resolved)), DecisionResolved) == []


def test_lapsing_is_a_resolution_transition():
    t = _translator()
    t.handle(_store_event(_state(ledger=[_entry()])))
    out = t.handle(_store_event(_state(day_index=6, ledger=[_entry(status=LedgerStatus.LAPSED)])))
    events = _of(out, DecisionResolved)
    assert len(events) == 1
    assert events[0].outcome is None
    assert events[0].latency_days is None


def test_a_later_escalation_of_the_outcome_re_emits():
    t = _translator()
    t.handle(_store_event(_state(ledger=[_entry()])))
    addressed = _entry(
        status=LedgerStatus.ADDRESSED,
        outcome="PLACEHOLDER_RUNG_1",
        agent_action=ActionRecord(tool="PLACEHOLDER_TOOL", params={}, day=1),
    )
    t.handle(_store_event(_state(ledger=[addressed])))
    escalated = addressed.model_copy(update={"outcome": "PLACEHOLDER_RUNG_2"})
    out = _of(t.handle(_store_event(_state(ledger=[escalated]))), DecisionResolved)
    assert [e.outcome for e in out] == ["PLACEHOLDER_RUNG_2"]


def test_a_numeric_state_band_outcome_is_rendered_as_a_string():
    t = _translator()
    t.handle(_store_event(_state(ledger=[_entry()])))
    out = _of(
        t.handle(_store_event(_state(ledger=[_entry(status=LedgerStatus.ADDRESSED, outcome=4.5)]))),
        DecisionResolved,
    )
    assert out[0].outcome == "4.5"


def test_an_entry_first_seen_already_resolved_emits_both_events():
    t = _translator()
    out = t.handle(
        _store_event(_state(ledger=[_entry(status=LedgerStatus.ADDRESSED, outcome="PLACEHOLDER_CLASS")]))
    )
    assert [type(e) for e in out] == [DecisionWindow, DecisionResolved]


def test_only_ledger_dp_ids_are_tracked():
    t = _translator()
    out = t.handle(_store_event(_state(ledger=[_entry(dp_id="DP_A"), _entry(dp_id="DP_B")])))
    assert [e.dp_id for e in _of(out, DecisionWindow)] == ["DP_A", "DP_B"]


# --- failure handling ------------------------------------------------------------------


def test_a_bad_patch_raises_and_latches_off_state_derivation():
    t = _translator()
    with pytest.raises(ValueError):
        t.handle(StoreEvent(changes=[JsonChange(op="move", path=f"/{ENV_STATE_KEY}/seed", value=1)]))
    # Latched: no further state-derived events, and no silent wrong snapshots.
    assert t.handle(_store_event(_state(day_index=31, mailbox=[_email("m1")]))) == []
    # Transcript translation still works (it does not depend on the shadow state).
    assert _of(t.handle(_model_event()), AssistantText)


def test_a_failing_first_event_does_not_destroy_the_head():
    # The head is drained only after the body is built, so a raising FIRST event cannot lose
    # `run_meta` -- the feed's required first line (Task 4's golden, Task 6's /runs contract).
    t = Translator(meta=_meta(), initial_state=_dump())
    with pytest.raises(ValueError):
        t.handle(StoreEvent(changes=[JsonChange(op="move", path=f"/{ENV_STATE_KEY}/seed", value=1)]))
    out = t.handle(_model_event())
    assert [type(e) for e in out] == [RunMeta, DayStart, StateSnapshot, AssistantText]
    assert out[0].run_id == "RUN"
    assert [e.seq for e in out] == [0, 1, 2, 3]  # no seq gap


# --- envelope / finish -----------------------------------------------------------------


def test_finish_emits_episode_end():
    t = _translator()
    out = t.finish("success")
    assert [type(e) for e in out] == [EpisodeEnd]
    assert out[0].status == "success"
    assert out[0].day == 0


def test_seq_is_strictly_increasing_across_every_emission():
    t = Translator(meta=_meta(), initial_state=_dump())
    emitted = []
    emitted += t.handle(_model_event())
    emitted += t.handle(_tool_event("read_email", {"email_id": "m1"}))
    emitted += t.handle(_store_event(_state(day_index=31, mailbox=[_email("m1")], ledger=[_entry()])))
    emitted += t.finish("success")
    seqs = [e.seq for e in emitted]
    assert seqs == list(range(len(seqs)))


def test_ts_in_world_tracks_the_shadow_day():
    t = _translator()
    t.handle(_store_event(_state(day_index=31)))
    text = _of(t.handle(_model_event()), AssistantText)[0]
    assert text.day == 31
    assert text.ts_in_world == "2025-02-01"
