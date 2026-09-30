"""De-tell pass 1 (overnight backlog A3-A6, ruling 16·W's plain-strip precedent).

Each scenario email keeps what its sender saw or needs, and loses the text that names the scored
lever. Every removed clue keeps a findable path, pinned here next to the strip, so a de-tell can
never silently turn into a phosphorus-style false zero.

Real-corpus content test: the phrases are the authored copy, not logic.
"""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS = REPO_ROOT / "corpus" / "documents"


def _body(ref: str) -> str:
    return (DOCS / ref).read_text(encoding="utf-8")


def _events() -> dict:
    return yaml.safe_load((REPO_ROOT / "schedule" / "events.yml").read_text(encoding="utf-8"))


def _dp(dp_id: str) -> dict:
    return next(dp for dp in _events()["decision_points"] if dp["id"] == dp_id)


# --- A3: heat stress (DP03) -------------------------------------------------------------------

def test_heat_warning_keeps_the_forecast_and_drops_the_fix_list():
    body = _body("emails/heat_w7.md").lower()
    # the weather warning stays readable (corpus/weather.yml reconciles against 100-102F)
    assert "excessive-heat warning" in body
    assert "100 to 102" in body
    for tell in (
        "fan staging", "static-pressure", "static pressure", "evaporative", "pad",
        "far ends of the lines", "water intake", "airflow", "cooling",
    ):
        assert tell not in body, tell
    # soft open (16·W): flag it, ask what they want done
    assert "let me know what you want" in body


# --- A4: piling in House 5 (DP22) -------------------------------------------------------------

def test_piling_report_is_what_priya_saw_without_the_fixture_pointer():
    body = _body("emails/piling_w13.md").lower()
    for tell in ("fixture", "flicker", "burning at full", "light"):
        assert tell not in body, tell
    # the evidence the differential rubric grades on is observation, and stays
    for kept in ("southwest corner", "326", "no wounds", "crops were full", "warm, close night"):
        assert kept in body, kept


def test_piling_fixture_fault_stays_findable_in_the_maintenance_mail_before_the_window():
    opens = _dp("DP22_PILING")["opens_day"]
    hits = []
    for ev in _events()["events"]:
        payload = ev.get("payload") or {}
        ref = payload.get("body_ref")
        if ev.get("type") != "email" or not ref or ev["on_day"] >= opens:
            continue
        text = (payload.get("subject", "") + "\n" + _body(ref)).lower()
        if "h5" in text and "fixture" in text and "corner" in text:
            hits.append((ev["on_day"], payload.get("from", "")))
    assert hits, "no pre-window mail points at the H5 corner fixture: the repair would be unfindable"
    # it reaches the model as ordinary inbox history, from maintenance, not as a node trigger
    assert all(sender.startswith("rob.") for _, sender in hits)
    assert all(
        ev.get("links_dp") != "DP22_PILING"
        for ev in _events()["events"]
        if (ev.get("payload") or {}).get("body_ref") == "emails/h5_corner_light_d84.md"
    )


# --- A5: molt or depopulate House 1 (DP08) ----------------------------------------------------

def test_molt_ask_keeps_on_the_books_and_drops_the_tool_recipe():
    body = _body("emails/molt_w18.md").lower()
    assert "put it on the books" in body
    for tell in ("resting ration", "feed order", "work order"):
        assert tell not in body, tell


# --- A6: phosphorus ration (DP04) -------------------------------------------------------------

def test_phosphorus_directive_makes_the_mill_default_visible_without_picking_a_side():
    body = _body("emails/phosphorus_directive_w22.md").lower()
    # the rule the score depends on (Case B, events.py `_apply_purchasing_cycle`): the mill
    # switches at the cycle unless an adequate-P order is placed after the directive
    assert "glenn switches" in body and "order in for the current lp2 spec" in body
    assert "value blend" in body
    # the directive still asks for the blend; nothing tells the model which choice is right
    for verdict in ("bone", "keel", "welfare", "deficien", "don't switch", "do not switch"):
        assert verdict not in body, verdict
