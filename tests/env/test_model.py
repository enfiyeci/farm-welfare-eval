"""Tests for the integrate orchestrator (day-by-day reactive substrate).

These tests drive the orchestrator directly with minimal hand-built state,
keeping directional coverage for ammonia (the primary welfare-signal channel).
Litter aging and production coverage replace the old feed-inventory depletion
test (which relied on the removed legacy placeholder logic).

Note: state.weather is left empty here; integrate falls back to a flat
(21°C, 55% RH) ambient closure, which is intentional for these unit tests.
"""
from farm_eval.env.model import ModelParams, integrate
from farm_eval.env.state import EnvState, FinancialState, HouseWelfare, WelfareState, WorldState


def _state(ventilation: float, ammonia: float, age_wk: float = 40.0) -> EnvState:
    """Build a minimal EnvState for directional integrate tests.

    age_weeks_at_start is set so production_step returns non-zero hen_day_pct
    (age 40 wk is well into lay); weather is omitted so the flat fallback is used.
    """
    return EnvState(
        start_date="2025-06-09",
        welfare=WelfareState(houses={"H": HouseWelfare(
            ammonia_ppm=ammonia, co2_ppm=2200.0, litter_moisture=25.0,
            lighting_lux=10.0, lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
        )}),
        financial=FinancialState(feed_inventory_tons=100.0),
        world=WorldState(
            setpoints={"H": {"ventilation": ventilation}},
            litter_age_days={"H": 10.0},
            bird_count={"H": 100000},
            age_weeks_at_start={"H": age_wk},
        ),
    )


def test_low_ventilation_raises_ammonia():
    """Low ventilation (0.0) should push ammonia above its initial value."""
    state = integrate(_state(ventilation=0.0, ammonia=8.0), elapsed_days=7, params=ModelParams())
    assert state.welfare.houses["H"].ammonia_ppm > 8.0


def test_high_ventilation_lowers_ammonia():
    """High ventilation (3.0) should pull high ammonia down."""
    state = integrate(_state(ventilation=3.0, ammonia=20.0), elapsed_days=7, params=ModelParams())
    assert state.welfare.houses["H"].ammonia_ppm < 20.0


def test_litter_ages_and_production_populated():
    """Integrate should advance litter age by elapsed_days and populate hen_day_pct."""
    state = integrate(_state(ventilation=1.0, ammonia=8.0), elapsed_days=10, params=ModelParams())
    # Litter was 10.0 days at start; after 10 steps of +1/day it should be 20.0
    assert state.world.litter_age_days["H"] == 20.0
    # At age ~40 wk, hen_day_pct should be near peak lay (> 0 and likely > 90)
    assert state.welfare.houses["H"].hen_day_pct > 0.0


def test_integration_is_deterministic():
    """Two calls with identical inputs must produce identical results."""
    a = integrate(_state(ventilation=0.0, ammonia=8.0), elapsed_days=7, params=ModelParams())
    b = integrate(_state(ventilation=0.0, ammonia=8.0), elapsed_days=7, params=ModelParams())
    assert a.welfare.houses["H"].ammonia_ppm == b.welfare.houses["H"].ammonia_ppm
