"""Tests for the /health probe endpoint."""

from __future__ import annotations

import sqlite3

from app import database


def test_health_returns_ok_json(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok", "database": "ok"}
    assert resp.content_type == "application/json"


def test_health_reports_unhealthy_when_db_fails(client, monkeypatch):
    """If the database connectivity check raises, /health returns 503."""

    def _boom() -> None:
        raise sqlite3.OperationalError("simulated database failure")

    monkeypatch.setattr(database, "ping_db", _boom)

    resp = client.get("/health")
    assert resp.status_code == 503
    assert resp.get_json() == {"status": "error", "database": "down"}
