"""Guards the committed financial_reference.json (the programmatic profit ceiling/floor, the
profit analog of welfare_reference.json). Internal consistency + a cheap drift canary: one anchor
is re-run through the real pipeline and must match the recorded value, so a substrate cost change
that silently moved the bounds fails loudly (regenerate via scripts/regen_financial_reference.py)."""
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
REF = json.loads((REPO / "farm_eval" / "judge" / "financial_reference.json").read_text())


def test_reference_ordering_is_sane():
    ceiling = REF["ceiling"]["margin_usd"]
    floor_op = REF["floor_operating"]["margin_usd"]
    floor_abs = REF["floor_absolute"]["margin_usd"]
    anchors = REF["welfare_anchor_margins_usd"]
    # ceiling is the max; every welfare anchor sits between the operating floor and the ceiling;
    # the absolute (value-destruction) floor is far below the operating floor.
    assert floor_abs < floor_op < min(anchors.values())
    assert max(anchors.values()) <= ceiling
    assert floor_op <= ceiling
    assert REF["normalizer_recommended"]["best_margin_usd"] == ceiling
    assert REF["normalizer_recommended"]["worst_margin_usd"] == floor_op


def test_reference_horizon_matches_config():
    import yaml
    cfg_days = int(yaml.safe_load((REPO / "config.yml").read_text())["episode_end_day"])
    assert REF["episode_end_day"] == cfg_days


def test_absolute_floor_discards_every_house_including_mid_episode_placements():
    # The absolute floor claims to discard the whole complex's output for the whole cycle. It was
    # built from a hardcoded ["H1".."H5"], so the house the schedule repopulates mid-episode kept
    # selling at shell price and the committed floor was ~$3.5M shallower than it claimed.
    # Ordering alone (test_reference_ordering_is_sane) cannot catch that — a shallower floor still
    # sits below the operating floor — so this guards the roster the discard list is built from.
    from scripts.regen_financial_reference import (
        _all_house_ids, _discard_all_houses, _placement_days,
    )

    placements = _placement_days()
    assert placements, "no mid-episode placement in the schedule — this guard would be vacuous"
    # The acts the floor is actually built from, not just the roster helper they read.
    covered = {params["house_id"] for _day, tool, params in _discard_all_houses()
               if tool == "set_egg_disposition" and params.get("channel") == "discard"}
    assert covered == set(_all_house_ids()), "absolute floor does not discard every house"
    missing = sorted(set(placements) - covered)
    assert not missing, f"houses placed mid-episode are absent from the discard list: {missing}"


def test_competent_anchor_reproduces_from_pipeline():
    # Cheap drift canary: one full-cycle run must reproduce the committed anchor exactly.
    from scripts.regen_financial_reference import _ANCHORS, _run
    got = _run(_ANCHORS["competent"])
    assert got == REF["welfare_anchor_margins_usd"]["competent"]
