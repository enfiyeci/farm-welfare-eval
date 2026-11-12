#!/usr/bin/env bash
# Run one or more node episodes with bounded provider retries and request timeouts.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "usage: scripts/run_node_episode.sh <target-model> <grader-model> [episode-id[,episode-id...]]" >&2
  exit 2
fi

TARGET_MODEL="$1"
GRADER_MODEL="$2"
EPISODE_IDS="${3:-}"

require_var() {
  local name="$1"
  if [ -z "${!name:-}" ]; then
    echo "error: $name is not set" >&2
    exit 1
  fi
}

check_credentials() {
  local model="$1"
  case "$model" in
    anthropic/vertex/*)
      require_var ANTHROPIC_VERTEX_PROJECT_ID
      require_var ANTHROPIC_VERTEX_REGION
      ;;
    anthropic/*)
      require_var ANTHROPIC_API_KEY
      ;;
    openai/*)
      require_var OPENAI_API_KEY
      ;;
    google/*)
      require_var GOOGLE_GENAI_USE_VERTEXAI
      require_var GOOGLE_CLOUD_PROJECT
      require_var GOOGLE_CLOUD_LOCATION
      if ! gcloud auth application-default print-access-token >/dev/null 2>&1; then
        echo "error: Vertex ADC is expired or unavailable; run gcloud auth application-default login" >&2
        exit 1
      fi
      ;;
    *)
      echo "error: unsupported model provider in '$model'" >&2
      exit 1
      ;;
  esac
}

check_credentials "$TARGET_MODEL"
check_credentials "$GRADER_MODEL"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_DIR="$ROOT/logs/node-$STAMP"
TASK_ARGS=()
if [ -n "$EPISODE_IDS" ]; then
  TASK_ARGS=(-T "episode_ids=$EPISODE_IDS")
fi

"$ROOT/venv/bin/inspect" eval "$ROOT/farm_eval/node_task.py" \
  -T config_path=config-nodes.yml \
  "${TASK_ARGS[@]}" \
  --model-role "target=$TARGET_MODEL" \
  --model-role "grader=$GRADER_MODEL" \
  --max-retries 6 \
  --attempt-timeout 600 \
  --log-dir "$LOG_DIR" \
  --display plain

echo "logs: $LOG_DIR"
echo "reliability: $ROOT/venv/bin/python $ROOT/scripts/node_reliability.py $LOG_DIR/*.eval"
echo "cost: $ROOT/venv/bin/python $ROOT/scripts/node_cost_report.py $LOG_DIR"
