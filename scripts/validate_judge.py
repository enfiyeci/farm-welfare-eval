"""Judge-validation runner (the spec §15/§16 credibility gate).

Pairs filled label sheets (from scripts/make_label_sheets.py) with the judge's scores in the
stored `.eval` logs and reports Spearman rho per node and per dimension against the
0.75-0.86 target band. Logs must be scored by the CURRENT judge — re-score stale logs with
`inspect score <log>` first. See docs/judge-validation.md.

Usage:
    ./venv/bin/python scripts/validate_judge.py --logs <dir-or-.eval> --labels <dir> \\
        [--out validation-report.md]
"""

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.judge.validation_harness import (  # noqa: E402
    extract_sample_record,
    load_filled_sheet,
    render_report,
    validation_result,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logs", required=True, help=".eval file or a directory of them")
    parser.add_argument("--labels", required=True, help="directory of FILLED label sheets (*.yml)")
    parser.add_argument("--out", default=None, help="write the markdown report here (also printed)")
    args = parser.parse_args()

    from inspect_ai.log import read_eval_log

    logs_path = pathlib.Path(args.logs)
    log_files = sorted(logs_path.glob("*.eval")) if logs_path.is_dir() else [logs_path]
    if not log_files:
        sys.exit(f"no .eval logs under {logs_path}")
    records = []
    for log_file in log_files:
        log = read_eval_log(str(log_file))
        for sample in log.samples or []:
            records.append(extract_sample_record(sample, log_file.name))

    label_files = sorted(pathlib.Path(args.labels).glob("*.yml"))
    if not label_files:
        sys.exit(f"no *.yml label sheets under {args.labels}")
    sheets = [load_filled_sheet(p) for p in label_files]

    report = render_report(validation_result(records, sheets))
    print(report)
    if args.out:
        pathlib.Path(args.out).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
