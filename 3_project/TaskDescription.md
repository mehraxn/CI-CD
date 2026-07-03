# CloudOps — Infrastructure as Code, Server Automation & Observability Lab

## Project Overview

CloudOps is a junior DevOps portfolio project focused on **provisioning, configuring, monitoring, and operating a small cloud-based application environment**.

The goal of this project is not to build a complex web app. The app can be a simple Flask or FastAPI service. The main focus is the DevOps work around it:

* creating cloud infrastructure with Terraform,
* configuring Linux servers with Ansible,
* deploying the application behind Nginx,
* collecting metrics with Prometheus,
* visualizing system health in Grafana,
* setting basic alerts,
* creating backup and restore scripts,
* documenting troubleshooting and incident response steps.

This project simulates a real-world situation where a junior DevOps engineer is asked to take a small application and prepare a reliable cloud environment for it.

---

## Why This Project Is Valuable

Many beginner DevOps projects stop at Docker or Kubernetes. This project shows another important side of DevOps: **cloud infrastructure and operations**.

It demonstrates that the developer understands how to:

* create infrastructure in a repeatable way,
* avoid manual server setup,
* manage environment variables and secrets safely,
* monitor CPU, memory, disk, and application health,
* debug failed services,
* recover from basic incidents,
* document operational procedures clearly.

Together with the other two projects, this gives a strong junior DevOps portfolio:

1. **TaskOps CI/CD** — testing, Docker, GitHub Actions, security scanning, deployment.
2. **KubeOps GitOps** — Kubernetes, Helm, Argo CD, GitOps workflow.
3. **CloudOps IaC** — Terraform, Ansible, Linux server operations, monitoring, backup, incident response.

---

## Real-World Scenario

A small company has a simple internal API that needs to run on a cloud Linux server.

At first, the server is configured manually. Someone logs in with SSH, installs packages, edits Nginx files, starts the app manually, and hopes everything keeps working.

This project improves that situation by making the setup repeatable and documented.

The infrastructure is created with Terraform. The server is configured with Ansible. Monitoring is added with Prometheus and Grafana. Backup and restore scripts are included so the project looks more realistic from an operations point of view.

---

## Main Objective

Build a small cloud operations lab that answers this question:

> “How can I provision, configure, monitor, and maintain a small production-style server environment using DevOps practices?”

By the end of the project, the repository should show that the environment can be recreated from code, checked, monitored, and recovered using documented steps.

---

## Suggested Application

The application should be intentionally simple.

Example app idea:

**StatusBoard API**

A small Flask or FastAPI app with:

* `/` homepage,
* `/health` endpoint,
* `/ready` endpoint,
* `/version` endpoint,
* `/metrics` endpoint,
* simple SQLite or file-based status records.

The app is not the main focus. It exists so the infrastructure and monitoring have something realistic to run.

---

## Tech Stack

### Application

* Python
* Flask or FastAPI
* SQLite or simple JSON/file storage
* Gunicorn or Uvicorn
* Nginx reverse proxy

### Infrastructure

* Terraform
* AWS EC2, DigitalOcean Droplet, Hetzner VM, or local VM
* Security groups / firewall rules
* SSH key management
* Environment variables

### Configuration Management

* Ansible
* Linux package installation
* User creation
* Nginx configuration
* Systemd service setup
* App deployment
* Firewall configuration

### Monitoring & Observability

* Prometheus
* Node Exporter
* Grafana
* Basic alert rules
* Application health checks
* Optional: OpenTelemetry traces/logs

### Automation & Quality

* GitHub Actions
* `terraform fmt`
* `terraform validate`
* `ansible-lint`
* basic app tests
* security checks with Checkov or Trivy

---

## Core Features

### 1. Infrastructure as Code

Use Terraform to create the infrastructure.

Terraform should define:

* VM/server instance,
* network/firewall rules,
* SSH access,
* public IP output,
* required tags/names,
* optional DNS record.

The project should include:

* `main.tf`
* `variables.tf`
* `outputs.tf`
* `providers.tf`
* `terraform.tfvars.example`
* clear documentation for `terraform init`, `plan`, `apply`, and `destroy`.

Important: real secrets must not be committed.

---

### 2. Server Configuration with Ansible

Use Ansible to configure the server after Terraform creates it.

Ansible should install and configure:

* Python runtime,
* Docker or system packages,
* Nginx,
* application service,
* Prometheus Node Exporter,
* firewall rules,
* log directory,
* backup directory.

The Ansible playbook should be idempotent, meaning it can be run multiple times without breaking the server.

Example playbooks:

* `site.yml`
* `deploy_app.yml`
* `setup_monitoring.yml`
* `backup.yml`

---

### 3. Application Deployment

Deploy the app to the server using Ansible.

The app should run as a service, not by manually typing `python app.py`.

Use either:

* systemd service, or
* Docker Compose.

Recommended junior-friendly approach:

* Nginx listens on port 80,
* Nginx forwards traffic to the app on localhost,
* app runs with Gunicorn/Uvicorn,
* health check endpoint confirms the app is alive.

---

### 4. Monitoring Stack

Add a small monitoring setup.

Prometheus should scrape:

* the app `/metrics` endpoint,
* Node Exporter metrics from the server.

Grafana should show a basic dashboard with:

* CPU usage,
* memory usage,
* disk usage,
* app uptime,
* HTTP request count,
* error count,
* service restart count if available.

The repository should include:

* Prometheus config,
* Grafana dashboard JSON or screenshots,
* alert rule examples,
* monitoring documentation.

---

### 5. Alerts

Add basic alerting rules.

Example alerts:

* server CPU usage too high,
* disk space almost full,
* app health check failing,
* app service down,
* high HTTP 5xx errors.

For a portfolio project, the alert can log locally or be documented as a simulated Alertmanager setup. It does not need to send real production alerts.

---

### 6. Backup and Restore

Add backup and restore scripts.

Example:

* backup SQLite database,
* compress logs,
* store backups in a local backup folder,
* optional upload to S3-compatible storage,
* restore the latest backup.

Scripts:

* `scripts/backup.sh`
* `scripts/restore.sh`
* `scripts/list_backups.sh`

Documentation should explain:

* how to run a backup,
* how to restore after failure,
* what is included and not included.

---

### 7. Incident Response Runbooks

Create clear troubleshooting documentation.

Example runbooks:

* app is down,
* server is unreachable,
* Nginx returns 502,
* disk is full,
* deployment failed,
* Prometheus cannot scrape target,
* high memory usage.

Each runbook should include:

* symptoms,
* possible causes,
* commands to check,
* fix steps,
* prevention notes.

This is very good for a junior DevOps resume because it shows operational thinking, not only tool usage.

---

## Suggested Repository Structure

```text
cloudops-iac-observability/
│
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
│
├── terraform/
│   ├── main.tf
│   ├── providers.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
│
├── ansible/
│   ├── inventory.example.ini
│   ├── site.yml
│   ├── deploy_app.yml
│   ├── setup_monitoring.yml
│   └── roles/
│
├── monitoring/
│   ├── prometheus.yml
│   ├── alert_rules.yml
│   ├── grafana-dashboard.json
│   └── README.md
│
├── nginx/
│   └── app.conf
│
├── scripts/
│   ├── backup.sh
│   ├── restore.sh
│   ├── smoke_test.sh
│   └── check_server.sh
│
├── docs/
│   ├── architecture.md
│   ├── infrastructure.md
│   ├── ansible.md
│   ├── monitoring.md
│   ├── backup-restore.md
│   ├── security.md
│   └── runbooks/
│       ├── app-down.md
│       ├── nginx-502.md
│       ├── disk-full.md
│       └── deployment-failed.md
│
├── .github/
│   └── workflows/
│       ├── validate.yml
│       └── security.yml
│
├── README.md
└── LICENSE
```

---

## GitHub Actions Pipeline

The pipeline should not deploy automatically at first. For a junior portfolio, validation is enough.

On every push or pull request:

* run Python tests,
* run `terraform fmt -check`,
* run `terraform validate`,
* run `ansible-lint`,
* run security checks,
* check shell scripts with ShellCheck if possible.

Optional advanced step:

* manual workflow dispatch for deployment.

This keeps the project safe and honest.

---

## Security Requirements

The project should show good basic security habits:

* no real secrets committed,
* `.env.example` only,
* SSH key ignored,
* Terraform variable examples only,
* firewall allows only needed ports,
* app does not run as root if using Docker,
* Nginx hides unnecessary headers,
* backup files are not publicly exposed,
* documentation explains the limits clearly.

---

## Screenshots to Include

Add real screenshots after implementation.

Recommended screenshots:

* Terraform plan output,
* Terraform apply success,
* Ansible playbook success,
* application homepage,
* `/health` endpoint,
* Prometheus targets page,
* Grafana dashboard,
* alert rule page,
* backup script output,
* restore script output.

Do not fake screenshots.

---

## README Positioning

The README should be honest and say:

> This is a production-style DevOps portfolio project, not a full enterprise production system. It demonstrates Infrastructure as Code, configuration management, monitoring, backup/restore, and operational troubleshooting for a small application environment.

---

## Limitations

Be honest about limitations.

Example limitations:

* single-server setup, not high availability,
* no real production domain required,
* no advanced secret manager by default,
* no full disaster recovery across regions,
* alerting may be local or simulated,
* monitoring is basic but practical,
* cloud costs must be controlled carefully.

This honesty makes the project look stronger, not weaker.

---

## Future Improvements

Possible future improvements:

* add remote Terraform state,
* add S3-compatible backup storage,
* add TLS with Let’s Encrypt,
* add Alertmanager email/Slack notifications,
* add OpenTelemetry tracing,
* add log aggregation with Loki,
* add blue/green deployment,
* add multi-environment setup: dev and prod,
* add autoscaling if moved to Kubernetes later.

---

## Resume Bullet Points

* Built a cloud operations lab using Terraform and Ansible to provision and configure a Linux server environment for a Python web application.
* Automated server setup including Nginx reverse proxy, application service configuration, firewall rules, and monitoring agents.
* Implemented Prometheus and Grafana monitoring for system metrics, application health, and basic alerting scenarios.
* Created backup and restore scripts with documented recovery procedures for a small application database.
* Wrote operational runbooks for common incidents such as app downtime, Nginx 502 errors, disk pressure, and failed deployments.
* Added GitHub Actions validation for Terraform, Ansible, Python tests, and security checks.

---

## Final Project Goal

By the end of this project, the repository should clearly show that the developer can think like a junior DevOps engineer:

* automate infrastructure,
* configure servers properly,
* monitor services,
* troubleshoot incidents,
* manage backups,
* document operations,
* and avoid manual, fragile deployment steps.
