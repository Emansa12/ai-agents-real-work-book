# AI Agents That Replace Real Work: The Future of Automation

**Product:** `ai-agents-real-work-book`  
**Topic:** AI Agents That Replace Real Work — The Future of Automation

A CrewAI-based system that researches live internet sources and produces a polished technical article or book as a LaTeX PDF.

**GitHub:** https://github.com/Emansa12/ai-agents-real-work-book

## Current status

- **Phase 0 (M0):** Complete — scaffold, PRD, PLAN, TODO, `.gitignore`, `.env.example`, README.
- **Phase 0.5 (M0.5):** Complete — repository pushed to GitHub on branch `main`.
- **Ready for:** M1 — Environment and Config.

No application code yet. No dependencies installed yet.

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

- `PRD.md` — product requirements
- `PLAN.md` — implementation phases (M0–M12)
- `TODO.md` — task tracking with milestones and Definition of Done
