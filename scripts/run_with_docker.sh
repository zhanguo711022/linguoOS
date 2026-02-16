#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME=${IMAGE_NAME:-linguoos:local}
PORT=${PORT:-8000}

echo "[linguoos] build docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" .

echo "[linguoos] run: http://127.0.0.1:${PORT}/ui"
docker run --rm -p "${PORT}:8000" \
  -e LINGUO_PROVIDER=${LINGUO_PROVIDER:-mock} \
  -e LINGUO_REQUIRE_API_KEY=${LINGUO_REQUIRE_API_KEY:-0} \
  -e LINGUO_API_KEY=${LINGUO_API_KEY:-dev-key-123} \
  "$IMAGE_NAME"
