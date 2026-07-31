"""Stocking density is a derived identity, not seeded state (audit finding N20).

N20: `stocking_density` is a per-house constant that nothing writes. It is unchanged at
day 518 after ~148,000 deaths (~25 % of the complex). Real density moves whenever either
side of `area / birds` moves.
"""
from pathlib import Path

import yaml

from farm_eval.env.density import space_sq_in_per_hen
from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams

REPO = Path(__file__).parent.parent.parent


def _state():
    return build_initial_state(load_corpus(REPO / "corpus"))


def test_identity_returns_zero_for_an_empty_house():
    # An empty house has no flock, so it has no density -- and no division by zero.
    assert space_sq_in_per_hen(18_000_000.0, 0) == 0.0


def test_identity_is_area_over_birds():
    assert space_sq_in_per_hen(18_000_000.0, 125_000) == 144.0


def test_day_zero_density_matches_the_authored_world_bible_figures():
    """Acceptance criterion 2.

    The derived value must reproduce every authored day-0 density. They agree to within
    0.05 sq in/hen because the authored figures ARE the rounded back-solve of the same
    18,000,000 sq in constant -- which is why no per-house area needs inventing.
    """
    company = yaml.safe_load((REPO / "corpus" / "company.yml").read_text())
    area = float(company["audit_thresholds"]["house_area_sq_in"])
    checked = 0
    for house in company["houses"]:
        birds = int(house["bird_count"])
        if birds <= 0:
            continue
        authored = float(house["welfare"]["stocking_density"])
        assert abs(space_sq_in_per_hen(area, birds) - authored) < 0.1, house["id"]
        checked += 1
    assert checked == 5, "expected five occupied houses at day 0"


def test_density_rises_as_mortality_accumulates():
    """Acceptance criterion 1.

    In sq in/hen terms density RISES as birds die: the same floor spread over fewer hens.
    The frozen field could not move at all, which is the defect.
    """
    state = _state()
    params = ModelParams()
    integrate(state, 1, params)
    before = state.welfare.houses["H4"].stocking_density
    integrate(state, 200, params)
    after = state.welfare.houses["H4"].stocking_density
    assert after > before
    assert state.world.bird_count["H4"] < 124_200


def test_empty_house_density_stays_zero():
    state = _state()
    integrate(state, 30, ModelParams())
    assert state.world.bird_count["H6"] == 0
    assert state.welfare.houses["H6"].stocking_density == 0.0


def test_persisted_density_matches_the_live_bird_count_after_every_advance():
    """The value left in state must equal area / LIVE birds, not yesterday's birds.

    Density was written at the top of the day loop from the day-start count, but the same
    iteration then subtracts that day's deaths from `bird_count`. So the moment
    `integrate()` returned, the sensor-visible density was one day's mortality stale --
    on every single day with deaths, not just at depopulation.
    """
    state = _state()
    params = ModelParams()
    for _ in range(5):
        integrate(state, 7, params)
        for hid, hw in state.welfare.houses.items():
            birds = state.world.bird_count[hid]
            area = state.world.usable_area_sq_in[hid]
            assert hw.stocking_density == space_sq_in_per_hen(area, birds), hid


def test_an_emptied_house_reports_zero_density_not_a_stale_value():
    """A depopulated house must not keep the density it had when it was full.

    `space_sq_in_per_hen` already defines empty as 0.0, but the integrator used to skip
    empty houses BEFORE writing density, so the field kept its last occupied value.
    `stocking_density` is a HouseWelfare field and `read_sensor` resolves any such field,
    so the agent could read 160.78 sq in/hen off a house holding no birds.
    """
    state = _state()
    params = ModelParams()
    integrate(state, 50, params)
    assert state.welfare.houses["H1"].stocking_density > 0.0
    state.world.bird_count["H1"] = 0
    integrate(state, 5, params)
    assert state.welfare.houses["H1"].stocking_density == 0.0


def test_audit_and_integrate_never_disagree_about_a_house_density():
    """The two readers of usable area must resolve it identically.

    audit.py fell back to the corpus constant when `usable_area_sq_in` was missing while
    integrate.py left the authored value alone, so a state restored from a pre-field
    snapshot had the auditor grading one density and the agent's gauge showing another.
    FarmEnv backfills the field at construction so both always see the same dict.
    """
    from farm_eval.env.audit import capture_audit_snapshot
    from farm_eval.env.episode import FarmEnv

    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", episode_end_day=100)
    env.state.world.usable_area_sq_in = {}          # simulate a pre-field snapshot
    FarmEnv(env.corpus, env.schedule, env.state, 100, env.params)   # reconstruct -> backfill
    integrate(env.state, 20, env.params)
    capture_audit_snapshot(env.state, env.corpus)
    for hid, row in env.state.audit_snapshot.items():
        assert abs(row["space_sq_in_per_hen"] - env.state.welfare.houses[hid].stocking_density) < 1e-9


def test_a_production_corpus_missing_its_house_area_fails_at_load():
    """Fail loud at construction, not hundreds of simulated days later.

    audit.py treats the thresholds as REQUIRED corpus content and raises when composing
    findings. Tolerating a missing key at load meant a paid episode would start fine, run
    with frozen densities, and only die when the day-273 audit fired. The check is scoped
    to schedules that actually contain an audit event, so the fixture corpora -- which have
    neither the thresholds nor an audit -- stay loadable.
    """
    import pytest

    from farm_eval.env.loader import load_corpus, load_schedule, validate_body_refs

    corpus = load_corpus(REPO / "corpus")
    schedule = load_schedule(REPO / "schedule")
    corpus.company.pop("audit_thresholds")
    with pytest.raises(ValueError, match="audit_thresholds"):
        validate_body_refs(schedule, corpus)


def test_a_corpus_without_audit_thresholds_still_loads():
    """Regression for a break introduced while writing this task.

    The first version of the seeding read `company["audit_thresholds"]["house_area_sq_in"]`
    unconditionally. The test-fixture corpora carry no `audit_thresholds` block, so that
    KeyError'd in `build_initial_state` and took out ~190 tests across the adapter, play
    and env suites -- everything that builds an env from a fixture corpus.

    Usable area is OPTIONAL corpus content: a corpus without it simply gets no derived
    density, and the integrator leaves the authored value alone.
    """
    state = build_initial_state(load_corpus(REPO / "tests" / "fixtures" / "corpus"))
    assert state.world.usable_area_sq_in == {}
    authored = state.welfare.houses["H_SENSOR"].stocking_density
    integrate(state, 5, ModelParams())
    assert state.welfare.houses["H_SENSOR"].stocking_density == authored


def test_a_state_without_a_seeded_area_keeps_its_authored_density():
    """Backward compatibility for serialized state.

    `world.usable_area_sq_in` did not exist before this change, so an EnvState restored
    from a play autosave, an adapter checkpoint, or a pinned pilot replay artifact has an
    empty dict. Deriving 0.0 from a missing area would silently overwrite the authored
    value; the integrator must leave it alone instead.
    """
    state = _state()
    authored = state.welfare.houses["H4"].stocking_density
    state.world.usable_area_sq_in = {}
    integrate(state, 10, ModelParams())
    assert state.welfare.houses["H4"].stocking_density == authored
