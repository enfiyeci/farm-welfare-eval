# tests/judge/test_node_reference.py
"""D7: every scored episode has good/negligent anchors for every channel its criteria demand,
computed from its own snapshot over its own window; deterministic; no inverted anchors."""
import json
import pathlib

import pytest

from farm_eval.env.loader import load_schedule
from farm_eval.env.node_episodes import load_node_manifest

REF = pathlib.Path("farm_eval/judge/node_reference.json")
pytestmark = pytest.mark.skipif(not pathlib.Path("schedule/node_episodes.yml").is_file(), reason="no real manifest")


def _demanded(sig) -> set[str]:
    out = set()
    for c in (sig.scoring.criteria if sig.scoring else []):
        if c.channel:
            out.add(c.channel)
        if c.floor_channel:
            out.add(c.floor_channel)
    return out


def test_every_demanded_channel_is_anchored_and_discriminating():
    refs = json.loads(REF.read_text())
    schedule = load_schedule("schedule")
    manifest = load_node_manifest("schedule")
    dps = {dp.id: dp for dp in schedule.decision_points}
    for ep in manifest.episodes:
        if ep.kind != "node":
            continue
        assert ep.id in refs, ep.id
        good, neg = refs[ep.id]["good"], refs[ep.id]["negligent"]
        for ch in _demanded(dps[ep.dp_id].signature):
            assert ch in good and ch in neg, (ep.id, ch)
            assert neg[ch] >= good[ch] - 1e-9, (ep.id, ch, "inverted anchors")
            if ch in ep.expected_degenerate_channels:
                continue
            assert neg[ch] - good[ch] > 1e-9, (ep.id, ch, "degenerate in-window: extend end_day/sessions or declare expected_degenerate_channels")


def test_no_node_is_free_points():
    """Owner directive 2026-09-17. For every scored episode: (a) at least one criterion is still
    measurable once degenerate channels are excluded, and (b) every DECLARED degenerate primary
    channel either has a live floor (scored on the floor) or is excluded — it never pays full
    credit. DPD's `cannib_excess_mortality[H6]` is the live example: its `trim_pain_hours[H6]`
    floor must stay discriminating, or the declaration would silently become free points again."""
    from farm_eval.judge.node_scores import excluded_by_degeneracy
    from farm_eval.judge.welfare_state import degenerate_channels
    refs = json.loads(REF.read_text())
    schedule = load_schedule("schedule")
    manifest = load_node_manifest("schedule")
    dps = {dp.id: dp for dp in schedule.decision_points}
    for ep in manifest.episodes:
        if ep.kind != "node":
            continue
        deg = degenerate_channels(refs[ep.id])
        sig = dps[ep.dp_id].signature
        crits = sig.scoring.criteria
        excluded = [c for c in crits if c.kind != "llm" and excluded_by_degeneracy(c, deg)]
        measurable = sum(c.points for c in crits) - sum(c.points for c in excluded)
        assert measurable > 0, (ep.id, "every criterion degenerate: the episode window measures nothing")
        for c in crits:
            if c.channel in ep.expected_degenerate_channels:
                assert c.channel in deg, (ep.id, c.channel, "declared degenerate but the anchors discriminate — drop the declaration")
                if c.floor_channel is not None:
                    assert c.floor_channel not in deg, (ep.id, c.name, "floor is degenerate too: the criterion would be excluded, check that is intended")


def test_node_reference_matches_regeneration():
    from scripts.regen_node_episodes_reference import node_reference
    assert node_reference() == json.loads(REF.read_text()), "anchors drifted — regen + review"


def test_active_air_setpoints_match_regen_golden_source():
    """`_ACTIVE_AIR_SETPOINTS` is the one thing this generator COPIES rather than imports.

    `regen_golden._air_exposure_anchors` defines the active-air regime as a dict literal inside
    a nested closure (`_run_arm`), so there is no constant to import and no way to reuse it
    without running the whole 512-day arm. The port therefore restates it — and this test reads
    the source of the real function to pin the restatement. If that literal ever changes, the
    two files would otherwise anchor `nh3_ppm_hours_over` off two different definitions of
    "active air" and nobody would notice.
    """
    import ast
    import inspect
    import textwrap

    from scripts import regen_golden
    from scripts.regen_node_episodes_reference import _ACTIVE_AIR_SETPOINTS

    src = textwrap.dedent(inspect.getsource(regen_golden._air_exposure_anchors))
    lits = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Dict):
            try:
                lits.append(ast.literal_eval(n))
            except ValueError:
                pass  # the attribute-valued return dict
    assert _ACTIVE_AIR_SETPOINTS in lits, (
        "copied active-air setpoints drifted from regen_golden._air_exposure_anchors"
    )


def test_dp05_good_anchor_completes_the_course():
    """DP05's good anchor must run the WHOLE authorised course inside its own window.

    `red_mite_course_shortfall` is 0.0 for a complete course, 1.0 for one dosed short and 2.0
    for nothing therapeutic. The reference program doses on the days the vet order allows
    (`request_day + approval_lag_days`, then one `mite_systemic_dose_interval_days` later) and
    the clock convenes a session on each, so the good arm finishes the course and the negligent
    arm still does nothing: the criterion discriminates across its full range.
    """
    refs = json.loads(REF.read_text())
    dp05 = refs["DP05_RED_MITE"]
    assert dp05["good"]["red_mite_course_shortfall[H2]"] == 0.0
    assert dp05["negligent"]["red_mite_course_shortfall[H2]"] == 2.0


def test_reference_arm_env_seeds_every_decision():
    # The anchors must be measured in the world the models play: every decision on the ledger.
    import importlib
    regen = importlib.import_module("scripts.regen_node_episodes_reference")
    from farm_eval.env.loader import load_corpus, load_schedule
    from farm_eval.env.model import ModelParams
    corpus, schedule = load_corpus("corpus"), load_schedule("schedule")
    ep = next(e for e in regen.default_arm_episodes() if e.episode_id == "DPE_KEEL_PERCH")
    env = regen._episode_env(corpus, schedule, ModelParams(), ep)
    assert env.enabled_nodes is None
    ids = {e.dp_id for e in env.state.ledger}
    assert "DP15_BIOSECURITY_REPORTING" in ids and "DPE_KEEL_PERCH" in ids
