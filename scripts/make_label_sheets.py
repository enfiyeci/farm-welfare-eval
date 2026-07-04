"""Generate BLIND judge-validation labeling sheets from a stored `.eval` log.

One YAML sheet per sample. Hand the sheets to the labeler (vet/welfare expert for the real
spec §15 gate; a proxy labeler only exercises the pipeline); they fill `labeler`,
`labeler_kind`, and every `score:` cell (0-10), then `scripts/validate_judge.py` pairs the
filled sheets back against the logs. See docs/judge-validation.md.

Usage:
    ./venv/bin/python scripts/make_label_sheets.py <log.eval> <out_dir> \\
        [--schedule schedule] [--dimensions judge/dimensions]
"""

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.judge.validation_harness import write_label_sheets  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", help="stored .eval log (scored by the CURRENT judge)")
    parser.add_argument("out_dir", help="directory for the blind label sheets")
    parser.add_argument("--schedule", default=str(ROOT / "schedule"))
    parser.add_argument("--dimensions", default=str(ROOT / "judge" / "dimensions"))
    args = parser.parse_args()
    paths = write_label_sheets(args.log, args.out_dir, args.schedule, args.dimensions)
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
