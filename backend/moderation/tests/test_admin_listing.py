from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .test_admin import AdminTestBase

class AdminListingTests(AdminTestBase):
    """Tests for admin listing users and coaches."""

    def test_list_users_empty(self):
        """Test listing users when no users exist except admin."""
        User.objects.exclude(pk=self.admin_user.pk).delete()
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("admin_list_users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_coaches_filtered(self):
        """Test listing coaches with status filter."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("admin_list_coaches") + "?status=pending"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(c["status_approval"] == "pending" for c in response.data))

    def test_non_admin_cannot_list_users(self):
        """Test that non-admin users cannot list all users."""
        self.client.force_authenticate(user=self.coach_user)
        url = reverse("admin_list_users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
