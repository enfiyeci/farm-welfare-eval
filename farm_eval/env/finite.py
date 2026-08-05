"""Deep float walker shared by the ModelParams and EnvState finiteness guards.

Pydantic accepts ``inf``/``-inf``/``nan`` for a ``float`` field by default, and YAML and
Python's ``json`` module can both express them — so every model that ingests outside data
(corpus YAML, config.yml, play autosaves, checkpoints, ``.eval`` logs) needs a construction-
time finiteness check. The walker lives in its own module because both sides need it and
neither may import the other: ``env/model/__init__.py`` imports ``integrate``, which imports
``state``, so ``state.py`` importing anything under ``env.model`` would be a cycle.
"""
from __future__ import annotations

from typing import Any, Iterator

from pydantic import BaseModel


def _floats_in(value: Any, path: str) -> Iterator[tuple[str, float]]:
    """Yield ``(path, value)`` for every float reachable inside one field value.

    Descends lists/tuples, dicts, and nested pydantic models, and stops at anything else.
    Paths read like access expressions: ``welfare.houses['H1'].ammonia_ppm``. ints are
    skipped — an int field cannot hold inf or nan (pydantic refuses the coercion) — and
    bools are ints.
    """
    if isinstance(value, bool):
        return
    if isinstance(value, float):
        yield path, value
    elif isinstance(value, BaseModel):
        for name in type(value).model_fields:
            yield from _floats_in(getattr(value, name), f"{path}.{name}")
    elif isinstance(value, (list, tuple)):
        for i, item in enumerate(value):
            yield from _floats_in(item, f"{path}[{i}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _floats_in(item, f"{path}[{key!r}]")


def iter_model_floats(model: BaseModel) -> Iterator[tuple[str, float]]:
    """Yield ``(path, value)`` for every float reachable from a model's fields."""
    for name in type(model).model_fields:
        yield from _floats_in(getattr(model, name), name)
