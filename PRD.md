# Product Requirements Document (PRD)

## Living documents

`PRD.md`, `PLAN.md`, and `TODO.md` are living documents. They must be reviewed and updated after every phase so requirements, plan, and checklist stay aligned with the codebase.

## Topic

**AI Agents That Replace Real Work: The Future of Automation**

The system will research, draft, review, and publish a technical mini-book / short book on how AI agents are replacing real human work and what that means for the future of automation.

## Live Internet Research

- All research must use live internet search via API keys (e.g., Serper or equivalent).
- No offline mode, no cached-only research, and no fake or stubbed production data.
- If required API keys are missing at runtime, the program must fail with a clear, actionable error message.

## Planned Production Pipeline

The end-to-end production flow is:

```
Live Internet Search via API
  → Researcher Agent
  → Writer Agent
  → Reviewer Agent
  → LaTeX Builder
  → PDF Compile
  → Verification Checklist
```

- **Live Internet Search via API:** Serper (or equivalent) supplies real-time research data; no offline substitute.
- **Researcher Agent:** Gathers and summarizes findings from live search results.
- **Writer Agent:** Drafts chapter/section content from research notes.
- **Reviewer Agent:** Reviews drafts for accuracy, clarity, and alignment with the topic.
- **LaTeX Builder:** Assembles agent output and static elements into `latex/` and `latex/generated/`.
- **PDF Compile:** Builds the final PDF via XeLaTeX + biber, using latexmk when available and a direct XeLaTeX fallback on Windows.
- **Verification Checklist:** Confirms page count, required elements, and design quality before submission.

## Content Source Rule

- The book must be generated from live research artifacts (search results, agent drafts, reviews), not from static lecture bodies or hardcoded course PDFs.
- Course materials are not part of the repository and are not used as the production content source.

## CrewAI Agents

- The system must be built with CrewAI.
- Explicit agents aligned with the production pipeline:
  - **Researcher Agent** — live internet search and research synthesis
  - **Writer Agent** — drafts from research context
  - **Reviewer Agent** — accuracy, clarity, citations, topic alignment
  - **LaTeX Builder Agent or service** — prepares reviewed content for `latex/generated/`
- Python code must remain small, modular, and organized under `src/`.

## LaTeX PDF Output

- The final deliverable is a polished LaTeX-compiled PDF (approximately 15 pages).
- The final submission PDF must be available in GitHub at `outputs/final/ai_agents_real_work_book.pdf`.
- `latex/main.pdf` remains the local build output.
- Source lives under `latex/`; generated LaTeX fragments under `latex/generated/`.

### PDF Design Requirements

The PDF must be visually polished, not a plain text dump:

- Clear chapter structure with consistent headings and spacing.
- Headers and footers on body pages.
- Callout boxes or styled boxes for key insights, warnings, or definitions.
- Fancy/highlighted LaTeX formulas (e.g., `tcolorbox`, `mdframed`, or equivalent)—not plain inline text masquerading as formulas.
- At least one **TikZ** architecture or workflow diagram (e.g., agentic workflow, agent pipeline, or system architecture).
- At least one **Python-generated graph** produced by `scripts/make_figures.py` and included in the PDF.
- **TikZ diagrams and the Python-generated graph are both required**; one does not replace the other.

### Required PDF Elements

The final PDF must include:

1. Cover page
2. Table of contents
3. Headers and footers
4. Chapters
5. At least one TikZ architecture/workflow diagram
6. At least one Python-generated graph (from `scripts/make_figures.py`)
7. At least one table
8. At least one fancy/highlighted mathematical formula (not plain-text)
9. At least one Hebrew–English BiDi section
10. Linked citations in the text
11. Bibliography
12. Callout boxes or styled boxes as part of the document design

## No Offline Mode

- The system must not support a production fallback that skips live research or uses hardcoded article content. Tests may use mocks or fixtures, but production research must require live API-backed search.

## No Committed Secrets

- Real API keys must never be committed to GitHub.
- Secrets are loaded from `.env` only; `.env.example` contains placeholders only.
- Only the final submission PDF may be tracked; intermediate/generated PDFs should remain ignored.

## Generated Evidence and Logs

- Research notes, drafts, reviews, logs, and other run artifacts must be written to `outputs/` (e.g., `outputs/research/`, `outputs/drafts/`, `outputs/reviews/`, `outputs/logs/`).
- These outputs serve as evidence of the live research and agent workflow for assignment submission.

## Tooling

- **uv** for Python dependency and environment management
- **Python** for agents, tools, and graph generation
- **CrewAI** for multi-agent orchestration
- **LaTeX** for PDF production
- **GitHub** for version control with small, phase-based commits
