# Implementation Plan

High-level phases for building the system incrementally. Each phase should be completed in a small, reviewable Git commit before moving to the next.

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

Phases 2–9 implement and validate this pipeline step by step. Phase 9 closes with the verification checklist (TikZ diagram, Python graph, table, fancy formula, BiDi, citations, bibliography, callout design).

## Phase 0 — Planning and Scaffold

- Repository folder structure, PRD, plan, TODO, `.gitignore`, `.env.example`, and stub README.
- No application code yet.

## Phase 1 — Environment and Config

- `pyproject.toml` with uv; dependency on CrewAI and related packages.
- Config module to load settings from environment variables.
- Fail fast with clear errors when required keys are missing.

## Phase 2 — Live Search Tool

- Implement a CrewAI-compatible tool that queries the internet via Serper (or chosen API).
- Validate with a minimal script that performs one real search.

## Phase 3 — CrewAI Agents

- Define agent roles (researcher, writer, reviewer) in modular Python files.
- Wire the researcher to the live search tool.

## Phase 4 — Tasks and Context Workflow

- Define CrewAI tasks, task dependencies, and shared context between agents.
- Document the workflow in code and/or `docs/`.

## Phase 5 — Run Crew per Chapter

- Orchestrate crew runs to produce content per chapter or section.
- Save intermediate outputs to `outputs/drafts/` and `outputs/research/`.

## Phase 6 — Cost and Token Tracking

- Track API usage (tokens, estimated cost) per run and per agent.
- Persist summaries to `outputs/logs/`.

## Phase 7 — LaTeX Structure

- Main LaTeX document, preamble, chapter templates, and `latex/generated/` for agent output.
- Cover page, TOC, headers/footers scaffolding.
- Preamble setup for TikZ, fancy formulas, and callout/styled boxes.

## Phase 8 — Required PDF Elements

- TikZ architecture/workflow diagram (does not replace the Python graph).
- `scripts/make_figures.py` to generate at least one graph; include output in LaTeX.
- Table, fancy/highlighted formula, Hebrew–English BiDi section, linked citations, and bibliography.
- Callout boxes or styled boxes for polished document design.

## Phase 9 — Compile and Verify PDF

- Build script (e.g., `scripts/compile_pdf.sh` or equivalent) using LuaLaTeX or XeLaTeX, preferably through latexmk.
- Run verification checklist: TikZ diagram, Python graph, table, fancy formula, BiDi, citations, bibliography, callout design, and ~15 pages.

## Phase 10 — Tests and Quality

- Unit tests for config, search tool, and critical helpers.
- Smoke test or integration test path where feasible.

## Phase 11 — README and Evidence

- Expand README with setup, run instructions, and evidence of live runs.
- Document required API keys and example outputs.

## Phase 12 — Final Submission

- Final PDF, clean repo state, submission checklist complete.
- All phases merged; no secrets in history.
