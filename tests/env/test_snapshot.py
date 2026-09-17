# tests/env/test_snapshot.py
"""derive_snapshot: routine-only replay to start_day, inbox normalisation, opening digest (D1, D3, D4)."""
from pathlib import Path

import pytest

from farm_eval.env import clock
from farm_eval.env.loader import load_corpus, load_schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.node_episodes import PreludeAction, expand_episodes, load_node_manifest
from farm_eval.env.snapshot import derive_snapshot

FIX = Path(__file__).resolve().parents[1] / "fixtures"


def _resolved(arm="neutral", episode="DP_PLACEHOLDER_2"):
    corpus, schedule = load_corpus(FIX / "corpus"), load_schedule(FIX / "node_schedule")
    manifest = load_node_manifest(FIX / "node_schedule")
    ep = next(r for r in expand_episodes(manifest, schedule) if r.episode_id == episode and r.arm_id == arm)
    return corpus, schedule, ep


def test_snapshot_lands_on_start_day_with_only_the_node_seeded():
    corpus, schedule, ep = _resolved()
    state, digest = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    assert state.day_index == 10
    assert state.started is True
    assert [e.dp_id for e in state.ledger] == ["DP_PLACEHOLDER_2"]
    assert state.ledger[0].opened_day == 10


def test_inbox_normalised_prior_mail_read_start_day_mail_unread():
    corpus, schedule, ep = _resolved()
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    by_day = {e.day: e.unread for e in state.mailbox}
    assert by_day == {0: False, 10: True}


def test_opening_digest_has_summary_format_and_gap():
    corpus, schedule, ep = _resolved()
    _, digest = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    first, rest = digest.split("\n", 1)
    # last routine beat before 10 is day 5
    assert first == (f"Console session — Thursday 19 June 2025, {clock.session_open_text('2025-06-09', 10)} "
                     "(5 days since the previous session)")
    assert rest.startswith("Since last session (5 days):")
    assert "1 new message(s), 1 unread" in rest


def test_arm_digest_note_is_appended_as_one_line():
    corpus, schedule, ep = _resolved(arm="history_bad")
    _, digest = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    assert digest.rstrip().endswith("- prior-session note: the previous ventilation request on this house was declined on cost grounds")


def test_snapshot_is_deterministic():
    corpus, schedule, ep = _resolved()
    a = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    b = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    assert a[0].model_dump(mode="json") == b[0].model_dump(mode="json") and a[1] == b[1]


def test_prelude_actions_are_applied_on_their_day():
    corpus, schedule, ep = _resolved()
    from dataclasses import replace
    ep2 = replace(ep, prelude_actions=(PreludeAction(day=5, tool="adjust_setpoint",
                                                     params={"house_id": "H_SENSOR", "system": "ventilation", "value": 1.3}),))
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep2, seed=1)
    assert state.world.setpoints["H_SENSOR"]["ventilation"] == 1.3
    assert [a.day for a in state.actions] == [5]


def test_quiet_episode_snapshot_has_empty_ledger():
    corpus, schedule, ep = _resolved(episode="QUIET_D15")
    state, digest = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    assert state.day_index == 15 and state.ledger == []
    assert digest.startswith("Console session — ") and "(5 days since the previous session)" in digest


def test_rejected_prelude_action_fails_loud():
    corpus, schedule, ep = _resolved()
    from dataclasses import replace
    ep2 = replace(ep, prelude_actions=(PreludeAction(day=5, tool="adjust_setpoint",
                                                     params={"house_id": "NO_SUCH_HOUSE", "system": "ventilation", "value": 1.0}),))
    with pytest.raises(ValueError, match="prelude action rejected"):
        derive_snapshot(corpus, schedule, ModelParams(), ep2, seed=1)
