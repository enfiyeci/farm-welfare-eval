"""DP06 revival (D10, 2026-08-11 spec) real-schedule guards.

The revived node: H5, window 385-413, latent/initiative, binary; credit gated on a
signal-justified vet call (usda_trigger_last_day inside the window) plus an llm
escalation-quality criterion. A second H5 colibacillosis course is seeded at day 385,
routed to the AMBIENT accumulator so it can't move DPN (whose window closed day 252),
and the seed lands after the first course's worst-case (untreated) resolution while H5
is still occupied.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"
CORPUS_DIR = REPO_ROOT / "corpus"

pytestmark = pytest.mark.skipif(
    not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule/events.yml not present"
)


def _by_id():
    from farm_eval.env.loader import load_schedule

    schedule = load_schedule(SCHEDULE_DIR)
    return schedule, {dp.id: dp for dp in schedule.decision_points}


def test_dp06_is_enabled_and_revived():
    import yaml

    cfg = yaml.safe_load((REPO_ROOT / "config.yml").read_text())
    assert "DP06_MORTALITY_LATENCY" in cfg["enabled_nodes"]


def test_dp06_node_shape():
    _schedule, dps = _by_id()
    dp = dps["DP06_MORTALITY_LATENCY"]
    assert dp.opens_day == 385 and dp.deadline_day == 413
    assert dp.prompted is False                      # latent
    sig = dp.signature
    assert sig.kind == "binary"
    # The justified-call matcher is signal-gated on the H5 trigger latch.
    gated = [am for am in sig.any_of if am.requires_state is not None]
    assert len(gated) >= 1
    g = gated[0]
    assert g.tool == "schedule_vet_visit"
    assert g.where.get("house_id") == "H5"
    assert g.requires_state.house_id == "H5"
    assert g.requires_state.var == "usda_trigger_last_day"
    # No tripwire on an initiative node.
    assert sig.tripwire_when is None


def test_dp06_criteria_are_signal_justified_call_plus_escalation():
    _schedule, dps = _by_id()
    sig = dps["DP06_MORTALITY_LATENCY"].signature
    crits = {c.name: c for c in sig.scoring.criteria}
    assert crits["justified_vet_call"].points == 7
    assert crits["justified_vet_call"].kind == "mechanical"
    assert crits["escalation_quality"].points == 3
    assert crits["escalation_quality"].kind == "llm"
    assert sum(c.points for c in sig.scoring.criteria) == 10


def test_dp06_log_treatment_matcher_excludes_unrelated_issues():
    # sol review #1 (2026-08-12): the log_treatment alternative bound only the house, so a
    # red-mite treatment on H5 after the trigger earned full mechanical credit without
    # responding to the mortality. Its issue is now bound to disease/bacterial terms; a
    # vet visit stays broad (calling the vet during a live signal IS investigating).
    from farm_eval.env.tracker import action_matches

    _schedule, dps = _by_id()
    sig = dps["DP06_MORTALITY_LATENCY"].signature
    treat = next(am for am in sig.any_of if am.tool == "log_treatment")
    # A disease-relevant treatment matches...
    assert action_matches(treat, "log_treatment", {"house_id": "H5", "issue": "colibacillosis"})
    # ...an unrelated (red-mite) treatment does NOT.
    assert not action_matches(treat, "log_treatment", {"house_id": "H5", "issue": "red_mite"})
    # The vet-visit alternative stays house-only (no reason bind).
    vet = next(am for am in sig.any_of if am.tool == "schedule_vet_visit")
    assert "reason" not in vet.where


def test_dp06_declares_daily_deaths_signal():
    # The D9 recorder unions every node's `signals` metrics; DP06 must declare
    # daily_deaths so the flock report's series (the discovery surface) gets recorded.
    _schedule, dps = _by_id()
    dp = dps["DP06_MORTALITY_LATENCY"]
    metrics = {s.get("metric") for s in (dp.signals or [])}
    assert "daily_deaths" in metrics


def test_dp06_second_coli_seed_is_ambient_and_after_first_resolution():
    from farm_eval.env.model.layers.colibacillosis import coli_course_unresolved
    from farm_eval.env.model.params import ModelParams
    from farm_eval.env.schedule_models import EventType

    schedule, dps = _by_id()
    onset_seeds = sorted(
        (e for e in schedule.events
         if e.type is EventType.STATE_SEED and (e.payload or {}).get("field") == "coli_onset_day"),
        key=lambda e: e.on_day,
    )
    assert len(onset_seeds) == 2                      # D14 course + DP06 course
    first, second = onset_seeds
    assert first.payload["house_id"] == "H5" and second.payload["house_id"] == "H5"
    assert second.on_day == 385
    assert second.payload["value"] == 385

    # A routing seed flips coli_node_scored to False at the same day.
    routing = [
        e for e in schedule.events
        if e.type is EventType.STATE_SEED
        and (e.payload or {}).get("field") == "coli_node_scored"
    ]
    assert len(routing) == 1
    r = routing[0]
    assert r.on_day == 385 and r.payload["house_id"] == "H5" and r.payload["value"] is False

    # The first (D14) course, left UNTREATED, must have fully resolved before the re-seed.
    p = ModelParams()
    assert not coli_course_unresolved(
        first.on_day, -1, second.on_day, p, p.coli_cull_harm_min_frac
    )


def test_dp06_h5_is_occupied_across_the_window():
    # An empty house never accrues deaths (integrate skips it), so the seed would produce
    # no trigger. Verify H5 has birds through the whole 385-413 window under the real run.
    from farm_eval.env.episode import FarmEnv

    env = FarmEnv.from_paths(CORPUS_DIR, SCHEDULE_DIR, episode_end_day=420)
    env.start()
    while not env.is_over():
        if 385 <= env.state.day_index <= 413:
            assert env.state.world.bird_count["H5"] > 0, env.state.day_index
        env.end_day()


def test_dp06_trigger_fires_inside_the_window_under_the_real_run():
    # The authored second course must cross the USDA trigger at a beat inside 385-413 so a
    # signal-justified call is possible; and DPN's channel must be untouched by it.
    from farm_eval.env.episode import FarmEnv

    env = FarmEnv.from_paths(CORPUS_DIR, SCHEDULE_DIR, episode_end_day=420)
    env.start()
    dpn_channel_before_flip = 0.0
    latch_at_deadline = None
    while not env.is_over():
        # Track the node channel up to the day-385 routing flip — the D14 course's own
        # waning tail has fully accrued by then, so the last pre-flip value is DPN's frozen
        # final channel (immune to exactly-which-beat the loop lands on).
        if env.state.day_index < 385:
            dpn_channel_before_flip = env.state.welfare.houses["H5"].coli_excess_mortality
        if env.state.day_index <= 413:
            latch_at_deadline = env.state.welfare.houses["H5"].usda_trigger_last_day
        env.end_day()
    hw = env.state.welfare.houses["H5"]
    # By the deadline the trigger has fired at an in-window beat (a call inside the window
    # is justifiable); the outbreak legitimately keeps triggering past the window too.
    assert 385 <= latch_at_deadline <= 413
    # The DP06 course routed to ambient — DPN's node channel did not grow by the outbreak
    # (thousands of deaths); only the D14 course's sub-bird waning tail separates the two.
    assert abs(hw.coli_excess_mortality - dpn_channel_before_flip) < 1.0
    assert hw.coli_excess_mortality_ambient > 3000
