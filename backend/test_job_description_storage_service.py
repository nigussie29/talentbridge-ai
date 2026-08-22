import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from job_description_storage_service import (
    JobDescriptionStorageError,
    delete_job_description,
    list_job_descriptions,
    load_job_description,
    save_job_description,
    update_job_description,
)


class JobDescriptionStorageServiceTests(unittest.TestCase):
    def test_save_job_description_stores_private_owned_record(self):
        client = MagicMock()
        table = client.table.return_value
        table.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data=None
        )
        table.insert.return_value.execute.return_value = SimpleNamespace(
            data=[{"id": "job-123", "job_title": "Data Analyst"}]
        )

        saved = save_job_description(
            client,
            "user-123",
            "Data Analyst",
            "Example Company",
            "https://example.com/jobs/123",
            "Analyze data with Python and SQL.",
        )

        self.assertEqual(saved["id"], "job-123")
        self.assertFalse(saved["already_exists"])
        payload = table.insert.call_args.args[0]
        self.assertEqual(payload["user_id"], "user-123")
        self.assertEqual(payload["job_title"], "Data Analyst")
        self.assertEqual(len(payload["content_sha256"]), 64)

    def test_save_job_description_returns_existing_duplicate(self):
        client = MagicMock()
        client.table.return_value.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data={"id": "existing", "job_title": "Data Analyst"}
        )

        saved = save_job_description(
            client,
            "user-123",
            "Data Analyst",
            "",
            "",
            "Analyze data with Python and SQL.",
        )

        self.assertTrue(saved["already_exists"])
        client.table.return_value.insert.assert_not_called()

    def test_save_job_description_validates_title_text_and_url(self):
        with self.assertRaises(JobDescriptionStorageError):
            save_job_description(
                MagicMock(),
                "user-123",
                "",
                "",
                "",
                "Python SQL",
            )
        with self.assertRaises(JobDescriptionStorageError):
            save_job_description(
                MagicMock(),
                "user-123",
                "Data Analyst",
                "",
                "javascript:alert(1)",
                "Python SQL",
            )

    def test_list_job_descriptions_returns_owned_rows(self):
        client = MagicMock()
        chain = client.table.return_value.select.return_value.eq.return_value
        chain.order.return_value.limit.return_value.execute.return_value = SimpleNamespace(
            data=[{"id": "job-123", "job_title": "Data Analyst"}]
        )

        rows = list_job_descriptions(client, "user-123")

        self.assertEqual(rows[0]["id"], "job-123")
        client.table.return_value.select.return_value.eq.assert_called_once_with(
            "user_id",
            "user-123",
        )

    def test_load_job_description_filters_by_owner_and_id(self):
        client = MagicMock()
        lookup = client.table.return_value.select.return_value.eq.return_value
        lookup.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data={
                "id": "job-123",
                "job_title": "Data Analyst",
                "description_text": "Python and SQL are required.",
            }
        )

        record = load_job_description(client, "user-123", "job-123")

        self.assertEqual(record["job_title"], "Data Analyst")
        lookup.eq.assert_called_once_with("id", "job-123")

    def test_update_job_description_filters_by_owner_and_id(self):
        client = MagicMock()
        update_chain = client.table.return_value.update.return_value.eq.return_value
        update_chain.eq.return_value.execute.return_value = SimpleNamespace(
            data=[{"id": "job-123", "job_title": "Senior Data Analyst"}]
        )

        updated = update_job_description(
            client,
            "user-123",
            "job-123",
            "Senior Data Analyst",
            "Example Company",
            "",
            "Lead reporting with Power BI and SQL.",
        )

        self.assertEqual(updated["job_title"], "Senior Data Analyst")
        client.table.return_value.update.return_value.eq.assert_called_once_with(
            "user_id",
            "user-123",
        )
        update_chain.eq.assert_called_once_with("id", "job-123")

    def test_delete_job_description_rejects_missing_or_foreign_record(self):
        client = MagicMock()
        delete_chain = client.table.return_value.delete.return_value.eq.return_value
        delete_chain.eq.return_value.execute.return_value = SimpleNamespace(data=[])

        with self.assertRaises(JobDescriptionStorageError):
            delete_job_description(client, "user-123", "foreign-job")


if __name__ == "__main__":
    unittest.main()
