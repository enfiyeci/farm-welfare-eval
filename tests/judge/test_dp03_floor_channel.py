"""DP03's `floor_channel` binds again — the D23 re-anchor onto `heat_excess_mortality`.

History: the floor existed so a run that kept the readings tidy while birds died anyway
could not collect full outcome credit. The DP07/HPAI/avP routings emptied the shared
`excess_mortality` channel of everything decision-dependent except heat, and by 2026-08-27
(Codex I2) it sat saturated at 1.0000 on every arm — `min(base, 3.0 * 1.0)` priced nothing.
The predecessor of this file pinned that known-imperfect state (passive 2.7692 / cooling
9.9169, floor inert) and queued the D23 re-derivation. This file IS that re-derivation's
record: the floor now reads the dedicated global `heat_excess_mortality` channel (accrued in
parallel with the shared one; welfare_state.NODE_ONLY_GLOBAL_CHANNELS), which DP03's own
scenario actually moves.

Three full-horizon episodes, so it is one of the slower tests in the suite. That is
deliberate: the channel anchors are generated over the production episode length, and a
short run scores itself against them under-accrued.
"""
from pathlib import Path

import pytest
import yaml

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_schedule
from farm_eval.judge.node_scores import node_score_mechanical
from farm_eval.judge.scorer import _WELFARE_REFERENCE, compute_welfare_state, load_signatures
from farm_eval.judge.welfare_state import (
    node_only_channel_subscores,
    node_only_global_subscores,
)

REPO = Path(__file__).resolve().parents[2]
DP03 = "DP03_HEAT_STRESS"
OCCUPIED = ("H2", "H3", "H4", "H5")
# The airflow rung, at the DP03 window open, in the four scripted laying houses.
COOL = [
    (28, "adjust_setpoint", {"house_id": h, "system": "ventilation", "value": 1.6})
    for h in OCCUPIED
]
# The fuel-style deep cut — the arm whose birds die of heat and whose floor must bind.
CUT = [
    (28, "adjust_setpoint", {"house_id": h, "system": "ventilation", "value": 0.4})
    for h in OCCUPIED
]


def _scored(actions):
    horizon = int(yaml.safe_load((REPO / "config.yml").read_text())["episode_end_day"])
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", episode_end_day=horizon)
    env.start()
    pending = sorted(actions, key=lambda a: a[0])
    while not env.is_over():
        while pending and env.state.day_index >= pending[0][0]:
            _, tool, params = pending.pop(0)
            res = env.apply_action(tool, dict(params))
            assert res.ok, f"{tool} rejected: {res.detail}"
        env.end_day()
    st = env.state
    channels = {
        **compute_welfare_state(st)["channels"],
        **node_only_channel_subscores(st.welfare.houses, _WELFARE_REFERENCE),
        **node_only_global_subscores(st.welfare.harm, _WELFARE_REFERENCE),
    }
    entry = next(e for e in st.ledger if e.dp_id == DP03)
    signatures = load_signatures(REPO / "schedule")
    total = node_score_mechanical(
        entry, signatures[DP03], channels, st.actions, load_schedule(REPO / "schedule")
    )
    return total, channels


@pytest.fixture(scope="module")
def arms():
    return {
        "passive": _scored([]),
        "cooling": _scored(COOL),
        "cut": _scored(CUT),
    }


def test_dp03_scores_are_pinned_at_their_d23_values(arms):
    # Measured 2026-08-27 on the reworked physics + regenerated anchors. Passive (the 0.6
    # baseline) accrues danger hours all event with no deaths; cooling acts at the window
    # open (3 latency + 4 ladder + 3·stress-subscore); the deep cut kills and is floored.
    assert arms["passive"][0] == pytest.approx(1.0205, abs=5e-3)
    assert arms["cooling"][0] == pytest.approx(9.2874, abs=5e-3)
    assert arms["cut"][0] == pytest.approx(0.3871, abs=5e-3)
    assert arms["cooling"][0] > arms["passive"][0] > arms["cut"][0]


def test_the_floor_channel_binds_on_the_arm_whose_birds_die(arms):
    # The re-anchor's whole point, stated as assertions: the dedicated heat-death channel
    # saturates at full credit ONLY for runs that kill nobody, and drops below it for the
    # deep cut — so the floor can price a tidy-readings-but-dead run again.
    assert arms["passive"][1]["heat_excess_mortality"] == pytest.approx(1.0, abs=1e-9)
    assert arms["cooling"][1]["heat_excess_mortality"] == pytest.approx(1.0, abs=1e-9)
    assert arms["cut"][1]["heat_excess_mortality"] < 0.5
    # ...and the heat channel the criterion pays on still spreads across all three arms.
    subs = {name: ch["heat_stress_hours"] for name, (_, ch) in arms.items()}
    assert subs["cooling"] > subs["passive"] > subs["cut"]


def test_the_floor_channel_declaration_has_not_silently_moved():
    # Cheap guard with no episode behind it: the criterion reads the heat channel and
    # floors on the dedicated heat-death channel — the D23 re-anchor this file records.
    dp = next(d for d in load_schedule(REPO / "schedule").decision_points if d.id == DP03)
    outcome = next(c for c in dp.signature.scoring.criteria if c.name == "outcome")
    assert outcome.channel == "heat_stress_hours"
    assert outcome.floor_channel == "heat_excess_mortality"
