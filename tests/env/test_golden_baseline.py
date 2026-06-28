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


def test_pipeline_anchor_equals_bare_integrate():
    # Post-DPH, no scheduled event perturbs the welfare substrate (the day-182 sensor
    # anomaly writes a gauge overlay, not real ammonia). So routing reference policies
    # through the full FarmEnv pipeline must produce the SAME terminal harm as a bare
    # integrate() of the same setpoint regime. This canary fires if a future event ever
    # starts changing welfare state, at which point anchors and scored runs would diverge.
    from scripts.regen_golden import run_reference, _POLICIES, _harm_to_dict, _EPISODE_DAYS
    for policy, overrides in _POLICIES.items():
        s = build_initial_state(load_corpus("corpus"))
        for hid in list(s.world.setpoints.keys()):
            if s.world.bird_count.get(hid, 0) <= 0:
                continue
            s.world.setpoints[hid].update(overrides)
        integrate(s, _EPISODE_DAYS, ModelParams())
        bare = _harm_to_dict(s.welfare.harm)
        assert run_reference(policy) == bare, f"{policy}: pipeline anchor diverged from bare integrate"
