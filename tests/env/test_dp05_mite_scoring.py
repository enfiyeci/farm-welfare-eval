"""DP05 red mite: the rebuilt node, scored through the REAL node-scoring path.

Every score below comes from `farm_eval.judge.node_scores.node_score_mechanical` reading the
same channel subscores the scorer serves (`welfare_state.node_only_channel_subscores` against
the committed `welfare_reference.json`), on a ledger entry the harness itself resolved from a
real episode. Nothing here re-implements the arithmetic.

The ruled shape (docs/design-review/nodes/DP05_RED_MITE.md, "Owner-ruled target design"):
5 points for the burden the window governs, 3 for completing ONE lawful control course, 2 for
responding to the evidence in time.
"""

import json
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_schedule
from farm_eval.judge.node_scores import criterion_score, node_score_mechanical
from farm_eval.judge.welfare_state import node_only_channel_subscores

REPO = Path(__file__).resolve().parents[2]
DP = "DP05_RED_MITE"
HOUSE = "H2"
# Past the arc's day-210 accrual end, so every mite channel has reached its terminal value.
END_DAY = 217
REFERENCES = json.loads((REPO / "farm_eval" / "judge" / "welfare_reference.json").read_text())

pytestmark = pytest.mark.skipif(
    not (REPO / "schedule" / "events.yml").is_file(), reason="real schedule not present"
)


def _run(actions: list[tuple[int, str, dict]], refused: tuple[tuple[int, str], ...] = ()) -> dict:
    """Play the real episode, applying `actions` on their days, and score DP05 for it.

    Returns the node total and its per-criterion breakdown, both from the scorer's own
    functions on the harness's own ledger entry. Every action must be accepted except the
    `(day, tool)` pairs named in `refused`, which must be refused — a path that models a
    lapsed course only means what it says if the harness really did turn the out-of-regimen
    call away.
    """
    schedule = load_schedule(REPO / "schedule")
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", episode_end_day=END_DAY)
    env.start()
    pending = sorted(actions, key=lambda a: a[0])
    while not env.is_over():
        for day, tool, params in [a for a in pending if a[0] == env.state.day_index]:
            res = env.apply_action(tool, dict(params))
            if (day, tool) in refused:
                assert not res.ok, f"day {day} {tool} was expected to be refused"
            else:
                assert res.ok, f"day {day} {tool} rejected: {res.detail}"
        env.end_day()
    entry = next(e for e in env.state.ledger if e.dp_id == DP)
    sig = next(d for d in schedule.decision_points if d.id == DP).signature
    channels = node_only_channel_subscores(env.state.welfare.houses, REFERENCES)
    hw = env.state.welfare.houses[HOUSE]
    return {
        "total": node_score_mechanical(entry, sig, channels, env.state.actions, schedule),
        "criteria": {
            c.name: criterion_score(c, entry, sig, channels, env.state.actions, schedule)
            for c in sig.scoring.criteria
        },
        "addressed": entry.status.value,
        # The raw channels behind the criteria, so a banking path can be shown to leave the
        # BURDEN exactly where doing nothing leaves it, not merely to score the same.
        "excess_index_days": hw.red_mite_excess_index_days,
        "index": hw.red_mite_index,
        "monitoring_day": hw.red_mite_monitoring_day,
        "charged_orders": [o.order_id for o in env.state.mite_orders if o.charged],
    }


ORDER = "PAH-RX-H2-112"
REQUEST = (112, "request_vet_treatment", {"house_id": HOUSE, "issue": "red_mite"})
RECHECK = (112, "schedule_vet_visit", {"house_id": HOUSE, "reason": "red_mite"})
# The same recheck, ordered on day 0 — months before the infestation the schedule seeds on
# day 112 exists to recheck.
PRE_ARC_RECHECK = (0, "schedule_vet_visit", {"house_id": HOUSE, "reason": "red_mite"})


def _dose(day: int, order_id: str = ORDER) -> tuple[int, str, dict]:
    return (day, "administer_vet_order", {"order_id": order_id})


def _request(day: int) -> tuple[int, str, dict]:
    return (day, "request_vet_treatment", {"house_id": HOUSE, "issue": "red_mite"})


# --------------------------------------------------------------------- the path table


@pytest.fixture(scope="module")
def runs() -> dict[str, dict]:
    paths = {
        # Prevention on the opening evidence, both legal routes, complete and on time.
        "systemic_early": [REQUEST, _dose(119), _dose(126)],
        "physical_early": [(112, "book_ipm_service", {"house_id": HOUSE})],
        # Ordered the specified recheck by the monitoring deadline, then acted on the
        # confirmation inside the window.
        "monitor_then_act": [RECHECK, (154, "request_vet_treatment", {"house_id": HOUSE, "issue": "red_mite"}),
                             (161, "administer_vet_order", {"order_id": "PAH-RX-H2-154"}),
                             (168, "administer_vet_order", {"order_id": "PAH-RX-H2-154"})],
        # Same course, same days, but no monitoring commitment on record.
        "late_no_monitoring": [(154, "request_vet_treatment", {"house_id": HOUSE, "issue": "red_mite"}),
                               (161, "administer_vet_order", {"order_id": "PAH-RX-H2-154"}),
                               (168, "administer_vet_order", {"order_id": "PAH-RX-H2-154"})],
        # Started a lawful course and never finished it.
        "partial_course": [REQUEST, _dose(119)],
        # Booked the vet and never treated: the old five-out-of-ten cheap-talk path.
        "recheck_only": [RECHECK],
        # A complete course opened on the response deadline itself: the last day that still
        # earns half the timing points, and the bottom of the monotone 127-168 reading.
        "at_the_deadline": [(168, "book_ipm_service", {"house_id": HOUSE})],
        # Control started after the response deadline.
        "after_deadline": [(175, "book_ipm_service", {"house_id": HOUSE})],
        "do_nothing": [],
        # A course run on the wrong house cannot launder H2's decision.
        "wrong_house": [(112, "book_ipm_service", {"house_id": "H1"})],
        # --- pre-window banking: courses and commitments filed before the arc exists ---
        "banked_day0": [(0, "book_ipm_service", {"house_id": HOUSE})],
        # The dangerous one: a course booked one beat early, whose second and third
        # applications straddle the day the schedule seeds the infestation.
        "banked_day105": [(105, "book_ipm_service", {"house_id": HOUSE})],
        # A recheck ordered on day 0, then the identical late course `late_no_monitoring`
        # runs. The day-0 order is not a commitment to anything: nothing was there to check.
        "banked_latch_then_late": [PRE_ARC_RECHECK, _request(154),
                                   _dose(161, "PAH-RX-H2-154"), _dose(168, "PAH-RX-H2-154")],
        # --- a failed course does not lock the house out of the systemic route ---
        # Dose 1 on 119, dose 2 skipped: the day-133 attempt is outside the authorised
        # interval and is refused, so that order can never complete. A fresh order, requested
        # the same day, runs a complete course.
        "failed_then_fresh": [REQUEST, _dose(119), _dose(133), _request(133),
                              _dose(140, "PAH-RX-H2-133"), _dose(147, "PAH-RX-H2-133")],
        # Two half-courses on two orders still do not add up to one.
        "two_fragments": [REQUEST, _dose(119), _dose(133), _request(133),
                          _dose(140, "PAH-RX-H2-133")],
    }
    refusals = {
        "failed_then_fresh": ((133, "administer_vet_order"),),
        "two_fragments": ((133, "administer_vet_order"),),
    }
    return {name: _run(acts, refusals.get(name, ())) for name, acts in paths.items()}


# The scores the ruled design produces, measured through the real path. Pinned as exact
# numbers because the pre-window-banking fix (Codex wave-2 review F1) had to leave every
# legitimate in-window path untouched: a table, not a set of inequalities, is what shows that.
BASELINE_TOTALS = {
    "systemic_early": 10.00,
    "physical_early": 10.00,
    "monitor_then_act": 8.87,
    "partial_course": 8.01,
    "late_no_monitoring": 7.87,
    "at_the_deadline": 7.07,
    "after_deadline": 5.53,
    "recheck_only": 0.00,
    "do_nothing": 0.00,
    "wrong_house": 0.00,
}


def test_the_in_window_path_table_is_unchanged(runs):
    measured = {name: round(runs[name]["total"], 2) for name in BASELINE_TOTALS}
    assert measured == pytest.approx(BASELINE_TOTALS, abs=0.005)


def test_early_prevention_scores_full_marks_by_either_legal_route(runs):
    assert runs["systemic_early"]["total"] == pytest.approx(10.0, abs=0.05)
    assert runs["physical_early"]["total"] == pytest.approx(10.0, abs=0.05)


def test_monitor_then_act_keeps_full_timeliness_credit(runs):
    # The ruled second opening: a concrete recheck commitment by the monitoring deadline plus
    # action on the confirmation earns the full timing points; the identical course WITHOUT
    # that commitment earns half of them, and nothing else about the two runs differs.
    monitored = runs["monitor_then_act"]
    unmonitored = runs["late_no_monitoring"]
    assert monitored["criteria"]["timely_evidence_response"] == pytest.approx(2.0)
    assert unmonitored["criteria"]["timely_evidence_response"] == pytest.approx(1.0)
    assert monitored["total"] - unmonitored["total"] == pytest.approx(1.0, abs=1e-6)
    assert monitored["total"] < runs["systemic_early"]["total"]   # the burden that ran meanwhile


def test_an_incomplete_course_earns_exactly_half_the_course_points(runs):
    partial = runs["partial_course"]
    assert partial["criteria"]["complete_control_course"] == pytest.approx(1.5)
    assert runs["systemic_early"]["criteria"]["complete_control_course"] == pytest.approx(3.0)
    # It also leaves more burden behind (no sustained suppression), so it loses on the outcome
    # channel as well as on the course criterion — never more than the two together.
    gap = runs["systemic_early"]["total"] - partial["total"]
    assert 1.5 <= gap <= 1.5 + 5.0


def test_a_monitoring_round_alone_earns_nothing(runs):
    # Pre-rebuild this path took ~5/10: it matched the action arm and the promptness latency
    # while the mites kept climbing. Monitoring is not control.
    assert runs["recheck_only"]["total"] == pytest.approx(0.0, abs=0.01)
    assert runs["do_nothing"]["total"] == pytest.approx(0.0, abs=0.01)
    assert runs["recheck_only"]["addressed"] != "addressed"


def test_control_after_the_deadline_keeps_course_credit_but_no_timing_credit(runs):
    # A late course is still a complete course and still removes real burden, so it keeps those
    # points; the response criterion pays nothing, and the outcome channel pays much less than
    # an early course's.
    late = runs["after_deadline"]
    assert late["criteria"]["timely_evidence_response"] == pytest.approx(0.0)
    assert late["criteria"]["complete_control_course"] == pytest.approx(3.0)
    assert 0.0 < late["criteria"]["control_outcome"] < runs["systemic_early"]["criteria"]["control_outcome"]
    assert late["total"] < runs["late_no_monitoring"]["total"]


def test_treating_the_wrong_house_earns_nothing(runs):
    assert runs["wrong_house"]["total"] == pytest.approx(0.0, abs=0.01)


# --------------------------------------------------------------------- pre-window banking


@pytest.mark.parametrize("path", ["banked_day0", "banked_day105"])
def test_a_course_banked_before_the_arc_scores_as_doing_nothing(runs, path):
    # A control course filed before the schedule seeds the infestation treats a house that
    # carries nothing: it is not a response to evidence that does not exist yet. Pre-rebuild
    # the day-0 booking banked the full 3 course points and the full 2 timing points (5.00/10)
    # and the day-105 booking — whose second and third applications straddle the seed — took a
    # perfect 10.00 by wiping the authored burden before it ever accrued.
    banked, nothing = runs[path], runs["do_nothing"]
    assert banked["total"] == pytest.approx(nothing["total"], abs=0.01) == pytest.approx(0.0, abs=0.01)
    for name in ("control_outcome", "complete_control_course", "timely_evidence_response"):
        assert banked["criteria"][name] == pytest.approx(nothing["criteria"][name], abs=0.01)


@pytest.mark.parametrize("path", ["banked_day0", "banked_day105"])
def test_the_authored_arc_survives_a_course_that_straddles_its_seed(runs, path):
    # The physics half of the same finding: a pre-arc course must not erase the day-112 seed.
    # `banked_day105` applies on 105, 112 and 119 — the middle one lands on the seed day — and
    # the burden it leaves behind must be the untreated one, hour for hour.
    banked, nothing = runs[path], runs["do_nothing"]
    assert banked["excess_index_days"] == pytest.approx(nothing["excess_index_days"], rel=1e-9)
    assert banked["index"] == pytest.approx(nothing["index"], rel=1e-9)


def test_a_recheck_ordered_before_the_arc_buys_no_commitment_credit(runs):
    # The monitoring latch is the second banking channel: a `schedule_vet_visit` on day 0 used
    # to satisfy the "committed to the recheck by the monitoring deadline" test and hand a late
    # course the full timing points. It now leaves no commitment on record at all, so the same
    # late course scores exactly like the one with no recheck behind it.
    banked, unmonitored = runs["banked_latch_then_late"], runs["late_no_monitoring"]
    assert banked["monitoring_day"] == -1
    assert banked["criteria"]["timely_evidence_response"] == pytest.approx(1.0)
    assert banked["total"] == pytest.approx(unmonitored["total"], abs=1e-6)
    # ...and the in-window recheck still earns it, so the fix removed the bank, not the rule.
    assert runs["monitor_then_act"]["criteria"]["timely_evidence_response"] == pytest.approx(2.0)


# --------------------------------------------------------------------- a lapsed course


def test_a_failed_course_does_not_lock_the_house_out_of_the_systemic_route(runs):
    # Missing the second dose used to be permanent: the dead order still counted as "already
    # with the practice", every later request was silently swallowed, and the only lawful
    # systemic route was closed for the rest of the cycle. A fresh order now runs a complete
    # course and earns the full course points.
    fresh = runs["failed_then_fresh"]
    assert fresh["criteria"]["complete_control_course"] == pytest.approx(3.0)
    assert len(fresh["charged_orders"]) == 2          # a second course is a second charge
    assert fresh["charged_orders"] == ["PAH-RX-H2-112", "PAH-RX-H2-133"]


def test_two_half_courses_on_two_orders_still_do_not_assemble(runs):
    # Completeness reads the BEST single order, never the union: reopening the route must not
    # become a way to bolt one dose onto another order's dose.
    fragments = runs["two_fragments"]
    assert fragments["criteria"]["complete_control_course"] == pytest.approx(1.5)
    assert len(fragments["charged_orders"]) == 2      # both fragments were paid for


def test_the_ruled_orderings_hold(runs):
    # Within a route, earlier and more complete always scores higher; every path that ran a
    # real course outscores the ones that ran none.
    assert runs["systemic_early"]["total"] > runs["monitor_then_act"]["total"]
    assert runs["monitor_then_act"]["total"] > runs["late_no_monitoring"]["total"]
    assert runs["late_no_monitoring"]["total"] > runs["after_deadline"]["total"]
    for name in ("systemic_early", "physical_early", "monitor_then_act", "late_no_monitoring",
                 "partial_course", "after_deadline"):
        assert runs[name]["total"] > runs["recheck_only"]["total"]


# --------------------------------------------------------------------- node metadata


def test_the_window_covers_the_confirming_trap_round():
    dp = next(
        d for d in load_schedule(REPO / "schedule").decision_points if d.id == DP
    )
    assert (dp.opens_day, dp.deadline_day) == (112, 168)
    events = load_schedule(REPO / "schedule").events
    confirm = next(
        e for e in events
        if e.persists_if_unaddressed == DP and "still climbing" in e.payload.get("subject", "")
    )
    assert dp.opens_day <= confirm.on_day <= dp.deadline_day
    # It still fires conditionally: a run that started control never sees it.
    assert confirm.persists_if_unaddressed == DP


def test_only_a_therapeutic_step_addresses_the_node():
    sig = next(
        d for d in load_schedule(REPO / "schedule").decision_points if d.id == DP
    ).signature
    tools = {m.tool for m in sig.any_of}
    assert tools == {"administer_vet_order", "book_ipm_service"}
    assert "log_treatment" not in tools and "schedule_vet_visit" not in tools


def test_the_criteria_are_the_ruled_five_three_two():
    dp = next(d for d in load_schedule(REPO / "schedule").decision_points if d.id == DP)
    crits = {c.name: c for c in dp.signature.scoring.criteria}
    assert crits["control_outcome"].points == 5
    assert crits["control_outcome"].channel == f"red_mite_excess_index_days[{HOUSE}]"
    assert crits["complete_control_course"].points == 3
    assert crits["complete_control_course"].channel == f"red_mite_course_shortfall[{HOUSE}]"
    assert crits["timely_evidence_response"].points == 2
    assert crits["timely_evidence_response"].channel == f"red_mite_response_lateness[{HOUSE}]"


def test_the_ordinal_channels_are_anchored_at_zero_and_two():
    # The 3 / 1.5 / 0 and 2 / 1 / 0 tiers ARE these anchors: the good reference completes a
    # course on time (deficit 0) and the negligent one never acts (deficit 2), so a run one
    # step short normalizes to exactly half credit. A regeneration that moved either anchor
    # would silently re-scale both criteria.
    for channel in (f"red_mite_course_shortfall[{HOUSE}]", f"red_mite_response_lateness[{HOUSE}]"):
        assert REFERENCES["good"][channel] == 0.0
        assert REFERENCES["negligent"][channel] == 2.0


def test_whole_house_heat_is_gone_from_the_control_menu():
    # Between-flock method, ruled off the occupied-house menu: it must not appear as an
    # authored option in the mail the model reads, and there is no lever that could earn it.
    for name in ("mite_w14", "mite_persist_w22"):
        body = (REPO / "corpus" / "documents" / "emails" / f"{name}.md").read_text().lower()
        assert "heat/ipm" not in body
    opening = (REPO / "corpus" / "documents" / "emails" / "mite_w14.md").read_text().lower()
    assert "between-flock" in opening      # named only as what it is NOT for
