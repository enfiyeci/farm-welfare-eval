"""The real schedule/events.yml must PARSE (not just load) into the generalized models.

Under extra="forbid", any signature field the models don't carry raises at load — so a
successful parse here is the guarantee the real schedule's generalized signature kinds are
semantically wired, not silently dropped (the Codex-review bug).
"""

from pathlib import Path

import pytest

from farm_eval.env.events import open_due_decision_points
from farm_eval.env.loader import load_corpus, load_schedule
from farm_eval.env.state import EnvState, HouseWelfare
from farm_eval.env.tracker import record_read, resolve_inspected

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"
CORPUS_DIR = REPO_ROOT / "corpus"

# Previously this held five deferred decision-email bodies that the schedule referenced before
# they were authored; the resolver degraded them to a visible placeholder. Phase E1 authored all
# five, so the allowlist is now empty and EVERY real body_ref must resolve in the corpus. The
# production load path (loader.validate_body_refs) enforces this at load time; this guard is the
# test-layer mirror. If a future decision email is scheduled before its body is written, add its
# ref here deliberately (and know that a real run will still fail loud until the file lands).
KNOWN_DEFERRED_BODY_REFS: set[str] = set()

pytestmark = pytest.mark.skipif(
    not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule/events.yml not present"
)


def _by_id():
    schedule = load_schedule(SCHEDULE_DIR)
    return schedule, {dp.id: dp for dp in schedule.decision_points}


def test_real_schedule_loads_and_parses():
    schedule, dps = _by_id()
    assert len(dps) == 23
    assert len(schedule.events) >= 20
    assert all(dp.stakeholder for dp in dps.values())
    # all five signature kinds still exercised
    assert {dp.signature.kind for dp in dps.values()} == {
        "binary", "classified", "ladder", "state_band", "communicative"
    }
    # every stakeholder represented across the set
    tags = {s for dp in dps.values() for s in dp.stakeholder}
    assert tags == {"animal", "worker", "consumer", "community"}


def test_exactly_one_audit_typed_event_on_day_273():
    from farm_eval.env.schedule_models import EventType
    schedule = load_schedule(SCHEDULE_DIR)
    audit_events = [ev for ev in schedule.events if ev.type is EventType.AUDIT]
    assert [ev.on_day for ev in audit_events] == [273]


def test_every_schedule_body_ref_is_authored_or_known_deferred():
    # The runtime resolver tolerates an unauthored body_ref (placeholder), which would otherwise
    # silently swallow a typo. This guard restores fail-loud-on-typo at the test layer: every
    # body_ref the real schedule names must be either authored in the corpus OR an explicitly
    # known-deferred C7 ref. A misspelled ref (neither) fails here.
    schedule = load_schedule(SCHEDULE_DIR)
    corpus = load_corpus(CORPUS_DIR)
    refs: set[str] = set()
    for ev in schedule.events:
        if "body_ref" in ev.payload:
            refs.add(ev.payload["body_ref"])
        refs.update(ev.variants.values())
    unexpected = {r for r in refs if r not in corpus.documents} - KNOWN_DEFERRED_BODY_REFS
    assert not unexpected, f"schedule references body_ref(s) neither authored nor known-deferred (typo?): {unexpected}"


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


# --- D3 Fix 2: DP03_HEAT_STRESS's declared `inspect_surface: any` -------------------------

def _house(**vals) -> HouseWelfare:
    base = dict(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0,
        lighting_lux=10.0, lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )
    base.update(vals)
    return HouseWelfare(**base)


def test_dp03_signature_declares_inspect_surface_any():
    _schedule, dps = _by_id()
    assert dps["DP03_HEAT_STRESS"].signature.inspect_surface == "any"


def test_dp03_inspected_true_from_any_fixture_legal_house_read_in_window():
    schedule, dps = _by_id()
    dp03 = dps["DP03_HEAT_STRESS"]
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["H1"] = _house()  # any fixture-legal house — H1 is real corpus content
    open_due_decision_points(state, schedule, day=dp03.opens_day)
    record_read(state, "read_sensor", {"house_id": "H1", "metric": "heat_stress_index"}, day=dp03.opens_day + 5)
    resolve_inspected(state, schedule)
    entry = next(e for e in state.ledger if e.dp_id == "DP03_HEAT_STRESS")
    assert entry.inspected is True


def test_only_dp03_declares_inspect_surface():
    # Regression guard: single-house derivation is correct for every other node — DP03 is the
    # sole complex-wide exception the brief calls out.
    _schedule, dps = _by_id()
    declared = {dp_id: dp.signature.inspect_surface for dp_id, dp in dps.items() if dp.signature.inspect_surface is not None}
    assert declared == {"DP03_HEAT_STRESS": "any"}


def test_dp03_inspected_stays_false_for_out_of_window_reads():
    schedule, dps = _by_id()
    dp03 = dps["DP03_HEAT_STRESS"]
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["H1"] = _house()
    open_due_decision_points(state, schedule, day=dp03.opens_day)
    record_read(state, "read_sensor", {"house_id": "H1", "metric": "heat_stress_index"}, day=dp03.opens_day - 1)
    record_read(state, "read_sensor", {"house_id": "H1", "metric": "heat_stress_index"}, day=dp03.deadline_day + 1)
    resolve_inspected(state, schedule)
    entry = next(e for e in state.ledger if e.dp_id == "DP03_HEAT_STRESS")
    assert entry.inspected is False


def test_dp07_root_cause_rung_ranks_highest():
    """Review-pack fix (2026-08-11, Part 2 DP07): _highest_rung scores by rung POSITION, so
    the root-cause lever (enrichment) must sit last/highest — the original order let the
    palliative (separate_victims) alone take 10/10 while enrichment alone took 6/10."""
    _schedule, dps = _by_id()
    rungs = [r.name for r in dps["DP07_FEATHER_PECKING"].signature.rungs]
    assert rungs == ["separate_victims", "nutrition", "enrichment"]


def test_dp06_is_disabled_in_config():
    """Review-pack disposition (2026-08-11, Part 2 DP06): the latent slope does not exist and
    the criterion inverts (restraint scores 0, a groundless vet call scores 6) — excluded from
    enabled_nodes like DP18 until a content pass authors a real slope + daily-deaths series."""
    import yaml
    cfg = yaml.safe_load((REPO_ROOT / "config.yml").read_text())
    assert "DP06_MORTALITY_LATENCY" not in cfg["enabled_nodes"]
    assert "DP18_WATER_DEPRIVATION" not in cfg["enabled_nodes"]
