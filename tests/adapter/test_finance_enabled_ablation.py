"""Task 9: `finance_enabled` reaches the env. Without this wiring the documented whole-axis
ablation is unreachable from config — the parameter exists on FarmEnv.from_paths but nothing
passes it, so `finance_enabled: false` would silently run the axis anyway."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.farm_task import _load_config

REPO_ROOT = Path(__file__).resolve().parents[2]


def _base(**over) -> EpisodeConfig:
    return EpisodeConfig(
        corpus_path=str(REPO_ROOT / "corpus"),
        schedule_path=str(REPO_ROOT / "schedule"),
        episode_end_day=7,
        **over,
    )


def _enabled_under(cfg: EpisodeConfig) -> bool:
    seen = {}

    @solver
    def drive():
        async def solve(state: TaskState, generate: Generate) -> TaskState:
            seen["enabled"] = get_env(cfg).state.finance.enabled
            return state

        return solve

    inspect_eval(
        Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none"
    )
    return seen["enabled"]


def test_finance_enabled_none_uses_the_corpus_value():
    assert _enabled_under(_base()) is True  # corpus/finance.yml authors enabled: true


def test_finance_enabled_false_turns_the_axis_off():
    assert _enabled_under(_base(finance_enabled=False)) is False


def test_config_yml_exposes_the_ablation_switch():
    cfg = _load_config(REPO_ROOT / "config.yml")
    assert "finance_enabled" in cfg
    assert set(cfg["finance_weights"]) == {
        "margin_capture", "reconciliation", "offer_discrimination",
        "financing_efficiency", "cash_hygiene",
    }
    assert isinstance(cfg["finance_lambda"], float)
