#!/usr/bin/env python3
"""The behaviour-report CLI (design §4): one finished `.eval` in, one behaviour model out.

    ./venv/bin/python scripts/behaviour_report.py <log.eval> [--out DIR] \
        [--reader off|candidates|sweep] [--reader-model NAME] [--json-only]

Everything the analysis stack does already lives behind two seams -- `build_behaviour_model` for
the mechanical model and `farm_eval.report.render` for the HTML -- so this file is deliberately
only wiring. Three choices in it are not arbitrary:

- **The reader never runs unless asked.** `--reader off` is the default because the reader is the
  one stage that spends real grader tokens; a diagnostic tool that quietly bills the caller for
  reading a 500-day log is not a tool anyone can run twice.
- **`--reader-model` defaults to the log's own recorded grader** (`run.grader_model`), not to a
  role lookup. The reader is an offline pass over a FINISHED log, so there is no live role
  configuration to inherit; the log's grader is simply the best-documented default, and it stays
  overridable.
- **The pilot history is read, never written.** `scripts/gen_pilot_report.py` owns appending a run
  to `docs/probes/pilot-history.json` -- that file is the trend chart's record of real runs, and a
  behaviour re-analysis of an old log is not a new run.
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from farm_eval.analysis.build import build_behaviour_model
from farm_eval.analysis.reader import read_behaviour
from farm_eval.report.analyze import analyze
from farm_eval.report.extract import extract
from farm_eval.report.history import load_history
from farm_eval.report.render import render

HISTORY_PATH = REPO_ROOT / "docs/probes/pilot-history.json"

JSON_NAME = "behaviour_model.json"
HTML_NAME = "behaviour_report.html"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the behaviour model for a finished .eval log (and render its report)."
    )
    parser.add_argument("eval_log", type=Path, help="the finished .eval log to analyse")
    parser.add_argument(
        "--out", type=Path, help=f"output directory for {JSON_NAME} (default: beside the log)"
    )
    parser.add_argument(
        "--reader",
        choices=["off", "candidates", "sweep"],
        default="off",
        help="LLM reader pass; costs real tokens, so it is off unless asked for (default: off)",
    )
    parser.add_argument(
        "--reader-model",
        metavar="NAME",
        help="model for the reader pass (default: the log's recorded grader model)",
    )
    parser.add_argument(
        "--json-only", action="store_true", help=f"write {JSON_NAME} without rendering the HTML"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    log_path = args.eval_log
    behaviour = build_behaviour_model(log_path)

    # The report model carries the transcript the reader quotes from and the grader the reader
    # defaults to, so it is needed for either of those two jobs -- and for nothing else.
    needs_report_model = args.reader != "off" or not args.json_only
    report_model = extract(log_path) if needs_report_model else None

    if args.reader != "off":
        reader_model = args.reader_model or report_model["run"]["grader_model"]
        if not reader_model:
            raise SystemExit(
                "--reader needs a model: this log records no grader, so pass --reader-model"
            )
        behaviour.reader_verdicts.extend(
            asyncio.run(
                read_behaviour(
                    behaviour,
                    report_model["transcript"],
                    reader_model=reader_model,
                    mode=args.reader,
                )
            )
        )

    out_dir = (args.out or Path(log_path).parent).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / JSON_NAME
    json_path.write_text(behaviour.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print(json_path)

    if not args.json_only:
        html_path = out_dir / HTML_NAME
        html_path.write_text(
            render(
                report_model,
                analyze(report_model),
                history=load_history(HISTORY_PATH),
                behaviour=behaviour,
            ),
            encoding="utf-8",
        )
        print(html_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
