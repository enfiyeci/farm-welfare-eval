"""Salmonella Enteritidis: hidden flock status + a deterministic, sensitivity-limited
environmental test. Detection is a pure hash of (seed, house, day) — never random — so a
negative environmental test does not fully clear an SE-positive house (the epistemic texture).
The agent-facing test action and the divert-vs-sell decision are wired in C3/C4."""

import hashlib

from farm_eval.env.model.params import ModelParams


def _unit_hash(seed: int, house_id: str, day: int) -> float:
    """Deterministic pseudo-uniform in [0,1) from the seed + house + day.

    Divides the 32-bit hash prefix by 2**32 (0x100000000), not 2**32-1, so the range is the
    half-open [0,1) the contract promises — dividing by 0xFFFFFFFF yields 1.0 for the maximum
    prefix and would cause a false negative at sensitivity == 1.0.
    """
    raw = hashlib.sha256(f"se:{seed}:{house_id}:{day}".encode()).hexdigest()
    return int(raw[:8], 16) / 0x100000000


def environmental_test(se_status: bool, seed: int, house_id: str, day: int,
                       params: ModelParams) -> bool:
    """Environmental swab result: positive only if the flock is truly SE+ AND the
    (deterministic) draw falls under the test sensitivity."""
    if not se_status:
        return False
    return _unit_hash(seed, house_id, day) < params.se_env_test_sensitivity
