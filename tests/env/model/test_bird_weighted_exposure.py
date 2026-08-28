# tests/env/model/test_bird_weighted_exposure.py
"""DP01's exposure channel is BIRD-weighted (Codex round-1 F4, 2026-08-27).

The gap-2 ruling words the channel as "bird-hours over the 15 ppm precautionary line", but
the accumulator took no bird count — a nearly empty house at 30 ppm charged exactly as much
as a 125,000-bird house at 30 ppm. `accrue_ammonia` now multiplies by live birds.

The worker channel (DPW) deliberately stays per-occupied-house: it prices CREW-hours over
the NIOSH REL, and the crew walks each occupied house whatever its headcount — worker
exposure does not scale with birds (see accrue_worker_nh3's docstring).
"""
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model.accumulators import accrue_ammonia
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import HarmAccumulators


def test_accrue_ammonia_multiplies_by_live_birds():
    h = HarmAccumulators()
    accrue_ammonia(h, 25.0, 24.0, 15.0, 100)
    assert abs(h.nh3_ppm_hours_over - 10.0 * 24.0 * 100) < 1e-9
    # Proportionality: double the birds, double the accrued exposure.
    h2 = HarmAccumulators()
    accrue_ammonia(h2, 25.0, 24.0, 15.0, 200)
    assert abs(h2.nh3_ppm_hours_over - 2 * h.nh3_ppm_hours_over) < 1e-9
    # Below threshold accrues nothing at any headcount.
    h3 = HarmAccumulators()
    accrue_ammonia(h3, 10.0, 24.0, 15.0, 100_000)
    assert h3.nh3_ppm_hours_over == 0.0


def test_integrated_nh3_channel_is_bird_scaled_and_worker_channel_is_not():
    # Winter passive run (the DP01 window): both channels accrue. The bird channel must sit
    # orders of magnitude above the crew channel — 1e5-bird flocks weight every exposed
    # hour — while the crew channel stays at house-hours scale. Before the fix both were
    # house-hours scale and their ratio was single-digit (excess-over-15 vs excess-over-25).
    s = build_initial_state(load_corpus("corpus"))
    s.day_index = 182
    # A bare integrate() fires no schedule events, so the authored day-147 belt drift never
    # lands here; lag every occupied house's belt so the passive run clears the 25 ppm REL
    # and the crew channel actually accrues.
    for hid, birds in s.world.bird_count.items():
        if birds > 0:
            s.world.setpoints.setdefault(hid, {})["belt_interval_days"] = 6
    integrate(s, 42, ModelParams())
    harm = s.welfare.harm
    assert harm.worker_nh3_ppm_hours_over > 0.0
    assert harm.nh3_ppm_hours_over > 1000 * harm.worker_nh3_ppm_hours_over
