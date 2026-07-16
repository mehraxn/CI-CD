# Continuous Integration

## Definition

Continuous integration (CI) is the practice of integrating small code changes into a shared codebase frequently and verifying each change with automated checks. Integration may happen by merging a reviewed pull request into the default branch. Many teams also run CI on the branch before the merge so problems are caught before shared code changes.

CI does not simply mean having a build server. A server can run a nightly build while developers keep large branches separate for weeks. Mature CI combines development habits - small changes, frequent integration, shared ownership - with reliable automated verification.

## Purpose and Working Pattern

The main purpose is to detect integration problems while a change is still small and fresh in the developer's mind. A common loop is:

```text
Push code
   |
   v
Install dependencies
   |
   v
Run formatter check
   |
   v
Run linter
   |
   v
Run unit tests
   |
   v
Build application
   |
   v
Report result
```

The exact checks depend on the project. Static checks inspect source without exercising the full running system. They can include formatting, linting, type analysis, security analysis, and dependency review. Automated tests check expected behavior at different levels. An automated build confirms that the source and declared dependencies can produce the intended output.

Pull-request CI gives both the author and reviewer evidence before merging. Main-branch CI then verifies the actual integrated result. A green result means only that the configured checks passed; it is not proof that the software is defect-free.

## Frequent, Small Integration

Small batches are easier to review, test, and diagnose. When a pipeline fails after a focused change, there are fewer possible causes. Frequent integration also reduces the distance between branches, which usually reduces difficult merge conflicts. This does not require committing unfinished behavior directly to users: feature flags and incremental design can keep incomplete features inactive.

Long-lived branches delay integration. Even if every branch passes its own tests, two branches may make incompatible assumptions. The problem appears only when they meet. CI aims to make that meeting routine rather than a special event.

## Handling CI Failures

A failed check should block the affected change until the cause is understood. First inspect the exact failed command and logs. Reproduce locally where practical, correct the change or the test, and rerun the complete required check set. Do not rerun repeatedly in the hope of getting a random pass; that hides unstable tests.

A broken default branch deserves immediate attention because every new branch starts from an unreliable baseline. The team should stop adding unrelated changes, identify the breaking change, and either fix it quickly or revert it safely. Ownership is shared: the goal is to restore useful feedback, not assign blame.

## Prerequisites

Useful CI normally needs:

- source stored in version control;
- a repeatable, non-interactive build and test process;
- dependencies declared in project files;
- checks that return meaningful success or failure codes;
- a runner with the required tools and isolated credentials;
- fast enough feedback for developers to act on it; and
- agreed rules about required checks and broken builds.

## Benefits and Limitations

CI finds many integration, build, style, test, and security problems earlier. It produces consistent evidence for review and creates a reliable base for delivery automation. It can shorten debugging because changes are smaller.

CI cannot decide whether requirements are correct, guarantee every execution path is safe, or replace code review. Poor tests create false confidence. Slow or flaky pipelines teach people to ignore results. CI also does not imply that an artifact is ready for production; delivery requires more controls and environment evidence.

## Common Mistakes

- **Integrating very large changes:** Review and diagnosis become harder.
- **Ignoring failed pipelines:** A red check becomes noise instead of a control.
- **Running only slow end-to-end tests:** Feedback arrives late and failures are harder to locate.
- **Keeping unstable tests:** Random results damage trust in the whole pipeline.
- **Allowing `main` to stay broken:** Everyone integrates against a bad baseline.
- **Depending on manual verification for every change:** Results become slow and inconsistent.
- **Testing branches but not the integrated result:** Merge interactions can remain unseen.

## Existing Project Example

Inspect the [TaskOps CI workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml). It runs for pull requests and pushes to `main`. Its `quality` job checks Ruff, Black, isort, pytest, Bandit, and dependencies. A dependent `docker` job builds and scans an image, starts a container, and smoke-tests `/health`. This is a concrete example of verification before delivery; the separate CD workflow performs deployment.

The [KubeOps CI workflow](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) also runs for pushes and pull requests. It combines source checks, tests, a Docker build, and an image scan in one job. Neither workflow proves that all possible CI practices are implemented.

## Practical Exercise

Spend 15-20 minutes with one workflow above. Write down its trigger, runner, jobs, five checks, and final output. Identify which failure would stop later work. Do not edit or run the workflow.

## Knowledge Check

1. Why is a build server alone not continuous integration?
2. Why do small, frequent changes improve CI feedback?
3. What should a team do when the default branch is broken?
4. Why are pull-request checks and main-branch checks both useful?

<details>
<summary>View answers</summary>

1. CI also requires frequent integration, automated verification, and team practices for acting on results.
2. They reduce possible failure causes, simplify review, and limit branch divergence.
3. Pause unrelated integration and restore the branch quickly with a fix or safe revert.
4. Pull-request checks prevent known problems before merge; main-branch checks verify the actual integrated state.

</details>

## Navigation

- [Back to CI/CD Fundamentals](../README.md)
- [Next: Continuous Delivery](../02-continuous-delivery/)
- [Back to All Learning Materials](../../README.md)
