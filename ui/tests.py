import hashlib
import hmac

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .views import _normalize_github_repository


class UIAuthenticationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.password = "TestPass123!"
        self.user = user_model.objects.create_user(
            username="etudiant1",
            email="etudiant1@example.com",
            password=self.password,
        )
        self.login_url = reverse("ui:login")
        self.oauth_login_url = reverse("ui:oauth_email_login")

    @staticmethod
    def _oauth_sig(email, ts, secret):
        payload = f"{email}:{ts}".encode("utf-8")
        return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()

    def test_login_accepts_email_identifier(self):
        response = self.client.post(
            self.login_url,
            {"username": self.user.email, "password": self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(self.user.id), self.client.session.get("_auth_user_id"))

    @override_settings(
        OAUTH_EMAIL_AUTOLOGIN_SECRET="oauth-secret-test",
        OAUTH_EMAIL_MAX_AGE_SECONDS=300,
    )
    def test_oauth_autologin_logs_in_matching_email(self):
        ts = int(timezone.now().timestamp())
        sig = self._oauth_sig(self.user.email, ts, "oauth-secret-test")

        response = self.client.get(
            self.oauth_login_url,
            {"email": self.user.email, "ts": ts, "sig": sig},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(self.user.id), self.client.session.get("_auth_user_id"))

    @override_settings(
        OAUTH_EMAIL_AUTOLOGIN_SECRET="oauth-secret-test",
        OAUTH_EMAIL_MAX_AGE_SECONDS=300,
    )
    def test_oauth_autologin_rejects_invalid_signature(self):
        ts = int(timezone.now().timestamp())

        response = self.client.get(
            self.oauth_login_url,
            {"email": self.user.email, "ts": ts, "sig": "invalid"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.client.session.get("_auth_user_id"))

    @override_settings(
        OAUTH_EMAIL_AUTOLOGIN_SECRET="oauth-secret-test",
        OAUTH_EMAIL_MAX_AGE_SECONDS=60,
    )
    def test_oauth_autologin_rejects_expired_link(self):
        ts = int(timezone.now().timestamp()) - 3600
        sig = self._oauth_sig(self.user.email, ts, "oauth-secret-test")

        response = self.client.get(
            self.oauth_login_url,
            {"email": self.user.email, "ts": ts, "sig": sig},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.client.session.get("_auth_user_id"))


class GitHubRepositoryNormalizationTests(TestCase):
    def test_normalize_https_url(self):
        repo = _normalize_github_repository(
            "https://github.com/karkouri001/exam-java-somme-pairs-tests.git"
        )
        self.assertEqual(repo, "karkouri001/exam-java-somme-pairs-tests")

    def test_normalize_ssh_url(self):
        repo = _normalize_github_repository(
            "git@github.com:karkouri001/exam-java-somme-pairs-tests.git"
        )
        self.assertEqual(repo, "karkouri001/exam-java-somme-pairs-tests")

    def test_keep_owner_repo_value(self):
        repo = _normalize_github_repository("karkouri001/exam-java-somme-pairs-tests")
        self.assertEqual(repo, "karkouri001/exam-java-somme-pairs-tests")
