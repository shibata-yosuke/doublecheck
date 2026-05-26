from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_MARKETPLACE = {
    "name": "personal",
    "interface": {
        "displayName": "Personal"
    },
    "plugins": []
}


def build_plugin_entry(plugin_name: str, source_path: str) -> dict:
    return {
        "name": plugin_name,
        "source": {
            "source": "local",
            "path": source_path,
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }


def load_marketplace(path: Path) -> dict:
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_MARKETPLACE))
    return json.loads(path.read_text(encoding="utf-8"))


def upsert_marketplace(
    marketplace_path: str | Path,
    plugin_name: str = "doublecheck",
    source_path: str = "./plugins/doublecheck",
) -> Path:
    path = Path(marketplace_path)
    payload = load_marketplace(path)
    payload.setdefault("name", "personal")
    payload.setdefault("interface", {}).setdefault("displayName", "Personal")
    plugins = payload.setdefault("plugins", [])
    new_entry = build_plugin_entry(plugin_name, source_path)

    for index, entry in enumerate(plugins):
        if isinstance(entry, dict) and entry.get("name") == plugin_name:
            plugins[index] = new_entry
            break
    else:
        plugins.append(new_entry)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or update the personal Codex marketplace entry for doublecheck."
    )
    parser.add_argument("marketplace_path")
    parser.add_argument("--plugin-name", default="doublecheck")
    parser.add_argument("--source-path", default="./plugins/doublecheck")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    upsert_marketplace(
        marketplace_path=args.marketplace_path,
        plugin_name=args.plugin_name,
        source_path=args.source_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
