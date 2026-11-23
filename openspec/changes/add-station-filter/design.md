# Design

## Context

The existing starvation result includes the monitoring window timestamps but does not record when the check was executed.

See `proposal.md` and `specs/starvation-result/spec.md`.

## Goals / Non-Goals

**Goals:**
- Generate a UTC-aware timestamp when the starvation check executes.
- Preserve the existing response structure and behaviour apart from the new field.

**Non-Goals:**
- Database changes.
- Changes to monitoring window calculations.
- Changes to authentication or repository queries.

## Decisions

### 1. Generate the timestamp in the service layer

Generate `checked_at` when the starvation check is executed in `service.py`.

**Rationale:**
- The service coordinates the operation.
- No database persistence is needed.
- The timestamp reflects execution rather than the monitoring window.

**Alternative considered:**
- Generate the timestamp in the API route. Rejected because it places business-related response construction in the HTTP layer.

### 2. Use an explicit UTC-aware timestamp

Use Python's timezone-aware UTC datetime functionality.

**Rationale:**
- Avoid naive datetime values.
- Make the timestamp unambiguous across time zones.

**Alternative considered:**
- Use local system time. Rejected because results should be consistent regardless of server location.

### 3. Keep the change backward-compatible where possible

Preserve existing response fields and calculations. Add only the new timestamp field.

## Risks / Trade-offs

- **System clock inaccuracies** → The timestamp depends on the host system clock being configured correctly.
- **Naive datetime accidentally returned** → Add a test verifying UTC awareness.

## Migration Plan

- No database migration is required.
- Deploy the updated application and tests.
- Rollback by reverting the application change if necessary.