#!/usr/bin/env sh
set -eu

SCRIPT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
HOME_ROOT=${DOUBLECHECK_HOME:-$HOME}
TARGET_PLUGIN_ROOT="$HOME_ROOT/plugins/doublecheck"
MARKETPLACE_PATH="$HOME_ROOT/.agents/plugins/marketplace.json"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  echo "Python 3 was not found. Install Python 3 before running this uninstaller." >&2
  exit 1
fi

rm -rf "$TARGET_PLUGIN_ROOT"

"$PYTHON_BIN" "$SCRIPT_ROOT/scripts/upsert_marketplace.py" \
  "$MARKETPLACE_PATH" \
  --mode uninstall \
  --plugin-name doublecheck

echo "Removed doublecheck from $TARGET_PLUGIN_ROOT"
echo "Updated marketplace: $MARKETPLACE_PATH"
