# Stages, Jobs, Steps, and Tasks

## From Logical Design to Execution

A pipeline or workflow defines automated work. A **stage** is usually a logical phase such as build, test, or deploy. A **job** is an executable unit assigned to a runner or agent. A **step** is ordered work inside a job. **Task**, **script**, and **command** may be generic terms or formal platform objects.

```text
Pipeline
|-- Build stage
|   `-- Build job
|       |-- Check out source
|       |-- Install dependencies
|       `-- Build application
|
|-- Test stage
|   |-- Unit-test job
|   `-- Integration-test job
|
`-- Deploy stage
    `-- Deploy job
```

GitHub Actions emphasizes workflows, jobs, and steps rather than an explicit stage object. GitLab CI/CD commonly groups jobs into stages. Jenkins pipelines often use stages and steps running on agents or nodes. An **executor** is the mechanism or environment that runs work, such as a shell, container, or virtual machine. Exact meanings remain platform-specific.

## Job Lifecycle

A typical job passes through:

1. **Scheduling:** The platform finds a runner matching labels and permissions.
2. **Setup:** The runner prepares a workspace and job environment.
3. **Source checkout:** A step obtains the required repository revision; this is not always automatic.
4. **Dependency installation:** Tools or packages are restored, installed, or built.
5. **Command execution:** Steps run scripts, actions, tests, builds, or deployments.
6. **Result collection:** Exit codes, logs, reports, and outputs determine job status.
7. **Cleanup:** Temporary processes and resources are stopped or removed.

Cleanup may need an explicit status condition. Cancellation can interrupt ordinary steps, so externally created resources need deliberate reconciliation or cleanup outside the runner as well.

## Steps, Processes, and Results

Steps in one job usually execute sequentially. A command returning exit code `0` conventionally indicates success; a nonzero exit code normally fails its step and job unless handling changes that behavior. Standard output and standard error become job logs. Clear step names and focused commands make a failure easier to locate.

Steps share the job workspace, but they may execute in separate processes. An environment variable set only inside one shell process may not persist to the next step. Platforms provide explicit environment files, job outputs, or configuration fields for durable value transfer. Secret values still require masking and minimal exposure.

Shell behavior matters. Bash, PowerShell, and command shells differ in quoting, variables, pipelines, path syntax, and failure semantics. A command that works on Ubuntu may not work unchanged on Windows.

## Job Isolation and Data Sharing

Separate jobs commonly run on different machines or containers. A file created in one job is not automatically available in another. Even two jobs with the same `runs-on` label may receive different temporary runners.

```yaml
name: Build and Test

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Check out source
        uses: actions/checkout@v4

      - name: Build
        run: |
          mkdir -p dist
          echo "application package" > dist/app.txt

  test:
    runs-on: ubuntu-latest

    steps:
      - name: Run tests
        run: echo "Testing on a separate runner"
```

The jobs have no dependency and can run in parallel. `test` does not automatically receive `dist/app.txt`: the build file exists only in the `build` workspace. Explicit artifact upload/download is one solution when the file is a durable output. A cache can reuse replaceable data such as dependencies. See [Artifacts, Packages, and Registries](../../07-artifacts-packages-and-registries/) for the later dedicated topic.

Metadata can move through declared job outputs. Large files should not be encoded into variables. Each platform has limits and mechanisms for outputs, artifacts, caches, and shared storage.

## Services and Working Directories

Integration jobs may start service containers for databases or queues. Those services belong to the job environment unless an external service is used. Parallel jobs should not assume the same service instance or port namespace.

A step's working directory controls relative paths. Repository layouts often require `working-directory` or an explicit `cd`, but hidden directory changes make examples confusing. Prefer a consistent workspace and visible configuration.

## Sequential and Parallel Work

Steps within one job are sequential because later steps often use files or setup from earlier ones. Jobs without dependencies may run concurrently. Jobs with declared dependencies wait and usually skip when a required upstream job fails.

One enormous job guarantees local state sharing but hides architecture and prevents useful parallelism. Dozens of trivial jobs increase scheduling delay and explicit transfer work. Boundaries should follow responsibility, execution requirements, credentials, and evidence.

## Designing Good Jobs

- Give each job a clear responsibility such as quality, build, or deploy.
- Avoid one enormous job containing the entire pipeline.
- Avoid fragmenting every command into a separate job.
- Use meaningful job and step names.
- Keep logs concise enough to locate failure.
- Make setup repeatable on a clean runner.
- Declare dependencies and data transfer explicitly.
- Minimize credentials per job.
- Ensure cleanup covers failure and cancellation.
- Avoid reliance on undocumented runner state.

## Existing Workflow Evidence

[TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) has `quality` and `docker` jobs. Each checks out source independently because their workspaces are isolated. Steps within `quality` install dependencies before running Ruff, Black, isort, pytest, Bandit, and pip-audit.

[KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) uses one job for source checks, tests, image build, and scanning. Compare its simple local state sharing with TaskOps job separation. The existing workflows do not transfer workflow artifacts between jobs.

## Practical Exercise

In 20-25 minutes, map one real workflow as `Workflow -> Job -> Step`. Mark setup, checkout, dependency installation, commands, cleanup, runner, and result. Identify one file that exists only in the job workspace. Do not modify the workflow.

## Knowledge Check

1. Why is a stage not necessarily an executable machine unit?
2. Why does a second job not automatically receive files from the first?
3. How do steps and jobs usually differ in ordering?
4. Why may an environment variable disappear between steps?
5. What is the architectural problem with one enormous job?

<details>
<summary>View answers</summary>

1. A stage is often a logical grouping, while jobs are scheduled onto runners.
2. Jobs commonly have isolated workspaces on separate temporary runners.
3. Steps in a job usually run sequentially; independent jobs may run in parallel.
4. Steps may use separate processes, so process-local state does not persist automatically.
5. It hides responsibilities, reduces parallelism, broadens credentials, and makes failures harder to locate.

</details>

## Navigation

- [Back to Pipeline Architecture](../README.md)
- [Previous: Triggers and Events](../01-triggers-and-events/)
- [Next: Job Dependencies and DAG Pipelines](../03-job-dependencies-and-dag-pipelines/)
- [Back to All Learning Materials](../../README.md)
