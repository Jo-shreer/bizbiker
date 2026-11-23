# Spec Delta

## Purpose

Ensure starvation check responses communicate when the check was performed, allowing consumers to distinguish the check timestamp from the monitoring window.

## ADDED Requirements

### Requirement: Starvation results include a check timestamp

The system SHALL include a `checked_at` timestamp in every starvation check response, representing when the check was performed in UTC.

#### Scenario: Successful starvation check

- **WHEN** an authenticated operator requests a starvation check
- **THEN** the response includes a `checked_at` timestamp representing the check time in UTC

#### Scenario: Existing response fields are preserved

- **WHEN** a starvation check response is returned
- **THEN** all existing response fields remain available and retain their existing meanings

#### Scenario: Check timestamp is distinct from monitoring window

- **WHEN** a starvation check response is returned
- **THEN** `checked_at` represents the execution time and is distinct from `window_start` and `window_end`