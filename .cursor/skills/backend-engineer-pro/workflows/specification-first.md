# Specification-first workflow

1. Restate the requested outcome and identify the user-visible behavior.
2. Inspect the existing project and identify relevant components and constraints.
3. Write a concise specification with:
   - context and goal
   - scope and explicit non-goals
   - actors and permissions
   - inputs, outputs, and validation
   - business rules and state transitions
   - success and error behavior
   - edge cases
   - data/schema impact
   - security and privacy requirements
   - performance/reliability expectations
   - acceptance criteria
4. Identify assumptions and ask only blocking questions.
5. Present the specification and implementation approach when requirements are ambiguous or high-impact. Do not start coding until material ambiguity is resolved.
6. Keep the spec updated if the user approves a change in scope.
7. Do not add test cases during implementation. Tests are a separate post-implementation phase by explicit user preference.
