from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .test_admin import AdminTestBase


class AdminUserManagementTests(AdminTestBase):
    """Tests for admin user management actions."""

    def test_admin_can_delete_user(self):
        """Test that an admin can delete a user."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("admin_delete_user", kwargs={"user_id": self.member_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.member_user.pk)

    def test_list_all_users_admin(self):
        """Test that an admin can list all users."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("admin_list_users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [u["username"] for u in response.data]
        self.assertIn("coach", usernames)
        self.assertIn("member", usernames)

    def test_list_all_users_non_admin(self):
        """Test that non-admin users cannot list all users."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse("admin_list_users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_user(self):
        """Test deleting a nonexistent user returns 404."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("admin_delete_user", kwargs={"user_id": 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_admin_cannot_delete_user_coach(self):
        """Test that coaches cannot delete a user."""
        self.client.force_authenticate(user=self.coach_user)
        url = reverse("admin_delete_user", kwargs={"user_id": self.member_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_delete_user_member(self):
        """Test that members cannot delete a user."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse("admin_delete_user", kwargs={"user_id": self.coach_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
