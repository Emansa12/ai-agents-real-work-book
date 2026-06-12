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

Phases 2–9 implement and validate this pipeline step by step. Phase 9 closes with the verification checklist (TikZ diagram, Python graph, table, fancy formula, BiDi, citations, bibliography, callout design).

## Phase 0 — Planning and Scaffold (M0)

- Repository folder structure, PRD, plan, TODO, `.gitignore`, `.env.example`, and stub README.
- Course PDFs stored locally under `_course_materials/` (gitignored).
- No application code yet.
- **Status:** Complete (committed).

## Phase 0.5 — GitHub Remote and First Push (M0.5)

- Create GitHub repository and add remote.
- Rename local branch to `main` if needed.
- Push Phase 0 commit to GitHub.
- Verify `.env`, PDFs, and `_course_materials/` are not on GitHub.
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
- **Status:** Complete locally; commit pending.

## Phase 4 — Tasks and Context Workflow (M4)

- Define Research, Writing, Review, and LaTeX tasks with sequential dependencies.
- Shared context flows Research → Write → Review → LaTeX.
- Document workflow in `docs/`.

## Phase 5 — Run Crew per Chapter (M5)

- `scripts/run_crew.py` orchestrates full pipeline per chapter or section.
- Save research, drafts, reviews, LaTeX fragments, and logs to `outputs/` and `latex/generated/`.

## Phase 6 — Cost and Token Tracking (M6)

- Track API usage (tokens, estimated cost) per run and per agent.
- Persist summaries to `outputs/logs/`; budget warning before expensive runs.

## Phase 7 — LaTeX Structure (M7)

- `latex/main.tex`, `latex/preamble.tex`, chapter templates, `latex/generated/` for agent output.
- LuaLaTeX or XeLaTeX, preferably through latexmk; Hebrew–English BiDi support.
- Cover page, TOC, headers/footers; bibliography setup with biber/BibTeX.
- Preamble setup for TikZ, fancy formulas, and callout/styled boxes.

## Phase 8 — Required PDF Elements and Design (M8)

- TikZ architecture/workflow diagram (does not replace the Python graph).
- `scripts/make_figures.py` to generate at least one graph; include output in LaTeX.
- Table, fancy/highlighted formula, Hebrew–English BiDi section, linked citations, bibliography.
- Callout boxes or styled boxes for polished document design.

## Phase 9 — Compile and Verify PDF (M9)

- Build script (e.g., `scripts/compile_pdf.sh` or equivalent) using LuaLaTeX or XeLaTeX, preferably through latexmk.
- Fix LaTeX escaping for special characters and BiDi mixing.
- Run verification checklist: ~15 pages, TikZ diagram, Python graph, table, fancy formula, BiDi, citations, bibliography, callout design.

## Phase 10 — Tests and Quality (M10)

- Unit tests for config, search tool, secret redaction, LaTeX escaping, and critical helpers.
- Optional smoke/integration test that does not waste tokens.
- `pytest` and `ruff` must pass.

## Phase 11 — README and Evidence (M11)

- Expand README: setup, API keys, `.env`, live search requirement, CrewAI pipeline, PDF compile.
- Document evidence paths and required submission artifacts:
  - Live internet search run evidence
  - CrewAI execution evidence
  - Generated LaTeX/source evidence
  - Saved research, draft, and review artifacts
  - PDF compilation evidence
  - Terminal logs or screenshots

## Phase 12 — Final Submission (M12)

- Final PDF meets all PRD requirements; live API research evidence exists.
- No static lecture bodies as main content source.
- No `.env`, PDFs, or `_course_materials/` in GitHub; all phases committed and pushed.
- GitHub repo public or shared with lecturer; Moodle submission with GitHub URL.
