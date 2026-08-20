from typing import Any
from urllib.parse import urlparse


VALID_PROGRESS_STATUSES = {"Not Started", "In Progress", "Completed"}


class PersistenceError(RuntimeError):
    """Raised when TalentBridge data cannot be saved or loaded safely."""


def save_job_analysis(
    client: Any,
    user_id: str,
    target_career: str,
    match_result: dict,
) -> str:
    if not user_id:
        raise PersistenceError("A signed-in user is required.")

    comparison = match_result.get("job_comparison", {})
    payload = {
        "user_id": user_id,
        "target_career": target_career,
        "user_mode": match_result.get("user_mode", "Job Seeker"),
        "match_score": comparison.get("match_score", 0),
        "semantic_match_score": match_result.get("semantic_match_score", 0),
        "result_data": match_result,
    }

    response = client.table("job_analyses").insert(payload).execute()
    rows = getattr(response, "data", None) or []
    if not rows or not rows[0].get("id"):
        raise PersistenceError("The analysis could not be saved.")

    return str(rows[0]["id"])


def list_job_analyses(client: Any, user_id: str, limit: int = 10) -> list[dict]:
    if not user_id:
        return []

    safe_limit = min(max(int(limit), 1), 50)
    response = (
        client.table("job_analyses")
        .select(
            "id, target_career, user_mode, match_score, "
            "semantic_match_score, created_at"
        )
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(safe_limit)
        .execute()
    )
    return getattr(response, "data", None) or []


def load_job_analysis(client: Any, user_id: str, analysis_id: str) -> dict:
    response = (
        client.table("job_analyses")
        .select("id, target_career, result_data")
        .eq("user_id", user_id)
        .eq("id", analysis_id)
        .maybe_single()
        .execute()
    )
    row = getattr(response, "data", None)
    if not row or not row.get("result_data"):
        raise PersistenceError("The saved analysis was not found.")
    return row


def delete_job_analysis(client: Any, user_id: str, analysis_id: str) -> None:
    if not user_id or not analysis_id:
        raise PersistenceError("Choose a saved analysis first.")

    response = (
        client.table("job_analyses")
        .delete()
        .eq("user_id", user_id)
        .eq("id", analysis_id)
        .execute()
    )
    rows = getattr(response, "data", None) or []
    if not rows:
        raise PersistenceError("The saved analysis was not found or could not be deleted.")


def _validate_evidence_url(url: str) -> str:
    clean_url = url.strip()
    if not clean_url:
        return ""

    parsed = urlparse(clean_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise PersistenceError(
            "Portfolio evidence links must begin with http:// or https://."
        )
    return clean_url


def save_skill_progress(
    client: Any,
    user_id: str,
    analysis_id: str,
    evidence_links: dict[str, str],
    progress_statuses: dict[str, str],
) -> None:
    if not user_id or not analysis_id:
        raise PersistenceError("Save an analysis before saving skill progress.")

    rows = []
    for skill, status in progress_statuses.items():
        if status not in VALID_PROGRESS_STATUSES:
            raise PersistenceError(f"Invalid progress status for {skill}.")
        rows.append(
            {
                "analysis_id": analysis_id,
                "user_id": user_id,
                "skill": skill,
                "evidence_url": _validate_evidence_url(
                    evidence_links.get(skill, "")
                ),
                "status": status,
            }
        )

    if rows:
        (
            client.table("skill_progress")
            .upsert(rows, on_conflict="analysis_id,skill")
            .execute()
        )


def load_skill_progress(
    client: Any,
    user_id: str,
    analysis_id: str,
) -> dict[str, dict]:
    if not user_id or not analysis_id:
        return {}

    response = (
        client.table("skill_progress")
        .select("skill, evidence_url, status")
        .eq("user_id", user_id)
        .eq("analysis_id", analysis_id)
        .execute()
    )
    rows = getattr(response, "data", None) or []
    return {row["skill"]: row for row in rows}
