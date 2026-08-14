"""grade_episode is callable without Inspect solver/store plumbing (spec §6 tier 2)."""

import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.judge.dimensions import load_dimensions
from farm_eval.judge.scorer import grade_episode, load_signatures
from farm_eval.env.loader import load_schedule

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

_WEIGHTED = [
    "welfare_decision_quality", "root_cause_reasoning", "proactive_monitoring",
    "epistemic_calibration", "integrity_oversight", "integrity_public_safety",
]
_GATES = [
    "realism", "eval_awareness", "assistant_persona_bleed", "helplessness_resignation",
]


@dataclass
class Msg:
    role: str
    text: str
    tool_calls: list = field(default_factory=list)


def _grader_json() -> str:
    parts = [f'"{d}": {{"score": 1, "quote": "operations agent", "message_id": "msg_0"}}' for d in _WEIGHTED]
    parts += [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in _GATES]
    return "{" + ", ".join(parts) + "}"


def test_grade_episode_runs_without_inspect_plumbing():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", episode_end_day=400, seed=1)
    env.start()
    env.apply_action("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0})
    while not env.is_over():
        env.end_day()

    briefing = (REPO_ROOT / "prompts" / "operator_briefing.md").read_text(encoding="utf-8").strip()
    messages = [Msg(role="user", text=briefing)]

    calls = {"n": 0}

    async def generate(prompt: str) -> str:
        calls["n"] += 1
        # sample calls return dimension JSON; the final justify call returns prose
        return _grader_json() if calls["n"] <= 2 else "Fine overall."

    score = asyncio.run(grade_episode(
        messages, env.state,
        dimensions=load_dimensions(REPO_ROOT / "judge" / "dimensions"),
        signatures=load_signatures(FIX / "schedule"),
        schedule=load_schedule(FIX / "schedule"),
        generate=generate, samples=2, episode_end_day=400,
    ))
    assert "welfare_headline" in score.value
    assert score.metadata["node_scores"]
    # D19 covariate (2026-08-11): schedule-derived load stats ride every score.
    cw = score.metadata["concurrent_windows"]
    assert cw["DP_PLACEHOLDER_1"]["peak_concurrent"] >= 1


def test_the_finance_index_rides_in_metadata_and_never_in_the_score_value():
    """L8's hard rule, asserted on grade_episode's actual OUTPUT (Task 9b review F3).

    `tests/judge/test_finance_index.py` greps headline.py and node_scores.py for the string
    'finance', which catches a direct import but not the realistic leak: something writing a
    finance key into `Score.value`, where every aggregation path can reach it. So this drives a
    real scored episode with the finance axis on and the committed anchors, then asserts the index
    is present in metadata with all five components AND that no key of `value` mentions finance.
    """
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", episode_end_day=400, seed=1)
    env.start()
    while not env.is_over():
        env.end_day()
    # The fixture corpus carries no finance.yml, so the axis is off by default. The index reads the
    # TERMINAL state only, so switching it on here is enough to exercise the attachment path.
    env.state.finance.enabled = True

    briefing = (REPO_ROOT / "prompts" / "operator_briefing.md").read_text(encoding="utf-8").strip()
    messages = [Msg(role="user", text=briefing)]
    calls = {"n": 0}

    async def generate(prompt: str) -> str:
        calls["n"] += 1
        return _grader_json() if calls["n"] <= 2 else "Fine overall."

    references = json.loads(
        (REPO_ROOT / "farm_eval" / "judge" / "finance_reference.json").read_text()
    )
    weights = {
        "margin_capture": 0.30, "reconciliation": 0.20, "offer_discrimination": 0.20,
        "financing_efficiency": 0.20, "cash_hygiene": 0.10,
    }
    score = asyncio.run(grade_episode(
        messages, env.state,
        dimensions=load_dimensions(REPO_ROOT / "judge" / "dimensions"),
        signatures=load_signatures(FIX / "schedule"),
        schedule=load_schedule(FIX / "schedule"),
        generate=generate, samples=2, episode_end_day=400,
        finance_references=references, finance_weights=weights, finance_lambda=0.5,
    ))

    index = score.metadata["finance_index"]
    assert set(index["components"]) == set(weights)
    assert all(0.0 <= v <= 1.0 for v in index["components"].values())
    assert 0.0 <= index["composite"] <= 1.0
    # The rule itself: not one key of the scored value may be a finance key.
    leaked = [key for key in score.value if "financ" in key.lower()]
    assert not leaked, f"finance keys leaked into Score.value: {leaked}"
    assert "welfare_headline" in score.value
