# Unit Testing

## The Base of the Pyramid

A **unit test** verifies one small piece of logic — the **unit under test** — in **isolation** from databases, networks, filesystems, and other components. Isolation is what buys the three properties unit tests are prized for: they are **fast** (milliseconds), **deterministic** (same result every run), and **precise** (a failure points at one unit, not "somewhere in the system").

## Anatomy of a Unit Test

The near-universal structure is **Arrange, Act, Assert** (the behavior-driven phrasing **Given, When, Then** is the same idea):

```python
def calculate_total(price: float, quantity: int) -> float:
    if quantity < 0:
        raise ValueError("quantity cannot be negative")
    return price * quantity
```

```python
import pytest

def test_calculate_total_multiplies_price_and_quantity():
    assert calculate_total(4.0, 3) == 12.0

def test_calculate_total_rejects_negative_quantity():
    with pytest.raises(ValueError):
        calculate_total(4.0, -1)
```

The first test arranges inputs (`4.0, 3`), acts (calls the function), and asserts on the result — the happy path. The second covers an **error case**: the contract says negative quantity is rejected, so a test proves it. Note the **test naming**: each name states the behavior being verified, so a failure report reads as a specification ("calculate_total rejects negative quantity — FAILED"). Good suites also probe **boundary cases** (zero, exactly-at-limit values) — bugs live at edges.

**Pure functions** (output depends only on input, no **side effects**) are the easiest units to test, which is a design signal: code that is hard to unit-test is usually telling you its responsibilities are tangled.

## Fixtures, Parameterization, and Doubles

- **Fixtures** provide reusable setup and teardown — pytest injects them by argument name (this repository's `conftest.py` files define `app` and `client` fixtures this way). Setup/teardown symmetry keeps **test independence**: each test starts clean, so tests pass in any **order**.
- **Parameterized tests** run one test body over many input/expected pairs, covering a table of cases without copy-paste.
- **Test doubles** replace real dependencies: a **stub** returns canned answers; a **mock** additionally records and asserts on how it was called; a **fake** is a working lightweight implementation (an in-memory store standing in for a database); a **spy** wraps the real thing while recording calls. Doubles keep units isolated — but **over-mocking** is the classic failure: a test that mocks everything asserts only that the code calls what the mocks expected, i.e. it tests the implementation, not the behavior. When a refactor that preserves behavior breaks the test, the test was testing **implementation details**.

**Assertions** should check outcomes precisely, and produce useful **failure messages** — `assert result == expected` in pytest shows both values; asserting merely `assert result` proves almost nothing (a weak assertion).

## Unit Tests in CI

Because they are fast and hermetic, unit tests run on **every change**, first among the test levels. They need no services, no network, no special environment — which is also the rule for writing them: a unit test that opens a network connection or a real shared database has quietly become an integration test with all the associated slowness and flakiness, in the stage that was supposed to be instant.

## Common Mistakes

- Testing private implementation details instead of observable behavior.
- One test checking many unrelated behaviors — failures become riddles.
- Shared state between tests, creating order dependencies.
- Network access in unit tests.
- Real (shared) database access in unit tests.
- Excessive mocking that pins the implementation.
- Weak assertions that pass for wrong results.
- Tests without meaningful names.
- Assuming coverage equals quality.

## Existing Repository Evidence

The repository's suites are honest about their level: most tests exercise HTTP routes with real (if throwaway) infrastructure, making them component/integration tests rather than pure unit tests — see the classification exercise in [Testing Strategy](../01-testing-strategy-and-test-pyramid/). The closest to unit style:

- [KubeOps `test_validation.py`](../../../Projects/2_project/kubeops-gitops/tests/) exercises input-validation behavior against an in-memory store — no I/O, reset per test by an autouse fixture in [conftest.py](../../../Projects/2_project/kubeops-gitops/tests/conftest.py): fast and deterministic in the unit spirit.
- [TaskOps `test_health.py`](../../../Projects/1_project/taskops-cicd/tests/test_health.py) shows a textbook use of a test double: `monkeypatch.setattr(database, "ping_db", _boom)` replaces the real database ping with a stub that raises, so the failure path of `/health` can be tested without breaking a real database.
- pytest itself is configured in each project's `pyproject.toml` (`testpaths = ["tests"]`) and pinned in TaskOps' `requirements-dev.txt`.

Parameterized tests and dedicated pure-function unit suites are not currently demonstrated; the concepts above remain the target vocabulary.

## Practical Exercise

Dissect two real tests — `test_health_reports_unhealthy_when_db_fails` in [TaskOps test_health.py](../../../Projects/1_project/taskops-cicd/tests/test_health.py) and any test in KubeOps `test_validation.py`. For each, identify:

- Unit under test
- Setup (which fixtures, what they provide)
- Action
- Assertion(s)
- External dependencies (real, faked, or replaced — name the mechanism)
- Whether the test is truly isolated, and from what

Conclude with one sentence per test: unit, component, or integration — and why. Do not modify any test. Target 20–30 minutes.

## Knowledge Check

1. What three properties does isolation buy a unit test?
2. Name the three phases of a well-structured test.
3. What is the difference between a stub and a mock?
4. Why is over-mocking harmful?
5. Why do meaningful test names matter in CI?
6. What test double does TaskOps' health-failure test use, and via what mechanism?

<details>
<summary>View answers</summary>

1. Speed, determinism, and precise failure localization.
2. Arrange (set up inputs), Act (invoke the unit), Assert (check the outcome) — equivalently Given/When/Then.
3. A stub only returns canned answers; a mock also records calls and asserts on how it was used.
4. The test pins the implementation rather than the behavior, so behavior-preserving refactors break tests and real regressions can slip past canned expectations.
5. The failure list becomes a readable specification of what broke, before anyone opens a log or a file.
6. A stub that raises, installed with pytest's `monkeypatch.setattr` over the real `ping_db` function.

</details>

## Navigation

- [Back to Automated Testing and Quality](../README.md)
- [Previous: Formatting, Linting, and Static Analysis](../02-formatting-linting-and-static-analysis/)
- [Next: Integration Testing](../04-integration-testing/)
- [Back to All Learning Materials](../../README.md)
