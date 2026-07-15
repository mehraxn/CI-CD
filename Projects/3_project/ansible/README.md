# Ansible Server Configuration

This directory demonstrates how Ansible would configure a Linux server after Terraform creates it. The example targets Ubuntu or Debian systems that use `apt` and systemd.

No real server, private key, password, or cloud credential is included.

## What the automation does

The main `site.yml` playbook applies four small roles in order:

1. `common` installs basic packages and enables the UFW host firewall.
2. `app` creates the `cloudops` service account, copies the Flask source, builds its Docker image, and manages the container with systemd.
3. `nginx` installs a reverse proxy that forwards HTTP traffic to the application on `127.0.0.1:8000`.
4. `monitoring` installs Docker Compose and starts Prometheus and Grafana on a shared Docker network.

The application port `8000` is bound only to localhost. Public web traffic enters through Nginx on port `80`. Port `443` is reserved for a future TLS configuration.

## Inventory placeholders

Copy the example inventory before using it:

```bash
cp inventory.example.ini inventory.ini
```

Replace these documentation values in `inventory.ini`:

- `203.0.113.20` with the server public IP produced by Terraform;
- `ubuntu` with the server's SSH user if different;
- `203.0.113.10/32` with the trusted administrator public IP that may access Prometheus and Grafana.

The example inventory intentionally does not reference a working private key. Use an SSH agent or pass an existing key at runtime. Never commit private keys.

## Validate the playbooks

Syntax validation does not connect to the placeholder server:

```bash
ansible-playbook -i inventory.example.ini site.yml --syntax-check
ansible-playbook -i inventory.example.ini deploy_app.yml --syntax-check
ansible-playbook -i inventory.example.ini setup_monitoring.yml --syntax-check
```

## Run the automation

After updating `inventory.ini`, configure the entire server:

```bash
ansible-playbook -i inventory.ini site.yml
```

If the key is not loaded in an SSH agent, provide the path to a real key that already exists on your machine:

```bash
ansible-playbook -i inventory.ini site.yml --private-key ~/.ssh/id_ed25519
```

The application and monitoring parts can also be run separately:

```bash
ansible-playbook -i inventory.ini deploy_app.yml
ansible-playbook -i inventory.ini setup_monitoring.yml
```

## Expected services

| Component | Server port | Access |
| --- | --- | --- |
| SSH | `22` | Administration |
| Nginx HTTP | `80` | Public web traffic |
| HTTPS placeholder | `443` | Reserved for future TLS setup |
| Flask/Gunicorn | `8000` | Localhost and Docker network only |
| Prometheus | `9090` | Trusted administrator CIDR |
| Grafana | `3000` | Trusted administrator CIDR |

Keep the cloud-provider firewall from the Terraform design in addition to UFW. Docker manages its own network rules, so the provider firewall should remain the outer restriction for ports `9090` and `3000`.

## Production follow-ups

This is a portfolio skeleton. Before a real deployment:

- configure TLS certificates before serving traffic on port `443`;
- replace all TEST-NET addresses and placeholder values;
- store environment-specific values in encrypted variables or a secret manager;
- pin and regularly update container image versions;
- change Grafana's initial administrator password;
- test the playbooks against a disposable server before using production hosts.
