# CrewAI Task Workflow (Phase 4)

## Pipeline

```
Live Internet Search (Researcher tool)
  → Research Task
  → Writing Task
  → Review Task
  → LaTeX Task
```

Agents:

1. **Researcher Agent** — runs live Serper search via `live_internet_search` tool
2. **Writer Agent** — drafts from research notes only
3. **Reviewer Agent** — checks accuracy, clarity, citations, topic alignment
4. **LaTeX Builder Agent** — prepares reviewed prose for `latex/generated/`

## Context flow

| Task | Receives context from | Produces |
|------|----------------------|----------|
| Research | — (uses live search tool) | Research notes with sources |
| Writing | Research Task | Chapter draft |
| Review | Research Task + Writing Task | Editorial review |
| LaTeX | Review Task | LaTeX-ready fragments |

Context is wired with CrewAI `context=[...]` on each downstream task.

## Code map

- `src/task_config.py` — task descriptions and expected outputs
- `src/tasks.py` — `create_research_task`, `create_writing_task`, `create_review_task`, `create_latex_task`
- `src/crew_factory.py` — `create_book_crew(topic_or_chapter)` returns a sequential `Crew`

## Phase boundaries

- **Phase 4 (this document):** Defines tasks, context links, and crew factory. No `kickoff()`.
- **Phase 5:** Runs `create_book_crew()` per chapter, saves artifacts to `outputs/` and `latex/generated/`.

## Constraints

- Live API-based research only; no offline or fake production mode.
- No static lecture bodies or course PDFs as primary content.
- API keys loaded from `.env`; never printed or committed.
