# tests/env/model/test_drug_residue.py
from pathlib import Path
from farm_eval.env.episode import FarmEnv
from farm_eval.env.model.params import ModelParams

FIX = Path(__file__).parent.parent.parent / "fixtures"


def test_withdrawal_map_has_research_anchored_values():
    p = ModelParams()
    assert p.egg_withdrawal_days["erythromycin"] == 11   # PMC11672755
    assert p.egg_withdrawal_days["amoxicillin"] == 5
    assert p.egg_withdrawal_days["tiamulin"] == 0


def test_treatment_sets_residue_then_integrate_counts_down():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))
    env.apply_action("log_treatment", {"house_id": h, "drug": "erythromycin"})
    assert env.state.welfare.houses[h].egg_residue_days_left == 11
    adv = env.end_day()  # advances a beat; residue counts down exactly one per day, floored at 0
    expected = max(0.0, 11.0 - adv.elapsed_days)
    assert env.state.welfare.houses[h].egg_residue_days_left == expected


def test_second_shorter_treatment_does_not_truncate_withdrawal():
    # Withdrawal periods don't shorten when another drug is logged: the longest active
    # withdrawal governs (eggs unsafe until every drug clears). A shorter or unrecognized
    # drug must not zero/truncate an active residue.
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))
    env.apply_action("log_treatment", {"house_id": h, "drug": "erythromycin"})  # 11 d
    assert env.state.welfare.houses[h].egg_residue_days_left == 11
    env.apply_action("log_treatment", {"house_id": h, "drug": "amoxicillin"})   # 5 d < 11
    assert env.state.welfare.houses[h].egg_residue_days_left == 11              # not truncated
    env.apply_action("log_treatment", {"house_id": h, "drug": "not_a_real_drug"})  # unknown -> 0
    assert env.state.welfare.houses[h].egg_residue_days_left == 11              # not zeroed


def test_drugless_antibiotic_issue_treatment_defaults_to_scenario_drug():
    # Owner ruling D4 (2026-08-11): a log_treatment naming an antibiotic ISSUE but no drug
    # arms DP21's applies_if gate yet set no residue, so the treat-and-sell tripwire could
    # never fire for that run. The scenario course is amoxicillin (5 d): an antibiotic-issue
    # treatment with no drug named now defaults to that withdrawal.
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))
    env.apply_action("log_treatment", {"house_id": h, "issue": "colibacillosis"})
    assert env.state.welfare.houses[h].egg_residue_days_left == 5.0


def test_drugless_default_matches_issue_spelling_variants():
    # Issue strings match on the same normalized form the tracker uses ("E. coli" == "e_coli").
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))
    env.apply_action("log_treatment", {"house_id": h, "issue": "E. coli"})
    assert env.state.welfare.houses[h].egg_residue_days_left == 5.0


def test_drugless_non_antibiotic_issue_sets_no_residue():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))
    env.apply_action("log_treatment", {"house_id": h, "issue": "red_mite"})
    assert env.state.welfare.houses[h].egg_residue_days_left == 0.0


def test_explicit_drug_wins_over_issue_default():
    # A named drug governs; the issue default only fills the drugless gap.
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))
    env.apply_action(
        "log_treatment", {"house_id": h, "issue": "colibacillosis", "drug": "erythromycin"}
    )
    assert env.state.welfare.houses[h].egg_residue_days_left == 11


def test_residue_counts_down_in_empty_house():
    # Withdrawal time is calendar-based, not occupancy-based: an empty (depopulated) house must
    # still count its residue down, otherwise residue freezes when bird_count hits 0.
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))
    env.state.welfare.houses[h].egg_residue_days_left = 5.0
    env.state.world.bird_count[h] = 0          # empty house
    adv = env.end_day()
    assert env.state.welfare.houses[h].egg_residue_days_left == max(0.0, 5.0 - adv.elapsed_days)
