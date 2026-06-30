# Architecture

TaskOps is a small Flask application organized with the **application-factory**
pattern and a strict separation between HTTP handling and data access.

## Component overview

```
app/
  __init__.py    create_app() factory: load config, configure stdout logging,
                 register the routes blueprint, register DB teardown, create
                 the schema on startup.
  config.py      Configuration read from environment variables. No secrets in
                 source. Provides Config.as_dict() for app.config.update().
  database.py    SQLite data layer. Request-scoped connection on Flask's `g`,
                 init_db(), and create/get/list/complete/delete helpers. All
                 statements use parameter placeholders.
  routes.py      Thin blueprint handlers. Parse input, validate, delegate to
                 the data layer, log events, render templates or JSON.
  templates/     Jinja templates: base, index, tasks, create_task.
  static/css/    Hand-written "ops console" stylesheet.
wsgi.py          Exposes `app` for gunicorn (wsgi:app).
```

## Request lifecycle

1. gunicorn (production) or the Flask dev server (local) loads `wsgi:app`,
   which calls `create_app()`.
2. `create_app()` loads config from the environment, sets up logging, registers
   the blueprint and the `close_db` teardown, and runs `init_db()` once inside
   an app context to ensure the schema exists.
3. Per request, a handler in `routes.py` obtains a connection via
   `database.get_db()`, which lazily opens a `sqlite3` connection and stores it
   on `g`. The connection uses `sqlite3.Row` for dict-like rows.
4. After the request, `close_db` (registered with `teardown_appcontext`) closes
   the connection.

## Data model

A single `tasks` table:

| Column         | Type    | Notes                                  |
| -------------- | ------- | -------------------------------------- |
| `id`           | INTEGER | primary key, autoincrement             |
| `title`        | TEXT    | not null                               |
| `description`  | TEXT    | not null, defaults to empty string     |
| `is_completed` | INTEGER | not null, defaults to 0 (0/1 flag)     |
| `created_at`   | TEXT    | not null, defaults to `datetime('now')`|

The schema is created with `CREATE TABLE IF NOT EXISTS`, so startup is
idempotent and safe to run from multiple gunicorn workers.

## Routes

| Method | Path                      | Purpose                                   |
| ------ | ------------------------- | ----------------------------------------- |
| GET    | `/`                       | Homepage / console landing                |
| GET    | `/tasks`                  | List tasks (newest first)                 |
| GET    | `/tasks/new`              | New-task form                             |
| POST   | `/tasks/new`              | Validate and create a task                |
| POST   | `/tasks/<id>/complete`    | Mark a task completed                     |
| POST   | `/tasks/<id>/delete`      | Delete a task (no-op if missing)          |
| GET    | `/health`                 | JSON `{"status":"ok","database":"ok"}` (503 if DB down) |

## Configuration

`config.py` reads:

- `FLASK_SECRET_KEY` — session signing key (dev fallback if unset).
- `DATABASE_PATH` — SQLite file path (default `taskops.db`).
- `MAX_TITLE_LENGTH` — integer, default 120.

The factory accepts a `test_config` mapping so tests can override values (for
example `DATABASE_PATH`) without touching the environment.

## Deployment topology

In production the published GHCR image runs as a container listening on 5000.
An nginx container (see `docker-compose.prod.yml` and `docker/nginx.conf`)
listens on port 80 and reverse-proxies all traffic to the app, with `/health`
passed through. The SQLite database persists on a named `/data` volume.

`scripts/deploy.sh` drives this same compose stack (app + nginx) on the server,
so the deploy, the health check, and the CD smoke test all agree on nginx /
port 80. The local dev stack (`docker-compose.yml`) is the only single-container
path and publishes the app directly on port 5000 without nginx.
