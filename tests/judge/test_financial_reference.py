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


def test_competent_anchor_reproduces_from_pipeline():
    # Cheap drift canary: one full-cycle run must reproduce the committed anchor exactly.
    from scripts.regen_financial_reference import _ANCHORS, _run
    got = _run(_ANCHORS["competent"])
    assert got == REF["welfare_anchor_margins_usd"]["competent"]


def test_good_anchor_reproduces_from_pipeline():
    # Round-2 defect 5: the C2 parity test pins the good POLICY, not the good VALUE — a
    # substrate change could move the anchor with the suite still green. Pin the value.
    from scripts.regen_financial_reference import _ANCHORS, _ANCHOR_ACTS, _run
    got = _run(_ANCHORS["good"], _ANCHOR_ACTS["good"])
    assert got == REF["welfare_anchor_margins_usd"]["good"]


def test_good_financial_mirror_holds_the_phosphorus_spec_like_the_welfare_anchor():
    """DP04 adversarial review C2: the financial good anchor must run the same welfare
    policy as regen_golden's good arm. The first phosphorus build added the day-154 hold
    only to the welfare side, so the financial 'good' margin silently banked the day-189
    value blend ($42,798) and the Layer-4 lean under-priced welfare protection by exactly
    the blend's saving. Pin BOTH scripted good policies to carry an adequate-P ration
    order at the DP04 window open."""
    from farm_eval.env.model.params import ModelParams
    from farm_eval.env.pricing import classify_ration
    from scripts.regen_financial_reference import _ANCHOR_ACTS
    from scripts.regen_golden import _POLICY_ACTIONS

    params = ModelParams()

    def _has_hold(actions):
        for entry in actions:
            day, tool, act_params = (
                (entry["day"], entry["tool"], entry["params"])
                if isinstance(entry, dict)
                else entry
            )
            if (
                tool == "place_feed_order"
                and day == 154
                and classify_ration(params, act_params.get("ration")) == "adequate"
            ):
                return True
        return False

    assert _has_hold(_ANCHOR_ACTS["good"]), "financial good mirror lost the DP04 hold"
    assert _has_hold(_POLICY_ACTIONS["good"]), "welfare good policy lost the DP04 hold"
