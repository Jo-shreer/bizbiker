---
description: Python coding standards covering readability, type hints, naming, error handling, async programming, maintainability and code quality.
globs: "**/*.py"
alwaysApply: false
---

# Python Coding Standards

## 1. General Principles

Write production-quality Python code that prioritizes:

- Readability and simplicity.
- Maintainability and extensibility.
- Explicit behavior and predictable execution.
- Performance without premature optimization.
- Security and reliability.
- Separation of responsibilities.

Follow PEP 8, PEP 257 and established Python conventions.

Prefer simple, idiomatic Python over unnecessary abstractions or clever implementations.

## 2. Naming Conventions

Follow standard Python naming conventions:

- Modules and packages: `snake_case`.
- Functions and variables: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Private attributes and methods: `_leading_underscore`.
- Type variables: descriptive `PascalCase` names.

Use descriptive names that communicate purpose.

Avoid unclear abbreviations, single-character names outside short loops, and misleading names.

## 3. Formatting and Imports

- Use four spaces for indentation.
- Follow the project's configured formatter.
- Prefer Ruff formatting or the existing Black configuration.
- Use a consistent import order.
- Group imports into standard library, third-party and local application imports.
- Avoid wildcard imports.
- Remove unused imports and variables.
- Keep functions and expressions reasonably concise.
- Avoid deeply nested conditional statements.

Do not introduce a new formatter or change formatting configuration without checking the existing project setup.

## 4. Type Hints

Use Python type annotations consistently.

- Annotate function parameters and return values.
- Use specific types instead of `Any` wherever possible.
- Use `list[T]`, `dict[K, V]` and other modern generic types.
- Use `str | None` for optional values when supported by the project's Python version.
- Use `Enum` for fixed sets of meaningful values.
- Use `TypedDict`, `Protocol` or dataclasses when they improve type clarity.
- Avoid unnecessary type ignores.

Example:

    def calculate_total(
        quantity: int,
        unit_price: float,
    ) -> float:
        return quantity * unit_price

Use `None` explicitly when checking for missing values:

    if user_id is None:
        raise ValueError("User ID is required")

Do not use `Any` as a shortcut for avoiding proper typing.

## 5. Functions and Classes

- Keep functions focused on one responsibility.
- Prefer small, reusable functions.
- Avoid excessive parameters.
- Avoid unnecessary classes.
- Use classes when they represent meaningful domain concepts or encapsulate state and behavior.
- Avoid functions with hidden side effects.
- Prefer explicit dependencies over global state.
- Avoid mutable default arguments.

Use keyword-only arguments when they improve clarity for functions with multiple parameters.

## 6. Error Handling

- Raise specific exceptions.
- Catch only exceptions that can be handled meaningfully.
- Avoid bare `except`.
- Never silently swallow exceptions.
- Do not use exceptions for ordinary control flow.
- Preserve the original exception when re-raising with additional context.
- Do not expose internal implementation details or secrets in error messages.

Bad:

    try:
        process_data()
    except Exception:
        pass

Good:

    try:
        process_data()
    except DatabaseError as exc:
        logger.exception("Database operation failed")
        raise ServiceError("Unable to process the request") from exc

Do not catch broad exceptions unless there is a clear boundary-level reason, such as logging and translating an unexpected application failure.

## 7. Async Programming

Use asynchronous programming appropriately.

- Use `async def` for functions that await asynchronous operations.
- Await asynchronous I/O operations.
- Do not call blocking I/O directly inside an async function.
- Use asynchronous database drivers when the project uses an async database architecture.
- Use thread offloading for unavoidable blocking synchronous operations.
- Do not pass an async function to a synchronous thread-pool helper.
- Avoid unnecessary `async` declarations for purely synchronous operations.
- Do not use `asyncio.create_task()` without considering task lifecycle and exception handling.

Do not mix synchronous and asynchronous database access patterns without a deliberate architectural decision.

## 8. Data Structures and Resource Management

- Choose data structures appropriate to the problem.
- Prefer immutable values when practical.
- Use context managers for files, connections and other managed resources.
- Avoid unnecessary copying of large collections.
- Avoid mutable global state.
- Use generators for large sequential data processing when appropriate.
- Validate data at system boundaries.

## 9. Logging

Use the standard Python logging module or the project's established logging framework.

- Do not use `print()` for production logging.
- Use appropriate log levels.
- Include useful contextual information.
- Avoid logging passwords, access tokens, API keys or sensitive personal data.
- Use structured logging if supported by the project.
- Include exception information when recording failures.

## 10. Documentation

- Add docstrings to public modules, classes and functions where useful.
- Follow a consistent docstring format.
- Explain complex business logic and non-obvious decisions.
- Avoid comments that simply repeat the code.
- Keep documentation synchronized with implementation changes.

## 11. Configuration and Secrets

- Do not hardcode credentials, secrets, tokens or environment-specific settings.
- Use the project's configuration management approach.
- Read environment-specific values from configuration.
- Validate required configuration at application startup.
- Provide safe defaults only when appropriate.

## 12. Code Quality and Maintainability

- Avoid duplicated logic.
- Follow SOLID principles where relevant.
- Prefer composition over unnecessary inheritance.
- Avoid circular imports.
- Avoid unnecessary dependencies.
- Avoid premature optimization.
- Preserve existing project conventions.
- Do not introduce abstractions without a clear benefit.

## 13. Code Change Requirements

Before modifying code:

1. Inspect the existing implementation.
2. Understand its callers and dependencies.
3. Identify the expected behavior.
4. Consider backward compatibility.
5. Make the smallest appropriate change.

After implementation:

1. Review the modified code.
2. Check types, imports and error handling.
3. Check for unintended side effects.
4. Identify potential security and performance issues.
5. Summarize the changes.

Do not create or execute tests during implementation. Testing must only happen after implementation is complete and the user explicitly approves it.

## 14. Priority of Standards

Apply standards in this order:

1. Explicit user requirements.
2. Existing project architecture and conventions.
3. Project-specific Cursor rules.
4. These general Python standards.
5. General Python community conventions.

If a deviation is necessary, explain why rather than silently introducing it.