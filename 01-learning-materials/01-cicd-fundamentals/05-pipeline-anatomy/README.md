# Pipeline Anatomy

## Pipeline Shapes and Platform Language

A **pipeline** is an automated sequence or dependency graph that processes a change. A **workflow** is often a platform's configured automation process. The words are sometimes interchangeable, but a platform may give them specific meanings. GitHub Actions emphasizes workflows, jobs, and steps. GitLab CI/CD commonly presents stages and jobs. Jenkins pipelines can use stage-oriented syntax. Always read a tool's model rather than forcing one vocabulary onto every system.

A **pipeline run** or workflow run is one execution of the definition for a particular trigger and source revision. The definition may stay the same while each run has different inputs, logs, outputs, and results.

## Basic Hierarchies

Job-oriented view:

```text
Pipeline or workflow
|-- Job 1
|   |-- Step 1
|   |-- Step 2
|   `-- Step 3
`-- Job 2
    |-- Step 1
    `-- Step 2
```

Stage-oriented view:

```text
Build stage
    |
    v
Test stage
    |
    v
Package stage
    |
    v
Deploy stage
```

Some tools organize primarily around jobs; others emphasize stages. A stage may contain several jobs. Jobs can run sequentially because of dependencies or in parallel when they are independent. A stage diagram is a logical view, not proof that every command runs one after another.

## Execution Vocabulary

- **Stage:** A logical phase such as build, test, or deploy. It groups work by purpose and may create an ordering boundary.
- **Job:** A set of related steps assigned to an execution environment. Jobs often have separate workspaces and can run concurrently.
- **Step:** One ordered unit inside a job. A step may invoke an action, script, or command and normally shares the job's workspace.
- **Task:** A generic unit of work. Some platforms use task as a formal object; elsewhere it is an informal description of a step or job.
- **Command:** A shell or program invocation, such as `pytest` or `docker build`. Several commands may appear in one step.
- **Dependency:** A requirement that one job, artifact, service, or value be available before another operation proceeds. Job dependencies form an execution graph.

If Job B depends on Job A, B normally waits for A and does not run after A fails unless failure behavior says otherwise. Without a dependency, runners may execute the jobs at the same time.

## Starting a Run

- **Event:** Something that occurs, such as a push, pull request, tag creation, schedule, or manual request.
- **Trigger:** The configured rule that maps an event to a workflow run. A push is an event; "pushes to `main`" is a filtered trigger.

Trigger filters matter. Running a deployment on every branch would be very different from running it only for reviewed changes on `main`. Scheduled and manual triggers may have no new commit, but the run still uses a particular source revision and inputs.

## Compute and Workspaces

- **Runner:** The compute system that accepts and executes a job. GitHub Actions uses this term for hosted or self-hosted machines.
- **Agent:** Another common name for software or a machine that performs pipeline work, used by several platforms.
- **Executor:** The mechanism or environment used to run work, such as a shell, container, virtual machine, or Kubernetes pod. Some platforms give executor a narrower formal meaning.
- **Workspace:** The filesystem area available to a job. Checked-out source and generated files live here during execution. A later job should not be assumed to share it.

Hosted runners are usually temporary. Self-hosted runners can retain state, which creates cache opportunities but also contamination and security risks. Jobs that need to exchange durable files should explicitly upload and download artifacts instead of relying on hidden machine state.

## Values and Targets

- **Environment:** A deployment target or operating context such as test, staging, or production. Some platforms also make environment a protected configuration object.
- **Variable:** A named value supplied to configuration or a process. Variables can hold paths, versions, feature settings, and other non-sensitive data.
- **Secret:** Sensitive data such as a token, password, or private key. A secret needs controlled storage, masked output, restricted access, and rotation. Calling a value a secret does not make unsafe logging harmless.

Environment-specific configuration should be separate from the artifact so the same verified output can be promoted. A runner should receive only the secrets needed by that job.

## Outputs and Storage

- **Artifact:** A durable output of a run, such as a package, binary, test report, or container image. Artifacts should be traceable to source and evidence.
- **Cache:** Reusable intermediate data intended to speed later work, such as downloaded dependencies. A cache is disposable and may be rebuilt; it should not be the only copy of a release.
- **Registry:** A service that stores and distributes packages or container images. Registries commonly provide versions, access controls, and retention settings.

An application package can be uploaded as a workflow artifact or published to a package registry. A container image is generally published to a container registry. Platform naming varies, but the durable-versus-accelerator distinction remains important.

## Decisions and Delivery

- **Quality gate:** A condition that must succeed before work progresses, such as tests, an allowed vulnerability threshold, or policy validation.
- **Approval:** An explicit authorization from a permitted person or system. An approval is a decision point, not a substitute for technical evidence.
- **Deployment:** Installing or activating a version in an environment.
- **Release:** Making a version available for intended use. A release can involve deployment, feature activation, publication, or a coordinated announcement.
- **Rollback:** Restoring a previous known-good version or state after a problem. Rollback safety depends on data and interface compatibility.

Pipeline logic connects these ideas. A gate may protect artifact publication; an environment approval may protect production deployment; monitoring may cause a rollback. Not every workflow performs all of these operations.

## Annotated GitHub Actions Example

```yaml
name: Basic CI

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out source code
        uses: actions/checkout@v4

      - name: Run tests
        run: echo "Run the project tests here"
```

- `name: Basic CI` gives the workflow a display name.
- `on` begins the trigger configuration.
- `push` selects push events, and `branches: - main` limits them to `main`.
- `jobs` contains the jobs in this workflow.
- `test` is the job identifier. It can be referenced by dependencies or expressions.
- `runs-on: ubuntu-latest` requests a GitHub-hosted Ubuntu runner label.
- `steps` lists ordered work inside the `test` job.
- The checkout step uses the versioned `actions/checkout` action to place repository source in the workspace.
- The test step uses `run` to execute a shell command. The `echo` is only a placeholder; a real workflow would invoke the project's test command.

The example has one job and no explicit dependency. Adding another independent job could allow parallel execution. Adding `needs: test` to a second job would make it wait for this job.

## Reading the Existing Workflows

In [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), the `docker` job uses `needs: quality`, so quality work gates the image build and smoke test. Both jobs request `ubuntu-latest`. The workflow's push and pull-request triggers provide different integration feedback paths.

[KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) has one `build-and-push` job. It can start from a push to `main` or `workflow_dispatch`, logs in to a registry, builds and publishes image tags, and scans the pushed SHA-tagged image. These files are examples, not universal pipeline templates.

## Practical Exercise

In 20-30 minutes, inspect one linked workflow. Record its workflow name, trigger filters, job IDs, runner labels, step types, commands, dependencies, variables, secret references, artifacts, and gates. Do not display secret values or edit the workflow.

## Knowledge Check

1. What is the difference between a workflow definition and a workflow run?
2. Why should two jobs not assume they share one workspace?
3. How does a cache differ from an artifact?
4. Can a stage contain parallel jobs?
5. Why can the same term mean slightly different things across platforms?

<details>
<summary>View answers</summary>

1. The definition describes automation; a run is one execution for specific inputs and source.
2. Jobs may execute on separate, temporary runners, so files must be transferred explicitly.
3. A cache is a disposable speed optimization; an artifact is a durable output or evidence.
4. Yes. A stage is a logical group and may contain independent concurrent jobs.
5. CI/CD products have different execution models and formal object names, so their documentation defines exact semantics.

</details>

## Navigation

- [Back to CI/CD Fundamentals](../README.md)
- [Previous: CI vs. Delivery vs. Deployment](../04-ci-vs-delivery-vs-deployment/)
- [Next: DevOps and Feedback Loops](../06-devops-and-feedback-loops/)
- [Back to All Learning Materials](../../README.md)
