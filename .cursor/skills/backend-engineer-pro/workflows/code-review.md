# Code review checklist

Review the change against the specification and consider:

- Correctness: does it meet all acceptance criteria?
- Security: authentication, authorization, validation, secrets, injection, data exposure.
- Data: constraints, transactions, concurrency, migrations, rollback/roll-forward.
- API: status codes, schemas, compatibility, pagination, error semantics.
- Reliability: timeouts, retries, idempotency, failure handling.
- Performance: query count, indexes, resource bounds, blocking calls.
- Architecture: clear boundaries, dependency direction, SOLID without overengineering.
- Operations: structured logs, metrics, health checks, configuration.
- Maintainability: naming, duplication, readability, dependency impact.
- Scope: no unrelated edits or accidental generated files.

Report findings by severity with file/line references where possible. Do not claim a review is clean if relevant files were not inspected.
