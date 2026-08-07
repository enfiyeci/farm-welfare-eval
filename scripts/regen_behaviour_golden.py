# Regenerate the behaviour-model golden: ./venv/bin/python scripts/regen_behaviour_golden.py
"""Deterministic generator for the behaviour-model golden (`tests/analysis/goldens/behaviour_model.json`).

Runs the SAME scripted keyless `mockllm` episode the spectator golden uses -- `run_episode` is
imported from `scripts/regen_spectator_golden.py` rather than re-scripted, so the two goldens can
never describe different runs -- and builds the behaviour model from the resulting `.eval` log.

`build_golden_model` / `normalize_model` are imported by `tests/analysis/test_build.py`, which is
what makes the test and the golden the same episode by construction (the same arrangement
`tests/spectator/test_extract.py` uses with the spectator golden).

The golden is stored NORMALIZED: `source_sha256` is the hash of the `.eval` file itself, which
Inspect re-mints on every run (fresh run id, sample uuid, timestamps), so a raw golden would churn
on every regeneration even when the behaviour model is unchanged. Everything else in the model is
already run-independent -- `msg_N` ids are positional, days and costs come from the deterministic
env core -- and that is exactly what the golden is here to keep true.
"""

from __future__ import annotations

import pathlib as _pathlib
import sys as _sys

_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent.parent))

import json
import tempfile
from pathlib import Path

from farm_eval.analysis.build import build_behaviour_model
from farm_eval.analysis.model import BehaviourModel
from scripts.regen_spectator_golden import run_episode

_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_PATH = _ROOT / "tests" / "analysis" / "goldens" / "behaviour_model.json"

#: Stand-in for the per-run `.eval` file hash. Not a real hash of anything.
PLACEHOLDER_SHA256 = "0" * 64


def normalize_model(model: BehaviourModel) -> dict:
    """The model as JSON-safe data, with the per-run source hash replaced by a fixed placeholder."""
    data = model.model_dump(mode="json")
    data["source_sha256"] = PLACEHOLDER_SHA256
    return data


def build_golden_model(work_dir: Path) -> tuple[str, BehaviourModel]:
    """Run the scripted episode under *work_dir* and build its behaviour model.

    Returns the log location alongside the model, so a test can re-run the builder over the same
    log (with a stage doctored) without paying for a second episode.
    """
    log = run_episode(work_dir / "logs")
    return log.location, build_behaviour_model(log.location)


def main() -> None:
    print("Generating the behaviour-model golden…")
    with tempfile.TemporaryDirectory() as tmp:
        _, model = build_golden_model(Path(tmp))
    data = normalize_model(model)
    GOLDEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    existed = GOLDEN_PATH.exists()
    GOLDEN_PATH.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  {'rewrote' if existed else 'wrote'} {GOLDEN_PATH.relative_to(_ROOT)}")
    print(f"  fidelity={data['feed_fidelity']} day_map_valid={data['day_map_valid']}")
    print(f"  dossiers={len(data['dossiers'])} tool_profiles={len(data['tool_profiles'])} "
          f"findings={len(data['offnode_findings'])} digest_days={len(data['digest'])}")


if __name__ == "__main__":
    main()
