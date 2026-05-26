#!/usr/bin/env sh
set -eu

REPO_SLUG=${DOUBLECHECK_REPO_SLUG:-shibata-yosuke/doublecheck}
REPO_REF=${DOUBLECHECK_REPO_REF:-main}
ARCHIVE_PATH=${DOUBLECHECK_ARCHIVE_PATH:-}
ARCHIVE_URL=${DOUBLECHECK_ARCHIVE_URL:-https://codeload.github.com/$REPO_SLUG/tar.gz/$REPO_REF}

if command -v mktemp >/dev/null 2>&1; then
  TMP_DIR=$(mktemp -d)
else
  TMP_DIR="${TMPDIR:-/tmp}/doublecheck.$$"
  mkdir -p "$TMP_DIR"
fi

cleanup() {
  rm -rf "$TMP_DIR"
}

trap cleanup EXIT INT TERM

ARCHIVE_FILE="$TMP_DIR/doublecheck.tar.gz"
EXTRACT_DIR="$TMP_DIR/extracted"

if [ -n "$ARCHIVE_PATH" ]; then
  cp "$ARCHIVE_PATH" "$ARCHIVE_FILE"
else
  if ! command -v curl >/dev/null 2>&1; then
    echo "curl was not found. Install curl before running this installer." >&2
    exit 1
  fi
  curl -fsSL "$ARCHIVE_URL" -o "$ARCHIVE_FILE"
fi

mkdir -p "$EXTRACT_DIR"
tar -xzf "$ARCHIVE_FILE" -C "$EXTRACT_DIR"

if [ -f "$EXTRACT_DIR/install-doublecheck.sh" ]; then
  REPO_DIR="$EXTRACT_DIR"
else
  REPO_DIR=$(find "$EXTRACT_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)
fi

if [ -z "${REPO_DIR:-}" ] || [ ! -f "$REPO_DIR/install-doublecheck.sh" ]; then
  echo "Could not find install-doublecheck.sh in downloaded archive." >&2
  exit 1
fi

sh "$REPO_DIR/install-doublecheck.sh"
