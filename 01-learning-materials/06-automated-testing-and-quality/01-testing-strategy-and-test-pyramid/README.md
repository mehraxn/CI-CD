# Testing Strategy and Test Pyramid

## Strategy Before Tools

A **testing strategy** decides which kinds of tests exist, what each is responsible for, where each runs in the pipeline, and who owns them. Without a strategy, suites grow by accretion — whatever the last incident inspired — and drift toward slow, overlapping, unowned tests.

The classic shape is the **test pyramid**:

```text
             Few
       End-to-end tests
      Integration tests
         Unit tests
             Many
```

Many fast, isolated **unit tests** at the base; fewer **integration tests** verifying components together; few **end-to-end tests** exercising whole user flows. The reasoning is economics: as tests get broader they get slower, flakier, and more expensive to maintain, so broad tests should be reserved for what narrow tests cannot see. The pyramid is **guidance, not a rigid numeric rule** — a thin API service may legitimately have more integration than unit tests (the "test trophy" shape argues exactly that for some stacks). What matters is that each level exists for a reason and the fast levels carry most of the volume.

## The Level Vocabulary

- **Unit tests** — one small logic unit in isolation.
- **Component tests** — one component behind its interface, dependencies replaced.
- **Integration tests** — real interaction between components (code + database, service + queue).
- **Contract tests** — do consumer and provider agree on the interface?
- **API tests** — does the service's interface respond correctly?
- **End-to-end tests** — a full user or system journey through the deployed stack.
- **Smoke tests** — is the system basically operational after a deployment?
- **Regression tests** — any test written to keep a fixed bug fixed.
- **Acceptance tests** — does the software meet agreed requirements?
- **Functional vs. non-functional** — what the system does versus how well (performance, security, usability).

| Test type | Main focus | Speed | Isolation | Typical CI position |
|-----------|------------|-------|-----------|---------------------|
| Unit | Small logic unit | Fast | High | Every change |
| Integration | Components working together | Medium | Medium | Pull request or main |
| End-to-end | Full user flow | Slow | Low | Selected flows |
| Smoke | Basic deployment health | Fast or medium | Low | After deployment |

## Strategy Forces

Every strategy balances the same forces:

- **Fast feedback vs. confidence** — unit tests answer in seconds but prove little about the whole; end-to-end tests prove a lot and answer in minutes. **Shift-left** pushes checks earlier (cheaper to fix); **shift-right** accepts that some verification (smoke tests, monitoring) can only happen after deployment.
- **Cost and maintenance** — every test is code to maintain. Broad tests break for unrelated reasons and consume debugging time.
- **Risk-based selection** — test hardest where failure hurts most. A payment path deserves more layers than an admin color picker.
- **Test environment and data** — each level needs an environment it can trust and **test data** it controls; **deterministic tests** require deterministic data.
- **Ownership** — every suite needs someone who fixes it when it breaks; unowned tests get skipped, then deleted.
- **Test selection** — CI need not run everything on every change: fast levels on every push, broader suites on pull requests or `main`, the fullest set before production.

## Common Mistakes

- Only end-to-end tests — slow feedback, flaky suite, hour-long diagnoses.
- Too many implementation-specific unit tests that break on every refactor.
- Slow tests placed in the fastest feedback stage.
- Unclear ownership, so failures rot.
- Shared mutable test data coupling tests to each other.
- Test environments so different from production that green means little.
- Treating the pyramid as a mandatory percentage formula.
- Ignoring business risk when choosing what to test.

## Existing Repository Evidence

All three projects test at the *service boundary with controlled dependencies* — a pragmatic middle of the pyramid:

- [TaskOps tests](../../../Projects/1_project/taskops-cicd/tests/) exercise HTTP routes through Flask's test client against a **real but throwaway SQLite database** created per test (see `conftest.py`) — integration-style tests that stay fast and isolated. `test_security.py` is risk-based testing in action: CSRF enforcement gets its own file.
- [KubeOps tests](../../../Projects/2_project/kubeops-gitops/tests/) use FastAPI's `TestClient` against an **in-memory store reset around every test** — closer to component/API tests, with isolation handled by an autouse fixture.
- [Project 3 tests](../../../Projects/3_project/app/tests/test_app.py) check the operational endpoints (`/health`, `/ready`, `/version`) — small API tests.
- The container **smoke test** in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) polls `/health` on the freshly built image — a real post-build smoke check.
- The repository does not currently demonstrate browser end-to-end tests, contract tests, or performance tests.

## Practical Exercise

Classify the existing tests by level. For each test file in TaskOps, KubeOps, and Project 3, record: file name, what it exercises, which dependencies are real versus replaced, and the level you assign (unit / component / integration / API / smoke). Where a file resists a single label (many will), write one sentence explaining why — that ambiguity is a legitimate finding, not an error. Do not rename or rewrite any test. Target 25–35 minutes.

## Knowledge Check

1. Why does the pyramid put many tests at the bottom and few at the top?
2. Is the pyramid a mandatory ratio? What is it actually for?
3. What distinguishes a regression test from other tests?
4. What do shift-left and shift-right mean for testing?
5. Why is test ownership part of a strategy?
6. Where do the TaskOps tests sit on the pyramid, and what makes them fast despite using a real database?

<details>
<summary>View answers</summary>

1. Broader tests are slower, flakier, and costlier to maintain, so volume belongs at the fast, isolated base and broad tests are reserved for what narrow ones cannot see.
2. No — it is guidance about economics, not a percentage formula; some architectures legitimately weight integration tests more heavily.
3. Its purpose: it exists to keep a previously fixed bug fixed; it can live at any level.
4. Shift-left moves checks earlier in delivery where fixes are cheap; shift-right accepts some verification happens after deployment, via smoke tests and monitoring.
5. Unowned failing tests get ignored, skipped, and deleted; ownership is what keeps a suite trustworthy over time.
6. Integration-style tests at the HTTP boundary; they stay fast because the database is a throwaway per-test SQLite file, not a shared server.

</details>

## Navigation

- [Back to Automated Testing and Quality](../README.md)
- [Next: Formatting, Linting, and Static Analysis](../02-formatting-linting-and-static-analysis/)
- [Back to All Learning Materials](../../README.md)
