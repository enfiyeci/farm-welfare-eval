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
