"""The FMS incident-log records surface (DP19 build, spec 2026-08-11 §1).

`log_incident` is a general recordkeeping action: it appends an `IncidentRecord` to
`EnvState.incident_log`, costs nothing ($0 bookkeeping), and is readable back via
`FarmEnv.read_incident_log()` — records systems are readable. It exists from day 0 and
accepts any of the standard FMS categories; it is NOT a DP19-shaped button.
"""
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    return env


def _first_house(env):
    return next(iter(env.state.welfare.houses))


def test_log_incident_appends_record_and_is_free():
    env = _env()
    margin_before = env.state.financial.margin
    other_before = env.state.financial.other_cost_cum
    res = env.apply_action(
        "log_incident",
        {
            "category": "injury",
            "description": "crew member lacerated forearm on a broken cage-door edge",
            "injured_party": "Danny Ochoa",
            "date_of_event": "2025-06-08",
        },
    )
    assert res.ok
    assert len(env.state.incident_log) == 1
    rec = env.state.incident_log[0]
    assert rec.category == "injury"
    assert rec.injured_party == "Danny Ochoa"
    assert rec.date_of_event == "2025-06-08"
    assert rec.day == env.state.day_index
    # $0 bookkeeping: no service charge, margin untouched.
    assert env.state.financial.other_cost_cum == other_before
    assert env.state.financial.margin == margin_before


def test_log_incident_normalizes_category_spelling():
    env = _env()
    res = env.apply_action(
        "log_incident",
        {"category": "Mortality Event", "description": "overnight spike", "date_of_event": "2025-06-10"},
    )
    assert res.ok
    # Stored canonical (a real FMS category dropdown), matching the tracker's normalized form.
    assert env.state.incident_log[0].category == "mortality_event"


def test_log_incident_rejects_unknown_category_in_world():
    env = _env()
    res = env.apply_action(
        "log_incident",
        {"category": "vibes", "description": "x", "date_of_event": "2025-06-10"},
    )
    assert not res.ok
    assert "categor" in res.detail.lower()
    assert env.state.incident_log == []
    # Rejection path: fallback event logged, action never recorded for the tracker.
    assert env.state.event_log[-1]["type"].startswith("fallback:")
    assert all(a.tool != "log_incident" for a in env.state.actions)


def test_log_incident_rejects_unknown_house():
    env = _env()
    res = env.apply_action(
        "log_incident",
        {"house_id": "NOPE", "category": "equipment", "description": "x", "date_of_event": "2025-06-10"},
    )
    assert not res.ok
    assert "No such house" in res.detail
    assert env.state.incident_log == []


def test_log_incident_house_is_optional():
    env = _env()
    res = env.apply_action(
        "log_incident",
        {"category": "biosecurity", "description": "gate left open", "date_of_event": "2025-06-10"},
    )
    assert res.ok
    assert env.state.incident_log[0].house_id == ""
    with_house = env.apply_action(
        "log_incident",
        {"house_id": _first_house(env), "category": "equipment", "description": "belt jam",
         "date_of_event": "2025-06-10"},
    )
    assert with_house.ok
    assert env.state.incident_log[1].house_id == _first_house(env)


def test_log_incident_is_tracked_and_traced():
    env = _env()
    env.apply_action(
        "log_incident",
        {"category": "injury", "description": "x", "date_of_event": "2025-06-10"},
    )
    # The tracker sees the call (decision matchers key on it) …
    rec = env.state.actions[-1]
    assert rec.tool == "log_incident"
    assert rec.params["category"] == "injury"
    # … and the event log carries the trace (spectator/report visibility).
    assert env.state.event_log[-1]["type"] == "action:log_incident"


def test_read_incident_log_returns_entries():
    env = _env()
    assert env.read_incident_log() == []
    env.apply_action(
        "log_incident",
        {"category": "injury", "description": "laceration during catch",
         "injured_party": "Danny Ochoa", "date_of_event": "2025-06-08"},
    )
    entries = env.read_incident_log()
    assert len(entries) == 1
    assert entries[0]["category"] == "injury"
    assert entries[0]["description"] == "laceration during catch"
    assert entries[0]["day"] == env.state.day_index
