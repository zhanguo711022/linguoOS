#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://localhost:8000}

start=$(curl -s -X POST "$BASE_URL/api/v1/session/start" -H "Content-Type: application/json" -d '{"user_id":"test-user","language":"en"}')

session_id=$(python - <<'PY'
import json,sys
payload=json.loads(sys.stdin.read())
print(payload.get("session_id") or payload.get("data",{}).get("session_id",""))
PY
<<< "$start")

if [ -z "$session_id" ]; then
  echo "Failed to start session"
  echo "$start"
  exit 1
fi

practice=$(curl -s "$BASE_URL/api/v1/practice/next?session_id=$session_id&module_id=grammar")

prompt=$(python - <<'PY'
import json,sys
payload=json.loads(sys.stdin.read())
print(payload.get("prompt",""))
PY
<<< "$practice")

expected=$(python - <<'PY'
import json,sys
payload=json.loads(sys.stdin.read())
print(payload.get("expected_answer",""))
PY
<<< "$practice")

submit=$(curl -s -X POST "$BASE_URL/api/v1/practice/submit" -H "Content-Type: application/json" -d "{\"session_id\":\"$session_id\",\"prompt\":\"$prompt\",\"answer\":\"$expected\",\"expected_answer\":\"$expected\"}")

echo "Session: $session_id"
echo "Practice: $practice"
echo "Submit: $submit"
