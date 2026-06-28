from pathlib import Path
from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent.parent / "fixtures"


def test_log_treatment_knocks_down_red_mite():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))            # any house id
    env.state.welfare.houses[h].red_mite_index = 2.5    # established infestation
    env.apply_action("log_treatment", {"house_id": h, "issue": "red_mite"})
    assert env.state.welfare.houses[h].red_mite_index < 0.2   # knocked down
