# Artifacts, Packages, and Registries

## Overview

Runner workspaces are temporary: when a job ends, its files are gone. Anything a pipeline produces that matters afterward — a tested package, a container image, a security report — must be deliberately preserved somewhere outside the runner. This section covers where pipeline outputs live, how they are named and versioned, why released outputs must be immutable, how the same verified artifact is promoted through environments, and how storage is governed over time.

```text
Job output:
A small metadata value passed between jobs.

Artifact:
A preserved file or collection of files produced by a pipeline.

Package:
A distributable unit published in a package ecosystem.

Container image:
An OCI-compatible application filesystem and metadata bundle.

Registry:
A service that stores, versions, controls, and distributes packages or images.

Cache:
Recreatable data used mainly to accelerate later runs.
```

A container image can be treated as a deployable artifact — in this repository it is *the* deployable artifact — but not every artifact is a container image: test reports, coverage files, and archives are artifacts too.

## From Build to Deployment

```text
Source code
    ↓
Build and verification
    ↓
Versioned output
    ↓
Artifact or package storage
    ↓
Promotion through environments
    ↓
Production deployment
```

The chain matters because deployment should consume *exactly* what was verified. If the tested output is discarded and production is rebuilt from source, the verification applied to one set of bytes and production runs another. Preserved, immutable, well-named artifacts are what make "deploy what you tested" literally true.

## Lessons

| Number | Lesson | Main focus |
|---|---|---|
| 01 | [Artifacts, Caches, and Job Outputs](./01-artifacts-caches-and-job-outputs/) | Moving files and metadata between isolated jobs |
| 02 | [Package Formats and Release Assets](./02-package-formats-and-release-assets/) | How ecosystems package and distribute software |
| 03 | [Package Registries](./03-package-registries/) | Publishing, permissions, and registry risk |
| 04 | [Container and OCI Registries](./04-container-and-oci-registries/) | Images, tags, digests, and this repository's real registry |
| 05 | [Artifact Naming, Versioning, and Metadata](./05-artifact-naming-versioning-and-metadata/) | Names and metadata that support traceability |
| 06 | [Immutability, Promotion, and Release Bundles](./06-immutability-promotion-and-release-bundles/) | Build once, promote the same artifact |
| 07 | [Retention, Cleanup, Access, and Replication](./07-retention-cleanup-access-and-replication/) | Governing storage, permissions, and availability |

## Learning Objectives

After completing this section, the learner should be able to:

- choose correctly among outputs, artifacts, caches, and registries;
- read a container-image reference down to registry, namespace, tag, and digest;
- design traceable artifact names and metadata;
- explain build-once-deploy-many and artifact promotion;
- reason about retention, cleanup, access control, and replication; and
- map every concept onto this repository's real image-publishing workflows.

## Recommended Study Order

Follow the numbered order: mechanics first (what goes where), then formats and registries (how software is distributed), then identity and immutability (how outputs stay trustworthy), and finally lifecycle governance.

## Practical Project Connections

The repository's artifact story is container-centric, published to **GitHub Container Registry (GHCR)**:

- [TaskOps CD](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) builds, scans (Trivy, *before* pushing), and pushes `ghcr.io/<owner>/taskops` with a commit-SHA tag and `latest`, then deploys the SHA-tagged image.
- [KubeOps image release](../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) publishes `ghcr.io/<owner>/kubeops` the same way, and [values-prod.yaml](../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) consumes the GHCR image.
- No workflow currently uses pipeline artifacts (`actions/upload-artifact`), GitHub releases, language-package publishing, or Helm chart packaging — the [Helm chart](../../Projects/2_project/kubeops-gitops/helm/kubeops/) is consumed from Git by Argo CD, not from a registry.

## Completion Checklist

- [ ] I can classify any pipeline output as job output, artifact, cache, or registry content.
- [ ] I mapped a real GHCR image reference into its components.
- [ ] I can explain why both workflows tag with the commit SHA *and* `latest`.
- [ ] I designed a promotion path for one project.
- [ ] I proposed retention rules for this repository's outputs.
- [ ] I completed all exercises and knowledge checks.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Automated Testing and Quality](../06-automated-testing-and-quality/)
- [Next: Environments, Configuration, and Secrets](../08-environments-configuration-and-secrets/)
