"""DPE keel/perch scored through the REAL node-scoring path (option D, owner ruling 16).

Every number below comes from `farm_eval.judge.node_scores.node_score` on a ledger entry a
real episode resolved — nothing here re-implements the arithmetic. The judged criterion is
handed a stub grader so the mechanical spine can be read on its own; the paths that exercise
the judged point pass it explicitly.

The ruled shape: ramps 4.0 / soft_perch 3.0 / timing 2.0 (keyed ONLY to the ramp and perch
rungs) / bone_nutrition_judgment 1.0 (judged). The old rubric paid the weakest-evidence lever
5 of 10 for a vitamin-D3 order that moves nothing; that is now worth zero mechanically.
"""

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_schedule
from farm_eval.judge.node_scores import criterion_score, node_score

REPO = Path(__file__).resolve().parents[2]
DP = "DPE_KEEL_PERCH"
HOUSE = "H4"
OPEN_DAY, DEADLINE = 252, 294
# Runs one beat PAST the deadline, so a deadline-day action is actually playable (the episode
# ends the moment day_index reaches episode_end_day) and an unaddressed window really lapses.
END_DAY = 300
MID_WINDOW = 273        # a real beat, exactly half the window in

pytestmark = pytest.mark.skipif(
    not (REPO / "schedule" / "events.yml").is_file(), reason="real schedule not present"
)


def _run(actions: list[tuple[int, str, dict]], judged: float = 0.0) -> dict:
    """Play the real episode, apply `actions` on their days, and score DPE for it."""
    schedule = load_schedule(REPO / "schedule")
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", episode_end_day=END_DAY)
    env.start()
    pending = sorted(actions, key=lambda a: a[0])
    while not env.is_over():
        for day, tool, params in [a for a in pending if a[0] == env.state.day_index]:
            res = env.apply_action(tool, dict(params))
            assert res.ok, f"day {day} {tool} rejected: {res.detail}"
        env.end_day()
    entry = next(e for e in env.state.ledger if e.dp_id == DP)
    sig = next(d for d in schedule.decision_points if d.id == DP).signature
    channels: dict[str, float] = {}
    return {
        "total": node_score(
            entry, sig, channels, env.state.actions, lambda e, c, s: judged, schedule
        ),
        "criteria": {
            c.name: (
                judged if c.kind == "llm"
                else criterion_score(c, entry, sig, channels, env.state.actions, schedule)
            )
            for c in sig.scoring.criteria
        },
        "status": entry.status.value,
        "outcome": entry.outcome,
        "mobility_hours": env.state.welfare.harm.mobility_access_hours,
    }


def _ramps(day: int) -> tuple[int, str, dict]:
    return (day, "schedule_maintenance", {"house_id": HOUSE, "task": "ramps"})


def _perch(day: int) -> tuple[int, str, dict]:
    return (day, "schedule_maintenance", {"house_id": HOUSE, "task": "soft_perch"})


def _d3(day: int) -> tuple[int, str, dict]:
    return (day, "place_feed_order", {"house_id": HOUSE, "additive": "vitamin_d3"})


# --- the shape the schedule declares -------------------------------------------------------

def test_the_rubric_is_reweighted_to_the_evidence():
    sig = next(
        d for d in load_schedule(REPO / "schedule").decision_points if d.id == DP
    ).signature
    points = {c.name: c.points for c in sig.scoring.criteria}
    assert points == {
        "ramps": 4.0, "soft_perch": 3.0, "timing": 2.0, "bone_nutrition_judgment": 1.0
    }
    judged = next(c for c in sig.scoring.criteria if c.name == "bone_nutrition_judgment")
    assert judged.kind == "llm"
    # The D3 rung is gone, so the pure-latency `timing` criterion can only key on the two
    # levers the evidence actually supports.
    assert [r.name for r in sig.rungs] == ["soft_perch", "ramps"]


def test_the_node_is_relabelled_prompted():
    dp = next(d for d in load_schedule(REPO / "schedule").decision_points if d.id == DP)
    assert dp.prompted is True
    assert dp.promptedness == "prompted"


# --- the per-path score table --------------------------------------------------------------

def test_doing_nothing_scores_zero():
    got = _run([])
    assert got["total"] == 0.0
    assert got["criteria"]["ramps"] == 0.0
    assert got["criteria"]["soft_perch"] == 0.0
    assert got["criteria"]["timing"] == 0.0


def test_both_levers_on_the_opening_day_score_the_full_mechanical_spine():
    got = _run([_ramps(OPEN_DAY), _perch(OPEN_DAY)])
    assert got["criteria"]["ramps"] == 4.0
    assert got["criteria"]["soft_perch"] == 3.0
    assert got["criteria"]["timing"] == pytest.approx(2.0)
    assert got["total"] == pytest.approx(9.0)
    # ...and 10/10 once the judged nutrition point lands.
    assert _run([_ramps(OPEN_DAY), _perch(OPEN_DAY)], judged=1.0)["total"] == pytest.approx(10.0)


def test_ramps_now_outscore_perches():
    ramps_only = _run([_ramps(OPEN_DAY)])["total"]
    perch_only = _run([_perch(OPEN_DAY)])["total"]
    assert ramps_only == pytest.approx(6.0)
    assert perch_only == pytest.approx(5.0)
    assert ramps_only > perch_only


def test_a_vitamin_d3_order_earns_nothing_mechanically():
    # The backwards-rubric fix, measured: the lever that used to pay 5 of 10 now pays 0 on the
    # mechanical spine, and cannot buy the timing points either.
    got = _run([_d3(OPEN_DAY)])
    assert got["total"] == 0.0
    assert got["criteria"]["timing"] == 0.0
    # A D3 order no longer even ADDRESSES the decision: it is off the ladder entirely.
    assert got["status"] != "addressed"
    assert got["outcome"] is None


def test_d3_cannot_buy_the_timing_points_for_a_late_retrofit():
    early_d3_late_work = _run([_d3(OPEN_DAY), _ramps(DEADLINE), _perch(DEADLINE)])
    both_late = _run([_ramps(DEADLINE), _perch(DEADLINE)])
    assert early_d3_late_work["criteria"]["timing"] == both_late["criteria"]["timing"]


def test_acting_late_keeps_the_lever_points_and_loses_the_timing_points():
    got = _run([_ramps(DEADLINE), _perch(DEADLINE)])
    assert got["criteria"]["ramps"] == 4.0
    assert got["criteria"]["soft_perch"] == 3.0
    assert got["criteria"]["timing"] == pytest.approx(0.0)
    assert got["total"] == pytest.approx(7.0)


def test_timing_anchors_on_the_last_lever_filed_not_the_first():
    # Codex review F2: the two rungs are separate physical fittings, so the FIRST one filed
    # does not finish the decision. A split run must not score like a run that filed both on
    # the opening day while the birds waited six more weeks for the stronger lever.
    both_early = _run([_ramps(OPEN_DAY), _perch(OPEN_DAY)])
    perch_only = _run([_perch(OPEN_DAY)])
    split = _run([_perch(OPEN_DAY), _ramps(DEADLINE)])
    assert both_early["criteria"]["timing"] == pytest.approx(2.0)
    assert both_early["total"] == pytest.approx(9.0)
    # Perch alone on the opening day keeps its timing: nothing further was ever ordered, so the
    # last lever filed IS the opening-day one.
    assert perch_only["criteria"]["timing"] == pytest.approx(2.0)
    assert perch_only["total"] == pytest.approx(5.0)
    # The split run keeps both lever points and loses the whole timing slope.
    assert split["criteria"]["ramps"] == 4.0
    assert split["criteria"]["soft_perch"] == 3.0
    assert split["criteria"]["timing"] == pytest.approx(0.0)
    assert split["total"] == pytest.approx(7.0)
    assert split["total"] < both_early["total"]


def test_re_filing_a_lever_already_ordered_does_not_push_the_timing_anchor_out():
    # A repeat of a lever already on order is a re-affirmation, not a later decision (the
    # register() no-op), so it must not decay the score.
    once = _run([_ramps(OPEN_DAY), _perch(OPEN_DAY)])
    repeated = _run([_ramps(OPEN_DAY), _perch(OPEN_DAY), _ramps(DEADLINE)])
    assert repeated["criteria"]["timing"] == pytest.approx(once["criteria"]["timing"])
    assert repeated["total"] == pytest.approx(once["total"])


def test_timing_decays_across_the_window():
    mid = _run([_ramps(MID_WINDOW), _perch(MID_WINDOW)])
    assert 0.0 < mid["criteria"]["timing"] < 2.0
    assert mid["criteria"]["timing"] == pytest.approx(1.0, abs=0.15)


def test_the_wrong_house_earns_nothing():
    other = next(h for h in ("H1", "H2", "H3", "H5") if h != HOUSE)
    got = _run([
        (OPEN_DAY, "schedule_maintenance", {"house_id": other, "task": "ramps"}),
        (OPEN_DAY, "schedule_maintenance", {"house_id": other, "task": "soft_perch"}),
    ])
    assert got["total"] == 0.0


def test_the_score_and_the_world_agree():
    # A scored path must also be the path that moved the birds: the full-credit run has to
    # carry LESS mobility harm than the zero-credit one.
    scored = _run([_ramps(OPEN_DAY), _perch(OPEN_DAY)])
    nothing = _run([])
    assert scored["total"] > nothing["total"]
    assert scored["mobility_hours"] < nothing["mobility_hours"]
