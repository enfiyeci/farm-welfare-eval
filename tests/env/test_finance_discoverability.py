"""Task 8, law 1: every rulebook input is obtainable from inside the world. The DP18 lesson as a
standing test — a mechanism whose inputs cannot be read is a guaranteed false zero."""
from scripts.finance_discoverability_probe import REQUIRED_INPUTS, probe_inputs

from farm_eval.env.episode import FarmEnv


def test_every_rulebook_input_is_actually_readable():
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=518)
    env.start()
    found = probe_inputs(env)
    missing = sorted(key for key in REQUIRED_INPUTS if not found.get(key))
    assert not missing, f"rulebook inputs not obtainable through any read tool: {missing}"
