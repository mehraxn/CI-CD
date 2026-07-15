# Terraform Infrastructure Skeleton

This directory describes the intended infrastructure for the CloudOps lab without creating paid cloud resources or requiring cloud credentials.

## What it models

The credential-free `terraform_data` resource records the plan for:

- one small Linux virtual machine;
- SSH access using a public key path;
- a requested public IP address;
- inbound TCP rules for SSH (`22`), HTTP (`80`), HTTPS (`443`), Prometheus (`9090`), and Grafana (`3000`);
- consistent project, environment, and ownership tags.

Ports `80` and `443` are public in the example. SSH and monitoring ports use the documentation-only CIDR `203.0.113.10/32`. Replace that CIDR with a trusted administrator IP before adapting the configuration for a real deployment.

## Why there is no cloud provider yet

Adding an AWS, DigitalOcean, or Hetzner resource would require provider credentials during planning or deployment. This skeleton instead uses Terraform's built-in `terraform_data` resource, so formatting, validation, and planning remain local and credential-free.

The `public_ip` output is intentionally `null` because no VM is created. When a provider is selected, point that output at the real VM or public-IP resource attribute.

## Local validation

Terraform 1.5 or newer is required. From this directory, run:

```bash
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
terraform plan -var-file=terraform.tfvars.example
```

The plan creates only a local `terraform_data` record. It does not contact a cloud API or incur cloud costs.

## Adapting to a cloud provider

Choose one provider and replace `terraform_data.infrastructure_plan` with its VM and firewall resources:

| Platform | VM resource | Firewall resource |
| --- | --- | --- |
| AWS | `aws_instance` | `aws_security_group` |
| DigitalOcean | `digitalocean_droplet` | `digitalocean_firewall` |
| Hetzner Cloud | `hcloud_server` | `hcloud_firewall` |

Then:

1. Add the selected provider to `providers.tf` with a pinned version constraint.
2. Map `linux_image`, `vm_size`, the SSH public key, firewall rules, and tags to provider resources.
3. Update the `public_ip` output to reference the VM's real public address.
4. Keep credentials outside the repository and provide them through the provider's supported environment variables or CI secret store.
5. Run `terraform fmt`, `terraform validate`, and review `terraform plan` before applying.

Do not commit `.tfvars` files containing environment-specific data, state files, private keys, tokens, or cloud credentials.
