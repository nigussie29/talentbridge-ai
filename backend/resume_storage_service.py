import hashlib
import re
from pathlib import Path
from typing import Any
from uuid import uuid4


RESUME_BUCKET = "resumes"
MAX_RESUME_BYTES = 5 * 1024 * 1024


class ResumeStorageError(RuntimeError):
    """Raised when a private resume cannot be saved or loaded safely."""


def _validate_pdf(file_name: str, file_bytes: bytes) -> tuple[str, bytes]:
    safe_name = Path(file_name or "resume.pdf").name.strip()
    if not safe_name.lower().endswith(".pdf"):
        raise ResumeStorageError("Only PDF resumes can be stored.")
    if not file_bytes:
        raise ResumeStorageError("The selected PDF is empty.")
    if len(file_bytes) > MAX_RESUME_BYTES:
        raise ResumeStorageError("Resume PDFs must be 5 MB or smaller.")
    if not file_bytes.startswith(b"%PDF-"):
        raise ResumeStorageError("The selected file is not a valid PDF.")

    clean_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(safe_name).stem)
    clean_stem = clean_stem.strip("-._") or "resume"
    return f"{clean_stem[:80]}.pdf", file_bytes


def save_resume(
    client: Any,
    user_id: str,
    file_name: str,
    file_bytes: bytes,
) -> dict:
    if not user_id:
        raise ResumeStorageError("A signed-in user is required.")

    clean_name, clean_bytes = _validate_pdf(file_name, file_bytes)
    content_hash = hashlib.sha256(clean_bytes).hexdigest()

    existing_response = (
        client.table("resume_documents")
        .select("id, original_name, storage_path, byte_size, created_at")
        .eq("user_id", user_id)
        .eq("content_sha256", content_hash)
        .maybe_single()
        .execute()
    )
    existing = getattr(existing_response, "data", None)
    if existing:
        return {**existing, "already_exists": True}

    storage_path = f"{user_id}/{uuid4()}-{clean_name}"
    bucket = client.storage.from_(RESUME_BUCKET)
    bucket.upload(
        path=storage_path,
        file=clean_bytes,
        file_options={
            "content-type": "application/pdf",
            "cache-control": "3600",
            "upsert": "false",
        },
    )

    try:
        response = (
            client.table("resume_documents")
            .insert(
                {
                    "user_id": user_id,
                    "original_name": clean_name,
                    "storage_path": storage_path,
                    "byte_size": len(clean_bytes),
                    "content_sha256": content_hash,
                }
            )
            .execute()
        )
        rows = getattr(response, "data", None) or []
        if not rows or not rows[0].get("id"):
            raise ResumeStorageError("The resume metadata could not be saved.")
    except Exception as error:
        try:
            bucket.remove([storage_path])
        except Exception:
            pass
        if isinstance(error, ResumeStorageError):
            raise
        raise ResumeStorageError("The resume could not be saved.") from error

    return {**rows[0], "already_exists": False}


def list_resumes(client: Any, user_id: str, limit: int = 20) -> list[dict]:
    if not user_id:
        return []

    safe_limit = min(max(int(limit), 1), 50)
    response = (
        client.table("resume_documents")
        .select("id, original_name, byte_size, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(safe_limit)
        .execute()
    )
    return getattr(response, "data", None) or []


def load_resume(client: Any, user_id: str, resume_id: str) -> tuple[dict, bytes]:
    if not user_id or not resume_id:
        raise ResumeStorageError("Choose a saved resume first.")

    response = (
        client.table("resume_documents")
        .select("id, original_name, storage_path, byte_size, created_at")
        .eq("user_id", user_id)
        .eq("id", resume_id)
        .maybe_single()
        .execute()
    )
    record = getattr(response, "data", None)
    if not record or not record.get("storage_path"):
        raise ResumeStorageError("The saved resume was not found.")

    file_bytes = client.storage.from_(RESUME_BUCKET).download(record["storage_path"])
    if not file_bytes:
        raise ResumeStorageError("The saved resume file could not be downloaded.")
    return record, file_bytes
