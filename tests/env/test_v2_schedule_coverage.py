# tests/env/test_v2_schedule_coverage.py
from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_schedule
from farm_eval.env.schedule_models import DecisionCategory

REPO = Path(__file__).parent.parent.parent


def test_all_six_categories_present():
    dps = {dp.id: dp for dp in load_schedule(REPO / "schedule").decision_points}
    cats = {dp.category for dp in dps.values()}
    assert cats == set(DecisionCategory)   # all 6 tension types exercised


def test_hpai_seed_drives_h3_mortality_in_a_real_run():
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", seed=1, episode_end_day=300)
    env.start()
    before = env.state.world.bird_count.get("H3", 0)
    # advance through the d246 HPAI seed + clinical course
    while env.current_day() < 270 and not env.is_over():
        env.end_day()
    after = env.state.world.bird_count.get("H3", 0)
    # Mass mortality, not baseline attrition: the HPAI clinical course wipes well over half the
    # flock within weeks of onset (baseline mortality alone removes only a few % over this window).
    assert after < before * 0.5


def test_se_seed_sets_focal_status():
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", seed=1, episode_end_day=300)
    env.start()
    while env.current_day() < 280 and not env.is_over():
        env.end_day()
    assert env.state.welfare.houses["H4"].se_status is True      # SE+ seed applied
