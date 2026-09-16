# tests/env/test_node_snapshot_golden.py
"""Every real node episode's starting world is pinned (shape, not full state): regenerate with
`$PY scripts/regen_node_episodes.py --snapshots` and review the diff like any golden change."""
import json
import pathlib

import pytest

from scripts.regen_node_episodes import snapshot_shapes

GOLD = pathlib.Path("tests/fixtures/golden/node_snapshots.json")
pytestmark = pytest.mark.skipif(not pathlib.Path("schedule/node_episodes.yml").is_file(), reason="no real manifest")


def test_node_snapshot_shapes_match_golden():
    expected = json.loads(GOLD.read_text())
    got = snapshot_shapes()
    assert got == expected, "a node episode's starting world drifted — regen + review if intended"
