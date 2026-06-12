# AI Agents That Replace Real Work · CrewAI → Live Research → LaTeX

**AI Agents That Replace Real Work: The Future of Automation**

| | |
|---|---|
| **Authors** | Eman Sarhan, Amir Fadila |
| **Course** | Orchestration of AI Agents |
| **Lecturer** | Dr. Yoram Segal |
| **Repository** | [github.com/Emansa12/ai-agents-real-work-book](https://github.com/Emansa12/ai-agents-real-work-book) |

`Python 3.11+` · `uv` · `CrewAI` · `XeLaTeX` · `Tests 96 passing`

---

This project demonstrates a production-style AI-agent workflow. A CrewAI team performs **live internet research**, writes and reviews chapter content, and prepares LaTeX fragments that compile into a professionally typeset mini-book. The book focuses on how AI agents change **real work** through task-level automation, human-in-the-loop supervision, workflow orchestration, risks, metrics, and bilingual Hebrew–English terminology for agent platforms.

The pipeline is end-to-end: topic in, evidence-backed prose out, then XeLaTeX + biber produce a submission-ready PDF. The production content path is designed around live research artifacts and reviewed agent drafts.

---

## Final deliverable

| Item | Detail |
|---|---|
| **Final PDF in GitHub** | `outputs/final/ai_agents_real_work_book.pdf` |
| **Local build output** | `latex/main.pdf` |
| **Build command** | `uv run python scripts/build_pdf.py` |
| **Page count** | 17 pages (verified) |
| **Verification** | `uv run python scripts/verify_pdf_elements.py` |
| **Report** | `outputs/logs/pdf_verification.md` |

The repository includes the final submission PDF at `outputs/final/ai_agents_real_work_book.pdf`. The local LaTeX build output remains `latex/main.pdf`; after rebuilding, copy the refreshed PDF to `outputs/final/ai_agents_real_work_book.pdf` before final submission.

---

## Required elements

| Required element | Where it is implemented | Verification |
|---|---|---|
| Cover page | `latex/main.tex` | `scripts/verify_pdf_elements.py` — PASS |
| TOC + chapters | `latex/main.tex` | PASS |
| Headers/footers | `latex/preamble.tex` | PASS |
| TikZ diagram | `latex/diagrams.tex` | PASS |
| Python graph | `scripts/make_figures.py`, `assets/automation_impact_graph.png`, `latex/figures.tex` | PASS |
| Table | `latex/tables.tex` | PASS |
| Highlighted formula | `latex/formulas.tex` | PASS |
| Hebrew–English BiDi | `latex/bidi_section.tex`, `latex/preamble.tex` | PASS |
| Citations / bibliography | `latex/references.bib`, biblatex + biber | PASS |
| Callout boxes | `latex/preamble.tex`, chapter files | PASS |
| No secrets in sources | `.env` gitignored, verification scan | PASS |

---

## How it works

```
Topic
  ↓
Researcher Agent
  ↓ live Serper search
Writer Agent
  ↓
Reviewer Agent
  ↓
LaTeX Builder Agent
  ↓
XeLaTeX + biber
  ↓
latex/main.pdf + outputs/logs/pdf_verification.md
```

| Agent | Role | Output |
|---|---|---|
| **Researcher** | Live internet research via Serper | Structured research notes with titles, URLs, snippets |
| **Writer** | Draft chapter prose from research only | Chapter draft with citation placeholders |
| **Reviewer** | Accuracy, clarity, citations, topic alignment | Editorial review and fix list |
| **LaTeX Builder** | Safe LaTeX fragments (XeLaTeX/BiDi-aware) | `latex/generated/*.tex` |

Sequential tasks and shared context are defined in `src/tasks.py` and `src/crew_factory.py`. See `docs/workflow.md` for context flow details.

---

## Repository structure

```
ai-agents-real-work-book/
├── src/                 # CrewAI agents, tasks, search adapter, cost tracking
├── scripts/             # run_crew, build_pdf, verify_pdf_elements, make_figures, …
├── latex/               # main.tex, preamble, diagrams, figures, tables, formulas, BiDi
├── assets/              # Python-generated graph (automation_impact_graph.png)
├── outputs/             # research, drafts, reviews, logs (including verification report)
├── tests/               # pytest suite (96 tests)
├── docs/                # workflow notes
├── README.md            # this file
├── PRD.md               # product requirements
├── PLAN.md              # implementation phases
└── TODO.md              # task tracking
```

---

## Quickstart

### 1. Install dependencies

```bash
uv sync
```

Requires [uv](https://docs.astral.sh/uv/) and Python 3.11+.

### 2. Configure API keys

**Linux / macOS:**

```bash
cp .env.example .env
```

**Windows (PowerShell):**

```powershell
copy .env.example .env
```

Edit `.env` and set:

```env
OPENAI_API_KEY=your_openai_key_here
SERPER_API_KEY=your_serper_key_here
```

`MODEL_NAME` is optional (defaults to `gpt-4o-mini`). Never commit `.env` or real keys.

### 3. Verify configuration

```bash
uv run python scripts/check_config.py
```

Expect `Config loaded successfully` and `OPENAI_API_KEY: present` / `SERPER_API_KEY: present` (values are never printed).

### 4. Optional — one live search (Serper only)

```bash
uv run python scripts/run_live_search.py
```

Evidence is saved under `outputs/research/`.

### 5. Run one chapter crew (live OpenAI + Serper)

**Warning:** uses paid API calls.

```bash
uv run python scripts/run_crew.py
```

Other options:

```bash
uv run python scripts/run_crew.py --chapter 2
uv run python scripts/run_crew.py --all
```

Artifacts: `outputs/research/`, `outputs/drafts/`, `outputs/reviews/`, `outputs/logs/`, `latex/generated/`.

### 6. Generate graph asset (no API keys)

```bash
uv run python scripts/make_figures.py
```

### 7. Build the PDF (XeLaTeX + biber)

Requires a local TeX distribution with `xelatex` and `biber` (MiKTeX or TeX Live).

```bash
uv run python scripts/build_pdf.py
```

Output: `latex/main.pdf`. The script prefers `latexmk -xelatex`; on Windows/MiKTeX without Perl it falls back to `xelatex` → `biber` → `xelatex` → `xelatex`.

### 8. Verify required PDF elements

```bash
uv run python scripts/verify_pdf_elements.py
```

Writes `outputs/logs/pdf_verification.md` and prints a PASS/FAIL summary.

### 9. Tests and lint

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

### 10. Optional — cost report from saved artifacts

```bash
uv run python scripts/report_costs.py
```

Writes `outputs/logs/cost_report.md` and `cost_report.json` (approximate token/cost estimates; no live API calls).

---

## Build and verification evidence

Latest local verification (re-run commands above to refresh):

| Check | Result |
|---|---|
| PDF page count | 17 pages |
| Verification script | **PASS** (all required elements) |
| pytest | **96 passed** |
| ruff | **all checks passed** |
| biber | succeeded (`latex/main.bbl` populated) |
| Build engine | **XeLaTeX** (XeTeX) |

Full checklist: `outputs/logs/pdf_verification.md`

---

## Security and secrets

- `.env` is gitignored; `.env.example` contains placeholders only.
- Do not commit API keys, tokens, or real credentials.
- `scripts/verify_pdf_elements.py` scans LaTeX sources for common secret patterns.
- `latex/main.pdf` remains a local generated build artifact. Only the final submission copy `outputs/final/ai_agents_real_work_book.pdf` is intended to be tracked in GitHub.

---

## Design decisions

| Decision | Rationale |
|---|---|
| **CrewAI** | Role-based orchestration mirrors research → draft → review → publish workflows |
| **Serper** | Live internet research with auditable URLs and snippets |
| **XeLaTeX + polyglossia** | Enables Hebrew–English BiDi text so the bilingual terminology section renders correctly in the PDF |
| **biblatex + biber** | Linked in-text citations and bibliography |
| **Source-level PDF verification** | `verify_pdf_elements.py` checks LaTeX sources and build artifacts—not OCR |
| **Cost tracking** | `report_costs.py` estimates API usage from saved artifacts for budget awareness |
| **uv** | Reproducible dependency management and script execution |

---

## Submission checklist

- [ ] GitHub repository pushed and accessible to lecturer
- [ ] `uv run pytest` passes (96 tests)
- [ ] `uv run ruff check .` passes
- [ ] `uv run python scripts/build_pdf.py` produces `latex/main.pdf`
- [ ] `uv run python scripts/verify_pdf_elements.py` reports **PASS**
- [ ] No `.env` or API keys committed
- [ ] Final PDF exists in GitHub at `outputs/final/ai_agents_real_work_book.pdf`

---

## Documentation

- `PRD.md` — product requirements
- `PLAN.md` — implementation phases (M0–M12)
- `TODO.md` — task tracking and Definition of Done
- `docs/workflow.md` — CrewAI context flow

---

## Live research requirement

This project requires live API-based internet research. There is no offline or fake production mode. If required API keys are missing at runtime, scripts fail with a clear error. Book content is intended to trace back to live research artifacts and reviewed agent outputs, not static hardcoded content.
