# Runners and Execution Environments

## What Executes a Job

Pipeline configuration describes work; something real has to do it. GitHub Actions calls that machine or process a **runner**; Jenkins says **agent** or **node** (with **executors** as the parallel work slots on a node); GitLab has **GitLab Runners** with pluggable executors. The concept is identical: a worker polls or receives jobs, prepares a **workspace**, executes steps, reports logs and results, and cleans up (or doesn't — which is where trouble starts).

Runner form factors vary: full **virtual machines**, **containers**, pods in a **Kubernetes** cluster, or **bare-metal** hosts. Each choice trades isolation strength, startup speed, and operational effort.

## Hosted vs. Self-Hosted

| Area | Hosted runner | Self-hosted runner |
|------|---------------|--------------------|
| Maintenance | Provider managed | User or organization managed |
| Customization | Limited to supported configuration | Highly customizable |
| Isolation | Often a fresh environment | Depends on the design |
| Internal-network access | Usually limited | Can be configured |
| Scaling | Often provider managed | Must be designed |
| Security responsibility | Shared | Mostly operator controlled |
| Cost | Usage or plan based | Infrastructure plus operational cost |

A hosted runner:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

`ubuntu-latest` names a provider-maintained **runner image** with a large set of **installed tools** (language runtimes, Docker, common CLIs). Fresh VM per job, discarded afterward.

A self-hosted runner selected by **labels**:

```yaml
jobs:
  internal-test:
    runs-on:
      - self-hosted
      - linux
      - internal-network
```

Labels (GitLab calls them **tags**) perform **job routing**: the job queues until a runner carrying *all* listed labels picks it up. **Runner groups** add organization-level control over which repositories may use which runners. Two facts about labels matter more than any syntax: jobs **queue** when no matching runner is free (measure queue time, plan **concurrency** limits and **autoscaling**), and labels are *routing*, **not security boundaries** — any workflow allowed to target the label runs there, with whatever network access and credentials that machine holds.

## Resources and Hygiene

Real jobs consume **CPU, memory, and disk**. Hosted runners have fixed sizes; self-hosted runners have whatever you gave them — and whatever previous jobs left behind. Persistent runners accumulate stale workspaces, growing tool caches, and full disks; **workspace cleanup** must be deliberate. Tool caches cut both ways: they speed up builds and they carry state between jobs.

Network matters too: self-hosted runners often sit behind **proxies** or inside private networks — that internal access is exactly why they are used, and exactly what makes running untrusted code on them dangerous.

## Service Containers

Integration tests often need a database or queue next to the job. Service containers start alongside the job and disappear with it:

```yaml
jobs:
  integration-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test-password
        ports:
          - 5432:5432

    steps:
      - name: Run integration tests
        run: echo "Connect tests to PostgreSQL"
```

The password here is a throwaway value for an ephemeral test database, not a secret — real credentials never belong in workflow files.

## Why Ephemeral Runners Are Usually Safer

An **ephemeral runner** serves one job and is destroyed; a **persistent runner** lives across many jobs. Ephemeral wins on security defaults:

- Every job gets a fresh environment — no leftover files, processes, or malware.
- Credentials do not persist beyond the job that used them.
- No cross-job contamination between different repositories, branches, or pull requests.
- Cleanup is automatic — destruction *is* the cleanup.
- A compromise ends when the runner does; the attacker gets minutes, not months.

Ephemeral is necessary but not sufficient. Ephemeral runners still need secure and updated base images, minimal permissions and cloud roles, network restrictions, logging, and safe secrets handling. A fresh VM with an over-privileged cloud role is freshly dangerous every single job.

## Privilege and Credential Hazards

Three patterns deserve special caution on any runner:

- **Privileged containers and Docker socket exposure** — mounting `/var/run/docker.sock` or running privileged containers hands the job effective root over the host and every other container on it.
- **Cloud credentials** — long-lived keys stored on a runner outlive jobs and leak; prefer **workload identity** (OIDC-style short-lived credentials issued per job).
- **Forked pull requests** — running untrusted fork code on a self-hosted runner inside your network is the classic CI compromise path. Platforms restrict secrets for fork events, but the runner's own network position and local credentials are still exposed to the code it executes.

Self-hosted fleets are operational software: they need **updates** (runner agent, OS, tools), **monitoring** (queue depth, disk, failures), **maintenance** ownership, and honest **cost** accounting — the infrastructure is often cheaper than the hosted minutes, but the humans are not.

## Common Mistakes

- Running untrusted code on privileged internal runners.
- Persistent credentials sitting on long-lived runners.
- Shared workspaces leaking state (or secrets) between jobs.
- Excessive cloud permissions attached to the runner identity.
- Exposing the Docker socket to job containers.
- Skipping runner and image updates.
- Manually installed tools nobody documented — builds that work on one runner only.
- Unlimited concurrency saturating shared services.
- Ignoring disk cleanup until jobs fail with "no space left on device".
- Treating labels or tags as isolation controls.

## Existing Workflow Evidence

Every job in this repository runs on GitHub-hosted runners: all four workflows declare `runs-on: ubuntu-latest` — see [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml), [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml), and [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml). TaskOps CI relies on tools preinstalled on the hosted image (Docker, Python tooling via `setup-python`) and starts its own test container inside the job rather than using `services:`. The repository does not currently demonstrate self-hosted runners, runner groups, service containers, or Kubernetes-based runners; those remain conceptual here.

## Practical Exercise

List every `runs-on` value across the four real workflow files and classify each as hosted, self-hosted, or unknown. Then answer for TaskOps CI's `docker` job specifically:

1. Which tools does it assume are already on the runner image?
2. What state (containers, images) does the job create, and what would happen on a *persistent* runner if the `if: always()` cleanup step were removed?
3. Which single change in this lesson's hazard list would be most dangerous if this job moved to a self-hosted runner behind a company firewall?

Keep answers as notes; change nothing. Target 20–30 minutes.

## Knowledge Check

1. What is the difference between a runner label and a security boundary?
2. Why are ephemeral runners safer by default than persistent ones?
3. What does exposing the Docker socket to a job effectively grant?
4. Why do forked pull requests plus self-hosted runners form a dangerous combination?
5. Name two costs of self-hosted runners beyond the hardware.

<details>
<summary>View answers</summary>

1. A label only routes jobs to matching runners; it does not restrict what the job can do once there. Isolation must come from the runner's design and permissions.
2. Each job gets a fresh environment, credentials and contamination do not persist across jobs, and a compromise ends when the runner is destroyed.
3. Effective root on the host: the job can start privileged containers, read other containers, and escape its own isolation.
4. Fork code is untrusted, and a self-hosted runner contributes its network position and any local credentials to whatever code it executes.
5. Ongoing maintenance (updates, monitoring, cleanup, scaling design) and security responsibility — the operational human time, not just infrastructure.

</details>

## Navigation

- [Back to Pipeline as Code and Platforms](../README.md)
- [Previous: Reusable Workflows, Templates, and Components](../04-reusable-workflows-templates-and-components/)
- [Next: GitHub Actions](../06-github-actions/)
- [Back to All Learning Materials](../../README.md)
