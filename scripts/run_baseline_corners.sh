#!/usr/bin/env bash
# Run the four 2x2 welfare x finance corner baselines (docs/future-work.md) SEQUENTIALLY over the
# locked env — one full episode per corner, goal-prefixed briefing per corner.
#
# Usage:  scripts/run_baseline_corners.sh <grader> <target>
# e.g.:   scripts/run_baseline_corners.sh google/gemini-2.5-pro google/gemini-3.1-pro-preview
#
# Sequential ON PURPOSE: parallel full episodes contend for the same Vertex model quota and can
# starve each other's retries. Do not run while another pilot/sweep is in flight, for the same
# reason. Regenerate the corner briefings/configs first if the base briefing or config changed:
#   ./venv/bin/python scripts/gen_corner_briefings.py
#
# Corner runs are EXPERIMENTAL (goal-prefixed briefing) — never comparable-sweep data.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GRADER="${1:?usage: run_baseline_corners.sh <grader> <target>}"
TARGET="${2:?usage: run_baseline_corners.sh <grader> <target>}"

CORNERS=(
  good_welfare_good_finance
  bad_welfare_bad_finance
  good_finance_bad_welfare
  good_welfare_bad_finance
)

# Refuse to spend on stale corners: every generated briefing/config must match a fresh render of
# the CURRENT base briefing + config, or four paid episodes would run against a drifted setup.
"$ROOT/venv/bin/python" "$ROOT/scripts/gen_corner_briefings.py" --check

for corner in "${CORNERS[@]}"; do
  echo ""
  echo "=== corner baseline: $corner ==="
  "$ROOT/scripts/run_pilot.sh" "config-baseline-$corner.yml" "$GRADER" "$TARGET"
done
