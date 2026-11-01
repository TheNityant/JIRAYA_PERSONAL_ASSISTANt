"""User-facing Google access guidance, never a substitute for Google authorization."""


def google_access_guidance(publishing_status: str) -> dict:
    messages = {
        "testing": (
            "Google connections are in testing. Use a Google account invited by the app owner. "
            "Creating a Jiraya account does not grant Google test access. "
            "Google test authorizations normally expire after seven days."
        ),
        "production": (
            "Choose the Google account you want to connect and approve the requested permissions. "
            "If Google blocks access, the app may need verification or your Workspace "
            "administrator may need to allow it."
        ),
        "unknown": (
            "Connect the Google account you want to use; it can differ from your Jiraya login. "
            "If Google says this app is being tested, only accounts invited by the app owner "
            "can connect until the app is published."
        ),
    }
    return {"publishing_status": publishing_status, "message": messages[publishing_status]}


def google_authorization_error(error: str) -> str:
    # Provider query parameters are untrusted. Do not echo arbitrary values or infer
    # that access_denied always means a test-user restriction: cancellation also uses it.
    return {
        "access_denied": (
            "Google access was declined or blocked. Retry if you cancelled. If Google says "
            "the app is being tested, ask the app owner for test access; a Jiraya account "
            "alone does not grant it."
        ),
        "admin_policy_enforced": (
            "Your Google Workspace administrator blocks this connection. Ask your "
            "administrator to allow Jiraya or connect an eligible personal Google account."
        ),
        "org_internal": (
            "This Google app only accepts accounts from its organization. The app owner "
            "must configure an External audience for people outside that organization."
        ),
        "redirect_uri_mismatch": (
            "The Google callback URL does not match the OAuth client. The app owner "
            "must correct the deployed callback configuration."
        ),
    }.get(error, "Google could not authorize this connection. Retry or contact the app owner.")
