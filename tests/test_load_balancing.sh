#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://localhost:8080"

echo "Checking Nginx health endpoint..."

for attempt in $(seq 1 30); do
    if curl --silent --fail "$BASE_URL/health" >/dev/null; then
        break
    fi
    if [ "$attempt" -eq 30 ]; then
        echo "ERROR: API did not become healthy"
        exit 1
    fi
    sleep 2
done

curl --fail --silent "$BASE_URL/health"
echo

echo "Sending requests through Nginx..."
responses="$(mktemp)"
trap 'rm -f "$responses"' EXIT

for i in $(seq 1 20); do
    curl --silent --show-error --fail "$BASE_URL/" \
        | python -c 'import json,sys; print(json.load(sys.stdin)["instance"])' \
        >> "$responses"
done

cat "$responses"

grep -q '^api-replica-1$' "$responses" || {
    echo "ERROR: api-replica-1 did not respond"
    exit 1
}

grep -q '^api-replica-2$' "$responses" || {
    echo "ERROR: api-replica-2 did not respond"
    exit 1
}

echo "PASS: Both API replicas received requests."