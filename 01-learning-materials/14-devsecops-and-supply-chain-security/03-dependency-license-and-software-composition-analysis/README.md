# Dependency, License, and Software Composition Analysis

## Most of Your Software Is Someone Else's

**Software Composition Analysis (SCA)** examines the third-party components in your software — their versions, known vulnerabilities, licenses, and trustworthiness. The scope boundary against neighboring tools:

```text
SCA:
Analyzes third-party components, versions, licenses, and known risks.

SAST:
Analyzes application source or compiled code.

Package-manager audit:
Checks dependencies known to the package ecosystem or advisory source.
```

SCA operates on the **dependency graph** — **direct** and **transitive** dependencies resolved from the **manifest** (and precisely known only with a **lockfile**, as Topic 05 established). Both **runtime** and **development dependencies** matter: a compromised test tool runs with full CI privileges.

## Vulnerability Data and Its Limits

Known vulnerabilities are cataloged as **CVEs** (identifiers), classified by weakness type (**CWE**), scored by **CVSS** (0–10 severity), and published in **advisories** with **vulnerable version ranges** and, ideally, **fixed versions**. Every number needs interpretation: CVSS measures the vulnerability in the abstract, not your exposure. Two questions the databases cannot answer for you — **exploitability** (is there a practical attack for your configuration?) and **reachability** (does your code ever call the vulnerable path?). Hence triage:

| Question | Why it matters |
|----------|----------------|
| Is the dependency used at runtime? | Affects exposure |
| Is the vulnerable code reachable? | Affects exploitability |
| Is a fixed version available? | Determines remediation path |
| Is the service internet-facing? | Changes threat likelihood |
| Is a compensating control present? | May reduce immediate risk |
| What is the license obligation? | Affects legal use and distribution |

**pip-audit** — the repository's real SCA tool — checks declared or installed Python dependencies against advisory data (PyPI's advisory database and OSV). Its honest scope: it does not analyze application logic, does not prove a vulnerable path is reachable, and its results depend on how packages resolve and how fresh the advisories are.

```bash
pip-audit
```

## Licenses Are Risk Too

Every dependency arrives with a **license**: **permissive** ones (MIT, BSD, Apache-2.0) ask little; **copyleft** ones (GPL family) can impose obligations on distribution — a legal, not technical, risk. **License compatibility** and a written **license policy** (what is allowed, what needs review) belong in SCA just as CVEs do. No license scanning exists in this repository; the concern is conceptual here.

## Trust and the Package Ecosystem

Beyond known CVEs sit supply-chain attacks: **dependency confusion** (public package shadowing an internal name), **typosquatting**, outright **malicious packages**, and **abandoned packages** whose next "maintainer" is an attacker. Defenses: **maintainer trust** assessment, **package provenance** (increasingly published by ecosystems), **integrity checksums** (automatic in modern installers and lockfiles), and controlled registries ([Topic 07](../../07-artifacts-packages-and-registries/03-package-registries/)).

**Update automation** (Dependabot, Renovate — neither configured in this repository) closes the loop: small, focused update pull requests, each still passing tests, with lockfile diffs reviewed. Automated *merging* needs strict gates; automated *proposing* is nearly free. Urgency scales with exposure — an internet-facing service's critical CVE is a today problem; a dev-tool advisory on an internal batch job is a this-sprint problem.

## Common Mistakes

- Scanning only direct dependencies.
- Treating CVSS as the only risk factor.
- Updating a package without running the tests.
- Ignoring development dependencies.
- Never reviewing licenses.
- Assuming private packages are safe because they are private.
- Pulling from uncontrolled registries.
- Allowing package names to resolve from unintended sources.
- Keeping vulnerable pins forever ("predictably vulnerable" — Topic 05's warning).
- Removing the scanner to make CI green.

## Existing Repository Evidence

- **pip-audit is real and blocking** in three workflows: [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) and [CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) run `pip-audit -r requirements.txt` — note the scope choice: they audit the *runtime* requirements file, so development dependencies (in `requirements-dev.txt`) are installed and used but **not audited** — a real, instructive gap. [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) runs the same pattern.
- **The three dependency styles change what an audit means** ([Topic 05](../../05-builds-dependencies-and-caching/02-dependency-management-and-lockfiles/)): TaskOps' exact pins make audits stable and reproducible; KubeOps' unpinned file means each audit checks whatever resolved that day; no lockfiles exist, so transitive versions are never pinned or precisely audited.
- **Trivy** also scans installed OS and Python packages inside built images (next lesson) — a second, overlapping SCA layer at the artifact level.
- **Absent**: Dependabot/Renovate configuration, GitHub Dependency Review, license scanning, and lockfile-based auditing — all conceptual here, candidates for a later enhancement phase.

## Practical Exercise

Audit the repository's dependency-security posture. For each of the three projects, record:

```text
Dependency source
Manifest or lockfile
Audit tool
Known limitations
Update mechanism
License information
```

Then answer two pointed questions with file evidence: (1) which project would show different pip-audit results on two consecutive days without any commit, and why; (2) name one dependency that is installed in CI but never audited by pip-audit, and state the risk that creates. Do not run any tool. Target 20–30 minutes.

## Knowledge Check

1. What does SCA examine that SAST does not?
2. Why is CVSS alone insufficient for a remediation decision?
3. What are exploitability and reachability, and which tools in this repository assess them?
4. What real audit-scope gap exists in the TaskOps workflows?
5. Why do unpinned dependencies undermine audit reproducibility?
6. Why do development dependencies deserve security attention?

<details>
<summary>View answers</summary>

1. Third-party components — their versions, known vulnerabilities, licenses, and provenance — rather than the application's own code.
2. It scores abstract severity, not your exposure: reachability, runtime use, internet-facing status, and compensating controls change the actual risk.
3. Whether a practical attack exists for your setup, and whether your code invokes the vulnerable path; no tool here assesses them — pip-audit and Trivy report version matches only.
4. `pip-audit -r requirements.txt` audits only runtime dependencies; the dev tools installed from `requirements-dev.txt` are never audited.
5. Each resolution can pick different versions, so results describe that day's graph, not a reviewed, stable one.
6. They run with full CI privileges (and developer machines); a compromised dev tool is a supply-chain compromise regardless of what ships to production.

</details>

## Navigation

- [Back to DevSecOps and Supply-Chain Security](../README.md)
- [Previous: SAST, Code Quality, and Secret Scanning](../02-sast-code-quality-and-secret-scanning/)
- [Next: Container, Kubernetes, and IaC Security Scanning](../04-container-kubernetes-and-iac-security-scanning/)
- [Back to All Learning Materials](../../README.md)
