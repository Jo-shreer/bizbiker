# Specification: JWT Authentication for Station Starvation Endpoint

## 1. Objective

Implement JWT-based authentication for the following endpoint only:

`GET /stations/{station_id}/starvation`

The implementation must authenticate the operator making the request while preserving the existing endpoint behaviour and business logic.

No other endpoint should require authentication as part of this change.

## 2. Scope

### In scope

- JWT authentication using HS256.
- Pre-generated JWTs for existing operators.
- Secure configuration of the JWT signing secret.
- JWT signature and payload validation.
- Integration with the existing FastAPI dependency-injection system.
- Consistent HTTP 401 responses for authentication failures.
- Preservation of existing station ownership checks and endpoint behaviour.

### Out of scope

- Login or registration endpoints.
- Password-based authentication.
- Token expiration.
- Refresh tokens.
- Database token storage.
- Role-based access control.
- Authentication for other endpoints.

## 3. Functional Requirements

### FR-01: JWT Generation

- Generate one JWT for each existing operator.
- Use HS256 as the signing algorithm.
- Include the operator ID in the JWT `sub` claim.
- Store the operator ID as a string in `sub`.
- Do not include an `exp` claim.
- Generate tokens once, not when the application starts.
- Tokens must remain unchanged across application restarts.

### FR-02: Secret Configuration

- Read the JWT signing secret from the `JWT_SECRET_KEY` environment variable.
- Never hardcode the signing secret in application code.
- Use the same secret for signing and validating tokens.
- The secret must be sufficiently strong.
- If the secret is missing, treat this as a server configuration error rather than an invalid client token.

### FR-03: Token Storage

- Retain the existing `TOKENS` dictionary in `supplied.py`.
- Replace the existing static tokens with the pre-generated JWTs.
- JWT strings must be dictionary keys.
- Operator IDs must remain dictionary values.

Expected structure:

```python
TOKENS: dict[str, int] = {
    "<jwt-for-operator-1>": 1,
    "<jwt-for-operator-2>": 2,
}
```

- Do not introduce database token storage.
- Do not regenerate tokens during application startup.

### FR-04: JWT Authentication

- Extract the Bearer token from the Authorization header.
- Reject requests with missing or empty tokens.
- Verify the JWT signature using the configured secret.
- Accept only the HS256 algorithm.
- Decode the JWT payload.
- Extract the operator ID from the `sub` claim.
- Validate that the operator ID is present and valid.
- Check that the exact JWT exists in the `TOKENS` dictionary.
- Verify that the decoded operator ID matches the operator ID associated with that token in the dictionary.
- Return the authenticated operator ID to the endpoint.

### FR-05: Authentication Error Handling

All client authentication failures must return:

- HTTP status: `401 Unauthorized`.
- A consistent error response.
- No sensitive implementation details in the response.

The following cases must be rejected:

- Missing Authorization header.
- Missing or empty Bearer token.
- Malformed JWT.
- Invalid JWT signature.
- Unsupported signing algorithm.
- Token not present in the `TOKENS` dictionary.
- Missing or invalid `sub` claim.
- Invalid operator ID.
- Operator ID mismatch between JWT and dictionary.
- Modified JWT payload.

A missing server-side signing secret is a configuration failure, not a client authentication failure.

### FR-06: Endpoint Integration

- Protect only `GET /stations/{station_id}/starvation`.
- Use FastAPI dependency injection for authentication.
- Preserve the existing endpoint signature and business logic wherever possible.
- Pass the authenticated operator ID into the existing station ownership validation.
- Preserve existing 404, 422 and 500 behaviour.
- Do not change authentication behaviour for unrelated endpoints.

## 4. Implementation Plan

The implementation will be broken into the following proposed tasks. The exact approach and task breakdown can be adjusted during the high-level design discussion.

### Priority 1: JWT Configuration and Generation

**Objective:** Configure the signing secret and generate fixed JWTs for existing operators.

Expected work:

- Add the required JWT library.
- Configure `JWT_SECRET_KEY`.
- Ensure the environment file is not committed to source control.
- Establish a one-time JWT generation process.
- Generate one HS256 JWT per operator.
- Include the operator ID in the `sub` claim.
- Exclude the expiration claim.
- Replace existing static tokens in `supplied.py`.
- Ensure tokens are not regenerated on application startup.

**Expected outcome:** Fixed, pre-generated JWTs and a configured signing secret.

### Priority 2: JWT Authentication

**Objective:** Replace static-token validation with JWT validation.

Expected work:

- Extract the Bearer token.
- Verify the signature using HS256.
- Decode and validate the `sub` claim.
- Check exact token membership in `TOKENS`.
- Verify the operator ID matches the dictionary value.
- Return the authenticated operator ID.
- Handle authentication failures consistently.

**Expected outcome:** A reusable FastAPI authentication dependency.

### Priority 3: Endpoint Integration

**Objective:** Protect the starvation endpoint using the JWT authentication dependency.

Expected work:

- Apply the dependency to the starvation endpoint.
- Pass the authenticated operator ID into existing business logic.
- Preserve station ownership validation.
- Preserve existing response and error behaviour.
- Confirm unrelated endpoints remain unaffected.

**Expected outcome:** The starvation endpoint requires a valid JWT without changing its existing business behaviour.

### Priority 4: Documentation and Final Review

**Objective:** Review the implementation against the agreed requirements.

Expected work:

- Review JWT configuration and validation.
- Review secret handling.
- Confirm tokens are not regenerated at startup.
- Confirm only the intended endpoint is protected.
- Review code organisation and consistency.
- Update project documentation if needed.

**Expected outcome:** Feature implementation is complete and ready for testing.

## 5. Testing Strategy

Testing will be implemented separately, after feature implementation is complete and when explicitly requested.

### 5.1 Successful Authentication

- Valid JWT for operator 1.
- Valid JWT for operator 2.
- Correct operator ID returned from the dependency.
- Fixed JWT remains valid after application restart, provided the secret and token configuration remain unchanged.

### 5.2 Authentication Failure Scenarios

- Missing Authorization header.
- Missing Bearer token.
- Empty Bearer token.
- Malformed JWT.
- Invalid signature.
- Unsupported algorithm.
- JWT signed using a different secret.
- Validly signed JWT that is not registered in `TOKENS`.
- Missing `sub` claim.
- Invalid `sub` claim.
- Zero or negative operator ID.
- Operator ID mismatch.
- Modified JWT payload.

All client authentication failures must return HTTP 401.

### 5.3 Configuration Scenarios

- Missing `JWT_SECRET_KEY`.
- Empty `JWT_SECRET_KEY`.
- Invalid signing configuration.

These must be handled as server configuration failures rather than incorrectly reported as invalid client credentials.

### 5.4 Endpoint Integration Tests

- Valid operator accessing their own station.
- Valid operator attempting to access another operator's station.
- Request for a nonexistent station.
- Invalid station ID.
- Missing date parameter.
- Invalid date parameter.
- Future date.
- Existing 404 behaviour.
- Existing 422 behaviour.
- Existing 500 behaviour.
- Unrelated endpoints remain accessible without JWT authentication.

### 5.5 Testing Principles

The testing phase must include:

- Happy-path tests.
- Negative tests.
- Boundary-value tests.
- Security-focused tests.
- Endpoint integration tests.
- Relevant edge cases.

After implementation:

1. Run the complete test suite.
2. Investigate and fix failures.
3. Rerun the tests.
4. Report the test results clearly.

## 6. Acceptance Criteria

The feature is considered complete when:

- JWTs are generated using HS256.
- Each existing operator has a fixed JWT.
- The JWT contains the correct operator ID in `sub`.
- No `exp` claim is included.
- The signing secret is loaded from `JWT_SECRET_KEY`.
- The secret is not hardcoded.
- JWT signatures are verified before trusting the payload.
- Only registered tokens are accepted.
- The JWT subject matches the operator ID in `TOKENS`.
- Invalid or missing client credentials return HTTP 401.
- Only the starvation endpoint requires authentication.
- Existing station ownership validation is preserved.
- Existing endpoint business logic and response behaviour are preserved.
- Tokens are not regenerated on application startup.

Testing acceptance will be assessed separately when the testing phase is requested.

## 7. Security Considerations

- The JWT signing secret must be sufficiently random and kept private.
- The `.env` file must not be committed to source control.
- JWTs stored in source code are long-lived credentials and must not be exposed publicly.
- Because tokens have no expiration, they remain valid until removed from `TOKENS` or the signing secret is changed.
- The allowed algorithm must be explicitly restricted to HS256 during validation.
- Never select the validation algorithm based on an untrusted JWT header.