"""Build the LaTeX book PDF using latexmk (LuaLaTeX + biber when available)."""

import re
import shutil
import subprocess
from pathlib import Path

LATEX_DIR = Path("latex")
GENERATED_DIR = LATEX_DIR / "generated"
BUILD_GENERATED_DIR = LATEX_DIR / ".build" / "generated"
MAIN_TEX = LATEX_DIR / "main.tex"
MAIN_JOBNAME = "main"
EXPECTED_PDF = LATEX_DIR / "main.pdf"

MARKDOWN_FENCE_RE = re.compile(r"^```(?:latex|tex)?\s*$|^```\s*$")
PERL_ERROR_MARKERS = (
    "could not find the script engine 'perl'",
    "perl which is required",
)


def sanitize_tex_fragment(content: str) -> str:
    """Strip markdown code fences from crew-generated LaTeX fragments."""
    lines: list[str] = []
    for line in content.splitlines():
        if MARKDOWN_FENCE_RE.match(line.strip()):
            continue
        lines.append(line)
    text = "\n".join(lines).strip()
    if text:
        return text + "\n"
    return ""


def prepare_generated_fragments() -> list[Path]:
    """
    Copy sanitized crew fragments to latex/.build/generated/ for compilation.

    Original artifacts in latex/generated/ are not modified.
    """
    BUILD_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    prepared: list[Path] = []

    if not GENERATED_DIR.exists():
        return prepared

    for source in sorted(GENERATED_DIR.glob("*.tex")):
        sanitized = sanitize_tex_fragment(source.read_text(encoding="utf-8"))
        if not sanitized:
            continue
        target = BUILD_GENERATED_DIR / source.name
        target.write_text(sanitized, encoding="utf-8")
        prepared.append(target)

    return prepared


def find_command(name: str) -> str | None:
    return shutil.which(name)


def print_expected_pdf_path() -> None:
    print(f"Expected PDF path: {EXPECTED_PDF.resolve()}")


def print_manual_fallback_instructions() -> None:
    print("Manual fallback (from the latex/ directory):")
    print("  lualatex -interaction=nonstopmode -file-line-error main.tex")
    print("  biber main")
    print("  lualatex -interaction=nonstopmode -file-line-error main.tex")
    print("  lualatex -interaction=nonstopmode -file-line-error main.tex")


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


def run_direct_lualatex_build() -> int:
    lualatex = find_command("lualatex")
    if lualatex is None:
        print("Error: lualatex is not installed or not on PATH.")
        print_manual_fallback_instructions()
        print_expected_pdf_path()
        return 1

    biber = find_command("biber")
    lualatex_args = [
        lualatex,
        "-interaction=nonstopmode",
        "-file-line-error",
        f"{MAIN_JOBNAME}.tex",
    ]

    sequence: list[list[str]] = [
        lualatex_args,
        [biber, MAIN_JOBNAME] if biber else [],
        lualatex_args,
        lualatex_args,
    ]

    print("Using direct LuaLaTeX + biber fallback build.")
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
        "-lualatex",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-use-biber",
        "-outdir=.",
        f"{MAIN_JOBNAME}.tex",
    ]
    print(f"Working directory: {LATEX_DIR.resolve()}")
    return run_command(command, LATEX_DIR)


def build_pdf() -> int:
    if not MAIN_TEX.exists():
        print(f"Error: missing LaTeX entry file: {MAIN_TEX}")
        return 1

    prepared = prepare_generated_fragments()
    if prepared:
        count = len(prepared)
        print(f"Prepared {count} sanitized fragment(s) under {BUILD_GENERATED_DIR}")
    else:
        print(
            "Warning: no generated fragments prepared. "
            "Run the crew pipeline to populate latex/generated/."
        )

    latexmk = find_command("latexmk")
    if latexmk is None:
        print("Warning: latexmk is not on PATH; trying direct LuaLaTeX build.")
        return run_direct_lualatex_build()

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
        print("Install Perl for MiKTeX, or use the direct LuaLaTeX fallback below.")
        print_manual_fallback_instructions()
        return run_direct_lualatex_build()

    if result.returncode != 0:
        print(f"Error: latexmk failed with exit code {result.returncode}.")
        print("Check latex/main.log for details.")
        print("Trying direct LuaLaTeX + biber fallback...")
        fallback_code = run_direct_lualatex_build()
        if fallback_code != 0:
            print_expected_pdf_path()
        return fallback_code

    print_expected_pdf_path()
    return 1


def main() -> int:
    return build_pdf()


if __name__ == "__main__":
    raise SystemExit(main())
