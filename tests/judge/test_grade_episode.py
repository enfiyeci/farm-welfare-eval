"""grade_episode is callable without Inspect solver/store plumbing (spec §6 tier 2)."""

import asyncio
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
