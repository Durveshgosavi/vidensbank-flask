# Multi-Agent Workflow

This playbook explains how to coordinate multiple AI or human agents when working inside the Vidensbank Flask repository. Use it whenever a task spans several domains (data, backend, frontend, DevOps, documentation) or when parallelizing work across assistants such as Claude Code and GPT/Codex.

## 1. Core Principles

1. **Single source of truth** – Keep requirements grounded in `ACTION_PLAN.md`, `WORKFLOW.md`, and the relevant feature specs. If something is unclear, update the shared notes before branching off.
2. **Explicit interfaces** – Every hand-off between agents must include inputs, expected outputs, test/validation steps, and file paths.
3. **Short feedback loops** – Prefer multiple light-weight iterations over one long cycle. After each loop, sync status in this document or in a scratch note so all agents know the current state.
4. **Ownership, not silos** – Each agent drives their deliverable end-to-end (code + docs + tests) but remains accountable for upstream/downstream impacts.

## 2. Recommended Roles

| Role | Focus | Typical Tasks |
| --- | --- | --- |
| **Navigator** (Lead) | Clarifies objective, keeps scope aligned to `ACTION_PLAN.md` | Define acceptance criteria, assign roles, maintain checklist |
| **Backend Builder** | Flask, SQLAlchemy, business logic | Models, services, API endpoints, calculations |
| **Frontend/UX Builder** | Templates, JS, CSS | Layouts, forms, visualizations, interactions |
| **Data & Calculations** | Climate datasets, baseline metrics | Import scripts, data validation, calculator accuracy |
| **QA / Reviewer** | Tests, code review, docs sanity | Run pytest/manual flows, verify acceptance criteria |
| **Release Steward** | Deployment + ops | Procfile, env vars, Heroku release validation |

One person/agent can own multiple roles if the scope is small.

## 3. Workflow Stages

### Stage 0 – Kickoff
- Navigator confirms context: feature name, desired outcome, non-goals.
- Gather references (`ACTION_PLAN.md`, `PROJECT_OVERVIEW.md`, open issues).
- Create a lightweight mission note (bullet list) with:
  - Success definition
  - Constraints/assumptions
  - Who owns what role

### Stage 1 – Plan & Decompose
1. Brainstorm approach synchronously (shared chat, doc, or repo note).
2. Write a task board (Kanban or checklist) with swimlanes per role.
3. Define shared contracts:
   - Data schemas (`app.py` models, migrations)
   - API signatures
   - Template blocks / component IDs
4. Decide review gates (e.g., backend PR must pass local tests before frontend starts wiring new endpoints).

### Stage 2 – Parallel Execution
- Each agent works in their area, keeping commits scoped.
- Post quick status notes after meaningful milestones (e.g., "BaselineComparison service ready, returns JSON contract X").
- If a dependency shifts, ping affected agents immediately and update the shared checklist.

### Stage 3 – Integration
1. Backend + frontend pair to verify end-to-end behavior locally (`python app.py`).
2. Run regression checks from `WORKFLOW.md` (auth, calculator flows, contact form).
3. QA agent validates acceptance criteria and documents test evidence (even brief notes in commit or docs).
4. Navigator confirms documentation updates (README sections, calculator guides, etc.).

### Stage 4 – Release
- Release Steward prepares deployment notes (config changes, DB migrations, feature flags).
- Coordinate the Heroku push:
  ```bash
  git push heroku main
  heroku run python init_db.py  # if schema changes
  heroku logs --tail            # live verification
  ```
- After release, record outcomes in `IMPLEMENTATION_SUMMARY.md` or relevant log.

## 4. Communication Templates

**Handoff note (from Backend Builder to Frontend Builder):**
```
Context: WeeklyMenuPlanner endpoint ready.
Endpoint: POST /api/menu/preview
Payload: { canteen_id, week_start, dishes[] }
Response: { baseline, proposed, co2_delta }
Validation: python -m pytest tests/test_menu_planner.py
Next: Hook calculator UI form submit to endpoint, display delta cards.
```

**Status ping:**
```
[Role] Backend Builder
[Status] Implemented CanteenProfile historical metrics. Local tests green.
[Blocks] Need updated dataset from Data agent for >2023 entries.
```

## 5. Conflict Resolution & Escalation

1. Default to Navigator decisions; if disagreement persists, document options with pros/cons and pick the safest reversible choice.
2. If progress stalls, schedule a focused sync (5–10 minutes) to realign scope rather than continuing async churn.
3. Capture lessons learned or new constraints at the end so future multi-agent sessions start faster.

## 6. Tooling Checklist

- Shared scratchpad: `/docs/notes/<feature>-session.md`
- Task tracking: simple checklist in existing md file or GitHub issue.
- Code reviews: use `git diff` summaries in chat, highlight risky changes first.
- Testing: follow recipes in `WORKFLOW.md` (app smoke test, calculator scenarios, db init).

## 7. Quick Start Cheat Sheet

1. Read `ACTION_PLAN.md` for context.
2. Assign roles + contracts.
3. Track tasks + status in a shared note.
4. Work in parallel with explicit handoffs.
5. Integrate, test, document, release.

Keep this file updated as you refine the process. Continuous improvements to the workflow compound over time, especially as new assistants join the project.
