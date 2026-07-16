# Retries, Timeouts, Cancellation, and Failures

## Job Results

A finished job normally reports one of a small set of results:

- **Success:** every required step completed with exit code 0.
- **Failure:** a step returned a non-zero exit code, or the platform detected an error.
- **Skipped:** a condition or a failed dependency prevented the job from running.
- **Cancelled:** the run was stopped by a person, a concurrency rule, or fail-fast behavior.
- **Timed out:** the job exceeded its time limit and was stopped; platforms usually report this as a failure.
- **Neutral / allowed failure:** the work failed but was configured not to affect the overall result.

Commands signal outcome through **exit codes**: 0 means success, anything else means failure. A step that fails normally fails its job, and a failed job propagates downstream — dependent jobs are skipped, and the run is marked failed. Understanding this propagation is essential: a skipped job is *not* a successful job, and cleanup logic must account for cancellation as well as failure. Diagnosis relies on **logs** (standard output and error output per step) and on artifacts such as test reports; preserve them, because a deleted log turns a five-minute diagnosis into guesswork.

## Failure Classes

Not all failures deserve the same response:

| Failure type | Example | Retry appropriate? |
|--------------|---------|--------------------|
| Deterministic code failure | Unit test assertion fails | Usually no |
| Transient network failure | Temporary registry timeout | Sometimes |
| Flaky test | Test fails unpredictably | Retry may hide the problem |
| Resource exhaustion | Runner runs out of disk | Fix infrastructure first |
| Invalid configuration | Incorrect YAML or missing variable | No |

A **deterministic failure** produces the same result every run from the same inputs — rerunning it wastes time and delays the real fix. A **transient failure** is caused by a temporary external condition and may genuinely succeed on retry. A **flaky test** fails unpredictably without code changes; it is a defect in the test or its environment, not bad luck. Distinguishing code failures from infrastructure failures is the first step of every pipeline diagnosis.

## Retry Is Not a Fix

- Retries may help with transient external failures such as a registry timeout.
- Retries should not replace root-cause investigation; an automatically retried failure is still a failure that happened.
- Automatically retrying tests hides instability — the flaky test stays flaky and eventually fails when it matters.
- Deployment retries must be safe and **idempotent**: running the same deployment twice must produce the same end state, not a duplicated or half-applied change.
- A partially completed deployment may require rollback or reconciliation, not a blind rerun.

Manual retries (rerunning a failed job from the UI) are common and reasonable for suspected transient causes. Automatic retries need a **retry limit** and ideally **backoff** (increasing delay between attempts) so a broken dependency is not hammered. GitHub Actions has no built-in job-level automatic retry; retries there are manual reruns, action inputs, or scripted loops. GitLab CI/CD offers a `retry` keyword with failure-reason filters, and Jenkins offers `retry` blocks — same concept, platform-specific syntax.

## Timeouts

A job that hangs — a stuck network call, a test waiting for input, a deadlock — will otherwise occupy a runner until the platform's default limit, which can be hours. Explicit timeouts turn a hang into a fast, visible failure:

```yaml
jobs:
  integration-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - name: Run integration tests
        run: echo "Run tests with a job timeout"
```

Choose a limit modestly above the honest worst case. GitHub Actions also supports `timeout-minutes` on individual steps, which is useful when one step (such as an external scan) is the likely hang point.

## Allowed Failures

`continue-on-error` lets a step or job fail without failing the run:

```yaml
jobs:
  experimental-check:
    runs-on: ubuntu-latest
    continue-on-error: true

    steps:
      - run: echo "Run a non-blocking experimental check"
```

This is legitimate for genuinely experimental checks — a new tool being evaluated, a test suite against an unreleased runtime version. It must not be used to silence important failures: an "allowed failure" that everyone ignores is a hidden failure, and hidden failures accumulate until they surface in production. If a check matters, let it fail the run; if it does not matter, question why it runs at all.

## Cancellation and Concurrency

**Concurrency groups** limit how many runs of the same logical pipeline execute at once. Two policies dominate:

Cancel outdated work — when a newer commit lands on the same pull request, the older validation run is obsolete:

```yaml
concurrency:
  group: pull-request-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

Serialize critical work — a production deployment must never be killed halfway through, and two deployments must never interleave:

```yaml
concurrency:
  group: production-deployment
  cancel-in-progress: false
```

With `cancel-in-progress: false`, a new run queues until the current one finishes — a **deployment lock**. Cancelling a deployment mid-run can leave a half-updated system (image pushed but service not restarted, one host updated of three), so production pipelines serialize instead of cancel. Cancellation also interacts with cleanup: steps guarded by `if: always()` run even after failure or cancellation (see [Conditions and Filters](../04-conditions-and-filters/)), which is how temporary containers and resources get released. Design cleanup deliberately; a cancelled run that skips cleanup leaks resources.

Most platforms also support **partial reruns** — rerunning only failed jobs — which saves time but assumes upstream results are still valid for the same commit.

## Notifications and Visibility

Failure handling ends with a person finding out. Notifications should be few and meaningful: a failed default-branch build or failed deployment deserves an alert; every flaky-test rerun does not. Teams that alert on everything soon read nothing. Scheduled workflows are especially prone to **silent failures** — nobody is watching a nightly run unless a notification or dashboard makes its result visible.

## Existing Workflow Evidence

- [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) uses a concurrency group of `${{ github.workflow }}-${{ github.ref }}` with `cancel-in-progress: true`, cancelling superseded runs of the same branch or pull request. Its `docker` job also shows in-step retry of a transient condition — the health check polls up to 10 times while the container starts — and cleanup with `if: always()` to remove the container even after failure.
- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) uses a workflow-wide concurrency group with `cancel-in-progress: false`, serializing deployments exactly as described above. Its SSH deploy script uses `set -e` to fail fast on any error.
- The repository workflows do not currently set `timeout-minutes`, use `continue-on-error`, or configure automatic retries. These are shown conceptually above and may be added during a later practical enhancement; do not modify the workflows now.

## Common Mistakes

- No timeout on jobs that can hang.
- Infinite or excessive automatic retries.
- Retrying deterministic failures instead of fixing them.
- Ignoring failed cleanup steps.
- Hiding failures with `continue-on-error`.
- Cancelling production deployments carelessly.
- Allowing multiple production deployments to run simultaneously.
- Failing to preserve logs and reports needed for diagnosis.
- Sending so many low-value notifications that real failures are missed.
- Treating an infrastructure failure as a code failure, or the reverse.

## Practical Exercise

Classify each scenario with one response: **retry**, **do not retry**, **investigate first**, **cancel outdated run**, or **serialize execution**.

1. `pip install` fails with a registry connection timeout; the registry status page reports a brief incident.
2. A unit test asserting `2 + 2 == 5` fails.
3. An integration test passes locally and fails in about one of every five CI runs.
4. A developer pushes a second commit to a pull request while the first commit's CI run is still executing.
5. Two merges to `main` arrive three minutes apart, and each triggers the production deployment workflow.

Write one sentence of justification per answer, then check your reasoning against the failure-classification table. Target 15–25 minutes.

<details>
<summary>Suggested classifications</summary>

1. Retry — a confirmed transient external failure.
2. Do not retry — deterministic; fix the code or the test.
3. Investigate first — a flaky test; retrying hides the instability.
4. Cancel outdated run — the older validation is obsolete.
5. Serialize execution — queue the second deployment; never run or cancel production deployments mid-flight.

</details>

## Knowledge Check

1. Why is retrying a deterministic test failure usually inappropriate?
2. What protection does a job timeout provide?
3. Why might production deployments use a concurrency lock instead of cancellation?
4. What risk comes from using `continue-on-error` broadly?
5. What must be true of a deployment before automatic retry is safe?
6. Is a skipped job the same as a successful job?

<details>
<summary>View answers</summary>

1. The same inputs produce the same failure, so the retry wastes time and delays the real fix.
2. It converts a hanging job into a fast, visible failure instead of occupying a runner for hours.
3. Cancelling mid-deployment can leave the system half-updated; queueing serializes changes safely.
4. Failures become invisible and accumulate, because the run stays green while a check fails.
5. It must be idempotent — running it again produces the same end state without duplication or partial application.
6. No — skipped means the job never ran; dependent logic must not treat it as verified success.

</details>

## Navigation

- [Back to Pipeline Architecture](../README.md)
- [Previous: Manual Approvals and Quality Gates](../06-manual-approvals-and-quality-gates/)
- [Back to All Learning Materials](../../README.md)
