# Notes

## Endpoint
- `GET /stations/{station_id}/starvation?date=YYYY-MM-DD` with `Authorization: Bearer <token>`.
- Response: `station_id`, `date`, `starved`, `empty_reading_count`, `min_empty_readings`, `window_start`, `window_end`.
- Structure: `starvation.py` (route), `service.py` (rule and window), `repository.py` (SQL), `schemas.py` (response model), `auth.py` (token lookup), `middleware.py` (request logging).
- Each request is logged with a request id (`X-Request-ID`), method, path, status and duration. Tokens are never logged. Logs go to the console (and to `station_health.log` if the file handler is enabled; the file is gitignored).

## Assumptions
- **Auth:** the token is looked up in the supplied `TOKENS` mapping. Missing or unknown token returns 401.
- **Operator isolation:** the station lookup is `WHERE id = ? AND operator_id = ?`. Another operator's station returns the same 404 as a nonexistent one.
- **Window:** `[date + peak_start, date + peak_end)`, start inclusive and end exclusive. Peak times and the requested date are interpreted in `PEAK_TIMEZONE` (UTC, per the brief). Per-operator timezones would need a schema change.
- **Duplicate readings** (same station and timestamp) count once, using `COUNT(DISTINCT recorded_at)`. Station 104 therefore gives 2 and is not starved. If two rows at the same timestamp disagreed, the timestamp would count as empty if any row had 0 bikes.
- **`docks_total = 0`** is not treated specially. Readings with 0 bikes are counted literally, so station 103 is starved. This is easy to change if such stations should be excluded.
- **Timestamps** are compared as strings, assuming the seeded format (`+00:00` UTC offset, same layout).
- **Future dates** are rejected with 422, because starvation is computed from recorded readings and cannot be known in advance. Today is accepted and its count reflects readings recorded so far. The comparison uses the current UTC date.
- **No readings** on a past date returns 200 with count 0 and `starved: false`.
- **Validation:** `station_id` must be between 1 and 2^63 - 1, and `date` must be a valid ISO date, otherwise 422.
- **Missing operator config** returns 500. The schema does not enforce one config row per operator.
- **Response format:** datetimes are serialised by Pydantic, so UTC appears as `Z` (for example `2026-09-15T08:00:00Z`) rather than `+00:00`.
- **Concurrency:** the route is `async`; blocking SQLite work runs in a worker thread via `run_in_threadpool`. Each request opens, uses and closes its own connection in that one thread. Tests patch `DATABASE_PATH` instead of overriding a dependency.
- **No retry or timeout handling.** SQLite is local and the endpoint is read-only.

## Setup changes
- Added `pydantic>=2,<3` to `requirements.txt` (response model).
- No changes to run commands or seed data.

## Incomplete
- Nothing known. All tests in `tests/test_starvation.py` and `tests/test_service.py` are passing.

## What I'd do next in production
- Rate limiting at the gateway.
- Signed tokens (for example JWT) with hashed storage, instead of a static mapping.
- Unique constraint on `(station_id, recorded_at)` to stop duplicates at the source, and a real timestamp type instead of text.
- Connection pool with timeouts and retries, and an async driver, once the database moves off SQLite.
- Structured JSON logging with request ids, latency and metrics.
- Option to reject today until the peak window has ended, so partial counts are not reported as results.