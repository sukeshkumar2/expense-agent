# Expense Agent: Product Requirements Document

| | |
|---|---|
| **Version** | 1.0 |
| **Date** | October 25, 2026 |
| **Owner** | Sukesh Kumar Dosapati |
| **Status** | Approved, ready to build |

---

## 1. Overview

Expense Agent is a web app where a user tracks personal expenses in two ways: by chatting with an AI agent in plain English ("I spent $12 on lunch and $40 on gas"), or through a normal dashboard with forms and filters. The AI agent is built **from scratch** in Python on top of the OpenAI Responses API, with no agent frameworks, so every part of the agent (tool schemas, tool dispatch, the agent loop, context handling, guardrails, human approval) is visible and explainable.

## 2. Goals

1. **Learning:** understand end to end how an AI agent is built: tools, schemas, the loop, context, guardrails, and how an agent fits into a real backend and UI.
2. **Portfolio:** a clean public GitHub repo with a strong README, tests, CI, and a live demo link.
3. **Working product:** a usable personal expense tracker.

### Non-goals (v1)

- Multiple currencies (USD only)
- Budgets, recurring expenses, receipt scanning, charts beyond a category breakdown
- Mobile app (planned later, reusing the same API)
- Stored chat history across sessions
- Agent frameworks (LangChain, LangGraph, CrewAI, OpenAI Agents SDK, etc.)

## 3. Users

- **v1:** the owner only, plus a public **demo account** for portfolio visitors.
- **Later (optional):** open signup for anyone. The data model and auth support multiple users from day one so this needs no rewrite.

## 4. User stories

| # | As a user, I want to... | So that... |
|---|---|---|
| U1 | sign up and log in | my expenses are private |
| U2 | type "spent $12 on lunch" in chat | I can log expenses quickly in plain English |
| U3 | log several expenses in one message | I don't have to repeat myself |
| U4 | ask "how much did I spend on food this month?" | I get answers without building filters |
| U5 | ask "did I spend more on food or transport?" | the agent compares for me |
| U6 | say "change the gas one to $45" | I can fix mistakes in chat |
| U7 | ask the agent to delete something, but confirm before it happens | the AI can never delete data without my approval |
| U8 | see my recent transactions on the dashboard | I know what I logged |
| U9 | switch between Day, Month, and Year views | I see spending for any period |
| U10 | see totals and a category breakdown for the period | I understand where money goes |
| U11 | add, edit, and delete expenses manually | I can work without the AI too |
| U12 | (visitor) try a demo account without signing up | I can evaluate the project quickly |

## 5. Functional requirements

### 5.1 Authentication

- **FR-A1:** Sign up with email and password. Email is normalized to lowercase. Password minimum 8 characters.
- **FR-A2:** Passwords are hashed with bcrypt. Plain passwords are never stored or logged.
- **FR-A3:** Login returns a JWT access token. Clients send it as `Authorization: Bearer <token>` (works for web now and mobile later).
- **FR-A4:** All expense and chat endpoints require a valid token. Expired or invalid tokens return `401`.
- **FR-A5:** A user can only ever read or change their own expenses. Accessing another user's expense returns `404` (not `403`, so existence is not leaked).

### 5.2 Expenses

- **FR-E1:** An expense has: amount (USD, 2 decimals, greater than 0), category, description, date.
- **FR-E2:** Categories are a fixed list: `food`, `transport`, `shopping`, `bills`, `entertainment`, `other`.
- **FR-E3:** The backend validates categories. An unknown category from any source becomes `other`.
- **FR-E4:** Users can create, edit, and delete expenses manually from the UI.
- **FR-E5:** Edits return before and after values so the UI can show what changed.

### 5.3 Dashboard

- **FR-D1:** Recent transactions list, newest first (default 10).
- **FR-D2:** Period selector with **Day**, **Month**, **Year**, a picker for each, and previous/next arrows.
- **FR-D3:** For the selected period: total, count, per-category breakdown, and the list of expenses.
- **FR-D4:** Periods are computed in the **user's timezone** (sent by the frontend on each request).
- **FR-D5:** The dashboard refreshes automatically after the agent adds, edits, or deletes expenses.

### 5.4 AI agent

- **FR-AI1:** The agent understands natural language and acts through five tools:

| Tool | Purpose | Needs confirmation |
|---|---|---|
| `add_expense` | Record one expense | No |
| `list_expenses` | Find expenses by category, date range, or description search | No |
| `get_total` | Sum and breakdown for a filter | No |
| `update_expense` | Change fields of one expense | No (reversible, UI shows before/after) |
| `delete_expense` | Request deletion of one expense | **Yes, enforced in code** |

- **FR-AI2:** The model maps free text to the fixed categories ("snacks" becomes `food`). The user's original words stay in `description`.
- **FR-AI3:** The model can make multiple tool calls per message, including several calls in one turn ("lunch $12 and gas $40" means two `add_expense` calls).
- **FR-AI4:** **Delete gate:** when the model calls `delete_expense`, the backend does **not** delete. It returns a `pending_delete` action. Only the user clicking **Confirm** in the UI deletes it, through the normal `DELETE /api/expenses/{id}` endpoint.
- **FR-AI5:** The model never receives or chooses `user_id`. The backend injects it into every tool call from the authenticated session.
- **FR-AI6:** The system prompt includes today's date and the user's timezone so "yesterday" and "this month" resolve correctly.
- **FR-AI7:** **Short-term context:** the frontend keeps the last **20** chat messages (user and assistant text only) and sends them with each request. Nothing is stored server-side. Refreshing the page clears the chat.
- **FR-AI8:** **Long-term memory is the database.** Questions about older data are answered by tool calls, not by chat history.

### 5.5 Guardrails

| ID | Guardrail | Value |
|---|---|---|
| G1 | Scope: agent only handles expense topics, politely refuses others in one sentence | System prompt |
| G2 | Max input length, rejected before any API call | 500 characters |
| G3 | Daily chat message cap per user | 50 (owner), 20 (demo), configurable |
| G4 | Max tool-call rounds per message | 5 |
| G5 | Max output tokens per model call | 500, configurable |
| G6 | Max messages in context | 20 |
| G7 | Monthly spending limit in the OpenAI dashboard | Set before first API call |
| G8 | Tool errors returned as data to the model, never crash the loop | Always |

## 6. Non-functional requirements

- **Security:** secrets only in environment variables; `.env` never committed; CORS restricted to the frontend origin; ownership checks on every query.
- **Money precision:** Postgres `NUMERIC(10,2)`, Python `Decimal`. No floats for stored money.
- **Dates:** stored as `DATE`; exchanged as ISO `YYYY-MM-DD`.
- **Performance:** dashboard queries use an index on `(user_id, date DESC)`. Typical non-AI API response under 200 ms.
- **Cost:** a small, cheap OpenAI model (configurable via `OPENAI_MODEL`). Token usage logged for every request.
- **Testability:** the agent loop accepts an injected OpenAI client so it can be tested with a fake client, no network.
- **Portability:** the backend is a plain JSON REST API, usable by a future React Native app.

## 7. Architecture

```
┌──────────────────────────────┐
│ React + Vite + TypeScript    │
│ Login, Dashboard, Chat panel │
│ keeps last 20 chat messages  │
└──────────────┬───────────────┘
               │ HTTPS, Bearer JWT, X-Timezone header
┌──────────────▼───────────────────────────────────────┐
│ FastAPI                                              │
│  /api/auth      signup, login, me                    │
│  /api/expenses  recent, period view, CRUD            │
│  /api/chat      runs the agent                       │
│                                                      │
│  Agent: loop -> OpenAI Responses API                 │
│         tool registry (injects user_id)              │
│         delete gate, guardrails                      │
│                       │                              │
│  Service layer (business rules, shared by API+tools) │
│                       │                              │
│  Repository layer (SQL)                              │
└───────────────────────┬──────────────────────────────┘
                        │
               ┌────────▼────────┐
               │ PostgreSQL      │
               │ users, expenses,│
               │ chat_usage      │
               └─────────────────┘
```

**Key layering idea:** the REST endpoints and the agent tools both call the **same service functions**. The dashboard's "October total" and the agent's answer to "what did I spend in October?" always match.

## 8. Data model

```sql
CREATE TABLE users (
  id            SERIAL PRIMARY KEY,
  email         TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  is_demo       BOOLEAN NOT NULL DEFAULT FALSE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE expenses (
  id          SERIAL PRIMARY KEY,
  user_id     INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  amount      NUMERIC(10,2) NOT NULL CHECK (amount > 0),
  category    TEXT NOT NULL CHECK (category IN
                ('food','transport','shopping','bills','entertainment','other')),
  description TEXT NOT NULL DEFAULT '',
  date        DATE NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_expenses_user_date ON expenses (user_id, date DESC);

CREATE TABLE chat_usage (
  user_id   INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  day       DATE NOT NULL,
  messages  INT NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, day)
);
```

## 9. API specification

All endpoints are prefixed with `/api`. All except `/health`, `/auth/signup`, and `/auth/login` require `Authorization: Bearer <token>`. Expense and chat endpoints read the optional `X-Timezone` header (IANA name, default `America/Los_Angeles`).

| Method | Path | Body / Query | Returns |
|---|---|---|---|
| GET | `/health` | | `{status: "ok"}` |
| POST | `/auth/signup` | `{email, password}` | `201 {id, email}` |
| POST | `/auth/login` | `{email, password}` | `{access_token, token_type: "bearer"}` |
| GET | `/auth/me` | | `{id, email, is_demo}` |
| GET | `/expenses/recent` | `?limit=10` | `[Expense]` |
| GET | `/expenses` | `?period=day&date=2026-10-25` or `period=month&date=2026-10` or `period=year&date=2026` | `{period, start, end, total, count, by_category, expenses}` |
| POST | `/expenses` | `{amount, category, description, date?}` | `201 Expense` |
| PATCH | `/expenses/{id}` | any of `{amount, category, description, date}` | `{before, after}` |
| DELETE | `/expenses/{id}` | | `204` |
| POST | `/chat` | `{messages: [{role, content}]}` (max 20, last is user) | `{reply, actions, usage, remaining_today}` |

**Chat `actions`** tell the UI what the agent did:

```json
[
  {"type": "added",          "expense": {...}},
  {"type": "updated",        "before": {...}, "after": {...}},
  {"type": "pending_delete", "expense": {...}}
]
```

**Error format** (all endpoints): `{"detail": "human readable message"}` with the right status code (`400`, `401`, `404`, `409`, `422`, `429`, `502`).

## 10. Agent design

### 10.1 The loop

```
input = system prompt + last 20 messages
for step in 1..MAX_AGENT_STEPS:
    response = openai.responses.create(model, instructions, input, tools)
    calls = function_call items in response.output
    if no calls: return response.output_text            # done
    input += response.output                            # keep the model's turn
    for call in calls:
        if call.name == "delete_expense": record pending_delete, output = "awaiting user confirmation"
        else: output = execute_tool(call.name, call.arguments, user_id)   # user_id injected
        input += {type: function_call_output, call_id, output}
return "I couldn't finish that, please try rephrasing."  # hit the step limit
```

### 10.2 System prompt rules

1. You are an expense assistant for one user. Today is `{today}` in `{timezone}`.
2. Only help with tracking and analyzing this user's expenses. For anything else, reply in one short sentence that you can only help with expenses.
3. Amounts are USD. Never invent amounts or dates; ask if unclear.
4. Use tools to read data. Never guess totals.
5. To delete, find the expense first, then call `delete_expense`. Tell the user to confirm in the app.
6. Keep replies short and friendly. Mention amounts and dates.

### 10.3 Tool schema rules

- OpenAI Responses API function tools with `strict: true`.
- All properties listed in `required`; optional ones use a `null` type option.
- `additionalProperties: false`.
- `category` is an `enum` of the fixed list, with mapping hints in the description.
- No `user_id` parameter anywhere.

## 11. UI specification

```
┌──────────────────────────────────────────────────────────────┐
│ Expense Agent                              sukesh@...  Logout │
├──────────────────────────────────────┬───────────────────────┤
│ [Day | Month | Year]  < October 2026 >│ Chat                  │
│ Total $482.30   23 expenses           │                       │
│ food ███████ $210                     │ You: spent $8 coffee  │
│ transport ████ $140                   │ Agent: Added coffee   │
│ bills ██ $90                          │   $8.00 (food) today  │
│ [+ Add expense]                       │  [chip: Added $8]     │
│ Oct 25  Lunch        food      $12.00 │                       │
│ Oct 24  Gas          transport $40.00 │ ┌ Delete Gas $40?    ┐│
│ ...                         [edit][x] │ │ [Confirm] [Cancel] ││
│                                       │ └────────────────────┘│
│                                       │ [ Type a message... ] │
│                                       │ 18 messages left today│
└──────────────────────────────────────┴───────────────────────┘
```

On mobile widths, chat becomes a tab or a bottom drawer.

## 12. Tech stack

| Layer | Choice |
|---|---|
| Language (backend) | Python 3.12 |
| API framework | FastAPI, Pydantic v2, pydantic-settings |
| Database | PostgreSQL 16 (Docker locally) |
| ORM and migrations | SQLAlchemy 2.0, Alembic, psycopg 3 |
| Auth | bcrypt, PyJWT |
| AI | OpenAI Python SDK, Responses API, small model (configurable) |
| Tests | pytest, FastAPI TestClient, fake OpenAI client |
| Lint/format | ruff |
| Frontend | React, Vite, TypeScript, Tailwind CSS, React Router, TanStack Query |
| CI | GitHub Actions |
| Hosting | Vercel or Netlify (frontend), Render or Railway (backend), Neon or Supabase (Postgres) |

## 13. Key decisions

| Decision | Choice | Why |
|---|---|---|
| Agent framework | None | Learning goal; the core loop is small; frameworks hide what we want to understand |
| OpenAI API | Responses API | Recommended for new projects |
| Database | Postgres over MongoDB | Relational data, fixed schema, easy SQL aggregation, exact NUMERIC money |
| Auth | Own JWT + bcrypt | Learning goal; Bearer tokens work for future mobile app |
| Delete safety | Code-enforced gate | A prompt rule can be ignored by the model; a code gate cannot |
| Chat memory | Client-side, last 20 text messages | DB is the long-term memory via tools; keeps cost low and requests focused |
| Categories | Fixed enum | Clean dashboard; model maps synonyms; backend validates |
| Build order | Phased, terminal agent first | Learn the agent before adding web complexity |

## 14. Milestones

| Phase | Steps | Git tag | Outcome |
|---|---|---|---|
| 0. Foundations | 01 | | Repo, docs, config |
| 1. Terminal agent | 02 to 06 | `v0.1-terminal-agent` | Working agent in the terminal, JSON storage |
| 2. Postgres | 07 to 08 | `v0.2-postgres` | Same agent on a real database |
| 3. API | 09 to 12 | `v0.3-api` | FastAPI with auth, expenses, chat |
| 4. Web UI | 13 to 15 | `v0.4-web` | Full web app locally |
| 5. Ship | 16 to 17 | `v1.0.0` | Deployed, CI, polished README |
| 6. Optional | 18 | `v1.1.0` | Framework comparison |

## 15. Acceptance tests (agent behavior)

The agent passes v1 when these prompts behave as expected:

| Prompt | Expected behavior |
|---|---|
| "I spent $12 on lunch and $40 on gas" | Two `add_expense` calls: food 12, transport 40 |
| "bought snacks for 5 bucks yesterday" | `add_expense` food 5, date = yesterday |
| "How much did I spend on food this week?" | `get_total` with correct week date range |
| "Did I spend more on food or transport this month, and by how much?" | Two totals, correct comparison |
| "How much on snacks?" | `list_expenses` with `search: "snacks"` |
| "Change the gas one to $45" | `list_expenses` then `update_expense` |
| "Delete the lunch one" | `list_expenses` then `delete_expense`, returns `pending_delete`, nothing deleted until confirm |
| "Write me a poem" | One-sentence polite refusal, no tool calls |
| A 600-character message | Rejected with `400` before any OpenAI call |

## 16. Future ideas

- Receipt photo upload (model reads the image and adds the expense)
- Budgets with alerts ("warn me if food passes $300")
- Recurring expenses
- CSV export
- Custom per-user categories
- React Native mobile app on the same API
- Rebuild the agent with a framework and compare (Step 18)

## 17. Risks

| Risk | Mitigation |
|---|---|
| Public demo burns OpenAI credits | Daily caps, demo cap, input length cap, OpenAI monthly limit |
| Model picks wrong dates | Today's date in prompt, eval cases for date phrases |
| Model tries to act on wrong user | `user_id` never exposed to the model, injected server-side |
| Accidental deletion | Code-enforced confirmation gate |
| OpenAI API changes | Pin SDK version; isolate all OpenAI calls in `app/agent/` |
| Timezone bugs | Frontend sends IANA timezone; tests for day-boundary cases |
