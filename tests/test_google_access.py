from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.integrations.google.access import google_authorization_error
from app.main import app
from app.services.connection_store import ConnectionStore
from app.services.runtime_state_store import RuntimeStateStore


@pytest.mark.parametrize("mode", ["unknown", "testing", "production"])
def test_catalog_guidance_does_not_change_connector_availability(monkeypatch, mode):
    settings = Settings(
        auth_required=False,
        google_oauth_client_id="client",
        google_oauth_client_secret="secret",
        token_encryption_key="configured",
        google_oauth_publishing_status=mode,
    )
    monkeypatch.setattr("app.routes.connections.get_settings", lambda: settings)
    with TestClient(app) as client:
        payload = client.get("/connections").json()
    assert payload["google_access"]["publishing_status"] == mode
    assert payload["google_access"]["message"]
    google = [c for c in payload["catalog"] if c["id"] in {"gmail", "google_calendar"}]
    assert all(c["status"] == "AVAILABLE" for c in google)
    assert "secret" not in str(payload)


@pytest.mark.parametrize("provider", ["google", "google_calendar"])
@pytest.mark.parametrize("error, expected", [
    ("access_denied", "declined or blocked"),
    ("admin_policy_enforced", "Workspace administrator"),
    ("org_internal", "External audience"),
    ("redirect_uri_mismatch", "callback URL"),
    ("untrusted-credential-looking-value", "could not authorize"),
])
def test_denial_uses_safe_guidance_and_consumes_state(provider, error, expected):
    from app.db import SessionLocal

    # Exercise the real callback/state path, never exchange a provider token.
    with TestClient(app) as client:
        with SessionLocal() as db:
            from app.config import get_settings

            settings = get_settings()
            store = ConnectionStore(db)
            store.ensure_user(user_id=settings.dev_user_id, email=settings.dev_user_email)
            state = store.create_oauth_state(user_id=settings.dev_user_id, provider=provider)
            nonce = state.state
            prefix = "oauth-google-pkce" if provider == "google" else "oauth-calendar-pkce"
            pkce_key = f"{prefix}:{nonce}"
            RuntimeStateStore(db).set(pkce_key, {"code_verifier": "private-verifier"})
        path = "/connections/google/callback" if provider == "google" else "/connections/google/calendar/callback"
        response = client.get(path, params={"state": nonce, "error": error}, follow_redirects=False)
        assert response.status_code == 302
        detail = parse_qs(urlparse(response.headers["location"]).query)["detail"][0]
        assert expected in detail
        assert "private-verifier" not in detail
        assert "untrusted-credential-looking-value" not in detail
        with SessionLocal() as db:
            assert RuntimeStateStore(db).get(pkce_key) is None
            assert ConnectionStore(db).consume_oauth_state(state=nonce, provider=provider) is None
            assert ConnectionStore(db).get_active(user_id=settings.dev_user_id, provider=provider) is None


def test_unknown_error_does_not_echo_provider_input():
    assert "sensitive" not in google_authorization_error("sensitive-data")
