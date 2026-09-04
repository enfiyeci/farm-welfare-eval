"""The four daily-wake config keys flow from config.yml into EpisodeConfig and FarmEnv."""
from pathlib import Path

from farm_eval.adapter.context import EpisodeConfig, EpisodeStore
from farm_eval.farm_task import farm_task

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

BASE = {
    "corpus_path": str(FIX / "corpus"),
    "schedule_path": str(FIX / "schedule"),
    "briefing_path": str(REPO_ROOT / "prompts" / "operator_briefing.md"),
    "dimensions_dir": str(REPO_ROOT / "judge" / "dimensions"),
    "episode_end_day": 30,
}


def test_episode_config_defaults_are_backwards_compatible():
    cfg = EpisodeConfig(corpus_path="c", schedule_path="s", episode_end_day=1)
    assert cfg.wake_mode == "sparse"
    assert cfg.context_window_days == 0
    assert cfg.context_window_tokens == 0
    assert cfg.notes_max_chars == 6000


def test_store_has_day_starts():
    assert EpisodeStore().day_starts == []


def test_farm_task_parses_the_daily_wake_keys():
    task = farm_task(config={
        **BASE, "wake_mode": "daily", "context_window_days": 7,
        "context_window_tokens": 40000, "notes_max_chars": 5000,
    })
    assert task is not None
    # the solver closure captured the config: read it back through the module-level helper
    from farm_eval.farm_task import _episode_config_from
    cfg = _episode_config_from({
        **BASE, "wake_mode": "daily", "context_window_days": 7,
        "context_window_tokens": 40000, "notes_max_chars": 5000,
    })
    assert (cfg.wake_mode, cfg.context_window_days, cfg.context_window_tokens, cfg.notes_max_chars) == (
        "daily", 7, 40000, 5000)


def test_farm_task_keys_absent_means_sparse_and_unlimited():
    from farm_eval.farm_task import _episode_config_from
    cfg = _episode_config_from(BASE)
    assert (cfg.wake_mode, cfg.context_window_days, cfg.context_window_tokens) == ("sparse", 0, 0)
