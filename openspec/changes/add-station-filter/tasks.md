# Tasks

## 1. Update the response model

- [ ] Add a `checked_at` field to `StarvationResult`.
- [ ] Ensure the field uses a UTC-aware datetime.

## 2. Update the starvation service

- [ ] Generate the current UTC timestamp when the starvation check executes.
- [ ] Populate the `checked_at` field in the returned result.
- [ ] Preserve existing starvation calculations and monitoring window behaviour.

## 3. Add tests

- [ ] Test that the starvation result includes `checked_at`.
- [ ] Test that the timestamp is timezone-aware and uses UTC.
- [ ] Test that existing response fields remain unchanged.

## 4. Verify

- [ ] Run the relevant service tests.
- [ ] Run the full test suite.
- [ ] Confirm all existing tests pass.