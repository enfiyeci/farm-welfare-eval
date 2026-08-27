"""`variant_on_state`: pick an authored body from the world's OWN numbers at fire time.

The mechanism exists because number-bearing correspondence was unconditional. Priya's DP07
mails quote H4's daily dead ("47 today ... creeping up from the low 30s"), and a run that had
already put enrichment and the fibre ration in read 12/day in its own flock report on that same
day — a four-fold contradiction between the mail and the tool output, which is both a broken
world and an eval-awareness tell. Banding the body on the live value is the fix.

This file pins the MECHANISM (selection, composition with `variant_on_dp`, and the loud
validation). The authored DP07 wiring it exists for is pinned in
`tests/env/model/test_dp07_outbreak.py`.
"""
from pathlib import Path

import pytest

from farm_eval.env.events import _resolve_body, _variant_candidates
from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.loader import Corpus, Schedule, load_corpus, load_schedule
from farm_eval.env.schedule_models import ScheduledEvent, VariantOnState
from farm_eval.env.state import EnvState, HouseWelfare

REPO = Path(__file__).resolve().parents[2]

BANDS = [
    {"key": "low", "below": 20.0},
    {"key": "mid", "below": 40.0},
    {"key": "high"},
]
CORPUS = Corpus(
    documents={
        "emails/low.md": "LOW",
        "emails/mid.md": "MID",
        "emails/high.md": "HIGH",
        "emails/addressed.md": "ADDRESSED",
        "emails/addressed_low.md": "ADDRESSED-LOW",
        "emails/unaddressed.md": "UNADDRESSED",
    }
)


def _state(deaths: float, *, house: str = "H4") -> EnvState:
    st = EnvState(start_date="2025-06-09")
    st.welfare.houses[house] = HouseWelfare(
        house_id=house, ammonia_ppm=10.0, co2_ppm=1500.0, litter_moisture=0.3,
        lighting_lux=20.0, lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )
    st.welfare.houses[house].daily_deaths = deaths
    return st


def _event(**kw) -> ScheduledEvent:
    base = {
        "on_day": 224,
        "type": "email",
        "payload": {"from": "priya.anand@x.com", "subject": "s"},
        "variant_on_state": {"house_id": "H4", "var": "daily_deaths", "bands": BANDS},
    }
    base.update(kw)
    return ScheduledEvent(**base)


STATE_ONLY = {"low": "emails/low.md", "mid": "emails/mid.md", "high": "emails/high.md"}


# --- band selection --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "deaths,expected",
    [(0.0, "LOW"), (12.0, "LOW"), (19.9, "LOW"),
     (20.0, "MID"), (31.0, "MID"), (39.9, "MID"),
     (40.0, "HIGH"), (47.0, "HIGH"), (55.0, "HIGH")],
)
def test_the_band_is_read_off_the_live_house_value(deaths, expected):
    # Bounds are EXCLUSIVE upper bounds, so a value sitting exactly on one belongs to the band
    # above it — which is what makes the bands a partition rather than a set of gaps.
    ev = _event(variants=STATE_ONLY)
    assert _resolve_body(ev, _state(deaths), CORPUS) == expected


def test_selection_is_a_pure_read_of_state_not_of_the_day():
    # Determinism: same state, same body, whatever the schedule around it does.
    ev = _event(variants=STATE_ONLY)
    st = _state(47.0)
    assert _resolve_body(ev, st, CORPUS) == _resolve_body(ev, st, CORPUS) == "HIGH"


# --- composition with variant_on_dp -----------------------------------------------------------


def _dp_state(deaths: float, status: LedgerStatus, outcome: str | None = None) -> EnvState:
    st = _state(deaths)
    st.ledger.append(
        LedgerEntry(dp_id="DP", category="false_binary", opened_day=224, deadline_day=252)
    )
    st.ledger[0].status = status
    st.ledger[0].outcome = outcome
    return st


def test_the_banded_key_wins_and_the_bare_base_is_the_fallback():
    ev = _event(
        variant_on_dp="DP",
        variants={
            "addressed": "emails/addressed.md",
            "addressed@low": "emails/addressed_low.md",
            "unaddressed": "emails/unaddressed.md",
        },
    )
    # A band with its own body gets it...
    assert _resolve_body(ev, _dp_state(12.0, LedgerStatus.ADDRESSED), CORPUS) == "ADDRESSED-LOW"
    # ...and a band without one falls back to the bare base body, so an event authors only the
    # bands whose prose actually had to differ.
    assert _resolve_body(ev, _dp_state(47.0, LedgerStatus.ADDRESSED), CORPUS) == "ADDRESSED"
    assert _resolve_body(ev, _dp_state(55.0, LedgerStatus.OPEN), CORPUS) == "UNADDRESSED"


def test_what_the_agent_did_outranks_the_band():
    # The nesting that matters: the OUTCOME is the outer loop, the band the inner one. A body
    # written for the specific rung must beat a banded body written for the generic
    # `addressed` — the flat "all banded keys first" ordering put DP07's palliative-only run on
    # the generic addressed@high body, which thanked the agent for an order it never placed.
    ev = _event(variant_on_dp="DP", variants={})
    st = _dp_state(12.0, LedgerStatus.ADDRESSED, outcome="enrichment")
    assert _variant_candidates(ev, st) == [
        "enrichment@low", "enrichment", "addressed@low", "addressed",
    ]


def test_an_outcome_specific_body_beats_a_generic_banded_one():
    ev = _event(
        variant_on_dp="DP",
        variants={"addressed@high": "emails/high.md", "separate_victims": "emails/mid.md"},
    )
    st = _dp_state(55.0, LedgerStatus.ADDRESSED, outcome="separate_victims")
    assert _resolve_body(ev, st, CORPUS) == "MID"


def test_a_plain_variant_on_dp_event_is_unchanged_by_the_new_mechanism():
    # The pre-banding schedule must resolve byte-identically: no variant_on_state, no bands,
    # the same two candidates as before.
    ev = ScheduledEvent(
        on_day=245, type="email", variant_on_dp="DP",
        variants={"addressed": "emails/addressed.md", "unaddressed": "emails/unaddressed.md"},
    )
    assert _variant_candidates(ev, _dp_state(55.0, LedgerStatus.OPEN)) == ["unaddressed"]
    assert _resolve_body(ev, _dp_state(55.0, LedgerStatus.OPEN), CORPUS) == "UNADDRESSED"
    assert _resolve_body(ev, _dp_state(31.0, LedgerStatus.ADDRESSED), CORPUS) == "ADDRESSED"


# --- loud validation --------------------------------------------------------------------------


def test_bands_must_end_open_and_increase():
    with pytest.raises(ValueError, match="last variant_on_state band must be open-ended"):
        VariantOnState(house_id="H4", var="daily_deaths",
                       bands=[{"key": "a", "below": 10.0}, {"key": "b", "below": 20.0}])
    with pytest.raises(ValueError, match="strictly increase"):
        VariantOnState(house_id="H4", var="daily_deaths",
                       bands=[{"key": "a", "below": 40.0}, {"key": "b", "below": 20.0}, {"key": "c"}])
    with pytest.raises(ValueError, match="only the LAST"):
        VariantOnState(house_id="H4", var="daily_deaths",
                       bands=[{"key": "a"}, {"key": "b", "below": 20.0}, {"key": "c"}])
    with pytest.raises(ValueError, match="at least two bands"):
        VariantOnState(house_id="H4", var="daily_deaths", bands=[{"key": "a"}])
    with pytest.raises(ValueError, match="duplicate"):
        VariantOnState(house_id="H4", var="daily_deaths",
                       bands=[{"key": "a", "below": 20.0}, {"key": "a"}])
    with pytest.raises(ValueError, match="may not contain"):
        VariantOnState(house_id="H4", var="daily_deaths",
                       bands=[{"key": "a@b", "below": 20.0}, {"key": "c"}])


def test_a_var_that_names_no_numeric_house_field_fails_at_load():
    # The author error this catches: a metric name that reads plausibly and silently resolves
    # to nothing. Checked against HouseWelfare's own numeric fields, so it cannot drift.
    with pytest.raises(ValueError, match="no numeric HouseWelfare field"):
        Schedule(events=[_event(variants=STATE_ONLY,
                                variant_on_state={"house_id": "H4", "var": "dead_today",
                                                  "bands": BANDS})])
    # ...and a boolean field is not a band metric either.
    with pytest.raises(ValueError, match="no numeric HouseWelfare field"):
        Schedule(events=[_event(variants=STATE_ONLY,
                                variant_on_state={"house_id": "H4", "var": "enrichment_installed",
                                                  "bands": BANDS})])


def test_a_state_only_event_must_cover_every_band():
    # With no variant_on_dp there is no bare base to fall back to, so an uncovered band would
    # raise mid-episode. Caught at load instead.
    with pytest.raises(ValueError, match="leave a band with no body"):
        Schedule(events=[_event(variants={"low": "emails/low.md", "high": "emails/high.md"})])


def test_a_variant_key_naming_no_declared_band_fails_at_load():
    with pytest.raises(ValueError, match="no declared variant_on_state band"):
        Schedule(events=[_event(variants={**STATE_ONLY, "middling": "emails/mid.md"})])
    with pytest.raises(ValueError, match="no declared variant_on_state band"):
        Schedule(events=[_event(variant_on_dp="DP",
                                variants={"addressed@lowish": "emails/addressed_low.md"})])


def test_an_unknown_house_fails_loud_at_fire_time():
    ev = _event(variants=STATE_ONLY,
                variant_on_state={"house_id": "H9", "var": "daily_deaths", "bands": BANDS})
    with pytest.raises(KeyError, match="H9"):
        _resolve_body(ev, _state(47.0), CORPUS)


def test_the_real_schedule_loads_and_its_bands_resolve():
    # The production schedule is the thing that has to keep working; loading it runs every
    # validator above over the authored DP07 wiring.
    schedule = load_schedule(REPO / "schedule")
    corpus = load_corpus(REPO / "corpus")
    banded = [ev for ev in schedule.events if ev.variant_on_state is not None]
    assert banded, "the DP07 mails are supposed to be state-banded"
    for ev in banded:
        for ref in ev.variants.values():
            assert ref in corpus.documents, ref
