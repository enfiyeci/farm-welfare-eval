# tests/env/model/test_layer_litter.py
"""Litter-moisture layer: moisture relaxes toward a belt-frequency-driven equilibrium.

This is the agent-reachable lever for footpad dermatitis: more-frequent manure-belt
removal (lower belt_interval_days) dries the litter; infrequent removal lets it wet up.
See docs/model-params.md §FPD and docs/eval-design-notes.md.
"""
from farm_eval.env.model.layers import litter
from farm_eval.env.model import ModelParams

P = ModelParams()


def test_frequent_belts_have_drier_equilibrium_than_infrequent():
    """Belt interval is a real, monotone moisture lever — a WEAK one, by measurement.

    The two assertions against `fpd_moisture_ref` are gone. They claimed daily belts sit BELOW
    the footpad onset threshold and weekly belts ABOVE it, which was true only while the belt
    curve spanned 15→45 % and the threshold sat at 30 % — and those two numbers were calibrated
    from each other, not from a measurement (see the fpd_moisture_ref comment in params.py).
    Groot Koerkamp Ch. 7 Table 4 measures an aviary's litter at 14.4–20.1 % across all five belt
    regimes, entirely below 30 %, and Wang et al. 1998 measures 13–17 % footpad prevalence on dry
    litter. So the footpad threshold is no longer a boundary that belt interval straddles: footpad
    responds across the whole operating band, and belt interval moves it by degree, not on/off.
    The claim worth keeping — and the one this layer is actually responsible for — is the ordering.
    """
    # Equilibrium is the fixed point of repeated stepping at a fixed belt interval.
    def equilibrium(belt_days):
        m = 25.0
        for _ in range(500):
            m = litter.litter_moisture_step(m, belt_days, P)
        return m

    daily = equilibrium(1)     # belt every day — driest
    weekly = equilibrium(7)    # belt weekly — wettest
    assert daily < weekly
    # Monotone across every interval in between, not just at the endpoints.
    curve = [equilibrium(d) for d in (1, 2, 3, 4, 5, 6, 7)]
    assert curve == sorted(curve), f"belt→moisture equilibrium is not monotone: {curve}"
    assert curve[0] < curve[-1]


def test_step_moves_toward_equilibrium_from_both_sides():
    # belt_days=7 has a high (wet) equilibrium: a dry start must rise toward it.
    up = litter.litter_moisture_step(20.0, 7, P)
    assert up > 20.0
    # belt_days=1 has a low (dry) equilibrium: a wet start must fall toward it.
    down = litter.litter_moisture_step(40.0, 1, P)
    assert down < 40.0


def test_step_does_not_overshoot_or_leave_bounds():
    # A single relaxation step never crosses the equilibrium or leaves [0, 100].
    for belt_days in (1, 2, 4, 7):
        m = litter.litter_moisture_step(0.0, belt_days, P)
        assert 0.0 <= m <= 100.0
        m = litter.litter_moisture_step(100.0, belt_days, P)
        assert 0.0 <= m <= 100.0
