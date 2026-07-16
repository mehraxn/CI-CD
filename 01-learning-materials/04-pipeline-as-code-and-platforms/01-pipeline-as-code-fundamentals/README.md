# Pipeline as Code Fundamentals

## Definition

**Pipeline as Code** stores the definition of an automated pipeline — its triggers, jobs, dependencies, and settings — as files under version control, normally beside the application source they build and verify. The pipeline changes through the same mechanism as the code: a commit, a pull request, a review, a merge.

Two styles of definition exist:

```text
Declarative configuration:
Describes the desired workflow, jobs, dependencies, and settings.

Scripted or imperative configuration:
Describes commands and control flow step by step.
```

GitHub Actions and GitLab CI/CD are primarily declarative YAML; Jenkins supports both a declarative and a scripted `Jenkinsfile`. In practice, most CI/CD systems combine the two: a declarative outer structure (jobs, triggers, dependencies) wrapping imperative shell scripts inside steps. The declarative layer is what the platform validates and visualizes; the scripts are what actually run.

## What Versioning Buys You

```yaml
name: Application CI

on:
  pull_request:

jobs:
  verify:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run verification
        run: ./scripts/verify.sh
```

This small educational example already demonstrates the core benefits:

- **Versioning** — the file lives in Git; every change is a commit with an author and a date.
- **Review** — a change to the trigger or the script path goes through a pull request like any code change.
- **Traceability and auditing** — `git log -- .github/workflows/ci.yml` shows exactly when behavior changed; combined with run logs, you can reconstruct what any past run did.
- **Repeatability** — the same file produces the same pipeline structure on every matching event. (Repeatable *structure* does not guarantee reproducible *results* — unpinned dependencies and changing runner images can still vary.)
- **Rollback** — `git revert` restores previous pipeline behavior without archaeology in a settings UI.
- **Event-driven automation** — the `on:` block declares when the pipeline runs, visible to every reader.

Notice also the **separation between application logic and pipeline logic**: the workflow calls `./scripts/verify.sh` rather than embedding fifty lines of shell. The script can be run locally, tested, and reviewed on its own, while the workflow stays a thin, readable trigger-and-structure layer. The tradeoff is that important logic must not *hide* in undocumented scripts — the script needs the same review and documentation discipline as the workflow.

## Ownership, Validation, and Change Discipline

Pipeline files need an owner — a person or team responsible for reviewing changes, keeping documentation current, and answering "why does this job exist?" Unowned pipelines rot: nobody dares remove anything, and every incident adds another unreviewed patch.

Healthy teams treat pipeline changes like code changes:

- **Linting and validation** — editors and platform tools can check syntax and schema before merge; GitHub validates workflow files when they are pushed, and GitLab offers a CI lint tool.
- **Testing pipeline changes** — try risky changes on a branch or in a fork before they reach the default branch; a pipeline change that breaks CI blocks everyone.
- **Security review** — pipeline files control what code runs with which credentials; a malicious or careless workflow change is a security event, not just a build problem.
- **Template versioning and backward compatibility** — when many repositories consume a shared workflow or template, changes to it must be versioned so consumers upgrade deliberately rather than breaking silently.

## Where Pipeline Definitions Live

- **Repository-local pipelines** — the definition sits in the repository it serves (this repository's model: each project carries its own `.github/workflows/`). Simple, self-contained, and reviewable in context.
- **Centralized pipeline repositories** — one repository holds shared workflows or libraries that many repositories call. Reduces duplication, but adds coupling: a central change can affect every consumer.
- **Monorepo pipelines** — one large repository uses path filters and multiple workflows to run only relevant checks per change.
- **Polyrepo pipelines** — many repositories each carry a pipeline; duplication pressure grows with the repository count, which is what reuse mechanisms (lesson 04) address.

Be aware of **platform lock-in**: the concepts transfer between platforms, but the files do not. A team migrating from GitHub Actions to GitLab CI/CD rewrites its YAML. Keeping logic in portable shell scripts and using the platform file only for structure reduces — but never eliminates — migration cost.

## Common Anti-Patterns

- Large unreviewed pipeline changes merged in a hurry.
- Unclear pipeline ownership ("nobody touches that file").
- Hidden UI-only configuration that contradicts or supplements the versioned file.
- The same workflow duplicated across many repositories with slow drift.
- Unpinned third-party components that change behavior without a commit.
- Important logic buried in undocumented scripts.
- Secrets committed into configuration files.
- Shared templates changed without compatibility testing against consumers.
- One enormous pipeline file that nobody can read end to end.
- Assuming syntactically valid YAML is operationally correct.

## Existing Workflow Evidence

This repository practices repository-local Pipeline as Code: [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml), [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml), and [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) are all versioned YAML files inside their project directories. TaskOps CD also shows the separation principle: the deployment logic lives in `scripts/deploy.sh` on the target, while the workflow provides structure, gates, and credentials.

## Practical Exercise

Pick one real workflow file (for example TaskOps CI) and inspect its Git history:

```bash
git log --oneline -- Projects/1_project/taskops-cicd/.github/workflows/ci.yml
```

For the most recent change that touched it, answer: what changed, who could have reviewed it, and how would you revert only that pipeline change if it broke CI? Write the exact `git revert` command you would use — but do not run it, and do not rewrite history. Target 15–25 minutes.

## Knowledge Check

1. What is the difference between declarative and scripted pipeline configuration?
2. Why does Pipeline as Code improve auditability?
3. Does storing a pipeline in Git guarantee it is secure or correct?
4. Why should important logic live in reviewable scripts rather than being scattered through the workflow file?
5. What risk does a centralized pipeline repository introduce?

<details>
<summary>View answers</summary>

1. Declarative configuration describes the desired structure (jobs, triggers, settings); scripted configuration describes commands and control flow step by step. Most systems combine both.
2. Every change is a Git commit with an author, date, and diff, which — combined with run logs — lets you reconstruct when and why behavior changed.
3. No. It makes the pipeline visible, reviewable, and reversible; quality and security still depend on review discipline and good design.
4. Scripts can be run locally, tested, and reviewed independently, and the workflow stays a readable structure layer — provided the scripts are documented and reviewed too.
5. Coupling: a change to the central workflow can break or alter every consuming repository at once, so it needs versioning and compatibility testing.

</details>

## Navigation

- [Back to Pipeline as Code and Platforms](../README.md)
- [Next: YAML Fundamentals](../02-yaml-fundamentals/)
- [Back to All Learning Materials](../../README.md)
