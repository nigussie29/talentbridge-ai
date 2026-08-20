import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from resume_storage_service import (
    MAX_RESUME_BYTES,
    ResumeStorageError,
    delete_resume,
    list_resumes,
    load_resume,
    save_resume,
)


class ResumeStorageServiceTests(unittest.TestCase):
    def test_save_resume_uploads_private_pdf_and_metadata(self):
        client = MagicMock()
        table = client.table.return_value
        table.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data=None
        )
        table.insert.return_value.execute.return_value = SimpleNamespace(
            data=[{"id": "resume-123", "original_name": "My-Resume.pdf"}]
        )

        saved = save_resume(
            client,
            "user-123",
            "My Resume.pdf",
            b"%PDF-1.4\nprivate resume",
        )

        self.assertEqual(saved["id"], "resume-123")
        self.assertFalse(saved["already_exists"])
        upload = client.storage.from_.return_value.upload
        self.assertTrue(upload.call_args.kwargs["path"].startswith("user-123/"))
        self.assertEqual(
            upload.call_args.kwargs["file_options"]["content-type"],
            "application/pdf",
        )
        payload = table.insert.call_args.args[0]
        self.assertEqual(payload["user_id"], "user-123")
        self.assertEqual(payload["original_name"], "My-Resume.pdf")

    def test_save_resume_returns_existing_duplicate_without_upload(self):
        client = MagicMock()
        client.table.return_value.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data={"id": "existing", "original_name": "resume.pdf"}
        )

        saved = save_resume(client, "user-123", "resume.pdf", b"%PDF-1.4\ncontent")

        self.assertTrue(saved["already_exists"])
        client.storage.from_.assert_not_called()

    def test_save_resume_rejects_non_pdf_and_oversized_files(self):
        with self.assertRaises(ResumeStorageError):
            save_resume(MagicMock(), "user-123", "resume.txt", b"not a pdf")
        with self.assertRaises(ResumeStorageError):
            save_resume(
                MagicMock(),
                "user-123",
                "resume.pdf",
                b"%PDF-" + b"x" * MAX_RESUME_BYTES,
            )

    def test_save_resume_removes_object_when_metadata_insert_fails(self):
        client = MagicMock()
        table = client.table.return_value
        table.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data=None
        )
        table.insert.return_value.execute.side_effect = RuntimeError("database down")

        with self.assertRaises(ResumeStorageError):
            save_resume(client, "user-123", "resume.pdf", b"%PDF-1.4\ncontent")

        client.storage.from_.return_value.remove.assert_called_once()

    def test_list_resumes_returns_private_metadata(self):
        client = MagicMock()
        chain = client.table.return_value.select.return_value.eq.return_value
        chain.order.return_value.limit.return_value.execute.return_value = SimpleNamespace(
            data=[{"id": "resume-123", "original_name": "resume.pdf"}]
        )

        rows = list_resumes(client, "user-123")

        self.assertEqual(rows[0]["id"], "resume-123")

    def test_load_resume_checks_owner_metadata_before_download(self):
        client = MagicMock()
        client.table.return_value.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data={
                "id": "resume-123",
                "original_name": "resume.pdf",
                "storage_path": "user-123/resume.pdf",
            }
        )
        client.storage.from_.return_value.download.return_value = b"%PDF-1.4\ncontent"

        record, file_bytes = load_resume(client, "user-123", "resume-123")

        self.assertEqual(record["original_name"], "resume.pdf")
        self.assertTrue(file_bytes.startswith(b"%PDF-"))
        client.storage.from_.return_value.download.assert_called_once_with(
            "user-123/resume.pdf"
        )

    def test_delete_resume_removes_owned_file_and_metadata(self):
        client = MagicMock()
        select_chain = client.table.return_value.select.return_value.eq.return_value
        select_chain.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data={"id": "resume-123", "storage_path": "user-123/resume.pdf"}
        )
        delete_chain = client.table.return_value.delete.return_value.eq.return_value
        delete_chain.eq.return_value.execute.return_value = SimpleNamespace(
            data=[{"id": "resume-123"}]
        )

        delete_resume(client, "user-123", "resume-123")

        client.storage.from_.return_value.remove.assert_called_once_with(
            ["user-123/resume.pdf"]
        )
        delete_chain.eq.assert_called_once_with("id", "resume-123")

    def test_delete_resume_does_not_touch_foreign_or_invalid_path(self):
        client = MagicMock()
        lookup = client.table.return_value.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute
        lookup.return_value = SimpleNamespace(data=None)

        with self.assertRaises(ResumeStorageError):
            delete_resume(client, "user-123", "foreign-resume")
        client.storage.from_.assert_not_called()

        lookup.return_value = SimpleNamespace(
            data={"id": "resume-123", "storage_path": "other-user/resume.pdf"}
        )
        with self.assertRaises(ResumeStorageError):
            delete_resume(client, "user-123", "resume-123")
        client.storage.from_.assert_not_called()


if __name__ == "__main__":
    unittest.main()
