# Roadmap

The whole project, broken into 18 steps across 6 phases. Do **one step at a time**. Each step has its own guide in [`docs/steps/`](steps/) with goals, concepts, tasks, tests, verification, git commits, and a ready-to-paste Claude Code prompt.

## Progress

### Phase 0: Foundations
- [x] [Step 01: Repo setup and conventions](steps/step-01-repo-setup.md)

### Phase 1: Terminal agent (learn the agent itself)
- [ ] [Step 02: Tools as plain Python functions](steps/step-02-tools.md)
- [ ] [Step 03: Tool schemas and the tool registry](steps/step-03-tool-schemas.md)
- [ ] [Step 04: First LLM call and one tool round trip](steps/step-04-first-llm-call.md)
- [ ] [Step 05: The agent loop](steps/step-05-agent-loop.md)
- [ ] [Step 06: Guardrails, delete gate, and context window](steps/step-06-guardrails.md) → tag `v0.1-terminal-agent`

### Phase 2: Real database
- [ ] [Step 07: Postgres, models, and migrations](steps/step-07-postgres-setup.md)
- [ ] [Step 08: Swap the tools to Postgres](steps/step-08-postgres-tools.md) → tag `v0.2-postgres`

### Phase 3: Backend API
- [ ] [Step 09: FastAPI skeleton](steps/step-09-fastapi-skeleton.md)
- [ ] [Step 10: Authentication (signup, login, JWT)](steps/step-10-auth.md)
- [ ] [Step 11: Expense and dashboard APIs](steps/step-11-expense-apis.md)
- [ ] [Step 12: Chat API (agent over HTTP)](steps/step-12-chat-api.md) → tag `v0.3-api`

### Phase 4: Web UI
- [ ] [Step 13: Frontend setup and auth pages](steps/step-13-frontend-auth.md)
- [ ] [Step 14: Dashboard](steps/step-14-dashboard.md)
- [ ] [Step 15: Chat panel](steps/step-15-chat-panel.md) → tag `v0.4-web`

### Phase 5: Ship it
- [ ] [Step 16: Deployment and demo account](steps/step-16-deploy.md) → tag `v1.0.0`
- [ ] [Step 17: CI, evals, and portfolio polish](steps/step-17-polish.md) → tag `v1.0.1`

### Phase 6: Optional
- [ ] [Step 18: Rebuild the agent with a framework and compare](steps/step-18-framework-comparison.md) → tag `v1.1.0`

## The big picture: why this order

```
Phase 1  Agent alone in a terminal      → you learn the agent with nothing else in the way
Phase 2  Swap JSON for Postgres         → you see that only storage changes, the agent does not
Phase 3  Wrap it in an API with auth    → you learn how an agent fits a real backend safely
Phase 4  Put a UI on top                → you see the agent's actions land in a real app
Phase 5  Deploy and polish              → you have a live link and a repo worth showing
```

Each phase ends with something that **works**. If you stop after any phase, you still have a complete project.

## How each step works

Every step guide has the same sections:

| Section | What it gives you |
|---|---|
| **Goal** | What exists at the end of the step |
| **What you'll learn** | The concepts this step teaches |
| **Concepts** | Short explanations before you code |
| **Tasks** | What to build, grouped by layer (DB, backend, AI, API, UI) |
| **Files** | Exactly which files are created or changed |
| **Tests** | What to test and why |
| **Verify** | Commands to run and what you should see |
| **Git** | Branch name and commit messages |
| **Docs** | What to update in README and Learning Log |
| **Claude Code prompt** | Paste this to start the step |
| **Pitfalls** | Common mistakes |
| **Check your understanding** | Answer these before moving on |

## Git workflow (every step)

```bash
# start a step
git checkout main
git pull
git checkout -b step-05-agent-loop

# work in small commits (messages are in each step guide)
git add <files>
git commit -m "feat(agent): add agent loop with max step limit"

# finish a step
git push -u origin step-05-agent-loop
# open a pull request on GitHub, review the diff yourself, merge it
git checkout main
git pull

# end of a phase
git tag v0.1-terminal-agent
git push origin v0.1-terminal-agent
```

**Commit types:** `feat` (new feature), `fix` (bug fix), `test` (tests), `docs` (documentation), `refactor` (no behavior change), `chore` (setup, deps), `ci` (pipelines).

Reviewing your own pull request diff before merging is a habit worth building: it's the moment you notice what Claude Code actually wrote.

## Using Claude Code well for this project

1. **Start each step in plan mode.** Paste the step's prompt, let Claude Code propose a plan, and read it before approving.
2. **Respect "Write it yourself first" blocks.** Steps 04 and 05 (the first API call and the loop) are the heart of the project. Type those yourself, then ask Claude Code to review.
3. **Ask "why" constantly.** "Why strict mode?", "Why return errors instead of raising?" Claude Code is your tutor, not just your typist.
4. **Run everything yourself.** Run the tests and the verify commands in your own terminal, not just through Claude Code.
5. **Write the Learning Log yourself.** Never let Claude Code write it.
6. **New session per step** is fine. `CLAUDE.md` and the step guide give it all the context it needs.

## Definition of done (every step)

- [ ] All tasks in the step guide are complete
- [ ] All tests pass (`pytest`, and `npm run build` for frontend steps)
- [ ] Verify section produces the expected output
- [ ] No secrets in `git status` or the diff
- [ ] README updated as the step says
- [ ] Learning Log entry written **by you**
- [ ] Pull request merged to `main`
- [ ] Box ticked above

## Estimated time

| Phase | Steps | Rough time |
|---|---|---|
| 0 | 01 | 1 hour |
| 1 | 02 to 06 | 6 to 8 hours |
| 2 | 07 to 08 | 3 to 4 hours |
| 3 | 09 to 12 | 6 to 8 hours |
| 4 | 13 to 15 | 8 to 10 hours |
| 5 | 16 to 17 | 4 to 6 hours |
| 6 | 18 | 2 to 3 hours |

Go slower if you need to. Understanding beats speed here.

## Stretch ideas (after v1)

- Receipt photo upload (model reads the image)
- Budgets with alerts (adds one tool, no architecture change)
- Recurring expenses
- CSV export
- Custom per-user categories (build the enum dynamically)
- React Native app on the same API
