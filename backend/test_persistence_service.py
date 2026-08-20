import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from persistence_service import (
    PersistenceError,
    list_job_analyses,
    load_job_analysis,
    load_skill_progress,
    save_job_analysis,
    save_skill_progress,
)


class PersistenceServiceTests(unittest.TestCase):
    def test_save_job_analysis_returns_created_id(self):
        client = MagicMock()
        client.table.return_value.insert.return_value.execute.return_value = (
            SimpleNamespace(data=[{"id": "analysis-123"}])
        )
        result = {
            "user_mode": "Job Seeker",
            "semantic_match_score": 75,
            "job_comparison": {"match_score": 80},
        }

        analysis_id = save_job_analysis(client, "user-123", "Data Analyst", result)

        self.assertEqual(analysis_id, "analysis-123")
        payload = client.table.return_value.insert.call_args.args[0]
        self.assertEqual(payload["user_id"], "user-123")
        self.assertEqual(payload["match_score"], 80)

    def test_list_job_analyses_returns_rows(self):
        client = MagicMock()
        chain = client.table.return_value.select.return_value.eq.return_value
        chain.order.return_value.limit.return_value.execute.return_value = SimpleNamespace(
            data=[{"id": "analysis-123"}]
        )

        rows = list_job_analyses(client, "user-123")

        self.assertEqual(rows, [{"id": "analysis-123"}])

    def test_load_job_analysis_requires_existing_result(self):
        client = MagicMock()
        client.table.return_value.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data=None
        )

        with self.assertRaises(PersistenceError):
            load_job_analysis(client, "user-123", "missing")

    def test_save_skill_progress_validates_evidence_urls(self):
        with self.assertRaises(PersistenceError):
            save_skill_progress(
                MagicMock(),
                "user-123",
                "analysis-123",
                {"Python": "javascript:alert(1)"},
                {"Python": "Completed"},
            )

    def test_save_and_load_skill_progress(self):
        client = MagicMock()
        client.table.return_value.upsert.return_value.execute.return_value = SimpleNamespace(
            data=[]
        )

        save_skill_progress(
            client,
            "user-123",
            "analysis-123",
            {"Python": "https://github.com/example/python"},
            {"Python": "Completed"},
        )

        rows = client.table.return_value.upsert.call_args.args[0]
        self.assertEqual(rows[0]["status"], "Completed")

        client.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = SimpleNamespace(
            data=[
                {
                    "skill": "Python",
                    "evidence_url": "https://github.com/example/python",
                    "status": "Completed",
                }
            ]
        )
        progress = load_skill_progress(client, "user-123", "analysis-123")
        self.assertEqual(progress["Python"]["status"], "Completed")


if __name__ == "__main__":
    unittest.main()
