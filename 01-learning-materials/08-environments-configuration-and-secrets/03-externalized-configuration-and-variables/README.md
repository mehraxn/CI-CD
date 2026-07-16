# Externalized Configuration and Variables

## Configuration Lives Outside the Artifact

**Externalized configuration** keeps environment-varying values out of the application artifact, supplied instead through **environment variables**, **configuration files**, or **command-line arguments**, with sensible **application defaults** for optional values. When configuration is external, one artifact serves every environment; when it is baked in, every environment needs its own build — which is why rebuilding for ordinary environment-specific values weakens build-once-deploy-many.

Timing matters as much as location:

```text
Build-time configuration:
Changes what is built.

Deployment-time configuration:
Changes how the artifact is deployed.

Runtime configuration:
Changes application behavior while running.
```

Most environment differences belong at deployment or runtime. Build-time configuration is legitimate for what genuinely changes the artifact (target platform, bundled assets) — not for a database URL. Further along this axis sit **feature flags** (runtime switches independent of deployment) and **remote configuration** services (values fetched while running, enabling **reload without redeploy**).

## Reading Configuration in an Application

```python
import os

database_url = os.environ["DATABASE_URL"]
log_level = os.getenv("LOG_LEVEL", "INFO")
```

Two idioms with different semantics: the first makes `DATABASE_URL` **required** — the application fails at startup if it is missing (good: fail fast and loud); the second gives `LOG_LEVEL` a **default** (good for genuinely optional values, dangerous when the default silently masks a missing required setting). A **configuration schema** — even an informal documented list of required/optional keys, types, and defaults — plus **startup validation** turns misconfiguration from a 2 a.m. mystery into an immediate, readable error.

## Where Values Come From, Per Layer

A conceptual GitHub Actions layer (workflow and job `env`, covered in [Topic 04](../../04-pipeline-as-code-and-platforms/03-variables-contexts-expressions-and-outputs/)):

```yaml
env:
  APPLICATION_NAME: task-api

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      LOG_LEVEL: INFO

    steps:
      - name: Display non-sensitive configuration
        run: echo "Deploying $APPLICATION_NAME with log level $LOG_LEVEL"
```

A Kubernetes **ConfigMap** (non-secret values mounted or injected as env):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: task-api-config
data:
  LOG_LEVEL: INFO
  FEATURE_TASK_EXPORT: "false"
```

The same role is played by **repository/organization variables** in CI platforms, **Docker Compose environment blocks**, **Helm values** files, **Terraform variables**, and **Ansible variables/inventory** — different carriers, one principle: named, versioned, reviewable values separated from code, with **sensitive values excluded** (those are Secrets, next lesson).

Scope limits where a value applies. An organization variable may supply a shared non-secret default; a repository variable narrows it to one project; an environment-scoped value can vary between staging and production; workflow, job, and step scopes narrow visibility inside a run. Broader scope is convenient but increases the number of consumers affected by a mistaken change. Secrets should use their dedicated mechanism rather than ordinary variables at any scope.

**Configuration templates** such as `.env.example` document required keys without carrying deployment values. Helm values and Terraform variable files can be versioned declarations, while generated configuration files should retain a clear source template and validation step. Ansible variables may live in inventory, group variables, or encrypted vault data depending on sensitivity. The carrier changes; the need for review, validation, ownership, and a documented consumer does not.

**Precedence** — which source wins when several define the same key — depends on the application and platform. The only universal rule: **document the precedence explicitly**; undocumented precedence is where "works in staging, broken in prod" bugs live. Configuration also deserves **versioning** (files in Git, reviewed like code) and **ownership** — stale keys nobody dares delete are drift in waiting.

Reload behavior is part of the contract. Some applications read values once at startup and require a restart; others watch a mounted file or remote service and reload. Dynamic reload needs validation and rollback just as deployment does: accepting an invalid value live can be faster—and more dangerous—than shipping a bad build.

## Common Mistakes

- Hard-coded environment URLs in application code.
- Secret values in ConfigMaps.
- Rebuilding the artifact for each environment.
- Different variable names in every environment (`DB_URL` here, `DATABASE_URI` there).
- Undocumented defaults.
- Missing startup validation.
- Printing every variable to logs (config next to secrets leaks).
- Mixing feature flags and secrets in one mechanism.
- Configuration without an owner.
- Stale configuration keys living forever.

## Existing Repository Evidence

This is the repository's richest topic, with real examples of nearly every mechanism:

- **Documented env templates**: TaskOps [.env.example](../../../Projects/1_project/taskops-cicd/.env.example) and KubeOps [.env.example](../../../Projects/2_project/kubeops-gitops/.env.example) — each key commented with purpose and allowed values, real values kept out of Git.
- **Compose with defaults and required values**: [docker-compose.prod.yml](../../../Projects/1_project/taskops-cicd/docker-compose.prod.yml) uses `${MAX_TITLE_LENGTH:-120}` (default) and `${FLASK_SECRET_KEY:?FLASK_SECRET_KEY is required}` — **deployment-time validation** that aborts on a missing secret, the fail-fast idiom in Compose syntax.
- **ConfigMap + envFrom**: KubeOps' [configmap.yaml](../../../Projects/2_project/kubeops-gitops/k8s/configmap.yaml) (`APP_ENV`, `LOG_LEVEL`) is injected via `envFrom` in the [deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml), alongside a secretRef — config and secrets cleanly split.
- **Helm values as environment configuration**: [values.yaml / values-dev / values-prod](../../../Projects/2_project/kubeops-gitops/helm/kubeops/) — the chart's `env:` block renders into the ConfigMap; identical keys, per-environment values.
- **Terraform variables with real validation blocks**: [variables.tf](../../../Projects/3_project/terraform/variables.tf) validates non-empty names, port ranges, and required ports — declarative configuration validation.
- **Ansible inventory variables**: [inventory.example.ini](../../../Projects/3_project/ansible/inventory.example.ini) (`monitoring_allowed_cidr`, connection settings).
- **`$GITHUB_ENV`**: TaskOps CD computes `IMAGE` at runtime and passes deployment-time configuration (`IMAGE_TAG`, `HTTP_PORT`, `MAX_TITLE_LENGTH`) to the server over SSH `envs`.
- Repository/organization variables (`vars` context) and remote-config/feature-flag services are not demonstrated.

## Practical Exercise

Build a configuration map for TaskOps across all its carriers (`.env.example`, `docker-compose.prod.yml`, `cd.yml`, the Dockerfile's `ENV` defaults):

```text
Configuration name
Location
Scope
Default
Sensitive or non-sensitive
Consumer
Validation
```

Cover at least `FLASK_SECRET_KEY`, `DATABASE_PATH`, `MAX_TITLE_LENGTH`, `HTTP_PORT`, `IMAGE`, and `IMAGE_TAG`. Note where the same key appears in multiple layers and which layer wins (and whether that precedence is documented). Do not expose secret values. Target 25–35 minutes.

## Knowledge Check

1. Why does baking a database URL into the artifact violate build-once-deploy-many?
2. When is build-time configuration legitimate?
3. What is the difference between `os.environ["X"]` and `os.getenv("X", default)` in failure behavior?
4. What real deployment-time validation does TaskOps' production Compose file perform?
5. Where do KubeOps' non-secret values live, and how do they reach the container?
6. Why must configuration precedence be documented?

<details>
<summary>View answers</summary>

1. The artifact then differs per environment, so each environment needs its own build and staging no longer validates production's bytes.
2. For values that genuinely change what is built — target platform, bundled assets — not for environment addresses or tunables.
3. The first fails fast at startup if the variable is missing (required); the second silently uses the default (optional — or a masked bug if the value was actually required).
4. `${FLASK_SECRET_KEY:?...}` aborts the stack if the secret is unset or empty — a required-value check at deployment time.
5. In a ConfigMap (rendered from Helm `env:` values), injected into the pod via `envFrom` with a configMapRef.
6. When several layers define the same key, the winner determines behavior; undocumented precedence makes environment-specific bugs undiagnosable.

</details>

## Navigation

- [Back to Environments, Configuration, and Secrets](../README.md)
- [Previous: Preview and Ephemeral Environments](../02-preview-and-ephemeral-environments/)
- [Next: Secrets Management and Injection](../04-secrets-management-and-injection/)
- [Back to All Learning Materials](../../README.md)
