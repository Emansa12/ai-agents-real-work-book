"""Build the LaTeX book PDF using latexmk (XeLaTeX + biber when available)."""

from src.latex_fragments import sanitize_tex_fragment
from src.latex_runner import run_direct_xelatex_build
from src.pdf_build import build_pdf

__all__ = ["build_pdf", "run_direct_xelatex_build", "sanitize_tex_fragment"]


def main() -> int:
    return build_pdf()


if __name__ == "__main__":
    raise SystemExit(main())
