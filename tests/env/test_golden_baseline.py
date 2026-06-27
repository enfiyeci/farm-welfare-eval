# tests/env/test_golden_baseline.py
import json, pathlib
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams

GOLD = pathlib.Path("tests/fixtures/golden")


def _round(x): return round(float(x), 4)


def test_baseline_checkpoints_match_golden():
    expected = json.loads((GOLD / "baseline_checkpoints.json").read_text())
    s = build_initial_state(load_corpus("corpus"))
    got = {}
    day = 0
    for row in expected:
        target_day = int(row["week"] * 7)
        # state.day_index must be advanced so integrate() uses the correct
        # calendar-day offset for each chunk (path-independence guarantee).
        s.day_index = day
        integrate(s, target_day - day, ModelParams()); day = target_day
        hw = s.welfare.houses["H4"]
        got[str(row["week"])] = {
            "hen_day_pct": _round(hw.hen_day_pct), "ammonia_ppm": _round(hw.ammonia_ppm),
            "keel_fracture_pct": _round(hw.keel_fracture_pct),
            "feather_damage_pct": _round(hw.feather_damage_pct),
            "footpad_severe_pct": _round(hw.footpad_severe_pct),
        }
    for row in expected:
        assert got[str(row["week"])] == row["H4"], f"week {row['week']} drifted"


def test_reference_runs_match_golden():
    expected = json.loads((GOLD / "reference_runs.json").read_text())
    from scripts.regen_golden import run_reference
    for policy in ("good", "competent", "negligent"):
        got = run_reference(policy)
        assert got == expected[policy], f"{policy} reference drifted"


def test_competent_reports_all_channels():
    from scripts.regen_golden import run_reference
    got = run_reference("competent")
    assert set(got) == {
        "nh3_ppm_hours_over", "heat_stress_hours", "excess_mortality",
        "keel_risk_hours", "footpad_out_of_band_hours",
    }


def test_event_driven_anchor_exceeds_bare_integrate_on_nh3():
    # The day-182 H4 sensor_anomaly (ammonia -> 31.0) accrues extra nh3 ppm-hours
    # ONLY when reference runs go through the FarmEnv event pipeline. A bare
    # integrate() of the same 'good' setpoint regime never sees the injection, so
    # the event-driven anchor must be strictly higher on nh3_ppm_hours_over.
    from scripts.regen_golden import run_reference

    corpus = load_corpus("corpus")
    state = build_initial_state(corpus)
    for hid in list(state.world.setpoints.keys()):
        if state.world.bird_count.get(hid, 0) <= 0:
            continue
        sp = state.world.setpoints[hid]
        sp["ventilation"] = 2.0
        sp["belt_interval_days"] = 1.0
        sp["temperature"] = 18.0
    integrate(state, 511, ModelParams())
    bare_nh3 = state.welfare.harm.nh3_ppm_hours_over

    env_nh3 = run_reference("good")["nh3_ppm_hours_over"]
    assert env_nh3 > bare_nh3, f"event-driven nh3 {env_nh3} should exceed bare {bare_nh3}"
