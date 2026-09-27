"""Authentication helpers for the AROHAN Flask APIs.

The dashboard should send a Firebase ID token in ``Authorization: Bearer``.
Trusted local services may use ``AROHAN_API_KEY``. Anonymous access is only
available when explicitly enabled for a non-production development session.
"""

from __future__ import annotations

import hmac
import os
from functools import wraps
from typing import Callable, Iterable, Optional

try:
    from flask import jsonify, request
except ImportError:  # pragma: no cover
    jsonify = None
    request = None

try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth
except ImportError:  # pragma: no cover - exercised in minimal deployments
    firebase_admin = None
    firebase_auth = None


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _anonymous_allowed() -> bool:
    return _truthy(os.getenv("AROHAN_ALLOW_ANONYMOUS", "false")) and os.getenv(
        "APP_ENV", "development"
    ).lower() not in {"production", "prod"}


def _roles_from_env() -> set[str]:
    return {
        role.strip()
        for role in os.getenv("AROHAN_OPERATOR_ROLES", "admin,operator").split(",")
        if role.strip()
    }


def _verify_bearer(token: str) -> Optional[dict]:
    if not token or firebase_admin is None or firebase_auth is None:
        return None
    if not firebase_admin._apps:
        return None
    try:
        return firebase_auth.verify_id_token(token, check_revoked=True)
    except Exception:
        return None


def authenticate_request() -> Optional[dict]:
    """Return the authenticated principal, or ``None`` when authentication fails."""
    configured_key = os.getenv("AROHAN_API_KEY", "")
    presented_key = request.headers.get("X-AROHAN-API-Key", "")
    if configured_key and presented_key and hmac.compare_digest(
        presented_key.encode("utf-8"), configured_key.encode("utf-8")
    ):
        return {"uid": "service-api-key", "role": "service", "service": True}

    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        return None
    return _verify_bearer(token.strip())


def require_auth(roles: Optional[Iterable[str]] = None) -> Callable:
    """Protect a Flask route and optionally require one of the given roles."""
    allowed_roles = set(roles or ())

    def decorator(view: Callable) -> Callable:
        @wraps(view)
        def wrapped(*args, **kwargs):
            if _anonymous_allowed():
                request.environ["arohan.principal"] = {
                    "uid": "anonymous-development",
                    "role": "development",
                }
                return view(*args, **kwargs)

            principal = authenticate_request()
            if principal is None:
                return jsonify({"error": "authentication required"}), 401

            if allowed_roles and principal.get("role") == "service":
                # A configured service key is intentionally limited to routes
                # that explicitly include the service role.
                if "service" not in allowed_roles:
                    return jsonify({"error": "insufficient permissions"}), 403
            elif allowed_roles and principal.get("role") not in allowed_roles:
                return jsonify({"error": "insufficient permissions"}), 403

            request.environ["arohan.principal"] = principal
            return view(*args, **kwargs)

        return wrapped

    return decorator


def principal() -> dict:
    """Return the principal stored by :func:`require_auth` for the request."""
    return request.environ.get("arohan.principal", {})
