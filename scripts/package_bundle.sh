#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DIST_DIR="$ROOT_DIR/dist"

mkdir -p "$DIST_DIR"

VERSION=${VERSION:-${GITHUB_REF_NAME:-dev}}
TS=$(date -u +%Y%m%dT%H%M%SZ)
BASENAME="linguoos-${VERSION}-${TS}"

echo "[package] root=$ROOT_DIR"
echo "[package] dist=$DIST_DIR"

# Source bundle (code + requirements + Dockerfile + docs)
SRC_ZIP="$DIST_DIR/${BASENAME}-src.zip"
rm -f "$SRC_ZIP"
(
  cd "$ROOT_DIR"
  zip -r "$SRC_ZIP" \
    linguoos \
    requirements.txt \
    Dockerfile \
    README.md \
    HANDOFF.md \
    TASKS.md \
    .github/workflows/release.yml \
    -x "**/__pycache__/*" "**/*.pyc" "**/.DS_Store"
)

echo "[package] wrote $SRC_ZIP"

# Scripts bundle
SCRIPTS_ZIP="$DIST_DIR/${BASENAME}-scripts.zip"
rm -f "$SCRIPTS_ZIP"
(
  cd "$ROOT_DIR"
  zip -r "$SCRIPTS_ZIP" scripts \
    -x "**/__pycache__/*" "**/*.pyc" "**/.DS_Store"
)

echo "[package] wrote $SCRIPTS_ZIP"

echo "[package] done"
