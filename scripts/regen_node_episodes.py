# Regenerate: $PY scripts/regen_node_episodes.py --snapshots --reference
"""Node-episode goldens: (a) the snapshot SHAPE golden, (b) the per-episode reference anchors.

(a) `snapshot_shapes()` -> tests/fixtures/golden/node_snapshots.json: per default-arm episode, the
    facts a reviewer can read — day, per-house birds, ledger ids, mail counts, digest hash.
(b) `node_reference()` -> farm_eval/judge/node_reference.json (Task 12): good/negligent terminal
    accumulators from each episode's OWN snapshot over its OWN window (D7).

Deterministic (no wall-clock, no RNG); sorted keys; 4-decimal rounding.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from farm_eval.env.loader import load_corpus, load_schedule, validate_body_refs, validate_reply_refs  # noqa: E402
from farm_eval.env.model import ModelParams  # noqa: E402
from farm_eval.env.node_episodes import ResolvedEpisode, expand_episodes, load_node_manifest, validate_manifest  # noqa: E402
from farm_eval.env.snapshot import derive_snapshot  # noqa: E402

_CORPUS = _ROOT / "corpus"
_SCHEDULE = _ROOT / "schedule"
_SNAPSHOT_GOLDEN = _ROOT / "tests" / "fixtures" / "golden" / "node_snapshots.json"
_NODE_REFERENCE = _ROOT / "farm_eval" / "judge" / "node_reference.json"


def _load():
    corpus, schedule = load_corpus(_CORPUS), load_schedule(_SCHEDULE)
    validate_body_refs(schedule, corpus)
    validate_reply_refs(corpus)
    manifest = load_node_manifest(_SCHEDULE)
    validate_manifest(manifest, schedule)
    return corpus, schedule, manifest


def default_arm_episodes() -> list[ResolvedEpisode]:
    corpus, schedule, manifest = _load()
    return [r for r in expand_episodes(manifest, schedule) if r.arm_id == manifest.meta.default_arm]


def _default_arm_episodes(corpus, schedule, manifest) -> list[ResolvedEpisode]:
    """Same filter as `default_arm_episodes()`, reusing already-loaded resources."""
    return [r for r in expand_episodes(manifest, schedule) if r.arm_id == manifest.meta.default_arm]


def snapshot_shapes() -> dict:
    corpus, schedule, manifest = _load()
    out: dict = {}
    for ep in _default_arm_episodes(corpus, schedule, manifest):
        state, digest = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=0)
        out[ep.episode_id] = {
            "start_day": state.day_index,
            "end_day": ep.end_day,
            "sessions": list(ep.sessions),
            "birds": {h: int(n) for h, n in sorted(state.world.bird_count.items())},
            "ledger": [e.dp_id for e in state.ledger],
            "mail_total": len(state.mailbox),
            "mail_unread": sum(1 for m in state.mailbox if m.unread),
            "prelude_actions": len(ep.prelude_actions),
            "digest_sha256": hashlib.sha256(digest.encode("utf-8")).hexdigest()[:16],
        }
    return out


def _write_json(path: pathlib.Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshots", action="store_true")
    ap.add_argument("--reference", action="store_true")
    args = ap.parse_args(argv)
    if not (args.snapshots or args.reference):
        ap.error("pass --snapshots and/or --reference")
    if args.snapshots:
        _write_json(_SNAPSHOT_GOLDEN, snapshot_shapes())
        print(f"wrote {_SNAPSHOT_GOLDEN}")
    if args.reference:
        from scripts.regen_node_episodes_reference import node_reference  # Task 12 adds this module
        # report=True: the pinned window-unsafe drops and any collapsed unread channel print on
        # the DOCUMENTED regeneration path, so a reviewer sees them without running the module.
        _write_json(_NODE_REFERENCE, node_reference(report=True))
        print(f"wrote {_NODE_REFERENCE}")


if __name__ == "__main__":
    main()
