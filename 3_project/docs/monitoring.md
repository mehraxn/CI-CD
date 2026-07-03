# Monitoring the CloudOps Lab

This project uses Prometheus and Grafana to provide a simple monitoring setup for the Flask application.

## Prometheus

Prometheus collects and stores measurements called metrics. In this project, it requests the application's `/metrics` endpoint every 15 seconds and stores the returned values as time-series data.

The scrape configuration is in `monitoring/prometheus.yml`. It uses the Docker Compose service name and port `cloudops-app:8000` because containers communicate with each other through the Compose network.

## Grafana

Grafana displays monitoring data in dashboards and graphs. It can use Prometheus as a data source, allowing application metrics to be explored visually.

When adding the Prometheus data source in Grafana, use this URL:

```text
http://prometheus:9090
```

Grafana data is stored in the `grafana-data` Docker volume, so local configuration and dashboards remain available after the containers are restarted.

## Ports

| Service | Local URL | Purpose |
| --- | --- | --- |
| Flask application | `http://localhost:8000` | Runs the sample application and exposes its endpoints. |
| Prometheus | `http://localhost:9090` | Collects, stores, and queries metrics. |
| Grafana | `http://localhost:3000` | Displays metrics in dashboards. |

These ports are published to the local machine by `docker-compose.yml`.

## Start the monitoring stack

From the repository root, build the application image and start all services:

```bash
docker compose up --build -d
```

Check that the containers are running:

```bash
docker compose ps
```

To stop the stack:

```bash
docker compose down
```

## Check Prometheus targets

Open `http://localhost:9090/targets` in a browser. The `cloudops-app` target should have the state **UP**. This means Prometheus can connect to the application and collect its metrics.

If the target is down, check the container status and logs:

```bash
docker compose ps
docker compose logs cloudops-app prometheus
```

## Access Grafana

Open `http://localhost:3000` in a browser. For a new local Grafana instance, sign in with the initial username `admin` and password `admin`, then change the password when prompted.

Add Prometheus as a data source using `http://prometheus:9090`. The service name works from inside the Grafana container; `localhost` would refer to the Grafana container itself.

## The `/metrics` endpoint

The Flask application exposes Prometheus-compatible data at `http://localhost:8000/metrics`. Prometheus reads this endpoint automatically using the configured scrape interval.

The output includes standard Python process metrics and the custom `cloudops_http_requests_total` counter. The custom counter records requests by HTTP method, Flask endpoint, and response status. Prometheus stores these values so they can later be queried, graphed in Grafana, or used for alerts.

## Import the example dashboard

The repository includes a starter dashboard at `monitoring/grafana-dashboard.json`. It displays total HTTP requests, application uptime, request rate, and service health guidance.

Import it manually after Grafana and Prometheus are running:

1. Open `http://localhost:3000` and sign in to Grafana.
2. Confirm that a Prometheus data source exists with the URL `http://prometheus:9090`.
3. Open **Dashboards**, select **New**, and then select **Import**.
4. Upload `monitoring/grafana-dashboard.json`, or paste its JSON into the import form.
5. Select the Prometheus data source when Grafana asks for the `DS_PROMETHEUS` input.
6. Select **Import** to create the dashboard.

The request panels will remain empty until the application has received requests and Prometheus has completed at least one scrape. Generate a few requests by opening `http://localhost:8000` or `http://localhost:8000/health`, then wait for the next 15-second scrape.
