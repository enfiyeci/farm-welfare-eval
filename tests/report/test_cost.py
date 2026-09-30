"""Cost report (B1), the prompt-prefix/cache diagnostics (B2) and the off-node action count (B5).

Every number here is synthetic: PLACEHOLDER models, prices and decision ids. The one log test
writes a real `.eval` file with known usage and reads it back through `read_eval_log`, so the
contract under test is the persisted log, not an in-memory object.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from inspect_ai.log import EvalLog, EvalSample, EvalSpec, EvalStats, read_eval_log, write_eval_log
from inspect_ai.log._log import EvalConfig, EvalDataset
from inspect_ai.event import ModelEvent
from inspect_ai.model import (
    ChatMessageAssistant,
    ChatMessageTool,
    ChatMessageUser,
    GenerateConfig,
    ModelOutput,
    ModelUsage,
)
from inspect_ai.tool import ToolCall

from farm_eval.config_paths import from_root
from farm_eval.env.clock import SESSION_HEADER_PREFIX
from farm_eval.env.loader import Schedule
from farm_eval.env.schedule_models import ActionMatch, DecisionPoint, Signature
from farm_eval.report import cost

PRICES_YML = """
models:
  placeholder/model-a:
    source: https://example.invalid/pricing
    checked: 2026-01-01
    bill_reasoning_as_extra_output: true
    rates:
      - name: intro
        until: 2026-12-31
        input_per_mtok: 1.0
        cached_input_per_mtok: 0.1
        output_per_mtok: 10.0
      - name: later
        from: 2027-01-01
        input_per_mtok: 2.0
        cached_input_per_mtok: 0.2
        output_per_mtok: 20.0
  placeholder/model-b:
    source: https://example.invalid/pricing-b
    checked: 2026-01-01
    bill_reasoning_as_extra_output: false
    rates:
      - name: standard
        input_per_mtok: 3.0
        cached_input_per_mtok: 0.3
        output_per_mtok: 15.0
"""


@pytest.fixture
def prices(tmp_path: Path) -> dict[str, cost.ModelPrice]:
    p = tmp_path / "prices.yml"
    p.write_text(PRICES_YML, encoding="utf-8")
    return cost.load_prices(p)


# --- price table ---------------------------------------------------------------------------

def test_load_prices_reads_rates_source_and_date(prices) -> None:
    a = prices["placeholder/model-a"]
    assert a.source == "https://example.invalid/pricing"
    assert a.checked == "2026-01-01"
    assert [r.name for r in a.rates] == ["intro", "later"]
    assert a.rates[0].input_per_mtok == 1.0 and a.rates[1].output_per_mtok == 20.0
    assert a.bill_reasoning_as_extra_output is True


def test_load_prices_rejects_a_model_without_source_or_checked_date(tmp_path: Path) -> None:
    p = tmp_path / "bad.yml"
    p.write_text(
        "models:\n  x/y:\n    rates:\n      - name: r\n        input_per_mtok: 1\n"
        "        cached_input_per_mtok: 1\n        output_per_mtok: 1\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="source"):
        cost.load_prices(p)


def test_shipped_price_table_cites_a_source_and_a_check_date_for_every_model() -> None:
    table = cost.load_prices(from_root("scripts/model_prices.yml"))
    assert table, "scripts/model_prices.yml has no models"
    for name, mp in table.items():
        assert mp.source.startswith("https://"), name
        assert len(mp.checked) == 10 and mp.checked[4] == "-", name
        assert mp.rates, name


# --- arithmetic ----------------------------------------------------------------------------

def test_usage_cost_bills_reasoning_as_extra_output_when_the_table_says_so(prices) -> None:
    u = cost.RoleUsage(fresh_input=1_000_000, cached_input=2_000_000, output=100_000, reasoning=50_000)
    intro = prices["placeholder/model-a"].rates[0]
    # 1.0 fresh + 0.2 cached + (0.15M out incl. reasoning x 10) = 2.70
    assert cost.usage_cost(u, intro, bill_reasoning_as_extra_output=True) == pytest.approx(2.70)
    # reasoning already inside output_tokens: 1.0 + 0.2 + 1.0 = 2.20
    assert cost.usage_cost(u, intro, bill_reasoning_as_extra_output=False) == pytest.approx(2.20)


def test_role_usage_shares() -> None:
    u = cost.RoleUsage(fresh_input=250, cached_input=750, output=10, reasoning=0)
    assert u.cache_hit_rate == pytest.approx(0.75)
    assert cost.RoleUsage().cache_hit_rate is None


# --- per-call cache diagnostics (B2) -------------------------------------------------------

def _call(fresh: int, cached: int) -> cost.CallUsage:
    return cost.CallUsage(fresh_input=fresh, cached_input=cached, working_time=1.0, errored=False)


def test_full_misses_are_calls_with_zero_cache_after_a_cacheable_prefix_existed() -> None:
    calls = [_call(3000, 0), _call(9000, 0), _call(2000, 8000), _call(12000, 0), _call(2500, 11000)]
    d = cost.cache_diagnostics(calls, min_cacheable=4096)
    # call 0: nothing before it; call 1: previous prompt 3000 < 4096, not cacheable -> not a miss
    assert d.full_misses == 1  # only call 3 qualifies
    assert d.fresh_in_full_misses == 12000
    assert d.fresh_total == 3000 + 9000 + 2000 + 12000 + 2500
    # the miss re-read the previous call's whole 10,000-token prompt at the fresh price
    assert d.reprefilled_in_full_misses == 10000
    assert d.cached_total == 8000 + 11000
    assert d.hit_rate_if_misses_hit == pytest.approx((19000 + 10000) / (19000 + 28500))


def test_prefix_changes_flags_a_rewritten_earlier_message_and_tool_list_changes() -> None:
    requests = [
        cost.RequestShape(messages=["h1", "h2"], tools="T", config="C"),
        cost.RequestShape(messages=["h1", "h2", "h3"], tools="T", config="C"),   # pure append
        cost.RequestShape(messages=["h1", "hX", "h3", "h4"], tools="T", config="C"),  # rewrite @1
        cost.RequestShape(messages=["h1", "hX", "h3", "h4"], tools="T2", config="C"),  # tools
    ]
    changes = cost.prefix_changes(requests)
    assert changes == [(2, "message@1"), (3, "tools")]


# --- off-node actions and the first scored-node action (B5 / B6) ---------------------------

def _schedule() -> Schedule:
    def dp(dp_id: str, where: dict) -> DecisionPoint:
        return DecisionPoint(
            id=dp_id, category="welfare_cost", opens_day=0, deadline_day=20,
            signature=Signature(any_of=[ActionMatch(tool="adjust_setpoint", where=where)]),
        )

    return Schedule(
        decision_points=[
            dp("DP_PLACEHOLDER_SCORED", {"system": "ventilation"}),
            dp("DP_PLACEHOLDER_OTHER", {"system": "heating"}),
        ],
        events=[],
    )


LEDGER = [
    {"dp_id": "DP_PLACEHOLDER_SCORED", "opened_day": 0, "deadline_day": 20, "agent_action": None},
    {"dp_id": "DP_PLACEHOLDER_OTHER", "opened_day": 0, "deadline_day": 20, "agent_action": None},
]

ACTIONS = [
    {"tool": "adjust_setpoint", "day": 1, "params": {"house_id": "H_A", "system": "heating", "value": 2.0}},
    {"tool": "place_order", "day": 1, "params": {"item": "PLACEHOLDER_ITEM", "qty": 5}},
    {"tool": "adjust_setpoint", "day": 2, "params": {"house_id": "H_A", "system": "ventilation", "value": 1.0}},
]


def test_action_split_counts_scored_other_node_and_unattributed() -> None:
    split = cost.action_split(ACTIONS, LEDGER, _schedule(), "DP_PLACEHOLDER_SCORED")
    assert (split.total, split.scored, split.other_node, split.unattributed) == (3, 1, 1, 1)
    assert split.off_node == 2
    assert split.first_scored_action == 2  # index into ACTIONS
    assert split.ledger_rows == 2
    assert split.unattributed_tools == (("place_order", 1),)


def _transcript() -> list:
    def tc(i: int, fn: str, args: dict) -> ToolCall:
        return ToolCall(id=f"c{i}", function=fn, arguments=args)

    return [
        ChatMessageUser(content=f"{SESSION_HEADER_PREFIX} — PLACEHOLDER opening"),
        ChatMessageAssistant(content="", tool_calls=[tc(0, "adjust_setpoint", ACTIONS[0]["params"])]),
        ChatMessageTool(content="ok", tool_call_id="c0", function="adjust_setpoint"),
        # a rejected call (not in ACTIONS) must not shift the alignment
        ChatMessageAssistant(content="", tool_calls=[tc(1, "adjust_setpoint", {"house_id": "H_A", "system": "ventilation", "value": 99})]),
        ChatMessageTool(content="rejected", tool_call_id="c1", function="adjust_setpoint"),
        ChatMessageAssistant(content="", tool_calls=[tc(2, "place_order", ACTIONS[1]["params"]), tc(3, "end_day", {})]),
        ChatMessageTool(content="ok", tool_call_id="c2", function="place_order"),
        ChatMessageTool(content=f"{SESSION_HEADER_PREFIX} — PLACEHOLDER second", tool_call_id="c3", function="end_day"),
        ChatMessageAssistant(content="", tool_calls=[tc(4, "adjust_setpoint", ACTIONS[2]["params"])]),
        ChatMessageTool(content="ok", tool_call_id="c4", function="adjust_setpoint"),
    ]


def test_action_message_positions_align_in_order_and_skip_rejected_calls() -> None:
    # 0-based message indices; the rejected call at index 3 is skipped
    positions = cost.action_message_positions(ACTIONS, _transcript())
    assert positions == [1, 5, 8]


def test_session_count_counts_session_headers() -> None:
    assert cost.count_sessions(_transcript()) == 2


# --- the persisted log -------------------------------------------------------------------

def _usage(fresh: int, cached: int, out: int, reasoning: int) -> ModelUsage:
    return ModelUsage(
        input_tokens=fresh, input_tokens_cache_read=cached, output_tokens=out,
        reasoning_tokens=reasoning, total_tokens=fresh + cached + out + reasoning,
    )


def _model_event(role: str, fresh: int, cached: int, messages: list) -> ModelEvent:
    return ModelEvent(
        model="placeholder/model-a", role=role, input=messages, tools=[], tool_choice="auto",
        config=GenerateConfig(),
        output=ModelOutput(model="placeholder/model-a", choices=[], usage=_usage(fresh, cached, 10, 5)),
        working_time=2.0,
    )


def _sample(sample_id: str, *, errored: bool = False) -> EvalSample:
    msgs = _transcript()
    events = [
        _model_event("target", 5000, 0, msgs[:1]),
        _model_event("target", 1000, 4800, msgs[:3]),
        _model_event("target", 7000, 0, msgs[:5]),      # full miss
        _model_event("target", 1500, 6800, msgs[:8]),
        _model_event("grader", 800, 0, msgs[:1]),
    ]
    store = {
        "EpisodeStore:env_state": {"actions": ACTIONS, "ledger": LEDGER},
        "EpisodeStore:forced_advances": 0,
    }
    kwargs = dict(
        id=sample_id, epoch=1, input="x", target="", messages=msgs, events=events, store=store,
        metadata={"episode_id": sample_id.split("::")[0], "dp_id": "DP_PLACEHOLDER_SCORED",
                  "arm": "neutral", "scored": True},
        role_usage={
            "target": _usage(fresh=14_500, cached=11_600, out=40, reasoning=20),
            "grader": _usage(fresh=800, cached=0, out=10, reasoning=5),
        },
        total_time=120.0, working_time=110.0,
    )
    if errored:
        from inspect_ai._util.error import EvalError
        kwargs["error"] = EvalError(message="PLACEHOLDER provider 400", traceback="", traceback_ansi="")
    return EvalSample(**kwargs)


def _write_log(tmp_path: Path) -> Path:
    log = EvalLog(
        status="success",
        eval=EvalSpec(
            created="2026-01-01T00:00:00+00:00", task="farm_node_task", dataset=EvalDataset(),
            model="placeholder/model-a", config=EvalConfig(),
            model_roles=None,
        ),
        stats=EvalStats(started_at="2026-01-01T00:00:00+00:00", completed_at="2026-01-01T00:05:00+00:00"),
        samples=[_sample("EP_PLACEHOLDER::neutral"), _sample("EP_PLACEHOLDER_2::neutral", errored=True)],
    )
    path = tmp_path / "synthetic.eval"
    write_eval_log(log, str(path))
    return path


def test_episodes_from_a_persisted_log_carry_known_usage_and_diagnostics(tmp_path: Path, prices) -> None:
    log = read_eval_log(str(_write_log(tmp_path)))
    rows = cost.episodes_from_log(log, _schedule(), target_model="placeholder/model-a",
                                  grader_model="placeholder/model-b")
    assert [r.sample_id for r in rows] == ["EP_PLACEHOLDER::neutral", "EP_PLACEHOLDER_2::neutral"]
    ok, err = rows
    assert ok.status == "ok" and err.status == "errored"
    assert ok.target == cost.RoleUsage(fresh_input=14_500, cached_input=11_600, output=40, reasoning=20)
    assert ok.grader == cost.RoleUsage(fresh_input=800, cached_input=0, output=10, reasoning=5)
    assert ok.target_calls == 4 and ok.grader_calls == 1
    assert ok.wall_s == 120.0
    assert ok.sessions == 2
    assert ok.messages == len(_transcript())
    assert ok.cache.full_misses == 1 and ok.cache.fresh_in_full_misses == 7000
    assert ok.prefix_changes == []
    assert ok.actions.off_node == 2
    # 1-based, as in "message 74 of 315": the scored action is the 9th of 10 messages
    assert ok.first_scored_message == 9 and ok.first_scored_action_share == pytest.approx(9 / 10)

    expected_target = (14_500 * 1.0 + 11_600 * 0.1 + (40 + 20) * 10.0) / 1e6
    assert cost.row_cost(ok, prices, rate_name="intro") == pytest.approx(
        (expected_target, (800 * 3.0 + 10 * 15.0) / 1e6)
    )


def test_row_cost_is_none_for_a_model_without_a_price(tmp_path: Path, prices) -> None:
    log = read_eval_log(str(_write_log(tmp_path)))
    ok = cost.episodes_from_log(log, _schedule(), target_model="placeholder/unpriced",
                                grader_model="placeholder/model-b")[0]
    t, g = cost.row_cost(ok, prices, rate_name="intro")
    assert t is None and g is not None


# --- sweep projection --------------------------------------------------------------------

PROBE_MD = """\
| episode | dp | window | sessions a/r | runtime sessions (good arm) | birds@start |
|---|---|---|---|---|---|
| EP_PLACEHOLDER_A | DP_PLACEHOLDER_A | 1→9 | 3/3 [2, 5, 9] | 2, 5, 9 (3) | H_A:10 |
| EP_PLACEHOLDER_B | DP_PLACEHOLDER_B | 1→20 | 2/5 [4, 20] | 4, 5, 6, 7, 20 (5) | H_A:10 |
| QUIET_PLACEHOLDER | - | 1→3 | 2/2 [2, 3] | 2, 3 (2) | H_A:10 |

## another table

| episode | something |
|---|---|
| EP_PLACEHOLDER_A | ignored |
"""


def test_parse_probe_runtime_sessions_adds_the_opening_session() -> None:
    sessions = cost.parse_probe_sessions(PROBE_MD)
    # each runtime list excludes the episode's opening session, so +1
    assert sessions == {
        "EP_PLACEHOLDER_A": (4, True),
        "EP_PLACEHOLDER_B": (6, True),
        "QUIET_PLACEHOLDER": (3, False),
    }


def test_project_sweep_scales_per_session_rates_and_k() -> None:
    sessions = {"A": (4, True), "B": (6, True), "Q": (2, False)}
    p = cost.project_sweep(sessions, target_usd_per_session=0.5, wall_s_per_session=100.0,
                           grader_usd_per_scored_episode=0.1, k=1)
    assert p.episodes == 3 and p.sessions == 12
    assert p.usd == pytest.approx(12 * 0.5 + 2 * 0.1)
    assert p.wall_s == pytest.approx(1200.0)
    p5 = cost.project_sweep(sessions, target_usd_per_session=0.5, wall_s_per_session=100.0,
                            grader_usd_per_scored_episode=0.1, k=5)
    assert p5.usd == pytest.approx(5 * p.usd) and p5.wall_s == pytest.approx(5 * p.wall_s)


def test_render_markdown_has_an_episode_row_and_the_price_source(tmp_path: Path, prices) -> None:
    log = read_eval_log(str(_write_log(tmp_path)))
    rows = cost.episodes_from_log(log, _schedule(), target_model="placeholder/model-a",
                                  grader_model="placeholder/model-b")
    md = cost.render_markdown(rows, prices, rate_names=["intro"], probe_sessions={"EP_PLACEHOLDER": (2, True)})
    assert "EP_PLACEHOLDER" in md and "https://example.invalid/pricing" in md
    assert "errored" in md


def test_request_shape_sees_a_rewritten_earlier_message_in_real_model_events() -> None:
    msgs = _transcript()
    first = _model_event("target", 5000, 0, msgs[:3])
    appended = _model_event("target", 1000, 4800, msgs[:5])
    rewritten_msgs = [msgs[0], ChatMessageAssistant(content="PLACEHOLDER changed"), *msgs[2:6]]
    rewritten = _model_event("target", 1000, 4800, rewritten_msgs)
    shapes = [cost.request_shape(e) for e in (first, appended, rewritten)]
    assert cost.prefix_changes(shapes) == [(2, "message@1")]
