from django.apps import apps
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()


def get_user_profile_model():
    return apps.get_model("users", "UserProfile")


class UserDeletionTests(TestCase):
    """Test delete-account endpoint"""

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
        self.client.force_login(user=self.user)
        url = reverse("delete-account")
        response = self.client.delete(
            url, data={"user_id": self.user.id}, format="json"
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["message"], "Account deleted permanently")

        # Verify user is deleted
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_unauthenticated_cannot_delete(self):
        """Unauthenticated users cannot delete accounts"""
        url = reverse("delete-account")
        response = self.client.delete(url)
        self.assertIn(response.status_code, [401, 403])

    def test_cannot_delete_other_users(self):
        """Users cannot delete other accounts"""
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="otherpass123",
        )
        self.UserProfile.objects.get_or_create(
            user=other_user,
            defaults={"age": 30, "gender": "F", "location": "O"},
        )

        self.client.force_login(user=self.user)
        url = reverse("delete-account")

        response = self.client.delete(
            url, data={"user_id": other_user.id}, format="json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn("You can only delete your own account", response.data["detail"])

        # Verify other user still exists
        self.assertTrue(User.objects.filter(id=other_user.id).exists())

    def test_delete_account_no_user_id(self):
        """Should return 400 if user_id is not provided"""
        self.client.force_login(self.user)
        url = reverse("delete-account")
        response = self.client.delete(url, {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["detail"], "User ID is required for account deletion."
        )

    def test_delete_account_profile_also_deleted(self):
        """Deleting user should also delete profile (cascade)"""
        self.client.force_login(self.user)
        url = reverse("delete-account")
        profile_id = self.profile.id

        response = self.client.delete(
            url, data={"user_id": self.user.id}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        # Profile should be deleted via cascade
        self.assertFalse(self.UserProfile.objects.filter(id=profile_id).exists())
