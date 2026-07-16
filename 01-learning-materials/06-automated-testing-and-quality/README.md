# Automated Testing and Quality

## Overview

Automated checks are what let a pipeline say "this change is safe to progress" without a human re-reading every line. This section covers the strategy layer (which tests to write and where), the fast source-level checks (formatting, linting, static analysis), the functional test levels (unit, integration, API, contract, end-to-end, smoke), performance testing, the reporting-and-gating layer (coverage, reports, quality gates), and the operational reality of keeping suites fast and trustworthy (parallelism, sharding, flaky tests).

## Why Testing Is Central to CI/CD

Continuous integration is only useful if integration is *verified* — merging often, unverified, just distributes breakage faster. Automated tests are the verification, and their speed sets the pipeline's feedback speed. A typical verification ladder:

```text
Code change
    ↓
Formatting check
    ↓
Linting and static analysis
    ↓
Unit tests
    ↓
Integration tests
    ↓
API or end-to-end tests
    ↓
Security and quality gates
    ↓
Build accepted or rejected
```

Cheap, fast checks run first so most failures are caught in seconds; expensive checks run later on changes that already passed the basics. Security checks (in this repository: Bandit, pip-audit, Trivy) sit alongside functional checks as gates of the same shape — machine-evaluated pass/fail rules, as covered in [Manual Approvals and Quality Gates](../03-pipeline-architecture/06-manual-approvals-and-quality-gates/).

## Honest Limits

Each layer proves less than it appears to:

- Formatting does not prove correctness.
- Linting does not replace testing.
- Unit tests do not prove successful integration.
- End-to-end tests should not be the only test layer.
- A green pipeline does not prove the absence of defects — it proves the encoded checks passed.

The testing pyramid (lesson 01) exists to balance these limits: many fast isolated tests, fewer broader ones, each level covering what the level below cannot see.

## Lessons

| Number | Lesson | Main focus |
|---|---|---|
| 01 | [Testing Strategy and Test Pyramid](./01-testing-strategy-and-test-pyramid/) | Levels, trade-offs, and risk-based strategy |
| 02 | [Formatting, Linting, and Static Analysis](./02-formatting-linting-and-static-analysis/) | Fast checks without executing the application |
| 03 | [Unit Testing](./03-unit-testing/) | Small, fast, isolated verification |
| 04 | [Integration Testing](./04-integration-testing/) | Components working together, real dependencies |
| 05 | [API, Contract, End-to-End, and Smoke Testing](./05-api-contract-end-to-end-and-smoke-testing/) | Interface, agreement, journey, and health checks |
| 06 | [Performance Testing](./06-performance-testing/) | Load, stress, spike, soak, and baselines |
| 07 | [Coverage, Reports, and Quality Gates](./07-coverage-reports-and-quality-gates/) | Measuring, reporting, and gating responsibly |
| 08 | [Parallel Tests, Flaky Tests, and Optimization](./08-parallel-tests-flaky-tests-and-optimization/) | Keeping suites fast and trustworthy |

## Learning Objectives

After completing this section, the learner should be able to:

- design a layered testing strategy using the pyramid as guidance;
- distinguish formatters, linters, static analyzers, and type checkers;
- write and recognize good unit and integration tests;
- classify API, contract, end-to-end, and smoke tests by the question each answers;
- explain what coverage does and does not measure;
- design deliberate quality gates and thresholds; and
- diagnose flaky tests and optimize suites safely.

## Recommended Study Order

Follow the numbered order: strategy first, then the checks in roughly the order a pipeline runs them, then the measurement and operational lessons that apply across all levels.

## Practical Project Connections

- [TaskOps (Project 1)](../../Projects/1_project/taskops-cicd/) — the richest example: a real test suite ([tests/](../../Projects/1_project/taskops-cicd/tests/)) with fixtures, a throwaway SQLite database, and security tests, plus a [CI workflow](../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) chaining Ruff, Black, isort, pytest, Bandit, pip-audit, Trivy, and a container smoke test.
- [KubeOps (Project 2)](../../Projects/2_project/kubeops-gitops/) — a FastAPI test suite ([tests/](../../Projects/2_project/kubeops-gitops/tests/)) with an isolated in-memory store and the same static-check family in [CI](../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml).
- [Project 3](../../Projects/3_project/app/tests/) — a compact suite covering health, readiness, and version endpoints.

Coverage measurement, performance tests, matrices, and test reports are not currently demonstrated in the repository; the relevant lessons mark them as conceptual.

## Completion Checklist

- [ ] I classified the real tests in all three projects by level.
- [ ] I mapped every static check in TaskOps CI to its category and limits.
- [ ] I can identify fixture, action, and assertion in a real test.
- [ ] I know which real tests touch a database and how they stay isolated.
- [ ] I can explain what the container smoke test in TaskOps CI proves.
- [ ] I designed a coverage/gate proposal without implementing it.
- [ ] I completed all exercises and knowledge checks.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Builds, Dependencies, and Caching](../05-builds-dependencies-and-caching/)
- [Next: Artifacts, Packages, and Registries](../07-artifacts-packages-and-registries/)
