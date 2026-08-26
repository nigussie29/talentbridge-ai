import unittest
from datetime import datetime, timezone

from launch_service import (
    build_launch_readiness_report,
    generate_launch_readiness_text,
)


class LaunchServiceTests(unittest.TestCase):
    def build_report(self, **overrides):
        values = {
            "role_scenarios_passed": 3,
            "role_scenario_count": 3,
            "ui_checks_passed": 5,
            "ui_check_count": 5,
            "health_status": "Operational",
            "demo_checks_passed": 5,
            "demo_check_count": 5,
            "safety_reviewed": True,
            "release_notes_reviewed": True,
            "checked_at": datetime(2026, 8, 26, 12, 0, tzinfo=timezone.utc),
        }
        values.update(overrides)
        return build_launch_readiness_report(**values)

    def test_all_six_gates_produce_ready_to_launch(self):
        report = self.build_report()

        self.assertEqual(report["status"], "Ready to Launch")
        self.assertEqual(report["ready_count"], 6)
        self.assertEqual(report["blocked_count"], 0)
        self.assertEqual(len(report["gates"]), 6)

    def test_failed_health_and_incomplete_checks_block_launch(self):
        report = self.build_report(
            ui_checks_passed=4,
            health_status="Degraded",
            safety_reviewed=False,
        )

        self.assertEqual(report["status"], "Launch Blocked")
        self.assertEqual(report["blocked_count"], 3)
        blocked = {
            gate["gate"] for gate in report["gates"] if gate["status"] == "Blocked"
        }
        self.assertEqual(
            blocked,
            {"Mobile and accessibility", "Production health", "Safety and privacy"},
        )

    def test_empty_checklist_does_not_pass(self):
        report = self.build_report(
            role_scenarios_passed=0,
            role_scenario_count=0,
        )

        role_gate = report["gates"][0]
        self.assertEqual(role_gate["status"], "Blocked")

    def test_download_text_contains_status_privacy_and_disclaimer(self):
        report_text = generate_launch_readiness_text(self.build_report())

        self.assertIn("Ready to Launch", report_text)
        self.assertIn("Role workflow: Ready", report_text)
        self.assertIn("does not include resume text", report_text)
        self.assertIn("not an independent security", report_text)


if __name__ == "__main__":
    unittest.main()
