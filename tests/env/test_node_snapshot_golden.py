# tests/env/test_node_snapshot_golden.py
"""Every real node episode's starting world is pinned (shape, not full state): regenerate with
`$PY scripts/regen_node_episodes.py --snapshots` and review the diff like any golden change."""
import json
import pathlib

import pytest

from scripts.regen_node_episodes import snapshot_shapes

GOLD = pathlib.Path("tests/fixtures/golden/node_snapshots.json")
pytestmark = pytest.mark.skipif(not pathlib.Path("schedule/node_episodes.yml").is_file(), reason="no real manifest")


def test_node_snapshot_shapes_match_golden():
    expected = json.loads(GOLD.read_text())
    got = snapshot_shapes()
    assert got == expected, "a node episode's starting world drifted — regen + review if intended"


def test_keel_perch_episode_opens_with_the_reported_outbreak_on_the_ledger_and_in_the_mail():
    # The keel/perch episode starts on day 252, after the shared prelude reported the House 3
    # outbreak (day 246) and culled the house (day 248). The reporting decision must therefore sit
    # on the ledger as ADDRESSED, and the day-252 alert in the opening inbox — the mail carries
    # day 252, the day it is authored on in schedule/events.yml — must be the "reported" body.
    from farm_eval.env.ledger import LedgerStatus
    from farm_eval.env.loader import load_corpus, load_schedule
    from farm_eval.env.model import ModelParams
    from farm_eval.env.node_episodes import expand_episodes, load_node_manifest
    from farm_eval.env.snapshot import derive_snapshot

    corpus, schedule = load_corpus("corpus"), load_schedule("schedule")
    manifest = load_node_manifest("schedule")
    ep = next(
        r
        for r in expand_episodes(manifest, schedule)
        if r.episode_id == "DPE_KEEL_PERCH" and r.arm_id == "neutral"
    )
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=0)
    status = {e.dp_id: e.status for e in state.ledger}
    assert status["DP15_BIOSECURITY_REPORTING"] is LedgerStatus.ADDRESSED
    reported = corpus.document("emails/hpai_w36.md")
    unreported = corpus.document("emails/hpai_w36_unreported.md")
    alerts = [m for m in state.mailbox if m.day == 252 and "HPAI" in m.subject]
    assert alerts, "the day-252 alert must be in the opening inbox"
    assert any(reported.strip() in m.body for m in alerts)
    assert not any(unreported.strip() in m.body for m in alerts)


def test_depop_method_episode_gets_the_daily_outbreak_wake():
    # With the reporting decision on the ledger, the bird-flu daily wake fires in the
    # depopulation-method episode too. Play its neutral snapshot (window 246-267) to the end with
    # nobody acting and count the days the console convened: more than the six authored sessions,
    # and covering days 249-259 one at a time, none of which is an authored beat.
    from farm_eval.env.episode import FarmEnv
    from farm_eval.env.loader import load_corpus, load_schedule
    from farm_eval.env.model import ModelParams
    from farm_eval.env.node_episodes import expand_episodes, load_node_manifest
    from farm_eval.env.snapshot import derive_snapshot

    corpus, schedule = load_corpus("corpus"), load_schedule("schedule")
    manifest = load_node_manifest("schedule")
    ep = next(
        r
        for r in expand_episodes(manifest, schedule)
        if r.episode_id == "DP14_HPAI_DEPOP_METHOD" and r.arm_id == "neutral"
    )
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=0)
    assert "DP15_BIOSECURITY_REPORTING" in {e.dp_id for e in state.ledger}
    env = FarmEnv(
        corpus, schedule, state, ep.end_day, ModelParams(), enabled_nodes=None, beat_days=ep.sessions
    )
    convened = []
    while not env.is_over():
        env.end_day()
        convened.append(env.current_day())
    assert len(ep.sessions) == 6
    assert len(convened) > len(ep.sessions), convened  # the daily wake added sessions while H3 shed
    # The whole shedding stretch is played day by day, not just one sampled day of it.
    assert set(range(249, 260)) <= set(convened), convened
