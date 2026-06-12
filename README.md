# AI Agents That Replace Real Work: The Future of Automation

**Product:** `ai-agents-real-work-book`  
**Topic:** AI Agents That Replace Real Work - The Future of Automation

A CrewAI-based system that researches live internet sources and produces a polished technical article or book as a LaTeX PDF.

**GitHub:** https://github.com/Emansa12/ai-agents-real-work-book

## Current status

- **Phase 0 (M0):** Complete - scaffold, PRD, PLAN, TODO, `.gitignore`, `.env.example`.
- **Phase 0.5 (M0.5):** Complete - repository pushed to GitHub on branch `main`.
- **Phase 1 (M1):** Complete - uv environment, config loading, secret redaction, tests.
- **Phase 2 (M2):** Complete - live Serper internet search, evidence saved to `outputs/research/`.
- **Phase 3 (M3):** Complete - modular CrewAI agents defined (committed).
- **Phase 4 (M4):** Complete - task workflow and crew factory (committed).
- **Phase 5 (M5):** Complete locally - per-chapter crew runner and artifacts; commit pending.
- **Next:** M6 - Cost and Token Tracking.

## Setup (Phase 1)

### 1. Install uv

Install [uv](https://docs.astral.sh/uv/) if it is not already on your system.

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set real values for:

- `OPENAI_API_KEY`
- `SERPER_API_KEY`
- `MODEL_NAME` (optional; defaults to `gpt-4o-mini`)

**Important:** `.env` is gitignored. Never commit `.env` or real API keys to GitHub.

### 4. Verify configuration

```bash
uv run python scripts/check_config.py
```

Expected on success:

- `Config loaded successfully`
- Model name printed
- `OPENAI_API_KEY: present` and `SERPER_API_KEY: present` (values are never printed)

If keys are missing or still placeholders, the script exits with a clear error.

### 5. Run tests and lint

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Live search (Phase 2)

Run one live internet search using `SERPER_API_KEY` from `.env`:

```bash
uv run python scripts/run_live_search.py
```

Pass a custom query:

```bash
uv run python scripts/run_live_search.py "AI agents automation jobs"
```

The script prints a safe summary only (query, result count, titles, and URLs). API keys are never printed.

Evidence is saved to `outputs/research/live_search_<timestamp>.json` with normalized results and the raw Serper response.

**Requires:** valid `SERPER_API_KEY` in `.env`. No offline or fake search mode.

## CrewAI agents (Phase 3)

Modular agents are defined in `src/agents.py`:

- **Researcher Agent** - uses the live internet search CrewAI tool (`src/search_adapter.py`)
- **Writer Agent** - writes from research context (not static lecture bodies)
- **Reviewer Agent** - checks accuracy, clarity, citations, and topic alignment
- **LaTeX Builder Agent** - prepares reviewed content for LaTeX fragments

Agents are **not executed** in Phase 3. The full Research → Write → Review → LaTeX task workflow is implemented in Phase 4.

## Task workflow (Phase 4)

Sequential task chain in `src/tasks.py` and `src/crew_factory.py`:

1. **Research Task** - live source-backed research (Researcher + Serper tool)
2. **Writing Task** - draft from research context (`context=[research_task]`)
3. **Review Task** - accuracy, clarity, citations, topic alignment
4. **LaTeX Task** - LaTeX-ready fragments from reviewed content

`create_book_crew(topic_or_chapter)` builds a sequential `Crew` but does **not** call `kickoff()`.

See `docs/workflow.md` for context flow details.

## Run crew per chapter (Phase 5)

**Warning:** These commands use live OpenAI and Serper API calls.

Default (chapter 1 only):

```bash
uv run python scripts/run_crew.py
```

Specific chapter:

```bash
uv run python scripts/run_crew.py --chapter 2
```

All chapters (explicit opt-in; many API calls):

```bash
uv run python scripts/run_crew.py --all
```

- Default runs **one chapter only** (chapter 1).
- `--all` is never run automatically.
- Artifacts saved under `outputs/research/`, `outputs/drafts/`, `outputs/reviews/`, `outputs/logs/`, and `latex/generated/`.

## Live research requirement

This project requires live API-based internet research. There is no offline or fake production mode. If required API keys are missing at runtime, the program must fail with a clear error.

The book must be generated from live research artifacts, not from static lecture bodies.

## Local-only materials

- `_course_materials/` holds local course reference PDFs and related files. It is for your machine only and is not part of the submitted project.
- PDFs and course materials are ignored by Git (see `.gitignore`) and must not be committed.

## Secrets

- Real API keys belong only in a local `.env` file (copy from `.env.example`).
- `.env.example` contains placeholders only.
- Never commit `.env` or real keys to GitHub.

## Documentation

- `PRD.md` - product requirements
- `PLAN.md` - implementation phases (M0-M12)
- `TODO.md` - task tracking with milestones and Definition of Done
