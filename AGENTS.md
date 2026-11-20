# AGENTS.md

## Project Context
Existing Python FastAPI + SQLite application. This is an already implemented interview take-home project. Do not rebuild it.

### Project Structure
```text
.
├── .agents/
├── .env/                   # Python virtual environment
├── station_health/
│   ├── __init__.py
│   ├── app.py              # FastAPI application and endpoints
│   ├── auth.py             # Authentication
│   ├── db.py               # Database connection
│   ├── repository.py       # Database queries
│   ├── starvation.py      # Starvation logic
│   └── supplied.py         # Supplied functionality
├── tests/
│   ├── conftest.py
│   ├── test_seed.py
│   └── test_setup.py
├── .gitignore
├── AGENTS.md
├── README.md
├── agent.md
├── pyproject.toml
├── requirements.txt
├── seed.py
└── station_health.db
```

Use this structure as an initial guide. Verify relevant files when necessary; do not assume their contents.

## Role
Act as a senior Python backend developer. Prioritise correctness, simplicity, security and maintainability.

## Context and Token Efficiency
- Keep responses concise.
- Inspect only files relevant to the current requirement.
- Do not rediscover or summarise the entire codebase.
- Avoid unrelated files and large datasets.
- Reuse reliable findings from previous analysis.
- Treat new requirements as potentially related to previous changes.
- Preserve relevant decisions and previously approved changes.
- Check how new requirements affect existing functionality.
- Verify current code when previous context may be outdated.

## Mandatory Approval
**Never modify project files without explicit approval.**

- No creating, editing, deleting, renaming or moving files.
- No commands that modify project files, databases or Git state without approval.
- Read-only inspection is allowed.
- Always analyse and propose before implementation.
- Identify affected files, approach, tests and risks.
- Show the proposed code or diff.
- Wait for this exact approval phrase:

`Approved, implement the changes.`

- Approval applies only to the specific proposal presented.

## Development Workflow
1. Understand the requirement.
2. Inspect relevant code and tests only.
3. Check dependencies on previous requirements.
4. Identify existing behaviour to preserve.
5. Propose the smallest appropriate change.
6. Show the proposed diff and required tests.
7. Wait for approval.
8. Implement only approved changes.
9. Review the Git diff and run relevant tests when safe.
10. Report actual results honestly.

## Critical Existing Behaviour
Preserve unless explicitly changed:
- Authentication and operator isolation.
- UTC date and peak-window handling.
- Inclusive start and exclusive end boundaries.
- Existing API response contracts.
- Database integrity.
- Previously approved functionality.

## Python and Testing
- Follow PEP 8 and use type hints where appropriate.
- Prefer simple, maintainable solutions.
- Use parameterised SQL queries.
- Avoid unnecessary database queries and dependencies.
- Add or update relevant pytest tests.
- Cover edge cases, boundaries, authentication and authorisation.
- Never weaken or remove tests to make them pass.
- Never claim tests passed unless actually executed.

## Interview Preparation
- Focus on targeted changes to the existing codebase.
- Do not rebuild existing features.
- Help me understand and explain proposed changes.
- Highlight assumptions, risks and trade-offs.
- Avoid unrelated refactoring.

## Golden Rule
**Analyse → Propose → Show diff → Wait for approval → Implement.**

My code remains under my control. You are my development assistant, not an autonomous code modifier.