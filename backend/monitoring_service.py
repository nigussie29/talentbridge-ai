"""Privacy-safe production health checks and structured monitoring events."""

from datetime import datetime, timezone
from importlib.util import find_spec
import json
import logging
import re
import sys


LOGGER = logging.getLogger("talentbridge.monitoring")
SAFE_METRIC_FIELDS = {
    "check_count",
    "passed_count",
    "failed_count",
    "scenario_count",
    "completed_count",
    "average_rating",
}
REQUIRED_MODULES = (
    ("streamlit", "Application framework"),
    ("PyPDF2", "PDF processing"),
    ("pandas", "Data processing"),
    ("sklearn", "Semantic matching"),
    ("supabase", "Authentication and storage SDK"),
)


def _utc_timestamp(value=None):
    timestamp = value or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc).isoformat(timespec="seconds")


def build_health_report(configuration=None, module_checker=None, checked_at=None):
    """Return deployment diagnostics without returning any configured values."""
    configuration = configuration or {}
    module_checker = module_checker or (lambda name: find_spec(name) is not None)
    checks = []

    python_ready = sys.version_info >= (3, 11)
    checks.append(
        {
            "component": "Python runtime",
            "status": "Healthy" if python_ready else "Needs attention",
            "detail": (
                f"Python {sys.version_info.major}.{sys.version_info.minor} is supported."
                if python_ready
                else "Python 3.11 or newer is required."
            ),
        }
    )

    for module_name, component in REQUIRED_MODULES:
        installed = bool(module_checker(module_name))
        checks.append(
            {
                "component": component,
                "status": "Healthy" if installed else "Needs attention",
                "detail": (
                    "Required dependency is available."
                    if installed
                    else "Required dependency is unavailable."
                ),
            }
        )

    auth_ready = bool(configuration.get("supabase_url_configured")) and bool(
        configuration.get("supabase_key_configured")
    )
    checks.append(
        {
            "component": "Supabase configuration",
            "status": "Healthy" if auth_ready else "Needs attention",
            "detail": (
                "Authentication configuration is present."
                if auth_ready
                else "Authentication configuration is incomplete."
            ),
        }
    )

    passed_count = sum(check["status"] == "Healthy" for check in checks)
    total_count = len(checks)
    failed_count = total_count - passed_count
    return {
        "status": "Operational" if failed_count == 0 else "Degraded",
        "checked_at": _utc_timestamp(checked_at),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "total_count": total_count,
        "checks": checks,
        "privacy_note": (
            "This diagnostic reports component status only. It does not inspect or "
            "record résumés, job descriptions, account details, or secret values."
        ),
    }


def generate_health_report_text(report):
    """Create a downloadable, privacy-safe deployment health report."""
    lines = [
        "TalentBridge AI - Production Health Report",
        "===========================================",
        "",
        f"Status: {report['status']}",
        f"Checked At (UTC): {report['checked_at']}",
        f"Healthy Checks: {report['passed_count']} / {report['total_count']}",
        "",
        "Component Checks",
        "----------------",
    ]
    for check in report["checks"]:
        lines.append(
            f"- {check['component']}: {check['status']} — {check['detail']}"
        )
    lines.extend(["", "Privacy", "-------", report["privacy_note"]])
    return "\n".join(lines)


def record_monitoring_event(
    event_name,
    status,
    component,
    metrics=None,
    occurred_at=None,
):
    """Write a structured event containing only allow-listed numeric metrics."""
    clean_event = re.sub(r"[^a-z0-9_.-]", "_", str(event_name).lower())[:80]
    clean_status = re.sub(r"[^a-z0-9_.-]", "_", str(status).lower())[:40]
    clean_component = re.sub(r"[^a-z0-9_.-]", "_", str(component).lower())[:80]
    safe_metrics = {
        key: value
        for key, value in (metrics or {}).items()
        if key in SAFE_METRIC_FIELDS and isinstance(value, (int, float))
    }
    payload = {
        "timestamp": _utc_timestamp(occurred_at),
        "event": clean_event,
        "status": clean_status,
        "component": clean_component,
        "metrics": safe_metrics,
    }
    LOGGER.info(json.dumps(payload, sort_keys=True))
    return payload
