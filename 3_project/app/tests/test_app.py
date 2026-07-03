"""Tests for the Flask application's operational endpoints."""

import pytest

from app.main import APP_VERSION, app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_ready(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json() == {"ready": True}


def test_version(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert response.get_json() == {"version": APP_VERSION}
