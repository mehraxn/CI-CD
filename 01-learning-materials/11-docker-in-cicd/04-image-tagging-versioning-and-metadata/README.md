# Image Tagging, Versioning, and Metadata

```text
ghcr.io/example/task-api:1.4.0
ghcr.io/example/task-api:sha-a1b2c3d
ghcr.io/example/task-api:latest
ghcr.io/example/task-api@sha256:<digest>
```

The parts are registry, namespace, repository, tag, or content-addressed digest. Tags are movable unless policy protects them. Normalize branch/PR tags to avoid invalid characters and collisions.

| Reference | Strength | Main limitation |
|-----------|----------|-----------------|
| `latest` | Easy | Mutable/weak alone |
| Semantic version | Clear release | Must prevent overwrite |
| Commit SHA | Source traceability | Less friendly |
| Digest | Exact content | Harder manually |

OCI labels can record title, description, source, revision, version, build date, license, docs URL, and build run. `docker/metadata-action` can generate normalized tags/labels but is absent here. TaskOps and KubeOps publish SHA plus `latest`; neither records digest or OCI labels. KubeOps production values use mutable `latest`.

## Practical Exercise

Audit real tags and propose semantic, SHA, PR, candidate, digest, and rollback identities without changing workflows.

## Knowledge Check

1. Are tags content? 2. Strongest exact identity? 3. Why sanitize branches? 4. What metadata is absent?

<details><summary>Answers</summary>

1. No, pointers. 2. Digest. 3. Validity/collision/security. 4. OCI labels and recorded digest.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Layers, Caching, and Multi-Stage Builds](../03-layers-caching-and-multi-stage-builds/)
- [Next: Docker Compose in Development and CI](../05-docker-compose-in-development-and-ci/)
- [Back to All Learning Materials](../../README.md)
