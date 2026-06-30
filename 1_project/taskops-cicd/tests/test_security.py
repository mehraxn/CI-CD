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
