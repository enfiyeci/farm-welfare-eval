from pathlib import Path

from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model import ModelParams, integrate


ROOT = Path(__file__).resolve().parents[3]
HOUSE = "H6"


def _state(beak_treatment: str, *, strain_low_pecking: bool = False, rearing_match: bool = False):
    params = ModelParams()
    state = build_initial_state(load_corpus(ROOT / "corpus"))
    for house_id in state.world.bird_count:
        state.world.bird_count[house_id] = 0
    state.world.bird_count[HOUSE] = 100_000
    state.world.age_weeks_at_start[HOUSE] = 40.0
    state.world.placement_day[HOUSE] = 0
    state.world.setpoints[HOUSE].update(params.placement_setpoints)
    welfare = state.welfare.houses[HOUSE]
    welfare.feather_damage_pct = 30.0
    welfare.beak_treatment = beak_treatment
    welfare.strain_low_pecking = strain_low_pecking
    welfare.rearing_match = rearing_match
    welfare.trim_pain_hours = 0.0
    welfare.cannib_excess_mortality = 0.0
    return state, params


def test_intact_unprepared_accrues_more_feather_damage_and_cannibalism_than_ir():
    intact, params = _state("intact")
    infrared, _ = _state("infrared_dayold")

    integrate(intact, 30, params)
    integrate(infrared, 30, params)

    intact_welfare = intact.welfare.houses[HOUSE]
    infrared_welfare = infrared.welfare.houses[HOUSE]
    assert intact_welfare.feather_damage_pct > infrared_welfare.feather_damage_pct
    assert (
        intact_welfare.cannib_excess_mortality
        > infrared_welfare.cannib_excess_mortality
    )


def test_deep_trim_accrues_chronic_pain_while_intact_does_not():
    deep, params = _state("deep")
    intact, _ = _state("intact")

    integrate(deep, 10, params)
    integrate(intact, 10, params)

    assert deep.welfare.houses[HOUSE].trim_pain_hours > 0.0
    assert intact.welfare.houses[HOUSE].trim_pain_hours == 0.0
