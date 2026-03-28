#!/usr/bin/env bash
set -euo pipefail

BASE=${BASE:-http://127.0.0.1:8000}
MODULE_ID=${MODULE_ID:-precision.generalization}
USER_ID=${USER_ID:-demo}

jq_cmd() { command -v jq >/dev/null 2>&1; }

echo "[verify] BASE=$BASE"

step() {
  echo
  echo "==> $1"
}

pp() {
  if jq_cmd; then jq .; else cat; fi
}

step "1) system/health"
curl -fsS "$BASE/api/v1/system/health" | pp

step "2) workspace/context"
curl -fsS "$BASE/api/v1/workspace/context" | pp

step "3) decision(first => practice)"
curl -fsS -X POST "$BASE/api/v1/decision/next" \
  -H 'Content-Type: application/json' \
  -d "{\"user_id\":\"$USER_ID\",\"module_id\":\"$MODULE_ID\",\"last_mode\":null,\"last_correct\":null}" | pp

step "4) practice/next"
curl -fsS "$BASE/api/v1/practice/next?module_id=$MODULE_ID" | pp

step "5) practice/submit (wrong)"
curl -fsS -X POST "$BASE/api/v1/practice/submit" \
  -H 'Content-Type: application/json' \
  -d "{\"user_id\":\"$USER_ID\",\"input_type\":\"text\",\"payload\":{\"content\":\"Students often learn much faster.\"},\"client_context\":{\"client_type\":\"script\",\"workspace_mode\":\"practice\",\"timestamp\":1730000000}}" | pp

step "6) decision(after wrong => explain)"
curl -fsS -X POST "$BASE/api/v1/decision/next" \
  -H 'Content-Type: application/json' \
  -d "{\"user_id\":\"$USER_ID\",\"module_id\":\"$MODULE_ID\",\"last_mode\":\"practice\",\"last_correct\":false}" | pp

step "7) explain/concept"
curl -fsS "$BASE/api/v1/explain/concept?module_id=$MODULE_ID" | pp

step "8) system/status"
curl -fsS "$BASE/api/v1/system/status" | pp

step "9) system/metrics"
curl -fsS "$BASE/api/v1/system/metrics" | pp

step "10) system/events/recent"
curl -fsS "$BASE/api/v1/system/events/recent?limit=10" | pp

step "11) history/recent"
curl -fsS "$BASE/api/v1/history/recent?user_id=$USER_ID" | pp

echo
echo "[verify] OK"
