# TODO — Task Tracking

**Product:** `ai-agents-real-work-book`  
**Companion to:** `PRD.md` / `PLAN.md`

**Status keys:**

- ☐ not started
- ◐ in progress
- ☑ done

**Owner:**

- `dev` for manual development work
- `ai` for AI-assisted/Cursor work

Each task includes or implies a Definition of Done.

---

## Overall Status

**Overall:** ☑ Phases 0–12 complete, committed, and pushed.  
**Current milestone:** M12 — Final Submission (complete).  
**Latest pushed commit will be updated after the final submission commit.**

- Every Python file in `src/`, `scripts/`, and `tests/` is under 150 lines after modular refactoring.
- README includes final screenshot evidence under `docs/screenshots/`.
- Required PDF elements in LaTeX: TikZ diagram, Python graph, table, formula, BiDi, citations.
- Reports saved to `outputs/logs/cost_report.md` and `cost_report.json`.
- `pytest` and `ruff` pass.
- Course materials are not part of the repository and are not used as the production content source.
- Real API keys are not committed.
- Final system will require live API-based internet research; no offline/fake production mode.

---

## Project Pipeline

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

---

## Documentation Maintenance Rule

- ☑ Before each phase, read `PRD.md`, `PLAN.md`, and `TODO.md`.
- ☑ During each phase, update `TODO.md` with current progress.
- ☑ After each phase, mark completed tasks.
- ☑ If requirements changed, update `PRD.md`.
- ☑ If implementation strategy changed, update `PLAN.md`.
- ☑ Add Phase Completion Notes after every phase.
- ☑ Commit documentation updates together with completed phase implementations (Phases 10–12 committed and pushed).

---

## Phase 0 — Planning and Scaffold (M0) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T0.1 | Create repository scaffold and folders | ai | ☑ |
| T0.2 | Add `README.md` stub | ai | ☑ |
| T0.3 | Write `PRD.md` | ai | ☑ |
| T0.4 | Write `PLAN.md` | ai | ☑ |
| T0.5 | Write `TODO.md` | ai | ☑ |
| T0.6 | Add `.gitignore` with `*.pdf`, `.env`, `.venv/`, caches, and other local-only paths | ai | ☑ |
| T0.7 | Add `.env.example` placeholders only | ai | ☑ |
| T0.8 | Keep course materials outside the repository | dev | ☑ |
| T0.9 | Commit Phase 0 locally | dev | ☑ |

**Definition of Done:** Repository scaffold exists; planning docs are complete; no application code; no secrets; ready for GitHub push.

### Phase 0 Completion Notes

- Scaffold created.
- No application code added.
- No dependencies installed.
- Course materials are not part of the repository.
- Secrets are not committed.
- Phase 0 committed and pushed.
- GitHub push completed in Phase 0.5.

---

## Phase 0.5 — GitHub Remote and First Push (M0.5) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T0.5.1 | Create GitHub repository | dev | ☑ |
| T0.5.2 | Rename local branch to `main` | dev | ☑ |
| T0.5.3 | Add GitHub remote | dev | ☑ |
| T0.5.4 | Push Phase 0 commit to GitHub | dev | ☑ |
| T0.5.5 | Confirm GitHub does not contain `.env`, PDFs, or course materials | dev | ☑ |
| T0.5.6 | Commit/push documentation cleanup if needed | dev | ☑ |

**Definition of Done:** Phase 0 commit exists on GitHub, repository is accessible, and private/course files are not uploaded.

### Phase 0.5 Completion Notes

- GitHub repository created.
- Local branch is `main`.
- Remote `origin` points to the GitHub repository.
- Phase 0 commits pushed successfully.
- Private files are ignored: `.env`, PDFs, and other non-repository materials.
- Ready for Phase 1.

---

## Phase 1 — Environment and Config (M1) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T1.1 | Create `pyproject.toml` with uv | ai | ☑ |
| T1.2 | Add `uv.lock` | ai | ☑ |
| T1.3 | Add dependencies: CrewAI, crewai-tools, python-dotenv, pydantic, requests or httpx, matplotlib, pytest, ruff | ai | ☑ |
| T1.4 | Create config module under `src/` | ai | ☑ |
| T1.5 | Load `.env` using python-dotenv | ai | ☑ |
| T1.6 | Validate required keys: `OPENAI_API_KEY`, `SERPER_API_KEY`, `MODEL_NAME` | ai | ☑ |
| T1.7 | Fail fast with clear error when keys are missing | ai | ☑ |
| T1.8 | Do not print API keys | ai | ☑ |
| T1.9 | Add simple secret redaction helper if logs are introduced | ai | ☑ |
| T1.10 | Update README setup instructions | ai | ☑ |
| T1.11 | Run `uv sync` | dev | ☑ |
| T1.12 | Commit Phase 1 | dev | ☑ |

**Definition of Done:** `uv sync` works, config loads from `.env`, missing keys produce a clear error, no secrets are committed.

### Phase 1 Completion Notes

- `pyproject.toml` created with Python >=3.11 and required dependencies.
- `uv.lock` generated via `uv sync`.
- `src/config.py` loads `.env`, validates API keys, defaults `MODEL_NAME` to `gpt-4o-mini`.
- `src/redaction.py` redacts `sk-*` patterns and explicit secrets.
- `scripts/check_config.py` prints safe status only (no key values).
- Tests cover missing keys, placeholder rejection, success with fake env, and redaction.
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 1 committed and pushed.

---

## Phase 2 — Live Internet Search Tool (M2) — ☑ complete, committed and pushed

Serper API or equivalent. Real API search. Save raw search evidence. No offline/fake mode.

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T2.1 | Implement Serper search client (`SerperSearchClient`) | ai | ☑ |
| T2.2 | Add minimal live search script | ai | ☑ |
| T2.3 | Save raw search output to `outputs/research/` | ai | ☑ |
| T2.4 | Extract title, URL, snippet, and date if available | ai | ☑ |
| T2.5 | Validate at least one real search succeeds with valid keys | dev | ☑ |
| T2.6 | Update README with search usage | ai | ☑ |
| T2.7 | Commit Phase 2 | dev | ☑ |

**Definition of Done:** One real API search succeeds, output is saved as evidence, and the search tool is ready for the Researcher Agent.

### Phase 2 Completion Notes

- `src/search_models.py` — `SearchResult` and `SearchResponse` Pydantic models.
- `src/search_tool.py` — `SerperSearchClient` using httpx and Serper Google search endpoint.
- `scripts/run_live_search.py` — live search with safe summary and JSON evidence output.
- `tests/test_search_tool.py` — mocked HTTP tests only; no real API calls in tests.
- Live search validated with real `SERPER_API_KEY`; evidence saved under `outputs/research/`.
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 2 committed and pushed.

---

## Phase 3 — CrewAI Agents (M3) — ☑ complete, committed and pushed

Explicit agents: Researcher Agent, Writer Agent, Reviewer Agent, LaTeX Builder Agent or LaTeX Builder service.

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T3.1 | Create modular agent definitions | ai | ☑ |
| T3.2 | Researcher uses the live search tool | ai | ☑ |
| T3.3 | Writer uses research context, not static lecture bodies | ai | ☑ |
| T3.4 | Reviewer checks accuracy, clarity, citations, and topic alignment | ai | ☑ |
| T3.5 | LaTeX Builder prepares reviewed output for LaTeX | ai | ☑ |
| T3.6 | Keep Python files small and focused | ai | ☑ |
| T3.7 | Commit Phase 3 | dev | ☑ |

**Definition of Done:** Agents are importable, roles are clear, Researcher uses live search, and no agent relies on hardcoded book content.

### Phase 3 Completion Notes

- `src/agent_config.py` - shared roles, goals, and backstories.
- `src/agents.py` - factory functions for Researcher, Writer, Reviewer, LaTeX Builder.
- `src/search_adapter.py` - Serper adapter and CrewAI `live_internet_search` tool.
- Researcher agent includes live search tool; no crew kickoff in this phase.
- `tests/test_agents.py` and `tests/test_search_adapter.py` pass with mocks only.
- `pytest` (26 passed), `ruff check`, and `ruff format --check` pass.
- Post-Phase 3 checkpoint audit (Phases 0-3): pass.
- Phase 3 committed and pushed.

---

## Phase 4 — Tasks and Context Workflow (M4) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T4.1 | Define Research Task | ai | ☑ |
| T4.2 | Define Writing Task | ai | ☑ |
| T4.3 | Define Review Task | ai | ☑ |
| T4.4 | Define LaTeX Task | ai | ☑ |
| T4.5 | Use context from previous tasks | ai | ☑ |
| T4.6 | Use sequential process unless a later reason justifies a change | ai | ☑ |
| T4.7 | Document workflow in `docs/` | ai | ☑ |
| T4.8 | Commit Phase 4 | dev | ☑ |

**Definition of Done:** Research → Write → Review → LaTeX task flow is defined and context passes correctly between tasks.

### Phase 4 Completion Notes

- `src/task_config.py` - task descriptions and expected outputs.
- `src/tasks.py` - four task factories with `context=[...]` chaining.
- `src/crew_factory.py` - `create_book_crew()` with `Process.sequential`; no kickoff.
- `docs/workflow.md` - pipeline and context flow documented.
- `tests/test_tasks.py` and `tests/test_crew_factory.py` pass with mocks only.
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 4 committed and pushed.

---

## Phase 5 — Run Crew per Chapter (M5) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T5.1 | Define final chapter list | ai | ☑ |
| T5.2 | Create `scripts/run_crew.py` | ai | ☑ |
| T5.3 | Run the full crew pipeline for the default chapter and keep `--all` as an explicit full-book option | dev | ☑ |
| T5.4 | Save research artifacts to `outputs/research/` | ai | ☑ |
| T5.5 | Save drafts to `outputs/drafts/` | ai | ☑ |
| T5.6 | Save reviews to `outputs/reviews/` | ai | ☑ |
| T5.7 | Save generated LaTeX fragments to `latex/generated/` | ai | ☑ |
| T5.8 | Save run logs to `outputs/logs/` | ai | ☑ |
| T5.9 | Commit Phase 5 | dev | ☑ |

**Definition of Done:** End-to-end crew run produces chapter content from live research, with evidence artifacts saved on disk.

### Phase 5 Completion Notes

- `src/chapters.py` - eight chapter titles including Hebrew-English BiDi summary.
- `src/run_artifacts.py` - artifact paths and safe file writers with redaction.
- `src/crew_runner.py` - `run_chapter_crew()` executes kickoff and saves outputs.
- `scripts/run_crew.py` - default chapter 1; `--chapter N`; explicit `--all`.
- Live chapter 1 run completed (default); `--all` remains an explicit opt-in for full-book runs.
- Artifacts saved under `outputs/` and `latex/generated/`.
- Tests for chapters, artifacts, and CLI (mocked) pass.
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 5 committed and pushed.

---

## Phase 6 — Cost and Token Tracking (M6) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T6.1 | Add token/cost estimation helper | ai | ☑ |
| T6.2 | Track usage per run and per agent where possible | ai | ☑ |
| T6.3 | Save cost report to `outputs/logs/` | ai | ☑ |
| T6.4 | Add budget warning before expensive live runs | ai | ☑ |
| T6.5 | Document cost tracking in README | ai | ☑ |
| T6.6 | Commit Phase 6 | dev | ☑ |

**Definition of Done:** Each run records readable usage/cost information or a clear estimate.

### Phase 6 Completion Notes

- `src/cost_tracker.py`, `src/cost_models.py`, and `src/token_estimator.py` split token/cost models, estimation logic, artifact summaries, and budget warnings while keeping all files under 150 lines.
- `scripts/report_costs.py` - scans artifacts; writes MD/JSON reports; no API calls.
- Estimates use chars/4 token proxy when provider usage metadata is unavailable.
- Budget warnings for high estimated cost and rough `--all` projection.
- `tests/test_cost_tracker.py` passes.
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 6 committed and pushed.

---

## Phase 7 — LaTeX Structure (M7) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T7.1 | Create `latex/main.tex` | ai | ☑ |
| T7.2 | Create `latex/preamble.tex` | ai | ☑ |
| T7.3 | Configure XeLaTeX + biber via latexmk (`-xelatex`) with direct fallback | ai | ☑ |
| T7.4 | Add Hebrew-English BiDi support | ai | ☑ |
| T7.5 | Add cover page | ai | ☑ |
| T7.6 | Add table of contents | ai | ☑ |
| T7.7 | Add headers/footers | ai | ☑ |
| T7.8 | Include `latex/generated/` chapter fragments | ai | ☑ |
| T7.9 | Add bibliography setup with biblatex + biber | ai | ☑ |
| T7.10 | Commit Phase 7 | dev | ☑ |

**Definition of Done:** A basic PDF can compile with cover, TOC, headers/footers, and placeholder/generated chapter structure.

### Phase 7 Completion Notes

- `latex/main.tex`, `latex/preamble.tex`, `latex/references.bib` created.
- Professional infrastructure: titlesec, color palette, tcolorbox macros, chapter banner.
- XeLaTeX + polyglossia BiDi; fancyhdr; biblatex + biber; TikZ/tcolorbox in preamble.
- `scripts/build_pdf.py` is now a thin CLI wrapper.
- Build logic is split into `src/pdf_build.py`, `src/latex_runner.py`, and `src/latex_fragments.py` to satisfy the 150-line file limit.
- `scripts/build_pdf.py` prefers latexmk with `-xelatex`; direct XeLaTeX + biber fallback on Windows/MiKTeX issues.
- Content from `latex/generated/` crew fragments; no static lecture bodies.
- `tests/test_latex_structure.py` passes (no LaTeX install required).
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 7 committed and pushed.

---

## Phase 8 — Required PDF Elements and Design (M8) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T8.1 | Add TikZ workflow/architecture diagram | ai | ☑ |
| T8.2 | Add `scripts/make_figures.py` | ai | ☑ |
| T8.3 | Generate at least one Python graph and include it in LaTeX | ai | ☑ |
| T8.4 | Confirm TikZ diagram and Python graph are both present | dev | ☑ |
| T8.5 | Add at least one table | ai | ☑ |
| T8.6 | Add fancy/highlighted mathematical formula | ai | ☑ |
| T8.7 | Add callout boxes or styled boxes | ai | ☑ |
| T8.8 | Add Hebrew-English BiDi section | ai | ☑ |
| T8.9 | Add linked citations in the text | ai | ☑ |
| T8.10 | Add bibliography | ai | ☑ |
| T8.11 | Commit Phase 8 | dev | ☑ |

**Definition of Done:** All required PDF elements are present in the LaTeX source and appear in a compiled PDF.

### Phase 8 Completion Notes

- `latex/diagrams.tex` — TikZ pipeline diagram (separate from Python graph).
- `scripts/make_figures.py` → `assets/automation_impact_graph.png`.
- `latex/figures.tex`, `tables.tex`, `formulas.tex`, `bidi_section.tex` added.
- Callout boxes used across chapters; crew chapter 1 fragment still included.
- `latex/references.bib` expanded with Phase 5 live research sources; linked `\cite{}` in text.
- All required PDF elements present in LaTeX source.
- `tests/test_pdf_elements.py` passes (no LaTeX install required).
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 8 committed and pushed.

---

## Phase 9 — Compile and Verify PDF (M9) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T9.1 | Add build script | ai | ☑ |
| T9.2 | Compile with XeLaTeX and biber | dev | ☑ |
| T9.3 | Fix LaTeX escaping issues for `&`, `%`, `_`, `#`, URLs, Hebrew/English mixing | ai | ☑ |
| T9.4 | Verify around 15 pages | dev | ☑ |
| T9.5 | Verify cover page, TOC, headers/footers, chapters | dev | ☑ |
| T9.6 | Verify TikZ, Python graph, table, fancy formula, callouts | dev | ☑ |
| T9.7 | Verify BiDi, linked citations, bibliography | dev | ☑ |
| T9.8 | Save final PDF to documented path | ai | ☑ |
| T9.9 | Commit Phase 9 | dev | ☑ |

**Definition of Done:** Single command builds the final PDF and the full verification checklist passes.

### Phase 9 Completion Notes

- `scripts/build_pdf.py` uses XeLaTeX (`latexmk -xelatex` or direct fallback).
- `scripts/verify_pdf_elements.py` remains the thin CLI entry point, while verification logic is split across `src/pdf_checks.py`, `src/pdf_content_checks.py`, `src/pdf_structure_checks.py`, `src/pdf_artifact_checks.py`, `src/pdf_report.py`, and `src/pdf_verification.py`.
- All verification behavior is preserved after the modular refactor.
- `outputs/logs/pdf_verification.md` remains the verification report path.
- Final PDF: `latex/main.pdf` (17 pages, all checklist items PASS; not tracked by git).
- Phase 9 build and verification workflow remains complete after the modular refactor.

---

## Phase 10 — Tests and Quality (M10) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T10.1 | Unit tests for config loading | ai | ☑ |
| T10.2 | Unit tests for missing key errors | ai | ☑ |
| T10.3 | Tests for secret redaction | ai | ☑ |
| T10.4 | Tests for search result parsing | ai | ☑ |
| T10.5 | Tests for LaTeX escaping | ai | ☑ |
| T10.6 | Optional smoke/integration test that does not waste tokens | ai | ☑ |
| T10.7 | Run pytest | dev | ☑ |
| T10.8 | Run ruff check | dev | ☑ |
| T10.9 | Run ruff format check | dev | ☑ |
| T10.10 | Commit Phase 10 | dev | ☑ |
| T10.11 | Refactor oversized Python files so every file in `src/`, `scripts/`, and `tests/` is under 150 lines | ai | ☑ |
| T10.12 | Add line-count evidence screenshot under `docs/screenshots/line_count_pass.png` | dev | ☑ |

**Definition of Done:** Tests pass, ruff passes, and key project helpers are covered.

### Phase 10 Completion Notes

- 96 pytest tests passing.
- `ruff check` and `ruff format --check` pass.
- Every Python file in `src/`, `scripts/`, and `tests/` is under 150 lines.
- Line-count evidence is saved under `docs/screenshots/line_count_pass.png`.
- Phase 10 committed and pushed.

---

## Phase 11 — README and Evidence (M11) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T11.1 | Expand README with setup instructions | ai | ☑ |
| T11.2 | Explain required API keys and `.env` | ai | ☑ |
| T11.3 | Explain live search requirement and no offline/fake mode | ai | ☑ |
| T11.4 | Explain how to run CrewAI pipeline | ai | ☑ |
| T11.5 | Explain how to compile PDF | ai | ☑ |
| T11.6 | Document evidence paths | ai | ☑ |
| T11.7 | Document live internet search evidence path | dev | ☑ |
| T11.8 | Document CrewAI execution evidence path | dev | ☑ |
| T11.9 | Document generated sources/artifacts path | dev | ☑ |
| T11.10 | Document saved research/draft/review artifact paths | dev | ☑ |
| T11.11 | Add PDF compilation evidence | dev | ☑ |
| T11.12 | Add final README screenshot evidence under `docs/screenshots/` | dev | ☑ |
| T11.13 | Commit Phase 11 | dev | ☑ |

**Definition of Done:** README is sufficient for a new developer or grader to run and verify the project.

### Phase 11 Completion Notes

- README includes architecture overview, CrewAI agent design, RAG-style live research, modular architecture, TikZ/PDF design, and screenshots.
- Screenshots are stored under `docs/screenshots/`.
- Screenshot evidence includes: final PDF cover, TikZ workflow diagram, Python graph, required table/formula elements, Hebrew–English BiDi section, PDF verification PASS, cost report, and 150-line source-file check.
- Submission-ready `README.md` with deliverable, required-elements table, quickstart, verification evidence.
- Evidence paths documented: `outputs/research/`, `outputs/drafts/`, `outputs/reviews/`, `latex/generated/`, `outputs/logs/pdf_verification.md`.
- Final submission PDF tracked at `outputs/final/ai_agents_real_work_book.pdf`; `latex/main.pdf` remains local build output.
- Phase 11 committed and pushed.

---

## Phase 12 — Final Submission (M12) — ☑ complete, committed and pushed

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T12.1 | Confirm final PDF meets all PRD requirements | dev | ☑ |
| T12.2 | Confirm live API research evidence exists | dev | ☑ |
| T12.3 | Confirm no static lecture bodies are used as main content source | dev | ☑ |
| T12.4 | Confirm no `.env`, API keys, intermediate PDFs, or course materials are in GitHub; only the final submission PDF is tracked at `outputs/final/ai_agents_real_work_book.pdf` | dev | ☑ |
| T12.4a | Confirm final PDF exists in GitHub at `outputs/final/ai_agents_real_work_book.pdf` | dev | ☑ |
| T12.4b | Confirm verification report exists at `outputs/logs/pdf_verification.md` | dev | ☑ |
| T12.4c | Confirm cost report exists at `outputs/logs/cost_report.md` and `cost_report.json` | dev | ☑ |
| T12.4d | Confirm screenshot evidence exists under `docs/screenshots/` | dev | ☑ |
| T12.4e | Confirm every Python file in `src/`, `scripts/`, and `tests/` is under 150 lines | dev | ☑ |
| T12.4f | Confirm README, PRD, PLAN, and TODO are aligned with the final refactored codebase | dev | ☑ |
| T12.5 | Confirm all phases are committed and pushed | dev | ☑ |
| T12.6 | Confirm GitHub repo is public or shared with lecturer | dev | ☑ |
| T12.7 | Prepare Moodle submission PDF/link with GitHub URL | dev | ☑ |
| T12.8 | Final tag or final commit if needed | dev | ☑ |

**Definition of Done:** Assignment is ready to submit; PDF, code, logs, README, and repository history align with the PRD and course requirements.

### Phase 12 Completion Notes

- Final submission PDF in GitHub: `outputs/final/ai_agents_real_work_book.pdf` (17 pages; verification PASS).
- Local build output `latex/main.pdf` remains gitignored.
- Verification report: `outputs/logs/pdf_verification.md`; cost report: `outputs/logs/cost_report.md` and `cost_report.json`.
- No `.env`, API keys, or course materials tracked in GitHub.
- Final submission commit includes code, docs, screenshots, verification report, cost report, and final PDF.
- Repository submission-ready.

---

## Milestone ↔ Phase Map

| Milestone | Phase |
|-----------|-------|
| M0 | Phase 0 — Planning and Scaffold |
| M0.5 | Phase 0.5 — GitHub Remote and First Push |
| M1 | Phase 1 — Environment and Config |
| M2 | Phase 2 — Live Internet Search Tool |
| M3 | Phase 3 — CrewAI Agents |
| M4 | Phase 4 — Tasks and Context Workflow |
| M5 | Phase 5 — Run Crew per Chapter |
| M6 | Phase 6 — Cost and Token Tracking |
| M7 | Phase 7 — LaTeX Structure |
| M8 | Phase 8 — Required PDF Elements and Design |
| M9 | Phase 9 — Compile and Verify PDF |
| M10 | Phase 10 — Tests and Quality |
| M11 | Phase 11 — README and Evidence |
| M12 | Phase 12 — Final Submission |
