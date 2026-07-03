#!/usr/bin/env bash
# Run the farm-welfare pilot over Vertex Gemini target(s) with a FIXED grader.
#
# Usage:  scripts/run_pilot.sh <config.yml> <grader> <target1> [target2 ...]
#
# Examples:
#   # cheap plumbing check (truncated episode, Flash, ~pennies):
#   scripts/run_pilot.sh config-smoke.yml google/gemini-2.5-flash google/gemini-2.5-flash
#   # real single-model pilot (full 17-month episode, Pro target + Pro grader, ~$10-20):
#   scripts/run_pilot.sh config.yml google/gemini-2.5-pro google/gemini-2.5-pro
#   # sweep two targets, fixed Pro grader:
#   scripts/run_pilot.sh config.yml google/gemini-2.5-pro google/gemini-2.5-flash google/gemini-2.5-pro
#
# Requires: Vertex ADC (run once: `gcloud auth application-default login`) and a Vertex env file.
# Point PILOT_VERTEX_ENV at your Vertex config (see scripts/pilot-vertex.env.example); it defaults
# to scripts/pilot-vertex.env (git-ignored) if present.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERTEX_ENV="${PILOT_VERTEX_ENV:-$ROOT/scripts/pilot-vertex.env}"

if [ ! -f "$VERTEX_ENV" ]; then
  echo "error: Vertex env not found: $VERTEX_ENV" >&2
  echo "       copy scripts/pilot-vertex.env.example -> scripts/pilot-vertex.env and fill in your project," >&2
  echo "       or set PILOT_VERTEX_ENV to your env file." >&2
  exit 1
fi

# Route the google-genai SDK at Vertex + your project. Unset any AI-Studio key so it can't win.
unset GOOGLE_API_KEY || true
set -a
# shellcheck disable=SC1090
source "$VERTEX_ENV"
set +a
export PATH="/opt/homebrew/bin:$PATH"   # ensure gcloud (ADC auth) is on PATH

if ! gcloud auth application-default print-access-token >/dev/null 2>&1; then
  echo "error: Vertex ADC is expired/invalid — run: gcloud auth application-default login" >&2
  exit 1
fi

exec "$ROOT/venv/bin/python" "$ROOT/scripts/run_pilot.py" "$@"
