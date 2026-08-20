from dataclasses import dataclass
from typing import Any


DEFAULT_ROLE = "Job Seeker"
ALLOWED_ROLES = {"Admin", "Job Seeker", "HR / Recruiter", "Training Center"}


class AuthConfigurationError(RuntimeError):
    """Raised when Supabase authentication is not configured."""


class AuthenticationError(RuntimeError):
    """Raised when a user cannot be authenticated safely."""


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: str
    email: str
    display_name: str
    role: str


def create_auth_client(url: str, key: str) -> Any:
    if not url or not key:
        raise AuthConfigurationError(
            "Supabase URL and public client key must be configured."
        )

    # Import lazily so the core analysis engine and its tests do not require
    # Supabase unless authentication is actually used.
    from supabase import create_client

    return create_client(url, key)


def authenticate_user(client: Any, email: str, password: str) -> AuthenticatedUser:
    clean_email = email.strip().lower()
    if not clean_email or not password:
        raise AuthenticationError("Email and password are required.")

    response = client.auth.sign_in_with_password(
        {"email": clean_email, "password": password}
    )
    user = getattr(response, "user", None)
    session = getattr(response, "session", None)

    if user is None or session is None:
        raise AuthenticationError("The email or password is incorrect.")

    profile_response = (
        client.table("profiles")
        .select("display_name, role")
        .eq("user_id", user.id)
        .maybe_single()
        .execute()
    )
    profile = getattr(profile_response, "data", None) or {}
    role = profile.get("role", DEFAULT_ROLE)
    if role not in ALLOWED_ROLES:
        role = DEFAULT_ROLE

    fallback_name = clean_email.split("@", 1)[0]
    return AuthenticatedUser(
        user_id=str(user.id),
        email=getattr(user, "email", clean_email) or clean_email,
        display_name=profile.get("display_name") or fallback_name,
        role=role,
    )


def register_job_seeker(
    client: Any,
    email: str,
    password: str,
    display_name: str,
) -> bool:
    clean_email = email.strip().lower()
    clean_name = display_name.strip()

    if not clean_name or not clean_email or not password:
        raise AuthenticationError("Name, email, and password are required.")
    if len(password) < 8:
        raise AuthenticationError("Password must contain at least 8 characters.")

    response = client.auth.sign_up(
        {
            "email": clean_email,
            "password": password,
            "options": {"data": {"display_name": clean_name}},
        }
    )

    if getattr(response, "user", None) is None:
        raise AuthenticationError("The account could not be created.")

    # Supabase returns no session when email confirmation is required.
    return getattr(response, "session", None) is not None


def sign_out_user(client: Any) -> None:
    client.auth.sign_out()
