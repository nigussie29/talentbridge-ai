import hashlib
from typing import Any
from urllib.parse import urlparse


MAX_JOB_DESCRIPTION_CHARS = 50_000
MAX_JOB_TITLE_CHARS = 160
MAX_COMPANY_NAME_CHARS = 160
MAX_SOURCE_URL_CHARS = 2_048


class JobDescriptionStorageError(RuntimeError):
    """Raised when a private job description cannot be stored safely."""


def _clean_short_text(value: str, field_name: str, maximum: int) -> str:
    clean_value = " ".join((value or "").split())
    if len(clean_value) > maximum:
        raise JobDescriptionStorageError(
            f"{field_name} must be {maximum} characters or fewer."
        )
    return clean_value


def _validate_source_url(source_url: str) -> str:
    clean_url = (source_url or "").strip()
    if not clean_url:
        return ""
    if len(clean_url) > MAX_SOURCE_URL_CHARS:
        raise JobDescriptionStorageError("The source URL is too long.")

    parsed = urlparse(clean_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise JobDescriptionStorageError(
            "The source URL must begin with http:// or https://."
        )
    return clean_url


def _validate_job_description(
    job_title: str,
    company_name: str,
    source_url: str,
    description_text: str,
) -> dict:
    clean_title = _clean_short_text(
        job_title,
        "Job title",
        MAX_JOB_TITLE_CHARS,
    )
    if not clean_title:
        raise JobDescriptionStorageError("Enter a job title before saving.")

    clean_company = _clean_short_text(
        company_name,
        "Company name",
        MAX_COMPANY_NAME_CHARS,
    )
    clean_description = (description_text or "").strip()
    if not clean_description:
        raise JobDescriptionStorageError(
            "Paste a job description before saving."
        )
    if len(clean_description) > MAX_JOB_DESCRIPTION_CHARS:
        raise JobDescriptionStorageError(
            "Job descriptions must be 50,000 characters or fewer."
        )

    return {
        "job_title": clean_title,
        "company_name": clean_company,
        "source_url": _validate_source_url(source_url),
        "description_text": clean_description,
        "content_sha256": hashlib.sha256(
            clean_description.encode("utf-8")
        ).hexdigest(),
    }


def save_job_description(
    client: Any,
    user_id: str,
    job_title: str,
    company_name: str,
    source_url: str,
    description_text: str,
) -> dict:
    if not user_id:
        raise JobDescriptionStorageError("A signed-in user is required.")

    validated = _validate_job_description(
        job_title,
        company_name,
        source_url,
        description_text,
    )
    existing_response = (
        client.table("job_descriptions")
        .select(
            "id, job_title, company_name, source_url, description_text, "
            "created_at, updated_at"
        )
        .eq("user_id", user_id)
        .eq("content_sha256", validated["content_sha256"])
        .maybe_single()
        .execute()
    )
    existing = getattr(existing_response, "data", None)
    if existing:
        return {**existing, "already_exists": True}

    response = (
        client.table("job_descriptions")
        .insert({"user_id": user_id, **validated})
        .execute()
    )
    rows = getattr(response, "data", None) or []
    if not rows or not rows[0].get("id"):
        raise JobDescriptionStorageError(
            "The job description could not be saved."
        )
    return {**rows[0], "already_exists": False}


def list_job_descriptions(
    client: Any,
    user_id: str,
    limit: int = 30,
) -> list[dict]:
    if not user_id:
        return []

    safe_limit = min(max(int(limit), 1), 50)
    response = (
        client.table("job_descriptions")
        .select(
            "id, job_title, company_name, source_url, created_at, updated_at"
        )
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .limit(safe_limit)
        .execute()
    )
    return getattr(response, "data", None) or []


def load_job_description(
    client: Any,
    user_id: str,
    job_description_id: str,
) -> dict:
    if not user_id or not job_description_id:
        raise JobDescriptionStorageError(
            "Choose a saved job description first."
        )

    response = (
        client.table("job_descriptions")
        .select(
            "id, job_title, company_name, source_url, description_text, "
            "created_at, updated_at"
        )
        .eq("user_id", user_id)
        .eq("id", job_description_id)
        .maybe_single()
        .execute()
    )
    record = getattr(response, "data", None)
    if not record or not record.get("description_text"):
        raise JobDescriptionStorageError(
            "The saved job description was not found."
        )
    return record


def update_job_description(
    client: Any,
    user_id: str,
    job_description_id: str,
    job_title: str,
    company_name: str,
    source_url: str,
    description_text: str,
) -> dict:
    if not user_id or not job_description_id:
        raise JobDescriptionStorageError(
            "Load a saved job description before updating it."
        )

    validated = _validate_job_description(
        job_title,
        company_name,
        source_url,
        description_text,
    )
    response = (
        client.table("job_descriptions")
        .update(validated)
        .eq("user_id", user_id)
        .eq("id", job_description_id)
        .execute()
    )
    rows = getattr(response, "data", None) or []
    if not rows:
        raise JobDescriptionStorageError(
            "The saved job description was not found or could not be updated."
        )
    return rows[0]


def delete_job_description(
    client: Any,
    user_id: str,
    job_description_id: str,
) -> None:
    if not user_id or not job_description_id:
        raise JobDescriptionStorageError(
            "Choose a saved job description first."
        )

    response = (
        client.table("job_descriptions")
        .delete()
        .eq("user_id", user_id)
        .eq("id", job_description_id)
        .execute()
    )
    rows = getattr(response, "data", None) or []
    if not rows:
        raise JobDescriptionStorageError(
            "The saved job description was not found or could not be deleted."
        )
