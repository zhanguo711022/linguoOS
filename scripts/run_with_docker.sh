#!/usr/bin/env bash
set -euo pipefail

docker build -t linguoos-backend .
docker run --rm -p 8000:8000 --env-file .env linguoos-backend
