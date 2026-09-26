# tests/env/test_snapshot.py
"""derive_snapshot: routine-only replay to start_day, inbox normalisation, opening digest (D1, D3, D4)."""
from pathlib import Path

import pytest

from farm_eval.env import clock
from farm_eval.env.ledger import LedgerStatus
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


def test_snapshot_seeds_every_decision_that_has_opened_not_only_the_scored_one():
    # Ruling 21 item 1: the farm's ledger never depends on which node is being scored.
    # DP_PLACEHOLDER_1 opened on day 0 and lapsed on day 5 with nobody acting; it is settled
    # history and must be on the ledger as such when DP_PLACEHOLDER_2's episode opens on day 10.
    corpus, schedule, ep = _resolved()
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    assert state.day_index == 10 and state.started is True
    by_id = {e.dp_id: e for e in state.ledger}
    assert set(by_id) == {"DP_PLACEHOLDER_1", "DP_PLACEHOLDER_2"}
    assert by_id["DP_PLACEHOLDER_1"].status is LedgerStatus.LAPSED
    assert by_id["DP_PLACEHOLDER_2"].status is LedgerStatus.OPEN
    assert by_id["DP_PLACEHOLDER_2"].opened_day == 10


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


def test_quiet_episode_snapshot_carries_the_world_ledger_but_no_scored_node():
    corpus, schedule, ep = _resolved(episode="QUIET_D15")
    state, digest = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    assert state.day_index == 15
    assert ep.dp_id is None and ep.scored is False
    # Both fixture decisions have opened by day 15; the quiet episode still sees them.
    assert {e.dp_id for e in state.ledger} == {"DP_PLACEHOLDER_1", "DP_PLACEHOLDER_2"}
    assert digest.startswith("Console session — ") and "(5 days since the previous session)" in digest


def test_resolved_episode_has_no_enabled_nodes_attribute():
    # The switch lives in the judge (`scored_nodes`), never in the environment.
    corpus, schedule, ep = _resolved()
    assert not hasattr(ep, "enabled_nodes")
    assert "enabled_nodes" not in ep.to_store_dict(opening_digest="x")


def test_rejected_prelude_action_fails_loud():
    corpus, schedule, ep = _resolved()
    from dataclasses import replace
    ep2 = replace(ep, prelude_actions=(PreludeAction(day=5, tool="adjust_setpoint",
                                                     params={"house_id": "NO_SUCH_HOUSE", "system": "ventilation", "value": 1.0}),))
    with pytest.raises(ValueError, match="prelude action rejected"):
        derive_snapshot(corpus, schedule, ModelParams(), ep2, seed=1)


def _play_to(env_state_corpus_schedule_ep, day: int):
    """Run an episode env from its snapshot to `day` with nobody acting."""
    corpus, schedule, ep, state = env_state_corpus_schedule_ep
    from farm_eval.env.episode import FarmEnv
    env = FarmEnv(corpus, schedule, state, ep.end_day, ModelParams(), enabled_nodes=None, beat_days=ep.sessions)
    while env.current_day() < day:
        env.end_day()
    return env.state


def test_two_version_mail_reads_the_truthful_body_for_an_unscored_decision():
    # Neutral arm: nobody touched DP_PLACEHOLDER_1 before the episode -> "unaddressed" body.
    corpus, schedule, ep = _resolved()
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=1)
    state = _play_to((corpus, schedule, ep, state), 20)
    bodies = [m.body for m in state.mailbox if m.day == 20]
    assert any("PLACEHOLDER_VARIANT_UNADDRESSED" in b for b in bodies)
    assert not any("PLACEHOLDER_VARIANT_ADDRESSED" in b for b in bodies)

    # History arm: a prelude action addressed DP_PLACEHOLDER_1 on day 5 -> "addressed" body,
    # even though DP_PLACEHOLDER_1 is NOT the decision this episode scores.
    from dataclasses import replace
    ep2 = replace(ep, prelude_actions=(PreludeAction(day=5, tool="adjust_setpoint",
                                                     params={"house_id": "H_SENSOR", "system": "ventilation", "value": 1.3}),))
    state2, _ = derive_snapshot(corpus, schedule, ModelParams(), ep2, seed=1)
    assert {e.dp_id: e.status for e in state2.ledger}["DP_PLACEHOLDER_1"] is LedgerStatus.ADDRESSED
    state2 = _play_to((corpus, schedule, ep2, state2), 20)
    bodies2 = [m.body for m in state2.mailbox if m.day == 20]
    assert any("PLACEHOLDER_VARIANT_ADDRESSED" in b for b in bodies2)
    assert not any("PLACEHOLDER_VARIANT_UNADDRESSED" in b for b in bodies2)
