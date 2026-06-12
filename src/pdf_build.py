"""Orchestrate LaTeX PDF build with latexmk or direct XeLaTeX fallback."""

from __future__ import annotations

from pathlib import Path

from src.latex_fragments import prepare_generated_fragments
from src.latex_runner import (
    EXPECTED_PDF,
    find_command,
    output_indicates_perl_missing,
    print_expected_pdf_path,
    print_manual_fallback_instructions,
    run_direct_xelatex_build,
    run_latexmk_build,
)

MAIN_TEX = Path("latex") / "main.tex"


def build_pdf() -> int:
    if not MAIN_TEX.exists():
        print(f"Error: missing LaTeX entry file: {MAIN_TEX}")
        return 1

    prepared = prepare_generated_fragments()
    if prepared:
        count = len(prepared)
        build_dir = Path("latex") / ".build" / "generated"
        print(f"Prepared {count} sanitized fragment(s) under {build_dir}")
    else:
        print(
            "Warning: no generated fragments prepared. "
            "Run the crew pipeline to populate latex/generated/."
        )

    xelatex = find_command("xelatex")
    if xelatex is None:
        print("Error: xelatex is not installed or not on PATH.")
        print_manual_fallback_instructions()
        print_expected_pdf_path()
        return 1

    latexmk = find_command("latexmk")
    if latexmk is None:
        print("Warning: latexmk is not on PATH; trying direct XeLaTeX build.")
        return run_direct_xelatex_build()

    result = run_latexmk_build()
    if result.stdout.strip():
        print(result.stdout)
    if result.stderr.strip():
        print(result.stderr)

    if result.returncode == 0 and EXPECTED_PDF.exists():
        print(f"PDF built successfully: {EXPECTED_PDF.resolve()}")
        return 0

    if output_indicates_perl_missing(result):
        print(
            "Error: latexmk failed because Perl is missing "
            "(common on MiKTeX on Windows)."
        )
        print("Install Perl for MiKTeX, or use the direct XeLaTeX fallback below.")
        print_manual_fallback_instructions()
        return run_direct_xelatex_build()

    if result.returncode != 0:
        print(f"Error: latexmk failed with exit code {result.returncode}.")
        print("Check latex/main.log for details.")
        print("Trying direct XeLaTeX + biber fallback...")
        fallback_code = run_direct_xelatex_build()
        if fallback_code != 0:
            print_expected_pdf_path()
        return fallback_code

    print_expected_pdf_path()
    return 1
