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
