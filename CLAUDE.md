# CLAUDE.md

Instructions for Claude Code when working in this repository.

## Project

Expense Agent: a personal expense tracker with an AI agent built **from scratch** (no agent frameworks). The full spec is in `PRD.md`. The build plan is in `docs/ROADMAP.md`, with one guide per step in `docs/steps/`.

**Stack:** Python 3.12, FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, OpenAI Responses API, React + Vite + TypeScript, Tailwind, TanStack Query.

## The owner's goal

The owner is building this to **deeply understand how AI agents are built** and to show it in a portfolio. Optimize for understanding, not speed:

- Explain what each new file does and why, in plain language, after creating it.
- Prefer simple, readable code over clever code.
- When a concept is new (tool schemas, the agent loop, JWT, migrations), explain it briefly before writing code.
- If the step guide marks a part as **"Write it yourself first"**, do not write that code. Review the owner's version and suggest improvements instead.

## How we work: one step at a time

1. The owner will say which step to work on, for example "Do step 05".
2. Read `docs/steps/step-XX-*.md` fully before doing anything.
3. Start by summarizing the plan for that step and listing the files you will create or change. Wait for approval.
4. Implement **only that step**. Never build features from future steps, even if they seem convenient.
5. Write the tests listed in the step. Run them. All must pass.
6. Run the step's **Verify** section and show the output.
7. Update docs as the step says (README sections, `docs/LEARNING_LOG.md` prompt for the owner).
8. Propose commits using the messages in the step guide. **Commit only when the owner says so.**
9. At the end, tick the step in `docs/ROADMAP.md`.

## Git rules

- One branch per step: `step-XX-short-name`, created from an up-to-date `main`.
- Conventional commits: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`, `ci:`. Optional scope: `feat(agent):`, `feat(api):`, `feat(ui):`, `feat(db):`.
- Small commits, each one leaves the project working.
- Merge to `main` with a pull request at the end of each step. Tag at the end of each phase.
- Never commit `.env`, API keys, `expenses.json`, `node_modules/`, or `venv/`. Run `git status` before every commit.

## Hard rules (never break these)

1. **No agent frameworks.** No LangChain, LangGraph, LlamaIndex, CrewAI, AutoGen, OpenAI Agents SDK, or similar until Step 18. We write the loop ourselves.
2. **OpenAI Responses API** (`client.responses.create`), not Chat Completions. If unsure about a field name, check the current OpenAI docs rather than guessing.
3. **The model never sees or chooses `user_id`.** Tools get `user_id` injected by `execute_tool` from the authenticated session.
4. **Tools return data, never raise.** Errors come back as `{"error": "..."}` so the model can read them and recover.
5. **Delete is gated in code.** The agent loop must never execute a deletion. It returns a `pending_delete` action; only the user's explicit confirmation deletes.
6. **REST endpoints and tools share the same service functions.** No duplicated business logic.
7. **Money:** `NUMERIC(10,2)` in Postgres, `Decimal` in Python. No floats for stored money (the Phase 1 JSON prototype is the only exception).
8. **Secrets** come only from environment variables via `app/config.py`. Never hardcode keys.
9. **Ask before adding any new dependency** not listed in the step guide.
10. The agent loop takes the OpenAI client as a parameter so tests can pass a fake client. Unit tests never call the real OpenAI API.

## Code style

- Python: type hints everywhere, `ruff` for lint and format, small functions, docstrings on public functions.
- TypeScript: `strict` mode, no `any` unless justified, components under 150 lines when practical.
- Names describe intent: `get_period_range`, not `calc`.
- Log tool calls and token usage with the `logging` module, never `print` in app code (scripts are fine).

## Repository layout (target)

```
expense-agent/
├── CLAUDE.md
├── PRD.md
├── README.md
├── docker-compose.yml
├── .env.example
├── docs/
│   ├── ROADMAP.md
│   ├── LEARNING_LOG.md
│   └── steps/
├── backend/
│   ├── requirements.txt
│   ├── alembic/
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # settings from env
│   │   ├── agent/             # loop, prompts, schemas, registry, context
│   │   ├── tools/             # tool functions (thin adapters over services)
│   │   ├── services/          # business logic shared by API and tools
│   │   ├── repositories/      # SQL queries
│   │   ├── db/                # engine, session, models
│   │   ├── api/routes/        # auth, expenses, chat
│   │   ├── core/              # security (JWT, bcrypt), deps
│   │   └── schemas/           # Pydantic request/response models
│   ├── scripts/               # learning scripts, seed data
│   ├── evals/                 # agent behavior evals
│   ├── cli.py                 # terminal chat with the agent
│   └── tests/
└── frontend/
    └── src/
        ├── api/  components/  pages/  hooks/  lib/
```

## Commands

Fill these in as each step adds them.

```bash
# backend
cd backend && source venv/bin/activate
pytest                          # run tests
ruff check . && ruff format .   # lint and format
python cli.py                   # terminal agent (Phase 1+)
uvicorn app.main:app --reload   # API (Phase 3+)
alembic upgrade head            # migrations (Phase 2+)

# database
docker compose up -d db

# frontend (Phase 4+)
cd frontend && npm run dev
```
