from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    severity: str
    criterion: str
    title: str
    location: str
    evidence: str
    recommendation: str


def build_report_filename(now: datetime | None = None) -> str:
    current = now or datetime.now()
    return current.strftime("doublecheck_%Y_%m_%d_%H%M.md")


def render_report(
    *,
    preview_url: str,
    excel_file: str,
    findings: list[Finding],
    unverified: list[str],
    generated_at: datetime | None = None,
) -> str:
    timestamp = generated_at or datetime.now()
    lines = [
        "# Doublecheck チェックレポート",
        "",
        f"- 生成日時: {timestamp.isoformat(timespec='minutes')}",
        f"- Preview URL: {preview_url}",
        f"- 調査票ファイル: {excel_file}",
        f"- 検出件数: {len(findings)}",
        f"- 未確認項目数: {len(unverified)}",
        "",
        "## 指摘事項",
        "",
    ]

    if findings:
        for index, finding in enumerate(findings, start=1):
            lines.extend(
                [
                    f"### {index}. [{finding.severity.upper()}] {finding.title}",
                    "",
                    f"- 観点: {finding.criterion}",
                    f"- 箇所: {finding.location}",
                    f"- 根拠: {finding.evidence}",
                    f"- 修正案: {finding.recommendation}",
                    "",
                ]
            )
    else:
        lines.extend(["指摘事項は見つかりませんでした。", ""])

    lines.extend(["## 未確認項目", ""])
    if unverified:
        lines.extend(f"- {item}" for item in unverified)
    else:
        lines.append("- なし")
    lines.append("")
    return "\n".join(lines)


def write_report(
    *,
    output_dir: str | Path,
    preview_url: str,
    excel_file: str,
    findings: list[Finding],
    unverified: list[str],
    generated_at: datetime | None = None,
) -> Path:
    destination_dir = Path(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    report_name = build_report_filename(generated_at)
    report_path = destination_dir / report_name
    report_text = render_report(
        preview_url=preview_url,
        excel_file=excel_file,
        findings=findings,
        unverified=unverified,
        generated_at=generated_at,
    )
    report_path.write_text(report_text, encoding="utf-8")
    return report_path
