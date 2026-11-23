# Bug-fixing workflow

1. Reproduce or characterize the reported behavior from evidence; do not guess at the cause.
2. Inspect logs, call paths, configuration, recent changes, and related code.
3. Write a short defect specification: expected behavior, actual behavior, reproduction conditions, impact, and constraints.
4. Identify the root cause and the narrowest safe correction.
5. Implement the fix without adding tests during the implementation phase.
6. Review regressions, security implications, and data consistency.
7. After implementation is complete, propose regression tests and wait for approval to add them.
8. Clearly distinguish confirmed facts from hypotheses.
