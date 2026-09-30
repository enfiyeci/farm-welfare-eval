"""Anchor a task config's relative paths to the repo root.

Inspect chdirs into the task file's directory (farm_eval/) while loading AND running a file-based
task, so a relative `config_path` -- and the relative corpus/schedule/prompt paths inside the
config -- must be anchored to the repo root, not the cwd. Absolute paths pass through untouched.
Shared by `farm_eval/node_task.py` and `farm_eval/farm_task.py` (D4).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent


def from_root(path: str | Path) -> str:
    p = Path(path)
    return str(p if p.is_absolute() else REPO_ROOT / p)


def anchor_paths(cfg: dict, keys: Iterable[str]) -> dict:
    """A copy of `cfg` with every present, non-empty `keys` entry anchored via `from_root`."""
    out = dict(cfg)
    for key in keys:
        if out.get(key):
            out[key] = from_root(out[key])
    return out
