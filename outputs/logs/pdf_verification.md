# PDF Verification Report

- **Build date/time:** 2026-06-12 16:42:58 UTC
- **PDF path:** `latex\main.pdf`
- **Page count:** 17
- **Build engine:** XeLaTeX (XeTeX)
- **Biber succeeded:** yes
- **Overall result:** PASS

## Required elements checklist

- [PASS] cover page
- [PASS] table of contents
- [PASS] headers/footers
- [PASS] chapters
- [PASS] TikZ diagram
- [PASS] Python-generated graph
- [PASS] table
- [PASS] highlighted formula
- [PASS] Hebrew-English BiDi section
- [PASS] citations
- [PASS] bibliography
- [PASS] callout/styled boxes
- [PASS] no API keys or secrets
- [PASS] PDF not tracked by git unless explicitly allowed

## Detailed checks

- [PASS] cover page — titlepage with book title
- [PASS] table of contents — \tableofcontents in main.tex
- [PASS] headers/footers — fancy page style enabled
- [PASS] chapters — 5 chapter(s) in main.tex
- [PASS] TikZ diagram — diagrams.tex with tikzpicture
- [PASS] Python-generated graph — figures.tex + assets\automation_impact_graph.png
- [PASS] table — tables.tex with tabularx/booktabs
- [PASS] highlighted formula — formulas.tex with formulabox
- [PASS] Hebrew-English BiDi section — bidi_section.tex with Hebrew text
- [PASS] citations — 24 \cite command(s) in LaTeX sources
- [PASS] bibliography — printbibliography + references.bib
- [PASS] callout/styled boxes — insightbox, warningbox, formulabox, chapterintrobox in preamble
- [PASS] no API keys or secrets — no secret patterns in latex/*.tex
- [PASS] PDF not tracked by git — latex/main.pdf is gitignored (not tracked)
- [PASS] PDF exists — latex\main.pdf
- [PASS] page count valid — 17 pages (expected 14-20)
- [PASS] XeLaTeX build configured — build_pdf.py and main.tex use XeLaTeX
