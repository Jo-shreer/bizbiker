---
description: Project structure, file responsibilities, Python standards and conventions for Station Health Take-Home.
globs: "**/*"
alwaysApply: true
---

# Station Health Take-Home

## 1. Project Overview
- Python, FastAPI and SQLite.
- pytest for automated testing.
- Extend the existing application; never rebuild unnecessarily.

## 2. Project Structure

```text
station-health-take-home/
├── LICENSE
├── NOTES.md
├── README.md
├── pyproject.toml
├── requirements.txt
├── seed.py
├── station_health/
│   ├── __init__.py
│   ├── app.py
│   ├── auth.py
│   ├── db.py
│   ├── middleware.py
│   ├── repository.py
│   ├── schemas.py
│   ├── service.py
│   ├── starvation.py
│   └── supplied.py
├── station_health.db
└── tests/
    ├── conftest.py
    ├── test_seed.py
    ├── test_service.py
    ├── test_setup.py
    └── test_starvation.py
```

## 3. File Responsibilities

### Root
- `README.md`: Project overview and setup instructions.
- `NOTES.md`: Assumptions, limitations and incomplete functionality.
- `pyproject.toml`: Project and tool configuration.
- `requirements.txt`: Python dependencies.
- `seed.py`: Synthetic database creation and seeding.
- `LICENSE`: Project licensing.
- `station_health.db`: SQLite database. Preserve supplied data.

### station_health/
- `app.py`: FastAPI application, routes and HTTP handling.
- `auth.py`: Token authentication and operator identification.
- `db.py`: SQLite connection management.
- `middleware.py`: HTTP middleware.
- `repository.py`: SQL queries and persistence.
- `schemas.py`: Pydantic request/response models and validation.
- `service.py`: Business orchestration.
- `starvation.py`: Starvation rules and calculations.
- `supplied.py`: Original supplied functionality.
- `__init__.py`: Package initialisation.

### tests/
- `conftest.py`: Shared fixtures.
- `test_seed.py`: Seed data tests.
- `test_service.py`: Service-layer tests.
- `test_setup.py`: Application setup tests.
- `test_starvation.py`: Starvation logic and boundary tests.

Verify actual implementation before assuming a file's responsibilities.

## 4. Architecture Rules
- Keep API handling in `app.py`.
- Keep authentication in `auth.py`.
- Keep database connections in `db.py`.
- Keep SQL operations in `repository.py`.
- Keep validation in `schemas.py`.
- Keep business orchestration in `service.py`.
- Keep starvation calculations in `starvation.py`.
- Avoid duplicated logic and unnecessary abstractions.
- Avoid unrelated refactoring.

## 5. Python Standards
- Follow PEP 8.
- Use type hints and meaningful names.
- Prefer small, focused functions.
- Use parameterised SQL queries.
- Handle exceptions appropriately.
- Keep business logic testable.
- Preserve existing API contracts.

## 6. Testing
- Use pytest.
- Add tests in the existing `tests/` directory.
- Cover normal cases, edge cases and failures.
- Test authentication and operator isolation.
- Test UTC handling and time boundaries.
- Never weaken or remove tests to make them pass.

## 7. Documentation
Update `NOTES.md` when material assumptions, limitations or incomplete functionality change.

## 8. General Rules
- Understand existing code before proposing changes.
- Prefer minimal, targeted modifications.
- Preserve existing functionality.
- Avoid unnecessary dependencies.
- Explain important assumptions and trade-offs.
- Follow project approval instructions before editing files.

### 9. Codebase Navigation Best Practices

- Start with the project structure and relevant entry points before exploring implementation details.
- Follow the execution flow from app.py through the service, repository and database layers.
- Trace authentication through auth.py when investigating protected endpoints.
- Check the relevant tests alongside implementation code.
- Use targeted file searches and symbol references instead of reading the entire codebase.
- Follow existing imports, function calls and data flow before changing code.
- Reuse existing implementations rather than introducing duplicate functionality.
- Inspect related callers and tests before modifying shared functions or interfaces.
- Avoid unnecessary directory traversal and unrelated files.
- Do not assume file responsibilities or behaviour without inspecting the actual code.
- Summarise relevant findings briefly before proposing changes.