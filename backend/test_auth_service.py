import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from auth_service import (
    AuthenticationError,
    authenticate_user,
    register_job_seeker,
    sign_out_user,
)


class AuthServiceTests(unittest.TestCase):
    def test_authenticate_user_returns_database_role(self):
        client = MagicMock()
        client.auth.sign_in_with_password.return_value = SimpleNamespace(
            user=SimpleNamespace(id="user-123", email="person@example.com"),
            session=SimpleNamespace(access_token="token"),
        )
        client.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data={"display_name": "Test Person", "role": "HR / Recruiter"}
        )

        user = authenticate_user(client, " Person@Example.com ", "safe-password")

        self.assertEqual(user.user_id, "user-123")
        self.assertEqual(user.email, "person@example.com")
        self.assertEqual(user.display_name, "Test Person")
        self.assertEqual(user.role, "HR / Recruiter")
        client.auth.sign_in_with_password.assert_called_once_with(
            {"email": "person@example.com", "password": "safe-password"}
        )

    def test_authenticate_user_rejects_unknown_database_role(self):
        client = MagicMock()
        client.auth.sign_in_with_password.return_value = SimpleNamespace(
            user=SimpleNamespace(id="user-123", email="person@example.com"),
            session=SimpleNamespace(access_token="token"),
        )
        client.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = SimpleNamespace(
            data={"display_name": "Test Person", "role": "Superuser"}
        )

        user = authenticate_user(client, "person@example.com", "safe-password")

        self.assertEqual(user.role, "Job Seeker")

    def test_register_job_seeker_requires_strong_enough_password(self):
        with self.assertRaises(AuthenticationError):
            register_job_seeker(MagicMock(), "person@example.com", "short", "Person")

    def test_register_job_seeker_reports_confirmation_requirement(self):
        client = MagicMock()
        client.auth.sign_up.return_value = SimpleNamespace(
            user=SimpleNamespace(id="user-123"),
            session=None,
        )

        signed_in = register_job_seeker(
            client,
            "person@example.com",
            "safe-password",
            "Test Person",
        )

        self.assertFalse(signed_in)
        client.auth.sign_up.assert_called_once()

    def test_sign_out_uses_supabase_auth(self):
        client = MagicMock()

        sign_out_user(client)

        client.auth.sign_out.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
