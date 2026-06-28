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


def test_log_treatment_never_increases_red_mite():
    # A knockdown must never raise the burden: a house already at/below the floor stays put,
    # not pushed up to the floor. (Guards the min() semantic against future sub-floor seeding.)
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    h = next(iter(env.state.welfare.houses))
    env.state.welfare.houses[h].red_mite_index = 0.0
    env.apply_action("log_treatment", {"house_id": h, "issue": "red_mite"})
    assert env.state.welfare.houses[h].red_mite_index == 0.0   # unchanged, not raised to the floor
