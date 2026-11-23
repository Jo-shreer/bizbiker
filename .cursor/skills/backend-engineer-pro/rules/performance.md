# Performance and reliability

- Establish the expected workload and latency/throughput target before optimizing.
- Measure before making performance claims.
- Inspect query plans and query counts; avoid N+1 access.
- Use bounded pagination and avoid loading unbounded collections into memory.
- Configure PostgreSQL connection pooling and timeouts deliberately.
- Use async I/O for concurrent I/O workloads only when the full call path supports it.
- Set timeouts for external calls; use bounded retries with backoff and jitter only for retry-safe operations.
- Make retryable writes idempotent.
- Cache only with a clear invalidation and consistency strategy.
- Avoid blocking CPU-heavy work on the event loop; offload or use a worker system when justified.
- Add structured logs, metrics, traces, and health/readiness checks appropriate to the deployment.
