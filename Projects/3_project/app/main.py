"""Small Flask application used by the DevOps lab."""

import os

from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest


APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

app = Flask(__name__)

REQUESTS_TOTAL = Counter(
    "cloudops_http_requests_total",
    "Total number of HTTP requests handled by the application.",
    ["method", "endpoint", "status"],
)


@app.after_request
def count_request(response):
    """Record one metric after each request has been handled."""
    REQUESTS_TOTAL.labels(
        method=request.method,
        endpoint=request.endpoint or "unknown",
        status=response.status_code,
    ).inc()
    return response


@app.get("/")
def index():
    return "Welcome to the CloudOps IaC & Observability Lab!"


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/ready")
def ready():
    return jsonify(ready=True)


@app.get("/version")
def version():
    return jsonify(version=APP_VERSION)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
