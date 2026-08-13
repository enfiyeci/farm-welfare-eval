"""Per-house daily-deaths series in the flock report (D10 / DP06 revival, 2026-08-12).

The flock report's mortality block gains a ``daily_deaths_last14`` series — the last
~14 recorded days of the house's ``daily_deaths`` from the D9 ground-truth series
(``state.daily_series[hid]["daily_deaths"]``, recorded once a schedule node declares
``daily_deaths`` in its ``signals``). This is DP06's discovery surface (the slow rise
is readable) and cures reviewer F12's D14 observability note (the coli deaths were
visible only as a shrinking headcount).

Graceful when the series is empty (fixtures / schedules that declare no daily_deaths
signal): the key is simply absent, never a crash.
"""

from pathlib import Path

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    env.end_day()
    return env


def test_report_omits_series_when_not_recorded():
    # The fixture schedule declares no daily_deaths signal, so the recorder never
    # populates the series — the report must render without the key, not crash.
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    rep = env.read_flock_report(hid)
    assert "daily_deaths_last14" not in rep["mortality"]


def test_report_renders_last_14_days_when_recorded():
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    # Simulate the D9 recorder having logged a daily_deaths series for this house.
    series = [float(x) for x in range(1, 21)]  # 20 days, 1..20
    env.state.daily_series[hid] = {"daily_deaths": list(series)}
    rep = env.read_flock_report(hid)
    got = rep["mortality"]["daily_deaths_last14"]
    assert got == series[-14:]
    assert len(got) == 14


def test_report_series_shorter_than_14_returns_all():
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    env.state.daily_series[hid] = {"daily_deaths": [3.0, 5.0, 8.0]}
    rep = env.read_flock_report(hid)
    assert rep["mortality"]["daily_deaths_last14"] == [3.0, 5.0, 8.0]


def test_report_series_absent_metric_omits_key():
    # A house with a series dict but no daily_deaths metric (other signals only).
    env = _env()
    hid = next(iter(env.state.welfare.houses))
    env.state.daily_series[hid] = {"water_ml": [200.0, 201.0]}
    rep = env.read_flock_report(hid)
    assert "daily_deaths_last14" not in rep["mortality"]
