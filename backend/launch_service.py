"""Deterministic, privacy-safe launch readiness checks for TalentBridge AI."""

from datetime import datetime, timezone


def _utc_timestamp(value=None):
    timestamp = value or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc).isoformat(timespec="seconds")


def _completion_gate(name, passed_count, total_count, ready_detail, blocked_detail):
    total = max(0, int(total_count or 0))
    passed = min(max(0, int(passed_count or 0)), total)
    ready = total > 0 and passed == total
    return {
        "gate": name,
        "status": "Ready" if ready else "Blocked",
        "evidence": f"{passed} / {total} completed",
        "detail": ready_detail if ready else blocked_detail,
    }


def build_launch_readiness_report(
    role_scenarios_passed,
    role_scenario_count,
    ui_checks_passed,
    ui_check_count,
    health_status,
    demo_checks_passed,
    demo_check_count,
    safety_reviewed=False,
    release_notes_reviewed=False,
    checked_at=None,
):
    """Evaluate the six evidence gates required for an MVP launch candidate."""
    gates = [
        _completion_gate(
            "Role workflow",
            role_scenarios_passed,
            role_scenario_count,
            "All role-specific beta scenarios passed.",
            "Complete every role-specific beta scenario.",
        ),
        _completion_gate(
            "Mobile and accessibility",
            ui_checks_passed,
            ui_check_count,
            "All interface checks passed.",
            "Complete every mobile and accessibility check.",
        ),
        {
            "gate": "Production health",
            "status": "Ready" if health_status == "Operational" else "Blocked",
            "evidence": str(health_status or "Not run"),
            "detail": (
                "The deployed runtime is operational."
                if health_status == "Operational"
                else "Run Production Health Check and resolve every failed check."
            ),
        },
        _completion_gate(
            "Public demo",
            demo_checks_passed,
            demo_check_count,
            "All recording-readiness checks passed.",
            "Complete every public-demo readiness check.",
        ),
        {
            "gate": "Safety and privacy",
            "status": "Ready" if bool(safety_reviewed) else "Blocked",
            "evidence": "Confirmed" if safety_reviewed else "Not confirmed",
            "detail": (
                "Safety, privacy, and evidence disclaimers were reviewed."
                if safety_reviewed
                else "Review and confirm the safety, privacy, and evidence disclaimers."
            ),
        },
        {
            "gate": "Release evidence",
            "status": "Ready" if bool(release_notes_reviewed) else "Blocked",
            "evidence": "Confirmed" if release_notes_reviewed else "Not confirmed",
            "detail": (
                "Release notes, test results, and demo instructions were reviewed."
                if release_notes_reviewed
                else "Review the release notes, test results, and demo instructions."
            ),
        },
    ]

    ready_count = sum(gate["status"] == "Ready" for gate in gates)
    total_count = len(gates)
    launch_ready = ready_count == total_count
    return {
        "status": "Ready to Launch" if launch_ready else "Launch Blocked",
        "checked_at": _utc_timestamp(checked_at),
        "ready_count": ready_count,
        "blocked_count": total_count - ready_count,
        "total_count": total_count,
        "gates": gates,
        "next_action": (
            "TalentBridge AI has passed every MVP launch gate."
            if launch_ready
            else "Complete the blocked gates before presenting this build as launch-ready."
        ),
        "privacy_note": (
            "This launch report records checklist status only. It does not include "
            "resume text, job descriptions, account details, or secret values."
        ),
        "disclaimer": (
            "Launch readiness confirms this MVP checklist only. It is not an "
            "independent security, accessibility, legal, or compliance certification."
        ),
    }


def generate_launch_readiness_text(report):
    """Create a portable launch-readiness report without private user inputs."""
    lines = [
        "TalentBridge AI - MVP Launch Readiness Report",
        "==============================================",
        "",
        f"Status: {report['status']}",
        f"Checked At (UTC): {report['checked_at']}",
        f"Ready Gates: {report['ready_count']} / {report['total_count']}",
        "",
        "Launch Gates",
        "------------",
    ]
    for gate in report["gates"]:
        lines.append(
            f"- {gate['gate']}: {gate['status']} — {gate['evidence']} — "
            f"{gate['detail']}"
        )
    lines.extend(
        [
            "",
            "Next Action",
            "-----------",
            report["next_action"],
            "",
            "Privacy",
            "-------",
            report["privacy_note"],
            "",
            "Important",
            "---------",
            report["disclaimer"],
        ]
    )
    return "\n".join(lines)
