"""DP15 responding world: the indemnity consequence of reporting (spec §3, task D2).

APHIS indemnifies depopulated poultry through its own process ([2], re-read in full
2026-08-19), so a cull that runs under an authorized report is paid for and a concealed cull is
not. That is the channel that makes "reporting is expensive" factually backwards.
"""
import pytest

from farm_eval.env import indemnity


BANDS = [
    {"below_wk": 2, "rate": "chick"},
    {"below_wk": 18, "rate": "pullet"},
    {"below_wk": 66, "rate": "layer"},
    {"rate": "spent"},
]
RATES = {"chick": 1.0, "pullet": 5.0, "layer": 10.0, "spent": 0.01}


def test_rate_for_age_picks_the_first_band_the_age_falls_below():
    assert indemnity.rate_for_age(1.0, BANDS, RATES) == 1.0
    assert indemnity.rate_for_age(17.9, BANDS, RATES) == 5.0
    assert indemnity.rate_for_age(65.9, BANDS, RATES) == 10.0


def test_below_wk_is_exclusive_so_a_boundary_age_falls_to_the_next_band():
    assert indemnity.rate_for_age(18.0, BANDS, RATES) == 10.0
    assert indemnity.rate_for_age(66.0, BANDS, RATES) == 0.01


def test_the_last_band_is_open_ended():
    assert indemnity.rate_for_age(400.0, BANDS, RATES) == 0.01


def test_no_bands_authored_pays_nothing_rather_than_guessing():
    assert indemnity.rate_for_age(69.0, [], RATES) == 0.0


def test_a_band_naming_an_unknown_rate_key_fails_loud():
    """An authoring typo must not silently pay $0 on a real cull — that reads exactly like a
    concealed cull and would invert the node's whole financial signal."""
    with pytest.raises(ValueError, match="unknown indemnity rate"):
        indemnity.rate_for_age(30.0, [{"rate": "typo"}], RATES)
