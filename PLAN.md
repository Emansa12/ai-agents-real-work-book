# Implementation Plan

High-level phases for building the system incrementally. Each phase should be completed in a small, reviewable Git commit before moving to the next.

Companion task tracker: `TODO.md` (milestones M0–M12).

## Planned Production Pipeline

```
Live Internet Search via API
  → Researcher Agent
  → Writer Agent
  → Reviewer Agent
  → LaTeX Builder
  → PDF Compile
  → Verification Checklist
```

The book must be generated from live research artifacts, not from static lecture bodies.

Phases 2–12 implement and validate this pipeline end to end. Phase 9 closes with the verification checklist; Phase 11 delivers a submission-ready README; Phase 12 commits the final submission PDF and evidence.

## Phase 0 — Planning and Scaffold (M0)

- Repository folder structure, PRD, plan, TODO, `.gitignore`, `.env.example`, and stub README.
- Course materials are not part of the repository and are not used as the production content source.
- No application code yet.
- **Status:** Complete (committed).

## Phase 0.5 — GitHub Remote and First Push (M0.5)

- Create GitHub repository and add remote.
- Rename local branch to `main` if needed.
- Push Phase 0 commit to GitHub.
- Verify `.env`, generated PDFs, and course materials are not on GitHub.
- Commit and push any documentation cleanup before Phase 1.
- **Status:** Complete (committed).

## Phase 1 — Environment and Config (M1)

- **Status:** Complete (committed).
- `pyproject.toml` with uv; `uv.lock` after `uv sync`.
- Dependencies: CrewAI, crewai-tools, python-dotenv, pydantic, requests or httpx, matplotlib, pytest, ruff.
- Config module under `src/` to load settings from `.env`.
- Validate `OPENAI_API_KEY`, `SERPER_API_KEY`, `MODEL_NAME`; fail fast with clear errors.
- Secret redaction helper if logs are introduced; never print API keys.

## Phase 2 — Live Internet Search Tool (M2)

- `SerperSearchClient` and `scripts/run_live_search.py`; evidence under `outputs/research/`.
- Real API search only; no offline/fake mode.
- **Status:** Complete (committed).

## Phase 3 — CrewAI Agents (M3)

- `src/agent_config.py`, `src/agents.py`, `src/search_adapter.py` with CrewAI `@tool` wrapper.
- **Researcher Agent:** Uses `live_internet_search` tool; gathers and summarizes findings.
- **Writer Agent:** Drafts from research context, not static lecture bodies.
- **Reviewer Agent:** Checks accuracy, clarity, citations, and topic alignment.
- **LaTeX Builder Agent or service:** Prepares reviewed output for `latex/generated/`.
- No crew kickoff in this phase; tasks wired in Phase 4.
- **Status:** Complete (committed and pushed).

## Phase 4 — Tasks and Context Workflow (M4)

- `src/task_config.py`, `src/tasks.py`, `src/crew_factory.py`; `docs/workflow.md`.
- Research → Write → Review → LaTeX tasks with `context=[...]` chaining.
- `create_book_crew()` returns sequential `Crew`; no kickoff in this phase.
- **Status:** Complete (committed and pushed).

## Phase 5 — Run Crew per Chapter (M5)

- `src/chapters.py`, `src/run_artifacts.py`, `src/crew_runner.py`, `scripts/run_crew.py`.
- Default one chapter; `--chapter N`; explicit `--all` for full book run.
- Save research, drafts, reviews, LaTeX fragments, and logs to `outputs/` and `latex/generated/`.
- **Status:** Complete (committed and pushed).

## Phase 6 — Cost and Token Tracking (M6)

- Cost/token estimation split across `src/cost_tracker.py`, `src/cost_models.py`, and `src/token_estimator.py`.
- `scripts/report_costs.py` generates reports from saved artifacts in `outputs/logs/`.
- Estimate tokens/cost from saved artifacts; reports in `outputs/logs/`.
- Budget warnings and rough `--all` projection in cost report.
- **Status:** Complete (committed and pushed).

## Phase 7 — LaTeX Structure (M7)

- `latex/main.tex`, `latex/preamble.tex`, `latex/references.bib`.
- PDF build logic is modular: `scripts/build_pdf.py` (thin CLI wrapper), `src/pdf_build.py`, `src/latex_runner.py`, and `src/latex_fragments.py`.
- Build behavior: XeLaTeX + biber; latexmk preferred; direct XeLaTeX fallback on Windows.
- Hebrew–English BiDi; cover, TOC, headers/footers; biblatex + biber.
- Includes `latex/generated/` crew fragments (sanitized at build time).
- Preamble prepares TikZ/tcolorbox/biblatex/polyglossia support.
- **Status:** Complete (committed and pushed).

## Phase 8 — Required PDF Elements and Design (M8)

- Required PDF elements and design complete.
- TikZ diagram, Python graph, table, highlighted formula, BiDi section, callouts, citations, bibliography.
- `scripts/make_figures.py`, `latex/diagrams.tex`, `figures.tex`, `tables.tex`, `formulas.tex`, `bidi_section.tex`, etc.
- **Status:** Complete (committed and pushed).

## Phase 9 — Compile and Verify PDF (M9)

- Verification logic is modular: `scripts/verify_pdf_elements.py` (thin CLI wrapper), `src/pdf_checks.py`, `src/pdf_content_checks.py`, `src/pdf_structure_checks.py`, `src/pdf_artifact_checks.py`, `src/pdf_report.py`, and `src/pdf_verification.py`.
- Report written to `outputs/logs/pdf_verification.md`.
- 17-page PDF verified; 96 tests passing.
- Verification checklist: TikZ diagram, Python graph, table, fancy formula, BiDi, citations, bibliography, callout design.
- **Status:** Complete (committed and pushed).

## Phase 10 — Tests and Quality (M10)

- 96 pytest tests; ruff check and format pass.
- PDF verification tests; LaTeX structure and element tests.
- All Python files in `src/`, `scripts/`, and `tests/` are under 150 lines after modular refactoring.
- The line-count check is part of final submission evidence.
- **Status:** Complete (committed and pushed).

## Phase 11 — README and Evidence (M11)

- Submission-ready README: setup, API keys, `.env`, live search, CrewAI pipeline, XeLaTeX build, verification.
- Documents final PDF at `outputs/final/ai_agents_real_work_book.pdf` and local build output at `latex/main.pdf`.
- **Status:** Complete (committed and pushed).

## Phase 12 — Final Submission (M12)

- Final PDF meets all PRD requirements; live API research evidence exists.
- No static lecture bodies as main content source.
- No `.env`, API keys, or course materials in GitHub.
- Final submission PDF committed at `outputs/final/ai_agents_real_work_book.pdf`; intermediate generated PDFs such as `latex/main.pdf` remain local/gitignored.
- Verification report (`outputs/logs/pdf_verification.md`) and cost report (`outputs/logs/cost_report.md`, `cost_report.json`) committed.
- All final code, documentation, screenshots, reports, and the final PDF are committed and pushed before submission.
- README includes screenshots under `docs/screenshots/`.
- Final evidence includes PDF verification, cost report, line-count evidence, and rendered PDF screenshots.
- GitHub repo public or shared with lecturer; Moodle submission with GitHub URL.
- **Status:** Complete (committed and pushed).
