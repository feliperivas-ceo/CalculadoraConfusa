#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:5000}"

curl --fail --silent "${BASE_URL}/health" > /dev/null
curl --fail --silent -X POST "${BASE_URL}/suma" \
  -H 'Content-Type: application/json' \
  -d '{"num1":"1/2","num2":"3/4"}' | grep -q '"resultado":"5/4"'
curl --fail --silent -X POST "${BASE_URL}/divide" \
  -H 'Content-Type: application/json' \
  -d '{"num1":"5","num2":"0"}' -o /dev/null -w '%{http_code}' | grep -q '^400$'

echo "Endpoint checks passed"