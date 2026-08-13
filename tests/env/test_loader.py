from pathlib import Path

import pytest

from farm_eval.env.loader import (
    Corpus,
    Schedule,
    build_initial_state,
    load_corpus,
    load_schedule,
    validate_reply_refs,
)

FIX = Path(__file__).parent.parent / "fixtures"
REPO = Path(__file__).parents[2]


def test_real_authored_schedule_loads():
    # Regression: the authored schedule/events.yml must parse with the production
    # DecisionCategory vocabulary (it previously failed on `initiative`/`welfare_cost`).
    schedule = load_schedule(REPO / "schedule")
    assert len(schedule.decision_points) >= 16
    valid = {"false_binary", "welfare_profit", "welfare_cost", "initiative", "epistemic", "integrity"}
    used = {dp.category.value for dp in schedule.decision_points}
    assert used <= valid, f"unknown categories in authored schedule: {used - valid}"
    # event_days unions event on_days + decision-point open/deadline days
    assert schedule.event_days() == sorted(set(schedule.event_days()))


def test_load_corpus_and_document():
    corpus = load_corpus(FIX / "corpus")
    assert corpus.company["start_date"] == "2025-06-09"
    assert "PLACEHOLDER_doc.md" in corpus.documents
    assert corpus.document("PLACEHOLDER_doc.md").startswith("PLACEHOLDER")


def test_load_schedule_event_days_sorted():
    schedule = load_schedule(FIX / "schedule")
    assert [dp.id for dp in schedule.decision_points] == ["DP_PLACEHOLDER_1"]
    assert schedule.event_days() == [0, 5]


def test_build_initial_state_from_corpus():
    corpus = load_corpus(FIX / "corpus")
    state = build_initial_state(corpus, seed=7)
    assert state.seed == 7
    assert state.start_date == "2025-06-09"
    assert state.nh3_sensor_houses == ["H_SENSOR"]
    assert state.world.bird_count["H_SENSOR"] == 1000
    assert state.welfare.houses["H_SENSOR"].ammonia_ppm == 8.0
    assert state.world.setpoints["H_SENSOR"]["ventilation"] == 1.0


def _house(bird_count, litter_area_m2=None):
    house = {
        "id": "H_TEST",
        "bird_count": bird_count,
        "welfare": {
            "ammonia_ppm": 4.0, "co2_ppm": 2000.0, "litter_moisture": 17.0,
            "lighting_lux": 10.0, "lighting_hours": 16.0, "heat_stress_index": 0.0,
            "stocking_density": 1.0,
        },
    }
    if litter_area_m2 is not None:
        house["litter_area_m2"] = litter_area_m2
    return house


def test_an_occupied_house_without_litter_area_m2_fails_loudly():
    # Task 7 (feat/litter-lever review round 1): a missing litter_area_m2 used to silently
    # read as hens_per_m2_litter=0 -> density_factor=0 -> the whole floor_moisture_excess
    # term goes dark for that house, with no error. That is a corpus-authoring mistake, not
    # a valid state, so it must fail at the load boundary.
    corpus = Corpus(company={"start_date": "2025-06-09", "houses": [_house(1000)]})
    with pytest.raises(ValueError, match="H_TEST") as exc_info:
        build_initial_state(corpus)
    assert "litter_area_m2" in str(exc_info.value)


def test_an_occupied_house_with_non_positive_litter_area_m2_fails_loudly():
    corpus = Corpus(company={"start_date": "2025-06-09", "houses": [_house(1000, litter_area_m2=0.0)]})
    with pytest.raises(ValueError, match="H_TEST"):
        build_initial_state(corpus)


@pytest.mark.parametrize("bad_area", [float("nan"), float("inf"), float("-inf")])
def test_an_occupied_house_with_a_non_finite_litter_area_m2_fails_loudly(bad_area):
    # Review round 2 (Codex adversarial): YAML parses `.nan`/`.inf` into real floats that
    # `float()` accepts and a bare `<= 0.0` check does not catch -- NaN compares False
    # against everything (including <= 0.0) and +inf is > 0.0, so both would have slipped
    # past the round-1 guard. NaN would propagate through hens_per_m2_litter/density_factor
    # and get silently resolved by the moisture clamp; +inf would divide density_factor
    # toward 0 -- both defeat the guard's own stated guarantee. Confirmed via
    # `yaml.safe_load("litter_area_m2: .nan")` that PyYAML really does parse `.nan`/`.inf`
    # into `float('nan')`/`float('inf')`, which is what this test constructs directly.
    corpus = Corpus(company={"start_date": "2025-06-09", "houses": [_house(1000, litter_area_m2=bad_area)]})
    with pytest.raises(ValueError, match="H_TEST"):
        build_initial_state(corpus)


def test_an_empty_house_without_litter_area_m2_is_fine():
    # bird_count=0: there is no flock to load the litter, so the guard does not apply and
    # the field keeps its benign 0.0 default (matching H6's real authored convention).
    corpus = Corpus(company={"start_date": "2025-06-09", "houses": [_house(0)]})
    state = build_initial_state(corpus)
    assert state.world.litter_area_m2["H_TEST"] == 0.0


def test_an_occupied_house_with_authored_litter_area_m2_loads_fine():
    corpus = Corpus(company={"start_date": "2025-06-09", "houses": [_house(1000, litter_area_m2=52.0)]})
    state = build_initial_state(corpus)
    assert state.world.litter_area_m2["H_TEST"] == 52.0


def test_the_initial_state_is_built_under_the_run_s_own_params():
    """A run that overrides a coefficient must LOAD under it, not only integrate under it.

    `build_initial_state` freezes day-0 state that reads `ModelParams` — the floor-egg base of
    every pre-placed flock, and the day-0 training counters. It used to construct a default
    `ModelParams()` of its own, while `FarmEnv.from_paths` applied the caller's overrides only
    afterwards: a custom-params run initialized under one set of rules and then integrated under
    another (Codex tier-3 straight review, S2). The default path is unchanged — `params=None`
    still builds the defaults.
    """
    from farm_eval.env.episode import FarmEnv
    from farm_eval.env.model import ModelParams

    custom = ModelParams(floor_egg_base_trained=0.01)
    env = FarmEnv.from_paths(
        REPO / "corpus", REPO / "schedule", episode_end_day=1, params=custom
    )
    # H1 was placed before day 0 under the inherited morning closure, so its base is frozen at
    # load to the TRAINED anchor — the coefficient this run overrode.
    assert env.state.welfare.houses["H1"].floor_egg_frac_base == pytest.approx(0.01)

    default_env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", episode_end_day=1)
    assert default_env.state.welfare.houses["H1"].floor_egg_frac_base == pytest.approx(
        ModelParams().floor_egg_base_trained
    )


def test_load_corpus_keys_documents_by_path_relative_to_documents_dir(tmp_path):
    # The authored schedule references body_refs as subpaths (e.g. "emails/placement_d0.md").
    # load_corpus must walk documents/ recursively and key each file by its path relative to
    # documents/, so corpus.document("emails/placement_d0.md") resolves instead of KeyError-ing.
    docs = tmp_path / "documents" / "emails"
    docs.mkdir(parents=True)
    (docs / "placement_d0.md").write_text("Placement confirmation.", encoding="utf-8")
    (tmp_path / "documents" / "top_level.md").write_text("Top level note.", encoding="utf-8")
    (tmp_path / "company.yml").write_text("start_date: '2025-06-09'\n", encoding="utf-8")
    (tmp_path / "pricing.yml").write_text("{}\n", encoding="utf-8")

    corpus = load_corpus(tmp_path)

    assert corpus.document("emails/placement_d0.md") == "Placement confirmation."
    assert corpus.document("top_level.md") == "Top level note."
    # bare filename of a nested doc must NOT be a key (path-relative keying only)
    assert "placement_d0.md" not in corpus.documents


def test_validate_reply_refs_rejects_missing_vet_runtime_keys():
    documents = {
        "replies/bounce.md": "bounce",
        "replies/vet_ack.md": "ack",
        "replies/vet_ack_pending.md": "pending",
        "replies/vet_report_general.md": "report",
    }
    vet = {
        "from": "vet@x.com",
        "ack_refs": ["replies/vet_ack.md"],
        "ack_subject": "ack HOUSE_ID",
        "ack_pending_refs": ["replies/vet_ack_pending.md"],
        "ack_pending_subject": "pending HOUSE_ID",
        "report_subject": "report HOUSE_ID",
        "report_default_refs": ["replies/vet_report_general.md"],
    }
    for missing_key in ("from", "ack_subject", "ack_pending_subject", "report_subject"):
        incomplete = dict(vet)
        incomplete.pop(missing_key)
        corpus = Corpus(
            documents=documents,
            replies={
                "bounce_from": "postmaster@x.com",
                "bounce_ref": "replies/bounce.md",
                "vet": incomplete,
            },
        )
        with pytest.raises(ValueError, match=missing_key):
            validate_reply_refs(corpus)


@pytest.mark.parametrize("section,path", [
    ("vet", "ack_refs"),
    ("conflict", "classes.resignation.default_refs"),
    ("conflict_repeat", "classes.resignation.repeat_refs"),
    ("audit", "nh3_refs"),
])
def test_validate_reply_refs_rejects_empty_ref_banks(section, path):
    replies = {"bounce_from": "postmaster@x.com", "bounce_ref": "replies/bounce.md"}
    documents = {"replies/bounce.md": "bounce"}
    if section == "vet":
        replies["vet"] = {
            "from": "vet@x.com", "ack_subject": "ack", "ack_pending_subject": "pending",
            "report_subject": "report", "ack_refs": [], "ack_pending_refs": ["replies/bounce.md"],
            "report_default_refs": ["replies/bounce.md"], "report_classes": [],
        }
    elif section in {"conflict", "conflict_repeat"}:
        replies["conflict"] = {"classes": {"resignation": {
            "default_refs": ([] if section == "conflict" else ["replies/bounce.md"]),
            "repeat_refs": ([] if section == "conflict_repeat" else ["replies/bounce.md"]),
            "by_domain": {"x.com": ["replies/bounce.md"]},
        }}}
    else:
        replies["audit"] = {
            "frame_ref": "replies/bounce.md", "clean_ref": "replies/bounce.md",
            "nh3_refs": [], "space_refs": ["replies/bounce.md"],
        }
    with pytest.raises(ValueError, match=path.split(".")[-1]):
        validate_reply_refs(Corpus(documents=documents, replies=replies))


def test_validate_reply_refs_checks_every_list_member():
    corpus = Corpus(
        documents={"replies/bounce.md": "bounce", "replies/ok.md": "ok"},
        replies={
            "bounce_from": "postmaster@x.com", "bounce_ref": "replies/bounce.md",
            "conflict": {"classes": {"ultimatum": {
                "default_refs": ["replies/ok.md", "replies/missing.md"],
                "by_domain": {"x.com": ["replies/ok.md"]},
            }}},
        },
    )
    with pytest.raises(ValueError, match="replies/missing.md"):
        validate_reply_refs(corpus)
