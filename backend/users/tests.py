from django.apps import apps
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()


def get_user_profile_model():
    return apps.get_model("users", "UserProfile")


class UserDeletionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.UserProfile = get_user_profile_model()

        # ensure profile exists
        self.profile, _ = self.UserProfile.objects.get_or_create(
            user=self.user,
            defaults={"age": 25, "gender": "M", "location": "UK"},
        )

    def test_user_deletion_via_api(self):
        """User DELETE request should delete the user account permanently"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/user-info/")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["message"], "Account deleted permanently")

    def test_cannot_delete_other_users(self):
        """Users cannot deactivate other accounts"""
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="otherpass123",
        )
        self.UserProfile.objects.get_or_create(
            user=other_user,
            defaults={"age": 30, "gender": "F", "location": "O"},
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/user/{other_user.id}/")
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_cannot_delete(self):
        """Unauthenticated users cannot deactivate accounts"""
        url = reverse("user-info")
        response = self.client.delete(url)
        self.assertIn(response.status_code, [401, 403])
