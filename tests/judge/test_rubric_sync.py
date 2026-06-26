"""Guard: the generated reference rubric (farm_eval/judge/rubric.yml) must not drift from the
AUTHORITATIVE judge dimension files (judge/dimensions/*.md) that the scorer actually loads.

build-rubric.mjs generates the rubric's `dimensions:` block FROM the .md files, so a mismatch here
means a committed rubric.yml is stale — rerun `node docs/build-rubric.mjs`. Skips when the (untracked)
reference artifact has not been generated.
"""

from pathlib import Path

import pytest
import yaml

from farm_eval.judge.dimensions import load_dimensions

REPO_ROOT = Path(__file__).resolve().parents[2]
DIMS_DIR = REPO_ROOT / "judge" / "dimensions"
RUBRIC = REPO_ROOT / "farm_eval" / "judge" / "rubric.yml"


@pytest.mark.skipif(not RUBRIC.exists(), reason="reference rubric.yml not generated (run docs/build-rubric.mjs)")
def test_rubric_dimensions_match_loaded_judge_dimensions():
    loaded = {d.id: d for d in load_dimensions(DIMS_DIR)}
    doc = yaml.safe_load(RUBRIC.read_text(encoding="utf-8"))
    ref = {d["id"]: d for d in doc.get("dimensions", [])}

    assert set(ref) == set(loaded), (
        "rubric.yml dimensions drifted from judge/dimensions/*.md — rerun `node docs/build-rubric.mjs`. "
        f"only-in-rubric={sorted(set(ref) - set(loaded))} only-in-dims={sorted(set(loaded) - set(ref))}"
    )
    for dim_id, dim in loaded.items():
        r = ref[dim_id]
        assert float(r["weight"]) == float(dim.weight), f"{dim_id}: weight drift {r['weight']} != {dim.weight}"
        assert bool(r.get("tripwire", False)) == bool(dim.tripwire), f"{dim_id}: tripwire drift"
        assert tuple(r["scale"]) == tuple(dim.scale), f"{dim_id}: scale drift {r['scale']} != {list(dim.scale)}"
        assert r["group"] == dim.group, f"{dim_id}: group drift {r['group']!r} != {dim.group!r}"
        # `headline` is the derived "contributes to the weighted welfare headline" flag.
        assert bool(r["headline"]) == (dim.weight > 0), f"{dim_id}: headline flag inconsistent with weight"
