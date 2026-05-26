from __future__ import annotations

import importlib.util
from datetime import datetime
from pathlib import Path
import sys


MODULE_PATH = Path(__file__).resolve().parents[1] / "plugin" / "doublecheck" / "scripts" / "doublecheck_report.py"
SPEC = importlib.util.spec_from_file_location("doublecheck_report", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_build_report_filename_uses_expected_timestamp_format() -> None:
    name = MODULE.build_report_filename(datetime(2026, 5, 26, 14, 37))
    assert name == "doublecheck_2026_05_26_1437.md"


def test_render_report_includes_findings_and_unverified_items() -> None:
    finding = MODULE.Finding(
        severity="high",
        criterion="skip logic",
        title="Broken branch",
        location="Q5",
        evidence="Preview shows a follow-up for an excluded respondent.",
        recommendation="Fix the branch condition.",
    )

    report = MODULE.render_report(
        preview_url="https://example.com/preview?id=2",
        excel_file="questionnaire.xlsx",
        findings=[finding],
        unverified=["Media plan alignment"],
        generated_at=datetime(2026, 5, 26, 14, 37),
    )

    assert "# Doublecheck Report" in report
    assert "Issues found: 1" in report
    assert "### 1. [HIGH] Broken branch" in report
    assert "- Unverified checks: 1" in report
    assert "- Media plan alignment" in report


def test_write_report_persists_markdown_file(tmp_path: Path) -> None:
    report_path = MODULE.write_report(
        output_dir=tmp_path,
        preview_url="https://example.com/preview?id=3",
        excel_file="questionnaire.xlsx",
        findings=[],
        unverified=[],
        generated_at=datetime(2026, 5, 26, 14, 37),
    )

    assert report_path.name == "doublecheck_2026_05_26_1437.md"
    assert report_path.read_text(encoding="utf-8").startswith("# Doublecheck Report")
