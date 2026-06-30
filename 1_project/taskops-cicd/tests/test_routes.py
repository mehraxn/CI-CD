"""Tests for the HTTP route handlers."""

from __future__ import annotations

from app import database


def _create_task(client, app, title, description=""):
    """Create a task via the route and return its real database id.

    Avoids assuming an autoincrement id of 1 — the create→fetch-id→act pattern
    keeps tests robust even if ordering or fixtures change.
    """
    client.post("/tasks/new", data={"title": title, "description": description})
    with app.app_context():
        rows = database.get_tasks()
    # get_tasks() returns newest first, so the just-created task is first.
    return rows[0]["id"]


def test_homepage_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_task_list_loads(client):
    resp = client.get("/tasks")
    assert resp.status_code == 200


def test_create_page_loads(client):
    resp = client.get("/tasks/new")
    assert resp.status_code == 200


def test_create_valid_task(client):
    resp = client.post(
        "/tasks/new",
        data={"title": "Ship pipeline", "description": "wire up CI"},
        follow_redirects=True,
    )
    assert resp.status_code == 200


def test_created_task_appears_in_list(client):
    client.post("/tasks/new", data={"title": "Visible task"})
    resp = client.get("/tasks")
    assert b"Visible task" in resp.data


def test_create_stores_data_correctly(client, app):
    """A created task is persisted with the exact title and description."""
    task_id = _create_task(client, app, "Write docs", "cover the data layer")
    with app.app_context():
        task = database.get_task(task_id)
    assert task is not None
    assert task["title"] == "Write docs"
    assert task["description"] == "cover the data layer"
    assert task["is_completed"] == 0


def test_empty_title_rejected(client, app):
    resp = client.post("/tasks/new", data={"title": "", "description": "x"})
    assert resp.status_code == 400
    assert b"Title is required" in resp.data
    # Nothing should have been stored.
    with app.app_context():
        assert database.get_tasks() == []


def test_whitespace_title_rejected(client, app):
    resp = client.post("/tasks/new", data={"title": "    "})
    assert resp.status_code == 400
    assert b"Title is required" in resp.data
    with app.app_context():
        assert database.get_tasks() == []


def test_over_max_length_title_rejected(client, app):
    resp = client.post("/tasks/new", data={"title": "a" * 121})
    assert resp.status_code == 400
    assert b"characters or fewer" in resp.data
    with app.app_context():
        assert database.get_tasks() == []


def test_max_length_title_accepted(client, app):
    """A title at exactly the limit (120) is allowed."""
    task_id = _create_task(client, app, "a" * 120)
    with app.app_context():
        assert database.get_task(task_id) is not None


def test_complete_changes_status_in_database(client, app):
    """Completing a task via the route flips is_completed in the database."""
    task_id = _create_task(client, app, "finish me")
    client.post(f"/tasks/{task_id}/complete")
    with app.app_context():
        task = database.get_task(task_id)
    assert task is not None
    assert task["is_completed"] == 1


def test_delete_removes_correct_task(client, app):
    """Deleting one task must remove only that task and leave others intact."""
    _create_task(client, app, "keep-A")
    target_id = _create_task(client, app, "delete-B")
    _create_task(client, app, "keep-C")

    client.post(f"/tasks/{target_id}/delete")

    with app.app_context():
        titles = {t["title"] for t in database.get_tasks()}
    assert titles == {"keep-A", "keep-C"}


def test_complete_missing_task_does_not_error(client):
    resp = client.post("/tasks/999999/complete", follow_redirects=True)
    assert resp.status_code == 200


def test_delete_missing_task_does_not_error(client):
    resp = client.post("/tasks/999999/delete", follow_redirects=True)
    assert resp.status_code == 200


def test_invalid_task_id_is_not_found(client):
    """A non-integer task id does not match the <int> route and 404s cleanly."""
    assert client.post("/tasks/not-a-number/complete").status_code == 404
    assert client.post("/tasks/not-a-number/delete").status_code == 404
