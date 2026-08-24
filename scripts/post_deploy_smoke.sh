#!/usr/bin/env bash
set -euo pipefail

TARGET_URL="${1:-http://localhost:8080}"
echo "Running post-deployment smoke probe against: $TARGET_URL"

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET_URL/api/v1/health/ready" || echo "000")

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "[SUCCESS] Health check returned HTTP 200 Ready."
    exit 0
else
    echo "[ERROR] Health probe failed with HTTP status $HTTP_STATUS"
    exit 1
fi

