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
- **Next:** M3 - CrewAI Agents.

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
