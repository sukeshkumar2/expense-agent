# Expense Agent

Track expenses by chatting in plain English. An AI agent, **built from scratch with no agent frameworks**, turns "I spent $12 on lunch and $40 on gas" into structured records, answers questions like "did I spend more on food or transport this month?", and never deletes anything without your confirmation.

> **Live demo:** _coming in Step 16_
> **Status:** 🚧 In development. See [Roadmap](docs/ROADMAP.md).

<!-- Step 17: add a GIF of the app here -->

## Why this project

Most agent demos hide the interesting parts behind a framework call. This project implements every piece by hand so it can be read and understood:

- **Tool schemas** that tell the model what it can do
- **The agent loop**: call the model, run the tools it asks for, feed results back, repeat
- **A code-enforced approval gate** for destructive actions
- **Server-side identity injection** so the model can never act on another user's data
- **Context management** with a fixed message window
- **Guardrails** for scope, cost, and runaway loops

## Features

- 💬 Chat with an AI agent to add, find, total, edit, and delete expenses
- 🧠 Natural language dates ("yesterday", "this month") and category mapping ("snacks" → food)
- ✅ Deletions require a click to confirm, enforced in code
- 📊 Dashboard with Day / Month / Year views, totals, and category breakdown
- ✍️ Manual add, edit, and delete without the AI
- 🔐 Email and password auth with JWT

## Architecture

<!-- Step 17: replace with a Mermaid diagram -->

```
React (Vite, TS)  ──HTTPS + JWT──▶  FastAPI  ──▶  Agent loop  ──▶  OpenAI Responses API
                                       │              │
                                       │         Tool registry (injects user_id)
                                       ▼              ▼
                                  Service layer (shared by REST and tools)
                                       ▼
                                   PostgreSQL
```

See [PRD.md](PRD.md) for the full design.

## How the agent works

<!-- Step 05: write this section in your own words after building the loop -->

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL 16 |
| AI | OpenAI Responses API (function calling), no agent framework |
| Auth | bcrypt, JWT |
| Frontend | React, Vite, TypeScript, Tailwind, TanStack Query |
| Testing | pytest with a fake OpenAI client |
| CI/CD | GitHub Actions; Vercel, Render, Neon (or equivalents) |

## Getting started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker (for local Postgres)
- An OpenAI API key

### Setup

<!-- Each step adds its commands here -->

```bash
git clone https://github.com/<your-username>/expense-agent.git
cd expense-agent
cp .env.example .env    # then add your OpenAI key

# backend
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# check that config loads
python -c "from app.config import settings; print(settings.openai_model)"
pytest
```

## Project structure

<!-- Step 17: final tree -->

## Testing

<!-- Step 02+: how to run tests -->

## Design decisions

<!-- Step 17: summarize the key decisions table from PRD.md and what you learned -->

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## License

MIT
