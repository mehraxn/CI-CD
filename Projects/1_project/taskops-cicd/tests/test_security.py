"""Security-focused tests: output escaping of user-supplied content."""

from __future__ import annotations


def test_task_title_is_html_escaped(client):
    """A task title containing HTML must be escaped, not rendered as markup."""
    payload = "<script>alert('xss')</script>"
    client.post("/tasks/new", data={"title": payload})

    resp = client.get("/tasks")
    body = resp.data.decode()

    # The raw, executable tag must NOT appear...
    assert "<script>alert('xss')</script>" not in body
    # ...but its escaped form should, proving Jinja autoescaping is active.
    assert "&lt;script&gt;" in body


def test_task_description_is_html_escaped(client):
    """A task description containing HTML must also be escaped."""
    client.post(
        "/tasks/new",
        data={"title": "safe title", "description": "<img src=x onerror=alert(1)>"},
    )

    resp = client.get("/tasks")
    body = resp.data.decode()

    assert "<img src=x onerror=alert(1)>" not in body
    assert "&lt;img" in body


def test_post_without_csrf_token_is_rejected(client, app):
    """A POST missing the CSRF token must be rejected and store nothing."""
    from app import database

    resp = client.post("/tasks/new", data={"title": "forged"}, csrf=False)
    assert resp.status_code == 400
    with app.app_context():
        assert database.get_tasks() == []


def test_post_with_wrong_csrf_token_is_rejected(client, app):
    """A POST with an incorrect CSRF token must also be rejected."""
    from app import database

    resp = client.post(
        "/tasks/new",
        data={"title": "forged", "_csrf_token": "wrong-token"},
        csrf=False,
    )
    assert resp.status_code == 400
    with app.app_context():
        assert database.get_tasks() == []


def test_security_headers_present(client):
    """Every response carries the hardening headers."""
    resp = client.get("/")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["Referrer-Policy"] == "no-referrer"
    assert "default-src 'self'" in resp.headers["Content-Security-Policy"]


def test_rendered_form_contains_csrf_field(client):
    """The create-task form embeds the hidden CSRF input."""
    resp = client.get("/tasks/new")
    assert b'name="_csrf_token"' in resp.data
