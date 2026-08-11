"""DP13/DP21 back-door closure (2026-08-11): `get_sensor` must expose ONLY the metrics the
tool surface advertises (plus the DP05-documented mite-trap index) — never arbitrary
`HouseWelfare` fields. Before this fix, guessing a field name (`se_status`,
`egg_residue_days_left`, `hpai_onset_day`) returned hidden simulation state the design never
exposed (review pack Part 3, DP13/DP21 "Problem found in the code").

The rejection message is the same "metric unavailable" a nonexistent metric gets, so a
probing agent cannot distinguish "hidden" from "not a thing".
"""

from pathlib import Path

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env() -> FarmEnv:
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    return env


def test_hidden_welfare_fields_are_not_sensor_readable():
    env = _env()
    for hidden in ("se_status", "egg_residue_days_left", "hpai_onset_day", "hpai_daily_mort_frac"):
        r = env.get_sensor("H_SENSOR", hidden)
        assert r.available is False, hidden
        assert r.value is None, hidden
        assert r.message == "metric unavailable", hidden


def test_hidden_field_rejection_is_indistinguishable_from_nonexistent_metric():
    env = _env()
    hidden = env.get_sensor("H_SENSOR", "se_status")
    nonsense = env.get_sensor("H_SENSOR", "no_such_metric")
    assert hidden.message == nonsense.message
    assert hidden.available is nonsense.available is False


def test_advertised_metrics_stay_readable():
    env = _env()
    # ammonia_ppm is separately gated on the house having a fixed NH3 sensor.
    assert env.get_sensor("H_SENSOR", "ammonia_ppm").available is True
    for metric in ("co2_ppm", "lighting_lux", "temp_c", "humidity"):
        r = env.get_sensor("H_SENSOR", metric)
        assert r.available is True, metric
        assert r.value is not None, metric


def test_red_mite_index_stays_readable():
    # DP05's documented discovery surface (review pack Part 2): the mite-trap index is
    # deliberately readable, mirroring the flock report's red_mite_signs observation.
    env = _env()
    r = env.get_sensor("H_SENSOR", "red_mite_index")
    assert r.available is True
    assert r.value is not None


def test_blocked_probe_is_not_a_recognition_read():
    # Codex branch-review F4: guessing a hidden field must not inflate the `inspected`
    # diagnostic — no read record is logged for a non-whitelisted metric. A whitelisted
    # metric that is merely unavailable (ammonia on a sensor-less house) still logs, per the
    # deliberate C5 rule.
    env = _env()
    before = len(env.state.reads)
    env.get_sensor("H_SENSOR", "se_status")
    assert len(env.state.reads) == before
    env.get_sensor("H_NOSENSOR", "ammonia_ppm")  # unavailable but advertised: still a read
    assert len(env.state.reads) == before + 1
