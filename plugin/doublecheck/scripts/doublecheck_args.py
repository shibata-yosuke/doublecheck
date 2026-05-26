from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True)
class ValidatedInputs:
    preview_url: str
    excel_path: Path


def validate_preview_url(preview_url: str) -> str:
    parsed = urlparse(preview_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("preview URL must be an absolute http or https URL")
    return preview_url


def validate_excel_path(excel_file: str, cwd: str | Path | None = None) -> Path:
    base_dir = Path(cwd) if cwd is not None else Path.cwd()
    candidate = Path(excel_file)
    resolved = candidate if candidate.is_absolute() else base_dir / candidate
    resolved = resolved.resolve()
    if resolved.suffix.lower() != ".xlsx":
        raise ValueError("Excel file must use the .xlsx extension")
    if not resolved.is_file():
        raise ValueError(f"Excel file was not found: {resolved}")
    return resolved


def validate_inputs(
    preview_url: str,
    excel_file: str,
    cwd: str | Path | None = None,
) -> ValidatedInputs:
    return ValidatedInputs(
      preview_url=validate_preview_url(preview_url),
      excel_path=validate_excel_path(excel_file, cwd=cwd),
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate inputs for the doublecheck Codex plugin."
    )
    parser.add_argument("preview_url")
    parser.add_argument("excel_file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    try:
        validated = validate_inputs(args.preview_url, args.excel_file)
    except ValueError as exc:
        print(str(exc))
        return 1
    print(validated.excel_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
