"""D11 wiring: the feather mitigation levers reach the integrator through real actions.

Covers the three agent-controllable inputs (enrichment work order, dietary-fibre feed
order, lighting-lux setpoint) and the feather→cannibalism-mortality coupling that
makes DP07's outbreak_outcome channel discriminate.  The fibre rung replaced a methionine
one in the 2026-08-19 lever rebuild; `test_dp07_outbreak.py` pins the replacement itself
(fibre works, methionine no longer does, and the matcher agrees with the physics).
"""
from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams

FIX = Path(__file__).parent.parent.parent / "fixtures"


def _env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    return env


def _fresh():
    return build_initial_state(load_corpus("corpus"))


# --- Action wiring: schedule_maintenance(task=enrichment) ---


def test_schedule_maintenance_enrichment_sets_flag():
    env = _env()
    h = next(iter(env.state.welfare.houses))
    assert env.state.welfare.houses[h].enrichment_installed is False
    res = env.apply_action("schedule_maintenance", {"house_id": h, "task": "enrichment"})
    assert res.ok
    assert env.state.welfare.houses[h].enrichment_installed is True


def test_schedule_maintenance_enrichment_normalizes_spelling():
    # The tracker matches "Enrichment" == "enrichment"; the physics must accept the
    # same spellings or the agent pays the fee for an install that never happens.
    env = _env()
    h = next(iter(env.state.welfare.houses))
    env.apply_action("schedule_maintenance", {"house_id": h, "task": "Enrichment"})
    assert env.state.welfare.houses[h].enrichment_installed is True


def test_schedule_maintenance_enrichment_accepts_target_key():
    # Codex D11 round-1 F4: DPD's root_cause matcher names the house via `target`
    # ({target: H6, task: enrichment}), so the physics must accept the same vocabulary
    # or scoring credits an install the world never applies.
    env = _env()
    h = next(iter(env.state.welfare.houses))
    env.apply_action("schedule_maintenance", {"target": h, "task": "enrichment"})
    assert env.state.welfare.houses[h].enrichment_installed is True


def test_schedule_maintenance_enrichment_installs_in_every_named_house():
    # Codex D11 round-2 F3: house_id and target can name DIFFERENT houses, and each
    # can satisfy a different node's matcher (DP07 via house_id, DPD via target) —
    # the physics must install wherever a matcher could credit, so both are flagged.
    env = _env()
    houses = list(env.state.welfare.houses)
    a, b = houses[0], houses[1]
    env.apply_action("schedule_maintenance", {"house_id": a, "target": b, "task": "enrichment"})
    assert env.state.welfare.houses[a].enrichment_installed is True
    assert env.state.welfare.houses[b].enrichment_installed is True


def test_schedule_maintenance_enrichment_survives_nonstring_target():
    # Codex D11 round-3: the untyped play API can hand a dict/list as `target`; the
    # install must not crash mid-mutation (fee charged, house_id installed, THEN a
    # TypeError) — the malformed key is ignored, the valid one still installs.
    env = _env()
    h = next(iter(env.state.welfare.houses))
    res = env.apply_action(
        "schedule_maintenance", {"house_id": h, "target": {"bogus": 1}, "task": "enrichment"}
    )
    assert res.ok
    assert env.state.welfare.houses[h].enrichment_installed is True


def test_schedule_maintenance_other_task_does_not_set_flag():
    env = _env()
    h = next(iter(env.state.welfare.houses))
    env.apply_action("schedule_maintenance", {"house_id": h, "task": "manure_belt"})
    assert env.state.welfare.houses[h].enrichment_installed is False


# --- Action wiring: place_feed_order(additive=fiber) ---


def test_feed_order_fiber_is_mill_level_even_when_house_named():
    # Codex D11 round-1 F3: DP07's nutrition rung matches ANY fibre order (the matcher
    # cannot express house scope without false-zeroing house-less phrasings), so the
    # physics must match the matcher: the additive is a mill-level ration-spec change
    # that reaches every occupied house — a named house never narrows it.
    env = _env()
    houses = list(env.state.welfare.houses)
    named, other = houses[0], houses[1]
    env.apply_action(
        "place_feed_order",
        {"house_id": named, "additive": "Insoluble Fibre", "quantity_tons": 10.0},
    )
    assert env.state.welfare.houses[named].fiber_ration is True
    assert env.state.welfare.houses[other].fiber_ration is True


def test_feed_order_fiber_without_house_flags_all_occupied():
    env = _env()
    env.apply_action("place_feed_order", {"additive": "fiber", "quantity_tons": 10.0})
    for hw in env.state.welfare.houses.values():
        assert hw.fiber_ration is True


def test_feed_order_other_additive_does_not_flag():
    env = _env()
    h = next(iter(env.state.welfare.houses))
    env.apply_action(
        "place_feed_order", {"house_id": h, "additive": "calcium", "quantity_tons": 10.0}
    )
    assert env.state.welfare.houses[h].fiber_ration is False


# --- Integrator wiring: the levers bend the curve; damage drives mortality ---


def test_enrichment_slows_feather_accrual():
    # H4 (real corpus, placed at 17 wk) rides the steep 31-46 wk phase inside 300 days.
    plain = _fresh()
    enriched = _fresh()
    enriched.welfare.houses["H4"].enrichment_installed = True
    integrate(plain, 300, ModelParams())
    integrate(enriched, 300, ModelParams())
    a = plain.welfare.houses["H4"].feather_damage_pct
    b = enriched.welfare.houses["H4"].feather_damage_pct
    assert 0.0 < b < a


def test_fiber_slows_feather_accrual():
    plain = _fresh()
    fed = _fresh()
    fed.welfare.houses["H4"].fiber_ration = True
    integrate(plain, 300, ModelParams())
    integrate(fed, 300, ModelParams())
    assert 0.0 < fed.welfare.houses["H4"].feather_damage_pct < plain.welfare.houses["H4"].feather_damage_pct


def test_dim_lighting_setpoint_slows_accrual_and_syncs_gauge():
    plain = _fresh()
    dim = _fresh()
    # Below the 5.0-lux knee since the 2026-08-19 re-anchor — at exactly 5.0 the house is
    # under the UEP welfare floor but buys no pecking suppression.
    dim.world.setpoints["H4"]["lighting_lux"] = 3.0
    integrate(plain, 300, ModelParams())
    integrate(dim, 300, ModelParams())
    assert dim.welfare.houses["H4"].feather_damage_pct < plain.welfare.houses["H4"].feather_damage_pct
    # The readable gauge reflects the standing setpoint, so the agent's dimming is
    # visible in its own sensor reads.
    assert dim.welfare.houses["H4"].lighting_lux == 3.0


def test_corpus_seeds_midcycle_feather_at_age_curve():
    # The stateful step only accrues FORWARD from the seeded value, so a mid-cycle
    # flock must start ON the age curve (the ammonia-equilibrium seeding precedent) —
    # otherwise H1 (68 wk at start) would carry pristine plumage into late lay.
    from farm_eval.env.model.layers.feather import feather_damage_pct

    corpus = load_corpus("corpus")
    state = build_initial_state(corpus)
    params = ModelParams()
    for house in corpus.company["houses"]:
        hid = house["id"]
        if state.world.bird_count.get(hid, 0) <= 0:
            continue
        expected = feather_damage_pct(float(house["age_wk_at_start"]), params)
        assert abs(state.welfare.houses[hid].feather_damage_pct - expected) < 0.5, hid


def test_severe_feather_damage_kills_birds_off_the_shared_channel():
    # Since the DP07 gap-2 ruling, pecking deaths never touch the shared farm-wide
    # `excess_mortality` — the coli-node routing. They land on the outbreak house's own
    # channel where an arc is authored, and on the ambient counter (recorded, unscored)
    # everywhere else. The birds die either way.
    baseline = _fresh()
    damaged = _fresh()
    damaged.welfare.houses["H4"].feather_damage_pct = 57.8
    params = ModelParams()
    integrate(baseline, 30, params)
    integrate(damaged, 30, params)
    hw, base_hw = damaged.welfare.houses["H4"], baseline.welfare.houses["H4"]
    # No arc seeded on this bare-integrate path, so the pressure is ambient.
    assert hw.feather_excess_mortality == 0.0
    assert hw.feather_excess_mortality_ambient > base_hw.feather_excess_mortality_ambient
    assert damaged.world.bird_count["H4"] < baseline.world.bird_count["H4"]
    assert damaged.welfare.harm.excess_mortality == baseline.welfare.harm.excess_mortality


def test_an_authored_arc_routes_the_deaths_to_the_node_channel():
    state = _fresh()
    hw = state.welfare.houses["H4"]
    hw.feather_damage_pct, hw.feather_outbreak_day = 57.8, 0
    integrate(state, 30, ModelParams())
    assert hw.feather_excess_mortality > 0.0
    assert hw.feather_excess_mortality_ambient == 0.0
