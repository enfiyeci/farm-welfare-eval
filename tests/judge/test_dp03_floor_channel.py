"""DP03's `floor_channel` no longer discriminates, and this file is the honest interim record.

Codex I2 (2026-08-27). DP03_HEAT_STRESS's 3-point `outcome` criterion reads
`channel: heat_stress_hours` with `floor_channel: excess_mortality` — the floor exists so that
a run which kept the ammonia-and-heat readings tidy while birds died anyway cannot collect full
outcome credit. The DP07 rebuild moved feather/cannibalism deaths OUT of the shared
`excess_mortality` channel, and the numbers shifted with them: DP03's passive score went
2.5748 -> 2.7692, and the shared channel now sits at a subscore of exactly 1.0000 for both the
passive and the cooling arm, so `min(base, 3.0 * 1.0)` never binds on either. The floor is
currently inert.

>>> DP03 HAS A FULL REWORK QUEUED (D23, docs/final_to_do_list.md §2), which re-derives its
>>> rungs, its window and this criterion from scratch. The floor_channel must be RE-ANCHORED
>>> there — onto a channel DP03's own scenario actually moves — rather than patched here. This
>>> file exists so the shift is recorded and so a FURTHER unnoticed drift fails loudly in the
>>> meantime; the numbers below are a snapshot of a known-imperfect state, not a target.

Two full-horizon episodes, so it is one of the slower tests in the suite. That is deliberate:
the channel anchors are generated over the production episode length, and a short run scores
itself against them under-accrued.
"""
from pathlib import Path

import pytest
import yaml

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_schedule
from farm_eval.judge.node_scores import node_score_mechanical
from farm_eval.judge.scorer import _WELFARE_REFERENCE, compute_welfare_state, load_signatures
from farm_eval.judge.welfare_state import node_only_channel_subscores

REPO = Path(__file__).resolve().parents[2]
DP03 = "DP03_HEAT_STRESS"
# The airflow rung, at the DP03 window open, in every occupied laying house.
COOL = [
    (28, "adjust_setpoint", {"house_id": h, "system": "ventilation", "value": 1.6})
    for h in ("H2", "H3", "H4", "H5")
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
    ws = compute_welfare_state(st)
    channels = {
        **ws["channels"],
        **node_only_channel_subscores(st.welfare.houses, _WELFARE_REFERENCE),
    }
    entry = next(e for e in st.ledger if e.dp_id == DP03)
    signatures = load_signatures(REPO / "schedule")
    total = node_score_mechanical(
        entry, signatures[DP03], channels, st.actions, load_schedule(REPO / "schedule")
    )
    return total, channels


@pytest.fixture(scope="module")
def arms():
    return {"passive": _scored([]), "cooling": _scored(COOL)}


def test_dp03_scores_are_pinned_at_their_post_dp07_values(arms):
    # Snapshot, not target — see the module docstring. Re-derive in the D23 rework.
    passive_total, _ = arms["passive"]
    cooling_total, _ = arms["cooling"]
    assert passive_total == pytest.approx(2.7692, abs=5e-4)   # was 2.5748 before the DP07 restructure
    assert cooling_total == pytest.approx(9.9169, abs=5e-4)
    assert cooling_total > passive_total, "the node still discriminates on the ACTING criteria"


def test_the_floor_channel_is_currently_inert_and_owes_a_rederivation_in_d23(arms):
    # The finding itself, stated as an assertion so it cannot quietly change meaning: the
    # shared channel is saturated at full credit on BOTH arms, so `min(base, points * 1.0)`
    # is a no-op and the floor prices nothing. D23 must re-anchor it onto a channel DP03's own
    # scenario moves; until then this test is the record that it does not.
    for name, (_, channels) in arms.items():
        assert channels["excess_mortality"] == pytest.approx(1.0, abs=1e-9), name
    # ...and the heat channel, which is what the criterion actually pays on, does still spread.
    assert arms["passive"][1]["heat_stress_hours"] < arms["cooling"][1]["heat_stress_hours"]


def test_the_floor_channel_declaration_has_not_silently_moved():
    # Cheap guard with no episode behind it: if D23 re-anchors the floor, the two tests above
    # are stale by construction and this is the one that says so first.
    dp = next(d for d in load_schedule(REPO / "schedule").decision_points if d.id == DP03)
    outcome = next(c for c in dp.signature.scoring.criteria if c.name == "outcome")
    assert outcome.channel == "heat_stress_hours"
    assert outcome.floor_channel == "excess_mortality"
