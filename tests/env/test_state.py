from farm_eval.env.state import EnvState, Email, FinancialState, HouseWelfare, WelfareState, WorldState


def test_email_from_alias():
    email = Email.model_validate(
        {"id": "m1", "day": 0, "date": "2025-06-09", "from": "a@x.com", "to": "b@x.com", "subject": "hi", "body": "."}
    )
    assert email.from_ == "a@x.com"
    assert email.unread is True


def test_env_state_minimal_construction():
    state = EnvState(
        start_date="2025-06-09",
        welfare=WelfareState(houses={"H_X": HouseWelfare(
            ammonia_ppm=8.0, co2_ppm=2200.0, litter_moisture=25.0,
            lighting_lux=10.0, lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
        )}),
        financial=FinancialState(),
        world=WorldState(setpoints={"H_X": {"ventilation": 1.0}}, litter_age_days={"H_X": 0.0}, bird_count={"H_X": 1000}),
    )
    assert state.day_index == 0
    assert state.welfare.houses["H_X"].ammonia_ppm == 8.0
    assert state.financial.feed_inventory_tons == 0.0
    assert state.mailbox == []
