#!/usr/bin/env bash
set -euo pipefail

bundle_name="linguoos_backend_bundle.tar.gz"
tar -czf "$bundle_name" linguoos requirements.txt Dockerfile .env.example README.md

echo "Created $bundle_name"
