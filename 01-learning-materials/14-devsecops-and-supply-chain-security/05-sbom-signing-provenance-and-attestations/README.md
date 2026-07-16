# SBOM, Signing, Provenance, and Attestations

## Evidence, Not Just Artifacts

Scanning asks "is this artifact vulnerable?" Supply-chain evidence asks harder questions: *what is in it, who built it, from what, and can I verify any of that?* Four instruments, four different answers:

```text
SBOM:
An inventory describing components included in software.

Signature:
Cryptographic evidence that an identity signed specific content.

Provenance:
Information about how, where, and from which inputs an artifact was built.

Attestation:
A signed or verifiable statement about an artifact or process.
```

## SBOMs

A **Software Bill of Materials** lists every component — packages, versions, ideally **dependency relationships** and identifiers like **Package URLs** — in a standard format: **SPDX** or **CycloneDX**. Generated at build time (Syft and Trivy can both produce them), stored and **attached** to the artifact (OCI registries can hold SBOMs beside images), an SBOM makes two things possible later: **vulnerability matching** against *tomorrow's* advisories without rebuilding ("which deployed images contain the newly-vulnerable package?" — the question every team asked during Log4Shell), and **license inventory**. **Freshness** matters — an SBOM describes the artifact it was generated from, so it must be regenerated per build and kept with the release.

## Signing

A **signature** binds an identity to exact content. Classic **key-based signing** requires protecting a long-lived private key (never as a plain repository variable). **Keyless signing** — the Sigstore/**Cosign** approach — replaces stored keys with workload identity: the build proves who it is (OIDC, as in [Topic 08](../../08-environments-configuration-and-secrets/05-oidc-workload-identity-and-short-lived-credentials/)), receives a short-lived **certificate**, signs, and the event lands in a public **transparency log** anyone can audit. Either way, the signature covers a **digest** — signing a mutable tag is meaningless, because the tag can point elsewhere tomorrow.

## Provenance and Attestations

**Build provenance** records the build's facts: **builder identity** (which workflow, which system), **source revision**, **build inputs**, parameters. An **attestation** packages any such claim as a verifiable **statement** (subject = artifact digest, **predicate** = the claim) signed by the maker. **SLSA** is the maturity framework for this space — levels describing how tamper-resistant the build and its evidence are; **in-toto** is the underlying attestation format family. At beginner level, the point is the chain:

```text
Source revision
      ↓
Trusted build workflow
      ↓
Artifact digest
      ↓
SBOM and provenance generated
      ↓
Artifact and statements signed
      ↓
Deployment verifies required evidence
```

**Verification** is where value materializes: a deployment policy that requires "signed by our CI's identity, provenance shows our repository and a protected branch" turns the evidence into a gate. Without verification, evidence is decoration. And the fine print: an SBOM does not prove components are secure; a signature does not prove the signer's *process* was secure; provenance quality depends on the build system; attestations must reference the exact **digest**; and the metadata itself must be protected from substitution.

A complete release bundle (extending [Topic 07's](../../07-artifacts-packages-and-registries/06-immutability-promotion-and-release-bundles/)):

```text
Release 1.4.0
├── Container-image digest
├── SPDX or CycloneDX SBOM
├── Provenance statement
├── Signature
├── Test evidence
└── Security-scan report
```

## Common Mistakes

- Generating an SBOM for the wrong artifact (source tree instead of the built image).
- SBOM not retained with the release.
- Signature verification absent — signing without checking.
- Trusting any signer instead of a defined identity set.
- Signing a mutable tag instead of a content digest.
- Private key stored as a normal repository variable.
- Provenance containing incorrect source identity.
- Treating SLSA as a product or scanner rather than a framework.
- Attestations never checked before deployment.
- Production release metadata generated from developer laptops.

## Existing Repository Evidence

**None of this layer is implemented**: no SBOM generation, no signing, no provenance, no attestations exist in any workflow — all examples in this lesson are conceptual, and this is stated plainly rather than implied otherwise. What the repository does provide are the *prerequisites* the evidence layer would build on: immutable-ish identities (commit-SHA image tags in [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) and [KubeOps image-release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml)), a trusted-builder candidate (GitHub-hosted workflows building from `main` only), scan reports that currently vanish with the job logs (retention gap noted in Topic 04's scanning lesson), and Trivy — which could generate SBOMs with a mode change. Implementation may arrive in a later project-enhancement phase; nothing should be created now.

## Practical Exercise

Design (on paper) the evidence bundle for a KubeOps release:

1. Subject: which artifact identity would every statement reference, given what image-release produces today?
2. SBOM: which tool (already in the workflows) could generate it, at which step, and where would it be stored?
3. Signing: keyless or key-based for this repository, and why? Which identity should the verification policy trust?
4. Provenance: list five facts the statement must contain, and which `github` context values would populate them.
5. Verification: at which point in the current KubeOps delivery flow (image-release → values-prod → Argo CD) could verification actually be enforced, and what is the honest answer if nothing verifies?

Do not create any workflow or signing configuration. Target 25–35 minutes.

## Knowledge Check

1. What different questions do an SBOM, a signature, and provenance answer?
2. Why must signatures and attestations reference a digest rather than a tag?
3. What made SBOMs valuable during incidents like Log4Shell?
4. What does keyless signing replace, and with what?
5. Why is unverified signing near-worthless?
6. What is SLSA?

<details>
<summary>View answers</summary>

1. SBOM: what is inside. Signature: who vouches for exactly this content. Provenance: how, where, and from which inputs it was built.
2. Tags are mutable pointers; a digest identifies exact bytes, so only digest-referenced statements are tamper-evident.
3. Teams could query stored inventories to find every affected artifact immediately, without rebuilding or rescanning everything.
4. Long-lived stored private keys — replaced by short-lived certificates issued against the build's OIDC identity, logged in a transparency log.
5. Evidence that no policy checks is decoration; the gate exists only when deployment verifies required identities and claims.
6. A framework of maturity levels for build and supply-chain integrity — guidance for how tamper-resistant the build process and its evidence are, not a tool.

</details>

## Navigation

- [Back to DevSecOps and Supply-Chain Security](../README.md)
- [Previous: Container, Kubernetes, and IaC Security Scanning](../04-container-kubernetes-and-iac-security-scanning/)
- [Next: Secure Pipelines, Permissions, Actions, and Runners](../06-secure-pipelines-permissions-actions-and-runners/)
- [Back to All Learning Materials](../../README.md)
