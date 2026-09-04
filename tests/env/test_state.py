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
    # Tracked tool-call history (used by classified all_of / ladder / transient_before).
    assert state.actions == []


def test_env_state_actions_records_history():
    from farm_eval.env.ledger import ActionRecord

    state = EnvState(start_date="2025-06-09")
    state.actions.append(ActionRecord(tool="adjust_setpoint", params={"system": "ventilation"}, day=3))
    assert state.actions[0].tool == "adjust_setpoint"
    assert state.actions[0].day == 3


def test_house_welfare_beak_decision_defaults():
    welfare = HouseWelfare(
        ammonia_ppm=8.0,
        co2_ppm=2200.0,
        litter_moisture=25.0,
        lighting_lux=10.0,
        lighting_hours=16.0,
        heat_stress_index=0.0,
        stocking_density=1.0,
    )

    assert welfare.beak_treatment == "infrared_dayold"
    assert welfare.strain_low_pecking is False
    assert welfare.rearing_match is False
    assert welfare.trim_pain_hours == 0.0
    assert welfare.cannib_excess_mortality == 0.0
