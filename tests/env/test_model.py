from farm_eval.env.model import ModelParams, integrate
from farm_eval.env.state import EnvState, FinancialState, HouseWelfare, WelfareState, WorldState


def _state(ventilation: float, ammonia: float) -> EnvState:
    return EnvState(
        start_date="2025-06-09",
        welfare=WelfareState(houses={"H": HouseWelfare(
            ammonia_ppm=ammonia, co2_ppm=2200.0, litter_moisture=25.0,
            lighting_lux=10.0, lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
        )}),
        financial=FinancialState(feed_inventory_tons=100.0),
        world=WorldState(setpoints={"H": {"ventilation": ventilation}}, litter_age_days={"H": 10.0}, bird_count={"H": 100000}),
    )


def test_low_ventilation_raises_ammonia():
    state = integrate(_state(ventilation=0.0, ammonia=8.0), elapsed_days=7, params=ModelParams())
    assert state.welfare.houses["H"].ammonia_ppm > 8.0


def test_high_ventilation_lowers_ammonia():
    state = integrate(_state(ventilation=3.0, ammonia=20.0), elapsed_days=7, params=ModelParams())
    assert state.welfare.houses["H"].ammonia_ppm < 20.0


def test_feed_inventory_depletes_and_litter_ages():
    state = integrate(_state(ventilation=1.0, ammonia=8.0), elapsed_days=10, params=ModelParams())
    assert state.financial.feed_inventory_tons < 100.0
    assert state.world.litter_age_days["H"] == 20.0


def test_integration_is_deterministic():
    a = integrate(_state(ventilation=0.0, ammonia=8.0), elapsed_days=7, params=ModelParams())
    b = integrate(_state(ventilation=0.0, ammonia=8.0), elapsed_days=7, params=ModelParams())
    assert a.welfare.houses["H"].ammonia_ppm == b.welfare.houses["H"].ammonia_ppm
