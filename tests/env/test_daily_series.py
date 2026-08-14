"""D9 (owner ruling, 2026-08-11): the env records a daily per-house series for every
metric any schedule node's `signals` declare, so the judge can hand llm criteria the
window's OBJECTIVE ground truth (DPF's claimed-readings check) instead of grading the
agent's claims against the transcript alone."""

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env():
    return FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)


def test_daily_series_records_signal_metrics_per_house_per_day():
    env = _env()
    env.start()
    adv = env.end_day()
    days = env.state.daily_series_days
    assert days == list(range(1, adv.elapsed_days + 1))
    for hid, hw in env.state.welfare.houses.items():
        series = env.state.daily_series[hid]
        assert set(series) == {"water_ml", "hen_day_pct"}   # fixture signals, nothing more
        for metric, values in series.items():
            assert len(values) == len(days)
            # The final recorded value is the committed end-of-day state.
            assert values[-1] == pytest.approx(getattr(hw, metric))


def test_daily_series_survives_multiple_beats_path_independently():
    env = _env()
    env.start()
    env.end_day()
    n1 = len(env.state.daily_series_days)
    env.end_day()
    n2 = len(env.state.daily_series_days)
    assert n2 > n1
    assert env.state.daily_series_days == list(range(1, n2 + 1))


def test_unknown_signal_metric_fails_loudly_at_env_init(tmp_path):
    import shutil

    sched_dir = tmp_path / "schedule"
    shutil.copytree(FIX / "schedule", sched_dir)
    events = (sched_dir / "events.yml").read_text()
    events = events.replace("{metric: water_ml, reliability: high}",
                            "{metric: water_l, reliability: high}")   # DP18's stale-name bug class
    (sched_dir / "events.yml").write_text(events)
    with pytest.raises(ValueError, match="water_l"):
        FarmEnv.from_paths(FIX / "corpus", sched_dir, seed=1, episode_end_day=400)


def test_series_stays_aligned_when_a_house_empties(tmp_path):
    # Codex round-3 CRITICAL (2026-08-11): empty houses skipped the recording, so their
    # series desynced from daily_series_days (real farm: H3 empties day 269 -> IndexError
    # in the objective-state block for any later window). Every house records every day.
    env = _env()
    env.start()
    env.end_day()
    victim = next(iter(env.state.welfare.houses))
    env.state.world.bird_count[victim] = 0          # house empties mid-run
    env.end_day()
    days = env.state.daily_series_days
    for hid in env.state.welfare.houses:
        for metric, values in env.state.daily_series[hid].items():
            assert len(values) == len(days), (hid, metric)
