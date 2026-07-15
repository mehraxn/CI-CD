# CI/CD Glossary

Short definitions for terms used throughout these learning materials.

- **Agent:** A machine or process that executes pipeline work; often synonymous with runner.
- **Artifact:** A stored output produced by a build or pipeline job.
- **Artifact promotion:** Advancing the same verified artifact through successive environments.
- **Attestation:** Signed evidence describing how an artifact or action was produced.
- **Blue-green deployment:** A release method that switches traffic between two complete environments.
- **Build:** The process that converts source and dependencies into a testable or deployable output.
- **Cache:** Reusable intermediate data stored to speed up later work.
- **Canary deployment:** A rollout that exposes a new version to a small subset before expansion.
- **CI (continuous integration):** Frequently merging changes and validating them with automated checks.
- **Continuous delivery:** Keeping software in a releasable state while production deployment remains a decision.
- **Continuous deployment:** Automatically deploying every change that passes the required controls.
- **DAST:** Dynamic application security testing performed against a running application.
- **DAG:** A directed acyclic graph that represents job dependencies and possible parallel execution.
- **Deployment:** Installing or activating a software version in an environment.
- **DORA metrics:** Delivery-performance measures covering deployment frequency, lead time, change failure rate, and recovery time.
- **Environment:** A target context such as development, test, staging, or production.
- **Feature flag:** A runtime control that enables or disables behavior independently of deployment.
- **GitOps:** Operating declarative systems through version-controlled desired state and automated reconciliation.
- **Infrastructure as Code (IaC):** Managing infrastructure through versioned, machine-readable definitions.
- **Immutable artifact:** An artifact whose contents cannot change after publishing.
- **Job:** A group of steps executed together on a runner.
- **Lockfile:** A file recording exact resolved dependency versions.
- **Matrix build:** Repeated pipeline work across combinations such as versions or operating systems.
- **OIDC:** OpenID Connect, often used by pipelines to obtain short-lived cloud credentials.
- **Pipeline:** An automated sequence or graph that builds, verifies, and delivers changes.
- **Policy as Code:** Machine-enforceable policies stored and reviewed as code.
- **Progressive delivery:** Gradually increasing a release's exposure based on controls and observations.
- **Provenance:** Verifiable information about an artifact's source and production process.
- **Quality gate:** A required condition that must pass before work can proceed.
- **Registry:** A service that stores and distributes packages or container images.
- **Release:** A named, versioned set of changes made available for use or deployment.
- **Rollback:** Restoring a previously known-good version or state.
- **Roll-forward:** Recovering by deploying a new corrective version rather than reverting.
- **Runner:** The compute environment that receives and executes pipeline jobs.
- **SAST:** Static application security testing that analyzes source or compiled code without running the application.
- **SBOM:** A software bill of materials listing components included in a software product.
- **Secret:** Sensitive data, such as a token or password, requiring controlled storage and access.
- **Semantic versioning:** A versioning convention using major, minor, and patch numbers to communicate compatibility.
- **Stage:** A logical pipeline phase, often containing one or more jobs.
- **Step:** An individual command or action within a job.
- **Supply chain:** The tools, dependencies, processes, and systems used to produce and deliver software.
- **Trigger:** An event or schedule that starts a workflow or pipeline.
- **Workflow:** A platform-defined automated process made of one or more jobs.
- **Workflow as code:** Storing the automated process in version-controlled configuration.

## Navigation

- [Back to Learning Materials](./README.md)
