"""P8 — write the committed spacing-audit report over the real schedule.

Usage: ./venv/bin/python scripts/audit_schedule.py [--out evals/hen/nodes/schedule-spacing-report.md]
"""

import argparse
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.env.loader import load_schedule  # noqa: E402
from farm_eval.probe.schedule_audit import audit_schedule, render_schedule_report  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(ROOT / "evals" / "hen" / "nodes" / "schedule-spacing-report.md"))
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / "config.yml").read_text(encoding="utf-8"))
    end_day = config["episode_end_day"]
    report = render_schedule_report(audit_schedule(load_schedule(ROOT / "schedule"), end_day=end_day))
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
