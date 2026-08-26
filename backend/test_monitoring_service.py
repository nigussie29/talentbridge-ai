import unittest
from datetime import datetime, timezone

from monitoring_service import (
    build_health_report,
    generate_health_report_text,
    record_monitoring_event,
)


class MonitoringServiceTests(unittest.TestCase):
    def test_health_report_is_operational_when_all_checks_pass(self):
        report = build_health_report(
            {
                "supabase_url_configured": True,
                "supabase_key_configured": True,
            },
            module_checker=lambda _name: True,
            checked_at=datetime(2026, 8, 26, 12, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(report["status"], "Operational")
        self.assertEqual(report["passed_count"], report["total_count"])
        self.assertEqual(report["failed_count"], 0)
        self.assertEqual(len(report["checks"]), 7)

    def test_health_report_identifies_missing_dependency_and_configuration(self):
        report = build_health_report(
            {
                "supabase_url_configured": True,
                "supabase_key_configured": False,
            },
            module_checker=lambda name: name != "PyPDF2",
        )

        self.assertEqual(report["status"], "Degraded")
        self.assertEqual(report["failed_count"], 2)
        problem_components = {
            check["component"]
            for check in report["checks"]
            if check["status"] == "Needs attention"
        }
        self.assertEqual(
            problem_components,
            {"PDF processing", "Supabase configuration"},
        )

    def test_health_report_never_contains_secret_values(self):
        secret_url = "https://private-project.example"
        secret_key = "private-secret-key"
        report = build_health_report(
            {
                "supabase_url_configured": bool(secret_url),
                "supabase_key_configured": bool(secret_key),
            },
            module_checker=lambda _name: True,
        )
        report_text = generate_health_report_text(report)

        self.assertNotIn(secret_url, report_text)
        self.assertNotIn(secret_key, report_text)
        self.assertIn("does not inspect or record", report_text)

    def test_monitoring_event_keeps_only_safe_numeric_metrics(self):
        payload = record_monitoring_event(
            "Health Check",
            "Operational",
            "Production Health",
            {
                "check_count": 7,
                "passed_count": 7,
                "email": "person@example.com",
                "resume_text": "private résumé content",
                "failed_count": "zero",
            },
            occurred_at=datetime(2026, 8, 26, 12, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(payload["event"], "health_check")
        self.assertEqual(
            payload["metrics"],
            {"check_count": 7, "passed_count": 7},
        )
        self.assertNotIn("person@example.com", str(payload))
        self.assertNotIn("private résumé content", str(payload))


if __name__ == "__main__":
    unittest.main()
