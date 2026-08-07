"""Shared feed comparator: normalize the volatile parts of a feed, then compare byte-for-byte.

Two feeds of the SAME episode must be identical -- the Task-4 golden compares a freshly
extracted feed against a committed one, and the Task-5 parity test compares the live emitter's
feed against the one extracted from the `.eval` the same run wrote. Neither comparison can be
literal: three things legitimately differ between two runs of the same deterministic episode.

1. **Run and sample identifiers** -- Inspect mints a fresh `run_id` per eval and a fresh sample
   `uuid` per sample. They appear in the `run_meta` line AND in the feed's path
   (`<out_dir>/<run_id>/<sample_uuid>/feed.ndjson`), so both are normalized to `RUN` / `SAMPLE`
   in line contents (`normalize_feed_lines`) and in paths (`normalize_feed_path`).
2. **Message ids** -- assistant message ids and tool-call ids are freshly generated per run
   (`AssistantText.msg_id` / `ToolCallEvent.msg_id`), so they are renumbered `MSG_0`, `MSG_1`, ...
   in order of first appearance. Renumbering rather than blanking keeps the join meaningful: a
   tool call and the turn it belongs to still share an id after normalization.
3. **Wall-clock timings** -- `run_health` lines are dropped entirely (they carry `wallclock_s`,
   and their every-10th-turn cadence makes them the only lines whose content is timing-derived),
   and any `_WALLCLOCK_FIELDS` key is dropped from every other line as a defense against a later
   event type gaining one.

Normalization is idempotent, so a golden may be stored either raw or already normalized (the
committed one is normalized, which keeps its diff readable across regenerations).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from farm_eval.spectator.events import parse_feed_line

#: Feed line kinds dropped before comparison (wall-clock dependent -- see the module docstring).
EXCLUDED_KINDS = frozenset({"run_health"})

#: Fields dropped from every retained line (belt-and-braces: today they live only on run_health).
_WALLCLOCK_FIELDS = frozenset({"wallclock_s"})

RUN_PLACEHOLDER = "RUN"
SAMPLE_PLACEHOLDER = "SAMPLE"
_MSG_PREFIX = "MSG_"


def _objects(lines: Iterable[str]) -> list[dict[str, Any]]:
    """Parsed feed lines, validated against the feed schema first.

    Validation is not optional: an unparseable or schema-drifted feed must fail here rather than
    silently compare equal as text.
    """
    raw = [line for line in (line.strip() for line in lines) if line]
    for line in raw:
        parse_feed_line(line)
    return [json.loads(line) for line in raw]


def _volatile_ids(objects: list[dict[str, Any]]) -> tuple[set[str], set[str]]:
    """The run ids and sample ids named by the feed's own `run_meta` line(s)."""
    run_ids: set[str] = set()
    sample_ids: set[str] = set()
    for obj in objects:
        if obj.get("kind") == "run_meta":
            run_ids.add(str(obj["run_id"]))
            sample_ids.add(str(obj["sample_id"]))
    return run_ids, sample_ids


def _replace_ids(text: str, run_ids: Iterable[str], sample_ids: Iterable[str]) -> str:
    # Longest first so the result never depends on set iteration order.
    for sample_id in sorted(sample_ids, key=len, reverse=True):
        if sample_id:
            text = text.replace(sample_id, SAMPLE_PLACEHOLDER)
    for run_id in sorted(run_ids, key=len, reverse=True):
        if run_id:
            text = text.replace(run_id, RUN_PLACEHOLDER)
    return text


def normalize_feed_lines(lines: Iterable[str]) -> list[str]:
    """Normalized, comparable NDJSON lines: volatile ids replaced, wall-clock data dropped."""
    objects = _objects(lines)
    run_ids, sample_ids = _volatile_ids(objects)
    msg_ids: dict[str, str] = {}
    out: list[str] = []
    for obj in objects:
        if obj.get("kind") in EXCLUDED_KINDS:
            continue
        for field in _WALLCLOCK_FIELDS:
            obj.pop(field, None)
        msg_id = obj.get("msg_id")
        if isinstance(msg_id, str) and msg_id:
            obj["msg_id"] = msg_ids.setdefault(msg_id, f"{_MSG_PREFIX}{len(msg_ids)}")
        line = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        out.append(_replace_ids(line, run_ids, sample_ids))
    return out


def normalize_feed_file(path: Path) -> list[str]:
    """`normalize_feed_lines` over a feed file's contents."""
    return normalize_feed_lines(path.read_text(encoding="utf-8").splitlines())


def normalize_feed_path(path: Path) -> str:
    """The feed's `<run_id>/<sample_uuid>/feed.ndjson` tail, with both ids normalized.

    The extractor encodes both volatile identifiers in the path, so comparing where two feeds
    were written needs the same normalization their contents get. The ids come from the file's
    own `run_meta` line, which is where the extractor took the path components from.
    """
    run_ids, sample_ids = _volatile_ids(
        _objects(path.read_text(encoding="utf-8").splitlines())
    )
    return _replace_ids("/".join(path.resolve().parts[-3:]), run_ids, sample_ids)


def assert_feeds_match(actual: Path, expected: Path) -> None:
    """Fail with a readable first-difference report when two feeds differ after normalization."""
    got, want = normalize_feed_file(actual), normalize_feed_file(expected)
    if got == want:
        return
    for index, (a, b) in enumerate(zip(got, want)):
        if a != b:
            raise AssertionError(
                f"feed mismatch at normalized line {index}:\n"
                f"  actual   ({actual}): {a}\n"
                f"  expected ({expected}): {b}"
            )
    raise AssertionError(
        f"feed length mismatch: {actual} has {len(got)} normalized lines, "
        f"{expected} has {len(want)}"
    )
