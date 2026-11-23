# Change: Add Optional Station ID Filter

## Why

Operators currently cannot restrict starvation checks to a specific station. Adding an optional station ID filter allows more targeted queries while preserving existing behaviour when no station is specified.

## What Changes

- Add an optional `station_id` query parameter to the starvation endpoint.
- Validate the supplied station ID.
- Apply the station filter when retrieving readings.
- Preserve operator-specific data isolation.
- Keep existing behaviour unchanged when `station_id` is omitted.

## Capabilities

- Update the existing starvation-check capability to support optional station filtering.

## Impact

- API: starvation endpoint and request validation.
- Service: apply the optional station filter.
- Repository: filter database queries by station ID.
- Tests: cover filtering, omitted parameters, invalid IDs and operator isolation.

## Out of Scope

- Changes to starvation calculation rules.
- Changes to authentication.
- Database schema changes unless existing schema inspection proves they are necessary.
- Changes to seed data.