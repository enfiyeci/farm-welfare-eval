#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from farm_eval.analysis.model import BehaviourModel
from farm_eval.report.analyze import analyze
from farm_eval.report.extract import extract
from farm_eval.report.history import history_row, load_history, update_history
from farm_eval.report.render import render


HISTORY_PATH = REPO_ROOT / "docs/probes/pilot-history.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a self-contained HTML report from an Inspect .eval log.")
    parser.add_argument("eval_log", type=Path, help="current .eval log")
    parser.add_argument("--vs", dest="prior_logs", type=Path, nargs="+", default=[], metavar="PRIOR.eval", help="one or more prior logs for paired comparison")
    parser.add_argument("--narrative", type=Path, help="markdown sidecar with named narrative sections")
    parser.add_argument("--behaviour", type=Path, metavar="BEHAVIOUR_MODEL.json", help="behaviour model JSON; adds the off-node, per-tool and per-node behaviour layers")
    parser.add_argument("--out", type=Path, help="output HTML path (default: beside the current log)")
    parser.add_argument("--no-history-write", action="store_true", help="render without updating docs/probes/pilot-history.json")
    return parser


def _load_behaviour(path: Path, eval_log: Path) -> BehaviourModel:
    """The behaviour model at *path*, refused unless it was built from *eval_log*.

    A behaviour model records the sha256 of the log it analysed, and `report.extract` hashes the
    log file the same way -- so the two are directly comparable and there is no reason to accept a
    pairing that does not hold. Rendering a mismatched pair produces a report whose scores and
    whose behaviour layer describe DIFFERENT runs, with nothing on the page to say so: every
    `msg_N` pointer, day and finding would be silently attached to the wrong episode. Refusing is
    the only safe answer, and the error names both hashes and both files so the caller can see
    which of the two arguments is the stale one.
    """
    behaviour = BehaviourModel.model_validate_json(path.read_text())
    actual = hashlib.sha256(eval_log.expanduser().resolve().read_bytes()).hexdigest()
    if behaviour.source_sha256 != actual:
        raise SystemExit(
            f"--behaviour {path} was built from a different log: it records source_sha256 "
            f"{behaviour.source_sha256}, but {eval_log} hashes to {actual}. Rebuild the behaviour "
            "model from this log (scripts/behaviour_report.py) or point --behaviour at the model "
            "for the log it was built from."
        )
    return behaviour


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    current = extract(args.eval_log)
    priors = [extract(path) for path in args.prior_logs]
    derived = analyze(current, priors=priors)
    narrative = args.narrative.read_text() if args.narrative else None
    behaviour = _load_behaviour(args.behaviour, args.eval_log) if args.behaviour else None

    if args.no_history_write:
        history = load_history(HISTORY_PATH)
    else:
        history = load_history(HISTORY_PATH)
        for model in [*priors, current]:
            history = update_history(HISTORY_PATH, history_row(model))

    output_path = (args.out or args.eval_log.with_suffix(".html")).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render(current, derived, narrative=narrative, history=history, behaviour=behaviour))
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
