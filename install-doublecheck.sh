#!/usr/bin/env sh
set -eu

SCRIPT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
HOME_ROOT=${DOUBLECHECK_HOME:-$HOME}
PLUGIN_SOURCE="$SCRIPT_ROOT/plugin/doublecheck"
TARGET_PLUGIN_ROOT="$HOME_ROOT/plugins/doublecheck"
MARKETPLACE_PATH="$HOME_ROOT/.agents/plugins/marketplace.json"

if [ ! -d "$PLUGIN_SOURCE" ]; then
  echo "Plugin source not found: $PLUGIN_SOURCE" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  echo "Python 3 was not found. Install Python 3 before running this installer." >&2
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "npx was not found. Install Node.js before running this installer." >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET_PLUGIN_ROOT")"
rm -rf "$TARGET_PLUGIN_ROOT"
cp -R "$PLUGIN_SOURCE" "$TARGET_PLUGIN_ROOT"

"$PYTHON_BIN" "$SCRIPT_ROOT/scripts/upsert_marketplace.py" \
  "$MARKETPLACE_PATH" \
  --plugin-name doublecheck \
  --source-path ./plugins/doublecheck

echo "Installed doublecheck to $TARGET_PLUGIN_ROOT"
echo "Updated marketplace: $MARKETPLACE_PATH"
