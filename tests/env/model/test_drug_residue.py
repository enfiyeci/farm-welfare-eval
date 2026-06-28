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
    env.end_day()  # advances several days; residue counts down but stays >= 0
    assert 0.0 <= env.state.welfare.houses[h].egg_residue_days_left < 11
