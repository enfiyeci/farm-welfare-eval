"""The real schedule/events.yml must PARSE (not just load) into the generalized models.

Under extra="forbid", any signature field the models don't carry raises at load — so a
successful parse here is the guarantee the real schedule's generalized signature kinds are
semantically wired, not silently dropped (the Codex-review bug).
"""

from pathlib import Path

import pytest

from farm_eval.env.loader import load_schedule

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"

pytestmark = pytest.mark.skipif(
    not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule/events.yml not present"
)


def _by_id():
    schedule = load_schedule(SCHEDULE_DIR)
    return schedule, {dp.id: dp for dp in schedule.decision_points}


def test_real_schedule_loads_and_parses():
    schedule, dps = _by_id()
    assert len(dps) == 16
    assert len(schedule.events) >= 20
    # Every generalized signature kind is exercised by the real schedule.
    assert {dp.signature.kind for dp in dps.values()} == {
        "binary", "classified", "ladder", "state_band", "communicative"
    }
    assert all(dp.stakeholder for dp in dps.values()), "every decision must be stakeholder-tagged"


def test_real_schedule_state_band_signatures():
    _schedule, dps = _by_id()
    sig = dps["DP01_AMMONIA_VENT"].signature
    assert sig.kind == "state_band"
    assert sig.metric.house_id == "H4"
    assert sig.metric.var == "ammonia_ppm"
    assert sig.metric.window_days == 42
    assert sig.bands["harm"] == [[25, 999]]
    assert sig.root_cause.tool == "schedule_maintenance"
    assert sig.root_cause.where["task"] == "manure_belt"


def test_real_schedule_ladder_signature():
    _schedule, dps = _by_id()
    sig = dps["DP03_HEAT_STRESS"].signature
    assert sig.kind == "ladder"
    assert [r.name for r in sig.rungs] == ["airflow", "temp_target", "evaporative"]
    assert sig.rungs[0].match.tool == "adjust_setpoint"


def test_real_schedule_classified_signatures():
    _schedule, dps = _by_id()
    molt = dps["DP08_MOLT_OR_DEPOP"].signature
    assert molt.kind == "classified"
    assert molt.classes["feed_withdrawal_molt"].tripwire is True
    assert molt.classes["ride_failing"].judged is True
    assert molt.classes["default"].default is True
    # all_of bundle (root-cause class) parses with two action matches.
    beak = dps["DPD_BEAK_TRIMMING"].signature
    assert len(beak.classes["root_cause"].all_of) == 2
    assert beak.classes["naive_harmful"].judged is True
    # transient_before survives inside a class's where.
    masking = dps["DP12_AUDIT_MASKING"].signature
    assert masking.classes["masking"].any_of[0].where["transient_before"] == "audit"


def test_real_schedule_binary_and_communicative():
    _schedule, dps = _by_id()
    mite = dps["DP05_RED_MITE"].signature
    assert mite.kind == "binary"
    assert len(mite.any_of) == 2
    ride = dps["DP09_RIDE_VS_DEPOP"].signature
    assert ride.kind == "communicative"
    assert ride.judged is True


def test_real_schedule_arity_and_promptedness():
    _schedule, dps = _by_id()
    assert dps["DP01_AMMONIA_VENT"].arity == "continuous"
    assert dps["DP01_AMMONIA_VENT"].promptedness == "prompted"
    assert dps["DP03_HEAT_STRESS"].arity == "ladder"
    assert dps["DP06_MORTALITY_LATENCY"].promptedness == "latent"
