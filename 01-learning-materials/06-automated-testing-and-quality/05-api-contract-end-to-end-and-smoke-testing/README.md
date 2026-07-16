# API, Contract, End-to-End, and Smoke Testing

## Four Questions

These test families are best distinguished by the question each answers:

| Type | Main question |
|------|---------------|
| API test | Does the interface respond correctly? |
| Contract test | Do consumer and provider expectations agree? |
| End-to-end test | Does the full user or system flow work? |
| Smoke test | Is the deployed system basically operational? |

## API Testing

An **API test** sends requests to a service's interface and validates responses: **status codes**, **headers** (content type, caching, security headers), body content and **schema**, and **authentication** behavior (valid credentials succeed, missing ones get 401, wrong permissions get 403). REST APIs dominate the examples, but GraphQL (query/response shape) and gRPC (typed procedure calls) get the same treatment with different tooling. **Request validation** deserves its own tests: what does the API do with malformed input?

```python
def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Whether this is an "API test" or an "integration test" depends entirely on what `client` is wired to: an in-process test client over a fake store makes it a fast API/component test; the same assertions against a deployed service with a real database make it an integration or smoke test. The label follows the setup, not the syntax.

Note the assertion checks the *body*, not just the status code — a 200 with `{"status": "error"}` should fail. Status-only assertions are the weakest useful check.

## Contract Testing

When a consumer (frontend, other service) and a provider (API) evolve independently, **contract tests** verify their expectations agree without a full joint environment. In **consumer-driven contract testing**, each consumer records the requests it makes and the responses it relies on (the contract); **provider verification** then replays those contracts against the provider in *its* CI. A contract suite without provider verification is half a mechanism — the consumer's beliefs are documented but never checked. Contracts also make **backward compatibility** concrete: a provider change that breaks a recorded contract is a breaking change, no archaeology required. No contract tests exist in this repository; the concept matters most once multiple services and teams are involved.

## End-to-End Testing

An **end-to-end (E2E) test** exercises a full **user journey** through the assembled system — often via **browser automation** (Playwright, Selenium) for web UIs, or full request flows for APIs. E2E tests have the widest **system boundaries** and therefore the most infrastructure, the slowest runtimes, and the most flakiness; they belong on a few critical journeys (sign up, pay, core workflow), running in a dedicated **test environment** with controlled **test data** and **cleanup**. Everything smaller should have been caught below this level.

## Smoke and Friends

A **smoke test** answers "is it basically alive?" after a deployment: the service responds, the health endpoint reports OK, the fundamental dependency (database) is reachable. **Post-deployment verification** should be **production-safe**: read-only checks or dedicated probe endpoints — never test logic that modifies real user data. Related labels: a **sanity test** is a quick "does the specific thing I just changed work" check; **regression tests** keep fixed bugs fixed; **acceptance tests** tie to agreed requirements. All need **timeouts** (a hanging check is worse than a failing one) and **failure evidence** — logs, response bodies, screenshots for browser tests — or CI-only failures become unsolvable.

## Common Mistakes

- End-to-end tests for every small rule that a unit test could cover.
- Contract tests without provider verification.
- Smoke tests that modify production data.
- Weak assertions that check only the status code.
- Hard-coded shared accounts coupling tests and leaking access.
- Tests depending on execution order.
- Running destructive tests against the wrong environment.
- No screenshots, logs, or request evidence on failure.

## Existing Repository Evidence

- All three projects have real **API-style health tests**: [TaskOps test_health.py](../../../Projects/1_project/taskops-cicd/tests/test_health.py) asserts status, JSON body, *and* content type — and tests the failure path (503 with `{"status": "error", "database": "down"}`); [Project 3 test_app.py](../../../Projects/3_project/app/tests/test_app.py) covers `/health`, `/ready`, and `/version`; [KubeOps test_health.py](../../../Projects/2_project/kubeops-gitops/tests/) does the same for FastAPI.
- Two real **smoke tests** exist: the container health poll in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) (pre-release smoke check against the just-built image) and the post-deploy check in [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml), which runs `scripts/smoke_test.sh` against the live server's `/health` — a read-only, production-safe verification.
- Browser E2E tests and contract tests are not currently demonstrated; both remain conceptual and could arrive with a multi-service enhancement later.

## Practical Exercise

Classify the repository's health-check behavior. For each of: (1) TaskOps' in-suite health tests, (2) the TaskOps CI container poll, (3) the TaskOps CD post-deploy smoke test, record — what sends the request, what receives it, what is real versus test-scoped, what exactly is asserted, and which of the four families it belongs to. Then answer: which of the three would catch a broken database credential in production, and why do the other two miss it? Do not modify anything. Target 20–30 minutes.

## Knowledge Check

1. Why can the same test code be an API test in one setup and an integration test in another?
2. What makes a contract test different from an API test?
3. Why is provider verification essential to contract testing?
4. What makes a smoke check production-safe?
5. Why should E2E tests cover few journeys?
6. What does asserting only the status code miss?

<details>
<summary>View answers</summary>

1. The label follows the setup: an in-process client over fakes is a fast API/component test; the same assertions against a deployed real stack are integration or smoke testing.
2. An API test checks the provider against the tester's expectations; a contract test checks that consumer and provider *agree*, using recorded consumer expectations.
3. Without it, contracts document the consumer's beliefs but never validate the provider — agreement is assumed, not verified.
4. It is read-only or uses dedicated probe endpoints, and never creates, modifies, or deletes real user data.
5. They are the slowest, most infrastructure-heavy, most flaky tests; the pyramid reserves them for critical journeys that lower levels cannot verify.
6. A well-formed error: the service can return 200 with a failure body, so the check passes while the system is broken.

</details>

## Navigation

- [Back to Automated Testing and Quality](../README.md)
- [Previous: Integration Testing](../04-integration-testing/)
- [Next: Performance Testing](../06-performance-testing/)
- [Back to All Learning Materials](../../README.md)
