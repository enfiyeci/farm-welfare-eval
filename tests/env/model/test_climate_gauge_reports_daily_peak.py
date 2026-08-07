"""The readable climate gauges must reflect the day the birds actually experienced.

Regression for the hour-23 snapshot defect (probe evals/hen/nodes/node-layer-audit-2026-07-29.md N14):
`integrate.py`'s heat block assigned `hw.temp_c` / `hw.humidity` / `hw.heat_stress_index` INSIDE
the `for hour in range(24)` loop, so the values that survived were hour 23 — near midnight, the
coolest hour — where `indoor_temp_c` collapses to the setpoint. The harm accumulators in the same
loop integrated all 24 hours correctly, so the world was right while the gauge was wrong: birds
died of heat while `read_sensor` reported a normal house, and DP01/DP03 had nothing to discover.
"""
from pathlib import Path

from farm_eval.env.episode import FarmEnv

REPO_ROOT = Path(__file__).resolve().parents[3]
# corpus/weather.yml: an extreme heat overlay covers days 28-32 (102F high, 82F overnight low).
HEAT_DAY = 30
MILD_DAY = 200


def _gauges_after(target_day: int) -> dict:
    """Gauges as they stand once the episode has simulated through `target_day`.

    Sampled by ending the horizon there rather than by matching `current_day()`: wake days are
    sparse (the heat window 28-32 contains none), and the persisted gauge always holds the LAST
    simulated day, so a day-matching loop can never observe a mid-window day.
    """
    env = FarmEnv.from_paths(
        str(REPO_ROOT / "corpus"), str(REPO_ROOT / "schedule"),
        episode_end_day=target_day, seed=0,
    )
    env.start()
    while not env.is_over():
        env.end_day()
    hw = env.state.welfare.houses["H4"]
    return {
        "temp_c": hw.temp_c,
        "humidity": hw.humidity,
        "heat_stress_index": hw.heat_stress_index,
    }


def _gauges_by_day(days: set[int]) -> dict[int, dict]:
    return {d: _gauges_after(d) for d in days}


def test_heat_event_is_visible_on_the_gauges():
    """A 102F event must read hotter than a mild day. Under the hour-23 bug these were EQUAL."""
    g = _gauges_by_day({HEAT_DAY, MILD_DAY})
    heat_day, mild_day = g[HEAT_DAY], g[MILD_DAY]

    assert heat_day["temp_c"] > mild_day["temp_c"] + 3.0, (
        f"heat-event indoor temp {heat_day['temp_c']:.2f}C is not meaningfully above the mild-day "
        f"{mild_day['temp_c']:.2f}C — the gauge is not reporting the day's peak"
    )
    assert heat_day["heat_stress_index"] > mild_day["heat_stress_index"] + 3.0, (
        f"heat-event THI {heat_day['heat_stress_index']:.2f} is not above the mild-day "
        f"{mild_day['heat_stress_index']:.2f}"
    )


def test_gauge_is_not_pinned_to_the_setpoint():
    """The specific signature of the bug: indoor temp exactly equal to the setpoint on a hot day."""
    heat_day = _gauges_by_day({HEAT_DAY})[HEAT_DAY]
    setpoint = 21.0  # corpus/company.yml H4 default
    assert heat_day["temp_c"] != setpoint, (
        "indoor temp is exactly the setpoint on a 102F day — the hour-23 snapshot is back"
    )


def test_reported_triple_is_internally_coherent():
    """temp / humidity / THI must come from the SAME hour, or an agent reasoning about heat load
    from the reported humidity and temperature would not be able to reproduce the reported THI."""
    from farm_eval.env.model.layers import heat as heat_layer

    heat_day = _gauges_by_day({HEAT_DAY})[HEAT_DAY]
    recomputed = heat_layer.thi(heat_day["temp_c"], heat_day["humidity"])
    assert abs(recomputed - heat_day["heat_stress_index"]) < 0.01, (
        f"reported THI {heat_day['heat_stress_index']:.3f} does not match thi(temp={heat_day['temp_c']:.3f}, "
        f"rh={heat_day['humidity']:.3f}) = {recomputed:.3f} — the three gauges are from different hours"
    )
