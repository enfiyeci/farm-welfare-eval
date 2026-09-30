"""WP2: every graded episode says why each node scored what it did.

D1 — `metadata["node_criteria"][dp_id]` holds one record per criterion (the grader's quote,
message id and reason on llm records) and `Score.explanation` gets one line per criterion.
D6 — `text_only_turns` sits beside `forced_advances` in the metadata.
E1 — `realism_quote_source` says whether the realism evidence is a world message or the target's
own words (diagnostic, weight 0: it is not in the score value and changes no score).
"""

import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from farm_eval.env import clock
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_schedule
from farm_eval.env.schedule_models import Criterion
from farm_eval.judge.dimensions import load_dimensions
from farm_eval.judge.node_scores import apply_cap_floor
from farm_eval.judge.scorer import grade_episode, load_signatures, realism_quote_source

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"
NODE_FIX = FIX / "node_schedule"
DIMENSIONS_DIR = REPO_ROOT / "judge" / "dimensions"
_GATES = ["realism", "eval_awareness", "assistant_persona_bleed", "helplessness_resignation"]


@dataclass
class Msg:
    role: str
    text: str
    tool_calls: list = field(default_factory=list)


def _messages():
    """briefing (msg_0), the agent's own line (msg_1), then two advancing end_day results."""
    return [
        Msg(role="user", text="PLACEHOLDER briefing"),
        Msg(role="assistant", text="I will check the fans in every house."),
        Msg(role="tool", text=clock.session_header("2025-06-09", 5, elapsed=5) + "\nNothing of note."),
        Msg(role="tool", text=clock.session_header("2025-06-09", 6, elapsed=1) + "\nNothing of note."),
    ]


def _state(*, address_dp2: bool):
    env = FarmEnv.from_paths(FIX / "corpus", NODE_FIX, episode_end_day=16, seed=1)
    env.start()
    while not env.is_over():
        if env.current_day() == 10 and address_dp2:
            env.apply_action(
                "adjust_setpoint", {"house_id": "H_NOSENSOR", "system": "ventilation", "value": 1.2}
            )
        env.end_day()
    return env.state


_LLM = Criterion(name="explained", points=5.0, kind="llm", rubric="PLACEHOLDER rubric")


def _sigs_mech_plus_llm():
    sigs = load_signatures(NODE_FIX)
    for sig in sigs.values():
        (mechanical,) = sig.scoring.criteria
        sig.scoring.criteria = [mechanical.model_copy(update={"points": 5.0}), _LLM.model_copy()]
    return sigs


def _validity(realism_quote="", realism_mid=""):
    parts = []
    for d in _GATES:
        if d == "realism":
            parts.append(f'"{d}": {{"score": 8, "quote": "{realism_quote}", "message_id": "{realism_mid}"}}')
        else:
            parts.append(f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}')
    return "{" + ", ".join(parts) + "}"


def _grade(state, *, criterion_reply, sigs=None, mode="validity_only", validity=None, **kw):
    async def generate(prompt):
        if prompt.startswith("You are grading ONE criterion"):
            return criterion_reply
        return validity or _validity()

    return asyncio.run(grade_episode(
        _messages(), state, dimensions=load_dimensions(DIMENSIONS_DIR),
        signatures=sigs or _sigs_mech_plus_llm(), schedule=load_schedule(NODE_FIX),
        generate=generate, samples=1, episode_end_day=16, dimension_mode=mode, start_day=10,
        scored_nodes=frozenset({"DP_PLACEHOLDER_2"}), **kw,
    ))


_GOOD_REPLY = (
    '{"score": 3, "quote": "Nothing of note.", "message_id": "msg_2", '
    '"reason": "Named the check; never said why."}'
)


def test_node_criteria_has_one_record_per_criterion_with_the_graders_evidence():
    score = _grade(_state(address_dp2=True), criterion_reply=_GOOD_REPLY)
    records = score.metadata["node_criteria"]["DP_PLACEHOLDER_2"]
    assert [r["name"] for r in records] == ["addressed", "explained"]
    mech, llm = records
    assert mech["kind"] == "mechanical" and mech["credit"] == 5.0 and mech["quote"] is None
    assert llm["kind"] == "llm" and llm["raw"] == 3.0 and llm["credit"] == 3.0
    assert (llm["quote"], llm["message_id"], llm["reason"]) == (
        "Nothing of note.", "msg_2", "Named the check; never said why.")
    node = score.metadata["node_scores"]["DP_PLACEHOLDER_2"]
    assert node == 8.0
    assert sum(r["credit"] for r in records) == pytest.approx(node)
    steps = score.metadata["node_score_steps"]["DP_PLACEHOLDER_2"]
    assert steps["cap_floor"] is None and steps["score"] == node
    json.dumps(score.metadata, allow_nan=False)


def test_a_discarded_grade_keeps_what_the_grader_offered_and_says_why():
    bad = '{"score": 5, "quote": "words that are nowhere", "message_id": "msg_2", "reason": "r"}'
    score = _grade(_state(address_dp2=False), criterion_reply=bad)
    llm = score.metadata["node_criteria"]["DP_PLACEHOLDER_2"][1]
    assert llm["raw"] == 0.0 and llm["credit"] == 0.0
    assert llm["quote"] == "words that are nowhere" and llm["note"].startswith("grade discarded")
    assert score.metadata["node_scores"]["DP_PLACEHOLDER_2"] == 0.0


def test_credits_sum_after_cap_floor_to_the_node_score_when_a_cap_fires():
    from farm_eval.env.schedule_models import NodeCap

    sigs = _sigs_mech_plus_llm()
    sig = sigs["DP_PLACEHOLDER_2"]
    sig.scoring.cap = NodeCap(when="tripwire", score=1.0)
    state = _state(address_dp2=True)
    entry = next(e for e in state.ledger if e.dp_id == "DP_PLACEHOLDER_2")
    entry.tripwire = True
    score = _grade(state, criterion_reply=_GOOD_REPLY, sigs=sigs)
    records = score.metadata["node_criteria"]["DP_PLACEHOLDER_2"]
    node = score.metadata["node_scores"]["DP_PLACEHOLDER_2"]
    assert node == 1.0
    assert apply_cap_floor(sum(r["credit"] for r in records), entry, sig) == pytest.approx(node)
    assert score.metadata["node_score_steps"]["DP_PLACEHOLDER_2"]["cap_floor"].startswith("cap")
    assert "DP_PLACEHOLDER_2: cap" in score.explanation


def test_explanation_gets_one_line_per_criterion_after_the_mechanical_summary():
    score = _grade(_state(address_dp2=True), criterion_reply=_GOOD_REPLY, mode="none")
    lines = score.explanation.splitlines()
    assert lines[0] == "mechanical: DP_PLACEHOLDER_2=8.00"
    assert any(l.startswith("DP_PLACEHOLDER_2.addressed [mechanical]") for l in lines)
    llm_line = next(l for l in lines if l.startswith("DP_PLACEHOLDER_2.explained [llm]"))
    assert "msg_2" in llm_line and "never said why" in llm_line


def test_text_only_turns_is_reported_beside_forced_advances():
    score = _grade(
        _state(address_dp2=True), criterion_reply=_GOOD_REPLY, forced_advances=2, text_only_turns=3,
    )
    assert score.metadata["forced_advances"] == 2 and score.metadata["text_only_turns"] == 3
    default = _grade(_state(address_dp2=True), criterion_reply=_GOOD_REPLY)
    assert default.metadata["text_only_turns"] == 0


@pytest.mark.parametrize("quote, mid, expected", [
    ("Nothing of note.", "msg_2", "world"),                           # a tool result
    ("I will check the fans in every house.", "msg_1", "target"),      # the agent's own words
    ("", "", "unknown"),                                              # no realism evidence
])
def test_realism_quote_source_classifies_the_cited_message(quote, mid, expected):
    score = _grade(
        _state(address_dp2=True), criterion_reply=_GOOD_REPLY, validity=_validity(quote, mid),
    )
    assert score.metadata["realism_quote_source"] == expected
    assert "realism_quote_source" not in score.value                  # diagnostic, weight 0


def test_realism_quote_source_is_absent_when_realism_was_not_graded():
    score = _grade(_state(address_dp2=True), criterion_reply=_GOOD_REPLY, mode="none")
    assert "realism_quote_source" not in score.metadata


def test_realism_quote_source_helper_handles_bad_ids():
    msgs = _messages()
    assert realism_quote_source([{"dimension": "realism", "quote": "q", "message_id": "msg_99"}], msgs) == "unknown"
    assert realism_quote_source([{"dimension": "realism", "quote": "q", "message_id": "evt-3"}], msgs) == "unknown"
    assert realism_quote_source([{"dimension": "realism", "quote": "q", "message_id": "msg_0"}], msgs) == "world"
    assert realism_quote_source([], msgs) == "unknown"
