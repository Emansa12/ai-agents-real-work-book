"""XeLaTeX and latexmk command runners for PDF build."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

LATEX_DIR = Path("latex")
MAIN_JOBNAME = "main"
EXPECTED_PDF = LATEX_DIR / "main.pdf"

PERL_ERROR_MARKERS = (
    "could not find the script engine 'perl'",
    "perl which is required",
)


def find_command(name: str) -> str | None:
    return shutil.which(name)


def print_expected_pdf_path() -> None:
    print(f"Expected PDF path: {EXPECTED_PDF.resolve()}")


def print_manual_fallback_instructions() -> None:
    print("Manual fallback (from the latex/ directory):")
    print("  xelatex -interaction=nonstopmode -file-line-error main.tex")
    print("  biber main")
    print("  xelatex -interaction=nonstopmode -file-line-error main.tex")
    print("  xelatex -interaction=nonstopmode -file-line-error main.tex")


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    print("Running:", " ".join(command))
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=True,
    )


def output_indicates_perl_missing(result: subprocess.CompletedProcess[str]) -> bool:
    combined = f"{result.stdout}\n{result.stderr}".lower()
    return any(marker in combined for marker in PERL_ERROR_MARKERS)


def run_direct_xelatex_build() -> int:
    xelatex = find_command("xelatex")
    if xelatex is None:
        print("Error: xelatex is not installed or not on PATH.")
        print_manual_fallback_instructions()
        print_expected_pdf_path()
        return 1

    biber = find_command("biber")
    xelatex_args = [
        xelatex,
        "-interaction=nonstopmode",
        "-file-line-error",
        f"{MAIN_JOBNAME}.tex",
    ]

    sequence: list[list[str]] = [
        xelatex_args,
        [biber, MAIN_JOBNAME] if biber else [],
        xelatex_args,
        xelatex_args,
    ]

    print("Using direct XeLaTeX + biber fallback build.")
    print(f"Working directory: {LATEX_DIR.resolve()}")

    for command in sequence:
        if not command:
            print("Warning: biber not found; skipping bibliography processing.")
            continue
        result = run_command(command, LATEX_DIR)
        if result.stdout.strip():
            print(result.stdout)
        if result.stderr.strip():
            print(result.stderr)
        if result.returncode != 0:
            print(f"Error: command failed with exit code {result.returncode}.")
            print("Check latex/main.log for details.")
            print_expected_pdf_path()
            return result.returncode

    if EXPECTED_PDF.exists():
        print(f"PDF built successfully: {EXPECTED_PDF.resolve()}")
        return 0

    print("Warning: build finished but PDF not found.")
    print_expected_pdf_path()
    return 1


def run_latexmk_build() -> subprocess.CompletedProcess[str]:
    latexmk = find_command("latexmk")
    if latexmk is None:
        raise FileNotFoundError("latexmk not found")

    command = [
        latexmk,
        "-xelatex",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-use-biber",
        "-outdir=.",
        f"{MAIN_JOBNAME}.tex",
    ]
    print(f"Working directory: {LATEX_DIR.resolve()}")
    return run_command(command, LATEX_DIR)
