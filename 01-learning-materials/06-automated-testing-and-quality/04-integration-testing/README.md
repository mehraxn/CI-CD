# Integration Testing

## Testing the Seams

An **integration test** verifies that components work *together* across a real boundary: application code with a **database**, a service with the **filesystem**, one service calling another over **HTTP**, a producer and a **message queue**. Unit tests prove each part; integration tests prove the wiring — the queries actually match the schema, the serialization survives the round trip, the transaction really commits.

```text
Application code
      ↓
Real database or realistic test service
      ↓
Integration behavior
      ↓
Assertions about the combined result
```

## Choosing the Dependency's Form

The central design decision is what stands on the other side of the boundary:

- **Real dependency** — highest fidelity; acceptable when cheap and disposable (a local SQLite file). Never production services.
- **Containerized dependency** — a real engine (PostgreSQL, Redis) in a disposable container: high fidelity, per-run isolation. In GitHub Actions this is the `services:` block; the Testcontainers libraries start containers from test code; Docker Compose can assemble multi-service test stacks.
- **Fake implementation** — an in-memory stand-in: fast, less faithful (no real SQL, no real network).
- **Stubbed external service** — for third-party APIs you cannot run locally: simulated responses at the HTTP level.
- **Shared test environment** — a long-lived staging-like system: most realistic and most trouble (shared state, contention, drift).

The trade-off runs one direction: fidelity up, speed and isolation down. Pick the cheapest form that can catch the bugs you are targeting.

A conceptual service-container job (not currently used in this repository):

```yaml
jobs:
  integration-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test-password
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4
      - run: echo "Run integration tests"
```

## The Hygiene List

Integration tests fail for environmental reasons unit tests never meet, so they need operational discipline:

- **Test database and migrations** — build the schema the same way production does (run the migrations), then load controlled **seed data** via **fixtures**.
- **Cleanup and isolation** — every test leaves the world as it found it: rollback **transactions**, truncate tables, or (best) give each test its own throwaway database. **Unique resource names** (per-run database names, temp paths) prevent parallel runs from colliding.
- **Environment variables and ports** — connection details must be injected, not hard-coded; hard-coded ports collide on shared runners.
- **Readiness checks** — a started container is not a ready service; poll a **health check** before testing, with a **timeout** so a dead service fails fast instead of hanging.
- **Retry behavior** — retry *connection establishment* during startup; do not retry test assertions (a deterministic failure retried is still a failure — see [failure handling](../../03-pipeline-architecture/07-retries-timeouts-cancellation-and-failures/)).
- **Logs on failure** — capture and print the dependency's logs when a test fails; without them, CI-only failures are unsolvable.

## Common Mistakes

- Calling every test an integration test until the term means nothing.
- Depending on production services from tests.
- Shared database state coupling tests together.
- Hard-coded ports and connection strings.
- Missing readiness checks — the "works locally, races in CI" classic.
- No cleanup, so failures cascade into later tests.
- Retrying deterministic failures.
- Hiding useful logs from failed runs.
- A very slow integration suite with no selection strategy, so people stop running it.

## Existing Repository Evidence

- [TaskOps tests](../../../Projects/1_project/taskops-cicd/tests/) are genuine lightweight integration tests: [conftest.py](../../../Projects/1_project/taskops-cicd/tests/conftest.py) creates a **real SQLite database in a temp file per test**, the app runs against it, and teardown deletes the file *and its WAL sidecar files* — cleanup done properly. `test_database.py` exercises the database layer directly; `test_routes.py` goes through HTTP to the same real database.
- The **container-level integration check** in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml)'s `docker` job starts the freshly built image and polls `/health` up to 10 times with sleeps — a real readiness-check loop with a bounded retry, plus `docker logs` printed on failure and an `if: always()` cleanup step. It demonstrates nearly every hygiene item above in miniature.
- [KubeOps tests](../../../Projects/2_project/kubeops-gitops/tests/) use a **fake** (in-memory store) rather than a containerized database — the deliberate other end of the fidelity trade-off.
- GitHub Actions `services:`, Testcontainers, and Compose-based test stacks are not currently demonstrated; the `services:` example above is conceptual.

## Practical Exercise

Audit the repository's integration boundaries. For each project, answer with file references: which tests interact with (a) a database, (b) the filesystem, (c) an HTTP layer, (d) a container? For TaskOps specifically, trace the full lifecycle of the test database — where it is created, what uses it, where it is cleaned up — and identify what would break if two tests shared one database file. Do not modify anything. Target 20–30 minutes.

## Knowledge Check

1. What do integration tests verify that unit tests cannot?
2. Rank real, containerized, fake, and stubbed dependencies by fidelity.
3. Why are readiness checks essential with containerized dependencies?
4. When is retrying acceptable in integration tests?
5. How does TaskOps keep database tests isolated from each other?
6. What integration hygiene does the TaskOps CI smoke-test step demonstrate?

<details>
<summary>View answers</summary>

1. The interaction across real boundaries — queries against real schemas, serialization round trips, transactional behavior — the wiring between verified parts.
2. Real > containerized > stubbed external service ≈ fake (order of the last two depends on what is simulated); fidelity trades against speed and isolation.
3. A started container is not yet a ready service; testing before readiness produces false failures that look like flakiness.
4. For connection establishment during dependency startup, bounded by a timeout — never for retrying failed assertions.
5. Each test gets its own temp-file SQLite database from the fixture, deleted (with WAL sidecars) in teardown.
6. Bounded readiness polling with timeout, failure evidence (`docker logs`), and guaranteed cleanup via `if: always()`.

</details>

## Navigation

- [Back to Automated Testing and Quality](../README.md)
- [Previous: Unit Testing](../03-unit-testing/)
- [Next: API, Contract, End-to-End, and Smoke Testing](../05-api-contract-end-to-end-and-smoke-testing/)
- [Back to All Learning Materials](../../README.md)
