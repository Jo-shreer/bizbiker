# FastAPI API design

- Use Pydantic request and response models; do not expose ORM entities directly.
- Define consistent response shapes and documented error semantics.
- Use correct HTTP methods and status codes.
- Validate path, query, and body inputs at the boundary.
- Enforce authentication and object-level authorization for every protected resource.
- Avoid leaking stack traces, SQL details, secrets, or internal identifiers in client errors.
- Use pagination and filtering for potentially large collections.
- Define request size limits and timeouts where appropriate.
- Consider idempotency for retryable operations and payment/order-like actions.
- Keep OpenAPI documentation accurate; hide internal endpoints where appropriate.
- Keep route functions thin and delegate use cases to application services.
