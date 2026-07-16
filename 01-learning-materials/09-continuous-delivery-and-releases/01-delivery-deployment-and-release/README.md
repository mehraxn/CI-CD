# Delivery, Deployment, and Release

## Five Related Decisions

| Concept | Main question |
|---------|---------------|
| Continuous integration | Can changes be integrated and verified safely? |
| Continuous delivery | Can the system be released safely on demand? |
| Continuous deployment | Can qualifying changes reach production automatically? |
| Deployment | Was the software installed or activated? |
| Release | Was the version or feature made available? |

CI creates fast feedback on merged changes. Continuous delivery adds a repeatable path to a **releasable state** and **release-on-demand**. Continuous deployment removes a required manual production decision for qualifying changes. Frequent deployment is not automatically continuous deployment if releases are still batched or performed manually.

A **technical deployment** changes a running environment. A **business release** changes availability or officially announces a version. Their frequencies can differ. Mobile and desktop products may deploy to an app store but wait for review and user installation; regulated systems may remain continuously deliverable while requiring documented authorization. Coordinated launches may need marketing, support, or contractual timing.

```text
Code merged
    ↓
Artifact built and verified
    ↓
Artifact deployed
    ↓
Feature remains disabled
    ↓
Feature enabled later
    ↓
Release occurs
```

This is deployment before release. A **feature flag** controls availability; a **dark launch** exercises deployed code or infrastructure without broad exposure. Flags are not authorization and need ownership and removal.

## Risk, Frequency, and Confidence

Small batches reduce deployment and release risk because each change is easier to understand, verify, and reverse. Fast feedback loops raise release confidence. Automation does not remove coordination: a release still needs ownership, evidence, monitoring, and communication proportional to risk. A manual decision is neither required for the definition of delivery nor proof that the candidate is correct.

Deployment risk concerns changing a technical environment: startup failure, incompatible configuration, unavailable capacity, or broken dependencies. Release risk concerns user and business impact: misunderstood behavior, support load, compliance obligations, or a launch at the wrong time. A deployment can succeed technically while the release fails commercially or operationally. Conversely, a disabled feature can be safely deployed and observed before anyone receives it.

Release frequency and deployment frequency should therefore be measured separately. A team might deploy infrastructure daily but release a mobile version monthly, or deploy hidden code continuously and enable it for customers after acceptance. Release-on-demand means the system is ready when the authorized decision arrives; it does not require releasing every change immediately.

Regulated systems may require traceable evidence and separation of duties without abandoning small batches or automation. Desktop and mobile distribution also includes signing, store review, staged availability, client upgrade behavior, and support for older versions. These constraints change the path after build, not the core requirement to identify verified content.

## Existing Repository Evidence

- [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) is CI: quality checks, image build, scan, and local smoke test.
- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) performs delivery preparation and deployment on every `main` push. It publishes and deploys without a workflow approval or feature flag, then smoke-tests `/health`.
- [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) is release preparation/image publication, not application deployment.
- [KubeOps Argo CD](../../../Projects/2_project/kubeops-gitops/argocd/application.yaml) is manual GitOps deployment. No source proves a business release process.

## Common Mistakes

- Treating deployment and release as identical.
- Calling every pipeline continuous delivery.
- Assuming frequent deployment means continuous deployment.
- Releasing large batches because deployment is automated.
- Having no release owner or post-release verification.
- Treating approval as the definition of delivery.
- Assuming continuous deployment suits every product or regulation.

## Practical Exercise

Classify each real workflow as `CI`, `Delivery preparation`, `Deployment`, `Release automation`, or `Unknown or partial`. Record its trigger, artifact identity, environment action, manual decision, and verification. A workflow can have more than one classification. Do not edit it.

## Knowledge Check

1. How do deployment and release differ?
2. What distinguishes continuous delivery from continuous deployment?
3. How can code be deployed but unreleased?
4. Why do small batches reduce risk?
5. Is TaskOps CD proof that production is continuously deployed?

<details>
<summary>View answers</summary>

1. Deployment installs software; release makes it officially or functionally available.
2. Delivery keeps production deployment available on demand; deployment automatically sends qualifying changes to production.
3. Keep the behavior disabled with a release flag or dark launch.
4. Each change is easier to understand, observe, and recover.
5. The YAML shows automatic deployment intent on `main`; it cannot prove external settings, successful runs, or business release behavior.

</details>

## Navigation

- [Back to Continuous Delivery and Releases](../README.md)
- [Next: Release Pipeline Design and Release Candidates](../02-release-pipeline-design-and-release-candidates/)
- [Back to All Learning Materials](../../README.md)
