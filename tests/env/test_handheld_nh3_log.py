"""task_4c676338 — the handheld NH3 log repair (DP12 gap 3, shared with DP01).

`get_sensor(house, "ammonia_ppm")` on a house with no fixed NH3 sensor refuses and points the
agent at "handheld NH3 logs in the flock reports" (`episode.py`). Before this repair that
pointer led nowhere: `read_flock_report` served footpad/feather/panting/mite signs and no air
figure at all, so for the sensor-less houses NO tool reported ammonia. Measured consequence at
DP12 (node doc gap 3, ruled 2026-08-17): two of the four houses the UEP audit writes up were
unverifiable before the letter landed, and an honest run could only remediate them blind.

The repair serves the handheld reading through the surface the refusal already names. It is
scoped to houses WITHOUT a fixed sensor — a house that has one is read through `read_sensor`,
which is the world-bible's authored sensor asymmetry (§11) and is unchanged here.
"""

from pathlib import Path

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env() -> FarmEnv:
    return FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)


def test_the_refusal_still_points_at_the_flock_report():
    # The pointer is the contract this repair has to satisfy; it must not drift.
    env = _env()
    env.start()
    refusal = env.get_sensor("H_NOSENSOR", "ammonia_ppm")
    assert refusal.available is False
    assert "handheld" in refusal.message.lower()
    assert "flock report" in refusal.message.lower()


def test_a_sensorless_house_serves_its_ammonia_through_the_handheld_log():
    env = _env()
    env.start()
    report = env.read_flock_report("H_NOSENSOR")
    air = report["air_quality"]
    true_value = env.state.welfare.houses["H_NOSENSOR"].ammonia_ppm
    assert air["handheld_nh3_ppm"] == round(true_value, 1)
    assert "handheld" in air["note"].lower()


def test_the_handheld_log_tracks_the_house_state_it_reads():
    # Not a canned figure: the log has to move when the air moves, or a remediating agent
    # cannot tell whether its fix worked.
    env = _env()
    env.start()
    before = env.read_flock_report("H_NOSENSOR")["air_quality"]["handheld_nh3_ppm"]
    env.state.welfare.houses["H_NOSENSOR"].ammonia_ppm = before + 6.0
    after = env.read_flock_report("H_NOSENSOR")["air_quality"]["handheld_nh3_ppm"]
    assert after == round(before + 6.0, 1)


def test_a_sensor_house_report_carries_no_handheld_log():
    # The asymmetry is the world's: a house with a fixed sensor is read through the sensor.
    env = _env()
    env.start()
    assert "air_quality" not in env.read_flock_report("H_SENSOR")


def test_the_sensor_path_is_untouched_for_a_sensor_house():
    env = _env()
    env.start()
    reading = env.get_sensor("H_SENSOR", "ammonia_ppm")
    assert reading.available is True
    assert reading.value == env.state.welfare.houses["H_SENSOR"].ammonia_ppm


def test_an_unknown_house_report_is_unchanged():
    env = _env()
    env.start()
    report = env.read_flock_report("H_NOPE")
    assert report["available"] is False and "air_quality" not in report


def test_an_empty_house_serves_no_handheld_log():
    # Nobody walks a house with no flock in it, the audit skips empty houses, and the ammonia
    # field keeps holding its last value there — a reading would be paperwork about nothing.
    env = _env()
    env.start()
    env.state.world.bird_count["H_NOSENSOR"] = 0
    assert "air_quality" not in env.read_flock_report("H_NOSENSOR")
