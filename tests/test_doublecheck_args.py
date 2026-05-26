from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "plugin" / "doublecheck" / "scripts" / "doublecheck_args.py"
SPEC = importlib.util.spec_from_file_location("doublecheck_args", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_validate_inputs_accepts_valid_url_and_xlsx(tmp_path: Path) -> None:
    workbook = tmp_path / "questionnaire.xlsx"
    workbook.write_text("stub", encoding="utf-8")

    validated = MODULE.validate_inputs(
        "https://example.com/preview?id=1",
        workbook.name,
        cwd=tmp_path,
    )

    assert validated.preview_url == "https://example.com/preview?id=1"
    assert validated.excel_path == workbook.resolve()


def test_validate_inputs_rejects_invalid_url(tmp_path: Path) -> None:
    workbook = tmp_path / "questionnaire.xlsx"
    workbook.write_text("stub", encoding="utf-8")

    with pytest.raises(ValueError, match="preview URL must be an absolute http or https URL"):
        MODULE.validate_inputs("preview", workbook.name, cwd=tmp_path)


def test_validate_inputs_rejects_missing_workbook(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Excel file was not found"):
        MODULE.validate_inputs(
            "https://example.com/preview?id=1",
            "missing.xlsx",
            cwd=tmp_path,
        )


def test_validate_inputs_rejects_non_xlsx_extension(tmp_path: Path) -> None:
    workbook = tmp_path / "questionnaire.xlsm"
    workbook.write_text("stub", encoding="utf-8")

    with pytest.raises(ValueError, match="Excel file must use the .xlsx extension"):
        MODULE.validate_inputs(
            "https://example.com/preview?id=1",
            workbook.name,
            cwd=tmp_path,
        )
