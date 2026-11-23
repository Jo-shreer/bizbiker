# Task: Implement Rate Limiting in Station Health FastAPI

## 1. Objective

Implement production-ready rate limiting in the existing Station Health FastAPI project. First inspect the repository and understand its authentication, middleware, configuration and testing conventions.

Do not rewrite unrelated code or introduce unnecessary dependencies.

## 2. Agreed Requirements

| Setting | Required value |
|---|---|
| Scope | All protected API endpoints |
| Client identity | Authenticated user ID only |
| Limit | 60 requests per user |
| Window | 60 seconds |
| Algorithm | Sliding Window Counter |
| Storage | In-memory |
| Deployment | Single application process |
| Failure policy | Fail Open |
| `/health` | Exempt |
| Authentication | Required |
| Configuration | Environment variables |
| Logging | Basic structured logging |

### Behaviour

- Authenticate requests before applying rate limits.
- Unauthenticated requests receive HTTP `401`.
- Each authenticated user has an independent counter.
- Requests exceeding the limit receive HTTP `429` with:
  ```json
  {"detail": "Rate limit exceeded. Please try again later."}
  ```
- Include a valid `Retry-After` response header.
- `/health` must never be rate-limited or consume a user's allowance.
- Authentication failures must never be bypassed by Fail Open behaviour.
- Internal rate-limiter errors must allow requests through and be logged.
- Never expose internal exceptions or authentication secrets.

### Algorithm and storage

Implement a Sliding Window Counter using weighted counts from the current and previous windows. Use a monotonic clock where appropriate.

In-memory counters must:
- Be independent per user.
- Support thread-safe concurrent updates.
- Prevent race conditions.
- Clean up expired entries automatically.
- Avoid unbounded memory growth.
- Reset on application restart.

Do not introduce Redis, databases or external storage.

**Deployment limitation:** Multiple processes or replicas maintain independent counters. Document that this implementation assumes a single application process.

### Environment variables

| Variable | Default |
|---|---|
| `RATE_LIMIT_ENABLED` | `true` |
| `RATE_LIMIT_REQUESTS` | `60` |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` |

Use the existing settings mechanism where possible. Validate configuration at startup. Disabling rate limiting must not disable authentication.

### Logging

Use existing Python logging. Log rate-limit rejections and internal limiter errors, including relevant user ID and endpoint. Never log passwords, tokens or secrets.

## 3. Existing Application Integration

The current application structure includes:

```python
from __future__ import annotations
import logging
from fastapi import FastAPI
from .middleware import request_context
from .starvation import router as starvation_router

app = FastAPI(title="Station Health")
logging.basicConfig(level=logging.INFO)
app.include_router(starvation_router)
app.middleware("http")(request_context)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

Inspect the actual repository before implementation. Reuse existing authentication, middleware, request context and configuration. Ensure correct execution order, preserve existing functionality, avoid duplicate middleware registration, and keep the implementation modular.

## 4. Automated Testing

Add tests using the existing testing framework. Cover:

- Requests within and exceeding the limit.
- HTTP 429 response and `Retry-After`.
- Independent counters for different users.
- HTTP 401 for unauthenticated requests.
- Authentication failures never bypassed.
- `/health` exemption.
- Sliding-window calculations, weighting and boundaries.
- Thread safety and concurrent requests.
- Expired-counter cleanup.
- Fail Open behaviour and error logging.
- Environment configuration, invalid values and disabled mode.

## 5. Code Quality

Use type hints, existing project conventions, modular design and minimal dependencies. Ensure compatibility with existing Python and FastAPI versions. Do not introduce unsynchronized global mutable state or silently swallow unrelated errors.

## 6. Mandatory Approval Workflow

**Never modify project files before explicit user approval.**

Follow these stages in order:

### Stage A — Inspect and propose (no changes)

1. Inspect the repository, authentication, middleware, configuration and tests.
2. Explain the implementation at a high level in simple terms.
3. List every file to create or modify, with its purpose.
4. Show the proposed code organized by filename.
5. Show the proposed test cases.
6. Explain important integration decisions and assumptions.

Then ask: **"Would you like me to proceed with these changes?"**

Stop and wait for explicit confirmation. If the user requests revisions, update the proposal and ask again.

### Stage B — Implement (after approval only)

1. Create and modify the approved files.
2. Implement all requirements in this specification.
3. Preserve unrelated functionality.
4. If additional or materially different changes become necessary, explain them and obtain approval first.

### Stage C — Test and report

1. Add and run the automated tests.
2. Run available linting, formatting and type checks.
3. Fix implementation-related failures.
4. Report created/modified files, implementation summary, configuration, tests added, commands executed, actual results and outstanding limitations.

Clearly distinguish passed, failed and unrun tests. Never claim tests passed unless actually executed.

## 7. Final Rules

- Preserve every agreed technical requirement.
- Do not invent authentication mechanisms; inspect and reuse the existing one.
- Do not make changes during analysis or proposal.
- Do not skip explicit approval.
- Implement only approved changes.
- Complete the tests after implementation.
- Do not change unrelated application behaviour.