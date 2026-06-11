# TODO Checklist

Track progress phase by phase. Check items only when the phase Definition of Done is satisfied.

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

---


## Phase 0 — Planning and Scaffold

- [x] Create folder structure (`src/`, `scripts/`, `latex/`, `latex/generated/`, `assets/`, `outputs/`, `docs/`, `tests/`, `_course_materials/`)
- [x] Add `README.md` (stub)
- [x] Add `PRD.md`
- [x] Add `PLAN.md`
- [x] Add `TODO.md` (this file)
- [x] Add `.gitignore` with required patterns (including `_course_materials/` and `*.pdf`)
- [x] Add `.env.example` with placeholders only
- [x] Move course PDFs from repo root into `_course_materials/`
- [ ] Commit Phase 0 to Git

**Definition of Done (Phase 0):** Repository scaffold exists; planning docs are complete; no application code; no secrets; ready for Phase 1 approval.

### Phase 0 Completion Notes

- Scaffold created: `src/`, `scripts/`, `latex/`, `latex/generated/`, `assets/`, `outputs/` (research, drafts, reviews, logs), `docs/`, `tests/`, `_course_materials/`.
- No application code added.
- No dependencies installed (`pyproject.toml` not created).
- Course PDFs moved from workspace root into `_course_materials/`; folder and `*.pdf` are gitignored.
- Secrets are not committed; `.env.example` has placeholders only; `.env` is gitignored.
- Git repository not yet initialized; Phase 0 commit pending.

---

## Phase 1 — Environment and Config

- [ ] Add `pyproject.toml` and configure uv
- [ ] Add dependencies (CrewAI, etc.)
- [ ] Implement config module in `src/` to load env vars
- [ ] Fail fast with clear error when API keys are missing
- [ ] Document local setup in README or `docs/`
- [ ] Commit Phase 1

**Definition of Done (Phase 1):** `uv sync` works; config loads from `.env`; missing keys produce a clear runtime error; no secrets in repo.

---

## Phase 2 — Live Search Tool

- [ ] Implement internet search tool (Serper API) in `src/`
- [ ] Tool is CrewAI-compatible
- [ ] Add minimal test script in `scripts/` for one live search
- [ ] Save sample search output to `outputs/research/`
- [ ] Commit Phase 2

**Definition of Done (Phase 2):** One real API search succeeds with valid keys; output saved as evidence; tool ready for agents.

---

## Phase 3 — CrewAI Agents

- [ ] Define agent roles (researcher, writer, editor, etc.) in modular files
- [ ] Connect researcher to live search tool
- [ ] Keep each Python file small and focused
- [ ] Commit Phase 3

**Definition of Done (Phase 3):** Agents are defined and importable; researcher uses live search; no hardcoded secrets.

---

## Phase 4 — Tasks and Context Workflow

- [ ] Define CrewAI tasks and dependencies
- [ ] Implement shared context between agents
- [ ] Document workflow in code or `docs/`
- [ ] Commit Phase 4

**Definition of Done (Phase 4):** Task graph is defined; context flows between tasks; workflow is documented.

---

## Phase 5 — Run Crew per Chapter

- [ ] Orchestrate crew execution per chapter/section
- [ ] Write drafts to `outputs/drafts/`
- [ ] Write research artifacts to `outputs/research/`
- [ ] Add entry script (e.g., `scripts/run_crew.py`)
- [ ] Commit Phase 5

**Definition of Done (Phase 5):** End-to-end crew run produces chapter drafts from live research; artifacts on disk.

---

## Phase 6 — Cost and Token Tracking

- [ ] Track tokens and estimated cost per run/agent
- [ ] Persist logs to `outputs/logs/`
- [ ] Commit Phase 6

**Definition of Done (Phase 6):** Each run records usage metrics; logs are readable and stored under `outputs/logs/`.

---

## Phase 7 — LaTeX Structure

- [ ] Main LaTeX document under `latex/`
- [ ] Preamble, chapter templates, headers/footers
- [ ] `latex/generated/` for agent-generated fragments
- [ ] Cover page and table of contents scaffolding
- [ ] Commit Phase 7

**Definition of Done (Phase 7):** LaTeX project compiles to a basic PDF with cover, TOC, and chapter structure.

---

## Phase 8 — Required PDF Elements

- [ ] TikZ workflow/architecture diagram included
- [ ] `scripts/make_figures.py` creates Python-generated graph and graph is included in LaTeX
- [ ] TikZ diagram and Python graph both present (neither replaces the other)
- [ ] At least one table
- [ ] Fancy/highlighted formula included (not plain-text)
- [ ] PDF design includes callouts or styled boxes
- [ ] At least one Hebrew–English BiDi section
- [ ] Linked citations in text
- [ ] Bibliography
- [ ] Commit Phase 8

**Definition of Done (Phase 8):** All required PDF elements and design requirements are present in source and appear in a compiled build.

---

## Phase 9 — Compile and Verify PDF

- [ ] Add compile script in `scripts/`
- [ ] Full build produces PDF (~15 pages)
- [ ] Final verification confirms TikZ, Python graph, table, formula, BiDi, citations, bibliography
- [ ] Final verification confirms callout/styled box design and headers/footers
- [ ] Commit Phase 9

**Definition of Done (Phase 9):** Single command builds PDF; page count and full verification checklist passed; PDF stored in `outputs/` or documented path.

---

## Phase 10 — Tests and Quality

- [ ] Unit tests for config and search tool
- [ ] Tests for critical helpers
- [ ] Optional smoke/integration test
- [ ] All tests pass via pytest
- [ ] Commit Phase 10

**Definition of Done (Phase 10):** `pytest` passes; core modules have meaningful test coverage.

---

## Phase 11 — README and Evidence

- [ ] Expand README with setup, env vars, and run instructions
- [ ] Document evidence paths (`outputs/research/`, drafts, logs)
- [ ] Include screenshots or sample log references if required
- [ ] Commit Phase 11

**Definition of Done (Phase 11):** README is sufficient for a new developer to run the project; evidence of live runs is documented.

---

## Phase 12 — Final Submission

- [ ] Final PDF meets all PRD requirements (pipeline evidence + PDF design)
- [ ] TikZ workflow/architecture diagram included
- [ ] Python-generated graph created by script and included
- [ ] Fancy/highlighted formula included
- [ ] PDF design includes callouts or styled boxes
- [ ] Final verification confirms TikZ, Python graph, table, formula, BiDi, citations, bibliography
- [ ] No secrets in repo or git history
- [ ] All phases complete and committed
- [ ] Submission checklist signed off
- [ ] Commit or tag final submission

**Definition of Done (Phase 12):** Assignment ready to submit; PDF, code, logs, and docs align with PRD and course requirements.
