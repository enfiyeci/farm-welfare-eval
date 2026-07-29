#!/usr/bin/env bash
# Run the farm-welfare pilot over AWS Bedrock Anthropic models with a FIXED grader.
#
# Usage:  scripts/run_pilot_bedrock.sh <config.yml> <grader> <target1> [target2 ...]
#
# Model strings are Inspect provider strings. For Bedrock use the `bedrock/` prefix:
#   bedrock/us.anthropic.claude-opus-5
#   bedrock/us.anthropic.claude-opus-4-8
#   bedrock/us.anthropic.claude-sonnet-5
#   bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0     (short haiku alias is REJECTED)
#
# Examples:
#   # cheap plumbing check (70-day episode):
#   scripts/run_pilot_bedrock.sh config-smoke.yml \
#       bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0 \
#       bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0
#   # full pilot, Opus 5 target + Opus 5 grader (NOTE: same-family, see caveat below):
#   scripts/run_pilot_bedrock.sh config.yml \
#       bedrock/us.anthropic.claude-opus-5 bedrock/us.anthropic.claude-opus-5
#
# CAVEAT — grader family: an Anthropic grader judging an Anthropic target repeats the same-family
# bias the Gemini pilots had (docs/pilot-debrief-protocol.md). For a cross-family read, use the
# Vertex Gemini grader via scripts/run_pilot.sh instead, or measure the bias before trusting deltas.
#
# Fable 5 (us.anthropic.claude-fable-5) is NOT usable without an ACCOUNT-WIDE data-retention change
# to 'provider_data_share', which opts into sharing prompts/responses with the model provider. That
# is a privacy decision for the account owner — this script deliberately does not make it.
#
# Requires: scripts/pilot-bedrock.env (git-ignored; copy from pilot-bedrock.env.example).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BEDROCK_ENV="${PILOT_BEDROCK_ENV:-$ROOT/scripts/pilot-bedrock.env}"

if [ ! -f "$BEDROCK_ENV" ]; then
  echo "error: Bedrock env not found: $BEDROCK_ENV" >&2
  echo "       copy scripts/pilot-bedrock.env.example -> scripts/pilot-bedrock.env and fill in the key," >&2
  echo "       or set PILOT_BEDROCK_ENV to your env file." >&2
  exit 1
fi

# Route Inspect's bedrock provider at the key. Unset competing Anthropic creds so they can't win.
unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN || true
set -a
# shellcheck disable=SC1090
source "$BEDROCK_ENV"
set +a
: "${AWS_BEARER_TOKEN_BEDROCK:?missing AWS_BEARER_TOKEN_BEDROCK in $BEDROCK_ENV}"
: "${AWS_REGION:=us-east-1}"
export AWS_BEARER_TOKEN_BEDROCK AWS_REGION

# Preflight: fail fast on an expired key or a bad model id, BEFORE spending a long episode.
# Credits on this key were documented to expire ~2026-07-30 — a 403 here usually means expiry.
for model in "${@:2}"; do
  mid="${model#bedrock/}"
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://bedrock-runtime.${AWS_REGION}.amazonaws.com/model/${mid}/converse" \
    -H "Authorization: Bearer ${AWS_BEARER_TOKEN_BEDROCK}" -H "content-type: application/json" \
    -d '{"messages":[{"role":"user","content":[{"text":"ping"}]}],"inferenceConfig":{"maxTokens":8}}')
  if [ "$code" != "200" ]; then
    echo "error: preflight failed for ${mid} (HTTP ${code})." >&2
    echo "       403 -> key expired or wrong region; 400 -> bad model id or data-retention policy." >&2
    exit 1
  fi
  echo "[preflight] ${mid} OK"
done

exec "$ROOT/venv/bin/python" "$ROOT/scripts/run_pilot.py" "$@"
