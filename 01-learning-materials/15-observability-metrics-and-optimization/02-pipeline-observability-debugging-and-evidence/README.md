# Pipeline Observability, Debugging, and Evidence

## What a Workflow Run Tells You

Every **workflow run** is a bundle of evidence: **status** at run, job, and step level; **durations** and **queue time**; the **trigger**, **commit SHA**, **branch/PR**, and **actor**; the **runner** and its image; per-step **exit codes**, stdout/stderr with **log grouping**; **annotations** (errors and warnings surfaced onto the summary and diff); any **artifacts** and reports; **attempt numbers** for retries and reruns; and cancellation/timeout records. CI/CD observability starts with knowing this evidence exists and reading it in the right order.

## The Debugging Order

```text
1. Identify the first meaningful failure.
2. Confirm trigger, commit, and inputs.
3. Inspect the failed job and step.
4. Check runner, environment, and permissions.
5. Read command output and exit code.
6. Compare with a successful run.
7. Reproduce safely where possible.
8. Preserve useful evidence.
```

Step 1 carries the key insight: **the last red step is often not the root cause** — a failed dependency install produces a cascade of downstream errors, and the loudest one is rarely the first one. Step 2 catches the embarrassing class ("this ran against the wrong branch"). Step 6 is the highest-value comparison: what changed between the last green run and this red one — code, workflow, action version, runner image, or external service?

Classify what you find:

| Failure type | Example |
|--------------|---------|
| Source failure | Test assertion fails |
| Configuration failure | Invalid workflow input |
| Dependency failure | Registry unavailable |
| Runner failure | Disk exhausted |
| Permission failure | Token lacks package access |
| Flaky failure | Timing-dependent test |
| Deployment failure | Health checks never pass |

The classification decides the response ([Topic 03's failure lesson](../../03-pipeline-architecture/07-retries-timeouts-cancellation-and-failures/)): source failures get fixes, dependency failures get retries, flaky failures get investigation — and **a rerun that passes does not prove a flaky failure is solved**; it proves it is flaky.

## Safe Debugging

- **Never print secrets** — masking is incomplete, and debug output (`env | sort`) is where leaks happen.
- Do not enable unrestricted **debug logging** permanently; it is verbose, slow, and leak-prone.
- Preserve logs and artifacts only as long as needed; **diagnostic bundles may contain sensitive data**.
- Record the exact **workflow attempt** you diagnosed — attempt 1 and attempt 2 are different executions with possibly different causes.
- Compare environment and tool versions before blaming code.

## Common Mistakes

- Reading the last error instead of the first.
- Rerunning until green and calling it fixed.
- No evidence preserved after failure — the crime scene cleaned before investigation.
- Debug output containing secrets.
- Diagnosing the wrong attempt.
- Never comparing against a successful run.
- Treating infrastructure failures as application failures (and vice versa).

## Existing Repository Evidence

- **Evidence by design**: [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml)'s smoke test is the repository's best diagnostic pattern — on failure it explicitly prints `docker logs taskops` before exiting 1, so the container's story survives; the `if: always()` cleanup step ensures the runner state is reported and released regardless of outcome.
- **Correlation built in**: every run is tied to its commit SHA, and the published image tag *is* the SHA ([CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml)), so a bad deployment traces to its run and source in one hop.
- **Attempt-relevant behavior**: TaskOps CI's `cancel-in-progress: true` means superseded runs are cancelled, not failed — a cancelled run in the history is expected noise, not a defect; CD's serialized queue means deployment runs may show long queue-time-to-start gaps by design.
- **Evidence gaps** (all noted in earlier topics, visible here as missing diagnosis material): no artifacts are uploaded anywhere — pytest results, Trivy reports, and coverage exist only as scrolled log text; there are no JUnit reports, no retained scan evidence, and no failure screenshots/bundles. A failed run older than the log-retention window leaves nothing.

## Practical Exercise

Annotate the diagnostic capabilities of [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), job by job:

```text
Job
Evidence
Logs
Artifacts
Reports
Timeout
Retry behavior
Failure classification
Missing evidence
```

Then run three thought experiments and classify each with the table: (a) `pip install` fails with a 503 from PyPI; (b) the Trivy step fails the morning after a new CVE publication, with no repository change; (c) the smoke test times out after 10 attempts. For each: first meaningful failure, classification, correct response, and what evidence you would want that the workflow currently does not preserve. Target 25–35 minutes.

## Knowledge Check

1. Why start from the first meaningful failure rather than the last error?
2. What does comparing against the last successful run reveal?
3. Why does a passing rerun not close a flaky-failure investigation?
4. What real failure-evidence pattern does TaskOps CI implement?
5. Why must diagnostic bundles be handled carefully?
6. What is this repository's largest pipeline-evidence gap?

<details>
<summary>View answers</summary>

1. Later errors are usually consequences of the first one; diagnosing a cascade's tail wastes time on symptoms.
2. The delta that matters: code, workflow, action versions, runner image, or external services — one of them changed, and the diff is the suspect list.
3. Passing on rerun is the definition of flakiness, not its resolution; the root cause (timing, state, environment) is still there.
4. Printing the container's logs (`docker logs`) on smoke-test failure before failing the step, plus guaranteed cleanup with `if: always()`.
5. They can contain environment variables, tokens, and internal details; preserving evidence and leaking secrets are one careless step apart.
6. Nothing is retained as artifacts — test results, scan reports, and coverage live only in job logs and vanish with retention.

</details>

## Navigation

- [Back to Observability, Metrics, and Optimization](../README.md)
- [Previous: Logs, Metrics, Traces, and Observability Fundamentals](../01-logs-metrics-traces-and-observability-fundamentals/)
- [Next: Deployment Monitoring, Alerting, SLIs, and SLOs](../03-deployment-monitoring-alerting-slis-and-slos/)
- [Back to All Learning Materials](../../README.md)
