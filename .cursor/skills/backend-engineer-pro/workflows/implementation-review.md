# Implementation review (before tests)

After implementation, compare the code to the specification and inspect the complete diff.

Review:
- acceptance criteria and behavior
- authorization and data exposure
- input validation and error handling
- transaction boundaries and database constraints
- migration safety and compatibility
- async correctness, timeouts, retries, and idempotency
- query count, indexes, pagination, and resource bounds
- logging, metrics, and sensitive-data handling
- maintainability and unnecessary complexity
- accidental or unrelated changes

Run available non-test checks where appropriate (formatting, linting, type checking, import checks, migration validation). Do not create test cases in this phase. Report checks and results accurately.
