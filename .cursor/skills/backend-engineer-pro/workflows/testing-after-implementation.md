# Testing after implementation

Testing is deliberately deferred until production implementation is complete, per the user's workflow preference.

When the user asks for or approves the test phase:
1. Re-read the agreed specification and inspect the final implementation.
2. Create a test plan mapped to each acceptance criterion.
3. Add unit tests for domain rules and application behavior.
4. Add API/integration tests for FastAPI routes, dependency wiring, and PostgreSQL behavior.
5. Cover authorization, validation, error paths, boundaries, concurrency, and data integrity as relevant.
6. Use isolated fixtures and a dedicated test database; never point tests at production.
7. Run focused tests, then the relevant full suite.
8. Fix defects and rerun affected checks.
9. Report test commands, results, and remaining gaps.

Do not imply that unrun tests passed. If the user has not approved testing, provide the proposed test plan without creating test files.
