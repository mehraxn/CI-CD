# DevSecOps Fundamentals and Security by Design

## The Vocabulary That Organizes Everything

Security conversations go in circles until four words are separated:

```text
Threat:
A possible cause of harm.

Vulnerability:
A weakness that may be exploited.

Risk:
The combination of likelihood and impact.

Control:
A measure intended to reduce risk.
```

A threat (an attacker wanting your registry credentials) meets a vulnerability (a token printed in logs) and produces risk proportional to **likelihood** (public repo? popular target?) and **impact** (what can that token do?). An **exploit** is a working method of using the vulnerability. **Risk treatment** picks a response: reduce it with controls, accept it knowingly, transfer it, or avoid the activity. Controls themselves divide into **prevention** (stop it happening), **detection** (notice it), **response** (contain it), and **recovery** (restore service).

## Security by Design

The cheapest vulnerability is the one never designed in. **Security by design** front-loads the thinking:

- **Secure defaults** — the out-of-box configuration is the safe one; danger requires opting in.
- **Least privilege** — every identity gets the minimum it needs (the recurring theme of this whole repository's `permissions:` blocks).
- **Separation of duties** — no single person authors, approves, and deploys unreviewed.
- **Defense in depth** — layered controls, so one failure is not a breach:

```text
Source review
+ dependency controls
+ secure build
+ artifact verification
+ deployment policy
+ runtime monitoring
```

- **Threat modeling** — a structured "what could go wrong?": map the **attack surface** (everything reachable by an attacker) and **trust boundaries** (where data or control crosses between trust levels — user→app, app→database, PR→CI runner), then enumerate threats per boundary. It need not be heavyweight; a table and an hour beat nothing, and it must be *revisited* as the system changes.
- **Security requirements, abuse and misuse cases** — alongside "user can reset password" write "attacker cannot enumerate accounts via reset"; give them **acceptance criteria** and test them like any requirement.

## The Delivery Loop

The Secure Software Development Lifecycle, compressed into the shape this section follows:

```text
Security requirement
        ↓
Design and threat review
        ↓
Secure implementation
        ↓
Automated verification
        ↓
Deployment controls
        ↓
Runtime observation
        ↓
Incident learning
```

**Shift-left** moves feedback into the early steps (review, static analysis, dependency checks); **shift-right** acknowledges some truths only exist after deployment (runtime behavior, real attacks, incident data). Both feed the loop: incident learning updates requirements and threat models. Culturally, DevSecOps means **shared responsibility** — developers own the security of what they ship, with security specialists as enablers and reviewers (a **security champion** in a team is a common bridge), pull-request review carrying security as a first-class concern, and automated gates enforcing the floor.

## Common Mistakes

- Security added only before release, when changes are most expensive.
- One team solely responsible for all security — a bottleneck and an excuse.
- No ownership for findings, so scanners shout into the void.
- Threat modeling performed once and forgotten as the system evolves.
- Security gates with no risk context, blocking trivia and missing what matters.
- Developers unable to understand scanner results — unusable feedback is no feedback.
- Production monitoring disconnected from development learning.
- Security exceptions without expiration (they become permanent silently).
- Treating compliance as proof of security.
- Security requirements written but never tested.

## Existing Repository Evidence

The repository practices several design-time controls without naming them: **least privilege** in workflow `permissions` ([KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) comments "Read-only token is all CI needs"), **secure defaults** in containers ([TaskOps Dockerfile](../../../Projects/1_project/taskops-cicd/Dockerfile) creates and switches to a non-root `appuser`; the [KubeOps Helm values](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values.yaml) set `runAsNonRoot`, `readOnlyRootFilesystem`, and `allowPrivilegeEscalation: false`), **defense in depth** in the CI gate stack (lint → tests → Bandit → pip-audit → Trivy → smoke test), and **abuse-case testing** in [TaskOps `test_security.py`](../../../Projects/1_project/taskops-cicd/tests/test_security.py), which asserts that requests *without* a CSRF token are rejected — a misuse case with an automated acceptance criterion. No written threat model exists in the repository; that remains this lesson's exercise.

## Practical Exercise

Build a threat-boundary map for TaskOps (Project 1). Identify at least four assets (the GHCR image, the deploy SSH key, the production database file, the CI pipeline itself) and for each:

```text
Asset
Trust boundary
Possible threat
Existing control
Missing control
Owner
```

Use only repository files as evidence for "existing control" (workflows, Dockerfile, compose files, tests). Do not perform any penetration testing or run any tool. Target 25–35 minutes.

## Knowledge Check

1. Distinguish threat, vulnerability, and risk in one sentence each.
2. What are the four control families, and why is prevention alone insufficient?
3. What is a trust boundary? Give one from this repository.
4. Why must threat modeling recur rather than happen once?
5. What real misuse-case test exists in this repository?
6. What does "secure defaults" mean in the TaskOps Dockerfile?

<details>
<summary>View answers</summary>

1. A threat is a possible cause of harm; a vulnerability is an exploitable weakness; risk combines the likelihood and impact of the threat exploiting the weakness.
2. Prevention, detection, response, and recovery — prevention eventually fails, so noticing, containing, and restoring must also be designed.
3. A point where data or control crosses trust levels — for example, a pull request (untrusted code) entering the CI runner, or user input entering the Flask app.
4. The system, its dependencies, and the threat landscape change; a stale model describes a system that no longer exists.
5. TaskOps' `test_security.py` asserts that POSTs without a CSRF token are rejected — an attacker behavior encoded as a failing-path test.
6. The image runs as a non-root user by default; privileged execution would require deliberately changing it.

</details>

## Navigation

- [Back to DevSecOps and Supply-Chain Security](../README.md)
- [Next: SAST, Code Quality, and Secret Scanning](../02-sast-code-quality-and-secret-scanning/)
- [Back to All Learning Materials](../../README.md)
