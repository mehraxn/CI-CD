"""SQLite data access layer for TaskOps.

This module is intentionally decoupled from the HTTP layer: it knows nothing
about requests or responses, only about connections and rows. Every statement
uses parameter placeholders -- user input is never concatenated into SQL.
"""

from __future__ import annotations

import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    description  TEXT    NOT NULL DEFAULT '',
    is_completed INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Covers the task-list query (ORDER BY created_at DESC, id DESC) so listing
-- stays an index scan instead of a sort as the table grows.
CREATE INDEX IF NOT EXISTS idx_tasks_created_at
    ON tasks (created_at DESC, id DESC);
"""


def get_db() -> sqlite3.Connection:
    """Return a request-scoped SQLite connection stored on Flask's ``g``."""
    if "db" not in g:
        conn = sqlite3.connect(
            current_app.config["DATABASE_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        # WAL lets readers proceed while a writer commits, and busy_timeout
        # makes concurrent writers wait instead of failing immediately with
        # "database is locked" -- essential once gunicorn runs >1 worker
        # against the same SQLite file.
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        # NORMAL is safe with WAL (no corruption on crash; at worst the last
        # transaction is lost) and avoids an fsync per commit.
        conn.execute("PRAGMA synchronous = NORMAL;")
        g.db = conn
    return g.db


def close_db(_exc: BaseException | None = None) -> None:
    """Close the request-scoped connection if one was opened."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Create the schema if it does not yet exist."""
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()


def ping_db() -> None:
    """Run a trivial query to confirm the database is reachable.

    Raises ``sqlite3.Error`` (or another exception) if the database cannot be
    queried; used by the /health endpoint as a readiness check.
    """
    get_db().execute("SELECT 1;").fetchone()


def create_task(title: str, description: str = "") -> int:
    """Insert a new task and return its id."""
    db = get_db()
    cur = db.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?);",
        (title, description),
    )
    db.commit()
    return int(cur.lastrowid)


def get_tasks() -> list[sqlite3.Row]:
    """Return all tasks, newest first."""
    db = get_db()
    cur = db.execute(
        "SELECT id, title, description, is_completed, created_at "
        "FROM tasks ORDER BY created_at DESC, id DESC;"
    )
    return cur.fetchall()


def get_task(task_id: int) -> sqlite3.Row | None:
    """Return a single task by id, or ``None`` if it does not exist."""
    db = get_db()
    cur = db.execute(
        "SELECT id, title, description, is_completed, created_at "
        "FROM tasks WHERE id = ?;",
        (task_id,),
    )
    return cur.fetchone()


def complete_task(task_id: int) -> int:
    """Mark a task completed. Returns the number of rows affected."""
    db = get_db()
    cur = db.execute(
        "UPDATE tasks SET is_completed = 1 WHERE id = ?;",
        (task_id,),
    )
    db.commit()
    return cur.rowcount


def delete_task(task_id: int) -> int:
    """Delete a task. Returns the number of rows affected (0 if missing)."""
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    db.commit()
    return cur.rowcount
