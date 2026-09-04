"""Property / fuzz tests for the reactive substrate.

The whole eval rests on the bet that the env-core is a *deterministic reactive substrate*:
the world responds to the agent's actions the same way every run, and stays physically
coherent no matter what sequence of actions it sees. Hand-picked tests verify specific
points; these fuzz tests assert the load-bearing invariants hold across many randomly
generated action sequences (the class of bug that only shows up when channels interact —
e.g. combined heat+HPAI mortality exceeding the flock, or a treatment corrupting state).

Randomness lives ONLY in the test (a seeded `random.Random`), never in the logic under
test. Each seed is fully reproducible; a failure prints the seed + day so it can be replayed.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams

ROOT = Path(__file__).resolve().parents[3]
CORPUS = ROOT / "corpus"
SCHEDULE = ROOT / "schedule"
P = ModelParams()


# --------------------------------------------------------------------------- helpers


def _iter_floats(obj):
    """Yield every float anywhere in a model_dump structure (dicts/lists/scalars)."""
    if isinstance(obj, bool):
        return
    if isinstance(obj, float):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_floats(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _iter_floats(v)


def _random_action(env: FarmEnv, rng: random.Random, houses: list[str]) -> None:
    """Apply one random agent action through the real apply_action lever semantics."""
    h = rng.choice(houses)
    kind = rng.choice(["vent", "temp", "belt", "treat_mite", "treat_drug", "feed", "ipm"])
    if kind == "vent":
        env.apply_action("adjust_setpoint", {"house_id": h, "system": "ventilation", "value": round(rng.uniform(0.0, 4.0), 2)})
    elif kind == "temp":
        env.apply_action("adjust_setpoint", {"house_id": h, "system": "temperature", "value": round(rng.uniform(12.0, 32.0), 1)})
    elif kind == "belt":
        env.apply_action("adjust_setpoint", {"house_id": h, "system": "belt_interval_days", "value": rng.randint(1, 7)})
    elif kind == "treat_mite":
        # Rejected since the DP05 target rebuild (2026-08-26) — kept in the fuzz precisely
        # because a rejected action must leave the substrate coherent.
        env.apply_action("log_treatment", {"house_id": h, "issue": "red_mite"})
    elif kind == "ipm":
        env.apply_action("book_ipm_service", {"house_id": h})
    elif kind == "treat_drug":
        env.apply_action("log_treatment", {"house_id": h, "drug": rng.choice(["erythromycin", "amoxicillin", "tiamulin", "not_a_drug"])})
    elif kind == "feed":
        # Include negative/zero quantities to fuzz the place_feed_order guard.
        env.apply_action("place_feed_order", {"quantity_tons": round(rng.uniform(-5.0, 50.0), 1)})


def _assert_invariants(state, initial_birds: dict, prev_harm: dict, ctx: str) -> dict:
    """Assert the substrate is physically coherent. Returns the current harm snapshot."""
    # No NaN / inf anywhere in the state.
    for v in _iter_floats(state.model_dump()):
        assert math.isfinite(v), f"non-finite float {v!r} ({ctx})"

    # Bird counts non-negative; deaths conserve birds (no phantom mortality).
    for hid, n in state.world.bird_count.items():
        assert n >= 0, f"negative bird_count {hid}={n} ({ctx})"
    removed = sum(initial_birds[h] - state.world.bird_count[h] for h in initial_birds)
    assert state.welfare.mortality_cumulative == removed, (
        f"mortality_cumulative {state.welfare.mortality_cumulative} != birds removed {removed} ({ctx})"
    )

    # Harm accumulators: non-negative AND monotone non-decreasing.
    harm = state.welfare.harm.model_dump()
    for k, v in harm.items():
        assert v >= 0.0, f"negative harm {k}={v} ({ctx})"
        assert v >= prev_harm[k] - 1e-6, f"harm {k} decreased {prev_harm[k]}->{v} ({ctx})"

    # Financial: non-negative cumulatives + the Tier-0 margin identity.
    f = state.financial
    assert f.feed_inventory_tons >= -1e-9, f"negative feed inventory ({ctx})"
    assert f.feed_book_value_usd >= -1e-9, f"negative feed book value ({ctx})"
    assert f.revenue_cum >= 0.0 and f.feed_cost_cum >= 0.0 and f.other_cost_cum >= 0.0, f"negative P&L cumulative ({ctx})"
    assert abs(f.margin - (f.revenue_cum - f.feed_cost_cum - f.other_cost_cum)) < 1e-3, f"margin identity broken ({ctx})"

    # Per-house biological bounds.
    for hid, hw in state.welfare.houses.items():
        assert 0.0 <= hw.hen_day_pct <= 100.0, f"hen_day_pct out of range {hid} ({ctx})"
        assert hw.footpad_mild_pct >= 0.0 and hw.footpad_severe_pct >= 0.0, f"negative footpad {hid} ({ctx})"
        assert hw.footpad_mild_pct + hw.footpad_severe_pct <= 100.0 + 1e-6, f"footpad sum >100% {hid} ({ctx})"
        assert 0.0 <= hw.feather_damage_pct <= 100.0, f"feather out of range {hid} ({ctx})"
        assert 0.0 <= hw.keel_fracture_pct <= 100.0, f"keel out of range {hid} ({ctx})"
        assert 0.0 <= hw.red_mite_index <= P.red_mite_carrying + 1e-6, f"red_mite out of range {hid} ({ctx})"
        assert hw.ammonia_ppm >= 0.0, f"negative ammonia {hid} ({ctx})"
        assert hw.egg_residue_days_left >= 0.0, f"negative residue {hid} ({ctx})"
        assert 0.0 <= hw.hpai_daily_mort_frac <= P.hpai_mort_cap + 1e-9, f"hpai frac out of range {hid} ({ctx})"
        assert 0.0 <= hw.panting_fraction <= 1.0, f"panting out of range {hid} ({ctx})"

    return harm


# --------------------------------------------------------------------------- tests


def test_fuzz_substrate_invariants_over_random_action_sequences():
    """Random agent actions + occasional disease seeding over a long horizon must keep the
    substrate physically coherent (no NaN, no negative/over-100% values, conserved mortality,
    monotone harm, margin identity).

    The `coverage` guard makes this test self-auditing: if a lever silently stops working
    (so the fuzz never reaches the interesting states), the run fails rather than passing
    vacuously."""
    coverage = {"hpai_mortality": False, "mite_over_threshold": False,
                "residue_set": False, "mass_deaths": False}
    for seed in range(25):
        env = FarmEnv.from_paths(str(CORPUS), str(SCHEDULE), seed=1, episode_end_day=10_000)
        state = env.state
        initial_birds = dict(state.world.bird_count)
        prev_harm = {k: 0.0 for k in state.welfare.harm.model_dump()}
        rng = random.Random(seed)
        houses = list(state.welfare.houses)
        total = 0
        while total < 200:
            for _ in range(rng.randint(0, 3)):
                _random_action(env, rng, houses)
            # Observe residue right after actions (it decrements toward 0 during integrate).
            if any(hw.egg_residue_days_left > 0 for hw in state.welfare.houses.values()):
                coverage["residue_set"] = True
            # Simulate the C3 disease-introduction events C2 leaves to the schedule.
            h = rng.choice(houses)
            if rng.random() < 0.04:
                state.welfare.houses[h].hpai_onset_day = state.day_index + rng.randint(1, 6)
            if rng.random() < 0.04:
                state.welfare.houses[h].se_status = True
            # A mite arc is schedule content, so the fuzz seeds it the way a state_seed does;
            # without one no house grows a population and the coverage guard below would be
            # unreachable.
            if rng.random() < 0.04:
                hw_arc = state.welfare.houses[h]
                hw_arc.red_mite_index = max(hw_arc.red_mite_index, 0.30)
                hw_arc.red_mite_arc_day = state.day_index
                hw_arc.red_mite_accrual_end_day = state.day_index + 98
            n = rng.randint(1, 25)
            integrate(state, n, P)
            state.day_index += n
            total += n
            prev_harm = _assert_invariants(state, initial_birds, prev_harm, f"seed={seed} day={state.day_index}")
            for hw in state.welfare.houses.values():
                if hw.hpai_daily_mort_frac > 0.0:
                    coverage["hpai_mortality"] = True
                if hw.red_mite_index > P.red_mite_action_threshold:
                    coverage["mite_over_threshold"] = True
        if any(initial_birds[h] - state.world.bird_count[h] > 0.5 * initial_birds[h] for h in initial_birds):
            coverage["mass_deaths"] = True

    missing = [k for k, v in coverage.items() if not v]
    assert not missing, f"fuzz never exercised: {missing} — the test passed vacuously"


def test_path_independence_under_random_chunk_splits():
    """Integrating N days at once must equal integrating the same N days in ANY random split,
    with the disease channels active (HPAI onset + SE set at fixed absolute days so both runs
    see identical inputs). Generalizes the fixed-split path-independence test."""

    def _make():
        s = build_initial_state(load_corpus(str(CORPUS)), seed=1)
        for h in list(s.welfare.houses)[:2]:
            s.welfare.houses[h].hpai_onset_day = 5   # active mid-run mortality course
            s.welfare.houses[h].se_status = True
        return s

    for seed in range(20):
        rng = random.Random(1000 + seed)
        n_total = rng.randint(60, 220)
        chunks, rem = [], n_total
        while rem > 0:
            c = rng.randint(1, min(40, rem))
            chunks.append(c)
            rem -= c

        one = _make()
        integrate(one, n_total, P)
        many = _make()
        for c in chunks:
            integrate(many, c, P)
            many.day_index += c

        assert one.model_dump() == {**many.model_dump(), "day_index": one.day_index}, (
            f"path-dependence at seed={seed}, N={n_total}, chunks={chunks}"
        )
