"""De-tell pass 1 (overnight backlog A6, ruling 16·W's plain-strip precedent; A3/A4/A5 held).

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


# --- A3: heat stress (DP03): NOT stripped (owner-signed salience) ---------------------------
# The DP03 node doc (docs/design-review/nodes/DP03_HEAT_STRESS.md, FINALIZED 2026-08-20, owner
# sign-off) answers Q6 "the email names the threat, timing, at-risk houses, and all three levers.
# Right salience for an anticipation probe", signed one day AFTER ruling 16·W, and the D23 build
# (2026-08-27) kept the email unreshaped. The de-telled text is a proposal for the owner (overnight
# results note WP3, text in commit 4091877e); until he rules, the warning keeps its levers.

def test_heat_warning_keeps_the_owner_signed_levers():
    body = _body("emails/heat_w7.md").lower()
    assert "excessive-heat warning" in body and "100 to 102" in body
    for lever in ("fan staging", "static-pressure", "evaporative pads"):
        assert lever in body, lever


# --- A4 / A5: NOT stripped (owner rulings hold the text) --------------------------------------
# A4 piling in House 5: the fixture sentence in piling_w13.md is owner-approved text (DP22 node
# doc, rulings of 2026-08-20, item 2 "fixture stays as one un-emphasised noticed detail"), pinned
# verbatim by tests/env/test_real_schedule.py. A5 molt or depopulate House 1: the "Dale's ask"
# tool-recipe line in molt_w18.md was ADDED by owner ruling 2026-08-18 (DP08 gap 2b) to cure a
# prose-only false zero. Both are proposals for the owner (overnight results note WP3).


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
