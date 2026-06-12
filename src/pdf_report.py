"""Markdown report rendering for PDF verification."""

from __future__ import annotations

from pathlib import Path

from src.pdf_verification import CHECKLIST_LABELS, REPORT_PATH, VerificationReport


def render_markdown_report(report: VerificationReport) -> str:
    checklist = report.checklist_map()
    lines = [
        "# PDF Verification Report",
        "",
        f"- **Build date/time:** {report.build_datetime}",
        f"- **PDF path:** `{report.pdf_path}`",
        f"- **Page count:** "
        f"{report.page_count if report.page_count is not None else 'unknown'}",
        f"- **Build engine:** {report.build_engine}",
        f"- **Biber succeeded:** {'yes' if report.biber_succeeded else 'no'}",
        f"- **Overall result:** {'PASS' if report.all_passed else 'FAIL'}",
        "",
        "## Required elements checklist",
        "",
    ]
    for label in CHECKLIST_LABELS:
        status = "PASS" if checklist.get(label, False) else "FAIL"
        lines.append(f"- [{status}] {label}")

    lines.extend(["", "## Detailed checks", ""])
    for check in report.checks:
        status = "PASS" if check.passed else "FAIL"
        detail = f" — {check.detail}" if check.detail else ""
        lines.append(f"- [{status}] {check.name}{detail}")

    lines.append("")
    return "\n".join(lines)


def write_report(report: VerificationReport) -> Path:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_markdown_report(report), encoding="utf-8")
    return REPORT_PATH


def print_summary(report: VerificationReport) -> None:
    print("PDF Verification Summary")
    print("=" * 40)
    print(f"PDF: {report.pdf_path}")
    print(f"Pages: {report.page_count if report.page_count is not None else 'unknown'}")
    print(f"Engine: {report.build_engine}")
    print(f"Biber: {'yes' if report.biber_succeeded else 'no'}")
    print()
    for check in report.checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"  [{status}] {check.name}")
    print()
    overall = "PASS" if report.all_passed else "FAIL"
    print(f"OVERALL: {overall}")
