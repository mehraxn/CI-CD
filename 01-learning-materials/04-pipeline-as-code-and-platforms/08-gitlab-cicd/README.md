# GitLab CI/CD

> This lesson is conceptual. The repository contains no `.gitlab-ci.yml` and no project uses GitLab CI/CD; the goal is to read GitLab pipeline configuration fluently and map it onto concepts you already know.

## The Model

GitLab CI/CD is built into the GitLab platform. One file — `.gitlab-ci.yml` at the repository root — defines the **pipeline**: a set of **jobs** grouped into ordered **stages**, executed by **GitLab Runners**. Where GitHub Actions organizes multiple workflow files around events, GitLab traditionally organizes one pipeline definition around stages, with **rules** deciding which jobs each pipeline run includes.

## A Basic Pipeline

```yaml
stages:
  - build
  - test
  - package

build-application:
  stage: build
  script:
    - echo "Build application"

unit-tests:
  stage: test
  script:
    - echo "Run unit tests"

package-application:
  stage: package
  script:
    - echo "Create package"
```

- **`stages`** declares the ordered phases of the pipeline.
- Each top-level key that is not a reserved word (`build-application`, `unit-tests`, …) is a **job name**.
- **`stage`** assigns the job to a phase; **`script`** is its list of shell commands (GitLab's `run:`, but always a list).
- **Stage ordering** is the default execution graph: all jobs in `build` finish before any job in `test` starts. Multiple jobs in one stage run **in parallel** (runner capacity permitting).

## Rules: Conditional Jobs

```yaml
deploy-staging:
  stage: deploy
  script:
    - echo "Deploy to staging"
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
```

`rules` evaluates conditions against **predefined variables** — GitLab populates dozens, such as `$CI_COMMIT_BRANCH`, `$CI_PIPELINE_SOURCE`, and `$CI_MERGE_REQUEST_IID` — to decide whether the job is included in this pipeline run. Rules can also set `when: manual` (a button, GitLab's basic manual gate) or `when: never`. You will still see **`only` and `except`** in older configurations; they are the legacy mechanism that `rules` replaced — read them, but write `rules`. **Variables** can also be defined at instance, group, project, and job level, with protected and masked options for secret-like values (GitLab's secrets story is variables with protection flags, plus external secret-manager integrations).

## Runners and Tags

```yaml
internal-test:
  tags:
    - linux
    - internal
  script:
    - echo "Run on a matching GitLab Runner"
```

**GitLab Runners** register with an instance, group, or project and advertise **tags**; a job runs only on a runner matching all its tags. Exactly like GitHub Actions labels, tags are routing, **not security boundaries** — a runner's isolation depends on its executor (shell, Docker, Kubernetes) and configuration, and shell-executor runners in particular share state between jobs. GitLab.com provides hosted runners; **self-managed GitLab** instances (and projects wanting private capacity on GitLab.com) run their own, with the same maintenance and hardening duties covered in [Runners and Execution Environments](../05-runners-and-execution-environments/).

## Beyond Stage Ordering: needs

```yaml
package:
  stage: package
  needs:
    - unit-tests
    - integration-tests
  script:
    - echo "Create package"
```

`needs` creates DAG relationships that cut across the stage grid: `package` starts as soon as its two named jobs finish, without waiting for the rest of their stage. This is GitLab's version of the dependency graphs from [Job Dependencies and DAG Pipelines](../../03-pipeline-architecture/03-job-dependencies-and-dag-pipelines/). `needs` also controls **artifact** download from the named jobs — GitLab jobs pass files via `artifacts:` declarations, and speed up repeated work with `cache:`. **Services** (`services:`) attach helper containers such as databases, mirroring GitHub Actions service containers.

## Composition and Larger Structures

```yaml
include:
  - local: .gitlab/ci/security.yml
```

- **`include`** merges other YAML files — local, from other projects, remote, or GitLab-provided **templates** — into the pipeline definition; **CI/CD components** are the newer, versioned, parameterized packaging of the same idea.
- **Parent-child pipelines**: a job can trigger a **child pipeline** from a generated or included file, isolating a subsystem's pipeline (a common monorepo pattern).
- **Multi-project pipelines** trigger pipelines in other projects — cross-repository delivery chains.
- **Merge-request pipelines** run in the context of an MR (GitLab's `pull_request` event, with its own predefined variables and rules), and **scheduled pipelines** run on cron.
- **Environments** (`environment: production`) track deployments; **protected environments** restrict who can deploy — GitLab's counterpart to environment approvals.
- **Pipeline validation**: GitLab ships a CI Lint tool and editor integration that validate `.gitlab-ci.yml` against the schema before you commit — use it; the file's merge behavior with `include` makes purely visual review unreliable.

## Common Mistakes

- Writing new configuration with `only`/`except` instead of `rules`.
- Treating runner tags as isolation.
- Using shell-executor runners for untrusted code.
- One giant `.gitlab-ci.yml` instead of `include`-structured files.
- Forgetting that jobs in the same stage run in parallel and may race on shared resources.
- Marking variables neither protected nor masked and treating them as secrets.
- Ignoring the difference between branch pipelines and merge-request pipelines, causing duplicate or missing runs.

## Practical Exercise

Translate the same CI flow you used in the Jenkins exercise:

```text
Checkout → Install dependencies → Lint → Test → Build image
```

Write a **non-executable** `.gitlab-ci.yml` snippet in your notes: define `stages`, one job per phase with `echo` placeholder scripts, put Lint and Test in the same stage so they parallelize, and add a `rules` entry so the image build runs only on the default branch. (In GitLab, checkout is implicit — the runner fetches the repository before `script` runs, so you need no checkout job.) Do not create a `.gitlab-ci.yml` file in the repository. Then note each element's GitHub Actions equivalent. Target 20–30 minutes.

## Knowledge Check

1. Where does GitLab CI/CD configuration live?
2. How do stages and `needs` interact?
3. What replaced `only`/`except`, and why should new configuration use it?
4. Are runner tags a security control?
5. What is a parent-child pipeline useful for?
6. How does GitLab handle the "manual approval" concept?

<details>
<summary>View answers</summary>

1. In `.gitlab-ci.yml` at the repository root, optionally composed from other files via `include`.
2. Stages define the default ordered phases; `needs` creates direct job-to-job dependencies that let a job start before its stage would normally begin.
3. `rules` — a single, more expressive conditional mechanism; `only`/`except` are legacy and should only be read, not written.
4. No — tags route jobs to matching runners; isolation depends on the runner's executor and configuration.
5. Isolating a subsystem's pipeline (for example, per-directory pipelines in a monorepo) by triggering a separately defined child pipeline.
6. Through `when: manual` jobs and protected environments that restrict who may run deployment jobs.

</details>

## Navigation

- [Back to Pipeline as Code and Platforms](../README.md)
- [Previous: Jenkins](../07-jenkins/)
- [Back to All Learning Materials](../../README.md)
