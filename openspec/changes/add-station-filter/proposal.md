# Change: Add Checked-At Timestamp

## Why
The starvation response includes the monitoring window but does not indicate when the check was performed.

## What Changes
- Add a `checked_at` field to `StarvationResult`.
- Populate it with the current UTC timestamp.
- Preserve all existing response fields and behaviour.

## Impact
- `station_health/schemas.py`: update the response model if applicable.
- `station_health/service.py`: populate the timestamp.
- `tests/test_service.py`: test timestamp generation and UTC awareness.

## Out of Scope
- Changes to starvation calculations.
- Changes to authentication.
- Database schema changes.
- Changes to existing monitoring windows.