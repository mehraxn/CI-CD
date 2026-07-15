"""Security hardening: CSRF protection and security response headers.

Implemented with the standard library only (``secrets`` + ``hmac``) so the
runtime image gains no extra dependencies. The token is a per-session random
value; every state-changing (POST) request must echo it back in the
``_csrf_token`` form field, compared in constant time.
"""

from __future__ import annotations

import hmac
import secrets

from flask import Flask, Response, abort, request, session

CSRF_FIELD = "_csrf_token"

# Sent on every response. The app serves only same-origin CSS/JS and never
# needs to be framed, so the policy can be strict.
SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; base-uri 'self'; frame-ancestors 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
}


def generate_csrf_token() -> str:
    """Return the session's CSRF token, creating one on first use."""
    token = session.get(CSRF_FIELD)
    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_FIELD] = token
    return token


def _validate_csrf() -> None:
    """Reject POST requests whose form token does not match the session."""
    if request.method != "POST":
        return
    expected = session.get(CSRF_FIELD, "")
    supplied = request.form.get(CSRF_FIELD, "")
    if not expected or not hmac.compare_digest(supplied, expected):
        abort(400, description="CSRF token missing or invalid.")


def _apply_security_headers(response: Response) -> Response:
    for name, value in SECURITY_HEADERS.items():
        response.headers.setdefault(name, value)
    return response


def init_app(app: Flask) -> None:
    """Wire CSRF validation, the template helper, and response headers."""
    app.before_request(_validate_csrf)
    app.after_request(_apply_security_headers)
    # Templates render the token with {{ csrf_token() }}.
    app.jinja_env.globals["csrf_token"] = generate_csrf_token
