"""Shared pytest fixtures."""

from __future__ import annotations

import os
import tempfile

import pytest
from flask.testing import FlaskClient

from app import create_app

# Deterministic token used by the test client. Tests that need to prove CSRF
# enforcement post with csrf=False (see CsrfClient below).
TEST_CSRF_TOKEN = "test-csrf-token"


class CsrfClient(FlaskClient):
    """Test client that injects the CSRF token into POSTs by default.

    Pass ``csrf=False`` to send a POST *without* the token, e.g. to assert
    that unprotected requests are rejected.
    """

    def post(self, *args, **kwargs):  # type: ignore[override]
        include_token = kwargs.pop("csrf", True)
        if include_token:
            data = kwargs.setdefault("data", {})
            if isinstance(data, dict):
                data.setdefault("_csrf_token", TEST_CSRF_TOKEN)
        return super().post(*args, **kwargs)


@pytest.fixture()
def app():
    """Create an app instance backed by a throwaway SQLite file."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    application = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": db_path,
            "SECRET_KEY": "test-secret",
        }
    )
    application.test_client_class = CsrfClient

    yield application

    os.unlink(db_path)
    # WAL mode leaves sidecar files next to the database; clean those too.
    for suffix in ("-wal", "-shm"):
        sidecar = db_path + suffix
        if os.path.exists(sidecar):
            os.unlink(sidecar)


@pytest.fixture()
def client(app):
    client = app.test_client()
    # Seed the session with the known token so default POSTs validate.
    with client.session_transaction() as sess:
        sess["_csrf_token"] = TEST_CSRF_TOKEN
    return client
