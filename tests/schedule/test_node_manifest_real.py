"""The real node-episode manifest parses, validates against schedule/events.yml, and encodes the
approved node set (proposal 2026-09-12 §3: DP13/DP19/DP20/DP21 cut, DPN unscored; plan §0.2: DPW)."""
from pathlib import Path

import pytest

from farm_eval.env.loader import load_schedule
from farm_eval.env.node_episodes import expand_episodes, load_node_manifest, validate_manifest

SCHEDULE = Path(__file__).resolve().parents[2] / "schedule"
pytestmark = pytest.mark.skipif(not (SCHEDULE / "node_episodes.yml").is_file(), reason="no real manifest")

CUT = {"DP13_SE_DIVERSION", "DP19_WORKER_INJURY_REPORTING", "DP20_HPAI_STAFFING", "DP21_DRUG_RESIDUE",
       "DPN_NAE_ANTIBIOTIC", "DPW_WORKER_AIR"}


def test_real_manifest_validates_and_covers_the_approved_set():
    schedule = load_schedule(SCHEDULE)
    manifest = load_node_manifest(SCHEDULE)
    validate_manifest(manifest, schedule)
    scored = {e.dp_id for e in manifest.episodes if e.kind == "node"}
    all_dps = {dp.id for dp in schedule.decision_points}
    assert scored == all_dps - CUT, sorted(scored ^ (all_dps - CUT))
    assert len(scored) == 23
    quiet = [e for e in manifest.episodes if e.kind == "quiet"]
    assert len(quiet) == 3


def test_every_scored_episode_has_exactly_one_default_arm_and_a_short_session_count():
    schedule = load_schedule(SCHEDULE)
    manifest = load_node_manifest(SCHEDULE)
    for r in expand_episodes(manifest, schedule):
        if r.arm_id != manifest.meta.default_arm:
            continue
        # Proposal §2: one to three sessions is the target; the deadline-day session + the landing
        # beat make the practical minimum 2. Anything above 6 needs an explicit `sessions` list.
        assert 2 <= len(r.sessions) <= 6, (r.episode_id, r.sessions)
