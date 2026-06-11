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

**Overall:** ☑ Phase 2 complete locally; ready for Phase 3.  
**Current milestone:** M3 — CrewAI Agents.  
**Next milestone:** M4 — Tasks and Context Workflow.

- Live Serper search client saves evidence to `outputs/research/`.
- `pytest` and `ruff` pass; live search script uses real `SERPER_API_KEY` from `.env`.
- Course PDFs are local-only under `_course_materials/` and ignored by git.
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

- ☐ Before each phase, read `PRD.md`, `PLAN.md`, and `TODO.md`.
- ☐ During each phase, update `TODO.md` with current progress.
- ☐ After each phase, mark completed tasks.
- ☐ If requirements changed, update `PRD.md`.
- ☐ If implementation strategy changed, update `PLAN.md`.
- ☐ Add Phase Completion Notes after every phase.
- ☐ Commit documentation updates together with the phase implementation.

---

## Phase 0 — Planning and Scaffold (M0) — ☑ complete locally

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T0.1 | Create repository scaffold and folders | ai | ☑ |
| T0.2 | Add `README.md` stub | ai | ☑ |
| T0.3 | Write `PRD.md` | ai | ☑ |
| T0.4 | Write `PLAN.md` | ai | ☑ |
| T0.5 | Write `TODO.md` | ai | ☑ |
| T0.6 | Add `.gitignore` with `_course_materials/`, `*.pdf`, `.env`, `.venv/`, caches | ai | ☑ |
| T0.7 | Add `.env.example` placeholders only | ai | ☑ |
| T0.8 | Store course PDFs locally under `_course_materials/` | dev | ☑ |
| T0.9 | Commit Phase 0 locally | dev | ☑ |

**Definition of Done:** Repository scaffold exists; planning docs are complete; no application code; no secrets; ready for GitHub push.

### Phase 0 Completion Notes

- Scaffold created.
- No application code added.
- No dependencies installed.
- Course PDFs are local-only and ignored.
- Secrets are not committed.
- Phase 0 committed locally.
- GitHub push pending.

---

## Phase 0.5 — GitHub Remote and First Push (M0.5) — ☑ complete

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T0.5.1 | Create GitHub repository | dev | ☑ |
| T0.5.2 | Rename local branch to `main` | dev | ☑ |
| T0.5.3 | Add GitHub remote | dev | ☑ |
| T0.5.4 | Push Phase 0 commit to GitHub | dev | ☑ |
| T0.5.5 | Confirm GitHub does not contain `.env`, PDFs, or `_course_materials/` | dev | ☑ |
| T0.5.6 | Commit/push documentation cleanup if needed | dev | ☑ |

**Definition of Done:** Phase 0 commit exists on GitHub, repository is accessible, and private/course files are not uploaded.

### Phase 0.5 Completion Notes

- GitHub repository created.
- Local branch is `main`.
- Remote `origin` points to the GitHub repository.
- Phase 0 commits pushed successfully.
- Private files are ignored: `.env`, PDFs, `_course_materials/`.
- Ready for Phase 1.

---

## Phase 1 — Environment and Config (M1) — ☑ complete locally

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
| T1.12 | Commit Phase 1 | dev | ☐ |

**Definition of Done:** `uv sync` works, config loads from `.env`, missing keys produce a clear error, no secrets are committed.

### Phase 1 Completion Notes

- `pyproject.toml` created with Python >=3.11 and required dependencies.
- `uv.lock` generated via `uv sync`.
- `src/config.py` loads `.env`, validates API keys, defaults `MODEL_NAME` to `gpt-4o-mini`.
- `src/redaction.py` redacts `sk-*` patterns and explicit secrets.
- `scripts/check_config.py` prints safe status only (no key values).
- Tests cover missing keys, placeholder rejection, success with fake env, and redaction.
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 1 commit pending.

---

## Phase 2 — Live Internet Search Tool (M2) — ☑ complete locally

Serper API or equivalent. Real API search. Save raw search evidence. No offline/fake mode.

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T2.1 | Implement Serper search client (`SerperSearchClient`) | ai | ☑ |
| T2.2 | Add minimal live search script | ai | ☑ |
| T2.3 | Save raw search output to `outputs/research/` | ai | ☑ |
| T2.4 | Extract title, URL, snippet, and date if available | ai | ☑ |
| T2.5 | Validate at least one real search succeeds with valid keys | dev | ☑ |
| T2.6 | Update README with search usage | ai | ☑ |
| T2.7 | Commit Phase 2 | dev | ☐ |

**Definition of Done:** One real API search succeeds, output is saved as evidence, and the search tool is ready for the Researcher Agent.

### Phase 2 Completion Notes

- `src/search_models.py` — `SearchResult` and `SearchResponse` Pydantic models.
- `src/search_tool.py` — `SerperSearchClient` using httpx and Serper Google search endpoint.
- `scripts/run_live_search.py` — live search with safe summary and JSON evidence output.
- `tests/test_search_tool.py` — mocked HTTP tests only; no real API calls in tests.
- Live search validated with real `SERPER_API_KEY`; evidence saved under `outputs/research/`.
- `pytest`, `ruff check`, and `ruff format --check` pass.
- Phase 2 commit pending.

---

## Phase 3 — CrewAI Agents (M3) — ☐ not started

Explicit agents: Researcher Agent, Writer Agent, Reviewer Agent, LaTeX Builder Agent or LaTeX Builder service.

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T3.1 | Create modular agent definitions | ai | ☐ |
| T3.2 | Researcher uses the live search tool | ai | ☐ |
| T3.3 | Writer uses research context, not static lecture bodies | ai | ☐ |
| T3.4 | Reviewer checks accuracy, clarity, citations, and topic alignment | ai | ☐ |
| T3.5 | LaTeX Builder prepares reviewed output for LaTeX | ai | ☐ |
| T3.6 | Keep Python files small and focused | ai | ☐ |
| T3.7 | Commit Phase 3 | dev | ☐ |

**Definition of Done:** Agents are importable, roles are clear, Researcher uses live search, and no agent relies on hardcoded book content.

---

## Phase 4 — Tasks and Context Workflow (M4) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T4.1 | Define Research Task | ai | ☐ |
| T4.2 | Define Writing Task | ai | ☐ |
| T4.3 | Define Review Task | ai | ☐ |
| T4.4 | Define LaTeX Task | ai | ☐ |
| T4.5 | Use context from previous tasks | ai | ☐ |
| T4.6 | Use sequential process unless a later reason justifies a change | ai | ☐ |
| T4.7 | Document workflow in `docs/` | ai | ☐ |
| T4.8 | Commit Phase 4 | dev | ☐ |

**Definition of Done:** Research → Write → Review → LaTeX task flow is defined and context passes correctly between tasks.

---

## Phase 5 — Run Crew per Chapter (M5) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T5.1 | Define final chapter list | ai | ☐ |
| T5.2 | Create `scripts/run_crew.py` | ai | ☐ |
| T5.3 | Run the full crew pipeline once per chapter or section | dev | ☐ |
| T5.4 | Save research artifacts to `outputs/research/` | ai | ☐ |
| T5.5 | Save drafts to `outputs/drafts/` | ai | ☐ |
| T5.6 | Save reviews to `outputs/reviews/` | ai | ☐ |
| T5.7 | Save generated LaTeX fragments to `latex/generated/` | ai | ☐ |
| T5.8 | Save run logs to `outputs/logs/` | ai | ☐ |
| T5.9 | Commit Phase 5 | dev | ☐ |

**Definition of Done:** End-to-end crew run produces chapter content from live research, with evidence artifacts saved on disk.

---

## Phase 6 — Cost and Token Tracking (M6) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T6.1 | Add token/cost estimation helper | ai | ☐ |
| T6.2 | Track usage per run and per agent where possible | ai | ☐ |
| T6.3 | Save cost report to `outputs/logs/` | ai | ☐ |
| T6.4 | Add budget warning before expensive live runs | ai | ☐ |
| T6.5 | Document cost tracking in README | ai | ☐ |
| T6.6 | Commit Phase 6 | dev | ☐ |

**Definition of Done:** Each run records readable usage/cost information or a clear estimate.

---

## Phase 7 — LaTeX Structure (M7) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T7.1 | Create `latex/main.tex` | ai | ☐ |
| T7.2 | Create `latex/preamble.tex` | ai | ☐ |
| T7.3 | Configure LuaLaTeX or XeLaTeX, preferably through latexmk | ai | ☐ |
| T7.4 | Add Hebrew-English BiDi support | ai | ☐ |
| T7.5 | Add cover page | ai | ☐ |
| T7.6 | Add table of contents | ai | ☐ |
| T7.7 | Add headers/footers | ai | ☐ |
| T7.8 | Include `latex/generated/` chapter fragments | ai | ☐ |
| T7.9 | Add bibliography setup with biber/BibTeX | ai | ☐ |
| T7.10 | Commit Phase 7 | dev | ☐ |

**Definition of Done:** A basic PDF can compile with cover, TOC, headers/footers, and placeholder/generated chapter structure.

---

## Phase 8 — Required PDF Elements and Design (M8) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T8.1 | Add TikZ workflow/architecture diagram | ai | ☐ |
| T8.2 | Add `scripts/make_figures.py` | ai | ☐ |
| T8.3 | Generate at least one Python graph and include it in LaTeX | ai | ☐ |
| T8.4 | Confirm TikZ diagram and Python graph are both present | dev | ☐ |
| T8.5 | Add at least one table | ai | ☐ |
| T8.6 | Add fancy/highlighted mathematical formula | ai | ☐ |
| T8.7 | Add callout boxes or styled boxes | ai | ☐ |
| T8.8 | Add Hebrew-English BiDi section | ai | ☐ |
| T8.9 | Add linked citations in the text | ai | ☐ |
| T8.10 | Add bibliography | ai | ☐ |
| T8.11 | Commit Phase 8 | dev | ☐ |

**Definition of Done:** All required PDF elements are present in the LaTeX source and appear in a compiled PDF.

---

## Phase 9 — Compile and Verify PDF (M9) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T9.1 | Add build script | ai | ☐ |
| T9.2 | Compile with LuaLaTeX/XeLaTeX and biber | dev | ☐ |
| T9.3 | Fix LaTeX escaping issues for `&`, `%`, `_`, `#`, URLs, Hebrew/English mixing | ai | ☐ |
| T9.4 | Verify around 15 pages | dev | ☐ |
| T9.5 | Verify cover page, TOC, headers/footers, chapters | dev | ☐ |
| T9.6 | Verify TikZ, Python graph, table, fancy formula, callouts | dev | ☐ |
| T9.7 | Verify BiDi, linked citations, bibliography | dev | ☐ |
| T9.8 | Save final PDF to documented path | ai | ☐ |
| T9.9 | Commit Phase 9 | dev | ☐ |

**Definition of Done:** Single command builds the final PDF and the full verification checklist passes.

---

## Phase 10 — Tests and Quality (M10) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T10.1 | Unit tests for config loading | ai | ☐ |
| T10.2 | Unit tests for missing key errors | ai | ☐ |
| T10.3 | Tests for secret redaction | ai | ☐ |
| T10.4 | Tests for search result parsing | ai | ☐ |
| T10.5 | Tests for LaTeX escaping | ai | ☐ |
| T10.6 | Optional smoke/integration test that does not waste tokens | ai | ☐ |
| T10.7 | Run pytest | dev | ☐ |
| T10.8 | Run ruff check | dev | ☐ |
| T10.9 | Run ruff format check | dev | ☐ |
| T10.10 | Commit Phase 10 | dev | ☐ |

**Definition of Done:** Tests pass, ruff passes, and key project helpers are covered.

---

## Phase 11 — README and Evidence (M11) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T11.1 | Expand README with setup instructions | ai | ☐ |
| T11.2 | Explain required API keys and `.env` | ai | ☐ |
| T11.3 | Explain live search requirement and no offline/fake mode | ai | ☐ |
| T11.4 | Explain how to run CrewAI pipeline | ai | ☐ |
| T11.5 | Explain how to compile PDF | ai | ☐ |
| T11.6 | Document evidence paths | ai | ☐ |
| T11.7 | Add live internet search run evidence | dev | ☐ |
| T11.8 | Add CrewAI execution evidence | dev | ☐ |
| T11.9 | Add generated sources evidence | dev | ☐ |
| T11.10 | Add saved research/draft/review artifact evidence | dev | ☐ |
| T11.11 | Add PDF compilation evidence | dev | ☐ |
| T11.12 | Add terminal logs or screenshots | dev | ☐ |
| T11.13 | Commit Phase 11 | dev | ☐ |

**Definition of Done:** README is sufficient for a new developer or grader to run and verify the project.

---

## Phase 12 — Final Submission (M12) — ☐ not started

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T12.1 | Confirm final PDF meets all PRD requirements | dev | ☐ |
| T12.2 | Confirm live API research evidence exists | dev | ☐ |
| T12.3 | Confirm no static lecture bodies are used as main content source | dev | ☐ |
| T12.4 | Confirm no `.env`, PDFs, or `_course_materials/` are in GitHub | dev | ☐ |
| T12.5 | Confirm all phases are committed and pushed | dev | ☐ |
| T12.6 | Confirm GitHub repo is public or shared with lecturer | dev | ☐ |
| T12.7 | Prepare Moodle submission PDF/link with GitHub URL | dev | ☐ |
| T12.8 | Final tag or final commit if needed | dev | ☐ |

**Definition of Done:** Assignment is ready to submit; PDF, code, logs, README, and repository history align with the PRD and course requirements.

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
