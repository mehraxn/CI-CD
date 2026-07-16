# Jenkins

> This lesson is conceptual. The repository contains no `Jenkinsfile` and no project uses Jenkins; the goal is to recognize Jenkins concepts and map them to the GitHub Actions vocabulary you already know.

## What Jenkins Is

Jenkins is a long-established, self-hosted automation server. Unlike GitHub Actions or GitLab CI/CD, it is not tied to a code-hosting platform: a team installs and operates a Jenkins **controller**, connects **agents** to do the work, and integrates with repositories through plugins and webhooks. That independence is Jenkins's strength — it automates anything, anywhere, including air-gapped internal networks — and its cost: everything the platform vendors do for you, a Jenkins team does itself.

## Architecture

```text
Developer
    ↓
Source repository
    ↓
Jenkins controller
    ↓
Build queue
    ↓
Selected agent
    ↓
Pipeline stages and steps
```

- The **controller** hosts the UI, stores configuration, schedules work, and should not execute heavy builds itself.
- **Agents** (running on **nodes** — the machines) execute jobs. Each node offers one or more **executors**, the parallel work slots; two executors means two concurrent jobs on that node.
- Jobs wait in the **build queue** until a node with a matching label and a free executor accepts them.
- Each job runs in a **workspace** directory on the agent — often *reused* between builds, unlike the fresh hosted runners of GitHub Actions, which is both a speed advantage and a contamination risk.

Rough translation table: controller ≈ the platform service; agent/node ≈ runner; executor ≈ a runner's concurrency slot; workspace ≈ the job's working directory.

## The Jenkinsfile

Jenkins jobs can be configured in the UI, but modern practice is Pipeline as Code via a `Jenkinsfile` committed to the repository. Two dialects exist: **Declarative Pipeline** (structured, opinionated, easier to read — shown below) and **Scripted Pipeline** (raw Groovy, maximum flexibility, harder to review).

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Build application'
            }
        }

        stage('Test') {
            steps {
                echo 'Run tests'
            }
        }

        stage('Package') {
            steps {
                echo 'Create package'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
```

- **`pipeline`** — the root block of a Declarative Pipeline.
- **`agent`** — where the pipeline (or a stage) runs; `any` accepts any available agent, while `agent { label 'linux' }` routes by label.
- **`stages` / `stage`** — the named phases shown in the Jenkins UI; roughly the jobs-and-graph layer of other platforms.
- **`steps`** — the commands inside a stage (`echo`, `sh`, plugin-provided steps).
- **`post`** — actions after the stages complete; **`always`** runs regardless of result (like `if: always()`), **`failure`** only on failure — the natural home for notifications and cleanup.

## Parameters, Environment, Credentials, Triggers

```groovy
pipeline {
    agent any

    parameters {
        choice(
            name: 'DEPLOY_ENVIRONMENT',
            choices: ['staging', 'production'],
            description: 'Target deployment environment'
        )
    }

    stages {
        stage('Display Selection') {
            steps {
                echo "Environment: ${params.DEPLOY_ENVIRONMENT}"
            }
        }
    }
}
```

`parameters` is Jenkins's `workflow_dispatch.inputs`: typed values a person supplies when starting the build, read via `params.*`. An `environment {}` block sets environment variables at pipeline or stage level. **Credentials** live in Jenkins's credential store and are bound to variables per use — the same rule applies as everywhere: scoped access, no printing, no long-lived secrets in the file. **Triggers** include webhooks from the repository host, cron schedules, and upstream-job completion.

**Shared Libraries** are Jenkins's main reuse mechanism: versioned Groovy code in its own repository, imported by many Jenkinsfiles — closest in spirit to reusable workflows, with the same versioning and ownership obligations.

## Plugins: Power and Liability

Almost everything in Jenkins — Git integration, Docker steps, credentials, UI themes — is a **plugin**. This gives Jenkins unmatched flexibility and a distinctive risk profile:

- Plugins run inside the controller with high privilege; a vulnerable plugin is a vulnerable server.
- Plugins have their own release cycles and **compatibility** matrices; upgrading Jenkins can break plugins and vice versa.
- Someone must own **updates**, security advisories, **backup and recovery** of controller configuration, and **upgrade testing** on a staging controller before touching production CI.

Self-hosting also means owning **scaling** (adding agents, autoscaling in cloud or Kubernetes) and availability of the controller itself — when Jenkins is down, nobody ships.

## When Jenkins Remains Useful

Jenkins remains a reasonable choice when automation must run entirely inside a private network, when the team needs deep customization no SaaS platform offers, when significant Jenkins expertise and investment already exist, or when one system must orchestrate across many code hosts. It is a poor default for a small team already on GitHub or GitLab with no operations capacity to spare.

Common Jenkins problems to recognize: aging unowned plugins, one overloaded controller doing builds itself, snowflake agents with undocumented tools, UI-configured jobs nobody can reproduce, and Jenkinsfiles that drifted into hundreds of lines of scripted Groovy.

## Practical Exercise

Take this simple CI flow — the same one you will translate to GitLab in the next lesson:

```text
Checkout → Install dependencies → Lint → Test → Build image
```

Write a **non-executable** Declarative `Jenkinsfile` snippet in your notes (or below in a scratch copy of this lesson) with one stage per phase, using only `echo` placeholder steps, plus a `post` block that reports failure. Do not create a `Jenkinsfile` in the repository. Then annotate each line with its GitHub Actions equivalent (`stage` ↔ job or step group, `agent` ↔ `runs-on`, `post/always` ↔ `if: always()`). Target 20–30 minutes.

## Knowledge Check

1. What are the roles of the controller and the agents?
2. What is an executor?
3. How do Declarative and Scripted Pipelines differ?
4. What is the Jenkins equivalent of `if: always()` cleanup?
5. Why are plugins both Jenkins's strength and its main operational risk?
6. Why does a Jenkins workspace differ from a fresh hosted runner?

<details>
<summary>View answers</summary>

1. The controller schedules work, stores configuration, and serves the UI; agents execute the actual pipeline work on nodes.
2. A parallel work slot on a node — the number of executors bounds how many jobs the node runs concurrently.
3. Declarative is a structured, opinionated syntax that is easier to read and validate; Scripted is raw Groovy with full programming flexibility and harder review.
4. The `post { always { ... } }` block, which runs after the stages regardless of result.
5. They provide nearly all functionality, but they run privileged in the controller, carry vulnerabilities, and create update/compatibility work the team must own.
6. Workspaces are directories on agents that are often reused between builds, so leftover state can persist — faster, but a contamination risk that fresh per-job runners avoid.

</details>

## Navigation

- [Back to Pipeline as Code and Platforms](../README.md)
- [Previous: GitHub Actions](../06-github-actions/)
- [Next: GitLab CI/CD](../08-gitlab-cicd/)
- [Back to All Learning Materials](../../README.md)
