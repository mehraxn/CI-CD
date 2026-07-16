# Job Dependencies and DAG Pipelines

## Dependencies and Graphs

A job dependency states that one job requires another job's completion or result. The required job is **upstream**; the waiting job is **downstream**. Independent jobs have no ordering relationship and may run in parallel.

A Directed Acyclic Graph (DAG) models these relationships:

- **Directed** means each edge points from a prerequisite toward dependent work.
- **Acyclic** means following edges can never return to the starting job.
- A cycle is invalid because every job in the loop would wait forever for another.

```text
                  +-- Unit tests --------+
Build application +-- Integration tests -+-- Package
                  +-- Security scan -----+
```

The build **fans out** into three verification jobs. Their results **fan in** at `Package`. The verification jobs can run concurrently after the build. Package waits for every required upstream job.

## GitHub Actions `needs` Example

```yaml
name: DAG Example

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build application"

  unit-tests:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Run unit tests"

  integration-tests:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Run integration tests"

  security-scan:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Run security scan"

  package:
    needs:
      - unit-tests
      - integration-tests
      - security-scan
    runs-on: ubuntu-latest
    steps:
      - run: echo "Create release package"
```

The three checks all depend only on `build`, so the scheduler can start them together when capacity exists. `package` lists all three and waits. By default, a failed required upstream job prevents downstream execution. Conditions can deliberately change status behavior, but a downstream job must not assume missing outputs exist.

## Results, Outputs, and Artifacts

Dependencies can expose upstream status and declared outputs. Small metadata such as a computed version can pass as a job output. A built package should pass through explicit artifact storage rather than an assumed shared filesystem. A downstream job must download the exact artifact and preserve source identity.

A skipped upstream job complicates fan-in. Depending on platform rules and conditions, downstream work may skip even if its own logical condition appears true. Designs should state whether optional checks are dependencies, allowed failures, or separate observations.

Partial failure means some graph branches succeed while others fail. Successful logs and artifacts may still help diagnosis, but publishing or deployment should require the full intended gate set.

## Critical Path

The critical path is the longest required dependency chain. It determines the minimum possible pipeline time before queue and startup overhead.

```text
Build: 3 minutes
Unit tests: 2 minutes
Integration tests: 8 minutes
Security scan: 4 minutes
Package: 2 minutes
```

The approximate critical path is:

```text
Build -> Integration tests -> Package
3 + 8 + 2 = 13 minutes
```

Making unit tests faster would not reduce the 13-minute minimum while integration tests remain the longest fan-out branch. Reducing integration time or moving safe work off that chain can help. Runner queues may make observed duration longer.

## Avoiding False Dependencies

If lint and unit tests both need only checked-out source, making unit tests depend on lint adds waiting without a data requirement. Both can start together and gate packaging. Add a dependency for a real reason: required output, ordered environment change, resource sequencing, or policy.

Conversely, hiding a deployment dependency is dangerous. Deployment should explicitly require the intended evidence and artifact rather than rely on file order or job names.

## Larger Pipeline Relationships

Parent/child pipelines split one logical system into separately defined executions. Downstream pipelines can deliver another component or environment after upstream success. Workflow chaining connects completed automation to later automation. These patterns need explicit source version, permissions, inputs, results, and failure ownership; a green upstream does not automatically make every downstream action safe.

## Existing Workflow Evidence

[TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) declares `docker` with `needs: quality`. It forms a simple sequential DAG: quality must succeed before image build, scan, and smoke test. [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) similarly makes `deploy` depend on `verify`.

KubeOps workflows currently contain one job each, so they do not demonstrate cross-job DAG edges. None of the four workflows demonstrates parent/child pipelines, workflow chaining, job outputs, or workflow artifact transfer.

## Common Mistakes

- Making every job depend on the previous job.
- Creating a dependency cycle.
- Depending on every earlier job without a data or policy reason.
- Forgetting to transfer required outputs or artifacts.
- Assuming downstream jobs run after failed dependencies.
- Treating skipped and successful results as identical.
- Hiding deployment prerequisites.
- Creating a graph too complicated to diagnose.

## Practical Exercise

Draw the TaskOps CI and CD dependency graphs. Then propose, on paper, a fan-out of lint, test, and scan jobs followed by one fan-in gate. Identify the critical path using assumed durations. Do not edit a workflow.

## Knowledge Check

1. Why must a DAG be acyclic?
2. What are fan-out and fan-in?
3. Why does `package` wait in the example?
4. What normally happens after a required upstream job fails?
5. Why can unnecessary dependencies increase duration?

<details>
<summary>View answers</summary>

1. A cycle would leave jobs waiting on one another with no valid start order.
2. Fan-out starts multiple branches from one prerequisite; fan-in joins required branches at one dependent job.
3. It explicitly needs all three verification jobs.
4. The downstream job is skipped unless status conditions deliberately change behavior.
5. They serialize work that could otherwise run concurrently and lengthen the critical path.

</details>

## Navigation

- [Back to Pipeline Architecture](../README.md)
- [Previous: Stages, Jobs, Steps, and Tasks](../02-stages-jobs-steps-and-tasks/)
- [Next: Conditions and Filters](../04-conditions-and-filters/)
- [Back to All Learning Materials](../../README.md)
