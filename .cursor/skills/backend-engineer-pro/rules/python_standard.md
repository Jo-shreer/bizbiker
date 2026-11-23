---
name: python-standards
description: Defines mandatory Python coding standards for production-grade backend development, including coding style, naming conventions, project structure, type safety, async programming, error handling, performance optimization, dead code removal, refactoring, maintainability, and code quality. Read this rule whenever creating, modifying, reviewing, optimizing, or refactoring Python code.
---

# Python Coding Standards

## Purpose

Define mandatory Python coding standards for writing, modifying, optimizing, and maintaining production-grade Python applications.

All Python implementation must prioritize correctness, readability, maintainability, security, and performance.

## 1. General Coding Principles

- Follow Python best practices and PEP 8.
- Prefer simple, explicit, readable code over clever or unnecessarily complex implementations.
- Follow the principle of least surprise.
- Avoid premature optimization and unnecessary abstractions.
- Follow DRY without creating excessive generalization.
- Apply SOLID principles where appropriate.
- Prefer composition over inheritance.
- Use functional programming principles where they improve clarity.
- Keep functions and modules focused on a single responsibility.
- Avoid deeply nested conditions and unnecessary control flow.
- Write code that is easy to understand, maintain, debug, and extend.

## 2. Naming Conventions

Follow consistent Python naming conventions.

- Variables and functions: `snake_case`.
- Modules and packages: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Private implementation details: prefix with `_`.
- Type variables: descriptive `PascalCase` names.
- Boolean variables: use meaningful prefixes such as `is_`, `has_`, `can_`, and `should_`.
- Functions must use descriptive, action-oriented names.
- Avoid abbreviations unless widely understood.
- Avoid generic names such as `data`, `value`, `obj`, and `temp` when more descriptive names are possible.

Examples:

Good:
- `is_active`
- `has_permission`
- `get_user_by_id`
- `calculate_order_total`
- `validate_payment_request`

Avoid:
- `flag`
- `check`
- `process_data`
- `tmp`
- `x`

## 3. Project and Module Organization

- Use lowercase `snake_case` for file and directory names.
- Organize modules by responsibility and domain.
- Keep modules cohesive and avoid unrelated functionality in the same file.
- Avoid circular imports.
- Avoid unnecessary package nesting.
- Keep public interfaces explicit.
- Avoid wildcard imports.
- Keep imports at the top of the module unless a local import is necessary to resolve a genuine dependency issue.
- Separate business logic from infrastructure concerns.
- Avoid creating modules containing only one trivial function unless separation provides a clear benefit.

## 4. Functions and Methods

- Keep functions focused on one responsibility.
- Prefer small, understandable functions.
- Use descriptive function and parameter names.
- Avoid functions with excessive parameters.
- Group related parameters into a Pydantic model or dataclass when appropriate.
- Avoid unnecessary side effects.
- Keep pure business logic separate from I/O operations where practical.
- Prefer early returns and guard clauses.
- Avoid unnecessary `else` and `elif` branches after returning.
- Avoid deeply nested loops and conditions.
- Never use mutable default arguments.
- Return meaningful values instead of modifying unrelated external state.
- Raise specific exceptions rather than returning ambiguous values.

## 5. Type Hints and Type Safety

- Add type hints to all function parameters and return values.
- Prefer precise types over `Any`.
- Use unions, generics, protocols, and type aliases appropriately.
- Use `TypedDict` for typed dictionary structures when necessary.
- Prefer Pydantic models for validated API data.
- Avoid unnecessary type casting.
- Avoid suppressing type-checking errors without justification.
- Keep type annotations accurate and synchronized with implementation.
- Use a static type checker such as mypy or Pyright when configured in the project.

## 6. Pythonic and Modern Practices

- Use modern Python features supported by the project's Python version.
- Prefer context managers for resource management.
- Use comprehensions when they improve readability.
- Use generators for memory-efficient iteration where appropriate.
- Use `enumerate()` instead of manually managing indexes.
- Use `zip()` for parallel iteration.
- Use `pathlib` for filesystem paths.
- Use `dataclasses` for simple structured internal data where appropriate.
- Prefer standard-library functionality before introducing third-party dependencies.
- Avoid unnecessary classes and inheritance.
- Avoid overly compressed one-line expressions.

## 7. Async and Concurrency

- Use `async def` for asynchronous operations.
- Use `await` for awaitable operations.
- Never call blocking I/O directly inside asynchronous execution paths.
- Prefer asynchronous database, HTTP, and filesystem clients where appropriate.
- Use synchronous functions for purely synchronous operations.
- Do not use `async` without actual asynchronous work.
- Avoid unnecessary task creation and concurrency.
- Use `asyncio.gather()` only when operations can safely execute concurrently.
- Handle cancellation, timeouts, and exceptions correctly.
- Avoid shared mutable state across concurrent tasks.
- Use thread or process executors when CPU-bound or blocking work must be offloaded.

## 8. Error and Exception Handling

- Handle expected errors explicitly.
- Catch specific exceptions instead of broad `Exception` handlers.
- Avoid silently swallowing exceptions.
- Preserve exception context using exception chaining where appropriate.
- Do not use exceptions for ordinary control flow.
- Validate inputs at appropriate boundaries.
- Provide actionable error messages without exposing sensitive information.
- Log exceptions with sufficient diagnostic context.
- Avoid duplicate logging at multiple layers.
- Never expose internal stack traces or implementation details to API consumers.

## 9. Performance and Optimization

- Prioritize algorithmic efficiency and appropriate data structures.
- Avoid unnecessary database queries and external API calls.
- Avoid repeated calculations when results can safely be reused.
- Avoid unnecessary object creation and copying.
- Use generators and iterators for large data processing.
- Avoid loading large datasets entirely into memory.
- Use efficient built-in operations and standard-library functions.
- Avoid unnecessary loops and repeated collection scans.
- Use caching only when there is a clear benefit and a defined invalidation strategy.
- Optimize serialization and deserialization in performance-sensitive paths.
- Consider memory consumption as well as execution time.
- Measure performance before introducing complex optimizations.
- Avoid sacrificing readability for insignificant performance gains.

## 10. Dead Code and Unused Code

- Remove unused imports, variables, functions, classes, and modules.
- Remove unreachable code and obsolete branches.
- Remove commented-out code instead of keeping it as a backup.
- Remove unused dependencies when safe and approved.
- Identify duplicate implementations and consolidate them when appropriate.
- Avoid retaining deprecated implementations without a migration reason.
- Check references before removing public interfaces or shared functionality.
- Do not remove code merely because it appears unused without checking dynamic imports, reflection, framework registration, and external consumers.

## 11. Refactoring Standards

- Refactor code when it improves readability, maintainability, reliability, or performance.
- Preserve existing behavior unless a behavior change is explicitly specified.
- Avoid combining unrelated refactoring with feature implementation.
- Reduce duplication without introducing unnecessary abstractions.
- Extract complex logic into focused functions.
- Simplify conditional logic and excessive nesting.
- Improve naming when it makes intent clearer.
- Break down oversized modules and functions when justified.
- Remove obsolete abstractions and unnecessary indirection.
- Maintain backward compatibility for public interfaces unless a breaking change is approved.
- Review all affected call sites when changing shared code.
- Document significant architectural or behavioral changes.
- Avoid large-scale refactoring without a clear specification and scope.

## 12. Code Quality and Maintainability

- Keep code consistent with existing project conventions.
- Avoid magic numbers and unexplained string literals.
- Use constants for meaningful repeated values.
- Avoid global mutable state.
- Avoid unnecessary comments that merely repeat the code.
- Add comments to explain complex decisions and non-obvious behavior.
- Keep documentation synchronized with implementation.
- Prefer explicit dependencies over hidden global dependencies.
- Ensure resource cleanup through context managers and lifecycle management.

## 13. Dependencies and Standard Library

- Prefer the Python standard library when it adequately solves the problem.
- Avoid adding dependencies for trivial functionality.
- Use maintained and reputable packages.
- Avoid duplicate libraries that solve the same problem.
- Pin and manage dependencies according to project conventions.
- Review dependency compatibility and security implications.
- Do not introduce new dependencies without a clear technical reason.
- Check the existing dependency configuration before installing or upgrading packages.

## 14. Code Formatting and Static Analysis

Follow the tools already configured in the project.

Recommended tools:

- Ruff: linting and formatting.
- Pyright or mypy: static type checking.
- Bandit: Python security analysis.
- pre-commit: automated code quality checks.

Standards:

- Follow the existing formatter and linter configuration.
- Do not introduce conflicting formatters or linters.
- Resolve relevant linting and type-checking issues.
- Do not disable rules simply to hide implementation problems.
- Avoid unrelated formatting changes across the codebase.

## 15. Documentation

- Use clear docstrings for public functions, classes, and modules where useful.
- Follow a consistent docstring convention.
- Document complex business rules and non-obvious implementation decisions.
- Document important exceptions and side effects.
- Keep documentation accurate and updated.
- Avoid excessive comments and redundant documentation.

## 16. Implementation Review Checklist

Before completing Python implementation, verify:

- [ ] Naming conventions are consistent.
- [ ] Functions and modules have clear responsibilities.
- [ ] Type hints are complete and accurate.
- [ ] Async and synchronous operations are used correctly.
- [ ] No accidental blocking I/O exists in async paths.
- [ ] Error handling is explicit and appropriate.
- [ ] Unused imports and dead code are removed.
- [ ] No unnecessary dependencies were introduced.
- [ ] Performance and memory usage have been considered.
- [ ] Refactoring preserves existing behavior.
- [ ] Code follows project conventions.
- [ ] No unnecessary abstractions or duplicated logic were introduced.
- [ ] Documentation reflects meaningful implementation changes.

## 17. Mandatory Engineering Principles

1. Readability is more important than cleverness.
2. Correctness comes before optimization.
3. Measure before optimizing.
4. Avoid premature abstraction.
5. Remove dead code when safe.
6. Refactor incrementally and preserve behavior.
7. Follow existing project conventions unless there is a good reason to improve them.
8. Never introduce complexity without a clear benefit.
9. Do not sacrifice maintainability for fewer lines of code.
10. Do not add tests during implementation. Testing follows the separate post-implementation workflow and requires user approval.