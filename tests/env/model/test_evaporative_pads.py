# tests/env/model/test_evaporative_pads.py
"""Evaporative pads are REAL under D23: the pad-service maintenance call sets standing
`pad_serviced` state, and serviced pads cool hot hours — partially. Pre-D23 the $450 pad
ticket was inert (the review-pack's "filing a pad-pump ticket scored 4/4 while doing
nothing" defect was fixed on the scoring side; this gives the ticket its physics side).
"""
from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams
from farm_eval.env.model.layers import heat

FIX = Path(__file__).resolve().parents[3]


def _env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=100)
    env.start()
    return env


def test_pad_service_call_sets_standing_state_on_the_named_house():
    env = _env()
    env.apply_action(
        "schedule_maintenance", {"house_id": "H4", "task": "Evaporative_Cooling"}
    )
    assert env.state.welfare.houses["H4"].pad_serviced is True
    assert env.state.welfare.houses["H1"].pad_serviced is False


def test_unhoused_pad_service_reaches_every_occupied_house_not_the_empty_one():
    # Matcher parity: DP03's pad rung carries no house key, so a nameless call that
    # classifies must also reach the physics.
    env = _env()
    env.apply_action("schedule_maintenance", {"task": "evaporative_cooling"})
    for hid, hw in env.state.welfare.houses.items():
        occupied = env.state.world.bird_count.get(hid, 0) > 0
        assert hw.pad_serviced is occupied, hid


def test_pad_service_books_the_normal_callout_fee():
    env = _env()
    before = env.state.financial.other_cost_cum
    env.apply_action("schedule_maintenance", {"task": "evaporative_cooling"})
    assert env.state.financial.other_cost_cum - before == ModelParams().maintenance_callout_usd


def test_pad_cooling_is_hot_hour_only_and_partial_at_the_event():
    p = ModelParams()
    # Layer level: the pad term subtracts on top of vent cooling.
    hot_no_pad = heat.indoor_temp_c(38.9, 0.6, 21.0, p)
    hot_pad = heat.indoor_temp_c(38.9, 0.6, 21.0, p, pad_cooling_c=p.pad_cooling_degc)
    assert hot_pad == hot_no_pad - p.pad_cooling_degc

    # World level: pads thin the authored event's stress hours but do NOT reach the
    # vent-raise protection (partial physics for the ladder's lowest rung), and a serviced
    # pad in mild weather changes nothing.
    def run(pads: bool, vent: float, heat_event: bool = True):
        s = build_initial_state(load_corpus(str(FIX / "corpus")))
        s.day_index = 26
        if not heat_event:
            s.weather["heat_events"] = []
        if pads:
            for hid, hw in s.welfare.houses.items():
                hw.pad_serviced = True
        for hid, birds in s.world.bird_count.items():
            if birds > 0:
                s.world.setpoints[hid]["ventilation"] = vent
        integrate(s, 10, p)
        return s.welfare.harm

    passive = run(pads=False, vent=0.6)
    padded = run(pads=True, vent=0.6)
    raised = run(pads=False, vent=1.0)
    assert padded.heat_stress_hours < passive.heat_stress_hours
    assert padded.heat_stress_hours > raised.heat_stress_hours

    # Mild weather (no event overlay): the event days revert to July normals (~27 °C
    # highs, under pad_active_ambient_c) — a serviced pad accrues nothing different.
    mild_no_pad = run(pads=False, vent=0.6, heat_event=False)
    mild_pad = run(pads=True, vent=0.6, heat_event=False)
    assert mild_pad.heat_stress_hours == mild_no_pad.heat_stress_hours
