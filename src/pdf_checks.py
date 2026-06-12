"""Run all PDF verification checks and assemble the report."""

from __future__ import annotations

from datetime import UTC, datetime

from src.pdf_artifact_checks import artifact_checks, load_main_sources
from src.pdf_check_helpers import biber_succeeded, detect_build_engine, pdf_page_count
from src.pdf_content_checks import content_checks
from src.pdf_structure_checks import structure_checks
from src.pdf_verification import MAIN_PDF, ROOT, VerificationReport


def run_verification() -> VerificationReport:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    main_content, preamble_content = load_main_sources()

    checks = []
    checks.extend(structure_checks(main_content, preamble_content))
    checks.extend(content_checks(main_content, preamble_content))
    checks.extend(artifact_checks(main_content))

    return VerificationReport(
        build_datetime=now,
        pdf_path=str(MAIN_PDF.relative_to(ROOT)),
        page_count=pdf_page_count(MAIN_PDF),
        build_engine=detect_build_engine(),
        biber_succeeded=biber_succeeded(),
        checks=checks,
    )
