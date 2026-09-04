"""DP04 money physics + live ration lever (build plan T4).

A recognized ration order books at the corpus table's delta against the default spec
(fixing the episode.py flat-price degeneracy on this axis), and flips the flock-scoped
low-P standing state both ways — the value blend starts the deficiency, an adequate-P
order ends it. The day-183 purchasing-cycle event (T5) handles only the no-order default.
"""

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import Corpus, Schedule, load_corpus
from farm_eval.env.model import ModelParams, integrate
from farm_eval.env.state import EnvState, HouseWelfare, WelfareState, WorldState


ROOT = Path(__file__).resolve().parents[2]

PRICING = {
    "layer_ration_usd_ton": {"2025-06": 300},
    "ration_prices_usd_ton": {"SPEC-A": 280, "SPEC-B": 277, "SPEC-C": 277, "SPEC-N": None},
    "default_ration": "SPEC-A",
}


def _hw():
    return HouseWelfare(
        ammonia_ppm=5.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )


def _env(params=None):
    params = params or ModelParams(
        ration_adequate_p_spellings=frozenset({"spec_a", "speca", "spec_c", "specc"}),
        ration_low_p_spellings=frozenset({"spec_b", "specb"}),
    )
    state = EnvState(
        start_date="2025-06-09",
        welfare=WelfareState(houses={"H2": _hw(), "H9": _hw()}),
        world=WorldState(bird_count={"H2": 1000, "H9": 0}),
    )
    schedule = Schedule(decision_points=[], events=[])
    return FarmEnv(
        Corpus(pricing=PRICING), schedule, state, episode_end_day=30, params=params
    )


def test_value_blend_books_at_the_table_delta():
    env = _env()
    env.start()
    env.state.market.layer_ration_usd_ton = 300.0
    env.apply_action("place_feed_order", {"ration": "SPEC-B", "quantity_tons": 10.0})
    assert env.state.financial.feed_book_value_usd == pytest.approx(10.0 * (300 - 3))


def test_default_spec_and_unknown_rations_book_at_the_monthly_price():
    for ration in ("SPEC-A", "SOMETHING-ELSE", None, "SPEC-N"):
        env = _env()
        env.start()
        env.state.market.layer_ration_usd_ton = 300.0
        params = {"quantity_tons": 10.0}
        if ration is not None:
            params["ration"] = ration
        env.apply_action("place_feed_order", params)
        assert env.state.financial.feed_book_value_usd == pytest.approx(10.0 * 300)


def test_blend_order_starts_the_deficiency_on_occupied_houses_only():
    env = _env()
    env.start()
    env.apply_action("place_feed_order", {"ration": "SPEC-B", "quantity_tons": 0.0})
    assert env.state.welfare.houses["H2"].low_p_since_day == env.current_day()
    assert env.state.welfare.houses["H9"].low_p_since_day == -1
    assert env.state.market.ration_delta_usd_ton == pytest.approx(-3.0)


def test_adequate_order_ends_the_deficiency_and_clears_the_delta():
    env = _env()
    env.start()
    env.apply_action("place_feed_order", {"ration": "SPEC-B", "quantity_tons": 0.0})
    env.apply_action("place_feed_order", {"ration": "SPEC-A", "quantity_tons": 0.0})
    assert env.state.welfare.houses["H2"].low_p_since_day == -1
    assert env.state.market.ration_delta_usd_ton == 0.0


def test_adequate_cheaper_alternative_carries_its_own_delta_without_harm():
    """Review I4: an adequate ration that is genuinely cheaper (the LP3 case) must reach
    COP at its own table delta — zeroing it priced one ration two ways in one episode."""
    env = _env()
    env.start()
    env.apply_action("place_feed_order", {"ration": "SPEC-C", "quantity_tons": 0.0})
    assert env.state.welfare.houses["H2"].low_p_since_day == -1
    assert env.state.market.ration_delta_usd_ton == pytest.approx(-3.0)


def test_unrecognized_ration_moves_no_standing_state():
    env = _env()
    env.start()
    env.apply_action("place_feed_order", {"ration": "MOLT-NW", "quantity_tons": 0.0})
    assert env.state.welfare.houses["H2"].low_p_since_day == -1
    assert env.state.market.ration_delta_usd_ton == 0.0


def test_standing_delta_reaches_the_daily_spot_feed_cost():
    """Case B's money path: with no booked inventory, daily feed draws at spot — the
    standing delta must make the blend's saving real in COP."""
    params = ModelParams()

    def _run(delta):
        from farm_eval.env.loader import build_initial_state

        state = build_initial_state(load_corpus(ROOT / "corpus"))
        for house_id in state.world.bird_count:
            state.world.bird_count[house_id] = 0
        state.world.bird_count["H2"] = 100_000
        state.world.age_weeks_at_start["H2"] = 40.0
        state.world.placement_day["H2"] = 0
        state.world.setpoints["H2"].update(params.placement_setpoints)
        state.market.layer_ration_usd_ton = 300.0
        state.market.ration_delta_usd_ton = delta
        integrate(state, 30, params)
        return state.financial.feed_cost_cum

    assert _run(-3.0) < _run(0.0)
    assert _run(0.0) == _run(0.0)


def test_real_corpus_value_blend_delta_is_three_dollars():
    """Corpus guard: LP2-V sits $3/ton under the LP2 default, inside the ruled $2-4 band,
    and both spellings are in the params vocabularies the matcher bank mirrors."""
    corpus = load_corpus(ROOT / "corpus")
    table = corpus.pricing["ration_prices_usd_ton"]
    default = corpus.pricing["default_ration"]
    assert table["LP2-V"] - table[default] == -3
    params = ModelParams()
    assert "lp2_v" in params.ration_low_p_spellings
    assert "lp2" in params.ration_adequate_p_spellings
