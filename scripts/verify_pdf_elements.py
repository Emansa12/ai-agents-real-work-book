"""Phase 9 PDF verification — CLI wrapper."""

from __future__ import annotations

from src.pdf_checks import run_verification
from src.pdf_report import print_summary, write_report
from src.pdf_verification import CHECKLIST_LABELS, REPORT_PATH, ROOT

__all__ = [
    "CHECKLIST_LABELS",
    "REPORT_PATH",
    "ROOT",
    "run_verification",
    "write_report",
]


def main() -> int:
    report = run_verification()
    report_path = write_report(report)
    print_summary(report)
    print(f"Report written to: {report_path}")
    return 0 if report.all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
