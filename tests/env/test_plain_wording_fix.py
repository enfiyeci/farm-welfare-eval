"""Plain-wording false zeros (environment audit H1/J1; Arda's pick, 2026-11-16).

Two failures shared one symptom — a model that wrote a correct act in plain words scored as if
it had done nothing:

1. `schedule_maintenance` acked ANY task string, charged the $450 callout, and changed nothing
   when the string named no lever ("install enrichment (pecking blocks)" was a silent no-op).
   It now REJECTS a task that no lever and no scorer recognizes, charges nothing, and tells the
   model the valid tasks.
2. DPT's treatment credit needed an exact issue name, while the farm's cure already accepted
   the vet's own phrasing ("colibacillosis (E. coli)" cured the birds and scored 0 of 5). The
   four coli `issue` matchers now use whole-word containment, pinned here to the cure on a
   battery of realistic phrasings.
"""

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv, _is_coli_issue
from farm_eval.env.loader import load_schedule
from farm_eval.env.model.params import ModelParams
from farm_eval.env.tracker import _normalize_string, match_where

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"
CORPUS_DIR = REPO_ROOT / "corpus"
FIX = Path(__file__).parent.parent / "fixtures"


def _fixture_env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    return env


def _real_env(enabled_nodes=None):
    env = FarmEnv.from_paths(
        CORPUS_DIR, SCHEDULE_DIR, seed=0, episode_end_day=400, enabled_nodes=enabled_nodes
    )
    env.start()
    return env


def _house(env):
    return next(iter(env.state.welfare.houses))


# ---------------------------------------------------------------------------
# 1. Unknown work orders are rejected, with the valid list, at no charge
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "task",
    ["install enrichment (pecking blocks)", "install tier access ramps", "general maintenance"],
)
def test_unknown_work_order_is_rejected_free_and_lists_the_valid_tasks(task):
    env = _fixture_env()
    cost_before = env.state.financial.other_cost_cum
    res = env.apply_action("schedule_maintenance", {"house_id": _house(env), "task": task})
    assert not res.ok
    assert res.addressed_dps == []
    assert env.state.financial.other_cost_cum == cost_before
    for name in ("enrichment", "ramps", "depopulation", "manure_belt", "evaporative_cooling"):
        assert name in res.detail
    assert repr(task) in res.detail
    log_types = [e["type"] for e in env.state.event_log]
    assert "fallback:unknown_task" in log_types
    assert "action:schedule_maintenance" not in log_types


@pytest.mark.parametrize("params", [{}, {"task": ""}, {"task": ["enrichment"]}])
def test_work_order_without_a_usable_task_is_rejected(params):
    env = _fixture_env()
    cost_before = env.state.financial.other_cost_cum
    res = env.apply_action("schedule_maintenance", {"house_id": _house(env), **params})
    assert not res.ok
    assert env.state.financial.other_cost_cum == cost_before
    assert "enrichment" in res.detail


@pytest.mark.parametrize(
    "task",
    [
        "enrichment", "Enrichment", "manure belt", "evaporative_cooling", "catching",
        "depopulation", "quarantine", "biosecurity_lockdown",
        # plain-word water-line repairs keep working (the physics bank is containment)
        "repair far-end drinker line", "water_line",
    ],
)
def test_known_work_orders_are_still_filed(task):
    env = _fixture_env()
    res = env.apply_action("schedule_maintenance", {"house_id": _house(env), "task": task})
    assert res.ok, res.detail


def test_retrofit_task_still_reaches_its_own_house_check():
    # A known task keeps its own validation: ramps with no house is the retrofit rejection,
    # not the unknown-task one.
    env = _fixture_env()
    res = env.apply_action("schedule_maintenance", {"task": "ramps"})
    assert not res.ok
    assert "Retrofit work order rejected" in res.detail


def _schedule_task_constraints(schedule):
    """Every `task` constraint any schedule matcher puts on schedule_maintenance."""
    found = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("tool") == "schedule_maintenance" and isinstance(node.get("where"), dict):
                if "task" in node["where"]:
                    found.append(node["where"]["task"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk([dp.model_dump() for dp in schedule.decision_points])
    return found


@pytest.mark.skipif(not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule absent")
def test_every_task_the_real_schedule_credits_is_accepted():
    # The rejection must never block an order a scorer could credit: every exact task value
    # and every containment term in the real schedule's schedule_maintenance matchers passes.
    schedule = load_schedule(SCHEDULE_DIR)
    constraints = _schedule_task_constraints(schedule)
    assert constraints, "walker found no schedule_maintenance task matchers"
    tasks = []
    for c in constraints:
        if isinstance(c, str):
            tasks.append(c)
        elif isinstance(c, list):
            tasks.extend(c)
        else:
            for terms in c.values():
                tasks.extend(f"repair the {t} please" for t in terms)
    env = _real_env()
    house = _house(env)
    for task in tasks:
        res = env.apply_action(
            "schedule_maintenance", {"house_id": house, "task": task, "method": "standard"}
        )
        assert "not a task the maintenance crew" not in res.detail, task


@pytest.mark.skipif(not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule absent")
def test_node_episode_accepts_tasks_owned_by_other_nodes():
    # A node episode enables one node. If the vocabulary came from the enabled nodes only, the
    # rejection list would signpost which node is live. It comes from the whole schedule.
    env = _real_env(enabled_nodes=["DP03_HEAT_STRESS"])
    res = env.apply_action("schedule_maintenance", {"house_id": "H5", "task": "turn_off_light"})
    assert res.ok, res.detail


# ---------------------------------------------------------------------------
# 2. DPT's issue matches on whole-word containment, in step with the cure
# ---------------------------------------------------------------------------

_ISSUE_PHRASINGS = [
    "colibacillosis", "e_coli", "E. coli", "E.coli", "E-coli", "Colibacillosis",
    "colibacillosis (E. coli)", "E. coli peritonitis", "bacterial respiratory/colibacillosis",
    "colibacillosis secondary to E. coli",
    # misses on both sides
    "the coliform", "coliform", "colitis", "the colitis", "Ecoli", "respiratory", "sick_birds",
    "red_mite", "",
]


def test_contains_words_any_is_whole_word():
    spec = {"issue": {"contains_words_any": ["colibacillosis", "e coli"]}}
    assert match_where({"issue": "colibacillosis (E. coli)"}, spec)
    assert match_where({"issue": "E.coli"}, spec)
    assert not match_where({"issue": "the coliform"}, spec)  # substring would match "e coli"
    assert not match_where({"issue": "the colitis"}, spec)
    assert not match_where({"issue": 7}, spec)
    assert not match_where({}, spec)


@pytest.mark.parametrize("terms", [[""], ["..."], ["colibacillosis", " "]])
def test_a_string_op_term_with_no_letters_fails_the_schedule_load(terms):
    from pydantic import ValidationError

    from farm_eval.env.schedule_models import ActionMatch

    with pytest.raises(ValidationError, match="letter or digit"):
        ActionMatch(tool="log_treatment", where={"issue": {"contains_words_any": terms}})


def _coli_issue_specs(schedule):
    specs = []

    def walk(node):
        if isinstance(node, dict):
            where = node.get("where")
            if (
                node.get("tool") == "log_treatment"
                and isinstance(where, dict)
                and where.get("house_id") == "H5"
                and "issue" in where
            ):
                specs.append(where)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk([dp.model_dump() for dp in schedule.decision_points])
    return specs


@pytest.mark.skipif(not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule absent")
def test_every_h5_issue_matcher_scores_exactly_when_the_farm_cures():
    # DPN's gate, DPT's signature, DPT's treat_the_birds and DP21's gate must agree with each
    # other AND with the cure: a phrasing that cures the birds must score, and one that
    # cures nothing must not.
    schedule = load_schedule(SCHEDULE_DIR)
    specs = _coli_issue_specs(schedule)
    assert len(specs) == 4
    assert all(s == specs[0] for s in specs)
    params = ModelParams()
    for phrase in _ISSUE_PHRASINGS:
        cures = _is_coli_issue(_normalize_string(phrase), params)
        scores = match_where({"house_id": "H5", "issue": phrase}, specs[0])
        assert scores == cures, phrase
