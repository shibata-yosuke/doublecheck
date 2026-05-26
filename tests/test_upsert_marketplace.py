from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "upsert_marketplace.py"
SPEC = importlib.util.spec_from_file_location("upsert_marketplace", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_upsert_marketplace_creates_default_file(tmp_path: Path) -> None:
    marketplace_path = tmp_path / "marketplace.json"

    MODULE.upsert_marketplace(marketplace_path)

    payload = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert payload["name"] == "personal"
    assert payload["interface"]["displayName"] == "Personal"
    assert payload["plugins"][0]["name"] == "doublecheck"


def test_upsert_marketplace_replaces_existing_doublecheck_entry(tmp_path: Path) -> None:
    marketplace_path = tmp_path / "marketplace.json"
    marketplace_path.write_text(
        json.dumps(
            {
                "name": "personal",
                "interface": {"displayName": "Personal"},
                "plugins": [
                    {
                        "name": "doublecheck",
                        "source": {"source": "local", "path": "./plugins/old"},
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Productivity",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    MODULE.upsert_marketplace(marketplace_path)

    payload = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert len(payload["plugins"]) == 1
    assert payload["plugins"][0]["source"]["path"] == "./plugins/doublecheck"


def test_remove_marketplace_entry_deletes_only_target_plugin(tmp_path: Path) -> None:
    marketplace_path = tmp_path / "marketplace.json"
    marketplace_path.write_text(
        json.dumps(
            {
                "name": "personal",
                "interface": {"displayName": "Personal"},
                "plugins": [
                    {
                        "name": "doublecheck",
                        "source": {"source": "local", "path": "./plugins/doublecheck"},
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Productivity",
                    },
                    {
                        "name": "other-plugin",
                        "source": {"source": "local", "path": "./plugins/other-plugin"},
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Productivity",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    MODULE.remove_marketplace_entry(marketplace_path)

    payload = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert [entry["name"] for entry in payload["plugins"]] == ["other-plugin"]


def test_remove_marketplace_entry_keeps_missing_file_unchanged(tmp_path: Path) -> None:
    marketplace_path = tmp_path / "missing-marketplace.json"

    result = MODULE.remove_marketplace_entry(marketplace_path)

    assert result == marketplace_path
    assert not marketplace_path.exists()
